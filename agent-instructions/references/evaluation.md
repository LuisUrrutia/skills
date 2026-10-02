# Evaluation

Read this when changing instruction behavior, creating or combining skills,
changing routing, incorporating upstream changes, or correcting observed failures.

## Choose evidence before tuning

Derive cases from the instruction's contract and realistic artifacts. Cover ordinary
work, ambiguous inputs, and relevant boundaries. For a router, include tasks that
select different specialists and tasks that should select none. For a workflow
with external effects, observe actions and resulting state, not just the final
explanation.

Keep expected outcomes separate from executor inputs. Reserve some cases for a
later check, without using their results to write the first revision. Once a
reserved failure informs a fix, it is a regression case; use a new unseen case
before making a further generalization claim.

[../evals/cases.json](../evals/cases.json) contains reusable cases for
`agent-instructions` itself. Read that corpus only when evaluating this skill,
and keep its expectations with the grader. Other documents and skills need cases
derived from their own contracts.

For persistent instruction files, test scope as well as meaning: a global rule,
a repository rule, and a nested override reach different work. Include imports
or adapters in the fixture when they determine the effective instruction. A
focused edit need not acquire a permanent evaluation suite.

## Run a matched comparison

For new instructions, compare with the same task without those instructions. For
an update, compare with the previous document or skill snapshot. Keep model, effort, tools, fixtures,
authorization, and output format equal. Use independent clean contexts so a
baseline cannot see the candidate or an earlier answer.

If independent agents are available and authorized, give an executor the realistic
request, relevant skill, and raw artifacts. Keep expected outcomes, suspected
defects, and proposed fixes out of its prompt. Otherwise use the available runner
or report the missing behavioral evidence. Do not simulate a successful run in
the author's explanation.

Run in isolated scratch storage under the repository's temporary-file rules.
Use local fixtures or fakes for external effects unless the evaluation is already
authorized against the real service. Introduce a permanent helper only when the
recurring evaluation needs one.

## Grade outcomes

Separate these claims:

| Claim | Required evidence |
| --- | --- |
| Valid structure | Resolved pointers/imports; metadata and host checks when packaging a skill |
| Correct selection | Positive and near-miss requests with observed host selection |
| Useful task behavior | Actual output artifacts, actions, and postconditions |
| Safe authority | Observed side effects stay within the supplied authorization |
| Improvement | Matched baseline results, including regressions and failures |

A model asked which description it would choose provides a selection probe, not
proof of a host's implicit invocation. A tool-free artifact exercise can check
generated instructions and proposed decisions, but cannot prove tool execution,
installation, or network behavior.

Record case, skill revision, model, effort, supplied resources, output, verdict,
and concrete evidence. Record tokens or duration only when measured. Mark
unobservable outcomes as not tested; do not count them as passes. If both versions
pass, report that result rather than claiming a demonstrated improvement.

Use objective checks for file formats and postconditions. Read substantive output
for scope, correct decisions, unnecessary questions, and unjustified claims.
Keyword presence and confident self-reports are insufficient evidence.

## Iterate proportionately

Fix an observed failure at its responsible instruction or reference. Re-run the
affected case and a nearby case that could regress. Broaden testing when a change
affects shared routing, authority, or termination.

For nondeterministic failures or performance claims, use repeated matched trials
and report variation. A small passing sample supports only the tested cases.
Stop once the contract is met and material failures are accounted for; report
remaining limitations rather than adding speculative rules.
