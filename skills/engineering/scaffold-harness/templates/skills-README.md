# Project Skills

## Shared Harness Workflow

| Skill | Use |
|---|---|
| `scaffold-harness` | Audit or establish the repository harness |
| `grill-harness-with-docs` | Resolve uncertain harness decisions |
| `agent-sync` | Evolve durable artifacts across sessions |
| `coding-discipline` | Make minimal implementation changes |
| `completion-gate` | Verify before completion |

Install one selected Skill from the approved public or private source:

```bash
npx skills add <approved-source> --skill <skill-name> --agent <tool> --copy
```

This command is a targeted install, not a reproducible dependency contract.
For repeated managed dependencies, record the immutable ref and resolved commit
in the target-owned manifest and update it through `update-harness`. Add
repository-specific Skills here only for repeated local workflows.

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

Resolve target semantics from project-local Skills or wrappers. Consume shared
non-public procedures from an approved organization or team catalog and
portable methods from a pinned public upstream. Keep only the discovery and
maintenance bootstrap global. Inspect the active host's real precedence and
select one owner per procedure.

For a missing public candidate, include the target technology and major version
in discovery, inspect compatibility and permissions, and install it
project-locally only when harness changes are authorized. Use an installed
upstream `find-skills` or `npx skills find` when no named complement fits.
Optional style guardrails such as upstream `ponytail` are not additional
delivery stages. Keep local wrappers outside managed dependencies and do not
copy public Skill text into the repository.
