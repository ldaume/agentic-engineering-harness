---
name: coding-discipline
description: Enforces clarity, surgical diffs, simplicity, and goal-driven TDD for any codebase. Use when implementing features, fixing bugs, refactoring, or making any code change.
---

# Coding Discipline

**Prime directive:** clarity, safe change, bounded impact. Small localized
diffs. Investigate discoverable facts; ask when intent, authority, domain
semantics, or material impact remain unresolved.

Bias toward caution over speed. Use judgment on trivial tasks.

## Project Fit Check

Before changing code:

1. Read the repo's local instructions: `AGENTS.md`, `CLAUDE.md`,
   `.cursor/rules/`, `README.md`, contributing docs, or equivalents.
2. Detect the package manager, formatter, linter, test runner, language level,
   and branch/worktree conventions from project files before choosing commands.
3. Match existing architecture, naming, test style, and error-handling patterns
   in the touched area.
4. If project rules conflict with this skill, follow the project rules and tell
   the user about the trade-off when it matters.
5. If expected agent docs are missing and the task is non-trivial, suggest
   **scaffold-harness** or adapt to the repo's existing docs.

## Think before coding

- State material assumptions explicitly.
- If multiple consequential interpretations remain after investigation, present
  them with a recommendation - do not pick silently.
- Name simpler approaches and push back when warranted.
- Stop before the dependent change when uncertainty cannot be resolved safely.

## Simplicity first

- Reuse the owning implementation or established repository pattern when it
  already fits.
- Prefer the language standard library, native platform behavior, or an
  installed dependency over new code or another dependency.
- Add only the minimum code for the requested problem. No speculative features,
  abstractions, or configuration.
- Prefer correction, consolidation, or deletion over another layer.
- Do not simplify away input validation at trust boundaries, security,
  accessibility, data integrity, necessary recovery, or error handling.
- Self-check: _Would a senior engineer call this overcomplicated?_ If yes,
  simplify.

## Language

- Follow the target repository's language and audience rules.
- When no rule exists, preserve the language and terminology of the touched
  area. Do not translate product copy, documentation, or tests incidentally.

## Surgical changes

- Touch only what the request requires.
- Do not refactor, reformat, or "improve" adjacent code.
- Match existing style and patterns in the touched area.
- Unrelated dead code: mention it - do not delete unless asked.
- Remove only imports/symbols **your** diff made unused.
- Every changed line should trace to the user's request.

## Goal-driven execution

| Request        | Success criteria                        |
| -------------- | --------------------------------------- |
| Add validation | Tests for invalid inputs pass           |
| Fix bug        | Failing test reproduces it, then passes |
| Refactor       | Tests pass before and after             |

Multi-step work: brief plan as `[Step] -> verify: [check]`.

## TDD

Tests are design feedback, not a phase after implementation. Use vertical
slices - one behavior test, minimal implementation, repeat. If the repo has a
**tdd** skill, follow it.

- Test through **public interfaces** (API routes, package exports, user-visible behavior).
- Name behavior in the target's domain language; keep examples, tests, code,
  and public contracts aligned.
- Do not mock internals; do not test private helpers in isolation.
- Match test type to risk: unit for logic, integration/e2e for user flows (per `AGENTS.md`).
- For a disposable spike whose purpose is learning, use a hypothesis, timebox,
  and exit decision instead of pretending it is production code. Discard it or
  restart the production slice from public behavior with tests.

## Quality mindset

- Understand the problem before choosing a solution; assess value and risk
  before estimating effort.
- For bugs, reproduce the failure, trace callers and shared ownership, and fix
  the root cause at the narrowest common boundary.
- Quality at the start: acceptance criteria and tests - not late inspection.
- Readable over clever; abstractions only when they remove real complexity.
- Direct communication: name trade-offs, constraints, and next step.

## Optional Complement

Use the upstream
[`ponytail`](https://github.com/DietrichGebert/ponytail) Skill only when repeated
overengineering justifies a stronger implementation-style guardrail and the
target host has passed a representative pilot. It complements this workflow; it
does not override target instructions or the safeguards above.

## Working signal

Fewer unnecessary diff lines, fewer rewrites from over-engineering, clarifying questions **before** implementation.
