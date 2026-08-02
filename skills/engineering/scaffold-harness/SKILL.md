---
name: scaffold-harness
description: Audits and upgrades repositories to a reliable, maturity-appropriate Agentic Engineering harness without overwriting local truth. Use when bootstrapping or repairing agent instructions, designing local/MCP/RAG context routing, controlling token bloat, defining review, model, or quality gates, coordinating repositories, or evaluating agents for CI, overnight, specialist, chat, and observability work.
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
- package manager, scripts, CI, deployment, observability, and security controls
- actual Fast Check and Full Gates
- repository boundaries, public integration contracts, owners, and consumers
- existing Skills, Rules, Hooks, MCP configuration, memory, and evals
- effective project and workspace roots, coordinator placement policy, managed
  private organization or team catalogs, public upstreams, user and global
  bootstrap roots, host precedence, and collisions
- live agent-host capabilities, available model controls, orchestration support,
  and the freshness of any model, pricing, feature, or community guidance

Resolve discoverable facts from repository evidence. Preserve user-written
content and local naming.

Complete grounding when existing sources, commands, boundaries, and gaps are
identified without relying on invented product semantics.

## 2. Assess the Target State

Read [REFERENCE.md](./REFERENCE.md). Read [MATURITY.md](./MATURITY.md) when
assessing a level, moving beyond repository work, changing human oversight, or
planning organizational transformation. Evaluate each maturity dimension
independently:

Select the smallest topology that matches real authority and coordination:

- **Single repository:** local instructions, context, checks, and learnings are
  sufficient; do not add a coordinator.
- **Multiple repositories:** use a coordinating harness only for durable
  relationships, public contracts, workflow state, oversight, and integration
  checks. Every member retains local truth and a session entrypoint.
- **Multiple teams:** federate team-local harnesses through named decision
  rights, bounded contexts, public contracts, compatibility policy,
  cross-team evals, and escalation. A central coordinator does not become the
  product or domain authority for every team.

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

Default to a reliable repository-level harness. Add grounded tools,
stateful workflows, delivery automation, or product loops only when evidence
supports the wider delegated unit.

Complete assessment when the current level, target level, and evidence for
each proposed addition are explicit.

## 3. Resolve Decisions

Use **grill-harness-with-docs** for unresolved intent, ownership, architecture,
governance, risk, or oversight transitions.

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

Read [CURRENTNESS.md](./CURRENTNESS.md) before proposing model routing,
multi-agent orchestration, provider features, or a community Golden Path.

Read [CONTEXT-ARCHITECTURE.md](./CONTEXT-ARCHITECTURE.md) when deciding what
belongs locally or behind MCP, RAG, search, projections, or memory; or when
large tool output, long sessions, handoffs, instruction growth, token pressure,
RTK, Context Mode, Headroom, or another compression layer affects the design.

Read [CAPABILITY-GATES.md](./CAPABILITY-GATES.md) on every significant harness
stewardship pass: decide whether Graphify-class discovery, Headroom/Context
Mode economy tools, or memory systems should enter, stay parked, or be removed.
Do not add them without an observed failure mode.

Read [RUNTIMES.md](./RUNTIMES.md) before adding agents to CI, schedules,
overnight windows, durable services, specialist roles, chat, or production
observability. Use **build-autonomous-agents** after the runtime gate passes and
a bounded workload is ready for implementation.

Use **run-product-engineering** when an L5-L7 delegated unit spans product
signals, delivery, production feedback, incidents, outcomes, or investment
decisions. Use **product-craft** when the target needs value-defined issues or
an honest Now/Next/Later/Never investment view. Use
**integrate-product-compliance** only for confirmed security, contractual,
certification, TISAX, PCI, or other control scope.

## 5. Apply

- Keep root agent instructions concise and reference detailed owners.
- Resolve the current human's preferred collaboration language from explicit
  preference or conversation evidence; ask once only when it remains unclear.
  Store personal preference in user-scoped or untracked state unless it is a
  shared repository rule. Chat language never changes artifact language.
- Write harness artifacts in US English with ASCII punctuation only (straight
  quotes, hyphen `-`, `...`) unless the human explicitly requests another
  language for a named artifact. Do not introduce curly quotes, em/en dashes,
  ellipsis characters, or odd spaces.
- Preserve an existing repository voice or style owner. Repository prose should
  be direct and concrete: lead with the problem or working model, state
  trade-offs and system effects, and remove generic hype, defensive setup, and
  text that changes no decision or action.
- Reserve first person for artifacts that explicitly speak for the repository
  owner. Keep agent instructions and operating procedures neutral and
  imperative.
- Add a harness operating contract for proactive, evidence-backed evolution.
- Add domain context only when confirmed language or invariants exist.
- Add a context map only for multiple contexts, repositories, or source routes.
- Add learnings when a durable evidence loop is needed.
- Add `STATUS.md` when cross-session or cross-repo work needs mid-flight state.
- Add a sync protocol and thin member pointers when several repositories must
  discover one coordinator.
- Require a session-safe local agent entrypoint in every listed member,
  including experiments. Session discovery does not grant unattended autonomy;
  autonomy remains gated by local checks, recovery, permissions, and status.
- Create the human `README.md` projection from the template when no adequate
  local equivalent exists, and keep it accurate when purpose, cycle,
  membership, working-root rules, or delegated operating level change. It must
  explain the current human and agent roles by product phase and operating
  level, the smaller loops nested inside the current delegated unit, technical
  controls, engineering method, why that allocation fits the evidence, and the
  trigger for wider delegation without duplicating the agent control plane.
- Design canonical instructions, context, state, contracts, and failures for
  agent comprehension first. Keep README and reference views legible for
  humans, but do not reproduce human ceremony in the agent control plane.
- Add ADRs only for accepted consequential trade-offs.
- Use Skills for repeated probabilistic procedures.
- Route from the goal and current lifecycle stage to one owning Skill plus only
  the needed local or managed private or public complements. Do not require the
  user to name Skills or prescribe a permanent Skill stack.
- Distinguish project-local semantics, private organization or team catalogs,
  private coordinator policy, public upstream Skills, and the small user or
  global bootstrap. Inspect host precedence, pin managed dependencies, and keep
  one semantic owner per workflow; public availability never grants private
  authority.
- Resolve the host's effective project, workspace, managed private and public,
  user, global, bundled, and plugin Skill scopes. When a selected loop needs a
  missing complement, prefer an approved managed source; for a new public
  candidate, follow `CURRENTNESS.md` to discover, evaluate, install
  project-locally, and invoke it. Never claim an uninstalled Skill was used.
- Use **update-harness** in hygiene mode to keep repository-specific Skills
  local, retain only justified reusable global Skills, preserve host-managed
  packages, and reconcile duplicate or conflicting effective installations.
- Compare overlapping public workflow collections before activation. Use
  upstream `ponytail` only as an optional, piloted implementation-style
  guardrail when repeated overengineering justifies it; do not weaken
  validation, security, accessibility, data integrity, recovery, or necessary
  error handling.
- Use Hooks, CI, tests, and platform controls for deterministic enforcement.
- Keep canonical semantics host-neutral. Use `AGENTS.md` as the portable owner
  and install the thin baseline bridges for Claude Code (`CLAUDE.md` import),
  Gemini CLI (`GEMINI.md` import), and Google Antigravity
  (`.agents/rules/harness.md`). Codex, Cursor, and Pi consume `AGENTS.md`
  directly. Verify the declared host matrix; add other bridges only for hosts
  the repository actually uses. Reference canonical owners instead of copying
  policy, and verify precedence, permissions, and behavior per host.
- Classify source authority, freshness, locality, shape, activation,
  persistence, access, and verification before adding MCP, RAG, memory, or a
  local projection. Keep stable session-critical routing local and query live
  systems only for task-relevant current information or actions.
- Retrieve at the lowest sufficient resolution and keep raw bulk output outside
  the active context when the host supports it. Use one filtering owner per
  data path; add compression only after a representative baseline exposes a
  residual problem.
- Add event-triggered self-review, independent review, currentness review, and
  autonomy review only where their evidence can change a decision.
- Use a capable current parent model for decomposition and integration. Route
  bounded worker tasks to the least expensive current model that passes
  representative checks; never optimize token price independently of retries,
  review cost, latency, and failure impact.
- Add `ORCHESTRATION.md` only for repeated multi-agent work, model routing, or
  cross-repository coordination. Discover live runtime controls before writing
  host-specific configuration.
- Add an agent runtime only for a bounded repeated workload. Prefer existing CI
  and scheduler controls, open-source self-hostable components, explicit
  isolation, budgets, cancellation, evals, and target-owned telemetry.
- Treat currentness as an evolution contract, not a frozen research note. When
  evidence expires, a host or tool changes, or representative tasks expose a
  mismatch, re-evaluate the affected owner and keep, change, remove, supersede,
  or rebuild it. Do not preserve incremental structure when replacement is the
  smaller reliable system.
- At L6-L7, close the product loop from attributable signals through delivery,
  production observation, incident and bug feedback, outcome review, and an
  explicit next decision. Release alone is not completion.
- For product work that uses shared investment or issue tracking, at any level,
  treat Now/Next/Later/Never as investment decisions rather than date promises.
  Keep Later coarse, record Never with rationale and a revisit trigger, and
  create decision or delivery issues only for sufficiently sharp Now or Next
  work. Raw intake records may remain without becoming commitments. The
  delegation level determines who maintains and approves these decisions, not
  whether the semantics apply.
- For product engineering, reject specification -> implementation -> testing ->
  deployment as a handoff pipeline. Use **run-product-engineering** for
  pull-based learning cycles, evolutionary DDD, bounded spikes, vertical TDD,
  shift-left security/operability, production feedback, and repeated evolution.
- Integrate compliance through target-owned risk, controls, evidence, and
  release policy. Agents do not infer scope, accept risk, or make assurance
  claims.
- For cross-repository work, preserve repository-local truth and coordinate
  through public contracts, owners, compatibility checks, and shared evals.
  Use **scaffold-distributed-context** when shared domain language, projections,
  or retrieval layers need their own cross-repository design.
- For multi-team work, record the team or role owning each bounded context,
  contract, policy, risk acceptance, and release decision. Version shared
  harness policy and Skills, but let team-local owners choose implementation
  and checks within their authority. Add cross-team escalation and integration
  evidence without creating a central ticket or documentation bureaucracy.

## 6. Verify

1. Run the documented Fast Check and relevant Full Gates.
2. Verify every referenced local file and command exists.
3. Confirm each active host resolves the intended Skill versions without
   collisions and agent instructions remain concise.
4. Review the diff for overwritten local truth, speculative layers, and
   customer or product assumptions.
5. Verify volatile claims have a source, check date, and re-check trigger; do
   not retain copied price tables or assumed model availability.
6. For a context-economy change, verify the complete routing path and compare
   successful-task quality, tokens, latency, retries, and recovery with the
   baseline.
7. State the operating level, remaining gaps, and next evidence trigger.

The scaffold is complete only when:

- instructions and source routing are discoverable,
- the declared host matrix is backed by verified thin bridges or an explicit
  non-interactive adapter that loads `AGENTS.md`,
- every listed repository has a local session entrypoint and safe coordinator
  fallback, independent of its autonomy level,
- a human README or local equivalent explains where to start, the current
  operating envelope, phase responsibilities, rationale, and graduation gates,
- domain facts and decisions have explicit owners,
- a real Fast Check and Full Gates are named,
- uncertainty and escalation behavior are defined,
- cross-session learning has one durable owner,
- review loops have triggers, stop conditions, and an action when they fail,
  including evidence-gated dependency-bot PR handling (inspect jump, run
  checks, merge or comment - never silent-merge or silent-ignore),
- model and worker routing is either live-discovered or explicitly absent,
- context routing has one owner per data path, visible authority and freshness,
  and preserves required evidence,
- scheduled or service execution has bounded authority, cost, isolation,
  recovery, cancellation, and observability,
- all introduced artifacts have a demonstrated purpose,
- multi-team systems expose decision rights, contract ownership, compatibility
  checks, escalation, and team-local authority,
- verification results are reported.

## Templates

| Artifact | Template |
|---|---|
| Human operating guide | [templates/README.md](./templates/README.md) |
| Root instructions | [templates/AGENTS.md](./templates/AGENTS.md) |
| Claude Code bridge | [templates/CLAUDE.md](./templates/CLAUDE.md) |
| Gemini CLI bridge | [templates/GEMINI.md](./templates/GEMINI.md) |
| Google Antigravity bridge | [templates/.agents/rules/harness.md](./templates/.agents/rules/harness.md) |
| Harness contract | [templates/HARNESS.md](./templates/HARNESS.md) |
| Domain language | [templates/CONTEXT.md](./templates/CONTEXT.md) |
| Context routing | [templates/CONTEXT-MAP.md](./templates/CONTEXT-MAP.md) |
| Multi-agent routing | [templates/ORCHESTRATION.md](./templates/ORCHESTRATION.md) |
| Durable learnings | [templates/LEARNINGS.md](./templates/LEARNINGS.md) |
| Open workflow state | [templates/STATUS.md](./templates/STATUS.md) |
| Member/coordinator sync | [templates/SYNC.md](./templates/SYNC.md) |
| Tool entrypoints | [templates/TOOLS.md](./templates/TOOLS.md) |
| Project Skills | [templates/skills-README.md](./templates/skills-README.md) |

## Related Skills

- **grill-harness-with-docs** - resolve uncertain harness decisions
- **agent-sync** - evolve the harness from evidence across sessions
- **scaffold-distributed-context** - establish domain context and contracts
  across repositories
- **build-autonomous-agents** - implement a bounded product or SDLC agent
- **run-product-engineering** - operate a closed signal-to-outcome value stream
- **integrate-product-compliance** - integrate confirmed control scope and
  evidence
- **coding-discipline** - make minimal implementation changes
- **completion-gate** - verify before claiming completion
