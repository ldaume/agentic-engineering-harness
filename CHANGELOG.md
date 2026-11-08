# Changelog

Each Skill is versioned independently. Release notes live in [GitHub Releases](https://github.com/ldaume/agentic-engineering-harness/releases);
current versions live in [`skills-lock.json`](./skills-lock.json). See
[`VERSIONING.md`](./VERSIONING.md).

## Unreleased

- `deliver-dependency-upgrades` 1.2.0: a compiler, runtime, or framework major counts as admissible only when the tools that wrap it (type checkers, lint plugins, test runners, framework checkers) accept it in their registry peer ranges; when one excludes it, the decision is `defer` with the blocking peer and what would lift it.
- `completion-gate` 1.9.0: the merge gate refuses a green pull request whose diff adds a git conflict marker (exit 5) and fails closed when gh cannot provide the diff; a bare required name matches a check's job part, skipped checks are neutral, and a refusal lists every check seen per required name.
- `shift-left-security` 1.0.0: security from the first line of a change - threat note, abuse-case test first, the platform's safe default (shift down), the control at the owning boundary, sessions and tokens, dependency verification and cooldowns, CI script injection and OIDC, zero trust paths, agent and MCP features, rules for the agent itself, and a list of retired folklore, backed by a 36-source registry opened on 2026-10-26.
