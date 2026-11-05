# Golden Path: Forms

## Intent

Get correct input from a person with the least effort and no lost work, and
make every error recoverable by keyboard, screen reader, and touch.

## Decision model

Answer these for each form before choosing a pattern; each answer changes the
design, which is why none of them has a fixed default.

1. What is the person trying to finish, and what happens right after?
2. Which inputs are really required now? Defer or derive the rest
   (supported) [SRC-A11Y-012].
3. When can the system detect each error reliably - on the client, only on
   the server, only after a slow check?
4. When does feedback help, and when does it interrupt? (table below)
5. What happens on submit with invalid data? (summary + focus)
6. Does the message say what happened and how to fix it?
7. Can the person fix it right there, with their input kept?
8. Where does focus go after submit, after a fix, after a dialog closes?
9. Is every status change perceivable without sight (4.1.3)?
10. Can the person lose data (reload, timeout, back button, crash)?
11. What happens on a network error or timeout?
12. How is a double submission prevented?
13. Does it work with keyboard only, touch, zoom to 200%, and a mobile
    keyboard of the right type?

## Submit button state

| Situation | Pattern | Evidence |
|---|---|---|
| Several fields, any non-obvious requirement | Enabled; validate on click; summary + focus | context-dependent [SRC-A11Y-004] [SRC-A11Y-013] [SRC-A11Y-015] |
| One required choice not yet made, nothing else on the step | May be disabled with `aria-disabled="true"` (stays focusable), a visible reason, readable contrast, action blocked in code | context-dependent [SRC-A11Y-007] [SRC-A11Y-016] |
| Request in flight | Label changes ("Creating account..."), second activation ignored, button stays focusable; idempotent endpoint | supported [SRC-A11Y-004] [SRC-A11Y-016] |
| Person lacks permission | Hide or explain; never a silent disabled control | hypothesis |

Counter-evidence kept visible: USWDS ships disabled styling and NN/g
documents "inactive until required fields are filled" as a normal state
without criticism [SRC-A11Y-007] [SRC-A11Y-010]. Neither claims it helps; no
controlled study compares completion rates. The case against disabling rests
on checkable mechanisms: native `disabled` removes the button from the tab
order, inactive controls are exempt from contrast rules, and the person
cannot learn what is missing.

## Validation timing

| Field kind | Timing | Evidence |
|---|---|---|
| Required text, email, name | Blur after the first edit; per keystroke while in error; on submit | context-dependent [SRC-A11Y-011] |
| Strict formats (date, IBAN, postcode) | Blur; accept variants and normalize; show a positive confirmation once valid | supported [SRC-A11Y-011] [SRC-A11Y-024] |
| Password strength | Live hint, not an error, while typing | hypothesis |
| Server-only checks (username taken) | After blur with a short debounce, or on submit; say it is checking | hypothesis |
| Long multi-step forms | On "continue" per step; never re-ask data given earlier (3.3.7) | verified [SRC-A11Y-001] |

Never validate on focus or before the person has typed, and clear an error on
the keystroke that fixes it (supported) [SRC-A11Y-011]. Contested: Adam
Silver argues for submit-only validation [SRC-A11Y-014], Baymard's moderated
checkout testing favors inline validation done as above [SRC-A11Y-011]. The
default here follows Baymard because its evidence is a larger observed study;
choose submit-only for short forms where inline messages would flicker.

## After a failed submit

1. Keep every value, because retyping is where people give up
   (supported) [SRC-A11Y-005].
2. Prefix the document title with "Error: " (supported) [SRC-A11Y-003].
3. Render an error summary at the top: heading "There is a problem", one
   link per error, the link text equal to the field message; focus the
   summary (supported) [SRC-A11Y-003].
4. Mark each field `aria-invalid="true"` and put the message above the input,
   tied by `aria-describedby` (hypothesis; common implementation practice,
   no registry source); word the message as below [SRC-A11Y-006].
5. A summary alone is not enough; show both (supported) [SRC-A11Y-009].

## Error messages

Say what happened and how to fix it, in the person's words: "Enter an email
address in the correct format, like name@example.com", not "Invalid input".
Avoid "please", "oops", blame, and codes (supported) [SRC-A11Y-006]. Suggest
the fix when the system knows it (3.3.3, verified) [SRC-A11Y-001].

DE: "Gib eine E-Mail-Adresse im richtigen Format ein, zum Beispiel
name@beispiel.de." EN: "Enter an email address in the correct format, like
name@example.com."

## Autofill, login, passwords

- `autocomplete` on every field that matches an HTML token: `name`,
  `email`, `tel`, `street-address`, `postal-code`, `cc-number`,
  `one-time-code`; the full token list is in the HTML standard (verified for
  the requirement) [SRC-A11Y-017] [SRC-A11Y-018].
- `current-password` on login, `new-password` on sign-up and change, so
  password managers generate and save (supported) [SRC-A11Y-020].
- Allow paste; offer "Show password"; never block managers (3.3.8,
  verified) [SRC-A11Y-019].

## Multi-step forms and interruption

- One question per page when answers branch (hypothesis); a task list when
  the form has independent sections (supported) [SRC-FLOW-019].
- Save and resume for long authenticated forms: the link next to the primary
  action and a confirmation (supported) [SRC-FLOW-018]; state the retention
  period, which the source leaves open (hypothesis).
- Any time limit lets people turn it off, adjust, or extend it (2.2.1,
  verified) [SRC-FLOW-007]; keeping data across a timeout for 20 hours is
  AAA (context-dependent) [SRC-FLOW-009].
- A local draft never contains passwords, card numbers, or other secrets.

## Accessibility checks

Labels visible and programmatic (1.3.1); errors in text (3.3.1); focus
visible and not hidden by sticky UI (2.4.7, 2.4.11); targets at least 24 px
(2.5.8); status announced (4.1.3); all verified [SRC-A11Y-001].

## Example

Registration with name, email, password: `examples/registration/index.html`
implements every rule above; `tests/registration.spec.mjs` proves them in
Chromium, including axe in the empty and error states.

## Agent prompt

"Improve this form. Before changing anything, answer the 13 questions in
`references/forms.md` from the code and context. Keep submit enabled unless
the submit-state table names this case. Implement validation timing, the
failed-submit pattern, failure recovery, and autocomplete; then write
Playwright tests in the shape of `tests/registration.spec.mjs` and run them."

## Evidence gaps

No controlled study on disabled versus enabled submit; no primary source on
optimistic UI; whether a live region must exist before content is injected is
commonly stated but was not confirmed. Re-check when Baymard or NN/g publish
on these.
