from __future__ import annotations

import json
import unittest

from publish_review import PublishError, anchor_lines, apply, validate_plan
from snapshot import prepare, verify
from test_support import AUDITOR, ReviewFixture

SUBMITTED = {'COMMENT': 'COMMENTED', 'APPROVE': 'APPROVED'}


class FakeGitHub:
    def __init__(self, fixture):
        self.f = fixture
        self.actor = 'reviewer'
        self.review = None
        self.comments = []
        self.calls = []
        self.foreign_thread = False
        self.fail_after_create = False
        self.fail_after_submit = False
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
        if endpoint.endswith('/reviews/17/events'):
            assert set(payload) <= {'event', 'body'}
            self.review.update(state=SUBMITTED[payload['event']], body=payload.get('body', ''))
            if self.fail_after_submit:
                raise PublishError('simulated lost response after submission')
            return self.review.copy()
        if endpoint.endswith('/reviews/17'):
            return self.review.copy()
        if endpoint.endswith('/reviews') and payload is not None:
            assert set(payload) == {'commit_id'}
            self.review = {'id':17,'node_id':'PRR_new','state':'PENDING','user':{'login':self.actor},'commit_id':payload['commit_id']}
            if self.fail_after_create:
                raise PublishError('simulated lost response after write')
            return self.review.copy()
        if endpoint == 'graphql':
            query = payload['query']
            if query.startswith('query'):
                return {'data':{'node':{'pullRequest':{'id':'PR_other' if self.foreign_thread else 'PR_target'}}}}
            data = payload['variables']['input']
            assert data['pullRequestReviewId'] == 'PRR_new'
            number = len(self.comments)+1
            comment = {'id':f'PRRC_{number}', 'body':data['body'],'pullRequestReview':{'id':'PRR_new','state':self.review['state']}}
            self.comments.append({'id':number,'node_id':comment['id'],'body':data['body'],'path':data.get('path'), 'line':data.get('line'),'side':data.get('side'),'pull_request_review_id':17})
            if 'addPullRequestReviewThreadReply' in query:
                return {'data':{'addPullRequestReviewThreadReply':{'comment':comment}}}
            return {'data':{'addPullRequestReviewThread':{'thread':{'comments':{'nodes':[comment]}}}}}
        raise AssertionError((endpoint, payload))

    def writes(self):
        return [(endpoint,payload) for endpoint,payload,_ in self.calls if payload and not payload.get('query','').startswith('query')]


class PublishReviewTests(unittest.TestCase):
    def setUp(self):
        self.f = ReviewFixture()
        self.addCleanup(self.f.close)
        self.api = FakeGitHub(self.f)
        self.plan = self.f.root / 'comment-plan.json'
        self.receipt = self.f.root / 'receipt.json'
        self.data = {'event':'COMMENT',
                     'comments':[{'key':'C1-site1','path':'src/example.py','line':2,'side':'RIGHT','body':'preserve the required return value'}],
                     'replies':[{'key':'C2-reply','thread_id':'PRRT_existing','body':'this path also needs the guard'}]}
        self.write_plan()

    def write_plan(self):
        self.plan.write_text(json.dumps(self.data))

    def apply(self):
        return apply(self.f.snapshot, self.plan, 'reviewer', self.receipt, self.api)

    def test_comments_publish_as_one_comment_review_and_rerun_writes_nothing(self):
        first = self.apply()
        before = len(self.api.writes())
        second = self.apply()

        self.assertEqual(first['status'], 'COMMENTED')
        self.assertEqual(second['status'], 'COMMENTED')
        self.assertEqual(len(self.api.writes()), before)
        submissions = [p for e,p in self.api.writes() if e.endswith('/events')]
        self.assertEqual(submissions, [{'event':'COMMENT'}])
        self.assertFalse(any('resolveReviewThread' in json.dumps(p) for _,p in self.api.writes()))
        reply = next(p for _,p in self.api.writes() if 'addPullRequestReviewThreadReply' in p.get('query',''))
        self.assertEqual(reply['variables']['input']['pullRequestReviewThreadId'], 'PRRT_existing')

    def test_clean_review_approves_the_frozen_head(self):
        self.data = {'event':'APPROVE','comments':[],'replies':[]}
        self.write_plan()

        state = self.apply()

        self.assertEqual(state['status'], 'APPROVED')
        self.assertEqual(self.api.review['commit_id'], self.f.head)
        self.assertEqual([p for e,p in self.api.writes() if e.endswith('/events')], [{'event':'APPROVE'}])

    def test_existing_unsubmitted_review_is_never_published(self):
        self.api.review = {'id':17,'node_id':'PRR_user','state':'PENDING','user':{'login':'reviewer'},'commit_id':self.f.head,'body':'user draft'}

        with self.assertRaisesRegex(PublishError, 'unsubmitted review'):
            self.apply()

        self.assertEqual(self.api.writes(), [])
        self.assertEqual(self.api.review['state'], 'PENDING')

    def test_actor_mismatch_and_remote_drift_prevent_writes(self):
        self.api.actor = 'another-user'
        with self.assertRaisesRegex(PublishError, 'actor differs'):
            self.apply()
        self.assertEqual(self.api.writes(), [])
        self.api.actor = 'reviewer'
        self.api.change_head = True
        with self.assertRaisesRegex(PublishError, 'drifted'):
            self.apply()
        self.assertEqual(self.api.writes(), [])

    def test_uncertain_create_or_submission_is_not_repeated(self):
        for flag, operation in (('fail_after_create', 'create-review'), ('fail_after_submit', 'submit-review')):
            with self.subTest(operation=operation):
                self.receipt.unlink(missing_ok=True)
                self.api = FakeGitHub(self.f)
                setattr(self.api, flag, True)
                with self.assertRaisesRegex(PublishError, 'lost response'):
                    self.apply()
                count = len(self.api.writes())
                self.assertEqual(json.loads(self.receipt.read_text())['pending_operation'], operation)

                with self.assertRaisesRegex(PublishError, 'outcome is uncertain'):
                    self.apply()

                self.assertEqual(len(self.api.writes()), count)

    def test_foreign_thread_blocks_before_its_reply(self):
        self.api.foreign_thread = True
        with self.assertRaisesRegex(PublishError, 'different PR'):
            self.apply()
        self.assertFalse(any('addPullRequestReviewThreadReply' in p.get('query','') for _,p in self.api.writes()))
        self.assertFalse(any(e.endswith('/events') for e,_ in self.api.writes()))

    def test_plan_event_rules_and_anchors(self):
        manifest = verify(self.f.snapshot)
        plan = {'event':'COMMENT','comments':[{'key':'deleted','path':'src/example.py','line':2,'side':'LEFT','body':'preserve this previous behavior'}]}
        validate_plan(plan, manifest, self.f.snapshot)
        plan['comments'][0].update(start_line=1,start_side='LEFT')
        validate_plan(plan, manifest, self.f.snapshot)
        validate_plan({'event':'APPROVE','replies':[{'key':'r','thread_id':'PRRT_x','body':'this one is done'}]}, manifest, self.f.snapshot)
        validate_plan({'event':'COMMENT','body':'the PR title needs the ticket format'}, manifest, self.f.snapshot)
        finding = dict(plan['comments'][0])
        plan['comments'][0]['line'] = 99
        cases = [(plan, 'outside'),
                 ({'comments':[]}, 'event'),
                 ({'event':'REQUEST_CHANGES'}, 'event'),
                 ({'event':'APPROVE','comments':[finding]}, 'APPROVE'),
                 ({'event':'COMMENT'}, 'nothing to publish'),
                 ({'event':'COMMENT','body':'x','resolve':['PRRT_x']}, 'unknown plan fields')]
        for invalid, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(PublishError, message):
                validate_plan(invalid, manifest, self.f.snapshot)

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
            plan = {'event':'COMMENT','comments':[{'key':'rename','path':'src/renamed.py','line':12,
                                 'side':'RIGHT','body':'Preserve the renamed contract.'}]}
            validate_plan(plan, verify(snapshot), snapshot)
            plan['comments'][0]['line'] = 8
            with self.assertRaisesRegex(PublishError, 'outside'):
                validate_plan(plan, verify(snapshot), snapshot)


if __name__ == '__main__':
    unittest.main()
