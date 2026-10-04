# Test design decisions

Read this when selecting the observable boundary, a trustworthy expectation, or
controlled collaborators for a TDD cycle.

## Observe the contract

A public boundary is an interface used by a caller. It can be a module function,
domain service, HTTP endpoint, command, or user interaction; it need not be an
external API. Choose the narrowest layer that includes the interaction responsible
for the behavior. A test of a helper alone cannot prove its caller uses it correctly.

Prefer results, retrievable state, and externally visible effects over private
fields or incidental method calls. Persistence, call count, or ordering can be
valid assertions when they are part of the actual contract. Exercise that contract
at its boundary rather than imposing a universal ban on those observations.

Use literal examples worked from the requirement or an independent oracle.
Avoid deriving expected results from the function under test, copying its
algorithm, or accepting snapshots without checking their meaning. Confirm that
the chosen input distinguishes the required behavior from a plausible mistake.

## Control what the test cannot own

Prefer real in-process collaborators and lightweight fakes. Control external
services, time, randomness, or storage when needed for a reliable local check.
Use the project's existing boundary for that control; introduce an interface
only when it protects a real boundary, not just to satisfy a mocking library.

A fake should implement the relevant external contract and let the real code
make the decisions under test. Returning the desired answer from a mock of the
very behavior being tested proves nothing. Extensive mocking of internal pieces
is a reason to reconsider the test boundary or production design.

Keep each check repeatable: isolate state, control nondeterministic inputs, and
clean up resources. Do not contact live services or install testing infrastructure
merely because a donor example does so. Those actions follow the task's authority
and the project's established setup.
