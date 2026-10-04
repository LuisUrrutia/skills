import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ledger import metric, validate
from period import instant, resolve_window
from render_report import build
from fixtures import example


class PeriodTests(unittest.TestCase):
    def test_calendar_week_month_and_dst(self):
        week = resolve_window("last-week", "Europe/Madrid", "2026-10-04T12:00:00+02:00")
        self.assertEqual(week["start"], "2026-09-21T00:00:00+02:00")
        self.assertEqual(week["end"], "2026-09-28T00:00:00+02:00")
        month = resolve_window("last-month", "Europe/Madrid", "2026-01-02T12:00:00+01:00")
        self.assertEqual(month["start"], "2025-12-01T00:00:00+01:00")
        spring = resolve_window("yesterday", "Europe/Madrid", "2026-03-30T12:00:00+02:00")
        autumn = resolve_window("yesterday", "Europe/Madrid", "2026-10-26T12:00:00+01:00")
        self.assertEqual((instant(spring["end"]) - instant(spring["start"])).total_seconds(), 23 * 3600)
        self.assertEqual((instant(autumn["end"]) - instant(autumn["start"])).total_seconds(), 25 * 3600)

    def test_naive_or_reversed_window_fails(self):
        with self.assertRaises(ValueError):
            instant("2026-09-20T12:00:00")
        with self.assertRaises(ValueError):
            resolve_window("custom", "UTC", start="2026-09-30", end="2026-09-01")


class LedgerTests(unittest.TestCase):
    def test_work_includes_public_employer_repository(self):
        data = validate(example())
        self.assertEqual(metric(data, "authored_prs_merged", "work", total=True)["count"], 20)
        self.assertEqual(metric(data, "authored_prs_merged", "work", "github.com/acme/public-sdk")["count"], 8)
        self.assertEqual(metric(data, "authored_prs_merged", "open-source", "github.com/community/cli")["count"], 3)
        self.assertEqual(metric(data, "authored_prs_merged", "open-source", "github.com/community/widgets")["count"], 2)

    def test_actor_roles_and_unique_entities_are_distinct(self):
        data = validate(example())
        self.assertEqual(metric(data, "prs_merged_by_you", "work", total=True)["count"], 0)
        self.assertEqual(metric(data, "prs_reviewed", "work", total=True)["count"], 3)
        self.assertEqual(metric(data, "reviews_submitted", "work", total=True)["count"], 4)
        self.assertEqual(metric(data, "incidents_attended", "work", total=True)["count"], 2)
        self.assertEqual(metric(data, "incidents_resolved", "work", total=True)["count"], 1)
        self.assertEqual(metric(data, "meetings_attended", "work", total=True)["count"], 0)

    def test_action_timestamp_and_half_open_window(self):
        data = example()
        data["events"][0]["time"] = data["window"]["end"]
        data["events"][1]["time"] = "2026-08-31T23:59:59+02:00"
        data["events"][2]["time"] = data["window"]["start"]
        result = metric(validate(data), "authored_prs_merged", "work", total=True)
        self.assertEqual(result["count"], 18)

    def test_duplicate_sightings_merge_but_conflicts_fail(self):
        data = example()
        data["events"].append(copy.deepcopy(data["events"][0]))
        self.assertEqual(metric(validate(data), "authored_prs_merged", "work", total=True)["count"], 20)
        data["events"][-1]["scope"] = "open-source"
        with self.assertRaises(ValueError):
            validate(data)

    def test_one_ticket_cannot_inflate_multiple_repository_rows(self):
        data = example()
        event = copy.deepcopy(next(e for e in data["events"] if e["id"] == "linear:1:closed"))
        event.update(id="linear:1:closed-again", repository="github.com/acme/public-sdk")
        data["events"].append(event)
        with self.assertRaisesRegex(ValueError, "one counting group"):
            validate(data)

    def test_reopened_ticket_retains_history_and_current_assignment(self):
        data = validate(example())
        self.assertEqual(metric(data, "tickets_closed", "work", total=True)["count"], 3)
        self.assertEqual(data["obligations"][1]["status"], "open")
        self.assertIn("Reopened", next(e for e in data["events"] if e["id"] == "linear:3:closed")["current_state"])

    def test_partial_missing_and_unclassified_do_not_look_exact(self):
        data = example()
        data["sources"][0].update(status="partial", pages_exhausted=False)
        self.assertEqual(metric(validate(data), "authored_prs_merged", "work", total=True)["display"], "20 observed")
        self.assertEqual(metric(validate(data), "meetings_attended", "work", total=True)["display"], "Unknown · 0 observed")
        data = example()
        data["events"][0]["scope"] = "unclassified"
        self.assertEqual(metric(validate(data), "authored_prs_merged", "work", total=True)["display"], "19 observed")

    def test_unknown_time_and_provisional_events_never_count(self):
        data = example()
        data["events"][0]["time"] = None
        data["events"][1]["confirmed"] = False
        self.assertEqual(metric(validate(data), "authored_prs_merged", "work", total=True)["display"], "18 observed")

    def test_invalid_evidence_or_obligation_owner_fails(self):
        data = example()
        data["events"][0]["evidence"] = ["missing"]
        with self.assertRaisesRegex(ValueError, "dangling evidence"):
            validate(data)
        data = example()
        data["obligations"][0]["owner"] = "slack:someone-else"
        with self.assertRaisesRegex(ValueError, "verified user owner"):
            validate(data)

    def test_unknown_attribution_prevents_exact_zero(self):
        for metric_key, kind, role in [("prs_reviewed", "pr_review", "actor"), ("authored_prs_merged", "pr_merged", "author")]:
            with self.subTest(metric=metric_key):
                data = example()
                for event in data["events"]:
                    if event["kind"] == kind and event["scope"] == "work":
                        event[role] = None
                        event["confirmed"] = False
                value = metric(validate(data), metric_key, "work", total=True)
                self.assertEqual(value["display"], "Unknown · 0 observed")
                self.assertGreater(value["unattributed"], 0)

    def test_known_other_actor_is_not_uncertainty_about_your_work(self):
        data = example()
        for event in data["events"]:
            if event["kind"] == "pr_review":
                event["actor"] = "github:someone-else"
        self.assertEqual(metric(validate(data), "prs_reviewed", "work", total=True)["display"], "0")

    def test_out_of_period_unknown_actor_is_context_only(self):
        data = example()
        for event in data["events"]:
            if event["kind"] == "pr_review":
                event.update(actor=None, confirmed=False, time="2026-08-01T12:00:00Z")
        self.assertEqual(metric(validate(data), "prs_reviewed", "work", total=True)["display"], "0")

    def test_contributing_source_cannot_hide_missing_metric_coverage(self):
        data = example()
        data["sources"].append({"id": "another-reviews", "label": "Second account", "scope": "Additional review account", "query": "Capped review search", "collected_at": data["as_of"], "notes": "Coverage for review metrics not established", "metrics": [], "pages_exhausted": False, "status": "partial"})
        next(e for e in data["events"] if e["kind"] == "pr_review")["source"] = "another-reviews"
        result = metric(validate(data), "prs_reviewed", "work", total=True)
        self.assertEqual(result["display"], "3 observed")
        self.assertIn("another-reviews", result["sources"])

    def test_partial_pagination_cannot_be_complete(self):
        data = example()
        data["sources"][0]["pages_exhausted"] = False
        with self.assertRaisesRegex(ValueError, "exhausted pagination"):
            validate(data)

    def test_duplicate_source_coverage_is_order_independent_and_survives_reload(self):
        data = example()
        data["sources"].append({"id": "another-reviews", "label": "Second account", "scope": "Additional review account", "query": "Capped review search", "collected_at": data["as_of"], "notes": "Coverage for review metrics not established", "metrics": [], "pages_exhausted": False, "status": "partial"})
        duplicate = copy.deepcopy(next(e for e in data["events"] if e["kind"] == "pr_review"))
        duplicate["source"] = "another-reviews"
        data["events"].append(duplicate)

        forward = validate(data)
        data["events"].reverse()
        backward = validate(data)
        reloaded = validate(json.loads(json.dumps(forward)))

        expected = metric(forward, "prs_reviewed", "work", total=True)
        self.assertEqual(expected["display"], "3 observed")
        self.assertIn("another-reviews", expected["sources"])
        self.assertEqual(metric(backward, "prs_reviewed", "work", total=True), expected)
        self.assertEqual(metric(reloaded, "prs_reviewed", "work", total=True), expected)

    def test_duplicate_current_state_is_retained_or_explicitly_conflicting(self):
        data = example()
        duplicate = copy.deepcopy(data["events"][0])
        duplicate["current_state"] = "Merged, deployment unknown"
        data["events"].append(duplicate)

        forward = validate(data)
        data["events"].reverse()
        backward = validate(data)

        for result in (forward, backward):
            event = next(e for e in result["events"] if e["id"] == duplicate["id"])
            self.assertEqual(event["current_state"], duplicate["current_state"])
        data["events"][-1]["current_state"] = "Deployed"
        with self.assertRaisesRegex(ValueError, "Conflicting current state"):
            validate(data)

    def test_unqualified_repository_and_blank_actor_fail(self):
        data = example()
        data["events"][0]["repository"] = "acme/platform"
        with self.assertRaisesRegex(ValueError, "host/namespace/repository"):
            validate(data)

    def test_conflicting_duplicate_description_requires_reconciliation(self):
        data = example()
        duplicate = copy.deepcopy(data["events"][0])
        duplicate["detail"] = "A different source claims this change was deployed."
        data["events"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "Conflicting duplicate event"):
            validate(data)

    def test_excluded_source_is_outside_declared_metric_scope(self):
        data = example()
        data["sources"].append({"id": "personal-account", "label": "Personal account", "scope": "Outside this work report", "query": "None", "collected_at": data["as_of"], "notes": "Explicitly excluded by scope", "metrics": [], "pages_exhausted": False, "status": "excluded"})
        self.assertEqual(metric(validate(data), "authored_prs_merged", "work", total=True)["display"], "20")
        data["sources"][-1]["metrics"] = ["authored_prs_merged"]
        with self.assertRaisesRegex(ValueError, "Excluded sources"):
            validate(data)

    def test_excluded_sightings_cannot_reenter_counting_scope(self):
        data = example()
        included = copy.deepcopy(data)
        source = next(s for s in data["sources"] if s["id"] == "github-owned")
        source.update(status="excluded", metrics=[])
        with self.assertRaisesRegex(ValueError, "excluded source"):
            validate(data)

        duplicate = copy.deepcopy(included["events"][0])
        duplicate["source"] = "excluded-account"
        excluded = dict(source, id="excluded-account")
        included["sources"].append(excluded)
        included["events"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "excluded source"):
            validate(included)
        included["events"].pop()
        self.assertEqual(metric(validate(included), "authored_prs_merged", "work", total=True)["display"], "20")
        data = example()
        data["events"][0]["actor"] = " "
        with self.assertRaisesRegex(ValueError, "Invalid actor"):
            validate(data)


class BundleTests(unittest.TestCase):
    def test_escaped_offline_bundle_retains_drilldown_and_no_overwrite(self):
        data = example()
        data["stories"][0]["title"] = '<script>alert("test")</script>'
        data["evidence"][0]["locator"] = "javascript:alert(1)"
        data["evidence"][0]["excerpt"] = '<img src=x onerror="alert(1)">'
        with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as temp:
            output = Path(temp) / "private-root" / "runs" / "run-id" / "bundle"
            page = build(validate(data), output)
            self.assertIn("&lt;script&gt;", page.read_text())
            evidence = (output / "evidence.html").read_text()
            self.assertNotIn('href="javascript:', evidence)
            self.assertNotIn("<img", evidence)
            saved = json.loads((output / "report.json").read_text())
            self.assertEqual(saved["obligations"][0]["due"], "2026-10-06")
            self.assertTrue(list((output / "details").glob("*.html")))
            self.assertEqual(output.stat().st_mode & 0o777, 0o700)
            for parent in (output.parent, output.parent.parent, output.parent.parent.parent):
                self.assertEqual(parent.stat().st_mode & 0o777, 0o700)
            with self.assertRaises(FileExistsError):
                build(validate(data), output)

    def test_cli_invalid_input_fails_without_output(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as temp:
            report = Path(temp) / "input.json"
            report.write_text('{"schema_version":99}')
            result = subprocess.run([sys.executable, str(ROOT / "scripts/activity_report.py"), "build", str(report), "--output", str(Path(temp) / "output")], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("schema_version", result.stderr)
            self.assertFalse((Path(temp) / "output").exists())


if __name__ == "__main__":
    unittest.main()
