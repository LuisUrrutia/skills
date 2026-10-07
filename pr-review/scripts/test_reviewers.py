from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import unittest
from pathlib import Path

from test_support import ReviewFixture

RUNNER = Path(__file__).with_name('reviewers.py')
FAKE = r'''import hashlib, json, os, sys, time
from pathlib import Path
name = Path(sys.argv[0]).name
args = sys.argv[1:]
if args == ['--version']:
    print(name + ' fixture-1')
    raise SystemExit()
if name == 'coderabbit' and args == ['review', '--help']:
    if os.environ.get('FAKE_HELP_FAIL'): raise SystemExit(2)
    print('  --agent\n  --committed\n  --base\n  --base-commit\n  -c, --config' + ('' if os.environ.get('FAKE_OLD_CODERABBIT') else '\n  --fresh'))
    raise SystemExit()
if name == 'coderabbit' and os.environ.get('FAKE_OLD_CODERABBIT') and '--fresh' in args:
    raise SystemExit('unknown option --fresh')
packet = ''
if name in ('claude', 'codex'):
    packet = sys.stdin.read()
elif name == 'coderabbit':
    packet = Path(args[args.index('--config')+1]).read_text()
entry = {'name':name, 'args':args, 'time':time.time(), 'packet_sha256':hashlib.sha256(packet.encode()).hexdigest()}
fd = os.open(os.environ['FAKE_LOG'],os.O_CREAT|os.O_APPEND|os.O_WRONLY,0o600)
os.write(fd,(json.dumps(entry)+'\n').encode()); os.close(fd)
if name in ('codex','claude','coderabbit'):
    if os.environ.get('FAKE_BARRIER'):
        deadline = time.monotonic() + 5
        while True:
            started = {json.loads(line)['name'] for line in Path(os.environ['FAKE_LOG']).read_text().splitlines()}
            if {'codex','claude','coderabbit'} <= started: break
            if time.monotonic() >= deadline: raise SystemExit('reviewers were not launched concurrently')
            time.sleep(0.01)
    time.sleep(float(os.environ.get('FAKE_SLEEP','0.2')))
    if name == os.environ.get('FAKE_FAIL'):
        marker = Path(os.environ['FAKE_MARKER'])
        if not marker.exists():
            marker.write_text('failed')
            print('synthetic failure',file=sys.stderr)
            raise SystemExit(7)
if name == 'claude':
    if os.environ.get('FAKE_BAD_FORMAT') and (os.environ.get('FAKE_STILL_BAD') or '## Format correction' not in packet):
        print('Here is my report:\n' + os.environ['FAKE_REPORT'], end='')
    else:
        print(os.environ['FAKE_REPORT'],end='')
elif name == 'codex':
    Path(args[args.index('-o')+1]).write_text(os.environ['FAKE_REPORT'])
elif name == 'coderabbit':
    print(json.dumps({'type':'review_context','reviewType':'committed','baseCommit':os.environ['FAKE_BASE']}))
    if os.environ.get('FAKE_NATIVE_ERROR'):
        print(json.dumps({'type':'error','errorType':'unknown','message':'Synthetic native error'}))
    else:
        print(json.dumps({'type':'complete','status':'review_completed','findings':0,'reviewedFiles':['src/example.py']}))
elif name == 'gh':
    if args[0] == 'api':
        endpoint = args[3]
        if endpoint == 'graphql':
            query = next(x for x in args if x.startswith('query='))
            if 'reviewThreads' in query:
                for i in (1,2): print(json.dumps({'data':{'repository':{'pullRequest':{'reviewThreads':{'nodes':[{'id':f'thread-{i}','isResolved':False}]}}}}}))
            else:
                for i in (1,2): print(json.dumps({'data':{'node':{'comments':{'nodes':[{'id':f'comment-{i}','body':'existing feedback'}]}}}}))
        elif endpoint.endswith('/pulls/12'):
            print(json.dumps({'head':{'sha':os.environ['FAKE_HEAD']}}))
        elif '/check-runs?' in endpoint:
            for i in (17,18): print(json.dumps({'check_runs':[{'id':i,'output':{'summary':'bot summary'}}]}))
        elif '/annotations?' in endpoint:
            if '/18/' in endpoint and os.environ.get('FAKE_PARTIAL'):
                print('synthetic inaccessible annotations',file=sys.stderr); raise SystemExit(1)
            print(json.dumps([{'path':'src/example.py','message':'annotation'}]))
        elif '/actions/runs?' in endpoint:
            for i in (41,42): print(json.dumps({'workflow_runs':[{'id':i}]}))
        else:
            for i in (1,2): print(json.dumps([{'id':i,'body':'existing feedback'}]))
    elif args[:2] == ['run','view']:
        print('review bot output')
    else:
        raise SystemExit('unsupported fake gh call')
'''


class ReviewerTests(unittest.TestCase):
    def setUp(self):
        self.f = ReviewFixture()
        self.addCleanup(self.f.close)
        self.bin = self.f.root / 'bin'
        self.bin.mkdir()
        for name in ('claude', 'codex', 'coderabbit', 'gh'):
            path = self.bin / name
            path.write_text('#!' + sys.executable + '\n' + FAKE)
            path.chmod(0o755)
        self.log = self.f.root / 'calls.jsonl'
        self.env = {**os.environ, 'PATH': str(self.bin) + os.pathsep + os.environ['PATH'],
                    'FAKE_LOG': str(self.log), 'FAKE_REPORT': self.f.report,
                    'FAKE_BASE': self.f.base, 'FAKE_HEAD': self.f.head,
                    'FAKE_MARKER': str(self.f.root / 'failure-marker'),
                    'PYTHONDONTWRITEBYTECODE': '1'}
        self.command = [sys.executable, str(RUNNER), 'run', '--snapshot', str(self.f.snapshot),
                        '--pr-json', str(self.f.pr), '--scratchpad', str(self.f.run), '--poll-interval', '0.01']

    def run_review(self, *extra):
        return subprocess.run(self.command + list(extra), env=self.env, capture_output=True, text=True, timeout=15)

    def state(self):
        return json.loads((self.f.run / 'reviewers-state.json').read_text())

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_legacy_coderabbit_does_not_receive_unsupported_fresh(self):
        self.env['FAKE_OLD_CODERABBIT'] = '1'
        result = self.run_review()

        self.assertEqual(result.returncode, 0, result.stderr)
        call = next(c for c in self.calls() if c['name'] == 'coderabbit')
        self.assertNotIn('--fresh', call['args'])
        self.assertIn('checkpoint reuse is not excluded', self.state()['workers']['coderabbit']['detail'])

    def test_local_subset_does_not_launch_delegated_reviewers(self):
        result = self.run_review('--workers', 'coderabbit', 'feedback')

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(self.state()['workers']), {'coderabbit', 'feedback'})
        self.assertEqual({c['name'] for c in self.calls()}, {'coderabbit', 'gh'})
        self.assertEqual(self.state()['status'], 'subset_completed')

    def test_coderabbit_help_failure_does_not_stop_other_seats(self):
        self.env['FAKE_HELP_FAIL'] = '1'
        result = self.run_review()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.state()['workers']['claude']['state'], 'completed')
        self.assertEqual(self.state()['workers']['codex']['state'], 'completed')
        self.assertEqual(self.state()['workers']['coderabbit']['state'], 'failed')
        self.assertIn('review --help failed', self.state()['workers']['coderabbit']['detail'])
        self.assertNotIn('coderabbit', {c['name'] for c in self.calls()})

    def test_single_coderabbit_seat_retains_fresh_when_supported(self):
        result = self.run_review('--workers', 'coderabbit')

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(self.state()['workers']), {'coderabbit'})
        self.assertEqual(len(self.calls()), 1)
        self.assertIn('--fresh', self.calls()[0]['args'])
        self.assertEqual(self.state()['status'], 'subset_completed')

    def test_format_retry_supplies_original_report_and_validator_diagnostics(self):
        self.env['FAKE_BAD_FORMAT'] = '1'
        self.assertEqual(self.run_review().returncode, 1)
        failed = self.state()['workers']['claude']
        original = (self.f.run / 'claude/review.md').read_text()
        packet = (self.f.snapshot.parent / 'packet.md').read_bytes()

        result = self.run_review()

        self.assertEqual(result.returncode, 0, result.stderr)
        correction = (self.f.run / 'claude/correction-prompt.md').read_text()
        self.assertIn(original, correction)
        self.assertIn(failed['detail'], correction)
        self.assertIn('never a line range', correction)
        self.assertIn('one backtick span', correction)
        self.assertEqual((self.f.snapshot.parent / 'packet.md').read_bytes(), packet)
        self.assertEqual((self.f.run / 'attempts/claude/1/review.md').read_text(), original)
        self.assertEqual(self.state()['workers']['claude']['attempts'], 2)

    def test_format_correction_failure_exhausts_the_existing_budget(self):
        self.env.update(FAKE_BAD_FORMAT='1', FAKE_STILL_BAD='1')
        for _ in range(3):
            self.assertEqual(self.run_review().returncode, 1)

        self.assertEqual(self.state()['workers']['claude']['attempts'], 2)
        self.assertEqual(self.state()['workers']['claude']['state'], 'failed')
        self.assertEqual(sum(c['name'] == 'claude' for c in self.calls()), 2)
        self.assertEqual(sum(c['name'] == 'codex' for c in self.calls()), 1)

    def test_parallel_identical_inputs_fork_feedback_and_cache(self):
        self.env['FAKE_BARRIER'] = '1'
        first = self.run_review()

        self.assertEqual(first.returncode, 0, first.stderr)
        state = self.state()
        self.assertEqual(state['status'], 'completed')
        calls = self.calls()
        engines = [c for c in calls if c['name'] != 'gh']
        self.assertEqual({c['name'] for c in engines}, {'claude','codex','coderabbit'})
        self.assertEqual(len({c['packet_sha256'] for c in engines}), 1)
        for c in calls:
            self.assertNotIn('example-contributor/fork', json.dumps(c))
            self.assertNotEqual(c['args'][:2], ['repo','view'])
        manifest = json.loads((self.f.run / 'existing-feedback/manifest.json').read_text())
        self.assertEqual(manifest['repository'], 'example-org/target')
        self.assertEqual(manifest['counts']['review_threads'], 2)
        self.assertEqual(manifest['counts']['workflow_runs'], 2)
        threads = json.loads((self.f.run / 'existing-feedback/review-threads.json').read_text())
        self.assertTrue(all(len(t['comments']['nodes']) == 2 for t in threads))
        ledger = self.f.run / 'candidate-ledger.md'
        ledger.write_text('Parent-owned decisions\n')
        before = len(calls)

        second = self.run_review()

        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(len(self.calls()), before)
        self.assertEqual(ledger.read_text(), 'Parent-owned decisions\n')

    def test_duplicate_launch_wait_and_terminal_status(self):
        self.env['FAKE_SLEEP'] = '1'
        process = subprocess.Popen(self.command, env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)
        for _ in range(100):
            if (self.f.run / 'reviewers-state.json').exists(): break
            time.sleep(0.02)
        duplicate = self.run_review()
        wait = subprocess.run([sys.executable, str(RUNNER), 'wait', '--scratchpad', str(self.f.run), '--after', '0', '--timeout', '5'], capture_output=True, text=True, env=self.env)
        out, err = process.communicate(timeout=10)

        self.assertEqual(duplicate.returncode, 0, duplicate.stderr)
        self.assertIn('already running', duplicate.stdout)
        self.assertEqual(wait.returncode, 0, wait.stderr)
        self.assertTrue(json.loads(wait.stdout)['events'])
        self.assertEqual(process.returncode, 0, err + out)

    def test_failure_retries_once_without_restarting_completed_engines(self):
        self.env['FAKE_FAIL'] = 'codex'
        first = self.run_review()
        self.assertEqual(first.returncode, 1, first.stderr)
        self.assertEqual(self.state()['status'], 'partial')

        second = self.run_review()

        self.assertEqual(second.returncode, 0, second.stderr)
        counts = {name: sum(c['name'] == name for c in self.calls()) for name in ('claude','codex','coderabbit')}
        self.assertEqual(counts, {'claude':1,'codex':2,'coderabbit':1})
        self.assertTrue((self.f.run / 'attempts/codex/1/stderr.log').is_file())

    def test_native_error_is_incomplete_and_retries_are_bounded(self):
        self.env['FAKE_NATIVE_ERROR'] = '1'
        for _ in range(3):
            self.assertEqual(self.run_review().returncode, 1)
        self.assertEqual(self.state()['status'], 'partial')
        self.assertEqual(self.state()['workers']['coderabbit']['attempts'], 2)
        self.assertEqual(sum(c['name']=='coderabbit' for c in self.calls()), 2)

    def test_partial_feedback_preserves_successful_channels(self):
        self.env['FAKE_PARTIAL'] = '1'
        result = self.run_review()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state()['status'], 'completed_with_warnings')
        manifest = json.loads((self.f.run / 'existing-feedback/manifest.json').read_text())
        self.assertEqual(manifest['status'], 'partial')
        self.assertEqual(manifest['counts']['annotations'], 1)
        self.assertEqual(manifest['counts']['review_comments'], 2)
        self.assertTrue(any('18-annotations' in e['source'] for e in manifest['errors']))

    def test_timeout_and_checkout_drift_cannot_reuse_success(self):
        result = self.run_review('--worker-timeout', '0.05')
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any(w['validation']=='timeout' for w in self.state()['workers'].values()))
        (self.f.repo / 'src/example.py').write_text('changed after snapshot\n')

        stale = self.run_review('--worker-timeout', '0.05')

        self.assertEqual(stale.returncode, 1)
        self.assertIn('drifted', stale.stderr)

    def test_modified_cached_report_is_failed_after_attempt_budget(self):
        self.assertEqual(self.run_review('--max-attempts', '1').returncode, 0)
        (self.f.run / 'codex/review.md').write_text(self.f.report.replace('high', 'low'))

        result = self.run_review('--max-attempts', '1')

        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.state()['workers']['codex']['state'], 'failed')
        self.assertEqual(sum(c['name']=='codex' for c in self.calls()), 1)

    def test_tampered_cached_report_is_not_used_as_format_correction_input(self):
        self.assertEqual(self.run_review().returncode, 0)
        report = self.f.run / 'claude/review.md'
        report.write_text(self.f.report.replace('The new value differs', 'TAMPERED_CONTENT differs'))

        result = self.run_review()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.f.run / 'claude/correction-prompt.md').exists())
        self.assertNotIn('TAMPERED_CONTENT', report.read_text())
        claude_calls = [c for c in self.calls() if c['name'] == 'claude']
        self.assertEqual(len(claude_calls), 2)
        self.assertEqual(claude_calls[0]['packet_sha256'], claude_calls[1]['packet_sha256'])

    def test_dead_supervisor_status_and_wait_preserve_saved_evidence(self):
        self.assertEqual(self.run_review().returncode, 0)
        path = self.f.run / 'reviewers-state.json'
        state = self.state()
        state.update(status='running', supervisor_pid=2147483647)
        state['workers']['codex'].update(state='running', pid=2147483646)
        path.write_text(json.dumps(state))
        saved = path.read_bytes()

        status = subprocess.run([sys.executable, str(RUNNER), 'status', '--scratchpad', str(self.f.run), '--json'], capture_output=True, text=True)
        wait = subprocess.run([sys.executable, str(RUNNER), 'wait', '--scratchpad', str(self.f.run), '--after', '999', '--timeout', '1'], capture_output=True, text=True)

        self.assertEqual(json.loads(status.stdout)['status'], 'interrupted')
        self.assertEqual(json.loads(status.stdout)['workers']['codex']['state'], 'interrupted')
        self.assertEqual(json.loads(wait.stdout)['run_status'], 'interrupted')
        self.assertEqual(wait.returncode, 0)
        self.assertEqual(path.read_bytes(), saved)

    def test_invalid_cache_emits_failure_before_retry_completion(self):
        self.assertEqual(self.run_review().returncode, 0)
        previous = self.state()['event_sequence']
        (self.f.run / 'codex/review.md').unlink()

        self.assertEqual(self.run_review().returncode, 0)

        events = [json.loads(path.read_text()) for path in sorted((self.f.run / 'reviewer-events').glob('*.json'))]
        retried = [event for event in events if event['sequence'] > previous and event['name']=='codex']
        self.assertEqual([event['state'] for event in retried], ['failed','completed'])
        self.assertIn('missing output', retried[0]['detail'])

    def test_dead_worker_after_budget_is_terminal_and_never_relaunched(self):
        self.assertEqual(self.run_review('--max-attempts', '1').returncode, 0)
        path = self.f.run / 'reviewers-state.json'
        state = self.state()
        state.update(status='running', supervisor_pid=2147483647)
        state['workers']['codex'].update(state='running', pid=2147483646)
        path.write_text(json.dumps(state))

        result = self.run_review('--max-attempts', '1')

        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.state()['workers']['codex']['state'], 'failed')
        self.assertEqual(self.state()['workers']['codex']['validation'], 'interrupted')
        self.assertIsNone(self.state()['workers']['codex']['pid'])
        self.assertEqual(sum(c['name']=='codex' for c in self.calls()), 1)


if __name__ == '__main__':
    unittest.main()
