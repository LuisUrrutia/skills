import contextlib
import email.message
import importlib.util
import io
from pathlib import Path
import time
import unittest
from unittest import mock
import urllib.error


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "search-domains.py"
spec = importlib.util.spec_from_file_location("search_domains", SCRIPT)
search_domains = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_domains)

IDENTITY_DIGITAL_NOT_FOUND = """Domain not found.
>>> Last update of WHOIS database: 2026-10-24T09:35:52Z <<<

Terms of Use: Access to WHOIS information is provided to assist persons. The Whois service may be scheduled for
downtime during production or OT&E maintenance periods. Queries to the Whois services are throttled. If too many
queries are received from a single IP address within a specified time, the service will begin to reject further
queries, and access is limited by detecting and limiting bulk query access from single sources.
"""


def items_for(names, tlds):
    return search_domains.targets(names, tlds)


def http_error(code, body=b"", headers=None):
    message = email.message.Message()
    for key, value in (headers or {}).items():
        message[key] = value
    return urllib.error.HTTPError("https://rdap.example/domain/acme.com", code, "status", message, io.BytesIO(body))


def fetch_raising(error):
    def fetch(url, **options):
        raise error
    return fetch


def fetch_returning(body):
    return lambda url, **options: body


class TargetsTest(unittest.TestCase):
    def test_label_expands_across_tlds_and_full_domain_stays_exact(self):
        items = items_for(["Acme", "acme.com.mx"], ["com", "io"])

        self.assertEqual([item["domain"] for item in items], ["acme.com", "acme.io", "acme.com.mx"])
        self.assertEqual(items[2]["tld"], "com.mx")

    def test_invalid_label_is_rejected(self):
        with self.assertRaises(ValueError):
            items_for(["-acme"], ["com"])

    def test_unicode_tld_is_encoded_like_a_name(self):
        self.assertEqual(search_domains.normalize(".ελ"), "xn--qxam")


class CatalogTest(unittest.TestCase):
    def test_keeps_dns_root_tlds_and_icann_second_levels_only(self):
        prices = {"com": {}, "com.mx": {}, "co.uk": {}, "br.com": {}, "com.de": {},
                  "0z": {"specialType": "handshake"}}

        tlds = search_domains.catalog_tlds(prices, {"com.mx", "co.uk"})

        self.assertEqual(tlds, ["com", "com.mx", "co.uk"])


class RanksTest(unittest.TestCase):
    def test_ranks_single_labels_and_requested_second_levels_by_count(self):
        counts = {"com": 100, "uk": 30, "co.uk": 20, "github.io": 50, "io": 40}

        ranks = search_domains.tld_ranks(counts, {"co.uk"})

        self.assertEqual(ranks, {"com": 1, "io": 2, "uk": 3, "co.uk": 4})


class WhoisTest(unittest.TestCase):
    def test_classifies_registry_answers_from_their_head(self):
        cases = {
            "Domain: zzqx.de\nStatus: free\n": "available",
            "The queried object does not exist: DOMAIN NOT FOUND\n": "available",
            "No_Se_Encontro_El_Objeto/Object_Not_Found\n": "available",
            "No Found\n": "available",
            "% EURid terms that limit the use of WHOIS\n%\nDomain: zzqx.eu\nScript: LATIN\n\nStatus: AVAILABLE\n":
                "available",
            IDENTITY_DIGITAL_NOT_FOUND: "available",
            "Domain Name: google.io\nRegistry Domain ID: REDACTED\nRegistrar: MarkMonitor\n": "taken",
            "Domain: google.de\nNserver: ns1.google.com\nStatus: connect\n": "taken",
            "Domain Name: google.tw\n   Record created on 2005-10-27\n": "taken",
            "Quota exceeded; try again later. No data found.\n": "throttled",
            "Error: backend database not found\n": None,
            "Notice: the WHOIS service has been retired. Domain not found.\n": None,
            "TLD is not supported.\n": None,
        }
        for text, expected in cases.items():
            with self.subTest(text=text[:40]):
                self.assertEqual(search_domains.classify_whois(text)[0], expected)

    def test_reads_empty_iana_whois_field_as_no_server(self):
        text = "domain:       LIVE\nwhois:        \n\nstatus:       ACTIVE\n"

        self.assertEqual(search_domains.WHOIS_SERVER.search(text).group(1), "")


class RdapTest(unittest.TestCase):
    def lookup(self, fetch):
        return search_domains.rdap_lookup("acme.com", "https://rdap.example/", fetch=fetch)

    def test_needs_an_rdap_answer_for_a_verdict(self):
        cases = [
            (fetch_returning(b'{"objectClassName": "domain", "ldhName": "acme.com"}'), "taken"),
            (fetch_returning(b"<html>maintenance</html>"), None),
            (fetch_raising(http_error(404)), "available"),
            (fetch_raising(http_error(404, b'{"errorCode": 404, "title": "Not Found"}')), "available"),
            (fetch_raising(http_error(404, b"<html>no route</html>")), None),
            (fetch_raising(http_error(503)), None),
        ]
        for fetch, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(self.lookup(fetch)[0], expected)

    def test_rate_limit_raises_with_its_retry_after(self):
        with self.assertRaises(search_domains.Throttled) as raised:
            self.lookup(fetch_raising(http_error(429, headers={"Retry-After": "86284"})))

        self.assertEqual(raised.exception.retry_after, 86284)


class RetryAfterTest(unittest.TestCase):
    def test_reads_seconds_and_describes_long_waits(self):
        self.assertEqual(search_domains.retry_after("86284"), 86284)
        self.assertIsNone(search_domains.retry_after(None))
        self.assertEqual(search_domains.describe_wait(86284), ", retry after 23h58m")


class RegistriesTest(unittest.TestCase):
    def test_throttled_host_is_skipped_for_the_rest_of_the_run(self):
        registries = search_domains.Registries({}, interval=0)
        sent = []

        def throttled():
            sent.append("query")
            raise search_domains.Throttled(3600)

        first = registries.lookup("rdap.example", throttled)
        second = registries.lookup("rdap.example", throttled)

        self.assertIsNone(first[0])
        self.assertIn("rdap.example throttled", second[1])
        self.assertEqual(sent, ["query"])

    def test_query_waiting_for_its_slot_is_dropped_when_the_host_got_throttled_meanwhile(self):
        registries = search_domains.Registries({}, interval=0)
        registries.wait = lambda host: registries.cooldowns.update({host: time.time() + 3600})
        sent = []

        status, note = registries.lookup("rdap.example", lambda: sent.append("query"))

        self.assertEqual(sent, [])
        self.assertIsNone(status)
        self.assertIn("throttled", note)

    def test_cooldown_from_an_earlier_run_still_applies_until_it_expires(self):
        registries = search_domains.Registries({}, cooldowns={"live.example": time.time() + 600,
                                                               "old.example": time.time() - 1}, interval=0)

        self.assertIsNone(registries.lookup("live.example", lambda: ("available", "RDAP: no record"))[0])
        self.assertEqual(registries.lookup("old.example", lambda: ("available", "RDAP: no record"))[0], "available")

    def test_short_throttle_is_retried_once(self):
        registries = search_domains.Registries({}, interval=0)
        answers = [search_domains.Throttled(0), ("available", "RDAP: no record")]

        def query():
            answer = answers.pop(0)
            if isinstance(answer, Exception):
                raise answer
            return answer

        self.assertEqual(registries.lookup("rdap.example", query), ("available", "RDAP: no record"))

    def test_iana_failure_is_not_cached_as_a_missing_server(self):
        registries = search_domains.Registries({}, interval=0)

        server = registries.whois_server("cl", query=lambda host, key: "Query rate limit exceeded\n")

        self.assertIsNone(server)
        self.assertEqual(registries.whois_servers, {})

    def test_iana_record_without_whois_is_cached_as_no_server(self):
        registries = search_domains.Registries({}, interval=0)

        server = registries.whois_server("live", query=lambda host, key: "domain:       LIVE\nwhois:        \n")

        self.assertEqual(server, "")
        self.assertEqual(registries.whois_servers["live"][0], "")

    def test_throttled_rdap_falls_back_to_whois(self):
        registries = search_domains.Registries({"ai": "https://rdap.example/"},
                                               {"ai": ["whois.example", time.time()]},
                                               {"rdap.example": time.time() + 600}, interval=0)

        with mock.patch.object(search_domains, "whois_lookup", return_value=("available", "WHOIS: no record")):
            self.assertEqual(registries.check("acme.ai", "ai"), ("available", "WHOIS: no record"))


class SearchTest(unittest.TestCase):
    def test_delegated_domains_skip_the_registry_and_failed_checks_stay_unconfirmed(self):
        items = items_for(["acme"], ["com", "io", "dev"])
        dns = {"acme.com": "NOERROR", "acme.io": "NXDOMAIN", "acme.dev": "NXDOMAIN"}
        verdicts = {"acme.io": (None, "rdap.example throttled"), "acme.dev": ("available", "RDAP: no record")}
        asked = []

        def registry(domain, tld):
            asked.append(domain)
            return verdicts[domain]

        search_domains.search(items, dns=dns.get, registry=registry, ranks={})

        self.assertEqual(sorted(asked), ["acme.dev", "acme.io"])
        self.assertEqual({item["domain"]: item["status"] for item in items},
                         {"acme.com": "taken", "acme.io": "unconfirmed", "acme.dev": "available"})

    def test_limit_checks_named_tlds_and_the_most_popular_undelegated_ones_per_name(self):
        items = items_for(["acme", "zeta"], ["xyz", "io", "com", "rare", "cl"])
        ranks = {"com": 1, "io": 2, "xyz": 3}
        asked = []

        def registry(domain, tld):
            asked.append(domain)
            return "available", "RDAP: no record"

        search_domains.search(items, dns=lambda domain: "NXDOMAIN", registry=registry, ranks=ranks, limit=2,
                              always={"cl"})

        self.assertEqual(sorted(asked), ["acme.cl", "acme.com", "acme.io", "zeta.cl", "zeta.com", "zeta.io"])
        unchecked = sorted(item["domain"] for item in items if item["status"] == "unchecked")
        self.assertEqual(unchecked, ["acme.rare", "acme.xyz", "zeta.rare", "zeta.xyz"])

    def test_a_failing_lookup_does_not_abort_the_other_domains(self):
        items = items_for(["acme"], ["com", "io"])

        def registry(domain, tld):
            if tld == "io":
                raise ValueError("malformed answer")
            return "available", "RDAP: no record"

        search_domains.search(items, dns=lambda domain: "NXDOMAIN", registry=registry, ranks={})

        self.assertEqual([item["status"] for item in items], ["available", "unconfirmed"])
        self.assertIn("malformed answer", items[1]["evidence"])


class RenderTest(unittest.TestCase):
    def row(self, tld, status, rank, price, evidence, dns="NXDOMAIN"):
        return {"domain": f"acme.{tld}", "name": "acme", "tld": tld, "status": status, "rank": rank,
                "price": price, "evidence": evidence, "dns": dns}

    def test_every_domain_bullet_carries_its_price_or_a_comparison_link(self):
        rows = [
            self.row("com", "taken", 1, {"registration": "11.08", "renewal": "11.08"}, "DNS delegation", "NOERROR"),
            self.row("io", "available", 14, {"registration": "28.12", "renewal": "51.80"}, "WHOIS: no record"),
            self.row("cl", "available", None, None, "RDAP: no record"),
        ]

        output = search_domains.render_markdown(rows, all_mode=False, footer=[])

        bullets = [line for line in output.splitlines() if line.startswith("- ")]
        self.assertEqual(bullets, [
            "- **acme.com**: taken, $11.08 first year, $11.08 renewal (TLD #1; DNS delegation)",
            "- **acme.io**: available, $28.12 first year, $51.80 renewal (TLD #14; WHOIS: no record)",
            "- **acme.cl**: available, no Porkbun price, compare at https://tld-list.com/tld/cl "
            "(TLD unranked; RDAP: no record)",
        ])

    def test_all_mode_lists_unchecked_undelegated_tlds_with_prices(self):
        rows = [
            self.row("com", "taken", 1, {"registration": "11.08", "renewal": "11.08"}, "DNS delegation", "NOERROR"),
            self.row("io", "available", 14, {"registration": "28.12", "renewal": "51.80"}, "WHOIS: no record"),
            self.row("xyz", "unchecked", 18, {"registration": "2.04", "renewal": "14.21"}, "not checked"),
            self.row("top", "unchecked", 21, {"registration": "1.63", "renewal": "4.63"}, "not checked"),
        ]

        output = search_domains.render_markdown(rows, all_mode=True, footer=[])

        self.assertNotIn("acme.com", output)
        self.assertIn("most popular first (first year/renewal): .xyz $2.04/$14.21 · .top $1.63/$4.63", output)
        self.assertIn("Taken: 1. Not checked with the registry: 2;", output)


class CommandLineTest(unittest.TestCase):
    def test_rejects_a_non_positive_limit_and_an_invalid_name_before_any_lookup(self):
        for argv in (["acme", "--all", "--limit", "0"], ["ac_me"], ["acme", "--tlds", "c_m"]):
            with self.subTest(argv=argv), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    search_domains.main(argv)
                self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
