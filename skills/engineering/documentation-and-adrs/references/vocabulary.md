# Documentation and Decision Record Vocabulary

The terms documentation writers and architects use to judge how a document is
built and whether a decision record is complete, so a review names the gap the
way the field does and points at something visible in the file. Authors and
check scripts use it; reviews do not load it by default. Prose terms (bottom
line up front, restating, target as built) live in `writing-core`; PR and
commit prose in `writing-engineering`. A term is admitted only with a
registered source and an observable marker; evidence and access dates are in
`sources.json`. Check: `exact` (a pattern in files or git data a script could
match; none ships here yet, so no rule ids), `jev` (a typed question), `judge`
(a person or model decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Documentation mode | A page serves one need: tutorial, how-to guide, reference, or explanation. | [SRC-WRITE-046] | A page that teaches, lists options, and argues design in turn. | judge |
| Compass | Two questions place content: action or cognition, acquisition or application. | [SRC-DOC-001] | A doc whose answers differ between its sections. | judge |
| Tutorial | A guided lesson that builds skill by doing, for a learner. | [SRC-DOC-001] [SRC-DOC-002] | A "getting started" page that is a bare task recipe. | judge |
| How-to guide | Steps to a stated goal for a reader who already has the skill. | [SRC-DOC-002] | A guide titled by a tool, or padded with background. | judge |
| Reference | Neutral facts about the machinery, laid out like the product. | [SRC-DOC-003] | A reference page with advice, opinion, or step-by-step teaching. | judge |
| Explanation | Background and reasoning that deepen understanding; not instructions. | [SRC-DOC-001] | Rationale buried in the middle of a procedure. | judge |
| Mode mixing | Explanation or reference packed into a guide; link it instead. | [SRC-DOC-002] [SRC-DOC-003] | A runbook step followed by paragraphs of design history. | judge |
| Audience analysis | The reader roles, and how close each is to the knowledge. | [SRC-DOC-005] | A doc that names no reader, or one role for mixed readers. | judge |
| Reader outcome | What the reader should know or be able to do afterward. | [SRC-DOC-005] [SRC-DOC-007] | No sentence saying what a reader can do after reading. | judge |
| Scope and non-scope | The opening says what the doc covers and what readers might expect but will not find. | [SRC-DOC-006] [SRC-DOC-007] | A doc with no scope line, or sections outside it. | judge |
| Prerequisites | The knowledge or setup the reader needs before starting. | [SRC-DOC-006] [SRC-DOC-007] | A procedure that assumes tools or access it never names. | judge |
| Task heading | A heading named for what the reader is doing, not for a tool. | [SRC-DOC-006] | Headings that are product or class names only. | judge |
| Doc granularity | One long document or short linked ones, chosen by reader and content. | [SRC-DOC-006] | A page too long to finish, or fragments that must be read in order. | judge |
| Docs as code | Docs live in the repository, in plain text, reviewed and checked like code. | [SRC-DOC-008] | Docs in a wiki or file store outside review, or a doc diff with no reviewer. | exact |
| Doc gate | A feature change merges only with its documentation, written while fresh. | [SRC-DOC-008] | A feature PR touching behavior and no doc change, or a doc-only follow-up weeks later. | judge |
| Generated reference | Reference produced from the code so it cannot drift from it. | [SRC-DOC-003] | A hand-copied option table beside a source of truth. | judge |
| ADR | A short record of one architecturally significant decision. | [SRC-DOC-004] | A choice of dependency, interface, or structure with no record. | judge |
| ADR anatomy | Title, context, decision, status, consequences, in prose, one to two pages. | [SRC-DOC-004] | An ADR missing a section, or written as bullet fragments. | exact |
| Context forces | The competing pressures, stated neutrally, that made a decision necessary. | [SRC-DOC-004] | A context section that already argues for the chosen option. | judge |
| Decision drivers | The concerns that shape the choice and against which options are judged. | [SRC-WRITE-047] | Options compared with no stated criteria. | judge |
| Considered options | The alternatives weighed, each with its good and bad sides. | [SRC-WRITE-047] | An ADR with one option, or "do nothing" missing. | exact |
| Consequences | Every effect of the decision, positive, negative, and neutral. | [SRC-DOC-004] | A consequences section with only benefits. | judge |
| Status | The record's state: proposed, accepted, deprecated, or superseded. | [SRC-DOC-004] [SRC-WRITE-047] | An ADR with no status, or "accepted" on a rejected path. | exact |
| Superseded ADR | A reversed decision stays in place, marked, pointing to its replacement. | [SRC-DOC-004] | A superseding ADR with no pointer, or the old one deleted or rewritten. | exact |
| Sequential numbering | ADRs carry increasing numbers that are never reused. | [SRC-DOC-004] | Duplicate or renumbered ADR ids. | exact |
| Confirmation | How compliance with the decision will be checked: review, test, or fitness check. | [SRC-WRITE-047] | A decision no test, review step, or check could show violated. | judge |
| Decision log | The set of ADRs kept in the repository as the project's decision history. | [SRC-DOC-004] | Decisions only in chat or a wiki, none under the repo's ADR directory. | exact |

## Not admitted

- One giant README for every reader: readers differ in role and closeness to the
  topic, and reference, how-to, and explanation need separate shapes
  [SRC-DOC-005] [SRC-DOC-006] [SRC-DOC-001].
- Editing an accepted ADR in place: the record keeps what was decided and why,
  so a reversal gets a new ADR and a superseded mark [SRC-DOC-004].
- An ADR for every small change: the form is for architecturally significant
  decisions with lasting effect [SRC-DOC-004].
- Documentation as a phase after the build: the field's practice is to write it
  with the change, while the feature is fresh [SRC-DOC-008].
