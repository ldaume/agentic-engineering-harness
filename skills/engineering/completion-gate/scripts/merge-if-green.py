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

A required name matches a check's full name ("<workflow> / <job> (<event>)")
or its job part. Skipped checks count as neither pass nor fail. When two
checks that answer to one name disagree, the gate refuses and lists every
full name it saw, so the caller can pass one exactly.

A green pull request is refused when its diff adds a git conflict marker
(`<<<<<<< `, `>>>>>>> `, `||||||| ` or a bare `=======`), in any file, fenced
code block or not: no CI job reads a Markdown file, so markers in one pass
every check. Only added lines count. A diff gh cannot provide fails closed.

Exit 0 merged (or green on --dry-run), 1 a required job failed, 2 timed out
waiting or no jobs named, 3 gh error, 5 the diff adds a conflict marker.
Every refusal ends with a "NOT MERGED: ..." line; test that the last line
starts with "MERGED:", never that it contains "MERGED".
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time

EXIT_MERGED, EXIT_RED, EXIT_TIMEOUT, EXIT_GH, EXIT_MARKERS = 0, 1, 2, 3, 5
MARKER_LINE = re.compile(r"(<<<<<<<|>>>>>>>|\|\|\|\|\|\|\|) ")
HUNK = re.compile(r"@@ -\d+(?:,\d+)? \+(\d+)")


def conflict_markers(diff: str) -> list[tuple[str, int, str]]:
    """(file, new line number, text) of every added line that is a conflict marker."""
    found: list[tuple[str, int, str]] = []
    path, number = "", 0  # number 0: before the first hunk of a file
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            number = 0
        elif number == 0 and line.startswith("+++ "):
            path = line[4:].removeprefix("b/")
        elif hunk := HUNK.match(line):
            number = int(hunk.group(1))
        elif number and line.startswith("+"):
            if MARKER_LINE.match(line[1:]) or line == "+=======":
                found.append((path, number, line[1:]))
            number += 1
        elif number and line.startswith(" "):
            number += 1
    return found


def _diff(pr: str, repo: str | None) -> str | None:
    """The pull request's diff as gh serves it, None when it cannot."""
    command = ["gh", "pr", "diff", pr] + (["--repo", repo] if repo else [])
    seen = subprocess.run(command, capture_output=True, text=True, check=False)
    return seen.stdout if seen.returncode == 0 and seen.stdout else None


def _severity(state: str) -> int:
    """fail is worst, pass is best, anything else (pending, skipping) sits between."""
    return {"fail": 0, "pass": 2}.get(state, 1)


def _job_names(check: str) -> tuple[str, ...]:
    """"CI / verify (pull_request)" also answers to "CI / verify" and "verify"."""
    without_event = re.sub(r"\s*\([^)]*\)$", "", check)
    return check, without_event, without_event.split(" / ", 1)[-1]


def _contexts(checks_output: str, required: tuple[str, ...]) -> dict[str, dict[str, str]]:
    """For each required name, the full check names that answer to it and their states.

    A name equal to a full check name is that check alone. A check listed
    twice keeps its worst state, because gh prints no times to pick the newest.
    """
    rows: dict[str, str] = {}
    for line in checks_output.splitlines():
        cells = line.split("\t")
        if len(cells) >= 2:
            state = cells[1].strip()
            seen = rows.get(cells[0])
            if seen is None or _severity(state) < _severity(seen):
                rows[cells[0]] = state
    found: dict[str, dict[str, str]] = {}
    for job in required:
        hits = {name: state for name, state in rows.items() if job in _job_names(name)}
        found[job] = {job: hits[job]} if job in hits else hits
    return found


def _verdicts(checks_output: str, required: tuple[str, ...]) -> dict[str, str]:
    """pass, fail, pending, or absent per required name.

    Skipped checks count as neither pass nor fail while a non-skipped one
    answers; a name with only skipped checks is still pending.
    """
    verdicts: dict[str, str] = {}
    for job, contexts in _contexts(checks_output, required).items():
        states = set(contexts.values())
        live = {state for state in states if state != "skipping"}
        if not states:
            verdicts[job] = "absent"
        elif "fail" in live:
            verdicts[job] = "fail"
        elif live and live == {"pass"}:
            verdicts[job] = "pass"
        else:
            verdicts[job] = "pending"
    return verdicts


def describe_required(checks_output: str, required: tuple[str, ...]) -> str:
    """Per required name, every full check name seen, so a caller can pass one exactly."""
    lines = []
    for job, contexts in _contexts(checks_output, required).items():
        seen = ", ".join(f"'{name}' ({state})" for name, state in contexts.items())
        lines.append(f"required '{job}': {seen or 'no check seen'}")
    return "\n".join(lines)


def decide(checks_output: str, required: tuple[str, ...]) -> str:
    """`green` when every required job reports pass, `red` when any reports fail, else `pending`."""
    verdicts = _verdicts(checks_output, required)
    if "fail" in verdicts.values():
        return "red"
    if all(verdicts[job] == "pass" for job in required):
        return "green"
    return "pending"


def stalled(checks_output: str, required: tuple[str, ...]) -> bool:
    """Whether a required job is absent while nothing required is still running.

    Such a job will not answer by waiting: the branch predates the job, so it
    never runs on this head. Nothing reported at all is not stalled, because
    that is also the moment right after a push.
    """
    verdicts = _verdicts(checks_output, required)
    seen = [state for state in verdicts.values() if state != "absent"]
    if not seen or "pending" in seen:
        return False
    return "absent" in verdicts.values()


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
            print(f"{output}\n{describe_required(output, required)}\nNOT MERGED: a required job failed on PR {args.pr}")
            return EXIT_RED
        if verdict == "green":
            diff = _diff(args.pr, args.repo)
            if diff is None:
                print(f"NOT MERGED: could not read the diff of PR {args.pr} to check it for conflict markers")
                return EXIT_GH
            markers = conflict_markers(diff)
            if markers:
                for name, number, text in markers:
                    print(f"conflict marker at {name}:{number}: {text}")
                print(f"NOT MERGED: PR {args.pr} adds git conflict markers; resolve them and push")
                return EXIT_MARKERS
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
            print(f"{output}\n{describe_required(output, required)}\nNOT MERGED: required jobs still pending on PR {args.pr}")
            return EXIT_TIMEOUT
        time.sleep(args.interval_seconds)


if __name__ == "__main__":
    sys.exit(main())
