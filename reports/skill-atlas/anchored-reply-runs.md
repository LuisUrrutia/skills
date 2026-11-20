# Anchored reply change: dry-run outputs

Outputs behind `anchored-reply-validation.json`. Every run was a tool-free dry
run by a T3 delegated task: Claude is `claude-opus-5-5` at effort xhigh, Codex is
`gpt-6.2-sol` at reasoningEffort xhigh. Each executor was told to read only a
staged copy of one arm's runtime files and to use no installed skill, and listed
the files it read. Those lists are the executors' own reports; their full traces
stay in local T3 threads. The coordinator graded every run, not blind.

Round 1 used an earlier case A prompt that carried identifiers from the private
incident. Its outputs below replace them with `<helper>`, `<count>` and
`<test file>`.

## Arms

SHA-256 of each staged runtime file. `comment-style/SKILL.md`
(`c5cf45ac…dd827d`), `pr-followup/SKILL.md` (`9d7b8f06…85b6c`),
`github-collection.md` (`38a5d0e3…49b400`) and `ci-and-observation.md`
(`0eacadb3…ff7dd`) are the same in every arm.

| Arm | Commit | `comment-style/references/review.md` | `pr-followup/references/feedback.md` |
| --- | --- | --- | --- |
| base | `00c71fc` | `49b0ddce2fa525d23478eafee023eae09d9aef7ff10873884805b582889a1e6f` | `c66b96fa26ca085ed17224b6619d705a4b5b7e3e7f7da4c9de60b80d730ff7dd` |
| cand1 | `f772e69` | `ec75f25b2f5cbb455c28b4b256d6fc43cfc993ec5787c942d18b03d40c9efc4e` | `ed331b97819afeb76c7587f2475876d1e31de95021dd4e5ba0d4778012a71e71` |
| cand2 | `fd135b3` | `22f893c95b0a84693ff9684f76dd823ff6f86acce20b7106b8358e6c0d401212` | `dea18aa894f65af50adda7a03feb4535e8a0a378614a7d0be067dc176fe8d167` |
| cand3 | `b5f3020` | `d958e9c618fa1a2473dd23d98fe5546b6447167008c37dc916b47f1114fa764c` | `dea18aa894f65af50adda7a03feb4535e8a0a378614a7d0be067dc176fe8d167` |
| cand4 | `721d4ae` | `50b16d9e0b92767eaaacc43acc170a2339bff67a673c0411f653159a4ad0380a` | `8ec5825603a5843cd0c624e93cf115dd5be089c50230ac8340d0efd8807a6de7` |

## Cases

- **A:** `pr-followup` eval 4 from round 2 on. Expectations A1 to A5 are its
  five expectations in order; round 1 graded A2 as "40 words or fewer" and had
  no A1.
- **B:** wording two messages with `comment-style`. B1 is a new inline finding
  given a call chain, a default, a reproduction, a second affected path and two
  possible fixes; it passes when it states the problem, its trigger and
  SHOP-219, names one fix, and carries no proof chain, second fix or optional
  label. B2 replies to a reviewer who disputes the earlier one-sentence answer
  and asks for a concrete case; it passes when it gives that case.
- **C:** `pr-followup` on an inline comment about a catch block in
  `orders.ts` that also names `payments.ts` and `refunds.ts`; it passes when
  the claim covers all three and nothing wider.
- **Evals 1, 2, 3 and 5:** `pr-followup/evals/evals.json`, graded on their
  expectations.

Every executor read `pr-followup/SKILL.md`, `references/feedback.md` and both
`comment-style` files unless a row says otherwise; most also read
`references/github-collection.md`.

## Round 1

| Case | Arm | Host | Reply or result | Grade |
| --- | --- | --- | --- | --- |
| A | base | Codex | "The rule flags dropped promises so we can await them and keep failures tied to the test that started the work. In `<test file>`, a dropped promise settled after the test ended, so its failure surfaced through `unhandledRejection`. Bare `describe` and `it` calls from `node:test` are exempt. `<helper>` returns nothing, so none of its `<count>` calls needs `await`" (57 words) | A2 to A4 fail |
| A | base | Claude | "it flags promises a test drops. `<test file>` had one that settled after its test ended, so the failure surfaced in the `unhandledRejection` hook instead of that test. tests stay easy to write: `<helper>` returns nothing, so none of its `<count>` calls needs `await`" (about 48 words) | A2 to A4 fail |
| A | cand1 | Codex | "you can still call `describe` and `it` from `node:test` without `await` while ESLint flags other dropped promises in the tests" (20 words); Not applicable, open | pass |
| A | cand1 | Claude | "exactly, the rule skips `describe`/`it` so tests stay as easy to write, but it still catches dropped promises like the one in `<test file>`, whose failure showed up in the `unhandledRejection` hook after its test had ended" (36 words) | A4 fails |
| B | cand1 | Codex | B1: "applying a coupon now makes US state tax use the discounted subtotal. Use `withPreDiscountBase()` to calculate tax on the pre-discount price as SHOP-219 requires". B2 gives the rejected Promise case. Read only the two `comment-style` files. | pass |
| B | cand1 | Claude | B1: "applying the coupon first taxes US orders on the discounted subtotal, but SHOP-219 requires tax on the pre-discount price. use `withPreDiscountBase()` for the tax base". B2 gives the case in about 40 words. | pass |

## Round 2

| Case | Arm | Host | Reply or result | Grade |
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

| Case | Arm | Host | Reply or result | Grade |
| --- | --- | --- | --- | --- |
| A | cand3 | Codex | "the rule exempts `node:test` calls to `describe` and `it` and catches dropped promises inside the tests" (16 words); Not applicable, open | pass |
| A | cand3 | Claude 1 | "right, the runner handles `describe` and `it`, so the config exempts them and the rule only flags other promises a test drops" (22 words); Not applicable, open; probe results kept for a dispute | pass |
| A | cand3 | Claude 2 | "the rule skips the tests themselves (`describe`/`it`), so they stay as convenient to write, but it's still on for any other promise in the test code" (26 words); Not applicable, open | pass |

## Round 4

Every run used cand4. Executors for evals 1 to 3 were told that skills other
than the two staged ones are available but not staged.

| Case | Host | Reply or result | Grade |
| --- | --- | --- | --- |
| Eval 1 | Codex | Hands both PRs and the originating request to `stacked-pr` as the stack's submission; collects feedback meanwhile; repairs, publication and batched watches wait for its result under its ownership. | pass |
| Eval 1 | Claude | Reads both PRs, then hands them to `stacked-pr` with the request word for word, asking no question; no `gh stack` or `gh pr create`; watches armed once by `stacked-pr`. Did not read the `comment-style` files. | pass |
| Eval 2 | Codex | Keeps the recorded pending membership, does not resubmit or wait for a second layer, collects every channel and evaluates the comment; stack changes go to `stacked-pr`. | pass |
| Eval 2 | Claude | Same, with a fresh state check of events the T3 watch never reports, and the push routed through `stacked-pr`. | pass |
| Eval 3 | Codex | Ordinary Drive: collects every channel and reads the failing lint job before any fix; no `stacked-pr`. Did not read the `comment-style` files. | pass |
| Eval 3 | Claude | Same, with the stack check stated as none. Did not read the `comment-style` files. | pass |
| Eval 4 | Codex | "You can still call `describe` and `it` from `node:test` without `await`, and the rule catches dropped promises inside test bodies" (19 words); Not applicable, open | pass |
| Eval 4 | Claude | "tests stay as easy to write bc the rule still skips `describe` and `it`, it only flags other promises a test drops" (21 words); Not applicable, open; probe results kept for a dispute | pass |
| Eval 5 | Codex | "Fixed in 4e1c9a7. We retry because the token endpoint briefly returns 503s during deploys, and every such burst last month cleared within two retries."; applied, resolve after the reply is visible | pass |
| Eval 5 | Claude | "Fixed in 4e1c9a7. We retry because the token endpoint returns short 503 bursts while it deploys, and last month every burst recovered within two retries."; applied, resolve after the reply is visible | pass |
| B | Codex | B1: "a 10% coupon on a $100 California cart now leaves $90 subject to tax. Can we use `withPreDiscountBase()` to calculate tax on the pre-discount subtotal as SHOP-219 requires in US states?". B2 gives the case. | pass |
| B | Claude | B1: "US orders with a coupon now get taxed on the discounted subtotal, but SHOP-219 requires tax on the pre-discount price. using `withPreDiscountBase()` for the tax base would fix it". B2 gives the case. | pass |
