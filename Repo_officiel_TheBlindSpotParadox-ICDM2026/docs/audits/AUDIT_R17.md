# AUDIT — R17, estimation cost of the parametric route (v87 L341)

| Field                   | Value                                                                                                       |
| ----------------------- | ----------------------------------------------------------------------------------------------------------- |
| Stream                  | R17, `experiments/R17_econometric_baseline/exp_R17_econometric_baseline.py`                                 |
| Source                  | `Priorite_6_econometric_baseline.py`, protocols `3a`, `3b`, `3c`, `3d`                                      |
| Manuscript locations    | `sec:misspecification` **L341** only; Table 1 **L117** for the arm definition                               |
| Figures of v87 rendered | **none** — `grep -c 'Fig10_Econometric_Baseline'` on the frozen `.tex` is `0`                               |
| Arms                    | `--qmle-options specs` (certifies v87), `--qmle-options legacy` (certifies nothing)                         |
| Register entries opened | `R17-eco-l1-arm-identity` (**D3**), `R17-campaign-redraw` (D2), `R17-sign-arm-crn-degeneracy` (no severity) |
| Camera-ready candidates | two, both `NO DEVIATION — clarification only`                                                               |
| Measured cost           | 362.2 s + 338.6 s = 700.8 s per full pass, serial                                                           |

---

## 1. What R17 establishes, in one paragraph

On a GJR-GARCH stream of true persistence `0.85`, a symmetric GARCH(1,1) fitted by Gaussian QMLE on a
250-step warm-up recovers a median `α̂+β̂` of **`0.6258`**, delivers a false-alarm rate of
**`10.5 %`** on the 5000 steps it then filters, and returns toward the truth as the window grows
(`0.775` at 500, `0.841` at 1000). The rate falls monotonically with the warm-up on **both** leverage
settings — `10.5 → 7.0 → 3.5 → 2.0 %` and `10.0 → 7.5 → 4.0 → 2.0 %` — with zero inversions beyond
two paired standard errors in six consecutive steps, and its `n = 500` Wilson interval covers the
nominal `5 %` on both. The sign arm, which estimates nothing, shows no warm-up dependence: its
weighted least-squares slope on `log(n_warmup)` is `+0.0021` with a paired stream bootstrap interval
of `[−0.0153, +0.0195]`, `p = 0.84`. Every qualitative claim of L341 therefore holds; four of its
printed numerals move under the 128-bit re-keying, and one of its attributions does not survive the
`ast` evidence.

## 2. Five things the reader must not take from this stream

**(i) Four of the five delivered tables certify nothing v87 prints.** L349's misspecification
numerals (`5.1 → 24.6 %`, `3.2 → 20.6 %`, `4.6`–`5.4 %`, `7.6`–`8.4 %`) come from `fig:leverage`,
which **R12** owns at 15 leverage points, 10 000 streams and a pseudo-Gaussian `ν = 100`; protocol 3c
runs four points, 1000 streams and Student-`t7`. The false-alarm explosion of protocol 3a belongs to
`fig:fpr_explosion` (**R03**) and the delay race of protocol 3b to `tab:isofpr_race` (**R04**). Only
protocol 3d feeds L341, and every macro this stream emits comes from it.

**(ii) The `ML` arm is not an oracle-parameter arm.** It estimates nothing and reads no true
parameter: it monitors `(ε_t > 0) − 0.5` at a fixed dead band and a fixed threshold. Its constancy
along the `Γ` and `γ_lev` grids is an **algebraic identity** of the simulators, not evidence of
robustness.

**(iii) The `3`–`8 %` envelope is an extremum over a grid and gates nothing.** It is a min–max over
**four** readings of 200 streams each, presented in eight cells. The tight **`10`–`11 %` regenerated 
envelope (1 point wide) is an artefact of pairing**: because `n_warmup` is excluded from the seed, 
the four cells share their innovation vector and differ only by the evaluation window shift. 
Independent samples at this count would span ~5 points. Any inferential statement about
warm-up independence must be read off the slope and its interval, never off the envelope.

**(iv) The delivered convergence flag does not measure convergence.** At the cell L341 publishes it
reports `share_nonconverged = 0.0` while **29 %** of the fits sit on the optimiser's lower bound
`(1e-6, 1e-6)` — persistence about zero, no GARCH at all — and are recorded as converged. 
This corner solution accounts for a third of the persistence collapse reported in v87.

**(v) SPECS §1.10 is not what moved the numerals.** The compliance change costs a fourth decimal on
the persistence median (`−1.4e-4`) and moves no false-alarm rate at all. The displacement against the
submitted campaign is the 128-bit re-keying and, for the persistence median, a definitional change
the witness's own storage forced.

---

## 3. Controls, with their margins and their trigger probabilities

Every trigger probability below is computed **under the control's own null law**, never under the
witness's numbers: `AUDIT_R14.md` §7 finding 2 established that a trigger probability conditional on
a draw the specification replaces is not a trigger probability. §S4bis's eighth corollary is the
governing rule.

### C1 — convergence, per fit, at all eight cells including the zeros

**Structural; trigger probability 0.** The quantile and median treatment was declared in the log
**before** the campaign ran: `\RSeventeenMedianPersistenceAtWarmupTwoFifty` is the median of the
per-fit sum `α̂ + β̂` over **all** fits, converged and not, at `(250, 0.00)`. Three companions are
persisted and none is published.

| cell `(nw, γ_lev)` | `share_nonconverged` | `=initialiser` | `at_lower_bound` | `at_upper_bound` |
| ------------------ | -------------------- | -------------- | ---------------- | ---------------- |
| `(250, 0.00)`      | `0.0000` (0/200)     | `0.0000`       | **`0.2900`**     | `0.0000`         |
| `(500, 0.00)`      | `0.0000` (0/200)     | `0.0000`       | `0.1800`         | `0.0000`         |
| `(1000, 0.00)`     | `0.0000` (0/200)     | `0.0000`       | `0.0600`         | `0.0050`         |
| `(2000, 0.00)`     | `0.0000` (0/200)     | `0.0000`       | `0.0100`         | `0.0000`         |
| `(250, 0.28)`      | `0.0150` (3/200)     | `0.0150`       | `0.0100`         | `0.0050`         |
| `(500, 0.28)`      | `0.0100` (2/200)     | `0.0100`       | `0.0050`         | `0.0000`         |
| `(1000, 0.28)`     | `0.0050` (1/200)     | `0.0050`       | `0.0000`         | `0.0000`         |
| `(2000, 0.28)`     | `0.0000` (0/200)     | `0.0000`       | `0.0000`         | `0.0000`         |

`share_nonconverged` and `share_equals_initialiser` coincide at every cell, which is the flag read
back: the delivered definition marks a fit unconverged **exactly** when it has been replaced by the
initialiser. The `at_lower_bound` column is the finding. It is derived **outside**
`fit_garch_qmle` — the primitive is carried byte for byte under C8 — from the returned parameters and
the box the delivered `bounds` declares, with a tolerance taken from the mechanism (the SPECS §1.10
truncation to six decimals) and not from any observed gap. The eight cells re-derive identically
from the 1600 rows of `R17_warmup_fits.csv`, checked in-run and again in the suite.

### C2 — the nature of the `ML` arm, and the sign-stream identity

**Deterministic; trigger probability 0.** Two clauses.

*What the arm is*, established by an `ast` walk and not assumed: both simulators assign the whole
innovation vector `z` **before** their variance recursion, so with `σ²_t > 0` always,
`ε_t = √σ²_t · z_t` gives `sign(ε_t) = sign(z_t)` **exactly**, and `z` is a function of the key, of
`ν` and of `n` alone. The arm reads no fitted and no true parameter.

*The identity*, asserted by SHA-256 over the monitored streams and not remarked:

| grid                                          | distinct digests | over |
| --------------------------------------------- | ---------------- | ---- |
| 3a, across the eight `Γ`                      | 1                | 8    |
| 3b at `c = 0`, across the eight `Γ`           | 1                | 8    |
| 3c, across the four `γ_lev`                   | 1                | 4    |
| 3d, across the two `γ_lev` at each `n_warmup` | 1 each           | 2    |

The run exits `1` on any other outcome. **Scope**, logged: the 3b identity holds at `c = 0` alone —
for `c > 0` the monitored stream is `(ε + c·σ_unc > 0)` and `σ_unc` carries `Γ` through `β`, so
`ADD_ML` moves along the grid while `FPR_ML` does not. The invariance of one column and the variation
of the other are the same mechanism read at two shift magnitudes.

*The three-table tension of the R17 prompt §2.3, resolved mechanically.* The witness prints
`ML = 0.065` at all eight `Γ` of 3a, `FPR_ML = 0.04` at all eight of 3b (the prompt misses this one),
`FPR_ML = 0.085` and `LB_Reject_ML = 0.055` at all four `γ_lev` of 3c, and yet `FPR_ML` **varies**
over 3d's warm-up axis. The witness key is the reason and not the arm: 3a/3b/3c hold `n = 7000`
fixed, so one draw serves the whole grid and a constant column is one measurement printed eight or
four times; 3d keys on `s*101 + nw`, which moves with the warm-up. The witness exhibits the identity
directly — its `FPR_ML` is equal at the two `γ_lev` for every warm-up (`0.075/0.075`, `0.030/0.030`,
`0.055/0.055`, `0.080/0.080`). Under the mandated key the same degeneracy holds for the same reason,
and the warm-up axis still carries four genuine draws because the vector **length** changes with
`nw`. Regenerated: `[(250, 0.100), (500, 0.095), (1000, 0.110), (2000, 0.100)]`, identical at both
`γ_lev`.

### C3 — realized penalty against target, at the eight grid points

**Bisection, 100 halvings of `[0, 0.919999]`, resolution `2⁻¹⁰⁰` of an interval below 1; trigger
probability 0.** Worst relative error over the eight points: **`2.554e-14`**, against the `1e-6`
threshold — eight orders of margin. No `β` saturates the ceiling `0.919999`.

| target   | `β`                  | `compute_gamma_exact(a_sim, b_sim)` | relative    |
| -------- | -------------------- | ----------------------------------- | ----------- |
| `1.00`   | `0.0`                | `1.0`                               | `0.000e+00` |
| `5.00`   | `0.8582264370343256` | `4.999999999999991`                 | `1.776e-15` |
| `11.58`  | `0.8889517521997994` | `11.58000000000005`                 | `4.219e-15` |
| `30.00`  | `0.9040143180471854` | `30.000000000000323`                | `1.088e-14` |
| `50.00`  | `0.9085808000511808` | `49.999999999999396`                | `1.210e-14` |
| `90.00`  | `0.9122144692891982` | `89.99999999999862`                 | `1.532e-14` |
| `140.00` | `0.9141758270445959` | `139.99999999999986`                | `9.992e-16` |
| `200.00` | `0.9154110864448526` | `199.99999999999488`                | `2.554e-14` |

**At `Γ = 1.00` the check is run on `(a_sim, b_sim) = (0, 0)`, the parameters actually simulated.**
At `α = 0.08` the value `Γ = 1` is unattainable inside the GARCH family
(`compute_gamma_exact(0.08, 0) = 1.1739`); the delivered script reaches it by leaving the family.
This is the structure `R11-gamma-grid-floor` already registers; it is cross-referenced, not
duplicated, and opens no second entry.

The suite re-derives the same table by a **second arithmetic route**: it solves for `β` with an
independently written bisection driven by the autocorrelation **series** of `ε²` summed over 4000
lags, where the experiment evaluates the closed form of the same series. The two routes agree to
`≤ 2.7e-14` relative.

### C4 — the argument order of `solve_beta_for_gamma`

**Deterministic; trigger probability 0.** The witness signature is
`solve_beta_for_gamma(alpha, target_gamma)`. All **3** call sites of this file and all **2** of the
witness carry the identical argument expressions `("Name(id='alpha')", "Name(id='gamma')")`. The
assertion is on the expressions and not merely on the arity, which is what makes it a check on the
order. Cross-reference: `R04-gamma-grid-defect`, registered **D3**, where the transposition of these
two arguments left the published `Γ` grid constant and destroyed a whole stream of this campaign.

### C5 — monotone restoration, characterised and never corrected

**Family-wise arithmetic logged before the result was read:** six consecutive-step comparisons, so
reading "no step inverts by more than two paired standard errors" as one simultaneous statement would
trigger with probability `1 − (1 − 0.0455)⁶ = 0.2423` under a null of exact equality at every step.
Nothing halts on it.

| `γ_lev` | step        | `FPR_Eco`       | paired Δ  | paired SE  | ratio    |
| ------- | ----------- | --------------- | --------- | ---------- | -------- |
| `0.00`  | 250 → 500   | `0.105 → 0.070` | `−0.0350` | `0.016439` | `−2.129` |
| `0.00`  | 500 → 1000  | `0.070 → 0.035` | `−0.0350` | `0.014832` | `−2.360` |
| `0.00`  | 1000 → 2000 | `0.035 → 0.020` | `−0.0150` | `0.013219` | `−1.135` |
| `0.28`  | 250 → 500   | `0.100 → 0.075` | `−0.0250` | `0.016530` | `−1.512` |
| `0.28`  | 500 → 1000  | `0.075 → 0.040` | `−0.0350` | `0.016439` | `−2.129` |
| `0.28`  | 1000 → 2000 | `0.040 → 0.020` | `−0.0200` | `0.012196` | `−1.640` |

**Zero inversions**, on either column. The design effect of each paired standard error is `1.0` **by
construction and not by approximation**, and it is logged in the same block as the square root that
uses it (§S4bis, sixth corollary): the pairing is *within* stream `s`, so all of the dependence the
common random numbers institute is absorbed inside the difference, and across `s` the keys are
distinct 128-bit condensates. **No gate is built on `FPR_ML`**, which is non-monotone in the witness
itself.

### C6 — the `Γ = 1` witness

**Exact identity; trigger probability 0.** At `Γ = 1.00`, `gamma_actual` is the float `1.0`, so
`65.0 * gamma_actual` and `65.0` are the **same float** and the two arms read one threshold. Both
count `4/200`. It is this witness that makes the `Uncal` column interpretable at every other point,
where the two separate (`0.515` against `0.005` at `Γ = 5`, `0.770` against `0.010` at `Γ = 200`).

### C7 — attribution, measured and not gated

**No trigger probability is quoted, and the reason is stated rather than omitted.** The entropy
migration redraws **both** arms, so the legacy arm shares no seed with the submitted campaign and
"the legacy arm reproduces the witness" is not a question this design can ask. What C7 measures is
the SPECS §1.10 displacement at a **common** draw.

| artefact                     | specs vs legacy                                                            |
| ---------------------------- | -------------------------------------------------------------------------- |
| `R17_fpr_baseline.csv`       | **bit-identical**                                                          |
| `R17_fpr_arms.csv`           | **bit-identical**                                                          |
| `R17_misspecification.csv`   | **bit-identical** (protocol 3c performs no fit at all)                     |
| `R17_warmup_sensitivity.csv` | every `FPR_Eco` and `FPR_ML` identical; medians move in the fourth decimal |
| `R17_add_baseline.csv`       | differs — `ADD` is a mean over delays, discontinuous in its stream         |
| `R17_warmup_fits.csv`        | differs — 1600 per-fit parameter vectors                                   |

Paired pricing at the published cell, on the same 200 warm-ups in one execution: median of the sum
`0.6257515` under SPECS §1.10 against `0.6258931244318199` under the delivered call, **delta
`−1.416e-4`**; mean absolute per-fit displacement `3.569e-05`, largest `1.088e-03`, over 200 fits
that moved at all. **Compliance costs a fourth decimal.**

### C8 — `ast` source identity, six byte-identical and three differential

**Deterministic; trigger probability 0 unless a copy has drifted.** Six primitives
(`compute_gamma_exact`, `solve_beta_for_gamma`, `strict_cusum`, `_garch_nll`, `filter_sigma2`,
`wilson_ci`) plus the three seed routines carried from `exp_R13_oracle_ceiling_a.py` are byte-identical
to the files that own them, **3316 characters compared**. §S4.2 forbids hoisting any of them into
`experiments/common/`, and the suite exhibits the reason: `_garch_nll`, `strict_cusum` and
`wilson_ci` all differ between this witness and R14's copies.

The three **adapted** routines cannot be byte-compared, so each carries a *differential* control that
is stronger than a visual diff: the named node is replaced by a sentinel in **both** trees and full
`ast.dump` equality is then required, which admits exactly one difference and proscribes every other
**at any depth**.

| routine            | permitted node                            | dump compared | witness node                                      | this port                            |
| ------------------ | ----------------------------------------- | ------------- | ------------------------------------------------- | ------------------------------------ |
| `simulate_garch11` | trailing argument, its default, `body[1]` | 3882 chars    | `seed`, `42`, `rng = np.random.default_rng(seed)` | `loc_rng`, `None`, `rng = loc_rng`   |
| `simulate_gjr11`   | idem                                      | 4453 chars    | idem                                              | idem                                 |
| `fit_garch_qmle`   | the single optimiser `Call` node          | 3924 chars    | `minimize(_garch_nll, init, …)`                   | `qmle_minimize(_garch_nll, init, …)` |

Each witness segment is quoted in full in the log **after** an §S4.4 grep on the segment returns
empty, per §S4.2; the five superseded routines (`protocol_3a`, `protocol_3b`, `protocol_3c`,
`protocol_3d_warmup_sensitivity`, `generate_figure`) are pinned by SHA-256 and **not** quoted, so no
proscribed wording enters by transcription. The witness's `__main__` is not a `FunctionDef` and
carries no segment digest; what replaces it is named in the log.

**The one `except Exception` this port carries verbatim is not silent.** `fit_garch_qmle`'s fallback
is the witness's and cannot be edited without breaking the differential control, so the logging is
placed in the adapted node instead: `qmle_minimize` catches the optimiser exception, logs it and
**re-raises**, so the carried handler runs exactly as written and preamble §S7's ban on an unlogged
handler is discharged. §S4.3 is satisfied by **recording** every fallback per fit — `converged`,
`equals_initialiser`, `at_lower_bound`, `at_upper_bound` in `R17_warmup_fits.csv` — and not by
halting on one, because here the fallback is the estimator's measured behaviour and not an
infrastructure failure. R14's "assert `conv is True` and stop" does not transfer for that reason.

### C9 — two consecutive executions, SHA-256 identical

**The prompt's "different worker counts" clause is declared NON-APPLICABLE, with its reason.** This
script creates no process pool, no thread pool and no worker; it is serial, and its primitives are
Python loops under an `ast` identity constraint. The clause has no referent. What is performed
instead is two consecutive executions of **each** arm with SHA-256 compared on every output, per
preamble §S2. Both digest sets are in §7 below.

### Every multi-test control logs `1 − (1 − p)^m` before its result is read

| control                                       | `m` | trigger probability under its own null |
| --------------------------------------------- | --- | -------------------------------------- |
| four sign-arm cell intervals                  | 4   | `1 − 0.95⁴ = 0.1855`                   |
| six consecutive-step monotonicity comparisons | 6   | `1 − (1 − 0.0455)⁶ = 0.2423`           |

Neither is used as a binary gate. The only quantity that halts the run is a falsified qualitative
claim of L341, and none is.

---

## 4. Deviation classification against v87

### The complete D0–D3 table, with the source cell of every value

| v87 numeral (L341)                | printed | witness  | regenerated | source cell                                                              | class                                                                                                           |
| --------------------------------- | ------- | -------- | ----------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| true persistence `α+β`            | `0.85`  | `0.85`   | `0.85`      | `ALPHA_DGP + BETA_DGP`, by design                                        | **D0**                                                                                                          |
| median `α̂+β̂` at `n = 250`         | `0.62`  | `0.6212` | `0.6258`    | `R17_warmup_sensitivity.csv`, `(250, 0.00)`, `persistence_median_pooled` | **D2**                                                                                                          |
| FPR at `n = 250`                  | `9.5 %` | `9.5 %`  | `10.5 %`    | same cell, `FPR_Eco`                                                     | **D2**                                                                                                          |
| restored level at `n = 500`       | `3.0 %` | `3.0 %`  | `7.0 %`     | `(500, 0.00)`, `FPR_Eco`                                                 | **D2**                                                                                                          |
| sign envelope, minimum            | `3 %`   | `3 %`    | `10 %`      | `FPR_ML`, min over the four warm-up lengths                              | **D2**                                                                                                          |
| sign envelope, maximum            | `8 %`   | `8 %`    | `11 %`      | `FPR_ML`, max over the same four                                         | **D2**                                                                                                          |
| (not printed) non-convergence max | —       | `0.5 %`  | `1.5 %`     | `share_nonconverged`, `(250, 0.28)`                                      | no class — v87 prints no convergence share; the `0.5 %` is the R17 prompt's, and a prompt is not the manuscript |

The three qualitative claims of L341 were tested separately, each on its own terms, and all three
hold: the persistence collapses below the truth at `n = 250` and climbs back (`0.626`, `0.775`,
`0.841`); the rate falls with the warm-up and its `n = 500` interval covers the nominal level on both
leverage settings; the sign-arm slope's interval covers zero.

### `R17-eco-l1-arm-identity` — Class A, **D3**

Established in three quoted steps **before** classification, as the plan required; the full text is
in `docs/DEVIATIONS.md`. In summary: Table 1 (L117) defines `Eco-L1` as `ε_t/σ̂_t`, a **signed
level** monitored for a **location (1st-order)** change; `protocol_3d` monitors `(ẑ² − μ)/σ`, a
**centred square** at the `(0.5, 65.0)` operating point, which the delivered script itself names
`Eco_L2` in `protocol_3b` (l.274–276) beside a separately named and separately thresholded
`adds_eco_l1` (l.279); and `protocol_3b`'s L1 arm **cannot** produce the numeral — at 100 seeds its
rate lattice is `k/100` and `9.5 %` is unattainable, whereas `9.5 % = 19/200` is exactly
`protocol_3d`'s resolution at the `n_str = 200` of `__main__` (l.515). The governing precedent is
`R16-dating-misdescription`, classified D3: a method description the pipeline does not produce
falsifies a qualitative claim whatever the numeral does.

**The scope is the false-alarm numerals and not the persistence median.** The QMLE fit is common to
both monitors, so `α̂+β̂` is arm-agnostic. Nothing here touches `tab:isofpr_race` or
`fig:crypto_race`, where `Eco-L1` **is** the level residual and R04 and R14 measure it as such.

**This entry is static evidence and did not halt the run.** It is established from the frozen `.tex`
and the vendored witness by `ast` and by arithmetic, not from a regenerated value, so there is no
regenerated quantity to stop producing. §S3's halting rule addresses a falsification discovered *in a
measurement*; the campaign was completed and the finding is reported in full, which is the same
handling `R16-dating-misdescription` received.

### `R17-campaign-redraw` — Class A, D2, pre-classified

Pre-classified before the first run by the `R05/R07/R09/R10/R13/R14/R08-campaign-redraw`
precedents. Four printed numerals move; every qualitative claim holds. The persistence gap
decomposes into three **named** terms rather than one residual, computed on the same fits:

| term                                                           | value        |
| -------------------------------------------------------------- | ------------ |
| total gap against v87's `0.62`                                 | `+0.0057515` |
| definitional — median of the sum minus sum of marginal medians | `+0.0426575` |
| optimiser options — SPECS arm minus legacy arm, common draw    | `−0.0001416` |
| 128-bit redraw — residual                                      | `−0.0367644` |

**The definitional term is the largest, and it carries no draw.** The witness stores marginal medians
and never the median of the sum; its `0.62` is `alpha_hat_50 + beta_hat_50 = 0.047881 + 0.573349 =
0.621230`. L341 reads "a median `α̂+β̂`", which is the median **of** the sum, and pooling converged
with non-converged fits is what a practitioner obtains. The rule was fixed and logged **before** the
regenerated values were read. Both constructions, on pooled and on converged-only subsets, are
persisted side by side on both arms; none of the three companions is published.

### `R17-sign-arm-crn-degeneracy` — Class A, no severity

Ruled in advance. Full text in `docs/DEVIATIONS.md`; the mechanism, the assertion and the R12
non-transfer are in §3 above under C2.

### What does **not** reach the register

**The corner solutions the convergence flag does not see.** At `(250, 0.00)`, `29 %` of the fits sit
on the optimiser's lower bound while the flag reports no failure at all. v87 prints no convergence
share anywhere, so no printed claim is contradicted and §S8's channel 1 does not receive it. It is in
the section, in the audit, in `R17_warmup_fits.csv` per fit, and asserted in the suite so that it
cannot quietly stop being true. 
A camera-ready candidate (`R17_v87_persistence_collapse_mechanism.md`) is provided to state that a 
third of the collapse comes from this boundary mechanism.

**The scope of "restored from `n = 500` onward".** The claim survives its own falsification rule — the
Wilson interval at `n = 500` covers the nominal level on both leverage columns, in both campaigns — so
it is not falsified and the scope filter keeps it out of the register. It goes to
`R17_v87_warmup_restoration_scope.md`, header `NO DEVIATION — clarification only`.

**The resolution of the two printed numerals.** `9.5 %` is `19/200` with a Wilson interval of
`[6.2, 14.4] %`, and the `3`–`8 %` envelope is a min–max over four cells of 200 streams. True but
incomplete, not false: `R17_v87_warmup_resolution.md`, same header.

**Protocol 3c's population limit.** Whether `α_sym = α + γ_lev/2` is the QMLE pseudo-true parameter
or only a mean-matching construction is a question `AUDIT_R12.md` already poses and no measurement of
this stream decides. An unsettled question is not a contradiction.

---

## 5. Design decisions taken outside the plan

**(a) The option delta is priced inside one execution, paired.** The plan defines
`\RSeventeenQmleOptionDelta` as the specs-minus-legacy displacement of the persistence median. A
difference between two *runs* would have made the macro of the first arm depend on a file the second
arm writes, which breaks C9's bit-identity across two consecutive executions and makes the very first
run of the repository emit an incomplete table. The published cell is therefore fitted under **both**
option sets on the same 200 warm-ups inside each arm, so the macro is a paired measurement, is
identical in both `.tex` files, and reproduces in a single execution. Cost: 200 extra fits at
`n_warmup = 250`, about 2 s.

**(b) The §S4.4 vocabulary is assembled from halves in the source.** `check_source_identity` runs the
§S4.2 grep over each quoted witness segment before quoting it. Written as literals, that pattern
would make the file fail the very check it implements. The words are built from two-part tuples with
the reason stated in a comment. The alternative — rewording the rule to accommodate its own
implementation — would have been the wrong repair.

**(c) `\RSeventeenUncalFprMax` is expressly dropped.** The R17 prompt §4 mandates it. Protocol 3a's
false-alarm explosion is `fig:fpr_explosion`, which R03 owns, and the preamble forbids a macro that
encroaches on another stream's results. Every emitted macro is produced by protocol 3d. The suite
asserts the absence.

**(d) The differential `ast` control is a redaction and not a statement diff.** The plan asks for
"every statement `ast.dump`-identical except the one named node". A statement-by-statement diff is
blind to a change nested inside a statement that is itself permitted to differ. Redacting the named
node in both trees and requiring full `ast.dump` equality is strictly stronger and is what is
implemented.

**(e) `data/reference/README.md` is appended to, not restored from `HEAD`.** See §6.

**(f) The four extra columns of `R17_warmup_sensitivity.csv` keep the witness's own column names for
the witness's own quantities.** `alpha_hat_10/50/90` and `beta_hat_10/50/90` remain **pooled**, as
the delivered script computed them, so the D0–D3 comparison is like for like; the converged-only
versions carry a `_converged` suffix.

---

## 6. Findings that revise the plan's own premises

**(i) The plan's "known conflict" on `data/reference/README.md` is stale, and the safe action is the
opposite of the one it prescribes.** The plan records the file as *deleted in the working tree* and
instructs R17 to restore it from `HEAD` and append its own row. At execution time the file is
**present and modified** (`git status` reports ` M`), and the modification is a parallel instance's
R08 block: two table rows and a paragraph. Restoring from `HEAD` would have deleted that work.
R17 therefore **appended only** — three table rows and one paragraph — which is what the plan's own
governing rule says (`append rows; never rewrite others`). The collision is recorded here rather than
resolved unilaterally.

**(i-bis) `docs/DEVIATIONS.md` carries the same collision, handled the same way.** It too was already
modified in the working tree when this stream began, by a parallel instance widening the register
table's columns. R17 inserted **three rows** after the last existing row and **appended** three
sections at the end of the file; it rewrote nothing. `git diff` reports no deletion attributable to
R17 — the 35 removed lines are the parallel instance's re-formatted table header and rows, none of
which mentions R17.

**(ii) `logs/all_tests.log` was already modified before this stream started, and R17 did not touch
it.** `git diff --stat run_all.sh run_tests.sh logs/all_tests.log` is **not** empty: it reports 524
insertions and 121 deletions in `logs/all_tests.log`. The file's mtime is `2026-08-11 14:27`, more
than an hour before this stream's first write, it appears as modified in the session's opening `git
status`, and it contains no occurrence of `R17`. `run_all.sh` and `run_tests.sh` are unmodified.
The verification item is discharged for the two orchestrators and the third is a pre-existing
parallel-instance edit, reported and left alone.

**(iii) The R17 prompt §1 has two stream counts inverted, and the traced values govern.** The prompt
gives `3c: n_streams = 200` and `3d: n_streams = 1000`. The source says the opposite:
`protocol_3c` forces `n_streams = 1000 if n_streams < 1000` (l.331) and `__main__` passes
`n_str = 200` to `protocol_3d_warmup_sensitivity` (l.515). The witness arithmetic corroborates the
source and refutes the prompt: 3c's `LB_Reject_Eco = 0.068` is not a multiple of `1/200`, and 3d's
`share_nonconverged = 0.005` is **one fit in 200**, not five per thousand. Preamble §S1 makes the
script the traceable source, so `3c = 1000` and `3d = 200` were used. Raising 3d to 1000 would have
confounded three channels — redraw, §1.10, sample size — where the legacy arm is built to separate
two, and it would have made the D0–D3 comparison a comparison at unequal `n`. **This is a defect of
the prompt, not of the manuscript, so it opens no register entry.**

**(iv) The prompt's §2.3 misses one of the constant columns.** It names 3a's `ML = 0.065` and 3c's
`FPR_ML = 0.085` / `LB_Reject_ML = 0.055`, but not 3b's `FPR_ML = 0.04`, which is constant at all
eight `Γ` for the same reason. The regenerated campaign asserts all four identities.

**(v) The `3`–`8 %` of L341 is located, and it is not where the prompt §2.5 supposes.** The prompt
suggests `protocol_3b_fpr_arms`. It is `protocol_3d :: FPR_ML`, min `0.030 → 3 %`, max `0.080 →
8 %`, and "across all warm-up lengths" matches 3d's design exactly. No other column produces that
range: 3a gives `6.5 %` and 3b gives `4.0 %`, both single constants.

---

## 7. Reproducibility and the whole suite

### Environment

Python 3.12.9; `numpy==1.26.4`, `pandas==2.3.2`, `scipy==1.16.2`, `statsmodels==0.14.5`,
`pytest==9.0.3`, transcribed at run time from `importlib.metadata`. Single-threaded BLAS
(`OMP/MKL/OPENBLAS/NUMEXPR/VECLIB = 1`), `MKL_CBWR=COMPATIBLE`, `PYTHONHASHSEED=42` exported by
`run_experiment_R17.sh` and verified by the script, which exits if it is unset.

### Cost, measured and not estimated

362.2 s for the SPECS arm and 338.6 s for the legacy arm, 700.8 s per full pass, serial. The
submitted campaign ran the same four protocols in 332 s without the per-fit diagnostics, the paired
bootstrap or the option pricing.

### Witness digests, vendored under `data/reference/R17/`

```
be404a694beede6a0c5c3d53a2c2726ac9221bc247b207e12f48a66bd975d0e8  Fig10_Econometric_Baseline.png
68f713920096d01fb25a384edff404f9c742457ecc64f54e599f172d72bad7e0  Priorite_6_econometric_baseline.log
48b7f1403879286cb0a3d0720cfb7a2b3ef58ce807dd4b4e4cf77b82d25cc78b  Priorite_6_econometric_baseline.py
80449ab8d45c38f35ee8baaf3a214d1351aa7c9a78e5f3bbe72962acb8089819  protocol_3a_fpr_baseline_v2.csv
3240067c1ca55ff7d5c53642ccb58a943e21a384b9e7ef614cd77a636567a740  protocol_3b_add_baseline_v2.csv
927bbec1d314ae7b83de72f63ec7267f0eb2f460a6f4d12dcffcba545e301b7b  protocol_3b_fpr_arms.csv
4fd3004f214689e7a74a9ec9d1f8db1f6d70ecd799b939d86d041031638c8da8  protocol_3c_misspec_v2.csv
4aa3baf17951a23051ae33b5356aa9ee6286161d32a340ef4e27fc71d4d14e74  protocol_3d_warmup_sensitivity.csv
```

### Control C9, both digest sets pasted as-is

Two consecutive executions of `./run_experiment_R17.sh`, each running the SPECS arm and then
the legacy arm. Every one of the fourteen outputs is identical across the two.

**First execution:**

```
27907f6ada17ea6414670ed25fd85f7ea01b20d6fc0a5afdc1bed2a2705e8185  data/R17_add_baseline.csv
120e79cdeafb9b0fd85047af67427652fecb93ed55be36e3321769fdb9fd09d2  data/R17_add_baseline_legacy_qmle.csv
931f1494165d361b35690dc3fba99a19157e6c755aca09255324f033eadf1580  data/R17_fpr_arms.csv
931f1494165d361b35690dc3fba99a19157e6c755aca09255324f033eadf1580  data/R17_fpr_arms_legacy_qmle.csv
c266a3411c102e6fbc753f2ff26a9e6665e7e3609ed509ffd9f1a25d3bc487f1  data/R17_fpr_baseline.csv
c266a3411c102e6fbc753f2ff26a9e6665e7e3609ed509ffd9f1a25d3bc487f1  data/R17_fpr_baseline_legacy_qmle.csv
30de1e905a4e48bc87fccd23538188283ad3e6a3e7d4db31ab9329f32197538d  data/R17_misspecification.csv
30de1e905a4e48bc87fccd23538188283ad3e6a3e7d4db31ab9329f32197538d  data/R17_misspecification_legacy_qmle.csv
6fa2a782c3cf8a97bd1fdec9886f2277196ce1ae380ce70f02f52f3c54dd5ff0  data/R17_warmup_fits.csv
567a9171534fef0abc3c091845148230061184b6ff59abd564cfcb5833f7fc0e  data/R17_warmup_fits_legacy_qmle.csv
6deaf22dec59581e1a02ae35f5f4632efe30b0831bbe6be7d44d1843e12c7657  data/R17_warmup_sensitivity.csv
247f5709d5e7f2c041058d7e99a561059a700879258d838c58dceb42748860e0  data/R17_warmup_sensitivity_legacy_qmle.csv
d6895e7c82f1ea5903dd6e273d60543cf90cd6295778137cb5f034c811d59eba  tables/R17_claims.tex
10980a7679638156aa56ee2db74f76fb8bb118d00f37ea04994eb8edff044a63  tables/R17_claims_legacy_qmle.tex
```

**Second execution:**

```
27907f6ada17ea6414670ed25fd85f7ea01b20d6fc0a5afdc1bed2a2705e8185  data/R17_add_baseline.csv
120e79cdeafb9b0fd85047af67427652fecb93ed55be36e3321769fdb9fd09d2  data/R17_add_baseline_legacy_qmle.csv
931f1494165d361b35690dc3fba99a19157e6c755aca09255324f033eadf1580  data/R17_fpr_arms.csv
931f1494165d361b35690dc3fba99a19157e6c755aca09255324f033eadf1580  data/R17_fpr_arms_legacy_qmle.csv
c266a3411c102e6fbc753f2ff26a9e6665e7e3609ed509ffd9f1a25d3bc487f1  data/R17_fpr_baseline.csv
c266a3411c102e6fbc753f2ff26a9e6665e7e3609ed509ffd9f1a25d3bc487f1  data/R17_fpr_baseline_legacy_qmle.csv
30de1e905a4e48bc87fccd23538188283ad3e6a3e7d4db31ab9329f32197538d  data/R17_misspecification.csv
30de1e905a4e48bc87fccd23538188283ad3e6a3e7d4db31ab9329f32197538d  data/R17_misspecification_legacy_qmle.csv
6fa2a782c3cf8a97bd1fdec9886f2277196ce1ae380ce70f02f52f3c54dd5ff0  data/R17_warmup_fits.csv
567a9171534fef0abc3c091845148230061184b6ff59abd564cfcb5833f7fc0e  data/R17_warmup_fits_legacy_qmle.csv
6deaf22dec59581e1a02ae35f5f4632efe30b0831bbe6be7d44d1843e12c7657  data/R17_warmup_sensitivity.csv
247f5709d5e7f2c041058d7e99a561059a700879258d838c58dceb42748860e0  data/R17_warmup_sensitivity_legacy_qmle.csv
d6895e7c82f1ea5903dd6e273d60543cf90cd6295778137cb5f034c811d59eba  tables/R17_claims.tex
10980a7679638156aa56ee2db74f76fb8bb118d00f37ea04994eb8edff044a63  tables/R17_claims_legacy_qmle.tex
```

`diff` over the two digest sets is empty. The two `.tex` files differ from each other by their
header and by the four macro bodies the two option arms move; the legacy file states in its own
header that it certifies no v87 value.

### The macros this stream emits

```
% Auto-generated by exp_R17_econometric_baseline.py -- do not edit.
% THE CSV CELL BEHIND EACH MACRO. EVERY ONE OF THEM IS PRODUCED BY PROTOCOL 3D.
%   \RSeventeenTruePersistence            ALPHA_DGP + BETA_DGP of protocol 3d, by design
%   \RSeventeenMedianPersistence...       R17_warmup_sensitivity.csv, cell (250,
%                                          0.00), persistence_median_pooled
%   \RSeventeenFprEcoAtWarmup...          same file, FPR_Eco at n_warmup 250 and 500
%   \RSeventeenSignFprMin / ...Max        same file, FPR_ML, min-max over FOUR distinct
%                                          values presented in eight cells
%   \RSeventeenNonConvergedMax            same file, max of share_nonconverged
%   \RSeventeenQmleOptionDelta            the paired specs-minus-legacy displacement of
%                                          the persistence median at (250, 0.00)
% \RSeventeenSignFprMin and ...Max are EXTREMA over a grid (S4bis, fourth corollary).
%   They ship with their paired stream bootstrap envelope beside them and GATE NOTHING.
%   The envelope is a min-max over the 4 readings the warm-up axis
%   carries, 200 streams each, and NOT over the eight cells of the table:
%   the gamma_lev axis is a bit-identical copy and carries no second reading.
% \RSeventeenNonConvergedMax is emitted even when it is zero: a counter reported only
%   when it is non-zero establishes nothing about the cells where it is not (control C1).
% NO MACRO IS EMITTED FOR 1/(4 n f_z(0)^2): it is an analytic result L341 cites to van
%   der Vaart and not a measurement of this stream. NO MACRO ENCROACHES ON
%   results/R04_isofpr_race/ OR results/R03_fpr_explosion/: the R17 prompt section 4
%   mandates \RSeventeenUncalFprMax for protocol 3a's FPR explosion, and it is
%   EXPRESSLY DROPPED here because that explosion is R03's to publish.
\newcommand{\RSeventeenTruePersistence}{0.85}
\newcommand{\RSeventeenMedianPersistenceAtWarmupTwoFifty}{0.63}
\newcommand{\RSeventeenFprEcoAtWarmupTwoFifty}{10.5\%}
\newcommand{\RSeventeenFprEcoAtWarmupFiveHundred}{7.0\%}
\newcommand{\RSeventeenSignFprMin}{10\%}
\newcommand{\RSeventeenSignFprMax}{11\%}
\newcommand{\RSeventeenSignFprMinCiLow}{5.5\%}
\newcommand{\RSeventeenSignFprMinCiHigh}{13.0\%}
\newcommand{\RSeventeenSignFprMaxCiLow}{7.5\%}
\newcommand{\RSeventeenSignFprMaxCiHigh}{15.5\%}
\newcommand{\RSeventeenNonConvergedMax}{1.5\%}
\newcommand{\RSeventeenQmleOptionDelta}{-0.0001}
```

### The test suite

`pytest tests/ -v` over the whole repository: **442 passed in 113.64 s**, no failure, no skip,
no warning summary. The transcript is the concatenation of every stream's block; R17's own block
is reproduced below in full, with `-s` so that the four reporting tests print what they measured.
Nothing is elided inside it.

```
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-9.0.3, pluggy-1.6.0 -- /home/m53/miniforge3/envs/Trading/bin/python3
cachedir: .pytest_cache
rootdir: /home/m53/The-Whitening-Advantage-Experiments
plugins: anyio-4.8.0
collecting ... collected 30 items

tests/test_R17_claims.py::test_R17_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED
tests/test_R17_claims.py::test_R17_the_per_fit_table_reproduces_every_aggregate_of_the_warmup_table PASSED
tests/test_R17_claims.py::test_R17_the_lower_bound_flag_is_the_box_constraint_and_not_a_threshold PASSED
tests/test_R17_claims.py::test_R17_the_realized_penalty_matches_its_target_at_the_eight_grid_points PASSED
tests/test_R17_claims.py::test_R17_every_persisted_interval_is_a_wilson_interval_inside_the_unit_square PASSED
tests/test_R17_claims.py::test_R17_the_carried_primitives_are_byte_identical_to_the_files_that_own_them PASSED
tests/test_R17_claims.py::test_R17_the_three_adapted_routines_differ_from_the_witness_at_one_node_each PASSED
tests/test_R17_claims.py::test_R17_the_argument_order_of_solve_beta_for_gamma_is_the_witness_s_at_every_call_site PASSED
tests/test_R17_claims.py::test_R17_the_sign_stream_is_bit_identical_across_the_leverage_axis PASSED
tests/test_R17_claims.py::test_R17_the_sign_arm_is_warm_up_independent_by_an_exact_paired_test PASSED
tests/test_R17_claims.py::test_R17_the_persistence_collapse_of_L341_reproduces PASSED
tests/test_R17_claims.py::test_R17_the_false_alarm_restoration_of_L341_reproduces PASSED
tests/test_R17_claims.py::test_R17_the_published_cell_carries_corner_solutions_the_convergence_flag_does_not_see PASSED
tests/test_R17_claims.py::test_R17_the_four_numerals_of_L341_do_not_reproduce_at_their_printed_precision PASSED
tests/test_R17_claims.py::test_R17_the_definitional_gap_between_the_two_persistence_constructions_is_measured PASSED
tests/test_R17_claims.py::test_R17_the_uncalibrated_and_recalibrated_arms_coincide_at_unit_penalty PASSED
tests/test_R17_claims.py::test_R17_the_sign_arm_is_constant_wherever_the_key_omits_the_grid_coordinate PASSED
tests/test_R17_claims.py::test_R17_the_misspecification_table_is_a_control_and_not_L349 PASSED
tests/test_R17_claims.py::test_R17_the_legacy_arm_reproduces_the_deterministic_content_of_the_witness PASSED
tests/test_R17_claims.py::test_R17_the_two_option_arms_differ_only_where_the_optimiser_reaches PASSED
tests/test_R17_claims.py::test_R17_the_legacy_artefacts_declare_that_they_certify_no_published_value PASSED
tests/test_R17_claims.py::test_R17_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED
tests/test_R17_claims.py::test_R17_every_produced_text_file_ends_in_a_newline PASSED
tests/test_R17_claims.py::test_R17_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED
tests/test_R17_claims.py::test_R17_the_produced_sources_carry_no_banned_construct PASSED
tests/test_R17_claims.py::test_R17_every_square_root_of_a_sample_size_follows_a_design_effect PASSED
tests/test_R17_claims.py::test_R17_report_the_campaign_against_its_witness 
==============================================================================
R17 -- the warm-up table against the submitted campaign's witness
==============================================================================
   g_lev    nw |                    FPR_Eco |                     FPR_ML |              nonconv
               |  witness    specs   legacy |  witness    specs   legacy | witness  specs legacy
    0.00   250 |    0.095    0.105    0.105 |    0.075    0.100    0.100 |  0.000  0.000  0.000
    0.00   500 |    0.030    0.070    0.070 |    0.030    0.095    0.095 |  0.000  0.000  0.000
    0.00  1000 |    0.030    0.035    0.035 |    0.055    0.110    0.110 |  0.000  0.000  0.000
    0.00  2000 |    0.030    0.020    0.020 |    0.080    0.100    0.100 |  0.000  0.000  0.000
    0.28   250 |    0.115    0.100    0.100 |    0.075    0.100    0.100 |  0.005  0.015  0.015
    0.28   500 |    0.060    0.075    0.075 |    0.030    0.095    0.095 |  0.005  0.010  0.005
    0.28  1000 |    0.045    0.040    0.040 |    0.055    0.110    0.110 |  0.000  0.005  0.005
    0.28  2000 |    0.035    0.020    0.020 |    0.080    0.100    0.100 |  0.000  0.000  0.000
  The two arms share every draw, so what separates them is SPECS 1.10 alone; what
  separates both from the witness is the 128-bit re-keying.
==============================================================================
PASSED
tests/test_R17_claims.py::test_R17_report_the_three_term_decomposition_of_the_persistence_gap 
==============================================================================
R17 -- the persistence median, and the three terms of its gap against v87's 0.62
==============================================================================
   g_lev    nw   median of sum   sum of medians   definitional   converged only
    0.00   250        0.625752         0.583094       0.042658         0.625752
    0.00   500        0.774814         0.754273       0.020541         0.774814
    0.00  1000        0.840557         0.819636       0.020921         0.840557
    0.00  2000        0.839223         0.840935      -0.001711         0.839223
    0.28   250        0.960839         0.953259       0.007580         0.961028
    0.28   500        0.966450         0.961646       0.004805         0.967100
    0.28  1000        0.971721         0.971301       0.000420         0.971768
    0.28  2000        0.975791         0.973677       0.002115         0.975791
  At the published cell (250, 0.00): total gap against 0.62 = +0.005752
    definitional term  (median of the sum vs sum of medians) = +0.042658
    optimiser options  (specs arm vs legacy arm, common draw) = -0.000142
    128-bit redraw     (residual)                            = -0.036764
==============================================================================
PASSED
tests/test_R17_claims.py::test_R17_report_the_sign_arm_over_the_warm_up_axis 
==============================================================================
R17 -- the sign arm: four readings in eight cells, and their paired comparison
==============================================================================
  n_warmup   250: FPR_ML 0.100 [0.066, 0.149] at gamma_lev 0.00, 0.100 at gamma_lev 0.28 -- identical by construction
  n_warmup   500: FPR_ML 0.095 [0.062, 0.144] at gamma_lev 0.00, 0.095 at gamma_lev 0.28 -- identical by construction
  n_warmup  1000: FPR_ML 0.110 [0.074, 0.161] at gamma_lev 0.00, 0.110 at gamma_lev 0.28 -- identical by construction
  n_warmup  2000: FPR_ML 0.100 [0.066, 0.149] at gamma_lev 0.00, 0.100 at gamma_lev 0.28 -- identical by construction
  envelope 9.5% -- 11.0%, against v87's printed 3--8%
      250 vs   500: discordant 2 / 1, exact paired p = 1.0000
      250 vs  1000: discordant 4 / 6, exact paired p = 0.7539
      250 vs  2000: discordant 7 / 7, exact paired p = 1.0000
      500 vs  1000: discordant 2 / 5, exact paired p = 0.4531
      500 vs  2000: discordant 5 / 6, exact paired p = 1.0000
     1000 vs  2000: discordant 4 / 2, exact paired p = 0.6875
==============================================================================
PASSED
tests/test_R17_claims.py::test_R17_report_the_convergence_diagnostics_at_every_cell 
==============================================================================
R17 -- what the delivered convergence flag does and does not see (control C1)
==============================================================================
   g_lev    nw   nonconv    =init    at low   at high   median a+b
    0.00   250    0.0000   0.0000    0.2900    0.0000     0.625752
    0.00   500    0.0000   0.0000    0.1800    0.0000     0.774814
    0.00  1000    0.0000   0.0000    0.0600    0.0050     0.840557
    0.00  2000    0.0000   0.0000    0.0100    0.0000     0.839223
    0.28   250    0.0150   0.0150    0.0100    0.0050     0.960839
    0.28   500    0.0100   0.0100    0.0050    0.0000     0.966450
    0.28  1000    0.0050   0.0050    0.0000    0.0000     0.971721
    0.28  2000    0.0000   0.0000    0.0000    0.0000     0.975791
  Every share is printed at every cell, zeros included: a counter reported only when
  it is non-zero establishes nothing about the cells where it is not.
==============================================================================
PASSED

============================== 30 passed in 1.09s ==============================
```
