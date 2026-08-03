# Harness Operations

Use this guide to set up or join a repository harness. It explains which
repositories are needed, where harness artifacts belong, and how an agent finds
the right instructions, capabilities, and related repositories.

A harness is the repository-owned combination of instructions, context,
capability routing, checks, and recovery that makes agent work reliable.

Start with the smallest topology that fits the work. Read
[`MULTI-REPO-HARNESS.md`](MULTI-REPO-HARNESS.md) only when the operating model,
delegation levels, or deeper rationale matter.

## The Working Model

Three rules keep the system understandable:

1. Each product or service repository owns its local truth.
2. A coordinator owns only relationships and evidence that span repositories.
3. Skill catalogs supply reusable capabilities; they do not become product
   control planes.

The complete system may use these scopes:

| Scope | Needed when | Owns |
|---|---|---|
| Target or member repository | Always | Local instructions, product and domain facts, code, commands, permissions, checks, and local adapters |
| Coordinating repository | Durable contracts, workflow state, policy, or verification span repositories | Membership, relationships, public contracts, shared policy, cross-repository state, integration checks, and escalation |
| Public Skill catalog | Portable public procedures are reused | Generic Skills, immutable releases, provenance, and templates |
| Private organization or team Skill catalog | Non-public procedures or approved adapters are reused across targets | Shared private Skills, approved pins, and internal adapters |
| User or global scope | A small bootstrap is useful across repositories | Discovery and harness maintenance only |

Both Skill catalogs and the user or global bootstrap are optional capability
sources. A single repository does not need a coordinator.

## Choose the Topology and Working Root

This table selects the root for harness setup or shared coordination. Start a
member-local product or operations change in that member repository.

| Scope | For harness setup or coordination, start in | Add |
|---|---|---|
| One repository | The target repository root | No coordinator |
| Several repositories | The existing coordinating repository, or a workspace containing the intended repositories as siblings | A coordinator only for durable cross-repository relationships or state |
| Several teams | A dedicated federated coordinating repository with access to the participating repositories | Named team and decision rights, compatibility policy, cross-team checks, and escalation |
| Target not known or accessible | This Skill catalog for discovery only | Switch to the target or coordinator before changing target files |

A practical multi-repository workspace can look like this:

```text
workspace/
  product-harness/       # coordinating repository
  checkout-service/      # member owned by one team
  web-application/       # member owned by one team
  platform/              # member owned by one team
  private-skills/        # optional shared non-public Skill catalog
```

The directory names are not a contract. The coordinator's context map records
the real paths, full canonical HTTPS discovery URLs, owners, relationships, and
checks. A discovery URL need not match a credentialed Git `origin`. Use
`local / no origin` when no remote exists; never infer a host from an
`owner/repository` shorthand. Repositories do not need to share a parent
directory, but sibling checkouts make local discovery fast and work offline.

This public Skill catalog is a capability source. Do not use it as the
coordinator for another system.

## How an Agent Finds the System

A session follows this path:

1. Start in the repository that owns the requested change.
2. Load the nearest `AGENTS.md`. Thin host bridges such as `CLAUDE.md`,
   `GEMINI.md`, or `.agents/rules/harness.md` point to that canonical owner.
3. Read the local `README.md`, `HARNESS.md`, and `CONTEXT-MAP.md` routes needed
   for the task. Local instructions remain authoritative for local work.
4. For a member repository, follow its thin coordinator pointer. Prefer a
   local sibling checkout and keep a stable remote or raw-file fallback.
5. Read the coordinator's `HARNESS.md` and `SYNC.md`, then use its
   `CONTEXT-MAP.md` to find relevant members, contracts, owners, revisions, and
   integration checks.
6. Inspect the active host's effective Skill, plugin, Rule, Hook, MCP,
   permission, and instruction precedence before relying on an adapter.
7. Retrieve only the sources required by the current task and write durable
   results back to their owning repositories.

If the coordinator is unavailable locally and remotely, continue only
reversible member-local work. Do not infer shared state, cross-repository
authority, or a higher autonomy level.

## What Lives Where

Create artifacts only when they have a consumer and a check. Use an existing
local equivalent instead of adding a preferred filename beside it.

| Artifact | Member or target repository | Coordinating repository | Why it exists |
|---|---|---|---|
| `README.md` | Human purpose, local usage, and checks | Human map of the system, members, and working roots | Gives people a legible starting point |
| `AGENTS.md` | Canonical local instructions plus a thin coordinator pointer | Canonical coordination boundaries and entrypoint | Starts every agent session with the right authority |
| Host bridges | Only for hosts actually used | Only for hosts used from the coordinator | Load `AGENTS.md` without copying policy |
| `HARNESS.md` | Local stewardship, permissions, review, and completion | Shared oversight, autonomy, recovery, and escalation | Defines how the harness evolves safely |
| `CONTEXT.md` | Confirmed local domain language and invariants | Only confirmed language shared across members | Prevents agents from inventing semantics |
| `CONTEXT-MAP.md` | Local source routing when several contexts exist | Members, paths, remotes, owners, contracts, compatibility, and checks | Makes relationships and source authority discoverable |
| `SYNC.md` | No separate file; keep a thin coordinator pointer in `AGENTS.md` | Member discovery, admission, fan-out, and write-back | Keeps coordination consistent without copying local truth |
| `STATUS.md` | Local mid-flight state when needed | Open cross-repository work, stop conditions, and recovery | Carries volatile workflow state across sessions; clear it when done |
| `LEARNINGS.md` | Durable local evidence when no harder owner fits | Durable cross-repository evidence when no harder owner fits | Changes future work without relying on chat history |
| ADRs and contracts | Local accepted decisions and provided contracts | Cross-repository decisions, public contracts, and compatibility policy | Makes consequential choices and integration boundaries reviewable |
| Project Skills and [`harness-skills.yaml`](skills/engineering/update-harness/REFERENCE.md#target-manifest) when no target-native manifest exists | Local procedures, wrappers, exact source, immutable ref, resolved commit, and active host targets | Approved sources, compatibility, and adoption policy | Separates reusable procedure supply from target semantics and installation state |
| Rules | Scoped local guidance for an active host | Shared rule versions only when coordination requires them | Narrows behavior without replacing canonical instructions |
| Hooks, tests, and CI | Local deterministic enforcement and real Fast Check or Full Gates | Integration checks, cross-team evals, and policy gates | Detects failures with executable evidence |
| `TOOLS.md` and MCP configuration | Host adapters, tools, permissions, source authority, and freshness when several tools need routing | Shared capability policy and cross-repository tools when justified | Explains how live context and actions are reached and governed |

The minimum coordinator discovery baseline is a human `README.md` or local
equivalent, `AGENTS.md`, `HARNESS.md`, `CONTEXT-MAP.md`, coordinator `SYNC.md`
plus thin member pointers, active-host bridges, and real checks. `STATUS.md`,
`LEARNINGS.md`, `CONTEXT.md`, `TOOLS.md`, local Skills, Rules, Hooks, and MCP
servers are conditional. Add them for observed work, not to make the repository
look complete.

Starting points for these files live in the
[`scaffold-harness` templates](skills/engineering/scaffold-harness/templates/).
Copy only the artifacts justified by the target.

## How Capabilities Are Owned and Loaded

| Capability | Canonical owner | Placement rule | Verification |
|---|---|---|---|
| Skill | The project, private catalog, or public upstream that owns the procedure | Keep target semantics local, shared non-public behavior private, portable behavior public, and only the small bootstrap global | Verify exact source, immutable ref, resolved commit, host target, and representative behavior |
| Rule | The repository and host scope that need the guidance | Keep it scoped and point to canonical instructions instead of copying them | Verify the active host loads it at the intended precedence |
| Hook | The repository or platform that owns the deterministic event | Add only for a repeated failure a Hook can reliably prevent | Trigger it and verify actionable pass and failure behavior |
| MCP server | The workspace or system that owns access to the live source or action | Record source authority, freshness, permissions, external-action approval, and fallback | Exercise the required resource, prompt, or tool with least privilege |
| Plugin or bundled capability | The repository or upstream owns semantics; the active host owns loading and adapter behavior | Treat the host capability as an adapter unless the repository explicitly assigns another role | Verify the live host behavior; do not infer portability to other hosts |

Semantic ownership and filesystem precedence are different. Inspect what the
active host actually loads. Select one owner for each procedure and avoid
stacking equivalent planning, testing, review, or style workflows.

## Set Up One Repository

1. Open the target repository as the working root.
2. Read its existing instructions, sources, commands, permissions, Fast Check,
   and Full Gates.
3. Use the one-repository prompt in [`README.md`](README.md#one-repository).
4. Apply the smallest useful harness upgrade in that repository.
5. Verify local references and checks, then use `agent-sync` before completion.

Do not create a coordinator for one clear authority boundary.

## Set Up Several Repositories

Create a dedicated coordinator only when durable work spans public contracts,
dependency order, shared workflow state, policy, or integration verification.

1. Open the intended repositories as siblings or record how each can be
   reached.
2. Resolve which repository owns coordination before installing or changing
   shared artifacts.
3. Establish the minimum coordinator discovery baseline named under
   [What Lives Where](#what-lives-where).
4. Establish a safe local harness and real checks in every member.
5. Add every member to the coordinator `CONTEXT-MAP.md` with its role, owner,
   path, full canonical HTTPS discovery URL or `local / no origin`, status,
   local checks, relationships, and authority boundary.
6. Add the thin coordinator pointer below to every member `AGENTS.md` and the
   required host bridges.
7. Record shared capability sources and policy in the coordinator. Record each
   consuming project's exact Skill refs and resolved commits in its existing
   dependency convention or `harness-skills.yaml`.
8. Add only the integration checks and workflow state the observed work needs.
9. Run member-local and coordinator checks. Commit members and coordinator
   separately.

Use the several-repositories prompt in
[`README.md`](README.md#several-repositories) to let an agent perform this
assessment and setup.

### Thin member pointer

Adapt paths and URLs, but keep the pointer small:

```markdown
## Coordinated system

- For cross-repository work, read `../product-harness/HARNESS.md` and
  `../product-harness/SYNC.md`, then use its `CONTEXT-MAP.md` to find members,
  contracts, owners, and checks.
- If the local coordinator is unavailable, use the pinned remote fallback at
  `<stable-url-or-raw-file>`. If neither source is reachable, continue only
  reversible member-local work.
- This repository remains authoritative for its product, domain, commands,
  permissions, implementation, and local checks.
```

## Add a Team or Member

Use this path for a new repository or a team joining an existing system:

1. Name the team or role that owns the repository and its bounded contexts.
2. Give the member a local `AGENTS.md`, human `README.md`, Fast Check, and Full
   Gates before granting cross-repository authority.
3. Add the member to the coordinator map as experimental until its repository,
   checks, ownership, and coordinator pointer are real.
4. Record provider and consumer contracts, compatibility responsibility, and
   escalation where the member crosses a boundary.
5. Add the thin member pointer and verify every active host loads the intended
   instructions and managed Skills.
6. Update coordinator `STATUS.md` while admission is incomplete.
7. Run local and cross-repository checks, then graduate the member to active.

For several teams, also record who may change shared policy, accept risk,
approve releases, resolve semantic conflicts, and widen autonomy. Version
shared Skills and policy so teams can adopt them with compatibility evidence.
Keep team backlogs, local implementation state, and inferred domain semantics
out of the coordinator.

Use the several-teams prompt in [`README.md`](README.md#several-teams) for a
federated setup.

## Bootstrap from This Repository

A session may start in this public catalog when the target cannot be opened:

1. Resolve the intended target paths, repositories, and authority.
2. Choose the smallest topology that fits the durable work.
3. Open the target or coordinator as the working root.
4. Re-read the local instructions there.
5. Continue with the matching setup above.

Do not edit target files while treating this catalog's instructions as their
authority. Do not store target facts or temporary workflow state here.

## Completion

Before claiming completion, verify:

- the working root matches the authority boundary
- every member has a local session entrypoint and real checks
- the coordinator map matches intended members, owners, relationships, and
  remotes
- local and remote coordinator discovery work, including safe degradation
- every active host resolves its intended instructions and managed Skills
- Rules, Hooks, plugins, and MCP servers have one owner and a demonstrated need
- introduced artifacts each solve an observed problem
- local and cross-repository checks pass
- unresolved decisions, recovery, escalation, and remaining gaps are explicit
- durable evidence has one owner and the next re-check trigger is named
