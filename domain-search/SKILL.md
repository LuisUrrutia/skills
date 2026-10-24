---
name: domain-search
description: Use when checking whether domain names are available to register or what registering them costs.
---

# Domain search

Answer with `scripts/search-domains.py` from this skill's directory. It runs a
DNS pass, takes each verdict from the TLD's registry (RDAP, then WHOIS), adds
Porkbun's public list price, and ranks each TLD by its domain count in the
Tranco top-1M list. It needs Python 3.10+, `dig` and network access; when it
exits with an error, report that message as the blocker.

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
- A request for all TLDs or every extension takes `--all`: every TLD in the DNS
  root that Porkbun prices, plus any `--tlds`. Per name, the registry confirms
  the 30 most popular TLDs that have no DNS delegation, listed by rank. Raise
  `--limit` only as far as the user asks for more results.
- `--format json` returns the same results as data.

Registries throttle bulk lookups per IP address: Identity Digital, which runs
about 250 TLDs including .ai and .info, answered a 660-TLD burst with a 24-hour
RDAP block. One run per request keeps every server within the script's pacing.

## Report the results

Present the results for each name in the user's language as bullet points, one
domain per bullet with its status and price, as the script prints them. Every
check the user asks for gets the prices, even when they ask only about
availability. With these statuses:

- **available:** the registry has no record of the domain.
- **taken:** the registry or DNS shows a registration.
- **unconfirmed:** DNS has no delegation, but the registry check failed or was
  throttled. Present it as probably available, with the evidence: a registered
  domain can lack DNS.
- **unknown:** neither DNS nor the registry answered.

Prices are Porkbun's standard first-year and renewal prices for the TLD, in USD.
Point out a renewal well above the first-year price. A registry-premium name
costs more, and only the registrar's checkout shows its price. To compare
registrars for a shortlisted TLD, link `https://tld-list.com/tld/<tld>`. When
you recommend a ccTLD, mention that it may restrict who can register it, as
.us, .eu and .ca do.

For `--all`, also give the number of TLDs checked and the counts of taken and
unchecked TLDs per name. TLDs that Porkbun does not sell, such as .cl, .es and
.fr, are checked only when named with `--tlds`; their bullet carries a
tld-list.com link in place of the price.

Done when each requested name has its bullets, every bullet carries its price
or that link, every unconfirmed or unknown domain is reported with its reason,
and each warning line from the script is relayed.
