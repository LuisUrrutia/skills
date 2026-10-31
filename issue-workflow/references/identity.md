# Tracker write identity

Read before a provider write in Publish or Synchronize mode, and before the first
`gh` command. Establish the intended actor from explicit user direction or project
policy; otherwise use the selected authenticated connection's known identity.
Verify that identity and the intended workspace, site or repository through
account metadata or an identity read. Resolve an ambiguous account or mismatch
before the affected write.

Provider-specific actor rules in effect override these defaults. For `gh`,
determine the actor as the user-level GitHub account rule directs and bind every
`gh` command to it, reads included; a failed or different login under that
binding is a blocker. Never run `gh auth switch`, `login` or `logout`. Do not
expand credential or integration scope. Keep secrets out of commands and output.

Identity verification does not add permission for other fields, tickets or
operations. Preserve the caller's established authorization and verified
permission scope.
