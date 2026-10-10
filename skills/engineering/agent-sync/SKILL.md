---
name: agent-sync
description: Proactively evolves a repository's harness artifacts from durable evidence across sessions and tools. Use when starting or completing a session, when repeated friction reveals missing context or checks, when a lesson should outlive the current task, or when instructions, Skills, Rules, Hooks, MCP, or learnings may be stale.
---

# Agent Sync

Learning lives in Git-tracked owning artifacts, not chat history, because the
next session starts from the repository and never sees this conversation.

## Project Fit

1. Read the applicable instruction hierarchy and context routing.
2. Map local equivalents before introducing preferred filenames; a second name
   for an existing owner splits the truth in two.
3. Use existing sources of truth and preserve repository conventions.
4. Run **scaffold-harness** when the repository lacks a reliable baseline.
5. Establish shared understanding for significant work. Use
   **grill-harness-with-docs** for unresolved material decisions in any topic.

## Session Start

First, take the **current** harness contract and pinned Skills. Do not skip
this because the task looks small: a stale contract is wrong on exactly the
rule that changed last.

1. Refresh the live harness: `git fetch` origin and read `HARNESS.md` from
   the origin default tip (`git show origin/<default>:HARNESS.md`) or the
   remote canonical file. Do not treat `./HARNESS.md` in a task worktree as
   current. Ff-only a clean primary when behind origin; if blocked, leave it.
2. Confirm managed Skill copies match the repository's **origin** pins before
   following a Skill. Read `SKILL.md` from that current copy.
3. Then load only the additional sources the task needs:

- agent instructions after the current harness contract
- the current human's preferred collaboration language from explicit or
  conversation evidence; ask once only if unclear, and keep personal preference
  in user-scoped or untracked state unless it is shared policy
- the active host and effective instruction, Skill, plugin, Rule, Hook, MCP,
  and permission precedence needed by the task
- relevant domain context, ADRs, and recent learnings
- Skills triggered by the task
- the managed `write-a-skill` owner before Skill creation or revision
- actual Fast Check and Full Gates
- volatile model, pricing, platform, or tool evidence only when the task
  depends on it

Do not treat "read only what the task needs" as permission to skip harness
currency or git-loop close-out. Do not re-derive conventions already owned by
an artifact.

## Stewardship During Work

Harness stewardship is part of every significant task. Notice repeated
friction, missing or stale context, weak feedback, unclear ownership,
unnecessary ceremony, and recurring workflows.

Keep canonical artifacts agent-first and host-neutral. Human README and
reference material are legible projections, while thin host adapters reference
the owning instructions, context, and contracts. Communicate in the human's
preferred language; keep persistent repository artifacts in US English unless
a named artifact is explicitly requested otherwise.

Follow the repository's owned voice or style guide. Without one, keep prose
direct and concrete: lead with the problem or working model, name trade-offs
and system effects, and remove generic hype, defensive setup, and text that
changes no decision or action. Reserve first person for artifacts that
explicitly speak for the repository owner; keep agent instructions neutral and
imperative.

Diagnose before changing. Update the smallest owning artifact when evidence
justifies a reversible in-scope improvement. Leave the harness unchanged when
no durable signal exists, because every added rule costs every later session.

Route a repeated missing-stack failure through `update-harness`, and use
`write-a-skill` for the smallest project-local profile only when repeated work
supplies real examples and checks. One-off stack work stays direct work.

Do not return an authorized routine decision to the human as a confirmation
question. Close it through the repository policy and available evidence, or
escalate a named conflict, authority gap, or material risk.

Before claiming done, ask and answer in the same loop:

1. **Manifest here?** Does this evidence belong in the current repository
   harness owner (`HARNESS.md`, `AGENTS.md`, checks, Hook, Skill,
   `LEARNINGS.md`)? Prefer a hard adaptation when the same mistake would recur.
2. **Port within your authority?** After every harness change, decide whether a
   generalized variant belongs in a catalog you own or are authorized to
   change. If yes, update that owner in the same loop. Do not push, open a pull
   request, or otherwise write back to an external public upstream you only
   consume - including `https://github.com/ldaume/agentic-engineering-harness`
   - unless you maintain it, because a consumer's local lesson is not the
   upstream's decision.
3. After a change that alters purpose, autonomy, git hygiene, or the harness
   cycle: does the human `README.md` still teach a new reader the current
   operating level and what would justify the next one?

## Route Durable Evidence

| Signal | Owning mechanism |
|---|---|
| New or changed commands, scope, permissions | Agent instructions |
| Domain term or invariant | Domain context |
| Harness oversight or evolution rule | Harness contract |
| Git working-tree start/finish hygiene | Harness contract (Git Working Tree Hygiene); ADR when accepted |
| Dependency-bot PR merge or defer | Harness contract (Dependency bot PRs) + PR comment |
| Accepted consequential trade-off | ADR |
| Repeated probabilistic workflow | Skill |
| Portable Skill authoring behavior | Managed `write-a-skill`; a native host creator stays an adapter |
| Scoped behavioral guidance | Rule or agent instruction |
| Deterministic event or enforcement | Hook, CI, test, platform control |
| Durable evidence-backed observation | `LEARNINGS.md` |
| Human understanding of purpose or where to work | Human `README.md` |

Route a lesson once, to the owner of the behavior, and reference that owner
from consumers instead of copying it. Prefer a hard adaptation of the owning
artifact when the lesson is a rule. Use a learning entry when evidence should
survive sessions but is not yet stable enough to hard-code.

## Verification

1. Run the smallest relevant checks for changed artifacts.
2. Verify referenced local paths and commands.
3. Review the diff for duplicated, stale, speculative, or unowned layers.
4. Consolidate or supersede prior learnings instead of appending duplicates;
   two entries on one lesson drift apart.
5. State what changed, why, and the next re-check condition.
6. Close the git integration loop for this session's ready work per the
   harness contract: commit and push when authorized, merge a session-owned
   PR when required checks are green, or record a named blocker.

## Do Not Persist

- one-off debugging and ticket chatter
- raw chat or temporary task state
- rules already enforced by a native config or deterministic control
- unverified product, architecture, ownership, or security assumptions
- a new artifact without an observed problem and owner

The sync is complete when durable evidence is routed, relevant checks pass,
uncertainty is explicit, and no further harness change is justified by the
current work.
