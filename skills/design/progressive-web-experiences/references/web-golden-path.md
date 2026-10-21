# Web golden path

From intent to a validated page for marketing, landing, editorial,
e-commerce, and docs sites. Copy is written by `progressive-marketing-ux`;
this path gives it slots with jobs. Building is `frontend-craft`.

## Trigger

A new site, a new page type, a redesign, or a page that "does not work"
without anyone being able to say why.

## Required context

- Who arrives, from where (search, ad, newsletter, direct, a link in docs),
  on which device, with what intent. Infer from analytics, the brief, and
  existing pages; mark guesses as assumptions.
- The one action the page must enable, and the proof the visitor needs
  before taking it.
- Brand assets that exist: logo, type, color, photography, product shots.
- Constraints: CMS, framework, hosting, legal content (imprint, privacy,
  cookie consent in the EU), languages.

## Workflow

1. **Intent.** One sentence per page type: "A [visitor] arriving from
   [source] needs [answer] so they can [action]." Without this, every later
   choice is decoration (hypothesis).
2. **IA.** List content items and their relationships in a sitemap or
   table, before wireframes; navigation renders the IA, it does not replace
   it (supported) [SRC-PROD-010]. Menu labels: clear, specific, familiar,
   front-loaded, no internal jargon (supported) [SRC-PROD-011].
3. **Page structure.** Order sections by the visitor's questions, not by
   the org chart. Each section gets a job ("answer: what is it", "proof:
   who uses it", "next step"). Hand the job list to the copy owner.
4. **Composition.** Grid, type scale, density, imagery; see
   `visual-craft.md`. One visual idea per page carries more than five
   competing ones (hypothesis, drawn from reading award sites, not
   measured).
5. **Motion.** Per `progressive-design-core/references/motion.md`: a job per
   motion, a reduced-motion variant, pause for autoplay over 5 s (verified)
   [SRC-WEB-003].
6. **Performance.** Budget and image rules from `performance.md`, set before
   the hero design is final.
7. **Validation.** See below; record what was not measured.

## Decision tree by site type

| Site type | Primary job | Structure default | Watch for |
|---|---|---|---|
| Marketing / homepage | orient a mixed audience, route to the right path | what it is, who it is for, proof, paths by audience | trying to say everything above the fold |
| Landing page | one audience, one action | claim, proof, objection handling, one CTA repeated | navigation that leaks the visitor away; consider removing it (hypothesis) |
| Editorial / magazine | reading and discovery | article template first, then index pages | line length, ads or popups over text, autoplay video (verified for autoplay) [SRC-WEB-003] |
| E-commerce | find, compare, buy | category, product detail, cart, checkout | LCP on product images, CLS from late price or stock badges, urgency timers (supported) [SRC-WEB-020] |
| Docs site | find the answer, copy the code | search, task-ordered nav, page with on-page TOC | decorative motion; reading position lost on navigation |

Rules that follow from the table:

- Product detail and article pages carry most traffic on e-commerce and
  editorial sites, so design the template before the homepage
  (hypothesis).
- Checkout and forms belong to `progressive-forms-interactions`; a
  storefront hands off at the cart.
- On a docs site this skill owns structure and layout; the page text
  itself belongs to `progressive-engineering`.

## Interaction and accessibility

- One `h1` per page, headings in order, landmarks, and content in the
  initial HTML. An award site with 31 `h1` elements and another with none in
  static HTML show how easily this slips (context-dependent, scan-based)
  [SRC-WEB-028] [SRC-WEB-027].
- Sticky headers and cookie banners must not cover the focused element
  (verified, WCAG 2.4.11) [SRC-A11Y-001].
- Pointer targets at least 24 by 24 CSS px (verified, WCAG 2.5.8)
  [SRC-A11Y-001]; `frontend-craft` holds the 44 px mobile default.
- Carousels and marquees: pause control, and never the only route to
  content (verified) [SRC-WEB-003].

## Deliverables

- Intent sentences, sitemap or IA table, section-job list per page type.
- Wireframe or composition per template at 375 px and a desktop width.
- Motion list: element, job, duration, reduced-motion variant.
- Performance budget and LCP element per template.
- Copy brief for `progressive-marketing-ux`.

## Quality gates

- Every section has a job a reviewer can check.
- The primary action is visible in the first screenful on mobile without
  a modal in the way (hypothesis, consistent with `frontend-craft`).
- CWV budget stated and lab-checked (verified thresholds) [SRC-WEB-012].
- Reduced-motion pass done; autoplay inventory complete.

## Anti-patterns

- Designing the homepage hero first and everything else as leftovers.
- A centered hero, three equal feature cards, and a gradient, chosen because
  it is the default (hypothesis) [SRC-WEB-029].
- Content that appears only after a scroll animation or JS runs.
- Lorem ipsum or invented testimonials in a review build; use slot jobs.
- Countdown timers and "only 2 left" badges without real stock data
  (supported for the timer) [SRC-WEB-020].

## Validation

- Real browser, throttled mobile profile: LCP element, INP on the main
  interactions, CLS while fonts and images load.
- Keyboard only: skip link, focus order, focus visible and not obscured.
- Screen reader: headings list and landmarks make sense out of context.
- OS reduced motion on: every motion shows its variant.
- 320 px width and 200 % zoom: no horizontal scroll, no clipped text.
- After launch: field CWV at p75 per device class; lab numbers are only an
  approximation (verified) [SRC-WEB-012].

## Example

A landscape architecture studio in Hamburg wants a site that brings in
municipal tenders and private garden commissions.

- Intent, municipal: "A procurement officer arriving from a tender portal
  needs references of comparable public projects so they can shortlist the
  studio."
- Intent, private: "A homeowner arriving from search needs to see finished
  gardens and the price range so they can request a consultation."
- IA: Projects (filter by public / private), Approach, Studio, Contact.
  Two audiences, so the homepage routes rather than sells.
- Homepage sections and slot jobs:
  - Claim slot, job "say what the studio does and for whom". Placeholder:
    DE "[Was wir gestalten, für wen]" / EN "[What we design, for whom]".
  - Two path cards: DE "Öffentliche Projekte" / EN "Public projects";
    DE "Private Gärten" / EN "Private gardens".
  - Proof slot, job "three finished projects with location and year, real
    photos only".
  - Contact slot, job "one next step per audience".
- Composition: large project photography as the one visual idea, a
  restrained serif for headings, generous whitespace (aesthetic).
- Motion: cross-fade between project images on user action only, 250 ms,
  reduced-motion variant instant swap; no autoplay slideshow.
- Performance: the first project photo is the LCP element, in the HTML,
  `fetchpriority="high"`, not lazy-loaded [SRC-WEB-014].
- Not measured: tender conversion, because no baseline exists; note it.

## Agent prompt

"Design the [site type] for [organization]. Start with one intent sentence
per page type and an IA table. Give every section a job and leave copy as
slots for progressive-marketing-ux. Apply the core motion guide and the
performance budget. Validate in a real browser and list what was not
measured."
