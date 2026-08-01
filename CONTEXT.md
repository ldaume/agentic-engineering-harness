# Repository Context

## Terms

- **Skills repository:** This portable, versioned source of reusable
  capabilities and harness blueprints.
- **Target repository:** One repository whose local harness is being built or
  evolved. It owns its product and engineering truth.
- **Coordinating repository:** A separate working root for a system spanning
  multiple repositories. It owns only cross-repository relationships, public
  contracts, shared workflow state, and cross-cutting verification.
- **Harness:** The smallest system of context, capabilities, feedback, and
  governance that makes delegated work reliable.
- **Currentness evidence:** Dated, sourced evidence for volatile model, cost,
  platform, security, or community claims.
- **Agent context architecture:** The placement, retrieval, freshness, shape,
  persistence, authority, and cost of evidence and capabilities available to
  agents.
- **Context economy:** The cost, latency, and risk of supplying sufficient
  evidence to complete a task correctly.
- **Fast Check:** The narrowest real command that gives useful feedback for the
  current change.
- **Full Gates:** The repository's broader checks required before integration.

## Invariants

- Portable Skills remain repository- and customer-agnostic.
- Target repository language and audience rules outrank portable defaults.
- Target-local truth stays in the target repository.
- Cross-repository coordination does not override local instructions.
- The lowest reliable delegation level is preferred.
- Agent-native structures may differ from human handbooks, but must remain
  inspectable while humans retain oversight.
- Skills guide probabilistic behavior; Hooks, CI, tests, and platform controls
  enforce deterministic guarantees.
- Volatile claims are discovered at decision time rather than frozen into
  static model or price tables.
- Token count is not optimized independently of task success, grounding,
  verification, or recovery.
- MCP makes external resources and tools reachable; it does not replace local
  source routing, persistence, authorization, or context selection.
- Human accountability and veto remain until evidence supports a narrower
  human-on-the-loop role.
