# Writing Vocabulary

The terms editors, content designers, and technical writers use to judge a
text, so a review names the defect the way the field does and points at
something a reader can see in the words. Authors and check scripts use it;
reviews do not load it by default. The other `writing-*` skills name it in
their metadata instead of keeping a copy. A term is admitted only with a
registered source and an observable marker. Check: `exact` (the rule id is the
one `scripts/quality_gate.py` reports under `rules`, or the diagnostic it
reports), `jev` (a typed question in `scripts/jev_questions.json`), `judge` (a
person or model decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Bottom line up front | The point, decision, or ask the reader needs comes first; context follows it. | [SRC-WRITE-033] [SRC-WRITE-067] [SRC-WRITE-069] | The main point or ask is not in the first two sentences; an executive summary has no bottom line in its first 40 words. | exact `artifact.bottom-line` |
| Front-loading | Headings, link text, and paragraph openings start with the words that carry the meaning. | [SRC-WRITE-069] [SRC-WRITE-067] | A heading or first sentence that opens with filler: "Introduction", "In this section", "There are". | judge |
| Descriptive heading | A heading says what its section says, so a scanning reader can skip or stop. | [SRC-WRITE-027] [SRC-WRITE-069] | Generic headings ("Overview", "Details", "Misc") or headings phrased as questions. | judge |
| Chunking | Content split into short units with one idea each, grouped under headings or in lists. | [SRC-WRITE-068] [SRC-WRITE-037] | A paragraph carrying more than one main idea; more than a screen of running text without a heading. | judge |
| Enumeration chain | A list of three or more items packed into running prose. | [SRC-WRITE-069] [SRC-WRITE-021] | Three or more comma items before "and" or "or", or two semicolons in one sentence. | exact `list.enumeration` `list.semicolons` |
| Sentence length | Words per sentence; every extra clause costs the reader working memory. | [SRC-WRITE-042] [SRC-WRITE-022] | A sentence over 25 words (DE) or 30 (EN); a mean over 15 (DE) or 20 (EN) words. | exact `readability.long-sentence` `readability.mean-sentence-length` |
| LIX | Readability index: words per sentence plus the share of words over six letters; a sensor, never a target. | [SRC-WRITE-032] | LIX above 50 in text for a general audience: reread the passage and keep every needed term. | exact `diagnostics.lix` |
| Plain language | Text the intended reader can find, understand, and use on first reading. | [SRC-WRITE-037] [SRC-WRITE-038] [SRC-WRITE-064] | A reader from the stated audience cannot restate the main point and the next action after one read. | judge |
| Hidden verb | An action turned into a noun with a weak verb attached (Nominalstil). | [SRC-WRITE-064] [SRC-WRITE-066] | A noun in -tion, -ment, -ance, -ung with make, take, perform, erfolgen, vornehmen, "zur Anwendung bringen". | judge |
| Agentless passive | A passive sentence that hides who acts where responsibility matters. | [SRC-WRITE-064] [SRC-WRITE-065] | "was decided", "wurde beschlossen", "mistakes were made" with no actor in that sentence or the one before. | judge |
| Audience term | The word the reader uses for a thing, used for that thing every time. | [SRC-WRITE-022] [SRC-WRITE-021] | A variant on the audience's avoided list, or two names for one thing in one text. | exact `term.avoided-variant` |
| Unexplained acronym | An abbreviation or internal name the reader cannot expand. | [SRC-WRITE-020] [SRC-WRITE-022] | An acronym without an expansion at first use that is not on the audience's known list. | exact `acronym.first-use` |
| Link purpose | Link text says where it goes without the sentence around it. | [SRC-WRITE-026] [SRC-WRITE-023] | Link text "here", "more", "read more", "hier", "mehr", or one text for different targets. | judge |
| Operating instruction | A sentence telling readers how to operate the page instead of saying something about the subject. | [SRC-WRITE-026] | "Scroll down", "swipe the diagram sideways", "click here", "siehe unten" in running text or captions. | exact `ai-tell.ui-instruction`; jev `ui_instruction` |
| Restating | The same statement again in another place; each statement has one home. | [SRC-WRITE-019] | Two sentences sharing most of their content words; a summary that repeats its section word for word. | exact `repetition.near-duplicate` |
| Self-contradiction | Two claims on one page that cannot both be true. | [SRC-WRITE-019] | One label with two different figures; "excluded" next to "exception today". | exact `figures.conflict`; jev `contradiction` |
| Claim class | Each claim reads as what it is: sourced fact, inference, recommendation, or unknown. | [SRC-WRITE-019] [SRC-WRITE-006] | A percentage with no matching source fact; a claim from the forbidden list stated as fact. | exact `claim.unsourced-percent` `claim.forbidden` |
| Universal claim | A statement about all cases (only, always, never, every, none) without evidence for all of them. | [SRC-WRITE-066] | "always", "never", "all", "nie", "immer" with no source, or contradicted elsewhere on the page. | jev `universal_claim` |
| Target as built | Something planned described in the present tense as done or running. | [SRC-WRITE-019] [SRC-WRITE-031] | "The service handles X" where the same page calls X planned, intended, or next. | jev `target_as_built` |
| Percent complete | A progress percentage with no model of the work and unknowns that remain. | [SRC-WRITE-031] | "80% done", "zu 70 Prozent fertig" in a progress update. | exact `artifact.percent-complete` |
| Not X but Y | A contrast that rejects a claim nobody made in order to stage the real one. | [SRC-WRITE-044] [SRC-WRITE-048] | "not just X, but Y", "nicht X, sondern Y", "it's not X, it's Y" where no reader holds X. | exact `ai-tell.not-x-but-y`; jev `tell_not_x_but_y` |
| Justifying filler | A phrase that defends a choice instead of stating the state. | [SRC-WRITE-048] | "bewusst schlank", "bewusst einfach gehalten", "damit wir schnell lernen". | exact `ai-tell.justifying-filler`; jev `tell_filler` |
| Inflated significance | Importance asserted instead of shown, or a vague mechanism where the text should say what happens. | [SRC-WRITE-044] | "plays a pivotal role", "spielt eine zentrale Rolle", "kommt ins Spiel", "echter Mehrwert". | exact `ai-tell.inflated-role` `ai-tell.filler-phrase` `ai-tell.vague-value` |
| Staged opener | A sentence that announces a point instead of making it; its twin, the one-line closer, restates the paragraph as a lesson. | [SRC-WRITE-044] | "Here's the thing", "Die Wahrheit ist", "Let's dive in"; a last line that adds no fact. | exact `ai-tell.staged-opener`; jev `tell_closer` |
| Stock AI vocabulary | Words that generated text overuses until they carry no meaning. | [SRC-WRITE-044] | `delve`, `tapestry`, `testament to`, `seamless`, `game changer`, `at its core`. | exact `ai-tell.stock-word` |
| Copula avoidance | A stock verb where "is" or "has" says it. | [SRC-WRITE-044] [SRC-WRITE-048] | "serves as", "stands as", "boasts", "fungiert als", "stellt ... dar". | exact `ai-tell.copula-avoidance` |
| Vague attribution | A claim credited to unnamed authorities (weasel words). | [SRC-WRITE-044] [SRC-WRITE-048] | "experts agree", "industry reports", "Experten sind sich einig", "einige Kritiker". | exact `ai-tell.vague-attribution` |
| Chat residue | A reply to the requester left inside the artifact. | [SRC-WRITE-048] | "I hope this helps", "Let me know if", "Natürlich!", "Ich hoffe, das hilft". | exact `ai-tell.chat-residue` |
| Forced triad | Three parallel items because three sounds complete, not because there are three. | [SRC-WRITE-044] | A list of three where one item repeats another or has no content of its own. | judge |
| Shallow -ing tail | A participle clause that comments on the sentence instead of adding a fact. | [SRC-WRITE-044] [SRC-WRITE-048] | ", highlighting its importance", ", ensuring a smooth experience" at the end of a sentence. | judge |
| Workslop | Generated text that looks finished but leaves the thinking to the reader. | [SRC-WRITE-053] | After reading, the reader still has to ask what was decided, what the numbers are, or who acts. | judge |
| Message length | Words per message against the artifact's budget; shorter requests get more answers. | [SRC-WRITE-058] | A word count over the artifact's ceiling (Slack 200, business email 180, PO summary 300). | exact `artifact.word-ceiling` |
| Why before what | A change description gives the problem and the reason before it lists the change. | [SRC-WRITE-013] [SRC-WRITE-028] | A pull request without a Why or Context section; a body that only lists files. | exact `artifact.missing-part` |
| Subject line | A commit's first line: an imperative summary short enough that tools do not cut it. | [SRC-WRITE-028] [SRC-WRITE-016] | A generic subject ("fixes", "update"), over 72 characters, or no blank second line. | exact `commit.generic-subject` `commit.subject-length` `commit.blank-line` |
| Documentation mode | One page serves one need: tutorial, how-to guide, reference, or explanation. | [SRC-WRITE-046] | A how-to page that stops to explain background, or a reference table inside a tutorial. | judge |
| Voice and tone | Voice stays the same across texts; tone fits the reader's situation. | [SRC-WRITE-025] | Register shifts inside one text for one reader: Sie to du, legal to chatty. | judge |
| Translation-ready English | English written so a translator or non-native reader gets one meaning. | [SRC-WRITE-022] [SRC-WRITE-002] | Idioms, humor, an ambiguous "it" or "this", a phrasal verb with a plain one-word alternative. | judge |
| Einfache and Leichte Sprache | Einfache Sprache is German plain language for a broad audience; Leichte Sprache is a stricter variety with its own rules for readers with learning difficulties. | [SRC-WRITE-038] [SRC-WRITE-054] | The two labels used as one; a text labeled Leichte Sprache that keeps subordinate clauses. | judge |

## Not admitted

- A fixed Flesch or LIX score as a goal: the formulas are sensors, and Amstad's
  German Flesch scores clear compounds as hard [SRC-WRITE-032]; reread, never
  rewrite to a number.
- "Never use the passive voice": passive fits when the actor is unknown,
  irrelevant, or a law [SRC-WRITE-064]; judge the agentless passive instead.
- Miller's "seven plus or minus two" as a limit for lists or menus: readers
  recognize items rather than recall them [SRC-WRITE-068].
- The em dash as an AI tell on its own: a historical indicator that newer
  models avoid [SRC-WRITE-044]; dashes stay under plain punctuation.
- An AI-detector score as proof of generation: signs are indicators, not proof
  [SRC-WRITE-044] [SRC-WRITE-048]; judge the text by the terms above.
- "Never start a sentence with And or But", "never split an infinitive":
  schoolroom rules with no cost to the reader.
- Typographic (curly) quotes: house plain punctuation wins, so straight quotes
  are correct everywhere (owner decision, 2026-11-24).
