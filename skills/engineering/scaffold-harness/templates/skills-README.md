# Project Skills

## Shared Harness Workflow

| Skill | Use |
|---|---|
| `scaffold-harness` | Audit or establish the repository harness |
| `grill-harness-with-docs` | Resolve uncertain harness decisions |
| `agent-sync` | Evolve durable artifacts across sessions |
| `coding-discipline` | Make minimal implementation changes |
| `completion-gate` | Verify before completion |

Install from the shared Skills repository:

```bash
npx skills add /path/to/local/skills --agent <tool> --copy
```

Add repository-specific Skills here only for repeated local workflows.

## Goal Routing

Agents infer the goal and current lifecycle stage, then select the smallest
useful loop. Users do not need to name Skills.

| Goal | Typical route |
|---|---|
| One bounded question | direct repository work; no Skill by default |
| Bounded implementation | relevant craft Skill -> `coding-discipline` -> `completion-gate` |
| Bug investigation | installed diagnostic Skill -> implementation loop |
| Repository harness | `scaffold-harness` -> `agent-sync` after evidence-producing work |
| Cross-repository change | `scaffold-distributed-context` -> repository-local loops |
| Product lifecycle | `run-product-engineering` -> current-stage Skills |
| Confirmed control scope | `integrate-product-compliance` inside the product loop |
| Autonomous workload | runtime gate -> `build-autonomous-agents` |

Resolve project-local Skills first, then installed user or global Skills, then
trusted public candidates. For a missing public candidate, include the target
technology and major version in discovery, inspect compatibility and
permissions, and install project-locally only when harness changes are
authorized. Use an installed upstream `find-skills` or `npx skills find` when
no named complement fits. Compare overlapping workflow collections and select
one owner per procedure. Optional style guardrails such as upstream `ponytail`
are not additional delivery stages. Do not copy public Skill text into the
repository.
