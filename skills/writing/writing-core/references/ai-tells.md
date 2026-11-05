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

## Terms the audience uses

The reader's own term wins over a translation the writer invents. For a
technical audience that is the term in the code, the API, the docs, or the
team's glossary (`CONTEXT.md` or similar): "Knowledge Store", not
"Wissensspeicher"; "Rate Limit", not "Abfragelimit"; "Retry", not
"Wiederholungsversuch". Germanizing an established term is as wrong as an
invented Denglisch compound: both make the reader translate back.

Before writing for a technical audience, collect the terms from the source
and pass them to the gate:

```json
{"terms": {"Knowledge Store": ["Wissensspeicher"], "Rate Limit": ["Abfragelimit"]}}
```

The gate matches a variant inside longer words, so inflections and compounds
are caught. For a non-technical audience the rule flips only where the
reader does not know the term: explain it once, keep using it.
