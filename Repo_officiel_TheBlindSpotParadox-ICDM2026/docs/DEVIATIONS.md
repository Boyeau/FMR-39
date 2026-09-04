# Deviations between this repository and the submitted manuscript

The manuscript was submitted on 2026-07-27 and is frozen. This repository was built
afterwards and, in the course of hardening the experimental code, corrected defects that
were present in the code used to produce the submitted results. Where a correction changed
a published quantity, the change is recorded here. **This file is the index; each entry
links to the experiment section that documents it in full.**

Nothing in this repository is adjusted to match the manuscript. Where the two disagree, both
values are printed and the reason is stated.

## Classification

- **Class A — correction of a defect in the submitted code.** The submitted code did
  something other than what the manuscript describes. The repository cannot ship the defect,
  so the deviation is unavoidable.
- **Class B — environment hardening.** The submitted code was correct; the environment was
  not reproducible. The submitted values remain exactly recoverable, and the command that
  recovers them is given.
- **Class C — presentation.** Figure formatting only; no numerical content changes.

## Severity

- **D0** — same conclusion, same printed value; only sub-display-precision digits move.
- **D1** — value moves below the manuscript's printing precision.
- **D2** — a printed value changes; the qualitative claim it supports still holds.
- **D3** — a qualitative claim of the manuscript is not reproduced.

## Register

| id                                  | Experiment | Manuscript location                        | Class | Severity | One-line summary                                                                                                                                                                                                                                                          |
| ----------------------------------- | ---------- | ------------------------------------------ | ----- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `R01-variance-target`               | R01        | Table 2 caption, Figure 2                  | A?    | D0       | `omega`, `sigma_unc` move by at most 2.7e-14 relative; no published number changes; **cause unidentified**                                                                                                                                                                |
| `R02-binary-error-rate`             | R02        | Section "Empirical Boundaries"             | A     | D2       | pooled binary-error rejection 4.4% → 4.2%; Wilson [2.8, 7.1]% → [2.5, 6.8]%                                                                                                                                                                                               |
| `R02b-iid-arm-rejection`            | R02 / R02b | Section "Empirical Boundaries"             | A     | **D3**   | the i.i.d.-arm over-rejection claim is not reproduced at `t_7`                                                                                                                                                                                                            |
| `R02-figure-1-redraw`               | R02        | Figure 1                                   | A     | D2       | the figure is regenerated from the corrected campaign, so its underlying data differ                                                                                                                                                                                      |
| `ALL-figure-presentation`           | all        | all figures                                | C     | —        | bold panel titles, uppercase `(A)`/`(B)` labels, some panels merged into single images                                                                                                                                                                                    |
| `R02c-mechanism-constraints`        | R02c       | Section "Empirical Boundaries"             | A     | —        | no manuscript claim affected; constrains the admissible explanation in camera-ready                                                                                                                                                                                       |
| `R03-cusum-nominal-level`           | R03        | Section "FPR explosion"                    | A     | D2       | the StrictCUSUM i.i.d. level is 2.0%, not the 5% the text ascribes to it                                                                                                                                                                                                  |
| `R03-campaign-redraw`               | R03        | Section "FPR explosion", Fig. 3            | A     | D2       | 128-bit seeding redraws the campaign; every printed rate moves, no claim moves                                                                                                                                                                                            |
| `R05-concept-threshold-numeral`     | R05        | Section "Scaling Validation"               | A     | D2       | the Concept threshold numeral `lambda_C = 10` matches no campaign of the study                                                                                                                                                                                            |
| `R05-campaign-redraw`               | R05        | Section "Scaling Validation", Appendix B   | A     | D2       | 128-bit seeding redraws both scaling campaigns; every Monte-Carlo value moves                                                                                                                                                                                             |
| `R05-recalibration-residual`        | R05        | Appendix B                                 | A     | D2       | "residual on the conservative side" is `-1.4%` at one of five penalties                                                                                                                                                                                                   |
| `R05-sixth-moment-attribution`      | R05        | Appendix B                                 | A     | —        | the sixth-moment attribution is unsupported by R05; its two numerals are exact                                                                                                                                                                                            |
| `R04-gamma-grid-defect`             | R04        | Section "Sensor Mismatch"                  | A     | **D3**   | the submitted `Gamma` grid never varied due to a transposed parameter argument                                                                                                                                                                                            |
| `R04b-efficiency-crossing`          | R04 / R04b | Section "Discussion", abstract             | A     | **D3**   | the efficiency crossing `nu* ~ 4.9` is falsified; R04b encloses it in `[7, 9]` and prices the cost at `3.6`                                                                                                                                                               |
| `R05-regime-column-contradiction`   | R05        | Appendix B                                 | A     | —        | `regime` column contradicts the appendix; sixth-moment gloss is wrong (`E[eps^6]` is 3rd moment of `eps^2`)                                                                                                                                                               |
| `R04b-calibration-variance`         | R04b       | —                                          | —     | —        | methodological: a threshold calibrated on a finite sample gives held-out counts twice the binomial variance                                                                                                                                                               |
| `R06-fourth-moment-boundary`        | R06        | Figure 6 and its caption                   | A / C | D1       | the fourth-moment boundary is now computed (`41.58`, printed `41.6`); the figure conflated it with `Γ = 41`                                                                                                                                                               |
| `R04b-oracle-ratio-offset`          | R04b       | Section "Discussion"                       | A     | D3       | the oracle curve exceeds its analytic prediction everywhere (+5%); the crossing does not track the prediction                                                                                                                                                             |
| `R11-onset-convention`              | R11        | Figure 15B caption, `sec:universality`     | A     | —        | the four caption delays were measured under two different onset conventions and are not comparable                                                                                                                                                                        |
| `R11-cusum-add`                     | R11        | Figure 15B caption                         | A     | D2       | `Concept` CUSUM delay `28.3` → **`28.4078`**                                                                                                                                                                                                                              |
| `R11-pht-slope`                     | R11        | `sec:universality`, L298                   | A     | D2       | log-log PHT slope `1.09` → **`1.0977`** on 12 of 20 points, delays conditional on detection                                                                                                                                                                               |
| `R11-pht-syncope`                   | R11        | `sec:universality`, L298                   | A     | D2       | "beyond `Γ ≈ 75`" → first point below 50% detection at **`Γ = 91.11`**                                                                                                                                                                                                    |
| `R11-pht-gamma-rule`                | R11        | `sec:fpr_explosion`, L171; Fig. 15 caption | A     | D2       | the PHT's `λ × Γ` rule holds no level: **14.46%** at the floor, **1.62%** at `Γ = 200`                                                                                                                                                                                    |
| `R11-figure11-caption`              | R11        | Figure 11 caption                          | A     | D2       | the caption applies panel A's `c=2 / n=1000` to a figure whose panel B is `c=1.5 / n=5000`                                                                                                                                                                                |
| `R11-gamma-grid-floor`              | R11        | `sec:universality`, L296                   | A     | —        | the lower endpoint of "`Γ ∈ [1, 200]`" is not attainable at `alpha = 0.08`; the grid starts at `1.1739`                                                                                                                                                                   |
| `R11-regenerated`                   | R11        | Figures 11 and 15                          | A     | D2       | 128-bit re-keying redraws the whole campaign; every Monte-Carlo value moves, no claim moves                                                                                                                                                                               |
| `R18-ljungbox-power`                | R18        | L278, L290, Fig. 6 caption L286, L318      | A     | —        | four Ljung--Box non-rejections are stated unqualified; the test resolves `rho_1 = 0.051` at `n = 8000`                                                                                                                                                                    |
| `R16-dating-misdescription`         | R16        | `sec:real_world`, L329                     | A     | **D3**   | a Pagan--Sossounov dating of the four streams yields **48** phases, not the `66` L329 attributes to it                                                                                                                                                                    |
| `R16-covid-phase-conditional`       | R16        | `sec:real_world`, L331                     | A     | —        | L331's four numerals reproduce exactly; the phase exists only under the SPY substitution                                                                                                                                                                                  |
| `R16-floor-frac-envelope`           | R16        | `sec:real_world`, L329                     | A     | D2       | `55--92\%` → **`50--92\%`**; cause **not identified**                                                                                                                                                                                                                     |
| `R16-boundary-sensitivity`          | R16        | `app:repro`, L392                          | A     | —        | 3 of 66 phases flip with the convention, all one way; the count is `[53, 56]`, never reported                                                                                                                                                                             |
| `R16-sign-arm-disagreement`         | R16        | `sec:real_world`, L329                     | A     | —        | "moves that count by one phase" is a net of 10 and 9; the arms disagree on 19 of 66                                                                                                                                                                                       |
| `R16-substitution-scope`            | R16        | `sec:real_world`, L329                     | A     | —        | the published fraction is conditional on the substitution reaching one ticker of four: 80.3% → 73.5%                                                                                                                                                                      |
| `R13-campaign-redraw`               | R13        | `sec:real_world`, L331                     | A     | D2       | 128-bit re-keying redraws the oracle campaign; the phase false-alarm probability moves `1.3%` → **`1.1%`**                                                                                                                                                                |
| `R13-operating-points-unnamed`      | R13        | `sec:real_world`, L331                     | A     | —        | one sentence reports two different operating points and names neither; `3 d / 1.3% / 16 d` are not locatable                                                                                                                                                              |
| `R13-frozen-null-scope`             | R13        | `sec:real_world`, L331                     | A     | —        | the frozen path binds on one detector arm and the threshold-selecting `ARL0` null is not frozen at all                                                                                                                                                                    |
| `R13-negative-control-scope`        | R13        | `sec:real_world`, L331                     | A     | —        | "no alarm on the 2011 correction" holds at the two dead bands the caption names; four others alarm at 69 days                                                                                                                                                             |
| `R07-bias-bound-not-a-bound`        | R07        | `sec:ar_garch`, L308                       | A     | D2       | the printed AR-bias bound `2.9e-3` is contradicted by the approximation `-2.5 phi/n` evaluated at the same cell                                                                                                                                                           |
| `R07-campaign-redraw`               | R07        | `sec:ar_garch` L308, Fig. 7                | A     | D2       | 128-bit re-keying redraws the campaign; `5.1%`→`4.9%`, `20.8%`→`21.0%`, `4.6`→`4.7%`, `11.4`→`11.5%`                                                                                                                                                                      |
| `R07-oracle-band-precision`         | R07        | Figure 7 caption                           | A     | —        | common random numbers make the `ORACLE` arm `phi`-invariant: the reference band carries `n_eff` = 10 000                                                                                                                                                                  |
| `R07-lambda-star-estimator`         | R07        | `sec:exactness`, L241                      | A     | —        | the delivered `lambda*` came from a sample quantile astride the lattice boundary, reproducible `73.8%` of runs                                                                                                                                                            |
| `R07-panelB-operating-level`        | R07        | Figure 7 caption                           | A     | —        | panel B operates at `5.16%`, the upper attainable level; the caption's parenthetical says `4.29%`                                                                                                                                                                         |
| `R07-dispersion-cost-numeral`       | R07        | `sec:ar_garch`, L308                       | A     | —        | "costs at most `0.4` points of rejection" matches no reading, in the witness campaign or the regenerated one                                                                                                                                                              |
| `R09-campaign-redraw`               | R09        | `sec:exactness` L243, Fig. 9               | A     | D2       | 128-bit re-keying redraws the campaign; `18%`→`19.9%`, `539`→`533`, `409`→`410`; no claim moves                                                                                                                                                                           |
| `R09-arl0-censoring`                | R09        | Figure 9 caption **(C)**                   | A     | —        | CUSUM and MIX `ARL0` are horizon artefacts at 65–99% right-censoring; the caption names only e-CUSUM                                                                                                                                                                      |
| `R09-add-conditioning`              | R09        | L243, Figure 9 caption **(B)**             | A     | —        | panel B's delay is conditional on detection at rates from `5.7%` to `97.6%`; the matched-rate reading holds                                                                                                                                                               |
| `R10-campaign-redraw`               | R10        | L290, Figure 10 caption                    | A     | D2       | 128-bit re-keying redraws the campaign; `-1.44`→`-1.43` (pure redraw, `+1.95` SE) and the caption's `1.8%`→`1.5%` (maximum over 4 cells, shift of `0.8` SE, within `[1.2%, 2.4%]` envelope); no claim moves                                                               |
| `R14-campaign-redraw`               | R14        | L345                                       | A     | D2       | 128-bit re-keying redraws the `t₃₀` synthetic control; `0.98`–`1.14`, mean `1.06` → **`0.95`–`1.24`, mean `1.04`**; every real-BTC value is bit-identical and every qualitative claim holds                                                                               |
| `R12-campaign-redraw`               | R12        | L349, L353, Figures 12 and 13              | A     | D2       | 128-bit re-keying redraws both campaigns; ten printed numerals move, including `7.6%`→`7.4%`, `8.4%`→`8.5%`, `83%`→`82%` and the censored delay floor `2,400`→`2,600`; no claim moves                                                                                     |
| `R12-concept-crn-degeneracy`        | R12        | Figure 12 caption, L349                    | A     | —        | under a key carrying no grid coordinate the Experiment A sign stream is **bit-identical at all 15 `γ_lev`**; the published arm is a second one whose key breaks the pairing                                                                                               |
| `R15-scatter-sign`                  | R15        | Figure 17 caption **(B)**                  | A     | D2       | the printed relation `r ≥ 0.99` holds under **neither** sign convention; the measured coefficient is `-0.9962` (witness `-0.9894`) and is negative at all five `c` by construction                                                                                        |
| `R15-campaign-redraw`               | R15        | Figure 17 caption **(A)**                  | A     | D2       | 128-bit re-keying redraws both calibrations; the bootstrap envelope `4.8`–`6.4%` → **`4.0`–`5.9%`**; the level is still held and no qualitative claim moves                                                                                                               |
| `R15-grid-provenance`               | R15        | Figure 17, `K` grid                        | A     | —        | two witness scripts are vendored and declare **different** `K` grids at the same line; the published ten-point grid is recovered from `…_UPDATED.py` and its log, not read off the figure                                                                                 |
| `R15-mkl-cbwr-rho`                  | R15        | L376, Figure 17 caption                    | **B** | D0       | `MKL_CBWR=COMPATIBLE` moves `rho_sign_meas` by ≤ `3.2e-15` on 7 of 9 `K`; **cause identified**, submitted values exactly recovered by `--witness-blas`                                                                                                                    |
| `R15-panel-vendor-drift`            | R15        | L389, public fetcher                       | B     | D0       | the network fetcher drifts by at most `2.16e-06` against the frozen versioned file, which remains the nominal input                                                                                                                                                       |
| `R08-delivered-level-above-nominal` | R08        | L241, its footnote, and Fig. 7 caption     | A     | **D3**   | **Scope bound: the exact null law is correct; the D3 is on the threshold selected.** L241's rule promises "at or below nominal" and its footnote implements the weak test, delivering `5.1021%` at `λ* = 11.4` rather than ≤5% (cross-propagates to R07 Figure 7 caption) |
| `R08-campaign-redraw`               | R08        | `sec:ar_garch` L311, Fig. 8 caption        | A     | D2       | 128-bit re-keying redraws both modules; `0.86%`→**`0.95%`**, and the two bracketing levels `5.03%`→`5.08%`, `4.29%`→`4.32%`; no qualitative claim moves                                                                                                                   |
| `R17-eco-l1-arm-identity`           | R17        | `sec:misspecification`, L341; Tab. 1 L117  | A     | **D3**   | L341 attributes its `9.5%` to `Eco-L1`, the **level** residual Table 1 defines; the producing cell is `protocol_3d`'s **squared** arm, which the delivered script itself names `Eco_L2`                                                                                   |
| `R17-campaign-redraw`               | R17        | `sec:misspecification`, L341               | A     | D2       | 128-bit re-keying redraws the warm-up campaign; `0.62`→**`0.63`**, `9.5%`→**`10.5%`**, `3.0%`→**`7.0%`**, `3`–`8%`→**`10`–`11%`**; every qualitative claim of L341 holds                                                                                                  |
| `R17-sign-arm-crn-degeneracy`       | R17        | `sec:misspecification`, L341               | A     | —        | under a key carrying no grid coordinate the `protocol_3d` sign stream is **bit-identical at both `γ_lev`**; the eight cells behind the `3`–`8%` envelope hold **four** readings                                                                                           |

*Entries are added as each experiment is certified. Streams R06 onwards are not yet complete;
this register is not final.*

---

### 1 — R01, variance target (class undetermined, D0)

`omega` and `sigma_unc` move by at most 2.7e-14 in relative terms against the submitted
campaign. `alpha`, `beta`, `gamma_hat`, `q_hat`, `n_days` and every Ljung-Box p-value are
bit-identical, and **every macro in `R01_claims.tex` is unchanged**: no published number moves.

**The cause is not identified, and one candidate has been tested and rejected.** A
`--legacy-blas` mode was added to test whether the drift came from BLAS thread pinning. It
lifts the pins and `MKL_CBWR`, and it reproduces the compliant output bit for bit without
recovering the submitted values. The hypothesis is refuted. It was weak on inspection as well:
the variance target is a one-dimensional NumPy reduction, which does not dispatch to BLAS.

Until the cause is established, this entry is not classified: it may be an environment
difference (class B, in which case the submitted values remain recoverable by some command we
have not found) or a code difference introduced during hardening (class A, in which case they
are not). The drift is bounded and affects no published quantity either way.

### 2 and 3 — R02 and R02b, whitening verification (Class A)

Two defects in the submitted code:

1. The script fell back to a majority-class stub whenever `river` was absent, and `river` was
   absent from the pinned requirements. The manuscript specifies an online Hoeffding Tree.
   Both learners produce an error rate near 0.5 on a sign stream, so no output revealed which
   one had run.
2. The 128-bit seed digest was truncated to its leading 32 bits.

Correcting both draws a different, equally valid set of 360 trajectories. Consequences:

**Pooled binary-error rate (D2).** 4.4% → 4.2%, Wilson [2.8, 7.1]% → [2.5, 6.8]%. The nominal
5% level remains inside the interval, so the claim that the binary error stream holds its
nominal level is unaffected. The per-regime range printed in the manuscript, 3.3-5.0%, is
reproduced exactly.

**i.i.d.-arm over-rejection (D3).** The manuscript reports that the squared inputs "already
over-reject on the i.i.d. arm (9.2%), where `t_7` innovations deprive `eps^2` of a fourth
moment and the chi-square approximation fails". Three findings, of decreasing importance:

- **The mechanism as stated is incorrect, independently of any sample.** For an i.i.d. series
  the Ljung-Box asymptotics require a finite variance of the tested series; with `Y = eps^2`
  that is `E[eps^4] < inf`, hence `nu > 4`, which holds at `t_7`. The moment that is missing
  below `nu = 8` is `E[eps^8]`, the fourth moment of `eps^2`, which governs the tail quantile
  rather than the validity of the limit.
- **The phenomenon is real, at heavier tails than stated.** A dedicated sweep (R02b, 1000
  streams per point) measures 8.8% at `nu = 5` (Wilson [7.2, 10.7]%) and 7.9% at `nu = 6`
  ([6.4, 9.7]%), both excluding the nominal level, against 5.8% at `nu = 7` ([4.5, 7.4]%). A
  negative control applying the same test to `eps_t` itself holds the nominal level at all six
  grid points, so the distortion is specific to the squaring step.
- **The published number is not itself an error.** Under a true rate of 5.8%, observing 11 or
  more rejections out of 120 has probability 8.9%. The submitted campaign reported an ordinary
  draw; what does not follow from 11/120 is the inference of a systematic effect.

The mechanism behind the measured transition is not identified. A convergence-rate explanation
predicts the transition point but fails its own counterfactual: the rejection rate at `nu = 5`
is flat across horizons from 2,000 to 128,000 steps. This repository asserts no mechanism.

See `docs/sections/R02.md` and `docs/sections/R02b.md`.

### 4 — R02, Figure 1 (Class A, D2)

Figure 1 in this repository is generated by the corrected script and therefore rests on the
corrected campaign. Re-plotting the submitted CSV files instead would produce a figure that
the shipped code does not generate, which is a worse failure of correspondence than a
documented difference. The visual conclusion — squared inputs rejecting throughout the
clustered regimes, binary errors at nominal — is unchanged.

### 5 — All experiments, figure presentation (Class C)

Every figure carries bold, left-aligned panel titles prefixed `(A)`, `(B)`, `(C)`, matching
the panel letters already used in the manuscript captions. Figures rendered in the manuscript
as multiple LaTeX subfigures are emitted here as single multi-panel images. No numerical
content is affected. Two manuscript captions ("Left:"/"Right:") do not carry panel letters and
are therefore desynchronised from the repository figures; this is noted in the relevant
experiment sections.

### 6 — R02c, mechanism explanation constraints (Class A, —)

R02c neither adds nor removes a manuscript claim: it constrains the causal explanation that a
camera-ready revision may offer for the over-rejection. Specifically, it rules out attributing
the effect to a convergence-rate delay, leaving the alternative hypothesis (asymptotic quantile
breakdown) untested. As this establishes an interpretative boundary without altering a numerical
finding of the paper, the severity is null. See `docs/sections/R02c.md`.

### 7 — R03, StrictCUSUM nominal level (Class A, D2)

The manuscript describes the StrictCUSUM as "calibrated to a 5% nominal level under i.i.d.
noise". The submitted campaign contains nothing that could support or refute this: its lowest
grid point sits at `Gamma = 1.174` with `alpha = 0.08` and `beta = 0`, which is an ARCH(1)
stream, not an i.i.d. one.

R03 adds an arm at `Gamma = 1` exactly (`alpha = beta = 0`), 300 streams of 5000 steps, with
the same innovations, the same standardisation chain, the same detectors and the same
thresholds as the grid. The script asserts `compute_gamma_exact(0, 0) == 1.0` before running
it.

| Detector    | FPR at `Gamma = 1` | Wilson 95%  | contains 5% |
| ----------- | ------------------ | ----------- | ----------- |
| StrictCUSUM | 2.0% (6/300)       | [0.9, 4.3]% | **no**      |
| ADWIN       | 5.0% (15/300)      | [3.1, 8.1]% | yes         |

The descriptor is accurate for the window-mean detector and inaccurate for the CUSUM. This is
not a defect of the detector: `lambda_iid = 65` is a conservative threshold, a legitimate
design choice, and a conservative i.i.d. level makes the explosion the section documents start
from a lower base. What is inexact is calling that threshold calibrated to 5%. **No figure,
table or theorem depends on the descriptor.** See `docs/sections/R03.md` and the parked
candidate `docs/camera_ready_candidates/v87_cusum_nominal_level.md`.

### 8 — R03, regenerated campaign (Class A, D2)

Two defects in the submitted seeding, both required to be corrected by the specifications:

1. The 256-bit digest of `make_seed` was truncated to its leading 32 bits, the same truncation
   already recorded for R02 at entry 3. The 300 stream seeds of protocols 1A and 1B are in fact
   collision-free at that width, so no collision occurred; the correction is required by the
   128-bit entropy rule, not by an observed failure.
2. Protocol 2C keyed its `H_0` seed stream on `int(lambda_c * 1000 + delta_c * 100000)`, which
   maps the 15 grid cells onto **12 distinct keys**: `(5.0, 0.02)` collides with `(2.0, 0.05)`,
   `(10.0, 0.02)` with `(2.0, 0.1)`, and `(10.0, 0.05)` with `(5.0, 0.1)`. Three pairs of cells
   therefore shared a realisation where the code intended independent entropy. This affects
   `R03_sensitivity.csv` only, which no version of v87 cites.

Correcting both draws a different, equally valid campaign, so every rate printed in
`sec:fpr_explosion` moves at the manuscript's printing precision. The classification of all
eleven published quantities is in `docs/sections/R03.md`; every one is D2 and every qualitative
claim of the section holds: the uncorrected rates explode with `Gamma`, `lambda x Gamma` holds
the nominal level (4.0% maximum), `lambda x sqrt(Gamma)` leaves a residual plateau (29.8%
mean), and the ADWIN correction contains the rate below 13% (9.6% mean).

One consequence deserves separate mention because it bears on how the section is certified.
The regenerated minimum of `FPR_raw` over `Gamma > 20` is 74.3%, below the 76.0% of the
submitted campaign. A certification gate placed on that minimum would abort the run while no
claim of the manuscript is contradicted. R03 therefore certifies on aggregates over the grid
region rather than on extrema; the reasoning is in the "Control design" section of
`docs/sections/R03.md`.

### 9 — R05, the `lambda_C` numeral (Class A, D2)

`sec:scaling_validation` states the Concept CUSUM was "fixed once and for all, `lambda_C = 10`,
`delta_C = 0.1`". Read in `float_precision='round_trip'`, the numeral matches no campaign of
the submitted study: the threshold was calibrated per horizon, at **10.8** for the abrupt
campaign (`H = 5,000`), **15.81** at `H = 2x10^5` and **19.02** at `H = 3x10^6`. R05
regenerates 11.40, 16.00 and 18.80.

What the sentence gets right, and what carries Proposition `prop:orthogonality`, is that the
threshold is fixed **with respect to `Gamma`**: constant within each campaign while the Data
threshold runs from 52.4 to 943.3 on the same rows. Only the numeral is wrong, and the
correction moves it onto a value the manuscript derives elsewhere — `lambda_star = 11.4`, from
the attainable-level analysis in "What ``exact'' means here". The submitted 10.8 realised a
9.5% level against a 5% target; the corrected campaign realises 5.5%.

`delta_C = 0.1` is correct and untouched. No figure, table or theorem depends on the numeral.
See `docs/sections/R05.md` and the parked candidate
`docs/camera_ready_candidates/v87_lambda_c_numeral.md`.

### 10 — R05, regenerated scaling campaigns (Class A, D2)

The submitted scripts derived seeds by integer offset, which the specifications require to be
replaced by a 128-bit digest. R05 keys the digest on the role and replicate index only — never
on `Gamma`, `beta`, `w` or the budget — repairing the entropy defect while preserving the
common-random-numbers design that makes a difference between two penalties an algorithmic
response rather than a difference of draw.

Both campaigns are therefore redrawn and every Monte-Carlo value moves. The movement is
mechanical: `lambda_star_Data`, a 95th percentile of 400 heavy-tailed CUSUM maxima, moves
`-7.9%` to `+19.4%` per cell, and `ADD_Data` moves `-12.2%` to `+14.4%` in lockstep, as
`ADD ~ lambda*/d + kappa` requires at fixed drift. The abrupt slope rises from 23.7 to 26.00
for that reason and no other; `R^2` is 0.9913, so the linearity it describes is unaffected.

Twenty-seven published quantities are classified in `docs/sections/R05.md`: seven D1 and
twenty D2. Every qualitative claim of the section holds — the delay is linear in the penalty,
Eq. (5) predicts the ramp delays with no fitted constant, the recalibration margin grows with
the penalty and with the horizon, and the Concept monitor is blind to the scale pathology.

### 11 — R05, the sign of the recalibration residual (Class A, D2)

`app:scaling` reports the `lambda_iid x Gamma` rule "holding to within 7-29% over a tenfold
range of `Gamma`, with the residual on the conservative side". In the regenerated 2e5 campaign
the margins are `+2.7%`, `-1.4%`, `+5.0%`, `+17.2%`, `+39.3%`. Four of the five keep the sign
the manuscript asserts; at `Gamma = 4` the residual is **`-1.4%`**, the opposite sign, which on
a strict reading of a one-sided statement is a D3.

It is recorded as D2, with the reasoning stated rather than buried: 
**this is an explicit boundary arbitration**. The estimator's own redraw noise is an order of 
magnitude larger than the violation — the same quantity moved `-7.9%` to `+19.4%` per cell 
under nothing but reseeding — so a residual of `-1.4%` is not distinguishable from zero at 
`N = 400`, and the sign at `Gamma = 4` is undetermined rather than shown negative. No parameter, 
tolerance, seed or bound was altered to reach this reading; the 400-seed design is the 
manuscript's own. Resolving the sign needs a larger `N`, not a rewording, which is why no 
camera-ready candidate is parked. See `docs/sections/R05.md`.

### 12 — R05, the sixth-moment attribution (Class A, —)

`app:scaling` attributes the degradation of the recalibration rule to "the loss of
`E[eps^6]`", placing the boundary at `Gamma ~ 7.1` with a moment margin `delta <= 0.8` at
`Gamma = 20`. **Both numerals are exact**: R05 recomputes them in closed form —
`E[eps^6] < infinity` iff `E[(alpha z^2 + beta)^3] < 1` — obtaining 7.0793 and 0.7931, with 
no Monte Carlo involved.

The **attribution** is a different matter. Every R05 campaign runs `t_7`; there is no `nu`
sweep, so no output of this experiment separates "the rule degrades because a moment is lost"
from "the rule degrades with `Gamma` and with the horizon, and a moment boundary happens to 
lie in the same range". The two budgets also place the measured transition differently, 
while the analytic boundary does not move. This repository reports the association and asserts 
no mechanism; establishing one needs an arm varying `nu` at fixed `Gamma`.

Separately, the parenthetical describing `E[eps^6]` as "the second moment of the monitored
statistic `eps^2`" is wrong independently of any measurement: `E[eps^6]` is the third moment 
of `eps^2`, and the second is `E[eps^4]`, whose boundary the same closed form puts at
`Gamma = 41.6`. No numerical finding is affected. As this constrains an interpretation 
without altering a value, the severity is null. A camera-ready candidate is parked in 
`docs/camera_ready_candidates/v87_sixth_moment_gloss.md`.

### 13 — R04, the transposed `Gamma` generator defect (Class A, D3)

In the submitted campaign, the `Gamma` grid never actually varied. `Priorite_15_isofpr_dichotomy.py` 
called `solve_beta_for_gamma(gamma, alpha)` against a definition of `(alpha, target_gamma)`, 
triggering an early return of `beta = 0` at every grid point. The four labels `{1, 11.58, 50, 200}` 
all silently ran the identical ARCH(1) process at `Gamma = 1.1053`.
Four qualitative claims of the manuscript (Recalib delay ratio, the efficiency crossing `nu*`, 
the oracle crossing, and the flat family control) are falsified when the grid genuinely spans. 
The discrepancy originates entirely from this defect. 

**Scope closure:** The project contains two homonymous functions with transposed argument 
orders. An exhaustive grep of all 23 call sites across the project confirms this collision 
is exclusively isolated to the R04 script. No other stream is affected.

### 14 — R04, the `nu*` efficiency crossing value (Class A, D3)

The manuscript states the efficiency ratio `ADD_Concept / ADD_Eco-L1` crosses unity at a 
measured `nu* ~ 4.9`, that an oracle arm crosses at `4.6`, and that the difference of `0.3` 
degrees of freedom is what a finite warm-up costs the parametric route. On a grid that 
genuinely  spans `Gamma`, the crossing moves up. R04's grid `{3, 4, 4.5, 5, 7, 30}` could 
not say by how much: the crossing fell strictly inside `(7, 30)`, an interval with no 
measurement points in it.

R04b resolved it on twelve degrees of freedom, `{4, 4.5, 5, 6, 7, 8, 9, 10, 12, 15, 20, 30}`, 
at the same `Gamma = 11.58`, `c = 0.5` and 2,000 streams, with continuity against R04 verified 
at the five common points.

- **`nu*(Eco-L1)` is enclosed by `[7, 9]`** — the last `nu` whose 95% ratio interval lies 
  entirely below unity and the first whose interval lies entirely above it — and estimated at 
  `8.10`, interval `[7.78, 8.37]`. The published `4.9` is far outside. **D3 stands**, now with 
  a location.
- **`nu*(Oracle)` is enclosed by `[4, 5]`**, estimated at `4.47`, interval `[4.31, 4.57]`. 
  The published `4.6` lies inside the bracket, and the arm sits on the analytic `4.7` (`4.678793`). 
  **This claim is not falsified.**
- **The estimation cost is `3.62`, interval `[3.31, 3.92]`**, or `3.22 [2.52, 3.82]` by a route 
  assuming no functional form, against the published `0.3`. Every interval excludes it. **D3.**

The bracket, not the point estimate, is the formulation to use in any revision: near the crossing 
one standard error spans 0.46 units of `nu`, so no point value is meaningful without its interval.

**The figure `8.52` that an earlier revision of `AUDIT_R04.md` obtained must not be quoted.** 
It was a two-point interpolation across the empty `(7, 30)` interval on a curve that is not linear 
in `nu`. The same rule on the refined grid gives `7.75`.

Full account, including the two controls that were re-specified before the result was read: 
`docs/sections/R04b.md` and `AUDIT_R04b.md`.

### 15 — R05, `regime` column contradiction (Class A, —)

The submitted script `Priorite_18b` wrote a `regime` column based on the recalibration rule's 
predicted crossover `w_star`, but the manuscript's appendix reported exponents fitted on `w_delta`, 
the crossover at the threshold the detector *actually* ran with. The CSV contradicted the paper it 
supported. R05 now emits both crossovers explicitly. No numerical claim of the manuscript is altered.

### 16 — R04b, the variance of a level read at a calibrated threshold (methodological, no manuscript claim affected)

Recorded here because it applies to every experiment of this repository that calibrates a threshold 
on one sample and measures at it on another, not because any published value moves.

A threshold selected on a finite calibration sample carries that sample's error into whatever is 
later read at it. The held-out false-alarm count of such a threshold therefore has the binomial 
variance **twice over**: once from the held-out draw, once from the calibration draw that placed 
the threshold. R04b verifies the factor distribution-free — calibrate on the empirical 95th 
percentile of 2,000 draws, read on 2,000 fresh ones, 20,000 replicates — and measures `1.4133` 
against the `sqrt(2) = 1.4142` a doubled variance predicts.

Two consequences were found by controls firing, and both were corrected in the specification of 
the control rather than in any draw:

1. A control that tests each arm's held-out level against *exactly* the nominal level omits half 
   the variance of its own statistic and rejects by construction as the sample grows. R04b replaces 
   it with a conditional two-sample test per arm, which removes the unknown true level from the 
   analysis, plus a pooled control that carries the factor 2 in its interval and the bisection 
   tolerance in its band. The two halves see different failures: the conditional test is blind 
   to a bias common to every arm, which is why the pooled one is retained.
2. A bootstrap that resamples only the measurement sample holds the threshold fixed and understates 
   the standard error of anything read at it — by a factor of 2.1 to 2.6 for the delay ratios of 
   R04b. An understated error narrows every interval and can also make a correct model fail its 
   own goodness-of-fit test, which is what happened before the correction.

**Recommended for `PROMPT_REPO_COMMON_PREAMBLE.md`, not applied**, since editing the shared preamble 
is outside the remit of one experiment: *the out-of-sample level of a threshold calibrated on a 
finite sample has twice the binomial variance, and any interval on that level must carry the factor, 
including after aggregation; more generally, any interval on a quantity read at a calibrated 
threshold must price the calibration error, and a bootstrap that resamples only the measurement 
sample does not.*

Whether any interval published by R04 or by another stream is affected is a question for an audit 
of those streams. It is posed here and not settled: R04's calibration control is in-sample by 
construction, which is a different situation, but the interaction has not been analysed.

### 17 — R06, the fourth-moment boundary and the pairing of Figure 6 (Class A and C, D1)

R06 is a port: its two tables are **byte-identical to the submitted campaign**, digests included, 
and every published quantity of Figure 6 is reproduced at D0. Three things nevertheless differ 
from what the manuscript shows or says.

**The fourth-moment boundary is computed rather than held as a literal (Class A, D1).** The 
submitted script carried the kurtosis of the standardized innovation as a default argument, 
`kurtosis=5.0`, with a comment naming `nu = 7`. The value is right — `3(nu-2)/(nu-4) = 5` — 
but a literal cannot follow `nu`. Computed from `(alpha, nu)`, the boundary is `beta = 0.9071`, 
`Gamma = 41.5843`. v87 prints `41.6`, so the value moves below the manuscript's printing 
precision and nothing published changes.

**The submitted figure conflates that boundary with the grid point beside it (Class C).** 
`Fig11_Whitening_Boundary.png` places an axis tick at the analytic boundary and plots the 
`Gamma = 41` measurement on top of it, so a reader takes a measurement to have been made *at* 
`41.6`. It was not: the grid contains `41`, which brackets the boundary from below by `0.58`, 
and nothing was run at the boundary. `fig06_validity_map.png` puts the grid on the ticks and 
the boundary on its own labelled rule. The claim is unaffected and supported — the binary 
stream is white at `41`, below the boundary, and at `60, 90, 120, 160, 200`, all above it.

**The caption's "100 independent streams per configuration" is true within a configuration 
and misleading across them (Class A, no published value affected).** The generator draws its 
innovations before the variance recursion, so `sign(eps_t) = sign(z_t)` and the submitted 
campaign, which keys streams on the seed alone, carries the same 100 label streams to all 13 
`Gamma`. The error streams are not shared — the classifier reads amplitudes — so the readings 
are correlated rather than identical: measured design effect **3.21**, effective sample size 
**405** of 1,300. This is a legitimate paired design that sharpens comparisons across `Gamma`; 
what it requires is declaration and the variance treatment it imposes, 
and **an undeclared paired design is a defect of analysis rather than of experiment**. 
R06 declares it, gates the pooled level on a seed-cluster bootstrap rather than on an interval 
that assumes independence, and measures the same design effect a second way with a counterfactual 
arm keyed per (`Gamma`, stream): **1.01** against **3.21**. The conclusion of the panel survives 
either treatment.

A camera-ready revision should say "100 paired streams per configuration", or cite the effective 
sample size, or both. Full account: `docs/sections/R06.md` and `AUDIT_R06.md`.

### 18 — R04b, oracle ratio offset (Class A, D3)

The manuscript claims the oracle arm crosses unity at 4.6 "on the analytic prediction". R04b 
demonstrates the oracle ratio exceeds its analytic prediction at all twelve grid points by a mean 
of ~5% (sign test p ~ 5e-4). The curve does not track the prediction; it lies systematically above 
it, and the crossing near 4.6 is the result of compensation between this offset and the curve's slope. 
The point `nu = 20` exceeding `pi/2` is the largest realization of this systematic offset, not an 
isolated anomaly. The crossing value is reproduced, but the characterization of its mechanism is 
falsified. Full account: `docs/sections/R04b.md`.

### `R11-onset-convention` — R11, the four delays of Figure 15B are not mutually comparable (Class A, no published value affected)

The submitted campaign gave the CUSUM one onset convention and the other four detectors another.
`worker_exp_b_h1` builds the CUSUM's stream as `eps[2000:] + Delta` with the statistic at zero
(`Priorite_12_multi_detector.py:308-310`), while PHT, ADWIN, DDM and EDDM receive the whole stream
with `onset=2000` (l.318-321). `strict_pht` tests `if m - M > threshold and t >= onset`, so a
crossing during warm-up is not returned **and does not reset the statistic**, and the warm-up loop 
of `run_river_detector` calls `update()` without ever reading `drift_detected`.

R11 runs three labelled arms. `reset` and `warmstart` put every detector on one convention;
`as_submitted` reproduces the per-detector mixture and is the only arm on which the caption's four
numerals reproduce.

| detector | `reset` | `warmstart` | `as_submitted` | v87  |
| -------- | ------- | ----------- | -------------- | ---- |
| CUSUM    | 28.4078 | 25.4347     | **28.4078**    | 28.3 |
| PHT      | —       | 27.0517     | **27.0517**    | 27.1 |
| ADWIN    | 2023.75 | 61.2123     | **61.2123**    | 61   |
| DDM      | 1873.61 | 249.6010    | **249.6010**   | 250  |

Placing the CUSUM and the PHT on one convention **reverses their published order**: the CUSUM 
falls to 25.4347 while the PHT stays at 27.0517, a paired seed-clustered difference of 
`+1.6170 ± 0.0318`, **50.9 standard errors**. This falsifies nothing v87 states — 
the caption asserts flat delays, and the delays are flat; neither the caption nor the body 
asserts an ordering in words — so the severity is null. What it establishes is that a reader 
comparing the four numerals compares across two conventions, and the caption does not say so.

The pre-onset leak is counted per detector over 100,000 streams: EDDM 91,560, DDM 9,780, 
CUSUM 3,180, PHT 2,400, ADWIN 40. It is logged even at zero and is deliberately not a gate.

Full account: `docs/sections/R11.md` and `AUDIT_R11.md`. Candidate:
`docs/camera_ready_candidates/R11_v87_detector_comparability.md`.

### `R11-cusum-add`, `R11-pht-slope`, `R11-pht-syncope` — R11, three moved numerals (Class A, D2)

All three follow from the 128-bit re-keying and are classified at v87's printing precision, 
each on the arm that produced it.

- **`Concept` CUSUM delay**, `reset` arm: `28.3` → **`28.4078`**. The three other caption delays 
  move below the printed precision and are D1: PHT `27.0517`, ADWIN `61.2123`, DDM `249.6010`.
- **PHT log-log slope**, `as_submitted`: `1.09` → **`1.0977 ± 0.0094`**, fitted on the **12 of 20**
  grid points where `DetRate ≥ 0.5`. Those delays are conditional on detection and biased downward 
  by selection on survival; the CUSUM and ADWIN are censored nowhere. The manuscript states neither 
  the domain nor the conditioning.
- **The stochastic syncope**: "beyond `Γ ≈ 75`" → the first grid point below 50% detection is
  **`Γ = 91.11`**. The collapse itself reproduces; the numeral moves. Both values are upper bounds 
  on a crossing the grid does not resolve, since detection declines across several points.

### `R11-pht-gamma-rule` — R11, the `λ × Γ` rule holds no level for the PHT (Class A, D2)

v87 L171 says the PHT "needs the same `λ × Γ` inflation" as the CUSUM, whose cure is described as 
one that "holds the nominal level", and the Figure 15 caption calls it the "same `λ × Γ` cure". 
Measured over the 20-point grid at 5,000 streams per point, with the `sqrt(2)` inflation that a 
calibrated threshold requires, the rate falls monotonically from **14.46%** `[13.14%, 15.89%]` at 
the attainable floor to **1.62%** `[1.19%, 2.19%]` at `Γ = 200` (value cited here; the macro
`\RElevenPhtGammaRuleHigh` reports the mean over `Γ > 20` at 2.10%). The extreme intervals do 
not overlap, so the drift is not sampling noise; there is no plateau at 5% anywhere.

**The cure works and only the word "same" fails.** False alarms are contained throughout — the raw
threshold runs above 80% on the same rows. This repository recorded the identical situation once
before: entry 7 found the StrictCUSUM's i.i.d. level to be 2.0% rather than the 5% ascribed to it 
and classified it D2, on the grounds that a conservative threshold is a legitimate design choice and 
what is inexact is calling it calibrated. The same reading and the same severity apply here. No figure,
table or theorem depends on the descriptor. Candidate:
`docs/camera_ready_candidates/R11_v87_pht_gamma_rule.md`.

### `R11-figure11-caption` — R11, the Figure 11 caption states one panel's parameters for both (Class A, D2)

The caption reads "abrupt drift `c=2`, `1,000` streams per point" for a figure whose panel A is
produced by `run_experiment_d(n_seeds=1000)` at `Delta = 2.0 σ` and whose panel B is produced by
`run_experiment_b(n_seeds=5000)` at `c = 1.5` (`Priorite_12_multi_detector.py:337, 592, 609, 613`).
v87 corroborates the correction twice in its own text: L296 and the Figure 15 caption both say
`c = 1.5` for the same `Concept` campaign. The claim the caption supports — "flat delays for all
detectors" — is a statement about panel B and is unaffected. Candidate:
`docs/camera_ready_candidates/R11_v87_figure11_caption.md`.

### `R11-gamma-grid-floor` — R11, the lower endpoint of the published `Γ` range is not attainable (Class A, no published value affected)

v87 L296 states the detectors hold a bounded FPR "across `Γ ∈ [1, 200]`". At `alpha = 0.08` the
penalty is minimised at `beta = 0`, where the closed form gives

    Gamma_floor(alpha) = 1 + 2*alpha/(1 - alpha) = 1.1739130435,

so no `beta ∈ [0, 1)` reaches `Γ = 1`. The submitted target grid
`concat(linspace(1, 50, 10), linspace(60, 200, 10))` therefore has an unattainable first point: the
bisection collapses to `beta = 0` and the process runs at the floor. The grid spans `1.1739` to
`200`, a ratio of **170.37**, which is what v87's own "`×170` range" describes — so the range
descriptor is right and the interval endpoint is not.

**This is the same finding entry 7 records for R03**, where the lowest grid point sat at
`Γ = 1.174` with `alpha = 0.08` and `beta = 0` and was an ARCH(1) stream rather than an i.i.d. one.
R11's macros carrying the sensitivity restriction are therefore named `…ExLowGamma` and not
`…ExIid`: excluding the point removes an ARCH(1) process at the attainable floor, not an i.i.d. one.

The control that found it was not adjusted. C2 carries two assertions decided by a closed form before
any solving — the realised penalty within `1e-6` of an attainable target, and `beta == 0.0` exactly
for an unattainable one — and `Gamma_target`, `Gamma_realised` and `attainable` are three distinct
persisted columns.

Separately: the R11 prompt lists the grid as the literals `1.17, 6.44, 11.89, …`. Those are the
submitted campaign's **realised** penalties rounded to two decimals, not its targets, and the script
verifies at run time that rounding each realised penalty reproduces the printed literal at all twenty
points. Solving for the targets instead of the literals moves `beta` at sixteen of the twenty points,
by at most `2.89e-5`.

### `R11-regenerated` — R11, the regenerated campaign (Class A, D2, pre-classified)

Prompt §2.1 requires migrating off `np.random.RandomState` keyed on the process parameter to a
128-bit `SeedSequence` keyed on role and index alone, which is the strategy R05 established. Every
Monte-Carlo value moves; this is acknowledged in advance and needs no per-value justification.

What it buys is a common-random-numbers design in which a difference between two `Γ` is an
algorithmic response rather than a difference of draw. What it costs is priced rather than ignored:
the seed-cluster bootstrap standard errors on the `Concept` slopes exceed their analytic OLS
counterparts by factors of **1.5 to 5.0**, and that ratio is the design effect. One consequence is
structural and is declared rather than corrected — under a key that carries no `gamma`, the `H0`
`Concept` arm is **bit-identical at all twenty penalties**, because `simulate_garch11` draws its
innovations before the variance recursion and `sign(eps_t) = sign(z_t)` exactly. That arm is kept as
an identity witness with a design effect of 20 by construction, it supports no claim, and every
published `H0` `Concept` rate is taken from a second arm whose key breaks the pairing.

Twelve published quantities are classified in `docs/sections/R11.md`: one D0, four D1, and the rest
D2. **No D3.** Every qualitative claim of `sec:universality` is reproduced.

### `R18-ljungbox-power` — R18, the Ljung–Box non-rejections are stated without their power (Class A, no published value affected)

Four sites of v87 carry the whitening property on an accumulation of Ljung–Box **non-rejections**:

| site                           | wording                                                                                        | design                          |
| ------------------------------ | ---------------------------------------------------------------------------------------------- | ------------------------------- |
| §4.4 L278 (`sec:validity_map`) | "the binary errors hold the nominal level in every regime (3.3–5.0%; 4.4% pooled)"             | 360 streams, `n = 8000`, lag 20 |
| §4.4 L290                      | "the binary error stream **stays strictly white** up to `Gamma = 200`"                         | Fig. 11A, 100 streams/config    |
| Fig. 6 caption L286            | "show **no detectable** autocorrelation in any GARCH regime"                                   | same 360 streams                |
| §4.8 L318 (`sec:real_world`)   | "a lag-20 Ljung–Box test finds no serial correlation on any asset …, **licensing** the filter" | 4 ETFs, 4 single tests          |

A non-rejection bounds nothing unless the instrument can reject, and an exhaustive grep of v87 for
`power`, `Type II`, `sensitivit*`, `false negative` and `fail to reject` returns no power analysis.
The gap was flagged independently by `AUDIT_R06.md` §8 item 3 and by `WRAPUP_Stream_B1.md` §6 item 3;
the second was written before submission and was not carried into v87.

**No published value changes and no D0–D3 severity applies**: R18 regenerates nothing. What is
registered is the other kind of divergence this file exists for — a claim whose evidential weight the
repository can bound while the manuscript states it unqualified. `R11-onset-convention` is the same
shape and carries the same null severity.

The bound, at the nominal 5% level and lag 20:

| `n`       | `rho_80`, the lag-1 autocorrelation the test detects with probability 0.8 |
| --------- | ------------------------------------------------------------------------- |
| `2,000`   | **0.1023** measured, `0.1018` analytic, 95% `[0.0992, 0.1050]`            |
| `8,000`   | **0.0506** measured, `0.0511` analytic, 95% `[0.0494, 0.0518]`            |
| `32,000`  | **0.0265** measured, `0.0256` analytic                                    |
| `128,000` | **0.0127** measured, `0.0128` analytic                                    |

`n = 8000` is the configuration behind L278 and the Figure 6 caption. L290's Figure 11A campaign runs
at the same horizon. L318's four ETF tests run on pre-2020 daily warm-up windows, bracketed by the two
shortest horizons above, so `rho_80` there lies between `0.051` and `0.102` — and each asset is read
once, not over 1,000 streams.

**What the non-rejections do and do not exclude.** Applied to the streams themselves — 13,000
HoeffdingTree error streams on R06's `Gamma` grid and 20,000 raw sign streams on R11's — the largest
pooled lag-1 autocorrelation measured anywhere is `0.000818`, which is `1.6%` of `rho_80`. At that
amplitude the instrument's power is **`0.050`, its own level**. The published non-rejections therefore
exclude a lag-1 autocorrelation above `0.051` at `n = 8000`, under a geometric-decay alternative, and
exclude nothing below it: the same non-rejection is returned whether the true autocorrelation is
`0.0008` or `0.04`.

This neither supports nor contradicts Proposition `prop:whitening`. It removes one reading — that the
non-rejections bound the autocorrelation by something smaller than `rho_80` — and it leaves the
proposition exactly where its own proof puts it.

Full account: `docs/sections/R18.md` and `AUDIT_R18.md`. Candidate:
`docs/camera_ready_candidates/R18_v87_whitening_evidence_strength.md`.

### `R16-dating-misdescription` — R16, the census is not the output of the dating L329 names (Class A, D3)

v87 L329 opens the census paragraph with "A retrospective multi-scale **Pagan--Sossounov**
bull/bear dating~\cite{pagan_sossounov_2003} **of the four streams** (2000--2025; $66$ phases
**after duration censoring**, the COVID-19 crash---too brief for the filter---dated at the *raw
scale*)". Measured on the same four derived FirstRate series, with the dating parameters the
delivered script fixes:

| dating run on the four streams                                 | phases | out of budget at `gamma = 20` | artefact                          |
| -------------------------------------------------------------- | ------ | ----------------------------- | --------------------------------- |
| Pagan--Sossounov on all four, no substitution                  | **48** | 38 (79.2%)                    | `R16_regime_census_strict_ps.csv` |
| Pagan--Sossounov on PFF, VNQ, BWX; Lunde--Timmermann on SPY    | **66** | **53 (80.3%)**                | `R16_regime_census.csv`           |
| Lunde--Timmermann wherever `check_sanity` fails, i.e. all four | 102    | 75 (73.5%)                    | `R16_regime_census_symmetric.csv` |

**The 66 are not reachable by the algorithm the sentence names.** `Priorite_16_regime_census.py`
evaluates `check_sanity` on SPY's Pagan--Sossounov MACRO dating (l.233), it fails, and the MACRO
turning points of that one stream are replaced by `lunde_timmermann(0.15, 0.15)` (l.237). SPY
contributes 30 of the 66 phases. Lunde--Timmermann applies **no duration censoring**: its
shortest SPY phase is 6 trading days, against 49 under strict Pagan--Sossounov on the same
stream. Both load-bearing clauses of the sentence — "of the four streams" and "after duration
censoring" — are therefore inexact.

**The values are not falsified.** `53`/`66` at the permissive budget, `52` on the sign arm, `64`
at one false alarm per year, `504\ln 20 = 1{,}510`, `504\ln 252 = 2{,}790`, the SPY 2011--2018
phase (`0.541 \to 0.554` over `1{,}753` days) and every numeral of L331 reproduce exactly, and
the regenerated census is **bit-identical** to the submitted `protocol_10b_regime_census_refined.csv`
on all 19 shared columns and all 66 rows. What is contradicted is the account of how the 66 were
obtained, which is why the severity falls on the method description and not on any number.

**The substitution is not silent in the delivered code.** Line 3 of the vendored
`data/reference/R16/Priorite_16_regime_census.log` reads `WARNING | [SPY] Sanity check P-S
failed. Fallback to Lunde-Timmermann for MACRO.` What preamble §S4.3 requires of a fallback that
is kept rather than removed is more than a warning — an explicit argument and a stamp in the
output filename — and that is what R16's three arms restructure. `sanity_ok` is moreover
initialised to `True` and reassigned only inside the `if ticker == 'SPY'` branch, so PFF, VNQ and
BWX are never tested by it; this repository evaluates the check on all four on every run, and
**all four fail it**.

**On §S3's halt obligation.** A D3 requires stopping, not reconciling. Here the halt lands on the
*manuscript*, which is frozen and cannot be edited, so the obligation is discharged by this
entry, by the camera-ready candidate, and by the persisted 48-phase counterfactual that makes the
claim checkable by a third party. No parameter, tolerance, seed or bound was moved to reconcile
anything, and the pipeline runs to completion because the regenerated *values* are not in
contradiction.

**No cause and no intent is attributed.** Preamble §S4.5 forbids it, and the evidence is equally
consistent with a description written from the design as intended rather than as executed.

Full account: `docs/sections/R16.md` and `AUDIT_R16.md`. Candidate:
`docs/camera_ready_candidates/R16_v87_dating_algorithm.md`.

### `R16-covid-phase-conditional` — R16, the COVID phase reproduces and is conditional on the substitution (Class A, no severity)

v87 L331's four numerals for the COVID crash reproduce **exactly**: `\Delta q = -0.2803`
(printed `\approx -0.28`), annualized Sharpe `-5.9904` (printed `\approx -6.0`), `23` trading
days, `\mathrm{kl} = 0.162042` nats/day (printed `0.162`), floors `34.12` at `\gamma = 252`
(printed `\approx 34`) and `18.49` at `\gamma = 20` (printed `18.5`), the latter being `80.4\%`
of the phase — v87's "four fifths". **Nothing in L331 is falsified.**

The phase nevertheless exists only under the SPY substitution: strict Pagan--Sossounov censors
the 23-day crash at its `min_phase = 84` rule, and the sentence and its four numerals disappear
with it. That is **the same measured fact** as `R16-dating-misdescription`, and one measured
fact produces one register entry: entering it twice at D3 would double the manuscript's apparent
exposure on a single finding, which is the over-declaration this campaign corrected on R11's
deviation table. This row therefore cross-references the D3 and registers no second severity.

**L329 already flags the exception.** The dating clause ends "the COVID-19 crash---too brief for
the filter---dated at the *raw scale*". The raw scale **is** the uncensored Lunde--Timmermann
dating, so the manuscript names the exception without naming the algorithm. Whether that
phrasing was meant to carry the substitution is not established by any measurement, and §S4.5
forbids deciding it. The D3 at `R16-dating-misdescription` stands unchanged and is unaffected by
this clause: "a Pagan--Sossounov dating of the four streams" still does not describe a
Lunde--Timmermann dating of one of them.

### `R16-floor-frac-envelope` — R16, the floor-fraction envelope of L329 (Class A, D2)

v87 L329 states that the phases the ceiling does not exclude are dominated on duration alone,
"and even there the floor consumes $55$--$92\%$ of the phase". Measured over the 13 phases
detectable at `\gamma = 20` on the unconditional arm: **`[50.1\%, 92.1\%]`**. The upper end
reproduces at the printed precision; the lower end does not. Two phases lie below 55%:

| phase                       | `T_days` | floor / duration |
| --------------------------- | -------- | ---------------- |
| PFF 2009-03-06 → 2011-05-19 | 556      | **50.11%**       |
| BWX 2021-01-05 → 2022-10-20 | 452      | **50.47%**       |
| SPY 2011-10-03 → 2018-09-20 | 1753     | 54.79%           |

**The cause is not identified.** SPY 2011--2018 is at `54.79\%`, which rounds to 55, and it is
the phase L329 names two clauses earlier — which *suggests* the published lower bound was read
off that single phase rather than off the minimum of the set. No measurement here establishes
it, so preamble §S4.5 applies and the association is recorded without a mechanism. Four
definitional variants were enumerated and logged by `exp_R16_regime_census_b.py`, and **none
yields 55--92**: bull phases only `[50.1\%, 92.1\%]`, `T_days >= 250` `[50.1\%, 92.1\%]`, both
together `[50.1\%, 92.1\%]`, the sign arm at `\gamma = 20` `[41.0\%, 97.5\%]`, and the
superseded `protocol_10a` census `[45.7\%, 95.9\%]`.

The qualitative claim the sentence supports — that the floor consumes most of even the phases it
does not exclude — holds at the corrected envelope, which is why the severity is D2 and not D3.

### `R16-boundary-sensitivity` — R16, the convention is declared and its effect is never reported (Class A, no severity)

v87 L392 declares the post-onset cut, states its mechanism correctly, and cites the right
example (`-18.6\%` on PFF, 2020-03-18, which this repository reproduces as
`-0.18583434620279932`). It never reports how much the convention moves the headline.

Three of the 66 phases change detectability with the convention, and **all three change in the
same direction** — they gain detectability under the post-onset cut:

| ticker | phase                   | Sharpe, inclusive → post-onset | floor, inclusive → post-onset |
| ------ | ----------------------- | ------------------------------ | ----------------------------- |
| PFF    | 2011-08-08 → 2013-05-08 | `1.0254 → 1.9800`              | `1435.8 → 385.1`              |
| PFF    | 2020-03-18 → 2021-12-31 | `0.9132 → 1.9046`              | `1810.7 → 416.2`              |
| BWX    | 2020-03-18 → 2021-01-05 | `1.8179 → 3.1323`              | `456.9 → 153.9`               |

The published count is therefore the **conservative end** of the interval `[53, 56]` =
`[80.3\%, 84.8\%]` that the two conventions bracket, and the sensitivity can only strengthen the
claim. Two of the three flips are the 2020-03-18 turning point L392 already cites.

**The direction runs against the manuscript's own headline, and the manuscript has the mechanism
right.** The double-counted trough return is a large negative outlier that depresses the mean
and inflates the variance of the phase that follows, biasing its floor upward — so the defect
*inflated* the published fraction (84.8%) and the correction *lowered* it (80.3%). Candidate:
`docs/camera_ready_candidates/R16_v87_boundary_sensitivity.md`.

### `R16-sign-arm-disagreement` — R16, "moves that count by one phase" is true of the count and false of the set (Class A, no severity)

v87 L329: "Pricing the binarization exactly through `kl(q_phase || q_ref)` moves that count by
one phase ($52$ of $66$)". The step of one holds — 14 phases detectable on the sign arm against
13 on the unconditional arm at `\gamma = 20`. **The two arms nevertheless disagree on 19 of the
66 phases**: 10 are detectable on the sign arm only and 9 on the unconditional arm only. The
step is a net, and there is no single flipping phase to name.

The two sets separate cleanly by phase type and by duration, which is a measured description and
not a mechanism: **all 10** sign-only phases are bear phases, of median duration 170 trading days
(SPY's 23-day COVID crash at `kl = 0.162`, its 40-day 2022 decline, VNQ's 2013 taper decline),
while **8 of the 9** unc-only phases are bull phases, of median duration 450 days (SPY 2003--2007
and 2011--2018 at `kl \approx 0.0003`, where the Bernoulli floor runs to nine thousand days
against an unconditional floor near nine hundred). All 19 are persisted in the
`arm_disagreement` column of `results/R16_regime_census/data/R16_sign_floor.csv`. No published
value moves; what is registered is that the sentence describes the count and not the set.

### `R16-substitution-scope` — R16, the published fraction is conditional on the substitution reaching one ticker of four (Class A, no severity)

The delivered script guards its dating substitution with `if ticker == 'SPY'`, and
`check_sanity` fails on all four tickers. Applying the same rule consistently — Lunde--Timmermann
wherever the check fails — gives **102** phases and **75** out of budget, i.e. **73.5%** against
the published 80.3%. That is 6.8 points: four times the displacement strict Pagan--Sossounov
produces (79.2%) and more than twice the boundary-convention envelope (80.3--84.8%).

The arm ships as `results/R16_regime_census/data/R16_regime_census_symmetric.csv` and is priced
by three macros. It is registered rather than left in the artefacts because an evaluator who
reads `if ticker == 'SPY'` will ask exactly this question, and finding the answer computed but
unremarked is worse than finding it stated.

**Direction, and the scrutiny it earns.** This arm moves the headline *against* the manuscript's
thesis, so preamble §S3's asymmetry rule assigns it the lighter examination, not the heavier. It
is also not a correction: Lunde--Timmermann at `\lambda = 0.15` on all four streams produces
102 phases of which seven are 2-to-6-day episodes of the 2008 crisis with a degenerate up-day
rate (`q_phase` exactly 0 or 1, clipped to `[10^{-6}, 1-10^{-6}]` before the divergence), which
is a different census rather than a better one. What it establishes is the conditionality, and
that is all it is recorded as establishing.

Full account: `docs/sections/R16.md` and `AUDIT_R16.md`.

### `R13-campaign-redraw` — R13, the regenerated oracle campaign (Class A, D2, pre-classified)

Prompt §2.6 requires migrating off the delivered `np.random.default_rng(20260716)` — a generator
keyed on nothing — to a 128-bit `SeedSequence` derived from an md5 condensate of each task's
semantic coordinates. That redraws the 20,000-replicate `FPR_H` bootstrap and the 5,000-replicate
`ARL0` null of every cell. It is required by the specification, not by an observed failure, and
this is the `R11-regenerated` and `R05-campaign-redraw` situation.

**One published numeral moves at v87's printing precision.** L331 prints the phase false-alarm
probability of the 3-day likelihood-ratio detection as `1.3\%`; the regenerated campaign measures
`0.01105`, i.e. **`1.1\%`**. Everything else in the sentence is unmoved: `3` days, `16` days, the
order of the two detector arms, and the `10.6x` Jensen ratio — which contains no Monte Carlo and
reproduces to the last digit of the witness.

**Two mechanisms, both readable from the shipped CSV.** `OP2b_ARL0_252` selects the first
threshold whose bootstrap `ARL0` reaches 252, and that `ARL0` is a mean over 5,000 regenerated
GARCH paths:

| grid index | `lambda`   | `FPR_H`   | `ARL0`     | `tau` |
| ---------- | ---------- | --------- | ---------- | ----- |
| 145        | `7.287181` | `0.01485` | `226.0884` | 3     |
| 146        | `7.748148` | `0.01140` | `250.2844` | 3     |
| **147**    | `8.238274` | `0.01105` | `293.1022` | 3     |
| 148        | `8.759404` | `0.00945` | `321.3612` | 3     |
| 149        | `9.313500` | `0.00895` | `350.9762` | 4     |

Index 146 is the threshold the submitted campaign selected; its regenerated `ARL0` is `250.28`,
just under 252, so the selection moves one grid step. At index 146 itself the regenerated `FPR_H`
is already `0.01140` — **the bootstrap redraw accounts for most of the movement and the one-step
shift for the rest**. The binomial standard error at `p = 0.0127` over `N = 20,000` is `0.00079`,
so `0.01275 -> 0.01140` is `1.7` standard errors, an ordinary draw. `tau = 3` holds at four
consecutive grid indices spanning `FPR_H` from `1.49\%` to `0.95\%`, which is why the delay does
not move while the probability beside it does.

**No qualitative claim of L331 is falsified.** Full account: `docs/sections/R13.md` and
`AUDIT_R13.md`. Candidate: `docs/camera_ready_candidates/R13_v87_covid_delay_numerals.md`.

### `R13-operating-points-unnamed` — R13, one sentence, two operating points, neither named (Class A, no severity)

The oracle frontier is a curve: `R13_oracle_frontier.csv` sweeps 200 thresholds per cell and
`R13_oracle_operating_points.csv` reads four calibrations off each sweep. L331 uses two of them in
one sentence and names neither.

| L331 clause                                                          | operating point read | rule                                              |
| -------------------------------------------------------------------- | -------------------- | ------------------------------------------------- |
| "detects it in `3` trading days ... false-alarm probability `1.3\%`" | `OP2b_ARL0_252`      | first `lambda` whose bootstrap `ARL0` reaches 252 |
| "to `16` days (standardized-mean CUSUM)"                             | `OP2b_ARL0_252`      | the same                                          |
| "no alarm on the 2011 correction at **the matched operating point**" | `OP1_isoFPR5_H`      | first `lambda` whose bootstrap `FPR_H` <= `5\%`   |

The consequence is concrete: at the iso-FPR point the same COVID row gives a **6**-day
standardized-mean delay, not 3 and not 16, and at `OP2b` the 2011 correction alarms on all ten
dead bands at `FPR_H` between `0.23` and `0.34`. Either number read at the other point contradicts
the sentence. `ARL0 >= 252` is not an arbitrary choice — it is one false alarm per trading year,
the calibration the two sentences immediately preceding L331 already use for the sign floor — so
naming it costs a clause and ties the two paragraphs together.

**Nothing is falsified.** Both operating points ship in the CSV and both reproduce the verdicts
v87 states. What is registered is that the sentence is not checkable as written. Candidate:
`docs/camera_ready_candidates/R13_v87_operating_points.md`.

### `R13-frozen-null-scope` — R13, the frozen path binds on one arm and not on the threshold (Class A, no severity)

L331: "against a bootstrap null freezing the same volatility path". The freeze is real and R13
asserts it: the `sigma_t` vector multiplying the resampled innovations under `H0` is byte-identical
to the one dividing the observed returns under `H1`, digested on its IEEE-754 bytes and compared on
all twelve (episode, oracle) pairs by control C4, which stops the run on any difference. Two things
the clause is read as covering are measured and are not covered.

**On the standardized-mean arm the frozen path cancels.** The `H0` increment is
`sign(Delta) * (mu_0 + sigma_t Z* - mu_0) / sigma_t = sign(Delta) * Z*`, so the path drops out and
`FPR_H` there is a property of the resampled innovations alone. Freezing it, redrawing it or
replacing it by a constant gives the same false-alarm axis. The freeze binds only on the
likelihood-ratio arm, where `sigma_t` enters squared — which is the arm the `3`-day figure comes
from, so the sentence's headline number is on the right side of the distinction and the `16`-day
number in the same sentence is not.

**The `ARL0` null is not frozen.** Both delays L331 prints are read at `OP2b_ARL0_252`, whose
threshold is the first whose in-control average run length over **5,000 regenerated GARCH paths**
reaches 252. That is a parametric null simulated forward from the fitted `(omega, alpha, beta)`
after a 500-step burn-in, and it is the null that fixes the operating point behind every numeral of
the sentence. The frozen-path null fixes the horizontal axis of Figure 14 and nothing else.

Neither limit falsifies anything; the correction is one clause. Candidate:
`docs/camera_ready_candidates/R13_v87_frozen_null_scope.md`.

### `R13-negative-control-scope` — R13, the 2011 clause holds at the two settings the caption names (Class A, no severity)

Figure 14's caption reads "the 2011 correction is not detected at either setting", naming
`delta = 0` and `delta_opt` on the standardized-mean CUSUM. **It is exact.** At
`OP1_isoFPR5_H` on the certified oracle `V1`, the 2011 correction does not alarm at `delta = 0`
(`FPR_H = 0.04015`) nor at `delta_opt = 0.079738` (`FPR_H = 0.0465`).

The L331 body sentence — "no alarm on the 2011 correction at the matched operating point" — does
not name the settings, and is true only of those two. Four larger dead bands **inside the same
iso-FPR band** alarm at 69 days of a 108-day phase:

| `delta` | `FPR_H`   | `tau` | `T` |
| ------- | --------- | ----- | --- |
| `0.25`  | `0.04325` | 69    | 108 |
| `0.30`  | `0.04480` | 69    | 108 |
| `0.40`  | `0.04350` | 69    | 108 |
| `0.50`  | `0.03520` | 69    | 108 |

The distinction is one of dead band, not one of calibration: all six settings sit inside the 5%
iso-FPR band the operating point defines. The caption is exact **because** it names its settings;
the body sentence is not, because it does not. No value moves and the negative control is not
falsified — what is registered is the gap between the caption's scope and the body's. The
correction is folded into `docs/camera_ready_candidates/R13_v87_operating_points.md` rather than
parked as a fourth candidate, since it is the second half of the same sentence.

---

### `R07-bias-bound-exceeded` — R07, L308's bound on the estimator bias is not respected (Class A, **D3**)

`sec:ar_garch` L308 states: "the systematic one, the classical small-sample AR bias
`E[φ̂] − φ ≈ −2.5 φ/n`, stays under `2.9 × 10⁻³`". The regenerated campaign gives a largest
`|E[φ̂] − φ|` of **`3.1269 × 10⁻³`**, at `φ = 0.15`, `n = 125`, with a standard error of
`1.5755 × 10⁻⁴` on the 10 000 trajectories — `+1.44` standard errors past the printed bound.

Source cell: `results/R07_estimated_mean/data/R07_estmean_diagnostics.csv`, row
`phi = 0.15, n_ols = 125`, columns `bias_phi_hat` and `bias_phi_hat_se`.

**Nothing was moved to reconcile it.** Three facts sit beside it and none of them excuses the
violation:

- **The argmax is structurally determined.** `−2.5 φ/n` is largest at the largest `φ` and the
  shortest window, which is exactly where the maximum lands, so the extremum carries the standard
  error of its own cell rather than the law of a maximum over 28 correlated cells.
- **v87's own approximation exceeds v87's own bound.** `−2.5 φ/n` at `(0.15, 125)` is
  `−3.0 × 10⁻³`, larger in magnitude than the `2.9 × 10⁻³` printed in the same sentence. The
  regenerated value is `+0.81` standard errors from that prediction: it agrees with the formula and
  disagrees with the bound.
- **The submitted campaign's own witness sits at `2.8697 × 10⁻³`**, `0.19` standard errors below
  the bound, and the delivered script's certification block gated on `max_bias < 2.9e-3` — a
  literal read off the output it had just produced. The bound is a Monte-Carlo realisation
  presented as a bound.

**Impact on the manuscript.** The qualitative claim of the sentence — that the systematic channel
is small, and that calibration depends on estimator *bias* rather than dispersion — is untouched:
`3.1 × 10⁻³` remains three orders of magnitude below the momentum coefficients being estimated, and
Figure 7's panel B is unaffected. What does not survive is the numeral read as a bound.
`docs/camera_ready_candidates/R07_v87_bias_bound.md` proposes the replacement.

Documented in full in `docs/sections/R07.md`.

### `R07-campaign-redraw` — R07, the campaign is regenerated under 128-bit keys (Class A, D2)

The delivered `np.random.SeedSequence(424242).spawn(7 × 10000)` keyed the trajectory
`(φᵢ, s)` on `phi_idx * N_SEEDS + s`, so paths differed across `φ`. Preamble §S6 requires a
128-bit key on the **role and index alone**. Keying on the index installs common random numbers
across the `φ` grid. 40 of the 42 Ljung–Box cells and all 42 FPR cells moved; four printed numerals
move at v87's printing precision:

| L308 / Figure 7 caption                  | submitted  | regenerated    | z against its own binomial SE |
| ---------------------------------------- | ---------- | -------------- | ----------------------------- |
| Ljung–Box rejection, `NAIVE`, `φ = 0`    | `5.1%`     | **`4.9%`**     | `−0.83`                       |
| `Concept` FPR, `NAIVE`, `φ = 0.15`       | `20.8%`    | **`21.0%`**    | `+0.49`                       |
| Ljung–Box envelope over the 28 OLS cells | `4.6–5.6%` | **`4.7–5.6%`** | extremum — see control C9     |
| `η` at `n = 125`                         | `11.4%`    | **`11.5%`**    | `+2.23`                       |

`99.8%` at `φ = 0.15` reproduces at printed precision. Every qualitative claim of L308 that these
support holds: the naive rejection climbs monotonically, every OLS cell stays inside the two bands
L308 prints, and the naive arm sits more than 20 paired standard errors outside the oracle band at
the top of the grid. Pre-classified Class A / D2 by the `R11-regenerated`, `R05-campaign-redraw`
and `R13-campaign-redraw` precedents.

### `R07-oracle-band-precision` — R07, the oracle reference band carries 10 000 trajectories, not 70 000 (Class A, no severity)

In the DGP, `h[t]` and `ε[t]` never reference `φ`; only `r[t] = φ r[t−1] + ε[t]` does. With the
trajectory keyed on its index alone, the oracle residual `r_curr − φ r_prev` is exactly `ε_curr` at
every `φ`, so the seven `ORACLE` cells are **bit-identical**: one measurement repeated seven times.
Control C4 measures `ρ = 1` exactly on that block — the statement rests on the bit-identity of the
columns, not on a float64 correlation estimate — giving a Kish design effect of `7.0` and
`n_eff = 10 000`.

The Figure 7 caption asserts that "all rolling-OLS arms match oracle false-alarm control". That
comparison is made against a reference band whose half-width is `√7 = 2.65` times what an
independent design would have bought. **This bounds the empirical corroboration; it touches no
theorem and no printed value** — the R18 precedent. Measured in
`results/R07_estimated_mean/data/R07_design_effect.csv`; the figure's `ORACLE` legend key states
the `n_eff`.

### `R07-lambda-star-estimator` — R07, `λ*` came from an estimator astride a lattice boundary (Class A, no severity)

The delivered script set `lambda_star = np.quantile(Ms_cal, 0.95)` on `N_CAL = 20 000` calibration
streams. The exact lattice law gives `F(11.2) = 0.948979`, so the interpolation position
`(N − 1) × 0.95 = 18 999.05` sits astride the boundary: the sample quantile returns `11.4` with
probability **`0.7380`** and otherwise `11.2` or the off-lattice `11.21`. The submitted log recorded
`lambda_star = 11.400000`; a re-keyed calibration had roughly one chance in four of contradicting it
for reasons unrelated to the science.

The repository implements the rule **L241 itself states** — "we take the nearest attainable level at
or below nominal" — on the exact law. `λ* = 11.4`, bit-identical to the float64 of the literal v87
prints. The delivered estimator is still computed and reported. **No published value moves.**

### `R07-panelB-operating-level` — R07, Figure 7 panel B operates at the upper attainable level (Class A, no severity)

Figure 7's caption reads "`Concept` FPR at threshold `λ* = 11.4` (exact lattice level `4.29%`,
`5.03%` at `λ = 11.2`; shaded band = the two attainable levels bracketing `5%`)". Both clauses are
individually true. Together they invite the reader to attribute `4.29%` to the panel, and the panel
does not operate there.

Floating-point accumulation leaves `M_H` above its exact lattice value on `9 652` of R07's
`10 000` `ORACLE` streams, below on `137`, exactly on it on `211`; of the `88` streams landing
exactly on `λ*`, all `88` are counted as exceedances. Over the `35 000` fair-coin streams R07
measured — its `ORACLE`, calibration and validation sets — the implemented test **coincides
exactly** with `M ≥ λ*` (`0` disagreements) and differs from `M > λ*` on `267`, so L241's footnote
holds as written at this threshold. The realised levels are:

| operator             | level on R07's `ORACLE` streams | exact law |
| -------------------- | ------------------------------- | --------- |
| float `M > λ*`       | `5.16%`                         | —         |
| exact `M_units > λ*` | `4.28%`                         | `4.3428%` |
| exact `M_units ≥ λ*` | `5.16%`                         | `5.1021%` |

On 25 000 independent fair-coin streams the delivered level is `5.064%`. The identity with
`M ≥ λ*` is **empirical, not structural** — the float `M` lands *below* its exact lattice value on
`480` of the `35 000` streams, so a stream whose exact maximum equals `λ*` can in principle be
missed — and it is asserted for this threshold, this horizon and this accumulation order only. The
footnote's last clause, "we report the level actually delivered", is what these numbers are.
**No printed value moves**; the register entry records that the caption's parenthetical is
about `λ*` and not about the panel. `docs/camera_ready_candidates/R07_v87_panelB_operating_level.md`
proposes the wording.

The exact levels `4.3428%` and `5.1021%` differ from the `4.29%` / `5.03%` v87 prints, by `+0.053`
and `+0.072` points. **R07 opens no entry on those two numerals**: L241 sources them to a
`2 × 10⁵`-stream campaign the repository's stream map assigns to R08, and a stream does not correct
what another stream owns. The evidence is handed over in
`docs/camera_ready_candidates/R07_v87_lattice_handoff_to_R08.md`.

### `R07-dispersion-cost-numeral` — R07, L308's "0.4 points" matches no reading (Class A, no severity)

L308 reads "the dispersion channel, whose RMSE reaches `11.4%` of `σ_unc` at `n = 125`, costs at
most `0.4` points of rejection". The sentence does not name the quantity. Six candidate readings
were enumerated by the script and logged; none returns `0.4`, in the regenerated campaign or in the
submitted witness:

| reading                                              | regenerated | witness   |
| ---------------------------------------------------- | ----------- | --------- |
| max over `φ` of (max OLS − `ORACLE`) at the same `φ` | `0.71` pt   | `0.62` pt |
| max OLS anywhere − max `ORACLE` anywhere             | `0.71` pt   | `0.29` pt |
| max OLS anywhere − mean `ORACLE` over the grid       | `0.71` pt   | `0.54` pt |
| max over `φ` of the spread across the four windows   | `0.89` pt   | `0.64` pt |
| max OLS anywhere − the `5%` nominal level            | `0.63` pt   | `0.57` pt |
| max OLS anywhere − min OLS anywhere                  | `0.93` pt   | `0.96` pt |

Since no reading returns `0.4` on the **witness** either, the numeral is not a casualty of the
redraw. The entry is opened against the manuscript: a printed quantity that cannot be located in
the campaign that produced the figure. `docs/camera_ready_candidates/R07_v87_dispersion_cost.md`
proposes stating the quantity and its value.

### `R09-campaign-redraw` — R09, the campaign is regenerated under 128-bit keys (Class A, D2)

The delivered `Priorite_22_eprocess_anytime.py` keys its whole campaign off `master_seed = 42027`
through a `SeedSequence.spawn` tree. Preamble §S6 requires a 128-bit key on the **role and index
alone**, so the port re-keys every task through `get_deterministic_seed` / `seed_sequence_for` /
`rng_for` and additionally replaces `rng.binomial(1, p, size)` by `(rng.random(size) < p)` — exact
Bernoulli either way, but a threshold on a shared uniform makes the common-random-numbers design
structural rather than dependent on an undocumented consumption pattern. Both changes redraw the
campaign by construction. Three printed numerals move at v87's own printing precision:

| L243 / Figure 9 caption          | submitted | regenerated | z of the difference |
| -------------------------------- | --------- | ----------- | ------------------- |
| peeking false-alarm rate at `4H` | `18\%`    | **`20\%`**  | `+4.77`             |
| MIX delay at `η = 0.10`          | `409`     | **`410`**   | `+0.24`             |
| CUSUM delay at `η = 0.10`        | `539`     | **`533`**   | `−0.44`             |

L243's "calibrated to `5\%` at `H = 5{,}000`" reproduces at printed precision (`0.0493 → 0.05345`,
both `5\%`), and `2\times10^4` is `N_NULL` in both campaigns.

**The peeking rate is the one displacement that is not an ordinary draw, and its channel is
named.** The CUSUM increment takes `+0.4` or `−0.6`, so `max_M` lives on a `0.2` lattice and the
calibrated threshold can sit only on that lattice. `np.quantile(max_M, 0.95)` returned `11.4` on the
submitted calibration sample and `11.2` on the regenerated one — **adjacent lattice points**, both
legitimate outputs of the same estimator. The two thresholds achieve the same level at the horizon
they were calibrated for (`0.0504` against `0.05034`); peeking to `4H` is where a one-step
difference is amplified (`0.1801 → 0.1988`, a ratio of `1.104`). Four of the seven levels moved one
step and three did not. R09 **does not separate** the threshold channel from the fresh-draw channel
— that would require the regenerated `H₀` sample replayed at the submitted threshold — and §S4.5
forbids asserting a decomposition the measurement does not establish. `R03-cusum-nominal-level` and
`R07-lambda-star-estimator` record the same estimator behaviour on the same statistic.

**Every qualitative claim these numerals support holds.** The fixed-horizon rate still climbs by
about a factor of four under continued watching; the mixture stays at or below `α` at all seven
levels (`FPR/α` ratios `0.945`–`1.000`); the CUSUM peeking rate exceeds the mixture's at all seven
levels at `22.9`–`68.5` **paired** standard errors on the same 20 000 streams; and e-CUSUM clears
`1/α` with a minimum margin of `20.54×`. Pre-classified Class A / D2 by the `R05-campaign-redraw`,
`R11-regenerated`, `R13-campaign-redraw` and `R07-campaign-redraw` precedents. Camera-ready
candidate: `docs/camera_ready_candidates/R09_v87_anytime_numerals.md`.

### `R09-arl0-censoring` — R09, panel C's CUSUM and MIX curves are horizon artefacts (Class A, no severity)

Figure 9's panel C plots the average run length of three arms against `α`, and its caption names
**one**: "e-CUSUM satisfies `ARL₀ ≥ 1/α`". That sentence is exact — e-CUSUM's run lengths are
right-censored on `0.00%` of streams at six of the seven levels and on `0.055%` at the seventh, and
it clears `1/α` by at least `20.54×`. **The other two curves in the same panel are not measurements
of a run length at all**:

| arm     | censored fraction over the seven levels | `ARL₀` range        | simulation horizon |
| ------- | --------------------------------------- | ------------------- | ------------------ |
| CUSUM   | `65.10%` – `95.54%`                     | `16 250` – `19 553` | `20 000`           |
| MIX     | `90.52%` – `99.06%`                     | `18 384` – `19 842` | `20 000`           |
| e-CUSUM | `0.00%` – `0.055%`                      | `205` – `2 751`     | `20 000`           |

`mean(min(fa, T_ext))` over a sample censored at fraction `c` is bounded below by `c · T_ext`
**by arithmetic**, with no reference to the detector: the MIX point at `α = 0.01` reads `19 842`
against a floor of `19 811`. Those points are the simulation horizon drawn on a log axis.

**Nothing printed is falsified**, which is why the entry carries no severity: the caption's only
`ARL₀` claim is about the one arm whose `ARL₀` is a measurement. What is registered is that the
figure gives three curves the same visual status. The repository's response is mechanical rather
than editorial — control **C1** refuses to persist, plot or macro-emit any `ARL₀` without
`censored_frac` on the same row; the macro emitter **exits `1`** rather than emit an `ARL₀`-derived
macro from a row censored above `50%`; and panel C draws the censored arms hollow on a lighter
dashed line, rules the horizon at `4H` and prints the per-arm censoring range in its legend. Three
`\RNine…CensoredFracMax` macros carry the fractions so a camera-ready sentence can cite them.
Candidate: `docs/camera_ready_candidates/R09_v87_arl0_censoring.md`.

The same table also settles what `arl0_bound_respected` is (`Priorite_22:613`). It is neither a
definitional tautology nor a literal: it is a computed comparison that is *arithmetically necessary*
on the censored arms, because `c · T_ext` already exceeds `1/α` there. It **carries information on
7 of 21 rows, all of them e-CUSUM**, and the port logs the implied lower bound and that verdict
row by row.

### `R09-add-conditioning` — R09, panel B's delay is conditional on detection (Class A, no severity)

`ADD` is a mean over the streams that alarmed inside `(τ, H]`, and at `α = 0.05` the detection rate
runs from `5.70%` (CUSUM, `η = 0.02`) to `97.60%` (MIX). The two arms therefore condition on
**different events**, and at the two smallest drifts the mixture — which detects `2.8×` and `3.7×`
more streams — averages over the hard streams the CUSUM never reaches, so its conditional mean comes
out **higher**: `+212` steps at `η = 0.02` (`z = +2.89`) and `+129` at `η = 0.04` (`z = +3.55`).
Read point by point, panel B at those two drifts inverts the ordering the data support.

**The severity of this entry was decided by a measurement whose decision rule was fixed before the
first number was read** (control C4). The primary instrument is a **matched-detection-rate
quantile**: at each `η`, set `q = min(p_CUSUM, p_MIX)` and compare the `q`-quantile of each arm's
alarm-time distribution with non-detections placed at `+∞`. It asks "to reach the same detection
rate, which arm needs fewer steps", conditions on nothing, and is the same iso-rate logic the
paper's own iso-FPR race uses.

| `η`    | `q`      | CUSUM `q`-quantile | MIX `q`-quantile | MIX − CUSUM | paired bootstrap 95% |
| ------ | -------- | ------------------ | ---------------- | ----------- | -------------------- |
| `0.02` | `0.0570` | `2404`             | `1292`           | **`−1112`** | `[−1242, −964]`      |
| `0.04` | `0.2000` | `2485`             | `981`            | **`−1504`** | `[−1562, −1427]`     |

The mixture is faster at every drift on the grid, and at the two points where the marginal curve
says the opposite the interval excludes zero. Under the pre-registered rule that is **case (1): the
reversal is an artefact of conditioning, `docs/camera_ready_candidates/R09_v87_delay_parity_scope.md`
stands, and the entry carries no severity.** Had the mixture been strictly slower with the interval
excluding zero, this would have been a D3.

**A second reading disagrees at the smallest drift and is reported rather than resolved.** On the
common-detection subset — the `70` of `2 000` streams both arms find at `η = 0.02` — the paired mean
difference is `+114` steps in the CUSUM's favour (paired SE `53`, within-pair correlation `0.757`).
That subset is the intersection of two detection events whose rates differ by `2.8×`; its
composition depends on both detectors, so it is a selected sample and gates nothing. Both readings
ship, and the disagreement is itself part of the finding. From `η = 0.04` onward the two instruments
agree.

### `R10-campaign-redraw` — R10, the skew-`t` campaign is regenerated under 128-bit keys (Class A, D2)

Preamble §S6 requires a 128-bit `SeedSequence` keyed on the **role and index alone**. The delivered
`Priorite_9_skew_robustness.py` keyed each stream on a bare integer `seed ∈ 1..1000` and built
`np.random.RandomState(seed)` inside `generate_garch_skew`. The migration is required by the
specification and not by any observed failure, and it redraws all 4 000 streams. It also installs
common random numbers across the `ξ` grid — the same `|T|` and `u` draws now serve all four grid
points — so every cross-`ξ` comparison is paired by construction and no pooled interval is read
before its design effect is measured (control C9).

Every Monte-Carlo value of the submitted campaign moves. **Two printed numerals move at v87's own
printing precision:**

| v87 site                      | printed | regenerated   | source cell                                      | z, one campaign | z, difference of two |
| ----------------------------- | ------- | ------------- | ------------------------------------------------ | --------------- | -------------------- |
| L290 realized skewness        | `−1.44` | **`−1.4280`** | `R10_skew_diagnostics.csv`, `xi=0.5`, `skewness` | `+2.76`         | `+1.95`              |
| Fig. 10 caption FPR upper end | `1.8\%` | **`1.5\%`**   | `R10_skew_fpr.csv`, max `fpr_qhat_rate`          | `−0.98`         | `−0.69`              |

**Three printed numerals do not move at that precision.** `q ≈ 0.58` regenerates at `0.582191`
(D1), the fixed-`1/2` firing rate `≈97\%` at `0.966` (D1), and the caption's FPR lower end `1.0\%`
reproduces exactly (D0). "1,000 streams per point" is structural and exact.

**The second `z` column is the one a comparison of two campaigns supports.** The printed value is
itself one Monte-Carlo realisation of the same design, so the standard error of the difference is
`sqrt(2)` times the standard error of either. At `+1.95` and `−0.69` standard errors the two
campaigns are two ordinary draws, and this entry does not claim the submitted values were wrong; it
records which draw the repository's artefacts contain.

**The moving envelope carries its own law.** A maximum over four cells that share all 1 000 streams
is an extremum statistic (§S4bis, fourth corollary). The bootstrap envelope of the regenerated
maximum, 2 000 replicates of the stream index, is `[1.2\%, 2.4\%]`, and the submitted `1.8\%` sits
inside it. Reading the printed numeral against a per-cell interval instead would have made this a
contradiction rather than a redraw.

**Every qualitative claim of L290 and of the Figure 10 caption holds.** The two Ljung–Box arms stay
within `4.6–6.3\%` of the `5\%` nominal across the whole grid while the fixed-`1/2` false-alarm rate
climbs monotonically from `0.5\%` to `96.6\%`, and the recentred arm stays below nominal at every
grid point. Camera-ready candidates `R10_v87_L290_skewness_numeral.md` and
`R10_v87_caption_fpr_envelope.md` propose the two numeral edits; both are **PARKED**.

Pre-classified Class A / D2 **before the first run**, by the `R11-regenerated`,
`R05-campaign-redraw`, `R13-campaign-redraw`, `R07-campaign-redraw` and `R09-campaign-redraw`
precedents. No parameter, tolerance, seed or bound was moved.

**Two R10 findings are deliberately *not* registered.** (i) Panel A's raw-sign curve is i.i.d.
`Bernoulli(q)` by construction of the delivered code — `ε_t = √h_t z_t` with `h_t > 0`, so
`1{ε_t > 0} = 1{z_t > 0}` bit-exactly on all 4 000 streams — so it measures the Ljung–Box test's
calibration rather than a property of the data-generating process. The caption's sentence is true
and §perimeter keeps an incomplete-but-not-false formulation out of this register; the camera-ready
candidate `R10_v87_panelA_sign_arm_scope.md` carries the clarification. (ii) The level this CUSUM
delivers under perfect centring is `0.345\%` at `δ = 0.1`, `λ = 15.0`, `n = 8 000`, so the recentred
arm's `1.0–1.5\%` is above the operator's own floor rather than below a `5\%` it could attain. v87
prints no nominal level attached to this detector, and the measurement exists only to make a control
readable, which §perimeter confines to `docs/audits/AUDIT_R10.md` and `docs/sections/R10.md`.

### `R12-campaign-redraw` — R12, both misspecification campaigns are regenerated (Class A, D2)

Preamble §S6 requires a 128-bit `SeedSequence` keyed on the **role and index alone**. The delivered
`Priorite_10_robustness_gjr_student.py` keys each stream on the **process parameter itself** —
`seed = int(gamma_lev * 1000) + s * 17` (l.131) and `seed = int(nu * 100) + s * 23` (l.194) — and the
second of those is a scheme the delivered script's own l.341–358 already flags as reusing seed values
across the `ν` sweep at shifted replicate indices. The migration is required by the specification and
not by any observed failure, and it redraws all 166 000 published streams.

**Ten printed numerals move at v87's own printing precision; six do not; four are structural.**

| v87 site                             | printed                          | regenerated                   | witness               | severity |
| ------------------------------------ | -------------------------------- | ----------------------------- | --------------------- | -------- |
| L349 Ljung–Box at `γ_lev = 0`        | `5.1\%`                          | **`5.4\%`**                   | `5.1\%`               | **D2**   |
| L349 Ljung–Box at `γ_lev = 0.28`     | `24.6\%`                         | **`24.2\%`**                  | `24.6\%`              | **D2**   |
| L349 FPR at `γ_lev = 0`              | `3.2\%`                          | **`3.5\%`**                   | `3.2\%`               | **D2**   |
| L349 FPR at `γ_lev = 0.28`           | `20.6\%`                         | **`20.5\%`**                  | `20.6\%`              | **D2**   |
| L349 Concept FPR range, lower end    | `7.6\%`                          | **`7.4\%`**                   | `7.6\%`               | **D2**   |
| L349 Concept FPR range, upper end    | `8.4\%`                          | **`8.5\%`**                   | `8.4\%`               | **D2**   |
| L349 Concept Ljung–Box, lower end    | `4.6\%`                          | **`4.7\%`**                   | `4.6\%`               | **D2**   |
| L353 detection at `ν = 10`           | `83\%`                           | **`82\%`**                    | `83\%`                | **D2**   |
| L353 detection at `ν = 7`            | `61\%`                           | **`62\%`**                    | `61\%`                | **D2**   |
| L353 censored delay, lower end       | `2{,}400`                        | **`2{,}600`**                 | `2{,}400`             | **D2**   |
| L349 Concept Ljung–Box, upper end    | `5.4\%`                          | `5.4\%` (`5.37`)              | `5.4\%`               | D1       |
| L349 "climbs by a factor of six"     | `six`                            | `6` (`5.92`)                  | `6` (`6.37`)          | D1       |
| L353 collapse threshold              | `5.5`                            | `5.5`                         | `5.5`                 | D1       |
| L353 censored delay, upper end       | `3{,}000`                        | `3{,}000` (`2998.77`)         | `3{,}000` (`3005.28`) | D1       |
| L353 Concept delay range             | `34`–`38`                        | `34`–`38` (`33.638`–`37.900`) | same                  | D1       |
| Figures 12/13 streams and grid sizes | `10{,}000` / `1{,}000` / 15 / 16 | identical                     | identical             | **D0**   |

**`83\% → 82\%` is a knife edge and is reported as one.** The regenerated rate is exactly `825/1000`.
As a decimal that is `82.5\%` — which rounds to `83` under round-half-up and to `82` under
round-half-even — but `0.825` is not representable in binary64 and its nearest double is
`0.82499999999999995559…`, so `82` is what every convention returns and the D2 does not rest on a tie
rule. The displacement is `−0.005` against a two-campaign standard error of `0.0168`, i.e. `0.30 σ`.

**The one printed range whose bracket was a halt candidate did not breach it.** v87 L353 prints
`2{,}400`–`3{,}000` **rounded to the hundreds**, and the submitted witness's own `2443.18` and
`3005.28` both round onto those numerals — so `3005` was never a contradiction and the watch item was
the rounding bracket `[2350, 3050)`. The submitted artefact carries **no standard error on the
censored domain at all** (`SEM_Data` is `NaN` exactly where `ADD_Data_Raw` is published), so §S3's
criterion — a printed bound is breached at D3 only if the regenerated 95 % interval excludes it —
could not have been evaluated on it; this port adds `SEM_Data_Raw` on the surviving streams of every
cell for that reason. Regenerated: minimum `2610.23` at `ν = 5.5` (`SEM = 93.57`, 471 survivors, 95 %
lower bound `2426.85`), maximum `2998.77` at `ν = 4.25` (`SEM = 112.64`, 341 survivors). Both stay
inside the bracket, so the pair is **D2 at its lower end and D1 at its upper end**, not D3.

**Every qualitative claim of L349 and L353 holds.** The baseline's rate climbs from `3.46\%` to
`20.48\%` and crosses its 5 % nominal at `γ_lev = 0.08`; its Ljung–Box rejection climbs `5.41\%` to
`24.19\%`; the sign pipeline is flat, with control C9's OLS slope at `−0.9286` points per unit
`γ_lev` (seed-cluster bootstrap 95 % `[−2.45, +0.66]`, `p = 0.248`, gate at `0.01` not fired, total
fitted drift `0.26` points over the whole grid); detection decays monotonically at all six adjacent
pairs of the uncensored domain; the collapse threshold is exactly `ν ≤ 5.5`; and the Concept delay
stays at `34`–`38` steps. Pre-classified Class A / D2 **before the first run** by the
`R03-campaign-redraw`, `R05-campaign-redraw`, `R11-regenerated`, `R13-campaign-redraw`,
`R07-campaign-redraw`, `R09-campaign-redraw` and `R10-campaign-redraw` precedents. No parameter,
tolerance, seed or bound was moved.

### `R12-concept-crn-degeneracy` — R12, the Experiment A sign stream is invariant by construction (Class A, no severity)

`simulate_gjr_garch` draws the whole innovation vector **before** the variance recursion, so
`ε_t = √σ²_t · z_t` with `σ²_t > 0` and therefore `sign(ε_t) = sign(z_t)` **exactly**, for every
`(ω, α, γ_lev, β)`. Experiment A holds `ν = 100` and `n = 7 000` fixed across the whole leverage grid,
so under the mandated key — role and index only — the monitored binary stream `(ε[2000:7000] > 0)` is
**bit-identical at all fifteen `γ_lev`**. Published on that arm, v87's "leverage-invariant" and
"`7.6`–`8.4\%`" would be true **mechanically** rather than measured.

R12 therefore runs two Concept arms and says which is which on every row of the CSV:

| arm                  | key                                     | `deff(fp_concept)` | `n_eff`   | status                     |
| -------------------- | --------------------------------------- | ------------------ | --------- | -------------------------- |
| `expA`               | `("R12", "expA", s)`                    | **15.0015**        | `10 000`  | identity witness, no claim |
| `expA_concept_indep` | `("R12", "expA_concept_indep", g_i, s)` | **1.0004**         | `150 000` | **published**              |

The degeneracy is **asserted, not remarked**: control C8 digests the monitored stream on 50 seeds ×
15 grid points and exits `1` unless all fifteen agree per seed, so a later change to
`simulate_gjr_garch` cannot silently break it. A Kish design effect of exactly 15 on a 15-point grid
is the arithmetic signature of readings that are one number repeated.
`R12_concept_crn_witness.csv` carries that one number fifteen times with
`supports_published_claim = False` on every row, and **no macro, figure point or interval reads it**.

**The Data arm is not degenerate on either key** — the symmetric filter reads `ε²_{t-1}` through the
variance recursion, which carries `γ_lev` — so the pairing sharpens the Data comparison
(`deff = 9.11` on the CRN key against `0.95` on the independent one) instead of collapsing it. This
is the same measured fact `R11-regenerated` records for R11's H0 Concept arm and entry 17 records for
R06's error streams: **an undeclared paired design is a defect of analysis rather than of
experiment**. No published value is affected, because no published value is taken from the degenerate
arm, which is why this row carries no severity.

**Three R12 findings are deliberately *not* registered.** (i) The two orphan CSVs
`expA_argarch_boundary.csv` and `expB_race_condition.csv` have **no producing script anywhere in the
delivery** — a grep for `argarch_boundary|race_condition` returns only the prompt that attaches them.
They are vendored verbatim under `data/reference/R12/orphans/` with a README stating the grounds.
Control C3 **reads** the first, recovers its two Wilson intervals to all 17 digits from the counts
`1000/1000` and `45/1000` at `z = Φ⁻¹(0.975)`, prints it beside R07's certified `φ = 0.15` cell
(`0.9979` / `0.0492` on `N = 10 000` against the orphan's `1.000` / `0.045` on `N = 1 000`) and
**leaves the gap unexplained**: recovering an interval construction does not recover a
data-generating process, and with the design unknown §S4.5 forbids attributing the difference. The
claim behind the file is v87 L302, which is R07's mission statement and which R07 has already
delivered, so no entry is opened and the two macros the R12 prompt lists for it are not emitted.
(ii) `expB_race_condition.csv` is **produced and not cited**: `delay_arf` is empty on 999 of its
1 000 rows (only `seed = 492` carries `216.0`), reported as measured with **no mechanism
attributed**, and v87 cites no frozen-versus-ARF race anywhere. (iii) v87 L349 calls
`α_sym = α + γ_lev/2` the symmetric GARCH(1,1) "*population limit*"; what the design gives is
mean-matching (`E[h_t]` obeys the same recursion as `E[σ²_t]`), while a population limit in the QMLE
sense is the Gaussian pseudo-true parameter, and **no measurement in this stream decides which one it
is** — the witness never fits anything. The question is posed in `docs/audits/AUDIT_R12.md` and left
open; an unsettled question is not a contradiction and §perimeter keeps it out of this register.

### `R14-campaign-redraw` — R14, the quasi-Gaussian control of L345 is regenerated under 128-bit keys (Class A, D2)

Preamble §S6 requires migrating the delivered `RandomState(100 / 200 / 201 / 300)` draws to a
128-bit `SeedSequence` keyed on **role and index alone**, never on a process parameter. R14 has
three such draws: the placebo micro-dither, the two synthetic GARCH controls, and the twenty QMLE
recovery streams. The migration redraws the synthetic controls outright, and three numerals of
v87 L345 move at the manuscript's own printing precision:

| v87 L345, the `t₃₀` control  | printed | witness              | regenerated                       |
| ---------------------------- | ------- | -------------------- | --------------------------------- |
| lower end of the range       | `0.98`  | `0.9818435754189944` | **`0.9544910179640719`** → `0.95` |
| upper end of the range       | `1.14`  | `1.1426127128069126` | **`1.2384142067139186`** → `1.24` |
| mean over the reliable range | `1.06`  | `1.0603026678597007` | **`1.041041514153539`** → `1.04`  |

**Every real-Bitcoin quantity is bit-identical to the submitted campaign.** The `Real_BTC` block of
the race table matches the witness on all 13 shared columns with a worst difference of exactly `0`:
the iso-FPR `4.7\%` (`5/106`), the `106` onsets, `ν̂ = 2.78`, `0.74` at `c = 0.35`, `1.01` at
`c = 1.5` and the mean `0.87` all reproduce at D0. The mechanism is structural rather than lucky:
the realized false-alarm rate is a discrete count and the `±1e-6` dither only breaks CUSUM ties, so
the migration cannot move the real arm.

**The mechanism of what did move is established by counterfactual, not asserted.** The
`--legacy-seeds` arm restores the delivered integer seeds and keeps every other change of this port
— the `round_trip` parser, the BLAS pinning, the assertion at every QMLE call site, the derived
reliability rule. It reproduces the witness on **all 88 cells** of `ADD`, `DetRate`, `SEM`,
`FPR_achieved`, `n_onsets` and `add_reliable`, and returns `1.0603026678597007` for the mean the
manuscript prints as `1.06`. Exactly two quantities drift in that arm, both by a mechanism:
`lambda_star` on the two ETH `Eco` calibrations (`7.7e-07` and `3.4e-07`, the only two bisections
that never break early and therefore run all forty halvings) and `Var_z_hat` (`4.7e-09`, the
`round_trip` parser moving the parsed returns by about one ULP through SLSQP's finite tolerance).
Neither changes a single delay. The redraw is therefore the whole cause, and a transcription error
is excluded.

**The qualitative claim of the sentence holds, and the interval says how comfortably.** L345 states
that the quasi-Gaussian control "inverts the ordering to \textsc{Eco-L1}-faster". The regenerated
mean ratio is `1.0410`, above parity, and the paired moving-block bootstrap over onsets
(`B = 2000`, block `24`, one resampled index vector shared by both arms and all seven magnitudes)
gives `[0.9793, 1.0688]` — an interval that **covers the published `1.06`**. The move is not
distinguishable from the redraw's own noise, which is why the severity is D2 and not more. The D3
condition was fixed before the run and evaluated separately: it is that the interval lie **entirely
below 1**, which would falsify the inversion; it does not. A single magnitude below parity
falsifies nothing at all, since v87 itself prints a range whose lower end `0.98` is already on the
other side.

**Three further consequences of the same re-keying are reported here and carry no separate
severity**, because none contradicts a printed value:

1. **The real-Ethereum iso-FPR match is lost.** The re-keyed dither moves the `Real_ETH` `Concept`
   calibration from `3/72` to `4/72` while `Eco` stays at `3/72`, so control C2 fires there. The
   arithmetic behind the fragility is in the test suite and is independent of any draw: the
   delivered bisection stops when `|k/N − 0.05| ≤ 0.005`, at `N = 106` exactly one integer count
   qualifies (`k = 5`, v87's `4.7\%`), and at `N = 72` **none** does — `3/72 = 4.17\%` and
   `4/72 = 5.56\%` straddle the band — so the submitted campaign's ETH agreement was an outcome of
   the bisection dynamics rather than a constraint the calibration enforces. v87 publishes no delay
   and no ordering claim about real Ethereum; what L345 says there is that "the fair-coin pivot does
   not hold exactly", which this corroborates. The source is stamped `iso_fpr_matched = False` on
   every row of the shipped CSV, no macro reads a speed comparison from it, and its ratio series is
   printed as description only. Nothing was reseeded, retuned or re-toleranced (§S4.10).
2. **The unreliable-cell count moves from `25` to `28` of `88`.** v87 prints the *rule*
   (`DetRate < 0.9`, hollow markers) and not the count; the count is a property of the redrawn
   synthetic controls and the legacy arm returns the submitted `25`.
3. **The QMLE recovery median bias moves from `0.0336` to `0.0228`.** v87 prints neither it nor the
   fallback fraction, which stays at `0.0000` and is logged even at zero (control C3).

**What is reported and not registered.** L345 and the Figure 16 caption both say "across the
reliable range" without defining it, while the aggregate they attach to it is taken over the
magnitudes at which **both** arms reach `DetRate ≥ 0.9` — seven points, `c ≥ 0.35`. That is
imprecise and not false: a ratio of two delays is only computable where both arms detect, so the
pairwise rule is forced by arithmetic rather than chosen. §S8's scope filter keeps it out of this
register; it is parked as a clarification in
`docs/camera_ready_candidates/R14_v87_reliable_range_scope.md`, which carries no register entry.

Full account: `docs/sections/R14.md` and `docs/audits/AUDIT_R14.md`. Candidate:
`docs/camera_ready_candidates/R14_v87_synthetic_control_numerals.md`.

### `R15-scatter-sign` — R15, the Figure 17 caption's `r ≥ 0.99` holds under neither sign convention (Class A, D2)

The Figure 17 caption closes with "Point-to-point scatter reflects threshold variations across
panel compositions (`r ≥ 0.99` with bootstrap threshold)". That prints a **relation**, not a value,
and the relation is false on both campaigns.

**The referent had to be defined, and it was defined on the text.** No line of either witness
script computes a correlation, so R15 defines one. "With bootstrap threshold" names `lambda_boot`.
"Scatter" names panel B's ordinate, and which ordinate that is comes from the delivered plotting
code rather than from a choice: line 378 sets `c_target = C_GRID[1]` and lines 379–380 draw exactly
one `budget_reduction` curve, at `c = 0.25`. Pearson `r` between those two over the ten `K`:

| campaign                         | `r` at `c = 0.25`     | `        | r     | `         | `r ≥ 0.99` | ` | r | ≥ 0.99` |
| -------------------------------- | --------------------- | -------- | ----- | --------- |
| submitted (`protocol_25d`)       | `-0.9893771840917368` | `0.9894` | false | **false** |
| regenerated (`R15_..._race.csv`) | `-0.9962104605839599` | `0.9962` | false | true      |

`-0.9894 ≥ 0.99` is false and so is `-0.9894 ≤ -0.99`: the printed inequality holds under neither
sign convention on the campaign the manuscript reports. The sign is negative at **every** magnitude
of the grid — `-0.9907`, `-0.9962`, `-0.9912`, `-0.9896`, `-0.9876` at `c = 0.10, 0.25, 0.50, 0.75,
1.0` — so it is a property of the mechanism and not of the one curve the figure draws.

**Why the sign is negative.** `budget_reduction` is `ADD_single / ADD_K`. A larger bootstrap
threshold slows the pooled monitor, which lengthens `ADD_K` and therefore shrinks the ratio. A
correlation between a ratio and the quantity in its denominator is negative by construction.

**The second reading is persisted and carries no entry.** The sentence admits `r` between `ADD_K`
itself and `lambda_boot`, which is `+0.9931` regenerated and `+0.9947` on the witness. Both
readings sit in `results/R15_cross_sectional/data/R15_scatter_correlation.csv` at all five `c`.
Both were computed during planning, on the witness campaign, **before** the referent was fixed; the
selection was made on the textual referent — panel B's ordinate against `lambda_boot` — and on
nothing else. Choosing after seeing which sign matched the caption would be selection on the
outcome, which preamble §S4 bans, so the order of operations is recorded here as sequence and not
offered as a defence.

**The severity is D2 and not more.** The qualitative claim the clause carries — the point-to-point
scatter of panel B is almost entirely explained by variation in the bootstrap threshold — holds on
both campaigns at `|r| ≈ 0.99`. Nothing about the escape, the plateau or the effective panel size
depends on the sign.

**`|r| ≥ 0.99` is not the correction.** That bound holds on the regenerated campaign (`0.9962`) and
**fails** on the submitted one (`0.9894`); a camera-ready printing it would be true of this
repository and false of the campaign the manuscript reports. `|r| ≈ 0.99` is the only form both
support. Two macros ship, `\RFifteenScatterCorrelation` (`-0.9962`) and
`\RFifteenScatterCorrelationAbs` (`0.9962`), both at four decimals: rounding the magnitude to two
prints `1.00` and hides that it sits just above the caption's bound while the witness sits just
below it.

**The attribution clause in the same sentence is a separate question and opens no entry.** Whether
the scatter is caused by *panel composition* cannot be tested here — the design draws exactly one
composition per `K`, so panel size and membership change together along the abscissa and are
confounded. The caption is not false, compositions do vary; see
`docs/camera_ready_candidates/R15_v87_scatter_attribution.md`.

Full account: `docs/sections/R15.md` and `docs/audits/AUDIT_R15.md`. Candidate:
`docs/camera_ready_candidates/R15_v87_scatter_sign.md`.

### `R15-campaign-redraw` — R15, both calibrations are regenerated under 128-bit keys (Class A, D2)

Preamble §S6 requires migrating the delivered `md5(...) % 2**32` seeds to a 128-bit `SeedSequence`
keyed on **role and integer grid index alone**. R15 has five such families — the naive calibration,
the bootstrap calibration windows, the held-out false-alarm windows, the H1 race windows and the H1
single-stream reference — and all five migrate. One printed pair moves at the manuscript's own
precision:

| v87, Figure 17 caption **(A)**       | printed       | witness         | regenerated                         |
| ------------------------------------ | ------------- | --------------- | ----------------------------------- |
| bootstrap holds the nominal 5% level | `4.8`–`6.4\%` | `4.75`–`6.35\%` | **`3.95`–`5.85\%`** → `4.0`–`5.9\%` |

Both endpoints are **extrema over a ten-point grid** and neither supports a gate (§S4bis, fourth
corollary): reading the wider of the two as a 95% statement over ten cells would trigger with
probability `1 − 0.95¹⁰ = 40.1%` under its own null. Their design-corrected standard errors are
`0.0407` at the minimum (`K = 75`) and `0.0391` at the maximum (`K = 40`), which are larger than
the move itself.

**The qualitative claim is what the caption asserts and it holds.** The clause says the real-window
bootstrap *holds the nominal 5% level* where the independence calibration does not. Regenerated,
every one of the ten `FPR_boot` values sits in `[3.95%, 5.85%]` against a `5%` target while
`FPR_naive` reaches `100%` by `K = 60`. The envelope moved; the level did not.

**What did not move.** The plateau (`2.0086` → `2.0299`, both rounding to the printed `2×`), the
whiteness switch point (`K = 10`, bit-identical), the COVID non-detection (`0` of `10`,
bit-identical) and the pooled sign correlation (`0.2610`, `0.26` at the printed precision) all
reproduce. The four RNG-free diagnostic columns are unaffected by construction, the panel
composition being frozen — see `R15-mkl-cbwr-rho` for the only residual there.

**One structural consequence of the re-keying is reported and carries no separate severity.** In
the delivered script the reference-arm seed string `real_race1_1_{c}_{MASTER_SEED}_{i}` and the
panel-arm string at `K = 1` are the **same string** on the **same** sub-panel, so the submitted
`budget_reduction(K = 1)` is exactly `1.0` by construction rather than by measurement — the
submitted CSV prints `1.0` to every digit at `c = 0.25, 0.50, 0.75, 1.0`. The migrated keys
`("race_h1", k_index, c_index, i)` and `("race_h1_ref", c_index, i)` separate the two roles, so the
regenerated `K = 1` cell is an honest estimate of 1 with sampling error: `0.9902`, `0.9986`,
`0.9785`, `0.9965`. No published aggregate reads `K = 1`; the plateau pools `K ≥ 20`. This is the
same class of finding as `R12-concept-crn-degeneracy`.

Full account: `docs/sections/R15.md` and `docs/audits/AUDIT_R15.md`. No camera-ready candidate: the
printed envelope is a measurement of a campaign, and which campaign the camera-ready prints is a
decision the register records rather than pre-empts.

### `R15-grid-provenance` — R15, two vendored witnesses declare different `K` grids at the same line (Class A, no severity)

Figure 17 publishes ten points on `K`. Two witness scripts are vendored under
`data/reference/R15/` and they declare **different** grids at the same line number:

| file                                                  | SHA-256 (first 16) | line 167                                             | its log runs          |
| ----------------------------------------------------- | ------------------ | ---------------------------------------------------- | --------------------- |
| `Priorite_25c_real_cross_sectional_escape_UPDATED.py` | `04bb704cb5474…`   | `K_GRID = [1, 5, 10, 20, 30, 40, 50, 60, 75, K_max]` | `K = 1, 5, 10, …, 97` |
| `Priorite_25c_real_cross_sectional_escape.py`         | `c8024944b5328…`   | `K_GRID = [1, 20, 50, K_max]`                        | `K = 1, 20, 50, 97`   |

Three facts settle which produced the figure, each verifiable with this repository and nothing
else. **(i)** `Priorite_25c_real_cross_sectional_escape_UPDATED.log` records
`Control (b) Whiteness K=5` and `K=10`, which no four-point grid can produce, and
`Priorite_25c_real_cross_sectional_escape.log` records neither. **(ii)** v87 embeds
`Fig30_RealCrossSectional_Escape_UPDATED.png`, the ten-point figure. **(iii)** The two runs agree
**exactly** at every shared `K` — `FPR_naive = 0.1115 / FPR_boot = 0.0490` at `K = 1`,
`0.9060 / 0.0615` at `K = 20`, `0.9865 / 0.0525` at `K = 50`, `1.0000 / 0.0495` at `K = 97` in
both — so they are the same code path on two grids and not two experiments. The four-point log is
timestamped `19:25` against the ten-point `14:16` **of the same day**: the coarse run is a later
re-run, not a predecessor.

**The published grid is therefore recovered from a source line and is not read off the artefact.**
The port carries `[1, 5, 10, 20, 30, 40, 50, 60, 75, K_max]` because
`Priorite_25c_..._UPDATED.py` line 167 declares it, and `exp_R15_cross_sectional_b.py` asserts both
lines and both logs at start-up so the claim cannot rot.

**Why the entry exists at all, given that nothing is contradicted.** The R15 prompt's §2.1 and the
planning that followed it both stated the delivered full real branch to be the four-point grid,
because both read the unsuffixed file — an exhaustive `grep -n 'K_GRID\|C_GRID'` over *that* file
returns four assignments and none of them is the published grid. The account was internally
coherent and wrong about which of two vendored files was authoritative. The lesson recorded here is
not that either reading was careless: it is that **neither party enumerated the candidate files
before asserting which one was authoritative**, and that a provenance claim has to name the digest
of the file it rests on. Both scripts and both logs are vendored for that reason.

No printed value of v87 is affected and no macro reads this entry. Full account:
`docs/audits/AUDIT_R15.md` §3. No camera-ready candidate.

### `R15-mkl-cbwr-rho` — R15, `MKL_CBWR=COMPATIBLE` moves the sign correlation in its last two bits (Class B, D0, **cause identified**)

The panel composition is frozen, so `rho_sign_meas`, `K_eff_meas`, `K_eff_ana` and `ljungbox_p_Pt`
carry no RNG and are deterministic functions of the panel. `K_eff_meas` and `ljungbox_p_Pt`
reproduce the submitted campaign **bit for bit at all ten `K`**. `rho_sign_meas` does not, on 7 of
the 9 cells where it is defined, and `K_eff_ana` follows it because it is a function of it:

| statistic       | worst relative difference | at     | mechanism-derived bound `T·K·ε` |
| --------------- | ------------------------- | ------ | ------------------------------- |
| `rho_sign_meas` | `3.214e-15`               | `K=10` | `1.144e-11`                     |
| `K_eff_ana`     | `2.367e-15`               | `K=10` | `1.144e-11`                     |
| `K_eff_meas`    | `0` (bit-identical)       | —      | —                               |
| `ljungbox_p_Pt` | `0` (bit-identical)       | —      | —                               |

**The cause is identified by controlled variation, not inferred.** `rho_sign_meas` is the mean of
the upper triangle of `np.corrcoef(signs)`, whose every entry is a BLAS inner product over the
`T = 5154` days — the only BLAS reduction in the block. Removing `MKL_CBWR` while keeping the four
thread pins recovers the submitted values **exactly, at all ten `K`, on all four columns**;
removing the thread pins as well (`fair_env.enforce_strict_determinism(legacy_blas=True)`) does
not, and neither does `VECLIB_MAXIMUM_THREADS`, which is inert here. The submitted campaign set the
four pins and never set `MKL_CBWR`; this repository's canonical bootstrap sets both.

**The recovery command is exact and it ships.** `exp_R15_cross_sectional_b.py --witness-blas`
removes `MKL_CBWR` from the environment before NumPy is loaded — `MKL_CBWR` is read once, when the
BLAS loads, so an assignment after `import numpy` is inert and argparse is far too late — and
stamps every output `_witness_blas`. It runs **unconditionally** from `run_experiment_R15.sh`,
after the default arm, on the construction R01's `--legacy-blas` and R14's `--legacy-seeds` already
use: a diagnostic executed only when a result looks wrong is an instrument of selection. Its
artefacts certify no v87 value; they exist to attribute a residual. `experiments/common/fair_env.py`
is shared by every stream and is **not** touched.

**Why the severity is D0.** No printed digit moves: v87 prints `ρ̂ ≈ 0.26` and the pooled mean is
`0.26100272704442673` (witness) against `0.2610027270444267` (default arm), both `0.26`. Every
published race quantity — `DetRate`, `ADD`, `SEM`, `ADD_single`, `budget_reduction`,
`add_reliable`, and the per-replicate windows and delays themselves — is **bit-identical between
the two arms**; only the design-effect columns move, at `≤ 2.6e-13`, because the Kish estimator
uses `np.dot`.

**Why the class is B and why that matters.** The submitted code was correct and the submitted
values remain exactly recoverable by a command this repository ships. That is the definition of
class B. `R01-variance-target` records the same shape of drift with the cause **not** identified
and is left unclassified for exactly that reason; two entries of the same shape, one explained and
one not, is what tells a reader which is which. The `R01` hypothesis that BLAS pinning was
responsible there was tested and **refuted**; here the counterpart hypothesis is tested and
confirmed, on a statistic that does dispatch to BLAS where R01's one-dimensional reduction does
not.

**The assertion this replaces, and why the replacement is stronger.** The plan for this stream
required asserting all four columns bit-identical. That gate is mis-specified: bit identity of a
BLAS reduction is not a property of the port, it is a property of the instruction-set constraint.
What must be frozen is the **integer** composition, and that is now asserted exactly, at all ten
`K`, by re-executing the witness's own extracted statements and comparing arrays (control C1
leg 1, `sys.exit(1)` on any difference). The four floats are then held to a bound **derived from
the mechanism** — a reordered double-precision sum of `N` terms moves by at most about `N·ε`
(Higham 2002, ch. 4), with `N ∼ T·K` — stated in the source above the run and not read off any
residual. The realised margin is at most `2.8e-4` of that bound.

Full account: `docs/sections/R15.md` and `docs/audits/AUDIT_R15.md` §5. No camera-ready candidate:
no printed value is affected.

### `R08-delivered-level-above-nominal` — R08, the level `λ*` delivers is above nominal, not below it (Class A, **D3**)

`sec:exactness` L241 states a selection rule and, in its own footnote, states which comparison the
code performs. Both are quoted here because the contradiction is between them and not inside either:

> we take the nearest attainable level **at or below nominal**, $\lambda^{\star} = 11.4$.

> The boundary case is not cosmetic: floating-point accumulation leaves $M_H$ a few ulps above its
> exact lattice value, so the implemented test $M_H > \lambda^{\star}$ **is** the mathematical
> $M_H \geq \lambda^{\star}$; we report the level actually delivered.

**R08 measures the footnote to hold**, and measures it rather than assuming it. Over all `200 000`
fair-coin streams of module B and at **every one of the six grid thresholds**, `float M > λ`
disagrees with the exact `M_units ≥ λ` on **zero** streams and with the exact `M_units > λ` on
between `970` and `2 032`. The mechanism is the footnote's own: the accumulated float sits above its
exact lattice value on `192 842` streams, below on `2 776` and exactly on it on `4 382`.

**On the integer lattice `P(M ≥ u) = P(M > u − 1)`, so four exact levels live at L241's two
thresholds and the sentence prints two of them.**

| operator at `λ`     | equals survival index | exact level    | measured (`2 × 10⁵` streams) |
| ------------------- | --------------------- | -------------- | ---------------------------- |
| strict `M > 11.2`   | `P(m > 56)`           | `5.1021 %`     | `5.0815 %`                   |
| weak `M ≥ 11.2`     | `P(m > 55)`           | `5.9900 %`     | `6.0200 %`                   |
| strict `M > 11.4`   | `P(m > 57)`           | `4.3428 %`     | `4.3230 %`                   |
| **weak `M ≥ 11.4`** | `P(m > 56)`           | **`5.1021 %`** | **`5.0815 %`**               |

The level `λ* = 11.4` **actually delivers** is `5.1021 %`, above the `5 %` nominal the rule promises
to stay at or below, and it is not among the numerals L241 prints. Requiring `P(M_H ≥ λ) ≤ 5 %`
requires `λ/2δ − 1 ≥ 57`, i.e. `λ ≥ 11.6`, where the delivered level is `4.3428 %` — one lattice
step.

**Two legs, and the classification rests on the first.**

- **Exact leg, decisive.** `5.1021 %` is produced by an absorbing-chain dynamic program that
  consumes no entropy at all, validated against exhaustive enumeration of all `2^H` sign paths at
  `H ∈ {8, 10, 12, 14}` and bit-identical to the independent table `R07_lattice_exact_law.csv`
  carries at the same horizon. It has no sampling interval and the trigger probability of the
  statement is `0`. It exceeds nominal by `0.1021` points, `2.0 %` of the nominal level itself.
- **Monte-Carlo leg, reported and *not* decisive.** The measured weak level is `5.0815 %` with a
  Wilson interval of `[4.9861 %, 5.1786 %]`, which **includes** `5 %`. On the Monte-Carlo evidence
  alone, preamble §S3's interval criterion would leave this at D2. At the exact level the Wilson
  bound clears `5 %` in expectation from about `1.8 × 10⁵` streams, so the `2 × 10⁵` basis L241
  states is right at that boundary and this draw came in `0.42` standard errors low.

**What is NOT falsified.** No printed numeral of L241 is wrong. `5.03 %` and `4.29 %` are correct
strict-comparison Monte-Carlo estimates of the basis the sentence states, and `λ* = 11.4` **is** the
threshold that rule selects under the strict comparison. What is falsified is the conjunction: the
level the code delivers at that threshold is not the level the rule promises, and the footnote's
closing clause — "we report the level actually delivered" — is not honoured by the numerals printed
beside it.

**Nothing was moved to reconcile.** No parameter, tolerance, seed or bound was touched; `λ*` comes
from L241's own rule evaluated on the exact law, and `57 × 0.2 == 11.4` bit-for-bit in float64.
Full account: `docs/sections/R08.md` and `docs/audits/AUDIT_R08.md` §4. Camera-ready candidate:
`docs/camera_ready_candidates/R08_v87_delivered_level.md`.

### `R08-campaign-redraw` — R08, both modules are regenerated under 128-bit keys (Class A, D2, pre-classified)

Preamble §S6 requires the trajectory key to carry the **role and index alone**. The delivered
`Priorite_21b_adverse_bias_and_null_law.py` took the `s`-th element of a
`SeedSequence(424242).spawn(7 * 10000)` list for module A, drew module B from
`SeedSequence(555555).spawn(N)`, and calibrated `λ*` from the bare integer seed
`np.random.default_rng(100)`. Migrating all three redraws every Monte-Carlo value of both modules.
This was pre-classified Class A / D2 **before the first run** by the
`R05/R07/R09/R10/R13-campaign-redraw` precedents.

| site                                    | v87 prints | regenerated   | source cell                                      |
| --------------------------------------- | ---------- | ------------- | ------------------------------------------------ |
| L311, Fig. 8 (B): FPR collapses to      | `0.86\%`   | **`0.95\%`**  | `R08_adverse_bias.csv`, `b = 0.15`, `fpr_biased` |
| L241: level bracketing `5\%` from above | `5.03\%`   | **`5.08\%`**  | `R08_null_law_lattice.csv`, `λ = 11.2`, strict   |
| L241: level bracketing `5\%` from below | `4.29\%`   | **`4.32\%`**  | `R08_null_law_lattice.csv`, `λ = 11.4`, strict   |
| (not printed) largest whiteness gap     | `2.84` pt  | **`2.21` pt** | `R08_adverse_bias.csv`, max `                    | delta_lb_pp | ` |

**Every qualitative claim holds.** The collapse is still an order of magnitude below the inflation
(`0.95 %` against `21.0 %`, a factor of `22`); both monotonicities of L311 hold over the whole grid
with zero inversions in ten consecutive steps; the two levels still bracket `5 %`, and `λ* = 11.4`
does not move because it comes from L241's own rule on the exact law rather than from a sample
quantile. The largest whiteness gap stays at `b = 0.075` and stays inside the three points the body
states, with a 95 % bootstrap envelope of the maximum of `[1.56, 3.61]` points.

**The two bracketing levels are corrected in the register and NOT in the manuscript.** They are
correct Monte-Carlo estimates of the basis L241 states, and the exact law is reported beside them
rather than substituted for them (`docs/camera_ready_candidates/R08_v87_lattice_exact_basis.md`).
The collapse numeral is corrected: `docs/camera_ready_candidates/R08_v87_adverse_numerals.md`.

**Two numerals of the same two sentences are NOT R08's to register.** `20.8 % → 21.0 %` and the
`1.1 → 1.3` point under-centering penalty are cells of
`results/R07_estimated_mean/data/R07_estmean_lb_fpr.csv`, arm `NAIVE`, whose redraw
`R07-campaign-redraw` already registers. R08 reads them at `round_trip`, control C6 asserts its own
recomputation of that arm is **bit-identical** to them on all six values of `b`, and R08 files the
numeral edit on the two sites it owns while opening no new entry.

Full account: `docs/sections/R08.md` and `docs/audits/AUDIT_R08.md` §4.

### `R17-eco-l1-arm-identity` — R17, L341 attributes its false-alarm numerals to the arm that did not produce them (Class A, **D3**)

L341 opens *Estimation cost.* with "\textsc{Eco-L1} must fit a persistent GARCH" and then quotes a
false-alarm rate of `9.5 %`. **Table 1 defines `Eco-L1`, and the definition is not the statistic the
producing cell monitors.** The finding is established in three steps, each quoted verbatim and cited
by line, before it is classified.

**Step 1 — what Table 1 defines.** `articleB_whitening_v87.tex` line 117:

> `\textsc{Eco-L1}   & $\varepsilon_t/\hat\sigma_t$, QMLE-standardized   & fitted GARCH,
> re-estimated per onset   & location ($1$st order) & …`

A **signed level** residual, monitored for a **first-order** change.

**Step 2 — what the producing cell monitors.** `data/reference/R17/Priorite_6_econometric_baseline.py`,
`protocol_3d_warmup_sensitivity`, lines 421–430:

```python
z_hat = eps_eval / np.sqrt(sigma2_eval)
x_eco = z_hat**2
…
z_eco = (x_eco - mu_eco) / max(sig_eco, 1e-8)
if strict_cusum(z_eco, 0.5, 65.0) >= 0:
```

A **centred square**, monitored for a **second-order** change at the `(0.5, 65.0)` operating point.
The delivered script distinguishes the two by name in its own `protocol_3b`: `adds_eco_l2` is the
squared arm at `(0.5, 65.0)` (l.274–276) and `adds_eco_l1` is `strict_cusum(z_eco_hat, 0.5, 10.0)`
on the level (l.279). The two arms are simultaneously present, separately named and separately
thresholded in the source, so they are not one statistic under two names.

**Step 3 — can the L1 arm produce the numeral anywhere?** No. `protocol_3b` runs `n_seeds = 100`, so
its rate lattice is `k/100` and **`9.5 %` is unattainable there**; its `FPR_Eco_L1` column reads
`0.07`–`0.12` in the submitted campaign and `0.13`–`0.16` in the regenerated one. `9.5 % = 19/200`
is exactly the resolution of `protocol_3d`, which `__main__` runs at `n_str = 200` (l.515). The
numeral is `protocol_3d`'s, and `protocol_3d`'s monitored statistic is the squared one.

**Classification.** The governing precedent is `R16-dating-misdescription`, classified **D3**: a
method description the pipeline does not produce falsifies a qualitative claim whatever the numeral
does. The three steps establish that Table 1's `\varepsilon_t/\hat\sigma_t` and `protocol_3d`'s
`(\hat z^2 - \mu)/\sigma` are different statistics of different orders at different operating points,
so the row is D3.

**Scope, stated precisely.** The misattribution reaches the **false-alarm numerals** of L341 —
`9.5 %` at `n = 250` and the restored `3.0 %` at `n = 500` — and **not** the persistence median. The
QMLE fit is common to both monitors, so `\hat\alpha+\hat\beta` is arm-agnostic and the collapse L341
reports is a statement about the estimator rather than about either detector. Nothing here concerns
`tab:isofpr_race` or `fig:crypto_race`, where `Eco-L1` **is** the level residual and R04 and R14
measure it as such.

Full account: `docs/sections/R17.md` and `docs/audits/AUDIT_R17.md` §4.

### `R17-campaign-redraw` — R17, the warm-up campaign is regenerated under 128-bit keys (Class A, D2, pre-classified)

Preamble §S6 requires the trajectory key to carry the **role and index alone**. The delivered
`Priorite_6_econometric_baseline.py` seeded `np.random.default_rng` with the bare integers `s*77`
(3a), `s*77 + 99` (3b), `s*42 + 888` (3c) and `s*101 + nw` (3d). Migrating all four redraws every
Monte-Carlo value of the campaign. This was pre-classified Class A / D2 **before the first run** by
the `R05/R07/R09/R10/R13/R14/R08-campaign-redraw` precedents.

| site                                  | v87 prints | regenerated     | source cell                                                              |
| ------------------------------------- | ---------- | --------------- | ------------------------------------------------------------------------ |
| L341, persistence median at `n = 250` | `0.62`     | **`0.63`**      | `R17_warmup_sensitivity.csv`, `(250, 0.00)`, `persistence_median_pooled` |
| L341, FPR at `n = 250`                | `9.5\%`    | **`10.5\%`**    | same cell, `FPR_Eco`                                                     |
| L341, restored level at `n = 500`     | `3.0\%`    | **`7.0\%`**     | `(500, 0.00)`, `FPR_Eco`                                                 |
| L341, sign envelope                   | `3`–`8\%`  | **`10`–`11\%`** | `FPR_ML`, min–max over the four warm-up lengths                          |
| (not printed) non-convergence maximum | `0.5\%`    | **`1.5\%`**     | `share_nonconverged`, `(250, 0.28)`                                      |

**Every qualitative claim of L341 holds.** The persistence still collapses at `n = 250` and climbs
back with the window (`0.626`, `0.775`, `0.841`); the parametric rate still falls monotonically with
the warm-up on **both** leverage settings, with zero inversions beyond two paired standard errors in
six consecutive steps; the `n = 500` Wilson interval still covers the nominal `5 %` on both columns,
which is the falsification rule §S3 fixes for a printed level; and the sign arm still shows no
warm-up dependence — its weighted least-squares slope on `log(n_warmup)` is `+0.0021` with a paired
stream bootstrap interval of `[-0.0153, +0.0195]` covering zero at `p = 0.84`.

**The persistence gap is not one number, and the largest of its three terms carries no draw at all.**
The witness stored the **sum of marginal medians** (`0.047881 + 0.573349 = 0.621230`) where L341
reads "a median `\hat\alpha+\hat\beta`", which is the median **of the sum**. Both constructions are
computed on the same fits and persisted side by side on both option arms, which decomposes the
`+0.0058` total against `0.62` into `+0.0427` definitional, `-0.0001` optimiser options and
`-0.0368` redraw. The definitional term is the largest, and it is exact.

**SPECS §1.10 is not what moved the numerals, and the attribution arm is what says so.**
`--qmle-options legacy` restores the delivered `minimize` call verbatim on the same draw. Three of
the six regenerated tables are then **bit-identical** to the compliant arm, the sign column of the
warm-up table is bit-identical, every false-alarm rate of the warm-up table is identical to the last
digit, and the persistence median moves by `-1.4e-4`. Compliance costs a fourth decimal; the
displacement is the re-keying.

Full account: `docs/sections/R17.md` and `docs/audits/AUDIT_R17.md` §4. Camera-ready candidates
(clarifications, no register entry of their own):
`docs/camera_ready_candidates/R17_v87_warmup_resolution.md` and
`docs/camera_ready_candidates/R17_v87_warmup_restoration_scope.md`.

### `R17-sign-arm-crn-degeneracy` — R17, the warm-up sweep's sign stream is invariant across the leverage axis by construction (Class A, no severity)

`simulate_gjr11` draws the whole innovation vector **before** the variance recursion, so
`\varepsilon_t = \sqrt{\sigma^2_t}\, z_t` with `\sigma^2_t > 0` and therefore
`sign(\varepsilon_t) = sign(z_t)` **exactly**, for every `(\omega, \alpha, \gamma_{lev}, \beta)`.
`protocol_3d` holds `\nu = 7` fixed and, at a given warm-up, holds the stream length fixed as well,
so under the mandated key — role and index only — the monitored binary stream
`(\varepsilon[nw:] > 0)` is **bit-identical at both `\gamma_{lev}`**. Its eight cells hold **four**
readings, and a mean over the eight carries a Kish design effect of exactly `2.0`.

**The submitted campaign carries the same identity, under its own seeds.** Its key `s*101 + nw`
omits `\gamma_{lev}` for the same reason, and its own table exhibits the consequence directly:
`FPR_ML` is equal at the two leverage settings for every warm-up length — `0.075/0.075`,
`0.030/0.030`, `0.055/0.055`, `0.080/0.080`. The degeneracy is therefore a property of the
experiment as delivered and not an artefact of the migration.

**The R12 precedent does not transfer, and no second arm is built.** `R12-concept-crn-degeneracy`
runs two Concept arms because there the degenerate axis **is** the axis v87 makes its claim about.
Here L341 says nothing about `\gamma_{lev}`; the invariance it asserts is across `n_warmup`, which is
**not** degenerate — the vector length changes with the warm-up, so the four evaluation windows
overlap by 65 % to 95 % and carry four genuine draws. A second `\gamma_{lev}` arm would be a variant
the manuscript does not describe, which the scope filter forbids.

**What the entry owes instead, and what discharges it.** The identity is **asserted** by SHA-256 over
the monitored streams at every warm-up and the run exits `1` otherwise, so a later change to
`simulate_gjr11` cannot break the statement silently; the test suite re-asserts it stream by stream
from the persisted per-fit table. The `3`–`8 %` envelope is published with its effective count
declared — a min–max over **four** readings of 200 streams each, not eight — with a paired stream
bootstrap around each extremum, and it **gates nothing** (§S4bis, fourth corollary). The invariance
itself is tested by a statistic that has a distribution: a WLS slope of the rate on `log(n_warmup)`,
weights from the binomial variance at 200 streams, null law from the same paired bootstrap so the
window overlap is priced.

**No published value is affected**, which is why this row carries no severity: the envelope L341
quotes runs along the warm-up axis, and the degenerate axis contributes no reading to it. What the
entry records is that the **evidence** behind a claim the manuscript makes is half as wide as its
table suggests, which is why it takes the heavier examination of §S3 rather than the lighter one.

Full account: `docs/sections/R17.md` and `docs/audits/AUDIT_R17.md` §3, control C2.
