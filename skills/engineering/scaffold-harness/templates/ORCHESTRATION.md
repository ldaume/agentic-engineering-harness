# Agent Orchestration Policy

Create this artifact only for repeated multi-agent, model-routed, or
cross-repository work. Discover the live host before filling it.

Keep capability tiers stable and model mappings replaceable. The same task
class must retain its quality and verification floor when a session moves
between Codex, Claude Code, Cursor, Gemini CLI, Pi, CI, or a later host.

## Scope and Oversight

- **Workflow:** `<bounded workflow or task class>`
- **Operating level:** `<L3-L7>`
- **Human oversight:** `<human-in-the-loop or human-on-the-loop>`
- **Veto boundary:** `<material branches requiring explicit acceptance>`
- **Permissions and blast radius:** `<repositories, tools, external writes>`

## Parent

- **Responsibilities:** frame, decompose, route risk, integrate, verify, report
- **Selection rule:** current capable model proven for ambiguity and synthesis
- **Stop conditions:** `<uncertainty, budget, failed eval, authority boundary>`

## Workers

| Task class | Required capability | Allowed tools and scope | Verification | Cost/latency limit |
|---|---|---|---|---|
| `<bounded task>` | `<capability>` | `<least privilege>` | `<test or evidence>` | `<local limit>` |

Use the least expensive worker that meets the required quality. Include retry,
review, latency, and failure impact in total cost. Do not delegate when
coordination costs more than the work.

Map provider models to three roles from current evidence:

- **Fast:** clear, repeatable, high-volume extraction, mapping, or mechanical
  checks.
- **Balanced:** bounded implementation, research, debugging, and normal review
  that still need sound reasoning and tools.
- **Frontier:** ambiguous decomposition, consequential synthesis, or material
  critique where a weaker result would create meaningful rework or risk.

Default spawned workers to Fast or Balanced rather than inheriting the parent's
Frontier model. Escalate after a representative failure or when the task crosses
the documented risk boundary. A Frontier reviewer may critique material output
from cheaper workers; routine green-path review does not require Frontier by
default. Independence still requires fresh context and evidence, not merely a
different model name.

## Host Adapters

Map every active host independently through its native controls:

| Host and surface | Native model control | Fast | Balanced | Frontier | Checked and re-check |
|---|---|---|---|---|---|
| `<host, app, CLI, SDK, or CI>` | `<per-call, agent file, settings, router, or unavailable>` | `<alias or ID>` | `<alias or ID>` | `<alias or ID>` | `<date; catalog, plan, quality, price, or host trigger>` |

Prefer a provider-maintained rolling alias when it preserves the intended tier
and automatic upgrades are acceptable. Pin an exact model ID when reproducible
behavior matters. A newly released or cheaper model starts as a candidate: run
representative work, compare total cost and failure behavior, then promote,
hold, or reject it. Never promote it because its name or benchmark is newer.

Record both the requested and resolved model when the host exposes that
telemetry. A host fallback may stay automatic only while it preserves the task's
minimum tier. Stop or re-route material work after an unverified downgrade.

If the host cannot override a subagent model, either accept inheritance as an
explicit cost decision or use a separate native session/runtime with the same
scope and checks. Do not claim cost-aware routing that the live host cannot
enforce.

## Review and Integration

- Self-review: `<trigger and check>`
- Independent review: `<risk trigger and reviewer independence>`
- Cross-repository contract check: `<command or source>`
- Recovery and rollback: `<mechanism>`

## Current Evidence

| Checked at | Host/version/plan | Official source | Candidate | Local evidence | Decision | Re-check |
|---|---|---|---|---|---|---|
| `<timestamp>` | `<environment>` | `<URL or live schema>` | `<alias or ID>` | `<eval, tokens, latency, failures>` | `<route>` | `<event or expiry>` |

Do not copy complete provider price tables. Keep only evidence that explains a
current decision.
