from __future__ import annotations

import json
import unittest

from pending_review import PendingError, anchor_lines, apply, validate_plan
from snapshot import prepare, verify
from test_support import AUDITOR, ReviewFixture


class FakeGitHub:
    def __init__(self, fixture):
        self.f = fixture
        self.actor = 'reviewer'
        self.review = None
        self.comments = []
        self.calls = []
        self.foreign_thread = False
        self.fail_after_create = False
        self.change_head = False

    def call(self, endpoint, payload=None, paginate=False):
        self.calls.append((endpoint, payload, paginate))
        if endpoint == 'user':
            return {'login': self.actor}
        if endpoint.endswith('/pulls/12'):
            return {'node_id':'PR_target', 'head':{'sha':'0'*40 if self.change_head else self.f.head}, 'base':{'sha':self.f.base}}
        if endpoint.endswith('/reviews?per_page=100'):
            return [self.review] if self.review else []
        if endpoint.endswith('/comments?per_page=100'):
            return self.comments.copy()
        if endpoint.endswith('/reviews/17'):
            return self.review.copy()
        if endpoint.endswith('/reviews') and payload is not None:
            assert set(payload) == {'commit_id'}
            self.review = {'id':17,'node_id':'PRR_pending','state':'PENDING','user':{'login':self.actor},'commit_id':payload['commit_id']}
            if self.fail_after_create:
                raise PendingError('simulated lost response after write')
            return self.review.copy()
        if endpoint == 'graphql':
            query = payload['query']
            if query.startswith('query'):
                return {'data':{'node':{'pullRequest':{'id':'PR_other' if self.foreign_thread else 'PR_target'}}}}
            data = payload['variables']['input']
            assert data['pullRequestReviewId'] == 'PRR_pending'
            number = len(self.comments)+1
            comment = {'id':f'PRRC_{number}', 'body':data['body'],'pullRequestReview':{'id':'PRR_pending','state':self.review['state']}}
            self.comments.append({'id':number,'node_id':comment['id'],'body':data['body'],'path':data.get('path'), 'line':data.get('line'),'side':data.get('side'),'pull_request_review_id':17})
            if 'addPullRequestReviewThreadReply' in query:
                return {'data':{'addPullRequestReviewThreadReply':{'comment':comment}}}
            return {'data':{'addPullRequestReviewThread':{'thread':{'comments':{'nodes':[comment]}}}}}
        raise AssertionError((endpoint, payload))

    def writes(self):
        return [(endpoint,payload) for endpoint,payload,_ in self.calls if payload and not payload.get('query','').startswith('query')]


class PendingReviewTests(unittest.TestCase):
    def setUp(self):
        self.f = ReviewFixture()
        self.addCleanup(self.f.close)
        self.api = FakeGitHub(self.f)
        self.plan = self.f.root / 'comment-plan.json'
        self.receipt = self.f.root / 'receipt.json'
        self.data = {'comments':[{'key':'C1-site1','path':'src/example.py','line':2,'side':'RIGHT','body':'preserve the required return value'}],
                     'replies':[{'key':'C2-reply','thread_id':'PRRT_existing','body':'this path also needs the guard'}]}
        self.plan.write_text(json.dumps(self.data))

    def apply(self):
        return apply(self.f.snapshot, self.plan, 'reviewer', self.receipt, self.api)

    def test_pending_commit_actor_binding_and_idempotent_retry(self):
        first = self.apply()
        before = len(self.api.writes())
        second = self.apply()

        self.assertEqual(first['status'], 'PENDING')
        self.assertEqual(second['status'], 'PENDING')
        self.assertEqual(len(self.api.writes()), before)
        for endpoint, payload in self.api.writes():
            self.assertNotIn('event', payload)
            self.assertNotIn('submitPullRequestReview', json.dumps(payload))
            self.assertNotIn('resolveReviewThread', json.dumps(payload))
        reply = next(p for _,p in self.api.writes() if 'addPullRequestReviewThreadReply' in p.get('query',''))
        self.assertEqual(reply['variables']['input']['pullRequestReviewId'], 'PRR_pending')
        self.assertEqual(reply['variables']['input']['pullRequestReviewThreadId'], 'PRRT_existing')

    def test_existing_pending_review_and_user_edits_are_preserved(self):
        self.api.review = {'id':17,'node_id':'PRR_pending','state':'PENDING','user':{'login':'reviewer'},'commit_id':self.f.head,'body':'user draft body'}
        self.api.comments = [{'id':40,'node_id':'USER_COMMENT','body':'User text in progress','path':'src/example.py','line':1,'side':'RIGHT'}]
        self.apply()
        self.assertEqual(self.api.review['body'], 'user draft body')
        self.assertEqual(self.api.comments[0]['body'], 'User text in progress')
        self.assertFalse(any(endpoint.endswith('/reviews') for endpoint,_ in self.api.writes()))
        self.api.comments[1]['body'] = 'User revised this finding'
        before = len(self.api.writes())

        with self.assertRaisesRegex(PendingError, 'changed or not associated'):
            self.apply()

        self.assertEqual(len(self.api.writes()), before)
        self.assertEqual(self.api.comments[1]['body'], 'User revised this finding')

    def test_actor_mismatch_and_remote_drift_prevent_writes(self):
        self.api.actor = 'another-user'
        with self.assertRaisesRegex(PendingError, 'actor differs'):
            self.apply()
        self.assertEqual(self.api.writes(), [])
        self.api.actor = 'reviewer'
        self.api.change_head = True
        with self.assertRaisesRegex(PendingError, 'drifted'):
            self.apply()
        self.assertEqual(self.api.writes(), [])

    def test_uncertain_write_is_not_automatically_repeated(self):
        self.api.fail_after_create = True
        with self.assertRaisesRegex(PendingError, 'lost response'):
            self.apply()
        count = len(self.api.writes())
        self.assertEqual(json.loads(self.receipt.read_text())['pending_operation'], 'create-review')

        with self.assertRaisesRegex(PendingError, 'outcome is uncertain'):
            self.apply()

        self.assertEqual(len(self.api.writes()), count)

    def test_foreign_thread_and_old_head_draft_block(self):
        self.api.foreign_thread = True
        with self.assertRaisesRegex(PendingError, 'different PR'):
            self.apply()
        self.assertFalse(any('addPullRequestReviewThreadReply' in p.get('query','') for _,p in self.api.writes()))
        self.api.review['commit_id'] = self.f.base
        with self.assertRaisesRegex(PendingError, 'another head'):
            self.apply()

    def test_deleted_side_ranges_invalid_anchors_and_submission_rejected(self):
        manifest = verify(self.f.snapshot)
        plan = {'comments':[{'key':'deleted','path':'src/example.py','line':2,'side':'LEFT','body':'preserve this previous behavior'}]}
        validate_plan(plan, manifest, self.f.snapshot)
        plan['comments'][0].update(start_line=1,start_side='LEFT')
        validate_plan(plan, manifest, self.f.snapshot)
        plan['comments'][0]['line'] = 99
        with self.assertRaisesRegex(PendingError, 'outside'):
            validate_plan(plan, manifest, self.f.snapshot)
        with self.assertRaisesRegex(PendingError, 'submission'):
            validate_plan({'event':'APPROVE'}, manifest, self.f.snapshot)

    def test_reused_comment_identity_is_checked_on_every_readback(self):
        self.data['replies'] = []
        self.plan.write_text(json.dumps(self.data))
        self.api.review = {'id':17,'node_id':'PRR_pending','state':'PENDING','user':{'login':'reviewer'},'commit_id':self.f.head}
        self.api.comments = [{'id':40,'node_id':'USER_COMMENT',**self.data['comments'][0]}]
        self.apply()
        self.assertEqual(self.api.writes(), [])
        self.api.comments[0]['body'] = 'User changed the existing comment'

        with self.assertRaisesRegex(PendingError, 'changed or not associated'):
            self.apply()

        self.assertEqual(self.api.writes(), [])
        self.assertEqual(self.api.comments[0]['body'], 'User changed the existing comment')

    def test_rename_anchors_keep_both_diff_sides_and_exclude_unchanged_lines(self):
        original = self.f.repo / 'src/example.py'
        original.write_text(''.join(f'line {i}\n' for i in range(1,31)))
        self.f.git('add', '.')
        self.f.git('commit', '-m', 'Prepare rename fixture')
        base = self.f.git('rev-parse', 'HEAD')
        self.f.git('mv', 'src/example.py', 'src/renamed.py')
        renamed = self.f.repo / 'src/renamed.py'
        renamed.write_text(renamed.read_text().replace('line 15\n', 'replacement\n'))
        self.f.git('add', '.')
        self.f.git('commit', '-m', 'Rename with a narrow change')
        head = self.f.git('rev-parse', 'HEAD')

        anchors = anchor_lines(self.f.repo, base, head, 'src/renamed.py', 'src/example.py')

        self.assertIn(15, anchors['LEFT'])
        self.assertIn(15, anchors['RIGHT'])
        self.assertNotIn(1, anchors['RIGHT'])
        self.assertNotIn(30, anchors['RIGHT'])
        self.f.data.update(baseRefOid=base,headRefOid=head)
        self.f.pr.write_text(json.dumps(self.f.data))
        for context in ('0','8'):
            self.f.git('config', 'diff.context', context)
            snapshot = prepare(self.f.repo, self.f.pr, self.f.context, AUDITOR,
                               self.f.root / ('context-' + context))
            frozen = (snapshot.parent / 'diff.patch').read_text()
            self.assertIn('@@ -12,7 +12,7 @@', frozen)
            plan = {'comments':[{'key':'rename','path':'src/renamed.py','line':12,
                                 'side':'RIGHT','body':'Preserve the renamed contract.'}]}
            validate_plan(plan, verify(snapshot), snapshot)
            plan['comments'][0]['line'] = 8
            with self.assertRaisesRegex(PendingError, 'outside'):
                validate_plan(plan, verify(snapshot), snapshot)


if __name__ == '__main__':
    unittest.main()
