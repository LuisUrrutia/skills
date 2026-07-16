# Shell in GitHub Actions

Apply every section that matches a changed or reviewed `run:` block.

## Select shell semantics explicitly

On Linux and macOS, an unspecified shell runs `bash -e {0}` and can fall back to `sh`. Explicit `shell: bash` runs `bash --noprofile --norc -eo pipefail {0}`. Use the explicit form when the script relies on Bash syntax or pipeline failure propagation:

```yaml
- name: Build
  shell: bash
  run: |
    set -u
    npm run build
```

Add `set -u` when unset variables are errors by contract. Initialize optional variables before enabling it. PowerShell and `cmd` have different failure rules; write and validate those scripts in their selected shell.

## Cross the expression boundary through `env`

Keep `${{ ... }}` out of generated shell syntax. Bind expressions to environment variables, then quote every expansion:

```yaml
- name: Print ref
  env:
    REF_NAME: ${{ github.ref_name }}
  shell: bash
  run: printf '%s\n' "$REF_NAME"
```

Use arrays for argument lists and `printf` for data. Quote file paths, URLs, and variables even when their current source appears constrained.

## Use runner-owned temporary storage

Write transient files under `$RUNNER_TEMP`, which is scoped and cleaned with the job:

```yaml
- name: Create request body
  env:
    BODY: ${{ github.event.issue.body }}
    GH_TOKEN: ${{ github.token }}
  shell: bash
  run: |
    body_file="$RUNNER_TEMP/issue-body.md"
    printf '%s' "$BODY" > "$body_file"
    gh issue create --title "Report" --body-file "$body_file"
```

Quote heredoc delimiters when literal content is intended. `<<-` strips tabs only; ordinary YAML indentation uses spaces, so use it only when the script actually contains tab-indented data.

## Handle failure as data only when expected

The runner's fail-fast shell should surface unexpected failures. Capture status explicitly when a command has an expected nonzero result:

```yaml
- name: Detect changes
  id: changes
  shell: bash
  run: |
    if git diff --quiet; then
      echo "changed=false" >> "$GITHUB_OUTPUT"
    else
      status=$?
      if [[ "$status" -eq 1 ]]; then
        echo "changed=true" >> "$GITHUB_OUTPUT"
      else
        exit "$status"
      fi
    fi
```

Apply the [`continue-on-error` contract](reliability.md#failure-cancellation-and-time-bounds) when a nonzero result becomes workflow data.

## Write workflow data safely

Use the [workflow channel](api.md#workflow-channels) whose scope matches the value. Within a shell step:

- append one logical record at a time with `printf`
- pass arbitrary multiline or attacker-controlled content through a file or artifact because a static delimiter can collide with the payload
- mask a generated sensitive value before another command can log it; keep sensitive data in its authoritative secret channel

## Review criterion

Every dynamic value crosses through `env`, every shell expansion is quoted, expected failures preserve unexpected exit codes, temporary data stays under `$RUNNER_TEMP`, and the selected shell matches the script syntax.

## Official source

https://docs.github.com/api/article/body?pathname=/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsshell
