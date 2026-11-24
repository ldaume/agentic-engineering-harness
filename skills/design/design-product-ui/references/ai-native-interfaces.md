# Golden Path: AI-Native Interfaces

## Intent

Let people use AI output while staying in control: they see what the AI
proposes, judge it, correct it, reject it, and undo it after the fact.

## Workflow

1. State the capability honestly: what the AI does, what it cannot, where its
   data comes from (supported) [SRC-FLOW-010] [SRC-FLOW-020].
2. Show changes as a proposal before applying: a diff for edits, a preview
   for generated content (supported) [SRC-FLOW-014].
3. Put accept, edit, reject or dismiss, retry, and undo next to the output,
   not in a menu (supported) [SRC-FLOW-014] [SRC-FLOW-015].
4. Confirm destructive, irreversible, or costly AI actions and name the
   consequence (supported) [SRC-FLOW-014] [SRC-FLOW-010].
5. Apply corrections at once and remember them; a correction can be
   corrected (supported) [SRC-FLOW-015].
6. On failure or low quality, say what the AI could not do and offer the
   manual route (supported) [SRC-FLOW-012].
7. Show progress specifically during long runs ("Reading 12 files"), not
   "Thinking..." [SRC-FLOW-014].
8. Keep provenance: which output came from the AI, from which input, when,
   and who accepted it.
9. Show which data the AI read or used for this output (files, records,
   sources, tools called), so a person can check the basis and spot data that
   should not have been used (hypothesis, from the oversight preprints)
   [SRC-FLOW-025].
10. Disclose cost and latency where they change the decision: a long run, a
    metered action, or a paid call gets an estimate before it starts and a
    stop control while it runs (hypothesis).

## Streaming and partial output

- While output streams, keep Stop beside it. After stop, failure, or timeout,
  offer Retry and Keep partial output; never discard text a person has
  already read or copied (hypothesis).
- Mark partial output as incomplete and keep it out of any downstream action
  (save, send, apply) until it is complete or the person accepts it.
- Announce the state change politely to assistive technology ("Generating",
  "Stopped, partial answer kept") without moving focus (4.1.3, verified)
  [SRC-A11Y-001].

## Agent autonomy

State per action class what the agent may do without asking, what needs
confirmation, and what it never does (supported) [SRC-FLOW-010]
[SRC-FLOW-014]. For each level, design:

- how control returns: a visible Pause or Take over that works mid-run;
- how a person inspects what it did: a log of actions with inputs and
  results, not only a summary (supported) [SRC-FLOW-025];
- how an action is reversed: an undo or a named compensating step, shown
  before the action runs when it cannot be undone.

Widen autonomy only after people show they catch errors at the current level
(hypothesis) [SRC-FLOW-024].

## Designing for agents as users

Agents already navigate and fill product interfaces, unreliably. The cheap
near-term step is the accessibility basics: descriptive labels (no icon-only
buttons or "click here"), predictable patterns, structure that matches the
visual grouping, semantic HTML (supported, context-dependent on whether the
product wants agent access) [SRC-FLOW-030]. Intentional friction in regulated
actions stays, and an agent gets no weaker checkpoint than a person.

## Confidence and explanations

Explanations can make people accept wrong output more often; do not ship a
confidence score or explanation as a safety feature until test users decide
better with it (context-dependent) [SRC-FLOW-028] [SRC-FLOW-013]. For
high-stakes decisions consider a forcing step, knowing people rate it worse
(context-dependent) [SRC-FLOW-029].

## States to design

idle, generating (with progress), streaming, stopped with partial output,
proposal ready, partially accepted, applied, rejected, failed, undone, stale
(the source changed since the proposal), agent paused, agent acting.

## Example

A writing assistant suggests rewriting a paragraph.

- EN: "Suggested rewrite - 2 sentences shorter. [Accept] [Edit] [Dismiss]"
  then after accept: "Rewrite applied. [Undo]"
- DE: "Vorschlag: zwei Sätze kürzer. [Übernehmen] [Bearbeiten] [Verwerfen]"
  then: "Übernommen. [Rückgängig]"

## Anti-patterns

Applying AI output directly with no revert; a chatbot with no stated
capability, no way to save output, and no human route [SRC-FLOW-020];
relying on people's corrections to compensate for poor results
[SRC-FLOW-015]; treating a pattern library as evidence [SRC-FLOW-027].

## Validation

Task-based tests where the AI is sometimes wrong on purpose: measure whether
people catch the error, how long review takes, and whether undo is found.

## Evidence gaps

No controlled study of diff-review interfaces; agent-supervision evidence is
2025-2026 preprints with small samples [SRC-FLOW-024] [SRC-FLOW-025]. NN/g
now has agents-as-users guidance [SRC-FLOW-030] and a 2024 generative UI
forecast [SRC-FLOW-031], both opinion, not measured. Streaming, stop, and
keep-partial patterns, and cost disclosure, rest on practice, not a study.
