// Browser tests for examples/registration: the forms golden path, executed.
// Run: npx playwright test -c skills/design/progressive-forms-interactions/tests
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const ok = (route) => route.fulfill({ status: 201, contentType: "application/json", body: "{}" });

async function fill(page, { name = "Ada Lovelace", email = "ada@example.com", password = "correct horse battery" } = {}) {
  await page.getByLabel("Full name").fill(name);
  await page.getByLabel("Email address").fill(email);
  await page.getByLabel("Password", { exact: true }).fill(password);
}

test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

test("given the empty form, the submit button is enabled and reachable by keyboard", async ({ page }) => {
  const submit = page.getByRole("button", { name: "Create account" });
  await expect(submit).toBeEnabled();
  await expect(submit).not.toHaveAttribute("aria-disabled", "true");
});

test("given an empty submit, an error summary takes focus and links to each field", async ({ page }) => {
  await page.getByRole("button", { name: "Create account" }).click();
  const summary = page.locator("#summary");
  await expect(summary).toBeFocused();
  await expect(summary).toContainText("There is a problem");
  await expect(summary.getByRole("link")).toHaveCount(3);
  await expect(page).toHaveTitle(/^Error: /);
  await expect(page.getByLabel("Email address")).toHaveAttribute("aria-invalid", "true");
});

test("given a summary link, activating it moves focus to the field", async ({ page }) => {
  await page.getByRole("button", { name: "Create account" }).click();
  await page.locator("#summary").getByRole("link", { name: /email/i }).click();
  await expect(page.getByLabel("Email address")).toBeFocused();
});

test("given an invalid email, the message appears on blur, not while focused", async ({ page }) => {
  const email = page.getByLabel("Email address");
  await email.fill("ada@");
  await expect(page.locator("#email-error")).toBeHidden();
  await email.blur();
  await expect(page.locator("#email-error")).toContainText("Enter an email address in the correct format");
});

test("given a field in error, the message clears on the keystroke that fixes it", async ({ page }) => {
  const email = page.getByLabel("Email address");
  await email.fill("ada@");
  await email.blur();
  await email.fill("ada@example.com");
  await expect(page.locator("#email-error")).toBeHidden();
  await expect(email).not.toHaveAttribute("aria-invalid", "true");
});

test("given a failed submit, every entered value is kept", async ({ page }) => {
  await fill(page, { email: "ada@" });
  await page.getByRole("button", { name: "Create account" }).click();
  await expect(page.getByLabel("Full name")).toHaveValue("Ada Lovelace");
  await expect(page.getByLabel("Email address")).toHaveValue("ada@");
});

test("given a valid form, success is announced in a status region", async ({ page }) => {
  await page.route("**/api/register", ok);
  await fill(page);
  await page.getByRole("button", { name: "Create account" }).click();
  await expect(page.getByRole("status")).toContainText("Account created");
});

test("given a double click, the request is sent once and the button stays focusable", async ({ page }) => {
  let calls = 0;
  await page.route("**/api/register", async (route) => {
    calls += 1;
    await new Promise((r) => setTimeout(r, 300));
    await ok(route);
  });
  await fill(page);
  const submit = page.getByRole("button", { name: /Create account|Creating/ });
  await submit.dblclick();
  await expect(submit).toHaveText("Creating account...");
  await expect(submit).toBeEnabled();
  await expect(page.getByRole("status")).toContainText("Account created");
  expect(calls).toBe(1);
});

test("given a server error, the input survives and a retry succeeds", async ({ page }) => {
  let first = true;
  await page.route("**/api/register", (route) => {
    if (first) {
      first = false;
      return route.fulfill({ status: 503, body: "" });
    }
    return ok(route);
  });
  await fill(page);
  await page.getByRole("button", { name: "Create account" }).click();
  await expect(page.locator("#summary")).toContainText("could not create your account");
  await expect(page.getByLabel("Email address")).toHaveValue("ada@example.com");
  await page.getByRole("button", { name: "Create account" }).click();
  await expect(page.getByRole("status")).toContainText("Account created");
});

test("given a timeout, the person is told and can try again", async ({ page }) => {
  await page.route("**/api/register", () => new Promise(() => {}));
  await fill(page);
  await page.getByRole("button", { name: "Create account" }).click();
  await expect(page.locator("#summary")).toContainText("taking too long", { timeout: 8000 });
  await expect(page.getByRole("button", { name: "Create account" })).toBeEnabled();
});

test("given keyboard only, the form can be completed and submitted", async ({ page }) => {
  await page.route("**/api/register", ok);
  await page.keyboard.press("Tab");
  await expect(page.getByLabel("Full name")).toBeFocused();
  await page.keyboard.type("Ada Lovelace");
  await page.keyboard.press("Tab");
  await page.keyboard.type("ada@example.com");
  await page.keyboard.press("Tab");
  await page.keyboard.type("correct horse battery");
  await page.keyboard.press("Enter");
  await expect(page.getByRole("status")).toContainText("Account created");
});

test("given autofill and password managers, fields carry autocomplete tokens and allow paste", async ({ page }) => {
  await expect(page.getByLabel("Full name")).toHaveAttribute("autocomplete", "name");
  await expect(page.getByLabel("Email address")).toHaveAttribute("autocomplete", "email");
  await expect(page.getByLabel("Password", { exact: true })).toHaveAttribute("autocomplete", "new-password");
  await expect(page.getByLabel("Email address")).toHaveAttribute("type", "email");
});

test("given an interruption, a draft survives a reload without the password", async ({ page }) => {
  await fill(page);
  await page.getByLabel("Email address").blur();
  await page.reload();
  await expect(page.getByLabel("Full name")).toHaveValue("Ada Lovelace");
  await expect(page.getByLabel("Email address")).toHaveValue("ada@example.com");
  await expect(page.getByLabel("Password", { exact: true })).toHaveValue("");
});

for (const width of [360, 768, 1280]) {
  test(`given a ${width}px viewport, nothing overflows horizontally`, async ({ page }) => {
    await page.setViewportSize({ width, height: 800 });
    await page.getByRole("button", { name: "Create account" }).click();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(0);
  });
}

test("given the empty and the error state, axe finds no WCAG 2.2 A/AA violations", async ({ page }) => {
  const scan = () => new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]).analyze();
  expect((await scan()).violations).toEqual([]);
  await page.getByRole("button", { name: "Create account" }).click();
  expect((await scan()).violations).toEqual([]);
});
