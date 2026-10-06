# Merge Gate

Load this when a session merges a pull request or waits on required checks.

## Rules and reasons

- **Name the required jobs and wait for an explicit pass from each.** A tool
  that treats "no failure line" as green merges red work: right after a push
  the check list is empty or partial, and an empty list contains no failure.
  A job that has not said "pass" has not passed.
- **Green counts only against the current base.** Two branches can each pass
  every job and leave the base red together, because each was green against a
  base the other had already moved. Update a branch that is behind (merge,
  never force-push) and re-check it.
- **A red verdict from an old base is also stale.** The failure may describe a
  tree nobody will merge. Bring the branch forward and ask again; only a
  failure measured against the current base stops the merge.
- **Stalled is not pending.** A branch opened before a job became required
  never runs it on that head, so waiting cannot produce an answer. When every
  reported required job has finished and one is absent, update the branch
  instead of waiting for the timeout.
- **Pass the required names as one explicit list.** Repeated flags are a trap:
  a CLI may silently keep only the last occurrence, so the gate waits for one
  job and merges without the rest. Use one comma-separated value, and give the
  list no default, because a default carries one repository's job names into
  every other repository.
- **Give the host CLI the identifier shape it wants.** A call that fails
  because it got a filesystem path where it wanted `OWNER/NAME` reads like "no
  job has reported yet". Validate the shape before polling, and print what the
  gate could not read instead of waiting in silence.
- **Say the verdict last.** A caller that pipes the output through `tail`
  loses the exit code, so the final line states merged or not merged.
- **Merge on the server only.** Do not ask the CLI to delete local branches
  while another worktree has the head branch checked out. Delete the remote
  branch separately and treat failure there as harmless.

## Background waiters

When several sessions run background waiters on one machine, stop only your
own: by PID, or by a pattern that names your pull request. A broad `pkill`
kills other sessions' waiters and leaves their pull requests unmerged without
a trace.

## Bundled script

[`scripts/merge-if-green.py`](./scripts/merge-if-green.py) implements the
rules above on top of the `gh` CLI. It needs Python 3.9+ and no packages.

```bash
python3 scripts/merge-if-green.py <PR> --repo OWNER/NAME \
  --required "lint,unit tests,ci passed" [--dry-run] [--timeout-seconds 1800]
```

Exit 0 merged, 1 a required job failed, 2 timed out or no jobs named, 3 `gh`
error. Run it with `--dry-run` first on a new repository. Tests live in
[`tests/test_merge_if_green.py`](./tests/test_merge_if_green.py); run
`python3 -m unittest discover -s tests` from this directory.

Before trusting it in a new repository, break one required job on purpose,
watch the gate refuse, and restore it.
