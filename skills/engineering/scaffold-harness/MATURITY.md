# Harness Maturity Reference

## Purpose

Use this reference when assessing a harness level, choosing or switching the
level of a harness, proposing a move beyond repository-level work, changing
human oversight, or discussing organizational transformation.

The levels describe the widest unit of work that can be delegated reliably.
They are capability profiles, not status, model intelligence, or a mandatory
roadmap. Assess each decision domain independently and use the lowest level
that solves the problem.

## Levels

| Level | Delegated unit | System capability | Human role | Minimum evidence | Operating-model effect |
|---|---|---|---|---|---|
| L1 - Direct task | One bounded task in one session | A model supports a person with transient context | Directs and reviews the task | Representative task completed under supervision | Individual work changes; the team system need not |
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
| L4 to L5 | Which end-to-end workflow needs durable state, recovery, observability, and outcome evaluation? |
| L5 to L6 | Which delivery domain has stable goals, risk classes, policy gates, isolation, rollback, production feedback, incident ownership, and proven human oversight? |
| L6 to L7 | Which product or investment decision domain has trusted signals, explicit budgets, experiment boundaries, kill criteria, accountability, and an effective human stop mechanism? |

Retain the lower level when evidence is missing. Name the missing capability
instead of adding artifacts that merely resemble a higher level.

## L6: Operating-Model Transformation

L6 is not "an agent can merge." It is a governed value stream spanning the
parts needed to create and operate value safely:

- intent and acceptance boundaries
- implementation and integration
- deterministic quality, security, and policy gates
- isolated environments and least privilege
- release, canary, rollback, and recovery
- production signals and outcome feedback
- incident ownership, audit, and escalation
- explicit human decision rights and veto

Before reducing direct human review, prove the controls through repeated
bounded runs. Expand autonomy one risk class or decision domain at a time.

Use **run-product-engineering** to close the value stream from attributable
signals through release, production observation, incidents and bugs, outcome
review, and an explicit next decision. An L6 system that stops at merge or
deployment is incomplete.

## Product Loop

At L6-L7, close the product loop from attributable signals through delivery,
production observation, incident and bug feedback, outcome review, and an
explicit next decision. Release alone is not completion.

## L7: Bounded Product Autonomy

L7 extends proven delivery autonomy into selected product decisions. It may
include problem selection, experiment design, resource allocation, or portfolio
recommendations, but only inside named boundaries.

For each decision domain define:

- accountable strategic objective
- trusted customer, product, financial, and operational signals
- allowed data and experiment methods
- investment and loss budget
- success, pivot, and kill criteria
- decision owner, review cadence, and audit trail
- stop, rollback, and escalation mechanism

L7 does not mean an autonomous company by default. Different domains can remain
at different levels, and legal, ethical, employment, security, or strategic
authority cannot be inferred from technical capability.

The same closed loop must expose whether agent-selected problems, experiments,
and investments created customer value without violating reliability, security,
compliance, financial, or organizational guardrails.

At department or company scale, map how product, engineering, data, operations,
support, customer success, sales, marketing, finance, security, compliance,
legal, and people functions contribute signals, decisions, controls, and
feedback. Shared goals and data do not imply shared authority.

Routine progress at L6-L7 must not depend on a human scheduling the next step.
Humans and agents may both contribute signals. Humans remain valuable as intent
and policy owners, domain and user evidence sources, capability enablers,
credential custodians, exception and incident operators, feedback providers,
and an effective stop path. Keep those contributions visible and durable
without turning them into mandatory approval gates for already authorized work.

### L7 Owner-Delegated Operating Profile

An optional operating style an accountable owner may choose for a named scope.
It does not replace the L7 decision-domain definition above, and it is not the
catalog default; without an explicit owner choice, the default
human-in-the-loop **Oversight** contract applies.

The profile moves the human on or out of the loop: agents decide everything
except a short closed list of owner-reserved classes (vision, values, risk
budgets, the list itself, and loosening safety controls; spending money or
sending to people outside the system; new external exposure or loosened
authentication on exposed surfaces; irreversible loss without an
independently verified restore; new third-party trust). Reserved decisions
arrive as a ready recommendation the owner only confirms, outcomes are recorded
as `accepted-as-recommended`, `changed`, or `rejected`, and agents propose
retiring a gate from that evidence. An in-session owner stop always wins.

Safety comes from agents on the loop rather than human approval: spike-first
craft with no document gates, specialist reviewers triggered by risk class,
tested fallbacks for every external dependency, commits that carry the durable
why and PRs that carry review evidence as labeled data, and a host-parity check
over each agent host's permission file.

Choose it only when the L6 controls it replaces are real for that scope:
deterministic gates at the moment of change, checked deployments,
observability, executable rollback, and an effective stop path. A missing
control is the first increment, not a reason to claim the profile anyway. The
operating text lives in the `templates/HARNESS.md` subsection **Optional:
Owner-Delegated Operating Profile** and the specialist table in **Review
Loops**; copy them only when the owner chooses the profile.

## Choosing and Switching the Operating Level

The lowest scaffolded level is L3; L1 and L2 need no harness, only a Skill.
Each level includes the prerequisites of every level below it. In a scaffolded
harness, choosing L7 is the owner's explicit choice of the owner-delegated
profile.

| Level | Minimum prerequisites observed in the repository | What the generated harness adds |
|---|---|---|
| L3 | Runnable Fast Check and Full Gates; Git as recovery | Template defaults: **Operating Level**, **Oversight** human-in-the-loop |
| L4 | Each external source or tool has an owner, access scope, currentness, and failure path | Those sources in `CONTEXT-MAP.md` and **Agent Context Architecture** |
| L5 | Durable workflow state, retries and recovery, run observability, a stop path | `STATUS.md` as workflow and promotion index; runtimes per `RUNTIMES.md` |
| L6 | Required CI checks at merge, a checked deployment, executable rollback, production telemetry and alerts, an incident owner | **Oversight** promotion loop with each human-on-the-loop class named; **run-product-engineering** closes the loop |
| L7 | Proven L6 plus trusted product signals, budgets, kill criteria, and an owner stop path | **Optional: Owner-Delegated Operating Profile**, its **Oversight** paragraph, and the **Review Loops** specialist table |

**Record.** The first line under `HARNESS.md` **Operating Level** is the single
record of the repository-wide level:

```text
Level: L<n> - <name>; scope: <repository or decision domain>; chosen <YYYY-MM-DD> by <owner>; pending gates: <none | list>
```

Fill every placeholder. The README **Current Operating Envelope** projects it
for humans; a decision domain there may sit lower than the line, never higher.

**Choose at scaffold time.** After grounding, recommend the highest level whose
prerequisites all exist, or a lower one when the owner's goal needs no more.
Name what was found (checks, CI, deploy, rollback, telemetry) and what is
missing, and ask the owner once with the table above. The owner may pick lower
or higher; a higher pick is recorded with its pending gates.

**Switch later** (scaffold-harness owns this; rerun it with the target level):

1. Read the `Level:` line. When it is absent, infer the current level from the
   sections present and the README envelope, confirm it with the owner, and
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
   what the levels above the target added: below L7 the owner-delegated
   subsection, its **Oversight** paragraph, and the specialist table; below L6
   the promoted human-on-the-loop classes (return them to human-in-the-loop
   and record why); below L5 unattended runtimes (pause them through their
   documented stop path); below L4 external tool access beyond read-only
   sources. Keep `STATUS.md` and the evidence the higher level produced.
4. Update the `Level:` line and the README envelope row, then commit with the
   from and to levels and the reason.

## Organizational Change

At L5 and above, changing the harness changes how work and responsibility flow.
Plan the transformation alongside the technology:

- roles, skills, and career paths
- decision rights and accountability
- team and platform boundaries
- incentives and performance measures
- planning, funding, and portfolio cadence
- communication and shared language
- security, legal, compliance, and worker representation where applicable
- psychological safety, job uncertainty, and learning support
- incident command and executive stop authority

Use staged adoption, visible evidence, reversible pilots, and explicit feedback
channels. Do not present autonomy as a tool rollout or hide material role
changes inside an engineering implementation.

## Anti-Patterns

- claiming a level from installed tools or model capability
- treating the levels as a universal maturity score
- adding multi-agent orchestration before one-agent work is reliable
- using a graph or generated summary as canonical domain truth
- moving to human-on-the-loop without meaningful observability and a stop path
- adopting the owner-delegated profile as a default instead of an explicit owner choice
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
