# Motion

Shared motion guide for every `progressive-*` design skill and for slides.
Each motion gets a job, a duration that follows from the job, and a
reduced-motion variant. Implementation stays with `frontend-craft`.

## Decision tree

Name the job before choosing a curve, because a motion without a job is the
one that distracts: peripheral vision picks up movement, so irrelevant motion
degrades the task and is hard to ignore (supported) [SRC-WEB-020].

1. **Feedback** - confirms an action registered (press, toggle, save, drag);
   start within about 0.1 s to feel direct (supported) [SRC-PROD-009].
2. **Orientation and continuity** - shows where something came from or went
   (drawer, modal, shared element, page or chart transition), so the user
   keeps reading position and focus (supported; the API is verified, the UX
   benefit is not) [SRC-WEB-007].
3. **Attention** - points at a change the user must notice; one short pulse,
   never a loop. Motion that hijacks attention or creates fear of loss, such
   as a flashing countdown, is a dark pattern (supported) [SRC-WEB-020].
4. **Delight as brand** - expressive motion on a marketing surface. No
   source shows a user benefit, so it is an (aesthetic) choice that must
   earn its performance cost and never gate content; Carbon keeps
   expressive motion separate from productive motion [SRC-WEB-023].

No job from this list: remove the motion. Every motion that stays:

- is never the only carrier of information (supported) [SRC-WEB-021];
- takes 150 ms or less, or nothing, on frequent interactions such as rows,
  tabs, and menu items, because the cost recurs on every click (supported)
  [SRC-WEB-021] [SRC-WEB-023];
- never makes people wait, and is cancellable when it blocks (supported)
  [SRC-WEB-021].

## Duration and easing

Starting points from NN/g, Material, and Carbon. They converge, but none is a
controlled duration study, so treat them as conventions (supported)
[SRC-WEB-019] [SRC-WEB-022] [SRC-WEB-023].

| Job | Duration | Easing | Reduced-motion variant |
|---|---|---|---|
| Micro-feedback: toggle, checkbox, press | 70-150 ms, about 100 | standard | keep the color or state change, no movement |
| Small reveal: fade, tooltip, popover | 100-200 ms | ease-out in, ease-in out | opacity only, or instant |
| Orientation: menu, drawer, modal, expand | 200-300 ms in, 150-250 ms out | decelerate in, accelerate out | cross-fade, no slide or scale |
| Continuity: shared element, page transition | 250-400 ms | emphasized | cross-fade or skip the transition |
| Attention to a change | one pulse under about 300 ms | ease-out | static highlight color |
| Large movement, full screen | up to 400 ms | emphasized | fade |
| Data view transition, same data | about 1-2 s, staged | ease-in-out per stage | jump to the end state, highlight what changed |
| Brand scroll sequence (marketing only) | bound to scroll | linear to scroll | static layout, no parallax |
| Autoplay loop or video | over 5 s requires a control | n/a | paused by default |

Rules behind the table:

- Exits shorter than entrances; ease-out on enter; linear looks mechanical
  outside scroll binding. Animations are far more often too long than too
  short, and 500 ms starts to drag in functional UI (supported)
  [SRC-WEB-019].
- Duration scales with distance and size, non-linearly (Carbon's rule, not
  a user finding) [SRC-WEB-023].
- The 400-500 ms ceiling is for functional UI only: Carbon dims backgrounds
  over 700 ms, Material's extra-long tokens reach 1000 ms, and the
  data-transition studies used about 1-2 s [SRC-WEB-023] [SRC-WEB-022]
  [SRC-VIZ-002]. Pick the band by job.

## Motion tokens

Use the project's tokens when they exist; token architecture belongs to
`progressive-design-systems`. Otherwise start from this set, which maps onto
published Material values (verified as published values) [SRC-WEB-022]:

```css
:root {
  --motion-fast: 100ms;      /* feedback; Material short2 */
  --motion-moderate: 200ms;  /* small reveal, exits; Material short4 */
  --motion-slow: 300ms;      /* overlay enter; Material medium2 */
  --motion-slower: 400ms;    /* large movement; Material medium4 */
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --ease-enter: cubic-bezier(0, 0, 0, 1);     /* standard-decelerate */
  --ease-exit: cubic-bezier(0.3, 0, 1, 1);    /* standard-accelerate */
  --ease-emphasized-enter: cubic-bezier(0.05, 0.7, 0.1, 1);
}
```

Carbon's set is 70/110/150/240/400/700 ms with productive and expressive
curves [SRC-WEB-023]; pick one family, because two rhythms read as
inconsistency (aesthetic).

## Reduced motion

`prefers-reduced-motion` is Baseline widely available since January 2020 and
means "remove, reduce, or replace non-essential motion" (verified)
[SRC-WEB-004]. Design the variant per motion:

- **Replace, do not delete.** MDN's own example turns a scale pulse into an
  opacity dissolve (verified) [SRC-WEB-004].
- **Not `animation: none`.** Code waiting for `animationend` never fires;
  a swapped keyframe or near-zero duration keeps the event (supported)
  [SRC-WEB-005].
- **Replace parallax, large scale, and pan**, the named vestibular triggers,
  and treat spin the same way (hypothesis for spin) (dizziness, nausea, migraine) (verified) [SRC-WEB-004]
  [SRC-WEB-005] [SRC-WEB-006].
- **JS motion checks `matchMedia` itself.** The media query does not stop
  the Web Animations API, nor, by the same mechanism, GSAP, WebGL, or
  scroll-jacking (supported for WAAPI, inference for libraries)
  [SRC-WEB-005].
- **Animated images** swap to a still via `<picture>` and a `media`
  attribute; a global `0.01ms !important` override is a user-side safety
  net, not a design (supported) [SRC-WEB-005].

```css
.reveal { animation: rise var(--motion-slow) var(--ease-enter) both; }
@keyframes rise { from { opacity: 0; transform: translateY(8px); } }
@keyframes fade { from { opacity: 0; } }
@media (prefers-reduced-motion: reduce) {
  .reveal { animation-name: fade; } /* same timing, animationend still fires */
}
```

```js
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");
// Read reduceMotion.matches before starting any JS, canvas, or WebGL motion,
// and listen for "change" so a mid-session switch takes effect.
reduceMotion.addEventListener("change", () => applyMotionPreference(reduceMotion.matches));
```

## WCAG

- **2.2.2 Pause, Stop, Hide (A).** Content that moves, blinks, or scrolls by
  itself for over 5 s beside other content needs pause, stop, or hide;
  one hero loop fails the whole page. A preload animation with nothing
  interactive during it can be essential (verified) [SRC-WEB-003].
- **2.3.1 Three Flashes (A).** At most three flashes in any 1 s, or a small
  flashing area; tool-check against general and red thresholds (verified)
  [SRC-WEB-001].
- **2.3.3 Animation from Interactions (AAA).** Interaction-triggered motion
  can be turned off unless essential; `prefers-reduced-motion` is a
  sufficient technique (verified) [SRC-WEB-002] [SRC-VIZ-010]. Target it by
  default although most regimes cite A/AA: it is the only criterion aimed at
  vestibular harm, and the variants above already meet it
  (context-dependent).

## Platform status (as of 2026-10-21)

| Feature | Status | Use as |
|---|---|---|
| Same-document view transitions | Baseline Newly available since 2025-10-14 (Firefox 144); Firefox lacks view transition types (verified) [SRC-WEB-008] | progressive enhancement; do not depend on types |
| Cross-document view transitions | Chrome 126+, same-origin, both pages opt in; Safari and Firefox status from secondary sources only (supported) [SRC-WEB-009] | enhancement for MPAs; Interop 2026 focus area, so re-check (context-dependent) [SRC-WEB-010] |
| Scroll-driven animations | shipped in Chromium; Safari 26 and Firefox (flagged) per secondary sources, mid-2026 (supported) [SRC-WEB-011] | decorative enhancement behind `@supports` |

Content must be complete with the effect off, because unsupported browsers
and reduced-motion users see that state (supported) [SRC-WEB-011]. Register
a cross-document `pagereveal` listener in a parser-blocking head script or
with `blocking=render`, or it runs too late (supported) [SRC-WEB-009]. Gate
both features on the preference:

```css
@media (prefers-reduced-motion: no-preference) {
  @view-transition { navigation: auto; }
}
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .card { animation: fade linear both; animation-timeline: view();
            animation-range: entry 0% cover 30%; }
  }
}
```

For same-document transitions, skip `document.startViewTransition` when
`reduceMotion.matches` and apply the DOM update directly.

## Per-surface rules

- **Product UI.** Productive motion: feedback and orientation, mostly under
  300 ms, nothing decorative on frequent actions (supported) [SRC-WEB-019]
  [SRC-WEB-021].
- **Marketing site.** One expressive brand moment per page (aesthetic).
  Loops, carousels, and marquees over 5 s get a visible pause (verified)
  [SRC-WEB-003]. Heavy JS motion is a plausible INP risk the source does not
  quantify, so trace it (hypothesis) [SRC-WEB-013]. No urgency animation
  (supported) [SRC-WEB-020].
- **Slides.** Presenter-controlled builds, no auto-advance; slide-to-slide
  is a cut or short fade (aesthetic). A deck exported to the web falls under
  2.2.2 and the reduced-motion rules (verified) [SRC-VIZ-009].
- **Data.** Animate between views of the same data, staged: rescale the axis,
  then move values, never both at once (verified for the tested charts)
  [SRC-VIZ-002]. Never animation as the way to read a trend; give small
  multiples or traces (verified, single study) [SRC-VIZ-003].

## Motion in text and slides

For the writing skills, when a deck, demo, or page reveals text step by
step. Default to static text; reveal only for one of these jobs.

When progressive reveal helps:

- **Segmenting.** A multi-step process broken into steps the presenter or
  learner paces is understood better than one continuous stream (supported,
  secondary summary of Mayer, narrated lessons) [SRC-VIZ-025].
- **Signaling.** Highlighting the part under discussion helps, but it is the
  weakest of Mayer's effects: median effect size 0.41, 24 of 28 tests (supported,
  author-lab corpus) [SRC-VIZ-024].
- **Staged chart change.** Short stages between views of the same data help
  tracking, not for every chart type (verified) [SRC-VIZ-002].

When it hurts:

- **Narration revealed as text.** Showing the words being spoken is
  redundancy: median effect size 0.86, 16 of 16 tests (supported) [SRC-VIZ-024].
- **Reveal as decoration.** Coherence (cut what does not serve the point)
  had a median 0.86 in 23 of 23 tests; decorative motion is such material
  by extension (hypothesis on the extension) [SRC-VIZ-024].
- **Animation instead of analysis.** Trend animation was fastest and liked
  for presentation but error-prone, and slowest and least accurate for
  analysis against small multiples (verified) [SRC-VIZ-003].
- **Too fast or complex to perceive.** Advantages mostly vanish when a static
  graphic carries the same information and interactivity; step control
  helps (supported) [SRC-VIZ-004].
- **Pre-reads and web pages.** A reveal hides structure from a scanning
  reader and from print; give the full text (hypothesis).

Rules for the writing skills: one segment per spoken step; the headline
claim is visible from the first build; the final build reads as a complete
slide for handouts; no reveal on a slide with a single point (hypothesis).

## Validation

- Emulate reduced motion (OS setting, or `reducedMotion: "reduce"` in
  Playwright) and walk every animated surface, JS and canvas included.
- Inventory autoplay: element, duration, pause control. Flash-check any
  strobing asset [SRC-WEB-001]. On marketing pages, trace INP with motion
  running [SRC-WEB-013].
- Manual: whether a motion's job is real is judgment; write the job down per
  motion so a reviewer can disagree.

## Evidence gaps

- Material's per-token guidance and the Apple HIG page were not readable;
  values come from the token file and the HIG JSON feed.
- Safari and Firefox support for cross-document view transitions and
  scroll-driven animation is from secondary sources only.
- No controlled study sets UI durations; all bands are conventions.
- No evidence that slide builds help outside narrated lessons; Mayer's
  segmenting effect size was not read from a primary chapter.
- No study found on whether fade-only motion harms vestibular users.
