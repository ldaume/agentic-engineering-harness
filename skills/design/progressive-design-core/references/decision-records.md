# Design Decision Records

Write one when a future reader would ask "why is it like this?" - a pattern
that goes against a common default, a trade-off between dimensions, or a
choice that is expensive to reverse. Keep it to one screen.

```text
Decision:
Context:
User problem:
Options considered:
Evidence: (each with level and source id)
Chosen direction:
Trade-offs:
Accessibility implications:
Validation plan:
Revisit trigger:
```

## Example

```text
Decision: Keep "Create account" enabled while fields are invalid.
Context: Three-field sign-up on web and mobile web.
User problem: People do not know why a disabled button will not work.
Options considered: Disabled until valid; enabled with submit validation; enabled with inline validation after blur.
Evidence: GOV.UK and practitioner sources advise against disabling (context-dependent) [SRC-A11Y-004] [SRC-A11Y-013]; inline validation done well (not before typing, rechecked per keystroke while in error) reduces submit surprises in Baymard testing (context-dependent) [SRC-A11Y-011]; no controlled study on disabled buttons.
Chosen direction: Enabled; validate on blur after the first edit and on submit; error summary takes focus.
Trade-offs: Some people will submit early and see errors; that is the point where they learn what is missing.
Accessibility implications: Button stays in tab order; errors announced via focus on the summary.
Validation plan: Browser tests for each state; a moderated test with five sign-ups including one screen reader user.
Revisit trigger: A controlled study on disabled submit buttons, or completion rate dropping after release.
```

Store records next to the code or design they govern, numbered, never
rewritten: a changed decision gets a new record that supersedes the old one.
