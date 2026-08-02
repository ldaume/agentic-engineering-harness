# <System Name>

<One paragraph describing the system, its users, and the outcome it owns.>

## Where Humans Start

- Start an agent in the repository that owns the intended change.
- State the outcome and relevant constraints. Do not prescribe a Skill or
  implementation stack unless that choice is itself required.
- Let the agent inspect local instructions, context, state, and checks; perform
  routine reversible work; review its own diff; and commit or push when local
  policy authorizes that completion path.
- Intervene for unresolved intent, domain semantics, authority, material risk,
  sensitive or irreversible effects, or a failed control required by the
  delegated unit.

The canonical agent behavior lives in `AGENTS.md` and `HARNESS.md`. This README
is the human projection: it explains how to use the system without copying the
control plane.

## Current Operating Envelope

| Decision domain | Reliable level | Human role and veto | Evidence or missing gate |
|---|---|---|---|
| <repository changes, release, security, product discovery, or other domain> | <L1-L7> | <what the human owns and may stop> | <checks, recovery, observability, repeated runs, or named gap> |

Levels are assessed per decision domain. The weakest required control sets the
safe level; installed models or tools do not prove maturity.

## How Human and Agent Work Change by Level

| Level | Human use and accountability | Agent operation | Engineering method | Why this fits |
|---|---|---|---|---|
| L1 - Direct task | Frame and review one bounded task | Use session context and run the relevant check | Small inspect-change-check loop | One-off work does not justify durable machinery |
| L2 - Repeatable procedure | Select and supervise a recurring procedure | Follow one versioned Skill or instruction with evidence and stop conditions | Repeat and improve an evaluated loop | It removes prompt variance without creating a full harness |
| L3 - Living repository | Own intent, domain semantics, and material trade-offs | Use Git-owned context, checks, decisions, and learnings across sessions | Evolve DDD language, vertical slices, TDD, and code together; bound or discard spikes | Ongoing work becomes recoverable, reviewable, and portable across sessions |
| L4 - Grounded system | Approve access, authority, and consequential external effects | Use attributable sources and controlled tools with currentness, failure handling, and audit evidence | Test assumptions early; shift quality, security, privacy, accessibility, compliance, and operability into each slice | External capability helps without becoming inferred authority |
| L5 - Stateful workflow | Design the workflow and handle exceptions | Coordinate durable state, retries, recovery, stop conditions, observability, and outcome evals | Pull small end-to-end DDD/TDD learning slices across repository boundaries | People supervise semantics and exceptions instead of carrying routine state |
| L6 - Governed value stream | Govern goals and risk on the loop; retain veto, incident authority, and accountability | Run signal through production feedback using isolation, policy gates, rollback, telemetry, and audit | Continuous discovery and delivery, vertical TDD, Shift-left DevSecOps and agile testing, observable rollout, incident learning | Autonomy expands only where failures are detectable, bounded, and recoverable |
| L7 - Adaptive product system | Set objectives, budgets, decision domains, and exceptions; stop the system when needed | Select bounded problems, experiments, and investments from trusted signals inside explicit limits and kill criteria | Hypothesis-driven product learning; discard prototypes or explicitly harden them | Product autonomy is bounded by strategy, economics, evidence, and accountability |

Use the lowest level that closes the real loop. Graduate one decision domain at
a time only after its specific evidence gate passes:

| Transition | Evidence required before delegation expands |
|---|---|
| L1 to L2 | A versioned procedure outperforms unstructured prompting on representative examples under supervision |
| L2 to L3 | Canonical repository context, owners, Fast Check, Full Gates, and cross-session learning are discoverable and work in a representative task |
| L3 to L4 | Sources, permissions, currentness, failure handling, audit evidence, and external-write boundaries are explicit and tested |
| L4 to L5 | Repeated workflow runs are observable, recoverable, idempotent where needed, safely stoppable, and evaluated against outcomes |
| L5 to L6 | Repeated bounded value-stream runs prove policy and quality gates, isolation, rollback, audit, production feedback, incident ownership, and effective human intervention |
| L6 to L7 | A bounded pilot proves trusted signals, experiment and data boundaries, investment and loss budgets, success, pivot, and kill criteria, accountability, audit, and a human stop mechanism |

## Working Loop

```text
signal or intent
-> triage domain, value, risk, and uncertainty
-> run the smallest research spike or production slice
-> evolve examples, model, tests, controls, and code together
-> integrate and release through proportional gates
-> observe production, incidents, controls, cost, and outcomes
-> keep, change, remove, pivot, or stop
```

Use only the loop needed by the current delegated decision:

| Level | Loop |
|---|---|
| L1 | bounded task: inspect -> change -> check |
| L2 | repeatable procedure: input -> action -> evidence -> improve |
| L3-L4 | repository: intent -> context -> change -> gates -> durable learning |
| L5 | workflow: state -> step -> evaluate -> retry, recover, or stop |
| L6 | value stream: signal -> frame -> experiment or slice -> release when warranted -> production evidence -> next decision |
| L7 | product: trusted signals -> bets and experiments -> outcomes -> investment decision |

Higher loops wrap smaller proven loops; they do not make every task traverse
the whole product system. Topology follows ownership, not level.

### Phase Responsibilities

The rows below describe the whole product loop, not blanket authorization. In
each decision domain, delegate only the activities allowed by the current
operating envelope, repository policy, permissions, and evidence. At lower
levels the human performs or directly approves more of the row; later levels
expand agent execution only after the transition gate passes.

| Phase | Human role | Agent work | Method and controls | Why |
|---|---|---|---|---|
| Signal and observation | Set objectives, allowed sources, privacy boundaries, and accountable outcomes | Collect, attribute, deduplicate, and relate customer, product, operational, security, and commercial evidence | Provenance, currentness, access control, and telemetry; signals are evidence, not requirements | Breadth and traceability improve without turning noise into priority |
| Triage and domain framing | Decide priority, authority, risk appetite, and material semantics | Map the problem, bounded context, examples, invariants, dependencies, uncertainty, and assurance needs | DDD discovery, hypotheses, and Shift-left risk, security, compliance, accessibility, and testing | The smallest valuable decision is found before implementation hardens assumptions |
| Spike, prototype, or experiment | Approve the question, budget, data boundary, and success or stop criteria | Build and measure the cheapest isolated learning vehicle; record discard, iterate, or harden evidence | Timebox, isolation, approved data, and no silent production promotion | Uncertainty is retired cheaply instead of hidden in speculative specifications |
| Production slice | Own material trade-offs and acceptance boundaries | Evolve examples, model, contracts, tests, code, telemetry, controls, and recovery in one vertical slice | DDD, TDD, agile testing, Fast Check, and self-review | Design, implementation, and assurance share one fast feedback loop |
| Integration and release | Handle policy exceptions and unusually critical release decisions | Run Full Gates, risk-triggered independent review, compatibility checks, staged rollout, rollback proof, audit evidence, commit, and push | Continuous delivery, least privilege, small batches, and canary or feature control | Routine delivery becomes autonomous while blast radius stays bounded |
| Operation, incident, and bug learning | Own objectives, incident authority, risk acceptance, and external communication | Observe outcomes and controls; detect, contain, reproduce, root-fix, recover, and route learning to context and checks | Observability, runbooks, rollback, regression TDD, and causal learning | Production reality becomes the next design input |
| Outcome and next decision | Decide keep, change, pivot, stop, or invest | Compare expected and observed value, reliability, risk, cost, adoption, and control effectiveness; propose the next bounded bet | Outcome evals, decision trail, budgets, and kill criteria | Output is not mistaken for customer or business value |

This is not a specification -> implementation -> testing -> deployment
handoff. Specifications, DDD models, tests, security, compliance, operability,
and delivery are feedback activities. Prototypes and technical spikes are
learning artifacts: discard them after learning or make an explicit production
investment.

If a backlog exists, keep it as a small pull queue for current decisions. It is
not a commitment inventory or evidence that future items create value.

For product work that uses shared investment or issue tracking, at any level,
use Now/Next/Later/Never as an investment view. Now is the current funded focus
or evidence decision; Next is a candidate without a commitment; Later stays
coarse; Never records a deliberate non-investment with rationale and a revisit
trigger. Horizons are not dates, and only sufficiently sharp Now or Next work
becomes a decision or delivery issue. Raw intake records may remain without
becoming commitments. The level determines who maintains and approves these
decisions, not whether the semantics apply.

## Repository Map and Checks

- Agent entry: `AGENTS.md`
- Harness and oversight: `HARNESS.md`
- Domain language: `<CONTEXT.md or existing owner>`
- Sources and relationships: `<CONTEXT-MAP.md or existing owner>`
- Current cross-session state: `<STATUS.md or existing owner>`
- Fast Check: `<smallest reliable command for narrow work>`
- Full Gates: `<integration, test, lint, typecheck, build, or release command>`
- Recovery and escalation: `<owner and path>`

For multi-repository or multi-team systems, add links to the coordinator,
member inventory, public contracts, compatibility checks, shared workflow
state, and cross-team decision rights. Keep member-local product and
architecture truth in the member that owns it.
