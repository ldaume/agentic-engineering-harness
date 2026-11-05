# Research Golden Paths

Every path starts with the decision the research must inform. Write it as a
question with options: "Do we build guided setup or templates first?"

## A - Unknown problem

1. Frame: who, in which situation, trying to do what; what we believe; what
   we do not know.
2. Observe: contextual interviews or observation of the current way people
   solve it (supported) [SRC-FLOW-021] [SRC-FLOW-022].
3. Hypothesize: write each belief as "We believe ... because we observed
   ...; we would be wrong if ...".
4. Rank uncertainties by impact if wrong and how cheaply they can be tested;
   opportunity solution trees help keep options tied to the outcome
   (hypothesis) [SRC-FLOW-006].
5. Test the top uncertainty with the smallest study that can change the
   decision.
Exit: the decision question has an answer or a sharper question.

## B - Improve an existing experience

1. Reconstruct the current journey from analytics, support tickets, session
   evidence, and a walkthrough.
2. Locate friction: drop-off points, error rates, repeated attempts, support
   contacts per step.
3. Combine: telemetry shows where, observation shows why; neither alone
   explains (context-dependent) [SRC-FLOW-023].
4. Develop two or three options against the friction.
5. Test with tasks (usability test; sample per `methods.md`) [SRC-FLOW-002].
6. Release behind a measurable signal and observe it against the baseline.
Exit: the change moved the signal, or the team learned why not.

## C - New concept

1. State the value and audience in one sentence each.
2. Name the riskiest assumptions: value (do they want it), usability (can
   they use it), feasibility, viability.
3. Build the cheapest prototype that tests behavior, not opinion (a fake
   door, a concierge run, a clickable flow).
4. Measure what people do, then ask why.
5. Iterate or stop; record the decision.
Exit: the riskiest assumption is confirmed or the concept is dropped or
reshaped.

## Experiments

Pre-register the metric, the expected direction, the minimum detectable
effect, and the stop rule before starting; for sample size and design use a
statistics skill when installed. Never stop early on a good-looking result.

## Evidence gaps

No credible primary source on onboarding time-to-value effects or on JTBD
method validity was found in the 2026-10 refresh; treat both as frameworks,
not evidence.
