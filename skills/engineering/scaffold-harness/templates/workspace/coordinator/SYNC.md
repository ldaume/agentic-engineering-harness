# Sync

How the repositories in this workspace stay one system: where work opens, how
a repository joins, how a shared rule reaches every member, and where lessons
go. The coordinator owns relationships and shared rules, never a member's
product truth; a coordinator that starts deciding for members becomes a second,
staler copy of them.

## Working root

| Work | Open |
|---|---|
| A change to one member's product, code, or checks | that member |
| Membership, shared rules, cross-repository status | this coordinator |
| A contract change between two members | the provider first, then each consumer named in `CONTEXT-MAP.md` |
| Unclear owner | this coordinator to find the owner, then switch |

## Discovery

Every member's `AGENTS.md` carries the section in `MEMBER-SNIPPET.md`, so a
session started in any member finds this coordinator and reads `HARNESS.md`
and this file before substantial work. The workspace root `AGENTS.md` does the
same for a session started above all repositories. Session discovery does not
grant autonomy; each member's operating level stays its own.

## Admit a member

1. Agree the name, remote host, and visibility with the owner before creating
   anything. Default to private; publishing cannot be undone.
2. Run `scaffold-harness` inside the new repository, so it gets its own
   `AGENTS.md` and names its real Fast Check. Do not invent a check that does
   not exist yet; an invented check reports green for nothing.
3. Add its row to `CONTEXT-MAP.md` as `experimental`, and any relationship it
   has with an existing member.
4. Paste `MEMBER-SNIPPET.md` into its `AGENTS.md`.
5. Set the row to `active` once it has a remote (or `local / no remote` by
   choice), a Fast Check, and the snippet.
6. Commit the member and the coordinator separately, so either can be reverted
   alone.

Retire a member by setting its row to `retired` and removing it from every
relationship; delete the row only after nothing references it.

## Sibling awareness

Read `CONTEXT-MAP.md` before choosing another repository. Open a sibling only
when a row, a relationship, or the working-root table above names it for the
work at hand. Do not copy the member list into members; copies drift. When a
repository appears in the workspace without a map row, admit it or ask its
owner; do not work in an unmapped repository as if it were a member.

## Fan-out

| Change | Members to touch | Same loop |
|---|---|---|
| Coordinator rules only (`HARNESS.md`, this file, `STATUS.md`) | none | Members read it through the snippet next session. |
| The snippet or a session entry obligation | every `active` and `experimental` member | Update `MEMBER-SNIPPET.md`, refresh each member's section, run each member's Fast Check. |
| A member-local rule | none | Keep it local until a second member needs the same rule. |

The session that changed the rule owns its fan-out, including after subagent
work, because only that session sees every change. No background process
rewrites members: every change to a member goes through that member's review
path.

Fan-out git hygiene:

1. Branch each member from its current default branch. Never commit fan-out
   onto someone's product work-in-progress branch, where it ships or is lost
   with their unfinished work.
2. Re-apply the snippet after a formatter or hook rewrites it, then re-run the
   check.
3. Integrate each member through its normal review path.

## Write-back

| Lesson | Goes to |
|---|---|
| A fact about one member's product, code, or operations | that member |
| A rule every member follows | coordinator `HARNESS.md`, then fan-out if the snippet changes |
| A relationship, contract, or owner | `CONTEXT-MAP.md` |
| In-flight cross-repository state | `STATUS.md` |
| Evidence that changed how the workspace works | coordinator `LEARNINGS.md` |

Prefer a check over a note when the lesson is a rule: a check applies every
time, a note only when someone reads it. Repeated manual sync - comparing the
snippet across members, finding unmapped repositories, catching an
`owner/name` remote - is the signal to automate it as the coordinator's Fast
Check.
