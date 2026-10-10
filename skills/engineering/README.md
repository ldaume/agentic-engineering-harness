# Engineering skills

Core workflow skills for AI-assisted development. Use together:

1. **scaffold-monorepo** - optional greenfield pnpm toolchain (CI, Renovate, verify)
2. **scaffold-harness** - establish or repair the repository harness
3. **build-autonomous-agents** - implement a bounded product agent or workflow
4. **start-gate** - before the first edit of a task
5. **coding-discipline** - during implementation
6. **completion-gate** - before claiming done
7. **agent-sync** - evolve the harness during significant work
8. **update-harness** - check, install, update, or clean managed Skills

Use **grill-harness-with-docs** to establish shared understanding, route
resolved material work through fresh-agent critique, and keep a human in the
loop only when evidence cannot resolve a material decision.

| Skill                                                       | Triggers                                                   |
| ----------------------------------------------------------- | ---------------------------------------------------------- |
| [start-gate](./start-gate/SKILL.md)                         | start a task, resume a session, branch, worktree, unknown tree state |
| [coding-discipline](./coding-discipline/SKILL.md)           | implement, fix, refactor, any code change                  |
| [completion-gate](./completion-gate/SKILL.md)               | done, commit, PR, ship, finish                             |
| [deliver-dependency-upgrades](./deliver-dependency-upgrades/SKILL.md) | dependency bump, Renovate PR, upgrade migration, rollout, rollback |
| [build-autonomous-agents](./build-autonomous-agents/SKILL.md) | product agent, finite workflow, tool, subagent, Flue      |
| [learn-agentic-engineering](./learn-agentic-engineering/SKILL.md) | learn, teach, coach, question, blocker, maturity path    |
| [agent-sync](./agent-sync/SKILL.md)                         | session start, learnings, harness evolution                 |
| [update-harness](./update-harness/SKILL.md)                 | check, install, update, clean project Skills, Renovate PR   |
| [scaffold-harness](./scaffold-harness/SKILL.md)             | bootstrap, audit, operating level, context economy, one repository |
| [grill-harness-with-docs](./grill-harness-with-docs/SKILL.md) | shared understanding, material critique, unresolved decision |
| [write-a-skill](./write-a-skill/SKILL.md)                   | create skill, SKILL.md, skill frontmatter, skills CLI      |
| [documentation-and-adrs](./documentation-and-adrs/SKILL.md) | ADRs, runbooks, public API docs, durable decisions         |
| [pnpm](./pnpm/SKILL.md)                                     | pnpm workspaces, lockfiles, Corepack, overrides, patches   |
| [scaffold-monorepo](./scaffold-monorepo/SKILL.md)           | new monorepo, pnpm workspaces, CI, Renovate, quality gates |

Retired from this catalog. The last public tag stays installable by pin and is
no longer maintained:

| Skill | Status |
| --- | --- |
| system-one-routing | retired, last public tag `system-one-routing-v1.5.0` |
| scaffold-distributed-context | retired, last public tag `scaffold-distributed-context-v1.2.0` |

Pair **coding-discipline** with an installed **tdd** skill when one exists.
Prefer the upstream
[mattpocock/skills `tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)
over copying it into this repository.

Use the upstream
[mattpocock/skills `domain-modeling`](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling)
when shared domain language is unresolved.

Adjacent craft skills:

- [product-craft](../product/product-craft/SKILL.md) - product strategy,
  discovery, bets, outcomes, AI-native operating model
- [frontend-craft](../frontend/frontend-craft/SKILL.md) - UX/UI, responsive
  product surfaces, copy, accessibility
- [backend-craft](../backend/backend-craft/SKILL.md) - TypeScript boundaries,
  APIs, PocketBase, Flue, BullMQ, workers
- [gitea-actions](../infrastructure/gitea-actions/SKILL.md) and
  [multi-stage-dockerfile](../infrastructure/multi-stage-dockerfile/SKILL.md) -
  CI/CD and deployment-adjacent infrastructure work
