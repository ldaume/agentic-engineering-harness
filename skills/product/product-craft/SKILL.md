---
name: product-craft
description: Shapes evidence-driven product investments, value-defined issues, honest Now/Next/Later/Never roadmaps, discovery, UX, architecture, delivery, and learning. Use when turning signals into bets, deciding whether or when work deserves investment, planning product work, or coordinating product and engineering trade-offs without backlog or milestone theater.
---

# Product Craft

Use this as the general all-in operating mode for product work that spans
strategy, UX, engineering, AI, architecture, delivery, and learning.

## Project Fit Check

Before shaping product work:

1. Read existing product context: repo instructions, domain glossary, roadmap,
   ADRs, research, analytics notes, customer feedback, and current plans.
2. Identify the local decision format before introducing Problem Briefs or Bet
   Briefs. Adapt to existing PRDs, RFCs, issues, or ADRs when they already work.
3. Separate canonical product docs from background research or old explorations.
4. If the repo has no durable product-memory structure, suggest a minimal
   glossary, decision log, or agent-doc setup before relying on chat context.
5. Do not impose SaaS, AI-native, or bet language where the product context uses
   different terms; map the concepts to local vocabulary.

## Core Stance

- Start with the actual user or business problem, not a backlog item, feature
  idea, framework, AI demo, or aesthetic preference.
- Treat software product development as product and system development under
  uncertainty.
- The main unit of decision is the **bet**, not the ticket.
- A signal is not a problem. A problem is not a solution. A release is not an
  outcome. An outcome only matters when it changes future decisions.
- AI-native work is an operating model, not a tool choice.
- Human responsibility remains final: AI drafts, explores, critiques, and
  accelerates; humans own trade-offs and decisions.

## Read First

Before acting in a repo, read current local sources instead of trusting memory:

1. `AGENTS.md` or the repo's agent instructions
2. `CONTEXT.md` or the repo's domain glossary
3. `LEARNINGS.md` or equivalent learning log, newest entries first
4. Relevant ADRs, plans, product docs, roadmap docs, or design docs
5. Existing code and tests around the surface being changed

Pair with `coding-discipline` for implementation, `completion-gate` before
claiming done, and `agent-sync` after durable learnings.

## Product Decision Loop

Do not replace one mandatory delivery pipeline with another. Use
**run-product-engineering** as the canonical branching loop. At each decision,
choose whether to discard, observe, investigate, contain, experiment, deliver,
or stop. A release happens only when current evidence justifies production
investment, and production evidence changes the next decision.

Keep these things separate:

- signal
- problem
- opportunity
- solution
- delivery work
- outcome
- learning

This Skill owns product framing, investment horizons, and issue quality. Use
**run-product-engineering** when the task spans delivery, production
observation, incidents, outcome review, or evolution.

## AI-Native Work Loop

For agent-assisted product and engineering work:

1. **Load context**: playbook, domain context, recent learning updates.
2. **Run with skill**: use the right skill for the step instead of free-form
   prompt improvisation.
3. **Implement narrowly**: small diff, clear goal, testable behavior.
4. **Gate before done**: correctness, security, regression, and verification.
5. **Sync learning**: durable errors, review feedback, and patterns become
   versioned artifacts, not chat shadow knowledge.

## Autonomy and Operating Model

Expand product autonomy only within a named decision domain. Define accountable
objectives, trusted product signals, experiment and data boundaries, investment
budgets, kill criteria, audit, and an effective human stop path before agents
select problems or allocate resources.

Treat the change as organizational design, not a tooling rollout. Make changes
to roles, decision rights, accountability, incentives, feedback, communication,
incident ownership, and learning support visible and reversible. Do not infer
product, employment, legal, security, or strategic authority from technical
capability. Humans retain veto until repeated bounded evidence supports a
narrower human-on-the-loop role.

Use `scaffold-harness/MATURITY.md` for L1-L7 evidence gates rather than
duplicating them here.

## Problem Brief

Use before investing in solution work. If the repository has no equivalent,
load the [Problem Brief template](./TEMPLATES.md#problem-brief).

## Bet Brief

Use when a problem may deserve focused investment. If the repository has no
equivalent, load the [Bet Brief template](./TEMPLATES.md#bet-brief).

## Investment Horizons

Treat a roadmap as a current investment view, not a delivery promise:

- **Now** - the currently funded outcome, risk reduction, or next evidence
  decision. Limit work in progress and name what this focus displaces.
- **Next** - an evidence-supported candidate without a delivery commitment.
  Promote it only when evidence, capacity, and dependencies justify focus.
- **Later** - a deliberately coarse option. Do not elaborate it into detailed
  specifications or ticket sets while important uncertainty remains.
- **Never** - an explicit non-investment decision with rationale, decision
  evidence, and a concrete trigger that would justify reconsideration.

Signals may also be discarded without entering a roadmap. If the repository
has no equivalent view, load the
[Outcome Roadmap template](./TEMPLATES.md#outcome-roadmap).

Horizons are not dates. Distinguish an external deadline, observation or
review date, forecast, and commitment. Record the source, owner, assumptions,
confidence, and reforecast trigger for any forecast. Use a milestone only for
a real coordination, external, release, or outcome boundary - never as an
arbitrary batch of hoped-for features.

## Value-Defined Issues

Create a decision or delivery work issue only when the next decision or action
is bounded and sharp enough to own. Use the target's existing tracker and
format:

- a **decision or learning issue** resolves one consequential unknown
- a **production value-slice issue** creates one observable vertical behavior
  change across the relevant public seam
- a **bug or control issue** restores an invariant or reduces verified risk,
  cost, support burden, or blocked flow; do not invent a fake user story

Raw signal, incident, request, or finding records may remain in the existing
intake system for provenance and triage; their existence is not an investment
decision. Only sufficiently sharp Now or Next work becomes a decision or
delivery issue. Later remains an option or fog; Never remains a decision
record. Preserve the linked problem or bet, affected actor and bounded context,
expected value, evidence, unknowns, smallest decision or behavior change,
examples, signals, non-goals, genuine blockers, and owner. If the repository
has no equivalent, load the
[Value-Defined Issue template](./TEMPLATES.md#value-defined-issue).

Draft or create tracker state only when the target repository and authority are
clear. Creating an issue does not grant product priority or implementation
authority.

## Decision Rules

- If evidence is weak, frame a discovery or risk burn-down step before delivery.
- If the value is unclear, write a Problem Brief before discussing solution
  shape.
- If risk is high, define kill or pivot criteria before build work starts.
- If AI is involved, define the human/AI boundary, failure handling, validation,
  provenance, and cost signal.
- If the work touches architecture, write down the trade-off and whether it
  belongs in an ADR.
- If a user-facing change cannot be measured directly, define at least one
  learning signal.

## AI Product Strategy

When AI is part of the product, start with the product job before the model:

- What user outcome improves because AI is present?
- Which part is judgment, generation, retrieval, classification, extraction,
  planning, or automation?
- Where must a human review, approve, edit, or override?
- What happens when the model is wrong, slow, unavailable, expensive, or
  uncertain?
- What data is needed, what data is forbidden, and what provenance must be kept?
- Which parts should be deterministic code instead of AI?

AI product choices should name the human-AI boundary, validation loop,
confidence handling, cost signal, and recovery path.

## Vision And Narrative

Use vision work when the team needs direction, not when a feature needs prose.

Good product vision is:

- emotionally legible
- specific enough to guide trade-offs
- achievable in phases
- grounded in a real user struggle
- memorable without becoming slogan-only

Write it as a decision tool. If the repository has no equivalent, load the
[Product Vision template](./TEMPLATES.md#product-vision).

## MVP Discipline

Default MVP path:

```text
Manual -> Processized -> Productized -> Automated -> Scaled
```

Rules:

- Do the smallest thing that tests the riskiest assumption.
- Prefer manual service delivery before building software for unknown demand.
- Productize repeatable steps only after the process is understood.
- Keep scope small enough that failure teaches something specific.
- Do not call a prototype an MVP unless it can create or disprove real value.

## Startup Ideation

For early ideas, separate imagination from commitment:

1. Generate many problem spaces, not only solution ideas.
2. Pick ideas with urgent pain, reachable users, and a plausible wedge.
3. Name distribution before product polish.
4. Identify unfair insight, data advantage, workflow access, or trust advantage.
5. Define the cheapest validation step before writing a roadmap.

Good ideation output is a shortlist of testable bets, not a pile of clever
concepts.

## Five Flows To Monitor

Progressive product systems are judged by flow quality:

1. **Signal flow**: how quickly relevant signals are recognized.
2. **Learning flow**: how quickly important uncertainty is reduced.
3. **Decision flow**: how quickly good, traceable decisions happen.
4. **Delivery flow**: how safely valuable changes ship.
5. **Outcome flow**: how reliably shipped changes create customer and business
   impact.

The central leadership question is:

> Where in the system is it decided whether a problem truly deserves focus?

## Red Flags

Stop and reframe when you see:

- backlog size used as proof of strategy
- velocity used as proof of value
- a feature idea treated as an already validated problem
- AI added because it is fashionable rather than useful
- no named user, segment, evidence, or outcome
- discovery that never changes scope
- delivery work with no kill criteria, review date, or learning plan
- "done" declared at release without adoption or outcome review
