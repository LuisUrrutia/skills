from __future__ import annotations

import json
import unittest

from publish_review import PublishError, RejectedError, anchor_lines, apply, validate_plan
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
        self.reject_submit = False
        self.change_head = False
        self.base = fixture.base
        self.merge_base = fixture.base
        self.unresolved_mine = False
        self.add_user_comment = False
        self.body_override = None
        self.lose_comment = False
        self.base_ref = 'baseline'
        self.author = 'author'
        self.many_threads = False

    def call(self, endpoint, payload=None, paginate=False):
        self.calls.append((endpoint, payload, paginate))
        if endpoint == 'user':
            return {'login': self.actor}
        if endpoint.endswith('/pulls/12'):
            return {'node_id':'PR_target', 'user':{'login':self.author}, 'head':{'sha':'0'*40 if self.change_head else self.f.head},
                    'base':{'sha':self.base, 'ref':self.base_ref}}
        if '/compare/' in endpoint:
            return {'merge_base_commit':{'sha':self.merge_base}}
        if endpoint.endswith('/reviews?per_page=100'):
            return [self.review] if self.review else []
        if endpoint.endswith('/comments?per_page=100'):
            if self.add_user_comment and self.review and self.review['state'] == 'PENDING' and self.comments:
                self.comments.append({'id':99,'node_id':'USER_DRAFT','body':'user draft text','pull_request_review_id':17})
                self.add_user_comment = False
            return self.comments.copy()
        if endpoint.endswith('/reviews/17/events'):
            assert set(payload) <= {'event', 'body'}
            if self.reject_submit:
                raise RejectedError('HTTP 422: Unprocessable Entity')
            self.review.update(state=SUBMITTED[payload['event']], body=self.body_override if self.body_override is not None else payload.get('body', ''))
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
            if 'reviewThreads' in query:
                author = {'login':self.actor}
                nodes = [{'isResolved':False,'comments':{'nodes':[{'author':author}]}}] if self.unresolved_mine else []
                return {'data':{'repository':{'pullRequest':{'reviewThreads':{'pageInfo':{'hasNextPage':self.many_threads},'nodes':nodes}}}}}
            if query.startswith('query'):
                return {'data':{'node':{'pullRequest':{'id':'PR_other' if self.foreign_thread else 'PR_target'}}}}
            data = payload['variables']['input']
            assert data['pullRequestReviewId'] == 'PRR_new'
            number = len(self.comments)+1
            comment = {'id':f'PRRC_{number}', 'body':data['body'],'pullRequestReview':{'id':'PRR_new','state':self.review['state']}}
            self.comments.append({'id':number,'node_id':comment['id'],'body':data['body'],'path':data.get('path'), 'line':data.get('line'),'side':data.get('side'),'pull_request_review_id':17})
            if self.lose_comment:
                self.lose_comment = False
                raise PublishError('simulated lost response after comment')
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

    def apply(self, max_event='APPROVE'):
        return apply(self.f.snapshot, self.plan, 'reviewer', self.receipt, self.api, max_event)

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

    def test_body_is_submitted_and_read_back(self):
        self.data['body'] = 'the PR title needs the ticket format'
        self.write_plan()
        self.apply()
        self.assertEqual([p for e,p in self.api.writes() if e.endswith('/events')],
                         [{'event':'COMMENT','body':'the PR title needs the ticket format'}])

        self.receipt.unlink()
        self.api = FakeGitHub(self.f)
        self.api.body_override = 'something else'
        with self.assertRaisesRegex(PublishError, 'did not read back'):
            self.apply()

    def test_unexpected_user_comment_stops_submission(self):
        self.api.add_user_comment = True

        with self.assertRaisesRegex(PublishError, 'unexpected content'):
            self.apply()

        self.assertFalse(any(e.endswith('/events') for e,_ in self.api.writes()))

    def test_approve_is_blocked_by_the_actors_unresolved_threads(self):
        self.data = {'event':'APPROVE'}
        self.write_plan()
        self.api.unresolved_mine = True

        with self.assertRaisesRegex(PublishError, 'unresolved'):
            self.apply()

        self.assertEqual(self.api.writes(), [])

    def test_base_tip_may_move_while_the_merge_base_holds(self):
        self.api.base = 'b' * 40
        self.assertEqual(self.apply()['status'], 'COMMENTED')

        self.receipt.unlink()
        self.api = FakeGitHub(self.f)
        self.api.base, self.api.merge_base = 'b' * 40, 'c' * 40
        with self.assertRaisesRegex(PublishError, 'drifted'):
            self.apply()

    def test_definite_rejection_clears_the_uncertainty_marker(self):
        self.api.reject_submit = True

        with self.assertRaises(RejectedError):
            self.apply()

        self.assertNotIn('pending_operation', json.loads(self.receipt.read_text()))

    def test_followup_caller_can_forbid_approval(self):
        self.data = {'event':'APPROVE'}
        self.write_plan()
        with self.assertRaisesRegex(PublishError, 'only COMMENT'):
            self.apply(max_event='COMMENT')
        self.assertEqual(self.api.writes(), [])

    def test_retarget_author_and_thread_limit_block_before_writing(self):
        cases = [('base_ref', 'release/other', 'base branch'), ('author', 'reviewer', 'authored'),
                 ('many_threads', True, '100 review threads')]
        self.data = {'event':'APPROVE'}
        self.write_plan()
        for field, value, message in cases:
            with self.subTest(message=message):
                self.receipt.unlink(missing_ok=True)
                self.api = FakeGitHub(self.f)
                setattr(self.api, field, value)
                with self.assertRaisesRegex(PublishError, message):
                    self.apply()
                self.assertEqual(self.api.writes(), [])

    def test_changed_recorded_comment_stops_submission(self):
        original = self.api.call

        def edit_then_read(endpoint, payload=None, paginate=False):
            if endpoint.endswith('/comments?per_page=100') and self.api.comments:
                self.api.comments[0]['body'] = 'user rewrote this'
            return original(endpoint, payload, paginate)

        self.api.call = edit_then_read
        with self.assertRaisesRegex(PublishError, 'changed or not associated'):
            self.apply()
        self.assertFalse(any(e.endswith('/events') for e,_ in self.api.writes()))

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

    def test_lost_comment_write_then_user_submission_is_not_overridden(self):
        self.api.lose_comment = True
        with self.assertRaisesRegex(PublishError, 'lost response'):
            self.apply()
        receipt = json.loads(self.receipt.read_text())
        self.assertEqual(receipt['pending_operation'], 'C1-site1')
        with self.assertRaisesRegex(PublishError, 'outcome is uncertain'):
            self.apply()

        receipt.pop('pending_operation')
        self.receipt.write_text(json.dumps(receipt))
        self.api.review['state'] = 'COMMENTED'
        count = len(self.api.writes())
        with self.assertRaisesRegex(PublishError, 'no longer pending'):
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
        validate_plan({'event':'APPROVE'}, manifest, self.f.snapshot)
        validate_plan({'event':'COMMENT','body':'the PR title needs the ticket format'}, manifest, self.f.snapshot)
        finding = dict(plan['comments'][0])
        plan['comments'][0]['line'] = 99
        cases = [(plan, 'outside'),
                 ({'comments':[]}, 'event'),
                 ({'event':'REQUEST_CHANGES'}, 'event'),
                 ({'event':'APPROVE','comments':[finding]}, 'APPROVE'),
                 ({'event':'APPROVE','replies':[{'key':'r','thread_id':'PRRT_x','body':'done'}]}, 'APPROVE'),
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
