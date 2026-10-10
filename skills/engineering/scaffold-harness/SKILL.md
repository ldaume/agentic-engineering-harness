---
name: scaffold-harness
license: MIT
description: Audits and upgrades one repository to a reliable, maturity-appropriate Agentic Engineering harness without overwriting local truth. Use when bootstrapping or repairing agent instructions, choosing or switching a repository's operating level, designing local/MCP/RAG context routing, controlling token bloat, or defining review and quality gates for a repository.
---

# Scaffold Harness

Build the smallest harness that makes delegated work reliable. Ideal means
fit for the repository and its current maturity, not the largest artifact set.

## 1. Ground the Repository

Inspect before proposing files:

- instruction entrypoints and bridges: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `.cursor/rules/`, or local equivalents
- repository and domain sources: `README.md`, `CONTEXT.md`, ADRs, specs,
  architecture docs, code, and tests
- package manager, scripts, CI, infrastructure desired state and state backend,
  deployment, drift detection, observability, security controls, compliance
  policy, and evidence
- actual Fast Check and Full Gates
- repository boundaries, public integration contracts, owners, and consumers
- existing Skills, Rules, Hooks, MCP configuration, memory, and evals
- the portable Skill-authoring owner and any host-bundled creator, scaffolder,
  command, plugin, or validator that may overlap it
- effective project, user, and global Skill roots, host precedence, and
  collisions
- live agent-host capabilities and the freshness of any model, pricing,
  feature, or community guidance the design would rely on

Resolve discoverable facts from repository evidence, because a harness built
on assumed commands or semantics fails on the first real task. Preserve
user-written content and local naming.

Complete grounding when existing sources, commands, boundaries, and gaps are
identified without relying on invented product semantics.

## 2. Assess the Target State

Read [REFERENCE.md](./REFERENCE.md). Read [MATURITY.md](./MATURITY.md) when
assessing or switching a level or changing human oversight. Evaluate each
maturity dimension independently, because one strong dimension does not
compensate for a weak one:

- product and domain clarity
- codebase changeability
- feedback and quality
- delivery and operations
- repository context
- agent operation
- governance and security
- learning system
- currentness and economics
- context architecture and economy

Default to a reliable repository-level harness. Add grounded tools only when
evidence supports the wider delegated unit; each addition is context and
maintenance every later session pays for.

**When one repository is not enough.** Work that spans several repositories or
teams needs a coordinator, one context map, and explicit hand-offs between
sessions. This Skill does not build that; the [levels](https://github.com/ldaume/agentic-engineering-harness/blob/main/docs/LEVELS.md)
and [beyond one repository](https://github.com/ldaume/agentic-engineering-harness/blob/main/docs/BEYOND-ONE-REPOSITORY.md) describe it.

Choose the operating level with the owner: recommend the highest level whose
prerequisites the repository already has, or less when the goal needs less,
ask once, and record the choice per
**Choosing and Switching the Operating Level** in [MATURITY.md](./MATURITY.md).
Rerunning this Skill with a different target level switches up or down through
the same procedure; it is a no-op when the recorded level already matches.
A granted level also needs the matching declaration in the host's permission
context (template `HARNESS.md` bullet **Autonomy is declared where it is enforced**).

Ask once whether review surfaces stay free of agent attribution. The default
and the recommendation are yes: keep template `HARNESS.md` item
**Review-surface attribution** with its enforcement. A no removes that item and
its enforcement as a unit; record the choice in the target's `HARNESS.md`
either way, so a later run does not ask again or add it back.

Complete assessment when the current level, target level, and evidence for
each proposed addition are explicit.

## 3. Resolve Decisions

Establish shared understanding for significant work. Use
**grill-harness-with-docs** for unresolved intent, semantics, ownership,
architecture, governance, consequential trade-offs, risk, or oversight
transitions in any topic. Route resolved material decisions and changes through
fresh-context agent critique.

Research facts first. Put genuine decisions to the human one at a time with
options, trade-offs, reversibility, evidence, and a recommendation. Wait before
implementing the dependent branch.

Complete decision work when every branch is resolved or explicitly blocked.

## 4. Plan the Smallest Upgrade

Match the requested mode: audit reports the current state, propose presents the
smallest viable options, and apply makes only authorized reversible changes.

Map existing files to the ownership model in `REFERENCE.md`. Prefer updating
an existing source over creating a parallel preferred name.

For every proposed artifact state:

- the observed problem it solves
- its single owning concern
- its consumers
- the smallest verification
- why a reference or existing control is insufficient

Use templates only for missing artifacts. Create optional artifacts lazily.
Merge `.serena/` into the target `.gitignore`; never commit Serena's local
project state and never overwrite existing ignore rules.

Read [CONTEXT-ARCHITECTURE.md](./CONTEXT-ARCHITECTURE.md) when deciding which
artifact owns a kind of context, when instruction growth or token pressure
affects the design, or when large tool output floods sessions. When auditing
token bloat, follow **Startup Context Budget** there.

Read [CAPABILITY-GATES.md](./CAPABILITY-GATES.md) on every significant harness
stewardship pass: decide whether Graphify-class discovery, Headroom/Context
Mode economy tools, or memory systems should enter, stay parked, or be removed.
Do not add them without an observed failure mode.

Agents in CI, on a schedule, or as a durable service are L5 work and outside
this Skill's scope. Use **build-autonomous-agents** when one bounded product
agent or finite workflow is ready for implementation.

Use **run-product-engineering** when the work spans product signals, delivery,
production feedback, incidents, or outcomes. Use **product-craft** when the
target needs value-defined issues or an honest Now/Next/Later/Never investment
view. Use
**integrate-product-compliance** only for confirmed security, contractual,
certification, TISAX, PCI, or other control scope. Use
**manage-infrastructure-as-code** when agents create, change, provision, or
reconcile infrastructure desired state.

## 5. Apply

- Keep root agent instructions concise and reference detailed owners, because
  every session pays for the entry chain before it starts working.
- Resolve the current human's preferred collaboration language from explicit
  preference or conversation evidence; ask once only when it remains unclear.
  Store personal preference in user-scoped or untracked state unless it is a
  shared repository rule. Chat language never changes artifact language.
- Write harness artifacts in US English with plain punctuation unless the
  human explicitly requests another language for a named artifact. Character
  rules and fixer limits: `REFERENCE.md` **Language and Punctuation**.
- Preserve an existing repository voice or style owner. Repository prose should
  be direct and concrete: lead with the problem or working model, state
  trade-offs and system effects, and remove generic hype, defensive setup, and
  text that changes no decision or action.
- Reserve first person for artifacts that explicitly speak for the repository
  owner. Keep agent instructions and operating procedures neutral and
  imperative, so an agent never mistakes one person's voice for its own rule.
- Add a harness operating contract for proactive, evidence-backed evolution.
- Add domain context only when confirmed language or invariants exist; invented
  terms become false authority for every later session.
- Add learnings when a durable evidence loop is needed.
- Keep the human `README.md` accurate when purpose, operating level, or working
  rules change, because a new reader learns the system from it, not from the
  agent control plane.
- Design canonical instructions, context, state, contracts, and failures for
  agent comprehension first. Keep README and reference views legible for
  humans, but do not reproduce human ceremony in the agent control plane.
- Add ADRs only for accepted consequential trade-offs.
- Use Skills for repeated probabilistic procedures.
- Install `write-a-skill` in every host scope where agents may create or change
  Skills. Treat a platform-bundled creator as a thin adapter for native
  metadata, scaffolding, or validation; it does not own portable Skill
  behavior. Do not infer cross-host discovery from a successful session on one
  host, because hosts load Skills from different roots.
- When copied bootstrap Skills are managed, record the exact source, immutable
  per-Skill tag, and resolved commit in a target-owned manifest. A one-off
  Skills CLI install is a pilot, not a reproducible dependency.
- Derive the actual stack and major versions from target evidence. Keep core
  craft methods separate from technology profiles, and use **update-harness**
  to reuse an owned profile, pilot a current public candidate, or work directly
  for a one-off gap. Create a project-local Skill only after repeated need
  provides examples and checks.
- Compare overlapping public workflow collections before activation. Use
  upstream `ponytail` only as an optional, piloted implementation-style
  guardrail when repeated overengineering justifies it; do not weaken
  validation, security, accessibility, data integrity, recovery, or necessary
  error handling.
- Use Hooks, CI, tests, and platform controls for deterministic enforcement.
- Match activation to how each host actually selects behavior, because
  "installed" is not "used". Where a host reads instruction files as behavior,
  a rule in `AGENTS.md` is enough. Where a host selects a Skill as a tool from
  its name and description - Claude Code does - a rule competes with
  everything else in the instruction chain and routinely loses: an observed
  session there loaded no Skill across roughly forty tool calls while writing a
  Skill and making five commits, with the routing rule in context the whole
  time. On such a host, put the routing in a Hook at the moment of the
  decision, keep it silent unless something is off, and commit it to the
  repository so contributors get it with the clone.
- Keep repeatable infrastructure desired state in version control. Route
  infrastructure changes through **manage-infrastructure-as-code** for plan,
  policy checks, protected state, controlled apply, drift, and recovery. Treat
  emergency console work as an incident action that must be reconciled or
  reversed, not as a second configuration source.
- Keep canonical semantics host-neutral. Use `AGENTS.md` as the portable owner
  and install the thin baseline bridges for Claude Code (`CLAUDE.md` import),
  Gemini CLI (`GEMINI.md` import), and Google Antigravity
  (`.agents/rules/harness.md`). Codex, Cursor, and Pi consume `AGENTS.md`
  directly. Add other bridges only for hosts the repository actually uses, and
  reference canonical owners instead of copying policy, so one rule never
  drifts into several versions.
- Classify source authority, freshness, locality, shape, activation,
  persistence, access, and verification before adding MCP, RAG, memory, or a
  local projection. Keep stable session-critical routing local and query live
  systems only for task-relevant current information or actions.
- Retrieve at the lowest sufficient resolution and keep raw bulk output outside
  the active context when the host supports it. Use one filtering owner per
  data path; add compression only after a representative baseline exposes a
  residual problem.
- Add event-triggered self-review, independent review, and autonomy review only
  where their evidence can change a decision; a review that cannot change the
  next action is cost without effect.
- Re-evaluate an owner when its evidence expires, a host or tool changes, or
  representative tasks expose a mismatch, and keep, change, remove, or replace
  it. Do not preserve incremental structure when replacement is the smaller
  reliable system.
- For product work that uses shared investment or issue tracking, at any level,
  treat Now/Next/Later/Never as investment decisions rather than date promises.
  Keep Later coarse, record Never with rationale and a revisit trigger, and
  create decision or delivery issues only for sufficiently sharp Now or Next
  work. Raw intake records may remain without becoming commitments.
- For product engineering, reject specification -> implementation -> testing ->
  deployment as a handoff pipeline. Use **run-product-engineering** for
  evolutionary DDD, bounded spikes, vertical TDD, shift-left
  security/operability, production feedback, and repeated evolution.
- Keep frontend and backend craft independently installable and useful. Route
  shared end-to-end discipline through **coding-discipline**, while each craft
  Skill retains its own thin-UI, boundary, data, operability, and experience
  guidance.
- Integrate compliance through target-owned risk, controls, evidence, and
  release policy. Encode stable enforceable controls as tested policy through
  **integrate-product-compliance**; keep interpretation, scope, risk acceptance,
  and assurance claims with named humans.

## 6. Verify

1. Run the documented Fast Check and relevant Full Gates.
2. Verify every referenced local file and command exists.
3. Confirm each active host resolves the intended Skill versions without
   collisions and agent instructions remain concise. When Skill authoring is
   in scope, verify that `write-a-skill` is the resolved portable owner and any
   native creator remains an adapter.
   The public catalog currently install-tests Codex, Cursor, Claude Code, and
   Gemini CLI. Treat Pi, CI, and later runtimes as candidate hosts until the
   target has a native adapter and a representative bootstrap check.
4. Review the diff for overwritten local truth, speculative layers, and
   customer or product assumptions.
5. Verify volatile claims have a source, check date, and re-check trigger; do
   not retain copied price tables or assumed model availability.
6. For a context-economy change, verify the complete routing path and compare
   successful-task quality, tokens, latency, retries, and recovery with the
   baseline.
7. Verify the `Level:` line matches the chosen level and its pending gates,
   and state the remaining gaps and next evidence trigger.

The scaffold is complete only when:

- instructions and source routing are discoverable,
- the declared host matrix is backed by verified thin bridges or an explicit
  non-interactive adapter that loads `AGENTS.md`,
- every declared host can discover the bootstrap Skills, including
  `write-a-skill` wherever agents may maintain Skills,
- a human README or local equivalent explains where to start, the current
  operating level, and what would justify the next one,
- domain facts and decisions have explicit owners,
- a real Fast Check and Full Gates are named,
- uncertainty and escalation behavior are defined,
- cross-session learning has one durable owner,
- shared understanding has an explicit entry and exit frame,
- review loops route resolved material work to fresh-agent critique and genuine
  unresolved decisions to a human, with triggers, stop conditions, and an
  action when they fail,
  including evidence-gated dependency-bot PR handling (inspect jump, run
  checks, merge or comment - never silent-merge or silent-ignore),
- context routing has one owner per data path, visible authority and freshness,
  and preserves required evidence,
- infrastructure automation has an owned desired state, reviewable plan,
  protected state, policy gates, drift path, runtime verification, and credible
  recovery,
- all introduced artifacts have a demonstrated purpose,
- verification results are reported.

## Templates

| Artifact | Template |
|---|---|
| Root instructions | [templates/AGENTS.md](./templates/AGENTS.md) |
| Claude Code bridge | [templates/CLAUDE.md](./templates/CLAUDE.md) |
| Review-surface attribution check | [scripts/verify-agent-attribution.py](./scripts/verify-agent-attribution.py), tested by [tests/test_verify_agent_attribution.py](./tests/test_verify_agent_attribution.py) |
| Gemini CLI bridge | [templates/GEMINI.md](./templates/GEMINI.md) |
| Google Antigravity bridge | [templates/.agents/rules/harness.md](./templates/.agents/rules/harness.md) |
| Harness contract | [templates/HARNESS.md](./templates/HARNESS.md) |
| Domain language | [templates/CONTEXT.md](./templates/CONTEXT.md) |
| Durable learnings | [templates/LEARNINGS.md](./templates/LEARNINGS.md) |
| Tool entrypoints | [templates/TOOLS.md](./templates/TOOLS.md) |
| Local tool state ignore | [templates/.gitignore](./templates/.gitignore) |

## Related Skills

- **grill-harness-with-docs** - ground, critique, and resolve material decisions
- **agent-sync** - evolve the harness from evidence across sessions
- **update-harness** - check, install, update, and clean managed Skills
- **build-autonomous-agents** - implement a bounded product agent or workflow
- **run-product-engineering** - run the signal-to-outcome product loop
- **integrate-product-compliance** - integrate confirmed control scope and
  evidence
- **manage-infrastructure-as-code** - manage desired state, plans, state,
  policy checks, apply, drift, and recovery
- **coding-discipline** - make minimal implementation changes
- **completion-gate** - verify before claiming completion
