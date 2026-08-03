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
goals, policy, risk, and accountability. Agents carry as much execution as the
proven controls allow.

## Start here

| Goal | Start with |
|---|---|
| Inspect the catalog | `npx skills add ldaume/agentic-engineering-harness --list` |
| Audit or establish a repository harness | [`scaffold-harness`](./skills/engineering/scaffold-harness/SKILL.md) |
| Set up a multi-repository or multi-team harness | [`HARNESS-OPERATIONS.md`](./HARNESS-OPERATIONS.md) |
| Understand the recommended defaults and alternatives | [`Golden Path and Known Alternatives`](./HARNESS-OPERATIONS.md#golden-path-and-known-alternatives) |
| Keep a harness current across sessions | [`agent-sync`](./skills/engineering/agent-sync/SKILL.md) |
| Shape value-defined issues and honest roadmaps | [`product-craft`](./skills/product/product-craft/SKILL.md) |
| Run the full signal-to-outcome loop | [`run-product-engineering`](./skills/product/run-product-engineering/SKILL.md) |
| Understand the complete operating model | [`MULTI-REPO-HARNESS.md`](./MULTI-REPO-HARNESS.md) |

## Choose a first prompt

Start the agent inside the authority boundary it should change. This catalog
supplies the capabilities; it is not the control plane for another system.

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
capabilities, feedback, and governance it needs. Preserve local truth, use the
lowest reliable delegation level, name the real Fast Check and Full Gates, and
verify the result with those repository checks. Use grill-harness-with-docs
for shared understanding, material critique, and unresolved decisions, and
run agent-sync before completion.
```

### Several repositories

```text
First verify that the working root is an existing coordinating repository or
a workspace containing the intended repositories as siblings. Discover
candidate repositories, but do not infer membership from proximity alone.
If this is only a workspace and no coordinator exists, resolve coordinator
placement and authority before installing or changing anything.

Use the Skills from
https://github.com/ldaume/agentic-engineering-harness.

Inspect that source. If any Skill named in this prompt is unavailable, install
only that missing Skill project-locally in the authority-bearing repository
for the active agent host. Do not install globally or expand permissions
without explicit authority.

Use scaffold-harness to establish or evolve the smallest reliable
cross-repository harness. Treat every member as the authority for its local
truth. Keep only relationships, public contracts, shared workflow state, and
cross-cutting verification in the coordinator. Use one coordinator
`CONTEXT-MAP.md` as the canonical repository relationship and discovery map,
reached through `SYNC.md` with a local route and stable remote fallback. Do not
create a parallel `HARNESS-MAP.md`. Present options with a
recommendation before creating a coordinator or expanding autonomy when
ownership or authority is unresolved. Run the real member and integration
checks, and run agent-sync before completion.
```

### Several teams

```text
First verify that the working root is a dedicated federated coordinating
repository with access to the participating repositories. If it is not, stop
and name the correct working root before installing or changing anything.

Use the Skills from
https://github.com/ldaume/agentic-engineering-harness.

Inspect that source. If any Skill named in this prompt is unavailable, install
only that missing Skill project-locally for the active agent host. Do not
install globally or expand permissions without explicit authority.

Use scaffold-harness and scaffold-distributed-context to establish or evolve a
multi-team harness.
Preserve each team's local authority. Map bounded contexts, public contracts,
compatibility policy, risk, release, and autonomy decisions to named owners. Use
one federated coordinator `CONTEXT-MAP.md` as the canonical repository
relationship and discovery map, reached through `SYNC.md` with local routes and
stable remote fallbacks. Do not create a parallel `HARNESS-MAP.md`. Define
cross-team checks and escalation without creating a central product or domain
authority. Present unresolved decision rights one at a time with a
recommendation, run the real team-local and cross-team checks, and run
agent-sync before completion.
```

## What is in this repository

- Focused Agent Skills for product work, implementation, testing,
  infrastructure, and harness stewardship.
- Repository-local harness patterns that route agents to real context, tools,
  checks, authority, memory, and recovery paths.
- Human guidance for using agents from a bounded task through governed
  multi-repository and multi-team product systems.

The Skills follow the portable `SKILL.md` convention. The harness is the
surrounding system that makes those procedures reliable in a specific
repository. A Skill is not a substitute for product context, permissions,
tests, observability, or human accountability.

## How humans and agents work

| Phase | Human responsibility | Agent work | Controls that matter |
|---|---|---|---|
| Signal and triage | Set outcomes, constraints, risk, and policy | Gather evidence, connect signals, propose the next learning step | Source authority, explicit scope, reversible decisions |
| Experiment and learn | Judge value and consequential domain choices | Build spikes, prototypes, and throwaway tests; record what changed | Timeboxes, discard criteria, user evidence, DDD language |
| Build and release | Retain accountability for product, security, and release authority | Implement vertical slices with TDD, update contracts, run checks, prepare integration | Fast Check, Full Gates, review, recovery, least privilege |
| Operate and evolve | Own outcomes, risk appetite, and operating policy | Observe production, diagnose failures, fix causes, feed evidence into the next loop | Telemetry, incident paths, audit trail, rollback, currentness review |

This is one closed learning system, not a sequence where a complete
specification is handed to development and tests appear at the end. Concepts
evolve through evidence. Prototypes may be discarded. Production behavior
changes the next decision.

A specification is a current boundary or hypothesis, not a promise that the
problem and solution are completely known. A backlog, when useful, is a small
pull queue for the next decisions - not an inventory of assumed future value.
For larger product decisions, Now/Next/Later/Never is an investment view rather
than a date promise: Later stays coarse, Never is explicit, and only sharp Now
or Next work becomes a decision or delivery issue. Raw signal records may stay
in the intake system without becoming commitments. The detailed guide shows the
product loop, the learning and delivery loops inside it, and which loop is
enough at each delegation level.

The detailed guide explains [L1-L7 delegation, topology, review, memory,
compliance, and host portability](./MULTI-REPO-HARNESS.md).

The three central views are:

- [human and agent work by L1-L7 delegation level](./MULTI-REPO-HARNESS.md#human-and-agent-operating-model-by-delegation-level)
- [the nested product engineering loops](./MULTI-REPO-HARNESS.md#product-engineering-loop)
- [public, private, coordinator, project, and global Skill ownership](./MULTI-REPO-HARNESS.md#skill-architecture)

Every significant topic starts and ends with shared understanding. Agents
ground facts and test safe hypotheses autonomously, fresh agents critique
resolved material work, and human grilling is reserved for genuinely
unresolved intent, semantics, authority, consequential trade-offs, or material
risk. Explicit authorization and veto remain at named external-risk
boundaries. The detailed guide explains why this avoids both permission theater
and unsupervised guesswork.

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
6. **Shared understanding before scale.** Significant work has explicit
   outcomes, boundaries, sources, decision rights, assumptions, checks, and
   stop conditions before autonomy or blast radius expands.
7. **Cost-aware delegation.** Spawn the least expensive model proven for the
   bounded role, then use stronger integration or review only where consequence
   or ambiguity warrants it. Count retries, review, latency, and failure impact,
   not token price alone.
8. **Provider-neutral routing.** Keep Fast, Balanced, and Frontier roles stable;
   map them through separate live Codex, Claude Code, Cursor, Gemini CLI, Pi,
   CI, or later-host adapters. New models earn promotion through representative
   work instead of replacing a proven route by name alone.

## Core Skills and technology profiles

Portable means that a Skill has a reusable installation and invocation
contract. It does not mean every Skill is language-neutral or that every agent
host behaves identically.

The core contains methods that transfer across stacks:

- Product system: [`product-craft`](./skills/product/product-craft/SKILL.md),
  [`run-product-engineering`](./skills/product/run-product-engineering/SKILL.md),
  [`integrate-product-compliance`](./skills/product/integrate-product-compliance/SKILL.md)
- Harness and agents: [`scaffold-harness`](./skills/engineering/scaffold-harness/SKILL.md),
  [`scaffold-distributed-context`](./skills/engineering/scaffold-distributed-context/SKILL.md),
  [`agent-sync`](./skills/engineering/agent-sync/SKILL.md),
  [`update-harness`](./skills/engineering/update-harness/SKILL.md),
  [`grill-harness-with-docs`](./skills/engineering/grill-harness-with-docs/SKILL.md),
  [`build-autonomous-agents`](./skills/engineering/build-autonomous-agents/SKILL.md),
  [`learn-agentic-engineering`](./skills/engineering/learn-agentic-engineering/SKILL.md),
  [`write-a-skill`](./skills/engineering/write-a-skill/SKILL.md)
- Engineering method: [`coding-discipline`](./skills/engineering/coding-discipline/SKILL.md),
  [`completion-gate`](./skills/engineering/completion-gate/SKILL.md),
  [`documentation-and-adrs`](./skills/engineering/documentation-and-adrs/SKILL.md),
  [`api-design`](./skills/backend/api-design/SKILL.md),
  [`testing-strategies`](./skills/testing/testing-strategies/SKILL.md)

`frontend-craft` and `backend-craft` stay separate, standalone Skills. They can
be installed directly without the full harness and retain the detail that
makes each surface useful. Shared end-to-end craft lives in
`coding-discipline`: thin UIs, task-shaped read models, intent-shaped
mutations, context-driven architecture, and representative fail-fast spikes.

Opinionated profiles and adapters carry real stack knowledge where generic
advice would be weaker: frontend experience, backend and data boundaries, pnpm
monorepos, Meilisearch, Playwright, Gitea, Docker, Ansible, and secure Linux
hosting. Languages, frameworks, databases, and architecture styles are tools
selected for the product and evidence. I add another specific profile only
after repeated use provides examples, checks, and a maintenance owner.

That specificity is intentional. A public catalog should not turn a working
pnpm monorepo, Playwright, Docker, or TypeScript procedure into vague advice to
look universal. The portable part is the selection and lifecycle contract:
agents inspect the target stack, combine core craft with the smallest relevant
profiles, and keep unsupported technology assumptions out of the common path.

When coverage is missing, the harness resolves it without asking a person to
curate framework prompts. It reuses an owned project, private, public, bundled,
or plugin Skill; searches and pilots a current public candidate; works directly
for a one-off; or uses `write-a-skill` to create a project-local profile after
repeated need supplies real examples and checks. Reuse and provenance decide
whether that profile later moves to a public or private catalog. Human grilling
is reserved for unresolved architecture, adoption, authority, security, cost,
or risk decisions.

Browse by category:

- [Engineering](./skills/engineering/README.md)
- [Product](./skills/product/README.md)
- [Frontend](./skills/frontend/README.md)
- [Backend](./skills/backend/README.md)
- [Infrastructure](./skills/infrastructure/README.md)
- [Testing](./skills/testing/README.md)

[`skills-lock.json`](./skills-lock.json) is the complete versioned catalog.

## Install

Review the source and requested scope before a global installation. Installed
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

Replace the example client list with every agent host you actually use. Install
only the five bootstrap Skills globally. The shared `.agents/skills` location
is useful where clients support it, but a harness must verify effective
discovery per host instead of assuming one installation covers every runtime.
Project and domain Skills normally belong in the target repository so they
remain visible, reviewable, and scoped to the work.

`write-a-skill` is the portable owner whenever an agent creates or changes a
Skill. Codex, Claude Code, Cursor, Gemini, Pi, CI, and later hosts may provide
native creators, commands, metadata, or validators; those capabilities remain
thin adapters around the same behavior contract.

To install one Skill into the current project:

```bash
npx skills add /path/to/agentic-engineering-harness \
  --skill coding-discipline \
  --agent codex \
  --copy -y
```

The validation workflow install-tests the complete catalog for Codex, Cursor,
Claude Code, and Gemini CLI. Thin `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and
Antigravity bridges make repository instructions discoverable. Packaging
compatibility does not guarantee identical runtime behavior; representative
workloads and target-local checks remain the evidence. Pi, CI, and later
runtimes need a target-owned adapter and bootstrap check before a harness
declares them supported.

## Repository maintenance

- [`AGENTS.md`](./AGENTS.md) is the executable entry point for agents working
  in this repository.
- [`HARNESS.md`](./HARNESS.md) defines stewardship, authority, review, and
  repository boundaries.
- [`VOICE.md`](./VOICE.md) keeps public prose direct, specific, and free of
  generic AI marketing language.
- [`VERSIONING.md`](./VERSIONING.md) defines independent Skill versions and
  release tags.
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) defines contribution and authorship
  expectations.

Run the local Fast Check before integration:

```bash
python3 scripts/audit-skills.py
```

For a new or materially changed Skill, also run the provenance audit and an
install test in a temporary target. External publication, remotes, and releases
remain explicit maintainer decisions.

## License

MIT. See [`LICENSE`](./LICENSE).
