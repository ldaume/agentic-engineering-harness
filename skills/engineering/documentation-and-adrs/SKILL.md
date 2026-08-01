---
name: documentation-and-adrs
description: Writes and updates durable project documentation, decision records, runbooks, and architecture notes for a clear reader or operational purpose. Use when making architecture decisions, changing public APIs, adding operational procedures, documenting trade-offs, or deciding whether a change needs an ADR.
---

# Documentation And ADRs

Use this when a decision or workflow must survive beyond the current chat.

## Project Fit Check

Before writing docs:

1. Read existing documentation structure: `docs/`, `docs/adr/`, `README.md`,
   `AGENTS.md`, `CONTEXT.md`, runbooks, and contributing docs.
2. Follow local naming, numbering, status, and index conventions.
3. Update existing docs before creating new ones when the topic already exists.
4. Do not create an ADR for trivial implementation details.
5. If there is no durable doc structure, suggest the smallest useful file.

## When To Write

Write durable docs for:

- architecture choices with real alternatives
- public API or data contract changes
- deployment, migration, rollback, or incident procedures
- security, privacy, or compliance decisions
- repeated workflows that multiple agents or humans need
- domain vocabulary that affects tests, UI copy, or architecture

## ADR Shape

```markdown
# NNNN Decision Title

## Status

Accepted | Proposed | Superseded

## Context

## Decision

## Consequences

## Alternatives Considered

## Follow-ups
```

## Writing Rules

- Prefer short, specific docs over sweeping essays.
- Capture why, not every implementation detail.
- Link to code, issues, PRs, or configs instead of duplicating them.
- Name trade-offs plainly.
- Keep runbooks actionable with commands, prerequisites, rollback, and
  verification.
- Update indexes and agent docs when discoverability matters.

## Red Flags

- doc repeats code or config verbatim
- decision has no alternatives or consequences
- runbook has no verification or rollback
- old docs conflict with new behavior
- documentation is added only to make a small change look larger
