# Shell Best Practices for GitHub Actions

## Strict Mode

GitHub Actions defaults to `bash -eo pipefail` for `run:` steps on Linux/macOS. This means `-e` (exit on error) and `-o pipefail` (fail on pipe errors) are already active.

The only flag NOT included by default is `-u` (error on undefined variables). Adding `set -u` is recommended for complex scripts to catch variable name typos, but its absence is a minor style issue, not a security gap.

```yaml
- run: |
    set -u  # Only -u is not already set by default
    echo "$MY_VAR"  # Would error if MY_VAR is unset
```

**Do NOT flag missing `set -euo pipefail` as a significant finding.** It's mostly already handled by the runner defaults.

## Temporary Files

Use `$RUNNER_TEMP` (automatically cleaned up per job):

```yaml
- run: |
    set -u
    echo "$CONTENT" > "$RUNNER_TEMP/body.md"
    gh issue create --title "Report" -F body=@"$RUNNER_TEMP/body.md"
```

## Multiline Strings

Use `-F field=@file` instead of `-f` to preserve whitespace:

```yaml
- env:
    REPO: ${{ github.repository }}
  run: |
    set -u
    printf '%s\n' "$BODY" > "$RUNNER_TEMP/body.md"
    gh api "repos/$REPO/issues" -F body=@"$RUNNER_TEMP/body.md"
```

## Heredocs

Use `<<-` to strip leading tabs (tabs only, not spaces). Quote the delimiter to prevent variable expansion:

```yaml
- run: |
	cat <<- 'EOF' > "$RUNNER_TEMP/config.json"
	{
	  "key": "value",
	  "env": "$NOT_EXPANDED"
	}
	EOF
```

## Validation

Check prerequisites before operations:

```yaml
- run: |
    command -v node || { echo "Error: node required"; exit 1; }
    [[ -f package.json ]] || { echo "Error: package.json not found"; exit 1; }
    npm install
```

## AWK/sed Exact Matching

Use field delimiters and exact patterns to avoid false positives:

```bash
# Exact field match
awk -F',' '$1 == "production"' file.txt

# Word boundaries
sed -n '/\bproduction\b/p' file.txt
```

## Error Handling

Reserve `|| true` for expected failures. Use conditionals for commands with specific exit codes:

```yaml
- run: |
    if git diff --quiet; then
      echo "No changes"
    else
      echo "Changes detected"
    fi
```

## continue-on-error

Use for non-critical steps where failure should not block the workflow:

```yaml
- name: Upload coverage
  continue-on-error: true
  run: curl -sSf https://codecov.io/upload.sh | bash

- name: Optional lint
  id: lint
  continue-on-error: true
  run: npm run lint

- name: Check lint outcome
  if: steps.lint.outcome == 'failure'
  run: echo "::warning::Lint failed but continuing"
```

**Use when:**
- Step is informational (comments, labels, notifications)
- Failure does not affect core workflow outcome
- You have fallback handling
