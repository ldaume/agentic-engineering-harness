---
name: write-a-skill
description: Creates, refactors, packages, and verifies portable Agent Skills. Use when changing SKILL.md, skill descriptions, bundled references or scripts, repository indexes, install behavior, or activation quality across Cursor, Codex, Claude Code, Gemini, and the skills CLI.
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
assuming the active host represents Claude Code, Codex, Cursor, Gemini, Pi,
CI, or a later runtime.

Map existing behavior before choosing a preferred structure. Preserve local
names and packaging unless the task requires a migration.

For a shared library or framework Skill, prefer ownership by that library's
maintainers. Require supported versions, boundaries, representative examples,
and verification commands; target-specific deltas stay in target-local
wrappers.

Grounding is complete when the current invocation surface, consumers,
resources, verification path, and ownership are known.

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

Do not duplicate the description as a metadata trigger list. Use metadata only
for information a real client or repository consumer reads.

## 4. Budget the Information

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

## 5. Write for Execution

- Lead with the action and its purpose.
- Use ordered steps only when order changes correctness.
- End fragile steps with an observable completion criterion.
- Give one default and a short escape hatch instead of an equal-weight menu.
- State the desired behavior positively; reserve prohibitions for hard
  boundaries and pair them with the safe action.
- Cut background knowledge the model already has.
- Remove duplicated, stale, speculative, and behavior-neutral prose.

The body is ready when every line changes activation, execution, verification,
or recovery.

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

Then:

1. Run `python3 scripts/audit-skills.py`.
2. Run the provenance check for new or materially changed Skills.
3. Run an isolated `npx skills add ...` test covering every changed Skill.
4. Exercise the description against realistic positive and near-miss prompts
   when activation behavior changed.
5. Run the Skill on a representative task when its execution behavior changed.
6. Review the result for missed steps, false activation, wasted work, and
   premature completion.
7. Remove temporary install artifacts.

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
