# Skills Repository Harness

## Purpose

This repository is the versioned source for portable agent Skills and harness
blueprints. It self-hosts the lifecycle used to audit, build, and evolve
harnesses elsewhere without becoming the source of truth for those targets.

## Operating Level

The default target is reliable L3 repository work with targeted L4 grounding.
Use bounded L5 workflows only for repeated skill packaging, installation, and
verification when state, retry, recovery, and checks are explicit.

Do not infer L6 or L7 authority from agent capability. Broader delivery or
product autonomy belongs in the affected system and requires its own controls,
evidence, ownership, and oversight decision.

## Autonomous Stewardship

For every significant task:

1. Observe friction, stale guidance, duplicated truth, missing checks, and
   repeated procedures.
2. Diagnose the owning artifact and whether a change would alter future work.
3. Make the smallest reversible in-scope improvement when evidence is clear.
4. Run the smallest relevant check and any required skill install test.
5. Keep, change, remove, or supersede the mechanism based on the result.
6. Route durable evidence to `LEARNINGS.md`; do not wait for a separate prompt.
7. Ask and answer, in the same loop, without waiting for the human:
   - Does the human `README.md` still explain purpose, cycle, and where to
     work after this change?
   - Should this lesson manifest as a hard harness owner here?
   - If portable, must `scaffold-harness` templates / `agent-sync` also change
     so future harnesses inherit it from day one?
   - Is this catalog still not acting as another system's control plane?
   - Is tracked text still ASCII-punctuation-clean?
   - Did repeated friction show a context/memory/discovery failure that
     `scaffold-harness/CAPABILITY-GATES.md` would promote, park, or reject
     (Graphify, Headroom, Context Mode, episodic memory, and similar)?

Leave the harness unchanged when the signal is transient or speculative.

## Git Working Tree Hygiene

Inspect `git status` and worktrees before edits; isolate only when needed;
clean up session-owned worktrees; never auto-delete foreign work or orphans.
The reusable baseline lives in
`skills/engineering/scaffold-harness/templates/HARNESS.md`.

## Always-On Skill Quality

Whenever work touches a Skill, packaging, repository instructions, or the
harness itself:

1. Run `python3 scripts/audit-skills.py` before editing so existing drift is
   visible.
2. Read the affected Skill, `write-a-skill`, and relevant `LEARNINGS.md`
   entries.
3. Inspect what static validation cannot prove: activation scope, near misses,
   behavior-neutral prose, premature completion, conditional reference loading,
   overlap with public upstream Skills, and whether changed prose passes
   `VOICE.md` without losing technical precision.
4. For a new or materially changed Skill, refresh the relevant public
   catalogs and run `scripts/audit-skill-provenance.py` against their checked-out
   roots.
5. Improve the smallest owner when evidence is clear; reference an upstream
   Skill instead of vendoring it.
6. Re-run the audit and the required install or execution checks before
   completion, then persist any durable change in future behavior.

This loop is implicit repository work. It does not require a user to request a
Skill or harness review.

## Goal-Driven Skill Routing

Agents select the smallest useful loop from the goal; users do not need to name
Skills:

1. Infer the intended outcome, current lifecycle stage, risk, authority, and
   observed maturity.
2. Start with `README.md`'s common development loops and the Skill descriptions.
   Select one owning local Skill and only the complementary Skills needed for
   the current stage.
3. Resolve Skills from the effective project scope, then installed user or
   global scope, then trusted public sources. Respect the host's actual
   precedence rules.
4. When the selected loop needs a referenced public complement, verify its
   source, technology-version fit, permissions, and installed version. Install
   it project-locally when harness changes are authorized, then use it in the
   same loop. Do not silently claim an uninstalled Skill was applied.
5. When no named complement fits, use an installed upstream `find-skills` or
   `npx skills find` to discover candidates. Treat popularity as a signal, not
   proof; inspect current upstream content, maintenance, security, license,
   overlap, and representative-task behavior before adoption.
6. Compare overlapping workflow collections and select one owner for each
   procedure. Do not stack equivalent planning, TDD, debugging, review, or
   style instructions by default.
7. Sequence implementation, checks, outcome evidence, and recovery as required.
   Re-route after a lifecycle transition, failed check, new signal, or changed
   authority.

At L1, the smallest loop may require no Skill. L2 adds a repeatable procedure;
L3-L4 compose repository truth, tools, and checks; L5-L7 compose bounded state,
delivery, product, governance, and operating-model loops. Level never justifies
unbounded permissions or ceremony.

Global installation, new credentials, broader permissions, and persistent
dependencies require their normal authority. Prefer a reversible project-local
pilot; manage a public Skill as a pinned dependency only after repeated use
justifies it.

## Agent Context Architecture

Optimize cost, latency, and risk per correctly completed task, not token count
in isolation. Keep stable, high-reuse, session-critical routing and truth local.
Use a versioned projection when remote truth must be reliably available across
sessions; fetch volatile or infrequent information and perform external actions
only when the current task requires them.

MCP makes resources, prompts, and tools reachable. It does not decide source
authority, freshness, persistence, activation, or what belongs in the model
context. Scope MCP servers and capabilities to the active workspace, and route
accepted decisions or learnings to their durable owners.

Use one owner for each data path. Context Mode is the preferred broad mechanism
when large tool, file, or web output would flood the context; RTK is a narrow
CLI fallback when that mechanism is unavailable. Add Headroom only for a
measured request-context problem that remains after the baseline is sound.
Pilot quality, cache behavior, retrieval, privacy, routing, and recovery before
keeping any compression layer.

`skills/engineering/scaffold-harness/CONTEXT-ARCHITECTURE.md` owns the detailed
placement, selection, and evaluation method.

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

## Review Triggers

- Self-review significant changes before completion.
- Request fresh-context review for every resolved material decision or change,
  including public methods and Skill semantics.
- Review the harness after repeated friction, a failed instruction, ownership
  ambiguity, or a harness change.
- Review current sources when model, pricing, platform, security, or community
  guidance affects a decision.
- Review autonomy before expanding permissions, repositories, blast radius, or
  moving from human-in-the-loop to human-on-the-loop.
- Dependency-bot PRs (Renovate or similar): inspect the version jump for this
  repo's usage, run Fast Check / Full Gates (plus feature smoke if runtime
  behavior is touched), merge only with safety evidence; if not merging, leave
  a PR comment with rationale and unblock criteria. Never silent-merge or
  silent-ignore.

Each review must end in an action or an explicit no-change result. Do not add
ceremony that cannot change the next action. Narrow reversible work may rely on
the target's Fast Check and Full Gates. Material resolved work receives
fresh-context review; add new standing reviewers or deterministic scripts only
when escaped defects show the current loops are insufficient.

When evidence should change future work, prefer updating the hard owner
(instructions, Skill, test, CI) over appending soft memory. Route learnings to
the repository that owns the behavior; in a multi-repo system that is the
member, the coordinator, or this catalog-not all three.

## Authority and Human Veto

Routine, reversible maintenance within documented repository scope is
autonomous. Commit and push coherent ready work when checks pass and repository
policy or the current task already grants that authority. Do not ask again for
an authorized routine push. Keep a human in the loop for unresolved intent,
consequential Skill semantics, remote creation, first publication, release,
deploy, force-push, destructive operations, sensitive data, broader
permissions, or material changes to oversight.

For such a branch, present two or three options, evidence, trade-offs,
reversibility, blast radius, and a recommendation. Do not execute the dependent
branch until the human accepts an option.

## External Target Boundary

Target repositories own their local facts, commands, decisions, checks,
permissions, and implementation state. A coordinating repository may own only
cross-repository maps, public contracts, dependency relationships, shared
workflow state, and cross-cutting verification.

Follow `HARNESS-OPERATIONS.md` to choose the correct working root. Never copy
target-specific truth into this repository.

## Canonical Method

- `skills/engineering/scaffold-harness/` owns harness assessment and upgrades.
- `skills/engineering/scaffold-harness/MATURITY.md` owns L1-L7 capability,
  oversight, and operating-model effects.
- `skills/engineering/scaffold-harness/RUNTIMES.md` owns CI, scheduled, durable,
  specialist, chat, and observable agent-runtime selection.
- `skills/engineering/scaffold-harness/CONTEXT-ARCHITECTURE.md` owns local and
  external context placement, MCP routing, context budgeting, and compression.
- `skills/engineering/scaffold-distributed-context/` owns bounded-context,
  contract, projection, and retrieval design across repositories.
- `skills/engineering/agent-sync/` owns continuous evidence routing.
- `skills/engineering/update-harness/` owns explicit versioned dependency and
  currentness updates.
- `skills/engineering/grill-harness-with-docs/` owns shared understanding,
  material critique, and unresolved decisions.
- `skills/product/run-product-engineering/` owns the closed product lifecycle
  from signals through production evidence and evolution.
- `skills/product/integrate-product-compliance/` owns the procedure for
  integrating confirmed control scope without replacing target assurance
  authority.
- `VERSIONING.md` owns per-Skill release semantics.
- `CONTEXT-MAP.md` routes repository-local sources.

Reference these owners instead of duplicating their procedures.
