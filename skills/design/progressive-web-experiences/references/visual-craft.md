# Visual craft

Typography, grid, density, imagery, responsive behavior, and how to find a
visual direction in the content instead of a template. Tokens and theming
belong to `progressive-design-systems`; contrast enforcement belongs to
`frontend-craft`.

## Trigger

Choosing type, layout, or imagery for a site; a draft that looks like every
other landing page; a page that breaks between phone and desktop.

## Decision tree

1. Is there a brand system? Use its type, color, and imagery rules and spend
   effort on layout and hierarchy. Otherwise go to step 2.
2. Derive a direction from the content (below), write it as three to five
   constraints, then choose type and grid that serve them.
3. Is the page mostly reading (editorial, docs) or mostly scanning
   (marketing, storefront)? Reading pages optimize line length and rhythm;
   scanning pages optimize hierarchy and image rhythm.

## Typography

Defaults for body text on the web (context-dependent, one expert's rules,
not experimental) [SRC-WEB-018]:

- 15-25 px body size; line height 120-145 % of the size; 45-90 characters
  per line.
- Bold and italic sparingly; underline only links; centered text only for
  short lines; 5-12 % extra letter spacing for all caps.

These are a start, not a pass: the page must still survive 200 % zoom and
user text-spacing overrides (verified, WCAG 2.2 AA) [SRC-A11Y-001].

**Fluid type.** Define the type and space scale at a small and a large
viewport and let the browser interpolate with `clamp()`, instead of
hand-tuning sizes per breakpoint (context-dependent, practitioner method
without a reading study) [SRC-WEB-017]. Two endpoints are easier to review
than six breakpoints, which is the actual gain.

```css
:root {
  /* 18px at 360px viewport -> 21px at 1280px viewport */
  --step-0: clamp(1.125rem, 1.05rem + 0.33vw, 1.3125rem);
  /* 28px -> 44px */
  --step-3: clamp(1.75rem, 1.36rem + 1.74vw, 2.75rem);
}
```

Keep a `rem` term in every `clamp()` so browser zoom still scales the text;
a size set only in viewport-width units ignores zoom (supported; WCAG 1.4.4
resize text, not listed in the registry's findings) [SRC-A11Y-001].

## Grid and density

- One grid per site, with a content measure that respects the line-length
  range above (context-dependent) [SRC-WEB-018].
- Density follows the job: editorial and docs get air around text;
  storefront category pages get denser grids because comparison is the job
  (hypothesis).
- Whitespace groups; unrelated items placed close read as one group
  (supported) [SRC-VIZ-029].

## Responsive layout

- **Container queries for components.** A card, teaser, or product tile
  responds to its container (`container-type: inline-size`), not the
  viewport, so the same component works in a sidebar and a full-width row
  (verified) [SRC-WEB-016]. Container query units fall back to small
  viewport units when no container exists, so declare the container
  explicitly (verified) [SRC-WEB-016].
- **Media queries for page layout.** Navigation pattern and column count
  still depend on the viewport.
- Check 320 px, 375 px, a tablet width, and a wide desktop; no horizontal
  scroll at 320 px (`frontend-craft` holds the mobile rules).

## Imagery

- Real product, place, and people photos over stock, because stock hides
  the product the visitor came to judge (hypothesis, consistent with
  `frontend-craft`).
- Every content image has `width` and `height`, `srcset` with `sizes`
  (verified) [SRC-WEB-015]; the LCP rules live in `performance.md`.
- Decorative images get empty `alt`; informative ones get alt text that
  states what the image proves.
- Animated images swap to a still under reduced motion (supported)
  [SRC-WEB-005].

## The "generic AI landing page" look

Treat it as a hypothesis for a critique pass, not as evidence. A design-tool
vendor argues that generated landing pages converge on a centered hero,
three equal feature cards, and purple or blue gradients because generators
share training data; it offers no data, and no independent study was found
(hypothesis) [SRC-WEB-029]. Nothing shows these patterns hurt comprehension
or conversion. What the pattern does reliably is say nothing specific about
the organization, which is the problem worth fixing.

Derive a direction from the content instead:

1. **Inventory what is real.** List the assets only this organization has:
   product screenshots, places, people, data, a process, a material, a
   history, a voice. If the list is empty, the copy brief comes first.
2. **Pick the one carrier.** Choose the asset that best proves the page's
   claim and let it lead the composition (a product UI, a map, a material
   texture, a typeface). One carrier, not five (hypothesis).
3. **Write three to five constraints.** Example: "photography full-bleed,
   type never over images, one accent color from the brand, no cards on the
   homepage, numbers set in tabular figures". Constraints make reviews
   arguable; adjectives like "modern" do not.
4. **Test against swap.** Replace the logo with a competitor's. If the page
   still works, the direction is not derived from the content yet
   (hypothesis).
5. **Record the choice** as (aesthetic) in a decision record per
   `progressive-design-core`, so a later reviewer knows it was deliberate.

## Anti-patterns

- Type sizes set per breakpoint by hand with no scale.
- Body text over busy imagery or gradients.
- Components that only respond to the viewport and break in a sidebar.
- Three equal cards as the default feature layout (hypothesis)
  [SRC-WEB-029].
- Stock illustrations where a product screenshot exists.

## Validation

- 200 % zoom and text-spacing override: no clipping or overlap
  [SRC-A11Y-001].
- Line length measured at the widest container: within 45-90 characters
  [SRC-WEB-018].
- Each component checked in its narrowest and widest container.
- Swap test from the direction section done and written down.

## Example

A regional organic bakery chain with twelve shops.

- Real assets: shop photos, the bakers, flour from named mills, a
  daily-changing bread list.
- Carrier: the daily bread list, set large in a serif with tabular prices.
- Constraints: warm off-white background, one brand red for actions only,
  photography of real loaves, no icons in feature rows, the opening hours
  of the nearest shop in the first screenful.
- Screen text: DE "Heute im Ofen" / EN "Baking today"; DE "Filiale finden" /
  EN "Find a shop".
- Swap test: with a supermarket logo the page fails, because the mills and
  the bakers are named. The direction holds.

## Evidence gaps

- No independent evidence for or against the "generic AI look"; only a
  vendor blog.
- No reading study behind fluid type; it is a practitioner method.
- Baseline status of container queries was not captured from MDN in this
  research.
