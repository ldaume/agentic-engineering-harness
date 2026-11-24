// Design loop: screenshots of a page, cheap checks first, a model only when in doubt.
//
//   node design-loop.mjs <url> [--out dir] [--level aa|aaa] [--model provider/model] [--detail]
//
// Tiers, in order of cost:
//   dom    - generic-look tells read from the DOM (`tellsAudit`): free, exact, with a selector.
//   audit  - `reading-audit.js` at 1280 and 390 px, light and dark: contrast, targets, overflow;
//            plus `layout.alignment` (`alignmentAudit`): cards in one row whose matching parts
//            (title, text, divider, footnote) sit at different heights.
//   jev    - typed questions on the screenshots (TypeSafe Jev, images are an opt-in beta):
//            a noul is a yes/no probability, a score a level; about $0.0001 per page.
//   diagrams - each large svg, canvas, figure or [role=img] (up to 6) is shot on its own, sticky
//            layers hidden and clipping containers opened, and checked for clipped text, stacked
//            labels, lines through boxes and small text: exactly from inline SVG geometry, then
//            by Jev and the model like the page.
//   llm    - only the rules Jev was unsure about go to a vision model, in one call, which
//            decides them and says where the problem is and what to change. --detail sends
//            Jev's confident failures too, for their where and fix.
// Keys from the environment: AI_GATEWAY_API_KEY or VERCEL_AI_GATEWAY_API_KEY (Vercel AI
// Gateway: Jev and the escalation model), or TYPESAFE_API_KEY (Jev only, no escalation).
// Without a key the dom and audit tiers still run and the report says the visual tier was
// skipped. Every model call asks for zero data retention and no prompt training.
// The screenshots leave the machine: do not point it at a page that shows secrets or tokens.
// Exit code 1 when a finding fails, so a hook or CI step can block on it.
// Playwright refuses file:// in some sandboxes: serve the page on 127.0.0.1.
import { readFileSync, writeFileSync, mkdirSync, realpathSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const AUDIT = readFileSync(fileURLToPath(new URL("reading-audit.js", import.meta.url)), "utf8");
const GATEWAY = "https://ai-gateway.vercel.sh";
const TYPESAFE = "https://api.typesafe.ai/v1/systemone";
const JEV_USD_PER_TOKEN = { gateway: 0.04e-6, typesafe: 0.042e-6 };
const DEFAULT_MODEL = "anthropic/claude-haiku-5.5";
// Gateway options: no retention, no training on the request, and Jev only from TypeSafe itself.
const PRIVACY = { zeroDataRetention: true, disallowPromptTraining: true };
// Screenshots go only to providers that do not train on API data and sit outside restricted
// jurisdictions; any other model needs the owner's approval for that exact id
// (OWNER_APPROVED_MODELS, comma-separated). Families are matched in the id, so a proxy slug
// cannot hide one.
const APPROVED_PROVIDERS = ["anthropic", "openai", "google", "vertex"];
const RESTRICTED_FAMILIES = ["deepseek", "kimi", "moonshot", "qwen", "qwq", "alibaba", "glm", "chatglm", "zhipu", "z-ai", "zai", "minimax", "bytedance", "doubao", "seed-", "ernie", "baidu", "hunyuan", "tencent", "stepfun", "xiaomi", "mimo", "baichuan", "internlm", "01-ai", "meituan", "longcat", "inclusionai", "klingai", "nex-agi"];

export function checkModel(model, env = process.env) {
  const approved = (env.OWNER_APPROVED_MODELS || "").split(",").map((m) => m.trim()).filter(Boolean);
  if (approved.includes(model)) return model;
  const id = model.toLowerCase();
  const ask = `it needs the owner's approval for this exact id before it sees screenshots (OWNER_APPROVED_MODELS=${model})`;
  const family = RESTRICTED_FAMILIES.find((f) => new RegExp(`(?:^|[/:_.\\s-])${f.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}`).test(id));
  if (family) throw new Error(`${model} belongs to a restricted-jurisdiction model family (${family}); ${ask}`);
  if (!APPROVED_PROVIDERS.includes(id.split("/")[0])) throw new Error(`${model} comes from a provider outside the approved list; ${ask}`);
  return model;
}

// Jev images: each side 280 to 1568 px, so a screenshot is the top 1568 px of the page.
const MAX_SIDE = 1568;
const SHOTS = [
  { name: "desktop-light", width: 1280, scheme: "light" },
  { name: "desktop-dark", width: 1280, scheme: "dark" },
  { name: "phone-light", width: 390, scheme: "light" },
  { name: "phone-dark", width: 390, scheme: "dark" },
];
const VISUAL_SHOTS = ["desktop-light", "phone-light", "desktop-dark"];
const LABEL = { "desktop-light": "desktop", "phone-light": "phone", "desktop-dark": "dark" }; // the names the questions use

// One question per rule; the ids are the rule ids in the report. Sources: generic-look
// tells (design-core), hierarchy and layout (design-web), disabled actions (design-product-ui).
export const VISUAL_RULES = [
  { id: "visual.hierarchy", type: "score", fail: 1, instructions: "In the desktop screenshot, how clear is the visual hierarchy: is there one obvious first thing to look at, then a clear reading order?", criteria: ["No clear first focus; everything competes at the same weight.", "A weak focus; several elements compete.", "A clear focus with minor competition.", "One obvious first focus and a clear order."] },
  { id: "visual.distinct", type: "score", fail: 0, instructions: "How specific to this product does the design in the screenshots look, versus a template that could fit any product?", criteria: ["A stock template; nothing points to this product.", "Mostly template with a few own touches.", "A recognizable own direction.", "Unmistakably this product."] },
  { id: "tell.hero-cards", type: "noul", instructions: "Does the desktop screenshot show a centered hero section followed by a row of three equal feature cards?" },
  { id: "tell.gradient", type: "noul", instructions: "Does the design use a purple-blue or violet-indigo decorative gradient?" },
  { id: "tell.emoji-icons", type: "noul", instructions: "Are emoji or generic line icons used as bullets or icons for features?" },
  { id: "tell.illustration", type: "noul", instructions: "Does the design use stock 3D renders or abstract blob illustrations instead of showing the product itself?" },
  { id: "tell.uniform", type: "noul", instructions: "Do all boxes share one radius, one padding and one height, so nothing stands out by size or shape?" },
  { id: "tell.slogan", type: "noul", instructions: "Is the main headline (see `headlines`) a slogan that could fit any product rather than saying what this one does?" },
  { id: "tell.placeholder", type: "noul", instructions: "Does the page show placeholder content: names like Acme or Jane Doe, lorem ipsum, or invented round numbers like 10,000+?" },
  { id: "layout.phone", type: "noul", instructions: "Does the phone screenshot show content that is cut off, overlapping, squeezed, or too small to read?" },
  { id: "layout.dark", type: "noul", instructions: "Does the dark screenshot show unreadable text, or a mix where some parts turned dark and others stayed light?" },
  { id: "ui.disabled", type: "noul", instructions: "Is there a greyed-out or disabled action with no visible reason why it cannot be used?" },
];

// Asked about each diagram on its own shot. Wording and thresholds from a spike on 7 synthetic
// diagrams, two runs (2026-11-24): one clean, one with every defect, one per single defect.
// Jev hit every single-defect case of clipped text, stacked labels and small text, and passed
// the clean one. "Does a line pass through a box it does not connect" scored 0.07 to 0.14 on
// true cases; the wording below hits a line across a label (0.84 to 0.90) but stays unsure
// (0.52 to 0.54) on a line across an empty part of a box, so that rule passes only when Jev is
// near-certain and otherwise goes to the model; on inline SVG the DOM tier checks it exactly.
export const DIAGRAM_RULES = [
  { id: "diagram.clipped-text", type: "noul", instructions: "Is any text in this diagram cut off, wrapped into a frame border, or partly hidden (for example a box or group title running past its frame)?" },
  { id: "diagram.overlap", type: "noul", yes: 0.6, no: 0.3, instructions: "Are two or more text labels drawn on top of each other?" },
  { id: "diagram.line-crossing", type: "noul", no: 0.2, instructions: "Does a connector line cross the text or the middle of a box?" },
  { id: "diagram.small-text", type: "noul", instructions: "Is any text in the diagram too small to read comfortably at this size?" },
];
const MAX_DIAGRAMS = 6;

// A noul between these bounds is unsure and goes to the model; so is a score within BAND of
// the first passing level. Jev's score confidence measures spread, not correctness, and
// gating on it escalated almost every page. Values from the spike on 8 pages (2026-11-24):
// 0.25/0.75 escalated 7 of 8 pages, 0.35/0.65 escalated 4 at the same recall.
const YES = 0.65;
const NO = 0.35;
const BAND = 0.25;

export function decide(rule, answer = {}) {
  if (rule.type === "score") {
    const score = Number(answer.score); // a position between levels, which count from 0
    if (!Number.isFinite(score)) return { status: "unsure", confidence: 0 };
    const boundary = rule.fail + 1;
    const confidence = Math.min(1, Math.abs(score - boundary));
    if (Math.abs(score - boundary) < BAND) return { status: "unsure", confidence, score };
    return { status: score < boundary ? "fail" : "pass", confidence, score };
  }
  const p = Number(answer.probability ?? answer.noul);
  if (!Number.isFinite(p)) return { status: "unsure", confidence: 0 };
  if (p >= (rule.yes ?? YES)) return { status: "fail", confidence: p, probability: p };
  if (p <= (rule.no ?? NO)) return { status: "pass", confidence: 1 - p, probability: p };
  return { status: "unsure", confidence: Math.abs(p - 0.5) * 2, probability: p };
}

// Runs in the page. Cards in one visual row (3+ siblings, same width, same structure, 2+ block
// children each) must line up part by part: the same child's top, a divider's included, may
// differ by at most TOL px, unless the bottoms line up (a part that grows to fill the card).
// A wrapped row is compared per visual row; fewer than 3 in a row is not a card row.
// Limit: structure is compared by tag sequence, two levels deep; cards of different build are skipped.
export function alignmentAudit() {
  const TOL = 4;
  const name = (el) => el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/).join(".") : "");
  const kids = (el) => [...el.children].filter((c) => c.getClientRects().length > 0 && getComputedStyle(c).position !== "absolute" && getComputedStyle(c).position !== "fixed");
  const block = (el) => !getComputedStyle(el).display.startsWith("inline");
  const spread = (xs) => Math.round(Math.max(...xs) - Math.min(...xs));
  const out = [];
  const compare = (cards, depth) => {
    const lists = cards.map((c) => kids(c).filter(block));
    if (lists[0].length < 2 || lists.some((l) => l.map((e) => e.tagName).join() !== lists[0].map((e) => e.tagName).join())) return;
    for (let i = 0; i < lists[0].length; i++) {
      const col = lists.map((l) => l[i].getBoundingClientRect());
      const top = spread(col.map((r) => r.top));
      if (top > TOL && spread(col.map((r) => r.bottom)) > TOL) {
        const text = lists[0][i].textContent.trim().replace(/\s+/g, " ").slice(0, 40);
        out.push({ element: `${name(cards[0])} > ${name(lists[0][i])} (child ${i + 1})`, text, observed: `${top} px spread across ${cards.length} cards`, required: `within ${TOL} px` });
        return; // everything below drifts with it
      }
      if (depth < 2) compare(lists.map((l) => l[i]), depth + 1);
    }
  };
  for (const parent of document.body.querySelectorAll("*")) {
    const items = kids(parent).filter(block);
    const rows = new Map();
    for (const el of items) {
      const r = el.getBoundingClientRect();
      const key = [...rows.keys()].find((t) => Math.abs(t - r.top) <= 2) ?? r.top;
      rows.set(key, [...(rows.get(key) || []), el]);
    }
    for (const row of rows.values()) {
      const w = row.map((e) => e.getBoundingClientRect().width);
      if (row.length >= 3 && spread(w) <= 0.1 * Math.max(...w)) compare(row, 0);
    }
  }
  return out;
}

// Runs in the page (page.evaluate). Each tell is a default taken without a decision;
// the report shows the selector so the agent can fix it or record why it stays.
export function tellsAudit() {
  const GENERIC_FONTS = ["inter", "system-ui", "-apple-system", "blinkmacsystemfont", "segoe ui", "roboto", "arial", "helvetica", "helvetica neue", "sans-serif", "ui-sans-serif"];
  const name = (el) => el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") +
    (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/).join(".") : "");
  const visible = (el) => el.getClientRects().length > 0 && getComputedStyle(el).visibility !== "hidden";
  const all = [...document.body.querySelectorAll("*")].filter(visible);
  const hits = [];
  const hit = (rule, el, detail) => { if (!hits.some((h) => h.rule === rule)) hits.push({ rule, element: name(el), detail }); };

  const typeface = [document.body, ...document.querySelectorAll("h1, h2")].filter(visible);
  const first = (el) => getComputedStyle(el).fontFamily.split(",")[0].trim().replace(/["']/g, "").toLowerCase();
  if (typeface.every((el) => GENERIC_FONTS.includes(first(el)))) hit("tell.font", document.body, "only " + first(document.body) + " or a system font, no display voice");

  const hue = ([r, g, b]) => {
    [r, g, b] = [r / 255, g / 255, b / 255];
    const max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min;
    if (d < 0.15) return null; // grey: no hue worth judging
    const h = max === r ? ((g - b) / d) % 6 : max === g ? (b - r) / d + 2 : (r - g) / d + 4;
    return (h * 60 + 360) % 360;
  };
  for (const el of all) {
    const cs = getComputedStyle(el);
    const box = el.getBoundingClientRect();
    if (cs.backgroundImage.includes("gradient") && box.width * box.height >= innerWidth * 200) { // a surface, not a button
      const colors = [...cs.backgroundImage.matchAll(/rgba?\((\d+), (\d+), (\d+)/g)].map((m) => m.slice(1, 4).map(Number));
      if (colors.some((c) => { const h = hue(c); return h !== null && h >= 230 && h <= 290; })) hit("tell.gradient", el, "violet-indigo gradient");
    }
    const left = parseFloat(cs.borderLeftWidth);
    if (left >= 3 && parseFloat(cs.borderTopWidth) < left && parseFloat(cs.borderTopLeftRadius) > 0 && cs.borderLeftStyle !== "none") hit("tell.left-bar", el, "colored left-edge bar on a rounded panel");
    if (/blur/.test(cs.backdropFilter || cs.webkitBackdropFilter || "") && !["sticky", "fixed"].includes(cs.position)) hit("tell.glass", el, "backdrop blur");
  }

  const pictograph = /\p{Emoji_Presentation}/u; // not ↔ or ©, which render as text
  for (const el of document.querySelectorAll("h2, h3, h4, li, dt")) {
    if (visible(el) && pictograph.test(el.textContent)) { hit("tell.emoji-icons", el, "emoji as an icon: " + el.textContent.trim().slice(0, 30)); break; }
  }

  const h1 = document.querySelector("h1");
  const centered = h1 && visible(h1) && getComputedStyle(h1).textAlign === "center" && h1.getBoundingClientRect().top < innerHeight;
  if (centered) {
    for (const el of all) {
      const kids = [...el.children].filter(visible);
      if (kids.length !== 3) continue;
      const r = kids.map((k) => k.getBoundingClientRect());
      const sameRow = r.every((b) => Math.abs(b.top - r[0].top) < 4);
      const sameSize = r.every((b) => Math.abs(b.width - r[0].width) <= r[0].width * 0.05 && Math.abs(b.height - r[0].height) <= r[0].height * 0.1);
      if (sameRow && sameSize && r[0].width >= 150) { hit("tell.hero-cards", el, "centered hero, then three equal cards"); break; }
    }
  }
  return hits;
}

// Runs in the page on one diagram element (locator.evaluate). Exact geometry checks on inline
// SVG, so no model is needed for these: text past the smallest box around it (or past the
// foreignObject that clips it), text boxes on top of each other, and a stroke-only line that
// runs through the inside of a leaf box holding neither of its ends. Canvas and images get none.
export function diagramAudit(root) {
  const hits = [];
  const hit = (rule, text, detail) => { if (!hits.some((h) => h.rule === rule)) hits.push({ rule, text, detail }); };
  const holds = (b, x, y, m = 0) => x >= b.left - m && x <= b.right + m && y >= b.top - m && y <= b.bottom + m;
  const within = (a, b) => a.left >= b.left - 1 && a.right <= b.right + 1 && a.top >= b.top - 1 && a.bottom <= b.bottom + 1;
  const svgs = root.tagName.toLowerCase() === "svg" ? [root] : [...root.querySelectorAll("svg")];
  for (const svg of svgs) {
    const boxes = [...svg.querySelectorAll("rect")].filter((r) => !r.closest("defs, marker, clipPath, mask, pattern"))
      .map((el) => el.getBoundingClientRect()).filter((b) => b.width > 4 && b.height > 4);
    // A Range measures the glyphs even where a foreignObject clips them.
    const texts = [...svg.querySelectorAll("text, foreignObject *")]
      .filter((el) => [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()) && !el.parentElement.closest("text"))
      .map((el) => { const r = document.createRange(); r.selectNodeContents(el); return { el, text: el.textContent.trim().replace(/\s+/g, " "), box: r.getBoundingClientRect() }; })
      .filter((t) => t.box.width > 0);
    for (const t of texts) {
      const cx = (t.box.left + t.box.right) / 2, cy = (t.box.top + t.box.bottom) / 2;
      const frame = boxes.filter((b) => holds(b, cx, cy)).sort((a, b) => a.width * a.height - b.width * b.height)[0];
      const fo = t.el.closest("foreignObject");
      if ((frame && !within(t.box, frame)) || (fo && !within(t.box, fo.getBoundingClientRect()))) hit("diagram.clipped-text", t.text, "text runs past its box or frame");
    }
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i].box, b = texts[j].box;
      if (texts[i].el.contains(texts[j].el) || texts[j].el.contains(texts[i].el)) continue;
      if (Math.min(a.right, b.right) - Math.max(a.left, b.left) > 2 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 2) hit("diagram.overlap", texts[i].text + " / " + texts[j].text, "labels drawn on top of each other");
    }
    const leaves = boxes.filter((b) => !boxes.some((o) => o !== b && within(o, b)));
    const lines = [...svg.querySelectorAll("path, line, polyline")].filter((el) => !el.closest("defs, marker, clipPath, mask, pattern")
      && (el.tagName === "line" || getComputedStyle(el).fill === "none") && getComputedStyle(el).stroke !== "none");
    for (const el of lines) {
      const length = el.getTotalLength(), steps = Math.min(400, Math.max(10, Math.ceil(length / 4))), ctm = el.getScreenCTM();
      if (!length || !ctm) continue;
      const points = Array.from({ length: steps + 1 }, (_, k) => el.getPointAtLength((length * k) / steps).matrixTransform(ctm));
      const [start, end] = [points[0], points[points.length - 1]];
      for (const b of leaves) {
        if (holds(b, start.x, start.y, 6) || holds(b, end.x, end.y, 6)) continue;
        if (points.some((p) => holds({ left: b.left + 3, right: b.right - 3, top: b.top + 3, bottom: b.bottom - 3 }, p.x, p.y))) {
          const label = texts.find((t) => holds(b, (t.box.left + t.box.right) / 2, (t.box.top + t.box.bottom) / 2));
          hit("diagram.line-crossing", label ? label.text : "a box", "a line runs through a box it does not connect");
        }
      }
    }
  }
  return hits;
}

// Runs in the page: marks the outermost large diagram candidates; icons are too small to count.
function markDiagrams(max) {
  const big = (el) => { const b = el.getBoundingClientRect(); return b.width >= 300 && b.height >= 150 && getComputedStyle(el).visibility !== "hidden"; };
  const all = [...document.querySelectorAll("svg, canvas, figure, [role=img]")].filter(big);
  return all.filter((el) => !all.some((o) => o !== el && o.contains(el))).slice(0, max).map((el, i) => {
    el.setAttribute("data-design-loop-diagram", String(i));
    const b = el.getBoundingClientRect();
    return { index: i, where: `${el.tagName.toLowerCase()}${el.id ? "#" + el.id : ""}${(el.getAttribute("class") || "").trim() ? "." + el.getAttribute("class").trim().split(/\s+/)[0] : ""} at y=${Math.round(b.top + scrollY)}` };
  });
}

// Runs in the page: hides fixed and sticky layers and opens clipping ancestors so the shot shows
// the whole diagram; with `undo` it puts every changed style back.
function isolate(el, undo) {
  if (undo) { for (const [node, style] of window.__designLoopUndo || []) style === null ? node.removeAttribute("style") : node.setAttribute("style", style); window.__designLoopUndo = []; return; }
  const changed = window.__designLoopUndo = [];
  const set = (node, css) => { changed.push([node, node.getAttribute("style")]); Object.assign(node.style, css); };
  for (const node of document.querySelectorAll("body *")) if (["fixed", "sticky"].includes(getComputedStyle(node).position) && !node.contains(el)) set(node, { visibility: "hidden" });
  for (let a = el.parentElement; a && a !== document.documentElement; a = a.parentElement) {
    const cs = getComputedStyle(a);
    if (cs.overflowX !== "visible" || cs.overflowY !== "visible" || cs.maxHeight !== "none") set(a, { overflow: "visible", maxHeight: "none" });
  }
}

// Runs in the page: Jev takes each side between 280 and MAX_SIDE px, so a diagram is scaled down
// or padded on white to fit.
async function fitShot([base64, max]) {
  const img = new Image();
  img.src = "data:image/png;base64," + base64;
  await img.decode();
  const scale = Math.min(1, max / img.width, max / img.height);
  const w = Math.round(img.width * scale), h = Math.round(img.height * scale);
  if (scale === 1 && w >= 280 && h >= 280) return base64;
  const c = document.createElement("canvas");
  c.width = Math.max(280, w); c.height = Math.max(280, h);
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, c.width, c.height);
  ctx.drawImage(img, (c.width - w) / 2, (c.height - h) / 2, w, h);
  return c.toDataURL("image/png").split(",")[1];
}

// A diagram that cannot be shot is left out with a note, so the rest of the review still runs.
async function shootDiagrams(page, outDir, notes) {
  const diagrams = [];
  for (const d of await page.evaluate(markDiagrams, MAX_DIAGRAMS)) {
    const name = `diagram-${d.index + 1}`;
    const element = page.locator(`[data-design-loop-diagram="${d.index}"]`);
    try {
      const dom = await element.evaluate(diagramAudit);
      await element.evaluate(isolate);
      let raw;
      try { raw = await element.screenshot({ animations: "disabled", timeout: 10000 }); }
      finally { await element.evaluate(isolate, true); }
      const base64 = await page.evaluate(fitShot, [raw.toString("base64"), MAX_SIDE]);
      const path = join(outDir, name + ".png");
      writeFileSync(path, Buffer.from(base64, "base64"));
      diagrams.push({ name, where: d.where, path, dom, base64 });
    } catch (error) {
      notes.push(`${name} (${d.where}) not checked: ${error.message.split("\n")[0]}`);
    }
  }
  await page.evaluate(() => document.querySelectorAll("[data-design-loop-diagram]").forEach((el) => el.removeAttribute("data-design-loop-diagram")));
  return diagrams;
}

async function shoot(page, outDir, level) {
  const shots = [];
  const audit = [];
  for (const s of SHOTS) {
    await page.setViewportSize({ width: s.width, height: 800 });
    await page.emulateMedia({ colorScheme: s.scheme, reducedMotion: "reduce" });
    const height = await page.evaluate(() => document.documentElement.scrollHeight);
    const path = join(outDir, s.name + ".png");
    const buffer = await page.screenshot({ path, fullPage: true, clip: { x: 0, y: 0, width: s.width, height: Math.min(Math.max(height, 280), MAX_SIDE) } });
    shots.push({ ...s, path, base64: buffer.toString("base64") });
    const r = await page.evaluate(`(${AUDIT})(${JSON.stringify({ level })})`);
    for (const [key, list] of Object.entries(r.findings)) for (const f of list) audit.push({ key, ...f, viewport: s.width, scheme: s.scheme });
    for (const f of await page.evaluate(alignmentAudit)) audit.push({ key: "alignment", ...f, viewport: s.width, scheme: s.scheme });
  }
  return { shots, audit };
}

function auditFindings(audit) {
  const seen = new Map();
  for (const f of audit) {
    const id = `${f.key}|${f.element}|${f.text}`;
    if (seen.has(id)) { seen.get(id).evidence.where.push(`${f.viewport} ${f.scheme}`); continue; }
    seen.set(id, { rule: f.key === "alignment" ? "layout.alignment" : "wcag." + f.key, status: "fail", tier: "audit", confidence: 1, evidence: { element: f.element, text: f.text, observed: f.observed, required: f.required, where: [`${f.viewport} ${f.scheme}`] } });
  }
  return [...seen.values()];
}

// The page's three screenshots, labeled as the questions name them.
const pageImages = (shots) => VISUAL_SHOTS.map((n) => shots.find((s) => s.name === n))
  .map((s) => ({ key: LABEL[s.name], caption: `The ${LABEL[s.name]} screenshot (${s.width} px wide, ${s.scheme}):`, base64: s.base64 }));
const DIAGRAM_CONTEXT = "A diagram from a web page, shot on its own at the size the reader sees it.";

// One Jev call: text state, labeled images, typed questions.
async function askJev({ rules, state, images, keys, fetch }) {
  const questions = Object.fromEntries(rules.map((r) => [r.id, r.type === "score"
    ? { type: "score", instructions: r.instructions, criteria: r.criteria }
    : { type: keys.gateway ? "boolean" : "noul", instructions: r.instructions }]));
  let response;
  if (keys.gateway) {
    const stateParts = Object.entries(state).map(([k, v]) => ({ type: "text", text: `${k}: ${JSON.stringify(v)}` }));
    for (const s of images) stateParts.push({ type: "text", text: s.caption }, { type: "file", mediaType: "image/png", data: { type: "data", data: s.base64 } });
    response = await fetch(GATEWAY + "/v4/ai/decision-model", {
      method: "POST",
      headers: { Authorization: "Bearer " + keys.gateway, "Content-Type": "application/json", "ai-gateway-protocol-version": "0.0.1", "ai-decision-model-specification-version": "4", "ai-model-id": "typesafe-ai/jev", "TypeSafe-Danger-Zone-Images": "true" },
      body: JSON.stringify({ stateParts, questions, providerOptions: { gateway: { ...PRIVACY, only: ["typesafe-ai"] } } }),
    });
  } else {
    const refs = images.map((s) => `shot-${s.key}-${crypto.randomUUID()}`);
    const assets = Object.fromEntries(images.map((s, i) => [refs[i], { type: "image", format: "png", data_base64: s.base64 }]));
    response = await fetch(TYPESAFE, {
      method: "POST",
      headers: { Authorization: "Bearer " + keys.typesafe, "Content-Type": "application/json", "TypeSafe-Danger-Zone-Images": "true" },
      body: JSON.stringify({ model: "jev-latest", state: { ...state, ...Object.fromEntries(images.map((s, i) => [s.key, refs[i]])) }, assets, questions }),
    });
  }
  if (!response.ok) throw new Error(`Jev ${response.status}: ${(await response.text()).slice(0, 200)}`);
  const payload = await response.json();
  const confidence = payload.providerMetadata?.typesafe?.confidence || {};
  const answers = Object.fromEntries(Object.entries(payload.answers || {}).map(([id, a]) => [id, { ...a, confidence: a.confidence ?? confidence[id] }]));
  const tokens = payload.usage?.inputTokens ?? payload.usage?.input_tokens ?? 0;
  return { answers, cost: tokens * JEV_USD_PER_TOKEN[keys.gateway ? "gateway" : "typesafe"] };
}

async function askModel({ rules, intro, images, key, model, fetch, env }) {
  checkModel(model, env);
  const text = intro + "\nFor each rule answer whether it fails, where on which image, and the smallest fix.\n" +
    rules.map((r) => `- ${r.id}: ${r.instructions}${r.type === "score" ? ` Fail when the answer is one of: ${JSON.stringify(r.criteria.slice(0, r.fail + 1))}` : " Fail when yes."}`).join("\n") +
    '\nReply with JSON only: {"<rule id>": {"fail": true|false, "where": "...", "fix": "..."}}';
  const response = await fetch(GATEWAY + "/v1/chat/completions", {
    method: "POST",
    headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" },
    body: JSON.stringify({ model, max_tokens: 1500, messages: [{ role: "user", content: [{ type: "text", text }, ...images.map((s) => ({ type: "image_url", image_url: { url: "data:image/png;base64," + s.base64 } }))] }], providerOptions: { gateway: PRIVACY } }),
  });
  if (!response.ok) throw new Error(`model ${response.status}: ${(await response.text()).slice(0, 200)}`);
  const payload = await response.json();
  const content = payload.choices?.[0]?.message?.content || "{}";
  return { verdicts: firstJson(content), cost: payload.usage?.cost ?? 0 };
}

// The first balanced JSON object in a model reply; models add prose around it.
export function firstJson(text) {
  const start = text.indexOf("{");
  if (start < 0) return {};
  let depth = 0, quoted = false;
  for (let i = start; i < text.length; i++) {
    const c = text[i];
    if (quoted) { if (c === "\\") i++; else if (c === '"') quoted = false; continue; }
    if (c === '"') quoted = true;
    else if (c === "{") depth++;
    else if (c === "}" && --depth === 0) return JSON.parse(text.slice(start, i + 1));
  }
  return {};
}

// Jev first; only the rules it is unsure about go to the model, in one call. A confident Jev
// failure stands on its own unless the caller wants the model's where and fix too (`detail`).
// Jev is asked every rule, also those the DOM proved (`proven`): its answers shift with the
// question set, and the thresholds were calibrated on the full set. Throws when Jev fails.
async function judge({ rules, proven, keys, detail, evidence, jev, model }) {
  const r = { findings: [], passed: [], verdicts: {}, cost: { jev: 0, llm: 0 }, escalated: 0, llm: "not needed" };
  const answers = await jev(rules);
  r.cost.jev = answers.cost;
  const open = [];
  for (const rule of rules) {
    if (proven.has(rule.id)) continue; // the DOM already proved it, exactly
    const d = decide(rule, answers.answers[rule.id]);
    r.verdicts[rule.id] = d; // kept so a reader can see why a rule escalated
    if (d.status === "pass") r.passed.push(rule.id);
    else open.push({ rule, d });
  }
  const ask = open.filter(({ d }) => detail || d.status === "unsure");
  const jevFinding = ({ rule, d }) => ({ rule: rule.id, status: d.status, tier: "jev", confidence: d.confidence, evidence: { ...evidence }, detail: rule.instructions });
  r.findings.push(...open.filter((o) => !ask.includes(o)).map(jevFinding));
  r.escalated = ask.length;
  if (!ask.length) return r;
  if (!keys.gateway) {
    r.llm = "skipped: no gateway key";
    r.findings.push(...ask.map(jevFinding));
    return r;
  }
  try {
    const m = await model(ask.map((o) => o.rule));
    r.cost.llm = m.cost;
    r.llm = "ran";
    for (const o of ask) {
      const v = m.verdicts[o.rule.id];
      if (v && v.fail === false) r.passed.push(o.rule.id);
      else if (v) r.findings.push({ rule: o.rule.id, status: "fail", tier: "llm", confidence: o.d.confidence, evidence: { ...evidence, where: v.where || evidence.where }, detail: v.fix || o.rule.instructions });
      else r.findings.push(jevFinding(o));
    }
  } catch (error) {
    r.llm = "failed: " + error.message;
    r.findings.push(...ask.map(jevFinding));
  }
  return r;
}

// Reviews the page that is already loaded in `page`; viewport and scheme change in place.
export async function review(page, { env = process.env, fetch = globalThis.fetch, outDir, level = "aa", model = DEFAULT_MODEL, detail = false } = {}) {
  const started = Date.now();
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, ".gitignore"), "*\n"); // screenshots and report never reach a commit
  const { shots, audit } = await shoot(page, outDir, level);
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.emulateMedia({ colorScheme: "light" });
  // A diagram far down a long page never reaches the 1568 px screenshots: each gets its own shot.
  const notes = [];
  const diagrams = await shootDiagrams(page, outDir, notes);
  const dom = await page.evaluate(tellsAudit);
  const headlines = await page.evaluate(() => [...document.querySelectorAll("h1, h2")].slice(0, 6).map((h) => h.textContent.trim().replace(/\s+/g, " ").slice(0, 120)));
  const findings = [
    ...dom.map((d) => ({ rule: d.rule, status: "fail", tier: "dom", confidence: 1, evidence: { element: d.element, where: "desktop-light" }, detail: d.detail })),
    ...auditFindings(audit),
    ...diagrams.flatMap((g) => g.dom.map((d) => ({ rule: d.rule, status: "fail", tier: "dom", confidence: 1, evidence: { diagram: g.name, where: g.where, element: d.text }, detail: d.detail }))),
  ];
  const cost = { jev: 0, llm: 0 };
  const keys = { gateway: env.AI_GATEWAY_API_KEY || env.VERCEL_AI_GATEWAY_API_KEY, typesafe: env.TYPESAFE_API_KEY };
  const dark = shots.find((s) => s.name === "desktop-dark").base64 !== shots.find((s) => s.name === "desktop-light").base64;
  if (!dark) notes.push("no dark scheme: the dark screenshots equal the light ones");
  const rules = VISUAL_RULES.filter((r) => dark || r.id !== "layout.dark");
  const tiers = { dom: "ran", audit: `ran (${level})`, visual: "skipped: no model key", llm: "not needed", diagrams: diagrams.length ? `${diagrams.length} shot, dom ran` : "none found" };
  const passed = [];
  let verdicts = {};
  let escalated = 0;
  const llmTier = (status) => status === "ran" ? `ran (${model})` : status;
  const add = (r, prefix = "") => {
    findings.push(...r.findings);
    passed.push(...r.passed.map((id) => prefix + id));
    cost.jev += r.cost.jev;
    cost.llm += r.cost.llm;
    escalated += r.escalated;
    if (r.llm !== "not needed" && tiers.llm === "not needed") tiers.llm = llmTier(r.llm);
  };
  if (keys.gateway || keys.typesafe) {
    try {
      const images = pageImages(shots);
      const r = await judge({
        rules, proven: new Set(dom.map((d) => d.rule)), keys, detail, evidence: { where: VISUAL_SHOTS.join(", ") },
        jev: (rs) => askJev({ rules: rs, state: { headlines }, images, keys, fetch }),
        model: (rs) => askModel({ rules: rs, intro: "You review a web page against design rules. Images in order: " + VISUAL_SHOTS.join(", ") + ". headlines: " + JSON.stringify(headlines), images, key: keys.gateway, model, fetch, env }),
      });
      tiers.visual = "ran";
      verdicts = r.verdicts;
      add(r);
    } catch (error) {
      tiers.visual = "failed: " + error.message; // fail open: the cheap tiers still stand
    }
    for (const g of diagrams) {
      const images = [{ key: "diagram", caption: "The diagram:", base64: g.base64 }];
      try {
        const r = await judge({
          rules: DIAGRAM_RULES, proven: new Set(g.dom.map((d) => d.rule)), keys, detail, evidence: { diagram: g.name, where: g.where },
          jev: (rs) => askJev({ rules: rs, state: { context: DIAGRAM_CONTEXT }, images, keys, fetch }),
          model: (rs) => askModel({ rules: rs, intro: "You review one diagram from a web page, shot on its own at the size the reader sees it, against design rules.", images, key: keys.gateway, model, fetch, env }),
        });
        g.jev = r.verdicts;
        add(r, g.name + "/");
      } catch (error) {
        g.jev = { failed: error.message }; // fail open: the DOM findings for this diagram still stand
      }
    }
    if (diagrams.length) tiers.diagrams = `${diagrams.length} shot, dom ${diagrams.some((g) => g.jev?.failed) ? "ran, jev failed on some" : "and jev ran"}`;
  }
  const report = {
    url: page.url(), tiers, notes, findings, passed, escalated, jev: verdicts,
    cost_usd: { jev: +cost.jev.toFixed(6), llm: +cost.llm.toFixed(6) },
    seconds: +((Date.now() - started) / 1000).toFixed(1),
    shots: shots.map(({ base64, ...s }) => s),
    diagrams: diagrams.map(({ base64, dom, ...g }) => g),
  };
  writeFileSync(join(outDir, "design-loop.json"), JSON.stringify(report, null, 2));
  return report;
}

// Playwright from the project the agent works in first, then from beside the script: an installed Skill has no node_modules.
export async function loadChromium(cwd, scriptDir = dirname(realpathSync(fileURLToPath(import.meta.url)))) {
  for (const dir of [cwd, scriptDir]) {
    const req = createRequire(join(dir, "package.json"));
    for (const name of ["playwright", "@playwright/test"]) {
      try { return req(name).chromium; } catch {}
    }
  }
  throw new Error("Playwright not found in the current project or beside the script. Run: npm i --no-save playwright && npx playwright install chromium");
}

async function main(argv) {
  const args = { out: ".design-loop", level: "aa", model: DEFAULT_MODEL, detail: false };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--detail") args.detail = true;
    else if (argv[i].startsWith("--")) args[argv[i].slice(2)] = argv[++i];
    else args.url = argv[i];
  }
  const usage = "usage: node design-loop.mjs <url> [--out dir] [--level aa|aaa] [--model provider/model] [--detail]";
  if (argv.includes("--help")) { console.log(usage); return; }
  if (!args.url) { console.error(usage); process.exit(2); }
  const chromium = await loadChromium(process.cwd());
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    await page.goto(args.url, { waitUntil: "networkidle" });
    const report = await review(page, { outDir: args.out, level: args.level, model: args.model, detail: args.detail });
    console.log(JSON.stringify(report, null, 2));
    process.exitCode = report.findings.some((f) => f.status === "fail") ? 1 : 0;
  } finally {
    await browser.close();
  }
}

function sameFile(a, b) { try { return realpathSync(a) === realpathSync(b); } catch { return false; } }
// Compare real paths: an installed Skill is started through a symlink.
if (process.argv[1] && sameFile(process.argv[1], fileURLToPath(import.meta.url))) await main(process.argv.slice(2));
