# Design Vocabulary

The terms practicing designers use to judge a page, screen, deck, or chart, so
a review names the defect the way the field does and points at something a
reader can see. Authors and check scripts use it; reviews do not load it by
default. The other `design-*` skills name it in their metadata instead of
keeping a copy. A term is admitted only with a registered source and an
observable marker. Check: `exact` (DOM, computed style, or geometry; the rule
id is the design loop's), `jev` (a typed question on a screenshot or text),
`judge` (a person or model decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Measure | Characters per line of running text; long lines make the eye miss the start of the next line. | [SRC-WEB-018] [SRC-WEB-033] [SRC-A11Y-001] | Median characters per line of body paragraphs outside about 45 to 90; over 80 fails WCAG 1.4.8 (AAA). | exact `wcag.lineLength` |
| Leading | Distance between baselines relative to the font size. | [SRC-WEB-018] | Body line-height divided by font-size outside about 1.2 to 1.45. | exact `wcag.lineHeight` |
| Body size | Size of running text; every other size is set relative to it. | [SRC-WEB-018] | Body font-size outside about 15 to 25 px; any text under 12 px. | exact `type.small-text` |
| Modular scale | Type sizes derived from one ratio, so each step is distinct from and related to the next. | [SRC-WEB-035] | Adjacent font sizes less than 10 percent apart, each used more than once. | exact `type.scale-near-duplicate` |
| Heading ladder | Heading levels step down in visual weight in level order, with as few levels as the text needs. | [SRC-WEB-034] | A lower heading level (h3) rendered larger or heavier than a higher one (h2) on the same page. | exact `type.heading-ladder` |
| Tabular figures | Digits of one width, so numbers in a column line up. | [SRC-WEB-036] | Digits 1, 0 and 8 rendered at different widths in the cells of a numeric table column (measured, so a font whose digits are equal by default passes). | exact `type.tabular-figures` |
| Rag and widow | The shape of the ragged line ends; a lone last word on a heading's final line. | [SRC-WEB-037] | A heading whose last line holds one word at a screenshot width. | exact `type.widow` |
| Family budget | The number of typefaces in use; each family needs a job. | [SRC-WEB-032] | More than 3 primary families in computed font-family. | exact `type.families` |
| Intrinsic layout | Content and available space decide wrapping and size, not fixed widths at fixed breakpoints. | [SRC-WEB-033] [SRC-WEB-016] | Horizontal overflow at a screenshot width. | exact `wcag.overflow` |
| Space scale | A small fixed set of spacing steps used everywhere, ideally fluid between two viewports. | [SRC-WEB-017] | Share of gap, margin, and padding values off the page's own step set. | exact |
| Reflow | Content fits 320 CSS px of width without scrolling in two directions. | [SRC-A11Y-001] | scrollWidth greater than clientWidth at 320 px wide. | exact `wcag.reflow` |
| Shared edge | Parts that belong together start on one alignment line, taken from a grid. | [SRC-WEB-041] | Text left edges 1 to 6 px apart in one landmark; matching parts of sibling cards at different heights. | exact `layout.edge-near-miss` `layout.alignment` |
| Proximity | Things near each other read as a group; space between groups separates them. | [SRC-VIZ-029] | A heading with less than 0.75 times as much space above it as below it, in a stacked layout (a one-line label above it is read as part of the heading). | exact `layout.proximity` |
| Visual hierarchy | The order of attention, set by size, color and contrast, and grouping. | [SRC-WEB-038] | No element clearly leads the view; primary and secondary actions look alike. | jev `visual.hierarchy` |
| Density | Content per area, matched to the task: scanning wants air, operating wants more on screen. | [SRC-WEB-038] [SRC-WEB-031] | Large empty areas with little content; gaps below the smallest space step. | jev `tell.sparse` |
| Signifier | A visible cue that something can be acted on. | [SRC-WEB-039] | Links in prose with neither underline nor another non-color cue; static text styled like a link. | exact |
| Information scent | How well a label predicts what is behind it. | [SRC-WEB-040] | Link or button text that says nothing out of context ("more", "click here"); one label for different targets. | jev |
| Empty state | What a container shows with nothing in it: why it is empty and the next action. | [SRC-PROD-012] [SRC-PROD-018] | A list or table rendered with zero rows and no text or action. | exact |
| Error identification | The field in error is named and the problem described in text next to it. | [SRC-A11Y-006] [SRC-A11Y-009] | aria-invalid="true" without aria-describedby pointing at visible error text. | exact |
| Status message | A result or progress update announced without moving focus. | [SRC-A11Y-023] | A toast or inline result outside role="status", role="alert", or aria-live. | exact |
| Target size | The hit area of a control. | [SRC-A11Y-001] | A pointer target under 24 by 24 CSS px without the spacing exception. | exact `wcag.targets` |
| Accessible name | The text assistive technology announces for a control. | [SRC-A11Y-035] [SRC-TOOL-001] | An interactive element with an empty computed name, such as an icon button without a label. | exact |
| Contrast ratio | Luminance ratio of text against its background. | [SRC-A11Y-031] | Text under 4.5:1, or large text under 3:1, against the composited background in each scheme. | exact `wcag.contrast` |
| Non-text contrast | Control boundaries, focus indicators, and meaningful graphics against their neighbors. | [SRC-VIZ-008] | An input whose border, fill, and shadow are all under 3:1 against the color behind it (chart lines are not checked yet). | exact `wcag.non-text-contrast` |
| Focus visible | The keyboard focus position can always be seen. | [SRC-A11Y-032] | Outline and box-shadow identical in focused and unfocused state while tabbing. | exact `wcag.focus-visible` |
| Focus not obscured | A focused element is never hidden behind a sticky header, banner, or widget. | [SRC-A11Y-001] | The focused element's box fully covered by a fixed or sticky layer. | exact `wcag.focus-not-obscured` |
| Use of color | Color is never the only carrier of meaning. | [SRC-VIZ-007] | Status, required fields, or series told apart by hue alone. | jev |
| Text spacing | Layout survives a reader's larger line, paragraph, letter, and word spacing. | [SRC-A11Y-033] | With the 1.4.12 override stylesheet injected, text clips or overflows. | exact `wcag.text-spacing` |
| Resize text | Text scales to 200 percent without losing content or function. | [SRC-A11Y-034] | With the root font-size doubled, text clips or overlaps, or controls disappear. | exact |
| Reduced motion | Honor the system request to remove or soften non-essential motion. | [SRC-WEB-004] [SRC-WEB-005] [SRC-WEB-002] | With prefers-reduced-motion: reduce emulated, transform or scroll animations still run longer than a few frames. | exact `motion.reduced` |
| Purposeful motion | Motion explains a change (origin, continuity, state) instead of decorating. | [SRC-WEB-020] | An animation tied to no state change or action, or one looping on idle content. | judge |
| Pause, stop, hide | Content that moves on its own for more than 5 seconds can be paused. | [SRC-WEB-003] | A carousel, marquee, or autoplay video without a pause control. | exact |
| Layout shift | Visible content moving without user input. | [SRC-WEB-012] | Cumulative Layout Shift above 0.1. | exact `perf.layout-shift` |
| Design token | A named design decision shared by design and code. | [SRC-PROD-002] | Share of colors and spacings in component CSS set as raw literals instead of custom properties. | exact |
| Scheme parity | Light and dark show the same content with the same legibility. | [SRC-PROD-036] [SRC-A11Y-031] | In the dark screenshot, unreadable text or regions left light. | jev `layout.dark` |
| Proportional ink | Shaded area is proportional to the value it shows, so bars start at zero. | [SRC-VIZ-037] [SRC-VIZ-021] | A bar or area chart whose value axis excludes zero. | exact |
| Direct labeling | Series are named at the data instead of in a separate legend. | [SRC-VIZ-038] [SRC-VIZ-006] | A legend for more than about 3 series and no labels at the line ends. | jev |
| Redundant coding | A second channel such as shape, pattern, or label repeats what color encodes. | [SRC-VIZ-038] [SRC-VIZ-007] | Series that differ in hue only. | jev |
| Generic tell | A default-template pattern that shows no design decision was made. | [SRC-WEB-031] [SRC-WEB-029] | Centered hero over three equal cards, violet gradient, one radius and padding everywhere; full list in `generic-tells.md`. | jev `tell.hero-cards` `tell.gradient` `tell.uniform` |
| Placeholder content | Invented names, lorem ipsum, and round made-up numbers standing in for real content. | [SRC-WEB-031] | Text such as Acme, Jane Doe, lorem ipsum, or 10,000+. | jev `tell.placeholder` |

## Not admitted

- Typographic (curly) quotes on rendered pages: house plain punctuation wins, so
  straight quotes are correct everywhere (owner decision, 2026-11-24).
- The three-click rule and "the fold": retired folklore; people keep clicking and
  scrolling while the scent holds, so judge information scent and what the first
  screen promises instead.
- APCA as a pass or fail rule: a WCAG 3 candidate, not normative [SRC-A11Y-002];
  advice next to the 2.x ratio at most.
- HSL lightness as a contrast proxy, a fixed 60-30-10 color split, and "always 12
  columns": recipes with no observable benefit; compute the ratio, use the grid
  the content needs.
- Kerning, optical sizing, logical properties, container queries, fluid type:
  real terms with a weak marker or low review value; they return when a check
  needs them.
