# Context Map

The single map of the repositories in this workspace: where each lives, how to
reach it, who owns it, and how members relate. Do not keep a second map; two
maps drift and no session can tell which is current.

## Members

| Path | Remote | Role | Owner | State | Fast Check |
|---|---|---|---|---|---|
| `<coordinator>/` | `https://<host>/<owner>/<coordinator>` | Coordinator: relationships, shared rules, status | `<team or role>` | active | `<command>` |
| `service-a/` | `https://<host>/<owner>/service-a` | `<what it owns>` | `<team or role>` | active | `<command>` |
| `experiment-b/` | `local / no remote` | `<what it tries>` | `<team or role>` | experimental | `<command or none yet>` |

- Record a full HTTPS URL with its host, so a session on another machine finds
  the repository. An `owner/name` shorthand resolves to different hosts on
  different machines. Use `local / no remote` only when no remote exists.
- `State` is `active`, `experimental` (no checks or pointer yet), or
  `retired`. Keep retired rows until no session can still reach the path.
- Owners are teams or roles, not personal names, so the map survives a change
  of people.

## Relationships

| Provider -> Consumer | Contract | Compatibility check | Escalation |
|---|---|---|---|
| `service-a -> web-app` | `<API, schema, event, package>` | `<command or test>` | `<who decides on a break>` |

Record a relationship only when a change on one side can break the other.

## Source routing

| Question | Source |
|---|---|
| How agents work here | `<coordinator>/HARNESS.md` |
| Admission, fan-out, write-back | `<coordinator>/SYNC.md` |
| What is in flight, who holds which checkout | `<coordinator>/STATUS.md` |
| Shared domain terms | `<coordinator>/CONTEXT.md`, when confirmed terms exist |
| A member's product, code, and checks | that member's `AGENTS.md` |

The map is not a backlog. Work items belong to the repository that owns them.
