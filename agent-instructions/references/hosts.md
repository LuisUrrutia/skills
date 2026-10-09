# Host compatibility

Read this for skills before choosing invocation controls, host metadata, tool
calls, or dependencies on other skills. Persistent instruction-file placement is
covered by [instruction-files.md](instruction-files.md).

Inspect the intended host's installed skill format, available tools, and current
primary documentation when local evidence is insufficient. Separate portable
instructions from host-specific adapters. An unfamiliar frontmatter key is not
portable merely because another agent accepts it.

- Use `name` and a precise `description` as the shared entrypoint. Preserve
  supported existing metadata rather than rebuilding the whole file.
- Preserve the existing invocation policy. New skills remain discoverable unless
  the user requests another mode; changing invocation is a product decision,
  separate from permission for a particular action.
- In Codex, use `skill-creator` for host requirements before editing
  `agents/openai.yaml`. A generator may replace the entire file; preserve
  unrelated policy and dependency settings.
- Treat Claude-style frontmatter and Codex invocation policy as separate host
  features. Verify their current behavior rather than copying one into the other.
- Reference other skills by their registered names, never by filesystem paths to
  their entrypoints or internal resources. When routing work to another skill,
  name the skill and its inputs; do not point the reader at a resource inside it,
  by path or by description such as "its PR review reference". That skill's
  entrypoint decides what it loads. Use a resource its entrypoint documents for
  callers, such as a validator to run or a protocol to freeze, only through that
  documented contract. Resolve each name through the installed catalog and the
  host's supported invocation mechanism. File links within the current skill may
  address its own resources.
- Loading a Markdown file and invoking a skill are not interchangeable on every
  host. Detect missing required dependencies before dependent work.
- Prefer available host tooling. A reference to a donor's CLI, task manager,
  evaluator, or viewer does not install it or make it necessary.

If the host supplies a creator, use it for its packaging requirements and available
validators. This skill owns composition and evaluation; the host creator supplies
mechanics. Reconcile applicable instructions explicitly rather than nesting two
complete authoring workflows or installing a second same-named creator.

Follow the required consultation and reconciliation contract in
[the entrypoint](../SKILL.md#get-both-model-perspectives) on every host. Model
reviews assess instructions; they do not establish runtime execution.

Validate on each supported host before claiming compatibility. If only structural
checks or supplied-context trials are available, state that limit. File presence
alone does not prove installation, implicit selection, or runtime execution.
