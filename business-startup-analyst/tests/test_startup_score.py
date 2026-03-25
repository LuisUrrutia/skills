import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tests.script_loader import load_script_module


startup_score = load_script_module("startup_score.py")


def write_json(path: Path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")


class StartupScoreTests(unittest.TestCase):
    def test_clamp_score_bounds_values(self):
        self.assertEqual(startup_score.clamp_score(-5), 0.0)
        self.assertEqual(startup_score.clamp_score(12), 10.0)
        self.assertEqual(startup_score.clamp_score(7.25), 7.25)

    def test_parse_input_handles_scores_and_clamps_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "score.json"
            write_json(
                input_path,
                {
                    "scores": {
                        "problem": 9,
                        "market": "11",
                        "differentiation": -2,
                        "economics": 7.5,
                    },
                    "notes": {"problem": "strong interview signal"},
                },
            )

            payload = startup_score.parse_input(input_path)

        scores = payload["scores"]
        self.assertEqual(scores["problem"], 9.0)
        self.assertEqual(scores["market"], 10.0)
        self.assertEqual(scores["differentiation"], 0.0)
        self.assertEqual(scores["gtm"], 0.0)
        self.assertEqual(payload["notes"], {"problem": "strong interview signal"})

    def test_parse_input_supports_scores_at_root_level(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "score.json"
            write_json(
                input_path,
                {
                    "problem": 8,
                    "market": 7,
                    "differentiation": 6,
                    "economics": 5,
                    "gtm": 4,
                    "execution": 3,
                },
            )

            payload = startup_score.parse_input(input_path)

        self.assertEqual(payload["scores"]["problem"], 8.0)
        self.assertEqual(payload["scores"]["execution"], 3.0)

    def test_parse_input_rejects_invalid_payload_shapes_and_types(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            list_path = Path(temp_dir) / "list.json"
            scores_path = Path(temp_dir) / "scores_list.json"
            invalid_value_path = Path(temp_dir) / "invalid_value.json"

            write_json(list_path, ["invalid"])
            write_json(scores_path, {"scores": [1, 2, 3]})
            write_json(invalid_value_path, {"scores": {"problem": "bad"}})

            with self.assertRaisesRegex(ValueError, "Input file must be a JSON object"):
                startup_score.parse_input(list_path)
            with self.assertRaisesRegex(ValueError, "`scores` must be an object"):
                startup_score.parse_input(scores_path)
            with self.assertRaisesRegex(ValueError, "Invalid score for `problem`"):
                startup_score.parse_input(invalid_value_path)

    def test_parse_input_ignores_non_object_notes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "score.json"
            write_json(input_path, {"scores": {"problem": 6}, "notes": "text"})

            payload = startup_score.parse_input(input_path)

        self.assertEqual(payload["notes"], {})

    def test_compute_weighted_score_returns_total_and_dimension_points(self):
        scores = {
            "problem": 10,
            "market": 10,
            "differentiation": 10,
            "economics": 10,
            "gtm": 10,
            "execution": 10,
        }

        total, weighted = startup_score.compute_weighted_score(scores)

        self.assertEqual(total, 100.0)
        self.assertEqual(weighted["problem"], 20.0)
        self.assertEqual(weighted["differentiation"], 15.0)
        self.assertEqual(weighted["execution"], 10.0)

    def test_recommendation_thresholds(self):
        self.assertEqual(startup_score.recommendation(75), "GO")
        self.assertEqual(startup_score.recommendation(74.99), "CONDITIONAL GO")
        self.assertEqual(startup_score.recommendation(60), "CONDITIONAL GO")
        self.assertEqual(startup_score.recommendation(59.99), "PIVOT")
        self.assertEqual(startup_score.recommendation(45), "PIVOT")
        self.assertEqual(startup_score.recommendation(44.99), "NO-GO")

    def test_confidence_levels(self):
        self.assertEqual(
            startup_score.confidence(
                {
                    "problem": 8,
                    "market": 8,
                    "differentiation": 7,
                    "economics": 7,
                    "gtm": 6,
                    "execution": 6,
                }
            ),
            "high",
        )
        self.assertEqual(
            startup_score.confidence(
                {
                    "problem": 3,
                    "market": 2,
                    "differentiation": 8,
                    "economics": 8,
                    "gtm": 8,
                    "execution": 8,
                }
            ),
            "low",
        )
        self.assertEqual(
            startup_score.confidence(
                {
                    "problem": 6,
                    "market": 7,
                    "differentiation": 5,
                    "economics": 6,
                    "gtm": 6,
                    "execution": 6,
                }
            ),
            "medium",
        )

    def test_markdown_report_contains_breakdown_and_filtered_notes(self):
        scores = {
            "problem": 8.0,
            "market": 7.0,
            "differentiation": 6.0,
            "economics": 7.5,
            "gtm": 5.0,
            "execution": 6.0,
        }
        total, weighted = startup_score.compute_weighted_score(scores)
        report = startup_score.markdown_report(
            scores,
            weighted,
            total,
            {"problem": "interviews completed", "unknown": "ignore me"},
        )

        self.assertIn("# Startup Viability Score", report)
        self.assertIn("| problem | 8.0 | 20% |", report)
        self.assertIn("## Notes", report)
        self.assertIn("- problem: interviews completed", report)
        self.assertNotIn("unknown", report)

    def test_main_renders_json_to_output_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.json"
            output_path = Path(temp_dir) / "result.json"
            write_json(
                input_path,
                {
                    "scores": {
                        "problem": 8,
                        "market": 8,
                        "differentiation": 7,
                        "economics": 8,
                        "gtm": 7,
                        "execution": 7,
                    }
                },
            )

            args = SimpleNamespace(
                input=str(input_path), format="json", output=str(output_path)
            )

            with patch.object(startup_score, "parse_args", return_value=args):
                startup_score.main()

            output = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(output["recommendation"], "GO")
        self.assertIn("weighted_points", output)

    def test_main_prints_markdown_when_no_output_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.json"
            write_json(input_path, {"scores": {"problem": 5}})

            args = SimpleNamespace(
                input=str(input_path), format="markdown", output=None
            )
            stdout = StringIO()

            with patch.object(startup_score, "parse_args", return_value=args):
                with redirect_stdout(stdout):
                    startup_score.main()

        output = stdout.getvalue()
        self.assertIn("# Startup Viability Score", output)
        self.assertIn("- Recommendation:", output)


if __name__ == "__main__":
    unittest.main()
