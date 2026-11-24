# Golden Path: Product Screens

## Density and expertise

| Situation | Choice | Why |
|---|---|---|
| Daily use by trained people | Higher density, compact rows, keyboard shortcuts | Scan and act speed dominates |
| Occasional use | Medium density, labels over icons, guided steps | Recognition over recall |
| First use | Lower density, empty states that teach, one next action | Learnability dominates |
| Mixed audience | A named density setting applied to table, header, and toolbar together (context-dependent) [SRC-PROD-014] | One setting, consistent result |

## Navigation and information architecture

- Structure follows the objects and tasks people know, not the org chart;
  IA comes before the navigation UI that expresses it (supported)
  [SRC-PROD-010].
- Menu labels are plain words people use, not cute names or internal jargon
  (supported) [SRC-PROD-011].
- The current location is always visible; deep links survive reload and
  sharing.

## Tables and bulk actions

- Selecting rows shows a batch action bar; per-row actions are disabled while
  it is active, because the target is otherwise ambiguous (context-dependent)
  [SRC-PROD-014].
- Sorting, filtering, and column choice persist per person.
- Large result sets paginate or virtualize; the count is stated.

## Loading, empty, error

- Skeletons for a page or table under 10 s, a spinner for one module, a
  progress bar with estimate beyond 10 s or for uploads (supported)
  [SRC-PROD-007] [SRC-PROD-013].
- Empty states: a positive title, one sentence on the next action, a direct
  action button (context-dependent) [SRC-PROD-012]; completed or cleared
  states stay brief and positive [SRC-PROD-018].
- Errors say what failed and how to recover; partial failures are local to
  the part that failed.

## Notifications

Owner stance: give people time instead of taking it; the product pushes, the
person does not watch. Attention is a budget (batching three times a day
improved attention and well-being in a field experiment; supported)
[SRC-PROD-033].

- Classify every signal: act now (interrupt), act today (digest), FYI (in the
  product, no push). Quiet by default; one channel per urgency, controllable
  by the person.
- Agent work that needs a person arrives as an inbox item: the decision, the
  proposed action, the evidence, and Approve / Edit / Reject. Nobody has to
  watch a run or a dashboard to find it. The item opens on the decision, not
  on a list.
- Routine results go into a scheduled digest, not one message each.
- Status stays pullable: push never hides state, so the current state of any
  run or item can be opened on demand.
- A notification with an action never auto-dismisses (context-dependent)
  [SRC-PROD-015]. Group, deduplicate, and let people control channels;
  interrupt only for what the person must act on now.

## Default view

Owner stance: do not leave people alone with filters. Defaults carry most of
the experience because most people never change them (supported)
[SRC-PROD-032].

- Each list or overview opens on the view this role needs now: exceptions and
  items waiting on the person first, the answer before the data.
- Filters, raw data, and saved views are one step away, keyboard-reachable,
  and encoded in the URL so a view can be shared and restored.
- Never an empty filter builder as the first screen. Choose the default and
  record why; configurable layouts are an addition, not the default.

## Actions that cannot run yet

Owner stance: support instead of silently disabling. An action that cannot
run yet stays reachable. On activation it says what is missing and marks the
places that need attention. A disabled control without a visible reason is a
defect. `design-forms` keeps its narrow submit-button exception (one required
choice not yet made, visible reason, `aria-disabled`); see its table.

## Settings and permissions

- Settings save explicitly or autosave with a visible "Saved"; do not mix
  both on one page (hypothesis).
- A person without permission sees why and who can grant it, not a dead
  control (hypothesis; GOV.UK advises against disabled controls without a reason
  [SRC-PROD-028]; USWDS documents them without criticism [SRC-A11Y-007]).

## Status and color

Status always pairs color with text or a symbol (verified for 1.4.1)
[SRC-A11Y-001] [SRC-PROD-016].

## Dark mode

Step surfaces lighter as they rise (context-dependent) [SRC-PROD-017];
override semantic tokens, never component styles (context-dependent)
[SRC-PROD-023].

## Multi-user context

Show who else is viewing or editing, lock or merge explicitly, and name the
person behind each change in history (hypothesis).

## Anti-patterns

Hiding needed actions to look minimal; a confirmation on every delete;
auto-dismissing actionable toasts; skeletons masking slow backends; status by
color only; per-row actions live during batch mode; hand-built combobox and
dialog focus logic [SRC-PROD-024] [SRC-PROD-025].

## Evidence gaps

No primary writeups from keyboard-first products on command palettes; no
primary evidence on permissions UI, settings patterns, or density for experts
versus novices; Apple HIG and Material 3 Expressive pages could not be read
in the 2026-10 refresh.
