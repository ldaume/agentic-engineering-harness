// Run: npx playwright test -c skills/design/design-review/tests
// The model calls are stubbed: these tests check the tiers and their wiring, not a model.
import { test, expect } from "@playwright/test";
import { readFileSync, mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { tellsAudit, decide, review, firstJson, loadChromium, checkModel, VISUAL_RULES } from "../scripts/design-loop.mjs";

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
