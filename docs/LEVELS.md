# Operating Levels

The seven levels describe the largest unit of work that can be delegated
reliably. They do not measure model intelligence or the number of installed
tools. Each level needs its own evidence, boundaries, and human
responsibility.

Autonomy does not grow through a claim. It grows when a smaller loop works
repeatedly, fails visibly, and can continue or stop safely. Higher levels build
on proven lower ones, and each decision domain is assessed separately, not the
team as a whole: a team can run releases at L6 and product discovery at L3.
Where authority, recovery, or evidence is weaker, that dimension limits the
safe level.

This page is for people. Agents assess against the level table in
[`scaffold-harness/MATURITY.md`](../skills/engineering/scaffold-harness/MATURITY.md);
this page is its human projection. The same model, with the consulting frame,
is on [daume.dev](https://daume.dev/en/agentic-engineering-maturity-model).

## L1 - Directly supervised task

**Means:** An agent supports one clearly bounded task in one session, with
context that does not outlive it.

**Human still does:** Frames the task, provides the context, and reviews the
result directly.

**Evidence for L2:** A procedure recurs often enough to be worth versioning,
and repeated runs of the versioned procedure outperform unstructured prompting
on relevant examples.

**In this catalog:** Any single Skill works on its own; no harness is needed.
`coding-discipline` and `completion-gate` are a good first pair.

## L2 - Repeatable procedure

**Means:** Versioned instructions or Skills stabilize one recurring method, so
it stops depending on how someone happened to phrase a prompt.

**Human still does:** Selects the procedure, supervises execution, and
evaluates repeated results.

**Evidence for L3:** Context, decisions, checks, and learnings need to survive
sessions, and a representative repository task works from canonical sources,
named owners, a real Fast Check and Full Gates, and one route for learnings.

**In this catalog:** `write-a-skill` to write and verify a procedure; the craft
Skills (`testing-strategies`, `api-design`, `frontend-craft`, `backend-craft`,
and the rest) as ready-made ones.

## L3 - Living repository

**Means:** Agents do ongoing work in one repository; context, decisions, checks,
and learnings survive between sessions. Routine work is committed when the
repository authorizes it.

**Human still does:** Owns intent, domain meaning, and material decisions;
reviews new meaning, not routine diffs.

**Evidence for L4:** A runnable Fast Check and Full Gates, named owners, and
learnings that changed a later session. Each external source or tool an agent
would use has an owner, a scope, and a failure path.

**In this catalog:** `scaffold-harness`, `agent-sync`, `update-harness`, with
`start-gate` and `completion-gate` at the edges of each task.

## L4 - Grounded system

**Means:** Sources and tools - APIs, MCP servers, browsers, retrieval - provide
attributable evidence and controlled external actions within named access.

**Human still does:** Sets access and authority boundaries and decides
consequential external effects.

**Evidence for L5:** Sources, permissions, currentness, failure paths, and audit
evidence are explicit and hold in a representative controlled task. One bounded
end-to-end workflow is worth carrying further, and its runs can be observed,
recovered, and stopped.

**In this catalog:** `scaffold-harness` (context architecture and capability
gates) and `grill-harness-with-docs` for the decisions evidence cannot settle.

## L5 - Stateful workflow

**Means:** A bounded end-to-end workflow keeps state, waits deliberately,
retries, recovers, or stops, without a person scheduling each next step.

**Human still does:** Designs the boundaries and handles exceptions instead of
scheduling every next step.

**Evidence for L6:** Repeated runs are observable, recoverable, reconciled after
missed progress, idempotent where needed, safely stoppable, and evaluated
against outcomes. One delivery domain has stable goals and risk classes,
required checks, executable rollback, production feedback, and an incident
owner.

**In this catalog:** Described here, built with teams. `build-autonomous-agents`
covers one product agent or one finite workflow, a building block of this
level rather than the level itself.

## L6 - Governed value stream

**Means:** The system carries signals within explicit goals and risk limits
through release, production evidence, and the next decision. An agent that can
merge or deploy is not L6 on its own.

**Human still does:** Governs goals and risk, retains veto and incident
authority, and intervenes on exceptions. People move from in the loop to on the
loop only for domains where the controls are proven.

**Evidence for L7:** Isolation, policy and quality gates, rollback, audit,
incident ownership, production feedback, and effective oversight are proven
over repeated runs. One bounded product or investment decision has trusted
signals, a budget, kill criteria, and a stop path.

**In this catalog:** Described here, built with teams. `run-product-engineering`
describes the closed signal-to-outcome loop as a team runs it.

## L7 - Adaptive product system

**Means:** Within a bounded decision domain, the system selects problems,
experiments, and investments from trusted signals and learns from outcomes. It
is not an autonomous company: legal, ethical, employment, security, and
strategic authority is never inferred from technical capability.

**Human still does:** Owns strategy, budgets, decision domains, kill criteria,
and stop authority.

**Evidence that keeps it:** Level 6 controls, trusted product signals, data and
experiment boundaries, budgets, kill criteria, and human-governed investment
decisions stay proven. A breach narrows the domain back to its proven scope.

**In this catalog:** Described here, built with teams. L7 runs today: I operate
my own repositories under an owner-delegated profile, in which agents decide
everything outside a short list of decisions I reserve, and bring those to me as
prepared recommendations.

## Not a status model

Not every piece of work should reach Level 7. A clearly bounded task belongs at
Level 1. A recurring workflow may be complete at Level 5. The highest number is
not the goal; delegation, risk, and evidence need to fit the work.

## Where to start

Teams do not start at Level 7. They start with a recurring constraint, an
explicit boundary, and the smallest level that creates measurable value.

I help teams find the loop they can delegate today and build the next level
from evidence: [daume.dev](https://daume.dev).
