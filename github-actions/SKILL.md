---
name: github-actions
description: Guidelines for writing secure and maintainable GitHub Actions workflows. Use when user says "workflow", "github actions", "CI/CD", "actions yaml", or asks to create, review, or modify .github/workflows files.
---

## Context

- Workflow files: !`ls .github/workflows/ 2>/dev/null`

Note: Read specific workflow files as needed before making changes.

## Key Principles

- **Fail Fast**: Run quickest checks first (linting before tests)
- **Parallel Execution**: Run independent jobs concurrently
- **Caching**: Reuse dependencies and build artifacts
- **Incremental**: Only test/build what changed
- **Idempotent**: Same input produces same output

## Quick Reference

- Pin actions to full-length commit SHAs for immutable releases
- Use `./` prefix for glob patterns (e.g., `./*.tar.gz`)
- Add `set -u` in complex shell scripts (the runner already sets `-eo pipefail`)
- Prefer job-level permissions (least privilege); use workflow-level when calling reusable workflows with `secrets: inherit`
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

Run these commands when writing or reviewing workflows. Always pin to full-length commit SHAs and verify version comments are correct.

```bash
# Check latest release version
gh api repos/{owner}/{repo}/releases/latest --jq '.tag_name'

# List recent tags (to see what versions exist)
gh api repos/{owner}/{repo}/tags --jq '.[].name' | head -20

# Get commit SHA for a tag (for pinning)
gh api repos/{owner}/{repo}/git/ref/tags/{tag} --jq '.object.sha'

# Find which tag a SHA belongs to
gh api repos/{owner}/{repo}/tags --jq '.[] | "\(.name) \(.commit.sha)"' | grep {sha_prefix}
```

### Resolving Mismatched Version Comments

When a version comment doesn't match the pinned SHA, determine which one is correct:

1. **Look up what the SHA actually is:** find its tag using the commands above.
2. **Look up what the comment says:** get the SHA for the commented tag.
3. **Fix whichever is wrong:**
   - If the SHA is already the latest version, update the comment to match.
   - If the comment is the intended version, update the SHA to match.

### Updating Action Versions

**Never update action versions without user confirmation.** When outdated actions are found:

1. List each action with its current and latest available version.
2. Flag which updates are **major** (e.g., v3 -> v4), **minor**, or **patch**.
3. Ask the user which updates to apply -- they may want only patch/minor updates,
   or may want to skip specific major bumps.

Major version updates can have breaking changes. Present them clearly:

```
actions/checkout:         v3.5.3 -> v4.2.0 (MAJOR)
actions/setup-node:       v4.0.0 -> v4.1.0 (minor)
actions/upload-artifact:  v4.3.0 -> v4.3.1 (patch)
```

After confirmation, update both the SHA and the version comment together.
