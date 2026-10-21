# Component Specifications

## When to make a component

- A pattern recurs with the same meaning in several places: extract it.
- It appears once: keep it local, because a premature abstraction hard-codes
  the first context's assumptions (hypothesis).
- It is an accessibility-critical widget (dialog, menu, combobox, tabs,
  listbox): share it at first use and build it on an APG-following primitive
  (React Aria, Radix), because hand-written roles and focus handling are where
  keyboard and screen reader bugs live (supported) [SRC-PROD-024]
  [SRC-PROD-025].
- shadcn/ui-style registries copy component source into the project: treat
  the copy as owned code to review and update, not a dependency
  (supported) [SRC-PROD-021] [SRC-PROD-022].

## Spec template

```text
Purpose:
When to use:
When not to use:
Anatomy:
Variants and sizes:
States: (default, hover, focus-visible, active, disabled-with-reason, loading, error, empty, selected, read-only)
Keyboard behavior:
Focus behavior:
Screen reader semantics: (role, name, state; the APG pattern name)
Responsive behavior:
Content guidance: (labels, lengths, localization, DE and EN examples)
Validation: (how errors show and are announced)
Status without color: (text or symbol)
Known trade-offs:
Implementation reference: (file, primitive used)
Tests: (unit, interaction, axe, visual)
Changelog: (date, change, breaking yes or no)
```

The fields that make a spec implementable and accessible are the state
matrix (hypothesis), keyboard and focus behavior and the APG pattern name
(supported) [SRC-PROD-024] [SRC-PROD-025], and a non-color status cue
(context-dependent) [SRC-PROD-016].

## Disabled state

A spec that offers a disabled state says why, how the reason is shown, and
whether `aria-disabled` keeps it focusable; prefer an enabled control that
explains on activation (supported) [SRC-PROD-028]. See
`progressive-forms-interactions` for submit buttons.

## Example: Button (excerpt)

```text
Purpose: Trigger one action.
When not to use: Navigation (use a link); toggles (use a switch or pressed button).
States: default, hover, focus-visible (3px outline, 3:1 against adjacent colors), active, loading (label "Saving...", stays focusable, ignores repeat activation), disabled-with-reason (aria-disabled, visible reason).
Keyboard: Enter and Space activate.
Screen reader: role button, accessible name = visible label.
Content: verb first; DE "Speichern", EN "Save".
```

## Anti-patterns

Specs without keyboard and focus behavior; status by color alone; disabled
by default; components forked per team instead of extended through variants.
