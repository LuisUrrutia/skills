#!/usr/bin/env python3
"""Check domain availability with each TLD's registry, priced from Porkbun and ranked by Tranco TLD popularity."""

import argparse
import concurrent.futures
import csv
import datetime
import email.utils
import http.client
import io
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile


DEFAULT_TLDS = ("com", "ai", "app", "io", "dev")
# ccTLDs the user wants in every --all search although Porkbun does not sell them.
ALL_EXTRA_TLDS = ("cl", "es")
DEFAULT_LIMIT = 30
# Registry minimum terms; without them a price line understates what the first purchase costs.
MIN_YEARS = {"ai": 2}
PORKBUN_PRICING = "https://api.porkbun.com/api/json/v3/pricing/get"
RDAP_BOOTSTRAP = "https://data.iana.org/rdap/dns.json"
TRANCO_LIST = "https://tranco-list.eu/top-1m.csv.zip"
PUBLIC_SUFFIX_LIST = "https://publicsuffix.org/list/public_suffix_list.dat"
IANA_WHOIS = "whois.iana.org"
USER_AGENT = "domain-search-skill/1"
DAY = 86400
# Registries throttle bursts: one RDAP server answered ~250 rapid lookups with a 24-hour block.
REGISTRY_INTERVAL = 1.0
SHORT_RETRY = 30
DEFAULT_COOLDOWN = 3600

LABEL = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)$")
DIG_STATUS = re.compile(r"status: ([A-Z]+)")
WHOIS_SERVER = re.compile(r"^whois:[ \t]*(\S*)", re.MULTILINE)
# Registries append terms of use that mention throttling and missing data, so only the answer's head is read.
WHOIS_HEAD_LINES = 10
WHOIS_HEAD_END = ("terms of use", "notice", "disclaimer", "url of the icann")
WHOIS_THROTTLED = ("exceeded", "too many", "quota", "try again", "rate limit")
WHOIS_FAILED = ("error", "denied", "unavailable", "maintenance", "not supported", "retired")
WHOIS_TAKEN = ("registrar:", "registry domain id:", "registrant:", "creation date:", "created:", "registered:",
               "record created", "nserver:", "name server:", "status: connect")
WHOIS_AVAILABLE = ("no match", "not found", "not_found", "no found", "no data found", "no entries found",
                   "no object found", "does not exist", "status: free", "status: available",
                   "available for registration", "nothing found")


class Throttled(Exception):
    def __init__(self, retry_after):
        super().__init__(retry_after)
        self.retry_after = retry_after


def cache_dir():
    return Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "domain-search"


def cache_date(name):
    path = cache_dir() / name
    return datetime.date.fromtimestamp(path.stat().st_mtime).isoformat() if path.exists() else None


def read_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + ".partial")
    partial.write_text(json.dumps(data))
    partial.replace(path)


def cached(name, max_age, fetch, warnings):
    """Return fresh data from fetch, or the cached copy; None only when both are unavailable."""
    path = cache_dir() / name
    stored = read_json(path)
    if stored is not None and time.time() - path.stat().st_mtime < max_age:
        return stored
    try:
        data = fetch()
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, http.client.HTTPException) as error:
        if stored is None:
            warnings.append(f"{name}: {error}")
            return None
        warnings.append(f"{name}: refresh failed ({error}); using the copy from {cache_date(name)}")
        return stored
    write_json(path, data)
    return data


def http_get(url, data=None, accept="application/json", timeout=30):
    headers = {"Accept": accept, "User-Agent": USER_AGENT}
    if data is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def fetch_prices():
    body = json.loads(http_get(PORKBUN_PRICING, data=b"{}"))
    if body.get("status") != "SUCCESS":
        raise ValueError(body.get("message", "unexpected Porkbun response"))
    return body["pricing"]


def fetch_rdap_servers():
    servers = {}
    for tlds, urls in json.loads(http_get(RDAP_BOOTSTRAP))["services"]:
        url = next((u for u in urls if u.startswith("https://")), urls[0])
        servers.update(dict.fromkeys(tlds, url))
    return servers


def fetch_icann_suffixes():
    """Multi-label suffixes from the ICANN section of the Public Suffix List, in punycode."""
    text = http_get(PUBLIC_SUFFIX_LIST, accept="text/plain").decode("utf-8")
    section = text.split("// ===BEGIN ICANN DOMAINS===", 1)[1].split("// ===END ICANN DOMAINS===", 1)[0]
    suffixes = []
    for line in section.splitlines():
        line = line.strip()
        if line and not line.startswith(("//", "*", "!")) and "." in line:
            try:
                suffixes.append(normalize(line))
            except ValueError:
                pass
    return suffixes


def fetch_tld_counts():
    """Count Tranco top-1M domains under each last label and each two-label suffix."""
    archive = zipfile.ZipFile(io.BytesIO(http_get(TRANCO_LIST, accept="application/zip", timeout=120)))
    counts = {}
    with archive.open(archive.namelist()[0]) as file:
        for row in csv.reader(io.TextIOWrapper(file, "ascii", errors="replace")):
            labels = row[1].lower().split(".")
            for size in (1, 2):
                if len(labels) > size:
                    suffix = ".".join(labels[-size:])
                    counts[suffix] = counts.get(suffix, 0) + 1
    return counts


def catalog_tlds(prices, icann_suffixes):
    """Porkbun TLDs in the DNS root. specialType marks Handshake names; a multi-label entry counts only when the
    Public Suffix List's ICANN section has it, which drops private registries such as br.com and com.de."""
    return [tld for tld, price in prices.items()
            if not price.get("specialType") and ("." not in tld or tld in icann_suffixes)]


def tld_ranks(counts, tlds):
    """Rank single-label TLDs by count; a requested second level such as co.uk takes the position its count
    reaches without shifting the others, so a TLD keeps its rank whatever else a run checks."""
    singles = sorted((key for key in counts if "." not in key), key=lambda key: (-counts[key], key))
    ranks = {key: rank for rank, key in enumerate(singles, 1)}
    for tld in tlds:
        if "." in tld and tld in counts:
            ranks[tld] = 1 + sum(counts[key] > counts[tld] for key in singles)
    return ranks


def normalize(name):
    labels = name.strip().lower().strip(".").split(".")
    try:
        labels = [label.encode("idna").decode("ascii") for label in labels]
    except UnicodeError as error:
        raise ValueError(f"invalid name {name!r}: {error}") from None
    if not all(LABEL.match(label) for label in labels):
        raise ValueError(f"invalid name {name!r}")
    return ".".join(labels)


def targets(names, tlds):
    """Expand bare labels across tlds; a name with a dot is one exact domain."""
    found = {}
    for raw in names:
        name = normalize(raw)
        if "." in name:
            label, tld = name.split(".", 1)
            found[name] = (label, tld)
        else:
            for tld in tlds:
                found[f"{name}.{tld}"] = (name, tld)
    return [{"domain": domain, "name": name, "tld": tld} for domain, (name, tld) in found.items()]


def dns_status(domain):
    try:
        result = subprocess.run(["dig", "+time=2", "+tries=2", "+noall", "+comments", "NS", domain],
                                capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        return None
    match = DIG_STATUS.search(result.stdout)
    return match.group(1) if match else None


def retry_after(value):
    if not value:
        return None
    if value.isdigit():
        return int(value)
    try:
        moment = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    return max(0, int((moment - datetime.datetime.now(datetime.timezone.utc)).total_seconds()))


def describe_wait(seconds):
    if seconds is None:
        return ""
    hours, minutes = divmod(int(seconds) // 60, 60)
    return f", retry after {hours}h{minutes:02d}m" if hours else f", retry after {minutes}m"


def json_object(body):
    try:
        return json.loads(body)
    except ValueError:
        return None


def rdap_lookup(domain, base, fetch=http_get):
    """A verdict needs an RDAP answer: a domain object, or a 404 whose body is empty or JSON."""
    try:
        body = fetch(base.rstrip("/") + "/domain/" + domain, accept="application/rdap+json", timeout=15)
    except urllib.error.HTTPError as error:
        if error.code == 429:
            raise Throttled(retry_after(error.headers.get("Retry-After"))) from None
        if error.code != 404:
            return None, f"RDAP HTTP {error.code}"
        try:
            body = error.read()
        except (OSError, http.client.HTTPException):
            body = b""
        if body.strip() and not isinstance(json_object(body), dict):
            return None, "RDAP 404 without an RDAP body"
        return "available", "RDAP: no record"
    except (urllib.error.URLError, OSError, http.client.HTTPException) as error:
        return None, f"RDAP {getattr(error, 'reason', error)}"
    record = json_object(body)
    if isinstance(record, dict) and record.get("objectClassName") == "domain":
        return "taken", "RDAP: registered"
    return None, "RDAP answer is not a domain record"


def whois_query(server, query, timeout=15):
    with socket.create_connection((server, 43), timeout=timeout) as connection:
        connection.sendall(query.encode("ascii") + b"\r\n")
        chunks = []
        while chunk := connection.recv(4096):
            chunks.append(chunk)
    return b"".join(chunks).decode("utf-8", "replace")


def whois_head(text):
    head = []
    for line in text.splitlines():
        line = line.strip().lower()
        if not line or line.startswith(("%", "#", ">>>")):
            continue
        if line.startswith(WHOIS_HEAD_END) or len(head) == WHOIS_HEAD_LINES:
            break
        head.append(line)
    return "\n".join(head)


def classify_whois(text):
    head = whois_head(text)
    if any(pattern in head for pattern in WHOIS_THROTTLED):
        return "throttled", "WHOIS throttled"
    if any(pattern in head for pattern in WHOIS_FAILED):
        return None, "WHOIS answered with an error"
    if any(pattern in head for pattern in WHOIS_TAKEN):
        return "taken", "WHOIS: registered"
    if any(pattern in head for pattern in WHOIS_AVAILABLE):
        return "available", "WHOIS: no record"
    return None, "WHOIS answer not recognized"


def whois_lookup(server, domain):
    try:
        text = whois_query(server, domain)
    except OSError as error:
        return None, f"WHOIS {error}"
    status, note = classify_whois(text)
    if status == "throttled":
        raise Throttled(None)
    return status, note


class Registries:
    """Registry lookups paced per server. A server that throttles stays in cooldown, and the cooldowns
    and IANA WHOIS referrals persist between runs."""

    def __init__(self, rdap_servers, whois_servers=None, cooldowns=None, interval=REGISTRY_INTERVAL):
        self.rdap_servers = rdap_servers or {}
        self.whois_servers = whois_servers or {}
        now = time.time()
        self.cooldowns = {host: until for host, until in (cooldowns or {}).items() if until > now}
        self.interval = interval
        self.lock = threading.Lock()
        self.next_slot = {}

    def wait(self, host):
        with self.lock:
            now = time.monotonic()
            slot = max(now, self.next_slot.get(host, now))
            self.next_slot[host] = slot + self.interval
        time.sleep(slot - now)

    def delay(self, host, seconds):
        with self.lock:
            self.next_slot[host] = max(self.next_slot.get(host, 0), time.monotonic() + seconds)

    def cooldown_note(self, host):
        with self.lock:
            remaining = self.cooldowns.get(host, 0) - time.time()
        return f"{host} throttled{describe_wait(remaining)}" if remaining > 0 else None

    def lookup(self, host, query):
        for attempt in (1, 2):
            note = self.cooldown_note(host)
            if note:
                return None, note
            self.wait(host)
            note = self.cooldown_note(host)
            if note:
                return None, note
            try:
                return query()
            except Throttled as error:
                if attempt == 1 and error.retry_after is not None and error.retry_after <= SHORT_RETRY:
                    self.delay(host, error.retry_after + 1)
                    continue
                seconds = DEFAULT_COOLDOWN if error.retry_after is None else error.retry_after
                with self.lock:
                    self.cooldowns[host] = time.time() + seconds
                return None, f"{host} throttled{describe_wait(seconds)}"

    def rdap_base(self, tld):
        return self.rdap_servers.get(tld) or self.rdap_servers.get(tld.rsplit(".", 1)[-1])

    def whois_server(self, tld, query=whois_query):
        """The registry's WHOIS host, "" when IANA lists none, or None when IANA gave no usable answer."""
        key = tld.rsplit(".", 1)[-1]
        with self.lock:
            entry = self.whois_servers.get(key)
        if isinstance(entry, list) and time.time() - entry[1] < 30 * DAY:
            return entry[0]
        try:
            self.wait(IANA_WHOIS)
            text = query(IANA_WHOIS, key)
        except OSError:
            return None
        if not re.search(rf"^domain:\s*{re.escape(key)}\s*$", text, re.IGNORECASE | re.MULTILINE):
            return None
        match = WHOIS_SERVER.search(text)
        server = match.group(1) if match else ""
        with self.lock:
            self.whois_servers[key] = [server, time.time()]
        return server

    def check(self, domain, tld):
        notes = []
        base = self.rdap_base(tld)
        if base:
            status, note = self.lookup(urllib.parse.urlparse(base).netloc, lambda: rdap_lookup(domain, base))
            if status:
                return status, note
            notes.append(note)
        server = self.whois_server(tld)
        if server:
            status, note = self.lookup(server, lambda: whois_lookup(server, domain))
            if status:
                return status, note
            notes.append(note)
        elif server is None:
            notes.append("IANA WHOIS referral lookup failed")
        elif not base:
            notes.append("no RDAP or WHOIS server known")
        return None, "; ".join(notes)


def search(items, *, dns, registry, ranks, limit=None, always=()):
    """Set each item's status and evidence. With a limit, the registry hears about the TLDs in always plus that
    many other undelegated domains per name, most popular TLD first; the rest stay unchecked."""
    # A TLD with wildcard DNS (.ph, .ws) resolves every name, so its DNS answer proves nothing.
    probe = f"wildcard-probe-{secrets.token_hex(8)}"
    tlds = sorted({item["tld"] for item in items})
    with concurrent.futures.ThreadPoolExecutor(32) as pool:
        wildcard = {tld for tld, status in zip(tlds, pool.map(lambda tld: dns(f"{probe}.{tld}"), tlds))
                    if status == "NOERROR"}
        for item, status in zip(items, pool.map(lambda item: dns(item["domain"]), items)):
            item["dns"] = "WILDCARD" if item["tld"] in wildcard else status
            if item["dns"] == "NOERROR":
                item["status"], item["evidence"] = "taken", "DNS delegation"
    candidates = [item for item in items if item["dns"] != "NOERROR"]
    if limit is not None:
        by_name = {}
        for item in candidates:
            by_name.setdefault(item["name"], []).append(item)
        candidates = []
        for group in by_name.values():
            ranked = sorted((item for item in group if item["tld"] not in always),
                            key=lambda item: (ranks.get(item["tld"], float("inf")), item["tld"]))
            candidates += [item for item in group if item["tld"] in always] + ranked[:limit]
            for item in ranked[limit:]:
                item["status"], item["evidence"] = "unchecked", "not checked with the registry"

    def verdict(item):
        try:
            return registry(item["domain"], item["tld"])
        except Exception as error:  # one malformed answer must not discard the rest of the run
            return None, f"lookup error: {error}"

    with concurrent.futures.ThreadPoolExecutor(16) as pool:
        for item, (status, note) in zip(candidates, pool.map(verdict, candidates)):
            if status:
                item["status"], item["evidence"] = status, note
            elif item["dns"] == "NXDOMAIN":
                item["status"], item["evidence"] = "unconfirmed", f"no DNS delegation; {note}"
            else:
                item["status"], item["evidence"] = "unknown", f"DNS {item['dns'] or 'failed'}; {note}"


def describe_price(row):
    price, years = row["price"], MIN_YEARS.get(row["tld"])
    if not (price and price.get("registration")):
        return f"no Porkbun price, compare at https://tld-list.com/tld/{row['tld']}"
    first = f"${price['registration']} per year with a {years}-year minimum" if years else \
        f"${price['registration']} first year"
    return f"{first}, ${price.get('renewal') or '?'} renewal"


def short_price(row):
    price, years = row["price"], MIN_YEARS.get(row["tld"])
    if not (price and price.get("registration")):
        return "no Porkbun price"
    minimum = f" ({years}-year minimum)" if years else ""
    return f"${price['registration']}/${price.get('renewal') or '?'}{minimum}"


def render_markdown(rows, all_mode, footer):
    lines = []
    for name in dict.fromkeys(row["name"] for row in rows):
        group = [row for row in rows if row["name"] == name]
        shown = [row for row in group if not all_mode or row["status"] not in ("taken", "unchecked")]
        lines += [f"## {name}", ""]
        for row in shown:
            rank = f"TLD #{row['rank']}" if row["rank"] else "TLD unranked"
            lines.append(f"- **{row['domain']}**: {row['status']}, {describe_price(row)} "
                         f"({rank}; {row['evidence']})")
        if all_mode:
            unchecked = [row for row in group if row["status"] == "unchecked"]
            undelegated = [row for row in unchecked if row["dns"] == "NXDOMAIN"]
            if undelegated:
                listing = " · ".join(f".{row['tld']} {short_price(row)}" for row in undelegated)
                lines.append("- Without DNS delegation, not checked with the registry, most popular first "
                             f"(first year/renewal): {listing}")
            taken = [f".{row['tld']}" for row in group if row["status"] == "taken"]
            if taken:
                lines.append(f"- Taken, most popular first: {' · '.join(taken)}")
            lines += ["", f"Taken: {len(taken)}. Not checked with the registry: {len(unchecked)}; raise --limit "
                          "to check more."]
        lines.append("")
    return "\n".join(lines + footer) + "\n"


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="+", help="labels to try across TLDs, or full domains such as acme.io")
    parser.add_argument("--tlds", help=f"comma-separated TLDs (default: {','.join(DEFAULT_TLDS)})")
    parser.add_argument("--all", action="store_true",
                        help="every DNS-root TLD that Porkbun prices, plus " + ", ".join(ALL_EXTRA_TLDS)
                             + " and any --tlds, listed by popularity")
    parser.add_argument("--limit", type=positive_int, default=DEFAULT_LIMIT,
                        help="with --all, registry checks per name besides the named TLDs (default: %(default)s)")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)

    try:
        named = [normalize(tld) for tld in args.tlds.split(",") if tld.strip()] if args.tlds else []
        targets(args.names, [])
    except ValueError as error:
        parser.error(str(error))
    if not shutil.which("dig"):
        print("error: dig is required for the DNS pass", file=sys.stderr)
        return 1

    warnings = []
    prices = cached("porkbun-pricing.json", DAY, fetch_prices, warnings)
    if args.all:
        if prices is None:
            print("error: --all needs Porkbun's TLD catalog, which could not be fetched: " + "; ".join(warnings),
                  file=sys.stderr)
            return 1
        icann = set(cached("psl-icann-suffixes.json", 30 * DAY, fetch_icann_suffixes, warnings) or ())
        tlds = list(dict.fromkeys(named + list(ALL_EXTRA_TLDS) + catalog_tlds(prices, icann)))
        always = set(named) | set(ALL_EXTRA_TLDS)
    else:
        tlds, always = named or list(DEFAULT_TLDS), set()
    items = targets(args.names, tlds)

    counts = cached("tranco-tld-counts.json", 30 * DAY, fetch_tld_counts, warnings) or {}
    ranks = tld_ranks(counts, {item["tld"] for item in items})
    whois_path, cooldown_path = cache_dir() / "whois-servers.json", cache_dir() / "cooldowns.json"
    registries = Registries(cached("rdap-servers.json", 7 * DAY, fetch_rdap_servers, warnings),
                            read_json(whois_path), read_json(cooldown_path))
    search(items, dns=dns_status, registry=registries.check, ranks=ranks,
           limit=args.limit if args.all else None, always=always)
    write_json(whois_path, registries.whois_servers)
    write_json(cooldown_path, registries.cooldowns)

    for item in items:
        item["rank"] = ranks.get(item["tld"])
        price = (prices or {}).get(item["tld"])
        item["price"] = {key: price.get(key) for key in ("registration", "renewal", "transfer")} if price else None
    if args.all:
        items.sort(key=lambda item: (item["rank"] or float("inf"), item["tld"]))

    footer = []
    if prices:
        footer.append(f"Prices: Porkbun standard USD prices for the TLD (fetched {cache_date('porkbun-pricing.json')}); "
                      "a premium name costs more at checkout.")
    if counts:
        footer.append("TLD rank: position by domain count in the Tranco top-1M list "
                      f"(fetched {cache_date('tranco-tld-counts.json')}).")
    footer.append(f"Checked {len({item['tld'] for item in items})} TLDs.")
    footer += [f"Warning: {warning}" for warning in warnings]
    if args.format == "json":
        print(json.dumps({"results": items, "notes": footer}, indent=2))
    else:
        print(render_markdown(items, args.all, footer), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
