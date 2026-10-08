# T3 child-task transport

Read this instead of launching the full CLI roster when running inside T3 Code.
The parent coordinates the same three independent attempts and owns synthesis.

## Dispatch

1. Call `orchestrator_capabilities` and resolve the Codex and Claude provider,
   model and supported effort options from that live catalog. Honor requested
   profiles; never infer provider IDs from display names. If tools are initially
   absent, use the host's documented discovery or ACP transport fallback before
   reporting delegation unavailable.
2. Verify the snapshot with `scripts/snapshot.py verify`. Initialize a parent-only
   `delegated-tasks.json` with the snapshot digest and an entry per seat containing
   provider, model, effort options, attempt, request ID, task ID, status and artifact paths.
   Preserve each returned task ID immediately. On restart, inspect those tasks
   before dispatching anything. Reuse requires the same snapshot and valid outputs.
3. Launch Codex and Claude with separate `delegate_task` calls, `mode: async`,
   `role: review`, a seat-specific title, and explicit catalog-resolved targets.
   Explicitly inherit `runtimeMode` and `interactionMode`; record their effective
   values with the task. Do not elevate permissions to bypass a host restriction. Use a stable
   `clientRequestId` per snapshot, seat and attempt, including across transport
   retries. Supply the complete frozen packet, its readable input paths and the
   reviewed checkout. Each child is the reviewer itself; do not ask it to launch
   another Codex or Claude CLI. Give each child an exclusive report path under its
   own seat directory. As a transport-only override to the packet's final-output
   instruction, have it write the canonical report there, run the frozen
   `inputs/report.py validate` once with the inventory, and return the artifact
   path and validation result. It may write only that report, not product files;
   it must not fetch feedback, delegate or inspect sibling outputs. Preserve an
   invalid report for the parent's bounded correction round. Give both identical
   audit inputs and no prior conclusions.
4. Launch a third child named CodeRabbit runner using an available host provider.
   Its task is only to run the exact guarded local CodeRabbit command below, retain
   native output and return a verbatim subset-state readback. It must not perform a model review or
   reinterpret findings. From the reviewed repository, its command is:

   ```bash
   python3 "$SKILL_DIR/scripts/reviewers.py" run \
     --snapshot "$SCRATCHPAD/inputs/snapshot.json" \
     --pr-json "$SCRATCHPAD/pr.json" --scratchpad "$SCRATCHPAD" \
     --workers coderabbit
   ```

   Start this as a host-managed background execution, retain its process handle,
   and observe it with bounded waits as in the CLI supervisor reference; a single
   foreground tool timeout is not the worker's 1500-second deadline.
   Resolve all variables to actual paths in the brief. The selected host model is
   the runner, not the CodeRabbit engine; record both identities separately.
5. Start the feedback collector separately in a parent-managed background process:

   ```bash
   python3 "$SKILL_DIR/scripts/reviewers.py" _collect-feedback \
     --pr-json "$SCRATCHPAD/pr.json" \
     --output-dir "$SCRATCHPAD/existing-feedback"
   ```

   Keep its process handle and logs. Do not read its findings before independent
   synthesis. A collector process need not masquerade as a fourth reviewer.

Do not use `t3_thread_launch`, `create_threads` or `t3_thread_send` to create or
continue these delegated attempts. Those create or operate ordinary conversations.
Do not run `reviewers.py run` without `--workers coderabbit` alongside this route.
The subset supervisor's `subset_completed` means only that local seat completed;
it does not establish completion of the three-engine review.

Native children follow the host's actual tool permissions. The CLI sandbox flags
are not applied to native delegation: record the effective restrictions and any
isolation limit rather than claiming OS sandbox parity. Keep private material out
of prompts and prohibit sibling/feedback reads. Where host or repository policy
requires enforced read isolation unavailable in the child runtime, report that
seat blocked instead of silently weakening that policy.

## Completion and format repair

Continue the parent seam sweep while children work. T3 completion notifications
wake the parent; use `task_status` when a result is needed mid-turn. If no
independent work remains, yield to the armed notification. Do not busy-poll or
launch a separate watcher. Observe the collector through its saved process handle.
For cancellation or snapshot drift, cancel live children with `task_cancel` using
the recorded task IDs and stop owned local processes; confirm they are terminal
before starting replacements. Preserve their outputs as invalidated evidence.

Read each terminal Codex/Claude report from its assigned artifact path, preserving
its bytes; do not reconstruct it from a task summary. Independently run:

```bash
python3 "$SKILL_DIR/scripts/reviewers.py" validate-report \
  --snapshot "$SCRATCHPAD/inputs/snapshot.json" --report "$REPORT"
```

Use the actual assigned report path. This uses the frozen canonical validator,
exact inventory and the snapshot's Scope; it also checks snapshot drift.
Record transport status separately from validation status, exact diagnostics,
report digest and observed model/effort. Check the snapshot again before accepting
any output. An unchanged task result is not reusable after snapshot drift.

For a format failure, archive the raw report and diagnostics. Call `delegate_task`
again for that same provider/model with a new attempt request ID, the original
packet, only that seat's previous report and the exact validator errors. Ask for
format correction without adding findings, claims or coverage. The validator
stops at the first error, so require a full pass over the supplied grammar,
including single-line evidence locations and a single backtick span per Checks
command. Have the child write a new artifact and validate it once. This is the second
and final attempt. Do not send a message to its backing `childThreadId`; record the
new task ID. Revalidate the result and compare every finding with the archived
report. Record changed or missing findings; do not accept silent finding loss or
new unsupported claims as a successful format repair. Transport failures share the same two-attempt
budget. An uncertain dispatch response needs reconciliation using its stable
request ID, not a new seat launch.

Read CodeRabbit's native report and subset state using the normal validators.
The wrapper child's successful turn alone does not prove the CLI completed. After
all seats terminate, aggregate their validated outcomes with the collector's actual
manifest. Keep `delegated-tasks.json` separate from the CLI supervisor's evidence;
never insert fake native workers into `reviewers-state.json`. Missing, cancelled,
invalid or failed seats leave the overall review incomplete. Preserve useful
findings with their source and limitation, then follow the ordinary parent ledger
and feedback reconciliation steps.
