# Beyond One Repository

The harness in this catalog makes one repository, or a workspace of several
repositories, reliable for agents. In one repository its instructions,
context, checks, and learnings live in that repository, and a session that
starts there has everything it needs. Most work should stay there. This page explains what changes once it cannot, so you can recognize the
moment. [`scaffold-harness`](../skills/engineering/scaffold-harness/SKILL.md)
builds the workspace when you need it.

## Why one repository stops being enough

A product rarely lives in one repository. A frontend consumes an API, a
service shares a contract with another, infrastructure lives apart from the
code it runs. An agent in one of them sees only its own truth. It changes a
contract without knowing who consumes it, repeats a lesson another repository
already learned, or edits a checkout another session is working in. None of
that shows up as an error. It shows up later as drift.

## What a multi-repository harness adds

**A workspace root.** One directory holds the repositories side by side, with
an `AGENTS.md` every session reads first. It names the coordinator and nothing
else, so a session that starts above all repositories still finds the rules.

**A coordinator.** One repository that owns what no single member owns: which
repositories belong together, how they relate, and which checks prove they
still fit. It holds relationships, not member truth. A coordinator that starts
owning members' decisions becomes a second, staler copy of them.

**One context map.** A single inventory of members, their owners, contracts,
and how to reach them, so every session answers "what else does this touch?"
the same way. Two maps disagree within weeks.

**Leases.** Several agent sessions on one machine, or one repository, need to
know which checkout belongs to whom. A lease is a visible claim on a working
copy, so no session deletes or overwrites another's unfinished work. It is
coordination, not a lock: it works because every session reads it. The
coordinator's `STATUS.md` holds them, next to the cross-repository work in
flight.

**Fan-out.** A lesson or rule that applies to every member has to reach every
member in the same loop. Otherwise each repository runs a different version of
the same policy, and the harness quietly stops being one system. Each member
carries the same short snippet that points at the coordinator; the snippet
changes in one place and is refreshed in every member in the same loop.

## What changes for people

The unit you delegate grows from a repository to a workflow and then to a value
stream (levels L5 and L6 in [`LEVELS.md`](./LEVELS.md)). People stop carrying
state between repositories and sessions by hand, and start owning boundaries,
exceptions, and the decisions only they can make. That shift needs evidence at
every step: recovery that has been exercised, checks that catch the failure
they own, and a stop path someone has used.

## What stays yours to build

The templates give a workspace a shared language and shared files; they do
not ship automation. Once a manual sync check repeats - snippet drift between
members, a repository on disk with no map row, an `owner/name` shorthand where
a full remote URL belongs, a lease nobody released - make it the coordinator's
Fast Check. The same holds for routing work to the right model, running gates
in hooks, or widening what agents may do alone: add each when evidence asks
for it, in your own coordinator.

## Where to go from here

Start with one repository and the [`scaffold-harness`](../skills/engineering/scaffold-harness/SKILL.md)
Skill until its loop is boring. When work keeps crossing repositories, rerun it
on the workspace directory (section **Multi-Repository Workspace**). The
levels page shows the path from there. I build and run the upper levels with
teams: [daume.dev](https://daume.dev).
