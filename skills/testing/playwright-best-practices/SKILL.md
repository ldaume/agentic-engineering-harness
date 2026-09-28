---
name: playwright-best-practices
description: Writes, reviews, and debugs Playwright tests for web apps with stable locators, fixtures, auth setup, API mocking, trace debugging, responsive checks, accessibility assertions, and CI reliability. Use when creating Playwright tests, fixing flaky e2e tests, debugging traces, testing UI flows, or configuring browser tests.
---

# Playwright Best Practices

Use this for browser-level tests that should behave like a reliable user.

## Project Fit Check

Before writing tests:

1. Read existing Playwright config, fixtures, helpers, test ids, auth setup,
   route mocks, and CI commands.
2. Follow the repo's locator strategy.
3. Reuse existing page objects/helpers only when they reduce duplication.
4. Keep assertions tied to user-visible behavior and accessibility semantics.
5. Do not add sleeps to hide race conditions.

## Test Rules

- Prefer role, label, text, and stable test ids over CSS selectors.
- Assert the outcome, not every implementation step.
- Keep tests isolated and repeatable.
- Leaving a page through a client-side navigation is not finished when the
  click returns. Wait for the destination before starting the next navigation:
  a `goto` into a navigation still in flight aborts it, and the failure is
  intermittent, which in a release gate means the gate decides by coin toss.
- Use fixtures for auth and shared setup.
- Mock external services at the boundary when real services make tests slow or
  flaky.
- Keep mobile/responsive tests explicit when layout or touch behavior matters.

## Debugging Flow

1. Reproduce with the smallest test command.
2. Inspect trace, screenshot, console, and network output.
3. Identify whether the failure is product bug, selector drift, async race,
   data setup, browser difference, or environment issue.
4. Fix the cause, not the timeout.
5. Re-run the failed test and any nearby coverage.

## Locator Rules

- Use `getByRole` when semantics are stable and meaningful.
- Use `getByLabel` for form controls.
- Use project test ids for complex widgets or localized copy.
- Avoid nth-child selectors unless testing ordered content explicitly.

## Red Flags

- `waitForTimeout`
- `goto` immediately after a click that navigates
- broad CSS selectors
- tests depend on run order
- production third-party service required for normal CI
- assertion passes before async work completes
- UI changed but accessibility name no longer matches intent
