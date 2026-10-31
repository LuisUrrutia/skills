---
name: humanize
description: Use only when the user explicitly asks to humanize text or to run it through humanizer ("humaniza esto", "humanize this", "pásalo por humanizer"). Not for ordinary rewriting or editing requests.
---

# Humanize

Rewrite the text with `scripts/humanize` from this skill's directory (also on
PATH as `humanize`). It calls Luis's humanizer model, a fine-tuned Gemma 4 12B
on a Runpod Serverless endpoint, and needs `RUNPOD_API_KEY` and
`HUMANIZER_URL` (the endpoint's `/completion` URL), read from the environment
or, when missing there, from fish universal variables. When a
variable is missing or the script exits 1, report its
message as the blocker; do not rewrite the text yourself instead.

```sh
humanize draft.md > draft.humanized.md
printf '%s' "$TEXT" | humanize
```

- **Languages:** the model only handles English and Chinese. For any other
  language, tell the user and stop; do not translate to work around it.
- **Input:** pass only the prose to rewrite. The script keeps fenced code
  blocks and one-line Markdown headings verbatim and splits long text into
  pieces of about 3,000 characters at paragraph breaks.
- **Cold start:** the endpoint scales to zero. The first call after idle
  waits about 2 minutes for a worker; the script retries for up to 7 minutes.
  Run it in the background when the harness would time out sooner.
- **Cost:** about USD 0.002 per warm request and 0.025 per cold start, billed
  to Luis's Runpod balance. Send each text once; do not loop for a better
  sample unless the user asks.

## Check the result

Exit code 2 means a piece still lost or gained a number or URL, or was cut
off at the output limit, after one automatic retry; stderr names it. Exit
code 0 checks only numbers, URLs and truncation.

Before handing the rewrite back, compare it with the original yourself:
names, dates, quotations and claims must survive, and nothing may be added.
Sampling runs at temperature 1.0, so tone can drift (slang, emoticons, a
changed register). Fix a factual slip by restoring the original wording in
that sentence; report tone problems instead of rewriting the text yourself.
Give the user the rewrite and a list of every fix or warning. Never send or
publish the rewrite on their behalf.

## Endpoint

The endpoint is a Runpod Load Balancing endpoint running llama.cpp's
`llama-server` with `humanizer-12b-Q8_0.gguf` from `jialinyyzz/humanizer-GGUF`
on a 24 GB GPU, scaling from 0 to 1 workers. If calls keep timing out, check it
with the `runpod:endpoint-ops` skill: Runpod sets max workers to 0 after 7 days
without requests.
