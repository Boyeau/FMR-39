# AUDIT — R06, empirical validity map of the whitening property (Figure 6)

Every measured block below is extracted from `logs/R06_validity_map/exp_R06_validity_map.log` or
from the captured `pytest` run. None is retyped.

**Starting state.** The bundle supplied `Priorite_7_whitening_boundary.py`, its log, the two
reference CSVs, `Fig11_Whitening_Boundary.png`, `WRAPUP_Stream_B1.md`, the normative preamble, the
FAIR specifications and `PROMPT_REPO_R06_validity_map.md`. The prompt states that the script was
already converted to FAIR format during stream B1 and must not be rebuilt: the mission is repository
restructuring, LaTeX emission, figure formatting, and a targeted audit of three named points.

**Headline.** The port is exact: `R06_gamma_grid.csv` and `R06_task_boundary.csv` are **byte-identical
to the vendored witness**, and their SHA-256 digests match the ones printed in the submitted log.
Every published quantity of Figure 6 is reproduced at D0. The three named audit points are answered
in §1. What did not survive contact with the preamble is the script's **control layer**, replaced for
three reasons given in §2, and a fourth finding — the design of panel A is **paired**, which the
submitted campaign neither declared nor priced — is documented and measured in §3.

---

## 1. The three points the prompt asks to audit

### 1.1 The argument order of `solve_beta_for_gamma` is correct

`Priorite_7_whitening_boundary.py:531` calls `solve_beta_for_gamma(alpha_fixed, gamma)` against the
signature `solve_beta_for_gamma(alpha: float, target_gamma: float)`. **The order is correct.** It is
confirmed by a deterministic identity rather than by reading: solve for the target, then evaluate the
closed form back on the solved pair.

```
Argument-order check: solve_beta_for_gamma(alpha, target_gamma) is called as
solve_beta_for_gamma(0.08, gamma), which matches the signature.
Realised penalty against target at each grid point: 1 -> beta = 0.000000 -> 1.000000, 2 -> beta =
0.732861 -> 2.000000, 5 -> beta = 0.858226 -> 5.000000, 8.16 -> beta = 0.879374 -> 8.160000, 11.58 ->
beta = 0.888952 -> 11.580000, 20 -> beta = 0.898968 -> 20.000000, 30.85 -> beta = 0.904309 ->
30.850000, 41 -> beta = 0.906997 -> 41.000000, 60 -> beta = 0.909861 -> 60.000000, 90 -> ...
Realised-penalty check (a): all 13 targets are attained to within 1e-6, so the grid genuinely spans
Gamma from 1 to 200.
```

Thirteen distinct betas for thirteen distinct targets. The transposition that pinned another stream
at a single penalty (`AUDIT_R04.md` §1) does not occur here, and the check that would have caught it
is now part of this experiment rather than a reading of the source.

One remark on the grid's first point. `Gamma = 1` runs `alpha = beta = 0`, a genuinely i.i.d. stream,
so it is a true unit penalty. This is unlike R03 and R04, where `alpha` stayed fixed and the point
labelled `Gamma = 1` was in fact an ARCH(1) process at the attainable floor of 1.105. No mislabel
here.

### 1.2 The fourth-moment boundary is now computed, and it is not the grid point next to it

The submitted script carried the kurtosis as a **default argument**, `boundary_4th_moment_beta(alpha,
kurtosis=5.0)`, with a comment naming `nu = 7`. The value is right — `3(nu-2)/(nu-4) = 3*5/3 = 5` —
but a literal cannot follow `nu`. It is computed here from `(alpha, nu)`:

```
Fourth-moment boundary: kurtosis of a standardized t_7 is 3*(nu-2)/(nu-4) = 5.000000; E[eps^4]
diverges at beta = 0.907117 for alpha = 0.08, which the closed form maps to Gamma = 41.584288. v87
prints 41.6.
```

Emitted as `\RSixFourthMomentGamma` = `41.58` and `\RSixFourthMomentBeta` = `0.9071`. Against v87's
printed `41.6` this is **D1**: the value moves below the manuscript's printing precision and nothing
published changes.

**The conflation the prompt suspected is real, and it was in the figure.** The grid contains `41`,
which brackets the boundary from below by `0.584`:

```
Fourth-moment boundary: the nearest MEASURED grid point is Gamma = 41, which is 0.584288 below the
analytic boundary 41.584288. The two are distinct and must not be conflated: the grid does not
sample the boundary. The submitted figure placed an axis tick at the boundary value and a marker at
41 on top of it, so a reader reads a measurement at a Gamma that was never run.
```

`Fig11_Whitening_Boundary.png` sets its x-ticks to `[1, 5, 20, gamma_star, 100, 200]`, so the axis
carries a tick labelled `41.6` — the analytic boundary — while the nearest plotted marker is the
`Gamma = 41` measurement, drawn essentially on top of it. A reader takes the measurement to be *at*
the moment boundary. In `fig06_validity_map.png` the ticks carry the grid alone (`1, 5, 20, 41, 100,
200`) and the boundary is a separate labelled rule, `Fourth-moment boundary (Γ = 41.58)`. No
measurement sits on it, because none was run there.

The claim v87 makes is unaffected and is supported: the binary stream is white at `Gamma = 41`, below
the boundary, and at `60, 90, 120, 160, 200`, all above it. The guarantee crosses the moment
singularity. What cannot be said is that anything was measured *at* `41.6`.

### 1.3 The median-task control covers the nominal level, and it is weakly resolved

```
Median-task control (e): binary c = 0 rejects 7/100 = 0.0700, Wilson 95% [0.034319, 0.137495],
contains 0.05: True.
Median-task control (e) RESOLUTION: at N = 100 the half-width of that interval is 5.2 percentage
points, 1.0 times the nominal level it is testing. Every true rate from 3.4% to 13.7% is compatible
with what was observed, so this control excludes very little: it is CONSISTENT WITH the median task
being white and does not confirm it. It must not be presented as a confirmation.
```

The interval contains 5%, so the control passes as specified. But its half-width equals the level it
is testing: a true rejection rate of 13.7% — nearly three times nominal — is equally compatible with
7 rejections out of 100. **This control is consistent with the median task being white; it does not
confirm it.** The test suite keeps that statement honest with an assertion that fires if the control
ever becomes sharp enough to confirm rather than merely to be consistent, at which point the prose
must be revised rather than the number.

The stronger evidence for the median task is elsewhere in this experiment: the pooled binary level
over 1,300 streams of panel A, §3.

---

## 2. The control layer of the submitted script, and why it was replaced

The prompt says the script must not be rebuilt. Its **scientific** code was not: the generator and
both task evaluators are copied character for character and the copy is verified at run time.

```
Verbatim-copy check: all 6 primitives are byte-identical to Priorite_7_whitening_boundary.py (3350
characters compared). lb_pvalue and boundary_4th_moment_beta are deliberately NOT in this set and
are adapted, each for a reason stated at its definition.
```

The set is `wilson_ci`, `gamma_exact`, `solve_beta_for_gamma`, `generate_garch`, `evaluate_sign_task`,
`evaluate_continuous_loss`. The consequence is checked rather than claimed: both regenerated tables
are byte-identical to the witness, digests included.

Its **control** code was replaced, on the preamble's precedence clause. Three defects, each of which
makes the script unable to serve as a measuring instrument.

### 2.1 The certifications were locked onto their own draw

`evaluate_empirical_certifications` holds the observed rejection rate of all 13 `Gamma` and all 5
task cells as literals and exits at `TOL = 1e-9`:

```python
expected_concept = {1.0: 0.03, 2.0: 0.07, 5.0: 0.02, 8.16: 0.06, 11.58: 0.05, 20.0: 0.02,
                    30.85: 0.05, 41.0: 0.05, 60.0: 0.03, 90.0: 0.06, 120.0: 0.03, 160.0: 0.07,
                    200.0: 0.08}
...
if abs(rej_g - exp_rate) > TOL:
    logger.error(...); sys.exit(1)
```

This is a self-certification. A single stream landing differently — a library version, a platform, a
seed — stops the script, and the only outcome it can report is the one already written into it.
Preamble §S1.2 makes the published values "la cible espérée, non une contrainte dure ... jamais de
mire à atteindre", and §S3 requires a *stricter* examination of a result that agrees with the
manuscript than of one that contradicts it. A test that can only pass by reproducing its own answer
supplies no examination at all.

Replaced in full by the controls of the prompt's §5, each anchored on a literal of v87: the pooled
level of the binary stream, the saturation of the task boundaries, the median-task control, the
realised penalty, the cardinalities. `WRAPUP_Stream_B1.md` describes these assertions as certifying
"les invariants mathématiques"; they certify a draw.

### 2.2 Thirteen per-cell gates, firing half the time under their own null

The submitted script exits if any one of the 13 per-`Gamma` Wilson intervals misses 5%:

```python
if not (low <= 0.05 <= high):
    logger.error(f"Wilson interval for Gamma={g} does not contain 0.05."); sys.exit(1)
```

Thirteen simultaneous 95% intervals miss at least once with probability `1 - 0.95^13 = 0.4867` under
their own null. §S4bis forbids exactly this door, and the prompt's control (b) already replaces it
with a pooled statement. The 13 rates are retained as description:

```
Binary stream per Gamma, descriptive and NOT a criterion: 1.0: 0.03, 2.0: 0.07, 5.0: 0.02,
8.16: 0.06, 11.58: 0.05, 20.0: 0.02, 30.85: 0.05, 41.0: 0.05, 60.0: 0.03, 90.0: 0.06, 120.0: 0.03,
160.0: 0.07, 200.0: 0.08
```

### 2.3 Three silent fallbacks, all three biased towards the thesis

| location | fallback | how it survives into the result |
| -------- | -------- | ------------------------------ |
| `lb_pvalue` | `except Exception: return np.nan` | `NaN < 0.05` is `False`, so an estimator failure is counted as a **non-rejection** |
| `lb_pvalue` | `if np.std(series) < 1e-12: return 1.0` | a degenerate stream is counted as **perfectly white** |
| `evaluate_sign_task` | `yp = ht.predict_one(x_dict) or 0` | a null prediction becomes class 0, indistinguishable in the output from a predicted 0 |

All three push the measured rate towards "white", which is the direction that supports the
proposition under test. §S4.3 proscribes a silent degraded path by name and calls it the gravest
defect of the repository. That none of them fired on this draw does not excuse them: their common
direction is the point.

Named, counted, and logged at zero as well as above it, because an absent counter and a zero counter
do not look different in a log:

```
Fallback counters. Degenerate streams mapped to p = 1.0 by the submitted script: 0 of 3100 (budget
0). Ljung-Box estimator failures mapped to NaN by its bare `except Exception`: 0 of 3100 (budget 0).
Null predictions substituted by class 0 through `predict_one(...) or 0`: 1 per sign-task stream, at
step(s) [0], 3000 in this campaign -- the tree cannot predict before it has seen an example, so this
one is structural and is reported rather than budgeted.
```

The first two now stop the run. The third is structural — a tree cannot predict before it has seen an
example — so it is measured rather than budgeted, and measured *outside* `evaluate_sign_task`, by a
probe that replays the loop, so that the function producing every published number stays byte-identical
to the witness.

### 2.4 Form

`PYTHONHASHSEED` was assigned at line 7 of the submitted script, from inside the interpreter, where it
is inert: CPython reads the hash seed at start-up. It is exported by `run_experiment_R06.sh` and
verified at start-up here. `tqdm` was dropped: a progress bar on stderr is not an output, and it was
the only use of that dependency.

---

## 3. The design of panel A is paired, and the submitted campaign did not price it

**The finding.** `generate_garch` draws the innovations *before* the variance recursion, so
`eps_t = sqrt(h_t) * z_t` with `h_t > 0` and therefore `sign(eps_t) = sign(z_t)` whatever `(alpha,
beta)`. The submitted campaign keys its streams on `seed` alone — `np.random.seed(seed)` with
`seed` in `1..100` at every `Gamma` — so **one seed carries the same label stream to all 13 grid
points**. Its own log records the consequence without drawing it: `Unique seeds: 100/1800`.

**The characterisation must stop there, and an earlier draft of this audit overstated it.** The label
stream is shared; the **error** stream is not, because the classifier reads amplitudes and therefore
`sigma_t`. Measured on the witness: 1,300 distinct `p_concept` values over 1,300 cells, and not one
seed constant across the grid. Panel A is not thirteen readings of the same thing.

**What it is, is a paired design, and its price is measurable:**

```
Paired design, declared and measured. ... the 1300 readings take 1300 distinct p-values and no seed
is constant across the grid. Mean correlation of the rejection indicator between two Gamma = 0.1747
(max 0.6564), over the 13 of 13 readings that carry any variation; Kish design effect = 3.2088;
effective sample size 405.1 of 1300.
```

The 1,300 streams carry the information of **405 independent ones**. Pairing is a legitimate choice
and a good one: it sharpens comparisons *across* `Gamma`, which is what panel A is about. What it
requires is declaration and the variance treatment it imposes. **An undeclared paired design is a
defect of analysis, not of experiment.**

**Control (b) as first specified was therefore wrong, and it was corrected before the result was
read.** A pooled Wilson interval over 1,300 streams assumes them independent and understates its
half-width by `sqrt(3.2088) = 1.79`:

```
Calibration check (b): pooled binary rejection 0.047692 (62/1300). Cluster bootstrap over 2000
replicates, resampling SEEDS and never streams: [0.029231, 0.069231], half-width 0.020000. Contains
0.05: True (GATING). The Wilson interval that assumes 1300 independent streams would read
[0.037381, 0.060669], half-width 0.011644, understating it by sqrt(design effect) = 1.7913.
```

Both intervals contain 5%, so the conclusion of panel A survives either way — but the wider one is
the correct one, and it is the one that gates. The seed is the unit of resampling: the 100 seeds are
independent of one another, the 13 readings a seed carries are not.

**The design effect is measured twice, by two routes.** The second is a counterfactual arm, keyed per
`(Gamma, stream)` on the repository's 128-bit condensate, differing from the primary campaign in the
seed and in nothing else:

```
Counterfactual arm (S4.5), independent per-cell seeds: pooled binary rejection 0.049231, interval
[0.038462, 0.061558], design effect 1.0133 against 3.2088 on the paired campaign. Two routes to the
same quantity: the design effect estimated from the paired campaign alone, and the one measured by
removing the pairing.
```

`1.0133` against `3.2088`: removing the pairing removes the design effect, which is what a design
effect means. And the binary stream holds the nominal level under independent label streams, where
pairing can mask nothing — `4.92%`, interval `[3.85%, 6.16%]`. The claim of panel A is not an artefact
of the shared labels.

The arm is persisted as `R06_gamma_grid_independent_seeds.csv`. Its seeds are the 128-bit condensate
truncated to the 32 bits `np.random.seed` accepts — forced, not chosen, since the arm must drive the
same `generate_garch` — and their uniqueness is asserted rather than assumed: `1300 distinct 32-bit
seeds over 1300 counterfactual tasks, zero collisions`.

---

## 4. Deviation classification against the submitted campaign

```
quantity                                       |  published | regenerated | degree
Pooled binary rejection over the Gamma grid    |     0.0477 |      0.0477 | D0
Pooled squared-stream rejection over the grid  |     0.9277 |      0.9277 | D0
Task boundary binary c = 0.0                   |     0.0700 |      0.0700 | D0
Task boundary binary c = 0.25                  |     0.4400 |      0.4400 | D0
Task boundary binary c = 0.5                   |     1.0000 |      1.0000 | D0
Task boundary binary c = 1.0                   |     1.0000 |      1.0000 | D0
Task boundary continuous MSE                   |     1.0000 |      1.0000 | D0
Fourth-moment boundary Gamma                   |    41.6000 |     41.5843 | D1
Witness identity: R06_gamma_grid.csv against whitening_boundary_gridA.csv: byte-identical
Witness identity: R06_task_boundary.csv against whitening_boundary_partB.csv: byte-identical
```

**No D2 and no D3.** Every claim v87 makes about Figure 6 is reproduced, and the one value that moves
does so below the manuscript's printing precision because it is now computed from `(alpha, nu)`
instead of held as a literal.

The byte-identity lines are reported and do **not** gate. `data/reference/README.md` forbids the
witness as the anchor of a blocking assertion, and preamble §S2 puts reproducibility on two runs of
*this* script. The one place they are asserted is `tests/test_R06_claims.py`, and the docstring there
states why the exception is admissible for this experiment specifically: R06 is a port, run with the
same code and the same seeds, so a difference would be an environment defect rather than a legitimate
correction.

---

## 5. Controls, with their margins

| control | statement | margin |
| ------- | --------- | ------ |
| (a) grid | 13 `Gamma`, 100 streams per configuration, `nu = 7`, 4 thresholds, 2 task types | exact |
| (a) penalty | realised `Gamma` against target at each of the 13 points | all within `1e-6` |
| (b) binary level | pooled `4.77%`, cluster bootstrap `[2.92%, 6.92%]` | contains 5%, `2.08` points of margin either side |
| (c) squared stream | pooled `92.77%`, reported without an assertion on any extremum | — |
| (d) task boundaries | `binary c = 0.5`, `binary c = 1.0`, `continuous` all at `1.00` | exact, blocking |
| (e) median control | `7/100`, Wilson `[3.43%, 13.75%]` | contains 5%; half-width `5.2` points, **weakly resolved** |
| (f) reproducibility | two runs at `-1` and at 12 workers | byte-identical |
| — | counterfactual arm, design effect | `1.0133` against `3.2088` |
| — | fallback counters | `0`, `0`, and `3000` structural |
| — | counterfactual seed uniqueness | 1300 of 1300, zero collisions |

Control (d) is blocking on a rate of exactly `1.00`, which deserves a word. The prompt argues that a
100% rate over 100 streams cannot fall through sampling noise without the effect itself having
changed, and the measured p-values support that: the cells are saturated, not marginal. The gate is
applied to the primary campaign only.

---

## 6. Reproducibility

Two consecutive runs at **different worker counts** produce byte-identical artefacts:

```
R06_gamma_grid.csv                     : b1b94011b8b94dd8fdfdbd60731da054e25ea774f6c2887e037714f709bbc744
R06_task_boundary.csv                  : 9a95701f7131e8a686a30d9293b2d439dd1bf3367ecdc536dacd20a078c1f93e
R06_gamma_grid_independent_seeds.csv   : c4fdeebc1ffebb01e54ee9717bf31ad1f0c362a890b0548826d7329e7e12a863
fig06_validity_map.png                 : 8909ad650d4969c0a47c2aebdcaa0abe3936b8d4988ae422798c6e82fa77d8fb
R06_claims.tex                         : 7572a736f24d9f27e7dcb9bedb043dd046adbf3ffccbe8c744f63615d31d7d7e
```

The first two are the digests printed in the submitted log of 2026-07-27, which is the strongest
available statement that this is a port. Verified at `--n-jobs -1` and at 12. Measured cost 33.6 s
over 3,100 monitored streams, of which 1,300 are the counterfactual arm; the submitted campaign ran
1,800 streams in 20.5 s.

`run_all.sh` and `run_tests.sh` are unmodified; `run_experiment_R06.sh` is discovered by sorted
enumeration and sorts last. The whole suite passes, 120 tests over R01 to R06:

```
tests/test_R06_claims.py::test_R06_cardinalities_and_grid PASSED
tests/test_R06_claims.py::test_R06_gamma_grid_is_realised_in_closed_form PASSED
tests/test_R06_claims.py::test_R06_fourth_moment_boundary_is_computed_not_hard_coded PASSED
tests/test_R06_claims.py::test_R06_boundary_is_not_confused_with_the_nearest_grid_point PASSED
tests/test_R06_claims.py::test_R06_panel_A_design_is_paired_and_declared PASSED
tests/test_R06_claims.py::test_R06_pooled_binary_level_covers_nominal_at_cluster_precision PASSED
tests/test_R06_claims.py::test_R06_counterfactual_arm_removes_the_pairing PASSED
tests/test_R06_claims.py::test_R06_no_per_gamma_gate_is_possible PASSED
tests/test_R06_claims.py::test_R06_squared_stream_rejects_massively PASSED
tests/test_R06_claims.py::test_R06_task_boundaries_saturate PASSED
tests/test_R06_claims.py::test_R06_intermediate_threshold_is_reported_and_labelled PASSED
tests/test_R06_claims.py::test_R06_median_task_control_covers_nominal_and_is_weakly_resolved PASSED
tests/test_R06_claims.py::test_R06_no_silent_fallback_survived_into_the_artefacts PASSED
tests/test_R06_claims.py::test_R06_reproduces_the_witness_byte_for_byte PASSED
tests/test_R06_claims.py::test_R06_macros_are_emitted_and_computed PASSED
tests/test_R06_claims.py::test_R06_report_against_the_witness PASSED
============================= 120 passed in 1.05s ==============================
```

---

## 7. Design decisions taken outside the prompt

1. **The control layer was replaced although the prompt says not to rebuild the script.** The
   preamble's precedence clause is explicit, and §2 gives the three provisions the submitted controls
   violate. The scientific code was not touched, and the byte-identity of both tables is the evidence.
2. **Control (b) carries the design effect.** The prompt specifies a pooled Wilson interval; that
   interval assumes independence the design does not have. The gate is a seed-cluster bootstrap and
   the naive interval is reported beside it, so the correction is visible rather than silent.
3. **A counterfactual arm was added** — 1,300 streams, about 15 s — to measure the design effect by a
   second route rather than estimate it once. §S4.5 asks for the counterfactual before an attribution.
4. **`binary, c = 0.25` is kept and labelled `not cited in v87`.** It is the only measurement of the
   transition between the white regime and the saturated one anywhere in this repository.
5. **`tqdm` was dropped** and its dependency with it. **`joblib` was kept**: the submitted parallel
   layer returns in submission order and changing it would have been a gratuitous divergence.
6. **The verbatim copies carry the witness's trailing whitespace.** Byte-identity is checked on the
   exact source text, so blank lines inside the copied functions keep the trailing spaces the
   submitted file has. A formatter run over this file would break the check, which is the intended
   behaviour.

## 8. Open questions

1. **Is the pairing of panel A intended?** It is a good design for comparing across `Gamma` and a
   poor one for reading each `Gamma` as an independent test of whiteness. The manuscript's caption
   says "100 independent streams per configuration", which is true within a configuration and
   misleading across them, since the same 100 label streams recur at all 13. A camera-ready revision
   should either say "100 paired streams" or cite the effective sample size. This repository does not
   edit the manuscript.
2. **The median-task control is weakly resolved at `N = 100`** and cannot be strengthened without
   more streams. Whether Figure 6 should carry a larger `N` on that cell alone is an authors'
   decision; the cost is about 4 s per additional 100 streams.
3. **The power of the Ljung-Box reading is not quantified anywhere.** `WRAPUP_Stream_B1.md` raises the
   same point: panel A measures a false-alarm rate under `H_0` and says nothing about the sensitivity
   of the same test to a real departure from whiteness. A rate at nominal is consistent with a test
   that has no power at all. Nothing in this repository measures that.
4. **`data/reference/R06/` now holds a `.py` and a `.log`**, where the other reference directories
   hold data only. The witness script is vendored because the verbatim check reads it at run time.
   Whether `data/reference/` is the right home for an executable witness is a question for the
   assembler.

Files to transmit for review: `experiments/R06_validity_map/exp_R06_validity_map.py`,
`tests/test_R06_claims.py`, `run_experiment_R06.sh`, `docs/sections/R06.md`, `requirements/R06.txt`,
`logs/R06_validity_map/exp_R06_validity_map.log`, the three CSVs, the figure and `R06_claims.tex`
under `results/R06_validity_map/`, and `data/reference/R06/`.
