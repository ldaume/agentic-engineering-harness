# Writing skills

A shared editorial model for professional German and
US English text plus four domain skills, each owning the golden path of its
artifacts. Not one "write better" prompt, because a Slack message is not a
short email and a status report is not a ticket inventory.

| Skill | Triggers |
| --- | --- |
| [writing-core](./writing-core/SKILL.md) | rewrite, edit, tighten, translate DE/EN, editorial and readability review, deterministic quality gate |
| [writing-editorial](./writing-editorial/SKILL.md) | email, Slack, decision requests, PO, management, C-level, and customer summaries |
| [writing-marketing](./writing-marketing/SKILL.md) | marketing email, hero sections, landing pages, website copy |
| [writing-product](./writing-product/SKILL.md) | status reports, adaptive and FaST-compatible roadmaps, progress, problem and bet briefs |
| [writing-engineering](./writing-engineering/SKILL.md) | PR descriptions, commit messages, Confluence and technical docs |

Domain skills summarize the core contract inline, so each works when installed
alone; with the core installed beside them they also get its quality gate.

Neighbors split the work instead of competing: `product-craft` decides what to
build and these skills write it up; `plain-numbers` owns how metrics read and
is loaded alongside status and executive text; `documentation-and-adrs`
decides whether a doc or ADR is needed and these skills own its prose.

Activation differs by host. Measured on 2026-10-21 with all five installed:
Codex loaded the owning skill for 6 of 6 sampled prompts; headless Claude Code
answered 12 of 12 short writing prompts directly without loading any skill,
the same as for an unrelated writing skill used as a control. With a
prompt-time hook that names the owning skill, Claude Code passed 13 of 14
routing cases, both near misses included; the miss was a one-sentence rewrite
it still answered directly. On Claude Code, put such a hook in the consuming
harness; it is host wiring, so it is not part of these skills.

## Renamed

The family dropped its `progressive-` prefix on 2026-11-05. The old names are
retired; their last public tag stays installable by pin. New pins use the new
name from its `-v1.0.0` tag.

| Old name | New name | Last tag under the old name |
| --- | --- | --- |
| progressive-writing-core | [writing-core](./writing-core/SKILL.md) | `progressive-writing-core-v1.1.0` |
| progressive-editorial | [writing-editorial](./writing-editorial/SKILL.md) | `progressive-editorial-v1.1.0` |
| progressive-engineering | [writing-engineering](./writing-engineering/SKILL.md) | `progressive-engineering-v1.1.0` |
| progressive-marketing-ux | [writing-marketing](./writing-marketing/SKILL.md) | `progressive-marketing-ux-v1.1.0` |
| progressive-product-agile | [writing-product](./writing-product/SKILL.md) | `progressive-product-agile-v1.1.0` |
