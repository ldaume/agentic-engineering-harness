---
name: progressive-product-interfaces
description: Use whenever designing or reworking screens of a SaaS product, app, admin tool, or internal tool - navigation and information architecture, settings, tables and bulk actions, permissions, notifications, search and command palettes, keyboard-first workflows, information density, loading and empty states, undo versus confirm, and AI-native interfaces where people review, correct, reject, or undo AI output (SaaS-Oberfläche, App-Screens, Navigation, Einstellungen, KI-Interface). Not for marketing sites or landing pages, which progressive-web-experiences owns. Implementation belongs to frontend-craft.
license: MIT
---

# Progressive Product Interfaces

Design product screens around the work people repeat, so that frequent tasks
are fast for experts and learnable for newcomers, and nothing important is
hidden to make a screen look calm. A reduced interface is not better when it
hides the information or action the task needs.

## Golden path

1. Name the task, its frequency, and who does it (expert, occasional,
   first-time), because density and discoverability trade against each other
   and frequency decides which wins.
2. Map the information architecture before navigation: what objects exist,
   how people find them, what they do with them (supported) [SRC-PROD-010].
3. Put the primary action where the task starts; keep secondary actions
   reachable, not removed.
4. Design every state of each view: loading, empty, partial, error, success,
   no permission, offline. State craft and copy follow `frontend-craft`.
5. Choose feedback by duration: response within 0.1 s, progress after 1 s,
   a progress bar with estimate after 10 s (supported) [SRC-PROD-009]
   [SRC-PROD-007].
6. Make destructive actions reversible where possible; confirm only severe
   ones and name the object (supported) [SRC-PROD-008].
7. Add keyboard paths for frequent tasks: focus order, shortcuts that do not
   collide with the browser or screen reader, a command palette when the
   product has many actions (hypothesis; no primary vendor writeup found).
8. Check accessibility: WCAG 2.2 AA, status not by color alone, focus visible
   and not hidden (verified) [SRC-A11Y-001] [SRC-PROD-016].
9. For AI features, load `references/ai-native-interfaces.md`.
10. Validate with task-based tests (`progressive-ux-research`) and verify in
    the browser (`progressive-design-review`).

## Load when

- `references/product-golden-path.md` - for any product screen: density,
  navigation, tables and bulk actions, settings, permissions,
  notifications, progressive disclosure, multi-user context.
- `references/ai-native-interfaces.md` - when AI generates, proposes, or
  applies content or actions.

## Rules that change the result

- Marketing aesthetics (large hero type, sparse layouts, decorative motion)
  do not transfer to dense product screens, because they trade scan speed
  for atmosphere on screens people use all day (hypothesis).
- Progressive disclosure hides advanced options behind a clear control, never
  options that most people need together (supported) [SRC-PROD-006].
- Motion in product UI is short and functional; see
  `progressive-design-core/references/motion.md`.

## Done when

Each view has its states designed, the frequent task has a keyboard path,
destructive actions are reversible or confirmed by name, AI output is
reviewable before it applies, and the accessibility checks pass.
