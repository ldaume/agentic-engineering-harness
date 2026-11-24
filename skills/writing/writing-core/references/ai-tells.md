# AI tells

A tell is a default choice a model makes because it fits the widest range of
readers. A careful writer chooses for one reader, so the same move reads as
generated. Every sentence that stays must add something the reader did not
have; a tell usually adds weight instead.

Evidence: observed. On 2026-11-05 two technical decks written with this skill
family loaded still carried the patterns below, and the reviewer named them
"AI slop". The house style covered tone and Nominalstil but had no list of
tells, and its loanword rule pushed toward German words the audience does not
use. This file and the gate's `ai-tell` warnings close that gap.

Tells are probabilistic and decay with each model generation: Wikipedia's
list of signs is descriptive, not proof, and says older indicators are much
rarer in newer models (supported) [SRC-WRITE-044]. Edit for the reader, not
for a detector, and re-read the live list before an audit. The German tell
list in this file is practitioner observation, not a measured result
(hypothesis).

## The pass

Run it as its own edit pass, after the line edit and before the copy edit,
because a line edit tightens a tell instead of removing it.

1. Run `scripts/quality_gate.py` with the artifact type (`slides` for deck
   text, `prose` for any other running text) and a `terms` map (below). Fix
   every `term` error; judge every `ai-tell` warning.
2. Read the text once more for the tells a regex cannot see: closers,
   triads, staging, inflated significance.
3. For each hit, state the point directly. Do not patch the phrase; rewrite
   the sentence around what it claims.

## Patterns

**Not X but Y.** "nicht X, sondern Y", "not just X, but Y", "it's not X,
it's Y", and the reversed "liegt im Code, nicht im Token". The negative half
names something nobody claimed, so the positive half sounds larger. State Y.
Keep a contrast only when the reader actually believes X, or both halves
carry a fact.

- Before: "Die Garantie liegt im Code, nicht im Token."
- After: "Dass nichts geschrieben wird, sichern Code und Tests ab."

**Justifying filler.** "bewusst schlank", "bewusst einfach gehalten",
"damit wir schnell lernen". It defends a state instead of describing it.
Say what is there today and what comes next.

- Before: "Heute bewusst schlank, damit wir schnell lernen"
- After: "Stand heute und nächster Schritt je Thema"

**Vague mechanism.** "kommt ins Spiel", "spielt eine zentrale Rolle",
"plays a pivotal role". Name what the thing does and where.

- Before: "Partnerteams kommen über ihre Prüfungen ins Spiel."
- After: "Partnerteams hängen sich über ihre Checks ein."

**One-line closer.** A last sentence that repeats the paragraph as a lesson
("Der Hebel ist das Wissen." after a paragraph that showed it). Cut it, or
make it carry the one fact the paragraph lacks.

**Forced triad.** Three parallel items because three sounds complete. Keep
three only when there are three distinct things.

**Staged opener.** "Here's the thing", "Let's dive in", "Die Wahrheit ist".
Start with the point.

**Stock words.** `delve`, `tapestry`, `testament to`, `landscape`,
`seamless`, `game changer`, `unlock the potential`, `at its core`, `echter
Mehrwert`. Replace with the specific claim or cut. The catalog's
`scripts/audit-skills.py` keeps the longer English list for Skill text.

**Em dash.** Wikipedia's "Signs of AI writing" lists em-dash overuse as a
historical indicator (section dated 2022 to September 2026, page read
2026-11-24, no revision date shown) and says it is most useful in combination
with other indicators (supported) [SRC-WRITE-044]. Keep the rule against the
dash as a universal connector, but there is no ban: a dash for rhythm is
fine. Third-party humanizer or copywriting Skills that ban the em dash
outright are stale on this point; this rule wins.

## Terms the audience uses

The term the target group uses daily wins over a translation the writer
invents, in both directions, whether English or German. For an IT audience
an established anglicism stays: "Knowledge Store", "Rate Limit", "Retry",
"Row-Level Security", "Service Account", "Secrets", "Drift", "Quota", not
"Wissensspeicher", "Abfragelimit", "Wiederholungsversuch", "Zeilenrechte",
"Dienstkonto", "Geheimnisse", "Abweichungen", "Kontingent". An established
German term stays where the group uses it: "Mandantentrennung" (not an
invented "Kundentrennung", not "Tenant Isolation" for German IT readers),
"Aufbewahrungsfristen" for data protection readers. An invented Denglisch
compound is wrong, and so is Germanizing an established term: both make the
reader translate back.

Find the terms in the group's own texts before writing (their emails,
tickets, wiki, code, the standard they work by), not by instinct. Explain a
term once when the group may not know it, then keep using it. Collect the
terms and pass them to the gate:

```json
{"terms": {"Knowledge Store": ["Wissensspeicher"], "Rate Limit": ["Abfragelimit"]}}
```

The gate matches a variant inside longer words, so inflections and compounds
are caught.
