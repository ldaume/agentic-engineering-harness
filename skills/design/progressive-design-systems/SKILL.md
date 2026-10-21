---
name: progressive-design-systems
description: Use whenever creating, extending, or auditing a design system - design tokens and their naming, color, typography, spacing and motion tokens, theming and dark mode, component specifications with states, keyboard and screen reader behavior, documentation, versioning, deprecation, migration, and design-to-code alignment (Designsystem, Design Tokens, Komponentenbibliothek, Theming). Checks token color pairs against WCAG contrast. Not for building one screen, which frontend-craft owns.
license: MIT
---

# Progressive Design Systems

Grow a system from needs that recur, with accessibility written into every
component contract, so that teams ship consistent, accessible UI faster
without being forced into uniformity. Abstract too early and the system
encodes a guess; never abstract and every team re-solves focus handling.

## Golden path

1. Inventory what exists: tokens, components, patterns, and where they
   diverge in code and design files.
2. Name tokens in three tiers - primitive (raw values, hidden from
   consumers), semantic (role and intent, the public layer), component (only
   when a semantic token cannot express it) - because consumers who bind to
   raw values break at a rebrand (practice context-dependent, the reason a
   hypothesis) [SRC-PROD-019] [SRC-PROD-020]. A small single-theme system may stop at surface and
   foreground pairs (context-dependent) [SRC-PROD-023].
3. Author tokens in the DTCG 2025.10 format, a stable Community Group report,
   not a W3C Standard; do not implement from the drafts URL (verified)
   [SRC-PROD-001] [SRC-PROD-002]. Keep themes as separate token sets until
   the resolver spec is stable (context-dependent) [SRC-PROD-003].
4. Check color pairs: `scripts/contrast.py --tokens tokens.json --pairs
   pairs.json` (WCAG 2 ratio: 4.5:1 text, 3:1 large text and UI). APCA is
   informational only, because conformance is judged by WCAG 2.
5. Promote a component when a pattern recurs with the same meaning;
   accessibility-critical widgets (dialog, menu, combobox) share from the
   first use, built on an APG-following primitive such as React Aria or
   Radix (hypothesis for the threshold; supported for primitives)
   [SRC-PROD-024] [SRC-PROD-025].
6. Write each component spec with the template in `references/components.md`.
7. Version and deprecate with a dated, per-component changelog and a
   breaking flag (supported) [SRC-PROD-029] [SRC-PROD-026].
8. Keep design and code linked and reviewed (context-dependent)
   [SRC-PROD-027].

## Load when

- `references/tokens.md` - tokens, naming, theming, dark mode, motion tokens,
  build tooling.
- `references/components.md` - a component spec or a decision whether to
  make one.
- `references/governance.md` - versioning, deprecation, migration,
  contribution, design-to-code alignment.

## Gates

Automated: `scripts/contrast.py` for token pairs (tests in
`tests/test_contrast.py`); the token build (Style Dictionary v5 or the
project's tool) in CI. Manual: component behavior with keyboard and screen
reader; visual review in each theme.

## Done when

Tokens resolve without cycles and pass the contrast gate, each shipped
component has a complete spec, breaking changes are flagged and dated, and
coherence is achieved without forbidding justified exceptions.
