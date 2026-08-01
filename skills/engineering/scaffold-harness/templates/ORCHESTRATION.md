# Agent Orchestration Policy

Create this artifact only for repeated multi-agent, model-routed, or
cross-repository work. Discover the live host before filling it.

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
