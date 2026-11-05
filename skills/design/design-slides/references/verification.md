# Verifying a deck

A deck is verified when its claims hold against their source and every
state a viewer can see has been looked at. Reading the source file proves
neither: a template wraps text differently than a measurer predicts, and an
element can show before its build step without any error.

Evidence: observed. On 2026-11-05 two technical deep-dive decks passed a
file-level check and a screenshot of each slide's final state. The reviewer
still found an arrowhead visible before its arrow's build step, a stage name
touching its box edge, and two paragraphs overlapping on one card. Each
finding maps to a check below.

## Claims against a pinned source

For a technical deck, the source is the code, config, or document the deck
describes, at one named revision (a commit, a document version).

1. Keep a claim ledger beside the deck: per slide, each claim, its source
   (file and line, document and section), and a verdict - holds, corrected,
   removed, or marked hypothesis on the slide.
2. Check every number and every "always", "never", "only", and "can't"
   against the source; these are the claims a technical audience tests.
3. Take terms from the source, not from memory: the stage names, component
   names, and flags the code uses. They feed the `terms` map of
   `writing-core`'s gate.
4. When the source moves on, re-run the ledger against the new revision
   before presenting.

Template:

```text
Source: <repository> at <commit>
| Slide | Claim | Source | Verdict |
| 4 | Nine stages from idea to observing | docs/CONTEXT.md:12-30 | holds |
| 10 | Budget per loop defaults to 100 | config/defaults.py:41 | corrected (was 50) |
```

## Every visible state

Render the deck the way it will be shown and look at what the viewer sees,
not at the source.

1. States: every slide, in every language, at every build step. A deck with
   builds has more states than slides; the final state alone hides early
   reveals.
2. Automated checks per state, in a headless browser:
   - **Overflow:** no text box whose content is taller or wider than the box
     (`scrollHeight > clientHeight` or `scrollWidth > clientWidth`), and no
     text touching its box edge.
   - **Overlap:** no two text boxes on one slide whose rendered rectangles
     intersect.
   - **Early reveal:** at step N, nothing assigned to a later step is
     visible. Check compound shapes part by part: an arrow and its head, a
     callout and its pointer, a line and its label are often separate
     elements, and only one of them carries the build class.
   - **Step zero:** a slide that builds starts in the state the speaker
     expects, usually empty of everything that builds.
3. Visual review: a contact sheet per language (all slides, final state)
   to catch rhythm, alignment, and density across the deck, plus a
   full-size screenshot of each slide whose checks warned.
4. Fix in the generator, not in the output file, so the next build keeps
   the fix; re-render and re-run all checks after every fix, because a fix
   to one slide's text can push another slide's layout.

A minimal early-reveal probe for an HTML deck whose build steps are classes
(adapt the selectors to the deck's own step mechanism):

```js
// For each slide and step: advance, then list visible elements of later steps.
const late = await page.$$eval('[class*="step-"]', (els, step) =>
  els.filter(e => Number(e.className.match(/step-(\d+)/)[1]) > step)
     .filter(e => getComputedStyle(e).visibility !== 'hidden'
               && getComputedStyle(e).opacity !== '0')
     .map(e => e.outerHTML.slice(0, 80)), currentStep);
```

## Technical deep dive

A deep dive answers "how does it work" for engineers who will test every
claim.

- One module or mechanism per slide; the headline states what it does,
  the body shows how, with the real names from the source.
- Diagrams show the real flow (who calls whom, where data is stored),
  built in the order the flow runs.
- Limits and open points are named with their source (an ADR, an issue),
  without apology and without "bewusst schlank".
- The last slide states where each topic stands today and its next step.
- The text pass of `writing-core` runs with the source's terms; a technical
  audience reads a translated term as a sign the author did not read the
  code.

## Done when

The ledger has a verdict for every claim; every state in every language
passed overflow, overlap, early-reveal, and step-zero checks or carries a
judged warning; the contact sheets were looked at; and the text gate of
`writing-core` passed for every language.
