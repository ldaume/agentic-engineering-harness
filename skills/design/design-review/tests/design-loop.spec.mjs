// Run: npx playwright test -c skills/design/design-review/tests
// The model calls are stubbed: these tests check the tiers and their wiring, not a model.
import { test, expect } from "@playwright/test";
import { readFileSync, mkdtempSync, mkdirSync, writeFileSync, symlinkSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import * as loop from "../scripts/design-loop.mjs";
import { tellsAudit, alignmentAudit, decide, review, firstJson, loadChromium, checkModel, VISUAL_RULES, DIAGRAM_RULES, TEXT_RULES, diagramAudit, uiInstructions, craftAudit, widowAudit, SPARSE_RULE } from "../scripts/design-loop.mjs";

const fixture = (name) => readFileSync(fileURLToPath(new URL(`fixtures/${name}`, import.meta.url)), "utf8");
const out = () => mkdtempSync(join(tmpdir(), "design-loop-"));

// A stub for fetch: Jev answers every visual rule with the given probability or score,
// the escalation model answers every rule it is asked about with `fail`.
function stubFetch({ p = 0.05, score = 3, fail = true } = {}) {
  const calls = [];
  const fn = async (url, init) => {
    const body = JSON.parse(init.body);
    calls.push({ url, body });
    if (url.includes("decision-model")) {
      // Jev's contract: score levels are an ordered array, low to high; an object is a 400.
      for (const q of Object.values(body.questions)) if (q.type === "score" && !Array.isArray(q.criteria)) return new Response("criteria must be an array", { status: 400 });
      const answers = Object.fromEntries(Object.entries(body.questions).map(([id, q]) =>
        [id, q.type === "score" ? { type: "score", score, probabilities: {} } : { type: "boolean", probability: p }]));
      return Response.json({ answers, usage: { inputTokens: 1000 }, providerMetadata: { typesafe: { confidence: {} } } });
    }
    const asked = [...body.messages[0].content[0].text.matchAll(/^- ([\w.-]+):/gm)].map((m) => m[1]);
    const verdicts = Object.fromEntries(asked.map((id) => [id, { fail, where: "top of the desktop screenshot", fix: "do X" }]));
    return Response.json({ choices: [{ message: { content: JSON.stringify(verdicts) } }], usage: { cost: 0.001 } });
  };
  fn.calls = calls;
  return fn;
}

test("given the generic AI page, the DOM tier flags gradient, hero with three cards, emoji icons, font, accent bar and glass", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.setContent(fixture("generic.html"));
  const hits = (await page.evaluate(tellsAudit)).map((f) => f.rule).sort();
  expect(hits).toEqual(["tell.emoji-icons", "tell.font", "tell.glass", "tell.gradient", "tell.hero-cards", "tell.left-bar"]);
});

test("given the clean page, the DOM tier flags nothing", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.setContent(fixture("clean.html"));
  expect(await page.evaluate(tellsAudit)).toEqual([]);
});

test("given Jev answers, a clear yes fails, a clear no passes, the middle band is unsure", () => {
  const noul = VISUAL_RULES.find((r) => r.type === "noul");
  expect(decide(noul, { probability: 0.9 }).status).toBe("fail");
  expect(decide(noul, { probability: 0.1 }).status).toBe("pass");
  expect(decide(noul, { probability: 0.5 }).status).toBe("unsure");
  expect(decide(noul, { probability: 0.3 }).status).toBe("pass");
  expect(decide(noul, { probability: 0.7 }).status).toBe("fail");
  // A score is a position between levels: near the first passing level it is unsure, whatever its spread.
  const score = VISUAL_RULES.find((r) => r.id === "visual.hierarchy"); // fails at level 1 or lower
  expect(decide(score, { score: 0.4, confidence: 0.2 }).status).toBe("fail");
  expect(decide(score, { score: 2.8, confidence: 0.2 }).status).toBe("pass");
  expect(decide(score, { score: 1.9, confidence: 0.9 }).status).toBe("unsure");
});

test("given no model key, the review still runs the DOM tier and the reading audit and says the visual tier was skipped", async ({ page }) => {
  await page.setContent(fixture("generic.html"));
  const r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  expect(r.tiers.visual).toBe("skipped: no model key");
  expect(r.findings.some((f) => f.rule === "tell.gradient" && f.tier === "dom")).toBe(true);
  expect(r.shots).toHaveLength(4);
});

test("given a clean page and confident Jev passes, the review passes with no escalation", async ({ page }) => {
  await page.setContent(fixture("clean.html"));
  const fetch = stubFetch({ p: 0.05, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  expect(r.findings, JSON.stringify(r.findings)).toEqual([]);
  expect(r.tiers.visual).toBe("ran");
  expect(r.escalated).toBe(0);
  expect(fetch.calls.filter((c) => c.url.includes("chat/completions"))).toHaveLength(0);
});

test("given unsure Jev answers, those rules escalate in one model call and its verdicts become findings", async ({ page }) => {
  await page.setContent(fixture("clean.html"));
  const fetch = stubFetch({ p: 0.6, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const nouls = VISUAL_RULES.filter((x) => x.type === "noul").length;
  expect(r.escalated).toBe(nouls + 1 + TEXT_RULES.length); // tell.sparse and the page-text rule escalate in their own calls
  expect(modelCalls(fetch).filter((c) => c.images > 0)).toHaveLength(2); // the shared rules, then tell.sparse
  expect(r.findings.filter((f) => f.tier === "llm" && !f.rule.startsWith("text."))).toHaveLength(nouls + 1);
  expect(r.findings[0].evidence).toMatchObject({ where: "top of the desktop screenshot" });
  expect(r.cost_usd.llm).toBeCloseTo(0.001);
  expect(r.cost_usd.jev).toBeGreaterThan(0);
});

test("given a sticky header with backdrop blur and a small gradient button, the DOM tier flags neither", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.setContent(fixture("clean.html").replace("<header>", `<header style="position:sticky;top:0;backdrop-filter:blur(8px)"><button style="background:linear-gradient(#6d28d9,#4f46e5);color:#fff">Go</button>`));
  expect(await page.evaluate(tellsAudit)).toEqual([]);
});

test("given a page without a dark scheme, the dark question is not asked and the report says why", async ({ page }) => {
  await page.setContent(fixture("generic.html"));
  const fetch = stubFetch();
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const asked = Object.keys(fetch.calls.find((c) => c.url.includes("decision-model")).body.questions);
  expect(asked).not.toContain("layout.dark");
  expect(r.notes).toContain("no dark scheme: the dark screenshots equal the light ones");
});

test("given text symbols such as an arrow or a copyright sign in list items, the DOM tier does not call them emoji icons", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.setContent(fixture("clean.html").replace("</main>", "<ul><li>Next page ↔ previous</li><li>© 2026 Harbor office ™</li></ul></main>"));
  expect(await page.evaluate(tellsAudit)).toEqual([]);
});

test("given a model reply with prose after the JSON, its verdicts are still read", () => {
  expect(firstJson('Here: {"tell.uniform": {"fail": true, "where": "cards {a}"}}\nNote: {"x": 1}')).toEqual({ "tell.uniform": { fail: true, where: "cards {a}" } });
  expect(firstJson("no json")).toEqual({});
});

test("given confident Jev failures, they stand as findings without a model call unless detail is asked for", async ({ page }) => {
  await page.setContent(fixture("clean.html"));
  const fetch = stubFetch({ p: 0.9, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  expect(fetch.calls.filter((c) => c.url.includes("chat/completions"))).toHaveLength(0);
  expect(r.findings.filter((f) => f.tier === "jev" && f.status === "fail").length).toBeGreaterThan(0);
  const detailed = stubFetch({ p: 0.9, score: 3 });
  const d = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch: detailed, outDir: out(), detail: true });
  expect(modelCalls(detailed).filter((c) => c.images > 0)).toHaveLength(2); // the shared rules, then tell.sparse
  expect(d.findings.some((f) => f.tier === "llm")).toBe(true);
});

test("given the project the agent works in has Playwright, the runner uses that one, since an installed Skill has no node_modules", async () => {
  const project = out();
  const pkg = join(project, "node_modules", "playwright");
  mkdirSync(pkg, { recursive: true });
  writeFileSync(join(pkg, "package.json"), JSON.stringify({ name: "playwright", main: "index.js" }));
  writeFileSync(join(pkg, "index.js"), "module.exports = { chromium: 'from-project' };");
  expect(await loadChromium(project)).toBe("from-project");
});

test("given the runner is started through a symlink to it, as an installed Skill is, it still runs", async () => {
  const link = join(out(), "design-loop.mjs");
  symlinkSync(fileURLToPath(new URL("../scripts/design-loop.mjs", import.meta.url)), link);
  const run = spawnSync(process.execPath, [link, "--help"], { encoding: "utf8" });
  expect(run.status).toBe(0);
  expect(run.stdout).toMatch(/usage: node design-loop\.mjs <url>/);
});

test("given the module is imported by a host whose argv[1] is not a file, the import does not throw", async () => {
  const src = fileURLToPath(new URL("../scripts/design-loop.mjs", import.meta.url));
  const run = spawnSync(process.execPath, ["--input-type=module", "-e", `await import(${JSON.stringify("file://" + src)})`, "no-such-file"], { encoding: "utf8" });
  expect(run.stderr).toBe("");
  expect(run.status).toBe(0);
});

test("given Playwright is in neither the project nor beside the script, the error names the exact install command", async () => {
  const empty = out();
  await expect(loadChromium(empty, empty)).rejects.toThrow(/npm i --no-save playwright && npx playwright install chromium/);
});

test("given only the script's own directory has Playwright, the runner falls back to it", async () => {
  const scriptDir = out();
  const pkg = join(scriptDir, "node_modules", "playwright");
  mkdirSync(pkg, { recursive: true });
  writeFileSync(join(pkg, "package.json"), JSON.stringify({ name: "playwright", main: "index.js" }));
  writeFileSync(join(pkg, "index.js"), "module.exports = { chromium: 'from-script-dir' };");
  expect(await loadChromium(out(), scriptDir)).toBe("from-script-dir");
});

test("given an escalation model from a restricted-jurisdiction family or an unlisted provider, the review refuses it unless that exact id is approved", async () => {
  expect(() => checkModel("anthropic/claude-haiku-5.5", {})).not.toThrow();
  expect(() => checkModel("google/gemini-3-flash", {})).not.toThrow();
  for (const id of ["deepseek/deepseek-v4-flash-vision-exp", "alibaba/qwen3.8-flash", "anthropic/qwen-proxy", "unknownco/vision-1"]) {
    expect(() => checkModel(id, {}), id).toThrow(/approv/);
  }
  expect(checkModel("alibaba/qwen3.8-flash", { OWNER_APPROVED_MODELS: "alibaba/qwen3.8-flash" })).toBe("alibaba/qwen3.8-flash");
  expect(() => checkModel("alibaba/qwen3.8-flash", { OWNER_APPROVED_MODELS: "alibaba/qwen3.7-flash" })).toThrow();
});

test("given a refused escalation model, no screenshot is sent to it and the unsure rules stay unsure", async ({ page }) => {
  await page.setContent(fixture("clean.html"));
  const fetch = stubFetch({ p: 0.5, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out(), model: "deepseek/deepseek-v4-flash-vision-exp" });
  expect(fetch.calls.filter((c) => c.url.includes("chat/completions"))).toHaveLength(0);
  expect(r.tiers.llm).toMatch(/^failed: .*approv/);
  expect(r.findings.every((f) => f.status === "unsure" || f.tier !== "llm")).toBe(true);
});

// Diagrams: each one is shot on its own and asked the diagram rules.
const modelCalls = (fetch) => fetch.calls.filter((c) => c.url.includes("chat/completions"))
  .map((c) => ({ ...c, images: c.body.messages[0].content.filter((p) => p.type === "image_url").length }));
const jevCalls = (fetch) => fetch.calls.filter((c) => c.url.includes("decision-model"));
const diagramCalls = (fetch) => jevCalls(fetch).filter((c) => Object.keys(c.body.questions).every((id) => id.startsWith("diagram.")));
const pngSize = (base64) => { const b = Buffer.from(base64, "base64"); return { width: b.readUInt32BE(16), height: b.readUInt32BE(20) }; };

test("given the broken diagram, the DOM tier flags the title past its frame, the stacked labels and the line through a box, and nothing on the clean one", async ({ page }) => {
  await page.setContent(fixture("diagram-broken.html"));
  const hits = await page.locator("svg.arch").evaluate(diagramAudit);
  expect(hits.map((h) => h.rule).sort()).toEqual(["diagram.clipped-text", "diagram.line-crossing", "diagram.overlap"]);
  expect(hits.find((h) => h.rule === "diagram.clipped-text").text).toMatch(/^Primary region, north pier/);
  expect(hits.find((h) => h.rule === "diagram.line-crossing").text).toBe("Tide model");
  await page.setContent(fixture("diagram-clean.html"));
  expect(await page.locator("svg.arch").evaluate(diagramAudit)).toEqual([]);
});

test("given a diagram far below the first screen, in a scroll container under a sticky header and a fixed banner, the review shoots all of it on its own and asks Jev every diagram rule about that shot", async ({ page }) => {
  const banner = '<div style="position:fixed;left:0;right:0;bottom:0;height:500px;background:rgb(200,0,0)"></div>';
  await page.setContent(fixture("diagram-clean.html").replace("</body>", banner + "</body>"));
  const fetch = stubFetch({ p: 0.05, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  expect(r.diagrams).toHaveLength(1); // the 24 px header icon is not a diagram
  const calls = diagramCalls(fetch);
  expect(calls).toHaveLength(1);
  expect(Object.keys(calls[0].body.questions).sort()).toEqual(DIAGRAM_RULES.map((x) => x.id).sort());
  const images = calls[0].body.stateParts.filter((p) => p.type === "file");
  expect(images).toHaveLength(1);
  const shot = images[0].data.data;
  const size = pngSize(shot); // an inline SVG may round up by a pixel
  expect(size.width).toBe(760);
  expect(size.height).toBeGreaterThanOrEqual(420);
  expect(size.height).toBeLessThanOrEqual(422);
  const pixels = await page.evaluate(async (b64) => {
    const img = new Image(); img.src = "data:image/png;base64," + b64; await img.decode();
    const c = document.createElement("canvas"); c.width = img.width; c.height = img.height;
    const ctx = c.getContext("2d"); ctx.drawImage(img, 0, 0);
    return [[30, 66], [40, 200], [40, 390], [700, 390]].map(([x, y]) => [...ctx.getImageData(x, y, 1, 1).data.slice(0, 3)]);
  }, shot);
  // Every sample sits inside a cluster: its fill, not the page behind a 260 px scroll box, a header or a banner.
  expect(pixels).toEqual([[238, 241, 246], [238, 241, 246], [238, 241, 246], [238, 241, 246]]);
  expect(r.findings, JSON.stringify(r.findings)).toEqual([]);
});

test("given the broken diagram and no model key, the DOM findings stand with the diagram as evidence", async ({ page }) => {
  await page.setContent(fixture("diagram-broken.html"));
  const r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  const dom = r.findings.filter((f) => f.rule.startsWith("diagram."));
  expect(dom.map((f) => f.rule).sort()).toEqual(["diagram.clipped-text", "diagram.line-crossing", "diagram.overlap"]);
  expect(dom.every((f) => f.tier === "dom" && f.evidence.diagram === r.diagrams[0].name)).toBe(true);
});

test("given the DOM tier already proved diagram rules, Jev is still asked the full set, since its answers shift with the set, but only the unproven rules take its verdict", async ({ page }) => {
  await page.setContent(fixture("diagram-broken.html"));
  const fetch = stubFetch({ p: 0.9, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  expect(Object.keys(diagramCalls(fetch)[0].body.questions).sort()).toEqual(DIAGRAM_RULES.map((x) => x.id).sort());
  const found = r.findings.filter((f) => f.rule.startsWith("diagram."));
  expect(found.map((f) => `${f.rule} ${f.tier}`).sort()).toEqual(["diagram.clipped-text dom", "diagram.line-crossing dom", "diagram.overlap dom"]); // small text on inline SVG is decided by the DOM, and these labels are 15 px
});

test("given the page tells the DOM already proved, Jev is still asked them so the rest keep their calibration", async ({ page }) => {
  await page.setContent(fixture("generic.html"));
  const fetch = stubFetch({ p: 0.05, score: 3 });
  await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const asked = Object.keys(jevCalls(fetch).find((c) => c.body.questions["visual.hierarchy"]).body.questions);
  expect(asked).toContain("tell.gradient");
});

test("given diagram rules, each has its own calibrated threshold instead of the page default", () => {
  const line = DIAGRAM_RULES.find((x) => x.id === "diagram.line-crossing");
  const clipped = DIAGRAM_RULES.find((x) => x.id === "diagram.clipped-text");
  const overlap = DIAGRAM_RULES.find((x) => x.id === "diagram.overlap");
  expect(decide(overlap, { probability: 0.62 }).status).toBe("fail");
  expect(decide(clipped, { probability: 0.62 }).status).toBe("unsure");
  expect(decide(line, { probability: 0.61 }).status).toBe("unsure"); // the false yes on stacked labels
  expect(decide(line, { probability: 0.3 }).status).toBe("unsure");
  expect(decide(clipped, { probability: 0.3 }).status).toBe("pass");
});

test("given unsure Jev answers about a diagram, those rules go to the model with only that diagram's shot and come back as findings naming it", async ({ page }) => {
  await page.setContent(fixture("diagram-clean.html"));
  const fetch = stubFetch({ p: 0.5, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const asks = fetch.calls.filter((c) => c.url.includes("chat/completions") && c.body.messages[0].content[0].text.includes("- diagram."));
  expect(asks).toHaveLength(1);
  expect(asks[0].body.messages[0].content.filter((p) => p.type === "image_url")).toHaveLength(1);
  const found = r.findings.filter((f) => f.rule.startsWith("diagram."));
  expect(found.map((f) => f.rule).sort()).toEqual(DIAGRAM_RULES.map((x) => x.id).filter((id) => id !== "diagram.small-text").sort()); // the DOM measured the text
  expect(found.every((f) => f.tier === "llm" && f.evidence.diagram === r.diagrams[0].name)).toBe(true);
});

test("given eight large diagrams, only the first six are shot", async ({ page }) => {
  const svg = '<svg width="400" height="200" viewBox="0 0 400 200"><rect x="10" y="10" width="380" height="180" fill="#eee" stroke="#333"/><text x="200" y="105" text-anchor="middle">Step</text></svg>';
  await page.setContent(`<main>${Array.from({ length: 8 }, () => `<figure>${svg}</figure>`).join("")}</main>`);
  const r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  expect(r.diagrams).toHaveLength(6);
});

test("given a diagram whose shot fails, the review leaves it out with a note and still reports the page", async ({ page }) => {
  await page.setContent(fixture("diagram-clean.html"));
  const locator = page.locator.bind(page);
  page.locator = (selector) => {
    const l = locator(selector);
    if (selector.startsWith("[data-design-loop-diagram")) l.screenshot = async () => { throw new Error("element is not attached"); };
    return l;
  };
  const r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  expect(r.diagrams).toEqual([]);
  expect(r.notes.some((n) => /^diagram-1 .*not checked: element is not attached/.test(n))).toBe(true);
  expect(r.shots).toHaveLength(4);
});

// Cards in one row: the same part of each card has to sit at the same height.
const align = async (page, name) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.setContent(fixture(name));
  return page.evaluate(alignmentAudit);
};

test("given a row of cards whose texts wrap differently, the alignment check reports the part that drifts and its spread", async ({ page }) => {
  const hits = await align(page, "align-drift.html");
  expect(hits.length).toBeGreaterThan(0);
  expect(hits[0].element).toContain("article.card");
  expect(hits[0].observed).toMatch(/^\d+ px spread/);
  expect(hits[0].required).toBe("within 4 px");
});

test("given the same row built with subgrid, the alignment check passes", async ({ page }) => {
  expect(await align(page, "align-subgrid.html")).toEqual([]);
});

test("given cards with identical text, the alignment check passes", async ({ page }) => {
  expect(await align(page, "align-equal.html")).toEqual([]);
});

test("given six cards wrapped into two aligned rows of three, the alignment check passes", async ({ page }) => {
  expect(await align(page, "align-wrapped.html")).toEqual([]);
});

test("given a nav list of linked cards (li > a, flex column, mt-auto bordered footers), the alignment check reports the drifting divider", async ({ page }) => {
  const hits = await align(page, "align-nav-drift.html");
  expect(hits.length).toBeGreaterThan(0);
  expect(hits[0].element).toContain("li");
  expect(hits[0].element).toContain("span.note");
});

test("given the same linked cards built with nested subgrid, the alignment check passes", async ({ page }) => {
  expect(await align(page, "align-nav-subgrid.html")).toEqual([]);
});

test("given the drifting row, the review reports layout.alignment from the audit tier with its viewports", async ({ page }) => {
  await page.setContent(fixture("align-drift.html"));
  const r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  const f = r.findings.find((x) => x.rule === "layout.alignment");
  expect(f, JSON.stringify(r.findings)).toBeTruthy();
  expect(f.tier).toBe("audit");
  expect(f.evidence.where.length).toBeGreaterThan(0);
});

test("given the visual rules, Jev is asked whether matching card parts sit at different heights, a yes failing as its own rule", async ({ page }) => {
  await page.setContent(fixture("align-drift.html"));
  const fetch = stubFetch({ p: 0.95, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const asked = fetch.calls.find((c) => c.url.includes("decision-model")).body.questions;
  expect(asked["tell.misaligned-cards"].type).toBe("boolean");
  expect(r.findings.some((f) => f.rule === "tell.misaligned-cards" && f.tier === "jev")).toBe(true);
});

test("given cards aligned at 1280 and 390 px but drifting in a band between, only the width sweep finds it and names the band", async ({ page }) => {
  for (const width of [1280, 390]) {
    await page.setViewportSize({ width, height: 800 });
    await page.setContent(fixture("align-band.html"));
    expect(await page.evaluate(alignmentAudit), `at ${width}`).toEqual([]);
  }
  await page.setContent(fixture("align-band.html"));
  const r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  const f = r.findings.find((x) => x.rule === "layout.alignment");
  expect(f, JSON.stringify(r.findings)).toBeTruthy();
  expect(f.evidence.where.join()).toMatch(/\d+(-\d+)? px/);
});

// Page text that tells the reader how to operate the page. Synthetic sentences, the same
// split as writing-core's gate tests: the page as object, a direction or a reveal goal
// count; product behavior and how-to steps inside a product do not.
const UI_INSTRUCTIONS = [
  "Auf dem Handy lässt sich das Diagramm seitlich wischen.", "Die Tabelle lässt sich auf kleinen Bildschirmen waagerecht scrollen.",
  "Zum Vergrößern auf das Bild tippen.", "Klicken Sie hier, um den Bericht zu öffnen.", "Scrollen Sie nach unten für die Details.",
  "Weitere Zahlen siehe unten.", "Fahren Sie mit der Maus über einen Balken, um den Wert zu sehen.", "Auf dem Smartphone kann man die Grafik seitlich wischen.",
  "On a phone, swipe the diagram sideways.", "Scroll horizontally to see the whole table.", "Tap to zoom.", "Click here for the full report.",
  "Hover over a bar to see its value.", "Scroll down to the results.", "See below for the numbers.", "Click on the image to enlarge it.",
];
const UI_DESCRIPTIONS = [
  "Der Nutzer klickt auf Freigeben, dann startet der Export.", "Die Liste scrollt automatisch zum neuen Eintrag.",
  "Klicken Sie auf Speichern, um den Entwurf zu sichern.", "Bei Klick auf Exportieren erzeugt das System ein PDF.",
  "Das Diagramm zeigt den Ablauf von links nach rechts.", "Die App erkennt Wischgesten und Zoomen mit zwei Fingern.",
  "Der Speicher lässt sich später vergrößern.", "Der Bericht lässt sich als PDF exportieren.",
  "The user clicks Approve and the export starts.", "The list scrolls to the newest item.", "Click Approve to publish the release.",
  "Users swipe left to archive a message.", "Hover states use the accent color.", "Tap targets are at least 44 px.",
  "Scrolling performance improved after the fix.", "The carousel lets shoppers swipe through products.", "See the runbook for the restore steps.",
  'Link text names its target, never "click here".',
];

test("given sentences that tell the reader how to operate the page, the text check finds each; product UI described or instructed stays quiet", () => {
  for (const t of UI_INSTRUCTIONS) expect(uiInstructions([t]), t).toHaveLength(1);
  for (const t of UI_DESCRIPTIONS) expect(uiInstructions([t]), t).toEqual([]);
});

test("given a caption that tells the reader to swipe the diagram, the DOM tier flags it with the sentence and Jev is not asked the text rule", async ({ page }) => {
  await page.setContent(fixture("text-instructions.html"));
  const fetch = stubFetch({ p: 0.05, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const f = r.findings.find((x) => x.rule === "text.ui-instructions");
  expect(f).toMatchObject({ status: "fail", tier: "dom", evidence: { text: "Auf dem Handy lässt sich das Diagramm seitlich wischen." } });
  expect(jevCalls(fetch).some((c) => c.body.questions["text.ui-instructions"])).toBe(false);
});

test("given page text the DOM check passes, Jev is asked the text rule on the visible text without screenshots and a confident no passes it", async ({ page }) => {
  await page.setContent(fixture("clean.html"));
  const fetch = stubFetch({ p: 0.05, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const call = jevCalls(fetch).find((c) => c.body.questions["text.ui-instructions"]);
  expect(Object.keys(call.body.questions)).toEqual(["text.ui-instructions"]);
  expect(call.body.stateParts.some((p) => p.type === "file")).toBe(false);
  expect(JSON.stringify(call.body.stateParts)).toContain("Tides at the north pier");
  expect(jevCalls(fetch).find((c) => c.body.questions["visual.hierarchy"]).body.questions["text.ui-instructions"]).toBeUndefined();
  expect(r.passed).toContain("text.ui-instructions");
});

test("given an unsure Jev answer on the page text, the model decides it from the text alone and its verdict becomes a finding", async ({ page }) => {
  await page.setContent(fixture("clean.html"));
  const fetch = stubFetch({ p: 0.5, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const call = modelCalls(fetch).find((c) => /- text\.ui-instructions:/.test(c.body.messages[0].content[0].text));
  expect(call.images).toBe(0);
  expect(call.body.messages[0].content[0].text).toContain("Tides at the north pier");
  expect(r.findings.find((f) => f.rule === "text.ui-instructions")).toMatchObject({ status: "fail", tier: "llm" });
});

test("given the text rule, its thresholds are the calibrated ones: a how-to step diluted in a long page reached 0.81, so a fail needs 0.85", () => {
  const rule = TEXT_RULES.find((x) => x.id === "text.ui-instructions");
  expect(decide(rule, { probability: 0.81 }).status).toBe("unsure");
  expect(decide(rule, { probability: 0.86 }).status).toBe("fail");
  expect(decide(rule, { probability: 0.33 }).status).toBe("pass");
  expect(decide(rule, { probability: 0.44 }).status).toBe("unsure");
});

test("given only a TypeSafe key, the text question goes without assets or the image opt-in, which Jev rejects when no image is sent", async ({ page }) => {
  await page.setContent(fixture("clean.html"));
  const calls = [];
  const fetch = async (url, init) => {
    const body = JSON.parse(init.body);
    calls.push({ url, body, headers: init.headers });
    const answers = Object.fromEntries(Object.entries(body.questions).map(([id, q]) => [id, q.type === "score" ? { score: 3 } : { probability: 0.05 }]));
    return Response.json({ answers, usage: { input_tokens: 100 } });
  };
  const r = await review(page, { env: { TYPESAFE_API_KEY: "test" }, fetch, outDir: out() });
  const text = calls.find((c) => c.body.questions["text.ui-instructions"]);
  expect(text.body.assets).toBeUndefined();
  expect(text.headers["TypeSafe-Danger-Zone-Images"]).toBeUndefined();
  expect(calls.find((c) => c.body.questions["visual.hierarchy"]).headers["TypeSafe-Danger-Zone-Images"]).toBe("true");
  expect(r.passed).toContain("text.ui-instructions");
});

// Type and layout craft: measured from the DOM in the audit tier, per viewport and scheme.
const craft = async (page, name, rule, width = 1280) => {
  await page.setViewportSize({ width, height: 800 });
  await page.setContent(fixture(name));
  return (await page.evaluate(craftAudit)).filter((f) => f.rule === rule);
};
const widows = async (page, name, width = 1280) => {
  await page.setViewportSize({ width, height: 800 });
  await page.setContent(fixture(name));
  return page.evaluate(widowAudit);
};

test("given text under 12 px, the craft check reports each element with its size; 12 px, display:none and aria-hidden text pass", async ({ page }) => {
  const hits = await craft(page, "type-small-bad.html", "type.small-text");
  expect(hits.map((h) => h.text)).toEqual(["Owner", "Status"]);
  expect(hits[0].observed).toBe("11.2 px");
  expect(hits[0].required).toBe(">= 12 px");
  expect(hits[0].element).toContain("p.l");
  expect(await craft(page, "type-small-ok.html", "type.small-text")).toEqual([]);
});

test("given adjacent font sizes under 10 percent apart that two texts each use, the craft check reports the pair; a size used once or a clear step passes", async ({ page }) => {
  const hits = await craft(page, "type-scale-bad.html", "type.scale-near-duplicate");
  expect(hits.map((h) => h.observed)).toEqual(["12 px (2 texts) and 13 px (2 texts), ratio 1.08", "13 px (2 texts) and 14 px (2 texts), ratio 1.08"]);
  expect(hits[0].text).toBe("Owner / Open");
  expect(hits[0].required).toContain("1.10");
  expect(await craft(page, "type-scale-ok.html", "type.scale-near-duplicate")).toEqual([]);
});

test("given a heading or bold text of 16 px or more whose last line is one word, the widow check reports it; two words, a plain text, small bold text and a one-line heading pass", async ({ page }) => {
  const hits = await widows(page, "type-widow-bad.html");
  expect(hits.map((h) => h.text)).toEqual(["Waiting for the person who filed it.", "Plans for the next quarter", "Bold text that ends alone"]);
  expect(hits[0].observed).toBe('last line is the single word "it."');
  expect(hits[0].rule).toBe("type.widow");
  expect(await widows(page, "type-widow-ok.html")).toEqual([]);
});

test("given text left edges 2 px apart that two texts each share inside one section, the craft check reports them; aligned, deliberately stepped, single stray and centered text pass", async ({ page }) => {
  const hits = await craft(page, "layout-edge-bad.html", "layout.edge-near-miss");
  expect(hits).toHaveLength(1);
  expect(hits[0].observed).toBe("left edges 66 and 68 px, 2 px apart (2 and 2 texts)");
  expect(hits[0].text).toBe("Nothing here.");
  expect(await craft(page, "layout-edge-ok.html", "layout.edge-near-miss")).toEqual([]);
});

test("given more than three rendered font families, the craft check names them; three or fewer pass", async ({ page }) => {
  const hits = await craft(page, "type-families-bad.html", "type.families");
  expect(hits).toHaveLength(1);
  expect(hits[0].observed).toContain("5 font families");
  expect(hits[0].required).toBe("at most 3");
  expect(await craft(page, "type-families-ok.html", "type.families")).toEqual([]);
});

test("given a page with small text, the review reports type.small-text from the audit tier with each viewport and scheme", async ({ page }) => {
  await page.setContent(fixture("type-small-bad.html"));
  const r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  const f = r.findings.find((x) => x.rule === "type.small-text" && x.evidence.text === "Owner");
  expect(f, JSON.stringify(r.findings)).toBeTruthy();
  expect(f.tier).toBe("audit");
  expect(f.evidence.where).toEqual(["1280 light", "1280 dark", "390 light", "390 dark"]);
});

test("given a heading that is alone on its last line only at 360 px, the width sweep finds it and names that band; the screenshot widths alone would not", async ({ page }) => {
  for (const width of [1280, 390]) expect(await widows(page, "type-widow-band.html", width), `at ${width}`).toEqual([]);
  expect(await widows(page, "type-widow-band.html", 360)).toHaveLength(1);
  await page.setContent(fixture("type-widow-band.html"));
  const r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  const f = r.findings.find((x) => x.rule === "type.widow");
  expect(f, JSON.stringify(r.findings)).toBeTruthy();
  expect(f.tier).toBe("audit");
  expect(f.evidence.where).toEqual(["360 px"]);
});

test("given the clean page, the craft and widow checks flag nothing", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.setContent(fixture("clean.html"));
  expect(await page.evaluate(craftAudit)).toEqual([]);
  expect(await page.evaluate(widowAudit)).toEqual([]);
});

// The one visual craft question: sparse only, never cramped. It is asked in its own Jev call:
// its context (rules and labeled examples) pulled every hierarchy score down in a spike, so it
// must not ride in the shared call the other 12 rules were calibrated on.
const PAGE_RULE_IDS = ["visual.hierarchy", "visual.distinct", "tell.hero-cards", "tell.gradient", "tell.emoji-icons", "tell.illustration", "tell.uniform", "tell.slogan", "tell.placeholder", "layout.phone", "layout.dark", "tell.misaligned-cards", "ui.disabled"];
const jevBodies = (fetch) => fetch.calls.filter((c) => c.url.includes("decision-model")).map((c) => c.body);
const pngHeight = (b64) => Buffer.from(b64, "base64").readUInt32BE(20);
const imagesOf = (body) => body.stateParts.filter((p) => p.type === "file").map((p) => p.data.data);

test("given the shared screenshot call, it carries the 13 page rules, the headlines and the three untrimmed shots exactly as before, and nothing about whitespace", async ({ page }) => {
  await page.setContent(fixture("clean.html"));
  const fetch = stubFetch({ p: 0.05, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const shared = jevBodies(fetch).find((b) => "visual.hierarchy" in b.questions);
  expect(Object.keys(shared.questions)).toEqual(PAGE_RULE_IDS);
  expect(VISUAL_RULES.map((x) => x.id)).toEqual(PAGE_RULE_IDS);
  const texts = shared.stateParts.filter((p) => p.type === "text").map((p) => p.text);
  expect(texts).toEqual(['headlines: ["Tides at the north pier"]', "The desktop screenshot (1280 px wide, light):", "The phone screenshot (390 px wide, light):", "The dark screenshot (1280 px wide, dark):"]);
  const files = ["desktop-light", "phone-light", "desktop-dark"].map((n) => readFileSync(r.shots.find((x) => x.name === n).path).toString("base64"));
  expect(imagesOf(shared)).toEqual(files);
  expect(pngHeight(files[0])).toBe(800); // not trimmed
});

test("given the visual rules, tell.sparse is asked alone in its own Jev call with the whitespace rules, a labeled NO and YES example and the trimmed shots, and a confident yes fails as its own rule", async ({ page }) => {
  await page.setContent(fixture("clean.html"));
  const fetch = stubFetch({ p: 0.95, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const calls = jevBodies(fetch).filter((b) => "tell.sparse" in b.questions);
  expect(calls).toHaveLength(1);
  const body = calls[0];
  expect(Object.keys(body.questions)).toEqual(["tell.sparse"]);
  expect(body.questions["tell.sparse"].type).toBe("boolean");
  expect(body.questions["tell.sparse"].instructions).toMatch(/sparse/);
  const parts = body.stateParts.map((p) => p.text ?? "[image]");
  expect(parts.some((t) => /whitespace/i.test(t) && /cramped/i.test(t))).toBe(true);
  const iNo = parts.findIndex((t) => /tell\.sparse example, answer NO/.test(t));
  const iYes = parts.findIndex((t) => /tell\.sparse example, answer YES/.test(t));
  expect(iNo).toBeGreaterThan(-1);
  expect(iYes).toBeGreaterThan(iNo);
  expect(parts[iNo + 1]).toBe("[image]");
  expect(parts[iYes + 1]).toBe("[image]");
  const shots = imagesOf(body).slice(0, 3);
  expect(imagesOf(body)).toHaveLength(5); // 3 trimmed shots, then the two examples
  expect(pngHeight(shots[0])).toBeLessThan(800);
  expect(pngHeight(shots[0])).toBeGreaterThanOrEqual(280);
  expect(r.findings.some((f) => f.rule === "tell.sparse" && f.tier === "jev")).toBe(true);
});

test("given empty space inside the content, the sparse call's shot keeps it; only the blank viewport below the last content is cut, 24 px below it", async ({ page }) => {
  await page.setContent('<body style="margin:0;font:16px Arial"><p>Top</p><div style="height:500px"></div><p>Bottom</p></body>');
  const fetch = stubFetch({ p: 0.05, score: 3 });
  await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const body = jevBodies(fetch).find((b) => "tell.sparse" in b.questions);
  expect(pngHeight(imagesOf(body)[0])).toBeGreaterThan(500);
  expect(pngHeight(imagesOf(body)[0])).toBeLessThan(620);
});

test("given an unsure tell.sparse answer, the model gets the trimmed page screenshots and the whitespace rules, never the examples", async ({ page }) => {
  await page.setContent(fixture("clean.html"));
  const fetch = stubFetch({ p: 0.6, score: 3, fail: false });
  await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const call = modelCalls(fetch).find((c) => /- tell\.sparse:/.test(c.body.messages[0].content[0].text));
  expect(call).toBeTruthy();
  expect(call.body.messages[0].content[0].text).toMatch(/Whitespace rules/);
  const images = call.body.messages[0].content.filter((p) => p.type === "image_url");
  expect(images).toHaveLength(3);
  expect(pngHeight(images[0].image_url.url.split(",")[1])).toBeLessThan(800);
});

test("given a Jev failure on the sparse call, the page rules and the DOM findings still stand", async ({ page }) => {
  await page.setContent(fixture("type-small-bad.html"));
  const inner = stubFetch({ p: 0.05, score: 3 });
  const fetch = async (url, init) => (Object.keys(JSON.parse(init.body).questions || {}).join() === "tell.sparse" ? new Response("boom", { status: 500 }) : inner(url, init));
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  expect(r.tiers.visual).toBe("ran");
  expect(r.tiers.sparse).toMatch(/^failed/);
  expect(r.findings.some((f) => f.rule === "type.small-text")).toBe(true);
});

test("given the text tier, tell.sparse is not part of its questions or of the shared visual rules", () => {
  expect(TEXT_RULES.map((r) => r.id)).not.toContain("tell.sparse");
  expect(VISUAL_RULES.map((r) => r.id)).not.toContain("tell.sparse");
});

test("given the tell.sparse thresholds from the 11-page calibration, 0.82 fails, 0.45 passes, and the 0.53 to 0.63 band that held a real and a noisy page goes to the model", () => {
  expect(decide(SPARSE_RULE, { probability: 0.82 }).status).toBe("fail");
  expect(decide(SPARSE_RULE, { probability: 0.45 }).status).toBe("pass");
  expect(decide(SPARSE_RULE, { probability: 0.53 }).status).toBe("unsure");
  expect(decide(SPARSE_RULE, { probability: 0.63 }).status).toBe("unsure");
});

// Diagram text size: inline SVG is measured exactly, so Jev's flipping answers on 15 px text never decide it.
const svgWith = (px, extra = "") => `<main><figure><svg viewBox="0 0 760 300" ${extra}><rect x="10" y="10" width="740" height="280" fill="#eef" stroke="#333"/><text x="40" y="100" font-size="${px}">Gauge reader</text><text x="40" y="200" font-size="${px}">Tide model</text></svg></figure></main>`;
const FIXED_STYLE = "<style>body,figure{margin:0}svg{display:block}</style>";
const SIZE_STYLE = "<style>body,figure{margin:0}svg{display:block;width:100%;height:auto}</style>";

test("given inline SVG text, its rendered size is the font size times the SVG scale: 15 px labels in a 760 unit viewBox shrink to 7.7 px at 390 px width and stay 15 px at 760", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 800 });
  await page.setContent(SIZE_STYLE + svgWith(15));
  const narrow = await page.locator("svg").evaluate(loop.diagramTextSize);
  expect(narrow.texts).toBe(2);
  expect(narrow.min).toBeGreaterThan(7.5);
  expect(narrow.min).toBeLessThan(7.9);
  await page.setViewportSize({ width: 760, height: 800 });
  const wide = await page.locator("svg").evaluate(loop.diagramTextSize);
  expect(wide.min).toBeGreaterThan(14.5);
  expect(wide.min).toBeLessThan(15.5);
});

test("given a diagram with 9 px labels, the review fails diagram.small-text from the DOM tier even when Jev says no; 15 px labels pass with no verdict from Jev", async ({ page }) => {
  await page.setContent(FIXED_STYLE + svgWith(9, 'width="760" height="300"'));
  let fetch = stubFetch({ p: 0.05, score: 3 });
  let r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const small = r.findings.filter((f) => f.rule === "diagram.small-text");
  expect(small.map((f) => f.tier)).toEqual(["dom"]);
  expect(small[0].evidence.element).toMatch(/Gauge reader|Tide model/);
  expect(small[0].detail).toMatch(/9/);
  await page.setContent(FIXED_STYLE + svgWith(15, 'width="760" height="300"'));
  fetch = stubFetch({ p: 0.95, score: 3 }); // Jev would fail it; the DOM already knows the text is large enough
  r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  expect(r.findings.filter((f) => f.rule === "diagram.small-text")).toEqual([]);
  expect(r.passed).toContain("diagram-1/diagram.small-text");
});

test("given a responsive SVG whose 15 px text renders under 12 px at 390 px, the review fails it, since phones are the house width", async ({ page }) => {
  await page.setContent(SIZE_STYLE + svgWith(25)); // 25 units * 390/760 = 12.8 px passes
  let r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  expect(r.findings.filter((f) => f.rule === "diagram.small-text")).toEqual([]);
  await page.setContent(SIZE_STYLE + svgWith(15));
  r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  expect(r.findings.filter((f) => f.rule === "diagram.small-text").map((f) => f.tier)).toEqual(["dom"]);
});

test("given a canvas diagram, there is no text to measure, so Jev still decides diagram.small-text", async ({ page }) => {
  await page.setContent('<main><canvas id="c" width="600" height="300" style="width:600px;height:300px"></canvas></main><script>const g=document.getElementById("c").getContext("2d");g.fillStyle="#eef";g.fillRect(0,0,600,300);g.fillStyle="#000";g.font="8px Arial";g.fillText("tiny label",20,40)</script>');
  const fetch = stubFetch({ p: 0.95, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  expect(r.findings.filter((f) => f.rule === "diagram.small-text").map((f) => f.tier)).toEqual(["jev"]);
});

test("given labels that render at 11.9 px, the floor of 12 px holds with a half pixel of rounding; 11.4 px fails", async ({ page }) => {
  await page.setContent(FIXED_STYLE + svgWith(11.9, 'width="760" height="300"'));
  let r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  expect(r.findings.filter((f) => f.rule === "diagram.small-text")).toEqual([]);
  await page.setContent(FIXED_STYLE + svgWith(11.4, 'width="760" height="300"'));
  r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  expect(r.findings.filter((f) => f.rule === "diagram.small-text").map((f) => f.tier)).toEqual(["dom"]);
});

test("given the phone question, Jev is told the screenshot ends at an artificial cut of a longer page and that content cut by the bottom edge is not a defect; the other 12 page questions are untouched", async ({ page }) => {
  await page.setContent(fixture("clean.html"));
  const fetch = stubFetch({ p: 0.05, score: 3 });
  await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const q = jevBodies(fetch).find((b) => "visual.hierarchy" in b.questions).questions;
  expect(q["layout.phone"].instructions).toMatch(/top part of a longer page/);
  expect(q["layout.phone"].instructions).toMatch(/ignore anything cut off by the bottom edge/);
  expect(q["layout.dark"].instructions).toBe("Does the dark screenshot show unreadable text, or a mix where some parts turned dark and others stayed light?");
  expect(q["tell.hero-cards"].instructions).toBe("Does the desktop screenshot show a centered hero section followed by a row of three equal feature cards?");
});
