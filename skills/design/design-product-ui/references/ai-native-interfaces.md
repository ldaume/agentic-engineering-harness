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

## Confidence and explanations

Explanations can make people accept wrong output more often; do not ship a
confidence score or explanation as a safety feature until test users decide
better with it (context-dependent) [SRC-FLOW-028] [SRC-FLOW-013]. For
high-stakes decisions consider a forcing step, knowing people rate it worse
(context-dependent) [SRC-FLOW-029].

## States to design

idle, generating (with progress), proposal ready, partially accepted,
applied, rejected, failed, undone, stale (the source changed since the
proposal).

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
2025-2026 preprints with small samples [SRC-FLOW-024] [SRC-FLOW-025].
