// Design loop: screenshots of a page, cheap checks first, a model only when in doubt.
//
//   node design-loop.mjs <url> [--out dir] [--level aa|aaa] [--model provider/model] [--detail]
//
// Tiers, in order of cost:
//   dom    - generic-look tells read from the DOM (`tellsAudit`): free, exact, with a selector.
//   audit  - `reading-audit.js` at 1280 and 390 px, light and dark: contrast, targets, overflow.
//   jev    - typed questions on the screenshots (TypeSafe Jev, images are an opt-in beta):
//            a noul is a yes/no probability, a score a level; about $0.0001 per page.
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
  if (p >= YES) return { status: "fail", confidence: p, probability: p };
  if (p <= NO) return { status: "pass", confidence: 1 - p, probability: p };
  return { status: "unsure", confidence: Math.abs(p - 0.5) * 2, probability: p };
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
  }
  return { shots, audit };
}

function auditFindings(audit) {
  const seen = new Map();
  for (const f of audit) {
    const id = `${f.key}|${f.element}|${f.text}`;
    if (seen.has(id)) { seen.get(id).evidence.where.push(`${f.viewport} ${f.scheme}`); continue; }
    seen.set(id, { rule: "wcag." + f.key, status: "fail", tier: "audit", confidence: 1, evidence: { element: f.element, text: f.text, observed: f.observed, required: f.required, where: [`${f.viewport} ${f.scheme}`] } });
  }
  return [...seen.values()];
}

async function askJev({ rules, shots, headlines, keys, fetch }) {
  const pick = VISUAL_SHOTS.map((n) => shots.find((s) => s.name === n));
  const questions = Object.fromEntries(rules.map((r) => [r.id, r.type === "score"
    ? { type: "score", instructions: r.instructions, criteria: r.criteria }
    : { type: keys.gateway ? "boolean" : "noul", instructions: r.instructions }]));
  let response;
  if (keys.gateway) {
    const stateParts = [{ type: "text", text: "headlines: " + JSON.stringify(headlines) }];
    for (const s of pick) stateParts.push({ type: "text", text: `The ${LABEL[s.name]} screenshot (${s.width} px wide, ${s.scheme}):` }, { type: "file", mediaType: "image/png", data: { type: "data", data: s.base64 } });
    response = await fetch(GATEWAY + "/v4/ai/decision-model", {
      method: "POST",
      headers: { Authorization: "Bearer " + keys.gateway, "Content-Type": "application/json", "ai-gateway-protocol-version": "0.0.1", "ai-decision-model-specification-version": "4", "ai-model-id": "typesafe-ai/jev", "TypeSafe-Danger-Zone-Images": "true" },
      body: JSON.stringify({ stateParts, questions, providerOptions: { gateway: { ...PRIVACY, only: ["typesafe-ai"] } } }),
    });
  } else {
    const assets = Object.fromEntries(pick.map((s) => [`shot-${s.name}-${crypto.randomUUID()}`, { type: "image", format: "png", data_base64: s.base64 }]));
    const refs = Object.keys(assets);
    response = await fetch(TYPESAFE, {
      method: "POST",
      headers: { Authorization: "Bearer " + keys.typesafe, "Content-Type": "application/json", "TypeSafe-Danger-Zone-Images": "true" },
      body: JSON.stringify({ model: "jev-latest", state: { headlines, desktop: refs[0], phone: refs[1], dark: refs[2] }, assets, questions }),
    });
  }
  if (!response.ok) throw new Error(`Jev ${response.status}: ${(await response.text()).slice(0, 200)}`);
  const payload = await response.json();
  const confidence = payload.providerMetadata?.typesafe?.confidence || {};
  const answers = Object.fromEntries(Object.entries(payload.answers || {}).map(([id, a]) => [id, { ...a, confidence: a.confidence ?? confidence[id] }]));
  const tokens = payload.usage?.inputTokens ?? payload.usage?.input_tokens ?? 0;
  return { answers, cost: tokens * JEV_USD_PER_TOKEN[keys.gateway ? "gateway" : "typesafe"] };
}

async function askModel({ rules, shots, headlines, key, model, fetch, env }) {
  checkModel(model, env);
  const pick = VISUAL_SHOTS.map((n) => shots.find((s) => s.name === n));
  const text = "You review a web page against design rules. Images in order: " + VISUAL_SHOTS.join(", ") +
    ". headlines: " + JSON.stringify(headlines) + "\nFor each rule answer whether the page fails it, where on which screenshot, and the smallest fix.\n" +
    rules.map((r) => `- ${r.id}: ${r.instructions}${r.type === "score" ? ` Fail when the answer is one of: ${JSON.stringify(r.criteria.slice(0, r.fail + 1))}` : " Fail when yes."}`).join("\n") +
    '\nReply with JSON only: {"<rule id>": {"fail": true|false, "where": "...", "fix": "..."}}';
  const response = await fetch(GATEWAY + "/v1/chat/completions", {
    method: "POST",
    headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" },
    body: JSON.stringify({ model, max_tokens: 1500, messages: [{ role: "user", content: [{ type: "text", text }, ...pick.map((s) => ({ type: "image_url", image_url: { url: "data:image/png;base64," + s.base64 } }))] }], providerOptions: { gateway: PRIVACY } }),
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

// Reviews the page that is already loaded in `page`; viewport and scheme change in place.
export async function review(page, { env = process.env, fetch = globalThis.fetch, outDir, level = "aa", model = DEFAULT_MODEL, detail = false } = {}) {
  const started = Date.now();
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, ".gitignore"), "*\n"); // screenshots and report never reach a commit
  const { shots, audit } = await shoot(page, outDir, level);
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.emulateMedia({ colorScheme: "light" });
  const dom = await page.evaluate(tellsAudit);
  const headlines = await page.evaluate(() => [...document.querySelectorAll("h1, h2")].slice(0, 6).map((h) => h.textContent.trim().replace(/\s+/g, " ").slice(0, 120)));
  const findings = [
    ...dom.map((d) => ({ rule: d.rule, status: "fail", tier: "dom", confidence: 1, evidence: { element: d.element, where: "desktop-light" }, detail: d.detail })),
    ...auditFindings(audit),
  ];
  const cost = { jev: 0, llm: 0 };
  const keys = { gateway: env.AI_GATEWAY_API_KEY || env.VERCEL_AI_GATEWAY_API_KEY, typesafe: env.TYPESAFE_API_KEY };
  const notes = [];
  const dark = shots.find((s) => s.name === "desktop-dark").base64 !== shots.find((s) => s.name === "desktop-light").base64;
  if (!dark) notes.push("no dark scheme: the dark screenshots equal the light ones");
  const rules = VISUAL_RULES.filter((r) => dark || r.id !== "layout.dark");
  const tiers = { dom: "ran", audit: `ran (${level})`, visual: "skipped: no model key", llm: "not needed" };
  const passed = [];
  const verdicts = {}; // Jev's verdict per visual rule, kept so a reader can see why a rule escalated
  let escalated = 0;
  if (keys.gateway || keys.typesafe) {
    try {
      const jev = await askJev({ rules, shots, headlines, keys, fetch });
      cost.jev = jev.cost;
      tiers.visual = "ran";
      const domRules = new Set(dom.map((d) => d.rule));
      const open = [];
      for (const rule of rules) {
        if (domRules.has(rule.id)) continue; // the DOM already proved it, with a selector
        const d = decide(rule, jev.answers[rule.id]);
        verdicts[rule.id] = d;
        if (d.status === "pass") passed.push(rule.id);
        else open.push({ rule, d });
      }
      // Only unsure rules need the model; a confident Jev failure stands on its own unless
      // the caller wants the model's where and fix for it too (`detail`).
      const ask = open.filter(({ d }) => detail || d.status === "unsure");
      const jevFinding = ({ rule, d }) => ({ rule: rule.id, status: d.status, tier: "jev", confidence: d.confidence, evidence: { where: VISUAL_SHOTS.join(", ") }, detail: rule.instructions });
      findings.push(...open.filter((o) => !ask.includes(o)).map(jevFinding));
      escalated = ask.length;
      if (!ask.length) {
        // nothing to ask
      } else if (!keys.gateway) {
        tiers.llm = "skipped: no gateway key";
        findings.push(...ask.map(jevFinding));
      } else {
        try {
          const m = await askModel({ rules: ask.map((o) => o.rule), shots, headlines, key: keys.gateway, model, fetch, env });
          cost.llm = m.cost;
          tiers.llm = `ran (${model})`;
          for (const o of ask) {
            const v = m.verdicts[o.rule.id];
            if (v && v.fail === false) passed.push(o.rule.id);
            else if (v) findings.push({ rule: o.rule.id, status: "fail", tier: "llm", confidence: o.d.confidence, evidence: { where: v.where || VISUAL_SHOTS.join(", ") }, detail: v.fix || o.rule.instructions });
            else findings.push(jevFinding(o));
          }
        } catch (error) {
          tiers.llm = "failed: " + error.message;
          findings.push(...ask.map(jevFinding));
        }
      }
    } catch (error) {
      tiers.visual = "failed: " + error.message; // fail open: the cheap tiers still stand
    }
  }
  const report = {
    url: page.url(), tiers, notes, findings, passed, escalated, jev: verdicts,
    cost_usd: { jev: +cost.jev.toFixed(6), llm: +cost.llm.toFixed(6) },
    seconds: +((Date.now() - started) / 1000).toFixed(1),
    shots: shots.map(({ base64, ...s }) => s),
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
