# Commit Message

A commit answers: what coherent change does this snapshot represent, and,
when not obvious, why.

## Default

Short subject of about 50 characters (hard ceiling 72), imperative mood, no
trailing period; blank line; optional body wrapped at about 72 explaining why,
constraints, consequences. The first paragraph is used as the title in many
tools.

Inspect the staged diff and the repository's recent `git log` first. Use
Conventional Commits only when the repository already uses them or asks for
them; do not import a format religion. Use the repository's language for
the message. Mention files only when the file is the meaningful change.

## House pattern

```text
Add audit export permission check

Reject export requests before creating a job when the caller lacks the
existing audit-data permission. This keeps failed requests out of the
export queue and makes authorization behavior consistent with audit view.
```

## Golden examples

<!-- golden: commit de -->
```text
Audit-Berechtigung vor Export prüfen

Ungültige Anfragen werden jetzt abgelehnt, bevor ein Export-Job entsteht.
Damit bleibt die Queue frei von nicht autorisierten Jobs.
```

<!-- golden: commit en -->
```text
Check audit permission before export

Reject unauthorized requests before creating an export job. This keeps
invalid work out of the queue and aligns export access with audit viewing.
```

Checks: coherent change, meaningful subject, body when the reason is not
obvious. Reject generic subjects such as "update stuff", "fixes", "changes".
