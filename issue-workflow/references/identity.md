# Tracker write identity

Read before a provider write in Publish or Synchronize mode. Establish the intended
actor from explicit user direction or project policy; otherwise use the selected
authenticated connection's known identity. Verify that identity and the intended
workspace, site or repository through account metadata or an identity read.
Resolve an ambiguous account or mismatch before the affected write.

Active provider-specific actor rules still apply, including the GitHub rule that
Git author/SSH identity alone does not establish the actor for an authenticated
API or CLI write. Follow the active account-switch policy when a switch is needed;
do not expand credential or integration scope. Keep secrets out of output.

Identity verification does not add permission for other fields, tickets or
operations. Preserve the caller's established authorization and verified scope.
