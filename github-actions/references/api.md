# GitHub API Usage in Actions

## Prefer actions/github-script

Has built-in retries with exponential backoff:

```yaml
- uses: actions/github-script@v7
  with:
    retries: 3
    retry-exempt-status-codes: 400 401 403 404 422
    script: |
      await github.rest.issues.createComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: context.issue.number,
        body: 'Automated comment'
      });
```

- `retries`: Number of retry attempts (uses exponential backoff)
- `retry-exempt-status-codes`: Client errors that should fail immediately

## gh CLI with Error Handling

When using `gh` CLI, handle errors and rate limits:

```yaml
- run: |
    set -euo pipefail
    API_STDERR="$RUNNER_TEMP/api_stderr.log"

    if ! RESULT=$(gh api repos/${{ github.repository }}/pulls \
      --header "Accept: application/vnd.github+json" \
      --jq '.[0].number' 2>"$API_STDERR"); then

      if grep -q "rate limit" "$API_STDERR" 2>/dev/null; then
        echo "::warning::Rate limited, waiting 60s..."
        sleep 60
        RESULT=$(gh api repos/${{ github.repository }}/pulls --jq '.[0].number')
      else
        echo "::error::API call failed"
        exit 1
      fi
    fi
```

## Retry with Exponential Backoff

For any command that may fail transiently (network calls, external services):

```yaml
- run: |
    set -euo pipefail
    MAX_ATTEMPTS=3
    DELAY=2

    for attempt in $(seq 1 $MAX_ATTEMPTS); do
      if curl -sSf https://example.com/api/deploy; then
        echo "Succeeded on attempt $attempt"
        break
      fi

      if [[ "$attempt" -eq "$MAX_ATTEMPTS" ]]; then
        echo "::error::Failed after $MAX_ATTEMPTS attempts"
        exit 1
      fi

      echo "::warning::Attempt $attempt failed, retrying in ${DELAY}s..."
      sleep "$DELAY"
      DELAY=$((DELAY * 2))
    done
```

## Workflow Commands

### Outputs and Environment Variables

```yaml
- name: Set output
  id: version
  run: echo "version=1.2.3" >> "$GITHUB_OUTPUT"

- name: Set env var
  run: echo "BUILD_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$GITHUB_ENV"

- name: Multiline output
  run: |
    {
      echo 'content<<EOF'
      cat report.txt
      echo 'EOF'
    } >> "$GITHUB_OUTPUT"
```

### Log Annotations

```yaml
- run: |
    echo "::notice file=app.js,line=1::Consider refactoring"
    echo "::warning file=config.yaml,line=10::Deprecated setting"
    echo "::error file=main.py,line=42::Missing bracket"
```

### Log Groups and Masking

```yaml
- run: |
    echo "::group::Installing dependencies"
    npm install
    echo "::endgroup::"

- run: |
    token=$(generate-temp-token)
    echo "::add-mask::$token"
    echo "TOKEN=$token" >> "$GITHUB_ENV"
```

### Job Outputs and Summaries

```yaml
jobs:
  build:
    outputs:
      version: ${{ steps.extract.outputs.version }}
    steps:
      - id: extract
        run: echo "version=1.2.3" >> "$GITHUB_OUTPUT"

      - name: Write summary
        run: |
          {
            echo "## Build Results"
            echo "| Test | Status |"
            echo "|------|--------|"
            echo "| Unit | Passed |"
          } >> "$GITHUB_STEP_SUMMARY"

  deploy:
    needs: build
    steps:
      - run: echo "Deploying ${{ needs.build.outputs.version }}"
```

## Useful Commands

```bash
# Check latest action version
gh api repos/{owner}/{repo}/releases/latest --jq '.tag_name'

# Get commit SHA for a tag (for SHA pinning)
gh api repos/{owner}/{repo}/git/ref/tags/{tag} --jq '.object.sha'
```
