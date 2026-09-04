# AUDIT — R05, scale law and location/scale orthogonality (Figure 5, Appendix B)

The submitted pipeline for this stream was four scripts — `Priorite_17_rerun_scale_gamma.py`,
`Priorite_18b_scale_add_vs_width_multigamma.py`,
`Priorite_18c_generate_fig_scale_orthogonality.py` and
`Priorite_18d_extract_appendixB_numbers.py` — none of which had been audited. This file
records what was found, what was changed, and what was deliberately left alone.

The headline is not a defect. Every number `articleB_whitening_v87.tex` prints for this stream
was recomputed from the vendored witness CSVs during the audit and **every one of them
reproduced at its printed precision**, including the analytic `Gamma ~ 7.1` moment boundary
and the `delta <= 0.8` margin. The submitted campaign is arithmetically sound. What this audit
changes is how it is seeded, how its two crossover definitions are named, and what evidence is
offered for its orthogonality claim.

---

## 1. The blocking finding: blindness and breakage were the same measurement

Proposition `prop:orthogonality` predicts that a pure scale pathology leaves the Concept
monitor at its own false-alarm rate. The submitted campaign confirms this: `DetRate_Concept`
equals `FPR_Concept_val` to within a stream or two, at every penalty, in every campaign.

The confirmation is **structurally incapable of failing**. The monitored sign stream is
`1{eps_t > 0} = 1{z_t > 0}`, a function of the innovation alone; it does not see `beta`, and
multiplying the variance by `s^2 > 0` cannot change the sign of anything. The Concept arm's
detection rate under the pathology is therefore its null rate by construction, and a monitor
that had silently stopped working — a threshold set too high, a stream wired to the wrong
array, a first-passage routine returning -1 unconditionally — would produce exactly the same
table.

This is the asymmetry rule of preamble §S4.5 in its sharpest form: the result that confirms
the manuscript deserves the harder look, and under that look it dissolves into an identity.

**Two devices were added.**

*An invariance assertion inside the drift workers.* Both `_worker_scale_drift` and
`_worker_ramp_drift` build the sign stream from the undrifted series and then assert, on every
replicate, that the drifted series would have produced the identical sign vector. It is not a
tolerance and not a statistical test: a positive multiplier cannot change a sign, so any
inequality means the pathology has leaked into the Concept branch. Cost is one vectorised
comparison per stream.

*A positive control on a fourth seed block.* One configuration at `Gamma = 11.58`, 400 seeds,
identical generator, identical calibrated `lambda_C`, identical `delta_C`, but carrying a pure
**location** shift of one unconditional standard deviation instead of a scale pathology. Its
magnitude is not tuned here: it is read off R04, which races the same sign-CUSUM family over
the same 5,000-step horizon at the same penalty and reports `DetRate = 1.0` with a conditional
delay of 42.6 steps at `c = 1.0`.

Result: **400/400 detections against 22/400 under the null, Fisher exact `p = 3.1e-203`,
conditional delay 42.9 steps** — within 0.7% of the delay R04 measures on independent
machinery. The instrument is responsive, so its silence under a scale pathology is
informative.

The blindness claim of R05 is therefore stronger than the one v87 states, which rests on the
identity alone and offers no responsiveness evidence.

### The vacuity guard

`DetRate == FPR` is also trivially true when both equal 0 or 1. The orthogonality control
refuses to report a pass unless the reference arm's hold-out level lies in `[0.01, 0.20]`, a
band taken from the attainable-level lattice of the Concept CUSUM (increments live on
multiples of `2 delta_C`, and the submitted campaigns realise between 3% and 10%) rather than
from any observed value. Outside it, the run aborts reporting degeneracy. This matters
concretely: the diagnostic arm at the literal `lambda_C = 10` saturates at long horizons, and
without the guard its saturation would have been reported as orthogonality confirmed.

---

## 2. The `lambda_C` numeral of v87 matches no campaign

v87 `sec:scaling_validation` states the Concept CUSUM was "fixed once and for all,
`lambda_C = 10`, `delta_C = 0.1`". Read in `float_precision='round_trip'`, the witnesses say
otherwise:

| Campaign                                        | `mon_len` | `lambda_star_Concept` | realised FPR |
| ----------------------------------------------- | --------- | --------------------- | ------------ |
| `protocol_17a` (abrupt)                         | 5,000     | **10.8**              | 0.095        |
| `protocol_18b` 2e5                              | 200,000   | **15.81**             | 0.0525       |
| `protocol_18b` 3e6                              | 3,000,000 | **19.02**             | 0.055        |
| `protocol_18a` (retired before submission)      | —         | **13.6**              | 0.030        |

The threshold was calibrated per horizon, exactly as the Data arm's `lambda_iid_H` was.

**What is exact in that sentence, and is preserved.** `lambda_star_Concept` is rigorously
constant *within* each campaign — one value across all thirteen penalties of the abrupt grid,
one across all sixty rows at 2e5, one across all eighty-five at 3e6 — while
`lambda_star_Data` runs from 43.9 to 847.7 on the same rows. "Fixed once and for all" is true
in the sense that carries the thesis: the Concept threshold needs **no recalibration in
`Gamma`**, where the Data arm needs one of a factor of nineteen. Only the numeral is wrong.

**Consequently control (a) was amended.** Asserting `lambda_C == 10` would fail against all
four witnesses. It is replaced by a blocking assertion that `lambda_star_Concept` is constant
across `Gamma` at fixed horizon — the testable form of the manuscript's claim — plus
`delta_C == 0.1`, which nothing contradicts, plus emission of the effective calibrated value
per campaign as computed macros.

**A finding in the manuscript's favour.** Correcting the seed derivation moves the regenerated
abrupt threshold to `lambda_star_Concept = 11.4`, which is precisely the value v87 derives
elsewhere, in "What ``exact'' means here": *"the levels bracketing 5% are 5.03% at
`lambda = 11.2` and 4.29% at `lambda = 11.4`; we take the nearest attainable level at or below
nominal, `lambda_star = 11.4`."* The submitted campaign's 10.8 was inconsistent with the
manuscript's own attainable-level analysis, and its realised level was 9.5% against a 5%
target. The corrected campaign realises 5.5%. The reseeding did not merely move a number; it
moved it onto the value the manuscript itself computes.

Parked as `docs/camera_ready_candidates/v87_lambda_c_numeral.md`.

**Not unified.** The submitted design calibrates the Concept arm to roughly 10% in the abrupt
campaign and roughly 5% in the ramp campaigns, while every Data arm targets 5%. v87 states no
Concept target. The witness's targets are kept, the discrepancy is logged, and unification is
recommended here rather than applied: changing it would move Figure 5A's annotation for a
reason no manuscript sentence requires.

---

## 3. Two crossover widths, and the one v87 prints

The submitted pipeline carries two different crossover definitions and uses each in a
different place:

- `w_delta = 2 lambda*_Data / [Delta_mu_max (1-rho)^2]`, the crossover at the threshold the
  detector actually ran with — used by `Priorite_18c` line 117 to draw the model curves and by
  `Priorite_18d` line 37 to fit the published exponents;
- `w_star = 2 lambda_iid_H Gamma / [Delta_mu_max (1-rho)^2]`, the crossover the recalibration
  rule predicts — written into the `regime` column of the CSV by `Priorite_18b` line 281.

They differ by the recalibration margin, 7-29% at the 2e5 budget, and the ramp-branch
exponents differ with them:

| `Gamma` (witness, 2e5)    | 2     | 4     | 8     | 11.58 | 20    | range               |
| ------------------------- | ----- | ----- | ----- | ----- | ----- | ------------------- |
| fit on `w >= w_delta`     | 0.710 | 0.696 | 0.683 | 0.695 | 0.653 | **0.65-0.71** ← v87 |
| fit on `regime == "ramp"` | 0.692 | 0.673 | 0.683 | 0.674 | 0.632 | 0.63-0.69           |

**The CSV's own `regime` column contradicts the appendix of the paper it supports.** R05 emits
both, under `w_star_predicted` / `regime_predicted` and `w_delta_applied` / `regime_applied`,
fits on the applied-threshold rule because that is what v87 prints, and logs the alternative
alongside every exponent it reports. The test suite reimplements both from first principles
and checks that they are genuinely distinct quantities rather than aliases.

---

## 4. Seeding: 128-bit entropy without destroying common random numbers

The submitted scripts derive seeds by integer offset — `SEED_NULL + i`, `SEED_IID + i`,
`SEED_DRIFT + i` — which violates SPECS §1.2.

The naive repair would be worse than the defect. Keying the digest on `(Gamma, w, i)` raises
the entropy of the key and **destroys the common-random-numbers design** of SPECS §1.4: the
submitted scripts feed every penalty the same innovation sequence, which is precisely what
makes a difference between two values of `Gamma` an algorithmic response rather than a
difference of draw. That property is load-bearing for this experiment and was preserved.

R05 keys the 128-bit digest on the **role and the replicate index only** — `("R05", "null", i)`,
`("R05", "iid", i)`, `("R05", "drift", i)`, `("R05", "loc", i)` — and never on `Gamma`,
`beta`, `w` or the budget. The four roles occupy disjoint key spaces because the role string
enters the digest. Each worker additionally pins `np.random.seed` and `random.seed` from a
spawned child of its own seed sequence, disjoint from the child driving its generator, so any
library sampling from global state is locked (SPECS §1.3).

**Effect on the published values.** The campaign is redrawn, so every Monte-Carlo quantity
moves. On the abrupt grid the per-cell threshold `lambda_star_Data` moves between -7.9% and
+19.4%, and `ADD_Data` moves between -12.2% and +14.4% — in lockstep, as
Proposition `prop:add_garch` requires, since `ADD ~ lambda*/d + kappa` at fixed drift. The
movement is redraw noise on a 95th percentile of 400 heavy-tailed maxima, not a change of
behaviour. Full classification in `docs/sections/R05.md`.

---

## 5. `protocol_18a`: superseded before submission, not regenerated

The R05 brief listed `R05_ramp_add_vs_width.csv` as a target output. That instruction was
withdrawn on evidence.

`protocol_18a` carries a **single** penalty, `Gamma = 11.58`, on all ten of its rows: read in
`round_trip`, its columns `lambda_star_Data`, `lambda_star_Concept`, `lambda_iid_H`, `w_star`,
`FPR_Data_val`, `FPR_Concept_val`, `DetRate_Concept`, `ADD_Concept` and `SEM_Concept` are
constant row to row, and only `w`, `regime`, `DetRate_Data`, `ADD_Data` and `SEM_Data` vary.
v87 describes the ramp campaign as "five penalties spanning `Gamma in [2, 20]`", so this file
cannot support that claim. Its generator is absent from the bundle, and `Priorite_18c` line 60
retired its design outright ("censure par horizon statique et grille absolue").

It is vendored to `data/reference/R05/superseded/`, deliberately **not** to
`data/reference/R05/`, which is defined as holding outputs of the submitted campaign; placing
it there would imply it supports a v87 claim. Its own README states the grounds. No R05 script
emits a counterpart, and `tests/test_R05_claims.py` asserts that none appears.

---

## 6. The `lambda_iid` ladder, and a number no shipped script produced

v87 `app:scaling` states the i.i.d. threshold grows `102.8 -> 129.5 -> 303.0` over
`H = 7.7e4, 2e5, 3e6`, i.e. as `H^0.24`-`H^0.31` rather than the `log H` of Siegmund's
`ARL_0` formula. The last two fall out of the two campaigns. **The 102.8 at `H = 77,000` is
produced by no script of the submitted study**: it survives only as a comment at
`Priorite_18b` line 209, an intermediate iterate of an earlier fixed-point loop. The fixed
point as shipped iterates `20,000 -> 198,768 -> 200,000` and never visits 77,000.

R05 adds `R05_lambda_iid_horizon.csv`: `Gamma = 1` exactly, the three published horizons, read
off **one** set of trajectories at three prefixes rather than three independent draws. Nesting
is then an identity of the recursion instead of a hope, and the ladder's value at each
campaign's horizon is bit-identical to that campaign's own `lambda_iid_H` — asserted, not
compared with a tolerance.

Because the three points are three prefixes of one trajectory set, they are perfectly
dependent: the log-log slope is emitted as a descriptive quantity with **no** standard error
and none is computed. A confidence interval on three nested reads of the same 400 paths would
be meaningless.

---

## 7. Control design

**No per-cell gates.** The ramp grid reaches 85 rows and the abrupt grid 13. At a 5% level,
five simultaneous cells reject with probability `1 - 0.95^5 = 22.6%` under correct
calibration, and thirteen with probability 48.7%. Preamble §S4bis therefore forbids a binary
per-cell door. The family-wise probability is computed and logged *before* the result is read,
and calibration is tested as a distribution: per-cell two-sided binomial p-values, then
Kolmogorov-Smirnov against `Uniform(0,1)`, retained as descriptive and never as an acceptance
criterion.

**Control (b) was given a consequence half.** The brief asked only that `mon_len` be constant.
But v87 justifies the common horizon by saying the null crossing probability is "identical
across `Gamma`", which is a claim about realised levels, not about a configuration value. A
chi-square homogeneity test on the five realised alarm counts was added — one aggregate test,
so §S4bis is not engaged — together with the pooled level against its 5% target.

**The horizon fixed point is clamped, and says so.** `Priorite_18b` caps the horizon at the
budget and then prints a margin computed from a stale prediction, so `SAFETY = 8` reads as
achieved when it is not. R05 recomputes the margin at the threshold the campaign will actually
use, reports the cap as binding when it binds, and states that censoring measured per cell —
not `SAFETY` — is what decides admissibility.

**Certification is on aggregates, not extrema**, for the reason recorded in R03: a gate on a
minimum over 85 cells aborts on draw noise while no claim is contradicted.

---

## 8. Control (e): what R05 can and cannot say about the sixth moment

v87 attributes the degradation of the recalibration rule to "the loss of `E[eps^6]`", locating
the boundary at `Gamma ~ 7.1` for `alpha = 0.08` and standardized `t_7`, with a margin
`delta <= 0.8` at `Gamma = 20`.

**The numerals are exactly right.** R05 recomputes them in closed form —
`E[eps^6] < infinity` iff `E[(alpha z^2 + beta)^3] < 1`, expanded by the binomial theorem over
the even moments of a unit-variance Student-t — and obtains `Gamma = 7.0793` and
`delta = 0.7931`. No Monte Carlo is involved and no draw can move them. The test suite
reimplements the cubic independently and asserts the boundary rather than classifying it.

**The attribution is not established by this experiment.** Every campaign runs `t_7`. There is
no `nu` sweep, so no output of R05 can separate "the rule degrades because a moment is lost"
from "the rule degrades with `Gamma` and with the horizon, and a moment boundary happens to
lie in the same range". The counterfactual of preamble §S4.5 has no arm to run. R05 reports
the association and asserts no mechanism. Establishing one needs an arm varying `nu` at fixed
`Gamma`, which is a different experiment.

**One gloss in v87 is wrong independently of any measurement.** `app:scaling` describes
`E[eps^6]` as "the second moment of the *monitored* statistic `eps^2`". `E[eps^6]` is the
**third** moment of `eps^2`; the second is `E[eps^4]`, whose boundary the same closed form
puts at `Gamma = 41.6`, far outside the grid. The numeral 7.1 is reproduced; the description
attached to it is not. This is a wording defect, not a numerical one, and is recorded in
`docs/sections/R05.md` rather than parked as a separate candidate.

---

## 9. Other defects of the submitted scripts

| Defect                                                                                  | Location                    | Disposition                                              |
| --------------------------------------------------------------------------------------- | --------------------------- | -------------------------------------------------------- |
| Absolute path `/home/m53/08_articleB/`                                                   | all four scripts            | replaced by `pathlib` resolution from `__file__`          |
| CSV written then reloaded to feed the next stage (SPECS §1.6)                            | `18c`, `18d`                | steps a/b/c run in one process; frames passed in memory   |
| `print` + `write_text` instead of the `logging` architecture (SPECS §4.1)                | all four scripts            | `setup_logging`, dual sink, `mode='w'`, ISO 8601          |
| No determinism bootstrap, no `PYTHONHASHSEED` check, no pandas backend disable           | all four scripts            | `fair_env` sequence, verified at start-up                 |
| `pd.read_csv` without `float_precision='round_trip'`                                     | `18c` line 59, `18d` line 29 | all reference reads are `round_trip` on both sides        |
| `df.iterrows()` (SPECS §1.9)                                                             | `Priorite_17` line 242      | vectorised comprehension                                  |
| Tolerance `abs(ratio - 1) < 0.02` not derived from a mechanism (preamble §6bis)          | `18d` line 60               | removed; the two crossovers are now named, not reconciled |
| `joblib` with implicit ordering                                                          | `17`, `18b`                 | `ProcessPoolExecutor` + `executor.map`, submission order  |
| Figure titles neither bold nor left-aligned (preamble §S6)                               | `18c` lines 94, 149         | corrected; Class C, no number moves                       |
| Docstring of `18c` still claims panel B reads `protocol_18a`, which line 60 abandoned    | `18c` lines 9-10            | dead reference; not carried forward (SPECS §2.3)          |

---

## 10. Reproducibility

Two consecutive runs of `run_experiment_R05.sh`, SHA-256 compared over every CSV, the PNG and
the macro file. Results are in `docs/sections/R05.md`.

Determinism rests on: the environment block posted before NumPy loads and **verified**, not
re-posted, by the two modules that step c imports after NumPy is already resident; seeds
carried per task so the worker count cannot change an output; reduction by `executor.map` in
submission order, never `as_completed`; workers accumulating no log state; and
`float_format='%.17g'` on every write.

---

## 11. Impact on the manuscript and next actions

No qualitative claim of v87 is contradicted by this stream. One numeral is wrong
(`lambda_C = 10`), one gloss is wrong (`E[eps^6]` as the second moment of `eps^2`), and one
published attribution is unsupported by the experiment that is cited for it (the sixth-moment
mechanism). All three are recorded; one is parked as a camera-ready candidate.

Next actions: none blocking. Files for audit are the three `exp_R05_scale_law_*.py`, the six
CSVs, `fig05_scale_law_orthogonality.png`, `R05_claims.tex`, `tests/test_R05_claims.py`,
`docs/sections/R05.md` and this file.
