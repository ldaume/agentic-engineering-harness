# Editorial Model

## Reconstruct before writing

Do not ask "how does this sound more professional?". Ask:

- What is happening?
- Who needs to understand it, and what do they already know?
- What must they know after reading?
- What should they think, decide, feel, or do?
- What evidence supports the message, and what uncertainty remains?
- What is the shortest structure that preserves the necessary meaning?

## The loop

FRAME, SHAPE, DRAFT, EDIT, VERIFY, TEST, SHIP.

**FRAME.** Fill in what context allows:

```yaml
artifact:
language:
primary_audience:
secondary_audience:
reader_context:
reader_knowledge:
intent:
desired_reader_change:
required_action:
evidence:
known_facts:
unknowns:
constraints:
voice:
channel:
deadline_or_time_horizon:
```

Derive gaps from repository, ticket, diff, conversation, or documents first.
Ask only about a gap that changes the artifact.

**SHAPE.** Write the information architecture, not sentences. Common shapes:

- Decision communication: situation, meaning, evidence, decision or
  recommendation, next step.
- Marketing: desired outcome, customer problem, value, mechanism, proof,
  action.
- Technical documentation: purpose, prerequisites, concept or model,
  procedure, verification, failure and recovery, related decisions.

Readers scan. Descriptive headings, front-loaded answers, and descriptive link
text serve scanning and accessibility at once.

**DRAFT.** Meaning over elegance, specificity over polish, verbs over
abstractions, evidence over adjectives, one idea over sentence gymnastics,
reader reality over internal terminology.

**EDIT.** Separate passes. The professional stages are structural,
stylistic, copy editing, and proofreading, in that order, because polishing a
sentence that the structural pass will cut wastes the work (verified)
[SRC-WRITE-019]. The passes below map onto them: A to structural, B to D to
stylistic, E to copy editing, F to proofreading.

- A Structural: does the order match the reader's decision path?
- B Meaning: is every claim precise and uncertainty honest?
- C Line: shorter, stronger, more concrete sentences.
- D Language-native: would a good native editor phrase it this way?
- E Copy: terminology, spelling, punctuation, capitalization, dates.
- F Proof: names, numbers, links, product names, dates, references.

**VERIFY.** See `verification.md`.

**TEST.** Deterministic structure, linguistic diagnostics, semantic rubric,
and human judgment for high-impact artifacts. See `quality-model.md`.

## Text that is presented or animated

Slides, hero sections, and product UI may reveal text step by step. No
evidence was found that progressive reveal helps comprehension in slides or
web copy; the multimedia-learning principles behind it come from narrated
instructional lessons (hypothesis) [SRC-WRITE-034]. So: write the full
message so it reads correctly without motion, keep the key claim visible by
default, and never make a reader wait for an animation to see the point. When
a build is used, one step carries one idea. Motion design itself follows
`progressive-design-core/references/motion.md` when that skill is installed.

## Golden paths in one line each

| Artifact | Path |
|---|---|
| Email | point, context, ask |
| Slack | signal, meaning, next |
| Executive summary | bottom line, impact, evidence, exposure, recommendation, next checkpoint |
| PO summary | what changed, product meaning, evidence, trade-off, decision, next learning step |
| Marketing email | relevance, value, proof or mechanism, one CTA |
| Hero | value, mechanism, action |
| Landing page | promise, problem or value, mechanism, proof, objection, action |
| Website page | user need, answer, useful depth, next path |
| Status | outcome, changed reality, learning, risk, decision, next |
| Roadmap | strategic intent, outcomes, opportunity, current bet, confidence, investment boundary, learning milestone |
| Progress | goal, new reality, uncertainty retired, uncertainty remaining, next breakthrough |
| Product doc | smallest artifact for the decision: problem brief, bet brief, experiment card, decision record, outcome review |
| Technical doc | purpose, prerequisites, model, procedure, verification, recovery |
| PR | why, behavioral change, review focus, validation, rollout |
| Commit | coherent change, optional reason and consequence |

## The rule behind all of them

Every artifact has a different job. A Slack message is not a short email. A
status report is not a ticket inventory. A roadmap is not a feature calendar.
A progress document is not percentage complete. A PR description is not a
diff transcription. A commit is not a changelog. A hero is not a slogan
generator. A landing page is not a long hero. A Confluence page is not meeting
exhaust. An executive summary is not merely a shorter technical document.
German is not translated English, and English is not translated German.

Length targets in the domain references are editorial starting values, not
laws. There is no SEO-preferred word count.
