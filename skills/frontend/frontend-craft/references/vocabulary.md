# Frontend Engineering Vocabulary

The terms frontend engineers use to judge markup, CSS, and runtime behavior,
so a review names the gap the way the field does and points at something a
reader can see in the DOM, the stylesheet, or a field performance report. Load
before judging frontend code. Design terms (type, layout, contrast, focus,
motion, layout shift) belong to `design-core`'s vocabulary when it is
installed; this file keeps only the engineering terms. A term is admitted only
with a registered source and an observable marker; evidence and access dates
are in `sources.json`. Check: `exact` (a DOM, CSS, or report pattern a script
can match; none ships here yet, so no rule ids), `jev` (a typed question),
`judge` (a person or model decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Field p75 | Core Web Vitals judged on real-user data at the 75th percentile, per device class. | [SRC-WEB-012] | Performance judged by a single lab score with no field data. | judge |
| LCP | Time until the largest content element renders; good within 2.5 s. | [SRC-WEB-012] [SRC-WEB-014] | The likely LCP image has `loading="lazy"`, or LCP over 2.5 s at p75. | exact |
| INP | Latency from an interaction to the next paint; good at 200 ms or less. | [SRC-WEB-012] [SRC-WEB-013] | INP over 200 ms at p75, or a long task inside a click handler. | exact |
| Reserved space | Room held for media and late content so nothing moves when it loads. | [SRC-FE-001] [SRC-WEB-015] | `img` or `iframe` without width and height or aspect-ratio; results inserted above content with no placeholder. | exact |
| Responsive image | `srcset` with width descriptors and a `sizes` attribute, so the browser picks a fitting file. | [SRC-WEB-015] | `srcset` with `w` descriptors and no `sizes`, or one large file for every width. | exact |
| Container query | A component that responds to its container's size, not the viewport's. | [SRC-WEB-016] | A component placed in containers of different widths but styled only by viewport media queries. | judge |
| Semantic HTML | Native elements that carry role, state, and keyboard behavior. | [SRC-FE-009] | A `div` or `span` with a click handler where `button` or `a` fits. | exact |
| First rule of ARIA | Use a native element before adding ARIA; ARIA obliges you to script its behavior. | [SRC-FE-010] | `role="button"`, `role="link"`, or `role="checkbox"` on an element that has a native equivalent. | exact |
| Positive tabindex | A tabindex above zero that overrides the source order. | [SRC-FE-009] | Any `tabindex` value greater than 0. | exact |
| Toggle button | A `button` with `aria-pressed` and a label that names what it toggles. | [SRC-FE-004] | A toggle with no pressed state, or one that changes both its label and its pressed state. | judge |
| Navigation is not a menu | Site navigation is a list of links, not an ARIA menu. | [SRC-FE-005] | `role="menu"` or `role="menuitem"` on navigation links. | exact |
| Native dialog | `dialog` opened with `showModal()`, which moves focus and closes on Escape. | [SRC-FE-014] | A custom modal that does not move focus, close on Escape, or offer a close button. | judge |
| Progressive enhancement | A working baseline of content and function, with richer behavior added where supported. | [SRC-FE-011] | A form or link that does nothing until JavaScript has loaded. | judge |
| Logical properties | Block and inline, start and end instead of top, bottom, left, and right. | [SRC-FE-012] | `margin-left`, `padding-right`, or `left` for flow direction in a component. | exact |
| Border-box | Declared sizes include padding and border, set globally. | [SRC-FE-002] | No global `box-sizing: border-box`, or widths computed to subtract padding. | exact |
| Stack | Spacing between siblings set by their parent, not by each component. | [SRC-FE-003] [SRC-FE-007] | Components that carry their own outer margin. | judge |
| Composition layer | Layout and flow rules kept apart from a component's visual treatment. | [SRC-FE-006] [SRC-FE-007] | One class that sets grid placement and colors, fonts, or shadows together. | judge |
| Exception | A deviation from a component's default, expressed as a data or ARIA attribute hook. | [SRC-FE-008] | State shown by JavaScript-toggled modifier classes where a `data-state` or ARIA attribute already exists. | judge |
| Cascade layers | Explicit `@layer` order that decides precedence before specificity. | [SRC-FE-013] | Reset, vendor, and app CSS competing unlayered by selector weight. | judge |
| Specificity | The selector weight the cascade uses to choose a declaration. | [SRC-FE-015] | ID selectors, chained selectors, or `!important` in component CSS to win an override. | exact |

## Not admitted

- A lab performance score as the goal: users experience the field p75
  [SRC-WEB-012].
- ARIA roles on generic elements as the way to make UI accessible: "no ARIA
  is better than bad ARIA" [SRC-FE-010].
- `!important` or ID selectors as the fix for an override: set layer order
  [SRC-FE-013] [SRC-FE-015].
- Lazy-loading every image, the hero included [SRC-WEB-014].
- An ARIA menu for site navigation [SRC-FE-005].
- Pixel-perfect fixed layouts as the composition target [SRC-FE-007].
