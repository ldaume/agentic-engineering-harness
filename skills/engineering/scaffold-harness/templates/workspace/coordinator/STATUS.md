# Status

Volatile state shared by every session in the workspace. Write it here, not
only in chat: the next session cannot read chat. Clear an entry when it is
done, so nobody acts on stale state.

## Worktree leases

One row per checkout a session is working in. A lease is coordination, not a
lock: it works because every session reads it before touching a checkout.

| Path | Branch | Repository | Session | State | Heartbeat |
|---|---|---|---|---|---|
| `../.worktrees/service-a-fix-login/` | `fix-login` | `service-a` | `<session id or short label>` | active | `<YYYY-MM-DD HH:MM>` |

- Add the row before the first edit; set `done` or `abandoned` before removing
  the checkout; delete the row after removal.
- Edit lease rows, and only those, in the primary coordinator checkout on its
  default branch and push at once, so every session sees them; on a push
  conflict, rebase and retry. Everything else in this file changes through
  the coordinator's normal branch and review path.
- Never remove, reset, or reuse a checkout another session's `active` row
  names, however old its heartbeat. A quiet session may still be working.
  Report it and leave it.

## Open work

| Item | Repositories | State | Next |
|---|---|---|---|
| `<cross-repository work item>` | `service-a, web-app` | `<state>` | `<next action>` |

Only work that spans members goes here. A member's own work stays in that
member's tracker.

## Stop conditions

- `<condition that blocks progress, for example a red contract check between two members>`

## Last updated

`<YYYY-MM-DD>` - `<one-line reason>`
