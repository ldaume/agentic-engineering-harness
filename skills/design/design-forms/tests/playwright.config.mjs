// Serves examples/registration over HTTP so fetch and page.route behave as in production.
import { defineConfig, devices } from "@playwright/test";
import { fileURLToPath } from "node:url";

const example = fileURLToPath(new URL("../examples/registration", import.meta.url));

export default defineConfig({
  testDir: ".",
  testMatch: "*.spec.mjs",
  fullyParallel: true,
  reporter: process.env.CI ? "github" : "list",
  use: { baseURL: "http://127.0.0.1:4173", trace: "retain-on-failure" },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: `python3 -m http.server 4173 --bind 127.0.0.1 --directory "${example}"`,
    url: "http://127.0.0.1:4173",
    reuseExistingServer: !process.env.CI,
  },
});
