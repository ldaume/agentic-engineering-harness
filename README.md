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
| Keep a harness current across sessions | [`agent-sync`](./skills/engineering/agent-sync/SKILL.md) |
| Shape value-defined issues and honest roadmaps | [`product-craft`](./skills/product/product-craft/SKILL.md) |
| Run the full signal-to-outcome loop | [`run-product-engineering`](./skills/product/run-product-engineering/SKILL.md) |
| Understand the complete operating model | [`MULTI-REPO-HARNESS.md`](./MULTI-REPO-HARNESS.md) |

A useful first prompt is:

```text
Use scaffold-harness to assess this repository and add only the context,
capabilities, feedback, and governance it needs. Preserve local truth, use the
lowest reliable delegation level, and verify the result with real repository
checks.
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

Opinionated profiles and adapters carry real stack knowledge where generic
advice would be weaker: TypeScript backend and React frontend craft, pnpm
monorepos, Meilisearch, Playwright, Gitea, Docker, Ansible, and secure Linux
hosting. I add another language or framework only after repeated use provides
examples, checks, and a maintenance owner.

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
  --agent codex \
  --copy -g -y
```

Replace `codex` with a client supported by the installed Skills CLI. Install
only the three bootstrap Skills globally. Project and domain Skills normally
belong in the target repository so they remain visible, reviewable, and scoped
to the work.

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
workloads and target-local checks remain the evidence.

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
