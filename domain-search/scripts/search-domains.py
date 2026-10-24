#!/usr/bin/env python3
"""Check domain availability with each TLD's registry, priced from Porkbun and ranked by Tranco TLD popularity."""

import argparse
import concurrent.futures
import csv
import datetime
import email.utils
import io
import json
import os
from pathlib import Path
import re
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
DEFAULT_LIMIT = 30
PORKBUN_PRICING = "https://api.porkbun.com/api/json/v3/pricing/get"
RDAP_BOOTSTRAP = "https://data.iana.org/rdap/dns.json"
TRANCO_LIST = "https://tranco-list.eu/top-1m.csv.zip"
IANA_WHOIS = "whois.iana.org"
USER_AGENT = "domain-search-skill/1"
DAY = 86400
# Registries throttle bursts: one RDAP server answered ~250 rapid lookups with a 24-hour block.
REGISTRY_INTERVAL = 1.0
SHORT_RETRY = 30

LABEL = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)$")
DIG_STATUS = re.compile(r"status: ([A-Z]+)")
WHOIS_SERVER = re.compile(r"^whois:[ \t]*(\S*)", re.MULTILINE)
WHOIS_TAKEN = ("registrar:", "registry domain id:", "registrant:", "creation date:", "created:", "registered:",
               "record created", "nserver:", "name server:", "status: connect")
WHOIS_AVAILABLE = ("no match", "not found", "not_found", "no found", "no data found", "no entries found",
                   "no object found", "does not exist", "status: free", "status: available",
                   "available for registration", "nothing found")
WHOIS_THROTTLED = ("limit exceeded", "too many", "quota", "try again later")


class Throttled(Exception):
    def __init__(self, retry_after):
        super().__init__(retry_after)
        self.retry_after = retry_after


def cache_dir():
    return Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "domain-search"


def cache_date(name):
    path = cache_dir() / name
    return datetime.date.fromtimestamp(path.stat().st_mtime).isoformat() if path.exists() else None


def cached(name, max_age, fetch, warnings):
    """Return fresh data from fetch, or the cached copy; None only when both are unavailable."""
    path = cache_dir() / name
    if path.exists() and time.time() - path.stat().st_mtime < max_age:
        return json.loads(path.read_text())
    try:
        data = fetch()
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        if not path.exists():
            warnings.append(f"{name}: {error}")
            return None
        warnings.append(f"{name}: refresh failed ({error}); using the copy from {cache_date(name)}")
        return json.loads(path.read_text())
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(".partial")
    partial.write_text(json.dumps(data))
    partial.replace(path)
    return data


def http(url, data=None, accept="application/json", timeout=30):
    headers = {"Accept": accept, "User-Agent": USER_AGENT}
    if data is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def fetch_prices():
    body = json.loads(http(PORKBUN_PRICING, data=b"{}"))
    if body.get("status") != "SUCCESS":
        raise ValueError(body.get("message", "unexpected Porkbun response"))
    return body["pricing"]


def fetch_rdap_servers():
    servers = {}
    for tlds, urls in json.loads(http(RDAP_BOOTSTRAP))["services"]:
        url = next((u for u in urls if u.startswith("https://")), urls[0])
        servers.update(dict.fromkeys(tlds, url))
    return servers


def fetch_tld_counts():
    """Count Tranco top-1M domains under each last label and each two-label suffix."""
    archive = zipfile.ZipFile(io.BytesIO(http(TRANCO_LIST, accept="application/zip", timeout=120)))
    counts = {}
    with archive.open(archive.namelist()[0]) as file:
        for row in csv.reader(io.TextIOWrapper(file, "ascii", errors="replace")):
            labels = row[1].lower().split(".")
            for size in (1, 2):
                if len(labels) > size:
                    suffix = ".".join(labels[-size:])
                    counts[suffix] = counts.get(suffix, 0) + 1
    return counts


def catalog_tlds(prices):
    """Porkbun TLDs in the DNS root: specialType marks Handshake names, and multi-label entries under a
    gTLD (br.com, uk.net) are private second-level registries without RDAP or WHOIS for their names."""
    return [tld for tld, price in prices.items()
            if not price.get("specialType") and ("." not in tld or len(tld.rsplit(".", 1)[1]) == 2)]


def tld_ranks(counts, tlds):
    keys = {key for key in counts if "." not in key} | {tld for tld in tlds if "." in tld and tld in counts}
    return {key: rank for rank, key in enumerate(sorted(keys, key=lambda key: (-counts[key], key)), 1)}


def normalize(name):
    labels = name.strip().lower().rstrip(".").split(".")
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
    hours, minutes = divmod(seconds // 60, 60)
    return f", retry after {hours}h{minutes:02d}m" if hours else f", retry after {minutes}m"


def rdap_lookup(domain, base):
    try:
        http(base.rstrip("/") + "/domain/" + domain, accept="application/rdap+json", timeout=15)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return "available", "RDAP: no record"
        if error.code == 429:
            raise Throttled(retry_after(error.headers.get("Retry-After"))) from None
        return None, f"RDAP HTTP {error.code}"
    except (urllib.error.URLError, OSError) as error:
        return None, f"RDAP {getattr(error, 'reason', error)}"
    return "taken", "RDAP: registered"


def whois_query(server, query, timeout=15):
    with socket.create_connection((server, 43), timeout=timeout) as connection:
        connection.sendall(query.encode("ascii") + b"\r\n")
        chunks = []
        while chunk := connection.recv(4096):
            chunks.append(chunk)
    return b"".join(chunks).decode("utf-8", "replace")


def classify_whois(text):
    lower = text.lower()
    if any(pattern in lower for pattern in WHOIS_TAKEN):
        return "taken", "WHOIS: registered"
    if any(pattern in lower for pattern in WHOIS_AVAILABLE):
        return "available", "WHOIS: no record"
    if any(pattern in lower for pattern in WHOIS_THROTTLED):
        return None, "WHOIS throttled"
    return None, "WHOIS answer not recognized"


class Registries:
    """Registry lookups paced per server; a server that throttles is skipped for the rest of the run."""

    def __init__(self, rdap_servers, whois_servers, interval=REGISTRY_INTERVAL):
        self.rdap_servers = rdap_servers or {}
        self.whois_servers = whois_servers
        self.interval = interval
        self.lock = threading.Lock()
        self.next_slot = {}
        self.blocked = {}

    def wait(self, host):
        with self.lock:
            now = time.monotonic()
            slot = max(now, self.next_slot.get(host, now))
            self.next_slot[host] = slot + self.interval
        time.sleep(slot - now)

    def rdap_base(self, tld):
        return self.rdap_servers.get(tld) or self.rdap_servers.get(tld.rsplit(".", 1)[-1])

    def whois_server(self, tld):
        key = tld.rsplit(".", 1)[-1]
        with self.lock:
            if key in self.whois_servers:
                return self.whois_servers[key]
        try:
            self.wait(IANA_WHOIS)
            match = WHOIS_SERVER.search(whois_query(IANA_WHOIS, key))
        except OSError:
            return None
        with self.lock:
            self.whois_servers[key] = match.group(1) if match else ""
        return self.whois_servers[key]

    def lookup(self, host, query):
        for attempt in (1, 2):
            if host in self.blocked:
                return None, f"{host} throttled{describe_wait(self.blocked[host])}"
            self.wait(host)
            try:
                return query()
            except Throttled as error:
                if attempt == 1 and error.retry_after is not None and error.retry_after <= SHORT_RETRY:
                    time.sleep(error.retry_after + 1)
                    continue
                self.blocked[host] = error.retry_after
                return None, f"{host} throttled{describe_wait(error.retry_after)}"

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
            def whois():
                text = whois_query(server, domain)
                status, note = classify_whois(text)
                if note == "WHOIS throttled":
                    raise Throttled(None)
                return status, note
            try:
                status, note = self.lookup(server, whois)
            except OSError as error:
                status, note = None, f"WHOIS {error}"
            if status:
                return status, note
            notes.append(note)
        elif not base:
            notes.append("no RDAP or WHOIS server known")
        return None, "; ".join(notes)


def search(items, *, dns, registry, ranks, limit=None):
    """Set each item's status and evidence. With a limit, only that many undelegated domains per name,
    most popular TLD first, reach the registry; the rest stay unchecked."""
    with concurrent.futures.ThreadPoolExecutor(32) as pool:
        for item, status in zip(items, pool.map(lambda item: dns(item["domain"]), items)):
            item["dns"] = status
            if status == "NOERROR":
                item["status"], item["evidence"] = "taken", "DNS delegation"
    candidates = [item for item in items if item["dns"] != "NOERROR"]
    if limit is not None:
        by_name = {}
        for item in candidates:
            by_name.setdefault(item["name"], []).append(item)
        candidates = []
        for group in by_name.values():
            group.sort(key=lambda item: (ranks.get(item["tld"], float("inf")), item["tld"]))
            candidates += group[:limit]
            for item in group[limit:]:
                item["status"], item["evidence"] = "unchecked", "registry not queried (--limit)"
    with concurrent.futures.ThreadPoolExecutor(16) as pool:
        verdicts = pool.map(lambda item: registry(item["domain"], item["tld"]), candidates)
        for item, (status, note) in zip(candidates, verdicts):
            if status:
                item["status"], item["evidence"] = status, note
            elif item["dns"] == "NXDOMAIN":
                item["status"], item["evidence"] = "unconfirmed", f"no DNS delegation; {note}"
            else:
                item["status"], item["evidence"] = "unknown", f"DNS {item['dns'] or 'failed'}; {note}"


def money(price, key):
    return f"${price[key]}" if price and price.get(key) else "–"


def render_markdown(rows, all_mode, footer):
    lines = []
    for name in dict.fromkeys(row["name"] for row in rows):
        group = [row for row in rows if row["name"] == name]
        shown = [row for row in group if not all_mode or row["status"] not in ("taken", "unchecked")]
        lines += [f"## {name}", "", "| Domain | Status | TLD rank | Porkbun 1st year | Porkbun renewal | Evidence |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for row in shown:
            rank = f"#{row['rank']}" if row["rank"] else "–"
            lines.append(f"| {row['domain']} | {row['status']} | {rank} | {money(row['price'], 'registration')} "
                         f"| {money(row['price'], 'renewal')} | {row['evidence']} |")
        if all_mode:
            taken = sum(row["status"] == "taken" for row in group)
            unchecked = sum(row["status"] == "unchecked" for row in group)
            lines += ["", f"Taken: {taken}. Unchecked: {unchecked} less popular TLDs that the registry was not "
                          "asked about; raise --limit to check them."]
        lines.append("")
    return "\n".join(lines + footer) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="+", help="labels to try across TLDs, or full domains such as acme.io")
    parser.add_argument("--tlds", default=",".join(DEFAULT_TLDS), help="comma-separated TLDs (default: %(default)s)")
    parser.add_argument("--all", action="store_true",
                        help="add every DNS-root TLD that Porkbun prices and list undelegated ones by popularity")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                        help="with --all, registry checks per name, most popular TLDs first (default: %(default)s)")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)

    warnings = []
    prices = cached("porkbun-pricing.json", DAY, fetch_prices, warnings)
    tlds = [tld.strip().lower().lstrip(".") for tld in args.tlds.split(",") if tld.strip()]
    if args.all:
        if prices is None:
            print("error: --all needs Porkbun's TLD catalog, which could not be fetched: " + "; ".join(warnings),
                  file=sys.stderr)
            return 1
        tlds = list(dict.fromkeys(tlds + catalog_tlds(prices)))
    try:
        items = targets(args.names, tlds)
    except ValueError as error:
        parser.error(str(error))
    if not shutil.which("dig"):
        print("error: dig is required for the DNS pass", file=sys.stderr)
        return 1

    counts = cached("tranco-tld-counts.json", 30 * DAY, fetch_tld_counts, warnings) or {}
    ranks = tld_ranks(counts, {item["tld"] for item in items})
    whois_path = cache_dir() / "whois-servers.json"
    whois_servers = json.loads(whois_path.read_text()) if whois_path.exists() else {}
    registries = Registries(cached("rdap-servers.json", 7 * DAY, fetch_rdap_servers, warnings), whois_servers)
    search(items, dns=dns_status, registry=registries.check, ranks=ranks, limit=args.limit if args.all else None)
    whois_path.parent.mkdir(parents=True, exist_ok=True)
    whois_path.write_text(json.dumps(registries.whois_servers))

    for item in items:
        item["rank"] = ranks.get(item["tld"])
        item["price"] = (prices or {}).get(item["tld"])
        if item["price"]:
            item["price"] = {key: item["price"].get(key) for key in ("registration", "renewal", "transfer")}
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
