# Launch setup

Read this before installing dependencies, creating an env file, running
migrations or seed data, or querying a remote environment for a launch. A
read-only caller gets none of this setup; the skill's launch step reports each
step as a missing prerequisite instead.

## Run the project's own setup

Use the project's documented commands. When the documentation is missing a step,
use only the scripts and targets the project itself declares, such as manifest
scripts, Makefile or task-runner targets, compose files, and its migration and
seed tooling, and report each step you had to discover. Setup changes only this
run's isolated local data: never write to a shared or remote environment, so no
deploy, publish, migration, or other change to staging or production, and report
a step whose target is unclear as a prerequisite instead of running it. Setup
covers installing the locked dependencies without changing the lockfile,
creating the env file, and running migrations and seed data. Adding
dependencies, changing a lockfile, and global installs need the active task's
authority.

## Read remote environments without changing them

To make the local environment realistic, you may read a shared or remote
environment through the project's own cloud or platform CLI, such as `gcloud`:
its configuration, resource and service versions, schema, flags, and data
shape. Run read-only commands only, with the CLI's existing authentication;
never log in. First confirm that the active project or account belongs to this
repository's environments, and report it as a prerequisite when it is missing
or unclear. Prefer queries that cannot print rows, such as counts and schema
introspection. Ask the user before copying data that may hold personal or
customer information into the local environment, the evidence, or the output,
and never copy a secret from a secret manager into a file or the output. Report
each remote query with its command and the environment it read.

## Prepare the env file

Use the project's mechanism:

- **`.env.schema` exists:** the project uses varlock. Validate with
  `varlock load --agent`, which redacts sensitive values, and run the project's
  commands through varlock unless its own scripts already load it. Invoke
  varlock through the project's package manager when it is a local dependency.
  Give this run its own ports and data paths through the process environment,
  which overrides every env file; never write them into `.env` or `.env.local`.
  The `varlock` skill, when installed, covers the details. Never read `.env` or
  `.env.local`, and never invent or fill a secret value. A missing required
  secret stops that step: ask the user to set it. When varlock is in neither the
  project nor the machine, report a blocker; do not install it.
- **Otherwise:** create a missing `.env` from `.env.example`, with this run's
  isolated ports and data paths, and never overwrite an existing env file. A
  missing secret: ask the user. Never print secret values.
