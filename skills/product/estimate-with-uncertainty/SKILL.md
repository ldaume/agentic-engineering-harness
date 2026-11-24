---
name: estimate-with-uncertainty
description: Computes estimates and forecasts from small, messy operational data as ranges with their basis - cost and budget forecasts, capacity and headcount sizing, volume and KPI projections. Use whenever asked to estimate, forecast, project, or size cost, load, capacity, or volume from measured data. Not for hypothesis tests or A/B sizing (statistical-analysis, statistical-power) or for wording the figures (plain-numbers).
license: MIT
compatibility: The bundled sketch needs only Python 3 standard library.
---

# Estimate With Uncertainty

A number about the future is a distribution. The job is to compute it honestly
from the data that exists, say which part of it a reader sees, and make every
published figure reproducible. Small samples, open items, skew, and bursty
counts are the normal case, so the first method that fits a textbook is
usually wrong for them.

## Standing rules

1. **Value before size.** Name the decision the number feeds and the threshold
   that would change it (the investment boundary). If no decision needs it,
   define the outcome and the most worth spending on it instead, and stop:
   precision nobody uses costs a day, and the threshold also tells how wide a
   range can be and still decide. `product-craft` owns that conversation.
2. **Ranges only.** Every future figure carries an interval, its basis (n,
   period, source), and what would move it; simulated shares (builds that
   wait, months over budget) too, from replicate runs. A single value reads
   as a commitment, and a miss reads as a broken promise.
3. **Measured beats guessed.** Compute from measured throughput, cost, or
   duration data; put each assumption next to the figure it drives. Where no
   data exists, use comparable past work as a reference range, not intuition.
4. **One method.** Publish one method. A replaced method moves to a
   correction log (old, new, reason), never sits beside the new one, because
   two sets of numbers make the reader pick the one they like.
5. **Reproducible.** Fixed seeds, scripts that rerun end to end, and a check
   that every figure you report equals the model output, also for an answer
   in chat. Hand-copied numbers drift within one review round.
6. **Headline by purpose.** A budget uses the mean (expected value: what you
   pay over many periods); "typical" uses the median; the interval says how
   sure. Label the headline figure "average" or "typical" where it stands.
   Under right skew the mean sits above the median: say so in one line, or
   readers think one of them is a mistake.
7. **Sensitivities in the method details.** They show robustness; they are
   not alternative headlines.

## Procedure

1. **Frame.** Decision, quantity, unit, horizon, threshold. Done when the
   threshold is written down; when nobody gave one, assume one, say so in
   the answer, and show what changes on either side of it.
2. **Inspect the data before choosing a model.** Write down: n per group;
   items still open (their cost to date is a lower bound); skew (look on a
   log scale); the dispersion index (variance over mean) of every count; the
   share of forecast inputs beyond the largest observed value. Each of these
   picks a row in the table below.
3. **Choose the method** from the table. One default per situation; deviate
   only for a reason you log.
4. **Simulate** the quantity the decision needs (see Three ranges).
5. **Run the sensitivity checks**, one line each in the method details.
6. **Report** with the headline rule above, then hand the wording to
   `plain-numbers` for a reader outside the work.
7. **Reproduce check.** Done when the saved script, rerun from scratch,
   prints `OVERALL PASS` against the figures in your answer (see below).

## Data situation -> method

| Data situation | Default method | Why not the obvious one |
|---|---|---|
| Positive, right-skewed amounts (cost, duration) with a size driver, n below about 50 | Bayesian lognormal regression on log scale, weakly informative priors (normal(0, 1) on log-scale slopes and group effects); bootstrap only as a cross-check | OLS plus bootstrap at n = 20 gives percentile and BCa intervals that disagree; the posterior also carries parameter uncertainty into the forecast |
| A small subgroup (a new customer, a new team: fewer than about 10 items) | A group term with a prior that shrinks toward zero; with several groups, a hierarchical model with a half-normal or half-t prior on the group scale | A raw subgroup mean at n = 6 overstates the difference; an Inverse-Gamma(eps, eps) prior on a group scale misbehaves with few groups |
| Items still open | Cost to date times an uplift factor from a stated range, redrawn in every posterior step; a censored (Tobit) fit as the upper scenario | Counting open items as finished biases every figure down |
| Counts per period (items per sprint, tickets per week) | Dispersion index first. Above 1: resample measured period counts (a month = two drawn sprint counts) or a negative binomial. About 1: Poisson | Poisson on overdispersed data gives too narrow ranges; quantiles plus Poisson on top double-counts the noise and gives too wide ones |
| A rate that may depend on size (questions per feature vs size) | Bayesian Poisson or negative-binomial regression; report the slope interval and P(slope > 0) | A p-value answers a question nobody asked; with few nonzero counts the bootstrap often separates the data |
| Capacity of a queue (runners, on-call people, workers) | State the wait target first (for example 95% wait at most 5 minutes). Discrete-event simulation with the measured burst pattern and lognormal durations, or replayed measured days; Erlang C as cross-check; then N+1 so the largest machine can fail | Average utilisation hides bursts; sizing to a peak without a wait target or failure reserve is either waste or an outage |
| Nothing measured | Do not compute. Define value and boundary, or give a reference range from comparable past work with its source | A model on invented inputs launders a guess into a figure |
| Hypothesis test, study or experiment design, power | `statistical-analysis`, `experimental-design`, `statistical-power` | Different question: a forecast needs a predictive distribution, not a test |

The rows trace to (supported) [SRC-EST-001] [SRC-EST-002] [SRC-EST-003]
[SRC-EST-008] for regression and priors, (supported) [SRC-EST-005] for the
bootstrap, (supported) [SRC-EST-006] for queues, (supported) [SRC-EST-009]
for open items as measurement error, and (supported) [SRC-EST-010] for the
Tobit scenario.

`scripts/forecast_sketch.py` is a stdlib starting point for the first, third,
and fourth rows: a Gibbs sampler with the open-item uplift, the resampled
volume, the three ranges, a dispersion check, and `check_published`. Copy and
adapt it rather than writing a sampler from scratch;
`tests/test_forecast_sketch.py` shows each behavior it guarantees.

## Three ranges

A period forecast mixes two uncertainties. Keep them apart and say which one a
figure is:

- **Expected period** (the budget): per posterior draw, the mean cost of a
  forecast item, `exp(mu + sigma^2 / 2)` averaged over the forecast mix, times
  the expected volume. Its interval says how sure the average is.
- **Period to period** at fixed (median) parameters: quiet, typical, busy
  periods from item and volume noise alone.
- **Predictive**: both together, for "what could next month cost".

Uncertainty about shared parameters does not shrink when you multiply by n
products or teams: scale the interval with n, do not divide it by sqrt(n).
When part of the forecast lies beyond the largest observed input, report that
share and its share of the cost; it is extrapolation, not measurement.

## Sensitivity checks

Run each, report one line, change the headline only through the correction
log:

- Duan smearing instead of the normal back-transform `exp(sigma^2 / 2)`
  (supported) [SRC-EST-004] [SRC-EST-007].
- Student-t residuals; with heavy tails the mean may not exist, so report
  quantiles only.
- Leave one out and influence (Cook's distance) on the slope and the headline.
- Inputs capped at the largest observed value.
- Bootstrap percentile vs BCa: a large gap means the sample is too small for
  the bootstrap; prefer the posterior (supported) [SRC-EST-005].
- Capacity: products peaking on the same days instead of independently, and
  the longest durations doubled; the recommendation should survive both or
  say which one breaks it.
- A known defect that confounds a group effect (same period, same customer):
  show the figure with the defect removed as a scenario, not as the estimate,
  because the data cannot separate the two.

## Reproduce check

Every forecast leaves one script with fixed seeds that reruns the models end
to end. Its last step holds the figures exactly as the answer or page states
them (a `STATED` dict, typed in from your draft, rounded as written) and
compares each with the freshly computed value (`check_published` in the
sketch), one
`PASS` or `FAIL` line each, last line `OVERALL PASS` or `OVERALL FAIL`. For a
page, render it to text first and format the numbers in its locale; for a
growing analysis, also compare each output file with the stored one. Run it
before every publish and after every data refresh. Draft the answer, type its
figures into `STATED`, rerun, then send: a check that compares the script with
its own variables proves nothing. A `FAIL` means the answer or the model is
wrong, never that the check is too strict.

## Correction log

Keep it at the end of the method document:

| Before | Now | Reason |
|---|---|---|
| OLS on log cost, bootstrap over 19 items | Bayesian lognormal regression | Open items counted as finished; percentile and BCa intervals disagreed |

Reviewers find the same first-draft errors again and again; check for them
before review: open items counted as finished, Poisson without a dispersion
check, a subgroup mean without shrinkage, a p-value instead of a probability,
capacity without a wait target or N+1, a median published as the budget,
interval scaled by sqrt(n) across products, and figures copied by hand.

## Example headline

"Budget about 1,160 USD a month (the average; 90% interval 520 to 2,290),
based on 19 measured features, 3 still open, and 20 sprints. A typical month
is about 900 and a busy one 1,470. The average sits above the typical month
because a few large items cost much more. 34 of the 90 planned items are
larger than anything built so far; splitting them is the biggest lever."
(Figures from the demo in `scripts/forecast_sketch.py`.)

## Sources

`references/sources.json` holds the registry. Practitioner anchor: a point
forecast is of almost no value without its prediction interval (verified)
[SRC-EST-011].
