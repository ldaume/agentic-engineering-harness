# Forecast Evaluation Vocabulary

The terms forecasters use to judge whether an estimate is honest, so a review
names the gap the way the field does and points at something visible in the
forecast, its script, or its page. Authors and check scripts use it; reviews do
not load it by default. Wording of figures lives in `plain-numbers`; hypothesis
tests in `statistical-analysis`. A term is admitted only with a registered
source and an observable marker; evidence and access dates are in
`sources.json`. Check: `exact` (a pattern a script could match; none ships
here, so no rule ids) or `judge` (a person or model decides). No `jev`: no
typed question exists yet.

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Point forecast | A single value for a future quantity; of little use alone. | [SRC-EST-011] | A figure with no interval next to it. | judge |
| Prediction interval | A range that should hold the future value with a stated probability. | [SRC-EST-011] | "80% interval" or "range" with its level and basis stated. | exact |
| Interval coverage | The share of actuals that fall inside the stated interval; an 80% interval should hold about 80%. | [SRC-EST-014] | A back-test that counts hits against the stated level. | judge |
| Naive benchmark | Forecast equal to the last observed value. | [SRC-EST-012] | A comparison row for "last value" next to the model. | judge |
| Seasonal naive | Forecast equal to the last value of the same season. | [SRC-EST-012] | A benchmark for weekly or monthly data that repeats a cycle. | judge |
| Drift benchmark | The average historical change extended forward. | [SRC-EST-012] | A line through first and last observation as comparison. | judge |
| Beats the benchmark | A method is worth using only if it does better than the simple ones. | [SRC-EST-012] | An error table without any benchmark row. | judge |
| Residual diagnostics | Check that residuals are uncorrelated with zero mean; constant variance and normality are useful, not required. | [SRC-EST-013] | A residual plot, ACF plot, or Ljung-Box result in the analysis. | judge |
| Training and test split | Fit on the training part, measure accuracy on held-out data, test at least as long as the horizon. | [SRC-EST-014] | A script with a held-out period and its length stated. | exact |
| Time series cross-validation | Many tests, each trained only on earlier data (rolling origin), accuracy averaged. | [SRC-EST-015] | A loop that grows the training window and scores the next step. | exact |
| MAE and RMSE | Scale-dependent errors; MAE tracks the median forecast, RMSE the mean. | [SRC-EST-014] | Errors compared only within one unit and series. | judge |
| MASE | Error scaled by the in-sample naive error; below 1 beats naive. | [SRC-EST-014] | A scaled error reported across series with different units. | exact |
| Quantile score | Pinball loss for one quantile; lower is better. | [SRC-EST-014] | A score per quantile for the stated interval limits. | judge |
| CRPS | Average quantile score over all probabilities: scores the whole distribution. | [SRC-EST-014] | One distributional score compared across methods. | judge |
| Skill score | Relative improvement over a benchmark. | [SRC-EST-014] | A percent better or worse than naive. | judge |
| Back-transformation bias | Back-transforming a log-scale forecast gives the median; adjust to get the mean. | [SRC-EST-016] [SRC-EST-004] | `exp(mu)` used as a budget with no smearing or sigma correction. | judge |
| Interval endpoint transform | Back-transform interval limits one by one; coverage holds, the range turns asymmetric. | [SRC-EST-016] | A symmetric plus/minus band around a log-model forecast. | judge |
| Bootstrap interval | Interval from resampled residuals; no normality needed, may be asymmetric. | [SRC-EST-011] [SRC-EST-005] | A resampling loop with a seed behind the interval. | exact |
| Partial pooling | A small subgroup is shrunk toward the shared estimate. | [SRC-EST-001] | A group term with a prior, not a raw subgroup mean. | judge |
| Utilization and queueing | Waits grow with load and bursts, so size to a wait target. | [SRC-EST-006] | A capacity figure from average utilization with no wait target. | judge |
| Measurement inversion | The decision-critical quantity is the one least measured. | [SRC-EST-017] | A model rich in easy inputs, with the key driver guessed. | judge |
| Value of information | Each variable has a worth for the decision; measure the high-value ones first. | [SRC-EST-018] | A call for more data with no decision it would change. | judge |

## Not admitted

- A single-number forecast with no interval: a point forecast is of almost no
  value alone [SRC-EST-011].
- In-sample fit as forecast accuracy: residuals look better than errors on
  unseen data [SRC-EST-014].
- MAPE on data near zero: undefined at zero, extreme near it [SRC-EST-014].
- More data always before deciding: information has a value that may not
  change the decision [SRC-EST-018].
- Calibrated estimator, 90 percent estimate, Rule of Five: no fetchable
  primary page was found (Hubbard pages returned 404), so not registered.
