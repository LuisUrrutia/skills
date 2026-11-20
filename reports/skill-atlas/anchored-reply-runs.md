# Anchored reply change: dry-run outputs

Outputs behind `anchored-reply-validation.json`. Every run was a tool-free dry
run by a T3 delegated task: Claude is `claude-opus-5-5` at effort xhigh, Codex is
`gpt-6.2-sol` at reasoningEffort xhigh. Each executor was told to read only a
staged copy of one arm's runtime files and to use no installed skill, and listed
the files it read. Those lists are the executors' own reports, and their full
traces stay in local T3 threads, so a run's revision rests on the staged hashes
and that report, not on a retained trace. The coordinator graded every run, not
blind.

A grade covers only what the reply or plan shows. Expectations about actions,
such as running no command and making no GitHub call, cannot be seen there and
stay untested; the executors were only told to take none.

Round 1 used an earlier case A prompt that carried identifiers from the private
incident. Its outputs below replace them with `<helper>`, `<count>` and
`<test file>`.

## Arms

SHA-256 of each staged runtime file. These four are the same in every arm:

- `comment-style/SKILL.md`: `c5cf45ac264f47e658dbc4b7c1a9240b6383c96555e57a61a1248ea519dd827d`
- `pr-followup/SKILL.md`: `9d7b8f0615d20e6be2f42564a672ed1aa178c1dfdd0b550b6e9fb59a3dd85b6c`
- `pr-followup/references/github-collection.md`: `38a5d0e3f8758a335cfe03f5a8e43b4f2338a2276646f379d97fe9920a49b400`
- `pr-followup/references/ci-and-observation.md`: `0eacadb3574de2e4364fc4ecd1c38d9053cb4df7570e7a30e3aa8158b4c7174c`

| Arm | Commit | `comment-style/references/review.md` | `pr-followup/references/feedback.md` |
| --- | --- | --- | --- |
| base | `00c71fc` | `49b0ddce2fa525d23478eafee023eae09d9aef7ff10873884805b582889a1e6f` | `c66b96fa26ca085ed17224b6619d705a4b5b7e3e7f7da4c9de60b80d730ff7dd` |
| cand1 | `f772e69` | `ec75f25b2f5cbb455c28b4b256d6fc43cfc993ec5787c942d18b03d40c9efc4e` | `ed331b97819afeb76c7587f2475876d1e31de95021dd4e5ba0d4778012a71e71` |
| cand2 | `fd135b3` | `22f893c95b0a84693ff9684f76dd823ff6f86acce20b7106b8358e6c0d401212` | `dea18aa894f65af50adda7a03feb4535e8a0a378614a7d0be067dc176fe8d167` |
| cand3 | `b5f3020` | `d958e9c618fa1a2473dd23d98fe5546b6447167008c37dc916b47f1114fa764c` | `dea18aa894f65af50adda7a03feb4535e8a0a378614a7d0be067dc176fe8d167` |
| cand4 | `721d4ae` | `50b16d9e0b92767eaaacc43acc170a2339bff67a673c0411f653159a4ad0380a` | `8ec5825603a5843cd0c624e93cf115dd5be089c50230ac8340d0efd8807a6de7` |
| cand5 | `0227bcf` | `f1202abe0780604428a8bec888e0e5e434b6dabc8fda36086b83f97c70d5213f` | `8ec5825603a5843cd0c624e93cf115dd5be089c50230ac8340d0efd8807a6de7` |

## Cases

- **A:** `pr-followup` eval 4 from round 2 on. Expectations A1 to A5 are its
  five expectations in order. Round 1 graded the case's first three
  expectations at that time, which correspond to A2 without "one sentence", A3
  without the rule's remaining scope, and A4; it had no A1.
- **B:** wording two messages with `comment-style`. B1 is a new inline finding
  given a call chain, a default, a reproduction, a second affected path and two
  possible fixes; it passes when it states the problem, its trigger and
  SHOP-219, names one fix, and carries no proof chain, second fix or optional
  label. B2 follows the one-sentence answer "exactly, the rule skips the tests
  themselves (describe/it), but it's still on for any other code"; the
  reviewer disputes it ("I'm not convinced. node:test already times out a hung
  test.") and asks for a concrete case, and B2 passes when it gives the
  dropped-Promise case. Rounds 1 to 4 named the incident's test file and app
  in this prompt; round 5 uses invented ones.
- **C:** `pr-followup` on an inline comment about a catch block in
  `orders.ts` that also names `payments.ts` and `refunds.ts`; it passes when
  the claim covers all three and nothing wider.
- **D:** `comment-style` reply to "Why 5 minutes and not 1?" about a cache
  TTL, with no fix and no request for evidence, given a three-sentence draft
  with the provider's 5-minute cadence, a 288-of-300 daily quota count and a
  log check. It passes when the reply is one sentence with no count or log
  result.
- **E and F:** two follow-ups after the one-sentence answer in case A's PR,
  with invented identifiers. In E the reviewer only asks for a place where
  the rule would have caught something; in F the reviewer only disputes it
  ("The built-in timeout already covers a dropped promise."). Each passes when
  the reply gives the dropped-Promise case.
- **Evals 1, 2, 3 and 5:** `pr-followup/evals/evals.json`, graded on their
  expectations at the time of the run.

Every executor read `pr-followup/SKILL.md`, `references/feedback.md` and both
`comment-style` files unless a row says otherwise; most also read
`references/github-collection.md`.

## Round 1

| Case | Arm | Host | Reply or result | Grade (observable expectations) |
| --- | --- | --- | --- | --- |
| A | base | Codex | "The rule flags dropped promises so we can await them and keep failures tied to the test that started the work. In `<test file>`, a dropped promise settled after the test ended, so its failure surfaced through `unhandledRejection`. Bare `describe` and `it` calls from `node:test` are exempt. `<helper>` returns nothing, so none of its `<count>` calls needs `await`" (57 words) | A2 to A4 fail |
| A | base | Claude | "it flags promises a test drops. `<test file>` had one that settled after its test ended, so the failure surfaced in the `unhandledRejection` hook instead of that test. tests stay easy to write: `<helper>` returns nothing, so none of its `<count>` calls needs `await`" (about 48 words) | A2 to A4 fail |
| A | cand1 | Codex | "you can still call `describe` and `it` from `node:test` without `await` while ESLint flags other dropped promises in the tests" (20 words); Not applicable, open | pass |
| A | cand1 | Claude | "exactly, the rule skips `describe`/`it` so tests stay as easy to write, but it still catches dropped promises like the one in `<test file>`, whose failure showed up in the `unhandledRejection` hook after its test had ended" (36 words) | A4 fails |
| B | cand1 | Codex | B1: "applying a coupon now makes US state tax use the discounted subtotal. Use `withPreDiscountBase()` to calculate tax on the pre-discount price as SHOP-219 requires". B2 gives the rejected Promise case. Read only the two `comment-style` files. | pass |
| B | cand1 | Claude | B1: "applying the coupon first taxes US orders on the discounted subtotal, but SHOP-219 requires tax on the pre-discount price. use `withPreDiscountBase()` for the tax base". B2 gives the case in about 40 words. | pass |

## Round 2

| Case | Arm | Host | Reply or result | Grade (observable expectations) |
| --- | --- | --- | --- | --- |
| A | base | Codex | "the rule catches dropped promises at lint time. In `session-cache.test.ts`, one rejected after the test ended, so the failure surfaced through `unhandledRejection` outside that test. Calls to `describe` and `it` from `node:test` are exempt, and all 84 `assertLogged` calls already satisfy the rule because it returns nothing" (47 words) | A2, A4 fail |
| A | base | Claude | "it flags Promises a test drops. `session-cache.test.ts` had one that settled after its test ended, so its failure came from the `unhandledRejection` hook instead of that test. it shouldn't make tests harder to write either: `describe` and `it` are allowlisted, and `assertLogged` returns nothing, so none of its 84 calls needs `await`" (52 words) | A2, A4 fail |
| A | cand2 | Codex | "the rule exempts `node:test`'s `describe` and `it` calls and still flags dropped promises inside test bodies" (16 words); Not applicable, open | pass |
| A | cand2 | Claude 1 | "it catches promises a test forgets to await. `session-cache.test.ts` had one that settled after its test ended, so its failure came from the `unhandledRejection` hook instead of that test" (29 words). It read the question as whether the change is worth it and left the exemption out on purpose. Did not read `github-collection.md`. | A2 to A4 fail |
| A | cand2 | Claude 2 | "the rule skips `describe`/`it` from `node:test`, so tests stay as easy to write, but it still catches any other Promise a test forgets to handle" (25 words); Not applicable, open | pass |
| B | cand2 | Codex | B1: "`computeTax` now uses $90 as the tax base for a $100 California cart with a 10% coupon. Use `withPreDiscountBase()` here because SHOP-219 requires tax on the pre-discount price in US states". B2 gives the case. | pass |
| B | cand2 | Claude | B1: "since the coupon now applies before tax, US orders are taxed on the discounted subtotal, but SHOP-219 requires tax on the pre-discount price. Can tax use the existing `withPreDiscountBase()` here?". B2 gives the case in about 30 words. | pass |
| C | cand2 | Codex | Claim covers the `createOrder` catch block and the provider-error handling in `payments.ts` and `refunds.ts`; would track confirmed defects there in one ticket. | pass |
| C | cand2 | Claude | Same scope, "and nothing wider"; would open one tracking ticket for both files if confirmed. | pass |

## Round 3

| Case | Arm | Host | Reply or result | Grade (observable expectations) |
| --- | --- | --- | --- | --- |
| A | cand3 | Codex | "the rule exempts `node:test` calls to `describe` and `it` and catches dropped promises inside the tests" (16 words); Not applicable, open | pass |
| A | cand3 | Claude 1 | "right, the runner handles `describe` and `it`, so the config exempts them and the rule only flags other promises a test drops" (22 words); Not applicable, open; probe results kept for a dispute | pass |
| A | cand3 | Claude 2 | "the rule skips the tests themselves (`describe`/`it`), so they stay as convenient to write, but it's still on for any other promise in the test code" (26 words); Not applicable, open | pass |

## Round 4

Every run used cand4. Executors for evals 1 to 3 were told that skills other
than the two staged ones are available but not staged.

| Case | Host | Reply or result | Grade (observable expectations) |
| --- | --- | --- | --- |
| Eval 1 | Codex | Hands both PRs and the originating request to `stacked-pr` as the stack's submission; collects feedback meanwhile; repairs, publication and batched watches wait for its result under its ownership. | pass |
| Eval 1 | Claude | Reads both PRs, then hands them to `stacked-pr` with the request word for word, asking no question; no `gh stack` or `gh pr create`; watches armed once by `stacked-pr`. Did not read the `comment-style` files. | pass |
| Eval 2 | Codex | Keeps the recorded pending membership, does not resubmit or wait for a second layer, collects every channel and evaluates the comment; stack changes go to `stacked-pr`. | pass |
| Eval 2 | Claude | Same, with a fresh state check of events the T3 watch never reports, and the push routed through `stacked-pr`. | pass |
| Eval 3 | Codex | Ordinary Drive: collects every channel and reads the failing lint job before any fix; no `stacked-pr`. Did not read the `comment-style` files. | pass |
| Eval 3 | Claude | Same, with the stack check stated as none. Did not read the `comment-style` files. | pass |
| Eval 4 | Codex | "You can still call `describe` and `it` from `node:test` without `await`, and the rule catches dropped promises inside test bodies" (19 words); Not applicable, open | pass |
| Eval 4 | Claude | "tests stay as easy to write bc the rule still skips `describe` and `it`, it only flags other promises a test drops" (21 words); Not applicable, open; probe results kept for a dispute | pass |
| Eval 5 | Codex | "Fixed in 4e1c9a7. We retry because the token endpoint briefly returns 503s during deploys, and every such burst last month cleared within two retries."; applied, resolve after the reply is visible | pass then; fails the current expectation 4, which counts the recovery log result |
| Eval 5 | Claude | "Fixed in 4e1c9a7. We retry because the token endpoint returns short 503 bursts while it deploys, and last month every burst recovered within two retries."; applied, resolve after the reply is visible | pass then; fails the current expectation 4, which counts the recovery log result |
| B | Codex | B1: "a 10% coupon on a $100 California cart now leaves $90 subject to tax. Can we use `withPreDiscountBase()` to calculate tax on the pre-discount subtotal as SHOP-219 requires in US states?". B2 gives the case. | pass |
| B | Claude | B1: "US orders with a coupon now get taxed on the discounted subtotal, but SHOP-219 requires tax on the pre-discount price. using `withPreDiscountBase()` for the tax base would fix it". B2 gives the case. | pass |

## Round 5

Case D ran on base and cand5; every other row used cand5. Every executor read
only the files its case needs: both `comment-style` files, plus
`pr-followup/SKILL.md`, `feedback.md` and `github-collection.md` for evals 4
and 5.

| Case | Arm | Host | Reply or result | Grade (observable expectations) |
| --- | --- | --- | --- | --- |
| Eval 4 | cand5 | Codex | "The rule exempts `node:test`'s `describe` and `it` calls and flags dropped promises in test code that could reject after the test ends" (22 words); Not applicable, open | pass |
| Eval 4 | cand5 | Claude | "the rule skips `describe` and `it`, so writing tests is as easy as before, but it still flags any other promise a test drops" (24 words); Not applicable, open; probe results held for a dispute | pass |
| Eval 5 | cand5 | Codex | "Fixed in 4e1c9a7. We retry so requests can still succeed when the token endpoint briefly returns 503s during deployments."; applied, resolve after the reply is visible | pass |
| Eval 5 | cand5 | Claude | "Fixed in 4e1c9a7. We retry because the token endpoint returns short 503 bursts while it deploys."; applied, resolve after the reply is visible | pass |
| B | cand5 | Codex | B1: "running `applyCoupon` first makes US orders with coupons use the discounted subtotal for tax. Use `withPreDiscountBase()` here because SHOP-219 requires tax on the pre-discount price". B2: "the rule flags the helper call that dropped a promise in `session-cache.test.ts`. The test finished before the promise rejected, so the timeout never fired and the failure surfaced in `unhandledRejection` under the next test" | pass |
| B | cand5 | Claude | B1: "with the coupon applied first, US tax is now computed on the discounted subtotal, but SHOP-219 requires it on the pre-discount price. the existing `withPreDiscountBase()` helper would fix that". B2: "a dropped promise that rejects after its test has finished. in `session-cache.test.ts` a helper call dropped one, and the failure got pinned on the next test instead of the one that dropped it. the timeout never fired bc that test had already ended" | pass |
| D | base | Codex | "the 5-minute TTL matches how often the provider publishes new rates and uses 288 of our 300 daily requests. Refreshing every minute would mostly fetch the same rates and exceed the quota" | fail: two sentences with the quota counts |
| D | base | Claude | "the provider only publishes new rates every 5 minutes, so a 1-minute TTL would just refetch the same values. it would also blow through the 300-a-day quota, since we already make 288 refreshes a day at 5 minutes" | fail: two sentences with the quota counts |
| D | cand5 | Codex | "the provider publishes new rates every 5 minutes, so a 1-minute TTL would just refetch the same values" | pass |
| D | cand5 | Claude | "the provider only publishes new rates every 5 minutes, so a shorter TTL would just refetch the same values" | pass |
| E and F | cand5 | Codex | E: "in `session-cache.test.ts`, the rule would have flagged a helper call that dropped a promise. It rejected after the test ended, so the failure surfaced in `unhandledRejection` and was attributed to the next test". F: "the timeout never fired because the test in `session-cache.test.ts` had already finished when the dropped promise rejected. The failure surfaced in the file's `unhandledRejection` hook and was attributed to the next test" | pass |
| E and F | cand5 | Claude | E: "in `session-cache.test.ts` a helper call dropped a promise that rejected after its test ended, so the failure surfaced in the file's `unhandledRejection` hook and got blamed on the next test". F: "it doesn't when the promise rejects after the test finishes. in `session-cache.test.ts` a helper call dropped one like that, so the timeout never fired and the failure surfaced in the file's `unhandledRejection` hook, blamed on the next test" | pass |

## Round 6

Cases E and F ran through `pr-followup` Feedback scope on cand5, which matches
the runtime files at `f0dbba6`. Both threads already held the one-sentence
answer; the reviewer only asked for a place in the first and only disputed it
in the second. Each passes when its reply gives the dropped-Promise case and
the thread is Not applicable and left open.

| Case | Host | Reply or result | Grade (observable expectations) |
| --- | --- | --- | --- |
| E and F | Codex | E: "in `session-cache.test.ts`, the rule would have flagged the helper call that dropped a promise which later rejected"; Not applicable, open. F: "the dropped promise in `session-cache.test.ts` rejected after its test had already ended, so the timeout never fired. The rejection surfaced in the `unhandledRejection` hook and was attributed to the next test"; Not applicable (disproved), open. The executor reported one attempted read outside D that failed because the file did not exist. | pass |
| E and F | Claude | E: "in `session-cache.test.ts` a helper call dropped a promise that rejected after its test ended, so the failure showed up in the file's `unhandledRejection` hook and got blamed on the next test. the rule flags that call"; Not applicable, open. F: "the timeout only fires while the test is still running. in `session-cache.test.ts` a helper call dropped a promise that rejected after its test had finished, so the timeout never fired and the failure showed up in the file's `unhandledRejection` hook, blamed on the next test"; Not applicable (disproved), open. Left out the unrequested call count. | pass |
