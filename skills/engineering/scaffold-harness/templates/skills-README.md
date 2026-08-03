# Project Skills

## Shared Harness Workflow

| Skill | Use |
|---|---|
| `scaffold-harness` | Audit or establish the repository harness |
| `grill-harness-with-docs` | Ground, critique, and resolve material decisions |
| `agent-sync` | Evolve durable artifacts across sessions |
| `update-harness` | Reconcile managed versions, scopes, and collisions |
| `write-a-skill` | Create and revise portable Skills across agent hosts |
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

Install the five bootstrap Skills - `scaffold-harness`, `agent-sync`,
`update-harness`, `grill-harness-with-docs`, and `write-a-skill` - into the
effective scope of every agent host used in this repository. Do not assume one
shared directory or one successful host session proves discovery everywhere.
When the host bundles its own Skill creator, keep `write-a-skill` as the
portable owner and use the bundled capability only as a native adapter.

Before calling the bootstrap managed, create or update the target-owned
dependency manifest described by the installed `update-harness` reference.
Record one entry per bootstrap Skill with the exact public source, immutable
per-Skill tag, resolved commit, and effective host targets. Use an equivalent
native lock only when it preserves those guarantees. The one-off command above
is an installation pilot, not the reproducible dependency contract.

The public catalog currently install-tests Codex, Cursor, Claude Code, and
Gemini CLI. Add Pi, CI, or a later runtime to the declared host matrix only
after its native adapter and a representative bootstrap check pass.

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

## Stack Capability Loop

Agents own routine stack resolution; users do not need to select Skills or
translate the repository into framework prompts.

1. Derive the technologies and major versions from manifests, lockfiles,
   runtime output, code, and existing checks.
2. Combine the stack-neutral craft owner with only the technology profiles the
   current task needs. Keep explicit profiles such as pnpm, Playwright, Docker,
   or a monorepo scaffold specific enough to remain useful.
3. Reuse an existing project, private, public, bundled, or plugin Skill when
   its source and behavior fit. Otherwise use `update-harness` to find and
   pilot a current public candidate project-locally.
4. If no candidate passes, complete a one-off directly, even when it is
   difficult or risky. Only repeated work with real examples and checks earns
   a project-local profile through `write-a-skill`.
5. Promote only after reuse proves the audience and provenance: portable
   behavior public, shared non-public behavior private, target semantics local.

Research and reversible pilots stay autonomous. Use fresh-agent critique for
a resolved material choice and human grilling only for unresolved product,
architecture, adoption, authority, security, cost, or risk decisions.
