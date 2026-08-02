# Engineering skills

Core workflow skills for AI-assisted development. Use together:

1. **scaffold-monorepo** - optional greenfield pnpm toolchain (CI, Renovate, verify)
2. **scaffold-harness** - establish or repair the repository harness
3. **build-autonomous-agents** - implement a bounded agent workload after the
   runtime gate passes
4. **scaffold-distributed-context** - add cross-repository domain context only
   when the system spans repositories or bounded contexts
5. **coding-discipline** - during implementation
6. **completion-gate** - before claiming done
7. **agent-sync** - evolve the harness during significant work
8. **update-harness** - check or apply explicit harness and Skill updates

Use **grill-harness-with-docs** to establish shared understanding, route
resolved material work through fresh-agent critique, and keep a human in the
loop only when evidence cannot resolve a material decision.

| Skill                                                       | Triggers                                                   |
| ----------------------------------------------------------- | ---------------------------------------------------------- |
| [coding-discipline](./coding-discipline/SKILL.md)           | implement, fix, refactor, any code change                  |
| [completion-gate](./completion-gate/SKILL.md)               | done, commit, PR, ship, finish                             |
| [build-autonomous-agents](./build-autonomous-agents/SKILL.md) | agent, workflow, CI agent, overnight agent, Flue          |
| [learn-agentic-engineering](./learn-agentic-engineering/SKILL.md) | learn, teach, coach, question, blocker, maturity path    |
| [agent-sync](./agent-sync/SKILL.md)                         | review loops, currentness, learnings, harness evolution     |
| [update-harness](./update-harness/SKILL.md)                 | resolve, install, update, clean Skill scopes, Renovate PR   |
| [scaffold-harness](./scaffold-harness/SKILL.md)             | bootstrap, audit, local/MCP context, context economy, cross-repo harness |
| [scaffold-distributed-context](./scaffold-distributed-context/SKILL.md) | bounded contexts, contracts, projections, Graphify |
| [grill-harness-with-docs](./grill-harness-with-docs/SKILL.md) | shared understanding, material critique, unresolved decision |
| [write-a-skill](./write-a-skill/SKILL.md)                   | create skill, SKILL.md, skill frontmatter, skills CLI      |
| [documentation-and-adrs](./documentation-and-adrs/SKILL.md) | ADRs, runbooks, public API docs, durable decisions         |
| [pnpm](./pnpm/SKILL.md)                                     | pnpm workspaces, lockfiles, Corepack, overrides, patches   |
| [scaffold-monorepo](./scaffold-monorepo/SKILL.md)           | new monorepo, pnpm workspaces, CI, Renovate, quality gates |

Pair **coding-discipline** with an installed **tdd** skill when one exists.
Prefer the upstream
[mattpocock/skills `tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)
over copying it into this repository.

Use the upstream
[mattpocock/skills `domain-modeling`](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling)
when shared domain language is unresolved. Use
**scaffold-distributed-context** for the repository boundaries, contracts,
projections, and retrieval architecture around that language.

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
