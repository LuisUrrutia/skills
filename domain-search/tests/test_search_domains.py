import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "search-domains.py"
spec = importlib.util.spec_from_file_location("search_domains", SCRIPT)
search_domains = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_domains)


def items_for(names, tlds):
    return search_domains.targets(names, tlds)


class TargetsTest(unittest.TestCase):
    def test_label_expands_across_tlds_and_full_domain_stays_exact(self):
        items = items_for(["Acme", "acme.com.mx"], ["com", "io"])

        self.assertEqual([item["domain"] for item in items], ["acme.com", "acme.io", "acme.com.mx"])
        self.assertEqual(items[2]["tld"], "com.mx")

    def test_invalid_label_is_rejected(self):
        with self.assertRaises(ValueError):
            items_for(["-acme"], ["com"])


class CatalogTest(unittest.TestCase):
    def test_keeps_dns_root_tlds_and_cctld_second_levels_only(self):
        prices = {"com": {}, "com.mx": {}, "co.uk": {}, "br.com": {}, "uk.net": {}, "0z": {"specialType": "handshake"}}

        self.assertEqual(search_domains.catalog_tlds(prices), ["com", "com.mx", "co.uk"])


class RanksTest(unittest.TestCase):
    def test_ranks_single_labels_and_requested_second_levels_by_count(self):
        counts = {"com": 100, "uk": 30, "co.uk": 20, "github.io": 50, "io": 40}

        ranks = search_domains.tld_ranks(counts, {"co.uk"})

        self.assertEqual(ranks, {"com": 1, "io": 2, "uk": 3, "co.uk": 4})


class WhoisTest(unittest.TestCase):
    def test_classifies_registry_answers(self):
        cases = {
            "Domain: zzqx.de\nStatus: free\n": "available",
            "The queried object does not exist: DOMAIN NOT FOUND\n": "available",
            "No_Se_Encontro_El_Objeto/Object_Not_Found\n": "available",
            "No Found\n": "available",
            "Domain Name: google.io\nRegistrar WHOIS Server: whois.markmonitor.com\nRegistrar: MarkMonitor\n": "taken",
            "Domain: google.de\nNserver: ns1.google.com\nStatus: connect\n": "taken",
            "Domain Name: google.tw\n   Record created on 2005-10-27\n": "taken",
            "Notice: the WHOIS service has been retired.\n": None,
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(search_domains.classify_whois(text)[0], expected)

    def test_reads_empty_iana_whois_field_as_no_server(self):
        text = "domain:       LIVE\nwhois:        \n\nstatus:       ACTIVE\n"

        self.assertEqual(search_domains.WHOIS_SERVER.search(text).group(1), "")


class RetryAfterTest(unittest.TestCase):
    def test_reads_seconds_and_describes_long_waits(self):
        self.assertEqual(search_domains.retry_after("86284"), 86284)
        self.assertIsNone(search_domains.retry_after(None))
        self.assertEqual(search_domains.describe_wait(86284), ", retry after 23h58m")


class RegistriesTest(unittest.TestCase):
    def test_throttled_host_is_skipped_for_the_rest_of_the_run(self):
        registries = search_domains.Registries({}, {}, interval=0)
        calls = []

        def throttled():
            calls.append("query")
            raise search_domains.Throttled(3600)

        first = registries.lookup("rdap.example", throttled)
        second = registries.lookup("rdap.example", throttled)

        self.assertEqual(first, (None, "rdap.example throttled, retry after 1h00m"))
        self.assertEqual(second, first)
        self.assertEqual(calls, ["query"])

    def test_short_throttle_is_retried_once(self):
        registries = search_domains.Registries({}, {}, interval=0)
        answers = [search_domains.Throttled(0), ("available", "RDAP: no record")]

        def query():
            answer = answers.pop(0)
            if isinstance(answer, Exception):
                raise answer
            return answer

        self.assertEqual(registries.lookup("rdap.example", query), ("available", "RDAP: no record"))


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

    def test_limit_checks_the_most_popular_undelegated_tlds_per_name(self):
        items = items_for(["acme", "zeta"], ["xyz", "io", "com", "rare"])
        ranks = {"com": 1, "io": 2, "xyz": 3}
        asked = []

        def registry(domain, tld):
            asked.append(domain)
            return "available", "RDAP: no record"

        search_domains.search(items, dns=lambda domain: "NXDOMAIN", registry=registry, ranks=ranks, limit=2)

        self.assertEqual(sorted(asked), ["acme.com", "acme.io", "zeta.com", "zeta.io"])
        unchecked = sorted(item["domain"] for item in items if item["status"] == "unchecked")
        self.assertEqual(unchecked, ["acme.rare", "acme.xyz", "zeta.rare", "zeta.xyz"])


if __name__ == "__main__":
    unittest.main()
