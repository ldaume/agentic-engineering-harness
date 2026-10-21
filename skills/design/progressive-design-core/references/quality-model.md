# Quality Model

Score each dimension 0 to 3 and show the profile. Do not average into one
number, because a strong visual score can hide an inaccessible flow, and the
release decision depends on the weakest relevant dimension.

| Dimension | Question | 0 | 3 |
|---|---|---|---|
| Utility | Does it solve a problem people have? | No observed need | Need evidenced, outcome defined |
| Usability | Can people finish their tasks? | Task fails in testing | Tasks finished without help |
| Clarity | Are structure, hierarchy, actions clear? | Primary action unclear | One obvious next step per view |
| Accessibility | Usable with keyboard, screen reader, zoom, low vision? | Blocking WCAG A failures | WCAG 2.2 AA met, manual checks done |
| Interaction quality | Feedback, states, transitions coherent? | Silent failures | Every state designed and announced |
| Visual craft | Precise, coherent, fitting the context? | Inconsistent, decorative | Deliberate system, derived from content |
| Performance | Fast and robust? | Core Web Vitals poor | Good thresholds in the field [SRC-WEB-012] |
| Trust | Transparent, predictable, respectful? | Dark patterns, surprises | Honest states, reversible actions |
| Continuity | Does the whole journey work? | One screen polished, journey broken | Entry to outcome, including recovery |
| Outcome | Did a person or product metric improve? | Not measured | Measured against a baseline |

## Gate

- Any dimension at 0 blocks release of the affected journey.
- Accessibility below 2 blocks public release.
- Outcome stays "not measured" until data exists; never estimate it.
- Each score cites its evidence: a test, a source, or "judgment" with the
  reviewer named. A score without evidence is shown as "unrated".

## Evidence levels

| Level | Meaning | Example |
|---|---|---|
| verified | A standard, specification, or test result you can check | WCAG 2.2 SC 3.3.1 [SRC-A11Y-001] |
| supported | Several credible signals agree | Error summary with focus move [SRC-A11Y-003] |
| context-dependent | Helps in some contexts, harms in others | Inline validation timing [SRC-A11Y-011] |
| hypothesis | Plausible, untested | Optimistic UI rules without a primary source |
| aesthetic | A deliberate taste choice, no claim of superiority | A typeface pairing |

Award recognition, usability evidence, accessibility conformance, product
outcome, and aesthetic preference are different claims; never let one stand
in for another [SRC-WEB-024].
