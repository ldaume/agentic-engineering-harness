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
2. Locate by test id (see Locator Rules); keep any older role, label, or text
   locators only in specs you are not touching.
3. Reuse existing page objects/helpers only when they reduce duplication.
4. Keep assertions tied to user-visible behavior; cover accessibility with
   explicit checks, not through locators.
5. Do not add sleeps to hide race conditions.

## Test Rules

- Locate every element by `data-testid` with `getByTestId`, never by role,
  label, text, or CSS.
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

- Use `getByTestId` only. A test id survives copy edits, translation, theme,
  and layout changes; role, label, text, and CSS locators break on each.
- Name ids by what the element is, stable and meaningful: `row-<id>` for an
  item in a list, `account-menu`, `submit-order`, `error-banner`. Describe the
  purpose, not the position, style, or copy. Never `div-3` or `blue-button`.
- Ask for the id in the markup change that adds the control; do not fall back
  to a text locator while it is missing.
- Avoid `nth` unless testing ordered content explicitly; prefer an id that
  carries the item's key.
- A spec touched for any reason moves its locators to test ids.

## Accessibility Coverage

Locators no longer prove role or name, so check them on purpose:

- Run an axe scan (`@axe-core/playwright`) over every reachable state: dialog,
  toast, error, empty, loading.
- Assert role and name explicitly where they are the contract, for example
  `await expect(page.getByTestId('account-menu')).toHaveRole('button')` and
  `toHaveAccessibleName(...)`. These are assertions, never locators.

## Red Flags

- `waitForTimeout`
- `goto` immediately after a click that navigates
- `getByRole`, `getByLabel`, `getByText`, or CSS used as a locator
- tests depend on run order
- production third-party service required for normal CI
- assertion passes before async work completes
- accessibility covered only by locators, with no axe scan or role/name assertion
