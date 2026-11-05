# Design skills

A shared UI/UX design core with an evidence registry plus nine
skills that each own the golden path of one kind of work. They decide what to
build and how to verify it; `frontend-craft` builds the screen, and the
`writing-*` skills write the words on it.

| Skill | Triggers |
| --- | --- |
| [design-core](./design-core/SKILL.md) | design framing, decision records, quality model, motion and animation, routing, evidence refresh |
| [design-research](./design-research/SKILL.md) | discovery, interviews, usability tests, synthesis, journey maps, sample sizes |
| [design-flows](./design-flows/SKILL.md) | user flows, journeys, state models, edge cases, recovery, flow lint |
| [design-forms](./design-forms/SKILL.md) | forms, validation timing, error recovery, submit state, undo and confirm, browser-tested example |
| [design-product-ui](./design-product-ui/SKILL.md) | SaaS and app screens, navigation, density, tables, settings, AI-native review and undo |
| [design-web](./design-web/SKILL.md) | marketing and editorial sites, landing pages, visual craft, awards, Core Web Vitals |
| [design-dataviz](./design-dataviz/SKILL.md) | dashboards, chart choice by decision question, accessible charts |
| [design-slides](./design-slides/SKILL.md) | decision decks, assertion-evidence slides, builds, architecture and system diagrams |
| [design-systems](./design-systems/SKILL.md) | design tokens (DTCG 2025.10), components specs, theming, contrast gate, governance |
| [design-review](./design-review/SKILL.md) | UX and accessibility audits, findings format, Playwright and axe verification |

## Evidence

Every material rule carries an evidence level - verified, supported,
context-dependent, hypothesis, aesthetic - and cites the registry in
`design-core/references/sources.json` as `[SRC-...]`. The
registry was built from sources opened on 2026-10-21 (156 entries with URL,
access date, findings, limits, and a revisit trigger); gaps found during that
research stay listed in each skill's "Evidence gaps". `scripts/check-knowledge.py`
fails the build when a citation has no registry entry.

An award is evidence of a jury's judgment of craft, not of usability,
accessibility, or product outcome; the skills keep those claims apart.

## Checks

- `python3 -m unittest discover -s skills/design/<skill>/tests` for the flow
  lint, the contrast gate, and the core tests.
- `npx playwright test -c skills/design/design-forms/tests`
  runs the reference form in Chromium, including axe WCAG 2.2 A/AA.
- `tests/routing-cases.json` in the core lists activation and near-miss
  prompts.

## Renamed

The family dropped its `progressive-` prefix on 2026-11-05. The old names are
retired; their last public tag stays installable by pin. New pins use the new
name from its `-v1.0.0` tag.

| Old name | New name | Last tag under the old name |
| --- | --- | --- |
| progressive-design-core | [design-core](./design-core/SKILL.md) | `progressive-design-core-v1.0.0` |
| progressive-design-review | [design-review](./design-review/SKILL.md) | `progressive-design-review-v1.0.0` |
| progressive-design-systems | [design-systems](./design-systems/SKILL.md) | `progressive-design-systems-v1.0.0` |
| progressive-forms-interactions | [design-forms](./design-forms/SKILL.md) | `progressive-forms-interactions-v1.0.0` |
| progressive-user-flows | [design-flows](./design-flows/SKILL.md) | `progressive-user-flows-v1.0.0` |
| progressive-product-interfaces | [design-product-ui](./design-product-ui/SKILL.md) | `progressive-product-interfaces-v1.0.0` |
| progressive-web-experiences | [design-web](./design-web/SKILL.md) | `progressive-web-experiences-v1.0.0` |
| progressive-slides-diagrams | [design-slides](./design-slides/SKILL.md) | `progressive-slides-diagrams-v1.0.0` |
| progressive-data-visualization | [design-dataviz](./design-dataviz/SKILL.md) | `progressive-data-visualization-v1.0.0` |
| progressive-ux-research | [design-research](./design-research/SKILL.md) | `progressive-ux-research-v1.0.0` |
