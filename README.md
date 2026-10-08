# Agentic Engineering Skills & Harness

I am [Leonard "Lenny" Daume](https://www.daume.dev). These are the Agent Skills
and harness patterns I use to make agent work reliable across product,
engineering, delivery, and operations.

They encode a practical operating model for work under uncertainty: learn
through small experiments, evolve domain models with DDD, build vertical slices
with TDD, shift quality, security, compliance, and operability left, and expand
autonomy only when evidence supports it.

The repository combines a portable Skill catalog with harness blueprints for
single-repository, multi-repository, and multi-team systems. Humans retain
goals, policy, risk, and accountability; agents carry as much execution as the
proven controls allow. You pick by what you need today: install Skills alone
(each works on its own, no harness required), read the blueprints alone
([`HARNESS-OPERATIONS.md`](./HARNESS-OPERATIONS.md),
[`MULTI-REPO-HARNESS.md`](./MULTI-REPO-HARNESS.md)), or take both, which the
prompts below assume. This is not a control plane for another system. Most first
uses stay on one repository.

## Start here

| Goal | Start with |
|---|---|
| Inspect the catalog | `npx skills add ldaume/agentic-engineering-harness --list` |
| Audit or establish a repository harness | [`scaffold-harness`](./skills/engineering/scaffold-harness/SKILL.md) |
| Choose or switch how much agents do alone | [`Operating levels`](#operating-levels) |
| Set up a multi-repository or multi-team harness | [`HARNESS-OPERATIONS.md`](./HARNESS-OPERATIONS.md) |
| Onboard a new sibling (simplest) | Session in the coordinator; ask the agent to fully onboard it and pass context - [`Simplest path`](./HARNESS-OPERATIONS.md#simplest-path-onboard-a-sibling) |
| Find which sibling or team is in scope for a task | [`Find Sibling Scope and Decide Relevance`](./MULTI-REPO-HARNESS.md#find-sibling-scope-and-decide-relevance) (human walkthrough) / [`How a Session Finds Related Repositories`](./HARNESS-OPERATIONS.md#how-a-session-finds-related-repositories) |
| Understand the recommended defaults and alternatives | [`Golden Path and Known Alternatives`](./HARNESS-OPERATIONS.md#golden-path-and-known-alternatives) |
| Keep a harness current across sessions | [`agent-sync`](./skills/engineering/agent-sync/SKILL.md) |
| Deliver a dependency upgrade through production | [`deliver-dependency-upgrades`](./skills/engineering/deliver-dependency-upgrades/SKILL.md) |
| Shape value-defined issues and honest roadmaps | [`product-craft`](./skills/product/product-craft/SKILL.md) |
| Write numbers a non-participant reads correctly | [`plain-numbers`](./skills/product/plain-numbers/SKILL.md) |
| Run the full signal-to-outcome loop | [`run-product-engineering`](./skills/product/run-product-engineering/SKILL.md) |
| Understand the complete operating model | [`MULTI-REPO-HARNESS.md`](./MULTI-REPO-HARNESS.md) |

## Operating levels

Every harness records one operating level: how much agents do on their own.
`scaffold-harness` recommends a level from what your repository already has,
asks you to choose, sets the harness up to match, and switches it up or down
when you rerun it with another level. L1 (one supervised task) and L2 (one
repeatable Skill) need no harness.

| Level | Agents do on their own | You still do | Minimum prerequisites |
|---|---|---|---|
| L3 Living repository | Change code, run checks, keep context and learnings, commit | Own intent, domain meaning, and material decisions | Runnable Fast Check and Full Gates |
| L4 Grounded system | Also use external sources and tools within named access | Approve new access and consequential external effects | Owner, scope, and failure path for each source or tool |
| L5 Stateful workflow | Also run a recurring workflow end to end, retry, and recover | Handle exceptions and open decisions | Durable workflow state, recovery, run observability, a stop path |
| L6 Governed value stream | Also merge, deploy, and roll back proven change classes | Set goals and risk; veto, incidents, accountability | Required CI checks, checked deploy, executable rollback, production alerts, incident owner |
| L7 Adaptive product system | Also choose bounded problems and experiments; with the owner-delegated profile, decide everything outside a short owner-reserved list | Set vision, budgets, the reserved list; confirm reserved items; stop the system | Proven L6, trusted product signals, budgets, kill criteria |

Details, the switch procedure, and where the level is recorded:
[Choosing and Switching the Operating Level](./skills/engineering/scaffold-harness/MATURITY.md#choosing-and-switching-the-operating-level).

## Install

Requires Node.js (`npx`). Review the source and requested scope before a global installation. Installed
Skills run through an agent with that agent's permissions, and `-y` skips the
Skills CLI confirmation.

```bash
npx skills add ldaume/agentic-engineering-harness --list
npx skills add ldaume/agentic-engineering-harness \
  --skill scaffold-harness \
  --skill agent-sync \
  --skill update-harness \
  --skill grill-harness-with-docs \
  --skill write-a-skill \
  --agent codex cursor claude-code gemini-cli \
  --copy -g -y
```

Replace the example client list with every agent host you actually use (`npx skills add --help` lists the ids), then
check that a real session loads what you installed: hosts differ in what
triggers a Skill. Install only these five bootstrap Skills globally (installs track the default branch; for exact pins see [`VERSIONING.md`](./VERSIONING.md#consumers)); keep
project and domain Skills in the target repository so they stay visible and
scoped. [`scaffold-harness`](./skills/engineering/scaffold-harness/SKILL.md)
carries a template for routing a host to Skills. Use
[`write-a-skill`](./skills/engineering/write-a-skill/SKILL.md) whenever an agent
creates or changes a Skill.

To install one Skill into the current project from a local clone (`git clone https://github.com/ldaume/agentic-engineering-harness`):

```bash
npx skills add /path/to/agentic-engineering-harness \
  --skill coding-discipline \
  --agent codex \
  --copy -y
```

The validation workflow install-tests the catalog for Codex, Cursor, Claude
Code, and Gemini CLI. That is packaging compatibility, not identical runtime
behavior; Pi, CI, and later runtimes need a target-owned adapter first.

## Choose a first prompt

Start the agent inside the authority boundary it should change. The prompt
selects the harness topology; there is no separate sibling-onboarding Skill.
To add a sibling, open a session in the coordinating repository and ask the
agent to fully onboard it
([detail](./HARNESS-OPERATIONS.md#simplest-path-onboard-a-sibling)). To decide
which sibling or team is in scope, see
[`Find Sibling Scope and Decide Relevance`](./MULTI-REPO-HARNESS.md#find-sibling-scope-and-decide-relevance).

| Scope | Start the session in |
|---|---|
| One repository | The target repository root |
| Several repositories | The existing coordinating repository, or a workspace containing the intended repositories as siblings |
| Several teams | A dedicated federated coordinating repository with access to the participating repositories |

### One repository

```text
First verify that the working root is the target repository root. If it is not,
stop and name the correct working root before installing or changing anything.

Use the Skills from
https://github.com/ldaume/agentic-engineering-harness.

Inspect that source. If any Skill named in this prompt is unavailable, install
only that missing Skill project-locally for the active agent host. Do not
install globally or expand permissions without explicit authority.

Use scaffold-harness to assess this repository and add only the context,
capabilities, feedback, and governance it needs. Preserve local truth,
recommend an operating level from what the repository already has and let me
choose it, name the real Fast Check and Full Gates, and
verify the result with those repository checks. Use grill-harness-with-docs
for shared understanding, material critique, and unresolved decisions, and
run agent-sync before completion.
```

### Several repositories

Use the one-repository prompt with these changes; onboarding detail is in
[`HARNESS-OPERATIONS.md`](./HARNESS-OPERATIONS.md#simplest-path-onboard-a-sibling).

```text
Verify that the working root is an existing coordinating repository or a
workspace containing the intended repositories as siblings; do not infer
membership from proximity alone. If no coordinator exists, resolve placement and
authority first.

Use scaffold-harness to establish the smallest reliable cross-repository
harness. Each member stays the authority for its local truth; the coordinator
holds only relationships, public contracts, shared workflow state, and
cross-cutting verification, with one `CONTEXT-MAP.md` as the relationship map.
Admit a sibling by composing scaffold-harness in it with the coordinator `SYNC.md`
admit checklist. Present options with a recommendation when ownership is
unresolved. Run the real member and integration checks and agent-sync before
completion.
```

### Several teams

Use the one-repository prompt with these changes.

```text
Verify that the working root is a dedicated federated coordinating repository
with access to the participating repositories.

Use scaffold-harness and scaffold-distributed-context to establish a
multi-team harness. Preserve each team's local authority: map bounded contexts,
public contracts, compatibility policy, risk, release, and autonomy decisions to
named owners in one federated `CONTEXT-MAP.md`, without creating a central
product or domain authority. Define cross-team checks and escalation. Present
unresolved decision rights one at a time with a recommendation, then run the
team-local and cross-team checks and agent-sync before completion.
```

For how the harness works and why, read
[`MULTI-REPO-HARNESS.md`](./MULTI-REPO-HARNESS.md): L1-L7 delegation, topology,
the nested product loops, review, memory, compliance, host portability, and
Skill ownership.

## Working principles

1. **One product loop.** Signal, discovery, implementation, delivery,
   operations, and evolution share evidence and ownership.
2. **DDD plus vertical TDD.** Domain language and boundaries guide design;
   small executable slices test both behavior and understanding.
3. **Shift assurance left.** Security, compliance, operability, accessibility,
   and recovery enter when a decision is still cheap to change.
4. **Autonomy through evidence.** Permissions and blast radius grow only when
   checks, observability, recovery, and representative results justify them.
5. **Git-owned truth.** Decisions, controls, checks, and evidence stay concise,
   versioned, reviewable, and close to the work.

## Core Skills and technology profiles

Portable means a reusable installation and invocation contract, not that every
Skill is language-neutral or every host behaves identically.

The core contains methods that transfer across stacks:

- Product system: [`product-craft`](./skills/product/product-craft/SKILL.md),
  [`run-product-engineering`](./skills/product/run-product-engineering/SKILL.md),
  [`integrate-product-compliance`](./skills/product/integrate-product-compliance/SKILL.md)
- Infrastructure system:
  [`manage-infrastructure-as-code`](./skills/infrastructure/manage-infrastructure-as-code/SKILL.md)
- Harness and agents: [`scaffold-harness`](./skills/engineering/scaffold-harness/SKILL.md),
  [`scaffold-distributed-context`](./skills/engineering/scaffold-distributed-context/SKILL.md),
  [`agent-sync`](./skills/engineering/agent-sync/SKILL.md),
  [`update-harness`](./skills/engineering/update-harness/SKILL.md),
  [`grill-harness-with-docs`](./skills/engineering/grill-harness-with-docs/SKILL.md),
  [`build-autonomous-agents`](./skills/engineering/build-autonomous-agents/SKILL.md),
  [`deliver-dependency-upgrades`](./skills/engineering/deliver-dependency-upgrades/SKILL.md),
  [`learn-agentic-engineering`](./skills/engineering/learn-agentic-engineering/SKILL.md),
  [`write-a-skill`](./skills/engineering/write-a-skill/SKILL.md),
  [`system-one-routing`](./skills/engineering/system-one-routing/SKILL.md)
- Engineering method: [`start-gate`](./skills/engineering/start-gate/SKILL.md),
  [`coding-discipline`](./skills/engineering/coding-discipline/SKILL.md),
  [`completion-gate`](./skills/engineering/completion-gate/SKILL.md),
  [`documentation-and-adrs`](./skills/engineering/documentation-and-adrs/SKILL.md),
  [`api-design`](./skills/backend/api-design/SKILL.md),
  [`testing-strategies`](./skills/testing/testing-strategies/SKILL.md)

`frontend-craft` and `backend-craft` are standalone Skills; shared end-to-end
craft lives in `coding-discipline`. Opinionated profiles carry real stack
knowledge (pnpm monorepos, Meilisearch, Playwright, Gitea, Docker, Ansible,
secure Linux hosting) where generic advice would be weaker. Missing coverage is
resolved by reusing an existing Skill or writing a project-local one with
`write-a-skill`.

Browse by category:

- [Engineering](./skills/engineering/README.md)
- [Product](./skills/product/README.md)
- [Frontend](./skills/frontend/README.md)
- [Backend](./skills/backend/README.md)
- [Infrastructure](./skills/infrastructure/README.md)
- [Testing](./skills/testing/README.md)

[`skills-lock.json`](./skills-lock.json) is the complete versioned catalog.

## Repository maintenance

Agents start at [`AGENTS.md`](./AGENTS.md), which also holds the Fast Check.
Release rules are in [`VERSIONING.md`](./VERSIONING.md), prose style in
[`VOICE.md`](./VOICE.md), and contribution policy in
[`CONTRIBUTING.md`](./CONTRIBUTING.md): consume and adapt; external pull
requests are not the supported path.

## License

MIT. See [`LICENSE`](./LICENSE).
