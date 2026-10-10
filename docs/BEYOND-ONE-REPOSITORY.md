# Beyond One Repository

The harness in this catalog makes one repository reliable for agents: its
instructions, context, checks, and learnings live in that repository, and a
session that starts there has everything it needs. Most work should stay
there. This page explains what changes once it cannot, so you can recognize the
moment; it does not specify how to build it.

## Why one repository stops being enough

A product rarely lives in one repository. A frontend consumes an API, a
service shares a contract with another, infrastructure lives apart from the
code it runs. An agent in one of them sees only its own truth. It changes a
contract without knowing who consumes it, repeats a lesson another repository
already learned, or edits a checkout another session is working in. None of
that shows up as an error. It shows up later as drift.

## What a multi-repository harness adds

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
coordination, not a lock: it works because every session reads it.

**Fan-out.** A lesson or rule that applies to every member has to reach every
member in the same loop. Otherwise each repository runs a different version of
the same policy, and the harness quietly stops being one system.

## What changes for people

The unit you delegate grows from a repository to a workflow and then to a value
stream (levels L5 and L6 in [`LEVELS.md`](./LEVELS.md)). People stop carrying
state between repositories and sessions by hand, and start owning boundaries,
exceptions, and the decisions only they can make. That shift needs evidence at
every step: recovery that has been exercised, checks that catch the failure
they own, and a stop path someone has used.

## Where to go from here

Start with one repository and the [`scaffold-harness`](../skills/engineering/scaffold-harness/SKILL.md)
Skill until its loop is boring. The levels page shows the path from there. I
build and run the multi-repository levels with teams:
[daume.dev](https://daume.dev).
