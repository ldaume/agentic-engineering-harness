# Slides

## Intent

A deck that gets one audience to one decision or insight, whose headlines
carry the argument, whose visuals prove it, and which still works as a
handout or a screen-reader document.

## Trigger

A decision deck, research readout, talk, pre-read, or a review of an
existing deck; any request for builds, animation, or slide transitions.

## Required context

- Audience: who decides, who influences, what they already know and believe.
- The point: the decision or ask, or the one insight, in one sentence.
- Mode: presented live, presented remotely, or read alone as a pre-read.
- Display: projector, room TV, shared window in a video call, laptop, phone.
- Time slot and what happens after the meeting.

## Decision tree - narrative structure

- **Decision deck** (people must choose) -> ask or recommendation first,
  then two or three supporting claims, then evidence, then risks and
  options, then the decision needed and by when. Putting the conclusion
  first is BLUF practice; in this registry it rests on a tertiary source and
  no study of decision-deck effectiveness was found (hypothesis)
  [SRC-VIZ-027].
- **Research readout** (people must understand what was learned) -> the
  question and why it matters, method and who took part in one slide,
  findings as assertion headlines each with its evidence (quote, clip,
  observation, count), confidence and limits per finding, then implications
  and open questions. Findings come from `progressive-ux-research`; the
  deck does not upgrade their evidence level (hypothesis).
- **Talk** (people must remember an idea) -> one problem the audience
  recognizes, the idea, two or three demonstrations of it, what to do on
  Monday (hypothesis).
- **Audience who must be walked to an unfamiliar conclusion** -> build the
  case before the conclusion, but still name the question on slide one,
  because BLUF fails when the reader rejects the conclusion before seeing
  the evidence (hypothesis).

## Workflow

1. **Point and audience** written in the speaker notes of slide one.
2. **Headline storyline.** Write all headlines as full-sentence assertions
   before any body; read them in order; fix the argument there, because a
   flaw in the argument is cheapest to fix in one column of text
   (context-dependent) [SRC-VIZ-022] [SRC-VIZ-023].
3. **Evidence per headline.** One visual that proves the claim: a chart
   chosen with `progressive-data-visualization`, a diagram per
   `diagrams.md`, a screenshot, a quote with its source. Words next to the
   picture they explain, not on another slide (supported, spatial
   contiguity) [SRC-VIZ-024].
4. **Text reduction without losing information.**
   - Delete bullets that restate the headline (supported, coherence)
     [SRC-VIZ-024].
   - Move detail to speaker notes, appendix, or a handout; keep a reference
     on the slide ("details: appendix A") so nothing is lost.
   - When presenting with narration, do not show the narration as text
     (supported, redundancy) [SRC-VIZ-024]. A pre-read is different: text
     is the medium there, so it may carry full sentences.
   - Split a slide that makes two points.
5. **Readability at real display size.** Open the deck on the target display
   or simulate it: projector from the back row, a video-call window at
   half screen, a phone for a pre-read. Fix labels, axis text, and diagram
   text that fail there. No sourced minimum font size exists in the
   registry, so this is a manual test, not a number (hypothesis).
6. **Glance test.** Each slide's point is clear within a few seconds;
   contrast and whitespace point at the one thing that matters (aesthetic)
   [SRC-VIZ-026].
7. **Builds and animation** (below).
8. **Accessibility and handout.** Real slide titles (not text boxes), alt
   text on every image and chart, a reading order that matches the visual
   order, color never the only cue (verified) [SRC-VIZ-007], text 4.5:1 and
   chart marks 3:1 (verified) [SRC-VIZ-008].

## Builds and animation

Use a build or animation only for one of these jobs:

- **Signaling** - highlight the part of a visual under discussion, dim the
  rest (supported, weakest of the measured effects) [SRC-VIZ-024].
- **Segmenting** - reveal a complex process or diagram in presenter-paced
  steps, one idea per step (supported) [SRC-VIZ-025].
- **Staged transition between two views of the same data** - for example
  rescale the axis, then move the bars - so the audience tracks what
  changed (verified, for the tested chart transitions) [SRC-VIZ-002].

Never for decoration: flying titles, spinning logos, and bouncing bullets
pull attention from the point, because movement in peripheral vision is
hard to ignore (supported) [SRC-WEB-020].

Rules:

- One idea per build step; the step that reveals it is the step you talk
  about.
- Do not use animation as the only way to show a trend or pattern; give the
  static equivalent (small multiples, a trace, the final frame), because
  animation lost to small multiples for analysis (verified, single study)
  [SRC-VIZ-003] and its benefits often vanish against an equivalent static
  graphic (supported) [SRC-VIZ-004].
- Timings, easing, and stage lengths come from
  `progressive-design-core/references/motion.md`; data transitions in the
  tested study ran about 1-2 seconds, longer than UI motion (verified)
  [SRC-VIZ-002].
- **Reduced motion**: in a web-exported deck honor `prefers-reduced-motion`
  - each build step appears with a cut or a short fade instead of movement
  (verified, AAA) [SRC-VIZ-010]. Anything that starts automatically and
  runs over 5 seconds has pause, stop, or hide (verified, level A)
  [SRC-VIZ-009]. Live presenter-driven builds are outside 2.2.2, but the
  exported deck is not.
- **Handout parity**: the exported PDF or handout shows each built slide in
  its final state, plus intermediate states when the sequence carries
  meaning, so a reader who missed the talk gets the same information
  (hypothesis).

## Anti-patterns

- Topic headline plus bullets ("Results") (context-dependent)
  [SRC-VIZ-023].
- Narration pasted as on-screen text (supported) [SRC-VIZ-024].
- Animation as decoration (supported) [SRC-WEB-020], or as the only path
  to the pattern (verified, single study) [SRC-VIZ-003].
- Auto-playing web deck with no pause and no reduced-motion path (verified)
  [SRC-VIZ-009].
- A research readout headline that states a hypothesis as a finding
  (hypothesis).
- The ask on the last slide of a decision deck (hypothesis) [SRC-VIZ-027].

## Example

Decision deck: whether to move the support team's on-call rotation to a
follow-the-sun model.

- Slide 1 EN: "We recommend follow-the-sun on-call from Q1; we need a
  decision on hiring two people in APAC" / DE: "Wir empfehlen ab Q1
  Follow-the-Sun-Bereitschaft; wir brauchen eine Entscheidung über zwei
  neue Stellen in APAC".
- Slide 2: "Night pages land on the same three people" - evidence: a bar
  chart of pages per person outside working hours, from the paging tool,
  period stated.
- Slide 3: "The handover is the main risk" - evidence: a sequence diagram of
  the handover, built in three steps (before, handover, after), each step
  one idea.
- Slide 4: options and risks, with the claim that no measured incident data
  exists for the new model marked "hypothesis" / "Hypothese".
- Appendix: the data table behind slide 2, the full rotation calendar.

## Validation

- Headlines alone tell the argument (read them aloud in order).
- Real-size check done on the target display.
- Every build has a named job; reduced-motion and handout versions checked.
- Alt text, reading order, and contrast checked in the export.

## Agent prompt

"Write the point and the audience first. Draft only headlines as
full-sentence assertions and show them to me before building slides. For
each headline name the evidence. Mark any claim without a source as
hypothesis. Add builds only for signaling or segmenting, and list the
static handout version."

## Evidence gaps

- No study of decision-deck effectiveness found; BLUF rests on a tertiary
  source; Minto's Pyramid Principle and AR 25-50 were not opened
  [SRC-VIZ-027].
- Garner and Alley 2013 and Wolfe, Alley, and Garner 2012 were not opened;
  only the 2011 conference paper [SRC-VIZ-023].
- Mayer's segmenting effect size and the Chen et al. meta-analysis were not
  read [SRC-VIZ-025].
- No sourced rule for readability at real display size or minimum font
  size.
- No evidence that slide builds help comprehension outside narrated-lesson
  settings; the build rules extrapolate from multimedia-learning and
  chart-transition studies.
