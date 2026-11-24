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
for a detector, and re-read the live list before an audit. German chat
residue and phrases carried over from English are listed on German Wikipedia's
WP:AKI page (supported) [SRC-WRITE-048]; the remaining German tells in this
file are practitioner observation, not a measured result (hypothesis).

Do not overcorrect. Perfect grammar, formal or "fancy" prose and transition
words alone are weak evidence, because many careful human writers produce them
(supported) [SRC-WRITE-044]. Never roughen a text to look human: remove a tell
only where it costs the reader something.

## The pass

Run it as its own edit pass, after the line edit and before the copy edit,
because a line edit tightens a tell instead of removing it.

1. Run `scripts/quality_gate.py` with the artifact type (`slides` for deck
   text, `prose` for any other running text) and a `terms` map (below). Fix
   every `term` error; judge every `ai-tell` warning.
2. Read the text once more for the tells a regex cannot see: closers,
   triads, staging, inflated significance, and the structural tells below
   (restating, contradiction, bloat, unknown vocabulary, unanchored claims).
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
Mehrwert`. Wikipedia marks the 2023 and 2024 word lists as historical: newer
models use them less (supported) [SRC-WRITE-044]. They stay in the gate
because they still occur. Replace with the specific claim or cut. The catalog's
`scripts/audit-skills.py` keeps the longer English list for Skill text.

**Em dash.** Wikipedia's "Signs of AI writing" lists em-dash overuse as a
historical indicator (section dated 2022 to September 2026, page read
2026-11-24, no revision date shown) and says it is most useful in combination
with other indicators (supported) [SRC-WRITE-044]. Keep the rule against the
dash as a universal connector, but there is no ban: a dash for rhythm is
fine. Third-party humanizer or copywriting Skills that ban the em dash
outright are stale on this point; this rule wins.

**Copula avoidance.** A stock verb where "is" or "has" says it: "serves as",
"stands as", "boasts", "stellt ... dar", "fungiert als", "dient als". The gate
warns (supported) [SRC-WRITE-044] [SRC-WRITE-048].

- Before: "The library serves as a bridge between the two teams."
- After: "The library connects the two teams."
- Before: "Das Modul stellt eine zentrale Schnittstelle dar."
- After: "Das Modul ist die Schnittstelle zwischen Export und Archiv."

**Shallow -ing tail.** A participle clause that comments instead of adding a
fact: "..., highlighting its importance", "..., ensuring a seamless
experience", German "..., wobei X hervorgehoben wird". Cut the tail or turn it
into its own sentence with a fact.

- Before: "The job retries twice, ensuring reliability."
- After: "The job retries twice and then reports the failure."

**Vague attribution.** "Experts argue", "observers have cited", "Experten
sind sich einig", "Branchenberichte zeigen". Name the source and its date, or
drop the claim (supported) [SRC-WRITE-044] [SRC-WRITE-048].

- Before: "Experten sind sich einig, dass der Ansatz skaliert."
- After: "In der Studie der ETH Zürich stieg der Aufwand um mehr als 20 Prozent."

**Inflated significance.** "a pivotal moment", "a lasting legacy" about something ordinary. State what changed and for whom.

**Challenges and outlook ending.** "Despite these challenges, X remains well
positioned for the future." A closing that restates and promises. End on the
last fact, or on the open risk with its owner.

**Chat residue.** "I hope this helps", "Let me know if", "Natürlich!", "Ich
hoffe, das hilft", letter-style greetings and knowledge-cutoff disclaimers
inside the artifact. This is a reply to the user left in the text; delete it
(supported) [SRC-WRITE-044] [SRC-WRITE-048].

**Formatting tells.** Title Case headings where sentence case is the norm, bold labels in front of every bullet, emoji in headings or
list entries, Markdown symbols in a plain-text channel. Use sentence case,
bold only for what readers scan for, no emoji in headings
(supported) [SRC-WRITE-044] [SRC-WRITE-048].

**Phrases carried over from English.** "nicht nur ..., sondern auch" as a
stiff parallel, participle clauses ("hervorhebend", "betonend"), a "sowohl ...
als auch" triad, "Es ist wichtig zu beachten, dass". Write the German
sentence the German reader would say (supported) [SRC-WRITE-048].

**Operating instructions for the page.** A sentence that tells readers how to
operate the page or document they are looking at: swipe, scroll, click, tap,
zoom, hover, "click here", "siehe unten", "klicken Sie hier". The interface
already shows it, so the sentence adds weight and no content. When readers
really cannot tell, the fix is design (a visible overflow edge, a scrollbar, a
larger default size), not prose. A hint a screen reader needs belongs in an
`aria-label`. Describing product behavior in technical docs ("Der Nutzer
klickt auf Freigeben", "the list scrolls to the newest item") or a how-to step
inside the product is content, not this tell. Evidence: observed. In November
2026 a published page shipped "swipe the diagram sideways" three times, and
neither the gate nor the design review flagged it; the gate now warns on it.

- Before: "Auf dem Handy lässt sich das Diagramm seitlich wischen."
- After: no caption; the diagram shows a cut-off edge that invites the swipe.
- Before: "Hover over a bar to see its value."
- After: "Berlin had the most orders in March (412)." The value sits on the bar.

## Structural tells

These need a reader, not a regex; the gate only helps with the first (it warns
on near-duplicate sentences and on one label with two figures).

**Restating.** The same point again in another paragraph or section, in other
or identical words: an intro that previews the body, a summary that repeats it,
a recommendation that repeats the finding. Rule: each statement has one home.
Keep the home where the reader needs it and cut or link the rest.

- Before: "Der Export prüft vorab die Berechtigung. [...] Wie erwähnt, wird vor dem Anlegen der Datei die Berechtigung geprüft."
- After: state it once, in the section on the export.
- Before: "The migration is safe. [...] In short, the migration carries no risk."
- After: "The migration is safe: it only adds a nullable column." Then nothing more.

**Self-contradiction.** Two claims that cannot both hold: a figure ("919 USD"
and "920 USD" for one item), a date, or a status ("decided" in one place and
"still open" in another). Read the claim ledger (`verification.md`) for the
pairs; fix the one the source does not back. The gate warns on one label with
two figures, nothing more.

- Before: "Das Konzept ist beschlossen. [...] Offen bleibt, ob wir das Konzept umsetzen."
- After: "Das Konzept ist beschlossen; offen ist der Starttermin."

**Bloat.** Intros that announce ("In this section we will look at"),
summaries of summaries, stacked hedges ("might potentially perhaps"), and
sentences about the text itself ("As described above", "This document
explains"). Cut test: for each paragraph ask whether the reader loses anything
if it goes. If not, cut it. If the answer is only "it sounds complete", cut it.

**Vocabulary the reader cannot know.** Internal words, acronyms and code names
used as if the reader knew them. Rule: every term, acronym or internal name the
target group may not know is explained at first use or sits in a glossary. The
gate warns once per acronym with no expansion in parentheses at first use. Its
built-in allowlist (OK, EU, US, UK, PDF, URL, API, HTML, CSS, HTTP, HTTPS, JSON,
ID, UI, AI, USD, EUR, PR, CI, GB, MB, FAQ) assumes an English technical
audience; add the audience's own terms to `known_terms` in the facts file.

- Before: "RLS schützt jede Tabelle."
- After: "Row-Level Security (RLS) schützt jede Tabelle."
- Before: "Project Atlas ships the DCC fix."
- After: "The fix for the Data Change Console (DCC) ships this week."

**Unanchored claim.** A claim about a system that neither the code nor a
source backs, in either direction. Overclaiming says more than the code, data
or merged change shows; underclaiming calls planned, partial or missing what is
already implemented and merged. Both are errors. Name the evidence for each
claim (file and line, merged change, measurement, source) and check it against
the current default branch, not memory (`verification.md`).

- Before: "Alle Exporte werden verschlüsselt." (the code encrypts only the archive)
- After: "Das Archiv wird verschlüsselt (`export/archive.py`); die Vorschau nicht."
- Before: "Retries are planned." (the retry loop merged last week)
- After: "The job retries twice (`jobs/runner.py`, merged)."

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
