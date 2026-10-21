# Awards and inspiration

How to read an award-winning site as a source of ideas without importing its
risks. An award is evidence of craft judged by a jury, not of usability,
accessibility, conversion, or field performance (verified for the rubric;
"not measured" is an inference from its absence) [SRC-WEB-024].

## Trigger

The brief cites Awwwards, a Site of the Day, or "make it feel like X"; a
stakeholder sends a reference site; a review of an expressive design.

## What the score measures

Awwwards scores Design 40 %, Usability 30 %, Creativity 20 %, Content 10 %;
the Developer award is a separate track. Each nominee goes to at least 18
jurors and the three scores furthest from the average are dropped
(verified) [SRC-WEB-024]. Usability is judged, but the method is not
disclosed, and the page names no accessibility or performance threshold.

Read a score as "jurors liked the design and creativity", weighted toward
looks. It says nothing about whether a screen-reader user can reach the
content or whether a mid-range phone stays responsive.

## Workflow

1. **Name what you want from the reference** in one sentence: a type
   treatment, a navigation idea, a transition, a mood. "The whole site" is
   not an answer.
2. **Separate the idea from the implementation.** A scroll-linked reveal can
   be built with CSS scroll-driven animation behind `@supports`; it does not
   need the reference's WebGL stack (supported) [SRC-WEB-011].
3. **Audit the reference in a real browser** before copying the pattern:
   LCP and INP trace on a throttled mobile profile, keyboard walk,
   screen-reader headings list, OS reduced motion on. Static scans are not
   enough (context-dependent) [SRC-WEB-026] [SRC-WEB-027].
4. **Transfer with constraints.** Write what the adapted version keeps and
   what it drops, and give the motion a job and a reduced-motion variant per
   `progressive-design-core/references/motion.md`.
5. **Mark the decision (aesthetic)** in a decision record; an award is not
   a supporting source for a usability claim.

## What tends to transfer, what does not

Inference from reading the sample below, not measured (hypothesis):

- Transfers: one strong visual idea per page; typographic hierarchy and
  restraint; motion tied to navigation continuity or scroll position; a
  designed loading state.
- Does not transfer to content pages: full-page WebGL, scroll-jacking, and
  content gated behind JS. These carry the risks in the table and serve a
  brand experience, not a visitor looking for information.

## Observed risks

From static scans of served files, not rendered audits; absence of a string
does not prove absence of a feature (context-dependent):

- A 1.7 KB HTML shell with no `h1` that loads about 1.9 MB of JS before any
  content [SRC-WEB-027]. Plausible INP and LCP risk on low-end devices,
  and a crawler or screen reader may see an empty page until JS runs.
- No `prefers-reduced-motion` rule found in served HTML or scanned JS on
  canvas- and WebGL-heavy sites [SRC-WEB-026] [SRC-WEB-027]. CSS media
  queries do not stop JS motion anyway, so the JS has to check
  (supported) [SRC-WEB-005].
- 31 `h1` elements in one page's HTML, a heading-structure risk
  [SRC-WEB-028].
- On the positive side, two recent Sites of the Day ship a reduced-motion
  rule in their served files; whether it covers all motion was not checked
  [SRC-WEB-028].

## Examples from the research

Scores are overall Site of the Day scores; category scores could not be
mapped reliably.

| Site | Award, date | What transfers | Risks (evidence status) |
|---|---|---|---|
| Lando Norris (OFF+BRAND) | SOTD 2025-11-17, 8.18; Site of the Year 2025, 43 votes [SRC-WEB-025] [SRC-WEB-026] | brand-led interaction on a personal hub; one `h1`, `lang` set | canvas-heavy; no reduced-motion string in static HTML (scan, inconclusive); INP, LCP, and keyboard not checked |
| Messenger | SOTD 2025-11-10, 7.92; Developer Site of the Year 2025, 54 votes [SRC-WEB-025] [SRC-WEB-027] | WebGL, Three.js, and WebSockets as a game-like narrative | about 1.9 MB JS behind a 1.7 KB shell, no `h1` in static HTML, no reduced-motion string in 3 scanned assets (heuristic) |
| Heron AI | SOTD 2026-10-12, 7.75 [SRC-WEB-028] | ships a reduced-motion rule in served files | coverage not checked |
| Butter | SOTD 2026-09-28, 7.38 [SRC-WEB-028] | ships a reduced-motion rule (static scan) | coverage not checked |
| Moto Finance | SOTD 2026-09-24, 7.25 [SRC-WEB-028] | reduced-motion string in HTML | assets not scanned |
| bleibtgleich'26 | SOTD 2026-09-22, 7.46 [SRC-WEB-028] | - | 31 `h1` in HTML; no reduced-motion string found |
| Scout Motors | E-commerce of the Year 2025, 28 votes [SRC-WEB-025] | only the award fact verified | not opened or audited |

Re-scan in a real browser before quoting any of these risks to a client;
they are leads, not findings.

## Anti-patterns

- "It won an award, so it is good UX."
- Copying a WebGL hero onto a page whose job is to answer a question fast.
- Quoting a static-scan risk as a proven failure.
- Using award sites as the only reference set; include sites that serve the
  same audience and task, even if they never won anything.

## Example

A stakeholder sends a Site of the Day with a full-screen 3D product turntable
and asks for "this feeling" on a B2B pump manufacturer's product page.

- Wanted, in one sentence: "the product feels physical and inspectable".
- Separated: a 3D turntable is one implementation; a sequence of large,
  well-lit photos with a drag-to-rotate enhancement is another.
- Audit of the reference: not done yet, so its numbers are "not measured".
- Transfer: six-angle photo set, first photo is the LCP image in HTML;
  drag-to-rotate loads on interaction only; reduced-motion variant shows a
  static grid of the six angles. Screen text: DE "Ansicht drehen" / EN
  "Rotate view".
- Decision record: (aesthetic), with the dropped WebGL stack named and why.

## Evidence gaps

- CSS Design Awards criteria pages returned 404; the FWA's 2026 status could
  not be confirmed. Neither is a registry source.
- No real-browser audit (Lighthouse, INP trace, screen reader, reduced
  motion) of any award site in this research.
- The Site of the Year 2025 attribution rests on the winners page; the
  annual-awards pages are JS-rendered.
- Category scores per site were not captured.
