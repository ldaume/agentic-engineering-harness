# Harness Maturity Reference

## Purpose

Use this reference when assessing a harness level, choosing or switching the
level of a harness, or changing human oversight.

The levels describe the widest unit of work that can be delegated reliably.
They are capability profiles, not status, model intelligence, or a mandatory
roadmap. Assess each decision domain independently and use the lowest level
that solves the problem, because every level above the need adds controls
someone has to keep working.

This Skill scaffolds L3 and L4 for one repository. L5-L7 are defined here so an
assessment can name them; what each means for people is in
[`docs/LEVELS.md`](https://github.com/ldaume/agentic-engineering-harness/blob/main/docs/LEVELS.md), and building them is outside this
Skill.

## Levels

| Level | Delegated unit | System capability | Human role | Minimum evidence | Operating-model effect |
|---|---|---|---|---|---|
| L1 - Directly supervised task | One bounded task in one session | A model supports a person with transient context | Directs and reviews the task | Representative task completed under supervision | Individual work changes; the team system need not |
| L2 - Repeatable procedure | One recurring procedure | Versioned instructions or Skills stabilize execution | Chooses and supervises the procedure | Repeated runs outperform unstructured prompting on relevant examples | Shared working methods begin to replace personal prompting habits |
| L3 - Living repository | Ongoing work in one repository | Context, decisions, commands, checks, and learnings persist across sessions | Owns intent and material decisions; agents maintain bounded repository artifacts | Canonical context, owners, Fast Check, Full Gates, and cross-session learning are discoverable | Repository conventions and review responsibilities become explicit |
| L4 - Grounded system | Work using external evidence or capabilities | Retrieval and tools provide attributable evidence and controlled actions | Approves authority, access, and consequential external effects | Sources, permissions, currentness, failure handling, and audit evidence are explicit | Information access and tool governance become part of delivery |
| L5 - Stateful workflow | A bounded end-to-end workflow | Agents coordinate durable state, wake conditions, retries, recovery, stop conditions, and outcome evaluation | Handles exceptions and unresolved decisions | Repeated workflow runs are observable, recoverable, reconciled after missed progress, idempotent where needed, and evaluated | Roles shift from executing steps to designing and supervising workflows |
| L6 - Governed value stream | Repeated delivery from intent through production feedback | The delivery system operates autonomously inside explicit goals, risk limits, and deterministic controls | Human-on-the-loop for governed domains; retains veto, incident authority, and accountability | Isolated execution, policy and quality gates, rollback, audit, incident ownership, production feedback, and proven oversight | Engineering, operations, security, and product delivery become one governed operating system |
| L7 - Adaptive product system | Bounded product, investment, or portfolio decisions | The system selects problems, experiments, and investments within accountable strategic boundaries | Governs objectives, budgets, decision domains, and exceptions; can stop the system | Proven L6 controls plus trusted product signals, experiment and data boundaries, investment budgets, kill criteria, and human-governed portfolio decisions | Product strategy, funding, organizational design, and decision rights change-not only software delivery |

## Independent Dimensions

Do not average these into a vanity score. Record the current evidence and
target separately for:

- product and domain clarity
- codebase changeability
- feedback and quality
- delivery and operations
- repository and cross-repository context
- agent operation and workflow state
- governance, security, and auditability
- learning and currentness
- organizational decision rights and change readiness

The system's safe operating level is constrained by its weakest required
dimension. A strong coding agent does not compensate for unclear authority,
missing rollback, or an unchangeable codebase.

## Transition Gates

Move only when the next level addresses a repeated failure or valuable bounded
opportunity and the target can verify the result.

| Transition | Required question |
|---|---|
| L1 to L2 | Which procedure recurs often enough to version and evaluate? |
| L2 to L3 | Which context, decisions, checks, or learnings must survive sessions? |
| L3 to L4 | Which external source or action is needed, and who owns its authority, access, currentness, and failure path? |

Retain the lower level when evidence is missing. Name the missing capability
instead of adding artifacts that merely resemble a higher level, because a
level claimed without its controls fails exactly where the controls were
supposed to catch it.

## Choosing and Switching the Operating Level

The lowest scaffolded level is L3; L1 and L2 need no harness, only a Skill.
This Skill scaffolds up to L4. Each level includes the prerequisites of every
level below it.

| Level | Minimum prerequisites observed in the repository | What the generated harness adds |
|---|---|---|
| L3 | Runnable Fast Check and Full Gates; Git as recovery | Template defaults: **Operating Level**, **Oversight** human-in-the-loop |
| L4 | Each external source or tool has an owner, access scope, currentness, and failure path | Those sources in `TOOLS.md` or a `CONTEXT-MAP.md`, and **Agent Context Architecture** |

**Record.** The first line under `HARNESS.md` **Operating Level** is the single
record of the repository-wide level:

```text
Level: L<n> - <name>; scope: <repository or decision domain>; chosen <YYYY-MM-DD> by <owner>; pending gates: <none | list>
```

Fill every placeholder. The README projects it for humans; a decision domain
there may sit lower than the line, never higher, because the line is what
agents act on.

**Choose at scaffold time.** After grounding, recommend the highest level whose
prerequisites all exist, or a lower one when the owner's goal needs no more.
Name what was found (checks, CI, deploy, rollback, telemetry) and what is
missing, and ask the owner once with the table above, because the level
changes the human's role and only the owner can accept that. The owner may pick
lower or higher; a pick above L4 is recorded with its pending gates and stays
outside what this Skill builds.

**Switch later** (scaffold-harness owns this; rerun it with the target level):

1. Read the `Level:` line. When it is absent, infer the current level from the
   sections present and the README, confirm it with the owner, and
   record it; a missing line never counts as a move down. When the line names
   the target with no pending gates and the target's sections are present,
   report no change and stop. When it names the target with pending gates,
   continue closing them and keep the `chosen` date.
2. **Up:** a higher level changes the human role, so only the owner chooses
   it. Check the prerequisites of every level up to the target. Record the
   target with every missing gate under `pending gates`; agents close those
   gates as the first increments. Until the list is empty, the highest fully
   proven level's sections and rules apply: add a level's sections only once
   its gates are closed, and never duplicate a section that exists.
3. **Down:** needs no prerequisites and takes effect at once; an owner stop or
   a boundary, observability, or recovery failure is reason enough. Remove
   what the levels above the target added: below L4, external tool access
   beyond read-only sources. Keep the evidence the higher level produced, so
   a later move up does not start from nothing.
4. Update the `Level:` line and the README, then commit with the
   from and to levels and the reason.

## Anti-Patterns

- claiming a level from installed tools or model capability
- treating the levels as a universal maturity score
- adding multi-agent orchestration before one-agent work is reliable
- using a graph or generated summary as canonical domain truth
- moving to human-on-the-loop without meaningful observability and a stop path
- calling autonomous merge an L6 software factory without production feedback
- optimizing a metric and calling it L7 product judgment
- expanding autonomy across domains because one bounded workflow succeeded

## Assessment Output

Produce only:

1. current evidence by relevant dimension
2. lowest reliable current level for the requested decision domain
3. desired delegated unit and why it is valuable
4. missing gates and the smallest next experiment
5. human role, veto, and re-check trigger
