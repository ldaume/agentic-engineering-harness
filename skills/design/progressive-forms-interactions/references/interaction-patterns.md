# Interaction Patterns: Commit, Undo, Confirm, Announce

## Feedback timing

Acknowledge input within 0.1 s, show progress when work exceeds 1 s, and
give a progress bar with an estimate beyond 10 s (supported) [SRC-PROD-009].
Skeletons for a page or table that loads in under 10 s; a spinner for one
module; never a skeleton to mask a slow backend (supported) [SRC-PROD-007].

## Destructive actions

| Action | Pattern | Evidence |
|---|---|---|
| Reversible (archive, remove from list, move) | Do it immediately, offer undo in a toast that stays until dismissed if it carries the action | context-dependent [SRC-A11Y-025] [SRC-PROD-015] |
| Irreversible or unusually large | Confirmation naming the object and the consequence; focus starts on the least destructive button | supported [SRC-PROD-008] [SRC-A11Y-021] |
| Legal, financial, or user-data change | One of reversible, checked, or confirmed (WCAG 3.3.4) | verified [SRC-A11Y-001] |

Confirm only what is severe; a dialog on every delete trains people to click
through it (supported) [SRC-PROD-008]. Name the item: "Delete project
Atlas and its 214 files?", not "Delete these items?".

## Optimistic UI

Show the result before the server confirms only when the action almost always
succeeds, is cheap to roll back, and the rollback is visible (hypothesis; no
primary source found). On failure, restore the previous state, say what
failed, and keep the person's input for a retry.

## Double submission

Ignore activations while a request is in flight; keep the control focusable
and its label honest; make the endpoint idempotent with a request key,
because a client guard alone fails on retries and slow networks
(supported) [SRC-A11Y-004] [SRC-A11Y-016].

## Autosave and drafts

Save on a debounce after input and on blur; show "Saved" quietly in a status
region; on conflict show both versions instead of overwriting (hypothesis).
Never persist secrets.

## Status announcements

- Results that do not move focus (saved, sent, 3 results) must be announced
  (4.1.3, verified) [SRC-A11Y-023]; put them in a `role="status"` region that
  exists before the text changes (hypothesis; widely stated, not confirmed).
- `role="alert"` only for blocking errors; do not stack `aria-live` on it
  (supported) [SRC-A11Y-022].
- Moving focus is itself an announcement; do not also announce the same text.

## Dialogs

Trap focus inside a modal, close on Escape, return focus to the opener
(supported) [SRC-A11Y-021]. Use an APG-following primitive instead of
hand-written focus code (supported) [SRC-PROD-024] [SRC-PROD-025].

## Motion

State changes may animate briefly to show continuity; follow
`progressive-design-core/references/motion.md` and keep every change readable
without motion.
