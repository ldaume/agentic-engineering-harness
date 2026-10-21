---
name: progressive-web-experiences
description: Use whenever designing, structuring, or reviewing a website rather than an app - marketing site, landing page, homepage, editorial or magazine site, e-commerce storefront, docs site - for information architecture, layout, typography, visual direction, motion, award-style inspiration, or Core Web Vitals (Website gestalten, Landingpage-Layout, Webdesign, Seitenstruktur, Ladezeit). Not for the copy itself (progressive-marketing-ux writes it), app or SaaS screens (progressive-product-interfaces), or building the code (frontend-craft).
license: MIT
---

# Progressive Web Experiences

Design a public website from what the visitor came to do and what the page
must prove, then make it fast, readable, and accessible before it is
memorable. A site that wins on looks and loses on load time or keyboard
access fails the people it was built for. Evidence levels, routing, and the
quality model live in `progressive-design-core`; this skill does not repeat
them.

## Golden path

Order matters because each step constrains the next.

1. **Intent.** Write one sentence per page type: who arrives, from where,
   what they need, what the page must make them do. Composition without it
   optimizes looks.
2. **Information architecture.** List content and relationships before any
   wireframe; navigation is the on-screen expression of IA, not the IA itself
   (supported) [SRC-PROD-010]. Label menus with clear, familiar words
   (supported) [SRC-PROD-011].
3. **Composition.** Derive the visual direction from the real content and
   brand, not from a template, because templated sameness is the first thing
   a returning visitor stops seeing (hypothesis) [SRC-WEB-029].
4. **Motion.** Give each motion a job and a reduced-motion variant per the
   core motion guide, `progressive-design-core/references/motion.md`, before
   choosing any library, because motion chosen first drives the JS budget.
5. **Performance.** Budget LCP, INP, and CLS at the 75th percentile before the
   hero is final (verified) [SRC-WEB-012], because the hero image and the
   motion library are what usually break them.
6. **Validation.** Check in a real browser: Core Web Vitals, keyboard,
   screen reader, reduced motion, 320 px width.

## Decision rules

- Copy is owned by `progressive-marketing-ux`; leave placeholders with the
  job each text must do ("proof of claim X") rather than writing filler
  that later survives into production.
- An award is a jury's subjective score - usability is 30% of it - not
  tested usability, accessibility, or performance (verified rubric)
  [SRC-WEB-024]. Copy a pattern from an award
  winner only after a real-browser check.
- Content must exist in the initial HTML with one `h1`; a JS-only shell
  hides the page from readers and crawlers until the bundle runs
  (context-dependent, scan-based) [SRC-WEB-027].
- Autoplaying motion over 5 s gets a pause control (verified) [SRC-WEB-003].
- Never lazy-load the LCP image (verified) [SRC-WEB-014].
- Urgency animation and fake scarcity are a trust breach, not a style
  (supported) [SRC-WEB-020].

## Load when

- `references/web-golden-path.md` - always, for a new page or site; it has
  the per-site-type path (marketing, landing, editorial, e-commerce, docs)
  and the worked example.
- `references/visual-craft.md` - when choosing typography, grid, density,
  imagery, responsive behavior, or a visual direction, or when a draft looks
  like every other landing page.
- `references/awards-and-inspiration.md` - when the brief cites Awwwards, an
  award site, or "make it feel like X", or when reviewing an expressive
  design.
- `references/performance.md` - when setting budgets, choosing images or
  fonts, adding a motion or 3D library, or when a page feels slow.
- Motion: `progressive-design-core/references/motion.md` for every animated
  surface.

## Gates

Before done:

- Intent sentence per page type and an IA list exist.
- Every motion has a job and a reduced-motion variant; no autoplay over 5 s
  without pause [SRC-WEB-003].
- Performance budget stated: LCP at most 2.5 s, INP at most 200 ms, CLS at
  most 0.1 at p75, mobile and desktop separately [SRC-WEB-012].
- WCAG 2.2 AA checked per the core [SRC-A11Y-001].

Automated: Lighthouse or a lab trace for LCP, CLS, and a long-task view;
axe or equivalent; a reduced-motion emulation pass. Manual: field CWV after
launch (lab only approximates), screen-reader walk-through, whether the
visual direction fits the brand, whether each motion earns its job.

## Done when

The gates pass, each material recommendation carries an evidence level and
a source or is marked hypothesis, what could not be measured is written as
"not measured", and the copy brief is handed to `progressive-marketing-ux`
with the job of each text slot.
