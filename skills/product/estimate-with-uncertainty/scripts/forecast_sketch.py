"""Stdlib sketch: Bayesian lognormal regression, a resampled-volume forecast, and the checks.

Copy and adapt it; it is a starting point, not a library. No numpy so it runs anywhere.

    log(y) = X b + e,  e ~ N(0, sigma2)
    b_j ~ N(0, prior_sd_j^2)   sigma2 ~ Inverse-Gamma(a0, b0)

The Inverse-Gamma prior is only for the residual variance, where the data dominate;
a group-level (hierarchical) scale needs a half-normal or half-t prior instead.

Run `python3 forecast_sketch.py` for a synthetic demo.
"""

from __future__ import annotations

import math
import random
import statistics


def _inv(m):
    """Gauss-Jordan inverse of a small symmetric positive definite matrix."""
    k = len(m)
    a = [row[:] + [1.0 if i == j else 0.0 for j in range(k)] for i, row in enumerate(m)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(a[r][c]))
        a[c], a[p] = a[p], a[c]
        piv = a[c][c]
        a[c] = [v / piv for v in a[c]]
        for r in range(k):
            if r != c:
                f = a[r][c]
                a[r] = [v - f * w for v, w in zip(a[r], a[c])]
    return [row[k:] for row in a]


def _chol(m):
    k = len(m)
    low = [[0.0] * k for _ in range(k)]
    for i in range(k):
        for j in range(i + 1):
            s = m[i][j] - sum(low[i][t] * low[j][t] for t in range(j))
            low[i][j] = math.sqrt(s) if i == j else s / low[j][j]
    return low


def fit_lognormal(rows, y, prior_sd, draws=4000, burn=1000, seed=1, open_mask=None,
                  uplift=(1.0, 1.5), a0=0.01, b0=0.01):
    """Gibbs sampler. Returns [(b, sigma2), ...] after burn-in.

    open_mask marks items whose cost to date is a lower bound: each step multiplies
    them by a fresh U(uplift) factor, so that uncertainty reaches the posterior.
    """
    rng = random.Random(seed)
    n, k = len(rows), len(rows[0])
    open_mask = open_mask or [False] * n
    logy = [math.log(v) for v in y]
    xtx = [[sum(r[i] * r[j] for r in rows) for j in range(k)] for i in range(k)]
    prec0 = [1.0 / s ** 2 for s in prior_sd]
    b, sigma2, out = [0.0] * k, statistics.pvariance(logy) or 1.0, []
    for step in range(burn + draws):
        z = [ly + (math.log(rng.uniform(*uplift)) if o else 0.0) for ly, o in zip(logy, open_mask)]
        xtz = [sum(r[i] * zi for r, zi in zip(rows, z)) for i in range(k)]
        v = _inv([[xtx[i][j] / sigma2 + (prec0[i] if i == j else 0.0) for j in range(k)] for i in range(k)])
        mean = [sum(v[i][j] * xtz[j] for j in range(k)) / sigma2 for i in range(k)]
        low, e = _chol(v), [rng.gauss(0, 1) for _ in range(k)]
        b = [mean[i] + sum(low[i][j] * e[j] for j in range(i + 1)) for i in range(k)]
        rss = sum((zi - sum(bi * xi for bi, xi in zip(b, r))) ** 2 for r, zi in zip(rows, z))
        sigma2 = 1.0 / rng.gammavariate(a0 + n / 2, 1.0 / (b0 + rss / 2))
        if step >= burn:
            out.append((b, sigma2))
    return out


def summary(xs):
    s = sorted(xs)
    q = lambda p: s[min(len(s) - 1, int(p * len(s)))]
    return {"mean": sum(s) / len(s), "p5": q(0.05), "p10": q(0.10), "p50": q(0.50), "p90": q(0.90), "p95": q(0.95)}


def forecast(draws, new_rows, counts, periods=2, sims=20000, seed=9):
    """Three different ranges for one period (for example a month of `periods` sprints).

    expected: how sure the average period is (the budget figure and its interval).
    period_to_period: quiet, typical, busy periods at the median parameters.
    predictive: both together. Volume is resampled from measured period counts, no Poisson.
    """
    rng = random.Random(seed)
    lin = lambda b, x: sum(bi * xi for bi, xi in zip(b, x))
    volume = periods * sum(counts) / len(counts)
    expected = [volume * sum(math.exp(lin(b, x) + s2 / 2) for x in new_rows) / len(new_rows) for b, s2 in draws]

    def period(b, s2):
        n = sum(rng.choice(counts) for _ in range(periods))
        return sum(math.exp(lin(b, rng.choice(new_rows)) + math.sqrt(s2) * rng.gauss(0, 1)) for _ in range(n))

    k = len(draws[0][0])
    med_b = [statistics.median(d[0][i] for d in draws) for i in range(k)]
    med_s2 = statistics.median(d[1] for d in draws)
    fixed = [period(med_b, med_s2) for _ in range(sims)]
    pred = [period(*rng.choice(draws)) for _ in range(sims)]
    return {"expected": summary(expected), "period_to_period": summary(fixed), "predictive": summary(pred)}


def dispersion(counts):
    """Variance over mean. About 1 fits Poisson; clearly above 1 means resample or use a negative binomial."""
    return statistics.variance(counts) / statistics.mean(counts)


def check_published(published, computed, round_to=1):
    """One PASS or FAIL line per figure the page shows, against the model output."""
    lines = []
    for name, shown in published.items():
        model = round(computed[name] / round_to) * round_to
        model = int(model) if float(model).is_integer() else model
        lines.append(f"{'PASS' if shown == model else 'FAIL'} {name}: page {shown}, model {model}")
    return lines


if __name__ == "__main__":
    rng = random.Random(42)
    rows, y = [], []
    for i in range(19):
        size, grp = math.exp(rng.gauss(5.6, 0.9)), 1.0 if i < 6 else 0.0
        rows.append([1.0, math.log(size), grp])
        y.append(math.exp(-0.6 + 0.55 * math.log(size) + 0.7 * grp + rng.gauss(0, 0.95)))
    open_mask = [i in (2, 9, 15) for i in range(19)]
    draws = fit_lognormal(rows, y, prior_sd=[10, 1, 1], open_mask=open_mask)
    backlog = [[1.0, rng.gauss(5.8, 1.2), 1.0] for _ in range(90)]
    sprints = [22, 10, 12, 7, 7, 10, 14, 9, 11, 7, 5, 4, 19, 12, 5, 14, 15, 6, 16, 20]
    print(f"dispersion of sprint counts: {dispersion(sprints):.2f}")
    for key, val in forecast(draws, backlog, sprints, periods=2, sims=5000).items():
        print(key, {k: round(v) for k, v in val.items()})
