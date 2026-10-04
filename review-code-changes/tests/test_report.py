import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
ROOT = SKILL.parent
spec = importlib.util.spec_from_file_location("review_report", SKILL / "scripts/report.py")
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)

VALID = """# Code change review

Scope: `base...head`

## Review basis

The export request requires tenant isolation. The local standard assigns it to the query boundary.

## Findings

### F1 | high | export.py:12 | Export returns another tenant's records

Class: security
Action: required
Affected: Export callers with records belonging to more than one tenant.
Diff cause: The new query omits the tenant predicate.
Impact: Another tenant's data appears in the export.
Evidence:
- producer | `export.py:12` | The query requests all rows.
- consumer | `export.py:18` | Every returned row is serialized.
Recommendation: Apply the tenant predicate before reading rows.
Unresolved premise: None.

## Open questions

None.

## Checks

- not-run | `application integration` | No service is available in this fixture.

## Coverage

- reviewed | `export.py` | Query and serialization traced.
"""


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scratch = ROOT / ".tmp/review-code-changes-tests"
        subprocess.run(["git", "check-ignore", "--quiet", str(cls.scratch)], cwd=ROOT, check=True)
        cls.scratch.mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        cls.scratch.rmdir()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=self.scratch)
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.source = self.directory / "review.md"
        self.source.write_text(VALID)
        self.inventory = self.directory / "paths.json"
        self.inventory.write_text(json.dumps(["export.py"]))

    def validate(self, text=None):
        if text is not None:
            self.source.write_text(text)
        return report.validate_report(self.source, self.inventory)

    def test_evidenced_finding_matches_declared_coverage(self):
        self.assertEqual(self.validate(), ("base...head", 1))

    def test_missing_or_extra_coverage_is_rejected(self):
        for paths in [["export.py", "schema.py"], []]:
            with self.subTest(paths=paths):
                self.inventory.write_text(json.dumps(paths))
                with self.assertRaisesRegex(report.ReportError, "differs from inventory"):
                    self.validate()

    def test_duplicate_inventory_is_rejected(self):
        self.inventory.write_text('["export.py", "export.py"]')
        with self.assertRaisesRegex(report.ReportError, "duplicates"):
            self.validate()

    def test_partial_coverage_and_open_question_remain_visible(self):
        text = VALID.replace("- reviewed |", "- partial |")
        text = text.replace("## Open questions\n\nNone.", "## Open questions\n\n### Q1 | remote service | Which schema revision is deployed?\n\nNeeded evidence: The caller-owned deployment revision.")
        self.validate(text)
        output = self.directory / "review.html"
        report.render_report(self.source, output, self.inventory)
        self.assertIn("partial |", output.read_text())
        self.assertIn("caller-owned deployment", output.read_text())

    def test_empty_diff_requires_empty_inventory(self):
        text = VALID[:VALID.index("### F1")] + VALID[VALID.index("## Open questions"):]
        text = text.replace("## Findings\n\n", "## Findings\n\nNone.\n\n")
        text = text[:text.index("## Coverage")] + "## Coverage\n\nNone.\n"
        self.inventory.write_text("[]")
        self.assertEqual(self.validate(text), ("base...head", 0))
        self.inventory.write_text('["export.py"]')
        with self.assertRaises(report.ReportError):
            self.validate()

    def test_finding_without_trace_is_rejected(self):
        text = "\n".join(line for line in VALID.splitlines() if not line.startswith(("- producer", "- consumer")))
        with self.assertRaisesRegex(report.ReportError, "evidence"):
            self.validate(text)

    def test_empty_impact_or_remedy_is_rejected(self):
        for prefix in ["Impact:", "Recommendation:"]:
            text = "\n".join(prefix if line.startswith(prefix) else line for line in VALID.splitlines())
            with self.subTest(field=prefix), self.assertRaisesRegex(report.ReportError, "empty"):
                self.validate(text)

    def test_duplicate_sections_are_rejected(self):
        with self.assertRaisesRegex(report.ReportError, "exactly once"):
            self.validate(VALID + "\n## Findings\n\nNone.\n")

    def test_required_and_optional_are_explicit(self):
        self.validate(VALID.replace("Action: required", "Action: optional"))
        with self.assertRaisesRegex(report.ReportError, "Action"):
            self.validate(VALID.replace("Action: required", "Action: maybe"))

    def test_render_escapes_review_data_and_copies_external_style(self):
        self.source.write_text(VALID.replace("The query requests all rows.", '<script>alert("x")</script>'))
        output = self.directory / "review.html"
        self.assertEqual(report.render_report(self.source, output, self.inventory), 1)
        self.assertIn('&lt;script&gt;', output.read_text())
        self.assertNotIn('<script>', output.read_text())
        self.assertIn('href="review.css"', output.read_text())
        self.assertEqual(output.with_suffix('.css').read_bytes(), (SKILL / 'assets/report.css').read_bytes())

    def test_render_cannot_overwrite_canonical_report(self):
        for output in [self.source, self.source.with_suffix(".css")]:
            with self.subTest(output=output), self.assertRaises(report.ReportError):
                report.render_report(self.source, output, self.inventory)
        self.assertEqual(self.source.read_text(), VALID)

    def test_cli_returns_failure_without_rendering_invalid_report(self):
        self.source.write_text(VALID.replace("Impact:", "Missing impact:"))
        output = self.directory / "review.html"
        result = subprocess.run([sys.executable, str(SKILL / "scripts/report.py"), "render", str(self.source), str(output), "--changed-paths", str(self.inventory)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(output.exists())
        self.assertIn("invalid code change review", result.stderr)


if __name__ == "__main__":
    unittest.main()
