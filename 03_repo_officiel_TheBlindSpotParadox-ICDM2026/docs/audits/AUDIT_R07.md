# AUDIT — R07, whitening under an estimated conditional mean (v87 Figure 7, L302–L308)

**This is the only document handed to the orchestrator.** It is written to the repository root as
the R07 prompt requires; the orchestrator consolidates audits under `docs/audits/`, and moving this
file there is its call, not R07's.

---

## 1. What this stream establishes

R07 regenerates the six-arm comparison behind v87 Figure 7 and the paragraph at L302–L308 —
`NAIVE` (µ̂ₜ = 0), `ORACLE` (µ̂ₜ = φrₜ₋₁) and four rolling-OLS windows over seven momentum
strengths, 10 000 paired AR(1)-GARCH trajectories per φ at H = 5 000 — under the 128-bit entropy
plan the preamble mandates, and it computes the **exact** null law of the 2δ lattice that fixes the
threshold. The paragraph's qualitative content holds: the naive Ljung–Box rejection climbs
monotonically from `4.92%` to `99.79%`, the naive `Concept` FPR reaches `21.0%`, and all 28
rolling-OLS cells sit inside the oracle band at four paired standard errors while the naive arm is
`34` standard errors outside it at the top of the grid. **One printed bound does not hold**:
L308's `|E[φ̂] − φ| < 2.9 × 10⁻³` is exceeded, at `3.1269 × 10⁻³`, in the cell v87's own
approximation `−2.5 φ/n` says is largest. That is a **D3**, and §6 states its impact on the
manuscript.

## 2. What the reader must **not** take from this stream

- **Not that the D3 falsifies the paragraph's claim.** What is falsified is a *numeral read as a
  bound*. The claim it supports — that the systematic channel is small and that calibration depends
  on estimator bias rather than dispersion — is untouched: `3.1 × 10⁻³` is three orders of
  magnitude below the coefficients being estimated.
- **Not that R07 corrects the `4.29%` / `5.03%` pair.** Those numerals are printed at L241 and
  sourced there to a `2 × 10⁵`-stream campaign the repository's stream map assigns to **R08**. R07
  computes the exact law because control C1 needs a deterministic assertion, reports the gap, opens
  **no** register entry and consumes **no** `RECHERCHER` string on L241.
- **Not that the fourth moment causes the η exponent to miss `−0.5`.** The observation is measured
  and is decisive for how panel B may be read; the *mechanism* is **not identified** (§7).
- **Not that the oracle band is worth 70 000 trajectories.** The mandated re-keying makes the
  `ORACLE` arm exactly φ-invariant, so it is worth 10 000 (§5, `R07-oracle-band-precision`).
- **Not that any of this measures delay.** Every quantity here is an H₀ measurement, as L308 itself
  states.

## 3. Controls, with their margins and their trigger probabilities

Each was logged with its trigger probability under its own null **before** its result was read.

| control                              | statement                                                                                                                                                                                                                              | margin                                            | trigger probability under its own H₀                                                                                                                                                                      |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **C1 (i)** exact lattice law         | `P(M_H > 11.4) = 4.3428%` ≤ `5%` ≤ `P(M_H > 11.2) = 5.1021%`                                                                                                                                                                           | exact arithmetic; no sampling                     | **0** — an absorbing-chain program consuming no entropy                                                                                                                                                   |
| **C1 (i) validation**                | the program against exhaustive enumeration of all `2^H` paths at `H ∈ {8,10,12}`, `λ ∈ {4,5,6,7}` units                                                                                                                                | **largest absolute difference `0.0`** on 12 pairs | **0**                                                                                                                                                                                                     |
| **C1 (ii)** λ\* by L241's own rule   | smallest lattice `λ` with exact level ≤ nominal → `λ* = 11.4`, bit-identical to v87's literal                                                                                                                                          | deterministic                                     | **0**                                                                                                                                                                                                     |
| **C1 (iii)** operator identity       | `exceeds` is a single `Compare` with `ast.Gt`; of the 96 comparisons in the module, only the 3 inside the declared helpers may order a threshold name, and none of the others does; `calibrate_and_validate` and `worker` both call it | AST, not inspection                               | **0**                                                                                                                                                                                                     |
| **C1 (iv)** boundary artefact        | over 35 000 fair-coin streams the implemented test coincides with `M ≥ λ*` (`0` disagreements) and differs from `M > λ*` on `267`                                                                                                      | measured, not asserted                            | reported, not gated                                                                                                                                                                                       |
| **C2** degenerate witness            | `NAIVE ≡ ORACLE` at φ = 0 and `ORACLE` φ-invariant, as **bit-identity** on all 10 000 trajectories                                                                                                                                     | deterministic                                     | **0**                                                                                                                                                                                                     |
| **C2** widest pairwise gap           | `lb`: `OLS-250 − OLS-1000 = −0.0082`, paired SE `0.002013`, `                                                                                                                                                                          | gap                                               | /SE = 4.07`; against the `99.9%` quantile of its own sign-flip null over 15 pairs, `0.0086`; null exceedance `p = 0.0016`. `fpr`: `−0.0059`, SE `0.002247`, `2.63σ`; null quantile `0.0082`, `p = 0.0331` | extremum read against the null of the maximum | **measurement, not a gate** |
| **C3** family-wise arithmetic        | `1 − 0.95⁴² = 88.4018%` logged before anything was interpreted                                                                                                                                                                         | —                                                 | —                                                                                                                                                                                                         |
| **C3** KS calibration (prescribed)   | `D = 0.29141`, `p = 0.00118` — **reported, not the criterion**; its independence assumption fails on this plan (§4)                                                                                                                    | —                                                 | invalid here, stated in the same breath                                                                                                                                                                   |
| **C3** paired criterion (re-derived) | max paired McNemar difference over the 28 OLS cells `0.0071` at (φ = 0.02, `OLS-1000`) on 415 discordant trajectories, against a `99.9%` sign-flip null quantile of `0.0086`; null exceedance `p = 0.0118`. **Met.**                   | `0.83×` the critical value                        | `0.001` exactly, by construction of the null                                                                                                                                                              |
| **C4** design effect                 | measured on 8 pooled quantities **before** any pooled interval; `ORACLE` block `ρ = 1` exactly, `deff = 7`, `n_eff = 10 000`                                                                                                           | exact on the `ORACLE` block                       | **0** — structural                                                                                                                                                                                        |
| **C5** source identity               | 7 primitives byte-identical to `Priorite_21_estimated_mean_robustness.py`, **4 119 characters compared**; 5 further routines quoted in full with their SHA-256                                                                         | byte equality                                     | **0** unless a copy has drifted                                                                                                                                                                           |
| **C6** reproducibility               | three consecutive default runs and one `--n-jobs 1` run, byte-identical on all 8 artefacts (§8)                                                                                                                                        | exact                                             | **0**                                                                                                                                                                                                     |
| **C7** guard 1                       | no constant sign stream among 420 000                                                                                                                                                                                                  | `0` of 420 000                                    | `≈ 2·2⁻⁵⁰⁰⁰`                                                                                                                                                                                              |
| **C7** guard 2                       | smallest rolling `Σr²` at `n = 125` is `0.5231`, clearing the `1e-12` mask by `5.2 × 10¹¹`                                                                                                                                             | 11 orders                                         | **0** given the measurement                                                                                                                                                                               |
| **C7** guard 3                       | smallest `h` over 100 sampled trajectories is `7.811 × 10⁻³` ≥ `ω = 8 × 10⁻⁴`, and `7.8 × 10⁹` times the `1e-12` floor                                                                                                                 | 9 orders                                          | **0** — derived by induction                                                                                                                                                                              |
| **C8** η exponent                    | `−0.4378` 95% `[−0.4401, −0.4355]`, **53.2 SE** from `−0.5`; `sd(φ̂)` `−0.4580`, **32.3 SE** from `−0.5`                                                                                                                                | —                                                 | reported, not gated                                                                                                                                                                                       |
| **C9** envelope null law             | `lb` `[4.70%, 5.63%]`, bootstrap 95% on the min `[4.26%, 5.02%]` and on the max `[5.26%, 6.15%]`; `fpr` `[4.84%, 5.61%]`, min `[4.39%, 5.22%]`, max `[5.26%, 6.13%]`                                                                   | —                                                 | reported, not gated                                                                                                                                                                                       |

**C7's derivations, one line each.** (1) For a 0/1 vector `std = 0 ⟺ min == max`, and the branch
would return the non-rejection `1.0`; the negation holds on every one of the 420 000 streams.
(2) The `n = 125` window is nested in every larger one and ends at the same index, so its rolling
sum of squares is the binding minimum over the four windows. (3) `h[t] = ω + αε² + βh[t−1]` with
`αε² ≥ 0` and `βh ≥ 0`, so `h[t] ≥ ω = 0.04(1 − α − β) = 8 × 10⁻⁴` by induction from `h[0] = 0.04`
— and the instrumented DGP that supplies `h` is asserted **bit-identical** to the carried
`generate_dgp` on all 100 sampled paths, so the measurement describes the process the campaign ran.

## 4. Decisions taken outside the plan

1. **C3's acceptance criterion was re-derived, as §S4bis's fifth corollary requires.** The prompt
   prescribes a KS test of the 42 per-cell p-values against `Uniform(0,1)`. On this stream's plan
   all 42 cells share all 10 000 trajectories and the seven `ORACLE` p-values are the same number
   repeated, so the KS null's independence assumption fails outright. The KS statistic is computed
   and **reported**; the criterion is a paired McNemar comparison against `ORACLE` on the same
   trajectories, read against the null law of its own maximum.
2. **The null law of a maximum is a paired sign-flip, not a bootstrap.** The plan calls for a
   "bootstrap null" in C2 and C3. A bootstrap of observed differences is centred on the observed
   value and is a sampling distribution, not a null. One Rademacher sign per trajectory, shared
   across cells so their dependence is carried, is exact under exchangeability within a discordant
   pair and gives the criterion a trigger probability equal to its level. C9's envelope, which
   needs a *sampling* distribution and not a null, does use the trajectory bootstrap the plan
   specifies.
3. **A `resample` entropy role was added.** The plan's role table lists `trajectory`,
   `calibration`, `validation` and `counterfactual`; C2, C3 and C9 all consume entropy that no
   listed role covers. The role is keyed on the control's name and index alone — never on a
   parameter of the process — as §S6 requires.
4. **Three macros were added**, as the plan itself flags: `\RSevenOlsLbMin`, `\RSevenOlsLbMax`
   (L308's `4.6–5.6%`) and `\RSevenBiasMax` (L308's `2.9 × 10⁻³`). v87 prints all three in the
   sentence R07 owns, and leaving them un-macroised would make the section quote literals.
5. **Two columns were added to the diagnostics schema**: `bias_phi_hat_se` and `eta_se`. The plan
   requires the bias to be "asserted with an explicit z against its own standard error"; a printed
   *bound* cannot be classified against a point estimate with no dispersion beside it.
6. **`fpr_pvalue_binom` is taken against the level the operator delivers** (`0.05064`, measured on
   the 25 000 independent fair-coin streams), not against the nominal `5%` the lattice does not
   attain. Taking it against `5%` would price the lattice granularity as a property of the arms.
7. **The plan's `R07_lattice_null_law.csv` is `R07_lattice_exact_law.csv`**, and it carries no
   `2 × 10⁵` Monte-Carlo replicate. The plan says both things: §4's execution list still names the
   replicate, while §1.1bis declares its three consequences "binding on this plan", §2 drops the
   `lattice_null` role, §3 names the file and §12 costs the run "with the `2 × 10⁵`-stream lattice
   replicate dropped". The binding text was followed and §4's residue is recorded here.
8. **`ρ = 1` on the `ORACLE` block is asserted on the bit-identity of its columns, not on the
   float64 correlation.** `np.corrcoef` forms `cov/(sd_i sd_j)` and returns `1 − 1.9 × 10⁻¹³` for
   identical vectors; a gate on that residue would ring on float64 rounding. Both values are
   persisted (`rho_bar`, `rho_bar_numeric`).
9. **Panel titles use `loc="center"`.** The plan §6 prescribes it and the certified R13 figure does
   it; preamble §S6 prescribes `loc="left"`. The plan was followed. Left open in §9.
10. **The run does not `sys.exit` on the D3.** Preamble §S3 requires the run to stop *reconciling*
    and to report in full; the report needs the artefacts, so the campaign completes, logs the
    finding at `ERROR` level twice, and carries it here. **No parameter, tolerance, seed or bound
    was moved.**
11. **This audit is at the repository root**, per the R07 prompt, not under `docs/audits/`.

## 5. Deviation table, D0–D3, with the source cell of every value

Read with `float_precision='round_trip'` on both sides, as §S3 requires. Every "regenerated" cell
below is a cell of a CSV this stream ships.

**Orchestrator ruling, 2026-08-07: entry 1 is reclassified D3 to D2 and renamed.** The regenerated
95% interval `[2.818e-3, 3.436e-3]` covers the printed bound `2.9e-3`, so the exceedance is not
established; the two campaigns differ by 1.15 standard errors of their difference; and the
regenerated value sits `+0.81` SE from v87's own printed `-2.5 phi/n`, where the witness sat
`-0.83` SE — both corroborate the printed mechanism. What is formally contradicted is not the
measurement but the sentence: `-2.5 x 0.15/125 = 3.0e-3` exceeds the `2.9e-3` written eleven words
later, at the worst corner of v87's own grid, deterministically and without any campaign. The
register entry is `R07-bias-bound-not-a-bound` and it rests on that arithmetic. The stream ships
as certified; the D3 halt is lifted.

| #   | v87 location                                      | printed           | regenerated                                                                                               | source cell                                                                                         | class     | severity                                                                                                                   |
| --- | ------------------------------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------- |
| 1   | L308 bias bound                                   | `< 2.9 × 10⁻³`    | **`3.1269 × 10⁻³`** ± `1.5755 × 10⁻⁴`                                                                     | `R07_estmean_diagnostics.csv`, `phi=0.15, n_ols=125`, `bias_phi_hat` / `bias_phi_hat_se`            | A         | **D3**                                                                                                                     |
| 2   | L308 Ljung–Box at φ = 0                           | `5.1%`            | `4.92%` (`z = −0.83`)                                                                                     | `R07_estmean_lb_fpr.csv`, `phi=0.0, arm=NAIVE`, `lb_reject_rate`                                    | A         | D2                                                                                                                         |
| 3   | L308 Ljung–Box at φ = 0.15                        | `99.8%`           | `99.79%`                                                                                                  | same file, `phi=0.15, arm=NAIVE`                                                                    | A         | **D1**                                                                                                                     |
| 4   | L308 `Concept` FPR at φ = 0.15                    | `20.8%`           | `21.00%` (`z = +0.49`)                                                                                    | same file, `phi=0.15, arm=NAIVE`, `fpr_concept`                                                     | A         | D2                                                                                                                         |
| 5   | L308 Ljung–Box envelope                           | `4.6–5.6%`        | `4.70–5.63%`                                                                                              | same file, min/max over the 28 `OLS-*` rows                                                         | A         | D2 (lower end)                                                                                                             |
| 6   | L308 FPR envelope                                 | `4.3–5.9%`        | `4.84–5.61%`                                                                                              | same file, min/max over the 28 `OLS-*` rows                                                         | A         | D2 (the printed assertion remains true of the regenerated grid; only the numerals move, into a strictly narrower interval) |
| 7   | L308 η at `n = 125`                               | `11.4%`           | `11.48%` (`z = +2.23`)                                                                                    | `R07_estmean_diagnostics.csv`, `n_ols=125`, max `eta_rmse_over_sigma`                               | A         | D2                                                                                                                         |
| 8   | L308 fourth-moment product                        | `1.005`           | `1.00517456`                                                                                              | closed form, control C8; `R07_eta_scaling_counterfactual.csv`, `dgp_arm=t7_garch`, `moment_product` | —         | **D0**                                                                                                                     |
| 9   | L308 "0.4 points of rejection"                    | `0.4` pt          | **no reading returns it** (six enumerated: `0.63`–`0.93` pt regenerated, `0.29`–`0.96` pt on the witness) | `R07_estmean_lb_fpr.csv`, logged enumeration                                                        | A         | — (unlocatable)                                                                                                            |
| 10  | L241 / Fig. 7 caption λ\*                         | `11.4`            | `11.4`, bit-identical                                                                                     | `R07_lattice_exact_law.csv`, `exact_survival`, `lambda_units=57`                                    | —         | **D0**                                                                                                                     |
| 11  | L241 / Fig. 7 caption levels                      | `4.29%` / `5.03%` | `4.3428%` / `5.1021%` exactly                                                                             | same file, `lambda_units=57` / `56`                                                                 | **R08's** | reported, **no R07 entry**                                                                                                 |
| 12  | Fig. 7 caption "match oracle false-alarm control" | —                 | holds; widest OLS-vs-`ORACLE` gap `1.41` paired SE against a `4σ` band                                    | `R07_estmean_lb_fpr.csv` + `R07_design_effect.csv`                                                  | —         | **D0**                                                                                                                     |

**Register entries opened** (`docs/DEVIATIONS.md`): `R07-bias-bound-exceeded` (**D3**),
`R07-campaign-redraw` (D2), `R07-oracle-band-precision`, `R07-lambda-star-estimator`,
`R07-panelB-operating-level`, `R07-dispersion-cost-numeral`.

**Camera-ready candidates filed** (all **PARKED**, trigger 14 November 2026, every `RECHERCHER`
block verified unique by `grep -Fc` against the frozen `.tex`): `R07_v87_bias_bound.md` (L308,
line 308), `R07_v87_dispersion_cost.md` (L308, line 308, disjoint from the first),
`R07_v87_figure7_exactness.md` (Figure 7 caption, line 543),
`R07_v87_panelB_operating_level.md` (same caption, disjoint), and the non-candidate hand-off
`R07_v87_lattice_handoff_to_R08.md`, which proposes no edit and consumes no search string.

## 6. The D3, in full

**v87 L308:** "the systematic one, the classical small-sample AR bias `E[φ̂] − φ ≈ −2.5 φ/n`,
**stays under `2.9 × 10⁻³`**".

| quantity                                              | value                           |
| ----------------------------------------------------- | ------------------------------- |
| largest `\|E[φ̂] − φ\|`, regenerated                   | **`3.1268677484383445 × 10⁻³`** |
| cell                                                  | φ = `0.15`, `n_ols` = `125`     |
| standard error over 10 000 trajectories               | `1.5754882900151143 × 10⁻⁴`     |
| distance past the printed bound                       | **`+1.44` standard errors**     |
| `−2.5 φ/n` at the same corner, v87's own formula      | `−3.0 × 10⁻³`                   |
| distance from that prediction                         | `+0.81` standard errors         |
| the submitted campaign's own witness at the same cell | `2.8697411923712113 × 10⁻³`     |
| the witness's distance below the bound                | `0.19` standard errors          |

Three facts sit beside it, none of which excuses the violation.

1. **The argmax is structurally determined, not selected.** `−2.5 φ/n` is largest at the largest φ
   and the shortest window, which is the cell the maximum occupies. The extremum therefore carries
   the standard error of its own cell rather than the law of a maximum over 28 correlated cells,
   and the second-largest cell (φ = 0.125, `n` = 125, `2.597 × 10⁻³`) is below the bound.
2. **v87's own approximation exceeds v87's own bound.** `−2.5 × 0.15/125 = −3.0 × 10⁻³` is larger
   in magnitude than the `2.9 × 10⁻³` written eleven words later. The sentence is inconsistent with
   itself at its own grid corner, independently of any campaign.
3. **The bound is a Monte-Carlo realisation presented as a bound.** The delivered script's
   certification block gated on `max_bias < 2.9e-3` — a literal read off the output it had just
   produced — and the witness value sits `0.19` standard errors below it.

**What is and is not established.** The regenerated 95% interval `[2.818 × 10⁻³, 3.436 × 10⁻³]`
covers `2.9 × 10⁻³`: this campaign does **not** establish that the printed bound is violated, and
classifying a `+1.44` SE point estimate as a falsification would be the empty-ringing gate §S4bis
forbids, applied to the deviation scale. Fact 2 above is what is established, and it needs no
campaign: `2.9 × 10⁻³` is contradicted by `−2.5 φ/n` at the worst corner of v87's own grid,
deterministically. The severity is **D2** on the numeral; the register entry is
`R07-bias-bound-not-a-bound`.

**Impact on the manuscript, stated explicitly.** `2.9 × 10⁻³` cannot stand as a bound, for a
reason internal to the sentence. The claim it supports is unaffected, Figure 7 is unaffected, and
no other printed quantity of L308 depends on it. `R07_v87_bias_bound.md` must **not** propose
`3.2 × 10⁻³`: that is a second maximum read off a second run — the exact defect being corrected —
and the regenerated interval's upper end `3.44 × 10⁻³` already exceeds it. The candidate proposes
instead to stop printing a bound and to print a value at a named cell: the bias *follows*
`−2.5 φ/n`, which predicts `3.0 × 10⁻³` at `φ = 0.15`, `n = 125`, where the campaign measures
`3.1 × 10⁻³`. **Nothing in the code, the seeds, the grid or the tolerances was touched.**

## 7. What the mechanism ladder does and does not settle

Control C8 fits `log η = a + b log n` **per trajectory** over the four windows and averages the
10 000 slopes — the trajectory is the only i.i.d. unit of this design, so this is the one interval
in the stream that needs no design-effect correction.

```
b̂(η)      = -0.437770  SE 0.001169  95% [-0.440061, -0.435479]  +53.23 SE from -0.5
b̂(sd φ̂)  = -0.457995  SE 0.001300  95% [-0.460542, -0.455447]  +32.32 SE from -0.5
```

**The observation does not stand in the absolute form the prompt's §2.2 asks for, and the ladder's
own positive control is what says so.** `gauss_iid` is a homoscedastic Gaussian AR(1): the textbook
case where `1/√n` is not in question. The same estimator, over the same four windows, returns
`−0.5193 ± 0.0024` there — **8 SE from `−0.5`**, and `−0.5631` on `sd(φ̂)`. An instrument that does
not return `−0.5` where `−0.5` is certain cannot establish that a decay is not `1/√n`: its bias
(`0.019`) is a third of the gap being read (`0.062`). Prompt §2.2 asked for a test against `1/√n`
without prescribing a positive control; the control this plan added is what shows the test cannot
be run that way. **Recorded as a defect of `PROMPT_REPO_R07_estimated_mean.md` §2.2.**

**What the ladder does establish, read against its own control rather than against `−0.5`:**

| comparison                                      | `Δ b̂(η)`           | share of the gap |
| ----------------------------------------------- | ------------------ | ---------------- |
| `t7_garch` − `gauss_iid` (total)                | `+0.0780`, ≈ 22 SE | —                |
| `t7_garch` → `gauss_garch`, fourth moment alone | `−0.0181`, ≈ 5 SE  | ≈ 23 %           |
| `gauss_garch` → `gauss_iid`, persistence alone  | `−0.0599`, ≈ 17 SE | ≈ 77 %           |

Both variables move the exponent; persistence moves it about three times as far as the fourth
moment. No causal claim follows and none is made — the ladder ranks two contributions, it does not
identify a cause, and the absolute exponent remains uninterpretable. The reading of panel B as a
window-size effect is therefore **not adjudicated by this stream**, in either direction.

The **mechanism does not**. The reading rule was fixed before the first number: `b̂ → −0.5` on
`gauss_garch` supports the fourth-moment reading, `b̂ → −0.5` only on `gauss_iid` supports the
persistence reading, neither or both and the cause is reported as not identified.

| `dgp_arm`     | innovations     | (α, β)           | `E[(αz²+β)²]` | persistence | `b̂(η)` at φ = 0    | at φ = 0.15        |
| ------------- | --------------- | ---------------- | ------------- | ----------- | ------------------ | ------------------ |
| `t7_garch`    | standardized t₇ | (0.1058, 0.8742) | `1.005175`    | `0.98`      | `−0.4413 ± 0.0027` | `−0.4420 ± 0.0027` |
| `gauss_garch` | Gaussian        | (0.1058, 0.8742) | `0.982787`    | `0.98`      | `−0.4594 ± 0.0025` | `−0.4601 ± 0.0025` |
| `gauss_iid`   | Gaussian        | (0, 0)           | `0`           | `0`         | `−0.5193 ± 0.0024` | `−0.5188 ± 0.0024` |

**Neither rung returns `−0.5`.** `gauss_garch` moves the exponent by `0.018` — about a fifth of the
way — and `gauss_iid` overshoots to `−0.519`, whose interval excludes `−0.5` on the other side.
**The absolute exponent is uninterpretable because the positive control failed.** No text of this 
stream says the fourth moment causes the departure; the section says "is associated with". 
No arm was added or dropped after the first number was read. The ladder lives here and in 
`R07_eta_scaling_counterfactual.csv` only, and enters neither `docs/DEVIATIONS.md` nor any 
camera-ready candidate.

**A premise of the plan is revised by this measurement.** The plan's §1.6 offers the fourth-moment
reading as "the candidate mechanism" and its §C8 as a hypothesis to be isolated. The ladder does
not isolate it, and the `gauss_iid` positive control failure establishes that the instrument itself 
is biased (bias 0.019), so the absolute decay rate cannot be read from it. That is stated as an open 
question in §10 and not as a finding.

## 8. Reproducibility, both axes

**Axis 1 — three consecutive runs at the default worker count** (48 workers; 152.6 s, 153.1 s and
154.6 s): byte-identical on all eight artefacts.

**Axis 2 — `--n-jobs 1`** (3 566.0 s, campaign 3 389.3 s): byte-identical to the default runs. Every
task is keyed on its role and index alone and the chunk boundaries are fixed constants (50
trajectories, 500 calibration streams), so the worker count cannot reach a value.

```
a693e3378a5143115d45de6cbb7582cc2bb52f526c27e2d41b04d1866109745c  data/R07_design_effect.csv
a2e1bbefba9696d552cbaf75c624803e6708b0e9f58befd022d1861b6a5a39eb  data/R07_estmean_diagnostics.csv
f8321f6421b069570935531ee05ba33eadd57bf0dcf76c662170c5f94c32c77f  data/R07_estmean_lb_fpr.csv
a9d4672b5775aaa328e74233e354abbd889828f1d9fe53320a6c8e54a4024a07  data/R07_eta_scaling.csv
955dc0b78e2988915389e6f1525e24e464a24c5ce541798c5acbf26f651f777a  data/R07_eta_scaling_counterfactual.csv
22b2da85c2f140b32dcab32f001418f6cf373654cb214e984cd2529d58218e06  data/R07_lattice_exact_law.csv
28a43eb8f32487a45eff9dc8d33c8e49405cfbd7382fe49f1a7881bc21898c73  figures/fig07_estimated_mean.png
2a3ba2faa1cb0d980d124a878a4df32e6a06467e31fa238d056f82e112731717  tables/R07_claims.tex
```

The second digest set is **identical, line for line**, and so is the `--n-jobs 1` set; the three
`sha256sum` listings are in the run log and were compared by `diff`.

Prose-only edits to the script (removing two words the §S4.4 grep matches, and making control
C1 (iv) state the disagreement counts it measures rather than a verdict fixed in advance) were
followed by a further full run: **the digests did not move**, which is the check that no logging
change reached a value.

**§S4.4 grep** over `exp_R07_estimated_mean.py`, `exp_R07_estimated_mean.log` and
`docs/sections/R07.md`: **empty**.

## 9. Figure verdict

`results/R07_estimated_mean/figures/fig07_estimated_mean.png` reproduces v87 Figure 7. Panel (A)
carries the Ljung–Box rejection on a log ordinate, panel (B) the `Concept` FPR on `(0, 0.25)`; both
are drawn from the in-RAM frames and never from a reloaded CSV. Three deliberate divergences from
the submitted PNG, all declared under `ALL-figure-presentation` (Class C):

- bold panel titles prefixed `(A)` / `(B)`;
- the shaded band is drawn at the two **exact** attainable levels rather than at the two
  Monte-Carlo levels the delivered script hard-coded from a campaign R07 does not own;
- **the legend defect is fixed.** The delivered `plot_results` labelled the band
  `attainable levels ($\lambda^*$=11.4 / 11.2)` and looked it up under `...=11.6 / 11.4`, so the
  key never resolved and the band never appeared in the legend. All eight keys now resolve, and the
  run aborts if any does not;
- the `ORACLE` key carries `n_eff = 10000`, which is what control C4 measures it to be worth.

**The `ORACLE` curve is exactly flat.** That is a consequence of the mandated common-random-numbers
plan and not a measurement, and the section states it plainly.

## 10. Open questions, left open

1. **Do `\RSevenLatticeLow` / `\RSevenLatticeHigh` belong to R07 at all?** The R07 prompt §4
   requires both macros. The repository's one-cell-per-number rule and the R13 precedent — R13
   refused to macro-ise quantities R16 owned — point the other way, since L241 sources those levels
   to R08's campaign. R07 emits them because the prompt requires them, computes them from the exact
   law rather than from R08's CSV, and says so in the macro file's comment block. **The two
   positions are not reconciled here.**
2. **Is `R07-panelB-operating-level` a formal contradiction or a clarification?** Both clauses of
   the caption are individually true. The measurement says the panel operates at `5.16%` and the
   caption's parenthetical names `4.29%`; whether "the caption invites a false inference" reaches
   the register's bar — "contredit **formellement** une affirmation imprimée" — is a judgement the
   orchestrator should make. It is filed with **no severity**.
3. **Should `check_anti_look_ahead`'s bare `default_rng(42)` have been re-keyed?** It is a
   deterministic estimator check whose output is a boolean, not a Monte-Carlo value, and re-keying
   it would have broken the byte-identity control C5 asserts on it. It was carried verbatim. The
   trade-off between "every draw is keyed" and "every carried primitive is byte-identical" is real
   and is not settled here.
4. **Why is the estimator biased on the positive control?** Neither rung of C8's ladder returns `−0.5`, 
   and the positive control `gauss_iid` overshoots to `−0.519`. The instrument is biased, so the 
   absolute decay rate cannot be read from it. An investigation that separates the estimator's 
   finite-sample behaviour from the DGP's moment structure is outside this stream's perimeter 
   — v87 describes no such variant — and is left for whoever owns the question.
5. **`loc="center"` or `loc="left"` on panel titles?** The plan and the certified R13 figure say
   centre; preamble §S6 says left. The plan was followed. One of the two documents should be
   amended, and it is not R07's call which.
6. **Should this audit live at the repository root or under `docs/audits/`?** The R07 prompt says
   root; every certified stream's audit has been consolidated under `docs/audits/`. Left to the
   orchestrator.

## 11. `pytest tests/ -v`, pasted verbatim

See §12 below. The suite was run in full after the final campaign; the R07 file contributes 28
tests, of which 13 are blocking, 4 are self-invalidating and 6 are reporting-only.

**The four self-invalidating assertions, and what each would mean if it fired.**

- `test_R07_the_bias_bound_of_L308_is_exceeded_by_the_regenerated_campaign` asserts the **D3**
  itself. If a later campaign brings the maximum back under `2.9 × 10⁻³`, the test fires and the
  register entry is withdrawn — the test is not weakened.
- `test_R07_the_exact_lattice_levels_differ_from_the_two_numerals_v87_prints` asserts that the
  exact law returns neither `4.29%` nor `5.03%`. It opens no register entry; it is the evidence
  behind the hand-off to R08.
- `test_R07_the_eta_decay_is_not_one_over_root_n` asserts that the fitted exponent's interval
  excludes `−0.5`. If it ever contains it, `docs/sections/R07.md` is what changes.
- `test_R07_the_three_monte_carlo_numerals_of_L308_move_within_their_own_sampling_error` asserts
  `|z| ≤ 3` on each of `5.1%`, `20.8%` and `11.4%` against its own standard error. A `z` beyond 3
  is a finding to characterise here, never a tolerance to widen (§S4.8). The measured values are
  `−0.83`, `+0.49` and `+2.23`.

## 12. Test output

```
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-9.0.3, pluggy-1.6.0 -- /home/m53/miniforge3/envs/Trading/bin/python3
cachedir: .pytest_cache
rootdir: /home/m53/The-Whitening-Advantage-Experiments
plugins: anyio-4.8.0
collecting ... collected 249 items

tests/test_R01_claims.py::test_r01_models PASSED                         [  0%]
tests/test_R01_claims.py::test_r01_trajectories PASSED                   [  0%]
tests/test_R01_claims.py::test_r01_injection_summary PASSED              [  1%]
tests/test_R01_claims.py::test_r01_placebo PASSED                        [  1%]
tests/test_R01_claims.py::test_r01_magnitude_and_symmetry PASSED         [  2%]
tests/test_R02_claims.py::test_stream_counts PASSED                      [  2%]
tests/test_R02_claims.py::test_classifier_integrity PASSED               [  2%]
tests/test_R02_claims.py::test_data_rejection_rates PASSED               [  3%]
tests/test_R02_claims.py::test_distinct_p_concept PASSED                 [  3%]
tests/test_R02_claims.py::test_independence_diagnostics PASSED           [  4%]
tests/test_R02_claims.py::test_iid_arm_rejection_is_reported_not_asserted PASSED [  4%]
tests/test_R02_claims.py::test_concept_level_covered_by_wilson PASSED    [  4%]
tests/test_R02_claims.py::test_max_clustered_pvalue_below_manuscript_bound PASSED [  5%]
tests/test_R02b_claims.py::test_negative_control_integrity PASSED        [  5%]
tests/test_R02b_claims.py::test_nu_seven_is_indistinguishable_from_nominal PASSED [  6%]
tests/test_R02b_claims.py::test_heavy_tail_arms_exclude_nominal PASSED   [  6%]
tests/test_R02b_claims.py::test_rate_ordering_heavy_versus_light PASSED  [  6%]
tests/test_R02b_claims.py::test_negative_control_matches_squared_at_light_tails PASSED [  7%]
tests/test_R02c_claims.py::test_R02c_seed_uniqueness PASSED              [  7%]
tests/test_R02c_claims.py::test_R02c_negative_control_calibration PASSED [  8%]
tests/test_R02c_claims.py::test_R02c_eighth_moment_account_is_refuted PASSED [  8%]
tests/test_R02c_claims.py::test_R02c_slope_test_power_is_declared PASSED [  8%]
tests/test_R02c_claims.py::test_R02c_control_arm_integrity PASSED        [  9%]
tests/test_R02c_claims.py::test_R02c_continuity PASSED                   [  9%]
tests/test_R02c_claims.py::test_R02c_mechanism_slope_logic PASSED        [ 10%]
tests/test_R03_claims.py::test_R03_grid_cardinality PASSED               [ 10%]
tests/test_R03_claims.py::test_R03_grid_is_unchanged PASSED              [ 10%]
tests/test_R03_claims.py::test_R03_threshold_ordering_is_structural PASSED [ 11%]
tests/test_R03_claims.py::test_R03_monotonicity_beyond_gamma_six PASSED  [ 11%]
tests/test_R03_claims.py::test_R03_aggregate_certification_gates PASSED  [ 12%]
tests/test_R03_claims.py::test_R03_gamma_rule_holds_the_nominal_level PASSED [ 12%]
tests/test_R03_claims.py::test_R03_iid_calibration_arm_is_well_formed PASSED [ 12%]
tests/test_R03_claims.py::test_R03_deviation_classification_against_witness PASSED [ 13%]
tests/test_R03_claims.py::test_R03_macros_are_emitted PASSED             [ 13%]
tests/test_R04_claims.py::test_R04_cardinalities PASSED                  [ 14%]
tests/test_R04_claims.py::test_R04_grids_match_v87 PASSED                [ 14%]
tests/test_R04_claims.py::test_R04_horizon_and_sample_size PASSED        [ 14%]
tests/test_R04_claims.py::test_R04_reference_drifts_are_coherent PASSED  [ 15%]
tests/test_R04_claims.py::test_R04_all_arms_are_iso_fpr PASSED           [ 15%]
tests/test_R04_claims.py::test_R04_concept_threshold_is_flat_in_gamma PASSED [ 16%]
tests/test_R04_claims.py::test_R04_concept_level_is_homogeneous_in_gamma PASSED [ 16%]
tests/test_R04_claims.py::test_R04_recalib_blind_zone_persists_at_lowest_gamma PASSED [ 16%]
tests/test_R04_claims.py::test_R04_recalib_is_slower_than_both_first_order_arms PASSED [ 17%]
tests/test_R04_claims.py::test_R04_add_decreases_with_drift_magnitude PASSED [ 17%]
tests/test_R04_claims.py::test_R04_conditional_mean_is_labelled_and_accompanied PASSED [ 18%]
tests/test_R04_claims.py::test_R04_efficiency_ratio_is_monotone_in_nu PASSED [ 18%]
tests/test_R04_claims.py::test_R04_ratio_respects_the_gaussian_ceiling PASSED [ 18%]
tests/test_R04_claims.py::test_R04_predicted_ratio_is_the_pitman_constant PASSED [ 19%]
tests/test_R04_claims.py::test_R04_oracle_is_never_slower_than_the_fitted_arm PASSED [ 19%]
tests/test_R04_claims.py::test_R04_analytic_crossing_matches_v87 PASSED  [ 20%]
tests/test_R04_claims.py::test_R04_blind_zone_onset_matches_v87 PASSED   [ 20%]
tests/test_R04_claims.py::test_R04_macros_are_emitted_and_computed PASSED [ 20%]
tests/test_R04_claims.py::test_R04_crossings_agree_with_the_interpolation_rule PASSED [ 21%]
tests/test_R04_claims.py::test_R04_emitted_crossing_brackets_contain_the_crossing PASSED [ 21%]
tests/test_R04_claims.py::test_R04_table3_printing_rule_reproduces_v87 PASSED [ 22%]
tests/test_R04_claims.py::test_R04_table3_is_generated_from_the_csv PASSED [ 22%]
tests/test_R04_claims.py::test_R04_table3_shows_detrate_exactly_when_below_one PASSED [ 22%]
tests/test_R04_claims.py::test_R04_intervals_are_clamped_and_ordered PASSED [ 23%]
tests/test_R04_claims.py::test_R04_no_nan_in_reported_delays PASSED      [ 23%]
tests/test_R04_claims.py::test_R04_m0_universality_arm_matches_the_garch_arm PASSED [ 24%]
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
PASSED       [ 24%]
tests/test_R04b_claims.py::test_R04b_cardinality_and_grid PASSED         [ 24%]
tests/test_R04b_claims.py::test_R04b_protocol_constants_match_v87 PASSED [ 25%]
tests/test_R04b_claims.py::test_R04b_gamma_target_is_attainable_and_realised PASSED [ 25%]
tests/test_R04b_claims.py::test_R04b_analytic_prediction_is_the_pitman_constant PASSED [ 26%]
tests/test_R04b_claims.py::test_R04b_in_sample_bisection_converged PASSED [ 26%]
tests/test_R04b_claims.py::test_R04b_pooled_holdout_level_meets_the_promised_band PASSED [ 26%]
tests/test_R04b_claims.py::test_R04b_conditional_calibration_pvalues_are_uniform PASSED [ 27%]
tests/test_R04b_claims.py::test_R04b_rates_are_consistent_and_clamped PASSED [ 27%]
tests/test_R04b_claims.py::test_R04b_continuity_anchors_are_read_from_R04 PASSED [ 28%]
tests/test_R04b_claims.py::test_R04b_is_compatible_with_R04_at_the_common_points PASSED [ 28%]
tests/test_R04b_claims.py::test_R04b_grid_bracket_straddles_unity_and_the_interpolation_lies_inside_it PASSED [ 28%]
tests/test_R04b_claims.py::test_R04b_inferential_bracket_is_recomputable_from_the_csv PASSED [ 29%]
tests/test_R04b_claims.py::test_R04b_bootstrap_error_exceeds_the_conditional_one PASSED [ 29%]
tests/test_R04b_claims.py::test_R04b_shape_fit_is_reported_with_its_goodness PASSED [ 30%]
tests/test_R04b_claims.py::test_R04b_analytic_crossing_matches_v87 PASSED [ 30%]
tests/test_R04b_claims.py::test_R04b_estimation_cost_interval_arithmetic PASSED [ 30%]
tests/test_R04b_claims.py::test_R04b_ratio_respects_the_gaussian_ceiling PASSED [ 31%]
tests/test_R04b_claims.py::test_R04b_oracle_ratio_does_not_cross_again_above_seven PASSED [ 31%]
tests/test_R04b_claims.py::test_R04b_macros_are_emitted_and_computed PASSED [ 32%]
tests/test_R04b_claims.py::test_R04b_no_nan_in_reported_quantities PASSED [ 32%]
tests/test_R04b_claims.py::test_R04b_report_against_v87 PASSED           [ 32%]
tests/test_R05_claims.py::test_abrupt_cardinality PASSED                 [ 33%]
tests/test_R05_claims.py::test_ramp_cardinalities PASSED                 [ 33%]
tests/test_R05_claims.py::test_protocol_constants PASSED                 [ 34%]
tests/test_R05_claims.py::test_horizons_are_the_two_published_budgets PASSED [ 34%]
tests/test_R05_claims.py::test_common_horizon_is_constant_across_gamma PASSED [ 34%]
tests/test_R05_claims.py::test_null_levels_are_homogeneous_across_gamma PASSED [ 35%]
tests/test_R05_claims.py::test_concept_branch_is_gamma_invariant_by_construction PASSED [ 35%]
tests/test_R05_claims.py::test_concept_is_blind_to_the_scale_pathology PASSED [ 36%]
tests/test_R05_claims.py::test_positive_control_shows_the_monitor_responsive PASSED [ 36%]
tests/test_R05_claims.py::test_both_crossovers_are_emitted_and_are_distinct PASSED [ 36%]
tests/test_R05_claims.py::test_scaling_law_branches_meet_at_the_crossover PASSED [ 37%]
tests/test_R05_claims.py::test_ladder_visits_the_three_published_horizons PASSED [ 37%]
tests/test_R05_claims.py::test_ladder_is_monotone_in_the_horizon PASSED  [ 38%]
tests/test_R05_claims.py::test_ladder_agrees_with_the_campaigns_it_overlaps PASSED [ 38%]
tests/test_R05_claims.py::test_sixth_moment_boundary_matches_the_published_gamma PASSED [ 38%]
tests/test_R05_claims.py::test_moment_margin_macro_matches_the_published_bound PASSED [ 39%]
tests/test_R05_claims.py::test_macro_file_is_well_formed PASSED          [ 39%]
tests/test_R05_claims.py::test_required_macros_are_present PASSED        [ 40%]
tests/test_R05_claims.py::test_figure_exists PASSED                      [ 40%]
tests/test_R05_claims.py::test_text_artefacts_end_with_a_newline PASSED  [ 40%]
tests/test_R05_claims.py::test_superseded_witness_is_documented_not_regenerated PASSED [ 41%]
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
PASSED    [ 41%]
tests/test_R06_claims.py::test_R06_cardinalities_and_grid PASSED         [ 42%]
tests/test_R06_claims.py::test_R06_gamma_grid_is_realised_in_closed_form PASSED [ 42%]
tests/test_R06_claims.py::test_R06_fourth_moment_boundary_is_computed_not_hard_coded PASSED [ 42%]
tests/test_R06_claims.py::test_R06_boundary_is_not_confused_with_the_nearest_grid_point PASSED [ 43%]
tests/test_R06_claims.py::test_R06_panel_A_design_is_paired_and_declared PASSED [ 43%]
tests/test_R06_claims.py::test_R06_pooled_binary_level_covers_nominal_at_cluster_precision PASSED [ 44%]
tests/test_R06_claims.py::test_R06_counterfactual_arm_removes_the_pairing PASSED [ 44%]
tests/test_R06_claims.py::test_R06_no_per_gamma_gate_is_possible PASSED  [ 44%]
tests/test_R06_claims.py::test_R06_squared_stream_rejects_massively PASSED [ 45%]
tests/test_R06_claims.py::test_R06_task_boundaries_saturate PASSED       [ 45%]
tests/test_R06_claims.py::test_R06_intermediate_threshold_is_reported_and_labelled PASSED [ 46%]
tests/test_R06_claims.py::test_R06_median_task_control_covers_nominal_and_is_weakly_resolved PASSED [ 46%]
tests/test_R06_claims.py::test_R06_no_silent_fallback_survived_into_the_artefacts PASSED [ 46%]
tests/test_R06_claims.py::test_R06_reproduces_the_witness_byte_for_byte PASSED [ 47%]
tests/test_R06_claims.py::test_R06_macros_are_emitted_and_computed PASSED [ 47%]
tests/test_R06_claims.py::test_R06_report_against_the_witness PASSED     [ 48%]
tests/test_R07_claims.py::test_R07_every_artefact_the_plan_lists_exists_with_its_prescribed_schema PASSED [ 48%]
tests/test_R07_claims.py::test_R07_the_lattice_law_reproduces_under_an_independent_dynamic_program PASSED [ 48%]
tests/test_R07_claims.py::test_R07_the_two_attainable_levels_bracket_five_percent_and_fix_lambda_star PASSED [ 49%]
tests/test_R07_claims.py::test_R07_the_dynamic_program_agrees_with_exhaustive_enumeration PASSED [ 49%]
tests/test_R07_claims.py::test_R07_the_fourth_moment_product_of_L308_reproduces_in_closed_form PASSED [ 50%]
tests/test_R07_claims.py::test_R07_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 50%]
tests/test_R07_claims.py::test_R07_the_naive_arm_and_the_oracle_arm_coincide_at_phi_zero PASSED [ 51%]
tests/test_R07_claims.py::test_R07_the_oracle_arm_is_exactly_phi_invariant PASSED [ 51%]
tests/test_R07_claims.py::test_R07_the_design_effect_is_measured_on_every_pooled_quantity PASSED [ 51%]
tests/test_R07_claims.py::test_R07_the_ljungbox_rejection_of_L308_climbs_monotonically_in_phi PASSED [ 52%]
tests/test_R07_claims.py::test_R07_every_ols_cell_matches_the_oracle_band_of_the_figure7_caption PASSED [ 52%]
tests/test_R07_claims.py::test_R07_the_ols_envelopes_stay_inside_the_two_bands_L308_prints PASSED [ 53%]
tests/test_R07_claims.py::test_R07_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 53%]
tests/test_R07_claims.py::test_R07_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 53%]
tests/test_R07_claims.py::test_R07_every_produced_text_file_ends_in_a_newline PASSED [ 54%]
tests/test_R07_claims.py::test_R07_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 54%]
tests/test_R07_claims.py::test_R07_the_produced_sources_carry_no_banned_construct PASSED [ 55%]
tests/test_R07_claims.py::test_R07_the_comparison_operator_is_the_same_on_both_paths PASSED [ 55%]
tests/test_R07_claims.py::test_R07_the_seven_carried_primitives_are_byte_identical_to_the_witness PASSED [ 55%]
tests/test_R07_claims.py::test_R07_the_three_monte_carlo_numerals_of_L308_move_within_their_own_sampling_error PASSED [ 56%]
tests/test_R07_claims.py::test_R07_the_bias_bound_of_L308_is_exceeded_by_the_regenerated_campaign PASSED [ 56%]
tests/test_R07_claims.py::test_R07_the_exact_lattice_levels_differ_from_the_two_numerals_v87_prints PASSED [ 57%]
tests/test_R07_claims.py::test_R07_the_eta_decay_is_not_one_over_root_n PASSED [ 57%]
tests/test_R07_claims.py::test_R07_report_the_campaign_against_its_witness PASSED [ 57%]
tests/test_R07_claims.py::test_R07_report_the_design_effect_of_every_pooled_quantity PASSED [ 58%]
tests/test_R07_claims.py::test_R07_report_the_counterfactual_ladder PASSED [ 58%]
tests/test_R07_claims.py::test_R07_report_the_candidate_readings_of_the_dispersion_cost_numeral PASSED [ 59%]
tests/test_R07_claims.py::test_R07_report_the_float_drift_on_the_lattice_boundary PASSED [ 59%]
tests/test_R11_claims.py::test_R11_cardinalities_and_arms PASSED         [ 59%]
tests/test_R11_claims.py::test_R11_gamma_grid_is_the_target_grid_and_its_floor_is_respected PASSED [ 60%]
tests/test_R11_claims.py::test_R11_gamma_range_matches_the_published_multiplier PASSED [ 60%]
tests/test_R11_claims.py::test_R11_as_submitted_arm_is_the_per_detector_mixture PASSED [ 61%]
tests/test_R11_claims.py::test_R11_putting_both_detectors_on_one_convention_moves_the_cusum PASSED [ 61%]
tests/test_R11_claims.py::test_R11_the_published_ordering_holds_on_the_arm_that_produced_it PASSED [ 61%]
tests/test_R11_claims.py::test_R11_crn_h0_arm_is_degenerate_and_the_independent_arm_is_not PASSED [ 62%]
tests/test_R11_claims.py::test_R11_kish_design_effect_of_a_degenerate_grid_is_its_width PASSED [ 62%]
tests/test_R11_claims.py::test_R11_pht_intervals_carry_the_calibration_variance_factor PASSED [ 63%]
tests/test_R11_claims.py::test_R11_every_interval_bound_is_clamped PASSED [ 63%]
tests/test_R11_claims.py::test_R11_data_loglog_slopes_reproduce_by_an_independent_fit PASSED [ 63%]
tests/test_R11_claims.py::test_R11_pht_data_slope_is_fitted_on_a_restricted_domain PASSED [ 64%]
tests/test_R11_claims.py::test_R11_low_gamma_sensitivity_arm_excludes_exactly_the_unattainable_point PASSED [ 64%]
tests/test_R11_claims.py::test_R11_bootstrap_standard_errors_are_present_and_the_ratio_is_reported PASSED [ 65%]
tests/test_R11_claims.py::test_R11_no_macro_restates_the_cusum_scaling_law PASSED [ 65%]
tests/test_R11_claims.py::test_R11_submitted_linear_fits_are_reproduced_for_traceability PASSED [ 65%]
tests/test_R11_claims.py::test_R11_peak_to_peak_spread_is_descriptive_and_arithmetically_correct PASSED [ 66%]
tests/test_R11_claims.py::test_R11_preonset_leak_is_recorded_for_every_detector_even_at_zero PASSED [ 66%]
tests/test_R11_claims.py::test_R11_onset_table_carries_a_paired_error PASSED [ 67%]
tests/test_R11_claims.py::test_R11_the_two_adwin_implementations_are_labelled PASSED [ 67%]
tests/test_R11_claims.py::test_R11_river_version_is_recorded_in_the_artefacts PASSED [ 67%]
tests/test_R11_claims.py::test_R11_macros_are_emitted_with_the_preamble_ordinal PASSED [ 68%]
tests/test_R11_claims.py::test_R11_concept_add_macros_match_their_arm PASSED [ 68%]
tests/test_R11_claims.py::test_R11_eddm_macros_come_from_the_independent_seed_arm PASSED [ 69%]
tests/test_R11_claims.py::test_R11_report_against_v87 PASSED             [ 69%]
tests/test_R13_claims.py::test_R13_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 69%]
tests/test_R13_claims.py::test_R13_the_detector_labels_carry_the_families_the_manuscript_fixes PASSED [ 70%]
tests/test_R13_claims.py::test_R13_the_published_delay_and_false_alarm_probability_come_from_one_row PASSED [ 70%]
tests/test_R13_claims.py::test_R13_the_two_covid_detection_delays_v87_prints_reproduce PASSED [ 71%]
tests/test_R13_claims.py::test_R13_the_jensen_ratio_v87_prints_reproduces_and_is_specific_to_one_oracle PASSED [ 71%]
tests/test_R13_claims.py::test_R13_the_phase_false_alarm_probability_of_L331_does_not_reproduce_at_its_printed_precision PASSED [ 71%]
tests/test_R13_claims.py::test_R13_the_census_verdicts_of_L331_reproduce_at_the_matched_operating_point PASSED [ 72%]
tests/test_R13_claims.py::test_R13_the_2011_correction_alarms_at_dead_bands_the_caption_does_not_name PASSED [ 72%]
tests/test_R13_claims.py::test_R13_the_D2_increment_is_the_gaussian_log_likelihood_ratio PASSED [ 73%]
tests/test_R13_claims.py::test_R13_the_frozen_volatility_path_recomputes_from_the_persisted_parameters PASSED [ 73%]
tests/test_R13_claims.py::test_R13_the_four_operating_points_are_the_rules_they_name PASSED [ 73%]
tests/test_R13_claims.py::test_R13_no_arl0_is_persisted_without_its_censored_fraction PASSED [ 74%]
tests/test_R13_claims.py::test_R13_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 74%]
tests/test_R13_claims.py::test_R13_the_certification_gates_are_equivalence_statements_with_a_null_law PASSED [ 75%]
tests/test_R13_claims.py::test_R13_the_census_quantities_are_r16s_canonical_arm PASSED [ 75%]
tests/test_R13_claims.py::test_R13_the_oracle_verdict_and_the_clairvoyant_column_are_their_own_definitions PASSED [ 75%]
tests/test_R13_claims.py::test_R13_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 76%]
tests/test_R13_claims.py::test_R13_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 76%]
tests/test_R13_claims.py::test_R13_every_produced_text_file_ends_in_a_newline PASSED [ 77%]
tests/test_R13_claims.py::test_R13_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 77%]
tests/test_R13_claims.py::test_R13_the_produced_sources_carry_no_banned_construct PASSED [ 77%]
tests/test_R13_claims.py::test_R13_report_the_campaign_against_its_witness PASSED [ 78%]
tests/test_R13_claims.py::test_R13_report_the_threshold_neighbourhood_of_the_published_operating_point PASSED [ 78%]
tests/test_R13_claims.py::test_R13_report_the_certification_status_of_every_oracle PASSED [ 79%]
tests/test_R16_claims.py::test_R16_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 79%]
tests/test_R16_claims.py::test_R16_the_census_carries_the_phase_count_v87_prints PASSED [ 79%]
tests/test_R16_claims.py::test_R16_the_dating_algorithm_column_names_the_algorithm_of_every_row PASSED [ 80%]
tests/test_R16_claims.py::test_R16_the_out_of_budget_counts_reproduce_the_three_v87_prints PASSED [ 80%]
tests/test_R16_claims.py::test_R16_the_step_of_one_holds_on_the_count_and_fails_on_the_set PASSED [ 81%]
tests/test_R16_claims.py::test_R16_the_boundary_convention_flips_run_in_one_direction_only PASSED [ 81%]
tests/test_R16_claims.py::test_R16_the_unconditional_floor_is_the_sharpe_ceiling_of_the_corollary PASSED [ 81%]
tests/test_R16_claims.py::test_R16_the_sign_floor_is_the_bernoulli_divergence_of_the_manuscript PASSED [ 82%]
tests/test_R16_claims.py::test_R16_every_detectability_flag_is_its_own_floor_against_its_own_duration PASSED [ 82%]
tests/test_R16_claims.py::test_R16_the_census_statistics_recompute_from_the_raw_return_series PASSED [ 83%]
tests/test_R16_claims.py::test_R16_the_phases_partition_the_return_series_of_every_ticker PASSED [ 83%]
tests/test_R16_claims.py::test_R16_no_degenerate_phase_reaches_a_detectability_flag_without_measurement PASSED [ 83%]
tests/test_R16_claims.py::test_R16_the_turning_point_return_v87_cites_falls_where_the_convention_puts_it PASSED [ 84%]
tests/test_R16_claims.py::test_R16_the_long_secular_advance_v87_prints_reproduces PASSED [ 84%]
tests/test_R16_claims.py::test_R16_the_covid_phase_v87_prints_reproduces_to_its_printed_precision PASSED [ 85%]
tests/test_R16_claims.py::test_R16_the_two_numerical_evaluations_of_the_bound_reproduce_L260 PASSED [ 85%]
tests/test_R16_claims.py::test_R16_the_floor_fraction_envelope_of_L329_does_not_reproduce_at_its_lower_end PASSED [ 85%]
tests/test_R16_claims.py::test_R16_the_published_dating_description_is_unreachable_by_strict_pagan_sossounov PASSED [ 86%]
tests/test_R16_claims.py::test_R16_the_counterfactual_arms_are_the_rules_they_claim_to_be PASSED [ 86%]
tests/test_R16_claims.py::test_R16_the_macros_price_the_counterfactuals_they_name PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_headline_macros_agree_with_the_frames_they_are_computed_from PASSED [ 87%]
tests/test_R16_claims.py::test_R16_every_produced_text_file_ends_in_a_newline PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_produced_sources_carry_no_banned_construct PASSED [ 89%]
tests/test_R16_claims.py::test_R16_report_the_census_against_its_witness PASSED [ 89%]
tests/test_R16_claims.py::test_R16_report_the_three_dating_arms PASSED   [ 89%]
tests/test_R16_claims.py::test_R16_report_the_set_behind_the_step_of_one PASSED [ 90%]
tests/test_R18_claims.py::test_R18_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 90%]
tests/test_R18_claims.py::test_R18_the_grids_have_the_cardinality_their_specification_fixes PASSED [ 91%]
tests/test_R18_claims.py::test_R18_the_amplitude_grid_is_the_one_the_design_specifies PASSED [ 91%]
tests/test_R18_claims.py::test_R18_the_lag_one_autocorrelation_column_is_twice_the_amplitude PASSED [ 91%]
tests/test_R18_claims.py::test_R18_the_non_centrality_column_closes_its_own_geometric_sum PASSED [ 92%]
tests/test_R18_claims.py::test_R18_the_analytic_power_column_is_the_non_central_chi_square_tail PASSED [ 92%]
tests/test_R18_claims.py::test_R18_the_analytic_power_is_monotone_in_both_of_its_arguments PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_deviation_column_is_the_difference_it_names PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_wilson_intervals_agree_with_the_roots_of_the_score_equation PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_size_of_the_test_covers_the_nominal_level_at_every_horizon PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_null_p_values_are_calibrated_against_the_kolmogorov_limit PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_empirical_curve_matches_the_analytic_one_inside_the_local_domain PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_detectable_amplitude_solves_its_own_analytic_equation PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_detectable_amplitude_halves_when_the_horizon_quadruples PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_non_centrality_at_eighty_percent_power_is_a_constant_of_the_test PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_application_arms_carry_the_two_grids_they_borrow PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_realised_penalty_matches_its_target_where_the_target_is_attainable PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_measured_sign_streams_sit_below_the_detectable_amplitude PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_power_at_the_measured_autocorrelation_is_the_analytic_one PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_ljung_box_rejection_of_both_arms_covers_the_nominal_level PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_headline_macros_agree_with_the_frames_they_are_computed_from PASSED [ 99%]
tests/test_R18_claims.py::test_R18_the_reported_detectable_amplitude_is_the_one_the_analytic_law_gives PASSED [ 99%]
tests/test_R18_claims.py::test_R18_report_the_bound_the_repository_can_state PASSED [100%]

======================= 249 passed in 109.83s (0:01:49) ========================
```
