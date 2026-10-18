#!/usr/bin/env python3
"""Check skills' origin.toml records against format version 2, or list the records that depend on a skill."""

import argparse
import datetime
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib


COMMIT = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SSH_REMOTE = re.compile(r"^(git@[^:\s]+:\S+|ssh://\S+)$")
LINE_CITATION = re.compile(r"origin\.(?:txt|toml):\d+")
MAX_WORDS = 100
COMMIT_CITATION = re.compile(r"(?<![0-9A-Za-z])[0-9a-f]{7,40}(?![0-9A-Za-z])")
LOCATION = re.compile(r"^([^\s#]+)(?:#([a-z0-9_-]+))?$")
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")

TEXT, TEXTS, PATHS, LOCATIONS, BOOL, DATE, INTEGER = "text", "texts", "paths", "locations", "bool", "date", "integer"
COMMIT_ID, DIGEST, HTTPS, SSH = "commit", "digest", "https", "ssh"

APPROACHES = {"base", "derive", "create", "wrap"}
ROLES = {"base", "ideas"}
SNAPSHOT_KINDS = {"installed-file", "repository-commit", "session"}
DEPENDENCY_KINDS = {"local", "installed"}
LEGACY_KEYS = {"borrowed", "local_choices"}
# Typed fields can name upstream commits that never belong on this repository's default branch.
PINNED_KEYS = {"baseline_commit", "reviewed_through", "from_commit", "to_commit", "commit", "approved_commit",
               "found_commit", "local_repository_commit", "sha256", "entrypoint_sha256", "review_sha256",
               "validator_sha256"}
DEFAULT_REFS = ("refs/remotes/origin/HEAD", "refs/remotes/origin/main", "refs/remotes/origin/master",
                "refs/heads/main", "refs/heads/master")

TOP = {
    "format_version": INTEGER, "skill": TEXT, "created": DATE, "approach": TEXT,
    "goal": TEXT,
}
TOP_OPTIONAL = {"invariants": None, "sources": None, "local_snapshots": None,
                "reference_documents": None, "dependencies": None}
INVARIANT = {"rule": TEXT}
INVARIANT_OPTIONAL = {"reason": TEXT, "where": LOCATIONS}
SOURCE = {
    "id": TEXT, "repository": HTTPS, "remote": SSH, "ref": TEXT, "license": TEXT,
    "role": TEXT, "baseline_commit": COMMIT_ID, "reviewed_through": COMMIT_ID,
    "baseline_paths": PATHS, "paths": PATHS,
}
SOURCE_OPTIONAL = {"author": TEXT, "ideas": None, "declined": None, "deviations": None,
                   "reviews": None}
IDEA = {"idea": TEXT, "serves": TEXT, "where": LOCATIONS, "shapes": TEXT}
IDEA_OPTIONAL = {"adapted": TEXT}
DECLINED = {"feature": TEXT, "reason": TEXT}
DEVIATION = {"change": TEXT, "reason": TEXT, "where": LOCATIONS}
REVIEW = {
    "from_commit": COMMIT_ID, "to_commit": COMMIT_ID, "incorporated": TEXTS,
    "skipped": TEXTS, "deferred": TEXTS, "validation": TEXTS,
}
SNAPSHOT = {"id": TEXT, "kind": TEXT}
SNAPSHOT_BY_KIND = {
    "installed-file": {"path": TEXT, "sha256": DIGEST, "update_policy": TEXT},
    "repository-commit": {"repository": TEXT, "commit": COMMIT_ID, "paths": TEXTS,
                          "verification": TEXT},
    "session": {"verification": TEXT},
}
SNAPSHOT_OPTIONAL = {
    "author": TEXT, "repository": TEXT, "path": TEXT, "paths": TEXTS, "sha256": DIGEST,
    "entrypoint_sha256": DIGEST, "review_sha256": DIGEST, "validator_sha256": DIGEST,
    "commit": COMMIT_ID, "local_repository_commit": COMMIT_ID,
    "repository_commit_status": TEXT, "update_policy": TEXT, "verification": TEXT,
    "license": TEXT, "role": TEXT, "ideas": None, "declined": None, "deviations": None,
}
REFERENCE = {"url": HTTPS, "checked": DATE, "role": TEXT}
REFERENCE_OPTIONAL = {"id": TEXT, "coverage": TEXT}
DEPENDENCY = {"kind": TEXT, "name": TEXT, "required": BOOL, "role": TEXT}
DEPENDENCY_BY_KIND = {
    "local": {},
    "installed": {"repository": HTTPS, "remote": SSH, "paths": TEXTS,
                  "approved_commit": COMMIT_ID, "installation": TEXT},
}
DEPENDENCY_OPTIONAL = {
    "resolution": TEXT, "decisions": TEXTS, "repository": HTTPS, "remote": SSH,
    "paths": TEXTS, "approved_commit": COMMIT_ID, "installation": TEXT,
    "found_commit": COMMIT_ID, "local_additions": TEXTS,
}


INLINE_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
SETEXT = re.compile(r"^\s{0,3}(=+|-+)\s*$")


def slug(heading):
    parts = re.split(r"(`+[^`]*`+)", heading.strip())
    text = "".join(part if part.startswith("`") else INLINE_LINK.sub(r"\1", part) for part in parts).lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s", "-", text)


def heading_slugs(path):
    slugs = set()
    counts = {}
    fence = None
    previous = ""

    def add(heading):
        anchor = slug(heading)
        seen = counts.get(anchor, 0)
        counts[anchor] = seen + 1
        slugs.add(anchor if seen == 0 else f"{anchor}-{seen}")

    lines = path.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].strip() == "---":
        for end, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                lines = lines[end + 1:]
                break
    for line in lines:
        marker = FENCE.match(line)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            previous = ""
            continue
        if fence is not None:
            continue
        match = HEADING.match(line)
        if match:
            add(match.group(1))
            previous = ""
        elif SETEXT.match(line) and previous.strip() and not previous.lstrip().startswith(("-", "*", ">", "|")):
            add(previous)
            previous = ""
        else:
            previous = line
    return slugs


def is_text(value):
    return isinstance(value, str) and bool(value.strip())


def git(directory, *args):
    try:
        result = subprocess.run(["git", "-C", str(directory), *args], capture_output=True, text=True, check=False)
    except OSError:
        return None, None
    return result.returncode, result.stdout.strip()


def review_range(review):
    return (review.get("from_commit"), review.get("to_commit")) if isinstance(review, dict) else None


def resolve_commit(directory, name):
    returncode, output = git(directory, "rev-parse", "--verify", "--quiet", f"{name}^{{commit}}")
    return output if returncode == 0 else None


def is_ancestor(directory, older, newer):
    return git(directory, "merge-base", "--is-ancestor", older, newer)[0] == 0


class Checker:
    def __init__(self, skill_dir, clones=None):
        self.skill_dir = skill_dir
        self.clones = clones or {}
        self.matched_sources = set()
        self.record = skill_dir / "origin.toml"
        self.diagnostics = []
        self.skipped = []
        self.slug_cache = {}
        self.citations = []
        self.default = None

    def issue(self, code, message, location=None):
        item = {"path": str(self.record), "code": code, "message": message}
        if location:
            item["location"] = location
        self.diagnostics.append(item)

    def run(self):
        if not self.record.is_file():
            if (self.skill_dir / "origin.txt").is_file():
                self.issue("legacy-file", "Rename origin.txt to origin.toml and convert it to format 2.")
            else:
                self.issue("missing-file", "origin.toml does not exist.")
            return self.diagnostics
        if (self.skill_dir / "origin.txt").is_file():
            self.issue("stale-legacy-file", "Delete origin.txt; origin.toml replaces it.")
        try:
            data = tomllib.loads(self.record.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
            self.issue("invalid-toml", str(error))
            return self.diagnostics
        self.scan_values(data, "")
        self.check_table(data, TOP, TOP_OPTIONAL, "")
        if data.get("format_version") != 2:
            self.issue("invalid-value", "format_version must be 2.", "format_version")
        if is_text(data.get("skill")) and data["skill"] != self.skill_dir.name:
            self.issue("skill-name-mismatch", f"skill is {data['skill']!r}, but the folder is {self.skill_dir.name!r}.", "skill")
        self.check_enum(data, "approach", APPROACHES, "approach")
        for index, invariant in enumerate(self.tables(data, "invariants", "invariants")):
            self.check_table(invariant, INVARIANT, INVARIANT_OPTIONAL, f"invariants[{index}]")
        sources = self.tables(data, "sources", "sources")
        snapshots = self.tables(data, "local_snapshots", "local_snapshots")
        dependencies = self.tables(data, "dependencies", "dependencies")
        for index, source in enumerate(sources):
            self.check_source(source, f"sources[{index}]")
        for index, snapshot in enumerate(snapshots):
            self.check_snapshot(snapshot, f"local_snapshots[{index}]")
        for index, document in enumerate(self.tables(data, "reference_documents", "reference_documents")):
            self.check_table(document, REFERENCE, REFERENCE_OPTIONAL, f"reference_documents[{index}]")
        names = set()
        for index, dependency in enumerate(dependencies):
            self.check_dependency(dependency, f"dependencies[{index}]")
            name = dependency.get("name")
            if isinstance(name, str):
                if name in names:
                    self.issue("duplicate-dependency", f"Dependency {name!r} appears more than once.", f"dependencies[{index}]")
                names.add(name)
        self.check_ids(data)
        self.check_approach(data, sources, snapshots, dependencies)
        if self.find_default_branch():
            self.check_commit_citations()
            self.check_against_default(sources)
        return self.diagnostics

    def scan_values(self, value, location):
        if isinstance(value, dict):
            for key, child in value.items():
                child_location = f"{location}.{key}" if location else key
                if key in LEGACY_KEYS:
                    self.issue("legacy-key", f"{key} is a format 1 field; convert it to ideas, declined, deviations, invariants or decisions.", child_location)
                self.scan_values(child, child_location)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                self.scan_values(child, f"{location}[{index}]")
        elif isinstance(value, str):
            if len(value.split()) > MAX_WORDS:
                self.issue("long-entry", f"Keep each field to {MAX_WORDS} words or fewer: record one decision and state it rather than copying the skill's text.", location)
            if LINE_CITATION.search(value):
                self.issue("line-citation", "Refer to a record by its content, not by line number.", location)
            if location.rsplit(".", 1)[-1] not in PINNED_KEYS:
                self.citations.extend((token, location) for token in COMMIT_CITATION.findall(value))

    def tables(self, data, key, location):
        value = data.get(key, [])
        if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
            self.issue("invalid-type", f"{key} must be an array of tables.", location)
            return []
        return value

    def check_table(self, table, required, optional, location):
        for key in sorted(required.keys() - table.keys()):
            self.issue("missing-key", f"{key} is required.", location)
        for key in sorted(table.keys() - required.keys() - optional.keys() - LEGACY_KEYS):
            self.issue("unknown-key", f"{key} is not a format 2 field here.", location)
        for key, kind in {**optional, **required}.items():
            if key in table and kind is not None:
                self.check_value(table[key], kind, f"{location}.{key}" if location else key)

    def check_value(self, value, kind, location):
        if kind == TEXT:
            valid = is_text(value)
        elif kind == TEXTS:
            valid = isinstance(value, list) and all(is_text(item) for item in value)
        elif kind == PATHS:
            valid = isinstance(value, list) and bool(value) and all(is_text(item) for item in value)
        elif kind == LOCATIONS:
            valid = isinstance(value, list) and bool(value) and all(is_text(item) for item in value)
            if valid:
                for item in value:
                    self.check_location(item, location)
        elif kind == BOOL:
            valid = isinstance(value, bool)
        elif kind == INTEGER:
            valid = isinstance(value, int) and not isinstance(value, bool)
        elif kind == DATE:
            valid = isinstance(value, datetime.date) or self.iso_date(value)
        elif kind == COMMIT_ID:
            valid = isinstance(value, str) and bool(COMMIT.match(value))
        elif kind == DIGEST:
            valid = isinstance(value, str) and bool(SHA256.match(value))
        elif kind == HTTPS:
            valid = isinstance(value, str) and value.startswith("https://") and len(value) > 8
        elif kind == SSH:
            valid = isinstance(value, str) and bool(SSH_REMOTE.match(value))
        else:
            raise ValueError(kind)
        if not valid:
            self.issue("invalid-value", self.expected(kind), location)

    @staticmethod
    def iso_date(value):
        if not isinstance(value, str):
            return False
        try:
            datetime.date.fromisoformat(value)
        except ValueError:
            return False
        return True

    @staticmethod
    def expected(kind):
        return {
            TEXT: "Expected a non-empty string.",
            TEXTS: "Expected a list of non-empty strings.",
            PATHS: "Expected a non-empty list of paths.",
            LOCATIONS: "Expected a non-empty list of local locations.",
            BOOL: "Expected true or false.",
            INTEGER: "Expected an integer.",
            DATE: "Expected a YYYY-MM-DD date.",
            COMMIT_ID: "Expected a full 40-character commit ID.",
            DIGEST: "Expected a 64-character SHA-256.",
            HTTPS: "Expected an https:// URL.",
            SSH: "Expected an SSH Git URL.",
        }[kind]

    def check_enum(self, table, key, allowed, location):
        value = table.get(key)
        if is_text(value) and value not in allowed:
            self.issue("invalid-value", f"{key} must be one of {sorted(allowed)}.", location)

    def child_tables(self, table, key, location):
        value = table.get(key, [])
        if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
            self.issue("invalid-type", f"{key} must be an array of tables.", f"{location}.{key}")
            return []
        return value

    def check_source(self, source, location):
        self.check_table(source, SOURCE, SOURCE_OPTIONAL, location)
        self.check_role(source, location)
        if source.get("role") == "base" and not (self.skill_dir / "THIRD-PARTY-NOTICES.txt").is_file():
            self.issue("missing-notice", "A base source's copied text needs THIRD-PARTY-NOTICES.txt in the skill folder.", f"{location}.role")
        reviews = self.child_tables(source, "reviews", location)
        for index, review in enumerate(reviews):
            self.check_table(review, REVIEW, {}, f"{location}.reviews[{index}]")
        self.check_review_chain(source, reviews, location)
        if isinstance(source.get("id"), str) and source["id"] in self.clones:
            self.matched_sources.add(source["id"])
            self.check_source_history(source, reviews, location, self.clones[source["id"]])

    def check_role(self, table, location):
        self.check_enum(table, "role", ROLES, f"{location}.role")
        role = table.get("role")
        if role == "base":
            for key in ("ideas", "declined"):
                if key in table:
                    self.issue("role-mismatch", f"A base records deviations, not {key}.", f"{location}.{key}")
            for index, deviation in enumerate(self.child_tables(table, "deviations", location)):
                self.check_table(deviation, DEVIATION, {}, f"{location}.deviations[{index}]")
        elif role == "ideas":
            if "deviations" in table:
                self.issue("role-mismatch", "An ideas record holds ideas and declines, not deviations.", f"{location}.deviations")
            ideas = self.child_tables(table, "ideas", location)
            if not ideas:
                self.issue("missing-ideas", "Record at least one idea this material contributed.", location)
            for index, idea in enumerate(ideas):
                self.check_table(idea, IDEA, IDEA_OPTIONAL, f"{location}.ideas[{index}]")
            for index, declined in enumerate(self.child_tables(table, "declined", location)):
                self.check_table(declined, DECLINED, {}, f"{location}.declined[{index}]")

    def check_review_chain(self, source, reviews, location):
        baseline, cursor = source.get("baseline_commit"), source.get("reviewed_through")
        if not all(isinstance(value, str) for value in (baseline, cursor)):
            return
        ranges = [review_range(review) for review in reviews]
        pending = bool(reviews) and bool(reviews[-1].get("deferred"))
        resolved = ranges[:-1] if pending else ranges
        for index, review in enumerate(reviews[:len(resolved)]):
            if review.get("deferred"):
                self.issue("review-chain", "Only the last review may hold deferred items; resolve them in that review.", f"{location}.reviews[{index}]")
        if pending and ranges[-1][0] != cursor:
            self.issue("review-chain", "A pending review must start at reviewed_through.", f"{location}.reviews[{len(ranges) - 1}]")
        if not resolved:
            if cursor != baseline:
                self.issue("review-chain", "reviewed_through moved past the baseline without a resolved review.", location)
            return
        if resolved[0][0] != baseline:
            self.issue("review-chain", "The first review must start at baseline_commit.", f"{location}.reviews[0]")
        for index in range(1, len(resolved)):
            if resolved[index][0] != resolved[index - 1][1]:
                self.issue("review-chain", "Each review must start where the previous one ended.", f"{location}.reviews[{index}]")
        if resolved[-1][1] != cursor:
            self.issue("review-chain", "The last resolved review must end at reviewed_through.", f"{location}.reviews[{len(resolved) - 1}]")

    def check_source_history(self, source, reviews, location, clone):
        if git(clone, "rev-parse", "--is-shallow-repository")[1] == "true":
            self.skip("source-history", f"The clone of {source['id']} is shallow, so missing ancestry proves nothing.")
            return
        known = {}

        def exists(commit):
            if not (isinstance(commit, str) and COMMIT.match(commit)):
                return False
            if commit not in known:
                known[commit] = resolve_commit(clone, commit) == commit
            return known[commit]

        pins = [(key, source.get(key), f"{location}.{key}") for key in ("baseline_commit", "reviewed_through")]
        ends = [(key, commit, f"{location}.reviews[{index}].{key}") for index, review in enumerate(reviews)
                for key, commit in zip(("from_commit", "to_commit"), review_range(review))]
        for key, commit, place in pins + ends:
            if isinstance(commit, str) and COMMIT.match(commit) and not exists(commit):
                self.issue("unknown-commit", f"{key} {commit} is not a commit in the clone of {source['id']}; if its history was rewritten, keep the pins and report the source as blocked.", place)
        baseline, cursor = source.get("baseline_commit"), source.get("reviewed_through")
        if exists(baseline) and exists(cursor) and not is_ancestor(clone, baseline, cursor):
            self.issue("commit-order", "reviewed_through does not descend from baseline_commit in the source's history.", f"{location}.reviewed_through")
        for index, review in enumerate(reviews):
            start, end = review_range(review)
            if exists(start) and exists(end) and not is_ancestor(clone, start, end):
                self.issue("commit-order", "The review's to_commit does not descend from its from_commit, so its range crosses rewritten or unrelated history.", f"{location}.reviews[{index}]")

    def check_snapshot(self, snapshot, location):
        kind = snapshot.get("kind") if isinstance(snapshot.get("kind"), str) else None
        required = {**SNAPSHOT, **SNAPSHOT_BY_KIND.get(kind, {})}
        self.check_table(snapshot, required, SNAPSHOT_OPTIONAL, location)
        self.check_enum(snapshot, "kind", SNAPSHOT_KINDS, f"{location}.kind")
        if kind == "session":
            for key in ("role", "ideas", "declined", "deviations"):
                if key in snapshot:
                    self.issue("role-mismatch", f"A session snapshot is evidence only; record its lessons as invariants, not {key}.", f"{location}.{key}")
        elif kind in SNAPSHOT_KINDS:
            if "role" not in snapshot:
                self.issue("missing-key", "role is required.", location)
            self.check_role(snapshot, location)

    def check_dependency(self, dependency, location):
        kind = dependency.get("kind") if isinstance(dependency.get("kind"), str) else None
        required = {**DEPENDENCY, **DEPENDENCY_BY_KIND.get(kind, {})}
        self.check_table(dependency, required, DEPENDENCY_OPTIONAL, location)
        self.check_enum(dependency, "kind", DEPENDENCY_KINDS, f"{location}.kind")

    def check_location(self, text, location):
        match = LOCATION.match(text.strip())
        if not match:
            self.issue("invalid-location", f"{text!r} is not a path with an optional lowercase #heading-anchor.", location)
            return
        relative, anchor = match.groups()
        root = self.skill_dir.resolve()
        target = (self.skill_dir / relative).resolve()
        if relative.startswith(("/", "~")) or (root not in target.parents and target != root):
            self.issue("escaping-location", f"{relative} resolves outside the skill folder.", location)
            return
        if not target.is_file():
            self.issue("missing-location", f"{relative} does not exist in the skill folder.", location)
            return
        if anchor:
            if target.suffix.lower() != ".md":
                self.issue("invalid-location", f"{relative} is not Markdown, so it has no heading anchors.", location)
                return
            if target not in self.slug_cache:
                self.slug_cache[target] = heading_slugs(target)
            if anchor not in self.slug_cache[target]:
                self.issue("missing-anchor", f"{relative} has no heading with anchor #{anchor}.", location)

    def skip(self, check, reason):
        self.skipped.append({"path": str(self.record), "check": check, "reason": reason})

    def find_default_branch(self):
        if git(self.skill_dir, "rev-parse", "--is-inside-work-tree")[1] != "true":
            return False
        self.default = next((ref for ref in DEFAULT_REFS if resolve_commit(self.skill_dir, ref)), None)
        if self.default is None:
            self.skip("default-branch", "No origin/HEAD, main or master ref was found.")
        return self.default is not None

    def check_commit_citations(self):
        if not self.citations:
            return
        if git(self.skill_dir, "rev-parse", "--is-shallow-repository")[1] == "true":
            self.skip("unmerged-commit", "The clone is shallow, so missing ancestry cannot prove a commit is off the default branch.")
            return
        branch = git(self.skill_dir, "rev-parse", "--abbrev-ref", self.default)[1] or self.default
        unmerged = {}
        for token, location in self.citations:
            if token not in unmerged:
                commit = resolve_commit(self.skill_dir, token)
                unmerged[token] = bool(commit) and git(self.skill_dir, "merge-base", "--is-ancestor", commit, self.default)[0] == 1
            if unmerged[token]:
                self.issue("unmerged-commit", f"Commit {token} is not on {branch}, so a rebase or squash merge can drop it. Describe the evidence or cite the pull request; cite a commit only once the default branch contains it.", location)

    def check_against_default(self, sources):
        returncode, fork = git(self.skill_dir, "merge-base", "HEAD", self.default)
        if returncode != 0:
            self.skip("published-record", "No merge base between HEAD and the default branch was found, as in unrelated histories or a shallow clone.")
            return
        prefix = git(self.skill_dir, "rev-parse", "--show-prefix")[1] or ""
        returncode, text = git(self.skill_dir, "show", f"{fork}:{prefix}origin.toml")
        if returncode != 0:
            return
        try:
            published = tomllib.loads(text)
        except tomllib.TOMLDecodeError:
            self.skip("published-record", "The record where this history joins the default branch is not valid TOML.")
            return
        entries = published.get("sources", [])
        if not isinstance(entries, list):
            self.skip("published-record", "The published record's sources is not an array of tables.")
            return
        before = {item["id"]: item for item in entries if isinstance(item, dict) and isinstance(item.get("id"), str)}
        for index, source in enumerate(sources):
            old = before.get(source["id"]) if isinstance(source.get("id"), str) else None
            if old is None:
                continue
            if old.get("baseline_commit") != source.get("baseline_commit"):
                self.issue("baseline-moved", "baseline_commit differs from the published record; give newer material a new source id instead of moving the baseline.", f"sources[{index}].baseline_commit")
            old_reviews, reviews = old.get("reviews", []), source.get("reviews", [])
            if not (isinstance(old_reviews, list) and isinstance(reviews, list)):
                continue
            # The last published review may still be pending, and a later run updates it in place.
            pending = bool(old_reviews) and isinstance(old_reviews[-1], dict) and bool(old_reviews[-1].get("deferred"))
            completed = old_reviews[:-1] if pending else old_reviews
            if len(reviews) < len(old_reviews) or [review_range(review) for review in reviews[:len(completed)]] != [review_range(review) for review in completed]:
                self.issue("reviews-dropped", "A review of the published record is missing, or a completed one changed its range; reviews are history and stay.", f"sources[{index}].reviews")

    def check_ids(self, data):
        seen = set()
        for key in ("sources", "local_snapshots", "reference_documents"):
            items = data.get(key, [])
            if not isinstance(items, list):
                continue
            for item in items:
                identifier = item.get("id") if isinstance(item, dict) else None
                if not isinstance(identifier, str):
                    continue
                if identifier in seen:
                    self.issue("duplicate-id", f"id {identifier!r} appears more than once.", key)
                seen.add(identifier)

    def check_approach(self, data, sources, snapshots, dependencies):
        approach = data.get("approach")
        material = sources + [snapshot for snapshot in snapshots if snapshot.get("kind") != "session"]
        bases = [item for item in material if item.get("role") == "base"]
        idea_material = [item for item in material if item.get("role") == "ideas"]
        installed = [dependency for dependency in dependencies if dependency.get("kind") == "installed"]
        if len(bases) > 1:
            self.issue("multiple-bases", "A skill has at most one base source.", "sources")
        if approach == "base" and len(bases) != 1:
            self.issue("approach-mismatch", "approach base needs exactly one record with role base.", "approach")
        if approach != "base" and bases:
            self.issue("approach-mismatch", "A record has role base, so approach must be base.", "approach")
        if approach == "derive" and not idea_material:
            self.issue("approach-mismatch", "approach derive needs at least one ideas source or snapshot.", "approach")
        if approach == "create" and material:
            self.issue("approach-mismatch", "approach create records no sources or material snapshots; use derive or base.", "approach")
        if approach == "wrap" and not installed:
            self.issue("approach-mismatch", "approach wrap needs an installed dependency.", "approach")


def dependents(name, root):
    found, unreadable = [], []
    for record in sorted(root.rglob("origin.toml")):
        relative = record.relative_to(root)
        if ".git" in relative.parts:
            continue
        try:
            data = tomllib.loads(record.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError):
            unreadable.append(str(relative))
            continue
        entries = data.get("dependencies", [])
        if not isinstance(entries, list) or not all(isinstance(entry, dict) for entry in entries):
            unreadable.append(str(relative))
            continue
        for dependency in entries:
            if dependency.get("name") == name:
                found.append({"skill": record.parent.name, "record": str(relative),
                              **{key: dependency[key] for key in ("kind", "required", "role", "decisions") if key in dependency}})
    return found, unreadable


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", action="append", type=Path, help="skill folder that contains origin.toml; repeat for several skills")
    parser.add_argument("--dependents", metavar="SKILL", help="list the records under --root that declare SKILL as a dependency, instead of checking records")
    parser.add_argument("--root", type=Path, help="repository root searched by --dependents")
    parser.add_argument("--source", action="append", default=[], metavar="ID=CLONE", help="local clone of the source with this id; checks its commits and their ancestry; repeat for several sources")
    args = parser.parse_args(argv)
    if args.dependents:
        if args.skill_dir or not args.root:
            parser.error("--dependents needs --root and no --skill-dir")
        if not args.root.is_dir():
            print(json.dumps({"error": "not a directory", "paths": [str(args.root)]}), file=sys.stderr)
            return 2
        found, unreadable = dependents(args.dependents, args.root)
        print(json.dumps({"skill": args.dependents, "root": str(args.root), "dependents": found, "unreadable": unreadable}, indent=2, default=str))
        return 1 if unreadable else 0
    if not args.skill_dir:
        parser.error("--skill-dir is required")
    missing = [str(path) for path in args.skill_dir if not path.is_dir()]
    if missing:
        print(json.dumps({"error": "not a directory", "paths": missing}), file=sys.stderr)
        return 2
    clones = {}
    for item in args.source:
        identifier, separator, path = item.partition("=")
        if not separator or not identifier or not path or git(path, "rev-parse", "--git-dir")[0] != 0:
            print(json.dumps({"error": "--source needs ID=CLONE with a Git clone", "value": item}), file=sys.stderr)
            return 2
        clones[identifier] = Path(path)
    diagnostics, skipped, matched = [], [], set()
    for skill_dir in args.skill_dir:
        checker = Checker(skill_dir, clones)
        diagnostics.extend(checker.run())
        skipped.extend(checker.skipped)
        matched |= checker.matched_sources
    unmatched = sorted(clones.keys() - matched)
    if unmatched:
        print(json.dumps({"error": "--source names no source of the checked records", "ids": unmatched}), file=sys.stderr)
        return 2
    print(json.dumps({"checked": [str(path) for path in args.skill_dir], "diagnostics": diagnostics, "skipped": skipped}, indent=2))
    return 1 if diagnostics else 0


if __name__ == "__main__":
    sys.exit(main())
