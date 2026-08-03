# Agentic Engineering Harness

## Operating Level

Current default: reliable repository-level work. Add wider delegation only
from observed evidence.

## Stewardship

Harness stewardship is part of every agent task:

```text
Observe -> Diagnose -> Route -> Change -> Verify -> Keep / Change / Remove
```

Improve a reversible owning artifact without waiting for a separate prompt.
Leave the harness unchanged when no observed problem justifies a change.

After every significant task, and before claiming done, agents must ask and
answer in the same loop:

1. **Manifest here?** Should this evidence become or update a hard owner in
   this repository's harness (`HARNESS.md`, `AGENTS.md`, checks, Hook, Skill,
   STATUS, LEARNINGS)? Prefer a hard adaptation when the same mistake would
   otherwise recur. Explicit no-change is valid when the signal is transient.
2. **Port to future harnesses?** If the lesson is portable (not product-
   private), also update the owning catalog artifact - typically
   `scaffold-harness` templates or `agent-sync` - so the next scaffolded
   harness inherits it from day one. Do not leave portable harness rules only
   in one live repository.
3. **Fan-out live members?** If this repository coordinates members, follow
   the fan-out checklist in `SYNC.md`: pointer-only policy needs no sibling
   edits; discovery/snippet changes refresh every listed member, including
   experiments, in the same
   loop. Parent sessions own fan-out after subagents.
4. **Siblings in view?** Keep the member map truthful; admit or graduate new
   siblings via `SYNC.md`; coordinator verify should fail on unlisted
   repo-like siblings or missing mapped members.
5. After changes to purpose, autonomy, working roots, git hygiene, or the
   harness cycle: does the human `README.md` still teach a new reader?

## Git Working Tree Hygiene

Applies to every repository an agent edits. Goal: cheap start gates and
session-owned cleanup - not worktree religion, not auto-reclaim of foreign
state.

### Before editing

1. Run `git status --short --branch` and, when available, `git worktree list`.
2. Note dirty paths, current branch, and existing worktrees.
3. If the tree is dirty or unexpected worktrees exist: report them. Do not
   silently overwrite unrelated WIP. Ask when ownership of the dirt is unclear.
4. Prefer the host's native isolated workspace when isolation is needed. Fall
   back to a project-local git worktree under an ignored `.worktrees/` (or
   existing project convention) only when parallel, long-lived, or risky work
   needs a clean baseline, or when the primary checkout is dirty and must not
   be touched.
5. Do not create a worktree for every trivial edit. Do not nest worktrees. Do
   not fight an already-isolated host workspace with a second `git worktree add`.

### On finish (this session's footprint)

1. Integrate ready work via the repository's commit/push or PR policy. When
   that policy authorizes routine commit/push, perform it after checks pass
   without asking again. Do not force-merge onto a shared branch as ceremony.
2. Remove worktrees **this session created** after successful integrate or
   confirmed discard; then `git worktree prune`. Prefer cleanup from the main
   checkout, not from inside the worktree being removed.
3. Never auto-delete worktrees this session did not create. List orphans; ask
   the human before reclaim - there is no reliable cross-session lock proving
   "no other agent is using this."
4. Leave the repository no worse for your own artifacts than you found it.

## Agent-Native Design

Optimize sources, contracts, state, and checks for reliable agent navigation.
Canonical artifacts are designed for agents first: explicit ownership,
machine-discoverable routes, executable commands, bounded context, structured
state, and actionable failures. Human README and reference views explain the
system without forcing agent workflows to imitate human ceremony. Human review
surfaces stay legible and no agent-facing mechanism may hide risk, authority,
or rationale.

## Language Contract

Communicate with each human in their preferred collaboration language. Infer it
from explicit preference or conversation evidence; if still unclear, ask once
and retain it in user-scoped or untracked state unless it is shared repository
policy.

Write persistent repository artifacts in US English unless the human explicitly
requests another language for a named artifact. The language used in chat does
not implicitly change code, documentation, schemas, prompts, tests, commits, or
other persisted output.

## Host Portability

Keep canonical semantics in host-neutral repository owners. Use root
`AGENTS.md` plus thin `CLAUDE.md`, `GEMINI.md`, and Antigravity bridges as the
portable interactive baseline; Codex, Cursor, and Pi load `AGENTS.md`
directly. Discover each active host's effective Skill, plugin, Rule, Hook, MCP,
permission, model, and isolation behavior. Add other adapters only for hosts
the target actually uses, reference canonical owners instead of copying
policy, verify precedence and behavior per host, and remove stale adapters.

Non-interactive CI or agent runtimes require a bounded workload contract, least
privilege, secrets policy, cancellation, deterministic gates, telemetry, and
retained evidence. A framework such as Flue is optional and must pass the
runtime gate in the active `scaffold-harness` `RUNTIMES.md` reference.

## Repository and Team Topology

Use the smallest topology that matches actual ownership:

- A single repository owns its instructions, context, checks, and learnings.
- A multi-repository coordinator owns relationships, public contracts, shared
  workflow state, oversight, and integration evidence, never member-local truth.
- A multi-team coordinator additionally records team/context decision rights,
  contract and risk owners, cross-team compatibility checks, shared-policy
  versions, and escalation paths. It does not become every team's product or
  domain authority.

Every listed repository, including an experiment, has a local agent entrypoint
and safe coordinator fallback. Session discovery is mandatory; unattended
autonomy remains separately gated by local evidence.

## Progressive Product Engineering

Product work is a closed learning loop, not a specification -> implementation
-> testing -> deployment handoff. Route end-to-end work through
`run-product-engineering` and the target's local craft Skills.

- Evolve ubiquitous language, bounded contexts, examples, contracts, tests, and
  code together; do not freeze a complete domain model up front.
- Shift quality, security, privacy, accessibility, compliance, operability,
  telemetry, and recovery into framing and every implementation slice.
- Mark prototypes and technical spikes as bounded learning work. Discard them
  or make an explicit production investment; never promote them silently.
- Use vertical TDD for production behavior and feed bugs, incidents, adoption,
  control effectiveness, cost, and outcome evidence back into triage.
- Express behavioral tests with Given/When/Then semantics using the target
  framework's normal structure. Do not require comments or a GWT library.
- Keep UIs thin and use task-shaped reads plus intent-shaped mutations when
  they expose the domain more clearly than persistence-shaped CRUD. Treat
  architecture styles, languages, frameworks, and databases as context-bound
  tools; settle consequential uncertainty with bounded representative spikes.
- For product work that uses shared investment or issue tracking, at any level,
  keep an outcome-oriented Now/Next/Later/Never investment view. Horizons are
  not dates; keep Later coarse, record Never with rationale and a revisit
  trigger, and create decision or delivery issues only for sharp Now or Next
  work. Raw intake records may remain without becoming commitments. The level
  determines who maintains and approves these decisions, not whether the
  semantics apply.
- Prefer Git-owned decisions, controls, and generated evidence. Preserve any
  official form or assurance path required by the applicable authority.
- Keep repeatable infrastructure desired state in version control and route
  changes through reviewable plans, policy checks, protected state, controlled
  apply, drift detection, runtime verification, and credible recovery. Name
  GitOps, GitOps-near, or bounded IaC honestly; do not add a controller only to
  improve the label.
- Encode stable enforceable controls as tested policy close to their inputs and
  enforcement point. Named humans retain interpretation, scope, risk acceptance,
  exceptions, and assurance claims.

## Shared Understanding and Grilling

- Start significant work by aligning outcome, scope, non-goals, authoritative
  sources, decision rights, assumptions, unknowns, checks, stop conditions,
  and recovery.
- Investigate discoverable facts and test bounded reversible hypotheses before
  asking a human.
- Use `grill-harness-with-docs` when intent, semantics, authority,
  consequential trade-offs, or material risk remain unresolved.
- Close with the same frame so another human or agent can independently state
  what is true, what changed, why it is complete, and what remains open.

## Review Loops

- Select and run the applicable review loop without asking the human to choose
  the reviewer; human escalation remains governed by `AGENTS.md` boundaries.
- Self-review significant work and run the relevant deterministic checks.
- Use fresh-context independent review for every resolved material decision or
  change, including public methods and Skill semantics.
- Review the harness after repeated friction or a harness change.
- Refresh volatile model, pricing, platform, or community evidence when a
  decision consumes it or an active adapter no longer matches observed host
  behavior. Expiry marks evidence stale; it does not trigger research alone.
- Review controls and human oversight before expanding autonomy or blast radius.
- Treat dependency-bot PRs (Renovate or similar) as evidence-gated merges - never
  merge on green CI alone. See **Dependency bot PRs** below.

Route subagents by task evidence, not by the parent's model. Use the least
expensive current model that passes representative work for the role; reserve a
frontier model for ambiguous integration, consequential decisions, or material
review. Count retries, review, latency, and failure impact in total cost. Keep
provider-specific aliases and checked dates in `ORCHESTRATION.md` or a thin
host adapter. Maintain one adapter for every active host that can route models;
Codex configuration is not a substitute for Claude Code, Cursor, Gemini CLI,
Pi, CI, or later host controls. Re-evaluate a route when a model, alias,
allowlist, plan, price, host fallback, or representative quality result changes.
New models enter a measured candidate lane before they replace a proven route.
Before the first delegated task in a session, resolve the active host adapter.
If it is absent, stale, or unenforceable, inspect the live controls and either
refresh the adapter or keep the task with the capable parent.

Every review ends with keep, change, remove, supersede, rebuild, or no action.

### Dependency bot PRs

When Renovate (or a similar bot) opens a dependency PR, do not silent-merge and
do not silent-ignore:

1. Inspect the version jump against this repository's usage (changelog, release
   notes, breaking changes that affect call sites here).
2. Run the relevant Fast Check / Full Gates. Add a feature-level smoke when the
   bump touches runtime behavior.
3. Merge only with evidence the jump is safe for this repo.
4. If not merging (major, risk, red CI, unclear impact, or deliberately
   deferred): leave a clear PR comment with rationale and unblock criteria.

Supply-chain cooldowns (`minimumReleaseAge` and related Renovate settings) are
config, not a substitute for this review.

Use the latest supported stable LTS runtime line where the ecosystem offers
one; use the current stable release otherwise. Pin exact versions, action
commits, and image digests where reproducibility or supply-chain integrity
requires it, then let the configured dependency bot propose updates after its
routine cooldown. Security updates bypass routine cooldowns. A deprecation or
forced-runtime annotation is a currentness failure: update the owning action,
runtime, or adapter instead of suppressing the warning.

A future LTS candidate may run in a separate preview lane before promotion.
Keep that lane non-production and non-blocking unless the repository explicitly
accepts the risk. Promote it only after upstream marks the line LTS, the used
ecosystem passes representative checks, and the normal cooldown has elapsed.

## Uncertainty

- Investigate discoverable facts from repository and primary sources.
- Run a bounded experiment for a reversible low-risk hypothesis.
- Use `grill-harness-with-docs` for unresolved intent, authority, trade-offs,
  product semantics, architecture, governance, or material risk.
- Implement only resolved branches.

## Oversight

Keep consequential workflows human-in-the-loop until scope, permissions,
checks or evals, recovery, rollback, observability, and repeated evidence
support a confirmed human-on-the-loop transition.

For a material human-in-the-loop branch, present two or three options,
including no change when meaningful, with evidence, trade-offs, blast radius,
reversibility, and a recommendation. The human may veto the branch.

For each active promotion candidate:

1. Name one bounded change or risk class, its owner, and its exclusions.
2. Make the smallest missing promotion gate part of each qualifying run.
3. Use the existing workflow-state owner as the promotion index. Record the
   durable change and check result, scope, recovery, and outcome there while
   linking authoritative checks, reviews, audit logs, and incidents.
4. Do not let a gate-changing run count until fresh critique and a negative
   proof show that the gate catches the failure it owns.
5. After at least two successful runs in the same class, including an exercised
   recovery or rollback path, run the autonomy review only when the evidence
   covers declared variability and meaningful failure modes. Two runs are a
   floor; require more when coverage or risk warrants it.
6. Present a ready promote-or-hold decision immediately. Promote only the
   demonstrated class; retain human veto, incident authority, and accountability.
7. On a boundary, observability, or recovery failure, immediately return the
   workflow to human-in-the-loop, record the hold reason, and reset its evidence
   before any new promotion run.

## Currentness

Do not freeze volatile model catalogs, prices, or platform features here.
Discover the live environment, consult current official sources, test
representative tasks, and record a check date plus re-check trigger only when a
durable routing decision exists. Expired evidence becomes stale and is refreshed
when a decision or active adapter consumes it; adapter mismatch is an immediate
trigger. Every significant harness review may keep, change, remove, supersede,
or rebuild an owner; preserve no structure merely because it already exists.

Keep update automation configured for every dependency ecosystem actually in
use. Cooldowns reduce fresh-release risk but do not justify unattended merges:
inspect the jump, run the repository gates, then merge or record why it is
deferred.

## Agent Context Architecture

Optimize cost, latency, and risk per correctly completed task. Retrieve the
smallest authoritative source, process large raw output outside the active
context when supported, load branch-specific reference only when needed, and
pass bounded evidence rather than chat transcripts.

Treat the applicable repository agent instructions, including any nearest
scoped instructions, as the only unconditional repository payload. Load README,
harness, context, status, learning, template, and Skill owners only when the
active branch needs them; route to a section or query before reading a full
large file.

Keep stable session-critical routing and truth local. Use MCP for required live
information or external actions; it does not replace source authority,
freshness, persistence, or context selection.

Use one filtering or compression owner per data path. Add a new layer only for
a measured problem and keep it only when representative tasks preserve quality,
retrieval, privacy, routing, and recovery.

During stewardship, re-check whether discovery, memory, or context-economy
tools (Graphify-class indexes, Headroom, Context Mode, episodic memory, and
similar) should start, stay parked, or be removed. Prefer Git owners first.
Follow the installed `scaffold-harness` capability gate when present.

## Ownership

| Concern | Owner |
|---|---|
| Agent behavior and scope | `AGENTS.md` |
| Domain language | `CONTEXT.md` |
| Source routing | `CONTEXT-MAP.md` |
| Git working-tree start/finish hygiene | `HARNESS.md` (Git Working Tree Hygiene) |
| Accepted trade-offs | ADR |
| Durable observations | `LEARNINGS.md` |
| Repeated probabilistic procedure | Skill |
| Portable future-harness defaults | upstream `scaffold-harness` / `agent-sync` |
| Deterministic enforcement | Test, Hook, CI, or platform control |
| Infrastructure desired state and drift | Target infrastructure repository and platform owners |
| Compliance scope and policy semantics | Target ISMS or GRC system and named control owners |

Reference the owner instead of duplicating its content.

## Goal-Driven Skill Routing

- Infer the outcome and current lifecycle stage; users do not need to name
  Skills.
- Select one owning Skill and only the complements needed for the current
  stage.
- Use managed `write-a-skill` as the portable owner for Skill creation and
  revision. Host-native creators, commands, and plugins are adapters only;
  verify discovery independently for every declared host.
- Resolve target semantics from project-local Skills or wrappers, then use the
  explicitly managed private organization, team, or public dependency. Keep
  installed user or global Skills to the small bootstrap and discovery role.
  Inspect the host's actual load precedence separately.
- Keep project semantics local, organization procedures in their private
  catalog, portable methods in their public upstream, and only the small
  bootstrap global. A coordinator owns placement and policy, not every Skill's
  source text.
- When a required public complement is missing, verify its source,
  technology-version fit, permissions, maintenance, license, and overlap.
  Install it project-locally only when harness changes are authorized, then
  use it in the same loop.
- Use an installed upstream `find-skills` or `npx skills find` when no named
  complement fits. Popularity is only a discovery signal.
- Select one owner for each workflow. Do not stack overlapping planning, TDD,
  debugging, review, or style profiles by default.
- Do not vendor public Skill text unless a distinct local delta and attribution
  justify the maintenance cost.

Use a current capable parent model for framing, integration, and consequential
judgment. Cheaper workers must first pass representative checks for their
bounded task. If no suitable model is available, reduce scope or autonomy
instead of retrying low-quality output.

Prefer an existing implementation, native capability, or installed dependency
before adding code or another layer. Never simplify away validation at trust
boundaries, security, accessibility, data integrity, recovery, or necessary
error handling.
