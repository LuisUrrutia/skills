# Shell Best Practices for GitHub Actions

## Strict Mode

Always start shell scripts with strict mode:

```yaml
- run: |
    set -euo pipefail
    npm install
    npm run build
```

- `set -e`: Exit on command failure
- `set -u`: Error on unset variables
- `set -o pipefail`: Fail if any command in a pipeline fails (critical for `cmd | grep` patterns)

## Temporary Files

Use `$RUNNER_TEMP` (automatically cleaned up per job):

```yaml
- run: |
    set -euo pipefail
    echo "$CONTENT" > "$RUNNER_TEMP/body.md"
    gh issue create --title "Report" -F body=@"$RUNNER_TEMP/body.md"
```

## Multiline Strings

Use `-F field=@file` instead of `-f` to preserve whitespace:

```yaml
- run: |
    set -euo pipefail
    printf '%s\n' "$BODY" > "$RUNNER_TEMP/body.md"
    gh api repos/${{ github.repository }}/issues -F body=@"$RUNNER_TEMP/body.md"
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
    set -euo pipefail
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
    set -euo pipefail
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
