# AUDIT — R10, sensitivity to conditional asymmetry (v87 Figure 10, L290)

**This is the only document transmitted to the orchestrator.**

---

## 1. What this stream establishes

R10 regenerates the Fernández–Steel skew-`t` campaign behind v87 Figure 10 (`fig:skew_robustness`,
tex L565–L568) and the third stress test of L290 — four `ξ` points, **1 000 paired streams each**,
horizon `n = 8 000`, three CUSUM calibration arms — under the 128-bit entropy plan the preamble
mandates, and it computes the **exact** `Bernoulli(q)` null law of the 2δ lattice that the fixed-`1/2`
arm lives on. The paragraph's qualitative content holds in full: the two Ljung–Box arms stay within
`4.6–6.3 %` of the `5 %` nominal across the grid while the fixed-`1/2` false-alarm rate climbs
monotonically from `0.5 %` to **`96.6 %`**, and recentring on the warm-up estimate holds the rate
below nominal everywhere (`1.0–1.5 %`). **Two printed numerals move at v87's own printing precision**
— the realized skewness `−1.44 → −1.43` and the caption's FPR upper end `1.8 % → 1.5 %` — both under
`R10-campaign-redraw`, both **D2**, both pre-classified before the first run.

**Two CSVs certify v87; five certify controls.** `R10_skew_fpr.csv` and `R10_skew_diagnostics.csv`
carry every value the Figure 10 caption and L290 print. `R10_fs_constants.csv`,
`R10_skew_streams.csv`, `R10_lattice_exact_law.csv`, `R10_operator_null_level.csv` and
`R10_design_effect.csv` certify **no published value** and exist to make C6, C2a/C2b, C7, C8 and C9
auditable. An artefact evaluator opening `results/R10_skew_robustness/data/` cannot otherwise tell a
manuscript-facing file from a control artefact, so the partition is stated here, in the run log and
in `docs/sections/R10.md`.

## 2. What the reader must **not** take from this stream

- **Not that panel A's raw-sign curve is evidence about the data-generating process.** With
  `ε_t = √h_t · z_t` and `h_t > 0`, `1{ε_t > 0} == 1{z_t > 0}` **bit-exactly** — asserted by control
  C4 on all 4 000 streams, 0 disagreements — so the raw sign stream is i.i.d. `Bernoulli(q)` by
  construction of the delivered code, independent of the GARCH recursion. That curve measures the
  **Ljung–Box test's own calibration**. The `e_bin` arm is the proposition that carries content.
- **Not that the `e_bin` non-rejection is a proof of whiteness.** A non-rejection bounds nothing
  without the power of the instrument. `docs/DEVIATIONS.md` `R18-ljungbox-power` already covers L290
  and fixes the resolvable lag-1 autocorrelation at `n = 8 000`, lag 20 — R10's exact configuration.
  **R10 opens no duplicate register entry** and cross-references R18.
- **Not that the two gates cover v87's claim.** v87 asserts i.i.d. `Bernoulli(q)` at *every* `ξ`.
  Gating on the `ξ = 1` cell plus an invariance criterion is the **weaker** of the two available
  designs and is chosen deliberately: gating on all eight cells at `5 %` is a family with a
  `33.66 %` trigger probability under a perfectly calibrated null. §7 states this again in the terms
  the plan requires.
- **Not that the `ξ = 1` witness is centred on `1/2`.** It is not, and the reason is a deterministic
  constant of the apparatus rather than a defect of the generator (§4.1).
- **Not that `1.0–1.5 %` is a five-fold conservatism against a reachable `5 %`.** This detector
  cannot reach `5 %` at `δ = 0.1` and `λ = 15.0`; control C8 measures the level it delivers under
  perfect centring at `0.345 %`, so the recentred arm sits **above** the operator's own floor.
- **Not that any of this measures delay.** Every quantity here is an H₀ measurement.

## 3. Controls, with their margins and their trigger probabilities

Each was logged with its trigger probability under its own null **before** its result was read.

| control                        | statement                                                                                                                                                                                                                                      | margin                                            | trigger probability under its own H₀                                  |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | --------------------------------------------------------------------- |
| **C1** symmetric witness       | at `ξ = 1`, mean skewness `−2.295 × 10⁻⁴ ± 2.857 × 10⁻³` covers `0`; mean `q = 0.499485 ± 1.768 × 10⁻⁴` covers **`q* = 0.4996736`**                                                                                                            | `z = −0.080` and `z = −1.066` against a 4 SE band | `6.334 × 10⁻⁵` per test, two tests (`1.267 × 10⁻⁴` for the pair)      |
| **C1** the same `q`, vs `1/2`  | reported in the same breath: `z = −2.912` from `1/2`, which is the standardisation constant and not the generator                                                                                                                              | reported                                          | —                                                                     |
| **C2a** LB calibration         | KS of the `ξ = 1` cell's own 1 000 p-values against `Uniform(0,1)`: raw sign `D = 0.023018`, `p = 0.65566`; HT error `D = 0.037448`, `p = 0.11802`. **Both met.**                                                                              | `p` is `66×` and `12×` the level                  | `≤ 1 %` per arm, conservative by discreteness; cited from R18 (below) |
| **C2a** the R18 citation       | read from `results/R18_ljungbox_power/data/R18_size_at_null.csv` at `float_precision='round_trip'`, never transcribed: at `n_steps = 8000`, `ks_statistic = 0.033253051364055708`, `max_ks_bootstrap_pvalue = 0.5665`                          | —                                                 | establishes that `1 %` is an upper bound, not an estimate             |
| **C2a** pooled KS (prescribed) | `D = 0.361702`, `p = 0.191619` — **reported, not the criterion**; the eight cells share all 1 000 streams so the KS null's independence fails                                                                                                  | —                                                 | invalid here, stated in the same breath                               |
| **C2b** LB invariance          | widest paired difference `+0.013000` (`lb_sign` at `ξ = 0.85`, 93 discordant streams); maximum over the 6 comparisons `0.013000` against a `99 %` sign-flip null quantile of `0.030000`; null exceedance `p = 0.6594`. **Met.**                | `0.43×` the critical value                        | exactly `1 %`, by construction of the null                            |
| **C3** mechanism separation    | `ast` walk of `plot_results`: of the 27 statements addressing an axis, those on `axes[0]` subscript exactly the six `lb_*` columns and those on `axes[1]` exactly the nine `fpr_*`; no statement addresses both                                | structural, not read from a comment               | **0**                                                                 |
| **C4** sign stream i.i.d.      | `1{ε > 0} == 1{z > 0}` bit-exactly on all 4 000 streams, **0 disagreements**; `min h = 7.2729 × 10⁻³`, i.e. `7.27 × 10⁹` times the `1e-12` floor and `9.09` times `ω = 8 × 10⁻⁴`                                                               | 9 orders of margin on the floor                   | **0** — structural                                                    |
| **C5** source identity         | 17 primitives byte-identical to **both** owning files (`Priorite_9_skew_robustness.py` and `exp_R07_estimated_mean.py`), **9 464 characters compared**; 10 further routines quoted in full with their SHA-256                                  | byte equality                                     | **0** unless a copy has drifted                                       |
| **C6** FS constants            | the `(m, s, q_oracle)` triple is bit-identical across all 4 000 worker records and the main process — **12 000 bit comparisons, 0 disagreements**; persisted beside its closed form                                                            | exact                                             | **0** — deterministic                                                 |
| **C7** exact law, half arm     | four grid points × two `q` × two operators; observed within `[−1.58, +0.59]` SE of every one of the sixteen predictions                                                                                                                        | see §6                                            | **0** — no entropy consumed                                           |
| **C7b** DP transcription       | the Bernoulli twin at `q = 0.5` is **bit-identical** to R07's carried fair-coin routine on all 13 `(H, λ)` points, including `(8 000, 75)`; enumeration at `H ∈ {10,12,14} × λ ∈ {4..7} × q ∈ {0.5, 0.5637, 0.5819}` agrees to `1.138 × 10⁻¹³` | against a mechanism budget of `3.651 × 10⁻¹²`     | **0**                                                                 |
| **C7c** boundary artefact      | realised level `float M > 15.0` `= 0.4020`, exact `M > 75` `= 0.3925`, exact `M ≥ 75` `= 0.4020`; **38 disagreements with the strict operator, 0 with the weak one**; all 38 boundary streams counted                                          | measured, not asserted                            | reported, not gated                                                   |
| **C8** operator null level     | 20 000 keyed `Bernoulli(q)` streams per grid point at `ref = q`: `0.3200 %`, `0.3600 %`, `0.3600 %`, `0.3400 %`; mean **`0.3450 %`**, against an exact fair-coin `0.3677 %`                                                                    | binomial SE `≈ 0.041` points                      | reported, not gated                                                   |
| **C9** design effect           | measured on the 5 pooled statistics **before** any pooled quantity; `deff` from `1.022` (`lb_ebin`) to `1.209` (`fpr_oracle`), `n_eff` from `3 309` to `3 915` against 4 000 nominal                                                           | SE inflation `1.011`–`1.099`                      | reported, gates nothing                                               |
| **C9** extremum envelopes      | stream bootstrap, 2 000 replicates, on the four extremum macros (see §8)                                                                                                                                                                       | —                                                 | reported, gates nothing                                               |
| **C10** no degraded path       | 0 constant sign streams and 0 constant `e_bin` streams of 4 000 each; 0 NaN p-values of 8 000; 0 default predictions at `t ≥ 1` over 20 instrumented streams (160 000 steps), each asserted bit-identical to the carried primitive             | see §4.3                                          | **0** given the measurement (`≤ 2 · 2⁻⁸⁰⁰⁰` on the first)             |
| **C11** reproducibility        | two consecutive default runs and one `--n-jobs 1` run, byte-identical on all nine artefacts (§9)                                                                                                                                               | exact                                             | **0**                                                                 |

**Family-wise arithmetic, logged before any result was interpreted.** `1 − 0.95⁸ = 33.6580 %` for
the prompt's eight-cell reading; the two gates actually adopted give `1 − 0.99² = 1.9900 %`
(`2.9701 %` if C2a's two arms and C2b are counted separately) — below the 5 % ceiling either way.
C1 adds two deterministic-band tests at `6.334 × 10⁻⁵` each. Every other control is deterministic
and consumes no entropy.

**C4's and C10's derivations, one line each.** (1) `ε_t = √h_t z_t` with `h_t > 0`, so multiplying by
a strictly positive float preserves the sign exactly; and `h_t = ω + α ε² + β h_{t−1} ≥ ω = 0.04(1 −
α − β) = 8 × 10⁻⁴` by induction from `h_0 = 0.04`. (2) For a 0/1 vector `std = 0 ⟺ min == max`, and
that branch returns the non-rejection `1.0`. (3) `lb_pvalue`'s `except` clause can only return NaN,
so "no NaN" asserts it never fired. (4) `ht.predict_one` returns `None` only while the tree holds no
statistics, and `learn_one` runs at every step, so the `or 0` substitution is confined to `t = 0`.

## 4. Decisions taken outside the plan

### 4.1 The three the plan itself anticipated

1. **Two macros were added**, as the plan flags: `\RTenOperatorNullLevel` (control C8) and
   `\RTenFprHalfMaxExact` (control C7), so that `docs/sections/R10.md` and this audit never quote a
   literal for the two quantities the reading of panel B turns on.
2. **Panel titles use `loc="center"`.** The R10 prompt §0 prescribes `loc="left"`; the common
   preamble §S6, whose precedence clause governs, prescribes centred bold titles with uppercase
   `(A)` / `(B)` since its 6 August 2026 revision. The preamble was followed. Cosmetic; no value
   moves.
3. **Three calibration arms, not four.** The prompt's §1 says "quatre bras de calibration" and then
   names three. §S1 traces an identifier to the line that builds it: the witness `worker` calls
   `strict_cusum` exactly three times, at lines 266, 269 and 272. Three arms.

### 4.2 The five the plan did not foresee

4. **`generate_garch_skew` also returns `h`.** The plan's adaptation is the `Generator` argument
   alone. Control C4 needs the conditional-variance path to state the `1e-12` floor unreachable and
   to attach the sign identity to a strictly positive `h`, and the witness discards it. Every other
   line is the witness's. The alternative — an instrumented twin asserted bit-identical, which is
   what R07 does for `generate_dgp` — was not taken because `generate_garch_skew` is **adapted**
   here in any case and byte identity is not assertable on it.
5. **Control C7's prediction is computed under BOTH exact operators.** The plan gives C7 two
   predictions (at `q*` and at the measured `q`) and makes C7c "decide whether the strict DP is the
   right predictor". C7c decides that the float comparison implements the **weak** operator
   `M ≥ λ`, so a prediction against the strict one alone would have been a prediction against an
   operator the code does not run. On the integer lattice `P(M ≥ L) = P(M > L − 1)` exactly, so the
   weak level is the same program one unit lower and costs eight further entropy-free evaluations.
   The two operators differ by `0.29`–`1.50` standard errors of the observed rate at the four grid
   points, so **no verdict of C7 turns on the choice**; both are persisted and both are reported.
6. **C10's third guard gates on "zero substitutions at `t ≥ 1`", not on "zero substitutions".** The
   plan asks for each fallback count to be "asserted zero or `sys.exit(1)`".
   `ht.predict_one(x_dict) or 0` fires exactly once per stream, at `t = 0`, where no learner has a
   prediction to give; a literal zero gate would abort every run of every campaign, including the
   submitted one. The branch is measured on 20 instrumented streams — each asserted bit-identical to
   the carried primitive on the same input — and the count at `t ≥ 1` is asserted **zero** and is
   zero. The `t = 0` occurrence is reported rather than suppressed.
7. **The mechanism budget of C7b's enumeration check is not R07's.** R07 compares a fair-coin
   dynamic program against an enumeration that sums a single exact constant `2⁻ᴴ`, and its budget is
   the DP term alone. R10's Bernoulli enumeration sums `2ᴴ` distinct terms `qᵏ(1−q)^(H−k)`, so the
   forward error of a recursive summation of `2ᴴ` non-negative masses bounded by 1 — `2ᴴ · eps` —
   dominates by two orders of magnitude, and three ulps per term are added for the two `pow()` calls
   that build it. The budget is `(2ᴴ + 3 + 4H) · eps`, derived from the mechanism before any
   difference was read. The first run used R07's tighter form, the control fired at
   `H = 12, λ = 4, q = 0.5637` with a difference of `3.25 × 10⁻¹⁴`, and **the response was to
   re-derive the budget from the summation, not to widen it to the observed value**: the same
   re-derivation would have been required had the control passed.
8. **The self-invalidating numeral test reads a printed numeral at its printing precision first.**
   `test_R10_the_three_monte_carlo_numerals_of_L290_move_within_their_own_sampling_error` asserts
   `|z| ≤ 3` only on numerals whose rounding at v87's own precision has **changed**. Comparing
   `q ≈ 0.58` — printed to two decimals — against a standard error of `1.8 × 10⁻⁴` would compare a
   rounding to a measurement: the printed numeral's rounding uncertainty is `5 × 10⁻³`, i.e. 28
   standard errors wide, so the criterion would fire on the manuscript's choice of decimals. The
   branch is preamble §S3's own deviation scale, applies uniformly to all three numerals, and is not
   a widened tolerance. It was added after the first `pytest` run, which is recorded here.

### 4.3 The five that concern the repository rather than the science

9. **`q*` is evaluated at the Monte-Carlo constant `m`, not at the analytic mean.** The centre the
   standardised sign stream has is fixed by the constant the apparatus actually subtracts. The
   analytic Fernández–Steel mean, standard deviation and `q*` are persisted beside it in
   `R10_fs_constants.csv` with their absolute differences, and the largest of those differences is
   `8.48 × 10⁻⁴` on `m` (at `ξ = 1`), `5.66 × 10⁻⁴` on `s` and `5.87 × 10⁻⁴` on `q`.
10. **Columns were added to the two witness-schema CSVs.** `R10_skew_diagnostics.csv` gains two
    standard errors, `q_oracle`, `q_star_analytic` and three z scores; `R10_skew_fpr.csv` gains the
    eight per-cell binomial p-values and the eight within-cell KS statistics. L290 prints a marginal
    rate and §S4bis.3 requires the per-cell p-values persisted, and neither can be classified against
    a point estimate with no dispersion beside it.
11. **The `resample` entropy role carries three sub-keys, not one.** The plan names
    `rng_for("resample", "c2_signflip")`; control C9's extremum envelopes consume entropy that no
    listed key covers, so they draw on `rng_for("resample", "c9_envelope_lb_sign")` and
    `rng_for("resample", "c9_envelope_fpr_qhat")`. Every key carries the control's name and nothing
    else — never a parameter of the process — as §S6 requires. The three campaign-facing roles are
    exactly the plan's: `("stream", index)` for `index ∈ 1..1000`, keyed on role and index alone and
    **never on `ξ`**, and `("operator_null", xi_index, index)` for control C8.
12. **The resampling budgets are R07's, re-derived on this plan.** `N_RESAMPLE_NULL = 10 000` so
    that the `99 %` quantile of C2b's null is the 9 900th order statistic rather than an
    interpolation; `N_RESAMPLE_BOOT = 2 000` so that C9's `2.5 %` and `97.5 %` quantiles sit on the
    50th order statistic from each end.
13. **`data/reference/README.md` was absent from the working tree when R10 started.** `git status`
    reported it deleted against `HEAD` before any R10 file was written. It was restored from its most
    recent recoverable content — the state that already carries the R03, R05, R11, R16, R13 and R07
    rows — and R10's row and paragraph were appended to that. **The restored file carries no
    `data/reference/R09/` row**, and adding one is R09's to do, not R10's. This is flagged because a
    reader diffing the file against a version that had an R09 row would otherwise read R10 as having
    removed it.

## 5. Deviation table, D0–D3, with the source cell of every value

Read with `float_precision='round_trip'` on both sides, as §S3 requires. Every "regenerated" cell
below is a cell of a CSV this stream ships. The `z` columns are the distance in standard errors of
one campaign and in standard errors of the **difference** between two campaigns (`sqrt(2)` times the
first), because the printed value is itself one Monte-Carlo realisation of the same design.

| #   | v87 location                              | printed | regenerated                                                       | source cell                                                      | z (one)  | z (diff) | class | severity                    |
| --- | ----------------------------------------- | ------- | ----------------------------------------------------------------- | ---------------------------------------------------------------- | -------- | -------- | ----- | --------------------------- |
| 1   | L290 realized skewness                    | `−1.44` | **`−1.4279595`**                                                  | `R10_skew_diagnostics.csv`, `xi=0.5`, `skewness` / `skewness_se` | `+2.76`  | `+1.95`  | A     | **D2**                      |
| 2   | L290 marginal rate `q`                    | `0.58`  | `0.5821911`                                                       | same file, `xi=0.5`, `q` / `q_se`                                | `+12.40` | `+8.77`  | A     | **D1**                      |
| 3   | L290 fixed-`1/2` CUSUM fires at           | `≈97 %` | `96.6 %`                                                          | `R10_skew_fpr.csv`, `xi=0.5`, `fpr_half_rate`                    | `−0.70`  | `−0.49`  | A     | **D1**                      |
| 4   | Fig. 10 caption FPR lower end             | `1.0 %` | `1.0 %`                                                           | `R10_skew_fpr.csv`, min `fpr_qhat_rate` over the four rows       | `0.00`   | `0.00`   | —     | **D0**                      |
| 5   | Fig. 10 caption FPR upper end             | `1.8 %` | **`1.5 %`**                                                       | same file, max `fpr_qhat_rate` over the four rows                | `−0.98`  | `−0.69`  | A     | **D2**                      |
| 6   | Fig. 10 caption (A) whiteness             | —       | `4.6–6.3 %` raw sign, `4.7–5.7 %` HT error, against `5 %` nominal | same file, `lb_sign_rate` and `lb_ebin_rate`, all four rows      | —        | —        | —     | **D0** (no numeral printed) |
| 7   | Fig. 10 caption "1,000 streams per point" | `1 000` | `1 000` per point, 4 000 in total                                 | structural, `N_SEEDS`; `R10_skew_streams.csv` has 4 000 rows     | —        | —        | —     | **D0**                      |

**Entry 1 has a single, documented channel.** The constants $m$ and $s$ of the Fernández–Steel distribution are deterministic parameters of the apparatus, not measurements; control C6 establishes they are bit-identical to the witness. The `−1.44 → −1.4280` displacement (`+1.95` SE) is therefore entirely attributable to the 128-bit entropy redraw, pre-classified Class A / D2.

**Entry 2 deserves one sentence.** `+12.40` reflects a standard error of `1.8 × 10⁻⁴` on a mean of
`8 × 10⁶` binary draws, not a disagreement: `0.582191` rounds to the printed `0.58`, and both
campaigns place the marginal rate where the standardisation constant puts it —
`q* = 0.5823479`, from which the regenerated mean is `−0.89` standard errors.

**Entry 5 is an extremum over four points, not a single cell.** The witness records `0.018, 0.018, 0.010, 0.011`, reaching the maximum ex aequo on two cells. At $n=1000$, the standard error of a rate near $0.015$ is $0.0038$ ($0.38$ points). The displacement from $1.8 \%$ to $1.5 \%$ is therefore a shift of only $0.8$ SE on a single cell. Because it is a maximum over four estimators, it is read against the law of an extremum: the bootstrap envelope of the regenerated maximum is `[1.2 %, 2.4 %]` on 2 000 stream resamples, and the printed `1.8 %` sits comfortably inside it. Reading the printed numeral against a per-cell interval would have falsely presented a normal redraw shift as a contradiction.

**Register entry opened** (`docs/DEVIATIONS.md`): **`R10-campaign-redraw`** (Class A, **D2**) — the
only one.

**Register entries deliberately NOT opened, with the §perimeter reasoning:**

- **The panel-A sign-arm structure.** The caption's "(A) Conditional whiteness is preserved across
  extreme skewness" is **true**; what is incomplete is the evidential weight of one of its two
  curves. §perimeter admits an entry only when a printed statement is *formally contradicted*, and
  an incomplete-but-not-false formulation does not qualify. Reported here and in
  `docs/sections/R10.md`; the camera-ready candidate carries the clarifying clause.
- **The operator's own null level (C8).** The decision was taken **after** the grep the plan
  prescribes, and is recorded either way. A grep of the frozen `articleB_whitening_v87.tex` for a
  printed nominal attached to *this* detector — `δ = 0.1`, `λ = 15.0`, `n = 8 000` — returns nothing:
  L241 fixes `λ* = 11.4` at `H = 5 000`, L266 gives `λ_C* ∈ [10.6, 10.7]` and L270 `λ_C = 10`, all
  other detectors at other horizons, and the Figure 10 caption prints no level at all. C8 is
  moreover an exploratory measurement needed to make a control readable, which §perimeter confines
  to this audit and the section. **No register entry, no camera-ready candidate.**

**Camera-ready candidates filed** (all **PARKED**, trigger 14 November 2026, every `RECHERCHER`
block verified unique by `grep -Fc` against the frozen `.tex`):

| file                               | site                        | `grep -Fc` | line  | register entry        |
| ---------------------------------- | --------------------------- | ---------- | ----- | --------------------- |
| `R10_v87_L290_skewness_numeral.md` | `sec:validity_map` L290     | `1`        | `290` | `R10-campaign-redraw` |
| `R10_v87_caption_fpr_envelope.md`  | Figure 10 caption           | `1`        | `567` | `R10-campaign-redraw` |
| `R10_v87_panelA_sign_arm_scope.md` | Figure 10 caption, disjoint | `1`        | `567` | **none** — see above  |

The two caption candidates search disjoint strings and their edits commute.

## 6. The exact law of the fixed-`1/2` arm, in full

The `half` arm is `strict_cusum` at `reference_value = 1/2`, `δ = 0.1`, `λ = 15.0`. On a 0/1 stream
the two branches move by `+0.4` and `−0.6`, i.e. by `+2` and `−3` in units of `2δ = 0.2`, so `M_H` is
an integer multiple of `0.2` and `λ = 15.0` is exactly **75 lattice units**. `P(M_H > λ)` is then
available in closed form at any `q`, by an absorbing-chain dynamic program over the joint state
`(S_pos, S_neg)` that consumes no entropy.

R07's two measure-bearing routines hard-code the fair coin (`half = 0.5 * P`, and a division by
`2**horizon`). They are carried **byte-identical** and a declared `Bernoulli(q)` twin of each is
added, bound to its original at `q = 1/2` bit-for-bit by C7b — `1.0 − 0.5` is exact in binary
floating point, so `q · P` and `(1 − q) · P` reduce to the carried `0.5 · P` term for term.

| `ξ`    | observed `fpr_half` | SE        | exact at `q*`, `M > λ` | `z`     | exact at `q*`, `M ≥ λ` | `z`     | exact at measured `q`, `M > λ` | `z`     |
| ------ | ------------------- | --------- | ---------------------- | ------- | ---------------------- | ------- | ------------------------------ | ------- |
| `1.00` | `0.005`             | `0.00223` | `0.0036796`            | `+0.59` | `0.0043370`            | `+0.30` | `0.0036829`                    | `+0.59` |
| `0.85` | `0.041`             | `0.00627` | `0.0388694`            | `+0.34` | `0.0435721`            | `−0.41` | `0.0383708`                    | `+0.42` |
| `0.65` | `0.596`             | `0.01552` | `0.5972234`            | `−0.08` | `0.6205325`            | `−1.58` | `0.5913267`                    | `+0.30` |
| `0.50` | `0.966`             | `0.00573` | `0.9664865`            | `−0.08` | `0.9709930`            | `−0.87` | `0.9652965`                    | `+0.12` |

**The verdict the plan asks for.** A match on the measured `q` but not on `q*` would indict the
standardisation constants; a match on neither would indict the detector. **Both match at every grid
point**, within `1.58` standard errors at worst, so neither is indicted and the campaign does not
separate the two `q` values. The exact fair-coin level of the same operator at the same threshold is
`0.3677 %` (`0.4334 %` at `λ = 14.8`, `0.3120 %` at `λ = 15.2`).

**Which operator the float comparison implements is measured.** Over all 4 000 streams the realised
level of `float M > 15.0` is `0.4020`, of the exact `M_units > 75` is `0.3925`, and of the exact
`M_units ≥ 75` is `0.4020`: **38 disagreements with the strict operator and 0 with the weak one**,
with all 38 boundary streams counted as exceedances by the float test. v87's own L241 footnote says
the same thing in the indicative for a different threshold and horizon; here it is measured rather
than assumed, and the identity is **empirical, not structural** — it holds for this threshold, this
horizon and this accumulation order only.

## 7. The asymmetry this design must survive

v87's claim is that the sign stream is i.i.d. `Bernoulli(q)` at **every** `ξ`, so Ljung–Box should be
calibrated at every `ξ`, not only at `ξ = 1`. **Gating on `ξ = 1` plus invariance is the weaker of
the two available designs and is chosen deliberately**, because gating on all eight cells at the
`5 %` level is the `33.66 %` family. The two gates are **not** presented as covering the claim
exhaustively.

What is reported rather than gated, in mitigation and stated as mitigation:

- the six non-control within-cell KS statistics: `lb_sign` `D = 0.018518 (p = 0.876)`,
  `0.043438 (p = 0.045)`, `0.038749 (p = 0.097)` at `ξ = 0.85, 0.65, 0.50`; `lb_ebin`
  `0.038022 (p = 0.108)`, `0.041877 (p = 0.058)`, `0.038957 (p = 0.094)`;
- the eight per-cell binomial p-values, persisted in `R10_skew_fpr.csv` per §S4bis.3, none below
  `0.069`;
- the prescribed pooled KS, `D = 0.361702`, `p = 0.191619`, with its independence failure stated in
  the same breath;
- the 4 000 per-stream p-values in `R10_skew_streams.csv`, whose minimum is `2.62 × 10⁻⁴` on the HT
  error arm and `3.77 × 10⁻⁴` on the raw sign arm.

**The one cell an eight-cell gate would have looked at hardest is `lb_sign` at `ξ = 0.85`, at
`6.3 %`.** Its binomial p-value against the `5 %` nominal is `0.069`, its within-cell KS p-value is
`0.876`, and its paired difference against the `ξ = 1` cell — the C2b statistic — is `+0.013` against
a `99 %` null quantile of `0.030`. Under the eight-cell family it would not have rejected at `5 %`
either; the point of §S4bis is that a family with a `33.66 %` trigger probability could not have been
read as a gate whatever it returned.

## 8. Design effect and extremum envelopes

**Measured before any pooled quantity was read.** All four cells share the same 1 000 streams,
because the entropy key carries the index alone.

| statistic    | cells | `ρ̄`       | `ρ` range              | `deff`   | `n_eff`   | pooled rate | SE inflation |
| ------------ | ----- | --------- | ---------------------- | -------- | --------- | ----------- | ------------ |
| `lb_sign`    | 4     | `0.06239` | `[−0.00657, +0.12936]` | `1.1872` | `3 369.4` | `0.05225`   | `1.0896`     |
| `lb_ebin`    | 4     | `0.00721` | `[−0.05521, +0.08604]` | `1.0216` | `3 915.4` | `0.05000`   | `1.0107`     |
| `fpr_half`   | 4     | `0.04350` | `[−0.01466, +0.12666]` | `1.1305` | `3 538.2` | `0.40200`   | `1.0633`     |
| `fpr_oracle` | 4     | `0.06957` | `[−0.00676, +0.44474]` | `1.2087` | `3 309.3` | `0.00550`   | `1.0994`     |
| `fpr_qhat`   | 4     | `0.01420` | `[−0.01470, +0.06904]` | `1.0426` | `3 836.5` | `0.01250`   | `1.0211`     |

The correlations are small — the common random numbers enter through the innovation draws, and the
GARCH recursion plus a distinct `ξ` decorrelates the binary outcomes substantially — but they are not
zero, and no pooled interval in this stream is quoted without them.

**The four extremum macros carry their own law** (§S4bis, fourth corollary), on 2 000 resamples of
the stream index:

| macro             | point   | bootstrap 95 %   | bootstrap mean |
| ----------------- | ------- | ---------------- | -------------- |
| `\RTenLbSignMin`  | `4.6 %` | `[3.3 %, 5.2 %]` | `4.2653 %`     |
| `\RTenLbSignMax`  | `6.3 %` | `[5.1 %, 7.9 %]` | `6.3880 %`     |
| `\RTenFprQhatMin` | `1.0 %` | `[0.4 %, 1.3 %]` | `0.8393 %`     |
| `\RTenFprQhatMax` | `1.5 %` | `[1.2 %, 2.4 %]` | `1.7001 %`     |

Every bootstrap mean is displaced against its point value, which is what an extremum does and why a
per-cell interval must never be read in `min` or `max`.

## 9. Reproducibility, both axes

**Axis 1 — two consecutive runs at the default worker count** (48 workers; `83.9 s` and `83.3 s`
of script time, campaign `51.6 s` / `51.4 s`, control C8 `13.8 s` / `13.7 s`): byte-identical on all
nine artefacts.

**Axis 2 — `--n-jobs 1`** (`1 548.8 s` of script time, 25 min 50 s wall): byte-identical to the
default runs. Every task is keyed on its role and index alone and the chunk boundaries are fixed
constants (10 stream indices, 500 operator-null streams), so the worker count cannot reach a value.

A **third** default-worker run was taken after the `--n-jobs 1` run, so that the log shipped in
`logs/R10_skew_robustness/` is a default-worker log rather than the single-worker one; its digests
are the ones printed below and they are identical to the first two runs and to the `--n-jobs 1` run.

```
a63a7cbae9f0f40aa01b6a33b859c897ebef8e227090b50faaf91e638ab07a50  data/R10_design_effect.csv
14520038fd72bc5dca1ac5f12496ed777f541036d2701205046a9ad37ea968b7  data/R10_fs_constants.csv
8cf75d61533283c0a9f036b6586d7afb96a6aaca928923216522c3c8cb4f0ec8  data/R10_lattice_exact_law.csv
226fbfc23aa11be36fb016792797a43f6c70417786fcd4483bffa652a2383962  data/R10_operator_null_level.csv
cc72f77fa539d29c614a222f5477e27708ae8e0519a6efa36e65b00f3bc52718  data/R10_skew_diagnostics.csv
d2bda65da5accec537d66ff8c4fee516d89cb524ed429cc0927af8297c131d5f  data/R10_skew_fpr.csv
cb1543dcd4b8cd5aa761dbf96b9312b4b325321377dfcf77a697a1c126696f73  data/R10_skew_streams.csv
7abce27915f8fe47e6a2f2d170000909dff5bc8cbc28c016db19ed2243c3da70  figures/fig10_skew_robustness.png
bcd03ff5abe7d121bc0acca0eb4fedf07940c47455652325ba3bfe48824ba07a  tables/R10_claims.tex
```

The second digest set is **identical, line for line**, and so are the `--n-jobs 1` set and the
third default-worker set; the four `sha256sum` listings were compared by `diff`.

**§S4.4 grep** over `exp_R10_skew_robustness.py`, `exp_R10_skew_robustness.log` and
`docs/sections/R10.md`: **empty**.

**§S7 form grep** — `except:` / `except Exception` / `iterrows` / `np.sqrt(len(` / `/home/` over the
`.py`: **empty**. The carried `lb_pvalue` catches three **named** exception classes and control C10
asserts that none of them fired.

## 10. Figure verdict

`results/R10_skew_robustness/figures/fig10_skew_robustness.png` reproduces v87 Figure 10. Panel (A)
carries the two Ljung–Box rejection rates against realized skewness with their Wilson bands and the
`5 %` nominal line; panel (B) the three CUSUM arms with their Wilson bands, the same nominal line and
**the level control C8 measures this operator to deliver under perfect centring**. Both are drawn
from the in-RAM frame and never from a reloaded CSV. Four deliberate divergences from the submitted
PNG, all declared under `ALL-figure-presentation` (Class C):

- bold panel titles prefixed `(A)` / `(B)` and centred (the delivered script writes
  `'A. Autocorrelation Robustness (Whitening)'` at the matplotlib default location);
- both panels carry a grid;
- **panel B carries the operator's own null level as a second reference**, which the submitted figure
  does not draw and without which `1.0–1.5 %` reads against a `5 %` this detector cannot reach;
- the abscissa is passed in rather than read from the frame inside the plotting routine, so that
  control C3 can assert structurally that the `axes[0]` statements subscript only `lb_*` columns.

**The connecting segments are guides for the eye.** The curve rests on **four** `ξ` values and no
interpolation between them is published; `docs/sections/R10.md` says so.

## 11. Open questions, left open

1. **Should `verify_fs_construction`'s bare `RandomState(999)` have been re-keyed?** It is a
   deterministic construction check whose output is a pass or a `sys.exit(1)`, it produces no
   Monte-Carlo value, and re-keying it would have broken the byte identity control C5 asserts on it.
   It was carried verbatim. This is the same trade-off `AUDIT_R07.md` open question 3 poses for
   `check_anti_look_ahead`, which the R10 plan explicitly declines to cite as precedent because it
   is unresolved there. It is not settled here either.
2. **Should `\RTenFprHalfMaxExact` carry the strict or the weak operator's level?** The macro carries
   the strict `P(M > λ)`, which is the plan's wording. Control C7c measures the code to implement the
   weak `P(M ≥ λ)`. At the cell the macro reports the two agree at the printed precision
   (`96.6 %` either way), but they need not in general, and the macro's comment block gives both.
   Which one a camera-ready sentence should quote is not R10's call.
3. **Is the panel-A clarification a camera-ready matter at all?** The caption's sentence is true, and
   the candidate proposes a clause rather than a correction. Whether an incomplete-but-true caption
   belongs in the camera-ready set — where `R07_v87_panelB_operating_level.md` is the precedent — is
   a judgement for the orchestrator. It is filed with **no register entry**.
4. **`loc="center"` or `loc="left"` on panel titles?** The common preamble's 6 August 2026 revision
   says centre; the R10 prompt §0 still says left. The preamble's precedence clause was applied. One
   of the two documents should be amended, and it is not R10's call which.
5. **Who restores `data/reference/R09/`'s register row?** `data/reference/README.md` was absent from
   the working tree when R10 started and was restored from its most recent recoverable content, which
   predates R09's own edit. R10 appended its row and paragraph to that. The R09 row is missing and
   R10 did not invent one.
6. **Does the operator's own null level deserve a manuscript sentence?** `1.0–1.5 %` against a floor
   of `0.345 %` is a different statement from `1.0–1.5 %` against a nominal of `5 %`, and the caption
   invites the second reading by printing neither. §perimeter keeps it out of the register and out of
   the candidates because the measurement exists to make a control readable; whether the manuscript
   should nonetheless say it is above R10's pay grade.

## 12. `pytest tests/ -v`, pasted verbatim

The suite was run in full after the final campaign. The R10 file contributes **26** tests, of which
**18** are blocking, **4** are self-invalidating and **4** are reporting-only.

**The four self-invalidating assertions, and what each would mean if it fired.**

- `test_R10_the_three_monte_carlo_numerals_of_L290_move_within_their_own_sampling_error` asserts
  `|z| ≤ 3` on every L290 numeral whose rounding at v87's own precision has changed, against the
  standard error of the difference between two campaigns. Exactly one numeral has moved — the
  realized skewness, at `+1.95` — and the test asserts that the moved set is exactly that one, so a
  later campaign that moves a second numeral fires the test and what changes is
  `docs/DEVIATIONS.md`, not the tolerance.
- `test_R10_the_caption_fpr_envelope_has_moved_at_its_upper_end` asserts the D2 itself: the
  regenerated upper end does not round to the printed `1.8 %`, the lower end does round to `1.0 %`,
  and the printed upper end sits inside the bootstrap envelope of the regenerated maximum. If a later
  campaign brings the upper end back, the register entry loses that numeral.
- `test_R10_the_symmetric_grid_point_is_not_centred_on_one_half` asserts that the `ξ = 1` marginal
  rate sits closer to `q*` than to `1/2`. It states a **specification imprecision of the R10
  prompt**, not a defect of the manuscript, which claims nothing about the `ξ = 1` cell.
- `test_R10_the_implemented_threshold_test_coincides_with_the_weak_operator` asserts control C7c's
  empirical finding. If a later campaign separates the two operators differently,
  `docs/sections/R10.md` and C7's predictor of record are what change.

```
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-9.0.3, pluggy-1.6.0 -- /home/m53/miniforge3/envs/Trading/bin/python3
cachedir: .pytest_cache
rootdir: /home/m53/The-Whitening-Advantage-Experiments
plugins: anyio-4.8.0
collecting ... collected 306 items

tests/test_R01_claims.py::test_r01_models PASSED                         [  0%]
tests/test_R01_claims.py::test_r01_trajectories PASSED                   [  0%]
tests/test_R01_claims.py::test_r01_injection_summary PASSED              [  0%]
tests/test_R01_claims.py::test_r01_placebo PASSED                        [  1%]
tests/test_R01_claims.py::test_r01_magnitude_and_symmetry PASSED         [  1%]
tests/test_R02_claims.py::test_stream_counts PASSED                      [  1%]
tests/test_R02_claims.py::test_classifier_integrity PASSED               [  2%]
tests/test_R02_claims.py::test_data_rejection_rates PASSED               [  2%]
tests/test_R02_claims.py::test_distinct_p_concept PASSED                 [  2%]
tests/test_R02_claims.py::test_independence_diagnostics PASSED           [  3%]
tests/test_R02_claims.py::test_iid_arm_rejection_is_reported_not_asserted PASSED [  3%]
tests/test_R02_claims.py::test_concept_level_covered_by_wilson PASSED    [  3%]
tests/test_R02_claims.py::test_max_clustered_pvalue_below_manuscript_bound PASSED [  4%]
tests/test_R02b_claims.py::test_negative_control_integrity PASSED        [  4%]
tests/test_R02b_claims.py::test_nu_seven_is_indistinguishable_from_nominal PASSED [  4%]
tests/test_R02b_claims.py::test_heavy_tail_arms_exclude_nominal PASSED   [  5%]
tests/test_R02b_claims.py::test_rate_ordering_heavy_versus_light PASSED  [  5%]
tests/test_R02b_claims.py::test_negative_control_matches_squared_at_light_tails PASSED [  5%]
tests/test_R02c_claims.py::test_R02c_seed_uniqueness PASSED              [  6%]
tests/test_R02c_claims.py::test_R02c_negative_control_calibration PASSED [  6%]
tests/test_R02c_claims.py::test_R02c_eighth_moment_account_is_refuted PASSED [  6%]
tests/test_R02c_claims.py::test_R02c_slope_test_power_is_declared PASSED [  7%]
tests/test_R02c_claims.py::test_R02c_control_arm_integrity PASSED        [  7%]
tests/test_R02c_claims.py::test_R02c_continuity PASSED                   [  7%]
tests/test_R02c_claims.py::test_R02c_mechanism_slope_logic PASSED        [  8%]
tests/test_R03_claims.py::test_R03_grid_cardinality PASSED               [  8%]
tests/test_R03_claims.py::test_R03_grid_is_unchanged PASSED              [  8%]
tests/test_R03_claims.py::test_R03_threshold_ordering_is_structural PASSED [  9%]
tests/test_R03_claims.py::test_R03_monotonicity_beyond_gamma_six PASSED  [  9%]
tests/test_R03_claims.py::test_R03_aggregate_certification_gates PASSED  [  9%]
tests/test_R03_claims.py::test_R03_gamma_rule_holds_the_nominal_level PASSED [ 10%]
tests/test_R03_claims.py::test_R03_iid_calibration_arm_is_well_formed PASSED [ 10%]
tests/test_R03_claims.py::test_R03_deviation_classification_against_witness PASSED [ 10%]
tests/test_R03_claims.py::test_R03_macros_are_emitted PASSED             [ 11%]
tests/test_R04_claims.py::test_R04_cardinalities PASSED                  [ 11%]
tests/test_R04_claims.py::test_R04_grids_match_v87 PASSED                [ 11%]
tests/test_R04_claims.py::test_R04_horizon_and_sample_size PASSED        [ 12%]
tests/test_R04_claims.py::test_R04_reference_drifts_are_coherent PASSED  [ 12%]
tests/test_R04_claims.py::test_R04_all_arms_are_iso_fpr PASSED           [ 12%]
tests/test_R04_claims.py::test_R04_concept_threshold_is_flat_in_gamma PASSED [ 13%]
tests/test_R04_claims.py::test_R04_concept_level_is_homogeneous_in_gamma PASSED [ 13%]
tests/test_R04_claims.py::test_R04_recalib_blind_zone_persists_at_lowest_gamma PASSED [ 13%]
tests/test_R04_claims.py::test_R04_recalib_is_slower_than_both_first_order_arms PASSED [ 14%]
tests/test_R04_claims.py::test_R04_add_decreases_with_drift_magnitude PASSED [ 14%]
tests/test_R04_claims.py::test_R04_conditional_mean_is_labelled_and_accompanied PASSED [ 14%]
tests/test_R04_claims.py::test_R04_efficiency_ratio_is_monotone_in_nu PASSED [ 15%]
tests/test_R04_claims.py::test_R04_ratio_respects_the_gaussian_ceiling PASSED [ 15%]
tests/test_R04_claims.py::test_R04_predicted_ratio_is_the_pitman_constant PASSED [ 15%]
tests/test_R04_claims.py::test_R04_oracle_is_never_slower_than_the_fitted_arm PASSED [ 16%]
tests/test_R04_claims.py::test_R04_analytic_crossing_matches_v87 PASSED  [ 16%]
tests/test_R04_claims.py::test_R04_blind_zone_onset_matches_v87 PASSED   [ 16%]
tests/test_R04_claims.py::test_R04_macros_are_emitted_and_computed PASSED [ 16%]
tests/test_R04_claims.py::test_R04_crossings_agree_with_the_interpolation_rule PASSED [ 17%]
tests/test_R04_claims.py::test_R04_emitted_crossing_brackets_contain_the_crossing PASSED [ 17%]
tests/test_R04_claims.py::test_R04_table3_printing_rule_reproduces_v87 PASSED [ 17%]
tests/test_R04_claims.py::test_R04_table3_is_generated_from_the_csv PASSED [ 18%]
tests/test_R04_claims.py::test_R04_table3_shows_detrate_exactly_when_below_one PASSED [ 18%]
tests/test_R04_claims.py::test_R04_intervals_are_clamped_and_ordered PASSED [ 18%]
tests/test_R04_claims.py::test_R04_no_nan_in_reported_delays PASSED      [ 19%]
tests/test_R04_claims.py::test_R04_m0_universality_arm_matches_the_garch_arm PASSED [ 19%]
tests/test_R04_claims.py::test_R04_report_deviation_degrees 
  R04 deviation classification against the submitted campaign
  quantity                     |    published |  regenerated | degree
  Table 3 Recalib     c=0.25  |  2293.457219 |  2746.329897 | D2
  Table 3 Recalib     c=0.5   |  1336.727426 |  2622.018789 | D2
  Table 3 Recalib     c=1.0   |   202.627814 |  1986.673764 | D2
  Table 3 Recalib     c=2.0   |    55.909000 |  1311.240964 | D2
  Table 3 Eco_L1      c=0.25  |   389.309500 |   409.219500 | D2
  Table 3 Eco_L1      c=0.5   |    72.002000 |    77.128500 | D2
  Table 3 Eco_L1      c=1.0   |    26.393500 |    30.886500 | D2
  Table 3 Eco_L1      c=2.0   |    12.579000 |    16.096000 | D2
  Table 3 Concept     c=0.25  |   460.290000 |   381.935500 | D2
  Table 3 Concept     c=0.5   |   100.639000 |    96.859500 | D2
  Table 3 Concept     c=1.0   |    43.831500 |    42.628500 | D2
  Table 3 Concept     c=2.0   |    28.881500 |    28.572000 | D2
  ratio at nu=3.0                  |     0.407263 |     0.331177 | D2
  ratio at nu=4.0                  |     0.778229 |     0.622199 | D2
  ratio at nu=4.5                  |     0.921953 |     0.694563 | D2
  ratio at nu=5.0                  |     1.022764 |     0.788887 | D2
  ratio at nu=7.0                  |     1.236853 |     0.985825 | D2
  ratio at nu=30.0                 |     1.489896 |     1.200608 | D2
  The witness is a record of the submitted campaign, not a target; see docs/sections/R04.md for why its Gamma grid does not span.
PASSED       [ 19%]
tests/test_R04b_claims.py::test_R04b_cardinality_and_grid PASSED         [ 20%]
tests/test_R04b_claims.py::test_R04b_protocol_constants_match_v87 PASSED [ 20%]
tests/test_R04b_claims.py::test_R04b_gamma_target_is_attainable_and_realised PASSED [ 20%]
tests/test_R04b_claims.py::test_R04b_analytic_prediction_is_the_pitman_constant PASSED [ 21%]
tests/test_R04b_claims.py::test_R04b_in_sample_bisection_converged PASSED [ 21%]
tests/test_R04b_claims.py::test_R04b_pooled_holdout_level_meets_the_promised_band PASSED [ 21%]
tests/test_R04b_claims.py::test_R04b_conditional_calibration_pvalues_are_uniform PASSED [ 22%]
tests/test_R04b_claims.py::test_R04b_rates_are_consistent_and_clamped PASSED [ 22%]
tests/test_R04b_claims.py::test_R04b_continuity_anchors_are_read_from_R04 PASSED [ 22%]
tests/test_R04b_claims.py::test_R04b_is_compatible_with_R04_at_the_common_points PASSED [ 23%]
tests/test_R04b_claims.py::test_R04b_grid_bracket_straddles_unity_and_the_interpolation_lies_inside_it PASSED [ 23%]
tests/test_R04b_claims.py::test_R04b_inferential_bracket_is_recomputable_from_the_csv PASSED [ 23%]
tests/test_R04b_claims.py::test_R04b_bootstrap_error_exceeds_the_conditional_one PASSED [ 24%]
tests/test_R04b_claims.py::test_R04b_shape_fit_is_reported_with_its_goodness PASSED [ 24%]
tests/test_R04b_claims.py::test_R04b_analytic_crossing_matches_v87 PASSED [ 24%]
tests/test_R04b_claims.py::test_R04b_estimation_cost_interval_arithmetic PASSED [ 25%]
tests/test_R04b_claims.py::test_R04b_ratio_respects_the_gaussian_ceiling PASSED [ 25%]
tests/test_R04b_claims.py::test_R04b_oracle_ratio_does_not_cross_again_above_seven PASSED [ 25%]
tests/test_R04b_claims.py::test_R04b_macros_are_emitted_and_computed PASSED [ 26%]
tests/test_R04b_claims.py::test_R04b_no_nan_in_reported_quantities PASSED [ 26%]
tests/test_R04b_claims.py::test_R04b_report_against_v87 PASSED           [ 26%]
tests/test_R05_claims.py::test_abrupt_cardinality PASSED                 [ 27%]
tests/test_R05_claims.py::test_ramp_cardinalities PASSED                 [ 27%]
tests/test_R05_claims.py::test_protocol_constants PASSED                 [ 27%]
tests/test_R05_claims.py::test_horizons_are_the_two_published_budgets PASSED [ 28%]
tests/test_R05_claims.py::test_common_horizon_is_constant_across_gamma PASSED [ 28%]
tests/test_R05_claims.py::test_null_levels_are_homogeneous_across_gamma PASSED [ 28%]
tests/test_R05_claims.py::test_concept_branch_is_gamma_invariant_by_construction PASSED [ 29%]
tests/test_R05_claims.py::test_concept_is_blind_to_the_scale_pathology PASSED [ 29%]
tests/test_R05_claims.py::test_positive_control_shows_the_monitor_responsive PASSED [ 29%]
tests/test_R05_claims.py::test_both_crossovers_are_emitted_and_are_distinct PASSED [ 30%]
tests/test_R05_claims.py::test_scaling_law_branches_meet_at_the_crossover PASSED [ 30%]
tests/test_R05_claims.py::test_ladder_visits_the_three_published_horizons PASSED [ 30%]
tests/test_R05_claims.py::test_ladder_is_monotone_in_the_horizon PASSED  [ 31%]
tests/test_R05_claims.py::test_ladder_agrees_with_the_campaigns_it_overlaps PASSED [ 31%]
tests/test_R05_claims.py::test_sixth_moment_boundary_matches_the_published_gamma PASSED [ 31%]
tests/test_R05_claims.py::test_moment_margin_macro_matches_the_published_bound PASSED [ 32%]
tests/test_R05_claims.py::test_macro_file_is_well_formed PASSED          [ 32%]
tests/test_R05_claims.py::test_required_macros_are_present PASSED        [ 32%]
tests/test_R05_claims.py::test_figure_exists PASSED                      [ 33%]
tests/test_R05_claims.py::test_text_artefacts_end_with_a_newline PASSED  [ 33%]
tests/test_R05_claims.py::test_superseded_witness_is_documented_not_regenerated PASSED [ 33%]
tests/test_R05_claims.py::test_report_deviation_classification 
--- R05 deviation classification against v87 ---
                   quantity  published  regenerated  printed_decimals degree                                                 source_cell
               abrupt_slope      23.70    26.001631                 1     D2       R05_abrupt_add_vs_gamma.csv, OLS of ADD_Data on Gamma
           abrupt_intercept      38.00    32.198021                 0     D2       R05_abrupt_add_vs_gamma.csv, OLS of ADD_Data on Gamma
          sqrt_rule_fpr_pct      31.00    24.500000                 0     D2        R05_abrupt_add_vs_gamma.csv, FPR_rule_xSqrtGamma max
   scaling_median_error_pct       5.40     5.346536                 1     D2            R05_ramp_multigamma_2e5.csv, ADD_Data vs Eq. (5)
 recalib_margin_min_pct_2e5       7.00    -1.420701                 0     D2         R05_ramp_multigamma_2e5.csv, lambda_star_Data/Gamma
 recalib_margin_max_pct_2e5      29.00    39.288641                 0     D2         R05_ramp_multigamma_2e5.csv, lambda_star_Data/Gamma
             lambda_iid_2e5     129.50   128.631853                 1     D2                   R05_ramp_multigamma_2e5.csv, lambda_iid_H
       grid_reach_wstar_2e5      22.50    22.500988                 1     D1     R05_ramp_multigamma_2e5.csv, w_over_wstar_predicted max
      censoring_max_pct_2e5       1.30     0.250000                 1     D2              R05_ramp_multigamma_2e5.csv, censored_Data max
      detection_min_pct_2e5      98.70    99.750000                 1     D2               R05_ramp_multigamma_2e5.csv, DetRate_Data min
  lambda_over_gamma_min_2e5     138.00   126.804379                 0     D2         R05_ramp_multigamma_2e5.csv, lambda_star_Data/Gamma
  lambda_over_gamma_max_2e5     167.00   179.169559                 0     D2         R05_ramp_multigamma_2e5.csv, lambda_star_Data/Gamma
        sd_over_add_max_2e5       3.20     0.940909                 1     D2      R05_ramp_multigamma_2e5.csv, SEM_Data and DetRate_Data
       med_over_add_min_2e5       0.68     0.758602                 2     D2              R05_ramp_multigamma_2e5.csv, MED_Data/ADD_Data
        rho_w_share_pct_2e5      58.00    57.259679                 0     D2                       R05_ramp_multigamma_2e5.csv, widest w
           exponent_min_2e5       0.65     0.679887                 2     D2    R05_ramp_multigamma_2e5.csv, ramp fit on w_delta_applied
           exponent_max_2e5       0.71     0.697822                 2     D2    R05_ramp_multigamma_2e5.csv, ramp fit on w_delta_applied
     model_exponent_min_2e5       0.71     0.708701                 2     D1 R05_ramp_multigamma_2e5.csv, Eq. (5) fit on w_delta_applied
     model_exponent_max_2e5       0.73     0.719008                 2     D2 R05_ramp_multigamma_2e5.csv, Eq. (5) fit on w_delta_applied
             lambda_iid_3e6     303.00   282.536302                 1     D2                   R05_ramp_multigamma_3e6.csv, lambda_iid_H
       grid_reach_wstar_3e6     225.00   224.999974                 1     D1     R05_ramp_multigamma_3e6.csv, w_over_wstar_predicted max
low_gamma_max_error_pct_3e6       5.70     5.797607                 1     D2          R05_ramp_multigamma_3e6.csv, Gamma <= 4 vs Eq. (5)
        rho_w_share_pct_3e6      78.00    78.106010                 0     D1                       R05_ramp_multigamma_3e6.csv, widest w
 recalib_margin_max_pct_3e6      96.00    96.435906                 0     D1         R05_ramp_multigamma_3e6.csv, lambda_star_Data/Gamma
         sixth_moment_gamma       7.10     7.079317                 1     D1                                 closed form, no Monte Carlo
 moment_margin_at_gamma_max       0.80     0.793127                 1     D1                                 closed form, no Monte Carlo
      lambda_iid_ladder_77k     102.80   111.025130                 1     D2                       R05_lambda_iid_horizon.csv, H = 77000

--- Concept threshold, witness against regenerated ---
 abrupt: witness lambda_star_Concept = 10.8000, FPR = 0.0950
    2e5: witness lambda_star_Concept = 15.8100, FPR = 0.0525
    3e6: witness lambda_star_Concept = 19.0200, FPR = 0.0550

The v87 numeral lambda_C = 10 matches none of the three. See docs/sections/R05.md.
PASSED    [ 33%]
tests/test_R06_claims.py::test_R06_cardinalities_and_grid PASSED         [ 34%]
tests/test_R06_claims.py::test_R06_gamma_grid_is_realised_in_closed_form PASSED [ 34%]
tests/test_R06_claims.py::test_R06_fourth_moment_boundary_is_computed_not_hard_coded PASSED [ 34%]
tests/test_R06_claims.py::test_R06_boundary_is_not_confused_with_the_nearest_grid_point PASSED [ 35%]
tests/test_R06_claims.py::test_R06_panel_A_design_is_paired_and_declared PASSED [ 35%]
tests/test_R06_claims.py::test_R06_pooled_binary_level_covers_nominal_at_cluster_precision PASSED [ 35%]
tests/test_R06_claims.py::test_R06_counterfactual_arm_removes_the_pairing PASSED [ 36%]
tests/test_R06_claims.py::test_R06_no_per_gamma_gate_is_possible PASSED  [ 36%]
tests/test_R06_claims.py::test_R06_squared_stream_rejects_massively PASSED [ 36%]
tests/test_R06_claims.py::test_R06_task_boundaries_saturate PASSED       [ 37%]
tests/test_R06_claims.py::test_R06_intermediate_threshold_is_reported_and_labelled PASSED [ 37%]
tests/test_R06_claims.py::test_R06_median_task_control_covers_nominal_and_is_weakly_resolved PASSED [ 37%]
tests/test_R06_claims.py::test_R06_no_silent_fallback_survived_into_the_artefacts PASSED [ 38%]
tests/test_R06_claims.py::test_R06_reproduces_the_witness_byte_for_byte PASSED [ 38%]
tests/test_R06_claims.py::test_R06_macros_are_emitted_and_computed PASSED [ 38%]
tests/test_R06_claims.py::test_R06_report_against_the_witness PASSED     [ 39%]
tests/test_R07_claims.py::test_R07_every_artefact_the_plan_lists_exists_with_its_prescribed_schema PASSED [ 39%]
tests/test_R07_claims.py::test_R07_the_lattice_law_reproduces_under_an_independent_dynamic_program PASSED [ 39%]
tests/test_R07_claims.py::test_R07_the_two_attainable_levels_bracket_five_percent_and_fix_lambda_star PASSED [ 40%]
tests/test_R07_claims.py::test_R07_the_dynamic_program_agrees_with_exhaustive_enumeration PASSED [ 40%]
tests/test_R07_claims.py::test_R07_the_fourth_moment_product_of_L308_reproduces_in_closed_form PASSED [ 40%]
tests/test_R07_claims.py::test_R07_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 41%]
tests/test_R07_claims.py::test_R07_the_naive_arm_and_the_oracle_arm_coincide_at_phi_zero PASSED [ 41%]
tests/test_R07_claims.py::test_R07_the_oracle_arm_is_exactly_phi_invariant PASSED [ 41%]
tests/test_R07_claims.py::test_R07_the_design_effect_is_measured_on_every_pooled_quantity PASSED [ 42%]
tests/test_R07_claims.py::test_R07_the_ljungbox_rejection_of_L308_climbs_monotonically_in_phi PASSED [ 42%]
tests/test_R07_claims.py::test_R07_every_ols_cell_matches_the_oracle_band_of_the_figure7_caption PASSED [ 42%]
tests/test_R07_claims.py::test_R07_the_ols_envelopes_stay_inside_the_two_bands_L308_prints PASSED [ 43%]
tests/test_R07_claims.py::test_R07_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 43%]
tests/test_R07_claims.py::test_R07_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 43%]
tests/test_R07_claims.py::test_R07_every_produced_text_file_ends_in_a_newline PASSED [ 44%]
tests/test_R07_claims.py::test_R07_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 44%]
tests/test_R07_claims.py::test_R07_the_produced_sources_carry_no_banned_construct PASSED [ 44%]
tests/test_R07_claims.py::test_R07_the_comparison_operator_is_the_same_on_both_paths PASSED [ 45%]
tests/test_R07_claims.py::test_R07_the_seven_carried_primitives_are_byte_identical_to_the_witness PASSED [ 45%]
tests/test_R07_claims.py::test_R07_the_three_monte_carlo_numerals_of_L308_move_within_their_own_sampling_error PASSED [ 45%]
tests/test_R07_claims.py::test_R07_the_bias_bound_of_L308_is_exceeded_by_the_regenerated_campaign PASSED [ 46%]
tests/test_R07_claims.py::test_R07_the_exact_lattice_levels_differ_from_the_two_numerals_v87_prints PASSED [ 46%]
tests/test_R07_claims.py::test_R07_the_eta_decay_is_not_one_over_root_n PASSED [ 46%]
tests/test_R07_claims.py::test_R07_report_the_campaign_against_its_witness PASSED [ 47%]
tests/test_R07_claims.py::test_R07_report_the_design_effect_of_every_pooled_quantity PASSED [ 47%]
tests/test_R07_claims.py::test_R07_report_the_counterfactual_ladder PASSED [ 47%]
tests/test_R07_claims.py::test_R07_report_the_candidate_readings_of_the_dispersion_cost_numeral PASSED [ 48%]
tests/test_R07_claims.py::test_R07_report_the_float_drift_on_the_lattice_boundary PASSED [ 48%]
tests/test_R09_claims.py::test_R09_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 48%]
tests/test_R09_claims.py::test_R09_every_sample_size_the_campaign_used_is_carried_on_the_row PASSED [ 49%]
tests/test_R09_claims.py::test_R09_the_mixture_martingale_remains_bounded_by_alpha_under_continuous_monitoring PASSED [ 49%]
tests/test_R09_claims.py::test_R09_only_the_mixture_controls_the_time_uniform_rate PASSED [ 49%]
tests/test_R09_claims.py::test_R09_the_ecusum_arl0_satisfies_the_reciprocal_of_alpha PASSED [ 50%]
tests/test_R09_claims.py::test_R09_the_peeking_horizon_is_four_times_the_calibration_horizon PASSED [ 50%]
tests/test_R09_claims.py::test_R09_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 50%]
tests/test_R09_claims.py::test_R09_the_mixture_threshold_is_villes_threshold_on_the_mixture_value PASSED [ 50%]
tests/test_R09_claims.py::test_R09_the_cusum_statistic_lives_on_the_two_delta_lattice PASSED [ 51%]
tests/test_R09_claims.py::test_R09_the_one_sided_kolmogorov_statistic_is_the_supremum_it_names PASSED [ 51%]
tests/test_R09_claims.py::test_R09_the_arl0_lower_bound_is_recomputed_from_the_persisted_columns PASSED [ 51%]
tests/test_R09_claims.py::test_R09_no_arl0_is_persisted_without_its_censored_fraction PASSED [ 52%]
tests/test_R09_claims.py::test_R09_the_macro_emitter_refuses_a_censored_arl0 PASSED [ 52%]
tests/test_R09_claims.py::test_R09_the_bound_flag_is_a_computed_comparison_not_a_literal PASSED [ 52%]
tests/test_R09_claims.py::test_R09_the_level_granularity_column_states_the_lattice_it_names PASSED [ 53%]
tests/test_R09_claims.py::test_R09_the_descriptive_binomial_p_values_are_the_exact_one_sided_tail PASSED [ 53%]
tests/test_R09_claims.py::test_R09_the_add_column_is_conditional_and_the_detection_rate_says_so PASSED [ 53%]
tests/test_R09_claims.py::test_R09_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 54%]
tests/test_R09_claims.py::test_R09_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 54%]
tests/test_R09_claims.py::test_R09_the_ecusum_censored_fraction_is_not_zero PASSED [ 54%]
tests/test_R09_claims.py::test_R09_every_produced_text_file_ends_in_a_newline PASSED [ 55%]
tests/test_R09_claims.py::test_R09_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 55%]
tests/test_R09_claims.py::test_R09_the_produced_sources_carry_no_banned_construct PASSED [ 55%]
tests/test_R09_claims.py::test_R09_the_orchestrator_passes_the_control_arm_and_never_calls_pytest PASSED [ 56%]
tests/test_R09_claims.py::test_R09_the_shared_orchestrators_are_untouched PASSED [ 56%]
tests/test_R09_claims.py::test_R09_the_three_monte_carlo_numerals_of_L243_does_not_reproduce_at_printed_precision PASSED [ 56%]
tests/test_R09_claims.py::test_R09_the_calibrated_level_and_the_stream_count_still_reproduces_v87s_numerals PASSED [ 57%]
tests/test_R09_claims.py::test_R09_report_the_campaign_against_its_witness PASSED [ 57%]
tests/test_R09_claims.py::test_R09_report_the_published_numerals_at_their_printed_precision PASSED [ 57%]
tests/test_R09_claims.py::test_R09_report_the_censoring_that_makes_panel_c_a_horizon_artefact PASSED [ 58%]
tests/test_R09_claims.py::test_R09_report_the_control_outcomes_the_log_records PASSED [ 58%]
tests/test_R10_claims.py::test_R10_every_artefact_the_plan_lists_exists_with_its_prescribed_schema PASSED [ 58%]
tests/test_R10_claims.py::test_R10_the_operating_threshold_is_seventy_five_lattice_units PASSED [ 59%]
tests/test_R10_claims.py::test_R10_the_half_arm_law_reproduces_under_an_independent_dynamic_program PASSED [ 59%]
tests/test_R10_claims.py::test_R10_the_bernoulli_twin_reduces_to_the_fair_coin_at_one_half PASSED [ 59%]
tests/test_R10_claims.py::test_R10_the_enumeration_validation_agrees_with_an_independent_enumeration PASSED [ 60%]
tests/test_R10_claims.py::test_R10_the_wilson_intervals_reproduce_from_a_second_algebraic_form PASSED [ 60%]
tests/test_R10_claims.py::test_R10_q_star_reproduces_from_the_student_t_survival_function PASSED [ 60%]
tests/test_R10_claims.py::test_R10_the_caption_stream_count_is_one_thousand_per_point PASSED [ 61%]
tests/test_R10_claims.py::test_R10_the_sign_stream_is_bit_identically_the_innovation_sign PASSED [ 61%]
tests/test_R10_claims.py::test_R10_no_degraded_path_is_taken PASSED      [ 61%]
tests/test_R10_claims.py::test_R10_the_standardisation_constants_are_one_deterministic_input PASSED [ 62%]
tests/test_R10_claims.py::test_R10_the_fixed_half_cusum_explodes_with_asymmetry PASSED [ 62%]
tests/test_R10_claims.py::test_R10_recentering_restores_false_alarm_control PASSED [ 62%]
tests/test_R10_claims.py::test_R10_the_carried_primitives_are_byte_identical_to_both_owning_files PASSED [ 63%]
tests/test_R10_claims.py::test_R10_the_family_wise_arithmetic_is_logged_before_any_gate_is_read PASSED [ 63%]
tests/test_R10_claims.py::test_R10_macros_are_emitted_and_agree_with_the_frames PASSED [ 63%]
tests/test_R10_claims.py::test_R10_text_artefacts_end_with_a_newline PASSED [ 64%]
tests/test_R10_claims.py::test_R10_no_confirmatory_language_in_the_script_the_log_or_the_section PASSED [ 64%]
tests/test_R10_claims.py::test_R10_the_three_monte_carlo_numerals_of_L290_move_within_their_own_sampling_error PASSED [ 64%]
tests/test_R10_claims.py::test_R10_the_caption_fpr_envelope_has_moved_at_its_upper_end PASSED [ 65%]
tests/test_R10_claims.py::test_R10_the_symmetric_grid_point_is_not_centred_on_one_half PASSED [ 65%]
tests/test_R10_claims.py::test_R10_the_implemented_threshold_test_coincides_with_the_weak_operator PASSED [ 65%]
tests/test_R10_claims.py::test_R10_report_deviation_classification 
  R10 deviation classification against v87, at the manuscript's printing precision
  site                                 printed   regenerated  z_paired  degree  source cell
  L290 realized skewness                 -1.44      -1.42796      1.95  D2      R10_skew_diagnostics.csv, xi=0.5, skewness
  L290 marginal rate q                    0.58      0.582191      8.76  D1      R10_skew_diagnostics.csv, xi=0.5, q
  L290 fixed-1/2 CUSUM fires at           0.97         0.966     -0.49  D1      R10_skew_fpr.csv, xi=0.5, fpr_half_rate
  Fig. 10 caption FPR lower end           0.01          0.01       nan  D0      R10_skew_fpr.csv, min fpr_qhat_rate
  Fig. 10 caption FPR upper end          0.018         0.015       nan  D2      R10_skew_fpr.csv, max fpr_qhat_rate
  The witness is a record of the submitted campaign, not a target; see data/reference/README.md.
  witness [diagnostics] xi = 1.0  : skewness 0.00286738 -> -0.000229514, q 0.499682 -> 0.499485
  witness [diagnostics] xi = 0.85 : skewness -0.47769 -> -0.474218, q 0.529572 -> 0.52947
  witness [diagnostics] xi = 0.65 : skewness -1.09725 -> -1.08484, q 0.564269 -> 0.564079
  witness [diagnostics] xi = 0.5  : skewness -1.44285 -> -1.42796, q 0.5823 -> 0.582191
  witness [fpr] xi = 1.0  : lb_ebin_rate 0.051 -> 0.047, lb_sign_rate 0.051 -> 0.05, fpr_half_rate 0.006 -> 0.005, fpr_oracle_rate 0.005 -> 0.004, fpr_qhat_rate 0.018 -> 0.01
  witness [fpr] xi = 0.85 : lb_ebin_rate 0.045 -> 0.048, lb_sign_rate 0.055 -> 0.063, fpr_half_rate 0.047 -> 0.041, fpr_oracle_rate 0.002 -> 0.009, fpr_qhat_rate 0.018 -> 0.014
  witness [fpr] xi = 0.65 : lb_ebin_rate 0.055 -> 0.048, lb_sign_rate 0.053 -> 0.046, fpr_half_rate 0.63 -> 0.596, fpr_oracle_rate 0.002 -> 0.005, fpr_qhat_rate 0.01 -> 0.011
  witness [fpr] xi = 0.5  : lb_ebin_rate 0.058 -> 0.057, lb_sign_rate 0.056 -> 0.05, fpr_half_rate 0.969 -> 0.966, fpr_oracle_rate 0.003 -> 0.004, fpr_qhat_rate 0.011 -> 0.015
PASSED [ 66%]
tests/test_R10_claims.py::test_R10_report_design_effect_and_extremum_envelopes 
  R10 design effect of every quantity pooled across the xi grid (control C9)
  statistic    cells   rho_bar     deff     n_eff    pooled  SE inflation
  lb_sign          4    0.0624   1.1872    3369.4   0.05225        1.0896
  lb_ebin          4    0.0072   1.0216    3915.4   0.05000        1.0107
  fpr_half         4    0.0435   1.1305    3538.2   0.40200        1.0633
  fpr_oracle       4    0.0696   1.2087    3309.3   0.00550        1.0994
  fpr_qhat         4    0.0142   1.0426    3836.5   0.01250        1.0211
  Extremum envelopes: an extremum over four correlated cells has neither the distribution nor the interval of one cell (S4bis.4).
  RTenLbSignMin      point 0.0460  bootstrap 95% [0.0330, 0.0520]  bootstrap mean 0.042653
  RTenLbSignMax      point 0.0630  bootstrap 95% [0.0510, 0.0790]  bootstrap mean 0.063880
  RTenFprQhatMin     point 0.0100  bootstrap 95% [0.0040, 0.0130]  bootstrap mean 0.008393
  RTenFprQhatMax     point 0.0150  bootstrap 95% [0.0120, 0.0240]  bootstrap mean 0.017001
PASSED [ 66%]
tests/test_R10_claims.py::test_R10_report_the_operator_null_level_and_the_exact_half_arm_law 
  R10 the level this CUSUM delivers under perfect centring (control C8)
  xi = 1.0   ref = 0.499674     64 alarms on 20000 streams -> 0.3200% [0.2507%, 0.4084%]; fair-coin exact 0.3677%; nominal 5.0%
  xi = 0.85  ref = 0.529604     72 alarms on 20000 streams -> 0.3600% [0.2860%, 0.4531%]; fair-coin exact 0.3677%; nominal 5.0%
  xi = 0.65  ref = 0.564281     72 alarms on 20000 streams -> 0.3600% [0.2860%, 0.4531%]; fair-coin exact 0.3677%; nominal 5.0%
  xi = 0.5   ref = 0.582348     68 alarms on 20000 streams -> 0.3400% [0.2683%, 0.4308%]; fair-coin exact 0.3677%; nominal 5.0%
  The exact Bernoulli(q) law of the fixed-1/2 arm (control C7), both operators:
  xi=0.5 strict  q = 0.582348  lambda = 75 units  exact 96.6487%  observed 96.6000%
  xi=0.5 weak    q = 0.582348  lambda = 74 units  exact 97.0993%  observed 96.6000%
  xi=0.65 strict q = 0.564281  lambda = 75 units  exact 59.7223%  observed 59.6000%
  xi=0.65 weak   q = 0.564281  lambda = 74 units  exact 62.0532%  observed 59.6000%
  xi=0.85 strict q = 0.529604  lambda = 75 units  exact 3.8869%  observed 4.1000%
  xi=0.85 weak   q = 0.529604  lambda = 74 units  exact 4.3572%  observed 4.1000%
  xi=1.0 strict  q = 0.499674  lambda = 75 units  exact 0.3680%  observed 0.5000%
  xi=1.0 weak    q = 0.499674  lambda = 74 units  exact 0.4337%  observed 0.5000%
  What the float comparison implements on the lattice boundary (control C7c):
  float M > lambda           realised level 0.402000 on 4000 streams, 38 disagreements with the strict operator
  exact M_units > lambda     realised level 0.392500 on 4000 streams, 0 disagreements with the strict operator
  exact M_units >= lambda    realised level 0.402000 on 4000 streams, 38 disagreements with the strict operator
  Panel B is read against both references: nominal 5.0% and the operator's own 0.3450%. The recentred arm spans 1.0-1.5%.
PASSED [ 66%]
tests/test_R10_claims.py::test_R10_report_the_ljungbox_calibration_and_its_power_bound 
  R10 Ljung-Box calibration, per cell (control C2a; only the xi = 1 row is a gate)
      xi  lb_sign rate      KS D      KS p  lb_ebin rate      KS D      KS p
     1.0        0.0500   0.02302   0.65566        0.0470   0.03745   0.11802
    0.85        0.0630   0.01852   0.87626        0.0480   0.03802   0.10818
    0.65        0.0460   0.04344   0.04459        0.0480   0.04188   0.05826
     0.5        0.0500   0.03875   0.09671        0.0570   0.03896   0.09361
  Family-wise arithmetic: gating on all 8 cells at 0.05 would trigger with probability 33.6580% under a perfectly calibrated null, which is why it is not a gate.
  Smallest p-value over the 4000 streams: raw sign 0.000377338, HT error 0.000262061.
  The HT-error arm's evidence is a NON-REJECTION; its power at n = 8000, lag 20 is bounded by docs/DEVIATIONS.md R18-ljungbox-power, and R10 opens no duplicate entry.
PASSED [ 66%]
tests/test_R11_claims.py::test_R11_cardinalities_and_arms PASSED         [ 67%]
tests/test_R11_claims.py::test_R11_gamma_grid_is_the_target_grid_and_its_floor_is_respected PASSED [ 67%]
tests/test_R11_claims.py::test_R11_gamma_range_matches_the_published_multiplier PASSED [ 67%]
tests/test_R11_claims.py::test_R11_as_submitted_arm_is_the_per_detector_mixture PASSED [ 68%]
tests/test_R11_claims.py::test_R11_putting_both_detectors_on_one_convention_moves_the_cusum PASSED [ 68%]
tests/test_R11_claims.py::test_R11_the_published_ordering_holds_on_the_arm_that_produced_it PASSED [ 68%]
tests/test_R11_claims.py::test_R11_crn_h0_arm_is_degenerate_and_the_independent_arm_is_not PASSED [ 69%]
tests/test_R11_claims.py::test_R11_kish_design_effect_of_a_degenerate_grid_is_its_width PASSED [ 69%]
tests/test_R11_claims.py::test_R11_pht_intervals_carry_the_calibration_variance_factor PASSED [ 69%]
tests/test_R11_claims.py::test_R11_every_interval_bound_is_clamped PASSED [ 70%]
tests/test_R11_claims.py::test_R11_data_loglog_slopes_reproduce_by_an_independent_fit PASSED [ 70%]
tests/test_R11_claims.py::test_R11_pht_data_slope_is_fitted_on_a_restricted_domain PASSED [ 70%]
tests/test_R11_claims.py::test_R11_low_gamma_sensitivity_arm_excludes_exactly_the_unattainable_point PASSED [ 71%]
tests/test_R11_claims.py::test_R11_bootstrap_standard_errors_are_present_and_the_ratio_is_reported PASSED [ 71%]
tests/test_R11_claims.py::test_R11_no_macro_restates_the_cusum_scaling_law PASSED [ 71%]
tests/test_R11_claims.py::test_R11_submitted_linear_fits_are_reproduced_for_traceability PASSED [ 72%]
tests/test_R11_claims.py::test_R11_peak_to_peak_spread_is_descriptive_and_arithmetically_correct PASSED [ 72%]
tests/test_R11_claims.py::test_R11_preonset_leak_is_recorded_for_every_detector_even_at_zero PASSED [ 72%]
tests/test_R11_claims.py::test_R11_onset_table_carries_a_paired_error PASSED [ 73%]
tests/test_R11_claims.py::test_R11_the_two_adwin_implementations_are_labelled PASSED [ 73%]
tests/test_R11_claims.py::test_R11_river_version_is_recorded_in_the_artefacts PASSED [ 73%]
tests/test_R11_claims.py::test_R11_macros_are_emitted_with_the_preamble_ordinal PASSED [ 74%]
tests/test_R11_claims.py::test_R11_concept_add_macros_match_their_arm PASSED [ 74%]
tests/test_R11_claims.py::test_R11_eddm_macros_come_from_the_independent_seed_arm PASSED [ 74%]
tests/test_R11_claims.py::test_R11_report_against_v87 PASSED             [ 75%]
tests/test_R13_claims.py::test_R13_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 75%]
tests/test_R13_claims.py::test_R13_the_detector_labels_carry_the_families_the_manuscript_fixes PASSED [ 75%]
tests/test_R13_claims.py::test_R13_the_published_delay_and_false_alarm_probability_come_from_one_row PASSED [ 76%]
tests/test_R13_claims.py::test_R13_the_two_covid_detection_delays_v87_prints_reproduce PASSED [ 76%]
tests/test_R13_claims.py::test_R13_the_jensen_ratio_v87_prints_reproduces_and_is_specific_to_one_oracle PASSED [ 76%]
tests/test_R13_claims.py::test_R13_the_phase_false_alarm_probability_of_L331_does_not_reproduce_at_its_printed_precision PASSED [ 77%]
tests/test_R13_claims.py::test_R13_the_census_verdicts_of_L331_reproduce_at_the_matched_operating_point PASSED [ 77%]
tests/test_R13_claims.py::test_R13_the_2011_correction_alarms_at_dead_bands_the_caption_does_not_name PASSED [ 77%]
tests/test_R13_claims.py::test_R13_the_D2_increment_is_the_gaussian_log_likelihood_ratio PASSED [ 78%]
tests/test_R13_claims.py::test_R13_the_frozen_volatility_path_recomputes_from_the_persisted_parameters PASSED [ 78%]
tests/test_R13_claims.py::test_R13_the_four_operating_points_are_the_rules_they_name PASSED [ 78%]
tests/test_R13_claims.py::test_R13_no_arl0_is_persisted_without_its_censored_fraction PASSED [ 79%]
tests/test_R13_claims.py::test_R13_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 79%]
tests/test_R13_claims.py::test_R13_the_certification_gates_are_equivalence_statements_with_a_null_law PASSED [ 79%]
tests/test_R13_claims.py::test_R13_the_census_quantities_are_r16s_canonical_arm PASSED [ 80%]
tests/test_R13_claims.py::test_R13_the_oracle_verdict_and_the_clairvoyant_column_are_their_own_definitions PASSED [ 80%]
tests/test_R13_claims.py::test_R13_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 80%]
tests/test_R13_claims.py::test_R13_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 81%]
tests/test_R13_claims.py::test_R13_every_produced_text_file_ends_in_a_newline PASSED [ 81%]
tests/test_R13_claims.py::test_R13_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 81%]
tests/test_R13_claims.py::test_R13_the_produced_sources_carry_no_banned_construct PASSED [ 82%]
tests/test_R13_claims.py::test_R13_report_the_campaign_against_its_witness PASSED [ 82%]
tests/test_R13_claims.py::test_R13_report_the_threshold_neighbourhood_of_the_published_operating_point PASSED [ 82%]
tests/test_R13_claims.py::test_R13_report_the_certification_status_of_every_oracle PASSED [ 83%]
tests/test_R16_claims.py::test_R16_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 83%]
tests/test_R16_claims.py::test_R16_the_census_carries_the_phase_count_v87_prints PASSED [ 83%]
tests/test_R16_claims.py::test_R16_the_dating_algorithm_column_names_the_algorithm_of_every_row PASSED [ 83%]
tests/test_R16_claims.py::test_R16_the_out_of_budget_counts_reproduce_the_three_v87_prints PASSED [ 84%]
tests/test_R16_claims.py::test_R16_the_step_of_one_holds_on_the_count_and_fails_on_the_set PASSED [ 84%]
tests/test_R16_claims.py::test_R16_the_boundary_convention_flips_run_in_one_direction_only PASSED [ 84%]
tests/test_R16_claims.py::test_R16_the_unconditional_floor_is_the_sharpe_ceiling_of_the_corollary PASSED [ 85%]
tests/test_R16_claims.py::test_R16_the_sign_floor_is_the_bernoulli_divergence_of_the_manuscript PASSED [ 85%]
tests/test_R16_claims.py::test_R16_every_detectability_flag_is_its_own_floor_against_its_own_duration PASSED [ 85%]
tests/test_R16_claims.py::test_R16_the_census_statistics_recompute_from_the_raw_return_series PASSED [ 86%]
tests/test_R16_claims.py::test_R16_the_phases_partition_the_return_series_of_every_ticker PASSED [ 86%]
tests/test_R16_claims.py::test_R16_no_degenerate_phase_reaches_a_detectability_flag_without_measurement PASSED [ 86%]
tests/test_R16_claims.py::test_R16_the_turning_point_return_v87_cites_falls_where_the_convention_puts_it PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_long_secular_advance_v87_prints_reproduces PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_covid_phase_v87_prints_reproduces_to_its_printed_precision PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_two_numerical_evaluations_of_the_bound_reproduce_L260 PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_floor_fraction_envelope_of_L329_does_not_reproduce_at_its_lower_end PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_published_dating_description_is_unreachable_by_strict_pagan_sossounov PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_counterfactual_arms_are_the_rules_they_claim_to_be PASSED [ 89%]
tests/test_R16_claims.py::test_R16_the_macros_price_the_counterfactuals_they_name PASSED [ 89%]
tests/test_R16_claims.py::test_R16_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 89%]
tests/test_R16_claims.py::test_R16_the_headline_macros_agree_with_the_frames_they_are_computed_from PASSED [ 90%]
tests/test_R16_claims.py::test_R16_every_produced_text_file_ends_in_a_newline PASSED [ 90%]
tests/test_R16_claims.py::test_R16_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 90%]
tests/test_R16_claims.py::test_R16_the_produced_sources_carry_no_banned_construct PASSED [ 91%]
tests/test_R16_claims.py::test_R16_report_the_census_against_its_witness PASSED [ 91%]
tests/test_R16_claims.py::test_R16_report_the_three_dating_arms PASSED   [ 91%]
tests/test_R16_claims.py::test_R16_report_the_set_behind_the_step_of_one PASSED [ 92%]
tests/test_R18_claims.py::test_R18_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 92%]
tests/test_R18_claims.py::test_R18_the_grids_have_the_cardinality_their_specification_fixes PASSED [ 92%]
tests/test_R18_claims.py::test_R18_the_amplitude_grid_is_the_one_the_design_specifies PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_lag_one_autocorrelation_column_is_twice_the_amplitude PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_non_centrality_column_closes_its_own_geometric_sum PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_analytic_power_column_is_the_non_central_chi_square_tail PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_analytic_power_is_monotone_in_both_of_its_arguments PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_deviation_column_is_the_difference_it_names PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_wilson_intervals_agree_with_the_roots_of_the_score_equation PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_size_of_the_test_covers_the_nominal_level_at_every_horizon PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_null_p_values_are_calibrated_against_the_kolmogorov_limit PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_empirical_curve_matches_the_analytic_one_inside_the_local_domain PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_detectable_amplitude_solves_its_own_analytic_equation PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_detectable_amplitude_halves_when_the_horizon_quadruples PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_non_centrality_at_eighty_percent_power_is_a_constant_of_the_test PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_application_arms_carry_the_two_grids_they_borrow PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_realised_penalty_matches_its_target_where_the_target_is_attainable PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_measured_sign_streams_sit_below_the_detectable_amplitude PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_power_at_the_measured_autocorrelation_is_the_analytic_one PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_ljung_box_rejection_of_both_arms_covers_the_nominal_level PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 99%]
tests/test_R18_claims.py::test_R18_the_headline_macros_agree_with_the_frames_they_are_computed_from PASSED [ 99%]
tests/test_R18_claims.py::test_R18_the_reported_detectable_amplitude_is_the_one_the_analytic_law_gives PASSED [ 99%]
tests/test_R18_claims.py::test_R18_report_the_bound_the_repository_can_state PASSED [100%]

======================= 306 passed in 111.87s (0:01:51) ========================
```
