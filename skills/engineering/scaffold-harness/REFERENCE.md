# Harness Target-State Reference

## Principle

An ideal harness is the smallest system that gives an agent enough context,
capability, feedback, and governance to change the intended system safely.
Higher delegation is useful only when the lower level is reliable.

## Operating Stance

- Optimize the whole work system, not a prompt, model, or tool in isolation.
- Use the lowest delegation level that solves the real problem reliably.
- Context, changeability, feedback, recovery, and decision rights matter more
  than a small benchmark advantage.
- Skills and automation support understood workflows; they do not replace
  understanding cause, effect, ownership, or artifact contents.
- Prefer native controls and the smallest reversible mechanism. Evaluate every
  candidate by utility, evidence, blast radius, maintenance, cognitive load,
  and removal cost.
- Let agent-facing systems be agent-native. Their structure may differ from a
  human-crafted handbook when machine routing, explicit contracts, progressive
  disclosure, or deterministic checks improve reliability.
- Communicate with each human in their preferred collaboration language, while
  keeping persistent repository artifacts in US English unless a named
  artifact is explicitly requested in another language. Personal preferences
  belong in user-scoped or untracked state unless they are shared policy.
- Keep canonical semantics host-neutral and map them through thin, verified
  adapters for the coding host or runtime actually in use. Native plugins,
  Skills, Rules, Hooks, MCP, permissions, and CI controls are adapters, not
  independent policy owners.
- Use root `AGENTS.md` as the portable owner. The baseline bridges are a
  `CLAUDE.md` import, a `GEMINI.md` import, and an Antigravity repository rule;
  Codex, Cursor, and Pi load `AGENTS.md` directly. Non-interactive adapters
  must explicitly load the owner and prove it in a representative workload.
- Keep human review surfaces legible while the workflow is human-in-the-loop.
  Agent-native does not mean opaque.
- Currentness is part of correctness. Volatile model, pricing, platform,
  security, and community claims need a source, check date, and re-check trigger.
- Context architecture makes authority, freshness, locality, activation, and
  persistence explicit before context economy optimizes successful-task cost,
  latency, and risk.
- Treat product engineering as pull-based domain and risk learning from signal
  through production evidence. Specifications, tests, security, operability,
  and deployment are feedback activities, not downstream departments.
- Represent repeatable deterministic state as versioned code or structured
  configuration when this makes review, checks, reconciliation, and recovery
  stronger. Keep unresolved meaning and accountable decisions with their named
  owners.

## Artifact Ownership

| Concern | Preferred owner |
|---|---|
| Stable agent behavior, scope, permissions | `AGENTS.md` or local equivalent |
| Domain language and invariants | `GLOSSARY.md` |
| Contexts, sources, and relationships | `CONTEXT-MAP.md` |
| Harness evolution and oversight | `HARNESS.md` |
| Current workflow or engagement state | Status document |
| Accepted consequential trade-off | ADR |
| Durable evidence-backed observation | `LEARNINGS.md` |
| Repeated probabilistic procedure | Skill |
| Scoped behavioral guidance | Rule or agent instruction |
| Deterministic event or enforcement | Hook, CI, test, platform control |
| Grounded external capability | Tool or MCP server |
| Outcome and regression signal | Eval, test, observability |
| Signal-to-outcome product lifecycle | Target product operating system; `run-product-engineering` supplies the procedure |
| Compliance scope, risks, controls, and evidence | Target ISMS or GRC system and named control owners |
| Infrastructure desired state, state backend, and drift | Target infrastructure repository and named platform owners; `manage-infrastructure-as-code` supplies the procedure |
| Executable control policy and tests | Target repository or policy system under the named control owner; `integrate-product-compliance` supplies the procedure |

Use the repository's existing equivalent when it already owns the concern.
Reference owners from consumers instead of copying the same truth.

## Reliable Repository Baseline

A reliable repository-level harness has:

- one concise, discoverable agent instruction entrypoint
- confirmed repository and domain sources
- source routing when more than one context or repository exists
- a real Fast Check for narrow work
- explicit Full Gates before integration
- clear decision rights, trust boundaries, and external-write limits
- Git-backed decisions and learnings, with Git history as the audit,
  comparison, and rollback path
- a documented escalation path
- versioned desired state and executable policy for repeatable infrastructure
  or control changes, with an explicit GitOps, GitOps-near, or bounded IaC
  reconciliation model, protected runtime state, and human-owned semantics
- only the Skills, Rules, Hooks, and tools justified by observed work

## Delegation Levels and Evidence

[MATURITY.md](./MATURITY.md) owns the L1-L7 capability profiles, transition
gates, evidence requirements, and human roles. Load it only when level
assessment, increased autonomy, or changed oversight affects the task.

Evidence belongs in the target or coordinating system, not in this Skills
repository. Add a missing control only when its owner, expected effect, and
verification are explicit. Otherwise retain the lower level and name the
missing evidence.

## Agent-Native Design

Design for system comprehension:

- make canonical sources, scope, permissions, state, and stop conditions
  directly discoverable
- expose real commands and contracts instead of prose approximations
- separate stable context from volatile state and currentness evidence
- prefer structured indexes and references over duplicated narrative
- make deterministic failures machine-readable and actionable
- preserve enough rationale for a human to exercise oversight and veto
- optimize canonical artifacts for agent routing and execution; keep human
  README and reference material as projections rather than the control plane

Do not reproduce human ceremony merely because it is familiar. Preserve
security, accessibility, product quality, maintainability, auditability, and
human accountability even when the implementation shape changes.

## Review Architecture

Use reviews when they can change an action:

| Loop | Trigger | Reviewer | Evidence and action |
|---|---|---|---|
| Work self-review | Significant change before completion | Implementing agent plus deterministic checks | Scope, diff, Fast Check; fix or report |
| Independent review | High coupling, material risk, integration, or weak failure detection | Fresh-context agent, preferably isolated | Findings tied to code, policy, tests, or sources |
| Harness review | Repeated friction, harness change, stale owner, or failed instruction | `agent-sync` or an independent agent | Keep, change, remove, or supersede |
| Currentness review | Volatile fact affects model, cost, feature, tool, or Golden Path choice | Research worker reading current primary sources | Refresh evidence or block the decision |
| Autonomy review | Broader permissions, blast radius, repositories, or oversight mode | Capable parent, independent critic, and human where required | Prove controls or retain the lower level |

Do not require multiple model reviews for trivial, reversible, well-checked
work. Correlated reviewers add cost without independence; change context,
evidence, model family, or review method when independence matters.

## Human Oversight

Keep a human in the loop when intent, semantics, authority, trade-offs, or
material risk remain unresolved.

While a workflow is human-in-the-loop, present each material branch as two or
three options, including no change when meaningful. State evidence, trade-offs,
reversibility, blast radius, and a recommendation. The human may veto any
option; do not execute the dependent branch without explicit acceptance.
Routine reversible maintenance remains autonomous within documented authority.

Propose human-on-the-loop only when:

- scope, ownership, and permissions are explicit
- inputs, outputs, and stop conditions are stable
- tests or evals detect meaningful failure
- state, retry, recovery, and rollback exist where needed
- observability and auditability make intervention possible
- repeated bounded runs provide evidence

Human-on-the-loop supervises outcomes and exceptions. It does not remove
accountability or decision rights.

## Language and Punctuation

Write harness artifacts in US English with plain punctuation (straight
quotes, hyphen `-`, `...`) unless the human explicitly requests another
language for a named artifact. Do not introduce curly or angle quotes,
ellipsis characters, exotic or no-break spaces, invisible format and
direction characters, decorative separators, or the hyphens indistinguishable
from `-` (`U+2010`, `U+2011`, `U+2212`). Do not ban em or en dashes: they are
correct typography, and a gate that calls a considered choice a defect is
wrong more often than it is right. This is not an ASCII-only
rule: natural-language letters in any script, arrows, box drawing, and math
or currency signs stay allowed where they carry meaning. Ban a character only
when its ASCII spelling is strictly better. The rule is about prose, not
design: a separator glyph in rendered markup is a typographic device someone
chose, and rewriting it is a different design, not a correction. A gate can
report it, because it cannot tell a label from a sentence, but an automatic
fix is the wrong instrument there. And a fixer must never corrupt what it
fixes - a straight quote is syntax inside a JSON string, a TypeScript
literal, a YAML scalar, so escape it where the format can be parsed and
treat the rest as a draft the repository's own checks confirm.

## Artifact Test

Before adding an artifact, answer:

1. Which observed problem does it solve?
2. Why is an existing artifact or native control insufficient?
3. Is the behavior probabilistic or deterministic?
4. Who owns the truth?
5. What verifies the expected effect?
6. When should the artifact be removed or superseded?
7. Which source and re-check trigger keep volatile claims current?
8. Does this duplicate or conflict with an installed workflow or style profile?
9. What authority, freshness, standing context load, or output-routing layer
   does it add?

## Agent-Ready Audit

Load this when a repository must work for a person who brings their own coding
agent and none of the author's tools: a new contributor on Claude Code, Codex,
Cursor, or Gemini CLI, with only the clone. It applies equally to a repository
that already has a harness and to one that must stay outside any coordinator;
it adds nothing that ties the repository to one.

Run the checks in order; each one names what the script reports and what an
agent has to judge.

1. **Every entrypoint loads.** Each host must reach `AGENTS.md` from wherever
   a session starts. Claude Code reads `CLAUDE.md`, not `AGENTS.md`, so a root
   without `CLAUDE.md` starts with no rules even when every app has one. Put a
   `CLAUDE.md` containing only `@AGENTS.md` at the root and beside every nested
   `AGENTS.md`. Script: `bridge`.
2. **Repository Skills are visible on every host.** Skills shipped in
   `.agents/skills` are invisible to Claude Code, which reads `.claude/skills`.
   Add one relative symlink per Skill (`.claude/skills/team-review ->
   ../../.agents/skills/team-review`) and a line in the Skills README that a new
   Skill gets its link. Before tracking the links, search the repository's
   automation for code that writes into or refuses `.claude/` paths, since a
   sandbox or packaging rule may reject them. Script: `skill-link`.
3. **No Skill hides behind a built-in.** A Skill named like a host's built-in
   command (`review`, `security-review`, `init`) competes with it. When
   automation or documentation finds the Skill by its name, a rename breaks
   them; name the built-in `/command` in the description and say what this
   Skill does instead. Rename only when `git grep -n <name>` finds no
   reference in code, automation, or documentation. Script:
   `name`, against a dated list of built-ins; extend the list when a host adds
   commands.
4. **Preconditions are stated.** A Skill that needs an MCP tool, a credential,
   or a service says so in its description, together with what a session
   without it does (stop and say which tool is missing, or take a named
   fallback). Judged: read each repository Skill.
5. **Newcomer gotchas are written down.** Collect what a first run trips over
   that no configuration reveals: an access switch a deployed sign-in needs, an
   API allowlist that answers 403 for anything not on it, a seed step, a port
   another service holds. Put each into the `AGENTS.md` of the app it affects.
   Judged: ask the maintainers, read recent onboarding issues.
6. **Unwritten rules have one home.** A rule explained only in conversation
   (for example, that each step in the interface maps onto one state of a core
   lifecycle) goes into the glossary, `GLOSSARY.md`. A `CONTEXT.md` that still
   holds a glossary is the same file under its old name: `git mv` it to
   `GLOSSARY.md`, update its references, and leave a two-line stub. Then sharpen the `AGENTS.md` pointer so it names the case,
   "read the glossary before changing a lifecycle step", because a bare "see
   the glossary" is not followed. Script: prints a note when no glossary
   exists and a rename note for `CONTEXT.md`; write one only for confirmed
   language.
7. **The bare case holds.** An agent with only the repository can follow every
   instruction: each referenced file and command exists, and nothing assumes a
   tool, Skill, path, or service from one person's machine or a private
   coordinator. Script: `missing` and `machine-path`. Judged: every command
   and Skill named in instructions runs or loads from the clone, or the text
   says where to get it.

Done when `scripts/verify-agent-ready.py` exits 0 and a fresh session on a
second host, started at the root with only the clone, finds the rules, the
Skills, and the glossary, and names the first command it would run.
