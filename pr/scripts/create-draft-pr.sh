#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE' >&2
Usage: create-draft-pr.sh --base <base> --head <branch> --title <title> (--body <body> | --body-file <file>) [extra gh pr create flags]

Creates a GitHub pull request as a draft, verifies isDraft=true, attempts one
conversion back to draft with `gh pr ready --undo` if needed, then fails closed.
USAGE
}

if [[ $# -eq 0 ]]; then
	usage
	exit 2
fi

create_args=(--draft)
for forbidden in --web -w --editor -e --recover --ready; do
	for arg in "$@"; do
		if [[ "$arg" == "$forbidden" ]]; then
			echo "Blocked: $forbidden is not allowed for deterministic draft PR creation." >&2
			exit 2
		fi
	done
done

for arg in "$@"; do
	[[ "$arg" == "--draft" ]] && continue
	if [[ "$arg" == "--draft=false" || "$arg" == "-d=false" ]]; then
		echo "Blocked: draft=false is not allowed for deterministic draft PR creation." >&2
		exit 2
	fi
	create_args+=("$arg")
done

pr_url="$(gh pr create "${create_args[@]}")"
if [[ -z "$pr_url" ]]; then
	echo "Blocked: gh pr create did not return a PR URL." >&2
	exit 1
fi

is_draft="$(gh pr view "$pr_url" --json isDraft --jq '.isDraft')"
if [[ "$is_draft" != "true" ]]; then
	gh pr ready --undo "$pr_url" >/dev/null
	is_draft="$(gh pr view "$pr_url" --json isDraft --jq '.isDraft')"
fi

if [[ "$is_draft" != "true" ]]; then
	echo "Policy violation: PR was not left in draft mode: $pr_url" >&2
	exit 1
fi

printf '%s\n' "$pr_url"
