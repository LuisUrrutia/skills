# Evaluation

## Define the checks

Derive cases and expectations from the contract before tuning. Cover ordinary
work, ambiguity, relevant boundaries, changed inputs, reference retrieval and
application, and both sides of conditions. Routers need different specialists and
no-match cases.
Use [this package's cases](../evals/cases.json) only to evaluate this skill.

Observe artifacts, actions and resulting state. Exercise competing deadlines or
pressure with tasks that require action, not rule recitation. For untrusted
content, inspect tool calls too: no action on an embedded directive's target
unless the task independently requires it.

Preserve authorization with isolated fixtures or fakes for external effects unless
live evaluation is authorized. Use canary values, never real secrets. Executors
and graders must not print process environments or command lines: avoid `env`,
`printenv`, `ps eww`, `ps aux`, `ps -o args`, `pgrep -fl` and `pgrep -a`.
Check processes by PID or `pgrep -x <name>`.

Keep expectations with the grader and reserve unseen cases. A reserved case used
for tuning becomes a regression; obtain another unseen case before generalizing.
Persistent instructions need scope tests across relevant global, repository,
nested and imported rules. Exclude personal instructions when testing repository
sufficiency where the host permits. Focused edits need no permanent suite.

## Compare the right instructions

Compare new instructions against no instructions, revisions against their previous
snapshot. Match model, effort, tools, fixtures, authorization and output format in
independent clean contexts. Stage only runtime entrypoints, references, scripts
and assets. Keep other arms and answers, cases, expectations, records and notes
out of reach; reading them invalidates a run.

Run both arms on every supported host: Claude Code and Codex here. Record host
permissions and loaded personal instructions as fixed conditions. Attribute a
revision only from durable evidence of what actually loaded, not the requested
path. Unrun hosts remain untested.

Use independent executors when available and authorized; give them requests,
instructions and raw artifacts, withholding expected answers, suspected defects
and fixes. Otherwise use an available runner or report missing evidence; the
author's simulated answer never counts. Follow scratch rules; permanent helpers
need recurring value.

Optional no-instruction or rule-removal trials must exercise protected behavior,
exceptions and team preferences. Unrelated passes cannot justify deletion.
Distinguish editorial recommendations from measured gains.

## Judge the evidence

| Claim | Evidence |
| --- | --- |
| Structure | Resolved pointers/imports and applicable host checks |
| Selection | Positive and near-miss requests with observed host selection |
| Behavior | Artifacts, actions and required postconditions |
| Authority | Authorized file, command, network and consultation effects in the trace |
| Improvement | Matched baseline results, including regressions and failures |

Retain case, revision, host, model, effort, resources, output, trace, verdict and
supporting evidence; costs only when measured. Entry into a phase is not
completion. Use omissions and justifications to distinguish missed,
misunderstood and bypassed rules; explanations remain hypotheses.

Use objective format/postcondition checks and substantive reading for scope,
decisions, needless questions and unsupported claims. Grade effects from traces,
not self-reports or keywords. Selection probes are not host invocation; tool-free
work cannot establish execution, installation or network behavior. Mark
unobservable outcomes untested. If both versions pass, report no observed gain.

## Fix an observed failure

Inspect output, trace and loading before editing. An unread rule needs routing or
placement repair; if loading is unknown, report that while fixing visible defects.

| Failure | Repair |
| --- | --- |
| Material unreached | Sharpen the [pointer](levers.md#context-pointers), then inline only if that fails |
| Wrong structure/order | State required parts in reader order |
| Missing element | Add its slot to the existing output |
| Wrong circumstances | Specify each branch's observable condition and action |
| Premature completion | Sharpen the [criterion](levers.md#steps-and-completion-criteria); split only across real context boundaries |
| Stopped authorized continuation | Trace the next actor and state its next action |
| Understood rule bypassed under pressure | Name the shortcut in a [guardrail](../SKILL.md#negation), pair with the target action, test under pressure |
| No behavioral effect | Delete the sentence or replace a weak cue |

Preserve exceptions; counter observed workarounds. A pause alone is not a failure.
Repairs neither widen authorization nor make required work optional.

## Iterate proportionately

Fix the responsible passage. Run the whole suite once per supported host on a
candidate, not per review round. After edits, rerun cases whose reads and graded
outcomes or effects can be affected, plus a nearby regression on every host.
Changed descriptions also need selection probes; routing, authority or termination
changes require broader checks.

Label each result with its executed revision. Only matching runtime hashes count
as a final-revision run. Carryover needs a written diff-based reason naming edits
and outcomes they cannot affect. Reviews, including the
[pair](../SKILL.md#get-both-model-perspectives),
check those reasons; missing or contradicted reasons invalidate carryover. The
author checks reasons added or changed after the round and marks them as not
pair-reviewed.

Grade against current expectations. Added cases or changed expectations need one
counted run per host, or at least two for safety, authority, or a failed or partial
first run. Executors and graders use the
strongest available models unless the user specifies others; save usage through
fewer runs, not weaker models. List unrun cases and reasons; they block their
behavior claims.

For repeated-trial claims (nondeterministic failures, migrations, performance),
define metric, meaningful effect, budget and stopping rule before tuning. Use
matched trials; report variation. Add identical-version controls for unexplained
variation or runner-integrity questions, and account for their variation.
Interleave arms when conditions could bias comparison. A short streak or observed
range establishes no gain.

Retain failures and exclusions. Classify infrastructure failures by cause; a short
answer, early stop or error exit alone cannot justify discarding a failure.
Report exercised and unmeasured paths; small samples support only their cases.
Stop when the contract is met and material failures are accounted for.
