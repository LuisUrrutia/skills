from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from adapters import validate_jsonl, validate_report
from read_only import guarded
from snapshot import SnapshotError, inventory, prepare, verify
from test_support import AUDITOR, ReviewFixture


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.f = ReviewFixture()
        self.addCleanup(self.f.close)

    def test_fork_target_and_inventory_are_frozen(self):
        manifest = verify(self.f.snapshot)

        self.assertEqual(manifest['target']['repository'], 'example-org/target')
        self.assertEqual(manifest['merge_base'], self.f.base)
        self.assertEqual(json.loads((self.f.snapshot.parent / 'changed-paths.json').read_text()), ['src/example.py'])

    def test_changed_index_worktree_untracked_and_head_ref_invalidate(self):
        changes = [lambda: (self.f.repo / 'src/example.py').write_text('changed\n'),
                   lambda: (self.f.repo / 'untracked.txt').write_text('new\n'),
                   lambda: self.f.git('symbolic-ref', 'HEAD', 'refs/heads/baseline')]
        for change in changes:
            with self.subTest(change=change):
                change()
                with self.assertRaisesRegex(SnapshotError, 'drifted'):
                    verify(self.f.snapshot)
                self.f.git('symbolic-ref', 'HEAD', 'refs/heads/feature')
                self.f.git('reset', '--hard', self.f.head)
                self.f.git('clean', '-fd')
        self.f.git('update-index', '--assume-unchanged', 'src/example.py')
        with self.assertRaisesRegex(SnapshotError, 'drifted'):
            verify(self.f.snapshot)

    def test_stat_refresh_and_unrelated_refs_preserve_the_snapshot(self):
        (self.f.repo / 'src/example.py').touch()
        self.f.git('status', '--short')
        self.f.git('update-ref', 'refs/remotes/origin/unrelated', self.f.head)

        verify(self.f.snapshot)

    def test_head_mismatch_and_stale_rules_block(self):
        self.f.data['headRefOid'] = self.f.base
        self.f.pr.write_text(json.dumps(self.f.data))
        with self.assertRaisesRegex(SnapshotError, 'HEAD differs'):
            prepare(self.f.repo, self.f.pr, self.f.context, AUDITOR, self.f.root / 'another')
        with self.assertRaisesRegex(SnapshotError, 'source changed'):
            verify(self.f.snapshot)

    def test_rename_delete_and_empty_inventory(self):
        self.f.git('mv', 'src/example.py', 'src/renamed.py')
        self.f.git('rm', 'untouched.md')
        self.f.git('commit', '-m', 'Rename and delete fixture paths')

        paths, renames = inventory(self.f.repo, self.f.head, self.f.git('rev-parse', 'HEAD'))

        self.assertEqual(paths, ['src/renamed.py', 'untouched.md'])
        self.assertEqual(renames, {'src/renamed.py': 'src/example.py'})
        self.assertEqual(inventory(self.f.repo, self.f.head, self.f.head), ([], {}))

    def test_packet_filters_private_sections_and_shares_rules(self):
        profile = self.f.root / 'profile.md'
        profile.write_text('# Profile\n## Matches\n| `example-org/target` | current |\n## Checkouts\nPRIVATE_ACCESS_SENTINEL\n## Blind spots\nInspect schema constraints.\n## Tracker\nPRIVATE_TRACKER_SENTINEL\n')
        rules = self.f.root / 'standards.md'
        rules.write_text('Required rule from repository policy: preserve return types.\n')

        prepared = prepare(self.f.repo, self.f.pr, self.f.context, AUDITOR, self.f.root / 'shared', profile, (rules,))
        packet = (prepared.parent / 'packet.md').read_text()

        self.assertIn('Inspect schema constraints.', packet)
        self.assertIn(rules.read_text(), packet)
        self.assertNotIn('PRIVATE_ACCESS_SENTINEL', packet)
        self.assertNotIn('PRIVATE_TRACKER_SENTINEL', packet)
        self.assertIn('Do not invoke compare-solutions, delegate', packet)
        rules.write_text('Changed guide after preparing the common packet.\n')
        with self.assertRaisesRegex(SnapshotError, 'source changed'):
            verify(prepared)

    def test_empty_scope_and_stacked_base(self):
        self.f.data['baseRefOid'] = self.f.head
        self.f.pr.write_text(json.dumps(self.f.data))
        empty = prepare(self.f.repo, self.f.pr, self.f.context, AUDITOR, self.f.root / 'empty')
        self.assertEqual(json.loads((empty.parent / 'changed-paths.json').read_text()), [])
        report = self.f.root / 'empty.jsonl'
        report.write_text('\n'.join(map(json.dumps, [
            {'type':'review_context','reviewType':'committed','baseCommit':self.f.head},
            {'type':'complete','status':'review_skipped','findings':0}])))
        self.assertTrue(validate_jsonl(report, empty)[0])
        (self.f.repo / 'top.py').write_text('top_layer = True\n')
        self.f.git('add', '.')
        self.f.git('commit', '-m', 'Stacked top layer')
        self.f.data['headRefOid'] = self.f.git('rev-parse', 'HEAD')
        self.f.pr.write_text(json.dumps(self.f.data))

        stacked = prepare(self.f.repo, self.f.pr, self.f.context, AUDITOR, self.f.root / 'stacked')

        self.assertEqual(json.loads((stacked.parent / 'changed-paths.json').read_text()), ['top.py'])
        self.assertNotIn('src/example.py', (stacked.parent / 'diff.patch').read_text())

    def test_new_report_grammar_and_exact_coverage(self):
        report = self.f.root / 'report.md'
        report.write_text(self.f.report)
        self.assertTrue(validate_report(report, self.f.snapshot)[0])
        for broken in (self.f.report.replace('Class: requirements\n', ''),
                       self.f.report.replace('Action: required', 'Action: unknown'),
                       self.f.report.replace('`src/example.py`', '`wrong.py`')):
            report.write_text(broken)
            self.assertFalse(validate_report(report, self.f.snapshot)[0])
        report.write_text(self.f.report.replace('Action: required', 'Action: optional').replace('Recommendation: Required:', 'Recommendation: Optional:'))
        self.assertTrue(validate_report(report, self.f.snapshot)[0])

    def test_report_scope_must_match_the_frozen_comparison(self):
        report = self.f.root / 'report.md'
        report.write_text(self.f.report.replace(f'{self.f.base}..{self.f.head}', 'different-review'))

        valid, detail = validate_report(report, self.f.snapshot)

        self.assertFalse(valid)
        self.assertIn('Scope', detail)

    def test_delegated_report_validation_checks_format_scope_and_drift(self):
        report = self.f.root / 'report.md'
        report.write_text(self.f.report)
        command = [sys.executable, str(Path(__file__).with_name('reviewers.py')),
                   'validate-report', '--snapshot', str(self.f.snapshot), '--report', str(report)]
        valid = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(valid.returncode, 0, valid.stderr)

        report.write_text(self.f.report.replace(f'{self.f.base}..{self.f.head}', 'different-review'))
        wrong_scope = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(wrong_scope.returncode, 1)
        self.assertIn('Scope differs', wrong_scope.stdout)

        report.write_text(self.f.report)
        (self.f.repo / 'src/example.py').write_text('changed after review')
        stale = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(stale.returncode, 1)
        self.assertIn('drifted', stale.stderr)

    def test_native_completion_errors_malformed_and_zero(self):
        report = self.f.root / 'native.jsonl'
        context = {'type': 'review_context', 'reviewType': 'committed', 'baseCommit': self.f.base}
        success = [context, {'type': 'complete', 'status': 'review_completed', 'findings': 0, 'reviewedFiles': ['src/example.py']}]
        cases = [('', False), ('{}\n', False), ('invalid', False),
                 (json.dumps({'type': 'error', 'message': 'failed'}), False),
                 ('\n'.join(map(json.dumps, success)), True),
                 ('\n'.join(map(json.dumps, [context, {**success[1], 'message':'No fresh detailed file review was performed in this run.'}])), False),
                 ('\n'.join(map(json.dumps, [context, {'type': 'complete', 'status': 'review_completed', 'findings': 1}])), False),
                 ('\n'.join(map(json.dumps, [context, {'type': 'complete', 'status': 'review_skipped', 'findings': 0}])), False),
                 ('\n'.join(map(json.dumps, [context, {**success[1], 'outcome': 'failed'}])), False),
                 ('\n'.join(map(json.dumps, [context, {**success[1], 'unreviewedFileCount': 1}])), False),
                 ('\n'.join(map(json.dumps, [context, {**success[1], 'reviewedFiles': []}])), False)]
        for value, expected in cases:
            report.write_text(value)
            self.assertEqual(validate_jsonl(report, self.f.snapshot)[0], expected, value)

    def test_guard_blocks_product_git_and_peer_access_but_allows_own_report(self):
        own = self.f.run / 'codex'
        own.mkdir()
        peer = self.f.run / 'claude'
        peer.mkdir()
        (peer / 'review.md').write_text('PRIVATE_PEER_RESULT')
        private = self.f.root / 'private-profile.md'
        private.write_text('PRIVATE_ACCESS_SENTINEL')
        script = '''import sys
from pathlib import Path
repo, own, peer, packet, manifest, private = map(Path, sys.argv[1:])
assert packet.parent.parent.stat().st_mode
for p in (repo/'src/example.py', repo/'new.txt', repo/'.git/HEAD', repo/'.git/index'):
    try:
        with p.open('ab') as f: f.write(b'MUTATION')
    except PermissionError: pass
    else: raise SystemExit('write guard failed: '+str(p))
for path in (peer, manifest, private):
    try: text = path.read_text()
    except (PermissionError, FileNotFoundError): pass
    else:
        if text: raise SystemExit('private input isolation failed: '+str(path))
assert 'Independent code change review' in packet.read_text()
(own/'probe.txt').write_text('allowed')
'''
        command = guarded([sys.executable, '-c', script, str(self.f.repo), str(own), str(peer / 'review.md'), str(self.f.snapshot.parent / 'packet.md'), str(self.f.snapshot), str(private)], self.f.repo, self.f.run, self.f.snapshot.parent, own, (self.f.snapshot, private))

        result = subprocess.run(command, capture_output=True, text=True)

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual((own / 'probe.txt').read_text(), 'allowed')
        verify(self.f.snapshot)


if __name__ == '__main__':
    unittest.main()
