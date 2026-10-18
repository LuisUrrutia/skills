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
Setup changes only this run's isolated local data: never write to a shared or
remote environment, so no deploy, publish, migration, or other change to staging
or production, and report a step whose target is unclear as a prerequisite
instead of running it. Setup covers installing the locked dependencies without
changing the lockfile, creating the env file, and running migrations and seed
data. Adding dependencies, changing a lockfile, and global installs need the
active task's authority.

## Read remote environments without changing them

To make the local environment realistic, you may read a shared or remote
environment through the project's own cloud or platform CLI, such as `gcloud`:
its configuration, resource and service versions, schema, flags, and data,
which may be copied into the run's local data. Run read-only commands only, with
the CLI's existing authentication; never log in. First confirm that the active
project or account belongs to this repository's environments, and report it as
a prerequisite when it is missing or unclear. Never copy a secret from a secret
manager into a file or the output; secrets follow the env-file rules below.
Report each remote query with its command and the environment it read.

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
