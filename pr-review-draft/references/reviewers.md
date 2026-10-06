# Reviewer supervision

Read before preparing inputs, launching, consuming events or reporting status.
Resolve `SKILL_DIR` from this package and `AUDITOR_DIR` from the registered
`review-code-changes` installation. `SCRATCHPAD` is a new ignored directory under
the reviewed project's permitted scratch root. Keep one directory per snapshot.
Commands below use shell variables whose real paths the parent has resolved.

## Shared input

```bash
python3 "$SKILL_DIR/scripts/snapshot.py" prepare \
  --repository "$REPOSITORY" --pr-json "$SCRATCHPAD/pr.json" \
  --context "$SCRATCHPAD/review-context.md" --audit-skill "$AUDITOR_DIR" \
  --output-dir "$SCRATCHPAD/inputs"
```

Append `--profile "$PROFILE"` only for an exactly matched external private profile.
Append `--rules "$RULE_FILE"` for each applicable repository or domain guide,
including a resolved React guide when needed. Every engine gets the same guides;
a guide absent for one participant is a recorded access gap, not presumed parity.
Keep access/account/tracker details and prior review conclusions out of those files.
The context records each rule's authority and applicability and caller-owned seams.

The adapter freezes the current protocol and its validator as run artifacts; it
never maintains a second audit implementation. The frozen packet supplies the
single non-delegating participant role instead of the auditor's standalone
orchestration. It points to frozen diff and inventory files for tools without shell
access; Claude's restricted read scope explicitly includes that input directory.
Runtime probes need a separate authorized parent investigation.
Codex uses `exec` with that review packet: `exec review` applies its own finding
formatter and did not preserve the canonical report in the real CLI trial.

## Launch and observe

From the reviewed repository, start one host-managed background execution:

```bash
python3 "$SKILL_DIR/scripts/reviewers.py" run \
  --snapshot "$SCRATCHPAD/inputs/snapshot.json" \
  --pr-json "$SCRATCHPAD/pr.json" --scratchpad "$SCRATCHPAD"
```

Optional explicit `--codex-model`, `--codex-effort`, `--claude-model` and
`--claude-effort` values must come from the host's available catalog. Omitted model
settings use engine defaults; the state records the request and CLI versions,
not an invented actual model. Preserve native logs for any model/effort disclosed
at runtime. `--worker-timeout` defaults to 1500 seconds. A failed seat may retry
once (`--max-attempts 2`) by rerunning this exact invocation only when its cause
is recoverable. There is no automatic roster substitution or usage-credit consent.

The supervisor locks the run against duplicate launches. It records worker
commands/settings, executable/version, start/end time, attempts and failure cause.
Reuse requires unchanged snapshot, semantic index/worktree/HEAD state, rules, runner and settings,
plus valid outputs. It archives failed-attempt outputs before a retry. Treat a
stale snapshot as a new assessment, not another attempt of the same run.
Index stat-cache refreshes and unrelated branch fetches do not change the frozen
comparison. Changes to staged entries/flags or HEAD do. Keep the captured PR JSON,
context and rule sources immutable; write refreshed PR metadata to another file.
A changed rule requires reassessment. A changed CLI version requires a new run,
so cached results are never silently mixed with another executable version.

The guards prevent changes to the reviewed checkout and Git directories and
hide sibling outputs, the private manifest and the unfiltered profile. Codex uses
its native named permissions profile extending `:read-only`, with command network
access, approvals, plugins, hooks and nested agents disabled. Its native sandbox
must not be nested inside macOS `sandbox-exec`. Claude and CodeRabbit use macOS
`sandbox-exec` or Linux bubblewrap; unavailable guards stop their launch. Claude
exposes only Read/Glob/Grep with hooks, MCP and automatic skill discovery disabled.
CLI-managed runtime state outside the reviewed
checkout is separate from product mutation. These controls do not guarantee a
provider's network privacy; CodeRabbit's local CLI can use its remote service.

Wait with a bounded host-managed call while the parent continues independent work:

```bash
python3 "$SKILL_DIR/scripts/reviewers.py" wait \
  --scratchpad "$SCRATCHPAD" --after 0 --kind reviewer --timeout 60
```

Consume the returned events through [ledger.md](ledger.md), then use its
`last_sequence` as `--after`. A timeout does not establish completion. Status and
wait detect a dead supervisor and report `interrupted` or live `orphaned` workers,
without rewriting saved execution evidence. Re-arm while supervised workers remain
nonterminal. Yield a turn only if the host has armed a wake
for this process; otherwise continue bounded waits. A standalone process does
not wake an agent by itself. For status:

```bash
python3 "$SKILL_DIR/scripts/reviewers.py" status --scratchpad "$SCRATCHPAD"
```

## Outputs and meaning

- `claude/review.md` and `codex/review.md`: canonical code change reports,
  validated against the exact changed-path inventory.
- `coderabbit/review.jsonl`: native output, including context, findings and
  completion. CodeRabbit 0.8.2 was observed to emit a final `complete` event with
  `status: review_completed`, an integer `findings` count and optional
  `reviewedFiles`. An empty comparison emitted `review_skipped` with zero findings;
  accept that only for an empty inventory. Empty output, errors, action_required,
  malformed events, missing completion or a count/snapshot mismatch fail the seat.
  The initial 0.7.5 probe auto-updated to 0.8.2. Retain native update logs alongside
  the version captured at launch; that launch value alone may not identify the
  version that finished a self-updating CLI run.
  Launches use `--fresh` so a local checkpoint cannot suppress the full independent
  review. A completion explicitly saying no fresh detailed review occurred fails
  validation; it is not a successful zero-finding audit. Do not add `--use-credits`
  by inference if the CLI asks for usage-credit consent.
- `reviewers-state.json`, `reviewer-events/`, engine logs and `attempts/`: execution
  evidence owned by the supervisor. Do not rewrite these to repair a failed seat.
- `candidate-ledger.md`: initialized once, then written only by the parent.
- `existing-feedback/`: parent-only collector output, unread until independent
  synthesis and the seam sweep are complete.

Native `reviewedFiles` is provenance, not fabricated canonical per-path coverage.
Record what CodeRabbit actually reports and preserve missing coverage as a limit.
A transport-complete seat is not proof of complete reasoning or correct findings.
An unsuccessful requested engine makes the three-engine workflow incomplete.

Use the canonical auditor's severity definitions based on demonstrated consequence.
CI failure is not automatically `blocker`; vendor labels remain provenance.
Class and required/optional Action survive synthesis independently of severity.
