# Harness Currentness and Orchestration Reference

## Principle

Model names, prices, limits, features, and community practices are volatile.
Discover them when they affect a decision. Do not freeze a provider catalog or
price table into agent instructions, Skills, or long-lived context.

## Evidence Order

1. Inspect the live host: version, available tools, model selectors, model
   allowlists, subagent schema, permissions, limits, and configured routing.
2. Check official product documentation, release notes, model catalogs, and
   pricing for the host and provider.
3. Check the organization plan, gateway, residency, privacy, and negotiated
   pricing that actually apply.
4. Use community sources to discover candidates and failure modes.
5. Decide with representative local tasks, evals, spend, latency, and failures.

When evidence conflicts, the live authorized environment determines what can
run; official current documentation determines intended behavior; local evals
determine fitness for this workload.

## Skill Resolution and Public Discovery

Resolve the effective Skill set in this order:

1. inspect the target project's Skills and host-specific precedence
2. inspect workspace, user, and global Skills already available to the host
3. follow an explicit upstream complement named by the selected local Skill
4. when no named complement fits, use an installed upstream
   [`find-skills`](https://www.skills.sh/vercel-labs/skills/find-skills) or
   `npx skills find "<technology> <major-version> <task>"`
5. proceed without a Skill when general capability plus existing checks is the
   smaller reliable path

Before adopting a public Skill:

- derive the technology and version from manifests, lockfiles, runtime output,
  and official documentation
- inspect the exact upstream Skill, repository ownership, license, recent
  maintenance, host compatibility, scripts, tools, permissions, and data access
- check overlap and conflicts with existing Rules, Skills, Hooks, and gates
- treat installs, stars, rankings, and third-party security reports as signals,
  not authority
- test the Skill on one representative task and one near miss

Install project-locally by default when repository harness changes are
authorized. Ask before a global installation, new credentials, broader
permissions, or an external side effect. If the Skill becomes a repeated
dependency, manage an immutable ref and resolved commit through
**update-harness**. Otherwise remove it after the pilot or leave it uninstalled.

## Currentness Record

Capture only fields needed for a durable routing decision:

| Field | Meaning |
|---|---|
| Checked at | Timestamp and reviewer |
| Environment | Host, version, plan, region, gateway, and allowlist |
| Source | Official URL or live command/schema |
| Candidate | Alias or exact model ID and stability status |
| Capability | Tools, context, reasoning, modalities, isolation, and limits |
| Economics | Input, cached input, output, reasoning, tool, platform, and retry cost |
| Evidence | Representative task, quality, latency, token use, retries, and failure detection |
| Decision | Parent, worker class, reviewer, pilot, rejected, or watch |
| Re-check | Expiry or event that invalidates the evidence |

Aliases are useful for current stable behavior. Pin a snapshot only when
reproducibility matters more than automatic upgrades. Never compare input-token
price alone; total cost includes output, caching, tools, retries, review,
latency, and failure impact.

Current does not mean newest preview. Prefer the latest approved stable
candidate that passes local evals; pilot previews behind an explicit fallback.

## Model Lifecycle

Keep the task tiers stable while models and hosts change:

1. **Discover:** a live catalog, allowlist, host release, deprecation, price
   change, or measured failure exposes a candidate.
2. **Pilot:** run representative tasks with the same tools, context, checks,
   retry accounting, and consequence boundary as the current route.
3. **Decide:** promote, retain as fallback, hold, reject, or remove. A newer or
   cheaper model is not automatically better for the completed task.
4. **Observe:** record requested and resolved models, quality, total cost,
   latency, retries, and escaped failures when the host exposes them.
5. **Re-route:** update each active host adapter independently. Do not leave a
   Claude Code, Cursor, Gemini CLI, Codex, Pi, SDK, or CI route stale because a
   different host was updated.

Use rolling family aliases when they intentionally follow the provider's newest
compatible model. Use exact IDs when reproducibility or regulated evidence
requires them. Automatic fallback is acceptable only inside the task's proven
minimum tier; an unverified downgrade stops or re-routes material work.

## Review Triggers

Refresh relevant evidence:

- before introducing model routing or a new agent host
- before expanding permissions, blast radius, repositories, or autonomy level
- when a product decision depends on a changed standard, assessment catalog,
  compliance FAQ, control interpretation, or assurance route
- after a provider, host, gateway, plan, or major client update
- when an instruction, Skill, plugin, Rule, Hook, MCP, permission, isolation,
  or model-routing adapter no longer matches observed host behavior
- when a model is added, deprecated, unavailable, or behavior changes
- when quality, latency, token use, retry rate, or spend crosses its local limit
- when a community Golden Path or tool would change the operating system
- when the locally defined maximum evidence age has expired and a decision or
  active adapter consumes that evidence

Do not run a scheduled research ritual without a consumer. If no decision
depends on the result, wait for an event trigger.

## Parent and Worker Routing

Use a capable current parent for task framing, decomposition, dependency
management, risk routing, integration, and final accountability.

Choose the least expensive worker that passes representative checks:

| Work | Default routing |
|---|---|
| Bounded search, inventory, formatting, or deterministic transformation | Efficient worker with narrow tools and output |
| Isolated implementation with strong tests | Cost-efficient coding worker proven on that task class |
| Ambiguous architecture, product semantics, security, or high coupling | Capable model with human involvement as required |
| Independent review | Fresh context and evidence; use a different model or method when correlated failure matters |
| Final synthesis across workers or repositories | Capable parent with integration and compatibility evidence |

Do not delegate when context transfer, coordination, merge risk, or review cost
is likely to exceed the work. Cap parallelism to the number of independent
workstreams and the environment's safe resource limits.

## Minimum Model Capability

The parent model must be capable enough to frame the task, select the loop,
preserve ownership boundaries, detect uncertainty, integrate results, and
verify completion. A cheap model that creates retries or plausible but
ungrounded output is not economical.

Use current model names only as a dated starting point. Inspect the live host
and official sources before configuration:

| Host | Parent starting point checked 2026-08-03 | Bounded worker policy |
|---|---|---|
| Claude Code | Opus 5 with `high` effort; Fable 5 for long-running or unusually ambiguous work when available | Sonnet 5 or a cheaper model only after the task class passes representative checks |
| Cursor | Auto **Intelligence**; use a manually selected current frontier model when reproducibility matters | Auto **Balance** or **Cost** only for bounded work with checks |
| Codex | GPT-5.6 Sol for complex, open-ended, or high-value integration; use the default effort first and raise it only when evidence requires more | GPT-5.6 Terra for everyday bounded workers and normal review; GPT-5.6 Luna for clear, repeatable, high-volume work; use Sol for material critique when correlated failure or consequence justifies it |
| Gemini CLI | Current Auto or Pro route after checking plan and live model selection | Flash or Flash-Lite for bounded work; set an explicit per-agent model or `modelConfig` when the route must not inherit or vary by built-in agent |

If the named option is unavailable, select the current host-equivalent at the
same capability tier and record the evidence. If no candidate meets the floor,
reduce scope, permissions, or autonomy and keep a human in the loop. Do not
retry the same under-capable model with increasingly elaborate prompts.

## Host Discovery Notes

Instruction-entry baseline checked 2026-08-01:

| Host | Verified repository entry |
|---|---|
| Codex | `AGENTS.md` |
| Cursor | root `AGENTS.md` |
| Pi coding agent | root and ancestor `AGENTS.md` context files |
| Claude Code | `CLAUDE.md`; import `AGENTS.md` with `@AGENTS.md` |
| Gemini CLI | `GEMINI.md`; import `AGENTS.md` with `@AGENTS.md` |
| Google Antigravity | `.agents/rules/*.md`; point a thin rule to `AGENTS.md` |

Treat these as adapters, not independent policy owners. Re-check when a host
changes context discovery, rule precedence, or project-root behavior.

- **Claude Code:** Inspect the current CLI and subagent schema. Official docs
  checked 2026-08-03 support rolling aliases or full IDs in agent frontmatter,
  per-invocation selection, and `CLAUDE_CODE_SUBAGENT_MODEL`, subject to the
  organization allowlist and documented precedence. Verify the resolved model;
  a global environment override can otherwise defeat role-specific routing.
- **Cursor:** Inspect the model selector, Auto behavior, plan usage, background
  or cloud agent controls, and current models/pricing. Official releases checked
  2026-08-03 support custom subagent models and rolling general model names.
  Verify the installed version and resolved model because provider API price and
  Cursor plan consumption are not interchangeable.
- **Codex:** Inspect the current runtime tool schema and available model
  overrides before delegating. Confirm model guidance and the applicable Codex
  rate card; capabilities can differ across app, CLI, API, and workspace plan.
  The Codex subagent guide checked 2026-08-03 supports a project
  `[agents].default_subagent_model`, per-agent model and reasoning overrides,
  and project-scoped `.codex/agents/*.toml` files. Use those controls to keep
  Balanced workers as the default and to make Efficient or Frontier routes
  explicit. Official Codex Speed guidance checked 2026-08-08 describes Fast
  Mode as 1.5x model speed with GPT-5.6 credit consumption at 2.5x the Standard
  rate. Keep Fast Mode off by default. It is a premium service tier, not a
  capability tier, and requires separate evidence that a bounded latency need
  justifies its higher total spend.
- **Gemini CLI or successor:** Inspect current model routing precedence,
  subagent overrides, host migration notices, and the applicable API or plan
  pricing before configuring workers. Official docs checked 2026-08-03 expose
  a per-agent `model` and `agents.overrides.*.modelConfig`. A custom subagent
  defaults to `inherit`; built-in or explicitly overridden agents may route
  differently. Configure the role explicitly when a stable tier matters and
  verify the resolved model.
- **Google Antigravity:** Inspect the current Antigravity product surface in
  use (application, IDE, CLI, or SDK), its instruction and Skill loading,
  customizations, MCP support, agent controls, permissions, and migration
  notices. Do not assume Gemini CLI behavior remains identical.
- **Pi coding agent:** Inspect the current project and user instruction paths,
  Skill and extension loading, tool policy, model registry, session behavior,
  and SDK surface before creating an adapter.
- **CI or durable runtime:** Inspect the actual runner, workload isolation,
  permissions, secrets, cancellation, structured I/O, deterministic gates,
  telemetry, and retained evidence. Evaluate Flue or another framework only
  after the runtime gate in `RUNTIMES.md` passes.

Host-specific configuration belongs in the target repository or environment,
not in this portable Skill.

## Official Source Registry

Checked on 2026-08-03 unless a later date is named above. Re-open at use:

- OpenAI model guidance: <https://developers.openai.com/api/docs/guides/latest-model>
- OpenAI API pricing: <https://openai.com/api/pricing/>
- OpenAI Codex rate card: <https://help.openai.com/en/articles/20001106-codex-rate-card>
- OpenAI Codex speed and Fast Mode: <https://learn.chatgpt.com/docs/agent-configuration/speed>
- OpenAI Codex subagents: <https://learn.chatgpt.com/docs/agent-configuration/subagents>
- OpenAI Codex `AGENTS.md` loader: <https://github.com/openai/codex/blob/main/codex-rs/core/src/agents_md.rs>
- Anthropic model overview: <https://platform.claude.com/docs/en/about-claude/models/overview>
- Anthropic pricing: <https://platform.claude.com/docs/en/about-claude/pricing>
- Claude Code subagents: <https://code.claude.com/docs/en/sub-agents>
- Claude Code changelog: <https://code.claude.com/docs/en/changelog>
- Cursor documentation: <https://cursor.com/docs>
- Cursor subagents: <https://cursor.com/docs/subagents>
- Cursor subagent release: <https://cursor.com/changelog/2-4>
- Cursor rolling subagent aliases: <https://cursor.com/changelog/page/5>
- Cursor CLI instruction loading: <https://docs.cursor.com/en/cli/using>
- Cursor pricing: <https://cursor.com/pricing>
- Cursor changelog: <https://cursor.com/changelog>
- Claude Code project memory and `AGENTS.md` import: <https://code.claude.com/docs/en/memory>
- Gemini API models: <https://ai.google.dev/gemini-api/docs/models>
- Gemini API pricing: <https://ai.google.dev/gemini-api/docs/pricing>
- Gemini CLI context files: <https://geminicli.com/docs/cli/gemini-md/>
- Gemini CLI model routing: <https://geminicli.com/docs/cli/model-routing/>
- Gemini CLI subagents: <https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md>
- Gemini CLI model selection: <https://geminicli.com/docs/cli/model/>
- Gemini CLI release notes: <https://github.com/google-gemini/gemini-cli/blob/main/docs/changelogs/index.md>
- Google Antigravity IDE codelab: <https://codelabs.developers.google.com/getting-started-agy-ide>
- Google Antigravity Skills codelab: <https://codelabs.developers.google.com/getting-started-with-antigravity-skills>
- Google Antigravity repository rules: <https://antigravity.google/docs/ide-rules>
- Pi coding agent repository and MIT license: <https://github.com/earendil-works/pi>
- Pi coding agent context files: <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md#context-files>
- Pi coding agent SDK: <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/sdk.md>
- Flue documentation: <https://flueframework.com/docs/>
- Flue agent guide: <https://flueframework.com/docs/guide/building-agents/>
- Flue Agent API: <https://flueframework.com/docs/api/agent-api/>
- Flue repository and license: <https://github.com/withastro/flue>
- Eve documentation: <https://eve.dev/>
- Eve repository, license, and beta status: <https://github.com/vercel/eve>
- ISO/IEC 27001 current standard and amendments: <https://www.iso.org/standard/27001>
- ENX TISAX downloads and ISA lifecycle: <https://www.enx.com/en-US/TISAX/downloads/>
- PCI SSC PCI DSS document library: <https://www.pcisecuritystandards.org/document_library/?class=pcidss&doc=pci_dss>
- DORA research and capabilities: <https://dora.dev/>
- OpenTelemetry documentation: <https://opentelemetry.io/docs/>
- MCP architecture: <https://modelcontextprotocol.io/docs/learn/architecture>
- MCP current specification: <https://modelcontextprotocol.io/specification/latest>
- Context Mode repository: <https://github.com/mksglu/context-mode>
- RTK repository: <https://github.com/rtk-ai/rtk>
- Headroom repository: <https://github.com/headroomlabs-ai/headroom>
- Headroom proxy documentation:
  <https://headroomlabs-ai.github.io/headroom/proxy/>
- Skills ecosystem: <https://skills.sh/>
- Upstream `find-skills`:
  <https://www.skills.sh/vercel-labs/skills/find-skills>

## Community Golden Path Evaluation

Community repositories are candidate sources, not authority:

- <https://github.com/mattpocock/skills>
- <https://github.com/obra/superpowers>
- <https://github.com/vercel-labs/skills>
- <https://github.com/anthropics/skills>
- <https://github.com/openai/skills>
- <https://github.com/getsentry/skills>
- <https://github.com/DietrichGebert/ponytail>
- <https://github.com/blader/humanizer>

Evaluate a candidate before adoption:

1. Which observed outcome or failure mode does it address?
2. What evidence supports it in a comparable environment?
3. Does the host, standard library, or existing harness already solve it?
4. What permissions, data access, dependencies, and blast radius does it add?
5. What context, coordination, latency, token, and maintenance cost does it add?
6. Does it duplicate or conflict with existing Rules, Skills, Hooks, or gates?
7. Can it be piloted, measured, rolled back, and removed cleanly?
8. Does it fit the current maturity level and human oversight mode?

Choose **adopt**, **bounded pilot**, **watch**, or **reject**. Persist the
decision only when it changes future behavior; do not maintain a news archive.
