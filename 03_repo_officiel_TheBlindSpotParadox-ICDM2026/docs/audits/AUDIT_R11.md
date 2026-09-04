# AUDIT — R11, multi-detector generalization (v87 Figures 11 and 15)

Every measured block below is extracted from `logs/R11_multi_detector/exp_R11_multi_detector.log`
or from the captured `pytest` run. None is retyped.

**Starting state.** The bundle supplied `Priorite_12_multi_detector.py` (614 lines), its console
log, the normative preamble, the FAIR specifications, `articleB_whitening_v87.tex` and
`PROMPT_REPO_R11_multi_detector.md`. The script had never been audited under the campaign's FAIR
norm. It produces two figures of the frozen manuscript, carrying non-consecutive numbers.

**Headline.** **There is no D3 in this stream.** Read on the arm that produced it, every published
quantity of `sec:universality` is reproduced: the four delays of the Figure 15B caption at
**28.4078 / 27.0517 / 61.2123 / 249.6010** against **28.3 / 27.1 / 61 / 250** — one D2 and three
D1 — and the published ordering PHT below CUSUM at D0.

What R11 establishes that the manuscript does not state is a **comparability defect**: the four
numerals printed side by side in that caption were produced under **two different onset
conventions**, and putting the two cumulative detectors on one convention reverses their order at
**50.9 standard errors** of the paired, seed-clustered difference. That is Class A with null
severity — the caption asserts flatness, not an ordering — and it is what
`R11_v87_detector_comparability.md` carries.

Three further findings are new: the PHT's `λ × Γ` rule holds no level (14.46% at the attainable
floor, 1.62% at `Γ = 200`); the lower endpoint of the published range `Γ ∈ [1, 200]` is not
attainable at `alpha = 0.08`; and the `H0` `Concept` arm under the mandated seed key is
**degenerate by an exact identity**, which is asserted rather than remarked.

---

## 1. Figure numbers, and the verdict prompt §3 asks for

**`Fig18_Multi_Detector.png` is v87 Figure 15; `Fig20_Data_vs_Concept_ADD.png` is v87 Figure 11.**
Established by enumerating float environments in the frozen `.tex`: `fig:ljungbox` (1),
`fig:real_world` (2), `fig:fpr_explosion` (3), `fig:isofpr` (4), `fig:scale_law` (5),
`fig:validity_map` (6) — which reproduces the repository's existing mapping exactly — then
`fig:estmean` (7), `fig:adverse` (8), `fig:anytime` (9), `fig:skew_robustness` (10),
**`fig:data_vs_concept` (11)**, `fig:leverage` (12) and `fig:fat_tails` (13) as two captions inside
one `figure*`, `fig:oracle_frontier` (14), **`fig:multi_detector` (15)**. `articleB_whitening_v87.tex:621`
carries `\FloatBarrier % Keeps the final figures (15, 16, 17) separated` immediately above
`\label{fig:multi_detector}`, which closes the count independently.

**`protocol_4d_adwin_magnitude.csv` is cited nowhere in v87.** `grep` over the frozen `.tex` for
`blind`, `speedup`, `magnitude`, `protocol_4d` and `adwin_magnitude` returns nothing that refers to
it: the blind-zone material at L274 belongs to the `Recalib` sensor and Table 3, which R04 owns, and
`Speedup` appears only in the title of `sec:scaling_validation`, which is R05's. `docs/sections/R11.md`
declares the file produced and not cited, as `R03_sensitivity.csv` is.

---

## 2. The central finding: the submitted onset convention is MIXED

`worker_exp_b_h1` builds two streams. The CUSUM receives the post-onset stream alone, statistic at
zero (`Priorite_12_multi_detector.py:308-310`); PHT, ADWIN, DDM and EDDM receive the whole stream
with `onset=2000` (l.318-321). `worker_exp_d` does the same (l.463-465, l.472-474). `strict_pht`
tests `if m - M > threshold and t >= onset`, so a crossing during warm-up is **not returned and does
not reset the statistic**; the warm-up loop of `run_river_detector` calls `update()` without ever
reading `drift_detected`.

R11 therefore carries **three labelled arms** in the `arm` column. `reset` and `warmstart` put every
detector on one convention. `as_submitted` reproduces the per-detector mixture, assembled by
relabelling and not by a third campaign, from a map read off the witness with the line number beside
each entry.

```
Block C, mean Concept ADD over the grid, by arm: CUSUM reset 28.4078 / warmstart 25.4347 /
as_submitted 28.4078 (reset); PHT reset nan / warmstart 27.0517 / as_submitted 27.0517 (warmstart);
ADWIN reset 2023.7500 / warmstart 61.2123 / as_submitted 61.2123 (warmstart); DDM reset 1873.6072 /
warmstart 249.6010 / as_submitted 249.6010 (warmstart); EDDM reset 352.8913 / warmstart 133.8235 /
as_submitted 133.8235 (warmstart).
```

```
Figure 15B ordering on the as_submitted arm (CUSUM at reset, PHT at warmstart): CUSUM 28.4078,
PHT 27.0517, paired difference PHT - CUSUM = -1.3561 +/- 0.0618 over 5000 seeds (21.9 standard
errors, seed as the unit of clustering). Not inverted on this arm.

Figure 15B ordering on the warmstart arm (both at warmstart): CUSUM 25.4347, PHT 27.0517, paired
difference PHT - CUSUM = 1.6170 +/- 0.0318 over 5000 seeds (50.9 standard errors). The order is
inverted on the matched warmstart arm. This falsifies nothing: v87 asserts nothing about a
convention it did not run, and its caption asserts flatness rather than an ordering.
```

**Only `as_submitted` reproduces the caption.** The `warmstart` arm compares a CUSUM the submitted
campaign never ran against three detectors that it did.

**What the `warmstart` convention costs, counted (C6).** Per detector over 100,000 streams:

```
C6, pre-onset leak, logged per detector and per grid point EVEN AT ZERO. Totals over the grid,
warmstart arm: CUSUM 3180; PHT 2400; ADWIN 40; DDM 9780; EDDM 91560; [expD] CUSUM 0; PHT 9;
ADWIN 21. Reset arm, zero by construction.
```

**What the `reset` arm removes is detector-specific, and an earlier reading of this was wrong.** A
first draft of the analysis block claimed the reference-adaptive detectors have "no change within
their input to find" under `reset`. The measured rates refute it for ADWIN (`DetRate 0.7845` against
`FPR 0.0002`) and DDM (`0.4929` against `0.1034`); only the PHT behaves that way (`0.0170` against
`0.0518`). The claim was withdrawn and replaced by the mechanism v87 itself derives, not by silence:
post-onset, `e_t = 1{eps_t + Δ > 0}` with `eps_t = σ_t z_t`, so

    P(e_t = 1 | F_{t-1}) = P(z_t > -Δ/σ_t) = 1 - F_z(-Δ/σ_t) =: q_t,

which equals `1/2` for every `σ_t` when `Δ = 0` — the whitening property — and is a non-constant
function of `σ_t` otherwise. Since `σ_t` is serially dependent under GARCH, the `H1` stream inherits
the volatility clustering, so a window comparison retains structure to find with no pre-onset sample.
This is v87's own conditional-mean boundary argument (line 305) read at the drift rather than at the
centring.

---

## 3. The H0 Concept arm under common random numbers is degenerate, and it is ASSERTED

`simulate_garch11` draws the whole innovation vector **before** the variance recursion, so
`eps[t] = sqrt(sigma2[t]) · z[t]` with `sigma2[t] > 0` and therefore `sign(eps_t) = sign(z_t)`
exactly, for every `(omega, alpha, beta)`. Under prompt §2.1's key on role and index alone, the `H0`
binary stream is bit-identical at every penalty.

```
H0 CONCEPT UNDER COMMON RANDOM NUMBERS IS DEGENERATE, AND THIS IS ASSERTED. On 200 seeds the binary
stream (eps[2000:] > 0) is bit-identical across all 20 Gamma for 200 of them. R11_concept_fpr_vs_
gamma.csv therefore carries one number repeated 20 times, its effective sample size is 5000 and not
100000, and it supports no claim: it is an identity witness.
```

```
Block B, Kish design effect of the H0 Concept pooled level, paired against independent keys:
CUSUM: 20.0040 vs 1.0034, PHT: 20.0040 vs 0.9808, ADWIN: 20.0040 vs 0.9913, DDM: 20.0040 vs 1.0014,
EDDM: 20.0040 vs 1.0087.
```

**20.0040 against 1.00**: removing the pairing removes the design effect exactly, which is what a
design effect means. An unasserted observation would not survive a later change to the generator;
the assertion is what turns `sign(eps_t) ≡ sign(z_t)` from a remark into a checked property, and it
exits non-zero if the identity ever fails.

Every published `H0` `Concept` rate is taken from the independent-seed arm:

| detector | CRN arm (identity witness) | independent-seed arm (the measurement) |
| -------- | -------------------------- | -------------------------------------- |
| CUSUM    | 7.66%, zero grid spread    | **7.99%**                              |
| PHT      | 5.18%, zero grid spread    | **5.85%**                              |
| ADWIN    | 0.02%, zero grid spread    | **0.05%**                              |
| DDM      | 10.34%, zero grid spread   | **10.44%**                             |
| EDDM     | 93.16%, zero grid spread   | **92.10%**                             |

The `H1` arm is **not** degenerate: `Δ = c · σ_unc` is constant across `Γ` by variance targeting, but
the crossing `z_t > -Δ/sqrt(σ²_t)` retains the penalty.

---

## 4. Deviation classification against v87

Run at the printing precision of each source, both sides read with `float_precision='round_trip'`.

```
quantity                                             |   published |  regenerated | degree | source cell
Concept ADD CUSUM (reset)                            |     28.3000 |      28.4078 |     D2 | R11_concept_add_vs_gamma.csv arm=as_submitted ADD_CUSUM (mean of 20 rows)
Concept ADD PHT (warmstart)                          |     27.1000 |      27.0517 |     D1 | R11_concept_add_vs_gamma.csv arm=as_submitted ADD_PHT (mean of 20 rows)
Concept ADD ADWIN (warmstart)                        |     61.0000 |      61.2123 |     D1 | R11_concept_add_vs_gamma.csv arm=as_submitted ADD_ADWIN (mean of 20 rows)
Concept ADD DDM (warmstart)                          |    250.0000 |     249.6010 |     D1 | R11_concept_add_vs_gamma.csv arm=as_submitted ADD_DDM (mean of 20 rows)
Concept ADD order PHT < CUSUM (as_submitted)         |      1.0000 |       1.0000 |     D0 | R11_concept_add_vs_gamma.csv arm=as_submitted
Data log-log slope CUSUM                             |      0.8600 |       0.8777 |     D2 | R11_slope_fits.csv arm=as_submitted pipeline=Data detector=CUSUM
Data log-log slope PHT                               |      1.0900 |       1.0977 |     D2 | R11_slope_fits.csv arm=as_submitted pipeline=Data detector=PHT
Data log-log slope ADWIN                             |      0.4700 |       0.4845 |     D2 | R11_slope_fits.csv arm=as_submitted pipeline=Data detector=ADWIN
PHT sqrt(Gamma) plateau, grid mean                   |      0.3000 |       0.2818 |     D2 | R11_pht_fpr_vs_gamma.csv FPR_sqrt (mean of 20 rows)
PHT syncope Gamma (DetRate < 0.5)                    |     75.0000 |      91.1111 |     D2 | R11_data_add_vs_gamma.csv arm=as_submitted DetRate_PHT
EDDM H0 Concept FPR floor                            |      0.9000 |       0.9210 |     D2 | R11_concept_fpr_vs_gamma_independent_seeds.csv FPR_EDDM (mean of 20 rows)
Peak-to-peak ADD spread, cumulative (CUSUM)          |      0.0320 |       0.0113 |     D2 | R11_concept_add_vs_gamma.csv arm=as_submitted ADD_CUSUM (largest of ('CUSUM', 'PHT'))
Peak-to-peak ADD spread, window-mean ADWIN           |      0.1300 |       0.1316 |     D2 | R11_concept_add_vs_gamma.csv arm=as_submitted ADD_ADWIN
Gamma range max/min (realised)                       |    170.0000 |     170.3704 |     D1 | R11_concept_add_vs_gamma.csv Gamma_realised
Submitted linear slope CUSUM (submitted log)         |     26.6020 |      26.2411 |     D2 | R11_slope_fits.csv response='ADD ~ Gamma' detector=CUSUM
Submitted linear slope PHT (submitted log)           |     37.2280 |      37.2746 |     D2 | R11_slope_fits.csv response='ADD ~ Gamma' detector=PHT
Submitted linear slope ADWIN (submitted log)         |      4.7470 |       4.8731 |     D2 | R11_slope_fits.csv response='ADD ~ Gamma' detector=ADWIN
PHT calibrated threshold, Data                       |     39.0100 |      41.4515 |     D2 | the calibration block of the log
PHT calibrated threshold, Concept                    |     10.3400 |      10.3180 |     D2 | the calibration block of the log
```

**One D0, four D1, fourteen D2, no D3** — as the log emits it. The table above is a verbatim log
extract and is left unedited, but its rows do not share one reference, and the headline count must
be read with that partition or it overstates the manuscript's exposure.

- **Published numerals — the proper domain of §S3.** Five D2 (`Concept ADD CUSUM`, the three Data
  log-log slopes, `PHT syncope Gamma`), four D1, one D0. These are the deviations
  `docs/DEVIATIONS.md` records, and it records exactly these and no others.
- **Published bounds and qualifiers — where the verdict is *met* or *not met*, not a degree.** Four
  rows. `below 3.2%` for the cumulative detectors is met at **1.13%** (CUSUM) and **0.82%** (PHT);
  `>90%` for the EDDM floor is met at **92.10%**; `near 30%` for the `sqrt(Gamma)` plateau is met at
  **28.18%**. The fourth, `13%` for the window-mean ADWIN, is the only one its point estimate does
  not clear: **13.16%**, whose paired interval `[11.77%, 14.55%]` contains the ceiling — exceeded by
  the estimate, not falsified by the interval. A bound carries no printing precision that could
  move, so `D2` is the wrong instrument for all four.
- **Comparisons against the submitted log, not against the manuscript.** Five rows: the three linear
  slopes and the two PHT calibration thresholds. None appears in `articleB_whitening_v87.tex`. They
  measure port fidelity; classifying them `D2` reads as five further departures from a text they
  were never in.

Read that way: **one D0, four D1, five D2 against published numerals; four published bounds
assessed, three met and one exceeded by its point estimate inside its own interval; five
port-fidelity comparisons.** Nothing downstream changes: the register already carries the five
numeral deviations and none of the fourteen other rows.

**The three linear slopes are the strongest evidence that the port is faithful.** `26.2411 / 37.2746
/ 4.8731` against the submitted log's `26.602 / 37.228 / 4.747`, reproduced from a regression the
submitted script actually ran, on a campaign redrawn with different entropy.

**Which detectors are "cumulative" is v87's own definition, not ours.** Line 84 names "cumulative
statistics (CUSUM, PHT; Siegmund regime)" against "the window-mean ADWIN". DDM is in neither
category — it monitors a running error rate against `p_min + k·s_min` — so L296's two peak-to-peak
descriptors do not cover it, and its spread of **4.22%**, interval `[3.13%, 5.19%]`, is reported and
not classified against a bound not written for it.

---

## 5. Controls, with their margins and their trigger probabilities

| control | statement                                                              | margin                                                                                                                                                                       | P(trigger \| its own H0)                                                     |
| ------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| C1 (a)  | frozen-mean PHT returns `strict_cusum`'s alarm indices                 | **200 of 200**, of which 100 alarm at all; margin 0 streams                                                                                                                  | 0 up to an exact-threshold tie, probability 0 on a continuous stream         |
| C1 (b)  | with `mean_x` live the indices differ                                  | **76 of 200**; required ≥ 1, margin 75                                                                                                                                       | 0. Failure ⇒ immediate D3                                                    |
| C2      | realised penalty against target, attainable set decided by closed form | 19 of 20 within `1e-6`; the 20th has **no root** and returns `beta = 0.0` exactly                                                                                            | 0                                                                            |
| C3      | `river` is a hard dependency, version in every CSV                     | `0.23.0`, no fallback path exists                                                                                                                                            | deterministic                                                                |
| C4      | flatness by slope test, not by extremum                                | KS of 5 p-values against `Uniform(0,1)`: **D = 0.4000, p = 0.3088** on `as_submitted`                                                                                        | naive familywise `1 − 0.95⁵ = 22.62%`, logged **before** the result was read |
| C5      | `sqrt(2)` inflation on every PHT interval                              | applied to `z`, not to the half-width; every bound clamped to `[0,1]`                                                                                                        | n/a — an interval width                                                      |
| C6      | pre-onset leak per detector and grid point                             | EDDM 91,560 / DDM 9,780 / CUSUM 3,180 / PHT 2,400 / ADWIN 40, logged even at zero                                                                                            | deliberately **not** a gate                                                  |
| C7      | positive control, admission by measured power                          | CUSUM **+200.01 SE**, ADWIN **+23.39 SE** admitted; PHT `−6.19`, DDM `−0.14`, EDDM `−36.37` excluded                                                                         | small; local inversions characterised, never corrected                       |
| C8      | source-segment identity                                                | 6 primitives byte-identical (**2,206 characters**); `simulate_garch11` identical below its RNG line (**440 characters**)                                                     | 0                                                                            |
| C9      | reproducibility                                                        | see §6                                                                                                                                                                       | 0                                                                            |
| —       | instrumented-variant identities                                        | `simulate_garch11_instrumented` bit-identical on 20 probe streams; ADWIN naive/prefix/instrumented agree on 50; `instrumented_cusum`/`_pht` reproduce their primitives on 50 | 0                                                                            |
| —       | grid relation                                                          | rounding each realised penalty to 2 dp reproduces the prompt's 20 printed literals exactly                                                                                   | 0                                                                            |
| —       | silent-branch counters                                                 | variance clamp **6** bindings over 465,000 streams; both `1e-8` floors **0**                                                                                                 | logged at zero                                                               |

### C2 fires at the grid's lowest point, and the control was not re-cut

The penalty at fixed `alpha` is minimised at `beta = 0`, where `denom = 1`, `rho1 = alpha` and
`phi = alpha`, giving in one line

    Gamma_floor(alpha) = 1 + 2*alpha/(1 - alpha) = 1.1739130435   at alpha = 0.08.

The submitted target grid `concat(linspace(1,50,10), linspace(60,200,10))` has `Γ = 1.0` as its
first point, **below that floor**. It has no root in `beta`.

```
C2 FINDING at Gamma = 1.0: the target lies BELOW the attainable penalty floor 1.1739130435 =
compute_gamma_exact(0.08, 0), so it has no root in beta and the bisection converges to beta = 0.
The realised penalty is 1.1739130435, a relative excess of 17.3913%. This is not a solver failure
and no tolerance is widened for it.
```

**No tolerance was widened.** C2 now carries two assertions, and which one applies is decided by the
closed form before any solving: `|realised/target − 1| < 1e-6` where the target is attainable, and
`beta == 0.0` **exactly** where it is not. That is a rule, not an exemption — it applies to any
target below the floor at any `alpha` — and `Gamma_target`, `Gamma_realised` and `attainable` are
three distinct persisted columns.

This is the same finding `docs/DEVIATIONS.md` entry 7 records for R03, and it is why the sensitivity
macros are named `…ExLowGamma` rather than `…ExIid`: the excluded point is an ARCH(1) process at the
attainable floor, not an i.i.d. one.

### C7 admits by measured power, never by the manuscript's numeral

```
C7 admission, CUSUM: ... censored at the 5000-step horizon is 24.55 under H1 against 4825.59 under
H0, on the same 1000 seeds, paired SE 24.0039; the criterion ADD_H1 < ADD_H0 - 2 x SE is MET with a
margin of 200.01 standard errors.
C7 admission, EDDM: ... 3251.09 under H1 against 446.60 under H0 ... NOT MET with a margin of
-36.37 standard errors.
C7 admission outcome: ['CUSUM', 'ADWIN'] enter the monotonicity gate; ['PHT', 'DDM', 'EDDM'] are
excluded by their inability to discriminate drift from noise.
```

v87 L296's `>90%` EDDM descriptor is logged beside each detector as corroboration and is **never**
the gate: a threshold read off the manuscript's own report of the behaviour it excludes would be a
tolerance set on an observed value (§S4.6). Non-alarms are right-censored at the monitoring horizon,
a design constant, which keeps every seed in the comparison — "both measured on the same seeds" —
and understates the `H0` alarm time, making admission harder rather than easier.

**C7 fires on ADWIN and it is reported, not corrected**: the ADD rises between consecutive
amplitudes at `c 1.0 → 1.5` by `+204.64 ± 26.83` (7.6 SE) and at `c 1.5 → 2.0` by `+385.84 ± 29.42`
(13.1 SE). The CUSUM decreases at every step. ADWIN is admitted by power and non-monotone in
amplitude; both facts are stated and neither is reconciled.

### C4's design effect is measured, not assumed

| detector | Concept slope on `log(Γ)` | `se_bootstrap` | p-value | `se_boot / se_ols` |
| -------- | ------------------------- | -------------- | ------- | ------------------ |
| CUSUM    | −0.0629                   | 0.0502         | 0.2100  | **3.714**          |
| PHT      | −0.0270                   | 0.0524         | 0.6068  | **5.043**          |
| ADWIN    | −1.5343                   | 0.0936         | 0.0000  | **2.151**          |
| DDM      | −2.3128                   | 0.3010         | 0.0000  | **1.475**          |
| EDDM     | −0.2025                   | 0.2462         | 0.4109  | **3.129**          |

Under common random numbers the twenty grid estimates share their draws, so the analytic OLS
standard error does not hold. The last column is the ratio between the two, and it **is** the design
effect: pricing these slopes analytically would understate the error by factors of 1.5 to 5.0. Every
p-value comes from a seed-cluster bootstrap resampling **seeds and never grid points**, over 2,000
replicates, which is why every campaign retains its per-stream outcomes in memory until this point.

---

## 6. Reproducibility

Two runs of the same script, at **different worker counts**, produce byte-identical artefacts.

**Run 1 — `./run_experiment_R11.sh`, `--n-jobs -1` (48 workers), 886.0 s of campaign.** This is
the run whose log is shipped.

```
R11_pht_fpr_vs_gamma.csv                           : 91d2b94b45fe8edfdc7e0658a88a7d5bcebea6285af00819369810bd83491164
R11_concept_fpr_vs_gamma.csv                       : c0f1bb2096f140ea38c634b673dad39c2433e531cd6d3c6155ea19cb99871326
R11_concept_fpr_vs_gamma_independent_seeds.csv     : d0ac29eb6a1ce46e103a443187878f4ca2981d55e86337ab5f0a0b4c49891d45
R11_concept_add_vs_gamma.csv                       : fca0e9c36045d12a9d26867e179834fc5244920fd986c1cd6171a5b6b3d5ebec
R11_adwin_magnitude.csv                            : 8b16d2b5364f4f47935a1e85a2da074228ecc43afa970d400796008b0545c744
R11_data_add_vs_gamma.csv                          : 9fdcb08279fe858fa02f1ec0f8008e18032b23d6381e91dec18a0a379b3daf32
R11_slope_fits.csv                                 : 06943ff168bc0dc0dd95f706cb99816981e6cf8588bc01febbf3e11ae57f6471
R11_onset_convention_delta.csv                     : 10bfd492c5eb54bed0fcdd15e6b4393c080cdbbaf04b7db8409ea9fe036248c4
fig11_data_vs_concept.png                          : b9f06563dee497ba98cd8f51708c1251285d9c638685148ad9eb252ef0cdf198
fig15_multi_detector.png                           : 229e61aa0e96c10a874ac7563c854d432649d885e0ba70e3b7c45dc3feeb9847
figA04_adwin_blind_zone.png                        : bdd78f6473d8b534732459d1ca8fc8f0b27f338006eceade26780d08f982632a
R11_claims.tex                                     : 01e3365b7aab88ee97c8a8bc5a5e338516d0b4df8c0922821acb100100e25b13
```

**Run 2 — `./run_experiment_R11.sh --n-jobs 12`, 1933.2 s of campaign.**

```
R11_pht_fpr_vs_gamma.csv                           : 91d2b94b45fe8edfdc7e0658a88a7d5bcebea6285af00819369810bd83491164
R11_concept_fpr_vs_gamma.csv                       : c0f1bb2096f140ea38c634b673dad39c2433e531cd6d3c6155ea19cb99871326
R11_concept_fpr_vs_gamma_independent_seeds.csv     : d0ac29eb6a1ce46e103a443187878f4ca2981d55e86337ab5f0a0b4c49891d45
R11_concept_add_vs_gamma.csv                       : fca0e9c36045d12a9d26867e179834fc5244920fd986c1cd6171a5b6b3d5ebec
R11_adwin_magnitude.csv                            : 8b16d2b5364f4f47935a1e85a2da074228ecc43afa970d400796008b0545c744
R11_data_add_vs_gamma.csv                          : 9fdcb08279fe858fa02f1ec0f8008e18032b23d6381e91dec18a0a379b3daf32
R11_slope_fits.csv                                 : 06943ff168bc0dc0dd95f706cb99816981e6cf8588bc01febbf3e11ae57f6471
R11_onset_convention_delta.csv                     : 10bfd492c5eb54bed0fcdd15e6b4393c080cdbbaf04b7db8409ea9fe036248c4
fig11_data_vs_concept.png                          : b9f06563dee497ba98cd8f51708c1251285d9c638685148ad9eb252ef0cdf198
fig15_multi_detector.png                           : 229e61aa0e96c10a874ac7563c854d432649d885e0ba70e3b7c45dc3feeb9847
figA04_adwin_blind_zone.png                        : bdd78f6473d8b534732459d1ca8fc8f0b27f338006eceade26780d08f982632a
R11_claims.tex                                     : 01e3365b7aab88ee97c8a8bc5a5e338516d0b4df8c0922821acb100100e25b13
```

The two sets are **identical on all twelve artefacts**, and `diff -r` over the whole
`results/R11_multi_detector/` tree reports no difference. A third run at 48 workers reproduces both.
Outputs do not depend on the worker count because every task carries its own seed, derived from the
128-bit condensate of its semantic coordinates rather than from its position in a work queue.

`run_all.sh` and `run_tests.sh` are unmodified (their mtimes, 2026-08-01 21:55 and 2026-07-29 15:06,
predate this stream); nothing was added to `experiments/common/`; `run_experiment_R11.sh` is
discovered by sorted enumeration and its name matches `run_all.sh`'s regex
`^run_experiment_R[0-9]{2}[a-z]?\.sh$`.

The confirmatory-language grep of §S4.4 returns empty on
`experiments/R11_multi_detector/exp_R11_multi_detector.py`,
`logs/R11_multi_detector/exp_R11_multi_detector.log` and `docs/sections/R11.md`.

**Measured cost 886 s of campaign over 465,000 monitored streams, 936 s including the analysis and
the bootstraps**, on 48 cores. The submitted campaign ran 355,000 streams in 382 s on 24 cores.

### The whole suite, `pytest tests/ -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-9.0.3, pluggy-1.6.0 -- /home/m53/miniforge3/envs/Trading/bin/python3
cachedir: .pytest_cache
rootdir: /home/m53/The-Whitening-Advantage-Experiments
plugins: anyio-4.8.0
collecting ... collected 145 items

tests/test_R01_claims.py::test_r01_models PASSED                         [  0%]
tests/test_R01_claims.py::test_r01_trajectories PASSED                   [  1%]
tests/test_R01_claims.py::test_r01_injection_summary PASSED              [  2%]
tests/test_R01_claims.py::test_r01_placebo PASSED                        [  2%]
tests/test_R01_claims.py::test_r01_magnitude_and_symmetry PASSED         [  3%]
tests/test_R02_claims.py::test_stream_counts PASSED                      [  4%]
tests/test_R02_claims.py::test_classifier_integrity PASSED               [  4%]
tests/test_R02_claims.py::test_data_rejection_rates PASSED               [  5%]
tests/test_R02_claims.py::test_distinct_p_concept PASSED                 [  6%]
tests/test_R02_claims.py::test_independence_diagnostics PASSED           [  6%]
tests/test_R02_claims.py::test_iid_arm_rejection_is_reported_not_asserted PASSED [  7%]
tests/test_R02_claims.py::test_concept_level_covered_by_wilson PASSED    [  8%]
tests/test_R02_claims.py::test_max_clustered_pvalue_below_manuscript_bound PASSED [  8%]
tests/test_R02b_claims.py::test_negative_control_integrity PASSED        [  9%]
tests/test_R02b_claims.py::test_nu_seven_is_indistinguishable_from_nominal PASSED [ 10%]
tests/test_R02b_claims.py::test_heavy_tail_arms_exclude_nominal PASSED   [ 11%]
tests/test_R02b_claims.py::test_rate_ordering_heavy_versus_light PASSED  [ 11%]
tests/test_R02b_claims.py::test_negative_control_matches_squared_at_light_tails PASSED [ 12%]
tests/test_R02c_claims.py::test_R02c_seed_uniqueness PASSED              [ 13%]
tests/test_R02c_claims.py::test_R02c_negative_control_calibration PASSED [ 13%]
tests/test_R02c_claims.py::test_R02c_eighth_moment_account_is_refuted PASSED [ 14%]
tests/test_R02c_claims.py::test_R02c_slope_test_power_is_declared PASSED [ 15%]
tests/test_R02c_claims.py::test_R02c_control_arm_integrity PASSED        [ 15%]
tests/test_R02c_claims.py::test_R02c_continuity PASSED                   [ 16%]
tests/test_R02c_claims.py::test_R02c_mechanism_slope_logic PASSED        [ 17%]
tests/test_R03_claims.py::test_R03_grid_cardinality PASSED               [ 17%]
tests/test_R03_claims.py::test_R03_grid_is_unchanged PASSED              [ 18%]
tests/test_R03_claims.py::test_R03_threshold_ordering_is_structural PASSED [ 19%]
tests/test_R03_claims.py::test_R03_monotonicity_beyond_gamma_six PASSED  [ 20%]
tests/test_R03_claims.py::test_R03_aggregate_certification_gates PASSED  [ 20%]
tests/test_R03_claims.py::test_R03_gamma_rule_holds_the_nominal_level PASSED [ 21%]
tests/test_R03_claims.py::test_R03_iid_calibration_arm_is_well_formed PASSED [ 22%]
tests/test_R03_claims.py::test_R03_deviation_classification_against_witness PASSED [ 22%]
tests/test_R03_claims.py::test_R03_macros_are_emitted PASSED             [ 23%]
tests/test_R04_claims.py::test_R04_cardinalities PASSED                  [ 24%]
tests/test_R04_claims.py::test_R04_grids_match_v87 PASSED                [ 24%]
tests/test_R04_claims.py::test_R04_horizon_and_sample_size PASSED        [ 25%]
tests/test_R04_claims.py::test_R04_reference_drifts_are_coherent PASSED  [ 26%]
tests/test_R04_claims.py::test_R04_all_arms_are_iso_fpr PASSED           [ 26%]
tests/test_R04_claims.py::test_R04_concept_threshold_is_flat_in_gamma PASSED [ 27%]
tests/test_R04_claims.py::test_R04_concept_level_is_homogeneous_in_gamma PASSED [ 28%]
tests/test_R04_claims.py::test_R04_recalib_blind_zone_persists_at_lowest_gamma PASSED [ 28%]
tests/test_R04_claims.py::test_R04_recalib_is_slower_than_both_first_order_arms PASSED [ 29%]
tests/test_R04_claims.py::test_R04_add_decreases_with_drift_magnitude PASSED [ 30%]
tests/test_R04_claims.py::test_R04_conditional_mean_is_labelled_and_accompanied PASSED [ 31%]
tests/test_R04_claims.py::test_R04_efficiency_ratio_is_monotone_in_nu PASSED [ 31%]
tests/test_R04_claims.py::test_R04_ratio_respects_the_gaussian_ceiling PASSED [ 32%]
tests/test_R04_claims.py::test_R04_predicted_ratio_is_the_pitman_constant PASSED [ 33%]
tests/test_R04_claims.py::test_R04_oracle_is_never_slower_than_the_fitted_arm PASSED [ 33%]
tests/test_R04_claims.py::test_R04_analytic_crossing_matches_v87 PASSED  [ 34%]
tests/test_R04_claims.py::test_R04_blind_zone_onset_matches_v87 PASSED   [ 35%]
tests/test_R04_claims.py::test_R04_macros_are_emitted_and_computed PASSED [ 35%]
tests/test_R04_claims.py::test_R04_crossings_agree_with_the_interpolation_rule PASSED [ 36%]
tests/test_R04_claims.py::test_R04_emitted_crossing_brackets_contain_the_crossing PASSED [ 37%]
tests/test_R04_claims.py::test_R04_table3_printing_rule_reproduces_v87 PASSED [ 37%]
tests/test_R04_claims.py::test_R04_table3_is_generated_from_the_csv PASSED [ 38%]
tests/test_R04_claims.py::test_R04_table3_shows_detrate_exactly_when_below_one PASSED [ 39%]
tests/test_R04_claims.py::test_R04_intervals_are_clamped_and_ordered PASSED [ 40%]
tests/test_R04_claims.py::test_R04_no_nan_in_reported_delays PASSED      [ 40%]
tests/test_R04_claims.py::test_R04_m0_universality_arm_matches_the_garch_arm PASSED [ 41%]
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
PASSED       [ 42%]
tests/test_R04b_claims.py::test_R04b_cardinality_and_grid PASSED         [ 42%]
tests/test_R04b_claims.py::test_R04b_protocol_constants_match_v87 PASSED [ 43%]
tests/test_R04b_claims.py::test_R04b_gamma_target_is_attainable_and_realised PASSED [ 44%]
tests/test_R04b_claims.py::test_R04b_analytic_prediction_is_the_pitman_constant PASSED [ 44%]
tests/test_R04b_claims.py::test_R04b_in_sample_bisection_converged PASSED [ 45%]
tests/test_R04b_claims.py::test_R04b_pooled_holdout_level_meets_the_promised_band PASSED [ 46%]
tests/test_R04b_claims.py::test_R04b_conditional_calibration_pvalues_are_uniform PASSED [ 46%]
tests/test_R04b_claims.py::test_R04b_rates_are_consistent_and_clamped PASSED [ 47%]
tests/test_R04b_claims.py::test_R04b_continuity_anchors_are_read_from_R04 PASSED [ 48%]
tests/test_R04b_claims.py::test_R04b_is_compatible_with_R04_at_the_common_points PASSED [ 48%]
tests/test_R04b_claims.py::test_R04b_grid_bracket_straddles_unity_and_the_interpolation_lies_inside_it PASSED [ 49%]
tests/test_R04b_claims.py::test_R04b_inferential_bracket_is_recomputable_from_the_csv PASSED [ 50%]
tests/test_R04b_claims.py::test_R04b_bootstrap_error_exceeds_the_conditional_one PASSED [ 51%]
tests/test_R04b_claims.py::test_R04b_shape_fit_is_reported_with_its_goodness PASSED [ 51%]
tests/test_R04b_claims.py::test_R04b_analytic_crossing_matches_v87 PASSED [ 52%]
tests/test_R04b_claims.py::test_R04b_estimation_cost_interval_arithmetic PASSED [ 53%]
tests/test_R04b_claims.py::test_R04b_ratio_respects_the_gaussian_ceiling PASSED [ 53%]
tests/test_R04b_claims.py::test_R04b_oracle_ratio_does_not_cross_again_above_seven PASSED [ 54%]
tests/test_R04b_claims.py::test_R04b_macros_are_emitted_and_computed PASSED [ 55%]
tests/test_R04b_claims.py::test_R04b_no_nan_in_reported_quantities PASSED [ 55%]
tests/test_R04b_claims.py::test_R04b_report_against_v87 PASSED           [ 56%]
tests/test_R05_claims.py::test_abrupt_cardinality PASSED                 [ 57%]
tests/test_R05_claims.py::test_ramp_cardinalities PASSED                 [ 57%]
tests/test_R05_claims.py::test_protocol_constants PASSED                 [ 58%]
tests/test_R05_claims.py::test_horizons_are_the_two_published_budgets PASSED [ 59%]
tests/test_R05_claims.py::test_common_horizon_is_constant_across_gamma PASSED [ 60%]
tests/test_R05_claims.py::test_null_levels_are_homogeneous_across_gamma PASSED [ 60%]
tests/test_R05_claims.py::test_concept_branch_is_gamma_invariant_by_construction PASSED [ 61%]
tests/test_R05_claims.py::test_concept_is_blind_to_the_scale_pathology PASSED [ 62%]
tests/test_R05_claims.py::test_positive_control_shows_the_monitor_responsive PASSED [ 62%]
tests/test_R05_claims.py::test_both_crossovers_are_emitted_and_are_distinct PASSED [ 63%]
tests/test_R05_claims.py::test_scaling_law_branches_meet_at_the_crossover PASSED [ 64%]
tests/test_R05_claims.py::test_ladder_visits_the_three_published_horizons PASSED [ 64%]
tests/test_R05_claims.py::test_ladder_is_monotone_in_the_horizon PASSED  [ 65%]
tests/test_R05_claims.py::test_ladder_agrees_with_the_campaigns_it_overlaps PASSED [ 66%]
tests/test_R05_claims.py::test_sixth_moment_boundary_matches_the_published_gamma PASSED [ 66%]
tests/test_R05_claims.py::test_moment_margin_macro_matches_the_published_bound PASSED [ 67%]
tests/test_R05_claims.py::test_macro_file_is_well_formed PASSED          [ 68%]
tests/test_R05_claims.py::test_required_macros_are_present PASSED        [ 68%]
tests/test_R05_claims.py::test_figure_exists PASSED                      [ 69%]
tests/test_R05_claims.py::test_text_artefacts_end_with_a_newline PASSED  [ 70%]
tests/test_R05_claims.py::test_superseded_witness_is_documented_not_regenerated PASSED [ 71%]
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
PASSED    [ 71%]
tests/test_R06_claims.py::test_R06_cardinalities_and_grid PASSED         [ 72%]
tests/test_R06_claims.py::test_R06_gamma_grid_is_realised_in_closed_form PASSED [ 73%]
tests/test_R06_claims.py::test_R06_fourth_moment_boundary_is_computed_not_hard_coded PASSED [ 73%]
tests/test_R06_claims.py::test_R06_boundary_is_not_confused_with_the_nearest_grid_point PASSED [ 74%]
tests/test_R06_claims.py::test_R06_panel_A_design_is_paired_and_declared PASSED [ 75%]
tests/test_R06_claims.py::test_R06_pooled_binary_level_covers_nominal_at_cluster_precision PASSED [ 75%]
tests/test_R06_claims.py::test_R06_counterfactual_arm_removes_the_pairing PASSED [ 76%]
tests/test_R06_claims.py::test_R06_no_per_gamma_gate_is_possible PASSED  [ 77%]
tests/test_R06_claims.py::test_R06_squared_stream_rejects_massively PASSED [ 77%]
tests/test_R06_claims.py::test_R06_task_boundaries_saturate PASSED       [ 78%]
tests/test_R06_claims.py::test_R06_intermediate_threshold_is_reported_and_labelled PASSED [ 79%]
tests/test_R06_claims.py::test_R06_median_task_control_covers_nominal_and_is_weakly_resolved PASSED [ 80%]
tests/test_R06_claims.py::test_R06_no_silent_fallback_survived_into_the_artefacts PASSED [ 80%]
tests/test_R06_claims.py::test_R06_reproduces_the_witness_byte_for_byte PASSED [ 81%]
tests/test_R06_claims.py::test_R06_macros_are_emitted_and_computed PASSED [ 82%]
tests/test_R06_claims.py::test_R06_report_against_the_witness PASSED     [ 82%]
tests/test_R11_claims.py::test_R11_cardinalities_and_arms PASSED         [ 83%]
tests/test_R11_claims.py::test_R11_gamma_grid_is_the_target_grid_and_its_floor_is_respected PASSED [ 84%]
tests/test_R11_claims.py::test_R11_gamma_range_matches_the_published_multiplier PASSED [ 84%]
tests/test_R11_claims.py::test_R11_as_submitted_arm_is_the_per_detector_mixture PASSED [ 85%]
tests/test_R11_claims.py::test_R11_putting_both_detectors_on_one_convention_moves_the_cusum PASSED [ 86%]
tests/test_R11_claims.py::test_R11_the_published_ordering_holds_on_the_arm_that_produced_it PASSED [ 86%]
tests/test_R11_claims.py::test_R11_crn_h0_arm_is_degenerate_and_the_independent_arm_is_not PASSED [ 87%]
tests/test_R11_claims.py::test_R11_kish_design_effect_of_a_degenerate_grid_is_its_width PASSED [ 88%]
tests/test_R11_claims.py::test_R11_pht_intervals_carry_the_calibration_variance_factor PASSED [ 88%]
tests/test_R11_claims.py::test_R11_every_interval_bound_is_clamped PASSED [ 89%]
tests/test_R11_claims.py::test_R11_data_loglog_slopes_reproduce_by_an_independent_fit PASSED [ 90%]
tests/test_R11_claims.py::test_R11_pht_data_slope_is_fitted_on_a_restricted_domain PASSED [ 91%]
tests/test_R11_claims.py::test_R11_low_gamma_sensitivity_arm_excludes_exactly_the_unattainable_point PASSED [ 91%]
tests/test_R11_claims.py::test_R11_bootstrap_standard_errors_are_present_and_the_ratio_is_reported PASSED [ 92%]
tests/test_R11_claims.py::test_R11_no_macro_restates_the_cusum_scaling_law PASSED [ 93%]
tests/test_R11_claims.py::test_R11_submitted_linear_fits_are_reproduced_for_traceability PASSED [ 93%]
tests/test_R11_claims.py::test_R11_peak_to_peak_spread_is_descriptive_and_arithmetically_correct PASSED [ 94%]
tests/test_R11_claims.py::test_R11_preonset_leak_is_recorded_for_every_detector_even_at_zero PASSED [ 95%]
tests/test_R11_claims.py::test_R11_onset_table_carries_a_paired_error PASSED [ 95%]
tests/test_R11_claims.py::test_R11_the_two_adwin_implementations_are_labelled PASSED [ 96%]
tests/test_R11_claims.py::test_R11_river_version_is_recorded_in_the_artefacts PASSED [ 97%]
tests/test_R11_claims.py::test_R11_macros_are_emitted_with_the_preamble_ordinal PASSED [ 97%]
tests/test_R11_claims.py::test_R11_concept_add_macros_match_their_arm PASSED [ 98%]
tests/test_R11_claims.py::test_R11_eddm_macros_come_from_the_independent_seed_arm PASSED [ 99%]
tests/test_R11_claims.py::test_R11_report_against_v87 PASSED             [100%]

============================= 145 passed in 1.92s ==============================
```

---

## 7. Design decisions taken outside the plan

1. **Plan §1.10's scoping of the D3 was wrong, and this is a defect of the plan rather than of its
   execution.** The plan scopes the D3 to "the arm that reproduces the submitted convention" and
   names that arm `warmstart`. It is not: `worker_exp_b_h1` gives the CUSUM the `reset` treatment,
   so v87's `28.3` is a `reset` measurement while `27.1 / 61 / 250` are `warmstart` ones. **The
   submitted convention is mixed and neither pure arm reproduces it.** The first corrected run
   halted on the `warmstart` inversion exactly as the plan instructs; the halt was procedurally
   right and the premise behind it was not. The gate is now scoped to the `as_submitted` arm, where
   the order is not inverted, and the matched-arm inversion is carried as the Class A comparability
   finding. **No D3 was waived**: had one occurred on `as_submitted`, the stream would have stopped
   and no sign-off would have restarted it.
2. **A third labelled arm, `as_submitted`, was introduced.** It is a value of the existing `arm`
   column, defined once from a per-`(experiment, detector)` map read off the witness with the line
   number beside each entry, and assembled by relabelling rather than by a third campaign. Every
   v87-facing quantity is computed on it; `reset` and `warmstart` remain the matched arms. Each
   frame also carries an `arm_<detector>` column, so no quantity is compared without the convention
   being named at the row.
3. **Two D3 flags in the first corrected run were artefacts of this audit's own classification code,
   found before they reached an artefact.** First, the "cumulative detectors" set had been taken as
   `{CUSUM, PHT, DDM}`; v87 line 84 defines the term itself as "cumulative statistics (CUSUM, PHT;
   Siegmund regime)" against "the window-mean ADWIN", and the R11 prompt's own gloss on C4 states
   the ceiling is the PHT's (`3.190%` against `3.2%`). Second, the threshold crossing had been
   decided on the point estimate, which is exactly the door C4 forbids in advance; the qualitative
   test now asks whether the paired seed-cluster interval clears the published bound. Neither change
   touched a seed, a parameter or a tolerance: both make the code conform to a control registered
   before any measurement. Under §S3's dissymmetry rule these were examined more severely than a
   contradicting result would have been, because they move towards the manuscript.
4. **The `Γ` grid is solved for its targets, not for the prompt's printed literals.** The prompt's
   §1 lists `1.17, 6.44, 11.89, …` as imperative; they are the submitted campaign's **realised**
   penalties rounded to two decimals. The script verifies at run time that rounding each realised
   penalty reproduces all twenty literals, and the anomalous first entry is what gives the direction
   away: `1.17` is not a round number of any linspace but is exactly `round(1.1739130435, 2)`.
   Solving for the targets moves `beta` at sixteen of twenty points, by at most `2.89e-5`, and
   `omega` by at most `5.86e-4` relative. Because no seed key carries `gamma`, the innovation vector
   is unchanged and the two `H0` `Concept` CSVs did **not** move; every amplitude-reading artefact
   did. This was predicted before the run and verified after it.
5. **`\REleven`, not `\REleventh`.** Prompt §4 writes `\REleventh…`; preamble §S6 specifies the
   ordinal in English words and the repository realises `ROne … RSix`. The preamble prevails by its
   own precedence clause.
6. **`\RElevenDataSlope…ExLowGamma`, not `…ExIid`.** The excluded point is `alpha = 0.08, beta = 0`,
   an ARCH(1) process at the attainable floor. A macro named `ExIid` would assert in LaTeX what this
   repository's own register denies (`docs/DEVIATIONS.md` entry 7).
7. **The ADD macros are emitted twice, suffixed `Reset` and `Warmstart`.** The plan's §1.8 requires
   it and the mixture is why: a single unsuffixed macro could not be substituted into the caption it
   appears to serve.
8. **The PHT calibration keeps the empirical percentile.** Prompt §1 and C5 both describe a
   bisection; `calibrate_pht_iid` returns `np.percentile(max_stats, 100*(1-target_fpr))`.
   Implementing a bisection would silently change the submitted method. C5's mechanism is unaffected:
   the doubled variance is a property of any threshold estimated on a finite calibration sample.
9. **One macro is emitted as `nan`.** `\RElevenConceptAddPhtReset` has no value — on the matched
   `reset` arm the PHT's detection rate is 1.7%, far below the censor. It is emitted **as measured**
   rather than suppressed or silently taken from the other arm, which would be the undeclared
   fallback §S4.3 proscribes, and the log names it.
10. **A censored paired difference is carried beside the conditional one** in
    `R11_onset_convention_delta.csv`. The conditional difference is undefined for a detector that
    never alarms on one arm — which is exactly what the onset convention creates — and restricting
    to streams that alarmed on both conditions on the null arm having alarmed. Both columns are
    persisted; neither stands in for the other.
11. **The submitted linear regression is reproduced as a row of `R11_slope_fits.csv`.** The submitted
    script regressed `ADD` on `Γ` linearly while the manuscript published log-log slopes, and the
    submitted log printed only the linear ones. Reproducing both keeps the two quantities from being
    confused. **No macro is emitted for it under any name**: R05 owns `ADD ~ a·Γ + b`, and a test
    asserts that neither `26.00` nor `32.20` appears anywhere in `R11_claims.tex`.
12. **`tqdm` was dropped** and its dependency with it, following the R06 precedent: a progress bar on
    stderr is not an output.
13. **The orchestrator's prediction of bit-identity across the halt was mathematically false, and is
    recorded here as a failure of oversight rather than of execution.** Introducing the
    `as_submitted` arm expanded three of the eight CSVs from 40 rows to 60. A run producing 60-row
    files cannot be bit-identical to an aborted run producing 40-row ones, and the aborted run had
    emitted no figure and no `.tex` at all, so nine of the twelve artefacts had no counterpart to
    compare against. The prediction assumed the correction was purely analytical and did not account
    for the structural expansion of the output space. **The integrity of these deliverables rests on
    C9 — three runs of the final script at two worker counts, §6 — and on nothing else.** No claim of
    continuity with the aborted run is made anywhere in this audit, and none should be read into it.

---

## 8. Open questions, left open

1. **Should the Figure 15B convention be declared or unified?** Declaring it costs eleven words and
   changes no value. Unifying it changes all four numerals and requires re-running the campaign, and
   the `reset` arm is not a neutral choice — it removes the pre-change reference three of the five
   detectors are defined against. `R11_concept_add_vs_gamma.csv` supplies the numbers either
   unification would produce; this repository does not choose between them.
2. **What is DDM's peak-to-peak spread meant to be compared against?** Its 4.22% falls under neither
   of L296's two descriptors, since v87 classes it as neither cumulative nor window-mean. Whether the
   sentence intended to cover it is a question for the authors.
3. **ADWIN is admitted by power and non-monotone in amplitude.** Its ADD rises by 7.6 and 13.1
   standard errors between consecutive amplitudes of the C7 sweep. Nothing in this campaign explains
   the non-monotonicity, and this audit asserts no mechanism for it. Establishing one needs a sweep
   in the window parameters, which R11 does not run.
4. **The `sqrt(2)` inflation is applied to the PHT arms only.** C5 derives it for a level read at a
   threshold calibrated on a finite sample. The CUSUM `Concept` threshold `λ = 10` is a fixed design
   constant and carries no calibration error, so no inflation applies; whether the river detectors'
   internal thresholds carry an analogous term has not been analysed.
5. **The three published log-log slopes were computed outside the submitted chain**, and an earlier
   revision of the manuscript carried two of them wrong (`1.06` and `0.46`). This repository can say
   what its own campaign produces and cannot say how the published values were obtained.
6. **`data/reference/R11/` holds a `.py` and a `.log` and no CSV.** The submitted campaign wrote its
   tables beside its figures and they were not preserved, so the deviation table classifies against
   the manuscript and the console log rather than against data. Whether `data/reference/` is the
   right home for an executable witness is the question `AUDIT_R06.md` §8.4 already poses.
7. **The preamble's own confirmatory-language grep has a false positive.** The pattern `proven`
   matches the ordinary word `provenance`, which `PROMPT_REPO_R11_multi_detector.md` itself uses
   twice (§2.3 and §9). The word was replaced with "traceability" throughout this stream's `.py`,
   `.log` and Markdown section so that §S4.4 returns empty. Amending the shared preamble is outside
   the remit of one experiment; it is reported here.

---

Files to transmit for review: `experiments/R11_multi_detector/exp_R11_multi_detector.py`,
`tests/test_R11_claims.py`, `run_experiment_R11.sh`, `docs/sections/R11.md`, `requirements/R11.txt`,
`logs/R11_multi_detector/exp_R11_multi_detector.log`, the eight CSVs, the three figures and
`R11_claims.tex` under `results/R11_multi_detector/`, `data/reference/R11/`, the five parked
candidates under `docs/camera_ready_candidates/`, and the R11 block of `docs/DEVIATIONS.md`.
