# Product Engineering Operating Model

## Contents

- [Closed Loop](#closed-loop)
- [Stage Contract](#stage-contract)
- [Exceptional Paths](#exceptional-paths)
- [Discovery Method by Risk](#discovery-method-by-risk)
- [Decision Rights](#decision-rights)
- [Cadence for Human Teams](#cadence-for-human-teams)
- [Evidence and Metrics](#evidence-and-metrics)
- [Portfolio Questions](#portfolio-questions)
- [Adopting the Model](#adopting-the-model)
- [FaST-Compatible Operating for Human Teams](#fast-compatible-operating-for-human-teams)
- [Primary Sources](#primary-sources)

## Closed Loop

```text
Signal
-> Triage
-> Problem Framing
-> Opportunity and Risk Burn-down
-> next evidence decision:
   - discard, stop, or observe -> Outcome Review
   - investigate, prototype, or experiment -> evidence -> Problem Framing
   - explicit production investment -> Candidate Bet -> Prioritized Focus
     -> Build, Validate, and Release -> Production Observation
-> Outcome Review
-> Learning and Evolution
-> new or changed Signal

Production bug, incident, or control failure
-> contain and restore as required
-> diagnose and reframe
-> smallest regression or recovery loop
-> Production Observation and Outcome Review
```

Work may enter through a product idea, customer request, bug, incident,
security finding, operational constraint, or compliance obligation. The stages
separate evidence, decision, intervention, outcome, and learning; they are not a
mandatory ticket ceremony.

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

## Discovery Method by Risk

Pick the cheapest method that can change the decision for the dominant risk.
A method that cannot change the decision is skipped.

| Dominant risk | Methods |
|---|---|
| value | interview, fake door, concierge |
| usability | prototype or task test |
| feasibility | spike or RFC |
| viability | pricing test, sales narrative |
| security or compliance | threat model, control mapping, data-flow mapping |
| operability | SLO review, load test |
| adoption | pilot or beta |
| data | profiling, eval dataset |

## Decision Rights

Name, per value stream, who decides each of these, and write it where the team
works: problem focus, scope cuts, stop or pivot, security risk, release, and
platform investment. Accountability without the decision right is not
ownership: an owner who must ask someone else to cut scope or stop a bet is
only the person blamed when it fails.

## Cadence for Human Teams

Guidance for human teams; agents follow the harness and their own loop, not a
calendar.

| Rhythm | Content |
|---|---|
| continuous | flow of work, incidents, production observation |
| weekly | triage and discovery review |
| monthly | bet review and investment decisions |
| quarterly | portfolio mix and team topology |

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

Add a trust and compliance row when confirmed scope applies: controls with
current evidence, evidence freshness, expiring exceptions, finding and
vulnerability age, and questionnaire cycle time.

Instrument the user behavior and system path needed to evaluate the bet.
OpenTelemetry can provide vendor-neutral traces, metrics, and logs; it does not
define product outcomes or replace an observability backend.

## Portfolio Questions

Ask each quarter, with the data the portfolio view already holds:

- Which outcomes are underfunded against their stated importance?
- How much capacity does maintenance drag take, and is it growing?
- Do short-term sales asks crowd out platform and risk work?
- Which dependencies make teams wait systemically, not once?

## Adopting the Model

In an existing organization, change the system in this order, so each step
shows value before the next costs anything:

1. Make the current system visible. Classify the backlog into signal, problem,
   solution, and delivery work; check the top 20 active items for a named
   outcome and risk; show flow (work age, blocked time).
2. Pilot the loop on one outcome, with its own bet, review date, and kill
   criteria.
3. Move steering to match what the pilot proved: bet review, decision rights,
   an outcome roadmap.

When a compliance scope applies, add one step inside the pilot: map its
controls to the slice with **integrate-product-compliance**, not a parallel
program.

## FaST-Compatible Operating for Human Teams

An option for human teams that want to organize around collective value
instead of fixed team ownership; agents do not need it. The Fluid Scaling
Technology guide (fastagile.io; licensed CC BY-NC-ND, so cite it and do not
copy it) describes a compatible way of working. In short:

- value is pursued in continuous, pull-based cycles of the shortest sensible
  length
- roles are member, product manager, a volunteer team steward per cycle, and
  optionally a feature steward
- a living collective agreement records how decisions are made and conflicts
  are resolved
- people self-select onto work in a marketplace
- teams resolve their dependencies themselves
- people may move between teams when it helps the work

Use **writing-product** `references/fast.md` for roadmaps in this mode.

## Primary Sources

- [DORA software delivery performance metrics](https://dora.dev/guides/dora-metrics/)
- [DORA customer feedback](https://dora.dev/capabilities/customer-feedback/)
- [DORA work visibility in the value stream](https://dora.dev/capabilities/work-visibility-in-value-stream/)
- [DORA continuous delivery](https://dora.dev/capabilities/continuous-delivery/)
- [DORA proactive failure notification](https://dora.dev/capabilities/proactive-failure-notification/)
- [OpenTelemetry observability primer](https://opentelemetry.io/docs/concepts/observability-primer/)
- [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/)
- [Fluid Scaling Technology](https://fastagile.io/) - cited, not reproduced
- Teresa Torres, *Continuous Discovery Habits* - opportunity solution tree
