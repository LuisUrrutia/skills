# Thread settlement

Read before acting on any thread in a tick. A reply or a resolution by someone
else is a claim to check on the current head, not proof. Act only on threads the
reviewer started.

| What happened | Verified on the current head | Action |
| --- | --- | --- |
| The author fixed it, or removed the code it was about | The issue no longer exists | Resolve. Reply only when it adds something. |
| The author fixed part of it | The rest still stands | Reply with what is done and what remains; keep it open. |
| A new head fixed it without a reply | The issue no longer exists | Resolve. |
| The author answered a question | The answer settles it, with evidence | Resolve. |
| The author answered, but the point still stands | Evidence still supports the finding | Reply once with the deciding fact. If the author disagrees again, report the thread to the user and stop replying there. |
| The author disagreed | The author is right | Resolve; a short acknowledgment is optional. |
| The author deferred it as out of scope | The issue still exists | Ask for a ticket to track it; keep it open. |
| The author gave a ticket key or link, or confirmed the ticket exists | — | Resolve. When the tracker is accessible, confirm the ticket exists first. |
| The author promised a ticket later, or refused one | — | Wait on a promise; report a refusal to the user. Keep it open. |
| A resolved thread awaits verification on this head, whoever resolved it | The issue no longer exists, or the thread was settled by a confirmed ticket | Mark it `verified`. |
| A resolved thread awaits verification on this head | The finding still stands | Reopen it with `unresolve` and reply with the deciding fact. |
| A resolved issue reappears in a new head | The issue is back | Reopen it and say what came back; `pr-review` raises the same point there. |
| Anything that needs the user's judgment | — | Report it; do not reply. |

Name the tracker the project uses when the repository instructions or the private
`pr-review` profile establish it, for example Jira; otherwise ask for "a ticket"
without naming a tool. An inaccessible tracker does not block resolving on the
author's ticket key or link. A resolved deferral stays an accepted deferral for
later reviews.

Keep every follow-up on a topic in its existing thread. A new thread is only for
a new finding, which `pr-review` publishes. Word every reply with `comment-style`
in the thread's language. Illustrative shapes, not templates:

- partial fix: "perfect, the guard is in now. the retry path still writes twice"
- deferral: "ok, could you open a Jira ticket so we can track it?"

When the reviewer cannot resolve or reopen a thread, report it instead of planning
the change. Never act on other reviewers' threads.
