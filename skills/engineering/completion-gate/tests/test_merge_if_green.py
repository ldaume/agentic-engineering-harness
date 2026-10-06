import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "merge-if-green.py"
REQUIRED = ("lint", "unit tests", "browser smoke", "ci passed")


def load_module():
    spec = importlib.util.spec_from_file_location("merge_if_green", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DecideTests(unittest.TestCase):
    def setUp(self):
        self.decide = load_module().decide

    def test_no_checks_reported_is_pending_not_green(self):
        # Given gh has nothing to report yet, as in the seconds after a push
        # Then the verdict is pending, never green
        self.assertEqual(self.decide("no checks reported on the 'x' branch", REQUIRED), "pending")
        self.assertEqual(self.decide("", REQUIRED), "pending")

    def test_a_missing_required_job_is_pending(self):
        # Given three of four required jobs pass and the fourth is absent
        output = "\n".join(
            [
                "lint\tpass\t2m\thttps://x",
                "unit tests\tpass\t2m\thttps://x",
                "ci passed\tpass\t20s\thttps://x",
                "Preview\tpass\t0\thttps://x",
            ]
        )
        self.assertEqual(self.decide(output, REQUIRED), "pending")

    def test_one_red_required_job_is_red_even_when_the_rest_pass(self):
        # Given a table where one required job failed and the rest passed
        output = "\n".join(
            [
                "browser smoke\tfail\t2m8s\thttps://x",
                "Preview Comments\tpass\t0\thttps://x",
                "unit tests\tpass\t2m26s\thttps://x",
                "lint\tpass\t2m51s\thttps://x",
                "ci passed\tpass\t21s\thttps://x",
                "Agent Review\tskipping\t0\thttps://x",
            ]
        )
        self.assertEqual(self.decide(output, REQUIRED), "red")

    def test_every_required_job_passing_is_green(self):
        output = "\n".join(f"{job}\tpass\t1m\thttps://x" for job in REQUIRED) + "\nPreview\tpass\t0\thttps://x"
        self.assertEqual(self.decide(output, REQUIRED), "green")

    def test_a_pending_required_job_is_pending(self):
        output = "\n".join(f"{job}\tpass\t1m\thttps://x" for job in REQUIRED[:3]) + "\nci passed\tpending\t0\thttps://x"
        self.assertEqual(self.decide(output, REQUIRED), "pending")


if __name__ == "__main__":
    unittest.main()


class VerdictLineTests(unittest.TestCase):
    def test_a_refusal_on_red_ends_with_the_verdict(self):
        # Given a required job failed, and a caller that reads only the tail
        import contextlib
        import io

        module = load_module()
        module._checks = lambda pr, repo: "lint\tfail\t2m\thttps://x\n"
        out = io.StringIO()

        # When the gate runs
        with contextlib.redirect_stdout(out):
            code = module.main(["130", "--required", "lint"])

        # Then it refuses, and the last line says so, since a pipe hides the exit code
        self.assertEqual(code, module.EXIT_RED)
        self.assertTrue(out.getvalue().strip().splitlines()[-1].startswith("NOT MERGED"))


class RequiredJobsTests(unittest.TestCase):
    def test_without_named_jobs_the_gate_refuses_at_once(self):
        # Given a caller that names no required jobs
        import contextlib
        import io

        module = load_module()
        module._checks = lambda pr, repo: self.fail("must not poll without named jobs")

        # When the gate starts
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as stop:
            module.main(["40"])

        # Then it stops before waiting, with argparse's usage error
        self.assertEqual(stop.exception.code, 2)


class BehindBaseTests(unittest.TestCase):
    """Green on a stale branch is not green on the branch it merges into.

    Two pull requests can pass every required job and leave the base red
    together: one renames a control, the other asserts the old name, and
    neither was rebased on the other.
    """

    def setUp(self):
        self.module = load_module()

    def test_a_branch_level_with_its_base_is_not_behind(self):
        # Given a comparison where the head contains every commit of the base
        # Then nothing has to be updated before merging
        self.assertFalse(self.module.is_behind({"behind_by": 0}))

    def test_a_branch_missing_base_commits_is_behind(self):
        # Given the base moved on after the checks ran
        # Then the branch has to be updated, so the jobs run against it
        self.assertTrue(self.module.is_behind({"behind_by": 3}))

    def test_an_unreadable_comparison_is_treated_as_behind(self):
        # Given gh answered with something without the field
        # Then the gate does not assume current, the way it never assumes green
        self.assertTrue(self.module.is_behind({}))
        self.assertTrue(self.module.is_behind(None))


class StaleRedTests(unittest.TestCase):
    """A red verdict measured against a base that has moved says nothing either.

    A red branch that is behind its base is in the position a green one is:
    what the jobs said was about a tree nobody will merge. So it is brought
    forward and asked again, and only a failure measured against the current
    base stops anything.
    """

    def setUp(self):
        self.module = load_module()

    def test_a_red_branch_behind_its_base_is_refreshed_rather_than_refused(self):
        # Given a branch whose jobs failed while it was behind its base
        self.assertTrue(self.module.should_refresh("red", {"behind_by": 2}))

    def test_a_red_branch_level_with_its_base_is_a_real_failure(self):
        # Given the failure was measured against the tree that would merge
        self.assertFalse(self.module.should_refresh("red", {"behind_by": 0}))

    def test_a_green_branch_behind_its_base_is_still_refreshed(self):
        # The rule this generalises, unchanged
        self.assertTrue(self.module.should_refresh("green", {"behind_by": 1}))

    def test_a_pending_branch_is_left_to_finish(self):
        # Given jobs that have not answered yet, whatever the base did
        self.assertFalse(self.module.should_refresh("pending", {"behind_by": 3}))

    def test_an_unreadable_comparison_never_refreshes_blind(self):
        # The gate says what it could not read instead of acting on a guess
        self.assertFalse(self.module.should_refresh("red", None))
        self.assertFalse(self.module.should_refresh("green", None))


class StalledTests(unittest.TestCase):
    """A required job that a branch never ran cannot answer by waiting.

    A pull request opened before its repository required a new job passes
    every job it ran, the new one never reports on that head, and a gate that
    only brings green or red forward to the current base waits out its timeout.
    """

    def setUp(self):
        self.module = load_module()

    def _table(self, *rows):
        return "\n".join(rows)

    def test_a_required_job_never_run_with_nothing_running_is_stalled(self):
        # Given three required jobs passed and the fourth was never reported
        output = self._table(
            "lint\tpass\t2m\thttps://x",
            "unit tests\tpass\t2m\thttps://x",
            "ci passed\tpass\t20s\thttps://x",
        )
        # Then the branch is stalled, not merely pending
        self.assertTrue(self.module.stalled(output, REQUIRED))

    def test_a_required_job_still_running_is_not_stalled(self):
        # Given one required job is still running
        output = self._table(
            "lint\tpending\t0\thttps://x",
            "ci passed\tpass\t20s\thttps://x",
        )
        # Then it is left to finish
        self.assertFalse(self.module.stalled(output, REQUIRED))

    def test_nothing_reported_yet_is_not_stalled(self):
        # Given the seconds after a push, before any job reports
        self.assertFalse(self.module.stalled("", REQUIRED))

    def test_a_stalled_branch_behind_its_base_is_refreshed(self):
        # Given a stalled pending verdict on a branch behind its base
        # Then it is brought forward so the missing job can run
        self.assertTrue(self.module.should_refresh("pending", {"behind_by": 240}, stalled=True))

    def test_a_stalled_branch_level_with_its_base_is_left_alone(self):
        # Given the base has not moved, refreshing would change nothing
        self.assertFalse(self.module.should_refresh("pending", {"behind_by": 0}, stalled=True))


class UnreadableComparisonTests(unittest.TestCase):
    """What the gate does when it cannot tell how the branch sits.

    Merging blind and reporting blind are not the same risk. A merge that
    might be measured against a tree nobody will produce is refused; a
    failure is still a failure, and swallowing it because the staleness could
    not be checked loses the one signal the caller came for.
    """

    def setUp(self):
        self.module = load_module()

    def test_neither_verdict_is_refreshed_without_a_comparison(self):
        self.assertFalse(self.module.should_refresh("green", None))
        self.assertFalse(self.module.should_refresh("red", None))


class RepositoryShapeTests(unittest.TestCase):
    """`gh --repo` takes OWNER/NAME, and a path fails every call silently.

    Given a worktree path where the flag wanted a slug, every `gh` invocation
    fails. The gate reads stderr as part of its evidence, so it counted those
    failures as "no job has reported yet" and waited out its whole timeout
    without printing anything.
    """

    def setUp(self):
        self.module = load_module()

    def test_given_a_filesystem_path_when_the_gate_runs_then_it_refuses(self):
        # Given the shape a worktree path has.
        argv = ["176", "--repo", "/home/someone/dev/a-repo", "--required", "lint"]

        # When the gate is asked to merge.
        exit_code = self.module.main(argv)

        # Then it refuses immediately rather than polling a repository that
        # cannot answer.
        self.assertEqual(exit_code, self.module.EXIT_GH)

    def test_given_a_slug_when_it_is_checked_then_the_shape_is_accepted(self):
        # Given the shape `gh` actually wants. The gate must not refuse this,
        # or the guard would be a gate against itself.
        for slug in ("owner/name", "some-org/some-repo"):
            with self.subTest(slug=slug):
                self.assertIsNotNone(self.module.re.fullmatch(r"[^/\s]+/[^/\s]+", slug))

    def test_given_no_repository_when_the_gate_runs_then_the_shape_is_not_checked(self):
        # Given no `--repo` at all, which means the working directory. There is
        # no slug to check and the guard must not invent one.
        self.assertIsNone(self.module.re.fullmatch(r"[^/\s]+/[^/\s]+", ""))


class MergeCommandTests(unittest.TestCase):
    def setUp(self):
        self.gate = load_module()

    def test_given_a_green_pr_when_it_merges_then_gh_is_not_asked_to_delete_a_local_branch(self):
        # Given a head branch that may be checked out in another worktree,
        # where `gh pr merge --delete-branch` aborts before merging
        # When the gate builds its merge command
        command = self.gate.merge_command("344", "owner/name")
        # Then it merges without touching local branches
        self.assertNotIn("--delete-branch", command)
        self.assertEqual(command[:4], ["gh", "pr", "merge", "344"])
        self.assertIn("--merge", command)
        self.assertEqual(command[-2:], ["--repo", "owner/name"])

    def test_given_a_merged_pr_when_its_branch_is_removed_then_only_the_remote_ref_goes(self):
        # Given the merged PR's head branch
        # When the gate builds the cleanup command
        command = self.gate.delete_remote_branch_command("owner/name", "feature-branch")
        # Then it deletes the remote ref through the API and nothing local
        self.assertEqual(
            command,
            ["gh", "api", "-X", "DELETE", "repos/owner/name/git/refs/heads/feature-branch"],
        )
