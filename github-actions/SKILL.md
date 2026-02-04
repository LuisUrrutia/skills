---
name: github-actions
description: Guidelines for writing secure and maintainable GitHub Actions workflows. Use when user says "workflow", "github actions", "CI/CD", "actions yaml", or asks to create, review, or modify .github/workflows files.
---

## Context

- Workflow files: !`ls -la .github/workflows/ 2>/dev/null || echo "No workflows directory"`
- Current workflow (truncated): !`cat .github/workflows/*.yml 2>/dev/null | head -100 || echo "No workflow files"`

Note: If workflows are truncated, read specific files as needed.

## Key Principles

- **Fail Fast**: Run quickest checks first (linting before tests)
- **Parallel Execution**: Run independent jobs concurrently
- **Caching**: Reuse dependencies and build artifacts
- **Incremental**: Only test/build what changed
- **Idempotent**: Same input produces same output

## Quick Reference

- Pin actions to full-length commit SHAs for immutable releases
- Use `./` prefix for glob patterns (e.g., `./*.tar.gz`)
- Always use `set -euo pipefail` in shell scripts
- Declare permissions explicitly at job level (least privilege)
- Use `actionlint` to validate workflows locally: `actionlint .github/workflows/`

## References

Load these based on what you're working on:

| File | When to load |
|------|--------------|
| `references/security.md` | Permissions, secrets, handling untrusted input, pull_request_target |
| `references/shell.md` | Writing bash scripts, error handling, heredocs, temp files |
| `references/api.md` | GitHub API calls, gh CLI, github-script, retries, workflow commands |
| `references/patterns.md` | Caching, matrix builds, concurrency, reusable workflows |

## Workflow Validation

Before committing, validate with actionlint:

```bash
# Validate all workflows
actionlint

# Validate specific file
actionlint .github/workflows/ci.yml
```

## Action Version Check

When writing new workflows or reviewing existing ones:

```bash
# Check latest version of an action
gh api repos/{owner}/{repo}/releases/latest --jq '.tag_name'

# Get commit SHA for pinning
gh api repos/{owner}/{repo}/git/ref/tags/{tag} --jq '.object.sha'
```
