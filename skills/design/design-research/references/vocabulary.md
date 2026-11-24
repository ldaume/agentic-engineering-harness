# Research Vocabulary

The terms research practitioners use to judge a study plan, a session, or a
synthesis, so a review names the gap the way the field does and points at
something a reader can see in the plan, script, notes, or report. Load before
judging research work. Design terms (layout, type, contrast) live in
`design-core/references/vocabulary.md`; none are repeated here. A term is
admitted only with a registered source and an observable marker; evidence and
access dates are in `sources.json` and the design-family registry. Check:
`exact` (a pattern a script could match in the document; none ships here yet,
so no rule ids), `jev` (a typed question), `judge` (a person or model decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Research question | What the team must learn, written open (who, what, why), not a question put to users. | [SRC-RES-010] | A plan whose questions start with do, will, or can, or are interview questions. | judge |
| Round objective | The actionable aim of one round, tied to a decision and to the assumptions under test. | [SRC-RES-014] | A round with no decision or assumption named. | judge |
| Attitudinal versus behavioral | What people say versus what they do; the two often differ. | [SRC-RES-001] | A behavioral claim sourced only from a survey or interview, not labeled self-reported. | judge |
| Self-reported claim | A statement about behavior taken from recall, with its recall and politeness limits. | [SRC-FLOW-021] [SRC-RES-001] | A finding written "users do X" with interviews as its only evidence. | judge |
| Generative versus evaluative | Generative methods find direction; formative and summative methods improve or measure a design. | [SRC-RES-001] | A usability test run to choose a product direction, or interviews offered as proof a design works. | judge |
| Think-aloud | The participant verbalizes thoughts continuously while using the system. | [SRC-RES-002] [SRC-FLOW-023] | A usability script with no instruction to talk through the task. | exact |
| Task scenario | A realistic goal with a little context, worded without the labels or steps under test. | [SRC-RES-005] [SRC-FLOW-023] | A task that names the menu item or button to find. | judge |
| Leading question | A question that contains the answer wanted or tells the participant where to look. | [SRC-RES-004] [SRC-FLOW-021] | "Did you find the filter helpful?" or "What does this link do?" in a guide. | judge |
| Biased stretch | A passage where the facilitator changed behavior; it is flagged and not used. | [SRC-RES-002] | A cited finding drawn from a moment after a hint, with no flag. | judge |
| Five users per round | About five per user group per round finds most problems under the model's assumptions. | [SRC-FLOW-001] [SRC-FLOW-002] | A plan with one large round instead of iterations, or a count with no groups named. | judge |
| Iterative rounds | Several small rounds with a fix between them beat one large study. | [SRC-FLOW-001] | A plan of 15 participants in one round and no redesign step. | judge |
| Group minimum | Three to four per group for two groups, about three per group for more. | [SRC-FLOW-001] | Fewer than three sessions for a group claimed as covered. | exact |
| Recruitment criteria | Written participant criteria: actual or likely users, including how they access the service. | [SRC-RES-012] | A plan that says "users" with no criteria, or recruits colleagues. | judge |
| Screener | The question list that admits or excludes candidates, checked against the brief. | [SRC-RES-012] | A study report with no screener or recruitment criteria. | judge |
| Recruiting bias | Who is included depends on activity, timing, place, and channel. | [SRC-RES-012] | A sample all from one channel or all with flexible schedules, limit not stated. | judge |
| Informed consent | Participants know who, why, what data, retention, observers, recording, and that they can withdraw. | [SRC-RES-013] [SRC-RES-009] | A script with no consent step, or a quote used beyond what was agreed. | judge |
| Participant with access needs | A participant using assistive technology or an assisted route, included and asked, not assumed. | [SRC-RES-015] [SRC-FLOW-005] | A sample with no disabled or assisted participant, or no note on their own devices. | judge |
| Observation over opinion | A note records what was seen or said, kept apart from what it means. | [SRC-RES-011] | A note such as "user was confused" with no quote or behavior. | judge |
| Affinity mapping | Observations are clustered into themes, then themes ranked for next steps. | [SRC-RES-003] [SRC-RES-011] | Findings listed in the order of sessions with no clustering or ranking. | judge |
| Finding versus insight | A finding is a short statement agreed from a cluster of observations; actions are written separately. | [SRC-RES-011] | A report in which findings and recommendations are one sentence, or no observation trail. | judge |
| Journey map | A map of what people do and feel over time, built from qualitative research with a named goal. | [SRC-FLOW-004] | A map with no research source or no stated user goal. | judge |
| Service blueprint | A map pairing the user's steps with the frontstage and backstage work behind them. | [SRC-FLOW-003] | A blueprint with only user steps, or built from stakeholder opinion. | judge |
| Research-based persona | A fictional target user built from clusters of observed characteristics. | [SRC-RES-007] | A persona with no named study behind it. | judge |
| Synthetic user | AI-simulated participant; a probe for ideas, not evidence of behavior. | [SRC-FLOW-035] | A quote or rate attributed to a model-played user. | judge |
| Research repository | A central, tagged store of notes, recordings, and reports, kept by ResearchOps. | [SRC-RES-008] | Findings that cannot be traced to a recording or note. | judge |

## Not admitted

- Asking what people would do as evidence of behavior: self-report is limited by awareness and willingness [SRC-RES-001]; observe or measure instead.
- A focus group as usability testing: it finds wants and feelings, not whether people can use the system [SRC-RES-006].
- "Five users are always enough": it holds for qualitative problem finding in iterations, while quantitative claims need larger samples [SRC-FLOW-001] [SRC-FLOW-002].
- Invented personas without research: a persona must rest on observed characteristics [SRC-RES-007].
