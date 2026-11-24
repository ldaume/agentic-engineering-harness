"""Behavior of the stdlib forecast sketch, in Given/When/Then form."""

import math
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import forecast_sketch as fs  # noqa: E402


def synthetic(n, a, b, sigma, seed, group=None, c=0.0):
    rng = random.Random(seed)
    rows, y = [], []
    for i in range(n):
        size = math.exp(rng.gauss(5.5, 1.0))
        g = 1.0 if group and i < group else 0.0
        rows.append([1.0, math.log(size), g])
        y.append(math.exp(a + b * math.log(size) + c * g + rng.gauss(0, sigma)))
    return rows, y


class FitTest(unittest.TestCase):
    def test_recovers_a_known_slope_from_plenty_of_data(self):
        # Given 300 items drawn with slope 0.6
        rows, y = synthetic(300, -1.0, 0.6, 0.8, seed=1)
        # When the lognormal regression is fitted
        draws = fs.fit_lognormal(rows, y, prior_sd=[10, 1, 1], draws=1500, burn=500, seed=2)
        # Then the posterior mean slope is close to 0.6
        slope = sum(d[0][1] for d in draws) / len(draws)
        self.assertAlmostEqual(slope, 0.6, delta=0.08)

    def test_a_tight_prior_shrinks_a_small_group_effect(self):
        # Given 20 items of which only 3 belong to a group with a large true effect
        rows, y = synthetic(20, -1.0, 0.6, 1.0, seed=3, group=3, c=1.5)
        # When the model is fitted with a weak and with a weakly informative prior on the group
        wide = fs.fit_lognormal(rows, y, prior_sd=[10, 1, 100], draws=1500, burn=500, seed=4)
        tight = fs.fit_lognormal(rows, y, prior_sd=[10, 1, 0.5], draws=1500, burn=500, seed=4)
        # Then the weakly informative prior pulls the group effect toward zero
        mean = lambda ds: sum(abs(d[0][2]) for d in ds) / len(ds)
        self.assertLess(mean(tight), mean(wide))

    def test_open_items_raise_the_estimate_above_their_cost_to_date(self):
        # Given items of which half are still open, with cost to date as a lower bound
        rows, y = synthetic(30, -1.0, 0.6, 0.5, seed=5)
        open_mask = [i % 2 == 0 for i in range(30)]
        # When fitted once treating open items as finished and once with an uplift
        plain = fs.fit_lognormal(rows, y, prior_sd=[10, 1, 1], draws=800, burn=300, seed=6)
        lifted = fs.fit_lognormal(rows, y, prior_sd=[10, 1, 1], draws=800, burn=300, seed=6,
                                  open_mask=open_mask, uplift=(1.0, 1.5))
        # Then the fitted log cost of a typical item rises
        typical = [sum(col) / len(rows) for col in zip(*rows)]
        fit = lambda ds: sum(sum(b * x for b, x in zip(d[0], typical)) for d in ds) / len(ds)
        self.assertGreater(fit(lifted), fit(plain) + 0.05)


class ForecastTest(unittest.TestCase):
    def setUp(self):
        rows, y = synthetic(40, -1.0, 0.6, 0.9, seed=7)
        self.draws = fs.fit_lognormal(rows, y, prior_sd=[10, 1, 1], draws=800, burn=300, seed=8)
        self.new = [[1.0, math.log(s), 0.0] for s in (50, 200, 400, 900, 3000)]
        self.counts = [9, 14, 11, 6, 17, 12, 8, 13]

    def test_same_seed_gives_the_same_forecast(self):
        # Given a fitted model, when the forecast runs twice with one seed
        one = fs.forecast(self.draws, self.new, self.counts, periods=2, sims=2000, seed=9)
        two = fs.forecast(self.draws, self.new, self.counts, periods=2, sims=2000, seed=9)
        # Then every reported figure is identical
        self.assertEqual(one, two)

    def test_the_expected_period_mean_sits_above_its_median_under_right_skew(self):
        # Given right-skewed costs, when the expected period is summarized
        out = fs.forecast(self.draws, self.new, self.counts, periods=2, sims=2000, seed=9)
        # Then the mean (the budget figure) is above the median of the uncertainty
        self.assertGreater(out["expected"]["mean"], out["expected"]["p50"])
        # And the predictive range is wider than the range at fixed parameters
        pred, fixed = out["predictive"], out["period_to_period"]
        self.assertGreater(pred["p90"] - pred["p10"], fixed["p90"] - fixed["p10"])


class ChecksTest(unittest.TestCase):
    def test_dispersion_flags_counts_wider_than_poisson(self):
        # Given steady counts and bursty counts, when the dispersion index is computed
        # Then only the bursty counts exceed 1
        self.assertLess(fs.dispersion([10, 11, 9, 10, 10, 11, 9]), 1)
        self.assertGreater(fs.dispersion([3, 22, 5, 18, 2, 25, 9]), 1)

    def test_a_published_figure_that_differs_from_the_model_fails(self):
        # Given a page that shows 1,540 where the model computed 1,534
        lines = fs.check_published({"budget": 1540, "items": 23}, {"budget": 1534.2, "items": 22.6}, round_to=1)
        # Then the budget line fails and the item line passes after rounding
        self.assertEqual(lines, ["FAIL budget: page 1540, model 1534", "PASS items: page 23, model 23"])


if __name__ == "__main__":
    unittest.main()
