---
name: agent-sync
description: Proactively evolves repository harness artifacts, review loops, currentness, and agent routing across sessions and tools from durable evidence. Use when starting or completing a session, after toolchain, model, pricing, or domain changes, when repeated friction reveals missing context or checks, or when instructions, orchestration, Skills, Rules, Hooks, MCP, or learnings may be stale.
---

# Agent Sync

Learning lives in Git-tracked owning artifacts, not chat history.

## Project Fit

1. Read the applicable instruction hierarchy and context routing.
2. Map local equivalents before introducing preferred filenames.
3. Use existing sources of truth and preserve repository conventions.
4. Run **scaffold-harness** when the repository lacks a reliable baseline.
5. Establish shared understanding for significant work. Use
   **grill-harness-with-docs** for unresolved material decisions in any topic.

## Session Start

Read only what the task needs:

- agent instructions and harness contract
- the current human's preferred collaboration language from explicit or
  conversation evidence; ask once only if unclear, and keep personal preference
  in user-scoped or untracked state unless it is shared policy
- the active host and effective instruction, Skill, plugin, Rule, Hook, MCP,
  permission, model, and isolation precedence needed by the task
- relevant context map, domain context, status, ADRs, and recent learnings
- Skills explicitly triggered by the task
- the managed `write-a-skill` owner before Skill creation or revision, plus
  only the active host's native authoring adapter when needed
- actual Fast Check and Full Gates
- volatile model, pricing, platform, or Golden Path evidence only when the task
  depends on it

Do not re-derive conventions already owned by an artifact.

## Stewardship During Work

Harness stewardship is part of every significant task. Notice repeated
friction, missing or stale context, weak feedback, unclear ownership,
unnecessary ceremony, and recurring workflows.

Keep canonical artifacts agent-first and host-neutral. Human README and
reference material are legible projections, while thin host adapters reference
the owning instructions, context, state, and contracts. Communicate in the
human's preferred language; keep persistent repository artifacts in US English
unless a named artifact is explicitly requested otherwise.

Follow the repository's owned voice or style guide. Without one, keep prose
direct and concrete: lead with the problem or working model, name trade-offs
and system effects, and remove generic hype, defensive setup, and text that
changes no decision or action.
Reserve first person for artifacts that explicitly speak for the repository
owner. Keep agent instructions and operating procedures neutral and imperative.

Diagnose before changing. Update the smallest owning artifact when evidence
justifies a reversible in-scope improvement. Leave the harness unchanged when
no durable signal exists.

When a recurring bounded workflow has a justified human-on-the-loop target,
make the smallest missing promotion gate part of each qualifying run. Keep the
promotion index in the target's existing workflow-state owner and link each
authoritative check, review, audit, incident, and outcome record. A run that
changes a gate cannot certify itself: require fresh-context critique and a
negative proof for the failure that gate owns. Once the evidence covers
repeated runs in one declared class, its variability and meaningful failure
modes, recovery, observability, outcomes, and veto, present the accountable
human one immediate promote-or-hold decision.

Route a repeated missing-stack failure through `update-harness`: reuse an
existing project, private, public, bundled, or plugin profile, or pilot an
approved current public candidate first. Use `write-a-skill` for the smallest
project-local profile only when repeated work supplies real examples and
checks. One-off stack work stays direct work.

Do not return an authorized routine decision to the human as a confirmation
question. Close it through the repository policy and available evidence, or
escalate a named conflict, authority gap, or material risk.

Before claiming done, ask and answer in the same loop:

1. **Manifest here?** Does this evidence belong in the current repository
   harness owner (`HARNESS.md`, `AGENTS.md`, checks, Hook, Skill, STATUS,
   LEARNINGS)? Prefer a hard adaptation when the same mistake would recur.
2. **Port within your authority?** After every harness change, decide in the
   same loop whether a generalized portable variant belongs in a catalog you
   own or are authorized to change. If yes, update that owner without waiting
   for a separate prompt - typically that catalog's `scaffold-harness`
   templates or this Skill. Do not push, open a pull request, or otherwise
   write back to an external public upstream you only consume - including
   `https://github.com/ldaume/agentic-engineering-harness` - unless you are
   that upstream's maintainer with explicit write authority for this change.
   Explicit no-port is valid when the change is target-private or when you
   have no owned shared catalog - harden locally instead; still never write
   back to a foreign public upstream. Ask only when placement is ambiguous or
   a port would leak private authority.
3. **Fan-out live members?** If a coordinator `SYNC.md` fan-out checklist
   applies: pointer-only policy needs no sibling edits; discovery/snippet
   changes refresh every listed member Private system section, including
   experiments, and must pass Full Gates. Parent sessions own fan-out after
   subagents.
4. **Siblings in view?** On coordinator work, keep `CONTEXT-MAP.md` aligned
   with repo-like siblings; admit or graduate via the coordinator admit
   checklist. Unlisted siblings are a verify failure.
5. After a change that alters purpose, membership, sync, autonomy, working-root
   rules, git hygiene, or the harness cycle: does the human `README.md` still
   teach a new reader the current human and agent roles by product phase and
   operating level, technical controls, engineering method, rationale, and
   evidence needed for wider delegation?

## Event-Triggered Review Loops

Run only loops that can change the next action:

1. **Work review:** self-review significant changes and run deterministic checks.
2. **Independent review:** use a fresh-context agent for every resolved
   material decision or change, including public methods and Skill semantics.
   Give it the shared-understanding frame, authoritative sources, diff or
   proposal, checks, and non-goals. Use an installed upstream `code-review`
   Skill when it owns the review procedure. Run the selected review directly;
   do not ask the human whether to spawn a reviewer.
3. **Harness review:** assess ownership, duplication, effectiveness, blast
   radius, and removal after harness friction or change.
4. **Currentness review:** use
   [`../scaffold-harness/CURRENTNESS.md`](../scaffold-harness/CURRENTNESS.md)
   when volatile model, cost, feature, tool, or community evidence affects a
   decision or an active adapter no longer matches observed host behavior.
   Keep stable task tiers separate from replaceable provider models. A new,
   deprecated, unavailable, repriced, or behaviorally changed model triggers a
   representative candidate evaluation and an update to every affected active
   host adapter - Codex, Claude Code, Cursor, Gemini CLI, Pi, SDK, CI, or a later
   host - rather than a Codex-only rename. Expired evidence is stale but
   triggers research only when consumed. The result may keep, change, remove,
   supersede, or rebuild the affected harness owner.
5. **Capability gate:** use
   [`../scaffold-harness/CAPABILITY-GATES.md`](../scaffold-harness/CAPABILITY-GATES.md)
   when sessions lose continuity, re-explore code wastefully, flood context,
   miss cross-repo relationships, or tempt a new memory/graph/compression
   product. Prefer Git owners first; add tools only for an observed failure
   mode with authority, scope, pilot, and exit path.
6. **Autonomy review:** require controls, independent critique, and the
   applicable human decision before increasing delegation or oversight mode.
   Promote only the evidenced change or risk class. After a scope breach,
   unobservable failure, failed recovery, or unresolved material decision,
   immediately return it to human-in-the-loop, record the hold reason, and
   reset its evidence before any new promotion run.
7. **Dependency bot PR:** when Renovate (or similar) opens an update PR, inspect
   the version jump for this repo's usage, run Fast Check / Full Gates (plus
   feature smoke if runtime behavior is touched), and merge only with safety
   evidence. If not merging, comment with rationale and unblock criteria - never
   silent-merge or silent-ignore. See harness **Dependency bot PRs**.

Every loop ends with keep, change, remove, supersede, rebuild, or explicitly no
action.
Do not create review artifacts when the result is transient and changes no
future behavior.

## Route Durable Evidence

| Signal | Owning mechanism |
|---|---|
| New or changed commands, scope, permissions | Agent instructions |
| Domain term or invariant | Domain context |
| Source, context, or repository relationship | Context map |
| Harness oversight or evolution rule | Harness contract |
| Portable harness default for future scaffolds | Catalog you own or are authorized to change (`scaffold-harness` templates and/or this Skill there); never a foreign public upstream you only consume |
| Live member discovery / snippet fan-out | Coordinator `SYNC.md` + `MEMBER-AGENTS-SNIPPET.md` |
| Git working-tree start/finish hygiene (branch gate, worktree default, ordinary names, leases, cross-agent non-interference) | Harness contract (Git Working Tree Hygiene); ADR when accepted |
| Dependency-bot PR merge or defer | Harness contract (Dependency bot PRs) + PR comment |
| Repeated model, worker, budget, or review routing | Orchestration policy |
| Current workflow or engagement state | Status document |
| Accepted consequential trade-off | ADR |
| Repeated probabilistic workflow | Skill |
| Portable Skill authoring behavior | Managed public `write-a-skill`; native host creator stays an adapter |
| Scoped behavioral guidance | Rule or agent instruction |
| Deterministic event or enforcement | Hook, CI, test, platform control |
| Portable public method or default | Public Skill or scaffold upstream only when you maintain that upstream; otherwise keep the method local or in your owned catalog |
| Shared non-public organization or team procedure | Private Skill catalog |
| Durable evidence-backed observation | Learning log in the owning repository |
| Cross-repository membership, contracts, coordinator policy | Coordinating repository owners (map, harness, learnings) |
| Member-local product or ops observation | That member's owners; create `LEARNINGS.md` lazily |
| Human understanding of purpose, cycle, or where to work | Human `README.md` in the owning or coordinating repo |

Route a lesson once by audience and authority. Portable practice belongs in a
catalog you own or are authorized to change; do not write it back to a foreign
public upstream you only consume. Shared confidential procedure belongs in the
private catalog; cross-repository relationship or policy belongs in the
coordinator; product, domain, service, or sensitive truth belongs in its local
owner. Reference that owner from consumers instead of copying the lesson.

Prefer a hard adaptation of the owning artifact when the lesson is a rule.
Use a learning entry when evidence should survive sessions but is not yet
stable enough to hard-code. Do not copy the same learning into every consumer.

Reference the owner instead of copying its content into consumers.

## Verification

1. Run the smallest relevant checks for changed artifacts.
2. Verify referenced local paths and commands.
3. Review the diff for duplicated, stale, speculative, or unowned layers.
4. Consolidate or supersede prior learnings instead of appending duplicates.
5. State what changed, why, and the next re-check condition.
6. Close the git integration loop for this session's ready work: commit and
   push when authorized; when repository policy makes merge the default (or
   otherwise authorizes it) and this session opened a PR/MR with green
   required checks and no conflicts, merge it through the normal path before
   claiming done. If policy disallows merge, record a named blocker instead.
   Do not leave mergeable session-owned PRs for a human reminder when merge
   is authorized. Do not force-merge past red required checks or over foreign
   WIP.

For volatile decisions, confirm the source, check date, live environment, and
expiry or event trigger. Re-run representative evals before routing a task
class to a cheaper worker.

## Do Not Persist

- one-off debugging and ticket chatter
- raw chat or temporary task state
- rules already enforced by a native config or deterministic control
- unverified product, architecture, ownership, or security assumptions
- a new artifact without an observed problem and owner

The sync is complete when durable evidence is routed, relevant checks pass,
uncertainty is explicit, authorized session-owned ready PRs/MRs are merged or
a named blocker is recorded (including policy-disallowed merge), and no
further harness change is justified by the current work.
