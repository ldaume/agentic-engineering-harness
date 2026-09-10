---
name: testing-strategies
description: Plans pragmatic test coverage across unit, integration, contract, e2e, visual, accessibility, performance, and smoke tests based on risk and behavior. Use when deciding what to test, designing a test pyramid, adding coverage for a feature, reducing flaky tests, or reviewing QA strategy.
---

# Testing Strategies

Use this when the question is not just "write a test" but "what kind of signal
should prove this works?"

Testing starts while framing behavior and risk, not after implementation. Use
examples, experiments, threat or failure models, executable checks, and
production signals as one continuous learning system.

## Project Fit Check

Before planning tests:

1. Read existing test commands, frameworks, CI gates, fixtures, test helpers,
   and coverage conventions.
2. Identify the changed behavior, risk, blast radius, and public interface.
3. Prefer the cheapest test that catches the likely regression.
4. Match the repo's existing layers unless the task is to improve them.
5. Do not chase coverage percentage when behavior risk is elsewhere.

## Risk To Test Mapping

| Risk                         | Best signal                     |
| ---------------------------- | ------------------------------- |
| pure logic                   | unit test                       |
| schema or API contract       | contract/schema test            |
| database/repository behavior | integration test                |
| queue/workflow behavior      | worker or workflow fixture test |
| user journey                 | e2e test                        |
| layout/a11y regression       | browser/accessibility test      |
| deployment boot path         | build or smoke test             |
| auth, permissions, or abuse  | negative + integration test     |
| migration or data integrity  | rehearsal + invariant test      |
| resilience and operability   | failure, load, recovery, or smoke test |
| AI behavior                  | representative eval + guardrail signal |

## Rules

- Test through public interfaces.
- Give behavioral tests explicit Given/When/Then semantics: Given states the
  relevant preconditions, When applies one meaningful stimulus, and Then
  asserts observable behavior. Express this through test names, structure, or
  local helpers; mandatory comments and framework-specific GWT libraries add
  no value.
- Apply the same semantics to contract, property, migration, load, recovery,
  and end-to-end tests: controlled context, action or disturbance, observable
  result or invariant.
- Keep test data explicit and local to the test where possible.
- Mock internals only when the boundary is genuinely external or expensive.
- Synchronize on the work, not on a duration. Where the interface returns
  before the work it started is finished - a response that begins streaming
  while the producer keeps writing, a task that outlives the call - wait for
  that work to complete before asserting. A sleep that passes at 95 ms and
  fails at 100 ms is not a flaky test; it is a deterministic race the machine's
  speed decides, and calling it flakiness sends the fix to the wrong place.
- A negative assertion needs an instrument that would notice the positive.
  "Nothing was fetched" proves nothing when the fake signals the breach by
  throwing and the code under test catches a failure as an ordinary outcome.
  Count the reaches on the fake and assert zero.
- Add regression tests before bug fixes when feasible.
- Define the cheapest decisive signal before or with the behavior it guides;
  do not create a downstream QA handoff.
- Pair pre-release checks with the telemetry and observation window needed to
  detect production-only failure and outcome drift.
- Autonomous gates return bounded, secret-safe, actionable failure context:
  identify the failed boundary, concise safe reason, correlated evidence, and
  retry or rollback decision without exposing secrets, untrusted payloads, or
  unbounded logs.
- A prototype may prove a learning hypothesis with experiment evidence. It
  needs production tests and controls before any code is promoted or rebuilt
  for release.
- Delete or rewrite tests that only assert implementation trivia.
- Track flaky tests as product risk, not background noise.

## Review Checklist

- Does the test fail for the bug or risk it claims to cover?
- Does it still pass if internals are refactored safely?
- Is setup smaller than the behavior under test?
- Is the assertion user-, contract-, or system-visible?
- Can CI run it reliably?

## Red Flags

- coverage added only by testing private helpers
- brittle snapshots for dynamic UI
- mocks that make the real integration untested
- e2e test used where a unit test would be clearer
- no test for auth, migration, or data ownership changes
