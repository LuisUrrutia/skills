from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from triage import TriageError, record, triage

PR = 'https://github.com/example-org/api/pull/12'


def page(*nodes, more=False):
    return {'pageInfo': {'hasNextPage': more}, 'nodes': list(nodes)}


class FakeGitHub:
    def __init__(self):
        self.actor = 'author'
        self.pr = {
            'state': 'OPEN', 'isDraft': False, 'headRefOid': 'a' * 40, 'baseRefName': 'main',
            'mergeable': 'MERGEABLE', 'reviewDecision': 'REVIEW_REQUIRED',
            'reviewThreads': page({'id': 'T1', 'isResolved': False,
                                   'comments': page({'id': 'C1', 'body': 'guard this write'})}),
            'reviews': page({'id': 'R1', 'state': 'COMMENTED', 'body': 'a few points'}),
            'comments': page({'id': 'I1', 'body': 'thanks for this'}),
            'commits': {'nodes': [{'commit': {'statusCheckRollup': {'contexts': page(
                {'__typename': 'CheckRun', 'name': 'test', 'status': 'IN_PROGRESS', 'conclusion': None},
                {'__typename': 'CheckRun', 'name': 'lint', 'status': 'QUEUED', 'conclusion': None},
                {'__typename': 'StatusContext', 'context': 'deploy', 'state': 'PENDING'})}}}]},
        }
        self.calls = []

    def call(self, endpoint, payload=None):
        self.calls.append(endpoint)
        if endpoint == 'user':
            return {'login': self.actor}
        return {'data': {'repository': {'pullRequest': self.pr}}}

    def contexts(self):
        return self.pr['commits']['nodes'][0]['commit']['statusCheckRollup']['contexts']['nodes']


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

    def test_check_progress_without_a_failure_or_completion_stays_quiet(self):
        self.record()

        self.api.contexts()[0].update(status='COMPLETED', conclusion='SUCCESS')
        self.api.contexts()[1].update(status='IN_PROGRESS')

        self.assertEqual(self.triage()['verdict'], 'quiet')

    def test_acts_on_each_change_a_turn_must_judge(self):
        changes = {
            'failed check': lambda pr, ctx: ctx[0].update(status='COMPLETED', conclusion='FAILURE'),
            'failed status': lambda pr, ctx: ctx[2].update(state='ERROR'),
            'all checks finished': lambda pr, ctx: [c.update(status='COMPLETED', conclusion='SUCCESS', state='SUCCESS')
                                                    for c in ctx],
            'thread reply': lambda pr, ctx: pr['reviewThreads']['nodes'][0]['comments']['nodes'].append(
                {'id': 'C2', 'body': 'still racy'}),
            'edited comment': lambda pr, ctx: pr['comments']['nodes'][0].update(body='please split this'),
            'resolution': lambda pr, ctx: pr['reviewThreads']['nodes'][0].update(isResolved=True),
            'review': lambda pr, ctx: pr['reviews']['nodes'].append({'id': 'R2', 'state': 'APPROVED', 'body': ''}),
            'decision': lambda pr, ctx: pr.update(reviewDecision='APPROVED'),
            'conflict': lambda pr, ctx: pr.update(mergeable='CONFLICTING'),
            'head': lambda pr, ctx: pr.update(headRefOid='b' * 40),
            'base': lambda pr, ctx: pr.update(baseRefName='release/1.2'),
            'ready': lambda pr, ctx: pr.update(isDraft=True),
        }
        for name, change in changes.items():
            with self.subTest(change=name):
                self.setUp()
                self.record()

                change(self.api.pr, self.api.contexts())

                self.assertEqual(self.triage()['verdict'], 'act')

    def test_an_unknown_mergeable_state_is_not_a_change(self):
        self.record()

        self.api.pr['mergeable'] = 'UNKNOWN'

        self.assertEqual(self.triage()['verdict'], 'quiet')

    def test_a_pending_review_is_not_published_feedback(self):
        self.record()

        self.api.pr['reviews']['nodes'].append({'id': 'R3', 'state': 'PENDING', 'body': 'draft'})

        self.assertEqual(self.triage()['verdict'], 'quiet')

    def test_a_partial_view_acts(self):
        self.record()

        self.api.pr['comments']['pageInfo']['hasNextPage'] = True

        self.assertEqual(self.triage()['verdict'], 'act')

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
