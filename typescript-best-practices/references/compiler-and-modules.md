# Compiler and module contracts

Read when changing compiler configuration, imports/exports, package boundaries,
or diagnosing a discrepancy between type checking and execution.

Use the repository's installed compiler, package scripts, and effective leaf
configuration, including inherited options and included files. A solution root
with `files: []` can pass without checking its referenced projects. Use the
project's build/reference orchestration or the owning package's check; include
required generated types and framework checkers. Confirm the changed file is
actually checked before interpreting a green result. Explicit file arguments can
bypass project configuration or be rejected, depending on compiler version.

Match module settings to the actual host and published contract. Do not switch
resolution modes, erase imports, or add ambient declarations merely to remove
an error. Type-only imports disappear at runtime: preserve imports required for
side effects or runtime values. TypeScript `paths` does not rewrite emitted
specifiers or configure the runtime/bundler. A new `lib` declaration does not
provide a runtime polyfill.

For package exports, test a consumer of the built or packed artifact through
its advertised entrypoints and supported module formats, including declaration
resolution. Source aliases and a passing producer build can conceal broken
consumer imports. Do not add support for another module format without a need.

Change strictness, dependency versions, or build architecture only within the
task's scope. Report which programs and execution paths were checked and any
unavailable checks; do not label transpile-only output as a clean type check.
