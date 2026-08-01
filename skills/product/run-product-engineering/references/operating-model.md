# Product Engineering Operating Model

## Contents

- [Closed Loop](#closed-loop)
- [Pull-Based Learning Cycles](#pull-based-learning-cycles)
- [Stage Contract](#stage-contract)
- [Exceptional Paths](#exceptional-paths)
- [Evidence and Metrics](#evidence-and-metrics)
- [Agent Ownership by Level](#agent-ownership-by-level)
- [Operating-Model Effects](#operating-model-effects)
- [Primary Sources](#primary-sources)

## Closed Loop

```text
Signal
-> Triage
-> Problem Framing
-> Opportunity and Risk Burn-down
-> Candidate Bet
-> Prioritized Focus
-> Build, Validate, and Release
-> Production Observation
-> Adoption and Outcome Review
-> Learning and Evolution
-> new or changed Signal
```

Work may enter through a product idea, customer request, bug, incident,
security finding, operational constraint, or compliance obligation. The stages
separate evidence, decision, intervention, outcome, and learning; they are not a
mandatory ticket ceremony.

## Pull-Based Learning Cycles

The states are decision lenses, not sequential departments. Pull the smallest
valuable or risk-burning work just in time. A slice may revisit problem,
language, examples, design, tests, and rollout several times before and after a
release.

When FaST fits the organization, let the collective visualize current work,
self-organize around the most useful next slice, work in the shortest sensible
value cycle, and synchronize learning before reorganizing. Do not impose fluid
teaming where stable ownership, regulation, specialist scarcity, or incident
command requires a named boundary.

Use experiments, prototypes, and technical spikes to buy knowledge cheaply.
Mark them provisional and end each with discard, iterate, or production
investment. Production work restarts from domain behavior, executable examples,
security and operability constraints, and an observation plan.

## Stage Contract

| State | Agent contribution | Human or accountable boundary | Exit evidence |
|---|---|---|---|
| Signal | collect, normalize, deduplicate, attribute provenance | approve new source access and sensitive use | attributable signal or discard reason |
| Triage | classify evidence, urgency, risk, reversibility, and route | own priority conflicts, emergencies, and authority | next action and owner |
| Problem framing | synthesize evidence and expose unknowns | confirm problem semantics and affected users | bounded problem and desired outcome |
| Opportunity and risk burn-down | propose interviews, experiments, spikes, threat or operability reviews | approve customer contact, spend, regulated interpretation, and consequential experiments | reduced uncertainty or explicit unknown |
| Candidate bet | draft intervention, non-goals, budget, signals, and kill criteria | accept investment and strategic trade-off | reviewable bet |
| Prioritized focus | compare evidence, capacity, dependencies, and portfolio balance | allocate accountable focus and funding | selected bet and displaced work |
| Build, validate, release | plan slices, implement, test, review, instrument, and prepare rollout | approve exceptions and risk-class release gates | live slice, rollback, telemetry, and owner |
| Production observation | correlate product and operational signals, detect anomalies | own incident command and sensitive investigation | trustworthy observation window |
| Outcome review | compare outcome, cost, risk, and externalities | decide continue, iterate, scale, rollback, or stop | explicit decision |
| Learning and evolution | route evidence into canonical owners and propose system changes | approve authority expansion and consequential policy changes | changed owner or explicit no-change |

## Exceptional Paths

### Bug

```text
production signal
-> severity and affected behavior
-> reproducible feedback loop
-> root cause
-> failing deterministic check
-> smallest safe fix
-> gated release
-> watch the original signal
-> product or harness learning
```

### Incident

```text
detection
-> contain and restore
-> communicate through the incident owner
-> preserve evidence
-> investigate contributing system conditions
-> remediate and verify
-> review product, control, runbook, and architecture implications
```

### Security or Compliance Finding

```text
finding
-> validate source and scope
-> contain urgent exposure
-> named security or compliance owner
-> risk and control impact
-> remediation or accepted exception
-> evidence and effectiveness review
```

Emergency paths shorten decision latency, not quality, evidence, or
accountability. Complete the missing review after recovery when prior review
would increase harm.

## Evidence and Metrics

Use a balanced set tied to a decision. Do not turn metrics into individual
targets or vanity dashboards.

| View | Examples | Decision served |
|---|---|---|
| Outcome | task success, adoption, retention, revenue, avoided cost, customer-reported value | continue, scale, iterate, or stop |
| Discovery | time to evidence, assumptions retired, experiment result, decision latency | invest, investigate, or reject |
| Delivery flow | change lead time, deployment frequency, work age, blocked time | improve the system constraint |
| Stability and operability | change fail rate, deployment rework, failed deployment recovery, SLO or error-budget behavior, incident recurrence | release, rollback, remediate, or improve controls |
| Product quality | defects by affected behavior, accessibility, security findings, support burden, performance and cost | fix, redesign, or change investment |
| Portfolio | active bets, investment mix, killed bets, outcome coverage, concentration and risk exposure | rebalance funding and focus |

Instrument the user behavior and system path needed to evaluate the bet.
OpenTelemetry can provide vendor-neutral traces, metrics, and logs; it does not
define product outcomes or replace an observability backend.

## Agent Ownership by Level

| Level | Agent may own when proven | Human remains accountable for |
|---|---|---|
| L1-L4 | bounded analysis, implementation, evidence retrieval, and proposals | intent, authority, material decisions, and effects |
| L5 | one stable workflow, state, retries, evaluation, and exception routing | unresolved exceptions and workflow boundaries |
| L6 | bounded delivery through production feedback under deterministic controls | goals, risk policy, incidents, veto, and accountability |
| L7 | bounded signal selection, experiment execution, and investment recommendations | strategy, budgets, decision domains, ethics, and stop authority |

Advance from human-in-the-loop to human-on-the-loop only after repeated runs
prove failure detection, recovery, auditability, and effective intervention.

## Operating-Model Effects

A closed agent-supported product loop changes:

- product, engineering, data, operations, support, customer success, sales,
  marketing, finance, security, compliance, legal, and people collaboration
- decision rights and funding cadence
- team and platform boundaries
- incident and service ownership
- measurement and incentives
- required skills, career paths, and learning support
- governance, worker participation, and change communication

Treat this as organizational change. Preserve psychological safety and make
role, authority, and accountability changes explicit and reversible.
At company scale, use an explicit context and decision map so shared signals and
goals do not become shared authority by accident.

## Primary Sources

- [DORA software delivery performance metrics](https://dora.dev/guides/dora-metrics/)
- [DORA customer feedback](https://dora.dev/capabilities/customer-feedback/)
- [DORA work visibility in the value stream](https://dora.dev/capabilities/work-visibility-in-value-stream/)
- [DORA continuous delivery](https://dora.dev/capabilities/continuous-delivery/)
- [DORA proactive failure notification](https://dora.dev/capabilities/proactive-failure-notification/)
- [OpenTelemetry observability primer](https://opentelemetry.io/docs/concepts/observability-primer/)
- [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/)
- [FaST Guide 3.0](https://www.fastagile.io/guide)
