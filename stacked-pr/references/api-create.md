# Create or extend a native stack through REST

Use this branch only for the requested create, adopt, or extend operation. The API route's live
contract is a precondition.

## Design and publish the branch chain

Load [stack-design.md](stack-design.md). State the layers bottom-to-top, then build each branch from
the layer below using plain Git. Preserve source tips before splitting existing work. Push only after
every adjacent parent is an ancestor of its child and each layer's checks pass.

This step is complete when all planned branch tips are present on the intended remote and their
ancestry, ownership, and checks match the layer plan.

## Create or adopt PRs

For each planned head branch, query open PRs by exact repository and head before creating anything.
Reuse an existing matching PR; inspect and correct its base only when the requested chain requires
it. Create missing PRs bottom-to-top against their direct parent branches.

Load the `pr` skill for titles, bodies, templates, and the shared bottom-to-top map. New PRs use the
requested draft state; existing PRs retain theirs unless the request changes it.

This step is complete when each planned layer has exactly one recorded PR, every head/base pair
forms the intended chain, and titles, bodies, maps, and draft states are verified from fresh reads.

## Create the stack object

Query membership by a known PR before creating a stack. Reuse a matching stack. If none exists, use
the current documented create request with PR numbers ordered bottom-to-top. Treat a validation
response as a chain or payload defect to inspect; treat a conflict response as concurrent state to
refetch.

Creation is complete when a fresh stack read proves the intended trunk, order, PR bases, and stage,
and Git ancestry agrees. Stop here for a create or adopt request.

## Extend the top

For an extend request, start the new branch from the verified current top, create or reuse its PR
against that top branch, then call the current documented append operation with only the new PRs in
bottom-to-top order. Refetch on concurrent state before deciding whether a retry is still needed.

Extension is complete when a fresh read shows the previous order unchanged and every requested PR
appended exactly once with the expected base. Stop after reporting the resulting order.
