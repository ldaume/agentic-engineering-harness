# Harness Target-State Reference

## Principle

An ideal harness is the smallest system that gives an agent enough context,
capability, feedback, and governance to change the intended system safely.
Higher delegation is useful only when the lower level is reliable.

## Operating Stance

- Optimize the whole work system, not a prompt, model, or tool in isolation.
- Use the lowest delegation level that solves the real problem reliably.
- Context, changeability, feedback, recovery, and decision rights matter more
  than a small benchmark advantage.
- Skills and automation support understood workflows; they do not replace
  understanding cause, effect, ownership, or artifact contents.
- Prefer native controls and the smallest reversible mechanism. Evaluate every
  candidate by utility, evidence, blast radius, maintenance, cognitive load,
  and removal cost.
- Let agent-facing systems be agent-native. Their structure may differ from a
  human-crafted handbook when machine routing, explicit contracts, progressive
  disclosure, or deterministic checks improve reliability.
- Communicate with each human in their preferred collaboration language, while
  keeping persistent repository artifacts in US English unless a named
  artifact is explicitly requested in another language. Personal preferences
  belong in user-scoped or untracked state unless they are shared policy.
- Keep canonical semantics host-neutral and map them through thin, verified
  adapters for the coding host or runtime actually in use. Native plugins,
  Skills, Rules, Hooks, MCP, permissions, and CI controls are adapters, not
  independent policy owners.
- Use root `AGENTS.md` as the portable owner. The baseline bridges are a
  `CLAUDE.md` import, a `GEMINI.md` import, and an Antigravity repository rule;
  Codex, Cursor, and Pi load `AGENTS.md` directly. Non-interactive adapters
  must explicitly load the owner and prove it in a representative workload.
- Keep human review surfaces legible while the workflow is human-in-the-loop.
  Agent-native does not mean opaque.
- Currentness is part of correctness. Volatile model, pricing, platform,
  security, and community claims need a source, check date, and re-check trigger.
- Context architecture makes authority, freshness, locality, activation, and
  persistence explicit before context economy optimizes successful-task cost,
  latency, and risk.
- Treat product engineering as pull-based domain and risk learning from signal
  through production evidence. Specifications, tests, security, operability,
  and deployment are feedback activities, not downstream departments.
- Represent repeatable deterministic state as versioned code or structured
  configuration when this makes review, checks, reconciliation, and recovery
  stronger. Keep unresolved meaning and accountable decisions with their named
  owners.

## Artifact Ownership

| Concern | Preferred owner |
|---|---|
| Stable agent behavior, scope, permissions | `AGENTS.md` or local equivalent |
| Domain language and invariants | `CONTEXT.md` |
| Contexts, sources, and relationships | `CONTEXT-MAP.md` |
| Harness evolution and oversight | `HARNESS.md` |
| Current workflow or engagement state | Status document |
| Accepted consequential trade-off | ADR |
| Durable evidence-backed observation | `LEARNINGS.md` |
| Repeated probabilistic procedure | Skill |
| Scoped behavioral guidance | Rule or agent instruction |
| Deterministic event or enforcement | Hook, CI, test, platform control |
| Grounded external capability | Tool or MCP server |
| Outcome and regression signal | Eval, test, observability |
| Signal-to-outcome product lifecycle | Target product operating system; `run-product-engineering` supplies the procedure |
| Compliance scope, risks, controls, and evidence | Target ISMS or GRC system and named control owners |
| Infrastructure desired state, state backend, and drift | Target infrastructure repository and named platform owners; `manage-infrastructure-as-code` supplies the procedure |
| Executable control policy and tests | Target repository or policy system under the named control owner; `integrate-product-compliance` supplies the procedure |

Use the repository's existing equivalent when it already owns the concern.
Reference owners from consumers instead of copying the same truth.

## Reliable Repository Baseline

A reliable repository-level harness has:

- one concise, discoverable agent instruction entrypoint
- confirmed repository and domain sources
- source routing when more than one context or repository exists
- a real Fast Check for narrow work
- explicit Full Gates before integration
- clear decision rights, trust boundaries, and external-write limits
- Git-backed decisions and learnings, with Git history as the audit,
  comparison, and rollback path
- a documented escalation path
- versioned desired state and executable policy for repeatable infrastructure
  or control changes, with an explicit GitOps, GitOps-near, or bounded IaC
  reconciliation model, protected runtime state, and human-owned semantics
- only the Skills, Rules, Hooks, and tools justified by observed work

## Delegation Levels and Evidence

[MATURITY.md](./MATURITY.md) owns the L1-L7 capability profiles, transition
gates, evidence requirements, human roles, and operating-model effects. Load it
only when level assessment, increased autonomy, changed oversight, or
organizational transformation affects the task.

Evidence belongs in the target or coordinating system, not in this Skills
repository. Add a missing control only when its owner, expected effect, and
verification are explicit. Otherwise retain the lower level and name the
missing evidence.

## Agent-Native Design

Design for system comprehension:

- make canonical sources, scope, permissions, state, and stop conditions
  directly discoverable
- expose real commands and contracts instead of prose approximations
- separate stable context from volatile state and currentness evidence
- prefer structured indexes and references over duplicated narrative
- make deterministic failures machine-readable and actionable
- preserve enough rationale for a human to exercise oversight and veto
- optimize canonical artifacts for agent routing and execution; keep human
  README and reference material as projections rather than the control plane

Do not reproduce human ceremony merely because it is familiar. Preserve
security, accessibility, product quality, maintainability, auditability, and
human accountability even when the implementation shape changes.

## Review Architecture

Use reviews when they can change an action:

| Loop | Trigger | Reviewer | Evidence and action |
|---|---|---|---|
| Work self-review | Significant change before completion | Implementing agent plus deterministic checks | Scope, diff, Fast Check; fix or report |
| Independent review | High coupling, material risk, integration, or weak failure detection | Fresh-context agent, preferably isolated | Findings tied to code, policy, tests, or sources |
| Harness review | Repeated friction, harness change, stale owner, or failed instruction | `agent-sync` or an independent agent | Keep, change, remove, or supersede |
| Currentness review | Volatile fact affects model, cost, feature, tool, or Golden Path choice | Research worker using `CURRENTNESS.md` | Refresh evidence or block the decision |
| Autonomy review | Broader permissions, blast radius, repositories, or oversight mode | Capable parent, independent critic, and human where required | Prove controls or retain the lower level |

Do not require multiple model reviews for trivial, reversible, well-checked
work. Correlated reviewers add cost without independence; change context,
evidence, model family, or review method when independence matters.

## Human Oversight

Keep a human in the loop when intent, semantics, authority, trade-offs, or
material risk remain unresolved.

While a workflow is human-in-the-loop, present each material branch as two or
three options, including no change when meaningful. State evidence, trade-offs,
reversibility, blast radius, and a recommendation. The human may veto any
option; do not execute the dependent branch without explicit acceptance.
Routine reversible maintenance remains autonomous within documented authority.

Propose human-on-the-loop only when:

- scope, ownership, and permissions are explicit
- inputs, outputs, and stop conditions are stable
- tests or evals detect meaningful failure
- state, retry, recovery, and rollback exist where needed
- observability and auditability make intervention possible
- repeated bounded runs provide evidence

Human-on-the-loop supervises outcomes and exceptions. It does not remove
accountability or decision rights.

For an active promotion candidate, define one bounded change or risk class and
its exclusions. Use the target's existing workflow-state owner as the promotion
index and summary; link checks, reviews, audit logs, incidents, and other
evidence from their authoritative owners instead of copying them. Each
qualifying run records its durable change and check result, declared class and
scope, recovery or rollback evidence, and outcome. A run that changes a gate
counts only after fresh-context critique and a negative proof that the gate
catches the failure it owns.

After at least two successful runs in the same declared class, including an
exercised recovery or rollback path, run the autonomy review only when the runs
also cover the class's declared variability and meaningful failure modes. Two
runs are a floor, not a general readiness threshold; require more when coverage,
risk, or failure impact warrants it. If every gate is complete, present the
accountable human one immediate promote-or-hold decision. Promotion applies
only to the demonstrated class. A breach, unobservable failure, failed recovery,
or unresolved material decision immediately returns the workflow to
human-in-the-loop, records the hold reason, and resets its evidence before any
new promotion run.

## Cross-Repository Harness

### Topology Selection

| Topology | Use when | Minimum coordination | Avoid |
|---|---|---|---|
| Single repository | One repository owns the behavior and its checks | Local `AGENTS.md`, real checks, local context and learning owners | A coordinator, copied policy, or organization tooling |
| Multiple repositories | Durable provider/consumer relationships, shared workflow state, or integration checks span repositories | Member entrypoints, context map, public contracts, compatibility checks, sync/write-back | Moving member-local truth into the coordinator |
| Multiple teams | Decision rights and delivery ownership cross team boundaries as well as repositories | Team/context owners, versioned shared policy, contract and risk owners, cross-team evals, escalation | Treating the central harness as universal domain or product authority |

Topology and autonomy are independent. Every repository needs safe session
discovery, including experiments; higher autonomy still requires local checks,
permissions, recovery, observability, and evidence.

Each repository owns its local architecture facts, commands, decisions,
checks, instructions, and implementation state.

A coordinating harness may own:

- the cross-repository context map (members, remotes, checks, relationships)
- public integration contracts and compatibility ranges
- provider, consumer, and owner relationships
- shared Golden Paths and versioned Skills references
- cross-cutting evals and release evidence
- workflow state (`STATUS.md`), recovery, isolation, and auditability
- member discovery / write-back protocol (thin `AGENTS.md` pointers + sync doc)
- oversight and autonomy policy for the coordinated system

Minimum coordinating baseline (add only what evidence needs, but do not omit
discovery or session survival):

| Concern | Typical owner |
|---|---|
| Agent entry | `AGENTS.md` |
| Oversight / autonomy | `HARNESS.md` |
| Shared terms | `CONTEXT.md` |
| Members / relationships | `CONTEXT-MAP.md` |
| Discovery + write-back | sync protocol + member `AGENTS.md` pointers |
| Mid-flight cross-repo work | `STATUS.md` |
| Durable lessons | `LEARNINGS.md` |
| Human map / cycle | `README.md` |
| Coordinator verify | real Fast Check / Full Gates |

The Skills catalog is a capability supplier. It must not become the
coordinating control plane for target product or private-system work. Edit
Skill source files in the catalog; decide multi-member Skill placement and
system policy in the coordinator.

### Skill and Policy Sources

Keep source ownership explicit across layers:

- public upstream: portable methods, releases, provenance, public compatibility
- private organization or team catalog: shared non-public procedures, approved
  pins, internal adapters, and organization controls
- private coordinator: membership, policy, placement, compatibility, and
  cross-repository evidence
- project repository: local semantics, commands, wrappers, project-only Skills,
  checks, and permissions
- user or global scope: small discovery and maintenance bootstrap only

These layers form a dependency and authority graph, not a universal filesystem
precedence. Inspect the active host. Project-local semantics outrank generic
procedure text; managed private or public content stays pinned and separate
from local wrappers. Select one owner per workflow and do not copy portable
source into a coordinator merely because several members consume it.

The coordinating harness never overrides repository-local instructions or
promotes inferred product semantics into shared truth.

Member sessions should load coordinator oversight (for example by requiring a
read of coordinator `HARNESS.md` from a Private system section) so autonomy
policy is consistent without copying the full harness into every member.

For demand-driven sibling and multi-team relevance (SYNC -> CONTEXT-MAP match,
named-owner rule, stay local on no match), follow the portable walkthrough in
[`MULTI-REPO-HARNESS.md`](../../../MULTI-REPO-HARNESS.md) under **Find
Sibling Scope and Decide Relevance**. Keep one coordinator inventory; do not
copy membership into every member.

Prefer ASCII punctuation in harness prose. Routine commit/push when checks
pass is normal completion when the owner authorizes that policy; ask only for
critical git or irreversible external effects.

When membership, sync, autonomy, or the cycle changes, update the human
`README.md` in the same loop if a new reader would otherwise misunderstand the
system.

Use a capable parent agent to frame work, select workers, manage dependencies,
integrate evidence, and own the final result. Give each worker a bounded
contract: inputs, repository, permissions, model budget, expected output,
verification, and stop condition.

Delegate only when work is meaningfully independent. Prefer isolated branches
or worktrees when supported. Use cheaper workers for bounded retrieval,
mechanical transformation, and checks with strong verification; retain capable
models for ambiguous design, security, high coupling, and final synthesis.
Cross-repository completion requires public contract and compatibility checks,
not only green local tests.

### Multi-Team Federation

For each participating team or role, record:

- owned bounded contexts, repositories, services, and decision classes
- public provider/consumer contracts and compatibility responsibility
- who may change shared policy, accept risk, approve release, or widen autonomy
- team-local Fast Check and Full Gates plus cross-team integration evidence
- escalation path for semantic conflict, contract breakage, security, incident,
  and competing priorities
- version and rollout policy for shared Skills, templates, rules, and controls

The coordinator owns relationships and shared evidence, not every team's
backlog, implementation plan, or domain model. Prefer asynchronous Git-owned
contracts and checks over recurring synchronization meetings. Use a software
catalog or policy engine only after scale creates an observed discovery or
enforcement failure.

## Artifact Test

Before adding an artifact, answer:

1. Which observed problem does it solve?
2. Why is an existing artifact or native control insufficient?
3. Is the behavior probabilistic or deterministic?
4. Who owns the truth?
5. What verifies the expected effect?
6. When should the artifact be removed or superseded?
7. Which source and re-check trigger keep volatile claims current?
8. Does this duplicate or conflict with an installed workflow or style profile?
9. What authority, freshness, standing context load, or output-routing layer
   does it add?
