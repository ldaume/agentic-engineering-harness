# Baseline CSS Cheat Sheet

Status read from the web platform status API on 2026-11-24
(`https://api.webstatus.dev/v1/features/<id>`) [SRC-WEB-030]. Status moves:
re-read the feature id before relying on a row older than a quarter.

## Rule

- **Widely available** (Baseline in all core browsers for 30 months): use
  freely.
- **Newly available** (in all core browsers, under 30 months): use as
  progressive enhancement. Guard with `@supports` or write a fallback that
  keeps the content and the function.
- **Limited** (a core browser lacks it): only behind a fallback. Re-check
  before every use.

Core browsers: Chrome, Edge, Firefox, Safari (desktop and mobile). Baseline
says nothing about your users' browser mix; check your own analytics for a
hard dependency (supported) [SRC-WEB-030].

## Status

| Feature | Feature id | Status | Newly since | Widely since | Missing in |
|---|---|---|---|---|---|
| Container queries (size) | `container-queries` | Widely | 2023-02-14 | 2025-08-14 | - |
| `:has()` | `has` | Widely | 2023-12-19 | 2026-06-19 | - |
| `text-wrap: balance` | `text-wrap-balance` | Widely | 2024-05-13 | 2026-11-13 | - |
| `light-dark()` | `light-dark` | Widely | 2024-05-13 | 2026-11-13 | - |
| `color-mix()` | `color-mix` | Widely | 2023-05-09 | 2025-11-09 | - |
| Oklab and OkLCh | `oklab` | Widely | 2023-05-09 | 2025-11-09 | - |
| `<dialog>` | `dialog` | Widely | 2022-03-14 | 2024-09-14 | - |
| Popover | `popover` | Newly | 2025-01-27 | - | - |
| View transitions (same-document) | `view-transitions` | Newly | 2025-10-14 | - | - |
| `@scope` | `scope` | Newly | 2026-03-24 | - | - |
| `contrast-color()` | `contrast-color` | Newly | 2026-04-10 | - | - |
| Scroll-driven animations | `scroll-driven-animations` | Newly | 2026-10-27 | - | - |
| `field-sizing` | `field-sizing` | Newly | 2026-06-16 | - | - |
| `text-wrap: pretty` | `text-wrap-pretty` | Limited | - | - | Firefox |
| View transitions (cross-document) | `cross-document-view-transitions` | Limited | - | - | Firefox |
| Anchor positioning | `anchor-positioning` | Limited | - | - | Firefox |
| Customizable `<select>` | `customizable-select` | Limited | - | - | Firefox |

All rows read on 2026-11-24 (verified) [SRC-WEB-030]. The "Missing in" column
comes from the browser implementation list of the same response.

## Use notes

- **Container queries.** Components respond to their container; page layout
  stays on media queries (`visual-craft.md`).
- **`:has()`.** Good for parent state, such as a card with an image or a form
  group with an invalid field. Keep selectors cheap and local; a `:has()` on
  `body` re-evaluates on every DOM change (hypothesis).
- **`text-wrap: balance`** for headings and short captions, **`pretty`** for
  body copy. Unsupporting browsers wrap as before, so no fallback is needed
  and nothing breaks.
- **`light-dark()`** needs `color-scheme: light dark` on the element or root.
  Pair it with the token layer; do not scatter literal colors.
- **`color-mix()` and OkLCh** for derived tints and state colors. Still check
  contrast in both schemes (WCAG 1.4.3 and 1.4.11) because mixing does not
  guarantee a ratio.
- **`contrast-color()`** picks black or white for a background. It chooses
  the better of two, not a passing color: verify the result against AA.
- **Popover and `<dialog>`.** Prefer the native elements over a script
  overlay for focus handling and light dismiss; test focus return and Escape.
  Popover is Newly: keep the trigger a working button without it.
- **View transitions.** Same-document is an enhancement with the view
  transition types gap noted in `design-core/references/motion.md`;
  cross-document is Limited, so the navigation must work without it. Both
  stay behind `prefers-reduced-motion: no-preference`.
- **Scroll-driven animations.** Enhancement only, behind
  `@supports (animation-timeline: view())`, content complete with the effect
  off, reduced motion respected (`motion.md`).
- **`@scope`.** Scopes selectors to a subtree; useful for component styles
  without naming conventions. Newly: a plain class fallback costs little.
- **`field-sizing: content`.** Auto-growing textareas and inputs; without it
  the field keeps a fixed size, which is a safe fallback.
- **Anchor positioning and customizable select.** Limited. Ship the existing
  pattern (a positioned popover, a native select) as the base and layer the
  new feature inside `@supports (anchor-name: --a)` or
  `@supports (appearance: base-select)`. Never rely on them for a primary
  task.

```css
/* Newly or Limited: base first, enhancement guarded */
@supports (field-sizing: content) {
  textarea { field-sizing: content; min-block-size: 3lh; }
}
@supports (anchor-name: --trigger) {
  .menu { position-anchor: --trigger; inset-area: bottom span-right; }
}
```

## Gaps

- Baseline is a browser-vendor signal, not a statement on assistive
  technology support. Test popover, dialog and select behavior with a screen
  reader (hypothesis).
- The `@supports` conditions in the snippet are the commonly used probes,
  not read from a specification in this run (supported).
