#!/usr/bin/env node
// Ask typed Jev questions from one JSON file. Node.js 22.18+ runs this TypeScript directly.
import { readFileSync, realpathSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

type Backend = "typesafe" | "gateway";
type Question =
  | { type: "noul"; instructions: string }
  | { type: "options"; instructions: string; options: Record<string, string> }
  | { type: "score"; instructions: string; criteria: string[] };
type Input = { state: Record<string, unknown>; questions: Record<string, Question> };
type Credential = { backend: Backend; key: string };

const scriptDir = dirname(fileURLToPath(import.meta.url));
const skillDir = dirname(scriptDir);
const config = {
  typesafe: { key: "TYPESAFE_API_KEY", file: join(homedir(), ".config/typesafe/api-key"), url: "https://api.typesafe.ai/v1/systemone" },
  gateway: { key: "VERCEL_AI_GATEWAY_API_KEY", file: join(homedir(), ".config/vercel/ai-gateway-key"), url: "https://ai-gateway.vercel.sh/v4/ai/evaluation-model" },
} as const;

function record(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function nonempty(value: unknown): value is string {
  return typeof value === "string" && value.trim().length > 0;
}

export function validateInput(value: unknown): Input {
  if (!record(value) || !record(value.state) || !record(value.questions) || Object.keys(value.questions).length === 0) {
    throw new Error("Input requires a state object and a nonempty questions object.");
  }
  for (const [name, raw] of Object.entries(value.questions)) {
    if (!/^[a-zA-Z][\w-]*$/.test(name) || !record(raw) || !nonempty(raw.instructions)) {
      throw new Error(`Invalid question ${name}: use a simple name and nonempty instructions.`);
    }
    if (raw.type === "noul") continue;
    if (raw.type === "options" && record(raw.options) && Object.keys(raw.options).length >= 2 &&
        Object.entries(raw.options).every(([key, label]) => /^[a-zA-Z][\w-]*$/.test(key) && nonempty(label))) continue;
    if (raw.type === "score" && Array.isArray(raw.criteria) && raw.criteria.length >= 2 && raw.criteria.every(nonempty)) continue;
    throw new Error(`Invalid question ${name}: options need at least two labeled choices; score needs at least two criteria.`);
  }
  return value as Input;
}

function dotenv(): Record<string, string> {
  let content: string;
  try { content = readFileSync(join(skillDir, ".env"), "utf8"); } catch { return {}; }
  const values: Record<string, string> = {};
  for (const line of content.split(/\r?\n/)) {
    const match = line.match(/^\s*([A-Z_]+)=(.*)$/);
    if (match) values[match[1]] = match[2].trim().replace(/^['"]|['"]$/g, "");
  }
  return values;
}

export function loadCredential(): Credential | null {
  const forced = process.env.JEV_BACKEND;
  if (forced && forced !== "typesafe" && forced !== "gateway") throw new Error("JEV_BACKEND must be typesafe or gateway.");
  const order: Backend[] = forced ? [forced as Backend] : ["typesafe", "gateway"];
  const local = dotenv();
  for (const source of [local, process.env]) {
    for (const backend of order) {
      const key = source[config[backend].key];
      if (nonempty(key)) return { backend, key };
    }
  }
  for (const backend of order) {
    try {
      const key = readFileSync(config[backend].file, "utf8").trim();
      if (key) return { backend, key };
    } catch { /* No user-level key file. */ }
  }
  return null;
}

export function buildRequest(input: Input, backend: Backend, key: string) {
  const questions = Object.fromEntries(Object.entries(input.questions).map(([name, question]) => {
    if (question.type === "options") return [name, { type: "choice", instructions: question.instructions, criteria: question.options }];
    if (question.type === "noul" && backend === "gateway") return [name, { ...question, type: "boolean" }];
    return [name, question];
  }));
  const headers: Record<string, string> = { Authorization: `Bearer ${key}`, "Content-Type": "application/json" };
  if (backend === "gateway") {
    Object.assign(headers, {
      "ai-gateway-protocol-version": "0.0.1",
      "ai-evaluation-model-specification-version": "4",
      "ai-model-id": "typesafe-ai/jev",
    });
  }
  return {
    url: config[backend].url,
    init: {
      method: "POST",
      headers,
      body: JSON.stringify({ state: JSON.stringify(input.state), questions, ...(backend === "typesafe" ? { model: "jev-latest" } : {}) }),
      signal: AbortSignal.timeout(10_000),
    },
  };
}

export async function askJev(input: Input, credential: Credential, fetchImpl: typeof fetch = fetch) {
  const { backend, key } = credential;
  let response: Response;
  try {
    const request = buildRequest(input, backend, key);
    response = await fetchImpl(request.url, request.init);
  } catch {
    return { status: "unavailable", backend, reason: "network_error", message: "Jev request failed; check network access and retry." };
  }
  if (!response.ok) {
    return { status: "unavailable", backend, reason: `http_${response.status}`, message: "Jev rejected the request; check credentials and service status." };
  }
  let payload: unknown;
  try { payload = await response.json(); } catch { payload = null; }
  if (!record(payload) || !record(payload.answers)) {
    return { status: "unavailable", backend, reason: "invalid_response", message: "Jev returned an invalid response." };
  }
  const answers: Record<string, unknown> = {};
  for (const [name, question] of Object.entries(input.questions)) {
    const answer = payload.answers[name];
    if (!record(answer)) return { status: "unavailable", backend, reason: "invalid_response", message: "Jev returned an invalid response." };
    const confidence = backend === "gateway" && record(payload.providerMetadata) && record(payload.providerMetadata.typesafe) &&
      record(payload.providerMetadata.typesafe.confidence) ? payload.providerMetadata.typesafe.confidence[name] : answer.confidence;
    if (question.type === "noul") {
      const probability = backend === "gateway" ? answer.probability : answer.noul;
      if (typeof probability !== "number" || probability < 0 || probability > 1) return { status: "unavailable", backend, reason: "invalid_response", message: "Jev returned an invalid response." };
      answers[name] = { type: "noul", probability, confidence };
    } else if (question.type === "options") {
      if (typeof answer.choice !== "string" || !Object.hasOwn(question.options, answer.choice) || !record(answer.probabilities) ||
          Object.keys(answer.probabilities).length !== Object.keys(question.options).length ||
          !Object.keys(question.options).every((key) => Object.hasOwn(answer.probabilities, key)) ||
          !Object.values(answer.probabilities).every((value) => typeof value === "number" && Number.isFinite(value) && value >= 0 && value <= 1)) return { status: "unavailable", backend, reason: "invalid_response", message: "Jev returned an invalid response." };
      answers[name] = { type: "options", choice: answer.choice, probabilities: answer.probabilities, confidence };
    } else {
      if (typeof answer.score !== "number" || !Number.isFinite(answer.score) || answer.score < 0 || answer.score > question.criteria.length - 1) return { status: "unavailable", backend, reason: "invalid_response", message: "Jev returned an invalid response." };
      answers[name] = { type: "score", score: answer.score, confidence };
    }
  }
  return { status: "answered", backend, model: typeof payload.model === "string" ? payload.model : (backend === "gateway" ? "typesafe-ai/jev" : "jev-latest"), answers,
    usage: payload.usage ?? null };
}

async function main() {
  if (process.argv.length !== 3) {
    process.stderr.write("Usage: node scripts/ask-jev.ts QUESTIONS.json\n");
    process.exitCode = 1;
    return;
  }
  let input: Input;
  try { input = validateInput(JSON.parse(readFileSync(resolve(process.argv[2]), "utf8"))); }
  catch (error) {
    process.stderr.write(`Invalid input: ${error instanceof Error ? error.message : "unknown error"}\n`);
    process.exitCode = 1;
    return;
  }
  const credential = loadCredential();
  const result = credential ? await askJev(input, credential) :
    { status: "unavailable", reason: "missing_credentials", message: "Set TYPESAFE_API_KEY or VERCEL_AI_GATEWAY_API_KEY." };
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  if (result.status !== "answered") process.exitCode = 2;
}

if (process.argv[1] && realpathSync(resolve(process.argv[1])) === realpathSync(fileURLToPath(import.meta.url))) {
  main().catch(() => {
    process.stdout.write(`${JSON.stringify({ status: "unavailable", reason: "unexpected_error", message: "Jev request could not complete." })}\n`);
    process.exitCode = 2;
  });
}
