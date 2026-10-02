# Logic and state models

Use this for questions about states, transitions, invariants, or data shapes that
benefit from being exercised. Prefer a small interactive demo when a domain expert
needs to try sequences; use a script when only the computed result matters.

Keep the model separate from its display. Use the form the question needs: pure
functions, a reducer, explicit transitions, or a small stateful module. This
separation makes behavior inspectable; it does not make the code production-ready.

Show the question and assumptions in domain language. Expose all state relevant
to the decision after each action, with readable labels. Provide free exploration
and a way to reset to a known state. For a guided walkthrough, reset its initial
conditions and execute real model actions rather than a separate scripted story.

Exercise a normal path, an awkward sequence, and an attempted invalid transition
when these exist in the model. Make rejection and unchanged state visible. A
disabled button alone cannot demonstrate how the model rejects an invalid action.
Keep hypothetical business rules labeled as assumptions; do not invent an
authoritative domain policy to make a scenario pass.

Drive the demo or script and compare the observed state with the question's
constraints. Include concrete action sequences and resulting states in the
evidence. Small assertions can protect a decisive invariant; a full test harness
is useful only if the experiment requires it or the project mandates it.
