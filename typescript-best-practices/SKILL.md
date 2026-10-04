---
name: typescript-best-practices
description: Use when implementing or reviewing TypeScript code, including type contracts and compiler or module configuration.
---

# TypeScript best practices

Use the simplest types that make the required operations safe. Preserve the
task's implementation or inspection scope and the repository's public contracts.

## Keep types honest

- **Strengthen types where an operation needs it.** An empty collection can have
  a valid result or explicit absence; introduce a non-empty representation only
  when the contract requires one. Use discriminated unions for dependent fields
  and compiler-checked exhaustiveness for closed variants. Keep independently
  optional fields optional. Brand primitives where mixing identities or units
  causes a concrete error; a brand alone proves no runtime constraint.
- **Use the authoritative contract.** Infer from the existing schema or generated
  source when it owns the same contract. Keep stable public interfaces independent
  of private implementation details. Preserve legitimate callers and documented
  states, including ones absent from today's call sites. A generic must express a
  real relationship; letting a caller choose an unchecked return type proves
  nothing. Prefer inference over redundant annotations or elaborate type machinery.
- **Parse untrusted values.** Treat incoming untyped data as `unknown`; reuse the
  project's validator and validate at the boundary that owns the contract.
  An annotation, generated client type, `as`, `satisfies`, or generic argument does
  not validate runtime data. Use `satisfies` to check static compatibility, not to
  repair a mismatch. Do not silence a real mismatch with `any`, `!`, double casts,
  suppression, or weaker compiler settings. Isolate a necessary assertion at a
  justified boundary and test the invariant it relies on; `as const` is not a
  claim that arbitrary input has been validated.
- **Check a predicate's whole promise.** A declared `value is T` must justify
  both branches: true means `T`, false excludes `T`. Property presence or one
  checked field rarely proves a whole object. Assertion functions need the same
  scrutiny for the guarantee they claim after returning.
- **Keep guarantees valid until use.** `readonly` and `as const` do not freeze
  runtime objects. Mutation through aliases, callbacks, or across an `await` can
  invalidate narrowing or a non-empty collection. Preserve ownership, capture a
  stable value, or recheck at the relevant transition.
- **Represent absence accurately.** Arbitrary dictionary keys and array indices
  can be missing, even with `Record<string, T>` or a non-empty array. Distinguish
  omission, explicit `undefined`, and `null` when the contract does. `strict`
  alone does not enable `noUncheckedIndexedAccess` or
  `exactOptionalPropertyTypes`; do not assume either guarantee or turn a small
  change into an unrelated configuration migration.
- **Own asynchronous completion.** An `async` function can fit a `void` callback
  whose caller ignores its promise. Check whether completion and rejection reach
  the intended owner. `void promise` only discards the value. Use `error-handling`
  when recovery policy needs design; do not invent a catch-and-log policy here.

## Verify the contract

Run the repository's checker against the changed files and affected consumers;
transpilation is not type checking. For changed type contracts, check valid and
invalid uses with assertions that actually fail on regression. A type alias
evaluating to `false` is not a failing test. Exercise runtime boundary behavior
separately. Keep formatting and enforceable style in existing tooling.

For compiler, import/export, or package changes, read
[compiler-and-modules.md](references/compiler-and-modules.md).
For requested upstream maintenance, read
[upstream-updates.md](references/upstream-updates.md).
