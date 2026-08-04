# Public Learnings

This log starts with the public repository candidate. Earlier private
development history is intentionally not reproduced here.

Add an entry only when reproducible evidence from this repository changes how
future work should run. Promote stable rules to the owning Skill, harness file,
test, or workflow instead of duplicating them here.

Use this shape:

```markdown
## YYYY-MM-DD - Short finding

- Signal:
- Evidence:
- Decision or change:
- Re-check trigger:
```

## 2026-08-04 - Consume-only for third-party harnesses

- Signal: Scaffold stewardship told consumer agents to update "this public
  catalog," which would write third-party harness lessons back here.
- Evidence: Owner instruction: other users building harnesses from this
  upstream must not write back; external contribution PRs are not supported.
- Decision or change: Templates and `agent-sync` port only within owned
  authority and forbid write-back to foreign public upstreams including this
  one. `CONTRIBUTING.md` is consume-and-adapt. Maintainer work in this
  repository remains the only supported change path. Bump `agent-sync` to
  1.15.0 and `scaffold-harness` to 1.31.0.
- Re-check trigger: Consumer agent opens a PR here from stewardship; templates
  again point ports at this upstream for non-maintainers.

## 2026-08-04 - Always check portable port after harness changes

- Signal: Stewardship "Port to future harnesses" was soft; consumers could
  leave portable harness lessons only in one live repository.
- Evidence: Coordinator owner instruction that "future harnesses" means this
  public upstream, and every harness change must decide whether a generalized
  portable variant belongs here.
- Decision or change: Strengthen stewardship in `HARNESS.md`, `AGENTS.md`,
  `agent-sync`, and `scaffold-harness` templates: always decide in the same
  loop; port autonomously when portable; ask only when public vs private
  placement is ambiguous or the port would leak private authority. Bump
  `agent-sync` to 1.14.0 and `scaffold-harness` to 1.30.0.
- Re-check trigger: Harness change ships without a same-loop port decision;
  agents ask for confirmation on unambiguous portable ports.
