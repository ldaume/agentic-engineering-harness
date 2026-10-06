#!/usr/bin/env python3
"""Merge a pull request only when every required job explicitly reports pass.

`gh pr checks` prints nothing, or "no checks reported", in the seconds after
a push before the workflow registers its jobs. A script that read the absence
of a failure line as green can merge a red pull request. The rule here is the
other way round: a job that has not said "pass" has not passed, and a job that
is missing is not green.

Usage:
    python3 merge-if-green.py PR --required "job a,job b" [--repo owner/name]
        [--timeout-seconds 1800] [--dry-run]

`--required` takes one comma-separated list of the repository's own required
jobs. It has no default: a default carries one repository's job names, and in
any other repository the gate waits the whole timeout for jobs that never exist.

A branch that is behind its base is brought forward before it merges, and the
gate waits for the rerun. Two pull requests can each pass every job and leave
the base red together when each was green against a base the other had moved.

Exit 0 merged, 1 a required job failed, 2 timed out waiting or no jobs named,
3 gh error.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time

EXIT_MERGED, EXIT_RED, EXIT_TIMEOUT, EXIT_GH = 0, 1, 2, 3


def decide(checks_output: str, required: tuple[str, ...]) -> str:
    """`green` when every required job reports pass, `red` when any reports fail, else `pending`."""
    states: dict[str, str] = {}
    for line in checks_output.splitlines():
        cells = line.split("\t")
        if len(cells) >= 2 and cells[0] in required:
            states[cells[0]] = cells[1].strip()
    if any(states.get(job) == "fail" for job in required):
        return "red"
    if all(states.get(job) == "pass" for job in required):
        return "green"
    return "pending"


def stalled(checks_output: str, required: tuple[str, ...]) -> bool:
    """Whether a required job is absent while nothing required is still running.

    Such a job will not answer by waiting: the branch predates the job, so it
    never runs on this head. Nothing reported at all is not stalled, because
    that is also the moment right after a push.
    """
    states: dict[str, str] = {}
    for line in checks_output.splitlines():
        cells = line.split("\t")
        if len(cells) >= 2 and cells[0] in required:
            states[cells[0]] = cells[1].strip()
    if not states or "pending" in states.values():
        return False
    return any(job not in states for job in required)


def is_behind(comparison: dict | None) -> bool:
    """Whether the branch is missing commits its base already has.

    Unreadable is behind, for the same reason unreported is not green: the
    gate never assumes the good case from an absent answer.
    """
    if not isinstance(comparison, dict):
        return True
    behind = comparison.get("behind_by")
    if not isinstance(behind, int):
        return True
    return behind > 0


def should_refresh(verdict: str, comparison: dict | None, *, stalled: bool = False) -> bool:
    """Whether the branch has to be brought forward before its verdict counts.

    Green and red are the same case. A branch can sit blocked behind a failed
    job from a run that predated the repair of the thing it failed on: the base
    moved, the failure was about a tree nobody would merge, and a gate that
    only updates on the way to a green merge neither merges nor updates.

    Pending is left alone - jobs that have not answered are not a verdict -
    unless it is stalled: a required job the branch never ran, with nothing
    else running. And an unreadable comparison never refreshes blind, for the
    same reason it never merges blind.
    """
    if verdict not in {"green", "red"} and not stalled:
        return False
    if not isinstance(comparison, dict):
        return False
    return is_behind(comparison)


def _comparison(pr: str, repo: str | None) -> dict | None:
    """How far the pull request's head sits behind its base."""
    view = ["gh", "pr", "view", pr, "--json", "baseRefName,headRefName,headRepositoryOwner"]
    if repo:
        view += ["--repo", repo]
    seen = subprocess.run(view, capture_output=True, text=True, check=False)
    if seen.returncode != 0:
        return None
    try:
        fields = json.loads(seen.stdout)
        base, head = fields["baseRefName"], fields["headRefName"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
    slug = repo or _slug()
    if slug is None:
        return None
    compared = subprocess.run(
        ["gh", "api", f"repos/{slug}/compare/{base}...{head}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if compared.returncode != 0:
        return None
    try:
        return json.loads(compared.stdout)
    except json.JSONDecodeError:
        return None


def _slug() -> str | None:
    """The repository the working directory belongs to, when `--repo` was not given."""
    seen = subprocess.run(
        ["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
        capture_output=True,
        text=True,
        check=False,
    )
    name = seen.stdout.strip()
    return name if seen.returncode == 0 and name else None


def _update_branch(pr: str, repo: str | None) -> bool:
    command = ["gh", "pr", "update-branch", pr]
    if repo:
        command += ["--repo", repo]
    return subprocess.run(command, check=False).returncode == 0


def merge_command(pr: str, repo: str | None) -> list[str]:
    """Merge on the server only.

    `--delete-branch` also deletes and switches local branches, and gh aborts
    before merging when another worktree has the head branch checked out.
    """
    command = ["gh", "pr", "merge", pr, "--merge"]
    if repo:
        command += ["--repo", repo]
    return command


def delete_remote_branch_command(repo: str, branch: str) -> list[str]:
    return ["gh", "api", "-X", "DELETE", f"repos/{repo}/git/refs/heads/{branch}"]


def _head_branch(pr: str, repo: str | None) -> str | None:
    command = ["gh", "pr", "view", pr, "--json", "headRefName", "--jq", ".headRefName"]
    if repo:
        command += ["--repo", repo]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    return result.stdout.strip() or None if result.returncode == 0 else None


def _checks(pr: str, repo: str | None) -> str:
    command = ["gh", "pr", "checks", pr]
    if repo:
        command += ["--repo", repo]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    # gh exits non-zero while a check is pending or failing; the table is still the evidence.
    return result.stdout + result.stderr


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pr")
    parser.add_argument("--required", required=True)
    parser.add_argument("--repo")
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--interval-seconds", type=int, default=30)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--skip-update",
        action="store_true",
        help="merge a branch that is behind its base without bringing it forward first",
    )
    args = parser.parse_args(argv)
    required = tuple(name.strip() for name in args.required.split(",") if name.strip())

    # `gh --repo` takes OWNER/NAME. Given a filesystem path it fails on every
    # call, and since the gate reads stderr as part of the evidence, that reads
    # as "no job has reported yet" - the gate then waits out its whole timeout
    # in silence. Removing this guard reproduces the hang, which is what its test
    # demonstrates.
    if args.repo is not None and not re.fullmatch(r"[^/\s]+/[^/\s]+", args.repo):
        print(f"NOT MERGED: --repo wants OWNER/NAME, not {args.repo!r}")
        return EXIT_GH

    deadline = time.monotonic() + args.timeout_seconds
    while True:
        output = _checks(args.pr, args.repo)
        verdict = decide(output, required)

        # A verdict counts only against the base this merge would produce, and
        # that is as true of a failure as of a pass. Read once per pass, for
        # both, so a red branch left behind by a repair is asked again rather
        # than blocking until somebody notices by hand.
        stuck = verdict == "pending" and stalled(output, required)
        if (verdict in {"green", "red"} or stuck) and not args.skip_update:
            comparison = _comparison(args.pr, args.repo)
            if comparison is None and verdict == "green":
                # Not knowing is not the same as being behind: the gate says
                # what it could not read instead of merging a branch blind.
                # Red falls through: a failure is still worth reporting, and
                # refusing to report it because the staleness could not be
                # checked loses the one signal the caller came for.
                print(f"NOT MERGED: could not read how PR {args.pr} sits against its base")
                return EXIT_GH
            if should_refresh(verdict, comparison, stalled=stuck):
                if not _update_branch(args.pr, args.repo):
                    print(f"NOT MERGED: PR {args.pr} is behind its base and could not be updated")
                    return EXIT_GH
                print(f"PR {args.pr} was behind its base; updated it and waiting for the rerun")
                time.sleep(args.interval_seconds)
                continue

        if verdict == "red":
            # The verdict prints last: a caller piping through `tail` loses the exit code.
            print(f"{output}\nNOT MERGED: a required job failed on PR {args.pr}")
            return EXIT_RED
        if verdict == "green":
            if args.dry_run:
                print(f"green: would merge PR {args.pr}")
                return EXIT_MERGED
            branch = _head_branch(args.pr, args.repo)
            merged = subprocess.run(merge_command(args.pr, args.repo), check=False)
            if merged.returncode != 0:
                print(f"NOT MERGED: gh pr merge failed on PR {args.pr}")
                return EXIT_GH
            repo = args.repo or _slug()
            if branch and repo:
                # Best effort: a repository that deletes merged branches itself
                # answers 422 here, and the merge already stands either way.
                subprocess.run(
                    delete_remote_branch_command(repo, branch), capture_output=True, check=False
                )
            print(f"MERGED: PR {args.pr}")
            return EXIT_MERGED
        if time.monotonic() >= deadline:
            print(f"{output}\nNOT MERGED: required jobs still pending on PR {args.pr}")
            return EXIT_TIMEOUT
        time.sleep(args.interval_seconds)


if __name__ == "__main__":
    sys.exit(main())
