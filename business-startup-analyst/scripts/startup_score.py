#!/usr/bin/env python3
"""
Compute weighted startup viability score from JSON inputs.

Input format:
{
  "scores": {
    "problem": 0-10,
    "market": 0-10,
    "differentiation": 0-10,
    "economics": 0-10,
    "gtm": 0-10,
    "execution": 0-10
  },
  "notes": {
    "problem": "optional note"
  }
}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Tuple


WEIGHTS = {
    "problem": 0.20,
    "market": 0.20,
    "differentiation": 0.15,
    "economics": 0.20,
    "gtm": 0.15,
    "execution": 0.10,
}


def clamp_score(value: float) -> float:
    return max(0.0, min(10.0, value))


def parse_input(path: Path) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise ValueError("Input file must be a JSON object.")

    raw_scores = payload.get("scores", payload)
    if not isinstance(raw_scores, dict):
        raise ValueError("`scores` must be an object.")

    scores: Dict[str, float] = {}
    for key in WEIGHTS:
        value = raw_scores.get(key, 0)
        try:
            score = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid score for `{key}`: {value}") from exc
        scores[key] = clamp_score(score)

    notes = payload.get("notes", {})
    if not isinstance(notes, dict):
        notes = {}

    return {"scores": scores, "notes": notes}


def compute_weighted_score(scores: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
    weighted_by_dimension: Dict[str, float] = {}
    total = 0.0

    for key, weight in WEIGHTS.items():
        weighted_points = scores[key] * weight * 10
        weighted_by_dimension[key] = round(weighted_points, 2)
        total += weighted_points

    return round(total, 2), weighted_by_dimension


def recommendation(score: float) -> str:
    if score >= 75:
        return "GO"
    if score >= 60:
        return "CONDITIONAL GO"
    if score >= 45:
        return "PIVOT"
    return "NO-GO"


def confidence(scores: Dict[str, float]) -> str:
    low_dims = [k for k, v in scores.items() if v < 4]
    high_dims = [k for k, v in scores.items() if v >= 7]

    if len(low_dims) >= 2:
        return "low"
    if len(high_dims) >= 4 and len(low_dims) == 0:
        return "high"
    return "medium"


def markdown_report(
    scores: Dict[str, float],
    weighted: Dict[str, float],
    total: float,
    notes: Dict[str, str],
) -> str:
    reco = recommendation(total)
    conf = confidence(scores)

    lines = [
        "# Startup Viability Score",
        "",
        f"- Recommendation: **{reco}**",
        f"- Weighted score: **{total}/100**",
        f"- Confidence: **{conf}**",
        "",
        "## Dimension Breakdown",
        "",
        "| Dimension | Raw (0-10) | Weight | Weighted Points |",
        "|---|---:|---:|---:|",
    ]

    for key, weight in WEIGHTS.items():
        lines.append(
            f"| {key} | {scores[key]:.1f} | {int(weight * 100)}% | {weighted[key]:.2f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- GO: strong evidence to execute and scale testing",
            "- CONDITIONAL GO: execute, but only after resolving top assumptions",
            "- PIVOT: core changes needed in segment/problem/model",
            "- NO-GO: stop current direction and redeploy effort",
        ]
    )

    if notes:
        lines.extend(["", "## Notes"])
        for key in WEIGHTS:
            note = notes.get(key)
            if note:
                lines.append(f"- {key}: {note}")

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score startup viability")
    parser.add_argument("input", help="Path to scoring JSON")
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format",
    )
    parser.add_argument("--output", help="Optional output file path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = parse_input(Path(args.input))
    scores = payload["scores"]
    notes = payload["notes"]

    total, weighted = compute_weighted_score(scores)
    reco = recommendation(total)
    conf = confidence(scores)

    result_json = {
        "recommendation": reco,
        "score": total,
        "confidence": conf,
        "scores": scores,
        "weighted_points": weighted,
    }

    if args.format == "json":
        rendered = json.dumps(result_json, indent=2)
    else:
        rendered = markdown_report(scores, weighted, total, notes)

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
        print(f"Wrote output to: {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
