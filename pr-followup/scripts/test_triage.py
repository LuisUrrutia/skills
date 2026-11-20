from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import triage as helper
from triage import TriageError, record, triage

PR = 'https://github.com/example-org/api/pull/12'


def check(name, status='IN_PROGRESS', conclusion=None, run=1):
    return {'__typename': 'CheckRun', 'databaseId': run, 'name': name, 'status': status, 'conclusion': conclusion}


class FakeGitHub:
    """GitHub as triage reads it: PR fields, paged threads and checks over GraphQL, paged lists over REST."""

    def __init__(self):
        self.actor = 'author'
        self.pr = {'state': 'OPEN', 'isDraft': False, 'headRefOid': 'a' * 40, 'baseRefName': 'main',
                   'mergeable': 'MERGEABLE', 'mergeStateStatus': 'BLOCKED', 'reviewDecision': 'REVIEW_REQUIRED'}
        self.threads = [{'id': 'T1', 'isResolved': False}]
        self.checks = [check('test'), check('lint', 'QUEUED'), check('build', 'COMPLETED', 'SUCCESS'), {'__typename': 'StatusContext', 'context': 'deploy',
                                                               'state': 'PENDING', 'createdAt': '2026-11-20T10:00:00Z'}]
        self.inline = [{'id': 1, 'body': 'guard this write'}]
        self.reviews = [{'id': 2, 'state': 'COMMENTED', 'body': 'a few points'}]
        self.conversation = [{'id': 3, 'body': 'thanks for this'}]
        self.page_size = 100
        self.head_moves_on_page_two = False
        self.calls = []

    def page(self, nodes, after):
        start = int(after or 0)
        end = start + self.page_size
        return {'pageInfo': {'hasNextPage': end < len(nodes), 'endCursor': str(end)}, 'nodes': nodes[start:end]}

    def call(self, endpoint, payload=None):
        self.calls.append(endpoint)
        if endpoint == 'user':
            return {'login': self.actor}
        if endpoint == 'graphql':
            after = payload['variables']['after']
            pr = dict(self.pr)
            if after and self.head_moves_on_page_two:
                pr['headRefOid'] = 'c' * 40
            if 'reviewThreads' in payload['query']:
                pr['reviewThreads'] = self.page(self.threads, after)
            else:
                pr['commits'] = {'nodes': [{'commit': {'oid': pr['headRefOid'], 'statusCheckRollup': {
                    'contexts': self.page(self.checks, after)}}}]}
            return {'data': {'repository': {'pullRequest': pr}}}
        lists = {'/pulls/12/comments?per_page=100': self.inline, '/pulls/12/reviews?per_page=100': self.reviews,
                 '/issues/12/comments?per_page=100': self.conversation}
        return next(items for suffix, items in lists.items() if endpoint.endswith(suffix))


class TriageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.state_file = Path(self.temp.name) / 'triage.json'
        self.api = FakeGitHub()

    def triage(self):
        return triage(PR, 'author', self.state_file, self.api)

    def record(self):
        return record(PR, 'author', self.state_file, self.api)

    def test_acts_until_a_turn_records_what_it_saw(self):
        self.assertEqual(self.triage()['verdict'], 'act')

        self.record()

        self.assertEqual(self.triage()['verdict'], 'quiet')

    def test_triage_writes_nothing(self):
        self.triage()

        self.assertFalse(self.state_file.exists())

    def test_running_checks_that_change_state_without_finishing_stay_quiet(self):
        self.record()

        self.api.checks[1].update(status='IN_PROGRESS')

        self.assertEqual(self.triage()['verdict'], 'quiet')

    def test_acts_on_each_change_a_turn_must_judge(self):
        changes = {
            'failed check': lambda api: api.checks[0].update(status='COMPLETED', conclusion='FAILURE'),
            'passed check while others run': lambda api: api.checks[0].update(status='COMPLETED', conclusion='SUCCESS'),
            'failed status': lambda api: api.checks[3].update(state='ERROR'),
            'rerun with the same result': lambda api: api.checks[2].update(databaseId=2),
            'thread reply': lambda api: api.inline.append({'id': 4, 'body': 'still racy'}),
            'edited inline comment': lambda api: api.inline[0].update(body='guard both writes'),
            'edited conversation comment': lambda api: api.conversation[0].update(body='please split this'),
            'resolution': lambda api: api.threads[0].update(isResolved=True),
            'review': lambda api: api.reviews.append({'id': 5, 'state': 'APPROVED', 'body': ''}),
            'decision': lambda api: api.pr.update(reviewDecision='APPROVED'),
            'conflict': lambda api: api.pr.update(mergeable='CONFLICTING'),
            'behind': lambda api: api.pr.update(mergeStateStatus='BEHIND'),
            'head': lambda api: api.pr.update(headRefOid='b' * 40),
            'base': lambda api: api.pr.update(baseRefName='release/1.2'),
            'draft': lambda api: api.pr.update(isDraft=True),
        }
        for name, change in changes.items():
            with self.subTest(change=name):
                self.setUp()
                self.record()

                change(self.api)

                self.assertEqual(self.triage()['verdict'], 'act')

    def test_every_page_is_compared(self):
        self.api.page_size = 1
        self.api.threads += [{'id': 'T2', 'isResolved': False}]
        self.record()

        self.api.threads[1]['isResolved'] = True
        self.assertEqual(self.triage()['verdict'], 'act')
        self.record()
        self.api.checks[3].update(state='SUCCESS')
        self.assertEqual(self.triage()['verdict'], 'act')

    def test_an_edit_to_an_old_item_of_a_long_list_acts(self):
        self.api.conversation = [{'id': i, 'body': f'note {i}'} for i in range(150)]
        self.record()

        self.api.conversation[0]['body'] = 'note 0, edited'

        self.assertEqual(self.triage()['verdict'], 'act')

    def test_a_head_that_moves_between_pages_fails_for_a_retry(self):
        self.api.page_size = 1
        self.api.head_moves_on_page_two = True

        with self.assertRaisesRegex(TriageError, 'run triage again'):
            self.triage()

    def test_the_gh_adapter_reads_every_rest_page(self):
        pages = [[{'id': i} for i in range(100)], [{'id': 100}]]
        done = subprocess.CompletedProcess([], 0, stdout=json.dumps(pages), stderr='')

        with mock.patch.object(helper.subprocess, 'run', return_value=done) as run:
            items = helper.GitHub('github.com').call('repos/o/r/issues/1/comments?per_page=100')

        self.assertEqual(len(items), 101)
        self.assertIn('--paginate', run.call_args.args[0])
        self.assertIn('--slurp', run.call_args.args[0])

    def test_an_unknown_mergeable_state_is_not_a_change(self):
        self.record()

        self.api.pr['mergeable'] = 'UNKNOWN'

        self.assertEqual(self.triage()['verdict'], 'quiet')

    def test_a_pending_review_is_not_published_feedback(self):
        self.record()

        self.api.reviews.append({'id': 6, 'state': 'PENDING', 'body': 'draft'})

        self.assertEqual(self.triage()['verdict'], 'quiet')

    def test_merged_or_closed_stops(self):
        for state in ('MERGED', 'CLOSED'):
            with self.subTest(state=state):
                self.api.pr['state'] = state
                self.assertEqual(self.triage()['verdict'], 'stop')

    def test_every_read_requires_the_bound_actor(self):
        self.api.actor = 'someone-else'

        with self.assertRaisesRegex(TriageError, 'actor'):
            self.triage()

        self.assertEqual(self.api.calls, ['user'])

    def test_state_file_belongs_to_one_pr_and_actor(self):
        self.record()

        with self.assertRaisesRegex(TriageError, 'belongs'):
            triage(PR.replace('12', '13'), 'author', self.state_file, self.api)
        self.assertEqual(json.loads(self.state_file.read_text())['pr'], PR)


if __name__ == '__main__':
    unittest.main()
