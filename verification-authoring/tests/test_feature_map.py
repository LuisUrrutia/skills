import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "check-feature-map.py"
FEATURE = """# Save

Save a note and reopen it.

## Sub-features

- save: persist a note.

## How to get to it (user POV)

Use the save command.

## Driving it with Note CLI

```sh
note save --text example
```

## Gotchas

Use an isolated data directory.
"""


class FeatureMapTests(unittest.TestCase):
    def setUp(self):
        scratch = Path(__file__).resolve().parents[2] / ".tmp" / "verification-skills" / "unit"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name)
        self.features = self.skill / "features"
        self.features.mkdir()
        self.index = self.features / "README.md"
        self.index.write_text("# Features\n\n## Features\n\n- [Save](save.md)\n", encoding="utf-8")
        (self.features / "save.md").write_text(FEATURE, encoding="utf-8")

    def run_check(self):
        result = subprocess.run([sys.executable, str(CHECKER), "--skill-dir", str(self.skill)], capture_output=True, text=True, check=False)
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout)

    def assert_defect(self, code, exit_code=1):
        actual, output = self.run_check()
        self.assertEqual(actual, exit_code)
        self.assertFalse(output["valid"])
        self.assertIn(code, [item["code"] for item in output["diagnostics"]])

    def test_valid_map_is_read_only(self):
        before = {p.relative_to(self.skill): p.read_bytes() for p in self.skill.rglob("*") if p.is_file()}
        code, output = self.run_check()
        self.assertEqual(code, 0)
        self.assertEqual(output["features"], ["save.md"])
        self.assertEqual(output["diagnostics"], [])
        self.assertEqual(before, {p.relative_to(self.skill): p.read_bytes() for p in self.skill.rglob("*") if p.is_file()})

    def test_duplicate_and_missing_links(self):
        with self.index.open("a") as stream:
            stream.write("- [Again](save.md#save)\n- [Lost](lost.md)\n")
        self.assert_defect("duplicate-link")
        self.assert_defect("missing-feature")

    def test_orphan_file(self):
        (self.features / "search.md").write_text(FEATURE, encoding="utf-8")
        self.assert_defect("unindexed-feature")

    def test_missing_index_is_unreadable(self):
        self.index.unlink()
        self.assert_defect("unreadable", 2)

    def test_invalid_encoding_is_unreadable(self):
        (self.features / "save.md").write_bytes(b"\xff")
        self.assert_defect("unreadable", 2)

    def test_links_must_be_local_siblings(self):
        for target in ["../outside.md", "https://example.test/a.md", "nested/a.md", "README.md", "a%20b.md"]:
            with self.subTest(target=target):
                self.index.write_text(f"## Features\n\n- [Save]({target})\n", encoding="utf-8")
                self.assert_defect("invalid-link")

    def test_symlink_cannot_escape_feature_directory(self):
        target = self.skill / "outside.md"
        target.write_text(FEATURE, encoding="utf-8")
        (self.features / "save.md").unlink()
        (self.features / "save.md").symlink_to(target)
        self.assert_defect("escaping-link")

    def test_code_fences_do_not_supply_headings_or_links(self):
        self.index.write_text("## Features\n```md\n- [Save](save.md)\n```\n", encoding="utf-8")
        self.assert_defect("empty-index")

    def test_sections_are_required_and_ordered(self):
        (self.features / "save.md").write_text(FEATURE.replace("## Sub-features", "## Incorrect"), encoding="utf-8")
        self.assert_defect("feature-sections")

    def test_harness_must_be_named(self):
        (self.features / "save.md").write_text(FEATURE.replace("Note CLI", "<real harness name>"), encoding="utf-8")
        self.assert_defect("harness-placeholder")

    def test_empty_sections_are_reported(self):
        (self.features / "save.md").write_text(FEATURE.replace("Use an isolated data directory.", ""), encoding="utf-8")
        self.assert_defect("empty-section")


if __name__ == "__main__":
    unittest.main()
