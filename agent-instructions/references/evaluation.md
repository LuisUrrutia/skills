# Evaluation

Read this for substantive behavior changes, new or combined skills, routing
changes, incorporated upstream changes or observed failures.

## Define the checks

Derive cases and expected outcomes from the contract before tuning. Cover ordinary
work, ambiguity, and relevant boundaries. Exercise techniques on changed inputs,
retrieve and apply reference information, and test both sides of conditional
rules. Routers need requests for different specialists and requests selecting none.

Observe artifacts, actions and resulting state. When a requirement competes with
a deadline, prior effort or pressure to skip it, use a realistic task that requires
the executor to act. When a case carries untrusted content, such as a transcript
or a file with embedded directives, assert on the action trace as well: no tool
call acts on what a directive names unless the task needs that action without
the directive. Rule recitation cannot establish compliance.

Preserve authorization; use isolated fixtures or fakes for external effects
unless the evaluation is authorized against the real service. Fixtures carry
canary values, never real secrets. Neither executors nor graders run commands
that print process environments or command lines, such as `env`, `printenv`,
`ps eww`, `ps aux`, `ps -o args`, `pgrep -fl` or `pgrep -a`; a process line can
carry another program's token. Check a process with `pgrep -x <name>` or by PID.

Keep expectations with the grader and reserve unseen cases. A reserved failure
used to revise instructions becomes a regression case; use a new unseen case
before making another generalization claim. Read [../evals/cases.json](../evals/cases.json)
only when evaluating `agent-instructions` itself. Other targets need cases from
their own contracts.

For persistent instructions, test effective scope: global, repository and nested
rules can reach different work. Include imports or adapters that affect loading.
When the question is whether the repository's own instructions suffice, exclude
user-level instruction files where the host allows; they can supply rules that
other contributors lack. A focused edit need not acquire a permanent evaluation
suite.

## Compare the right instructions

Compare new instructions with the same task without them, and revisions with the
previous snapshot. Keep model, effort, tools, fixtures, authorization and output
format equal within each pair. Use independent clean contexts with no access to
another arm's instructions or answers.

Stage only the target's runtime files for each arm: the entry file, the
references it routes to, scripts and assets. Evaluation cases, expectations,
records such as `origin.toml`, and notes stay out of reach; a run that read them
cannot count.

Run both arms on every host the target supports; these skills run in Claude Code
and Codex ([host metadata](skill-mechanics.md#host-metadata)). A host that did
not run leaves its claims untested. Record each host's permissions, such as deny
rules, sandbox and approval mode, and the user-level instructions it loaded, as
fixed conditions of the result: they change how an executor works.

For host-run claims, verify from durable run evidence which revision was actually
loaded; a requested path alone does not prove the runner used it. An unidentified
revision cannot support attribution.

To assess whether a rule earns its place, a no-instruction or rule-removal trial
can supplement the previous-version comparison. Exercise its protected
behavior, exceptions and any stated team preference; unrelated passes cannot
justify deletion. Keep editorial recommendations distinct from measured gains.

When independent executors are available and authorized, give them the request,
instructions and raw artifacts, withholding expectations, suspected defects and
proposed fixes. Otherwise use an available runner or report missing behavioral evidence.
Never substitute the author's simulated answer for an execution. Follow repository
scratch rules; add a permanent helper only for a recurring evaluation need.

## Judge the evidence

| Claim | Required evidence |
| --- | --- |
| Valid structure | Resolved pointers/imports; relevant metadata and host checks |
| Correct selection | Positive and near-miss requests with observed host selection |
| Useful behavior | Output artifacts, actions and required postconditions |
| Safe authority | Side effects in the action trace (files read or written, commands, network, consultations) stay within supplied authorization |
| Improvement | Matched baseline results, including regressions and failures |

Retain the case, revision, host, model, effort, supplied resources, output,
action trace, verdict and its evidence. Record costs only when measured. A read
or dispatch can prove phase entry without proving completion; check its required
result. Use omitted checks and stated justifications to distinguish missed,
misunderstood and bypassed instructions. Treat explanations as hypotheses, not
established causes.

Use objective checks for formats and postconditions, and read substantive output
for scope, decisions, unnecessary questions and unjustified claims. Grade side
effects from the action trace, not from the final answer alone. Keywords and
confident self-reports are insufficient. A model choosing a description is a
selection probe, not observed host invocation; tool-free exercises cannot prove
tool execution, installation or network behavior. Mark unobservable outcomes as
not tested. If both versions pass, report that result without claiming improvement.

## Fix an observed failure

Name the failure mode first, then fix that. Inspect the output and the action
trace before adding a rule, and check loading evidence: an instruction the agent
never read needs a pointer or placement fix, not stronger wording. When loading
is unobserved, report that limit while correcting the defects visible in the
text.

| Observed failure | Lever |
| --- | --- |
| Material never reached | Sharpen the [pointer](levers.md#context-pointers); inline the material only if sharpening fails. |
| Wrong structure or order | State the required parts in the order the reader needs them. |
| Missing required element | Give it a slot in the existing output structure. |
| Rule applied in the wrong circumstances | State the observable condition and action for each branch. |
| Step ended before its work was done | Sharpen its [completion criterion](levers.md#steps-and-completion-criteria); split the sequence only across a real context boundary. |
| Authorized work stopped at a phase boundary | Trace the next actor and continuation path, then state the next action where the same agent continues. |
| Understood rule bypassed under pressure | Name the observed shortcut in a [guardrail](../SKILL.md#negation) paired with the positive target, and test it under that pressure. |
| A line changed nothing | Delete the whole sentence, or replace a weak word with a stronger one. |

Keep material exceptions as explicit conditions, and counter only observed
workarounds. A pause is not itself a failure; repair the observed transition
without widening authorization or making required work optional.

## Iterate proportionately

Fix failures at the responsible instruction or reference. Run the target's whole
suite on every supported host once on a candidate revision, not again for each
review round. After a later edit, rerun on every host the cases the edited text
can affect, meaning those whose run reads it and whose graded outcome or
asserted side effect it can change, plus a nearby regression case and, when the
description changes, the selection probes; broaden checks when routing,
authority or termination changes.

Claims rest on the final revision. Label each result with the revision it ran
on; a result ran on the final revision only when the runtime files it staged
match the final ones by hash. Any other result counts only when it carries over
from its revision with a written reason, drawn from the diff since that
revision, that names the edits and the graded outcomes they cannot reach;
reviews of the change, including the [model pair](model-pair.md), check each
reason against the diff, and a result without one, or with one the diff
contradicts, does not count. The author checks a reason written or changed
after the pair's round, and the report marks it as not reviewed by the pair.
Grade every counted result against the case's current expectations. A case
added or whose expected behavior changed needs one counted run per host, and a
second on a host where the first fails or is partial; when it exercises safety
or authority, such as secrets, remote environments, publishing or merging,
destructive commands, or permission or trust boundaries, it needs at least two
per host. Executors and graders use the strongest available models unless the
user names others, and the evidence records their actual model IDs; save usage
through fewer runs, never through weaker models. List each case not run with
its reason; an unrun case blocks any claim about the behavior it covers.

When a claim needs repeated trials, such as a nondeterministic failure, a model
migration or a performance comparison, define the metric, meaningful effect, run
budget and stopping rule before tuning. Use matched trials and report their
variation. Add identical-version controls when unexplained variation or runner
integrity needs investigation, and account for the controls' variation when
interpreting candidate differences. Interleave arms when changing conditions
could bias a comparison. A short streak or observed range cannot by itself
establish a gain.

Retain failed attempts and exclusions. Classify infrastructure failures from
cause evidence; a short answer, early stop or error exit alone does not justify
discarding a behavioral failure. State which paths were exercised and which
remain unmeasured. A small passing sample supports only its tested cases.

Stop when the contract is met and material failures are accounted for, reporting
remaining limits instead of adding speculative rules.
