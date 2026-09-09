# Claude Code activation hooks (template)

Use this when the repository's host list includes Claude Code. On that host a
Skill is selected as a tool from its description against the task at hand, so a
routing rule in `AGENTS.md` competes with the whole instruction chain and often
loses. These hooks put the same routing at the moment of the decision.

Commit them: contributors then get the behavior with the clone rather than from
their own configuration. Keep a user-scope copy for repositories that ship
none, and have that copy return early when a repository-local copy exists, or
both fire and the duplicate output is noise.

Every hook here is non-blocking and silent unless something is actually off.
A hook that speaks on every turn is ignored on the turn that mattered.

## `.claude/settings.json`

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat \"$CLAUDE_PROJECT_DIR/.claude/agent-briefing.md\""
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/completion-gate-reminder.py\""
          }
        ]
      },
      {
        "matcher": "Edit|Write|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/start-gate-reminder.py\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/merge-cleanup-reminder.py\""
          }
        ]
      }
    ]
  }
}
```

## The four moments

| Event | Fires on | Says |
| --- | --- | --- |
| `SessionStart` | every session | the Skill routing table and the rules that do not bend |
| `PreToolUse` `Edit\|Write` | the first file edit of a session | the starting point, when it is wrong |
| `PreToolUse` `Bash` | a `git commit` | the completion gate |
| `PostToolUse` `Bash` | a `gh pr merge` | what is left to clean up |

## What each check looks for

**Starting point**, once per session, keyed by the session id, silent when all
four are fine: editing on the default branch; a tree that was already dirty,
which may be another session's work; a checkout behind the remote default
branch after a fetch; other worktrees, meaning another session may hold one.
Measure "behind" against the remote default rather than `@{upstream}` - a
freshly created task branch has no upstream, which is exactly the case this
check exists for.

**Completion gate**: the repository's own verify commands, including any build
step that the fast check does not cover, plus the rules the repository does not
bend on.

**Cleanup after a merge**: return the checkout to the default branch and
fast-forward it; remove the worktree this session created, because deleting the
branch does not delete the checkout it lived in; never remove a worktree this
session did not create. Left-behind worktrees are what the next session's start
check reports as another session at work.

## Matching commands

Match a command where one actually starts - line start, or after `;`, `&&`,
`|` - not as a substring. `"git commit" in command` also matches an `echo` that
mentions it, and it will fire on the session that writes the hook.
