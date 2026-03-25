#!/usr/bin/env python3
"""
Generate a startup analysis case pack from a minimal brief.

Creates a folder with standardized markdown files so the analyst can
fill, refine, and deliver a complete startup assessment quickly.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict


FILE_ORDER = [
    "00-executive-brief.md",
    "01-problem-customer-fit.md",
    "02-market-opportunity.md",
    "03-competitive-landscape.md",
    "04-business-model-unit-economics.md",
    "05-go-to-market-plan.md",
    "06-financial-scenarios.md",
    "07-validation-experiments.md",
    "08-risk-register.md",
    "09-90-day-execution-plan.md",
    "assumptions-log.md",
    "sources-and-evidence.md",
]


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", value).strip().lower()
    cleaned = re.sub(r"[\s_-]+", "-", cleaned)
    return cleaned or "startup-idea"


def load_brief(args: argparse.Namespace) -> Dict[str, str]:
    data: Dict[str, str] = {}

    if args.from_json:
        with open(args.from_json, "r", encoding="utf-8") as handle:
            loaded = json.load(handle)
        if not isinstance(loaded, dict):
            raise ValueError("Input JSON must be an object.")
        for key, value in loaded.items():
            data[key] = str(value)

    cli_fields = {
        "idea": args.idea,
        "customer": args.customer,
        "problem": args.problem,
        "solution": args.solution,
        "business_model": args.business_model,
        "price": args.price,
        "geography": args.geography,
        "stage": args.stage,
        "founder": args.founder,
        "notes": args.notes,
    }

    for key, value in cli_fields.items():
        if value:
            data[key] = value

    if "idea" not in data or not data["idea"].strip():
        raise ValueError(
            "`idea` is required. Pass --idea or include it in --from-json."
        )

    defaults = {
        "customer": "[Define target customer]",
        "problem": "[Define core pain/problem]",
        "solution": "[Define solution]",
        "business_model": "[Define business model]",
        "price": "[Define pricing hypothesis]",
        "geography": "[Define target geography]",
        "stage": "idea",
        "founder": "[Founder/team context]",
        "notes": "",
    }

    for key, value in defaults.items():
        data.setdefault(key, value)

    return data


def build_files(brief: Dict[str, str]) -> Dict[str, str]:
    header = (
        f"- Idea: {brief['idea']}\n"
        f"- Customer: {brief['customer']}\n"
        f"- Problem: {brief['problem']}\n"
        f"- Solution: {brief['solution']}\n"
        f"- Business model: {brief['business_model']}\n"
        f"- Pricing hypothesis: {brief['price']}\n"
        f"- Geography: {brief['geography']}\n"
        f"- Stage: {brief['stage']}\n"
    )

    files: Dict[str, str] = {}
    files["00-executive-brief.md"] = (
        f"""# Executive Brief\n\n{header}\n## Recommendation\n- Decision: [GO | CONDITIONAL GO | PIVOT | NO-GO]\n- Score: [0-100]\n- Confidence: [high | medium | low]\n\n## Why this decision\n- [Top reason 1]\n- [Top reason 2]\n- [Top reason 3]\n\n## Critical unknowns\n- [Unknown 1]\n- [Unknown 2]\n\n## 14-day validation plan\n1. [Experiment 1]\n2. [Experiment 2]\n3. [Experiment 3]\n"""
    )

    files["01-problem-customer-fit.md"] = (
        f"""# Problem and Customer Fit\n\n{header}\n## Core problem statement\n- [One sentence problem statement]\n\n## Customer segment definition\n- Primary segment: [segment]\n- Trigger moment: [when problem occurs]\n- Current workaround: [how they solve it today]\n\n## Pain evidence\n- Frequency: [daily/weekly/monthly]\n- Economic impact: [time/money/risk]\n- Behavioral evidence: [quotes, complaints, usage behavior]\n\n## Assumptions to validate\n- [Assumption 1]\n- [Assumption 2]\n- [Assumption 3]\n"""
    )

    files["02-market-opportunity.md"] = (
        """# Market Opportunity\n\n## TAM / SAM / SOM\n- TAM: [value] ([method])\n- SAM: [value] ([filters])\n- SOM (3-5y): [value] ([capture logic])\n\n## Methodology\n- Bottom-up approach: [details]\n- Top-down validation: [details]\n- Variance between methods: [percent]\n\n## Market dynamics\n- Growth rate (CAGR): [value]\n- Key trends: [trend 1], [trend 2], [trend 3]\n- Timing risk: [too early / right timing / too late]\n\n## Confidence and limits\n- Confidence: [high | medium | low]\n- Data gaps: [gap 1], [gap 2]\n"""
    )

    files["03-competitive-landscape.md"] = (
        """# Competitive Landscape\n\n## Competitor map\n- Direct competitors: [list]\n- Indirect/substitutes: [list]\n- Status quo alternatives: [list]\n\n## Comparison matrix\n| Factor | Us | Competitor A | Competitor B | Competitor C |\n|---|---|---|---|---|\n| Core capability | | | | |\n| Time-to-value | | | | |\n| Pricing model | | | | |\n| Switching friction | | | | |\n\n## Wedge and defensibility\n- Proposed wedge: [statement]\n- Why this is defendable: [reason]\n- Time-to-copy estimate: [months]\n\n## Strategic implication\n- [What this means for positioning and GTM]\n"""
    )

    files["04-business-model-unit-economics.md"] = (
        f"""# Business Model and Unit Economics\n\n## Revenue model\n- Model: {brief["business_model"]}\n- Pricing hypothesis: {brief["price"]}\n- Expansion paths: [upsell/cross-sell]\n\n## Unit economics baseline\n- CAC: [value]\n- LTV: [value]\n- LTV/CAC: [value]\n- Gross margin: [value]\n- Payback period: [months]\n\n## Economics risk points\n- [Risk 1]\n- [Risk 2]\n\n## Model revisions to test\n- [Revision 1]\n- [Revision 2]\n"""
    )

    files["05-go-to-market-plan.md"] = (
        """# Go-To-Market Plan\n\n## Beachhead segment\n- Primary segment: [segment]\n- Why this segment first: [rationale]\n\n## Channel strategy\n- Channel 1: [channel] -> [expected conversion]\n- Channel 2: [channel] -> [expected conversion]\n- Channel 3 (optional): [channel]\n\n## Messaging and offer\n- Positioning statement: [statement]\n- Core promise: [promise]\n- Initial offer: [offer]\n\n## 90-day funnel targets\n- Traffic/leads: [target]\n- Activation: [target]\n- Paid conversion: [target]\n- Retention: [target]\n"""
    )

    files["06-financial-scenarios.md"] = (
        """# Financial Scenarios\n\n## Scenario assumptions\n| Scenario | Growth | Churn | CAC | Gross Margin |\n|---|---|---|---|---|\n| Conservative | | | | |\n| Base | | | | |\n| Upside | | | | |\n\n## Outcome summary\n| Scenario | 12-Month Revenue | Burn | Runway |\n|---|---|---|---|\n| Conservative | | | |\n| Base | | | |\n| Upside | | | |\n\n## Break conditions\n- [Condition that breaks model 1]\n- [Condition that breaks model 2]\n"""
    )

    files["07-validation-experiments.md"] = (
        """# Validation Experiments\n\n## Prioritization rule\nPrioritize assumptions by: impact if wrong x uncertainty.\n\n## Experiment backlog\n| ID | Assumption | Test | Success threshold | Cost | Duration |\n|---|---|---|---|---|---|\n| E1 | | | | | |\n| E2 | | | | | |\n| E3 | | | | | |\n\n## Next 14 days\n1. [Day 1-3 experiment]\n2. [Day 4-7 experiment]\n3. [Day 8-14 experiment]\n"""
    )

    files["08-risk-register.md"] = (
        """# Risk Register\n\n| Risk | Probability | Impact | Early Signal | Mitigation | Owner |\n|---|---|---|---|---|---|\n| Market adoption | | | | | |\n| Competitive response | | | | | |\n| Unit economics failure | | | | | |\n| Execution bandwidth | | | | | |\n"""
    )

    files["09-90-day-execution-plan.md"] = (
        """# 90-Day Execution Plan\n\n## Month 1: Validate\n- [Task]\n- [Task]\n\n## Month 2: Build and launch\n- [Task]\n- [Task]\n\n## Month 3: Improve and decide\n- [Task]\n- [Task]\n\n## Decision checkpoint\n- Continue criteria: [criteria]\n- Pivot criteria: [criteria]\n- Stop criteria: [criteria]\n"""
    )

    files["assumptions-log.md"] = (
        """# Assumptions Log\n\n| Assumption | Status (known/inferred/untested) | Evidence | Last Updated |\n|---|---|---|---|\n| | | | |\n| | | | |\n"""
    )

    files["sources-and-evidence.md"] = (
        """# Sources and Evidence\n\nUse one line per source.\n\n| Claim Supported | Source | Type | Date | Quality (A/B/C) |\n|---|---|---|---|---|\n| | | | | |\n| | | | | |\n"""
    )

    return files


def write_casepack(
    target_dir: Path, files: Dict[str, str], brief: Dict[str, str]
) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)

    for file_name in FILE_ORDER:
        path = target_dir / file_name
        path.write_text(files[file_name], encoding="utf-8")

    (target_dir / "startup-brief.json").write_text(
        json.dumps(brief, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate startup analysis case pack")
    parser.add_argument("--idea", help="Startup idea summary")
    parser.add_argument("--customer", help="Target customer segment")
    parser.add_argument("--problem", help="Core problem statement")
    parser.add_argument("--solution", help="Proposed solution summary")
    parser.add_argument("--business-model", help="Revenue/business model")
    parser.add_argument("--price", help="Pricing hypothesis")
    parser.add_argument("--geography", help="Target geography")
    parser.add_argument("--stage", help="Startup stage", default="idea")
    parser.add_argument("--founder", help="Founder/team context")
    parser.add_argument("--notes", help="Additional notes")
    parser.add_argument("--from-json", help="Path to JSON brief")
    parser.add_argument("--slug", help="Folder slug for the case pack")
    parser.add_argument(
        "--output-dir",
        help="Parent output directory",
        default="./outputs",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    brief = load_brief(args)

    slug = args.slug or slugify(brief["idea"])
    target_dir = Path(args.output_dir) / slug

    files = build_files(brief)
    write_casepack(target_dir, files, brief)

    print(f"Created case pack at: {target_dir}")
    print("Generated files:")
    for file_name in FILE_ORDER:
        print(f"- {file_name}")
    print("- startup-brief.json")


if __name__ == "__main__":
    main()
