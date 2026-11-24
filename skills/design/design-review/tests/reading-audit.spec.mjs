// Run: npx playwright test -c skills/design/design-review/tests
import { test, expect } from "@playwright/test";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const audit = readFileSync(fileURLToPath(new URL("../scripts/reading-audit.js", import.meta.url)), "utf8");
const long = "Readable prose keeps the reader moving from one clause to the next without effort. ".repeat(3);

const shell = (body, css = "") => `<!doctype html><meta name="color-scheme" content="light dark"><style>
  body { margin: 0; padding: 16px; font: 18px/1.6 sans-serif; color: #111; background: #fff; }
  @media (prefers-color-scheme: dark) { body { color: #eee; background: #111; } }
  main { max-width: 34rem; } ${css}</style><main>${body}</main>`;

const clean = shell(`<p>${long}</p><ul><li>One item of a list.</li></ul><button style="min-height:44px;min-width:44px;color:inherit;background:transparent;border:1px solid">Go</button>`);

async function run(page, html, { scheme = "light", width = 390, level } = {}) {
  await page.emulateMedia({ colorScheme: scheme });
  await page.setViewportSize({ width, height: 800 });
  await page.setContent(html);
  return page.evaluate(`(${audit})(${JSON.stringify(level ? { level } : {})})`);
}

const none = { contrast: [], fontSize: [], lineHeight: [], lineLength: [], targets: [], overflow: [] };

test("given a clean page, nothing is reported at either level in light and dark", async ({ page }) => {
  for (const level of ["aa", "aaa"]) {
    for (const scheme of ["light", "dark"]) {
      const r = await run(page, clean, { scheme, level });
      expect(r.scheme).toBe(scheme);
      expect(r.level).toBe(level);
      expect(r.findings, JSON.stringify(r.findings)).toEqual(none);
      expect(r.notes).toEqual(none);
    }
  }
});

test("given no level, the audit runs at AA", async ({ page }) => {
  expect((await run(page, clean)).level).toBe("aa");
});

test("given grey text at 4.6:1, AA passes and AAA fails the 7:1 target", async ({ page }) => {
  const html = shell(`<p style="color:#757575">${long}</p>`);
  expect((await run(page, html, { level: "aa" })).findings.contrast).toHaveLength(0);
  const r = await run(page, html, { level: "aaa" });
  expect(r.findings.contrast).toHaveLength(1);
  expect(r.findings.contrast[0].required).toBe(7);
});

test("given grey text at 2.8:1, AA fails the 4.5:1 target", async ({ page }) => {
  const r = await run(page, shell(`<p style="color:#999">${long}</p>`));
  expect(r.findings.contrast).toHaveLength(1);
  expect(r.findings.contrast[0].required).toBe(4.5);
});

test("given a dark-only failure, light passes and dark reports it", async ({ page }) => {
  const html = shell(`<p>${long}</p>`, "@media (prefers-color-scheme: dark) { p { color: #666; } }");
  expect((await run(page, html, { scheme: "light" })).findings.contrast).toHaveLength(0);
  expect((await run(page, html, { scheme: "dark" })).findings.contrast).toHaveLength(1);
});

test("given text over a semi-transparent background, contrast is composited", async ({ page }) => {
  const html = shell(`<p style="color:#444;background:rgba(0,0,0,.8)">${long}</p>`);
  expect((await run(page, html)).findings.contrast).toHaveLength(1);
});

test("given large text at 3.5:1, AA passes (3:1) and AAA fails (4.5:1)", async ({ page }) => {
  const html = shell(`<p style="font-size:24px;color:#848484">Big words here</p>`);
  expect((await run(page, html, { level: "aa" })).findings.contrast).toHaveLength(0);
  expect((await run(page, html, { level: "aaa" })).findings.contrast).toHaveLength(1);
});

test("given list text at line-height 1.45, AA notes it and AAA fails it", async ({ page }) => {
  const html = shell(`<ul><li style="line-height:1.45">Tight list item.</li></ul><dl><dd style="line-height:1.5">Fine.</dd></dl>`);
  const aa = await run(page, html, { level: "aa" });
  expect(aa.findings.lineHeight).toHaveLength(0);
  expect(aa.notes.lineHeight).toHaveLength(1);
  const aaa = await run(page, html, { level: "aaa" });
  expect(aaa.findings.lineHeight[0]).toMatchObject({ element: "li", observed: 1.45, required: 1.5 });
  expect(aaa.notes.lineHeight).toHaveLength(0);
});

test("given 14px body text, AA notes it and AAA fails it", async ({ page }) => {
  const html = shell(`<p style="font-size:14px">Small body text.</p>`);
  expect((await run(page, html, { level: "aa" })).notes.fontSize).toHaveLength(1);
  expect((await run(page, html, { level: "aaa" })).findings.fontSize).toHaveLength(1);
});

test("given a paragraph wider than 75 characters, AA notes it and AAA fails it", async ({ page }) => {
  const html = shell(`<p>${long}</p>`, "main { max-width: 60rem; }");
  const aa = await run(page, html, { width: 1280 });
  expect(aa.findings.lineLength).toHaveLength(0);
  expect(aa.notes.lineLength[0].observed).toBeGreaterThan(75);
  expect((await run(page, html, { width: 1280, level: "aaa" })).findings.lineLength).toHaveLength(1);
});

test("given a 30px button, both levels fail 24px or 44px as set; an inline link is exempt", async ({ page }) => {
  const html = shell(`<p>See <a href="#x">the guide</a> for more.</p><button style="height:30px;width:60px">Tiny</button><button style="height:20px;width:60px">Tinier</button>`);
  const aa = await run(page, html, { level: "aa" });
  expect(aa.findings.targets).toHaveLength(1);
  expect(aa.findings.targets[0]).toMatchObject({ observed: "60x20", required: "at least 24x24 px" });
  expect((await run(page, html, { level: "aaa" })).findings.targets).toHaveLength(2);
});

test("given content wider than 390px, overflow fails at both levels", async ({ page }) => {
  const html = shell(`<div style="width:600px;height:10px"></div>`);
  for (const level of ["aa", "aaa"]) expect((await run(page, html, { level })).findings.overflow).toHaveLength(1);
});

test("given a failing diagram source, it is skipped", async ({ page }) => {
  const r = await run(page, shell(`<pre class="mermaid" style="color:#bbb;font-size:10px">graph TD; A-->B</pre>`), { level: "aaa" });
  expect(r.count).toBe(0);
});

const lineOf = (n) => shell(`<p style="font-family:monospace;overflow-wrap:anywhere;width:${n}ch">${"a".repeat(400)}</p>`, "main { max-width: none; }");

test("given a 78 character line, AAA notes it as above the reading target and does not fail it (1.4.8 allows 80)", async ({ page }) => {
  const r = await run(page, lineOf(78), { width: 1280, level: "aaa" });
  expect(r.findings.lineLength).toHaveLength(0);
  expect(r.notes.lineLength).toHaveLength(1);
  expect(r.notes.lineLength[0]).toMatchObject({ observed: 78, required: "above the 45-75 reading target" });
});

test("given an 85 character line, AAA fails it", async ({ page }) => {
  const r = await run(page, lineOf(85), { width: 1280, level: "aaa" });
  expect(r.findings.lineLength).toHaveLength(1);
  expect(r.findings.lineLength[0]).toMatchObject({ observed: 85, required: "at most 80 characters per line" });
});

const hiddenInput = "position:absolute;width:1px;height:1px;opacity:0;margin:0";

test("given a visually hidden radio inside a 44px label, the label is the target and both levels are clean", async ({ page }) => {
  const html = shell(`<label style="display:inline-block;min-height:44px;min-width:88px;line-height:44px"><input type="radio" name="v" style="${hiddenInput}">Weekly</label>`);
  for (const level of ["aa", "aaa"]) expect((await run(page, html, { level })).findings.targets).toHaveLength(0);
});

test("given a bare 16px checkbox without a label, AA reports it", async ({ page }) => {
  const r = await run(page, shell(`<input type="checkbox" style="width:16px;height:16px;margin:0">`), { level: "aa" });
  expect(r.findings.targets).toHaveLength(1);
  expect(r.findings.targets[0]).toMatchObject({ observed: "16x16", required: "at least 24x24 px" });
});
