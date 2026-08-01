# Contributing

I welcome focused changes that improve a real workflow, remove ambiguity, or
add a capability backed by repeatable use.

## Before changing a Skill

1. Open an issue or discussion for a new Skill, major behavior change, or
   overlapping workflow. Small corrections can go straight to a pull request.
2. Read `AGENTS.md`, `VOICE.md`, `VERSIONING.md`, the target `SKILL.md`, and
   `skills/engineering/write-a-skill/SKILL.md`.
3. Keep the method reusable, or make the technology boundary explicit. Do not
   add language or framework coverage without real examples, checks, and a
   maintenance path.
4. Preserve original authorship and licensing. Reference an upstream Skill
   instead of copying it into this repository.

## Pull requests

- Explain the observed problem and the behavior that changes.
- Keep one coherent concern per pull request.
- Update the changed Skill's version when `VERSIONING.md` requires it.
- Run `python3 scripts/audit-skills.py`.
- For a new or materially changed Skill, include provenance and install-test
  evidence.
- Write persistent artifacts in US English with ASCII punctuation.

AI assistance is welcome, but the submitting human must understand, review,
and take responsibility for the contribution. Do not list an AI system as an
author or co-author in commit metadata or trailers. Legitimate human
co-authorship remains welcome.

Be direct and respectful. Critique behavior, evidence, and system effects, not
people. A separate code-of-conduct document can be added if community scale
shows that this compact rule is insufficient.
