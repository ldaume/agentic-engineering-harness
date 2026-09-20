---
name: system-one-routing
description: Routes delegated subagent tasks to a capability tier, effort, and host model, and gates spikes and iteration loops, using a typed System One model (Jev, TypeSafe AI) with a fail-open Balanced default. Use when spawning subagents across Claude Code, Codex, Cursor, or Gemini; deciding effort or model for a worker; judging whether a spike or iteration is ready, should continue, switch, or stop; or ranking candidate work items.
license: MIT
---

# System One Routing

Routes a delegated task to a capability tier (Efficient, Balanced, Frontier),
a reasoning effort, and a live host model, and gates spike and iteration
decisions -- all backed by Jev, a typed "System One" model that answers
calibrated-probability questions instead of generating text. The decision
logic lives in code, not in the model: Jev answers what kind of task this
is, the code maps that to a route, and the calling agent still owns
integration and checks.

## Quickstart: key only, everything else has a default

```bash
export TYPESAFE_API_KEY=sk-...          # or ~/.config/typesafe/api-key
python3 scripts/route-subagent.py --host claude "Rename a variable in one file"
```

That is the entire setup. The built-in host model table already covers
Claude Code, Codex, Cursor, and Gemini CLI; no config file is required. If
`TYPESAFE_API_KEY` is missing, unset, or the API is unreachable, every
script below still runs to completion: it prints the Balanced default (for
example `sonnet` at `medium` effort on Claude Code) and says the router was
unavailable, exit code 0. A consumer that never sets the key still gets a
working, if unrouted, harness -- adopting this Skill cannot break a caller.

## When to route

- Before spawning any subagent, worker, or delegated task: route it first.
- Before a spike: gate the hypothesis (falsifiable, measurable, smallest
  increment, reversible).
- After an iteration: decide continue, switch, or stop from measured
  movement, not from prose.
- When choosing among several candidate iterations or work items: rank them.

## Tier table

| Task class | Capability tier | Effort | Verification |
|---|---|---|---|
| Clear extraction, inventory, or mechanical checks | Efficient | low | deterministic output check or bounded sample |
| Bounded implementation, research, or debugging | Balanced | medium | target checks and behavior evidence |
| Normal independent review | Balanced | high | fresh context, concrete findings, target checks |
| Material critique or consequential integration | Frontier | high or higher only when needed | fresh context, independent evidence, human boundary where required |

Default every subagent to the active host's Balanced route. Do not spend
Frontier on routine workers. Escalate only after a representative failure or
when the documented consequence boundary requires more capability. Total
cost includes retries, review, latency, coordination, and failure impact,
not token price alone.

## Route before you spawn

```bash
python3 scripts/route-subagent.py --host claude "Fix the null check in parseOrder"
```

It answers the task class, ambiguity, consequence, and depth of the task and
maps them to the tier table and the host model table below. **The calling
agent's own model plays no role in the decision**: a frontier parent still
gets an efficient route for mechanical work, and an efficient parent gets a
frontier route for a critique. Take the returned tier and effort unless
`confident` is `false`, in which case the Balanced default applies and the
caller decides. A router outage or a missing key yields the same Balanced
default and says so; it never blocks a spawn.

```json
{
  "host": "claude", "model": "sonnet", "effort": "medium", "tier": "balanced",
  "task_class": "implementation", "confident": true,
  "reasons": ["implementation defaults to balanced at medium effort"]
}
```

`--json` prints the full decision; the plain-text form is a one-line summary
plus reasons. `--context FILE` passes extra state (repo, files, constraints)
as JSON alongside the task text.

## Fail-open, always

Every script in this Skill fails open on any router problem: missing key,
unreachable API, malformed answer, or timeout. The caller always gets a
usable default and an explanation, never a crash or a hang:

- `route-subagent.py` -> Balanced tier, medium effort, `confident: false`.
- `iteration-gate.py hypothesis` -> "ready" is never assumed; it prints
  "gate unavailable" and exits 0 so the caller decides.
- `iteration-gate.py continue` -> same: "gate unavailable", exit 0.
- `iteration-gate.py rank` -> ranking has no code-only fallback (there is no
  default order for arbitrary candidates), so it exits 2 and says why.
- the Claude Code hook (`route-subagent-hook.py`) -> passes the spawn
  through with the Balanced default model and logs the reason.

Never silence this by wrapping calls in a broader try/except that hides the
"router unavailable" reason from the caller; the reason is what tells a
human or agent that the route was not really decided.

## Host model table

A small built-in default (`DEFAULT_HOST_MODELS` in `scripts/route-subagent.py`)
maps each tier to a live model per host, current as of this Skill's last
review:

| Host | Efficient | Balanced | Frontier | Control |
|---|---|---|---|---|
| Claude Code | `haiku` | `sonnet` | `opus` | Agent tool `model` parameter; effort as an instruction in the prompt |
| Codex | `gpt-5.6-luna` | `gpt-5.6-terra` | `gpt-5.6-sol` | `model` plus `model_reasoning_effort`, or `--model` / `-c` |
| Cursor | `composer-2.5` | `cursor-grok-4.6-medium` (`-high` for review) | `cursor-grok-4.6-high` | `--model` on cursor-agent; effort is part of the model ID |
| Gemini CLI | `gemini-flash-lite` | `gemini-flash` | `gemini-pro` | explicit per-agent `model` or `modelConfig`; effort as an instruction in the prompt |

These are dated starting points, not permanent assignments: a new, cheaper,
repriced, deprecated, or changed model earns its place through a
representative pilot on your own tasks, same as any other model choice.
**Never enable a premium speed or service tier** ("Fast", "-fast", a
provider's high-speed tier, or a model name containing `fast`). Every script
here rejects a resolved model whose name contains "fast" and raises instead
of silently downgrading capability for speed.

### Overriding the table (optional)

No config file is required. To change the table, point `--models FILE` (or
set `ROUTE_SUBAGENT_MODELS`) at a JSON file shaped like the default:

```json
{"claude": {"balanced": "your-preferred-sonnet-alias"}}
```

Only the hosts and tiers you name are overridden; everything else keeps the
built-in default. This lets a consumer repin one model without forking the
script or maintaining a full copy of the table.

## Iteration and spike gates

```bash
python3 scripts/iteration-gate.py hypothesis \
  --goal "Reduce checkout drop-off" \
  --hypothesis "A one-field form reduces abandonment" \
  --measure "completion rate over 200 sessions" \
  --increment "ship the one-field variant to 10 percent of traffic"
```

Verdict `ready` (exit 0) or `grill` (exit 3, escalate to a human or a
fresh-context review before building). Checks four criteria as calibrated
probabilities (falsifiable, measurable, smallest increment, reversible) plus
how likely the increment is to teach something decisive; any failing
criterion or low confidence on that last question forces `grill`.

```bash
python3 scripts/iteration-gate.py continue --goal "Reduce checkout drop-off" --log iterations.json
```

`iterations.json` is a list of `{"summary": "...", "measurements": {...},
"checks": {...}}` entries, oldest first. Exit codes: `continue` (0), `switch`
(4, abandon this hypothesis), `stop` (5, ship or park it). **Refuses to call
Jev at all when the latest entry has neither `measurements` nor `checks`**
(exit 6, `no-measurements`): rating "distance to shippable" from prose the
model cannot verify is asking it to rate its own writing, not the work.
Observed on a historical dataset: most iteration state carrying no
measurement was actually infrastructure failure text, and judging it as
"progress" inflated agreement to match a trivial always-say-stop baseline
with zero real discriminative signal. Add a measurement or a check to the
log entry before asking for a verdict.

```bash
python3 scripts/iteration-gate.py rank --candidates items.json --goal "..." --weights 1,1,1,1
```

Ranks by value and urgency minus risk and effort, each scored 0 to 3 by Jev
per candidate; `--weights v,u,r,e` reweights the combination. No fallback
order exists for arbitrary candidates, so an unreachable API exits 2 rather
than printing a fabricated ranking.

Every gate decision is appended as one JSON line to
`~/.harness/jev-iteration-log.jsonl` (timestamp, command, verdict,
confidences, an empty `outcome` field for later evidence) unless
`--no-record` is passed. Treat `continue`/`switch`/`rank` verdicts as
advisory input until your own log of outcomes confirms real agreement with
what actually shipped; treat `grill` and `no-measurements` as acting
immediately, since both check the input rather than predict an outcome.
Never assume a noul threshold is 0.5 -- set it from your own observed
distribution the way `AMBIGUITY_THRESHOLD` (0.8, not 0.5) was set here after
a pilot showed ordinary terse task text scoring 0.3 to 0.75 on "ambiguous".

## Claude Code hook (optional, host-specific)

`scripts/route-subagent-hook.py` is a PreToolUse hook for the Agent tool: it
routes every subagent spawn automatically, rewriting `model` to the routed
alias and prepending a `Routed: model=... effort=...` line plus the router's
`Consider Jev:` brief (the `brief` field: check whether a typed System One
decision fits before writing a classifier, judgment, ranking, gate, or
threshold as an LLM prompt, and report whether Jev was used or why not) so
the child works at the intended effort. Forks, spawns that already carry a
`Routed:` line, and sessions with `CLAUDE_CODE_SUBAGENT_MODEL` set pass
through untouched. Fails open to `sonnet` at `medium` effort and logs the
reason to `~/.claude/hooks/route-subagent.log`.

Install by adding `templates/settings.snippet.json` to your `PreToolUse`
hooks in `settings.json` (project, user, or global scope) and setting
`ROUTE_SUBAGENT_SCRIPT` only if `route-subagent.py` is not installed next to
the hook:

```bash
mkdir -p ~/.claude/hooks
cp scripts/route-subagent.py scripts/route-subagent-hook.py ~/.claude/hooks/
# merge templates/settings.snippet.json into your settings.json PreToolUse array
```

Other hosts translate the same routing decision through their own worker
config (Codex `.codex/agents/*.toml` or `--model`/`model_reasoning_effort`,
Cursor `--model` on `cursor-agent`, Gemini CLI per-agent `model` or
`modelConfig`) instead of a PreToolUse hook, since none of them expose an
equivalent pre-spawn rewrite point as of this Skill's last review.

## Data flow

Jev's direct API has no per-request zero-data-retention switch; task text
and any `--context` you pass leave for TypeSafe AI's processor without a
retention guarantee (their policy states no model is trained on it).
Decide, per your own data-handling policy, whether task descriptions are
safe to send before adopting this Skill in a repository with contractual or
regulatory retention constraints. Do not route tasks containing secrets,
credentials, or content that must never leave the local environment.

## Verify a change to this Skill

```bash
python3 -m unittest discover -s tests
```

Covers `tests/test_route_subagent.py` (tier decisions, host resolution, the
models-file override, fail-open behavior), `tests/test_iteration_gate.py`
(all three gate subcommands, fail-open, the no-measurements refusal), and
`tests/test_route_subagent_hook.py` (the Claude Code PreToolUse hook: fail-open,
fast-route rejection, fork and already-routed pass-through).

Then run the quickstart twice: once with `TYPESAFE_API_KEY` set, once with a
clean `HOME` and no key anywhere, and confirm both exit 0 with a route
printed.
