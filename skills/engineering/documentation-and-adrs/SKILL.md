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
- When a decision lands, re-read the plan documents written before it and
  correct them in the same change. A plan records the state at the time and
  goes stale silently; nothing in the decision record shows which plan it just
  contradicted, so a superseded instruction survives and is followed later as
  if it were current.
- A claim is checked against the system before it is written. A statement
  about behavior names the file that implements it. A number carries the date
  and the command or query that produced it, or says it was reasoned and shows
  the input. A claim you cannot settle without running something you should not
  run is written as unverified, naming what would settle it. When you touch a
  document, re-check the claims about the paths your change touched, not only
  the lines you edit. Every false claim was true when written.
- Reading an artifact is not checking it. A code comment, a docstring or an
  older record that states a mechanism is not evidence - it is where a false
  claim hides best, because it reads exactly like a verified one. So: if you
  cannot name the command that would falsify the sentence, you have not checked
  it, you have read something. Run it - the grep for a retired symbol, the
  query behind a count, the conversion behind a schema claim - and say in the
  change which claims you ran what against. A reviewer aimed at named claims
  re-derives; an unaimed one reads.
- A diagram is checked by rendering it, not by reading it. Diagram grammars
  reserve words that look like ordinary node ids - in Mermaid's flowchart
  `call` parses as a callback name and fails the whole graph, and `end`,
  `class`, `click`, `style`, `graph` and `subgraph` behave the same way - so a
  diagram that reads correctly in the diff can render as nothing at all. Check
  the grammar outside the repository, so it needs no diagram tooling of its
  own: install `mermaid` and `jsdom` in a scratch directory, put a JSDOM window
  on `globalThis` before importing mermaid, and call `mermaid.parse()` on each
  fenced block. Whether the result is readable is a separate question and needs
  a real browser - JSDOM has no `CSSStyleSheet`, so `mermaid.render()` throws
  on it, and a browser driver refuses a `file:` URL, so serve the scratch
  directory over localhost.
- A document that has outgrown its purpose is deleted, not maintained. Length
  is a defect of its own: nobody re-reads what they cannot finish, and the part
  nobody reaches is where stale claims survive. Version control is the archive.

## Red Flags

- doc repeats code or config verbatim
- decision has no alternatives or consequences
- runbook has no verification or rollback
- a claim in a doc is not true of the code, or cannot be checked at all
- no command would falsify the sentence, so nothing ever will
- a document is kept because deleting it feels lossy, not because it is read
- a diagram was checked by reading it, so nobody knows whether it renders
- documentation is added only to make a small change look larger
