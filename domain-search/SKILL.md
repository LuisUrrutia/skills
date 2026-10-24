---
name: domain-search
description: Use when checking whether domain names are available to register or what registering them costs.
---

# Domain search

Answer with `scripts/search-domains.py` from this skill's directory. A domain
with a DNS delegation counts as taken; for the rest, the TLD's registry gives
the verdict over RDAP, then WHOIS. Each result carries Porkbun's list price and
the TLD's popularity rank. The script needs `python3`, `dig` and network
access; when it exits with an error, report that message as the blocker.

## Run the search

Put every name of the request into one run. A bare label (`acme`) is tried
across the TLDs; a full domain (`acme.io`) is checked as given.

```sh
python3 <skill-dir>/scripts/search-domains.py acme acmehq
python3 <skill-dir>/scripts/search-domains.py acme --tlds com,co,xyz
python3 <skill-dir>/scripts/search-domains.py acme --all
```

- When the user names no TLDs, omit `--tlds`: the default set is the user's
  usual com, ai, app, io and dev. Named TLDs replace it.
- A request for all TLDs or every extension takes `--all`. Raise `--limit`
  (30 registry checks per name) only as far as the user asks for more confirmed
  results.

The script replaces tldx here, and one run per request keeps its pacing intact.
Registries throttle bulk lookups per IP address: a 660-TLD tldx burst drew a
24-hour RDAP block from Identity Digital, which serves over 400 TLDs including
.ai and .info, and tldx then reported throttled lookups such as google.live as
available.

## Report the results

Present the results for each name in the user's language as bullet points, one
domain per bullet with its status and price, as the script prints them. Every
check the user asks for gets the prices, even when they ask only about
availability. With these statuses:

- **available:** the registry has no record of the domain. Reserved and premium
  names have no record either, so the registrar's checkout confirms that it can
  be registered and at what price.
- **taken:** the registry or DNS shows a registration.
- **unconfirmed:** DNS has no delegation, but the registry check failed or was
  throttled. Report that availability is not confirmed, with the reason, apart
  from the confirmed results: a registered domain can lack DNS. An unconfirmed
  .cl or .es gets a link to https://www.nic.cl or https://www.dominios.es:
  neither registry offers RDAP, and their WHOIS servers did not answer this
  machine.
- **unknown:** DNS gave no clear answer, because it failed or the TLD has
  wildcard DNS, and the registry check failed too.

Point out a renewal well above the first-year price. To compare registrars for
a shortlisted TLD, link `https://tld-list.com/tld/<tld>`. When you recommend a
ccTLD, mention that it may restrict who can register it, as .us, .eu and .ca do.

For `--all`, also give the number of TLDs checked, the counts of taken TLDs and
of TLDs not checked with the registry per name, and the most popular of the
unchecked ones with their prices, marked as not confirmed. Its universe is
every DNS-root TLD that Porkbun prices, plus .cl and .es; another TLD, such as
.fr, is checked only when named with `--tlds`.

Done when each requested name has its bullets, every bullet carries its price
or the script's tld-list.com link, every unconfirmed or unknown domain is
reported with its reason, and each warning line from the script is relayed.
