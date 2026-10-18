import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "check-origin.py"
COMMIT_A = "a" * 40
COMMIT_B = "b" * 40
SKILL = """---
name: demo
description: Demo skill.
---

# Demo

## Launch

Start it.

```md
## Fenced heading
```

## Report

Cite evidence.

## Report

A repeated heading gets a numbered anchor.
"""
HEADER = """format_version = 2
skill = "demo"
created = "2026-10-17"
approach = "{approach}"
goal = "Prove a change with evidence that survives cleanup."
"""
SOURCE = f"""
[[sources]]
id = "{{id}}"
repository = "https://github.com/example/skills"
remote = "git@github.com:example/skills.git"
ref = "refs/heads/main"
license = "MIT; notice retained in THIRD-PARTY-NOTICES.txt"
role = "{{role}}"
baseline_commit = "{COMMIT_A}"
reviewed_through = "{COMMIT_B}"
baseline_paths = ["skills/demo/SKILL.md"]
paths = ["skills/demo/SKILL.md"]
"""
IDEA = """
[[sources.ideas]]
idea = "A claim needs evidence captured after the last change."
serves = "Prevents reporting success from stale output."
where = ["SKILL.md#report"]
shapes = "The report requires each claim to cite this run's evidence; package.json scripts stay the caller's workload."
"""
DEVIATION = """
[[sources.deviations]]
change = "Replaced generating a project skill with running the steps directly."
reason = "The user verifies work without creating a skill."
where = ["SKILL.md#launch"]
"""
REVIEW = f"""
[[sources.reviews]]
from_commit = "{COMMIT_A}"
to_commit = "{COMMIT_B}"
incorporated = []
skipped = ["Wording only."]
deferred = []
validation = ["Read the scoped diff."]
"""
SNAPSHOT_IDEA = """
[[local_snapshots.ideas]]
idea = "A claim needs evidence."
serves = "Prevents stale claims."
where = ["SKILL.md#report"]
shapes = "The report cites evidence."
"""


def ideas_source(source_id="donor"):
    return SOURCE.format(id=source_id, role="ideas") + IDEA + REVIEW


def base_source(source_id="donor"):
    return SOURCE.format(id=source_id, role="base") + DEVIATION + REVIEW


class CheckOriginTest(unittest.TestCase):
    def check(self, record, name="demo", files=None):
        with tempfile.TemporaryDirectory() as directory:
            skill_dir = Path(directory) / name
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(SKILL, encoding="utf-8")
            (skill_dir / "THIRD-PARTY-NOTICES.txt").write_text("MIT\n", encoding="utf-8")
            for relative, text in (files or {}).items():
                if text is None:
                    (skill_dir / relative).unlink()
                else:
                    (skill_dir / relative).write_text(text, encoding="utf-8")
            if record is not None:
                (skill_dir / "origin.toml").write_text(record, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CHECKER), "--skill-dir", str(skill_dir)],
                capture_output=True,
                text=True,
                check=False,
            )
            codes = [item["code"] for item in json.loads(result.stdout)["diagnostics"]]
            return result.returncode, codes

    def test_valid_ideas_source_passes(self):
        returncode, codes = self.check(HEADER.format(approach="derive") + ideas_source())

        self.assertEqual((returncode, codes), (0, []))

    def test_valid_base_source_passes(self):
        returncode, codes = self.check(HEADER.format(approach="base") + base_source() + ideas_source("other"))

        self.assertEqual((returncode, codes), (0, []))

    def test_base_source_needs_a_notice_file(self):
        _, codes = self.check(HEADER.format(approach="base") + base_source(), files={"THIRD-PARTY-NOTICES.txt": None})

        self.assertEqual(codes, ["missing-notice"])

    def test_invariants_are_rules_with_optional_reason_and_location(self):
        invariants = """
[[invariants]]
rule = "Never approve a head that was not reviewed."
reason = "Approving an unreviewed head was the observed failure."
where = ["SKILL.md#report"]

[[invariants]]
rule = "Stop on approval outside personal repositories."
"""
        bad = '\n[[invariants]]\nreason = "No rule."\n'

        returncode, codes = self.check(HEADER.format(approach="derive") + invariants + ideas_source())
        _, bad_codes = self.check(HEADER.format(approach="derive") + bad + ideas_source())

        self.assertEqual((returncode, codes), (0, []))
        self.assertEqual(bad_codes, ["missing-key"])

    def test_format_one_fields_are_reported(self):
        record = HEADER.format(approach="derive") + SOURCE.format(id="donor", role="ideas") + 'borrowed = ["x"]\nlocal_choices = ["y"]\n' + IDEA + REVIEW

        returncode, codes = self.check(record)

        self.assertEqual(returncode, 1)
        self.assertEqual(codes.count("legacy-key"), 2)

    def test_legacy_file_is_reported_alone_or_beside_the_record(self):
        returncode, codes = self.check(None, files={"origin.txt": "format_version = 1\n"})
        _, both = self.check(HEADER.format(approach="derive") + ideas_source(), files={"origin.txt": "format_version = 1\n"})

        self.assertEqual((returncode, codes), (1, ["legacy-file"]))
        self.assertEqual(both, ["stale-legacy-file"])

    def test_two_bases_are_rejected(self):
        record = HEADER.format(approach="base") + base_source() + base_source("other")

        _, codes = self.check(record)

        self.assertIn("multiple-bases", codes)
        self.assertIn("approach-mismatch", codes)

    def test_approach_must_match_the_records(self):
        _, base_role = self.check(HEADER.format(approach="derive") + base_source())
        _, create_with_sources = self.check(HEADER.format(approach="create") + ideas_source())
        returncode, create_alone = self.check(HEADER.format(approach="create"))

        self.assertEqual(base_role, ["approach-mismatch", "approach-mismatch"])
        self.assertEqual(create_with_sources, ["approach-mismatch"])
        self.assertEqual((returncode, create_alone), (0, []))

    def test_roles_keep_their_own_tables(self):
        _, codes = self.check(HEADER.format(approach="base") + SOURCE.format(id="donor", role="base") + IDEA + REVIEW)

        self.assertIn("role-mismatch", codes)

    def test_idea_needs_every_field(self):
        idea = '\n[[sources.ideas]]\nidea = "Evidence first."\nshapes = "Changed the report section."\n'

        _, codes = self.check(HEADER.format(approach="derive") + SOURCE.format(id="donor", role="ideas") + idea + REVIEW)

        self.assertEqual(codes, ["missing-key", "missing-key"])

    def test_locations_and_anchors_must_exist(self):
        idea = ideas_source().replace("SKILL.md#report", "SKILL.md#fenced-heading")
        deviation = base_source().replace("SKILL.md#launch", "references/missing.md")

        _, idea_codes = self.check(HEADER.format(approach="derive") + idea)
        _, base_codes = self.check(HEADER.format(approach="base") + deviation)

        self.assertEqual(idea_codes, ["missing-anchor"])
        self.assertEqual(base_codes, ["missing-location"])

    def test_repeated_headings_and_whole_files_are_valid_locations(self):
        record = HEADER.format(approach="derive") + ideas_source().replace('["SKILL.md#report"]', '["SKILL.md#report-1", "SKILL.md"]')

        returncode, codes = self.check(record)

        self.assertEqual((returncode, codes), (0, []))

    def test_location_cannot_escape_the_skill(self):
        _, codes = self.check(HEADER.format(approach="derive") + ideas_source().replace("SKILL.md#report", "../other/SKILL.md"))

        self.assertIn("escaping-location", codes)

    def test_review_chain_must_reach_the_cursor(self):
        reversed_review = REVIEW.replace(COMMIT_A, "c" * 40).replace(COMMIT_B, COMMIT_A).replace("c" * 40, COMMIT_B)
        no_review = SOURCE.format(id="donor", role="ideas") + IDEA

        _, reversed_codes = self.check(HEADER.format(approach="derive") + SOURCE.format(id="donor", role="ideas") + IDEA + reversed_review)
        _, missing_codes = self.check(HEADER.format(approach="derive") + no_review)

        self.assertEqual(reversed_codes, ["review-chain", "review-chain"])
        self.assertEqual(missing_codes, ["review-chain"])

    def test_pending_review_starts_at_the_cursor(self):
        source = SOURCE.format(id="donor", role="ideas").replace(f'reviewed_through = "{COMMIT_B}"', f'reviewed_through = "{COMMIT_A}"')
        pending = REVIEW.replace("deferred = []", 'deferred = ["A new lint tool needs the user\'s decision."]')

        returncode, codes = self.check(HEADER.format(approach="derive") + source + IDEA + pending)
        _, advanced = self.check(HEADER.format(approach="derive") + SOURCE.format(id="donor", role="ideas") + IDEA + pending)

        self.assertEqual((returncode, codes), (0, []))
        self.assertEqual(advanced, ["review-chain", "review-chain"])

    def test_line_citations_and_short_commits_are_rejected(self):
        review = REVIEW.replace('"Wording only."', '"Conflicts with demo/origin.toml:18."').replace(f'from_commit = "{COMMIT_A}"', 'from_commit = "abc123"')

        _, codes = self.check(HEADER.format(approach="derive") + SOURCE.format(id="donor", role="ideas") + IDEA + review)

        self.assertIn("line-citation", codes)
        self.assertIn("invalid-value", codes)

    def test_fields_over_one_hundred_words_are_reported(self):
        at_limit = " ".join(["word"] * 100)
        record = HEADER.format(approach="create") + f'\n[[invariants]]\nrule = "{at_limit}"\nreason = "{at_limit} more"\n'

        _, codes = self.check(record)

        self.assertEqual(codes, ["long-entry"])

    def test_malformed_types_are_reported_without_crashing(self):
        record = HEADER.format(approach="derive").replace('approach = "derive"', "approach = []").replace(
            'goal = "Prove a change with evidence that survives cleanup."', "goal = 42"
        ) + ideas_source().replace('idea = "A claim needs evidence captured after the last change."', "idea = []")

        returncode, codes = self.check(record)

        self.assertEqual(returncode, 1)
        self.assertEqual(codes.count("invalid-value"), 3)

    def test_source_paths_cannot_be_empty(self):
        _, codes = self.check(HEADER.format(approach="derive") + ideas_source().replace('paths = ["skills/demo/SKILL.md"]', "paths = []"))

        self.assertEqual(codes, ["invalid-value", "invalid-value"])

    def test_malformed_kinds_are_reported_without_crashing(self):
        snapshot = '\n[[local_snapshots]]\nid = "copy"\nkind = []\n'
        dependency = '\n[[dependencies]]\nkind = {}\nname = "verify"\nrequired = true\nrole = "Checks evidence."\n'

        returncode, codes = self.check(HEADER.format(approach="derive") + ideas_source() + snapshot + dependency)

        self.assertEqual(returncode, 1)
        self.assertEqual(codes.count("invalid-value"), 2)

    def test_linked_and_setext_headings_have_github_anchors(self):
        guide = "---\nname: guide\n---\n\nOverview\n========\n\nText.\n\n## [Review](other.md) `steps`\n\n### <ID>: <Verifiable result>\n\n## `[label](url)`\n\nMore.\n"
        record = HEADER.format(approach="derive") + ideas_source().replace(
            '["SKILL.md#report"]', '["guide.md#overview", "guide.md#review-steps", "guide.md#id-verifiable-result", "guide.md#labelurl"]'
        )

        returncode, codes = self.check(record, files={"guide.md": guide})

        self.assertEqual((returncode, codes), (0, []))

    def test_snapshot_kind_sets_its_evidence(self):
        installed = """
[[local_snapshots]]
id = "installed-copy"
kind = "installed-file"
role = "ideas"
path = "~/.agents/skills/demo/SKILL.md"
""" + SNAPSHOT_IDEA
        session = """
[[local_snapshots]]
id = "followup-session"
kind = "session"
verification = "One supervised session on 2026-10-07."

[[invariants]]
rule = "Review every new head before approving it."
reason = "In the followup-session snapshot, an unreviewed head was approved."
"""

        _, installed_codes = self.check(HEADER.format(approach="derive") + installed)
        returncode, session_codes = self.check(HEADER.format(approach="create") + session)
        _, session_ideas = self.check(HEADER.format(approach="create") + session + SNAPSHOT_IDEA)

        self.assertEqual(installed_codes, ["missing-key", "missing-key"])
        self.assertEqual((returncode, session_codes), (0, []))
        self.assertEqual(session_ideas, ["role-mismatch"])

    def test_snapshot_can_be_the_base(self):
        snapshot = f"""
[[local_snapshots]]
id = "private-draft"
kind = "repository-commit"
role = "base"
repository = "https://github.com/example/private-skills"
commit = "{COMMIT_A}"
paths = ["draft/"]
verification = "Fetched the private main revision."

[[local_snapshots.deviations]]
change = "Replaced the pending draft with direct publication."
reason = "The user publishes reviews directly."
where = ["SKILL.md#report"]
"""

        returncode, codes = self.check(HEADER.format(approach="base") + snapshot)

        self.assertEqual((returncode, codes), (0, []))

    def test_references_and_dependencies(self):
        reference = '\n[[reference_documents]]\nurl = "https://www.w3.org/TR/WCAG22/"\nchecked = "2026-10-04"\nrole = "Success criteria."\n'
        dependency = '\n[[dependencies]]\nkind = "local"\nname = "verify"\nrequired = true\nrole = "Checks evidence."\ndecisions = ["Freeze the validator per run."]\n'

        returncode, codes = self.check(HEADER.format(approach="derive") + ideas_source() + reference + dependency)
        _, duplicate = self.check(HEADER.format(approach="derive") + ideas_source() + dependency + dependency)

        self.assertEqual((returncode, codes), (0, []))
        self.assertEqual(duplicate, ["duplicate-dependency"])

    def test_wrap_needs_an_installed_dependency(self):
        local = '\n[[dependencies]]\nkind = "local"\nname = "verify"\nrequired = true\nrole = "Checks evidence."\n'
        installed = f"""
[[dependencies]]
kind = "installed"
name = "e2e"
required = true
role = "Runs the end-to-end suite."
repository = "https://github.com/example/e2e"
remote = "git@github.com:example/e2e.git"
paths = ["skills/e2e/"]
approved_commit = "{COMMIT_A}"
installation = "~/.agents/.skill-lock.json"
"""

        _, local_codes = self.check(HEADER.format(approach="wrap") + local)
        returncode, installed_codes = self.check(HEADER.format(approach="wrap") + installed)

        self.assertEqual(local_codes, ["approach-mismatch"])
        self.assertEqual((returncode, installed_codes), (0, []))

    def test_skill_name_must_match_folder(self):
        _, codes = self.check(HEADER.format(approach="create"), name="other")

        self.assertIn("skill-name-mismatch", codes)

    def test_missing_directory_is_a_usage_error(self):
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--skill-dir", "/nonexistent/skill"],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 2)


def git(directory, *args):
    return subprocess.run(
        ["git", "-C", str(directory), "-c", "user.name=Test", "-c", "user.email=test@example.com", "-c", "commit.gpgsign=false", *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def run_checker(*args):
    result = subprocess.run([sys.executable, str(CHECKER), *map(str, args)], capture_output=True, text=True, check=False)
    return result.returncode, json.loads(result.stdout) if result.stdout else None


class CommitCitationTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.repository = Path(self.directory.name)
        self.skill_dir = self.repository / "demo"
        self.skill_dir.mkdir()
        (self.skill_dir / "SKILL.md").write_text(SKILL, encoding="utf-8")
        git(self.repository, "init", "--quiet", "--initial-branch=main")
        git(self.repository, "add", ".")
        git(self.repository, "commit", "--quiet", "-m", "Add demo")
        self.main_commit = git(self.repository, "rev-parse", "HEAD")
        git(self.repository, "switch", "--quiet", "-c", "feature")
        (self.skill_dir / "notes.md").write_text("Trial notes.\n", encoding="utf-8")
        git(self.repository, "add", ".")
        git(self.repository, "commit", "--quiet", "-m", "Add trial notes")
        self.branch_commit = git(self.repository, "rev-parse", "HEAD")

    def tearDown(self):
        self.directory.cleanup()

    def check_record(self, record):
        (self.skill_dir / "origin.toml").write_text(record, encoding="utf-8")
        returncode, output = run_checker("--skill-dir", self.skill_dir)
        return returncode, [(item["code"], item.get("location")) for item in output["diagnostics"]], output["skipped"]

    def check_reason(self, reason):
        returncode, diagnostics, _ = self.check_record(HEADER.format(approach="create") + f'\n[[invariants]]\nrule = "Cite evidence."\nreason = "{reason}"\n')
        return returncode, diagnostics

    def commit_record(self, record, branch):
        git(self.repository, "switch", "--quiet", branch)
        (self.skill_dir / "origin.toml").write_text(record, encoding="utf-8")
        git(self.repository, "add", ".")
        git(self.repository, "commit", "--quiet", "-m", f"Record on {branch}")

    def test_commit_only_on_a_branch_is_reported(self):
        returncode, diagnostics = self.check_reason(f"Trials at {self.branch_commit[:7]} showed it.")

        self.assertEqual((returncode, diagnostics), (1, [("unmerged-commit", "invariants[0].reason")]))

    def test_commits_on_the_default_branch_and_unknown_hashes_pass(self):
        returncode, diagnostics = self.check_reason(f"Decided in {self.main_commit[:7]}; upstream 49dd158d1076 agreed.")

        self.assertEqual((returncode, diagnostics), (0, []))

    def test_pinned_commit_fields_are_not_citations(self):
        snapshot = f'''
[[local_snapshots]]
id = "draft"
kind = "repository-commit"
role = "ideas"
repository = "https://github.com/example/drafts"
commit = "{self.branch_commit}"
paths = ["draft/"]
verification = "Read the draft at that commit."
''' + SNAPSHOT_IDEA

        returncode, diagnostics, _ = self.check_record(HEADER.format(approach="derive") + snapshot)

        self.assertEqual((returncode, diagnostics), (0, []))

    def test_shallow_history_skips_the_citation_check(self):
        git(self.repository, "switch", "--quiet", "main")
        (self.skill_dir / "later.md").write_text("Later.\n", encoding="utf-8")
        git(self.repository, "add", ".")
        git(self.repository, "commit", "--quiet", "-m", "Later main commit")
        shallow = self.repository / git(self.repository, "rev-parse", "--git-path", "shallow")
        shallow.write_text(git(self.repository, "rev-parse", "HEAD") + "\n", encoding="utf-8")

        returncode, diagnostics, skipped = self.check_record(HEADER.format(approach="create") + f'\n[[invariants]]\nrule = "Cite evidence."\nreason = "Decided in {self.main_commit[:7]}."\n')

        self.assertEqual((returncode, diagnostics), (0, []))
        self.assertEqual([item["check"] for item in skipped], ["unmerged-commit"])

    def publish_then_branch(self, published):
        self.commit_record(published, "main")
        git(self.repository, "switch", "--quiet", "-c", "topic")

    def test_moved_baseline_and_dropped_reviews_are_reported(self):
        c, d = "c" * 40, "d" * 40
        two_reviews = HEADER.format(approach="derive") + SOURCE.format(id="donor", role="ideas").replace(f'reviewed_through = "{COMMIT_B}"', f'reviewed_through = "{c}"') + IDEA + REVIEW + REVIEW.replace(f'from_commit = "{COMMIT_A}"', f'from_commit = "{COMMIT_B}"').replace(f'to_commit = "{COMMIT_B}"', f'to_commit = "{c}"')
        self.publish_then_branch(two_reviews)
        cursor_at_baseline = SOURCE.format(id="donor", role="ideas").replace(f'reviewed_through = "{COMMIT_B}"', f'reviewed_through = "{COMMIT_A}"')
        replaced = two_reviews.replace(f'reviewed_through = "{c}"', f'reviewed_through = "{d}"').replace(f'from_commit = "{COMMIT_B}"', f'from_commit = "{c}"').replace(f'to_commit = "{c}"', f'to_commit = "{d}"').replace(f'to_commit = "{COMMIT_B}"', f'to_commit = "{c}"')

        _, dropped, _ = self.check_record(HEADER.format(approach="derive") + cursor_at_baseline + IDEA)
        _, rewritten, _ = self.check_record(replaced)
        _, moved, _ = self.check_record(two_reviews.replace(f'baseline_commit = "{COMMIT_A}"', f'baseline_commit = "{"e" * 40}"').replace(f'from_commit = "{COMMIT_A}"', f'from_commit = "{"e" * 40}"'))
        _, renamed, _ = self.check_record(two_reviews.replace('id = "donor"', 'id = "newer-donor"'))

        self.assertEqual(dropped, [("reviews-dropped", "sources[0].reviews")])
        self.assertEqual(rewritten, [("reviews-dropped", "sources[0].reviews")])
        self.assertEqual(moved, [("baseline-moved", "sources[0].baseline_commit"), ("reviews-dropped", "sources[0].reviews")])
        self.assertEqual(renamed, [])

    def test_branch_work_that_keeps_history_passes(self):
        pending_source = SOURCE.format(id="donor", role="ideas").replace(f'reviewed_through = "{COMMIT_B}"', f'reviewed_through = "{COMMIT_A}"')
        pending = REVIEW.replace("deferred = []", 'deferred = ["A new lint tool needs the user\'s decision."]')
        self.publish_then_branch(HEADER.format(approach="derive") + pending_source + IDEA + pending)

        resolved = self.check_record(HEADER.format(approach="derive") + ideas_source())
        git(self.repository, "switch", "--quiet", "main")
        self.commit_record(HEADER.format(approach="derive") + ideas_source(), "main")
        git(self.repository, "switch", "--quiet", "topic")
        behind_main = self.check_record(HEADER.format(approach="derive") + pending_source + IDEA + pending)

        self.assertEqual(resolved[:2], (0, []))
        self.assertEqual(behind_main[:2], (0, []))

    def test_deleting_a_pending_review_is_reported(self):
        pending_source = SOURCE.format(id="donor", role="ideas").replace(f'reviewed_through = "{COMMIT_B}"', f'reviewed_through = "{COMMIT_A}"')
        pending = REVIEW.replace("deferred = []", 'deferred = ["A new lint tool needs the user\'s decision."]')
        self.publish_then_branch(HEADER.format(approach="derive") + pending_source + IDEA + pending)

        _, diagnostics, _ = self.check_record(HEADER.format(approach="derive") + pending_source + IDEA)

        self.assertEqual(diagnostics, [("reviews-dropped", "sources[0].reviews")])

    def test_malformed_source_ids_do_not_crash_the_comparison(self):
        self.publish_then_branch(HEADER.format(approach="derive") + ideas_source().replace('id = "donor"', "id = []"))

        returncode, diagnostics, _ = self.check_record(HEADER.format(approach="derive") + ideas_source().replace('id = "donor"', 'id = ["donor"]'))

        self.assertEqual((returncode, diagnostics), (1, [("invalid-value", "sources[0].id")]))

    def test_merged_branch_commit_passes(self):
        git(self.repository, "switch", "--quiet", "main")
        git(self.repository, "merge", "--quiet", "--no-ff", "-m", "Merge feature", "feature")

        returncode, diagnostics = self.check_reason(f"Trials at {self.branch_commit[:7]} showed it.")

        self.assertEqual((returncode, diagnostics), (0, []))


class CitationPatternTest(unittest.TestCase):
    def test_commit_like_tokens_of_seven_to_forty_hex_digits(self):
        spec = importlib.util.spec_from_file_location("check_origin", CHECKER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        text = f"Cited 5756208, deadbee and 1a2b3c4d; not abc123, decade, a{'0' * 63}, x1234567 or 1234567z."

        self.assertEqual(module.COMMIT_CITATION.findall(text), ["5756208", "deadbee", "1a2b3c4d"])


class DependentsTest(unittest.TestCase):
    def write_record(self, root, skill, dependencies=""):
        folder = root / skill
        folder.mkdir()
        (folder / "origin.toml").write_text(HEADER.replace('"demo"', f'"{skill}"').format(approach="create") + dependencies, encoding="utf-8")

    def test_lists_records_that_declare_the_skill_as_a_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_record(root, "verify")
            self.write_record(root, "accessibility", '\n[[dependencies]]\nkind = "local"\nname = "verify"\nrequired = false\nrole = "Runs checks through the recipe."\ndecisions = ["Calls it for interface changes."]\n')
            self.write_record(root, "pr", '\n[[dependencies]]\nkind = "local"\nname = "commit"\nrequired = false\nrole = "Commits."\n')

            returncode, output = run_checker("--dependents", "verify", "--root", root)

        self.assertEqual(returncode, 0)
        self.assertEqual(output["dependents"], [{
            "skill": "accessibility",
            "record": "accessibility/origin.toml",
            "kind": "local",
            "required": False,
            "role": "Runs checks through the recipe.",
            "decisions": ["Calls it for interface changes."],
        }])

    def test_records_in_hidden_folders_are_listed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".agents" / "skills").mkdir(parents=True)
            self.write_record(root / ".agents" / "skills", "caller", '\n[[dependencies]]\nkind = "local"\nname = "verify"\nrequired = true\nrole = "Verifies."\n')

            returncode, output = run_checker("--dependents", "verify", "--root", root)

        self.assertEqual((returncode, [item["record"] for item in output["dependents"]]), (0, [".agents/skills/caller/origin.toml"]))

    def test_malformed_dependencies_are_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_record(root, "table", '\n[dependencies]\nkind = "local"\nname = "verify"\n')
            self.write_record(root, "dated", '\n[[dependencies]]\nkind = "local"\nname = "verify"\nrequired = false\nrole = 2026-10-18\n')

            returncode, output = run_checker("--dependents", "verify", "--root", root)

        self.assertEqual(returncode, 1)
        self.assertEqual(output["unreadable"], ["table/origin.toml"])
        self.assertEqual([(item["skill"], item["role"]) for item in output["dependents"]], [("dated", "2026-10-18")])

    def test_unreadable_record_makes_the_list_incomplete(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_record(root, "verify")
            (root / "broken").mkdir()
            (root / "broken" / "origin.toml").write_text("not = [toml", encoding="utf-8")

            returncode, output = run_checker("--dependents", "verify", "--root", root)

        self.assertEqual((returncode, output["dependents"], output["unreadable"]), (1, [], ["broken/origin.toml"]))

    def test_dependents_needs_a_root_and_no_skill_dir(self):
        missing_root, _ = run_checker("--dependents", "verify")
        mixed, _ = run_checker("--dependents", "verify", "--root", ".", "--skill-dir", ".")

        self.assertEqual((missing_root, mixed), (2, 2))


if __name__ == "__main__":
    unittest.main()
