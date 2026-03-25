---
name: business-startup-analyst
description: End-to-end startup and business analysis for turning one idea into a structured decision-ready case. Use when users ask to validate a startup idea, size a market (TAM/SAM/SOM), analyze competitors, define pricing and unit economics, build go-to-market strategy, estimate financial scenarios, or decide go/no-go. Especially useful when the user wants one or multiple output files (memo, analysis pack, investor-style brief, execution plan) for a single startup concept.
---

# Ultimate Business Startup Analyst

Build a startup analysis that is rigorous enough for investors and practical enough for founders to execute.

Default behavior: produce a clear recommendation and the exact next validation actions, not just theory.

## Output Modes

Choose one mode based on user intent and available data.

1. **Quick Verdict (single file)**
   - Use when user asks "is this idea worth it?"
   - Deliver one concise memo with score, key risks, and 2-week plan

2. **Case Pack (multi-file, recommended)**
   - Use when user asks for complete analysis, startup dossier, investor prep, or full strategy
   - Generate a structured set of files covering market, competition, economics, GTM, risks, and execution

3. **Focused Deep Dive**
   - Use when user asks for one dimension only (for example, pricing or TAM)
   - Deliver that section plus a short impact note on adjacent sections

## Required Workflow

Follow this sequence. Do not skip steps.

1. **Normalize the idea**
   - Capture: problem, customer, alternative, solution, business model, geography, stage
   - Convert vague idea statements into explicit hypotheses

2. **Build assumption map**
   - Identify critical assumptions in 6 buckets: problem, demand, differentiation, distribution, economics, execution
   - Mark each assumption as `known`, `inferred`, or `untested`

3. **Analyze market opportunity**
   - Estimate TAM/SAM/SOM with transparent assumptions
   - Use both bottom-up and top-down checks when possible
   - Document source quality and confidence

4. **Analyze competition and alternatives**
   - Include direct competitors, indirect substitutes, and status quo behavior
   - Extract real customer pain from reviews/complaints when available
   - Identify 1-3 defensible wedges

5. **Model business viability**
   - Define pricing logic and revenue model
   - Calculate baseline unit economics (CAC, LTV, payback, gross margin)
   - Flag breakage points where economics fail

6. **Define GTM and growth path**
   - Select beachhead segment and first channels
   - Tie channel plan to conversion assumptions
   - Specify leading indicators for first 90 days

7. **Stress test with scenarios**
   - Build conservative, base, and upside scenario assumptions
   - State what must be true in each scenario
   - Highlight runway-sensitive risks

8. **Recommend go/no-go and next experiments**
   - Provide weighted score and confidence
   - Recommend `GO`, `CONDITIONAL GO`, `PIVOT`, or `NO-GO`
   - End with a concrete 14-day validation backlog

## Multi-File Deliverable Standard

When generating a full analysis pack, use this file set (exact names):

- `00-executive-brief.md`
- `01-problem-customer-fit.md`
- `02-market-opportunity.md`
- `03-competitive-landscape.md`
- `04-business-model-unit-economics.md`
- `05-go-to-market-plan.md`
- `06-financial-scenarios.md`
- `07-validation-experiments.md`
- `08-risk-register.md`
- `09-90-day-execution-plan.md`
- `assumptions-log.md`
- `sources-and-evidence.md`

Use `references/deliverable-templates.md` for section-level structure.

## Evidence and Citation Rules

- Prefer primary and high-quality secondary sources first
- Separate facts from assumptions explicitly
- Add confidence level (`high`, `medium`, `low`) to major claims
- If evidence is weak, reduce recommendation confidence and increase validation priority

Use `references/research-source-quality.md` for source ranking and citation format.

## Scoring Rules

Use weighted scoring across six dimensions:

- Problem severity and urgency: 20%
- Market attractiveness: 20%
- Differentiation defensibility: 15%
- Unit economics viability: 20%
- GTM feasibility: 15%
- Founder/execution fit: 10%

Score each dimension 0-10, then compute weighted score out of 100.

Decision thresholds:

- `>= 75`: GO
- `60-74`: CONDITIONAL GO
- `45-59`: PIVOT
- `< 45`: NO-GO

## Scripts

### `scripts/generate_casepack.py`

Create a startup analysis file pack from a minimal brief.

Example:

```bash
python3 scripts/generate_casepack.py \
  --idea "AI copilot for compliance-heavy SMB accounting" \
  --customer "US bookkeeping firms with 5-25 employees" \
  --problem "Manual reconciliation and month-end close are slow" \
  --solution "Workflow + AI assistant for close automation" \
  --business-model "SaaS subscription" \
  --price "$299/month starting price" \
  --geography "United States" \
  --output-dir ./outputs
```

### `scripts/startup_score.py`

Calculate weighted startup viability score from JSON inputs.

Example:

```bash
python3 scripts/startup_score.py ./inputs/score-input.json --format markdown
```

## References

- `references/framework-playbook.md`: Practical frameworks and formulas used in analysis
- `references/deliverable-templates.md`: Output templates for single-file and case-pack modes
- `references/research-source-quality.md`: Source quality rubric and citation rules

Load only the reference file needed for the current task to keep context focused.
