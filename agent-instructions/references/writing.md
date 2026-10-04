# Writing instructions

Read this when writing or revising instructions an agent consumes.

## Put decisions where they apply

A skill description or persistent-file pointer determines when detailed guidance
is reached. Name the task and distinguishing conditions; add exclusions for likely
collisions. Keep shared requirements in the entrypoint and substantial conditional
detail in references with explicit loading conditions. A bare "see references"
does not make that decision.

Fit new guidance into the existing structure: revise, combine or replace the
relevant passages, and rewrite the section or document when needed for coherence
within the authorized scope. Add separate text for a distinct decision that has
no suitable existing home. Keep each rule, its reason and exceptions together in
one authoritative home.

Orchestrators name a specialist's inputs and completion evidence rather than
copying its procedure. Create a separate skill only for a distinct task or an
independent invocation; otherwise use the existing owner or a conditional reference.

Resolve other skills by name using [hosts.md](hosts.md). Locate bundled resources
relative to this skill's resolved installation, without assuming its path or the
caller's directory. State what to read or run, when, its invocation and working
directory. Identify the target project root separately and give input/output
paths under the requested layout and local conventions. Pass project paths
explicitly when running from the skill folder.

## Preserve the intended meaning

Use familiar, precise words. Preserve actors, actions, scope, conditions,
exceptions, authority, obligation, effort and certainty: "prefer" is not "require", and "create"
does not imply "run". Explain non-obvious constraints once. Prefer the intended
action over prohibition lists while retaining consequential boundaries.

Make type, quantity, depth and completion evidence explicit where they distinguish
plausible requests. For "create tests", establish the behavior or risk, test level,
scope, whether to write or run them, and sufficient coverage or quantity. Resolve
uncertainty from the user's objective and context, asking when intent remains
unclear. Available tooling does not choose the objective. Preserve judgment within
the confirmed scope rather than inventing specificity.

Separate reusable steps from unresolved domain decisions. Resolve schemas,
rounding policies and rules for discarding records from an authoritative contract,
not invented defaults. Tell the future agent where to find that contract and when
to ask; labeling an invented default as an assumption in the completion report
does not prevent its use.

## Diagnose before prescribing

When correcting a failure, inspect the output and action trace before adding a
rule. Check loading evidence: an unread instruction needs a selection or placement
fix. When loading is unobserved, report that limit while correcting defects visible in the text.

| Observed failure | Useful correction |
| --- | --- |
| Wrong structure or order | State the required parts in the order the reader needs them. |
| Missing required element | Give it a field or slot in the existing output structure. |
| Rule applied in the wrong circumstances | State the observable condition and action for each branch. |
| Understood requirement bypassed | Address the observed shortcut and test it under relevant pressure. |
| Authorized work left unfinished at a phase boundary | Trace the next actor and resumption path before changing continuation. |

At a handoff, distinguish a phase in the same conversation, a real child-agent
return, a user decision and a host-supported pause with later resumption. State
the next required action where the same agent continues; preserve genuine return
boundaries, decisions and blockers. A pause is not itself a failure. Repair the
observed transition without widening authorization or making required work optional.

Preserve material exceptions and counter only observed workarounds.

## Make progress observable

Keep fixed sequences where order protects an invariant, such as identity checks
before a remote write. Give open-ended work a result and decision criteria rather
than a ritual. End phases with evidence that distinguishes completion from an
attempt; loops need a progress signal, an end condition and a response to a
recurring blocker.

## Reconcile overlapping guidance

Compare trigger, owner, action, completion evidence and authority. Similar prose
can hide incompatible behavior, such as a read-only review and an automatic repair.
Resolve conflicts from established authority, scope or an explicit user decision;
ask when those do not settle the intended behavior. Then keep the governing rule
or state distinct conditions.

Record intentional donor deviations in an existing skill's provenance record;
other documents keep their established attribution conventions. Popularity does
not justify replacing a local rule. Check changes to invocation, approvals,
testing, tools and external writes especially carefully.

## Prune without weakening the contract

Remove duplicate meanings, generic encouragement and guidance already supplied
by an authoritative local owner. Use configuration and CLI help for discoverable
facts; retain the reason or gotcha they cannot supply.

Distinguish general technique from project constraints, team preferences and
organizational policy. They can be valuable even when they differ from a model's
default. Code and tests show behavior without necessarily establishing intended
policy; keep a consequential rule's reason and source reachable, especially when those disagree.

Before deleting a rule as enforced elsewhere, inspect the actual configuration,
execution path and coverage. Preserve rare consequential constraints and authorized
preferences. Brevity, a donor's score or a capable model's apparent knowledge cannot
establish redundancy. Use behavioral evidence when value is uncertain; a small
passing sample does not justify retirement.

Compare the revision with the original meaning and evidence. Compression must not
turn a suggestion into a universal rule, a read into a write or an attempted check
into a successful one.
