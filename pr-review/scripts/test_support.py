from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from snapshot import prepare

AUDITOR = Path(os.environ['AUDIT_SKILL_DIR']).resolve()

REPORT = '''# Code change review

Scope: `{base}..{head}`

## Review basis

The fixture requires retaining its guarded return. No additional standards apply.

## Findings

### F1 | high | src/example.py:2 | The changed return loses the required value

Class: requirements
Action: required
Affected: Fixture callers.
Diff cause: The return was changed.
Impact: The returned value violates the supplied requirement.
Evidence:
- code | `src/example.py:2` | The new value differs from the fixture contract.
Recommendation: Required: preserve the required value.
Unresolved premise: None.

## Open questions

None.

## Checks

- not-run | `runtime checks` | Fixture source inspection only.

## Coverage

- reviewed | `src/example.py` | Compared the return contract.
'''


class ReviewFixture:
    def __init__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / 'repository'
        self.repo.mkdir()
        self.run = self.root / 'run'
        self.run.mkdir()
        self.git('init', '-b', 'feature')
        (self.repo / 'src').mkdir()
        (self.repo / 'src/example.py').write_text('def value():\n    return 1\n')
        (self.repo / 'untouched.md').write_text('A separate smoke path.\n')
        self.git('add', '.')
        self.git('commit', '-m', 'Create fixture')
        self.base = self.git('rev-parse', 'HEAD')
        self.git('branch', 'baseline')
        (self.repo / 'src/example.py').write_text('def value():\n    return 2\n')
        self.git('add', '.')
        self.git('commit', '-m', 'Change fixture')
        self.head = self.git('rev-parse', 'HEAD')
        self.pr = self.root / 'pr.json'
        self.data = {'url': 'https://github.com/example-org/target/pull/12', 'number': 12,
                     'baseRefName': 'baseline', 'baseRefOid': self.base, 'headRefOid': self.head,
                     'title': 'Preserve the fixture return', 'body': 'Return the required value.',
                     'headRepository': {'nameWithOwner': 'example-contributor/fork'}}
        self.pr.write_text(json.dumps(self.data))
        self.context = self.root / 'context.md'
        self.context.write_text('Requirement: retain the guarded return. Source: fixture request.\nSeams: none; one local pure function.\n')
        self.snapshot = prepare(self.repo, self.pr, self.context, AUDITOR, self.run / 'inputs')
        self.report = REPORT.format(base=self.base, head=self.head)

    def git(self, *args):
        result = subprocess.run(['git', '-c', 'user.name=Review Fixture', '-c',
                                 'user.email=fixture@example.test', *args], cwd=self.repo,
                                stdin=subprocess.DEVNULL, text=True, capture_output=True, check=True)
        return result.stdout.strip()

    def close(self):
        self.temp.cleanup()
