# Harness Operations

Use this guide to set up or join a repository harness. It explains which
repositories are needed, where harness artifacts belong, and how a session
finds the right instructions, capabilities, and related repositories.

A harness is the repository-owned combination of instructions, context,
capability routing, checks, and recovery that makes agent work reliable.

Start with the smallest topology that fits the work. Read
[`MULTI-REPO-HARNESS.md`](MULTI-REPO-HARNESS.md) only when the operating model,
delegation levels, or deeper rationale matter.

## Simplest path: onboard a sibling

For an existing multi-repository or multi-team harness:

1. Open a session in the **coordinating repository**.
2. Tell the agent to **fully onboard** the new sibling (or joining team
   repository).
3. Give the context it needs: name and path, purpose or role, remote or
   "create remote", intended checks, experimental vs active, and any
   boundaries.

The agent follows the coordinator `SYNC.md` admit checklist and runs
`scaffold-harness` in the member. No dedicated onboarding Skill. Detail below
under [Add a Team or Member](#add-a-team-or-member).

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

## Golden Path and Known Alternatives

The golden path is the default for this operating model, not a claim that one
shape fits every system. Use an alternative when its named conditions apply,
and record the reason where future humans and agents will find it.

| Decision | Golden path and why | Known alternative and when it fits |
|---|---|---|
| Local authority | Each member owns its product, domain, code, permissions, and checks. This keeps truth beside the system that can verify it. | Central ownership fits a genuinely centralized system with one accountable owner. Do not centralize only to make agent navigation easier. |
| Coordinator | Add one only for durable cross-repository relationships, contracts, state, or checks. This keeps coordination visible without turning it into product authority. | No coordinator is simpler for one repository or loosely related repositories. A shared folder alone does not justify one. |
| Membership | Record explicit members, owners, paths, and full canonical discovery URLs. Proximity and Git remotes are useful evidence, not authority. | Automatic discovery may propose candidates in a dynamic fleet, but an owner or governed registry must confirm membership. |
| Relationship map | Keep one coordinator `CONTEXT-MAP.md`, reached through `SYNC.md` with a local route and stable remote fallback. One source is fast locally, location-independent remotely, and mechanically verifiable. | A separate `HARNESS-MAP.md` duplicates relationships and can drift. A member-to-member pointer mesh becomes incomplete as membership grows. See [ADR 0001](docs/decisions/0001-one-canonical-cross-repository-discovery-map.md). |
| Reusable capabilities | Keep portable procedures in provenance-checked Skill catalogs and target-specific truth in the owning repository. This permits reuse without importing another repository's authority. | Copying or global unpinned installation can be convenient for experiments, but it obscures provenance and update boundaries. |
| Coordination record | Prefer Git-owned contracts, decisions, state, and executable checks. They survive sessions and can be reviewed with the code they affect. | Chat and meetings remain useful for resolving ambiguity, but they are not durable system authority until the outcome is written back. |
| Autonomy | Set autonomy per decision domain from permissions, checks, recovery, observability, and evidence. Topology alone says nothing about safe delegation. | One system-wide autonomy label is simpler to announce, but hides where controls or decision rights differ. |

## Choose the Topology and Working Root

Pick the smallest topology that matches durable authority. The first prompt in
[`README.md`](README.md#choose-a-first-prompt) selects that topology for the
session. Agents do not need a separate onboarding Skill to learn the type:

| Evidence | Topology |
|---|---|
| One product or service root; no coordinator map of siblings | One repository |
| Coordinator `CONTEXT-MAP.md` lists member repositories and relationships | Multi-repository |
| Same map also names team or role owners and decision rights | Multi-team federation |

Then open the working root from the table below.

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

## How a Session Finds Related Repositories

Humans and agents use the same discovery path. Start in the repository that
owns the change. Open another repository or team surface only when the
coordinator map names a match for the task.

1. Start in the repository that owns the requested change.
2. Load the nearest `AGENTS.md`. Thin host bridges such as `CLAUDE.md`,
   `GEMINI.md`, or `.agents/rules/harness.md` point to that canonical owner.
3. Read the local `README.md`, `HARNESS.md`, and `CONTEXT-MAP.md` routes needed
   for the task. Local instructions remain authoritative for local work.
4. For a member repository, follow its thin coordinator pointer. Prefer a
   local sibling checkout and keep a stable remote or raw-file fallback.
5. Read the coordinator's `HARNESS.md` and `SYNC.md`, then use its
   `CONTEXT-MAP.md` to find relevant members, contracts, owners, revisions, and
   integration checks. Match the task to Role, Relationships, Source Routing,
   and the SYNC working-root table before opening another root; stay local when
   nothing matches. For the portable multi-repository and multi-team walkthrough
   (with an out-of-scope example), see
   [`Find Sibling Scope and Decide Relevance`](MULTI-REPO-HARNESS.md#find-sibling-scope-and-decide-relevance).
6. Inspect the active host's effective Skill, plugin, Rule, Hook, MCP,
   permission, and instruction precedence before relying on an adapter.
7. Retrieve only the sources required by the current task and write durable
   results back to their owning repositories.

If the coordinator is unavailable locally and remotely, continue only
reversible member-local work. Do not infer shared state, cross-repository
authority, or a higher autonomy level.

`CONTEXT-MAP.md` is the single repository relationship and discovery map.
Keep a local route and stable remote fallback in the coordinator sync document;
do not add a parallel `HARNESS-MAP.md`.

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

**Simplest human move:** session in the coordinator; ask the agent to fully
onboard the sibling and pass its context (see
[Simplest path: onboard a sibling](#simplest-path-onboard-a-sibling)).

When you want the checklist, or the agent is executing admission, do not create
a dedicated sibling-onboarding Skill; compose existing owners:

1. Name the team or role that owns the repository and its bounded contexts.
2. In the member, run `scaffold-harness` (or adapt existing instructions) so
   local `AGENTS.md`, human `README.md`, Fast Check, and Full Gates exist before
   granting cross-repository authority.
3. In the coordinator, follow the admit checklist in `SYNC.md`: add the member
   to `CONTEXT-MAP.md` as experimental until its repository, checks, ownership,
   and coordinator pointer are real.
4. Record provider and consumer contracts, compatibility responsibility, and
   escalation where the member crosses a boundary.
5. Add the thin member pointer and verify every active host loads the intended
   instructions and managed Skills.
6. Update coordinator `STATUS.md` while admission is incomplete.
7. Run local and cross-repository checks, integrate mergeable session-owned
   tips, then graduate the member to active.

For several teams, also record who may change shared policy, accept risk,
approve releases, resolve semantic conflicts, and widen autonomy. Version
shared Skills and policy so teams can adopt them with compatibility evidence.
Keep team backlogs, local implementation state, and inferred domain semantics
out of the coordinator.

Match task relevance with
[`Find Sibling Scope and Decide Relevance`](MULTI-REPO-HARNESS.md#find-sibling-scope-and-decide-relevance)
before opening another member or team surface.

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
