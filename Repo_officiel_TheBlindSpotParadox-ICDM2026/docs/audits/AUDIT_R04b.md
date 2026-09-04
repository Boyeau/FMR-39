# AUDIT — R04b, resolution of the efficiency crossing point (Appendix Figure A3)

Every measured block below is extracted from `logs/R04b_nu_refinement/exp_R04b_nu_refinement.log`
or from the captured `pytest` run. None is retyped.

**Starting state.** `AUDIT_R04.md` established that the submitted campaign never varied `Gamma`,
and that on a grid which genuinely spans, the delay ratio `ADD_Concept / ADD_Eco-L1` crosses unity
strictly inside `(7, 30)` — an interval R04's grid `{3, 4, 4.5, 5, 7, 30}` does not sample at all.
The `8.52` quoted there is a two-point interpolation across that void and was explicitly marked as
not publishable. `docs/DEVIATIONS.md` entry 14 recorded the crossing as indeterminate and deferred
it to a dedicated sweep. This is that sweep. R04 and all eight of its artefacts are untouched.

**Headline.** The crossing is located. `nu*(Eco-L1)` is enclosed by `[7, 9]` with 95% confidence
and estimated at `8.10` with interval `[7.78, 8.37]`; `nu*(Oracle)` is enclosed by `[4, 5]` and
estimated at `4.47` with interval `[4.31, 4.57]`. The estimation cost is `3.62` degrees of freedom,
interval `[3.31, 3.92]`, against the `0.3` v87 prints — an order of magnitude, and the interval
excludes the published value by a wide margin. **Case (A)**: R04's falsification of `nu* ~ 4.9`
holds and now carries a localization. The oracle crossing, by contrast, is the one claim of this
family that survives: v87's `4.6` lies inside its measured bracket.

**Two controls were found to be mis-specified in the same way, and both were corrected before
any result was read as final.** A threshold calibrated on a finite sample carries that sample's
error into every quantity later read at it. Omitting this doubles nothing and halves everything:
it made a correctly calibrated campaign fail a calibration control, and it made two compatible
campaigns fail a continuity control. Section 3 documents both, with the measurement that
establishes the mechanism. Neither correction touched a seed, a tolerance or a draw.

---

## 1. The four questions of the prompt

### 1.1 Between which two values of `nu` does the `Eco-L1` ratio cross unity?

Two brackets are reported and they are not the same statement.

```
Crossing estimators [Eco_L1]: (1) grid bracket [7.0, 8.0] -- model free, resolution limited, no
confidence attached. (1b) two-point interpolation inside it = 7.7465, R04's rule, kept for
comparability only. (2) inferential bracket [7.0, 9.0] -- the largest nu whose 95% ratio interval
is entirely below unity and the smallest whose interval is entirely above it; this is the statement
that carries confidence. (3) shape fit ratio = -0.360962 + 1.081884*1/(4 f_z(0)^2), weighted
R^2 = 0.990350, largest standardized residual 1.587, chi2 = 8.368 on 10 dof (p = 0.5929), inverted
at 8.0972. (4) analytic root of 1/(4 f_z(0)^2) = 1 at nu = 4.678793, a property of the innovation
law alone and therefore one number for both arms.
```

The **grid bracket** `[7, 8]` names the two adjacent measured points that straddle unity. It says
nothing about whether either point is distinguishable from unity, and it moves between draws.
The **inferential bracket** `[7, 9]` is the statement that carries confidence: at `nu = 7` the
ratio interval lies entirely below unity, at `nu = 9` entirely above it, and the crossing is
between them. **`[7, 9]` is the formulation that must govern any manuscript text.** v87's `4.9`
is far outside it.

The point estimate is `8.10`, interval `[7.78, 8.37]`, from a fit of the measured ratio against
the analytic shape across all twelve points. The model-free two-point interpolation gives `7.75`,
interval `[7.03, 8.32]`. Neither may be quoted without its interval.

### 1.2 The same for the oracle arm

```
Crossing estimators [Oracle_Eco]: (1) grid bracket [4.5, 5.0] ... (1b) two-point interpolation
inside it = 4.5267 ... (2) inferential bracket [4.0, 5.0] ... (3) shape fit ratio = -0.075012 +
1.107943*1/(4 f_z(0)^2), weighted R^2 = 0.985529, largest standardized residual 1.494,
chi2 = 11.839 on 10 dof (p = 0.2960), inverted at 4.4728.
```

Inferential bracket `[4, 5]`, point estimate `4.47` with interval `[4.31, 4.57]`, model-free route
`4.53` with interval `[4.35, 4.70]`. **v87's `4.6` lies inside the bracket** and inside the
model-free interval, though marginally outside the fit interval. The analytic prediction is
`4.678793`, which v87 prints as `4.7`; the oracle sits on it, which is the claim v87 makes about
that arm and the claim this campaign supports.

**The prompt's original eight-point grid could not have answered this question.** Over `[7, 30]`
the oracle ratio never approaches unity:

```
Monotonicity check (d): over [7, 30] the oracle ratio stays at or above 1.2536 at every point, so
it crosses unity nowhere on the interval the prompt's original grid covered, and no second crossing
exists on the extended grid.
```

The three low-`nu` points `{4, 4.5, 5}` were added for exactly this reason, and they also lift the
continuity control from two common points with R04 to five.

### 1.3 The estimation cost against the published `0.3`

```
Estimation cost nu*(Eco-L1) - nu*(Oracle): point estimate 3.6243 from the difference of the two
shape fits, paired bootstrap 95% interval [3.3085, 3.9222] over 2000 replicates in which both
curves invert. v87 prints 0.3. The model-free outer bound from the two inferential brackets is
[2.0000, 5.0000]: it treats two quantities that share their numerator and their streams as if they
were independent, so it is an outer bound and not a measurement.

Estimation cost, model-free route: difference of the two interpolated crossings = 3.2198, paired
bootstrap 95% interval [2.5228, 3.8245] over 2000 replicates in which both arms bracket a crossing.
This route assumes no functional form and is the one to quote if the affine fit is refused.
```

Three statements, in decreasing strength of assumption and all consistent: `3.62 [3.31, 3.92]`
from the shape fits, `3.22 [2.52, 3.82]` with no functional form assumed, and the model-free outer
bound `[2, 5]` from the two inferential brackets alone. **Every one of them excludes `0.3`.**

The intervals are paired: a bootstrap replicate resamples one set of streams and one calibration
sample, recomputes all three arms on them, and inverts both curves inside that replicate. The two
ratios share their numerator `ADD_Concept` and are measured on the same streams, so their common
noise cancels; treating the two crossings as independent, which is what interval arithmetic over
two brackets does, prices the cost roughly three times too wide.

**The mechanism R04 proposed is confirmed in direction and in magnitude.** R04 attributed the gap
to the persistence `Eco-L1` must estimate from 500 observations at `Gamma = 11.58`, where the
submitted campaign was in fact running at `Gamma = 1.105` with almost no persistence to estimate.
This campaign measures that cost at `Gamma = 11.58` and finds it an order of magnitude above the
published figure. It does not re-measure the `Gamma = 1.105` counterfactual, which R04 already
carries.

### 1.4 Do the interpolation and the analytic prediction agree?

They answer different questions, and the audit reports the distance rather than a verdict.

| arm          | interpolation (2)   | analytic (4) | distance |
| ------------ | ------------------- | ------------ | -------- |
| `Eco-L1`     | 7.75 `[7.03, 8.32]` | 4.678793     | 3.07     |
| `Oracle-Eco` | 4.53 `[4.35, 4.70]` | 4.678793     | 0.15     |

For the **oracle** the two agree to within the interval: the exactly standardized arm sits on the
Pitman prediction, which is what the prediction is about. For **`Eco-L1`** the distance is the
estimation cost itself, not a defect of the interpolation — the fitted arm is not the arm the
proposition describes.

The adequacy of the linear interpolation is a separate question and is answered separately. Within
the bracket the two estimators of the crossing — the two-point interpolation and the shape fit —
differ by `0.35` degrees of freedom for `Eco-L1` and `0.05` for the oracle, both inside their own
intervals. **On this grid the interpolation is adequate**; on R04's it was not, because there the
same rule interpolated across 23 units of `nu`.

---

## 2. What the campaign measures, and what governs each number

**Design.** Twelve `nu` in `{4, 4.5, 5, 6, 7, 8, 9, 10, 12, 15, 20, 30}`, three arms, `Gamma =
11.58`, `c = 0.5`, 2,000 streams per cell per pass, three passes (calibration, held-out null,
drift) — 72,000 monitored streams. The eight high-`nu` points are the prompt's; `{4, 4.5, 5}`
recover the oracle crossing and extend the continuity control; `{6}` refines the interval where
the `Eco-L1` inferential edge sits.

**A grid bracket is not an inferential bracket, and refining a grid does not by itself resolve a
crossing.** Near the crossing the ratio moves slowly against its own sampling error:

```
Resolution: near the fitted crossing the ratio moves by 0.044834 per unit of nu while its standard
error at the nearest grid point is 0.020569, so one standard error spans 0.46 units of nu. This is
why the primary estimate is a fit over twelve points and not an interpolation between two.
```

At R04's precision — where the standard error was understated by a factor of about 2.6, see
section 3.2 — one standard error would have spanned well over a unit of `nu`. Adding grid points
does not shrink the error at any single point; using the whole curve does.

**Order of precedence for any manuscript-facing statement**, in decreasing robustness:
the inferential bracket, then the shape fit with its bootstrap interval, then the grid bracket
and the two-point interpolation as diagnostics. No crossing is ever to be quoted as a point value
without its interval.

**Verdict register**, transcribed from the log. `held` means v87's value lies inside the interval
this campaign measures.

```
claim                                                | published    | regenerated                                                            | verdict
efficiency ratio crosses unity at nu* ~ 4.9          | 4.9          | inferential bracket [7.0, 9.0], fit 8.10 [7.78, 8.37]                  | not held
oracle arm crosses unity at nu* ~ 4.6                | 4.6          | inferential bracket [4.0, 5.0], fit 4.47 [4.31, 4.57]                  | held
finite warm-up costs 0.3 degrees of freedom          | 0.3          | 3.62 [3.31, 3.92]                                                      | not held
  the same cost by the model-free route              | 0.3          | 3.22 [2.52, 3.82]                                                      | not held
analytic crossing at 4.7                             | 4.7          | 4.6788                                                                 | held
ratio never exceeds the Gaussian ceiling pi/2        | <= 1.5708    | max 1.2546                                                             | held
AUDIT_R04.md interpolated 8.52 across the (7, 30) void | 8.52       | two-point interpolation on this grid 7.75                              | not held
```

The last line is the point of the experiment: `8.52` was an interpolation across an empty interval,
and the refined grid puts the same rule at `7.75` and the fit at `8.10`. **`8.52` must not be
quoted.**

**One observation that no claim of v87 covers.** The Gaussian ceiling `pi/2` is stated for the
`Concept / Eco-L1` curve, and that curve respects it. The oracle curve — the one Proposition
`prop:are` speaks about directly — does not:

```
Ceiling check: the largest Concept/Eco-L1 ratio is 1.2546, below the Gaussian ceiling
pi/2 = 1.5708 that v87 states for this curve. The Concept/Oracle-Eco ratio reaches 1.5810 at
nu = 20.0, above that ceiling and +9.1% against its own analytic prediction there. prop:are is an
asymptotic in the small-drift limit; c = 0.5 is not small, and the size of the departure is not
attributed here.
```

Reported, not gated, and **the cause is not established**. The proposition is an asymptotic in the
small-drift limit and this campaign runs at `c = 0.5`; whether that accounts for a 9% overshoot is
not something this design separates from any other explanation.

---

## 3. Two controls tested nulls their own procedure does not deliver

Both defects have one root: **a threshold calibrated on a finite sample carries that sample's error
into everything later read at it.** Both were found by a control firing, diagnosed rather than
worked around, and corrected in the specification of the control rather than in the draw. No seed,
no tolerance, no parameter and no grid point was changed in response to either.

### 3.1 Control (c): the held-out level of 36 arms

As first specified, control (c) tested each arm's held-out count against exactly 5%. It fired:

```
Calibration check (c), REPORTED and not gating: KS of the 36 one-sample p-values, each testing its
arm against exactly 0.05: D = 0.313568, p = 0.001209.
```

**It fires by construction, not by accident of the draw.** The bisection promises that the
in-sample rate lands within `0.003` of 5%; it does not promise that the true level at the selected
threshold *is* 5%. The held-out count therefore carries the binomial variance twice over — once
from its own draw, once from the calibration draw that placed the threshold. The factor is verified
inside the script, distribution-free, before any campaign value is read:

```
Pre-registered variance factor, verified distribution-free over 20000 replicates of
calibrate-on-2000, read-on-2000: held-out rate has standard deviation 0.006888 against 0.004873 for
a binomial at a KNOWN threshold, a ratio of 1.4133 against the sqrt(2) = 1.4142 a doubled variance
predicts. The inflation survives pooling, because each arm carries its own independent calibration
error, so it applies to the pooled interval as well as to the per-arm one.
```

Measured across the 36 arms the held-out spread is `0.007699`, against `0.004873` for a binomial
and `0.006892` for the doubled variance. The one-sample test omits half the variance of its own
statistic, so it must reject as `N` grows whatever the campaign does.

**The control was replaced by two halves that see different failures, both blocking.**

*Half 1, per-arm instability.* Each threshold is compared to itself: the count it produced on the
sample that chose it against the count it produced on a fresh one, conditionally, which removes the
unknown true level from the analysis.

```
Calibration check (c) HALF 1, per-arm instability: KS of the 36 conditional two-sample mid-p values
against Uniform(0,1): D = 0.119344, p = 0.640974 (GATING at p > 0.01).
```

*Half 2, common bias.* Half 1 conditions the level out, which is what makes it correctly specified
and also what makes it **blind to a bias shared by every arm** — if all 36 thresholds were
uniformly too high, both counts would move together and half 1 would see nothing. The pooled level
carries that half, with the factor 2 in its interval and the procedure's tolerance in its band:

```
Calibration check (c) HALF 2, common bias: pooled held-out level 0.050667 (3648/72000), 95%
interval 0.050667 +/- 1.959964*sqrt(2*0.050667*0.949333/72000) = 0.050667 +/- 0.002266 =
[0.048401, 0.052932]. Intersects the pre-registered band [0.047000, 0.053000]: True (GATING).
Contains 0.05: True (reported). The plain Wilson interval of a binomial would read
[0.049089, 0.052293], understating the half-width by the sqrt(2) established above.
```

The decomposition avoids double counting: **sampling uncertainty is carried by the interval**, with
the factor 2; **the procedure's tolerance is carried by the band**, alone, because it is systematic
and does not shrink under pooling. Both terms derive from `0.05`, `0.003`, `2000` and `36` and were
logged before the level was read. The literal predicate of the prompt — that the pooled interval
contain 5% — is computed and reported, and holds; it does not gate.

**Per-arm diagnostics, descriptive by construction** (preamble §S4bis requires the individual
p-values persisted and forbids using them as acceptance criteria):

```
Calibration diagnostic [Eco_L1]:     held-out level 0.0486, spread 0.006823, conditional KS D = 0.2602, p = 0.3313, distinct suprema 1.0000
Calibration diagnostic [Oracle_Eco]: held-out level 0.0488, spread 0.006341, conditional KS D = 0.1523, p = 0.9046, distinct suprema 1.0000
Calibration diagnostic [Concept]:    held-out level 0.0546, spread 0.008759, conditional KS D = 0.2503, p = 0.3763, distinct suprema 0.8681
```

The sign arm is the one whose null statistic is not continuous: 13% of its suprema tie in the band
where the threshold is chosen, because the sign stream takes two values and its CUSUM lives on a
lattice. Its held-out level sits at 5.46% against 4.86% and 4.88% for the two continuous arms.

```
Calibration diagnostic, residual excess NOT ATTRIBUTED: over all 36 arms the held-out spread is
0.007699 against the 0.006892 the doubled variance predicts, a ratio of 1.1171. At 36 arms the
standard error of an estimated standard deviation is about 12.0% of it, so the excess is of the
order of one such error. The coarseness of the bisection lattice, measured per arm above, is a
candidate explanation and is not established as the cause: no counterfactual in this campaign
separates it from ordinary sampling variation in a variance estimate.
```

### 3.2 Control (b): continuity with R04, and every interval in this experiment

The same omission, one level further in, and this one was consequential for the result rather than
only for a gate. The continuity control compares this campaign's delay ratios with R04's at the
five common points. On its first run it failed at `p = 0.0000`, with `z` scores of `-3.3`, `+1.0`,
`-2.1`, `-3.2`, `+2.4`.

The standard error used was a delta method **conditional on the calibrated threshold**. But the
delay is read at `lambda*`, and `lambda*` is itself estimated on 2,000 null streams. Measured
directly against R04, at the five common points:

| `nu` | `lambda_Eco` R04 | R04b   | difference | `lambda_Concept` R04 | R04b   | difference | ratio difference |
| ---- | ---------------- | ------ | ---------- | -------------------- | ------ | ---------- | ---------------- |
| 4    | 28.321           | 29.298 | +3.45%     | 8.790                | 8.790  | +0.00%     | −5.24%           |
| 4.5  | 25.880           | 26.368 | +1.89%     | 9.034                | 9.034  | +0.00%     | +1.51%           |
| 5    | 24.415           | 25.392 | +4.00%     | 9.400                | 9.400  | −0.00%     | −2.73%           |
| 7    | 21.485           | 22.218 | +3.41%     | 9.828                | 9.767  | −0.62%     | −3.89%           |
| 30   | 20.509           | 20.020 | −2.38%     | 10.743               | 10.743 | +0.00%     | +3.02%           |

The `Eco-L1` threshold moves by two to four percent between campaigns while the `Concept` threshold
lands on the same lattice point, so the ratio inherits almost all of that movement, and in four of
the five cells it moves in the opposite direction to the threshold, as a longer threshold and a
longer delay require.

**The bootstrap was rebuilt to resample both samples.** A replicate now resamples the calibration
streams and the drifted streams, re-runs the bisection on its own calibration resample to get its
own three thresholds, and reads its delays at those thresholds. To make that possible the drifted
pass records first passage at a ladder of thresholds around the calibrated one rather than at that
one alone; the ladder worker shares every line with `_worker_race` up to the reduction, and the two
are asserted equal at the centre of the ladder:

```
Worker identity check: over 50 streams at nu = 4.0, the centre rung of the ladder worker reproduces
_worker_race index for index on all four arms, so the two differ only in what they record.
Bootstrap threshold ladder: 0 of 72000 re-calibrated thresholds fell outside the ladder span 0.85
to 1.15 and were read at its edge.
```

The correction is large:

```
Bootstrap standard error of the delay ratio [Eco_L1] ... Against the delta-method error conditional
on the threshold, the inflation runs from 2.15 to 3.26, median 2.63.
Bootstrap standard error of the delay ratio [Oracle_Eco] ... the inflation runs from 1.72 to 2.86,
median 2.11.
```

**Every interval in this experiment uses the corrected error**: the inferential brackets, the
weights of the shape fit, the bootstrap intervals of both crossings and of the estimation cost, and
the continuity statistic. With it, continuity holds:

```
Continuity check (b) [Eco_L1]:     z at nu = 4.0: -1.094, 4.5: +0.300, 5.0: -0.765, 7.0: -1.282, 30.0: +1.102; omnibus sum z^2 = 4.7296 on 5 dof, p = 0.4498
Continuity check (b) [Oracle_Eco]: z at nu = 4.0: +0.083, 4.5: -0.334, 5.0: -1.387, 7.0: -1.013, 30.0: +0.875; omnibus sum z^2 = 3.8334 on 5 dof, p = 0.5736
```

**A consequence worth recording.** On the first run the shape fit was refused by its own
goodness-of-fit test (`chi2 = 55.97` on 10 dof) and the primary estimator was withdrawn. That
refusal was an artefact of the understated error, not curvature of the model: with the corrected
error the same fit gives `chi2 = 8.37` on 10 dof, `p = 0.5929`, weighted `R^2 = 0.990350`. An
understated error does not only narrow intervals — it also makes correct models look wrong.

### 3.3 Scope: this is not a defect of R04b

Any design that calibrates on one sample and measures on another carries this factor. That includes
the held-out level of any future stream and, potentially, any interval this repository places on a
quantity read at a calibrated threshold. **Whether R04's own control (c) is affected is a question
for an audit of R04, not for this one**, and it is posed here rather than settled: R04's control (c)
is in-sample by construction and its audit argues that this is what makes it admissible, which is a
different situation from the held-out design used here, but the interaction has not been analysed.

Recommended for the common preamble, **not applied here** — editing `PROMPT_REPO_COMMON_PREAMBLE.md`
is outside the remit of a single experiment:

> The out-of-sample level of a threshold calibrated on a finite sample has twice the binomial
> variance; any interval on that level must carry the factor, including after aggregation. More
> generally, any interval on a quantity read at a calibrated threshold must price the calibration
> error, and a bootstrap that resamples only the measurement sample does not.

---

## 4. Controls that were specified, ran, and held

- **Verbatim primitives.** Sixteen routines are copied from `exp_R04_isofpr_race.py` rather than
  hoisted into `experiments/common/`, which preamble §S4.2 forbids. The copies are asserted
  byte-identical at start-up by parsing both sources — a deterministic identity with no probability
  of firing under any null, and the check that actually addresses divergence between the two
  scripts, since the statistical continuity control resolves only a few percent per point.

  ```
  Verbatim-copy check: all 16 primitives are byte-identical to exp_R04_isofpr_race.py (14548
  characters compared).
  ```

- **The realised `Gamma`.** `solve_beta_for_gamma(alpha = 0.05, target_gamma = 11.58) = 0.930072`,
  and the closed form maps that back to `11.580000`. This is the check the submitted campaign
  lacked and the one that would have caught its transposed arguments on the first run.

- **Seeds.** 72,000 distinct 128-bit seeds over 72,000 tasks, zero collisions. Keys carry
  `("R04b", role, nu, stream)`; no common random numbers across `nu` or across roles.

- **In-sample calibration**, a convergence check rather than a test: all 36 arms within `0.003` of
  5%, achieved rates spanning `[0.0475, 0.0530]` over 7 to 14 bisection iterations.

- **QMLE.** 0 of 72,000 warm-ups failed on all three starts of the multistart ladder (budget 0.5%);
  0 fired the stationarity guard (budget 0%); 268 of 72,000 (0.3722%) returned
  `alpha + beta >= 0.999`, the optimiser's own feasibility boundary, and are kept as in R04.

- **Monotonicity (d)**, reported and not gated, as the prompt requires: Spearman `rho = 0.9930`
  (`p = 1.302e-10`) for `Eco-L1` and `0.9860` (`p = 4.117e-09`) for the oracle over twelve points.
  R04 gated on consecutive differences; at twelve points the consecutive steps are of the order of
  the sampling error by construction, so such a gate would test the draw rather than the shape.

- **Multiple testing.** 36 simultaneous 95% tests fire at least once with probability 0.8422 under
  the null, and 5 continuity tests with probability 0.2262. Both families are judged by one omnibus
  statistic each, at `p > 0.01`, as §S4bis requires. No per-cell gate exists anywhere in this
  experiment.

---

## 5. Reproducibility

Three consecutive runs at **different worker counts** produce byte-identical artefacts:

```
R04b_ratio_vs_nu.csv            : 1cdac74bb72e4a8bbf825ba26e6577de7691fd203f225fc6c21193717f553875
R04b_continuity_with_R04.csv    : 7015f506c59c72b59dafe4789aa801882c203ee2a5959f89cd59a775f640495d
figA03_nu_star_refinement.png   : a6d4b45167895acb95ec7d713d2d4e2d15c33deceee2e8cbf99432a2894a748f
R04b_claims.tex                 : 454f735d7c01dab8c508a69cb1a300e008cb8639544e15022e354b55f9069f27
```

Verified at 48, 20 and 12 workers. Measured cost 94.2 s on 48 workers, 198.0 s on 12, for 72,000
monitored streams over three passes plus 2,000 bootstrap replicates and a 20,000-replicate variance
probe.

R04 is untouched: `experiments/R04_isofpr_race/` and `results/R04_isofpr_race/` are unmodified and
the eight digests recorded in `AUDIT_R04.md` §6 still verify. `run_all.sh` and `run_tests.sh` are
not edited by this experiment.

The whole suite passes, 104 tests over R01 to R05 and R04b:

```
tests/test_R04b_claims.py::test_R04b_cardinality_and_grid PASSED
tests/test_R04b_claims.py::test_R04b_protocol_constants_match_v87 PASSED
tests/test_R04b_claims.py::test_R04b_gamma_target_is_attainable_and_realised PASSED
tests/test_R04b_claims.py::test_R04b_analytic_prediction_is_the_pitman_constant PASSED
tests/test_R04b_claims.py::test_R04b_in_sample_bisection_converged PASSED
tests/test_R04b_claims.py::test_R04b_pooled_holdout_level_meets_the_promised_band PASSED
tests/test_R04b_claims.py::test_R04b_conditional_calibration_pvalues_are_uniform PASSED
tests/test_R04b_claims.py::test_R04b_rates_are_consistent_and_clamped PASSED
tests/test_R04b_claims.py::test_R04b_continuity_anchors_are_read_from_R04 PASSED
tests/test_R04b_claims.py::test_R04b_is_compatible_with_R04_at_the_common_points PASSED
tests/test_R04b_claims.py::test_R04b_grid_bracket_straddles_unity_and_the_interpolation_lies_inside_it PASSED
tests/test_R04b_claims.py::test_R04b_inferential_bracket_is_recomputable_from_the_csv PASSED
tests/test_R04b_claims.py::test_R04b_bootstrap_error_exceeds_the_conditional_one PASSED
tests/test_R04b_claims.py::test_R04b_shape_fit_is_reported_with_its_goodness PASSED
tests/test_R04b_claims.py::test_R04b_analytic_crossing_matches_v87 PASSED
tests/test_R04b_claims.py::test_R04b_estimation_cost_interval_arithmetic PASSED
tests/test_R04b_claims.py::test_R04b_ratio_respects_the_gaussian_ceiling PASSED
tests/test_R04b_claims.py::test_R04b_oracle_ratio_does_not_cross_again_above_seven PASSED
tests/test_R04b_claims.py::test_R04b_macros_are_emitted_and_computed PASSED
tests/test_R04b_claims.py::test_R04b_no_nan_in_reported_quantities PASSED
tests/test_R04b_claims.py::test_R04b_report_against_v87 PASSED
============================= 104 passed in 1.00s ==============================
```

---

## 6. Impact on the manuscript and next actions

`sec:discussion`, the abstract, `sec:contributions` and the caption of `fig:isofpr` all carry
`nu^star ~ 4.9` and the `0.3` degrees of freedom. Nothing in the manuscript has been touched:
preamble §S4.1 forbids it, and the numbers a corrected campaign should carry are a decision for the
authors.

1. **`nu* ~ 4.9` is falsified with a localization.** The replacement formulation is the bracket:
   the crossing lies between `nu = 7` and `nu = 9`, estimated at `8.1` with interval `[7.8, 8.4]`.
   The abstract's "overtakes it below a measured `nu^star ~ 4.9` degrees of freedom, precisely
   where parametric estimation is most fragile" needs both the value and the gloss revisited: `8.1`
   is outside the moment singularity `nu < 8` the sentence appeals to, and the qualitative reading
   that the crossing sits where estimation is most fragile does not follow from a crossing at 8.1.
2. **The oracle crossing stands.** `4.6` lies inside the measured bracket `[4, 5]`, and the arm
   sits on the analytic `4.7`. The claim that the exactly standardized arm follows the Pitman
   prediction is the one this family of claims retains.
3. **`0.3` degrees of freedom becomes `3.6 [3.3, 3.9]`**, or `3.2 [2.5, 3.8]` with no functional
   form assumed. The sentence "the extra 0.3 degrees of freedom is what a finite warm-up costs the
   parametric route" is right in mechanism and wrong in magnitude by an order of magnitude.
4. **`8.52` must not be quoted** from `AUDIT_R04.md`. It was an interpolation across an empty
   interval; the same rule on the refined grid gives `7.75` and the fit gives `8.10`.
5. **`docs/DEVIATIONS.md` entry 14 has been rewritten** in terms of the measured brackets, and
   entry 16 appended for R04b. No entry was renumbered and none was inserted mid-register.
6. **Recommended, not applied:** the register's sequential numbering is fragile under exactly this
   kind of transversal correction — an entry edited by a later experiment keeps a number that other
   sections already cite. Final assembly should replace the numbers with stable identifiers
   (`R04-nu-star`, `R02b-iid-arm`, `R01-variance-target`). This touches every file that cites the
   register and belongs to assembly, not to one experiment.
7. **Open question for an audit of R04**, posed and not settled here: whether the variance factor
   of §3.3 affects any interval R04 publishes.

Files to transmit for review: `experiments/R04b_nu_refinement/exp_R04b_nu_refinement.py`,
`tests/test_R04b_claims.py`, `run_experiment_R04b.sh`, `docs/sections/R04b.md`,
`requirements/R04b.txt`, `logs/R04b_nu_refinement/exp_R04b_nu_refinement.log`, the two CSVs, the
figure and `R04b_claims.tex` under `results/R04b_nu_refinement/`, and the diff of
`docs/DEVIATIONS.md`.
