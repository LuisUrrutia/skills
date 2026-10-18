# Create a project verification skill

## Interview the repository

Read the code and existing runbooks before asking about discoverable setup.
Establish these facts from actual project files and execution:

- **Surface:** the UI, CLI/TUI, desktop or mobile app, API, or public library API
  a user actually exercises. Identify the primary surface and other entry points.
- **Run:** exact build and launch commands, working directory, runtime, readiness
  signal, ports, environment variable names, authentication, and seed data.
- **Drive:** existing tests or harnesses first, then host-supported browser,
  device, PTY, or HTTP tools. Inspect real commands and stable handles.
- **Observe:** action traces and resulting state, screenshots, terminal output,
  responses, logs, files, or persisted records that can support a precise claim.
- **Isolate:** independent ports, profiles, data directories, test accounts, and
  processes. Separate output paths do not isolate shared application state.

Build and start the real application with its established tooling. A broken base
needs an in-scope correction or a precise blocker; do not invent launch steps for
an application you could not run. An irrelevant missing directory or sample
configuration may be explicit verification scaffolding when safe and authorized;
record why it is irrelevant to the behavior, create it only for the run, and
remove it afterward. Never use scaffolding to conceal a missing product boundary.

### Launch setup

Unless the caller is read-only, a launch may use the project's documented
commands. When the documentation is missing a step, use only the scripts and
targets the project itself declares, such as manifest scripts, Makefile or task-
runner targets, compose files, its migration and seed tooling, and the
environment variables its source reads, and record each discovered step in the
generated Launch section. Never compose a setup command from the project's
internals. Setup changes only the run's isolated local data: never write to a
shared or remote environment, so no deploy, publish, migration, or other change
to staging or production, and report a step whose target is unclear as a
prerequisite instead of running it. Setup covers installing the locked
dependencies without changing the lockfile, creating the env file, and running
migrations and seed data. Adding dependencies, changing a lockfile, and global
installs need the active task's authority. A read-only caller gets none of this
setup; each step becomes a reported prerequisite.

To make the local environment realistic, a launch may read a shared or remote
environment through the project's own cloud or platform CLI, such as `gcloud`:
its configuration, resource and service versions, schema, flags, and data, which
may be copied into the run's local data. Run read-only commands only, with the
CLI's existing authentication; never log in. First confirm that the active
project or account belongs to this repository's environments, and report it as a
prerequisite when it is missing or unclear. Never copy a secret from a secret
manager into a file or the output; secrets follow the env-file rules below.
Report each remote query with its command and the environment it read, and
record the ones a later run needs in the generated Launch section. These queries
belong to launch setup, so a read-only caller gets none of them.

Prepare the env file by the project's mechanism:

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
- **Otherwise:** create a missing `.env` from `.env.example`, with the run's
  isolated ports and data paths, and never overwrite an existing env file. A
  missing secret: ask the user. Never print secret values.

When the run's ports and data paths cannot go into an env file it created, pass
them through the process environment; never write them into an env file the run
did not create. Remove an env file the run created during cleanup.

This rule governs your own builds and starts during the interview and the proof,
and the generated Launch section states it with the project's actual commands.

## Write instructions for the next agent

Use `agent-instructions` with the discovered facts, intended verification scope,
and target location. The generated `SKILL.md` needs valid host metadata and the
following operating contract, filled with real project commands and paths:

| Section | Required content |
| --- | --- |
| Launch | Exact build/start command and working directory; prerequisites; the [launch setup](#launch-setup) with this project's install, env-file, migration and seed commands; for a run-owned instance, startup from empty data through any migrations and seed data; a bounded readiness check that proves a usable state, not only an answering process or port; how the run identifies its build, instance, and owned resources. |
| Doctor | A read-only check of whether this specific instance is worth driving: identity/version, readiness, expected data/profile/port, and relevant auth state. Explain failures without exposing credentials. |
| Drive | The actual harness and selectors, routes, commands, public API calls, or device actions. Explain reset to a known state and reference the feature index. |
| Evidence | Required action and result artifacts, independent side-effect checks, build/input identity, and the exact output location outside disposable state. |
| Cleanup | Bounded teardown of owned processes, sessions, and fixtures on success and failure; preserve user-owned instances and prove retained evidence still exists. |
| Helpers | Each bundled executable's invocation, working directory, inputs, outputs, exit states, and effects, or the existing commands that make helpers unnecessary. |

For servers and long-lived UIs, use an isolated instance driven by one owner.
For short-lived CLIs/TUIs, build once and use a fresh isolated session per drive
when that is the launch model. Never kill by process name or claim ownership
because something answers on the expected port. Shared instances need explicit
ownership boundaries and serial driving; clean only the residue the run created.

Use code for stable repeated mechanics such as startup, identity/health checks,
or capture when existing commands do not suffice. Keep platform and application
specific helpers in the generated skill, not in this generic authoring skill.
Keep diagnostics read-only and distinguish an unavailable check from a pass.
Test added helpers, including failure and cleanup behavior, and make their
execution permissions and invocations usable by the next agent.

## Seed the feature map

Create `features/README.md` and one file per initially selected user-facing
feature. Start with the top three to five identifiable features, or all when the
application has fewer; use actual routes, commands, menus, and documented behavior.
List the remaining known surfaces as coverage not yet mapped rather than implying
completeness. Follow this skill's
[feature-map contract](feature-map.md).

Derive expected behavior from requirements, public contracts, or documented
decisions, checking them against implementation. When sources disagree about
intent, ask rather than silently making the current output the expectation.
Map each user entry point and observable end state. A UI path, keyboard shortcut,
CLI command, and API call are not interchangeable evidence for one another.

Proof exercises the real public path, captures the action and resulting state,
and checks side effects independently: reopen saved data, read the resulting
file, or observe the persisted value through an appropriate second view. Internal
setters and test-only endpoints do not establish that a real user path works.
Mocks belong only at an existing boundary outside the behavior being claimed.
For a dry-run or test mode, observe what it actually changes, including files,
network activity, and Git refs where relevant; its name is not an isolation guarantee.

## Prove the generated instructions

Follow them as written: launch, doctor, drive one mapped feature through its
declared proof, capture evidence, and clean up. Name the feature and entry points
actually exercised. This demonstrates the recipe, not that every mapped feature
has passed. Check that the evidence is still readable at its named location.

After a failure, clean owned residue before retrying. Fix instruction or harness
defects under authoring scope, rerun the affected path, and finish with final
teardown after the last proof. A healthy process can still contain a wedged UI;
reset or relaunch when doctor cannot establish a usable state. Report a product
failure or inaccessible prerequisite without rewriting the intended result.

Deliver the tested skill, its map and helpers, evidence, and coverage limits.
Point to `verification-authoring` in Maintain mode for later upkeep. Scheduling
requires a separate requested cadence.
