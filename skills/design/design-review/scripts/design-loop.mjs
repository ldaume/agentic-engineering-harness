// Design loop: screenshots of a page, cheap checks first, a model only when in doubt.
//
//   node design-loop.mjs <url> [--out dir] [--level aa|aaa] [--model provider/model] [--detail]
//
// Tiers, in order of cost:
//   dom    - generic-look tells read from the DOM (`tellsAudit`): free, exact, with a selector. Also
//            `measuredAudit("slop")`: `tell.glow` and `tell.gray-on-color` block; `tell.icon-tile` and
//            `tell.nested-cards` are advisory (status "advisory", never fail the run).
//   audit  - `reading-audit.js` at 1280 and 390 px, light and dark: contrast, targets, overflow;
//            plus `layout.alignment` (`alignmentAudit`): cards in one row whose matching parts
//            (title, text, divider, footnote) sit at different heights. The width sweep is 360 to 1592 px in 32 px steps (light). Jev asks the same of
//            the screenshots as `tell.misaligned-cards`.
//            Type and layout craft (`craftAudit`, per screenshot viewport and scheme): `type.small-text`
//            (under 12 px), `type.scale-near-duplicate` (sizes under 10 percent apart, each used twice),
//            `layout.edge-near-miss` (text edges 1 to 6 px apart in one landmark) and `type.families`
//            (more than 3). `type.widow` (`widowAudit`, a lone last word in a heading or bold text of 16 px
//            or more) runs in the width sweep and reports bands, because it depends on wrapping.
//            Per screenshot viewport and scheme, `measuredAudit`: `render.hidden-at-rest` (before any scrolling),
//            `render.broken-image` and, last because it scrolls and restores, `render.text-occluded`.
//            Vocabulary rules (design-core `references/vocabulary.md`), also audit tier: per screenshot viewport and scheme
//            `vocabAudit` (`type.heading-ladder`, `layout.proximity`, `type.tabular-figures`, `wcag.non-text-contrast`,
//            `wcag.text-spacing`); at 320 px `reflowAudit` (`wcag.reflow`); with reduced motion emulated `motionAudit`
//            (`motion.reduced`); `shiftAudit` on the loaded page (`perf.layout-shift`); `focusAudit` tabbing through it
//            (`wcag.focus-visible`, `wcag.focus-not-obscured`). Only `wcag.reflow` and `wcag.non-text-contrast` fail the run;
//            the other eight are advisory until a real page confirms them.
//   jev    - typed questions on the screenshots (TypeSafe Jev, images are an opt-in beta):
//            a noul is a yes/no probability, a score a level; about $0.0001 per page. `tell.sparse` ("is
//            the page noticeably sparse") is a second Jev call of its own, so its context does not shift
//            the shared questions: the whitespace rules, a labeled NO and YES example (assets/examples)
//            and the shots cut 24 px below the last content, so blank viewport is never read as empty.
//            It detects sparse only, never cramped.
//   diagrams - each large svg, canvas, figure or [role=img] (up to 6) is shot on its own, sticky
//            layers hidden and clipping containers opened, and checked for clipped text, stacked
//            labels, lines through boxes and small text: exactly from inline SVG geometry (text size is
//            font size times the SVG scale, measured at 390 and 1280 px, floor 12 px; Jev decides it
//            only for a diagram without SVG text), then by Jev and the model like the page.
//   text   - the visible page text (headings, paragraphs, list items, captions; capped) checked for
//            sentences that tell the reader how to operate the page (swipe, scroll, click here):
//            first exactly by pattern, then, when no pattern hit, as one typed Jev question on the
//            text alone, with the model deciding when Jev is unsure.
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
const SWEEP = Array.from({ length: 39 }, (_, i) => 360 + 32 * i); // 360 to 1592 px
const VISUAL_SHOTS = ["desktop-light", "phone-light", "desktop-dark"];
const LABEL = { "desktop-light": "desktop", "phone-light": "phone", "desktop-dark": "dark" }; // the names the questions use

// layout.phone: the phone shot is the top 1568 px of the page, so text running off its bottom edge
// read as "cut off": 4 of 5 runs failed two clean real pages at 0.67 to 0.80 (2026-11-24). The
// question now names that cut; clean pages scored 0.10 to 0.21, real defects 0.64 to 0.95 (default band).
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
  { id: "layout.phone", type: "noul", instructions: "Does the phone screenshot show content that is cut off at its sides or inside its container, overlapping, squeezed, or too small to read? The screenshot is only the top part of a longer page and ends at an artificial cut: ignore anything cut off by the bottom edge of the image." },
  { id: "layout.dark", type: "noul", instructions: "Does the dark screenshot show unreadable text, or a mix where some parts turned dark and others stayed light?" },
  { id: "tell.misaligned-cards", type: "noul", instructions: "Look at each row of cards or tiles. Draw an imaginary horizontal line through a part of one card (its title, its divider, its footer or its button). Does that line miss the same part of a neighboring card by more than a few pixels? Empty space inside a card is not misalignment; only the position of the matching parts counts." },
  { id: "ui.disabled", type: "noul", instructions: "Is there a greyed-out or disabled action with no visible reason why it cannot be used?" },
];

// Context for tell.sparse, sent with the page screenshots: the rule in the house words and one
// labeled NO and one labeled YES example (synthetic pages, assets/examples). The question asks
// about sparse pages only. It never reports a cramped page: a spike on 22 shots found Jev's
// whitespace answer separated sparse pages from the rest but not cramped ones.
// Asked in its own Jev call, not in the shared one: a spike showed that rules plus labeled examples
// in the request pull every other answer (hierarchy scores fell, 21 of 22 pages flagged), and the
// shared rules are calibrated without that context. Thresholds: 11 pages twice each (2026-11-24).
export const SPARSE_RULE = { id: "tell.sparse", type: "noul", yes: 0.75, no: 0.5, instructions: "Is the page noticeably sparse: large empty areas with little content?" };
export const WHITESPACE_RULES = "Whitespace rules: padding and gaps follow one rhythm, and the space between groups is clearly larger than the space inside a group. A page is sparse when large empty areas strand a little content so that it feels unfinished. A short page that simply ends early, or a page with a few well-spaced groups, is not sparse. Only the question tell.sparse is asked about whitespace; cramped pages are not asked about.";
const EXAMPLE_DIR = new URL("../assets/examples/", import.meta.url);
export const sparseExamples = () => [
  { key: "sparse_example_answer_no", file: "sparse-no.png", caption: "tell.sparse example, answer NO (a filled page with balanced whitespace; synthetic, unrelated to the page under test):" },
  { key: "sparse_example_answer_yes", file: "sparse-yes.png", caption: "tell.sparse example, answer YES (one short line in a large empty panel; synthetic, unrelated to the page under test):" },
].map(({ file, ...e }) => ({ ...e, base64: readFileSync(new URL(file, EXAMPLE_DIR)).toString("base64") }));

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

// Asked about the page text, in its own call without screenshots, so the visual rules keep the
// question set they were calibrated on. Wording and thresholds from a spike on 16 synthetic
// pages, three runs (2026-11-24), each page alone and inside 40 blocks of other content:
// instructions scored 0.73 to 0.97 (one ambiguous "a tap on a box opens it" 0.16 to 0.29, a
// miss); product behavior 0.01 to 0.44, except the how-to step "Click Approve to publish",
// 0.66 to 0.81. So a fail needs 0.85 and the middle goes to the model.
export const TEXT_RULES = [
  { id: "text.ui-instructions", type: "noul", yes: 0.85, no: 0.35, instructions: "Does the page text contain a sentence that tells the reader how to operate this page or document itself (scroll, swipe, click, tap, zoom, hover, 'see below') instead of giving content? Describing how a product or app behaves, or a how-to step inside a product, does not count." },
];
const MAX_TEXT_BLOCKS = 80;

// The exact tier for text.ui-instructions. writing-core's quality_gate.py carries the same
// patterns as UI_INSTRUCTION; change both together. The verbs need the page as object, a
// direction or a reveal goal, so "Click Approve to publish" inside product docs stays quiet.
const START = String.raw`(?:^|(?<=[.!?:;,]\s)|(?<=\())`;
const UI_INSTRUCTION = new RegExp([
  String.raw`(?<!["'\u201e])\b(?:click|tap) here\b`, String.raw`(?<!["'\u201e])\bhier (?:klicken|tippen)\b`, String.raw`\bklicken sie hier\b`,
  String.raw`\b(?:see|siehe) (?:below|above|unten|oben)\b`,
  String.raw`(?:${START}|\byou can )(?:swipe|scroll)(?: the \w+)? (?:sideways|horizontally|left and right|down|up)\b`,
  String.raw`${START}(?:click|tap|hover|swipe|scroll|pinch|zoom)(?: (?:on|over) (?:the|this|a|an|any) (?:image|picture|photo|chart|diagram|graphic|figure|table|map|bar|point|node))? to (?:see|view|enlarge|zoom|expand|read|show|reveal|explore)\b`,
  String.raw`\blässt sich\b[^.!?\n]{0,40}?\b(?:wischen|scrollen|zoomen)\b`,
  String.raw`\b(?:kann man|können sie|kannst du)\b[^.!?\n]{0,40}?\b(?:wischen|scrollen|zoomen)\b`,
  String.raw`\b(?:zum|für) (?:vergrößern|zoomen|anzeigen|weiterlesen)\b[^.!?\n]{0,30}?\b(?:tippen|klicken|wischen|scrollen)\b`,
  String.raw`\b(?:scrollen|wischen) sie (?:nach|seitlich|weiter|horizontal|waagerecht)\b`,
  String.raw`\b(?:nach (?:unten|oben|rechts|links)|seitlich|waagerecht|horizontal) (?:scrollen|wischen)\b`,
  String.raw`\bfahren sie mit der maus\b`,
  String.raw`\b(?:tippen|klicken) sie auf (?:das|die|den|ein|eine) (?:bild|diagramm|grafik|abbildung|tabelle|karte|foto)\b`,
].join("|"), "iu");

// The sentences of the page text that match, each once.
export function uiInstructions(blocks) {
  const hits = blocks.flatMap((b) => b.split(/(?<=[.!?])\s+/)).filter((t) => UI_INSTRUCTION.test(t));
  return [...new Set(hits)];
}

// Runs in the page: the visible text blocks a reader sees, innermost only so nothing counts twice.
function pageText(max) {
  const sel = "h1, h2, h3, p, li, dd, figcaption, caption";
  return [...document.querySelectorAll(sel)]
    .filter((el) => el.getClientRects().length > 0 && getComputedStyle(el).visibility !== "hidden" && !el.querySelector(sel))
    .map((el) => el.textContent.trim().replace(/\s+/g, " ").slice(0, 300)).filter(Boolean).slice(0, max);
}

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
// Limit: structure is compared by tag sequence, four levels deep; cards of different build are skipped.
export function alignmentAudit() {
  const TOL = 4;
  const name = (el) => el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/).join(".") : "");
  const kids = (el) => [...el.children].filter((c) => c.getClientRects().length > 0 && getComputedStyle(c).position !== "absolute" && getComputedStyle(c).position !== "fixed");
  const block = (el) => !getComputedStyle(el).display.startsWith("inline");
  const spread = (xs) => Math.round(Math.max(...xs) - Math.min(...xs));
  const out = [];
  const divider = (el) => el.tagName === "HR" || parseFloat(getComputedStyle(el).borderTopWidth) > 0;
  const compare = (cards, depth, label) => {
    const lists = cards.map((c) => kids(c).filter(block));
    if (lists.some((l) => l.map((e) => e.tagName).join() !== lists[0].map((e) => e.tagName).join())) return;
    // A wrapper with one child (li > a) is not a part: the parts are one level down.
    if (lists[0].length === 1 && depth < 4) return compare(lists.map((l) => l[0]), depth + 1, label);
    if (lists[0].length < 2) return;
    for (let i = 0; i < lists[0].length; i++) {
      const col = lists.map((l) => l[i].getBoundingClientRect());
      const top = spread(col.map((r) => r.top));
      // A divider is judged by its own top; equal bottoms (mt-auto) do not excuse it.
      const grows = !lists.some((l) => divider(l[i])) && spread(col.map((r) => r.bottom)) <= TOL;
      if (top > TOL && !grows) {
        const text = lists[0][i].textContent.trim().replace(/\s+/g, " ").slice(0, 40);
        out.push({ element: `${label} > ${name(lists[0][i])} (child ${i + 1})`, text, observed: `${top} px spread across ${cards.length} cards`, required: `within ${TOL} px` });
        return; // everything below drifts with it
      }
      if (depth < 4) compare(lists.map((l) => l[i]), depth + 1, label);
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
      if (row.length >= 3 && spread(w) <= 0.1 * Math.max(...w)) compare(row, 0, name(row[0]));
    }
  }
  return out;
}

// Runs in the page. Type and layout craft, measured from the DOM (a spike on 8 app pages and 3
// clean references kept only rules whose findings were mostly real and that flagged no clean
// page). The probes are the text leaves: visible elements with a text node of their own.
//   type.small-text           rendered text under 12 px (aria-hidden and hidden text excluded)
//   type.scale-near-duplicate adjacent font sizes under 10 percent apart, each used by 2+ texts
//   layout.edge-near-miss     text left edges 1 to 6 px apart inside one landmark, each shared by 2+ texts
//   type.families             more than 3 font families rendered (first face of each computed stack)
// Left alone because the spike showed no signal: line length, line height, a spacing grid, the count
// of edges or weights, and the Jev questions on hierarchy, focal point and grouping (see
// references/browser-verification.md).
export function craftAudit() {
  const SMALL_PX = 12, NEAR_RATIO = 1.1, EDGE_NEAR = [1, 6], MAX_FAMILIES = 3; // inside: page.evaluate sends only this function
  const name = (el) => el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/)[0] : "");
  const px = (n) => `${+n.toFixed(1)} px`;
  const leaves = [];
  const walk = (el) => {
    const cs = getComputedStyle(el);
    const box = el.getBoundingClientRect();
    if (["SCRIPT", "STYLE", "NOSCRIPT", "TEMPLATE", "IFRAME", "svg", "SVG"].includes(el.tagName) || cs.display === "none" || cs.visibility === "hidden" || +cs.opacity < 0.05 || el.getAttribute("aria-hidden") === "true") return;
    const own = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim());
    if (own.length && box.width > 2 && box.height > 2) {
      const range = document.createRange();
      let first = null;
      for (const n of own) { range.selectNodeContents(n); first ||= [...range.getClientRects()].find((r) => r.width > 0); }
      leaves.push({ el, text: own.map((n) => n.textContent).join(" ").trim().replace(/\s+/g, " "), size: parseFloat(cs.fontSize), family: cs.fontFamily.split(",")[0].replace(/["']/g, "").trim(), first, inline: cs.display === "inline", align: cs.textAlign });
    }
    for (const c of el.children) walk(c);
  };
  walk(document.body);
  const out = [];
  const found = (rule, el, text, observed, required) => out.push({ rule, element: name(el), text: text.slice(0, 40), observed, required });

  for (const l of leaves) if (l.size < SMALL_PX && l.text.length > 1) found("type.small-text", l.el, l.text, px(l.size), `>= ${SMALL_PX} px`);

  const bySize = new Map();
  for (const l of leaves) { const s = Math.round(l.size * 2) / 2; bySize.set(s, [...(bySize.get(s) || []), l]); }
  const sizes = [...bySize.keys()].sort((a, b) => a - b);
  for (let i = 1; i < sizes.length; i++) {
    const [lo, hi] = [bySize.get(sizes[i - 1]), bySize.get(sizes[i])];
    const ratio = sizes[i] / sizes[i - 1];
    if (ratio < NEAR_RATIO && lo.length >= 2 && hi.length >= 2) found("type.scale-near-duplicate", lo[0].el, `${lo[0].text.slice(0, 18)} / ${hi[0].text.slice(0, 18)}`, `${sizes[i - 1]} px (${lo.length} texts) and ${sizes[i]} px (${hi.length} texts), ratio ${ratio.toFixed(2)}`, `a ratio of at least ${NEAR_RATIO.toFixed(2)} between sizes in use, or one size`);
  }

  const families = [...new Set(leaves.map((l) => l.family))];
  if (families.length > MAX_FAMILIES) found("type.families", document.body, families.join(", ").slice(0, 40), `${families.length} font families: ${families.join(", ")}`, `at most ${MAX_FAMILIES}`);

  // A landmark is the nearest main, nav, aside, header, footer or section that has a heading.
  const LANDMARK = "main, nav, aside, header, footer, [role=main], [role=complementary], section:has(h1, h2, h3, h4, h5, h6)";
  const regions = new Map();
  for (const l of leaves) {
    if (!l.first || l.inline || ["center", "right", "end"].includes(l.align) || l.el.closest("button, [role=button], [role=tab], th, td, label, input, select")) continue;
    const region = l.el.closest(LANDMARK) || document.body;
    regions.set(region, [...(regions.get(region) || []), { x: Math.round(l.first.left * 2) / 2, l }]);
  }
  for (const edges of regions.values()) {
    const clusters = [];
    for (const e of edges.sort((a, b) => a.x - b.x)) {
      const c = clusters[clusters.length - 1];
      if (c && e.x - c.x < 0.75) c.items.push(e); else clusters.push({ x: e.x, items: [e] });
    }
    const shared = clusters.filter((c) => c.items.length >= 2);
    for (let i = 1; i < shared.length; i++) {
      const gap = shared[i].x - shared[i - 1].x;
      if (gap >= EDGE_NEAR[0] && gap <= EDGE_NEAR[1]) found("layout.edge-near-miss", shared[i].items[0].l.el, shared[i].items[0].l.text, `left edges ${shared[i - 1].x} and ${shared[i].x} px, ${gap} px apart (${shared[i - 1].items.length} and ${shared[i].items.length} texts)`, `one shared edge, or a step of more than ${EDGE_NEAR[1]} px`);
    }
  }
  return out;
}

// Runs in the page, in the width sweep because it depends on how text wraps: the last line of a
// heading (h1 to h6, role=heading) or of bold text (weight 600 or more) of 16 px or more holds one
// word. Measured with Range rects of every word; a heading of fewer than 3 words is skipped.
export function widowAudit() {
  const name = (el) => el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/)[0] : "");
  const strong = (el) => { const cs = getComputedStyle(el); return parseFloat(cs.fontSize) >= 16 && +cs.fontWeight >= 600; };
  const isHead = (el) => /^H[1-6]$/.test(el.tagName) || el.getAttribute("role") === "heading";
  // Labels wrap by the width of their cell or column, not by a layout decision: cells, term and
  // caption text, form labels, buttons and links are not judged unless they are headings themselves.
  const LABEL = "td, th, dt, dd, caption, figcaption, label, button, a";
  const ctx = document.createElement("canvas").getContext("2d");
  const narrow = (el) => { // bold text under 30ch of its own font wraps by its box, not by a decision; a heading is judged at any width
    const cs = getComputedStyle(el);
    ctx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    return el.getBoundingClientRect().width < 30 * ctx.measureText("0").width;
  };
  // A parenthetical or a capitalized abbreviation of up to 3 letters ("a)", "(1)", "Inc.") ends a heading without being its last word.
  const skippable = (w) => /[()]/.test(w) && w.length <= 4 || /^[A-Z][a-z]{0,2}\.$/.test(w);
  const candidates = [...document.body.querySelectorAll("*")].filter((el) => el.getClientRects().length > 0 && getComputedStyle(el).visibility !== "hidden" && !el.closest("svg, [aria-hidden=true]")
    && (isHead(el) || !el.closest(LABEL))
    && (isHead(el) || !narrow(el))
    && (isHead(el) || ([...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()) && strong(el))));
  const out = [];
  for (const el of candidates) {
    if (candidates.some((o) => o !== el && o.contains(el))) continue; // judged as part of the outer heading or bold block
    const range = document.createRange();
    const words = [];
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      for (const m of n.textContent.matchAll(/\S+/g)) {
        range.setStart(n, m.index); range.setEnd(n, m.index + m[0].length);
        const r = [...range.getClientRects()].find((x) => x.width > 0);
        if (r) words.push({ word: m[0], top: r.top });
      }
    }
    if (words.length < 3) continue;
    let end = words.length - 1;
    if (skippable(words[end].word)) end--;
    const last = words[end];
    const sameLine = words.filter((w) => Math.abs(w.top - last.top) < 3);
    if (sameLine.length === 1) out.push({ rule: "type.widow", element: name(el), text: el.innerText.trim().replace(/\s+/g, " ").slice(0, 40), observed: `last line is the single word "${last.word}"`, required: "two or more words on the last line" });
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

// Runs in the page (page.evaluate(measuredAudit, phase)). Rules measured on real pages, with their
// thresholds, by colour and box arithmetic; every phase returns exact findings with an element.
//   "slop"  dom tier, once: tell.glow, tell.gray-on-color (blocking); tell.icon-tile, tell.nested-cards
//           (advisory: true, their thresholds rest on synthetic fixtures with narrow margins).
//   "rest"  audit tier, per viewport and scheme, before any scrolling: render.hidden-at-rest, render.broken-image.
//   "late"  audit tier, run last because it scrolls (and restores): render.text-occluded.
export function measuredAudit(phase) {
  const T = { glowBlur: 24, glowAlpha: 0.2, glowChroma: 0.25, glowStrength: 12, glowMin: 48, bigBox: 200, tileMin: 32, tileMax: 128, tileGap: 40, tileChroma: 0.05,
    cardMinW: 120, cardMinH: 56, cardRadius: 6, nestedOuterPad: 20, grayChromaMax: 0.08, grayLMin: 0.3, grayLMax: 0.75, bgSatMin: 0.4, grayBgLMax: 0.8, occCover: 0.4, cap: 10 };
  const found = [];
  const cs = (el, p) => getComputedStyle(el, p);
  const name = (el) => el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/)[0].slice(0, 24) : "");
  const textOf = (el) => (el.innerText || el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 40);
  const add = (rule, el, extra) => { if (found.filter((f) => f.rule === rule).length < T.cap) found.push({ rule, element: name(el), ...extra }); };
  const canvas = document.createElement("canvas"); canvas.width = canvas.height = 1;
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  const memo = new Map();
  const parse = (s) => { // canvas takes rgb, oklch, color() and hex alike
    if (!memo.has(s)) {
      let v = null;
      try { ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = "#000"; ctx.fillStyle = s; ctx.fillRect(0, 0, 1, 1); const d = ctx.getImageData(0, 0, 1, 1).data; v = { r: d[0], g: d[1], b: d[2], a: d[3] / 255 }; } catch { /* unparsable colour: unknown */ }
      memo.set(s, v);
    }
    return memo.get(s);
  };
  const COLOR = /(rgba?\([^)]*\)|oklab\([^)]*\)|oklch\([^)]*\)|color\([^)]*\)|hsla?\([^)]*\)|#[0-9a-fA-F]{3,8})/g;
  const chroma = (c) => (Math.max(c.r, c.g, c.b) - Math.min(c.r, c.g, c.b)) / 255;
  const hsl = (c) => { const [r, g, b] = [c.r / 255, c.g / 255, c.b / 255], mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn, l = (mx + mn) / 2; return { l, s: d === 0 ? 0 : d / (1 - Math.abs(2 * l - 1)) }; };
  const ownBg = (el) => { // a solid colour, the mean of gradient stops, or {unknown} for an image
    const s = cs(el), bi = s.backgroundImage;
    if (bi && bi !== "none") {
      if (/url\(/.test(bi) && !/gradient/.test(bi)) return { unknown: true };
      const cols = (bi.match(COLOR) || []).map(parse).filter((c) => c && c.a > 0.05);
      if (cols.length) { const n = cols.length, m = (k) => cols.reduce((a, c) => a + c[k], 0) / n; return { r: m("r"), g: m("g"), b: m("b"), a: 1 }; }
    }
    const c = parse(s.backgroundColor);
    return c && c.a > 0.02 ? c : null;
  };
  const effBg = (el) => { // layers blended up to the first opaque one; null when an image sits behind
    const layers = [];
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const b = ownBg(e); if (b?.unknown) return null; if (b) { layers.push(b); if (b.a >= 0.99) break; } }
    let acc = { r: 255, g: 255, b: 255 };
    for (const b of layers.reverse()) acc = { r: acc.r * (1 - b.a) + b.r * b.a, g: acc.g * (1 - b.a) + b.g * b.a, b: acc.b * (1 - b.a) + b.b * b.a };
    return acc;
  };
  const all = [...document.body.querySelectorAll("*")].filter((e) => !/^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE|PATH|DEFS|LINEARGRADIENT|STOP|BR)$/i.test(e.tagName));
  const leaves = [];
  for (const el of all) {
    if (el.closest("svg") && !(el instanceof SVGTextElement) && el.tagName.toLowerCase() !== "svg") continue;
    const own = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim());
    if (own.length) leaves.push({ el, text: own.map((n) => n.textContent).join(" ").trim().replace(/\s+/g, " "), node: own[0] });
  }
  const isHeading = (el) => /^H[1-6]$/.test(el.tagName) || (parseFloat(cs(el).fontSize) >= 18 && +cs(el).fontWeight >= 600 && el.textContent.trim().length < 120);
  const pinned = (el, position) => { for (let p = el; p && p.nodeType === 1; p = p.parentElement) if (cs(p).position === position) return true; return false; };

  if (phase === "slop") {
    const splitTop = (s) => { const parts = []; let depth = 0, cur = ""; for (const ch of s) { if (ch === "(") depth++; if (ch === ")") depth--; if (ch === "," && depth === 0) { parts.push(cur.trim()); cur = ""; } else cur += ch; } if (cur.trim()) parts.push(cur.trim()); return parts; };
    for (const el of all) { // tell.glow: a coloured large soft box-shadow, a radial-gradient halo or a big blur() blob
      const s = cs(el), r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2 || s.display === "none") continue;
      for (const sh of s.boxShadow && s.boxShadow !== "none" ? splitTop(s.boxShadow) : []) {
        if (/inset/.test(sh)) continue;
        const col = parse((sh.match(COLOR) || [])[0] || ""); if (!col) continue;
        const [ox = 0, oy = 0, blur = 0, spread = 0] = (sh.replace(COLOR, "").match(/-?[\d.]+px/g) || []).map(parseFloat);
        if (blur >= T.glowBlur && col.a >= T.glowAlpha && chroma(col) >= T.glowChroma && (blur + 2 * spread) * col.a >= T.glowStrength && Math.max(r.width, r.height) >= T.glowMin && Math.hypot(ox, oy) <= blur * 0.75)
          add("tell.glow", el, { detail: `coloured soft shadow, blur ${blur} px, alpha ${+col.a.toFixed(2)}: a glow; use a neutral elevation or a border` });
      }
      const bg = s.filter && /blur\(/.test(s.filter) ? ownBg(el) : null;
      if (bg && !bg.unknown && parseFloat((s.filter.match(/blur\(([\d.]+)px/) || [])[1]) >= 40 && chroma(bg) >= T.glowChroma && r.width >= T.bigBox) add("tell.glow", el, { detail: "blurred coloured blob behind the content: a glow" });
      for (const pseudo of [null, "::before", "::after"]) {
        const p = pseudo ? cs(el, pseudo) : s;
        if (pseudo && (p.content === "none" || p.content === "normal")) continue;
        if (!/radial-gradient/.test(p.backgroundImage || "")) continue;
        const cols = (p.backgroundImage.match(COLOR) || []).map(parse).filter(Boolean);
        const solid = cols.some((c) => c.a >= T.glowAlpha && chroma(c) >= T.glowChroma), fades = cols.some((c) => c.a < 0.6) || /transparent/.test(p.backgroundImage);
        const w = (pseudo && parseFloat(p.width)) || r.width, h = (pseudo && parseFloat(p.height)) || r.height;
        if (solid && fades && w >= T.bigBox && h >= T.bigBox * 0.6 && (pseudo || p.position === "absolute" || p.position === "fixed" || !el.textContent.trim()))
          add("tell.glow", el, { detail: `radial gradient halo ${Math.round(w)} x ${Math.round(h)} px: a glow` });
      }
    }
    for (const { el, text } of leaves) { // tell.gray-on-color: mid-gray text on a saturated background; a pale tint or near-black is exempt
      const fg = parse(cs(el).color);
      if (text.length < 2 || !fg || fg.a < 0.5 || !el.checkVisibility()) continue;
      const bg = effBg(el); if (!bg) continue;
      const L = hsl(fg).l, b = hsl(bg);
      if (chroma(fg) <= T.grayChromaMax && L >= T.grayLMin && L <= T.grayLMax && b.s >= T.bgSatMin && b.l > 0.08 && b.l < T.grayBgLMax)
        add("tell.gray-on-color", el, { detail: `gray text ${cs(el).color} on a saturated background: tint the text from the background hue or use white or black` });
    }
    const tiles = []; // tell.icon-tile (advisory): the same tinted near-square icon tile above a heading, 2 or more times
    for (const el of all) {
      const r = el.getBoundingClientRect(), s = cs(el), bg = ownBg(el);
      if (r.width < T.tileMin || r.width > T.tileMax || r.height < T.tileMin || r.height > T.tileMax || r.width / r.height < 0.8 || r.width / r.height > 1.25 || s.display === "inline") continue;
      if (!bg || bg.unknown || chroma(bg) < T.tileChroma || (parseFloat(s.borderTopLeftRadius) < 4 && !/%/.test(s.borderTopLeftRadius))) continue;
      const pbg = el.parentElement && effBg(el.parentElement);
      if (pbg && Math.hypot(bg.r - pbg.r, bg.g - pbg.g, bg.b - pbg.b) < 8) continue;
      const t = el.textContent.trim();
      if (!(el.querySelector("svg, img, i, [class*=icon]") || /^[\p{Extended_Pictographic}\s]{1,4}$/u.test(t)) || (t.length > 4 && !/^[\p{Extended_Pictographic}\s]+$/u.test(t))) continue;
      let node = el, heading = null;
      for (let up = 0; up < 3 && node && !heading; up++, node = node.parentElement) {
        const n = node.nextElementSibling; if (!n) continue;
        heading = isHeading(n) ? n : n.firstElementChild && isHeading(n.firstElementChild) ? n.firstElementChild : null;
        if (up === 0 && !heading) break;
      }
      if (!heading) continue;
      const h = heading.getBoundingClientRect(), gap = h.top - r.bottom;
      if (gap >= -2 && gap <= T.tileGap && (Math.abs(h.left - r.left) <= 12 || Math.abs(h.left + h.width / 2 - (r.left + r.width / 2)) <= 12))
        tiles.push({ el, key: `${Math.round(r.width)}x${Math.round(r.height)}|${Math.round(bg.r)},${Math.round(bg.g)},${Math.round(bg.b)}` });
    }
    const byKey = Object.groupBy(tiles, (t) => t.key);
    for (const g of Object.values(byKey)) if (g.length >= 2) add("tell.icon-tile", g[0].el, { advisory: true, detail: `${g.length} identical tinted icon tiles above headings: use the real icon without a tile, or vary the layout` });
    const isCard = (el) => { // tell.nested-cards (advisory): a bordered or shadowed opaque card inside another, the outer padded 20 px or more
      if (/^(PRE|BUTTON|INPUT|SELECT|TEXTAREA|A|TD|TH|TR|TABLE|LI|SUMMARY|IMG|SVG)$/i.test(el.tagName)) return false;
      const s = cs(el), r = el.getBoundingClientRect(), bg = ownBg(el);
      if (s.display === "inline" || r.width < T.cardMinW || r.height < T.cardMinH || (parseFloat(s.borderTopLeftRadius) < T.cardRadius && !/%/.test(s.borderTopLeftRadius)) || !bg || bg.unknown || bg.a < 0.9) return false;
      const bordered = ["Top", "Right", "Bottom", "Left"].every((d) => parseFloat(s["border" + d + "Width"]) >= 1 && (parse(s["border" + d + "Color"]) || { a: 0 }).a > 0.05 && s["border" + d + "Style"] !== "none");
      return bordered || (s.boxShadow && s.boxShadow !== "none");
    };
    const cards = new Set(all.filter(isCard));
    for (const el of cards) {
      let p = el.parentElement; while (p && !cards.has(p)) p = p.parentElement;
      if (p && p !== document.body && parseFloat(cs(p).paddingLeft) >= T.nestedOuterPad) add("tell.nested-cards", el, { advisory: true, detail: `card inside card (${name(p)}): drop the inner border and shadow, or split the content` });
    }
  }

  if (phase === "rest") {
    const scrolls = (el) => { for (let p = el.parentElement; p && p !== document.documentElement; p = p.parentElement) if (/(auto|scroll)/.test(cs(p).overflowX) && p.scrollWidth > p.clientWidth + 2) return true; return false; };
    const pageWidth = Math.max(document.documentElement.scrollWidth, innerWidth);
    for (const { el, text } of leaves) { // render.hidden-at-rest: text that is in the layout but never shown (a reveal that did not fire, off-screen, visibility)
      const s = cs(el), r = el.getBoundingClientRect();
      if (text.length < 3 || s.display === "none" || r.width <= 1 || r.height <= 1) continue;
      if (el.closest("[hidden], details:not([open]) :not(summary), [role=tooltip], [aria-hidden=true], dialog:not([open]), template")) continue; // collapsed, tooltips, skip links
      if (!el.checkVisibility({ checkOpacity: false, checkVisibilityCSS: false, contentVisibilityAuto: true })) continue;
      let opacity = 1; for (let p = el; p && p.nodeType === 1; p = p.parentElement) opacity *= +cs(p).opacity;
      const why = opacity < 0.02 ? `opacity ${opacity.toFixed(2)}` : s.visibility === "hidden" ? "visibility: hidden" : (r.right <= 0 || r.left >= pageWidth) && !scrolls(el) && !pinned(el, "fixed") && !el.closest("a[href^='#']") ? `off-screen at x ${Math.round(r.left)} px` : null;
      if (why) add("render.hidden-at-rest", el, { text, observed: why, required: "visible text at rest, or hidden on purpose (hidden, aria-hidden, a scroll container, a collapsed section)" });
    }
    for (const img of document.images) { // render.broken-image: loaded, nothing decoded
      if (img.complete && img.naturalWidth === 0 && (img.currentSrc || img.getAttribute("src") !== null || img.getAttribute("srcset"))) add("render.broken-image", img, { text: (img.getAttribute("alt") || "").slice(0, 40), observed: "naturalWidth 0: " + (img.currentSrc || img.getAttribute("src") || "").slice(-60), required: "an image that decodes" });
    }
  }

  if (phase === "late") { // render.text-occluded: an opaque box on top of the text, found by elementFromPoint with the text scrolled to mid screen
    const [sx, sy] = [scrollX, scrollY];
    for (const { el, text, node } of leaves) {
      if (text.length < 3 || cs(el).visibility === "hidden" || +cs(el).opacity < 0.5 || !el.checkVisibility()) continue;
      const range = document.createRange(); range.selectNodeContents(node);
      const first = [...range.getClientRects()].find((x) => x.width > 4 && x.height > 4); if (!first) continue;
      scrollTo(sx, Math.max(0, first.top + sy - innerHeight / 2));
      const rect = range.getClientRects()[0]; if (!rect) continue;
      const points = [0.5, 0.1, 0.3, 0.7, 0.9].map((f) => [rect.left + rect.width * f, rect.top + rect.height / 2]).filter(([x, y]) => x >= 0 && y >= 0 && x < innerWidth && y < innerHeight);
      let covered = 0, by = null;
      for (const [x, y] of points) {
        const top = document.elementFromPoint(x, y);
        if (!top || top === el || el.contains(top) || top.contains(el) || pinned(top, "fixed") || pinned(top, "sticky") || (top.textContent || "").includes(text)) continue; // pinned chrome is not caught; a wrapper or a duplicate is not a cover
        const tb = ownBg(top), solid = /^(IMG|VIDEO|CANVAS)$/i.test(top.tagName) || (tb && !tb.unknown && tb.a >= 0.95 && +cs(top).opacity >= 0.95);
        if (solid) { covered++; by = top; }
      }
      if (points.length && covered && covered / points.length >= T.occCover - 1e-9) add("render.text-occluded", el, { text, observed: `covered by ${name(by)} at ${covered} of ${points.length} points`, required: "text that no box covers" });
    }
    scrollTo(sx, sy);
  }
  return found;
}

// The exact checks behind ten design-core vocabulary terms. Each in-page function sends only itself
// to page.evaluate, so its constants and helpers live inside it. Findings: { rule, element, text, observed, required }.
//   vocabAudit  per viewport and scheme: type.heading-ladder, layout.proximity, type.tabular-figures,
//               wcag.non-text-contrast, wcag.text-spacing (injects the WCAG 1.4.12 override and removes it again).
//   reflowAudit at 320 px wide: wcag.reflow.  motionAudit with reduced motion emulated: motion.reduced.
//   shiftAudit  after a load, waits 1 s: perf.layout-shift.  focusAudit(page) tabs through the page:
//               wcag.focus-visible and wcag.focus-not-obscured.
export function vocabAudit() {
  const T = { ladderSize: 1.05, ladderWeight: 200, proxRatio: 0.75, tabular: 0.5, nonText: 3, cap: 12 };
  const visible = (el) => { if (!el.isConnected) return false; const r = el.getBoundingClientRect(); if (r.width < 1 || r.height < 1) return false; const s = getComputedStyle(el); return s.visibility !== "hidden" && s.display !== "none" && !el.closest("[hidden],[aria-hidden=true]") && (el.checkVisibility ? el.checkVisibility() : true); };
  const name = (el) => el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/)[0].slice(0, 24) : "");
  const textOf = (el) => (el.innerText || el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 40);
  const out = [];
  const add = (rule, el, text, observed, required) => { if (out.filter((f) => f.rule === rule).length < T.cap) out.push({ rule, element: typeof el === "string" ? el : name(el), text, observed, required }); };
  const canvas = document.createElement("canvas"); canvas.width = canvas.height = 1;
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  const parse = (s) => { try { ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = "#000"; ctx.fillStyle = s; ctx.fillRect(0, 0, 1, 1); const d = ctx.getImageData(0, 0, 1, 1).data; return { r: d[0], g: d[1], b: d[2], a: d[3] / 255 }; } catch { return null; } };
  const COLOR = /(rgba?\([^)]*\)|oklab\([^)]*\)|oklch\([^)]*\)|color\([^)]*\)|hsla?\([^)]*\)|#[0-9a-fA-F]{3,8})/g;
  const ownBg = (el) => { const s = getComputedStyle(el), bi = s.backgroundImage; if (bi && bi !== "none") { if (/url\(/.test(bi) && !/gradient/.test(bi)) return { unknown: true }; const cols = (bi.match(COLOR) || []).map(parse).filter((c) => c && c.a > 0.05); if (cols.length) { const n = cols.length, m = (k) => cols.reduce((a, c) => a + c[k], 0) / n; return { r: m("r"), g: m("g"), b: m("b"), a: 1 }; } } const c = parse(s.backgroundColor); return c && c.a > 0.02 ? c : null; };
  const effBg = (el) => { const layers = []; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const b = ownBg(e); if (b?.unknown) return null; if (b) { layers.push(b); if (b.a >= 0.99) break; } } let acc = { r: 255, g: 255, b: 255 }; for (const b of layers.reverse()) acc = { r: acc.r * (1 - b.a) + b.r * b.a, g: acc.g * (1 - b.a) + b.g * b.a, b: acc.b * (1 - b.a) + b.b * b.a }; return acc; };
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const over = (fg, bg) => ({ r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a) });

  // type.heading-ladder: a lower level rendered larger, or as heavy at the same size, than a higher one.
  const hs = [...document.querySelectorAll("h1,h2,h3,h4,h5,h6,[role=heading]")].filter(visible);
  const lvl = (h) => (h.getAttribute("role") === "heading" ? +h.getAttribute("aria-level") || 2 : +h.tagName[1]);
  const by = {};
  for (const h of hs) { const s = getComputedStyle(h); (by[lvl(h)] ??= []).push({ h, size: parseFloat(s.fontSize), weight: +s.fontWeight || 400 }); }
  const med = (a) => [...a].sort((x, y) => x - y)[a.length >> 1];
  const stat = Object.fromEntries(Object.entries(by).map(([l, a]) => [l, { size: med(a.map((x) => x.size)), weight: med(a.map((x) => x.weight)), a }]));
  const levels = Object.keys(stat).map(Number).sort((a, b) => a - b);
  for (const b of levels) for (const a of levels) {
    if (a >= b) continue;
    const A = stat[a], B = stat[b];
    const bigger = B.size > A.size * T.ladderSize;
    const heavier = B.size >= A.size / T.ladderSize && B.weight >= A.weight + T.ladderWeight;
    if (!bigger && !heavier) continue;
    const h = B.a.find((x) => (bigger ? x.size > A.size * T.ladderSize : x.weight >= A.weight + T.ladderWeight)).h;
    add("type.heading-ladder", h, textOf(h), `h${b} ${B.size} px, weight ${B.weight}; h${a} ${A.size} px, weight ${A.weight}`, `h${b} no larger or heavier than h${a}`);
    break;
  }

  // layout.proximity: a heading nearer the block above it than the content below it.
  const ink = (el, side) => { // visual bottom (1) or top (0) of an element's content
    const s = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const painted = s.backgroundColor !== "rgba(0, 0, 0, 0)" || s.backgroundImage !== "none" || s.boxShadow !== "none" || ["Top", "Right", "Bottom", "Left"].some((d) => parseFloat(s["border" + d + "Width"]) > 0 && s["border" + d + "Style"] !== "none");
    if (painted || /^(IMG|SVG|CANVAS|VIDEO|TABLE|HR|INPUT|BUTTON|SELECT|TEXTAREA|IFRAME)$/i.test(el.tagName)) return side ? r.bottom : r.top;
    let v = null;
    const take = (y) => { v = v === null ? y : side ? Math.max(v, y) : Math.min(v, y); };
    for (const n of el.childNodes) {
      if (n.nodeType === 3 && n.textContent.trim()) { const g = document.createRange(); g.selectNodeContents(n); const q = g.getBoundingClientRect(); if (q.height) take(side ? q.bottom : q.top); }
      else if (n.nodeType === 1 && visible(n)) take(ink(n, side));
    }
    return v === null ? (side ? r.bottom : r.top) : v;
  };
  for (const h of [...document.querySelectorAll("h2,h3,h4,h5,h6,[role=heading]")].filter(visible)) {
    const prev = h.previousElementSibling, next = h.nextElementSibling;
    if (!prev || !next || !visible(prev) || !visible(next)) continue;
    if (/^(absolute|fixed)$/.test(getComputedStyle(prev).position) || /^(absolute|fixed)$/.test(getComputedStyle(next).position)) continue;
    const r = h.getBoundingClientRect(), pr = prev.getBoundingClientRect(), nr = next.getBoundingClientRect();
    if (pr.bottom > r.top + 1 || nr.top < r.bottom - 1 || pr.right <= r.left || pr.left >= r.right || nr.right <= r.left || nr.left >= r.right) continue; // side by side, not stacked
    const hSize = parseFloat(getComputedStyle(h).fontSize), pSize = parseFloat(getComputedStyle(prev).fontSize);
    if (pr.height <= pSize * 1.7 && pSize < hSize) continue; // a one-line kicker above the heading belongs to it
    const above = r.top - ink(prev, 1), below = ink(next, 0) - r.bottom;
    if (above < below * T.proxRatio) add("layout.proximity", h, textOf(h), `${above.toFixed(0)} px above, ${below.toFixed(0)} px below`, "more space above a heading than below it");
  }

  // type.tabular-figures: a numeric table column whose digits differ in width.
  const NUM = /^[\s+\-\u2212\u2013\u20ac$\u00a3\u00a5(]*\d[\d.,:'\s]*[%\u20ac$\u00a3\u00a5)]?\s*[A-Za-z%]{0,3}\)?$/;
  const digit = (cell, ch) => { const s = getComputedStyle(cell); const sp = document.createElement("span"); sp.textContent = ch; sp.style.cssText = `position:fixed;left:-9999px;top:0;white-space:nowrap;visibility:hidden;font-kerning:none;letter-spacing:${s.letterSpacing};font-family:${s.fontFamily};font-size:${s.fontSize};font-weight:${s.fontWeight};font-style:${s.fontStyle};font-stretch:${s.fontStretch};font-variant-numeric:${s.fontVariantNumeric};font-feature-settings:${s.fontFeatureSettings}`; cell.append(sp); const w = sp.getBoundingClientRect().width; sp.remove(); return w; };
  for (const t of document.querySelectorAll("table")) {
    if (!visible(t)) continue;
    const cols = {};
    for (const row of t.rows) [...row.cells].forEach((c, i) => { if (c.tagName === "TD" && NUM.test(c.textContent.trim()) && visible(c)) (cols[i] ??= []).push(c); });
    for (const cells of Object.values(cols)) {
      if (cells.length < 2) continue;
      const w = ["1", "0", "8"].map((d) => digit(cells[0], d));
      const spread = Math.max(...w) - Math.min(...w);
      if (spread > T.tabular) add("type.tabular-figures", cells[0], cells.slice(0, 3).map((x) => x.textContent.trim()).join(" | "), `digits differ by ${spread.toFixed(2)} px each`, "equal-width digits: font-variant-numeric: tabular-nums");
    }
  }

  // wcag.non-text-contrast: an input whose border, fill and shadow all sit under 3:1 against what is behind it.
  const sel = 'input:not([type=checkbox]):not([type=radio]):not([type=hidden]):not([type=submit]):not([type=button]):not([type=reset]):not([type=range]):not([type=color]):not([type=file]):not([type=image]),textarea,select,[role=textbox],[role=combobox],[role=searchbox]';
  for (const el of document.querySelectorAll(sel)) {
    if (!visible(el) || el.disabled || el.getAttribute("aria-disabled") === "true") continue;
    const r = el.getBoundingClientRect(); if (r.width < 24 || r.height < 16) continue;
    const parentBg = el.parentElement ? effBg(el.parentElement) : { r: 255, g: 255, b: 255 };
    if (!parentBg) continue;
    const s = getComputedStyle(el);
    const fill = ownBg(el);
    if (fill?.unknown) continue;
    let best = fill ? ratio(over(fill, parentBg), parentBg) : 0;
    for (const d of ["Top", "Right", "Bottom", "Left"]) if (parseFloat(s["border" + d + "Width"]) >= 1 && s["border" + d + "Style"] !== "none") { const c = parse(s["border" + d + "Color"]); if (c && c.a > 0.02) best = Math.max(best, ratio(over(c, parentBg), parentBg)); }
    if (s.boxShadow !== "none") { const m = s.boxShadow.match(COLOR); const c = m && parse(m[0]); if (c && c.a > 0.3) best = Math.max(best, ratio(over(c, parentBg), parentBg)); }
    for (let w = el.parentElement, i = 0; w && i < 2 && best < T.nonText; w = w.parentElement, i++) { // a wrapper may draw the boundary
      if (w.getBoundingClientRect().height > r.height * 2.5) break;
      const ws = getComputedStyle(w), pb = w.parentElement && effBg(w.parentElement);
      for (const d of ["Top", "Right", "Bottom", "Left"]) if (pb && parseFloat(ws["border" + d + "Width"]) >= 1 && ws["border" + d + "Style"] !== "none") { const c = parse(ws["border" + d + "Color"]); if (c) best = Math.max(best, ratio(over(c, pb), pb)); }
    }
    if (best < T.nonText) add("wcag.non-text-contrast", el, (el.placeholder || el.getAttribute("aria-label") || "").slice(0, 40), `${best.toFixed(2)}:1`, `>= ${T.nonText}:1`);
  }

  // wcag.text-spacing: text newly clipped or spilling out of its box under the WCAG 1.4.12 override. HTML text only.
  const snap = () => {
    const clipped = new Set(), spill = new Set();
    for (const el of document.body.querySelectorAll("*")) {
      if (!visible(el) || el.closest("svg")) continue;
      const own = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim().length > 1);
      if (!own.length) continue;
      const s = getComputedStyle(el);
      if (/(hidden|clip)/.test(s.overflowY + s.overflowX) && s.textOverflow !== "ellipsis" && (el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1)) clipped.add(el);
      let box = null, cut = false;
      for (let p = el; p && p !== document.body; p = p.parentElement) {
        const q = getComputedStyle(p);
        if (/(hidden|clip|auto|scroll)/.test(q.overflowY)) { cut = true; break; }
        if (q.backgroundColor !== "rgba(0, 0, 0, 0)" || ["Top", "Bottom"].some((d) => parseFloat(q["border" + d + "Width"]) > 0 && q["border" + d + "Style"] !== "none")) { box = p; break; }
      }
      if (!box || cut) continue;
      const b = box.getBoundingClientRect();
      if (own.some((n) => { const g = document.createRange(); g.selectNodeContents(n); return g.getBoundingClientRect().bottom > b.bottom + 1; })) spill.add(el);
    }
    return { clipped, spill, wide: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1 };
  };
  const before = snap();
  const st = document.createElement("style");
  st.textContent = "*{line-height:1.5 !important;letter-spacing:.12em !important;word-spacing:.16em !important} p{margin-bottom:2em !important}";
  document.head.append(st);
  const after = snap();
  st.remove();
  for (const el of after.clipped) if (!before.clipped.has(el)) add("wcag.text-spacing", el, textOf(el), "text clipped by its box", "text survives line height 1.5, letter spacing 0.12em, word spacing 0.16em");
  for (const el of after.spill) if (!before.spill.has(el)) add("wcag.text-spacing", el, textOf(el), "text spills out of its box", "text survives line height 1.5, letter spacing 0.12em, word spacing 0.16em");
  if (after.wide && !before.wide) add("wcag.text-spacing", "document", "", "horizontal scroll appears", "text survives line height 1.5, letter spacing 0.12em, word spacing 0.16em");
  return out;
}

// Runs at 320 px wide (setViewportSize first). Content in a scrolling or clipping box of its own is exempt.
export function reflowAudit() {
  const de = document.documentElement;
  if (de.scrollWidth <= de.clientWidth + 1) return [];
  const w = de.clientWidth;
  const name = (el) => el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/)[0].slice(0, 24) : "");
  let worst = null;
  for (const el of document.body.querySelectorAll("*")) {
    const r = el.getBoundingClientRect();
    if (r.right <= w + 1 || r.width < 2 || getComputedStyle(el).display === "none") continue;
    let clipped = false;
    for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) if (/(auto|scroll|hidden|clip)/.test(getComputedStyle(p).overflowX) && p.getBoundingClientRect().right <= w + 1) { clipped = true; break; }
    if (!clipped && (!worst || r.right > worst.right)) worst = { el, right: r.right };
  }
  return [{ rule: "wcag.reflow", element: worst ? name(worst.el) : "document", text: worst ? (worst.el.innerText || "").trim().replace(/\s+/g, " ").slice(0, 40) : "", observed: `${de.scrollWidth} px wide at 320 px`, required: "no horizontal scroll at 320 px" }];
}

// Runs with prefers-reduced-motion: reduce emulated. A running animation of position, size, rotation or scale
// (opacity and colour are soft enough to stay) means the page ignores the request.
export function motionAudit() {
  const out = [];
  const name = (el) => el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/)[0].slice(0, 24) : "");
  const MOVE = /^(transform|translate|rotate|scale|top|left|right|bottom|margin|inset|backgroundPosition|background-position|offset)/;
  for (const a of document.getAnimations()) {
    if (a.playState !== "running") continue;
    const e = a.effect, tgt = e?.target;
    if (!(tgt instanceof Element) || tgt.getBoundingClientRect().width < 1 || getComputedStyle(tgt).display === "none") continue;
    let props = [];
    try { props = [...new Set(e.getKeyframes().flatMap((k) => Object.keys(k)))].filter((p) => !["offset", "easing", "composite", "computedOffset"].includes(p)); } catch { /* unreadable keyframes */ }
    if (!props.some((p) => MOVE.test(p)) && a.timeline?.constructor?.name !== "ScrollTimeline") continue;
    if (out.length < 12) out.push({ rule: "motion.reduced", element: name(tgt), text: (tgt.innerText || "").trim().replace(/\s+/g, " ").slice(0, 40), observed: `${a.animationName || "animation"} still runs (${props.filter((p) => MOVE.test(p)).join(", ") || "scroll timeline"})`, required: "no transform or scroll animation under prefers-reduced-motion: reduce" });
  }
  if (getComputedStyle(document.documentElement).scrollBehavior === "smooth") out.push({ rule: "motion.reduced", element: "html", text: "", observed: "scroll-behavior: smooth", required: "scroll-behavior: auto under prefers-reduced-motion: reduce" });
  return out;
}

// Cumulative Layout Shift of the page so far (buffered entries) plus one and a half more seconds, as the largest session window.
export function shiftAudit() {
  const MAX = 0.1;
  return new Promise((resolve) => {
    const entries = [];
    const o = new PerformanceObserver((l) => entries.push(...l.getEntries()));
    o.observe({ type: "layout-shift", buffered: true });
    setTimeout(() => {
      o.disconnect();
      let best = 0, cur = 0, first = 0, last = 0;
      for (const e of entries) { if (e.hadRecentInput) continue; if (cur && (e.startTime - last > 1000 || e.startTime - first > 5000)) cur = 0; if (!cur) first = e.startTime; cur += e.value; last = e.startTime; best = Math.max(best, cur); }
      const worst = entries.filter((e) => !e.hadRecentInput).sort((a, b) => b.value - a.value)[0];
      const n = worst?.sources?.[0]?.node;
      const el = n && n.nodeType === 1 ? n : null;
      resolve(best > MAX ? [{ rule: "perf.layout-shift", element: el ? el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/)[0].slice(0, 24) : "") : "page", text: el ? (el.innerText || "").trim().replace(/\s+/g, " ").slice(0, 40) : "", observed: `CLS ${best.toFixed(3)}`, required: `<= ${MAX}` }] : []);
    }, 1500); // a frame may paint late on a busy machine
  });
}

// Tabs through the page (up to 40 stops, keyboard focus) and reports, per stop, a focus that changes nothing a reader
// can see (own style, the parent's and its children's) and a focus fully behind a fixed or sticky layer. Leaves nothing focused.
export async function focusAudit(page, max = 40) {
  const out = { visible: [], obscured: [], stops: 0 };
  await page.evaluate(() => { document.activeElement?.blur?.(); scrollTo(0, 0); });
  const seen = new Set();
  for (let i = 0; i < max; i++) {
    await page.keyboard.press("Tab");
    const stop = await page.evaluate(() => {
      const el = document.activeElement;
      if (!el || el === document.body || el === document.documentElement) return null;
      el.__focusStop ??= Math.random().toString(36).slice(2);
      const name = el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/)[0].slice(0, 24) : "");
      const text = (el.innerText || el.getAttribute("aria-label") || el.value || "").trim().replace(/\s+/g, " ").slice(0, 40);
      const sig = (n) => { const s = getComputedStyle(n); const ow = parseFloat(s.outlineWidth); return [s.outlineStyle === "none" || !ow ? "none" : s.outlineStyle + s.outlineWidth + s.outlineColor + s.outlineOffset, s.boxShadow, s.borderTopColor, s.borderRightColor, s.borderBottomColor, s.borderLeftColor, s.borderTopWidth, s.backgroundColor, s.backgroundImage === "none" ? "" : s.backgroundImage.slice(0, 60), s.color, s.textDecorationLine, s.transform, s.filter, s.opacity].join("|"); };
      const scope = () => { const p = el.parentElement; return [el, p, p?.parentElement, ...(p ? [...p.querySelectorAll("*")].slice(0, 40) : [])].filter(Boolean).map(sig).join("#"); };
      const focused = scope();
      const box = el.getBoundingClientRect();
      const vis = { left: Math.max(box.left, 0), top: Math.max(box.top, 0), right: Math.min(box.right, innerWidth - 1), bottom: Math.min(box.bottom, innerHeight - 1) }; // the part of the box on screen
      const points = vis.right > vis.left && vis.bottom > vis.top ? [[.5, .5], [.15, .15], [.85, .15], [.15, .85], [.85, .85]].map(([fx, fy]) => [vis.left + (vis.right - vis.left) * fx, vis.top + (vis.bottom - vis.top) * fy]) : [];
      let covered = 0, layer = "";
      for (const [x, y] of points) {
        const hit = document.elementFromPoint(x, y);
        if (!hit || hit === el || el.contains(hit) || hit.contains(el)) continue;
        for (let l = hit; l && l !== document.documentElement; l = l.parentElement) {
          const pos = getComputedStyle(l).position;
          if ((pos === "fixed" || pos === "sticky") && !l.contains(el)) { covered++; layer = l.tagName.toLowerCase() + (typeof l.className === "string" && l.className.trim() ? "." + l.className.trim().split(/\s+/)[0] : ""); break; }
        }
      }
      el.blur();
      const unchanged = focused === scope();
      el.focus({ focusVisible: true });
      return { id: el.__focusStop, name, text, unchanged, covered, total: points.length, layer, tiny: box.width < 2 || box.height < 2 };
    });
    if (!stop || seen.has(stop.id)) break;
    seen.add(stop.id);
    out.stops++;
    if (stop.tiny) continue;
    if (stop.unchanged) out.visible.push({ rule: "wcag.focus-visible", element: stop.name, text: stop.text, observed: "no outline, shadow, border or color change on keyboard focus", required: "a visible focus indicator" });
    if (stop.total && stop.covered === stop.total) out.obscured.push({ rule: "wcag.focus-not-obscured", element: stop.name, text: stop.text, observed: `fully behind ${stop.layer}`, required: "focused element not hidden by a fixed or sticky layer" });
  }
  await page.evaluate(() => { document.activeElement?.blur?.(); scrollTo(0, 0); });
  return out;
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

// Runs in the page on one diagram element (locator.evaluate). The rendered size of every inline
// SVG text, exactly: its font size in user units times the scale from user units to CSS px (the
// SVG's viewBox against its box, transforms included). A diagram without such text (canvas, an
// image) has `texts: 0` and is left to Jev. The house floor is 12 px, checked at 390 px too.
export function diagramTextSize(root) {
  const svgs = root.tagName.toLowerCase() === "svg" ? [root] : [...root.querySelectorAll("svg")];
  const sizes = [];
  for (const svg of svgs) {
    for (const el of svg.querySelectorAll("text, foreignObject *")) {
      if (!el.parentElement.closest("text") && [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) {
        const cs = getComputedStyle(el);
        if (cs.display === "none" || cs.visibility === "hidden") continue;
        const m = (el.closest("foreignObject") || el).getScreenCTM();
        if (!m) continue;
        const scale = Math.sqrt(Math.abs(m.a * m.d - m.b * m.c));
        sizes.push({ text: el.textContent.trim().replace(/\s+/g, " ").slice(0, 40), px: +(parseFloat(cs.fontSize) * scale).toFixed(1) });
      }
    }
  }
  return { texts: sizes.length, min: sizes.length ? Math.min(...sizes.map((x) => x.px)) : null, smallest: sizes.sort((a, b) => a.px - b.px)[0] };
}
const SMALL_DIAGRAM_PX = 12, SMALL_DIAGRAM_TOLERANCE = 0.5; // a text that rounds to 12 px reads as 12: 11.9 px measured on real SVG scaling is not a defect

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

// Runs in the page: a page shorter than the viewport still shoots 800 px tall, and a blank
// strip would read as "sparse". The shot ends 24 px below the last row that differs from the
// bottom row (but keeps `min` px, which Jev needs). A page that ends in a footer, a dev badge or a
// gradient is not trimmed: that is the safe direction.
async function trimShot([base64, min]) {
  const img = new Image();
  img.src = "data:image/png;base64," + base64;
  await img.decode();
  const c = document.createElement("canvas");
  c.width = img.width; c.height = img.height;
  const ctx = c.getContext("2d");
  ctx.drawImage(img, 0, 0);
  const { data } = ctx.getImageData(0, 0, c.width, c.height);
  const stride = c.width * 4;
  const bottom = data.subarray((c.height - 1) * stride);
  let y = c.height - 1;
  while (y > 0 && data.subarray(y * stride, (y + 1) * stride).every((v, i) => v === bottom[i])) y--;
  const height = Math.min(c.height, Math.max(min, y + 24));
  if (height === c.height) return base64;
  const out = document.createElement("canvas");
  out.width = c.width; out.height = height;
  out.getContext("2d").drawImage(c, 0, 0);
  return out.toDataURL("image/png").split(",")[1];
}

// A diagram that cannot be shot is left out with a note, so the rest of the review still runs.
async function shootDiagrams(page, outDir, notes) {
  const diagrams = [];
  const marked = await page.evaluate(markDiagrams, MAX_DIAGRAMS);
  // Text size is a property of the layout: measured at the phone width as well as the desktop one.
  const sizes = {};
  for (const width of [SHOTS.find((s) => s.name === "phone-light").width, 1280]) {
    await page.setViewportSize({ width, height: 800 });
    for (const d of marked) sizes[d.index] = [...(sizes[d.index] || []), await page.locator(`[data-design-loop-diagram="${d.index}"]`).evaluate(diagramTextSize).catch(() => null)];
  }
  for (const d of marked) {
    const name = `diagram-${d.index + 1}`;
    const element = page.locator(`[data-design-loop-diagram="${d.index}"]`);
    try {
      const dom = await element.evaluate(diagramAudit);
      const measured = (sizes[d.index] || []).filter((x) => x?.texts);
      const exact = measured.length > 0;
      const worst = measured.map((x) => x.smallest).sort((a, b) => a.px - b.px)[0];
      if (worst && worst.px < SMALL_DIAGRAM_PX - SMALL_DIAGRAM_TOLERANCE) dom.push({ rule: "diagram.small-text", text: worst.text, detail: `text renders at ${worst.px} px, under the ${SMALL_DIAGRAM_PX} px floor (measured at 390 and 1280 px width)` });
      await element.evaluate(isolate);
      let raw;
      try { raw = await element.screenshot({ animations: "disabled", timeout: 10000 }); }
      finally { await element.evaluate(isolate, true); }
      const base64 = await page.evaluate(fitShot, [raw.toString("base64"), MAX_SIDE]);
      const path = join(outDir, name + ".png");
      writeFileSync(path, Buffer.from(base64, "base64"));
      diagrams.push({ name, where: d.where, path, dom, exact, base64 });
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
    for (const f of await page.evaluate(measuredAudit, "rest")) audit.push({ key: "render", ...f, viewport: s.width, scheme: s.scheme }); // before any scrolling
    const height = await page.evaluate(() => document.documentElement.scrollHeight);
    const path = join(outDir, s.name + ".png");
    const buffer = await page.screenshot({ fullPage: true, clip: { x: 0, y: 0, width: s.width, height: Math.min(Math.max(height, 280), MAX_SIDE) } });
    writeFileSync(path, buffer);
    shots.push({ ...s, path, base64: buffer.toString("base64"), trimmed: await page.evaluate(trimShot, [buffer.toString("base64"), 280]) });
    const r = await page.evaluate(`(${AUDIT})(${JSON.stringify({ level })})`);
    for (const [key, list] of Object.entries(r.findings)) for (const f of list) audit.push({ key, ...f, viewport: s.width, scheme: s.scheme });
    for (const f of await page.evaluate(craftAudit)) audit.push({ key: "craft", ...f, viewport: s.width, scheme: s.scheme });
    for (const f of await page.evaluate(vocabAudit)) audit.push({ key: "vocab", ...f, viewport: s.width, scheme: s.scheme });
    for (const f of await page.evaluate(measuredAudit, "late")) audit.push({ key: "render", ...f, viewport: s.width, scheme: s.scheme }); // last: it scrolls and restores
  }
  // Card drift depends on how the text wraps, so it is measured over a width sweep (DOM only, light).
  await page.emulateMedia({ colorScheme: "light", reducedMotion: "reduce" });
  const widths = [...new Set([...SWEEP, ...SHOTS.map((s) => s.width)])].sort((a, b) => a - b);
  for (const width of widths) {
    await page.setViewportSize({ width, height: 800 });
    for (const f of await page.evaluate(alignmentAudit)) audit.push({ key: "alignment", ...f, viewport: width, widths });
    for (const f of await page.evaluate(widowAudit)) audit.push({ key: "widow", ...f, viewport: width, widths });
  }
  await page.setViewportSize({ width: 320, height: 256 }); // WCAG 1.4.10: reflow at 320 CSS px
  for (const f of await page.evaluate(reflowAudit)) audit.push({ key: "reflow", ...f, viewport: 320, scheme: "light" });
  await page.setViewportSize({ width: 1280, height: 800 });
  for (const f of await page.evaluate(motionAudit)) audit.push({ key: "motion", ...f, viewport: 1280, scheme: "light" }); // reduced motion is emulated above
  const last = SHOTS[SHOTS.length - 1];
  await page.setViewportSize({ width: last.width, height: 800 });
  await page.emulateMedia({ colorScheme: last.scheme, reducedMotion: "reduce" });
  return { shots, audit };
}

// Consecutive tested widths that fail become one band: "1024-1072 px".
function bands(hit, widths) {
  const out = [];
  for (const w of widths.filter((x) => hit.includes(x))) {
    const i = widths.indexOf(w);
    if (out.length && widths[i - 1] === out[out.length - 1][1]) out[out.length - 1][1] = w;
    else out.push([w, w]);
  }
  return out.map(([a, b]) => (a === b ? `${a} px` : `${a}-${b} px`));
}

// Vocabulary rules no real page has confirmed yet (zero real hits on 14 pages, caught on synthetic and mutated pages):
// reported, never failing the run, like tell.icon-tile. wcag.reflow and wcag.non-text-contrast hit real defects and fail.
const ADVISORY = new Set(["type.heading-ladder", "layout.proximity", "type.tabular-figures", "wcag.text-spacing", "motion.reduced", "perf.layout-shift", "wcag.focus-visible", "wcag.focus-not-obscured"]);

function auditFindings(audit) {
  const seen = new Map();
  for (const f of audit) {
    const id = `${f.key}|${f.rule}|${f.element}|${f.text}`;
    if (f.key === "alignment" || f.key === "widow") { // width dependent: the failing widths become bands
      const hit = seen.get(id) ?? seen.set(id, { rule: f.rule ?? "layout.alignment", status: "fail", tier: "audit", confidence: 1, hits: [], widths: f.widths, evidence: { element: f.element, text: f.text, observed: f.observed, required: f.required } }).get(id);
      hit.hits.push(f.viewport);
      hit.evidence.where = bands(hit.hits, hit.widths);
      continue;
    }
    if (seen.has(id)) { seen.get(id).evidence.where.push(`${f.viewport} ${f.scheme}`); continue; }
    seen.set(id, { rule: f.rule ?? "wcag." + f.key, status: ADVISORY.has(f.rule) ? "advisory" : "fail", tier: "audit", confidence: 1, evidence: { element: f.element, text: f.text, observed: f.observed, required: f.required, where: [`${f.viewport} ${f.scheme}`] } });
  }
  // A lone last word that appears only between the screenshot widths is not what a reader of the shots sees: the sweep does not report it.
  return [...seen.values()].filter((f) => f.rule !== "type.widow" || SHOTS.some((s) => f.hits.includes(s.width))).map(({ hits, widths, ...f }) => f);
}

// The page's three screenshots, labeled as the questions name them.
const pageImages = (shots) => VISUAL_SHOTS.map((n) => shots.find((s) => s.name === n))
  .map((s) => ({ key: LABEL[s.name], caption: `The ${LABEL[s.name]} screenshot (${s.width} px wide, ${s.scheme}):`, base64: s.base64 }));
const trimmedImages = (shots) => pageImages(shots).map((img, i) => ({ ...img, base64: VISUAL_SHOTS.map((n) => shots.find((s) => s.name === n))[i].trimmed }));
const DIAGRAM_CONTEXT = "A diagram from a web page, shot on its own at the size the reader sees it.";

// One Jev call: text state, labeled images, typed questions.
export async function askJev({ rules, state, images, keys, fetch }) {
  const questions = Object.fromEntries(rules.map((r) => [r.id, r.type === "score"
    ? { type: "score", instructions: r.instructions, criteria: r.criteria }
    : { type: keys.gateway ? "boolean" : "noul", instructions: r.instructions }]));
  let response;
  if (keys.gateway) {
    const stateParts = Object.entries(state).map(([k, v]) => ({ type: "text", text: `${k}: ${JSON.stringify(v)}` }));
    for (const s of images) stateParts.push({ type: "text", text: s.caption }, { type: "file", mediaType: "image/png", data: { type: "data", data: s.base64 } });
    response = await fetch(GATEWAY + "/v4/ai/decision-model", {
      method: "POST",
      headers: { Authorization: "Bearer " + keys.gateway, "Content-Type": "application/json", "ai-gateway-protocol-version": "0.0.1", "ai-decision-model-specification-version": "4", "ai-model-id": "typesafe-ai/jev", ...(images.length && { "TypeSafe-Danger-Zone-Images": "true" }) },
      body: JSON.stringify({ stateParts, questions, providerOptions: { gateway: { ...PRIVACY, only: ["typesafe-ai"] } } }),
    });
  } else {
    const refs = images.map((s) => `shot-${s.key}-${crypto.randomUUID()}`);
    const assets = Object.fromEntries(images.map((s, i) => [refs[i], { type: "image", format: "png", data_base64: s.base64 }]));
    // Jev rejects the image opt-in and an empty assets map on a text-only question.
    const withImages = images.length ? { assets } : {};
    response = await fetch(TYPESAFE, {
      method: "POST",
      headers: { Authorization: "Bearer " + keys.typesafe, "Content-Type": "application/json", ...(images.length && { "TypeSafe-Danger-Zone-Images": "true" }) },
      body: JSON.stringify({ model: "jev-latest", state: { ...state, ...Object.fromEntries(images.map((s, i) => [s.key, refs[i]])) }, ...withImages, questions }),
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
  const shift = await page.evaluate(shiftAudit); // first: a later resize or scroll must not count as a shift of the load
  const { shots, audit } = await shoot(page, outDir, level);
  for (const f of shift) audit.push({ key: "shift", ...f, viewport: 1280, scheme: "light" });
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.emulateMedia({ colorScheme: "light" });
  // A diagram far down a long page never reaches the 1568 px screenshots: each gets its own shot.
  const notes = [];
  const diagrams = await shootDiagrams(page, outDir, notes);
  const dom = [...await page.evaluate(tellsAudit), ...await page.evaluate(measuredAudit, "slop")];
  const focus = await focusAudit(page); // keyboard tabbing: last among the DOM checks, it moves focus and scroll
  for (const f of [...focus.visible, ...focus.obscured]) audit.push({ key: "focus", ...f, viewport: 1280, scheme: "light" });
  const text = await page.evaluate(pageText, MAX_TEXT_BLOCKS);
  const textHits = uiInstructions(text);
  const headlines = await page.evaluate(() => [...document.querySelectorAll("h1, h2")].slice(0, 6).map((h) => h.textContent.trim().replace(/\s+/g, " ").slice(0, 120)));
  const findings = [
    ...dom.map((d) => ({ rule: d.rule, status: d.advisory ? "advisory" : "fail", tier: "dom", confidence: 1, evidence: { element: d.element, where: "desktop-light" }, detail: d.detail })),
    ...auditFindings(audit),
    ...diagrams.flatMap((g) => g.dom.map((d) => ({ rule: d.rule, status: "fail", tier: "dom", confidence: 1, evidence: { diagram: g.name, where: g.where, element: d.text }, detail: d.detail }))),
    ...textHits.map((t) => ({ rule: "text.ui-instructions", status: "fail", tier: "dom", confidence: 1, evidence: { text: t, where: "page text" }, detail: "tells the reader how to operate the page; cut it and fix the design so the page shows it (a hint for screen readers goes in aria-label)" })),
  ];
  const cost = { jev: 0, llm: 0 };
  const keys = { gateway: env.AI_GATEWAY_API_KEY || env.VERCEL_AI_GATEWAY_API_KEY, typesafe: env.TYPESAFE_API_KEY };
  const dark = shots.find((s) => s.name === "desktop-dark").base64 !== shots.find((s) => s.name === "desktop-light").base64;
  if (!dark) notes.push("no dark scheme: the dark screenshots equal the light ones");
  const rules = VISUAL_RULES.filter((r) => dark || r.id !== "layout.dark");
  const tiers = { dom: "ran", audit: `ran (${level})`, visual: "skipped: no model key", llm: "not needed", diagrams: diagrams.length ? `${diagrams.length} shot, dom ran` : "none found", text: textHits.length ? `dom flagged ${textHits.length}` : `dom clean (${text.length} blocks)` };
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
    // tell.sparse alone, on shots that end below the last content, with its own context.
    try {
      const trimmed = trimmedImages(shots);
      const r = await judge({
        rules: [SPARSE_RULE], proven: new Set(), keys, detail, evidence: { where: VISUAL_SHOTS.join(", ") },
        jev: (rs) => askJev({ rules: rs, state: { whitespace_rules: WHITESPACE_RULES }, images: [...trimmed, ...sparseExamples()], keys, fetch }),
        model: (rs) => askModel({ rules: rs, intro: "You review a web page against a whitespace rule. Images in order: " + VISUAL_SHOTS.join(", ") + ", each ending just below the last content.\n" + WHITESPACE_RULES, images: trimmed, key: keys.gateway, model, fetch, env }),
      });
      tiers.sparse = "jev ran";
      verdicts = { ...verdicts, ...r.verdicts };
      add(r);
    } catch (error) {
      tiers.sparse = "failed: " + error.message; // fail open
    }
    for (const g of diagrams) {
      const images = [{ key: "diagram", caption: "The diagram:", base64: g.base64 }];
      try {
        const r = await judge({
          rules: DIAGRAM_RULES, proven: new Set([...g.dom.map((d) => d.rule), ...(g.exact ? ["diagram.small-text"] : [])]), keys, detail, evidence: { diagram: g.name, where: g.where },
          jev: (rs) => askJev({ rules: rs, state: { context: DIAGRAM_CONTEXT }, images, keys, fetch }),
          model: (rs) => askModel({ rules: rs, intro: "You review one diagram from a web page, shot on its own at the size the reader sees it, against design rules.", images, key: keys.gateway, model, fetch, env }),
        });
        g.jev = r.verdicts;
        add(r, g.name + "/");
        if (g.exact && !g.dom.some((d) => d.rule === "diagram.small-text")) passed.push(g.name + "/diagram.small-text"); // the DOM measured every text
      } catch (error) {
        g.jev = { failed: error.message }; // fail open: the DOM findings for this diagram still stand
      }
    }
    // A pattern hit is exact, so Jev is asked only about text the patterns passed.
    if (!textHits.length && text.length) {
      try {
        const r = await judge({
          rules: TEXT_RULES, proven: new Set(), keys, detail, evidence: { where: "page text" },
          jev: (rs) => askJev({ rules: rs, state: { page_text: text }, images: [], keys, fetch }),
          model: (rs) => askModel({ rules: rs, intro: "You review the visible text of a web page against a writing rule; there are no images. Page text, one block per line:\n" + text.join("\n"), images: [], key: keys.gateway, model, fetch, env }),
        });
        tiers.text += ", jev ran";
        add(r);
      } catch (error) {
        tiers.text += ", jev failed: " + error.message; // fail open: the pattern tier still stands
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
    assertLoaded(await page.goto(args.url, { waitUntil: "networkidle" }), args.url);
    const report = await review(page, { outDir: args.out, level: args.level, model: args.model, detail: args.detail });
    console.log(JSON.stringify(report, null, 2));
    process.exitCode = report.findings.some((f) => f.status === "fail") ? 1 : 0;
  } finally {
    await browser.close();
  }
}

// A server that answers 404 still renders a page, and every tier would review that error page as if it were the target.
export function assertLoaded(response, url) {
  const status = response?.status();
  if (status >= 400) throw new Error(`HTTP ${status} for ${url}: nothing to review; check the URL and that the server serves this file`);
}

function sameFile(a, b) { try { return realpathSync(a) === realpathSync(b); } catch { return false; } }
// Compare real paths: an installed Skill is started through a symlink.
if (process.argv[1] && sameFile(process.argv[1], fileURLToPath(import.meta.url))) await main(process.argv.slice(2));
