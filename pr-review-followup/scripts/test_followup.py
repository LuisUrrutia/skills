from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from followup import FollowupError, RejectedError, apply, begin, record, settle, state

PR = 'https://github.com/example-org/api/pull/12'
HEAD = 'a' * 40


def thread(node, *comments, resolved=False, resolved_by=None, can_resolve=True):
    return {'id': node, 'isResolved': resolved, 'isOutdated': False, 'path': 'src/a.ts', 'line': 4,
            'resolvedBy': {'login': resolved_by} if resolved_by else None,
            'viewerCanResolve': can_resolve and not resolved, 'viewerCanUnresolve': resolved,
            'comments': {'pageInfo': {'hasNextPage': False},
                         'nodes': [{'databaseId': 100 + i, 'author': {'login': login}, 'body': body,
                                    'createdAt': f'2026-10-07T0{i}:00:00Z'}
                                   for i, (login, body) in enumerate(comments)]}}


class FakeGitHub:
    def __init__(self):
        self.actor = 'reviewer'
        self.author = 'author'
        self.pr_state = 'OPEN'
        self.head = HEAD
        self.base_ref = 'main'
        self.reviews = []
        self.threads = [thread('T1', ('reviewer', 'guard this write'), ('author', 'fixed in the last push')),
                        thread('T2', ('reviewer', 'cover the timezone case'), resolved=True, resolved_by='reviewer'),
                        thread('T3', ('other', 'nit: rename this'))]
        self.calls = []
        self.lose_reply = False
        self.reject_resolve = False
        self.more_comments = False
        self.reopen_after_reads = None

    def call(self, endpoint, payload=None):
        self.calls.append((endpoint, payload))
        if endpoint == 'user':
            return {'login': self.actor}
        if endpoint == 'graphql' and payload['query'].startswith('query'):
            if self.more_comments:
                self.threads[0]['comments']['pageInfo']['hasNextPage'] = True
            if self.reopen_after_reads is not None:
                self.reopen_after_reads -= 1
                if self.reopen_after_reads < 0:
                    self.threads[0].update(isResolved=False, resolvedBy=None)
            return {'data': {'repository': {'pullRequest': {
                'id': 'PR_node', 'state': self.pr_state, 'headRefOid': self.head, 'baseRefName': self.base_ref,
                'author': {'login': self.author},
                'reviewThreads': {'pageInfo': {'hasNextPage': False}, 'nodes': self.threads}}}}}
        if endpoint.endswith('/reviews?per_page=100'):
            return self.reviews
        if endpoint.endswith('/replies'):
            number = int(endpoint.split('/')[-2])
            target = next(t for t in self.threads if t['comments']['nodes'][0]['databaseId'] == number)
            target['comments']['nodes'].append({'databaseId': 900, 'author': {'login': self.actor},
                                                'body': payload['body'], 'createdAt': '2026-10-07T09:00:00Z'})
            if self.lose_reply:
                raise FollowupError('simulated lost response after reply')
            return {'id': 900, 'body': payload['body'], 'pull_request_review_id': 55}
        if endpoint.endswith('/reviews/55'):
            return {'state': 'COMMENTED'}
        if endpoint == 'graphql':
            node = payload['variables']['id']
            target = next(t for t in self.threads if t['id'] == node)
            resolving = 'unresolveReviewThread' not in payload['query']
            if resolving and self.reject_resolve:
                raise RejectedError('HTTP 403: Resource not accessible by integration')
            target.update(isResolved=resolving, resolvedBy={'login': self.actor} if resolving else None)
            name = 'resolveReviewThread' if resolving else 'unresolveReviewThread'
            return {'data': {name: {'thread': {'id': node, 'isResolved': resolving}}}}
        if endpoint.endswith('/reviews') and payload is not None:
            assert payload == {'commit_id': self.head, 'event': 'APPROVE'}
            review = {'id': 77, 'state': 'APPROVED', 'commit_id': self.head, 'user': {'login': self.actor}}
            self.reviews.append(review)
            return review
        raise AssertionError((endpoint, payload))

    def writes(self):
        return [(e, p) for e, p in self.calls if p and not p.get('query', '').startswith('query')]


class FollowupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state_file = self.root / 'state.json'
        self.snapshot = self.root / 'snapshot.json'
        self.snapshot.write_text(json.dumps({'target': {'url': PR, 'head': HEAD, 'base_name': 'main'}}))
        self.api = FakeGitHub()
        self.ticks = 0

    def record(self, complete=True, standing=0, questions=0):
        return record(PR, 'reviewer', self.state_file, self.snapshot, complete, standing, questions)

    def apply(self, **data):
        self.ticks += 1
        plan = self.root / f'plan-{self.ticks}.json'
        plan.write_text(json.dumps({'expected_head': HEAD, 'expected_base_ref': 'main', **data}))
        return apply(PR, 'reviewer', self.state_file, plan, self.root / f'receipt-{self.ticks}.json', self.api)

    def test_state_lists_reviewer_threads_with_speaker_roles(self):
        result = state(PR, 'reviewer', self.state_file, self.api)

        self.assertEqual([t['id'] for t in result['threads']], ['T1', 'T2'])
        self.assertTrue(result['threads'][0]['awaiting_reviewer'])
        self.assertEqual(result['threads'][0]['comments'][-1]['role'], 'author')
        self.assertFalse(result['review_current'])
        self.assertEqual(result['unresolved'], 1)
        self.assertEqual(self.api.writes(), [])

    def test_record_binds_the_review_to_its_snapshot(self):
        begin(PR, 'reviewer', self.state_file, HEAD)
        self.assertTrue(state(PR, 'reviewer', self.state_file, self.api)['review_in_progress'])

        self.record()
        result = state(PR, 'reviewer', self.state_file, self.api)

        self.assertTrue(result['review_current'])
        self.assertFalse(result['review_in_progress'])
        self.api.base_ref = 'release/1.2'
        self.assertFalse(state(PR, 'reviewer', self.state_file, self.api)['review_current'])

    def test_state_file_and_snapshot_must_match_the_pr_and_reviewer(self):
        self.record()
        with self.assertRaisesRegex(FollowupError, 'state file belongs'):
            state('https://github.com/example-org/api/pull/13', 'reviewer', self.state_file, self.api)
        self.snapshot.write_text(json.dumps({'target': {'url': PR.replace('12', '13'), 'head': HEAD, 'base_name': 'main'}}))
        with self.assertRaisesRegex(FollowupError, 'snapshot'):
            self.record()

    def test_reviewer_who_authored_the_pr_is_refused(self):
        self.api.author = 'reviewer'
        with self.assertRaisesRegex(FollowupError, 'pr-followup'):
            state(PR, 'reviewer', self.state_file, self.api)

    def test_truncated_comment_history_fails_closed(self):
        self.api.more_comments = True
        with self.assertRaisesRegex(FollowupError, 'comments'):
            state(PR, 'reviewer', self.state_file, self.api)

    def test_reply_and_resolve_in_the_same_thread_and_repeat_nothing(self):
        self.record()

        self.apply(replies=[{'thread_id': 'T1', 'body': 'this one is done'}], resolve=['T1'])
        writes = len(self.api.writes())
        second = self.apply(replies=[{'thread_id': 'T1', 'body': 'this one is done'}], resolve=['T1'])

        self.assertEqual(self.api.writes()[0][0], 'repos/example-org/api/pulls/12/comments/100/replies')
        self.assertTrue(self.api.threads[0]['isResolved'])
        self.assertEqual(len(self.api.writes()), writes)
        self.assertEqual((second['replied'], second['skipped']), ([], ['T1']))

    def test_other_reviewers_threads_are_never_touched(self):
        self.record()
        for data in ({'resolve': ['T3']}, {'replies': [{'thread_id': 'T3', 'body': 'agreed'}]}):
            with self.subTest(data=data), self.assertRaisesRegex(FollowupError, 'not a thread the reviewer started'):
                self.apply(**data)
        self.assertEqual(self.api.writes(), [])

    def test_malformed_plans_write_nothing(self):
        self.record()
        for data in ({'approve': 'false'}, {'resolve': 'T1'}, {'replies': [{'thread_id': 'T1', 'body': 3}]},
                     {'verified': [1]}, {'merge': True}, {'resolve': ['T1'], 'unresolve': ['T1']},
                     {'verified': ['T1']}, {'unresolve': ['T2'], 'verified': ['T2']}, {'expected_base_ref': 3}):
            with self.subTest(data=data), self.assertRaisesRegex(FollowupError, 'plan'):
                self.apply(**data)
        self.assertEqual(self.api.writes(), [])

    def test_approval_requires_every_gate(self):
        cases = [(None, 'not been reviewed'), ((False, 0, 0), 'incomplete'), ((True, 1, 0), 'required findings'),
                 ((True, 0, 1), 'questions'), ((True, 0, 0), 'unresolved')]
        for recorded, message in cases:
            with self.subTest(message=message):
                self.state_file.unlink(missing_ok=True)
                if recorded:
                    self.record(*recorded)
                with self.assertRaisesRegex(FollowupError, message):
                    self.apply(approve=True)
        self.assertFalse(any(e.endswith('/reviews') for e, _ in self.api.writes()))

    def test_resolution_by_someone_else_needs_verification_before_approval(self):
        self.record()
        self.api.threads[0].update(isResolved=True, resolvedBy={'login': 'author'}, viewerCanUnresolve=True)

        with self.assertRaisesRegex(FollowupError, 'verified'):
            self.apply(approve=True)
        result = self.apply(verified=['T1', 'T2'], approve=True)

        self.assertEqual(result['approved'], HEAD)

    def test_reopening_a_thread_whose_finding_stands(self):
        self.record()
        self.api.threads[0].update(isResolved=True, resolvedBy={'login': 'author'}, viewerCanUnresolve=True)

        self.apply(unresolve=['T1'], replies=[{'thread_id': 'T1', 'body': 'the retry path still writes twice'}])

        self.assertFalse(self.api.threads[0]['isResolved'])
        self.assertNotIn('T1', state(PR, 'reviewer', self.state_file, self.api)['needs_verification'])

    def test_approval_after_the_last_thread_resolves_and_end_state(self):
        self.record()

        result = self.apply(resolve=['T1'], verified=['T2'], approve=True)
        again = self.apply(approve=True)

        self.assertEqual(result['approved'], HEAD)
        self.assertEqual(again['approved'], HEAD)
        self.assertEqual(sum(e.endswith('/reviews') for e, _ in self.api.writes()), 1)
        self.assertTrue(state(PR, 'reviewer', self.state_file, self.api)['done'])

    def test_blockers_prevent_writes(self):
        self.record()
        blockers = [
            ('reviews', [{'state': 'PENDING', 'user': {'login': 'reviewer'}}], 'unsubmitted review'),
            ('head', 'b' * 40, 'head moved'),
            ('actor', 'someone-else', 'actor differs'),
            ('pr_state', 'MERGED', 'not open'),
            ('base_ref', 'release/1.2', 'base branch'),
        ]
        for field, value, message in blockers:
            with self.subTest(message=message):
                self.api = FakeGitHub()
                setattr(self.api, field, value)
                with self.assertRaisesRegex(FollowupError, message):
                    self.apply(resolve=['T1'])
                self.assertEqual(self.api.writes(), [])

    def test_unresolvable_thread_is_refused_before_writing(self):
        self.record()
        self.api.threads[0]['viewerCanResolve'] = False
        with self.assertRaisesRegex(FollowupError, 'cannot resolve'):
            self.apply(replies=[{'thread_id': 'T1', 'body': 'done'}], resolve=['T1'])
        self.assertEqual(self.api.writes(), [])

    def test_uncertain_write_blocks_later_ticks_and_rejection_does_not(self):
        self.record()
        self.api.lose_reply = True
        with self.assertRaisesRegex(FollowupError, 'lost response'):
            self.apply(replies=[{'thread_id': 'T1', 'body': 'this one is done'}])
        count = len(self.api.writes())

        with self.assertRaisesRegex(FollowupError, 'outcome is uncertain'):
            self.apply(replies=[{'thread_id': 'T1', 'body': 'this one is done'}])
        self.assertEqual(len(self.api.writes()), count)

        data = json.loads(self.state_file.read_text())
        data.pop('pending_operation')
        self.state_file.write_text(json.dumps(data))
        self.api.reject_resolve = True
        with self.assertRaises(RejectedError):
            self.apply(resolve=['T1'])
        self.assertNotIn('pending_operation', json.loads(self.state_file.read_text()))

    def test_verification_holds_only_for_the_head_it_checked(self):
        self.record()
        self.apply(resolve=['T1'], verified=['T2'])
        self.assertEqual(state(PR, 'reviewer', self.state_file, self.api)['needs_verification'], [])

        newer = 'c' * 40
        self.api.head = newer
        self.snapshot.write_text(json.dumps({'target': {'url': PR, 'head': newer, 'base_name': 'main'}}))
        self.record()
        result = state(PR, 'reviewer', self.state_file, self.api)

        self.assertEqual(result['needs_verification'], ['T1', 'T2'])
        self.assertIn('verified', ' '.join(result['approval_blockers']))

    def test_done_uses_the_whole_gate(self):
        self.record()
        self.apply(resolve=['T1'], verified=['T2'], approve=True)
        self.assertTrue(state(PR, 'reviewer', self.state_file, self.api)['done'])

        self.api.base_ref = 'release/1.2'
        self.assertFalse(state(PR, 'reviewer', self.state_file, self.api)['done'])

    def test_settle_updates_only_the_current_review(self):
        self.record(standing=1, questions=1)
        settle(PR, 'reviewer', self.state_file, 0, 0, self.api)
        result = self.apply(resolve=['T1'], verified=['T2'], approve=True)
        self.assertEqual(result['approved'], HEAD)

        self.api.head = 'd' * 40
        with self.assertRaisesRegex(FollowupError, 'current head'):
            settle(PR, 'reviewer', self.state_file, 0, 0, self.api)

    def test_final_approval_rechecks_the_gate_on_its_own_read(self):
        self.record()
        self.apply(resolve=['T1'], verified=['T2'])
        self.api.reopen_after_reads = 2

        with self.assertRaisesRegex(FollowupError, 'unresolved'):
            self.apply(approve=True)

        self.assertFalse(any(e.endswith('/reviews') for e, _ in self.api.writes()))

    def test_a_record_without_counts_fails_closed(self):
        self.record()
        data = json.loads(self.state_file.read_text())
        del data['reviewed']['questions']
        self.state_file.write_text(json.dumps(data))

        self.assertIn('incomplete', ' '.join(state(PR, 'reviewer', self.state_file, self.api)['approval_blockers']))


if __name__ == '__main__':
    unittest.main()
