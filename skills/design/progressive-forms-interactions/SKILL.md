---
name: progressive-forms-interactions
description: Use whenever designing, building, fixing, or reviewing a form or an input-heavy interaction - sign-up, login, checkout, settings forms, multi-step forms, validation and error messages, submit buttons, autosave and drafts, destructive actions, undo, optimistic UI, double submits (Formular, Validierung, Fehlermeldung, Registrierung, Checkout). Decides validation timing, error recovery, focus, and status announcements, and ships browser tests for them. Not for whole user flows across screens, which progressive-user-flows owns.
license: MIT
---

# Progressive Forms and Interactions

Make every input recoverable: a person who makes a mistake learns what
happened, where, and how to fix it, without losing what they typed. Decide
each pattern from the person's task and the evidence, not from habit,
because the most common form defects are inherited defaults (a disabled
submit, errors on focus) that nobody chose.

## Golden path

1. Name the task and cut the form to the inputs it needs, because field count
   drives checkout abandonment more than step count (supported) [SRC-A11Y-012].
2. Give every field a visible label, a hint where the format is not obvious,
   the right `type`, `inputmode`, and `autocomplete` token, because autofill
   is a WCAG requirement (1.3.5) and blocking paste or managers fails 3.3.8
   (verified) [SRC-A11Y-017] [SRC-A11Y-019].
3. Choose validation timing with `references/forms.md` (decision table).
   Default: no message while typing, validate on blur after the first edit,
   re-check per keystroke while in error, always validate on submit
   (context-dependent) [SRC-A11Y-011] [SRC-A11Y-014].
4. Keep submit enabled and explain on click, unless the decision table names
   your case, because a disabled button hides the reason and is often
   unreachable by keyboard (context-dependent; expert consensus, no
   controlled study) [SRC-A11Y-004] [SRC-A11Y-013] [SRC-A11Y-015].
5. On a failed submit keep every value, prefix the title with "Error: ", show
   an error summary that links to each field and takes focus, and repeat the
   same wording at each field (supported) [SRC-A11Y-003] [SRC-A11Y-005]
   [SRC-A11Y-009].
6. While sending, change the label, ignore a second activation, keep the
   button focusable, and make the endpoint idempotent, because a disabled
   button drops focus mid-submit (supported) [SRC-A11Y-004] [SRC-A11Y-016].
7. Announce results that do not move focus in a `role="status"` region;
   the requirement is WCAG 4.1.3 (verified) [SRC-A11Y-023]; reserve
   `role="alert"` for blocking errors that do not move focus (supported)
   [SRC-A11Y-022].
8. Plan failure: server error, timeout, offline, session expiry. Input
   survives every one of them; a long form saves a draft (never secrets).
9. Destructive actions: undo when reversible, a specific confirmation naming
   the object when not (context-dependent) [SRC-A11Y-025] [SRC-PROD-008].
10. Verify in a real browser with the test pattern below, then check the
    manual list.

## Load when

- `references/forms.md` - always for a form: the 13-question decision model,
  validation timing table, error message rules, multi-step and save-and-resume.
- `references/interaction-patterns.md` - for optimistic UI, autosave, undo,
  confirmation, destructive actions, double-submit prevention, status
  announcements outside forms.

## Gates

Automated, in a real browser: `tests/registration.spec.mjs` with
`tests/playwright.config.mjs` exercises `examples/registration/index.html`,
a reference form built from this golden path: empty submit, invalid email,
timing, kept values, success announcement, double submit, server error and
retry, timeout, keyboard-only, autocomplete, draft after reload, overflow at
360/768/1280 px, and axe WCAG 2.2 A/AA in empty and error states. Run with
`npx playwright test -c <skill>/tests` after installing `@playwright/test`
and `@axe-core/playwright`. Copy the spec's shape for the form you build.

Manual, because automation cannot judge it: the wording of each message,
screen reader announcement order (test with VoiceOver or NVDA), the 2.4.11
check that sticky UI never hides the focused field, and whether a field is
really needed. axe states it finds about 57% of WCAG issues [SRC-TOOL-001]; treat its
`incomplete` results as a manual list.

## Done when

The decision for submit state, validation timing, and failure handling is
written down with its evidence level, the browser tests for those decisions
pass, and the manual list is checked or handed over by name.
