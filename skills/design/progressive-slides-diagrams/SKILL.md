---
name: progressive-slides-diagrams
description: Use whenever building or revising a slide deck, presentation, talk, research readout, or decision deck, or a diagram - architecture or system map, C4 view, sequence or state diagram, Mermaid, D2, or Graphviz source - covering headlines, storyline, builds and animation, readability, diagram type, labels, and text alternatives (Präsentation, Folien, Foliensatz, Vortrag, Architekturdiagramm, Schaubild). Not for user-journey flowcharts (progressive-user-flows), dashboards or standalone charts (progressive-data-visualization), or .pptx file mechanics. The product decision itself belongs to product-craft.
license: MIT
---

# Progressive Slides and Diagrams

Make a deck or diagram that moves one audience to one decision or insight,
and that still works when someone reads it alone, on a small screen, or
with a screen reader. This skill decides structure, wording on the slide,
visual evidence, builds, and diagram semantics. Rendering a deck file is the
host's presentation tooling; charts on a slide are chosen with
`progressive-data-visualization`; evidence levels and motion rules live in
`progressive-design-core`.

## Golden path for a deck

1. **Audience and the point first.** Name who decides or learns what, and
   write the decision, ask, or insight in one sentence before any slide,
   because a deck built from the material outward ends on a summary nobody
   asked for. For a decision deck the ask goes on the first content slide
   (hypothesis, BLUF) [SRC-VIZ-027].
2. **Write the storyline as headlines only.** One full-sentence assertion
   per slide; read the headlines in order and the argument must stand
   without the bodies. Assertion headlines with visual evidence beat topic
   titles with bullets for understanding complex concepts in one experiment
   (context-dependent) [SRC-VIZ-023] [SRC-VIZ-022].
3. **One visual that proves each headline.** A chart, diagram, image, or
   short table; cut what does not serve the claim (supported, coherence)
   [SRC-VIZ-024].
4. **Reduce text without losing information.** Detail moves to speaker
   notes, appendix, or handout; narration is not pasted onto the slide,
   because hearing and reading the same words at once costs understanding
   (supported, redundancy) [SRC-VIZ-024].
5. **Check at real display size.** View each slide on the screen it will be
   shown on - projector, meeting-room TV, a shared window in a video call -
   and fix anything that is not readable there (hypothesis; no sourced size
   rule was found).
6. **Builds only to signal or segment**, one idea per step, with a static
   handout that carries the same content. Details in `references/slides.md`.

## Golden path for a diagram

Question first, then entities and relations, then one abstraction level,
then type, layout, labels, edge cases, semantic check, and text
alternative. Load `references/diagrams.md` for any diagram; user-journey
flowcharts belong to `progressive-user-flows`.

## Decision rules

- A pre-read deck may carry more text than a presented one, but keeps
  assertion headlines and the ask on page one (hypothesis) [SRC-VIZ-027].
- Every slide passes a glance test - its point is clear within a few
  seconds - or it is split (aesthetic) [SRC-VIZ-026].
- Animation and builds signal what to look at or segment a complex visual;
  decoration goes (supported) [SRC-VIZ-024] [SRC-VIZ-025]. Under reduced
  motion, or in an exported web deck, each step appears without movement,
  and anything auto-playing over 5 seconds has a pause (verified)
  [SRC-VIZ-009] [SRC-VIZ-010].
- Color is never the only cue on a slide or diagram (verified)
  [SRC-VIZ-007].
- A claim on a slide that no source supports is marked as hypothesis on the
  slide, because a readout headline is read as a finding (hypothesis).
- Words on slides follow the `progressive-writing` skills and figures
  `plain-numbers` when installed.

## Load when

- `references/slides.md` - any deck: decision deck, research readout, talk,
  pre-read, or builds and animation on slides.
- `references/diagrams.md` - any diagram: architecture, C4, system map,
  sequence, state, data model, or choosing a diagram-as-code format.

## Gates

- Automated: diagram source parses and renders (`mmdc`, `d2`, or `dot`
  exit codes); color pairs meet 3:1 for marks and 4.5:1 for text (verified)
  [SRC-VIZ-008], for example with
  `progressive-design-systems/scripts/contrast.py` when installed. A tool
  that renders proves syntax, not meaning.
- Manual: headlines read alone tell the argument; real-size check; reduced-
  motion and handout parity; diagram semantic check and text alternative.

## Done when

The audience and the point are written; every slide has an assertion
headline and evidence; builds have a job and a static equivalent; every
diagram passed its semantic check and ships with a text alternative and an
editable source; claims carry evidence levels or are marked hypothesis; and
what was not checked is listed.
