// Run: npx playwright test -c skills/design/design-review/tests
// The model calls are stubbed: these tests check the tiers and their wiring, not a model.
import { test, expect } from "@playwright/test";
import { readFileSync, mkdtempSync, mkdirSync, writeFileSync, symlinkSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { tellsAudit, alignmentAudit, decide, review, firstJson, loadChromium, checkModel, VISUAL_RULES, DIAGRAM_RULES, diagramAudit } from "../scripts/design-loop.mjs";

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
  const fetch = stubFetch({ p: 0.5, score: 3 });
  const r = await review(page, { env: { AI_GATEWAY_API_KEY: "test" }, fetch, outDir: out() });
  const nouls = VISUAL_RULES.filter((x) => x.type === "noul").length;
  expect(r.escalated).toBe(nouls);
  expect(fetch.calls.filter((c) => c.url.includes("chat/completions"))).toHaveLength(1);
  expect(r.findings.filter((f) => f.tier === "llm")).toHaveLength(nouls);
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
  expect(detailed.calls.filter((c) => c.url.includes("chat/completions"))).toHaveLength(1);
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
  expect(found.map((f) => `${f.rule} ${f.tier}`).sort()).toEqual(["diagram.clipped-text dom", "diagram.line-crossing dom", "diagram.overlap dom", "diagram.small-text jev"]);
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
  const asks = fetch.calls.filter((c) => c.url.includes("chat/completions") && c.body.messages[0].content[0].text.includes("diagram."));
  expect(asks).toHaveLength(1);
  expect(asks[0].body.messages[0].content.filter((p) => p.type === "image_url")).toHaveLength(1);
  const found = r.findings.filter((f) => f.rule.startsWith("diagram."));
  expect(found.map((f) => f.rule).sort()).toEqual(DIAGRAM_RULES.map((x) => x.id).sort());
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

test("given the drifting row, the review reports layout.alignment from the audit tier with its viewports", async ({ page }) => {
  await page.setContent(fixture("align-drift.html"));
  const r = await review(page, { env: {}, fetch: stubFetch(), outDir: out() });
  const f = r.findings.find((x) => x.rule === "layout.alignment");
  expect(f, JSON.stringify(r.findings)).toBeTruthy();
  expect(f.tier).toBe("audit");
  expect(f.evidence.where.length).toBeGreaterThan(0);
});
