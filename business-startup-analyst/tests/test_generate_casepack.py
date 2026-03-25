import argparse
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from tests.script_loader import load_script_module


generate_casepack = load_script_module("generate_casepack.py")


def make_args(**overrides):
    defaults = {
        "idea": None,
        "customer": None,
        "problem": None,
        "solution": None,
        "business_model": None,
        "price": None,
        "geography": None,
        "stage": None,
        "founder": None,
        "notes": None,
        "from_json": None,
        "slug": None,
        "output_dir": "./outputs",
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


class GenerateCasepackTests(unittest.TestCase):
    def test_slugify_normalizes_and_falls_back(self):
        self.assertEqual(
            generate_casepack.slugify("  AI & SMB -- Tool_Kit  "),
            "ai-smb-toolkit",
        )
        self.assertEqual(generate_casepack.slugify("!!!"), "startup-idea")

    def test_load_brief_applies_defaults_for_missing_fields(self):
        brief = generate_casepack.load_brief(make_args(idea="AI finance copilot"))

        self.assertEqual(brief["idea"], "AI finance copilot")
        self.assertEqual(brief["stage"], "idea")
        self.assertEqual(brief["customer"], "[Define target customer]")
        self.assertEqual(brief["notes"], "")

    def test_load_brief_merges_json_and_cli_with_cli_precedence(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            brief_path = Path(temp_dir) / "brief.json"
            brief_path.write_text(
                json.dumps(
                    {
                        "idea": "Original idea",
                        "customer": "Original customer",
                        "problem": "Pain point",
                    }
                ),
                encoding="utf-8",
            )

            args = make_args(
                from_json=str(brief_path),
                customer="CLI customer",
                geography="Mexico",
            )
            brief = generate_casepack.load_brief(args)

        self.assertEqual(brief["idea"], "Original idea")
        self.assertEqual(brief["customer"], "CLI customer")
        self.assertEqual(brief["geography"], "Mexico")

    def test_load_brief_requires_idea(self):
        with self.assertRaisesRegex(ValueError, "`idea` is required"):
            generate_casepack.load_brief(make_args())

    def test_load_brief_rejects_non_object_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            brief_path = Path(temp_dir) / "brief.json"
            brief_path.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Input JSON must be an object"):
                generate_casepack.load_brief(make_args(from_json=str(brief_path)))

    def test_build_files_returns_expected_set_and_includes_brief_values(self):
        brief = {
            "idea": "Ledger automation",
            "customer": "Small firms",
            "problem": "Manual close",
            "solution": "AI workflows",
            "business_model": "SaaS",
            "price": "$299/mo",
            "geography": "US",
            "stage": "pre-seed",
            "founder": "Solo founder",
            "notes": "",
        }

        files = generate_casepack.build_files(brief)

        self.assertEqual(set(files.keys()), set(generate_casepack.FILE_ORDER))
        self.assertIn("- Idea: Ledger automation", files["00-executive-brief.md"])
        self.assertIn("Model: SaaS", files["04-business-model-unit-economics.md"])

    def test_write_casepack_writes_all_expected_files_and_json_brief(self):
        brief = {
            "idea": "Ops assistant",
            "customer": "B2B SaaS",
            "problem": "Slow support",
            "solution": "Automation",
            "business_model": "Subscription",
            "price": "$99",
            "geography": "US",
            "stage": "idea",
            "founder": "Team",
            "notes": "",
        }
        files = generate_casepack.build_files(brief)

        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = Path(temp_dir) / "casepack"
            generate_casepack.write_casepack(target_dir, files, brief)

            for file_name in generate_casepack.FILE_ORDER:
                self.assertTrue((target_dir / file_name).is_file(), file_name)

            persisted_brief = json.loads(
                (target_dir / "startup-brief.json").read_text(encoding="utf-8")
            )
            self.assertEqual(persisted_brief, brief)

    def test_main_uses_slugified_idea_when_slug_not_provided(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            args = make_args(
                idea="AI Assistant for Bookkeepers",
                output_dir=temp_dir,
                stage="idea",
            )
            stdout = StringIO()

            with patch.object(generate_casepack, "parse_args", return_value=args):
                with redirect_stdout(stdout):
                    generate_casepack.main()

            expected_path = Path(temp_dir) / "ai-assistant-for-bookkeepers"
            self.assertTrue(expected_path.is_dir())
            output = stdout.getvalue()
            self.assertIn(f"Created case pack at: {expected_path}", output)
            self.assertIn("- startup-brief.json", output)

    def test_main_uses_explicit_slug_when_provided(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            args = make_args(
                idea="Any idea",
                slug="custom-slug",
                output_dir=temp_dir,
                stage="idea",
            )

            with patch.object(generate_casepack, "parse_args", return_value=args):
                generate_casepack.main()

            expected_path = Path(temp_dir) / "custom-slug"
            self.assertTrue(expected_path.is_dir())


if __name__ == "__main__":
    unittest.main()
