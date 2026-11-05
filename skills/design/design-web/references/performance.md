# Performance

Design decisions that set a site's Core Web Vitals: the hero, images,
fonts, and motion libraries. Measuring and fixing code is `frontend-craft`'s
job; this file sets the budget the design must fit.

## Trigger

Setting a budget for a new site or template; choosing a hero, image
strategy, font set, or animation or 3D library; a page that feels slow.

## Thresholds (as of 2026-10-21)

Good at the 75th percentile of page loads, mobile and desktop measured
separately (verified) [SRC-WEB-012]:

| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP, Largest Contentful Paint | at most 2.5 s | - | - |
| INP, Interaction to Next Paint | at most 200 ms | 200-500 ms | over 500 ms |
| CLS, Cumulative Layout Shift | at most 0.1 | - | - |

The INP bands come from [SRC-WEB-013] (verified). The LCP and CLS
"needs improvement" bands were not captured in the research, so they are
left blank rather than quoted from memory.

These are field thresholds. Lab tools (Lighthouse, a DevTools trace) only
approximate them, so a lab pass before launch is a prediction and field
data after launch is the verdict (verified) [SRC-WEB-012].

## Decision tree

1. **What is the LCP element per template?** Name it at design time: the
   hero image, the headline, the product photo. If it is a canvas or WebGL
   scene, the generic LCP guidance does not cover it, so budget it as a
   risk and test early (verified that the guidance does not cover it)
   [SRC-WEB-014].
2. **Is it an image?** Apply the image rules below.
3. **Does the page need a motion or 3D library?** Default no. CSS
   transitions, view transitions, and scroll-driven animation cover most
   jobs without main-thread JS (supported) [SRC-WEB-008] [SRC-WEB-011]. If
   yes, load it after first render and trace INP with it running, because
   heavy main-thread animation is a plausible INP risk the INP guidance does
   not quantify (hypothesis) [SRC-WEB-013].
4. **What arrives late and moves the layout?** Cookie banners, badges,
   price or stock, ads, web fonts. Reserve their space in the design.

## Image rules

All verified practice from web.dev [SRC-WEB-014] [SRC-WEB-015]:

- Never lazy-load the LCP image.
- Put the LCP image in the initial HTML as an `<img>`; an image injected by
  JS, hidden in `data-src`, or set as a CSS background is not discoverable
  early.
- `fetchpriority="high"` on the likely LCP image, and on one or two images
  at most, because prioritizing everything prioritizes nothing.
- Host critical resources on the same origin to reuse the connection.
- `srcset` with width descriptors needs `sizes`; give every image `width`
  and `height` so the browser reserves space.
- Do not preload different formats per browser; it causes extra downloads.

```html
<img src="/img/hero-1280.avif"
     srcset="/img/hero-640.avif 640w, /img/hero-1280.avif 1280w, /img/hero-1920.avif 1920w"
     sizes="100vw" width="1920" height="1080"
     fetchpriority="high" alt="Finished courtyard garden, Hamburg-Ottensen, 2025">
```

## Motion and performance

- Animate `transform` and `opacity`, not layout properties (`frontend-craft`
  holds the rule).
- Autoplay hero video is both an LCP and a 2.2.2 question: provide a poster
  image as the LCP candidate and a pause control (verified for the control)
  [SRC-WEB-003].
- Reduced-motion users should not download what they will not see: load the
  WebGL or video bundle only when `matchMedia` allows motion (hypothesis;
  the reduced-motion requirement itself is in the core motion guide).

## Trade-offs

- A WebGL hero can be the brand moment the client wants. Ship it as an
  enhancement over a static LCP image, so the page is useful before the
  scene loads; the cost is two assets to design and maintain.
- Same-origin hosting of images and fonts helps LCP but may conflict with a
  CMS or DAM that serves from its own domain; measure before moving.

## Anti-patterns

- Lazy-loading every image, the hero included [SRC-WEB-014].
- `fetchpriority="high"` on a whole gallery [SRC-WEB-014].
- A JS-only shell that renders content after a large bundle; observed on
  an award site with about 1.9 MB JS behind 1.7 KB HTML (context-dependent,
  scan-based) [SRC-WEB-027].
- Quoting a Lighthouse score as the CWV result.

## Validation

- Lab, before launch: throttled mobile trace per template; confirm the LCP
  element is the one named in design, LCP within budget, no layout shifts
  from late content, no long tasks on the main interactions.
- Field, after launch: CrUX or RUM at p75, mobile and desktop separately
  [SRC-WEB-012]. Until field data exists, write "not measured" for field
  CWV.

## Evidence gaps

- WebGL and canvas heroes as LCP candidates: no source in this research.
- No quantified link between animation libraries and INP.
- LCP and CLS "needs improvement" and "poor" bands were not captured.
