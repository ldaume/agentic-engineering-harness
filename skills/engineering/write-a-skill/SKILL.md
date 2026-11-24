---
name: write-a-skill
description: Creates, refactors, packages, and verifies portable Agent Skills. Use when changing SKILL.md, skill descriptions, bundled references or scripts, repository indexes, install behavior, or activation quality across Claude Code, Codex, Cursor, Antigravity or Gemini CLI, pi, and the skills CLI.
license: MIT
metadata:
  vocabulary: house
---

# Write A Skill

A useful Skill narrows execution variance for a recurring class of work. Keep
the contract small, observable, and portable.

This Skill owns the portable authoring workflow. A host-bundled creator,
scaffolder, command, or plugin may add native metadata or validation after this
contract is established; it never replaces the portable owner.

## 1. Ground the Repository

Read the repository instructions, root and category indexes, lockfile, target
`SKILL.md`, and its directly referenced resources. Detect the install targets,
validation commands, naming conventions, and public-source policy.

Identify every agent host that must discover or execute the Skill. Inspect its
effective project, user, global, bundled, and plugin scopes rather than
assuming the active host represents Claude Code, Codex, Cursor, Antigravity
or Gemini CLI, pi, CI, or a later runtime.

Before creating a new Skill, use `update-harness` to check project, bundled,
and plugin owners and public candidates. Create only when no suitable owned
capability exists and repeated work supplies real examples and checks. Complete
a one-off task directly, even when it is difficult or risky. Use a local
wrapper instead of a fork when only target semantics differ.

Map existing behavior before choosing a preferred structure. Preserve local
names and packaging unless the task requires a migration.

For a shared library or framework Skill, prefer ownership by that library's
maintainers. Require supported versions, boundaries, representative examples,
and verification commands; target-specific deltas stay in target-local
wrappers.

Grounding is complete when the current invocation surface, consumers,
resources, verification path, ownership, and creation evidence are known.

## 2. Define the Behavior Contract

Write down:

- the recurring task or failure mode the Skill changes
- realistic prompts that should activate it
- near-miss prompts that should not activate it
- the observable behavior that differs from an unassisted agent
- the completion signal for every fragile phase

Use one coherent Skill when the branches share the same activation and common
procedure. Split only when a branch must activate independently or when a
sequence repeatedly closes early because later steps distract from the current
one.

The contract is complete when each branch has one activation reason and a
checkable expected effect.

## 3. Design the Invocation Surface

For portable Skills, `name` and `description` are the discovery contract:

- make `name` specific and stable
- describe both the capability and the user intent that should activate it
- include each distinct trigger branch once
- keep the description concise enough to coexist with the full catalog
- keep client-specific invocation controls in target-local wrappers
- preserve the portable contract when a host offers extra frontmatter,
  commands, UI metadata, or a native creator

**Hard limits.** The portable `SKILL.md` carries only the six spec fields:
`name` (at most 64 characters of `a-z`, `0-9` and `-`, no leading or trailing
hyphen, equal to the directory name), `description` (1 to 1024 characters),
and optionally `license`, `compatibility` (at most 500 characters), `metadata`
and `allowed-tools`. claude.ai uploads and the Skills API reject any other
field, so a host-only field such as Claude Code's `when_to_use`, `paths` or
`disable-model-invocation` goes into a target-local copy, never the portable
file. Write the description in the third person, without XML tags, and keep
`claude` and `anthropic` out of the name.

**The listing is a shared budget.** Every installed Skill competes for one
listing: Claude Code gives it about 1% of the context window and, on
overflow, drops the descriptions of the least-invoked Skills while keeping
their names; it also cuts `description` plus `when_to_use` at 1,536
characters. Codex starts with about 2% of the context (8,000 characters when
the window is unknown) and shortens descriptions first. So:

- put the trigger in the first sentence, in about 150 characters of task
  words, because that is what survives shortening; a "Use whenever ..." opening
  is fine, capitals and shouting are not
- aim for about 350 characters and stay under about 500; a long description
  costs every other Skill its place in the listing
- name the closest neighbouring Skill and what is left to it ("Not for X;
  `other-skill` owns it"); naming neighbours measurably improves selection
  among similar Skills, and selection collapses when similar Skills crowd
- after adding or growing a Skill, check the live listing on the target host
  (Claude Code: `/context` and `/skill-doctor`) and confirm it still shows
  with its description

**Host discovery differs.** Codex, Antigravity or Gemini CLI, and pi read
`.agents/skills` (project, walking up the tree) and `~/.agents/skills`; pi
does not load a Skill without a description. Claude Code reads
`.claude/skills` and `~/.claude/skills` and does not scan `.agents/skills`,
so a shared catalog reaches it through symlinks or an installer. Check the
target host's docs before assuming a path.

Do not duplicate the description as a metadata trigger list. Use metadata only
for information a real client or repository consumer reads.

**Activation is host-shaped, and installed is not used.** Hosts differ in what
actually triggers behavior, and most Skills are installed on their own, with no
instruction file and no harness around them. Then the description is the only
thing that decides, every time. Where a project does carry an instruction file,
a host that reads such files as behavior will follow a rule naming the Skill;
a host that instead selects a Skill as a tool from its name and description
against the task at hand leaves that rule competing with the whole file, and it
can lose silently: an observed session with the Skill installed, the routing
rule in context, and a matching task loaded no Skill at all across dozens of
tool calls. Nothing errors when this happens, and the transcript looks like a
session that simply chose not to.

Design for the bare case, where nothing but the description is present. Make it
carry the trigger on its own, in the vocabulary of the task rather than of the
method, so selection never depends on a rule being read or remembered. A host
that supports hooks or an equivalent can additionally put the routing at the
moment of the decision - that is a few lines of host configuration, not a
harness. Either way it stays out of the portable Skill: the description is
the contract, the host wiring is target-local.

## 4. Budget the Information

First decide whether it is a Skill at all. Knowledge an agent needs on almost
every task (a house rule, a command, a map of the repository) belongs in a
compressed index in the always-loaded instruction file (`AGENTS.md`,
`CLAUDE.md`, `GEMINI.md`): a Skill is chosen per task and is skipped often
enough that a rule needed every time loses. A procedure needed only sometimes
belongs in a Skill. A rule that must hold every time, whatever the agent
decides, belongs in a hook or a check.

Keep the body under about 500 lines and 5,000 tokens, and put the standing
rules (the ones that apply to the whole task) in the first screen: after
compaction Claude Code re-attaches only the first 5,000 tokens of an invoked
Skill and never re-reads the file. Keep references one level deep, and give a
reference over 100 lines a table of contents.

Keep in `SKILL.md`:

- the common procedure every activation needs
- defaults that prevent meaningful variance
- non-obvious guardrails needed before the risky action
- completion and stop conditions

Put conditional reference behind a pointer that states exactly when to load it.
Use bundled scripts for deterministic validation, transformation, or
scaffolding that an agent would otherwise regenerate.

Prefer one directly referenced resource over a chain of references. Keep
templates and examples out of the common path when only one branch needs them.

## 4a. Name the Expert Vocabulary

A Skill that judges quality (a review, audit, gate, or craft standard) names
each defect in the terms its field's practitioners use, because a defect named
that way, with something a reader can see, is one the author can fix and a
check can later catch; "feels off" is neither.

- Keep the terms in `references/vocabulary.md`, one table row per term:
  `| Term | Definition | Source | Marker | Check |`, definitions in your own
  words.
- Admit a term only with a primary source registered in the family's
  `references/sources.json` (with `accessed` and `revisit`) and an observable
  marker. No marker, no term: a term nobody can observe turns review back
  into taste.
- Take sources from active practitioners and maintained references whose
  current work sets practice; fame alone does not qualify. List retired or
  disproven rules (the three-click rule, "the fold") under "Not admitted"
  with the reason, so the next author does not add them back.
- Check is `exact` (DOM, file, or geometry), `jev` (a typed question), or
  `judge`. Name the rule id of an `exact` row once a check script ships it; a
  row without one is the backlog for the next check.
- Stay under 40 terms and 80 lines, and load the file through one pointer at
  the judging step, because it costs context only when it is used. A family
  keeps one vocabulary; its other Skills point to it instead of copying it.
- A vendor-tool or house-process Skill has no field vocabulary of its own:
  declare `metadata.vocabulary: vendor` or `house` in the frontmatter.

## 5. Write for Execution

- Lead with the action and its purpose.
- Give every rule, default, and step its why: what goes wrong without it, or
  what it protects. An agent that knows the reason applies the rule to the
  case the text did not foresee; one that only knows the rule guesses, or
  follows it where it no longer fits. One clause is usually enough ("because
  titles are written by whoever sent the invite"); a reason that would take a
  paragraph belongs in a referenced file.
- Use ordered steps only when order changes correctness.
- End fragile steps with an observable completion criterion.
- Give one default and a short escape hatch instead of an equal-weight menu.
- State the desired behavior positively; reserve prohibitions for hard
  boundaries and pair them with the safe action.
- Cut background knowledge the model already has.
- Use one term per concept throughout, and leave out time-sensitive text
  ("as of this month"); a dated fact goes into a referenced file with its
  date.
- Ask for an outcome, not for reasoning in a fixed or verbatim format; some
  models refuse to reproduce their reasoning, and the format adds nothing the
  outcome check does not.
- Remove duplicated, stale, speculative, and behavior-neutral prose.

The body is ready when every line changes activation, execution, verification,
or recovery, and every rule in it says why it exists.

## 6. Protect Provenance

Before porting content:

1. Compare it with globally installed and public Skills.
2. Exclude exact or lightly edited public copies from this repository.
3. Prefer installing the upstream Skill when it already owns the behavior.
4. Create an original wrapper only for a real local delta, and keep the
   attribution and dependency explicit.
5. Keep target-specific facts in the target repository.

For catalog work, compare against current checkouts of relevant public sources:

```bash
python3 scripts/audit-skill-provenance.py \
  /path/to/public-skills-repo [...]
```

Treat the similarity check as a guardrail, not as proof that unattributed
copying is acceptable.

## 7. Integrate and Verify

When adding, renaming, or moving a Skill, update its category README, the root
README, and `skills-lock.json`.

Give a new Skill a `license` field in its frontmatter, and add one to an
existing Skill whenever it is being changed for another reason. A Skill is
copied out of its catalog far more often than it is installed from it, and the
repository `LICENSE` does not travel with a single directory. Not a reason for
a pass over every file: in a catalog with pinned tiers, touching every Skill
costs a version, a tag, a release and a re-pin each, which buys nothing for
readers who already have the repository.

Then:

1. Run `python3 scripts/audit-skills.py`, and
   `python3 scripts/check-knowledge.py --vocabulary` where the catalog ships
   it (`--root DIR` for another catalog, such as a private one): the changed
   Skill's vocabulary passes with no errors, or it carries a pointer or an
   exemption.
2. Run the provenance check for new or materially changed Skills.
3. Run an isolated `npx skills add ...` test covering every changed Skill.
4. When activation behavior changed, run a trigger eval: about 20 realistic
   prompts, half of them near-misses that a neighbouring Skill or no Skill
   should take, each run 3 times in a fresh session, with a held-out part you
   do not tune the description against. Record the result before the change
   too, so a drop is visible.
5. When execution behavior changed, run a representative task three ways:
   without the Skill (the RED baseline that shows the failure it fixes),
   with a one-line instruction instead of the Skill (the no-guidance
   control), and with the Skill. Keep the Skill only for the difference it
   makes over both; a Skill that does not beat the control is cost.
6. Review the result for missed steps, false activation, wasted work, a rule
   whose reason is missing or wrong, and
   premature completion.
7. Confirm the Skill was actually loaded on each declared host, not merely
   installed and plausible. A Skill nobody activates is indistinguishable from
   one that does not exist, and only a real session shows the difference.
8. Remove temporary install artifacts.

The change is complete when repository validation passes, installation works,
every declared host resolves the intended owner without collision, and
fresh-context evidence supports the intended activation and behavior.

## Sources and Complements

- Follow the current
  [Agent Skills specification](https://agentskills.io/specification) for the
  portable format.
- If the upstream
  [`writing-great-skills`](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills)
  Skill is installed and compatible with the active host, use it as an
  optional conceptual review for predictability, information hierarchy,
  completion criteria, and pruning. Reference or install it; do not vendor its
  text or make its host-specific invocation metadata part of the portable
  contract.
