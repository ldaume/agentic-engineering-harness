# Harness Operations

## Choose the Working Root

| Scope | Start the session in |
|---|---|
| Develop or maintain portable Skill **source** files | This repository |
| Build or evolve one repository harness | The target repository |
| Coordinate a system spanning repositories | A dedicated coordinating repository or workspace |
| Target is not known or cannot be opened yet | This repository for discovery only, then switch scope |

This repository supplies capabilities. It is not the normal control plane for
target work because that would weaken local instruction discovery and increase
context leakage and blast radius. Do not coordinate other members' product or
ops work from a skills session.

## One Target Repository

1. Open or activate the target as the working root.
2. Read its instruction hierarchy and discover existing sources, commands,
   boundaries, permissions, Fast Check, and Full Gates.
3. Invoke `scaffold-harness` to assess the current and justified target level.
4. Use `grill-harness-with-docs` only for decisions that evidence cannot
   resolve.
5. Apply the smallest upgrade in the target repository.
6. Use `agent-sync` during and at the end of work.
7. Verify target-local references and checks before handoff.

Example agent prompt:

```text
Use scaffold-harness to audit and evolve this repository to the lowest
delegation level that makes the current work reliable. Preserve local truth,
name the real Fast Check and Full Gates, use grill-harness-with-docs for
unresolved material decisions, and run agent-sync before completion.
```

## Multiple Repositories

Use a dedicated coordinating repository when the work has durable
cross-repository contracts, dependency order, shared workflow state, or
cross-cutting verification. Do not turn this Skills repository into that
coordinator.

The coordinator may own:

- repository and owner relationships
- public integration contracts and compatibility ranges
- cross-repository workflow state and stop conditions
- shared Skills or policies that genuinely apply to all targets
- integration checks, evals, recovery, and audit evidence

Each target still owns its architecture, commands, implementation state,
permissions, decisions, and local checks. Create only the coordinating
artifacts that observed work requires.

### Coordinating repository baseline

A dedicated coordinator (not this Skills catalog) should, at minimum, keep:

| Concern | Typical owner |
|---|---|
| Agent entry + boundaries | `AGENTS.md` |
| Oversight, autonomy, stewardship | `HARNESS.md` |
| Shared terms (only confirmed cross-repo language) | `CONTEXT.md` |
| Members, remotes, checks, relationships | `CONTEXT-MAP.md` |
| How members discover the coordinator and write back | sync protocol (e.g. `SYNC.md`) + thin member `AGENTS.md` pointers |
| Open cross-repo work / stop conditions | `STATUS.md` (volatile; clear when done) |
| Durable coordinator lessons | `LEARNINGS.md` |
| Human map of the system | `README.md` |
| Coordinator verify | smallest real Fast Check / Full Gates |

Cross-session survival means those files are git-tracked and updated via
`agent-sync`. Chat is not memory. Member product truth stays in members.

### Coordinator availability

Keep concise coordinator pointers in each member. Prefer a local sibling or
workspace checkout because it is fast, offline-capable, and can match the
working revision. Also include a stable remote repository or raw-file fallback
for sessions that open only one member.

If neither local nor remote coordinator sources are reachable, degrade safely:
follow the member's local instructions, continue only reversible member-local
work, and do not infer cross-repository authority, shared state, or a higher
autonomy level. Do not copy the full coordinator policy into every member.

Example agent prompt:

```text
Use scaffold-harness to establish or evolve a cross-repository harness for the
named repositories. Treat every repository as the authority for its local
truth. Keep only relationships, public contracts, workflow state, and
cross-cutting verification in the coordinating repository. Present options
with a recommendation before creating the coordinator or expanding autonomy
when ownership or authority is unresolved.
```

## Multiple Teams

Use a federated coordinating harness when repository coordination also crosses
team decision boundaries. Keep each team's local harness authoritative for its
domain model, implementation, commands, checks, permissions, and delivery
choices.

The federation adds only what no team can own alone:

- bounded-context, provider, consumer, and team/role relationships
- public contract ownership and compatibility policy
- shared Skill, rule, and control versions with adoption evidence
- cross-team integration evals, release evidence, and incident signals
- named semantic, security, risk, release, and autonomy decision rights
- escalation when contracts or priorities conflict

Do not centralize team backlogs, local implementation state, or inferred domain
semantics. Prefer Git-owned contracts and asynchronous checks over mandatory
coordination meetings. Add catalogs, graph indexes, or policy engines only for
an observed scale failure with a pilot and removal path.

Example agent prompt:

```text
Use scaffold-harness and scaffold-distributed-context to establish a federated
multi-team harness. Preserve each team's local authority, map bounded contexts
and public contracts to named owners, version shared policy and Skills, define
cross-team compatibility checks and escalation, and create no central product
or domain authority.
```

## Bootstrap from This Repository

A session may start here when no target root is available:

1. Resolve the intended target paths, repositories, and authority.
2. Decide whether the scope is one repository or a durable multi-repository
   system.
3. Open or activate the target or coordinator.
4. Re-read the applicable local instructions there.
5. Continue with the matching workflow above.

Do not edit target files while still treating this repository's instructions
as the only authority. Do not persist target facts or temporary workflow state
here.

## Completion

Before claiming completion:

- the working root matches the authority boundary
- repository-local facts remain local
- introduced artifacts each solve an observed problem
- checks and references are real
- unresolved decisions and remaining gaps are explicit
- durable evidence has one owner
- the next review or currentness trigger is named
