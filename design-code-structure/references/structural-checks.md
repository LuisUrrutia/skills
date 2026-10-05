# Prove a structural boundary

Read this when designing, adding, or changing a check for the selected data,
interface, or module boundary, or when a boundary change exceeds an existing
check's demonstrated coverage. Reuse relevant evidence when its inputs and
coverage still apply. A design-only request produces a validation plan; an
isolated experiment may test it when that fits the requested design work.
Installing or changing a check in the project requires implementation authority.
Honor explicit read-only restrictions on experiments as well as product changes.

## Match the mechanism to the contract

Name the invariant, the callers and paths it covers, supported exceptions, and
the failure it prevents. Prefer expressing the rule through the existing data
model or public interface when that preserves valid states and behavior. Use the
project's type, lint, test, or build mechanism for what structure cannot express.
A runtime trust or mutable-state check cannot be replaced by static enforcement.

Inspect the existing configuration and the command that actually consumes it.
Reuse established tools and verification entry points. Add a custom check only
when the invariant cannot be expressed by those mechanisms; keep a repeatable
check in the project's suite or task runner. Do not install a general architecture
toolkit to protect one boundary.

Land the rule together with the handling of existing violations so the check
passes. Fix in-scope cases or use the tool's narrow rule-specific exceptions
with their reason and retirement condition. Keep that handling in existing tool
configuration rather than adding a parallel violation-count baseline.
Migration exceptions identify existing offenders without silently exempting new
ones; category exclusions such as generated code retain their intended scope.
Preserve other rules' coverage and supported compatibility routes. A warning or
report-only stage can make migration visible, but does not establish a blocking
gate. Unresolved violations or unavailable execution stay visible as gaps; do not
disable the rule or widen exclusions to obtain a passing result.

## Exercise the real path

Plan both a supported input and an in-scope violation before changing the check.
Choose a violation representative of the failure, including import forms or
aliases that matter to this boundary. During authorized implementation or an
isolated design experiment within scope:

1. Run the project's real check command on the supported case. Confirm it
   actually examines the intended files or relationships; exit 0 on no inputs
   is not a baseline.
2. Introduce the violation in a disposable fixture or isolated copy that uses
   the same configuration and command. Observe failure for the intended rule,
   with a diagnostic that identifies the violated contract or its correction.
   An unrelated syntax error, missing dependency, or different failing test does
   not establish detection. If the tool's message is fixed, keep the explanation
   beside the rule or in the existing project guidance.
3. Remove only the owned mutation and rerun the same command. Confirm the
   supported case passes and the fixture or copied tree has been restored.
   Preserve pre-existing and concurrent edits; do not reset the user's tree.

Keep the failure contained: no deliberately invalid live data, deployed changes,
or permission-policy changes. If a representative isolated probe is not possible
within scope, report the missing proof instead of introducing a live failure.
Existing unrelated failures require a separately observed, relevant result;
they never become a claim that the full command passed.

Follow the exit status through the actual entry point. An underlying tool's
failure is insufficient if its wrapper suppresses it, a filter skips the affected
path, the check is skipped by a condition, cached output ignores the mutation,
or the rule only warns. Connect the check to the existing required verification
route within scope. Use `github-actions` when that requires workflow changes;
hooks, remote policies, schedules, and
automatic approvals are separate choices, not prerequisites of this procedure.
Use `create-project-instructions` when requested project guidance needs discovery;
an already-established clause can go to `agent-instructions` directly. Use `verify`
for application-level execution evidence. Resolve each skill by registered name.

Record the command, inputs, observed status and relevant diagnostic for the valid,
violating, and restored cases, plus the route that invokes the check. Distinguish
a proposed check, an observed check, and a gate wired into that route. A local
run cannot establish remote enforcement that was not exercised.
