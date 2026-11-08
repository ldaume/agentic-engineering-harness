# Changelog

Each Skill is versioned independently. Release notes live in [GitHub Releases](https://github.com/ldaume/agentic-engineering-harness/releases);
current versions live in [`skills-lock.json`](./skills-lock.json). See
[`VERSIONING.md`](./VERSIONING.md).

## Unreleased

- `scaffold-harness` 3.1.0: scaffolds a multi-repository workspace as well as one repository - a workspace root `AGENTS.md`, a coordinator with `CONTEXT-MAP.md`, `SYNC.md` (working root, admission, sibling awareness, fan-out, write-back), and `STATUS.md` (worktree leases), and a member snippet every member's `AGENTS.md` carries; the template `HARNESS.md` gains **Repository and Team Topology** and a **Leases** item. Single-repository use is unchanged.
- `agent-sync` 2.1.0: routes workspace-wide rules and lessons to the coordinator per its `SYNC.md` **Write-back**, and membership and contracts to its `CONTEXT-MAP.md`.
- `deliver-dependency-upgrades` 1.2.0: a compiler, runtime, or framework major counts as admissible only when the tools that wrap it (type checkers, lint plugins, test runners, framework checkers) accept it in their registry peer ranges; when one excludes it, the decision is `defer` with the blocking peer and what would lift it.
- `completion-gate` 1.9.0: the merge gate refuses a green pull request whose diff adds a git conflict marker (exit 5) and fails closed when gh cannot provide the diff; a bare required name matches a check's job part, skipped checks are neutral, and a refusal lists every check seen per required name.
- `shift-left-security` 1.0.0: security from the first line of a change - threat note, abuse-case test first, the platform's safe default (shift down), the control at the owning boundary, sessions and tokens, dependency verification and cooldowns, CI script injection and OIDC, zero trust paths, agent and MCP features, rules for the agent itself, and a list of retired folklore, backed by a 36-source registry opened on 2026-10-26.
