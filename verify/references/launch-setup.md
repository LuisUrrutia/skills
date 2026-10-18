# Launch setup

Read this before any setup or remote query, and before building or starting an
instance even when nothing needs setup: it covers installing dependencies,
creating an env file, running migrations or seed data, querying a remote
environment, and running commands through varlock. A read-only caller gets no
setup and runs no remote queries; each needed step or query is a reported
prerequisite.

## Run the project's own setup

Use the project's documented commands. When the documentation is missing a step,
use only the scripts and targets the project itself declares, such as manifest
scripts, Makefile or task-runner targets, compose files, and its migration and
seed tooling, and the environment variables its source reads; report each step
you had to discover. Never compose a setup command from the project's internals.
Read every step before running it, documented or discovered, including what it
calls: a step that reaches a shared or remote environment follows the next
section when it only reads, and never runs when it writes there, and an export
or dump that lands in a remote bucket is a write, whatever the step's name says.
Setup changes only this run's isolated local data: never write to a shared or
remote environment, so no deploy, publish, migration, or other change to staging
or production, and report a step whose target is unclear as a prerequisite
instead of running it. Setup covers installing the locked dependencies without
changing the lockfile, creating the env file, and running migrations and seed
data. Adding dependencies, changing a lockfile, and global installs need the
active task's authority.

## Read remote environments without changing them

To make the local environment realistic, you may read a shared or remote
environment: through the project's own cloud or platform CLI, such as `gcloud`,
or through a step the project declares, such as a script, when reading that step
and everything it calls shows that it only reads remote state; otherwise the
step is a reported prerequisite. You may read its configuration, resource and
service versions, schema, flags, and data, and copy that data into the run's
local data. Run read-only commands only, with existing authentication; never log
in. First confirm that the active project or account belongs to this
repository's environments, and report it as a prerequisite when it is missing or
unclear. Report each remote query with its command and the environment it read.

## Keep remote secrets out of the run

No command of this run brings a secret value from a remote environment into a
file, the output, the evidence, or the process environment. When a configuration
read can include secret values, such as a service's environment, select only the
fields the launch needs with the CLI's format or filter flags. The project's
documented launch may still resolve its own secrets the way it does for its
developers, such as varlock resolvers or `op run`, with existing authentication
only: a locked vault, a biometric prompt, or a sign-in prompt is a reported
prerequisite, never a login by this run. No secret value is printed, written to
a file, or put in the evidence or the output. A secret the launch still lacks
follows the env-file rules below and goes to the user.

## Prepare the env file

Use the project's mechanism:

- **`.env.schema` exists:** the project uses varlock. Validate with
  `varlock load --agent`, which redacts sensitive values, and run the project's
  commands through varlock unless its own scripts already load it. Invoke
  varlock through the project's package manager when it is a local dependency;
  the process environment overrides every env file, so this run's own ports and
  data paths go there. The `varlock` skill, when installed, covers the details.
  Never read `.env` or `.env.local`, and never invent or fill a secret value. A
  missing required secret stops that step: ask the user to set it. When varlock
  is in neither the project nor the machine, report a blocker; do not install
  it.
- **Otherwise:** create a missing `.env` from `.env.example`, with this run's
  isolated ports and data paths, and never overwrite an existing env file. A
  missing secret: ask the user. Never print secret values.
