# Agent Skills

[![skills.sh](https://skills.sh/b/LuisUrrutia/skills)](https://skills.sh/LuisUrrutia/skills)

A collection of reusable skills for AI agents, including Claude Code, OpenCode,
and other tools that support the Agent Skills format. The repository covers
development workflows, writing, meeting updates, and Obsidian knowledge
management.

## Skills

| Skill | Use it for |
| --- | --- |
| [`article-processing`](article-processing/) | Turn article URLs into bilingual English/Spanish Obsidian notes with canonical URL deduplication, local attachments, and Medium/Freedium fallback. |
| [`commit`](commit/) | Create one safe Conventional Commit from a coherent change boundary, validate it, and optionally push only when explicitly requested. |
| [`daily-meeting-update`](daily-meeting-update/) | Build a meeting-ready development update from recent Git, GitHub, Jira/Atlassian, and OpenCode activity. |
| [`github-actions`](github-actions/) | Create, modify, or audit GitHub Actions workflows for security, correctness, reliability, cost, and performance. |
| [`humanize`](humanize/) | Rewrite, review, or edit prose so it sounds natural while preserving meaning, facts, citations, and the author's voice. |
| [`people-memory`](people-memory/) | Maintain persistent Obsidian People profiles from names, aliases, and contextual references in conversation. |
| [`pr`](pr/) | Create or update GitHub pull requests with safe Git and `gh` handling; every new PR is created and verified as a draft. |
| [`walkthrough`](walkthrough/) | Explain the current branch's changes from a user perspective, organized around flows, behavior, risks, and validation. |
| [`youtube-processing`](youtube-processing/) | Turn YouTube URLs into bilingual Obsidian study notes with reusable transcripts, local thumbnails, and compatible frontmatter. |

## Usage

Ask your agent for the outcome in natural language. For example:

```text
Create a safe commit for these changes.
Open a draft PR for the current branch.
Audit this GitHub Actions workflow for security and performance issues.
Turn this YouTube video into bilingual Obsidian study notes.
Summarize my recent development activity for today's standup.
```

The agent selects the matching skill from its description and follows that
skill's safety checks and workflow.

## Installation

### Using the Skills CLI

Install the repository with the recommended `skills` CLI:

```bash
npx skills add LuisUrrutia/skills
```

### Manual Installation

Clone the repository, then symlink its skill directories into your agent's
personal skills directory:

```bash
git clone https://github.com/LuisUrrutia/skills.git
cd skills

# Claude Code
mkdir -p "$HOME/.claude/skills"
for skill_file in "$PWD"/*/SKILL.md; do
  skill_dir=${skill_file%/SKILL.md}
  skill_name=${skill_dir##*/}
  ln -s "$skill_dir" "$HOME/.claude/skills/$skill_name"
done

# OpenCode
mkdir -p "$HOME/.config/opencode/skills"
for skill_file in "$PWD"/*/SKILL.md; do
  skill_dir=${skill_file%/SKILL.md}
  skill_name=${skill_dir##*/}
  ln -s "$skill_dir" "$HOME/.config/opencode/skills/$skill_name"
done
```

To install only selected skills, symlink those directories instead of running
the loops above.

## License

[MIT](LICENSE)
