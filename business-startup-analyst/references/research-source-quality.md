# Research Source Quality

## Source Ranking

Rate every source used in analysis.

### A (highest confidence)
- Official filings and regulated disclosures (10-K, annual reports)
- Government data and official statistics
- Reputable industry datasets with transparent methodology
- Primary first-party product/pricing documentation

### B (moderate confidence)
- Recognized analyst reports with partial methodology
- Well-structured market intelligence summaries
- Trade publications with named data sources

### C (low confidence)
- Vendor marketing content without clear methodology
- Opinion articles without source traceability
- Aggregated numbers copied without citation chain

Default rule: never anchor major decisions on C-only evidence.

## Citation Format

Use one line per claim:

`[Claim] - [Source title], [publisher], [date], [URL], Quality [A/B/C]`

Example:

`US SMB accounting software spend exceeded $X in 2025 - [Source], [Publisher], 2025-11-02, https://..., Quality A`

## Evidence Hygiene Rules

- Separate `fact`, `inference`, and `assumption`
- If no strong source exists, mark claim as low confidence
- Prefer most recent data that still reflects market cycle context
- Cross-check critical numbers with at least 2 independent sources

## Confidence Labels

Apply confidence labels to major conclusions:

- `high`: multiple A/B sources, low variance
- `medium`: mixed A/B/C sources, moderate assumptions
- `low`: sparse evidence or conflicting data

If a key recommendation depends on low-confidence evidence, require a validation experiment before execution.

## Red Flags

Flag explicitly when you detect:
- TAM inflated from broad category without filters
- SOM assumed above realistic capture rates for stage
- Pricing assumptions copied from non-comparable segments
- Competitor claims based only on homepage messaging
- Unit economics computed without churn or gross margin
