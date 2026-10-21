# Design skills

Progressive UI/UX design: a shared core with an evidence registry plus nine
skills that each own the golden path of one kind of work. They decide what to
build and how to verify it; `frontend-craft` builds the screen, and the
`progressive-writing` skills write the words on it.

| Skill | Triggers |
| --- | --- |
| [progressive-design-core](./progressive-design-core/SKILL.md) | design framing, decision records, quality model, motion and animation, routing, evidence refresh |
| [progressive-ux-research](./progressive-ux-research/SKILL.md) | discovery, interviews, usability tests, synthesis, journey maps, sample sizes |
| [progressive-user-flows](./progressive-user-flows/SKILL.md) | user flows, journeys, state models, edge cases, recovery, flow lint |
| [progressive-forms-interactions](./progressive-forms-interactions/SKILL.md) | forms, validation timing, error recovery, submit state, undo and confirm, browser-tested example |
| [progressive-product-interfaces](./progressive-product-interfaces/SKILL.md) | SaaS and app screens, navigation, density, tables, settings, AI-native review and undo |
| [progressive-web-experiences](./progressive-web-experiences/SKILL.md) | marketing and editorial sites, landing pages, visual craft, awards, Core Web Vitals |
| [progressive-data-visualization](./progressive-data-visualization/SKILL.md) | dashboards, chart choice by decision question, accessible charts |
| [progressive-slides-diagrams](./progressive-slides-diagrams/SKILL.md) | decision decks, assertion-evidence slides, builds, architecture and system diagrams |
| [progressive-design-systems](./progressive-design-systems/SKILL.md) | design tokens (DTCG 2025.10), components specs, theming, contrast gate, governance |
| [progressive-design-review](./progressive-design-review/SKILL.md) | UX and accessibility audits, findings format, Playwright and axe verification |

## Evidence

Every material rule carries an evidence level - verified, supported,
context-dependent, hypothesis, aesthetic - and cites the registry in
`progressive-design-core/references/sources.json` as `[SRC-...]`. The
registry was built from sources opened on 2026-10-21 (156 entries with URL,
access date, findings, limits, and a revisit trigger); gaps found during that
research stay listed in each skill's "Evidence gaps". `scripts/check-knowledge.py`
fails the build when a citation has no registry entry.

An award is evidence of a jury's judgment of craft, not of usability,
accessibility, or product outcome; the skills keep those claims apart.

## Checks

- `python3 -m unittest discover -s skills/design/<skill>/tests` for the flow
  lint, the contrast gate, and the core tests.
- `npx playwright test -c skills/design/progressive-forms-interactions/tests`
  runs the reference form in Chromium, including axe WCAG 2.2 A/AA.
- `tests/routing-cases.json` in the core lists activation and near-miss
  prompts.
