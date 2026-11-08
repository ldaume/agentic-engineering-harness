# Agent Instructions

Workspace root. Every repository below has its own `AGENTS.md`; this file
only tells a session where it is and where the shared rules live. The
coordinator is `<coordinator>/`.

## Start

- Know which repository you are in before the first edit. A session opened
  here, at the workspace root, has no repository yet: pick one from
  `<coordinator>/CONTEXT-MAP.md` before changing anything.
- Before substantial work, read `<coordinator>/HARNESS.md` and
  `<coordinator>/SYNC.md` from the coordinator's current default branch, then
  the target repository's own `AGENTS.md`. Repository-local instructions win
  for that repository's product and engineering truth.
- Open another repository only when the map names a relationship to the work
  at hand. No match: stay where you are.

## Boundaries

- This root is not a repository of record. Do not put policy, status, or
  learnings here; they belong in the coordinator or the member that owns them.
- Treat every checkout and worktree this session did not create as someone
  else's live work. Claim yours in `<coordinator>/STATUS.md` when several
  sessions share the workspace.
