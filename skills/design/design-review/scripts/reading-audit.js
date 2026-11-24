// Reading-page audit: contrast, text size, line height, line length, target
// size and overflow, at WCAG AA (default) or AAA.
// A single function expression: no dependencies, no globals, no side effects.
// Playwright: const r = await page.evaluate(fs.readFileSync(path, "utf8"));
//   (emulate the scheme first: page.emulateMedia({ colorScheme: "dark" }),
//   and set the viewport, e.g. 390 x 800, before calling).
// Console: paste "(" + this file + ")()" and read the returned object.
// Options: { level: "aa" | "aaa", skip: "extra css selector", minChars: 45, maxChars: 75 }
//   aa  (default): contrast 4.5:1 (3:1 large text, 1.4.3), targets 24px (2.5.8),
//       no overflow at the viewport (1.4.10). Text size, line height (1.4.8 is
//       AAA) and line length come back as `notes`, not `findings`.
//   aaa: contrast 7:1 (4.5:1 large, 1.4.6), targets 44px (2.5.5); text size,
//       line height 1.5 and line length are failures.
// Too-narrow columns are only checked at 768px and wider; phones are narrow by nature.
// Limits: background images and gradients are not composited; text on them
// needs a person.
(opts = {}) => {
  const AAA = opts.level === "aaa";
  const NOTE = AAA ? [] : ["fontSize", "lineHeight", "lineLength"];
  const SKIP = ".mermaid, script, style, noscript, svg" + (opts.skip ? ", " + opts.skip : "");
  const MIN_CH = opts.minChars || 45;
  const MAX_CH = opts.maxChars || 75;
  const ctx = document.createElement("canvas").getContext("2d", { willReadFrequently: true });
  const rgba = (css) => {
    ctx.clearRect(0, 0, 1, 1);
    ctx.fillStyle = "#000";
    ctx.fillStyle = css;
    ctx.fillRect(0, 0, 1, 1);
    const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data;
    return [r, g, b, a / 255];
  };
  const over = (top, bottom) => {
    const a = top[3] + bottom[3] * (1 - top[3]);
    return [0, 1, 2].map((i) => (top[i] * top[3] + bottom[i] * bottom[3] * (1 - top[3])) / (a || 1)).concat(a);
  };
  const lum = ([r, g, b]) => {
    const f = (v) => ((v /= 255) <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4);
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const ratio = (a, b) => {
    const [hi, lo] = [lum(a), lum(b)].sort((x, y) => y - x);
    return (hi + 0.05) / (lo + 0.05);
  };
  const background = (el) => {
    const layers = [];
    for (let n = el; n; n = n.parentElement) {
      const c = rgba(getComputedStyle(n).backgroundColor);
      if (c[3] > 0) layers.push(c);
      if (c[3] === 1) break;
    }
    // Canvas default is white in light and black in dark when nothing opaque is set.
    const dark = matchMedia("(prefers-color-scheme: dark)").matches;
    return layers.reduceRight((below, layer) => over(layer, below), dark ? [0, 0, 0, 1] : [255, 255, 255, 1]);
  };
  const name = (el) => {
    const id = el.id ? "#" + el.id : "";
    const cls = typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/).join(".") : "";
    return el.tagName.toLowerCase() + id + cls;
  };
  const visible = (el) => el.getClientRects().length > 0 && getComputedStyle(el).visibility !== "hidden";
  const skipped = (el) => el.closest(SKIP) !== null;
  const hasOwnText = (el) => [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
  const snippet = (el) => el.textContent.trim().replace(/\s+/g, " ").slice(0, 40);
  const out = { contrast: [], fontSize: [], lineHeight: [], lineLength: [], targets: [], overflow: [] };
  const notes = { contrast: [], fontSize: [], lineHeight: [], lineLength: [], targets: [], overflow: [] };
  const add = (key, el, observed, required) => (NOTE.includes(key) ? notes : out)[key].push({ element: name(el), text: snippet(el), observed, required });

  for (const el of document.body.querySelectorAll("*")) {
    if (skipped(el) || !visible(el) || !hasOwnText(el)) continue;
    const cs = getComputedStyle(el);
    const size = parseFloat(cs.fontSize);
    const bg = background(el);
    const fg = over(rgba(cs.color), bg);
    const large = size >= 24 || (size >= 18.66 && parseInt(cs.fontWeight, 10) >= 700);
    const need = AAA ? (large ? 4.5 : 7) : large ? 3 : 4.5;
    const got = Math.round(ratio(fg, bg) * 100) / 100;
    if (got < need) add("contrast", el, got, need);

    if (el.matches("p, li, dd, td")) {
      if (size < 16) add("fontSize", el, size, 16);
      const lh = cs.lineHeight === "normal" ? 1.2 * size : parseFloat(cs.lineHeight);
      const rel = Math.round((lh / size) * 100) / 100;
      if (rel < 1.5) add("lineHeight", el, rel, 1.5);
    }

    if (el.matches("p")) {
      const lines = new Map();
      for (const node of [...el.childNodes].filter((n) => n.nodeType === 3)) {
        const r = document.createRange();
        for (let i = 0; i < node.length; i++) {
          r.setStart(node, i);
          r.setEnd(node, i + 1);
          const rect = r.getClientRects()[0];
          if (rect) lines.set(Math.round(rect.top), (lines.get(Math.round(rect.top)) || 0) + 1);
        }
      }
      const counts = [...lines.entries()].sort((a, b) => a[0] - b[0]).map((e) => e[1]);
      const full = counts.slice(0, -1);
      const widest = Math.max(0, ...counts);
      const avg = full.length ? full.reduce((a, b) => a + b, 0) / full.length : widest;
      if (el.textContent.trim().length >= 100) {
        if (widest > MAX_CH) add("lineLength", el, widest, "at most " + MAX_CH + " characters per line");
        else if (innerWidth >= 768 && full.length && avg < MIN_CH) add("lineLength", el, Math.round(avg), "at least " + MIN_CH + " characters per line");
      }
    }
  }

  const interactive = 'a[href], button, input:not([type="hidden"]), select, textarea, summary, [role="button"], [role="link"]';
  for (const el of document.body.querySelectorAll(interactive)) {
    if (skipped(el) || !visible(el)) continue;
    const inline = el.matches("a") && getComputedStyle(el).display === "inline" && el.parentElement &&
      [...el.parentElement.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
    if (inline) continue; // 2.5.8 and 2.5.5 exempt targets inside a sentence
    const r = el.getBoundingClientRect();
    const min = AAA ? 44 : 24;
    if (r.width < min || r.height < min) add("targets", el, Math.round(r.width) + "x" + Math.round(r.height), `at least ${min}x${min} px`);
  }

  const root = document.documentElement;
  if (root.scrollWidth > root.clientWidth) out.overflow.push({ element: "html", text: "", observed: root.scrollWidth, required: "at most " + root.clientWidth + " px" });

  const count = Object.values(out).reduce((n, list) => n + list.length, 0);
  return { level: AAA ? "aaa" : "aa", viewport: innerWidth, scheme: matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light", count, findings: out, notes };
}
