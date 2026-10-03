# Feature map contract

The generated skill owns `features/README.md` and a sibling Markdown file for
each mapped feature. This is executable guidance for another agent, grounded in
the application. Do not copy the donor's example commands or invent a harness.

The index describes baseline prerequisites, instance/data identity, driving and
reset conventions, proof and blocked-path reporting, and unmapped coverage. Its
`## Features` section links each feature file once using a relative Markdown
link. Each indexed file is a direct sibling of the index. The index and files
must agree; preserve existing stable feature IDs when maintaining them.

Each feature file has an H1 and a short user-visible description, followed by
these four H2 sections in order:

1. **Sub-features:** stable short IDs and the behavior each covers.
2. **How to get to it (user POV):** every known user entry point, including
   shortcuts or alternate clients where relevant.
3. **Driving it with the actual harness:** replace that phrase with
   `Driving it with <real harness name>`. Start with explicit preconditions.
   Pair each user action with the exact command/tool action and independently
   observable expected result. Include readiness waits, reset, and proof capture.
4. **Gotchas:** focus, timing, data, permissions, or session conditions that can
   invalidate an otherwise plausible run.

Concrete values in the recipe must be usable, with runtime parameters explained
where they are necessary. For example, a run-owned data directory is variable;
the flag that supplies it must be the application's real flag. Describe how
the caller obtains parameters rather than leaving unresolved placeholders.

Capture both action and outcome. A screenshot of the final screen alone cannot
show which control produced it. A save confirmation alone does not establish
persistence. Include a second observation of the stored result where that is
the feature's contract. Record the feature and entry point with evidence.

Treat this structure check as a way to catch missing files, duplicate links,
or missing sections. It cannot prove that a command exists, a requirement is
correct, the application was driven, or an outcome was observed. Those require
the source review and live proof in Create or Maintain mode.
