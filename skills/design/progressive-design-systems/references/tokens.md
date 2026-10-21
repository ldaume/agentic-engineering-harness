# Design Tokens

## Format status (2026-10)

- DTCG Format 2025.10 is the first stable release, announced 2025-10-28; it
  is a Community Group report, not a W3C Standard (verified) [SRC-PROD-001].
- The drafts URL is a working draft marked not to implement (supported)
  [SRC-PROD-002]. Resolver and modes were not stable in the sources read
  (context-dependent) [SRC-PROD-003].
- Style Dictionary is on v5 (5.7.0); full 2025.10 support is unverified, so
  pin the version and test the build against your tokens (supported)
  [SRC-PROD-004] [SRC-PROD-005] [SRC-TOOL-005].

## Tiers and naming

| Tier | Example | Who uses it |
|---|---|---|
| Primitive | `color.blue.800` | Only semantic tokens |
| Semantic | `color.text.default`, `color.surface.raised`, `color.border.danger` | Components and product code |
| Component | `button.primary.background` | Only where semantic tokens cannot express the need |

Name semantic tokens by role and state, not by value, because a role
survives a rebrand and a value does not (the reason is a hypothesis; the
sources show the practice, not misuse data) (context-dependent) [SRC-PROD-019]
[SRC-PROD-020]. Avoid component tokens for every component; reuse semantic
ones (context-dependent) [SRC-PROD-020].

## Example (DTCG 2025.10)

```json
{
  "color": {
    "gray": {
      "900": { "$type": "color", "$value": { "colorSpace": "srgb", "components": [0.067, 0.067, 0.067], "hex": "#111111" } },
      "0": { "$type": "color", "$value": { "colorSpace": "srgb", "components": [1, 1, 1], "hex": "#ffffff" } }
    },
    "text": { "default": { "$value": "{color.gray.900}" } },
    "surface": { "default": { "$value": "{color.gray.0}" } }
  }
}
```

Pairs for the contrast gate:

```json
[{ "fg": "color.text.default", "bg": "color.surface.default", "use": "text" }]
```

## Theming and dark mode

- Themes override semantic tokens only, never component styles
  (context-dependent) [SRC-PROD-023].
- In dark themes, raised surfaces step lighter; a component darker than its
  background reads as a hole (context-dependent) [SRC-PROD-017].
- Check every semantic pair in every theme with `scripts/contrast.py`.

## Motion tokens

Expose duration and easing as tokens (for example `motion.duration.short`,
`motion.easing.enter`) and map them to the values in
`progressive-design-core/references/motion.md`; reduced motion is a mode of
the same tokens, not an afterthought in components.

## Anti-patterns

Calling DTCG 2025.10 a W3C standard; raw primitives in components; one
component token per property for every component; theme overrides inside
component styles [SRC-PROD-001] [SRC-PROD-020].
