# Agent Tool Entrypoints

Create this file only when several tools need different bridges.

| Tool | Instruction entrypoint | Skill location | Notes |
|---|---|---|---|
| Cursor | `AGENTS.md` or scoped Rules | `.agents/skills/` | Add Hooks only for observed deterministic needs |
| Codex | `AGENTS.md` | `.agents/skills/` or installed Skills | Keep local overrides untracked |
| Claude Code | `CLAUDE.md` bridge | `.claude/skills/` or `.agents/skills/` | Reference canonical instructions |
| Gemini CLI | configured context file | installed or project Skills | Verify current model and instruction precedence; reference canonical instructions |
| Google Antigravity | product-specific context or Skill bridge | project or installed Skills | Discover the active application, IDE, CLI, or SDK surface; do not assume Gemini CLI behavior |
| Pi coding agent | project or user instruction and Skill bridge | project or user Skills | Verify current extension, tool, and prompt loading behavior |
| CI workflow | workflow plus bounded workload contract | repository-owned scripts, Skills, or code | Use native runner controls before adding a framework |
| Flue runtime | bounded workload contract plus Flue adapter | repository-owned workload Skills or code | Add only after the runtime gate; verify non-interactive permissions, secrets, cancellation, gates, telemetry, and evidence |

The bridges point to host-neutral owning sources; they do not duplicate them.
For each active host, record effective precedence, supported native controls,
the smallest adapter, a representative verification, and a re-check trigger.
Plugins, Skills, Rules, Hooks, MCP servers, and runtime configuration remain
host adapters unless the repository explicitly assigns them another ownership
role.

For every MCP server, record the required resources, prompts, or tools, source
authority, freshness evidence, permissions, local projection if any, and the
approval boundary for external actions.

When a context filter or compression layer is present, record the exact data
path, owner, passthrough or removal path, privacy boundary, and verification.
Use one owner for each output path.
