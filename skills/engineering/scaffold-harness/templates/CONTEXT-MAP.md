# Context Map

## Contexts

- [`CONTEXT.md`](CONTEXT.md) - confirmed shared domain language.
- `<path-or-repository>` - purpose, owning team or role, and authority boundary.

For every non-local repository, record a full canonical HTTPS discovery URL
including its host. It need not match a credentialed Git `origin`. Never use an
`owner/repository` shorthand or infer a host from local Git configuration. Use
`local / no origin` only when no remote exists, and make the coordinator Fast
Check reject ambiguous remote values.

## Relationships

- **Provider -> Consumer**: public contract, provider and consumer owners,
  compatibility check, and escalation path.

For cross-repository work, record the repository revision or compatibility
range, local Fast Check, contract check, and authority boundary. The
coordinating harness never overrides repository-local instructions.

## Source Routing

| Question | Canonical source | Owner |
|---|---|---|
| Repository instructions | `AGENTS.md` | `<owner>` |
| Harness evolution | `HARNESS.md` | `<owner>` |
| Domain language | `CONTEXT.md` | `<owner>` |
| Current state | `<status source>` | `<owner>` |
| Accepted decisions | `docs/adr/` | `<owner>` |
| Durable learnings | `LEARNINGS.md` | `<owner>` |

For multi-team systems, add the smallest fields needed to expose bounded
context ownership, risk/release decision rights, shared-policy version, and
cross-team integration evidence. Do not use the map as a central backlog.
