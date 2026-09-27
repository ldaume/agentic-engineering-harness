import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdirSync, mkdtempSync, rmSync, symlinkSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import { askJev, buildRequest, validateInput } from "../scripts/ask-jev.ts";

const input = {
  state: { change: "Update reusable public harness guidance" },
  questions: {
    portable: { type: "noul", instructions: "Is the method portable?" },
    placement: { type: "options", instructions: "Where should it live?", options: { public: "Reusable method", private: "Local policy" } },
    value: { type: "score", instructions: "How useful is this?", criteria: ["No benefit", "Some benefit", "High benefit"] },
  },
};

test("accepts noul, options, and score without inventing a verdict", () => {
  assert.deepEqual(Object.keys(validateInput(input).questions), ["portable", "placement", "value"]);
  assert.throws(() => validateInput({ ...input, questions: { x: { type: "options", instructions: "Pick", options: { only: "One" } } } }), /at least two/);
});

test("direct request maps options to choice", () => {
  const request = buildRequest(input, "typesafe", "secret");
  const body = JSON.parse(request.init.body);
  assert.equal(body.questions.placement.type, "choice");
  assert.deepEqual(body.questions.placement.criteria, input.questions.placement.options);
  assert.equal(body.questions.portable.type, "noul");
  assert.equal(body.questions.value.type, "score");
  assert.equal(body.model, "jev-latest");
});

test("gateway request maps noul to boolean and keeps choices", () => {
  const request = buildRequest(input, "gateway", "secret");
  const body = JSON.parse(request.init.body);
  assert.equal(body.questions.portable.type, "boolean");
  assert.equal(body.questions.placement.type, "choice");
  assert.equal(request.init.headers["ai-model-id"], "typesafe-ai/jev");
});

test("returns Jev answers and preserves model and backend identity", async () => {
  const response = { ok: true, json: async () => ({ model: "jev-1.13.0", answers: {
    portable: { type: "noul", noul: 0.82 },
    placement: { type: "choice", choice: "public", probabilities: { public: 0.75, private: 0.25 } },
    value: { type: "score", score: 1.4 },
  }, usage: { input_tokens: 100 } }) };
  const result = await askJev(input, { backend: "typesafe", key: "secret" }, async () => response);
  assert.equal(result.status, "answered");
  assert.equal(result.model, "jev-1.13.0");
  assert.equal(result.answers.placement.choice, "public");
});

test("normalizes gateway boolean answers", async () => {
  const response = { ok: true, json: async () => ({ answers: {
    portable: { type: "boolean", probability: 0.6 },
    placement: { type: "choice", choice: "private", probabilities: { public: 0.4, private: 0.6 } },
    value: { type: "score", score: 1.2 },
  }, providerMetadata: { typesafe: { confidence: { placement: 0.8 } } } }) };
  const result = await askJev(input, { backend: "gateway", key: "secret" }, async () => response);
  assert.equal(result.status, "answered");
  assert.equal(result.answers.portable.probability, 0.6);
  assert.equal(result.answers.placement.confidence, 0.8);
});

test("network failure is unavailable, never a synthetic answer", async () => {
  const result = await askJev(input, { backend: "typesafe", key: "secret" }, async () => { throw new TypeError("fetch failed"); });
  assert.deepEqual(result, { status: "unavailable", backend: "typesafe", reason: "network_error", message: "Jev request failed; check network access and retry." });
  assert.equal("answers" in result, false);
});

test("malformed remote response is unavailable", async () => {
  const result = await askJev(input, { backend: "typesafe", key: "secret" }, async () => ({ ok: true, json: async () => ({ answers: {} }) }));
  assert.equal(result.status, "unavailable");
  assert.equal(result.reason, "invalid_response");
});

test("rejects incomplete option distributions and out-of-range scores", async () => {
  const missingOption = { ok: true, json: async () => ({ answers: {
    portable: { noul: 0.5 }, placement: { choice: "public", probabilities: { public: 1 } }, value: { score: 1 },
  } }) };
  const badScore = { ok: true, json: async () => ({ answers: {
    portable: { noul: 0.5 }, placement: { choice: "public", probabilities: { public: 0.8, private: 0.2 } }, value: { score: 9 },
  } }) };
  assert.equal((await askJev(input, { backend: "typesafe", key: "secret" }, async () => missingOption)).reason, "invalid_response");
  assert.equal((await askJev(input, { backend: "typesafe", key: "secret" }, async () => badScore)).reason, "invalid_response");
});

test("HTTP rejection exposes status but not response body or key", async () => {
  const result = await askJev(input, { backend: "typesafe", key: "secret" }, async () => ({ ok: false, status: 401 }));
  assert.equal(result.reason, "http_401");
  assert.equal(JSON.stringify(result).includes("secret"), false);
});

test("CLI exits 2 with no credentials and no fabricated answer", () => {
  const home = mkdtempSync(join(tmpdir(), "ask-jev-test-"));
  try {
    const skill = join(home, "skill");
    mkdirSync(join(skill, "scripts"), { recursive: true });
    mkdirSync(join(skill, "examples"));
    copyFileSync(fileURLToPath(new URL("../scripts/ask-jev.ts", import.meta.url)), join(skill, "scripts/ask-jev.ts"));
    copyFileSync(fileURLToPath(new URL("../examples/public-harness-question.json", import.meta.url)), join(skill, "examples/question.json"));
    copyFileSync(fileURLToPath(new URL("../package.json", import.meta.url)), join(skill, "package.json"));
    symlinkSync(join(skill, "scripts/ask-jev.ts"), join(home, "ask-jev.ts"));
    const env = Object.fromEntries(Object.entries(process.env).filter(([name]) =>
      !["TYPESAFE_API_KEY", "VERCEL_AI_GATEWAY_API_KEY"].includes(name)));
    const result = spawnSync(process.execPath, [join(home, "ask-jev.ts"), join(skill, "examples/question.json")],
    { env: { ...env, HOME: home, JEV_BACKEND: "typesafe" }, encoding: "utf8" });
    assert.equal(result.status, 2);
    assert.equal(JSON.parse(result.stdout).status, "unavailable");
    assert.equal("answers" in JSON.parse(result.stdout), false);
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});
