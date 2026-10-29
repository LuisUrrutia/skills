# Agentic Workflows

Apply this reference when a repository uses GitHub Agentic Workflows, recognizable as a Markdown file under `.github/workflows/` with a generated `.lock.yml` companion, or when a request asks for agent-driven automation such as issue triage or CI-failure analysis.

An agentic workflow is a Markdown file: its frontmatter configures triggers, permissions, tools, network, engine, and safe outputs, and its body holds natural-language instructions. `gh aw compile` generates the `.lock.yml` Actions workflow that runs.

- Edit the Markdown source; the generated `.lock.yml` carries a do-not-edit notice. After a frontmatter change, run `gh aw compile .github/workflows/<name>.md` and commit the source and `.lock.yml` together. The body loads at run time, so a body-only edit needs no compilation unless repository policy requires current generated files.
- Audit the generated `.lock.yml` as an ordinary workflow, and trace each finding back to the frontmatter that produces it. Supported agent jobs run without write access in a sandbox behind the Agent Workflow Firewall, and writes pass through separate safe-output jobs after threat detection. Custom jobs and relaxed permission, network, or safe-output settings form separate trust boundaries; map them like any other job.
- Keep builds, tests, and deployments that must be reproducible in ordinary workflows. Use an agentic workflow for reasoning work whose writes a safe-output job or human review gates.
- Each engine needs its own credential, such as a Copilot license or an `ANTHROPIC_API_KEY` secret; apply the [secrets rules](security.md#secrets-oidc-and-environments). Estimate AI credit spend with `gh aw forecast`, separately from Actions minutes.

Sources: [how agentic workflows work](https://github.github.com/gh-aw/introduction/how-they-work/), [editing workflows](https://github.github.com/gh-aw/setup/working-with-workflows/#editing-workflows), the [compilation process](https://github.github.com/gh-aw/reference/compilation-process/), and the [general availability release note](https://github.blog/changelog/2026-10-28-github-agentic-workflows-generally-available/).
