---
name: progressive-marketing-ux
description: Use whenever writing or revising a hero section, landing page, homepage, service or product page, website copy, CTA, or marketing email or newsletter, in German or English (Hero schreiben, Landingpage, Website-Texte, Marketing-Mail). Carries the value-first narrative (what you get, how it compounds, proof, next step), evidence discipline against invented proof, and golden examples. Prefer it over generic copywriting skills when the copy must be value-first, evidence-bound, or German.
license: MIT
---

# Progressive Marketing & UX Writing

Help one defined reader see a valuable change, believe it, and take the next
useful step.

## Public narrative

Lead with positive value: what the reader gets, how that value compounds, the
mechanism or proof that makes it credible, then the next useful conversation
or action. Do not default to grievance, competitor bashing, anti-framework
positioning, or "not for you" hooks, because contrast-first copy defines you by
what you oppose and loses readers who never had the problem. When writing in a
specific person's or brand's voice, also load that voice guide or skill.

## Workflow

1. Define segment, situation or trigger, and one primary job for the page or
   message.
2. Extract the valuable change; separate capability from consequence.
3. Identify the mechanism and the evidence that exists.
4. Shape the information architecture, then draft.
5. Remove unsupported claims and generic hype; replace adjectives with
   specifics.
6. Check message-to-CTA continuity: the CTA names the next step the copy
   earned.
7. Native DE/EN edit.

## Evidence discipline

Never invent customer logos, testimonials, metrics, market leadership,
urgency, scarcity, certifications, or case-study outcomes, because public
copy is checkable and one fake proof point discredits the page. When proof is
missing, write more specifically and flag the gap to the user.

## Route

- marketing email: `references/marketing-email.md`
- hero section: `references/heroes.md`
- landing page: `references/landing-pages.md`
- homepage, service page, website content: `references/web-content.md`

## Gate

From this skill's directory, run
`python3 ../progressive-writing-core/scripts/quality_gate.py --artifact <type>
--lang <de|en> FILE` with type one of `marketing_email|hero|landing_page|website_content`.
If the file is missing (this skill was installed alone), check the
artifact's checklist in its reference by hand. Fix every error; judge each
warning, because warnings are heuristics, not rules.

## Done when

The reader can answer: is this for me, what changes for me, how does it work,
why believe it, what do I do next.
