# AUDIT — R04, iso-FPR race and relative efficiency (Figure 4, Table 3)

Every measured block below is extracted from `logs/R04_isofpr_race/exp_R04_isofpr_race.log` or
from the captured `pytest` run. None is retyped.

**Starting state.** The bundle supplied `Priorite_15_isofpr_dichotomy.py`, its log, five
reference CSVs, `Fig22_IsoFPR_Race.png`, the body of `tab:isofpr_race`, the normative preamble,
the FAIR specifications, `articleB_whitening_v87.tex` and `PROMPT_REPO_R04_isofpr_race.md`. No
part of R04 existed in the repository. `fair_env.py` and `fair_harness.py` in the bundle are
byte-identical to `experiments/common/`, so nothing shared moved.

**Headline.** The submitted campaign never varied `Gamma`. A transposed argument pair pinned
`beta` at 0 for every grid point, so all four labels `{1, 11.58, 50, 200}` ran the same ARCH(1)
process at `Gamma = 1.1053`. Four qualitative claims of v87 do not survive a grid that genuinely
spans, and the counterfactual reproduces the published figures when `beta` is pinned back to 0.

**Scope closure.** The project contains two homonymous functions with transposed argument orders: `Priorite_6/12/2/7/8` declare `(alpha, target_gamma)`, while `Priorite_2_run_whitening_dense_final.py` declares `(gamma_target, alpha)`. `Priorite_15_isofpr_dichotomy.py` imports the former and calls it using the latter's convention. An exhaustive grep of all 23 call sites across the project confirms this is the *only* affected script. The defect is fully isolated to R04.

---

## 1. The blocking defect: the `Gamma` grid does not span

`StreamGenerator.__init__` calls

```python
self.beta = solve_beta_for_gamma(gamma, alpha)
```

against a definition of `solve_beta_for_gamma(alpha, target_gamma)`. The arguments are
transposed, `target_gamma` receives `alpha = 0.05`, and the first line of the function,
`if target_gamma <= 1.0: return 0.0`, returns immediately.

| Target `Gamma` | `beta` produced | Realised `Gamma` | `beta` required | Realised with correct order |
| -------------- | --------------- | ---------------- | --------------- | --------------------------- |
| 1.0            | 0.000000        | 1.1053           | 0.000000        | 1.1053                      |
| 11.58          | 0.000000        | **1.1053**       | 0.930072        | 11.5800                     |
| 50.0           | 0.000000        | **1.1053**       | 0.942467        | 50.0000                     |
| 200.0          | 0.000000        | **1.1053**       | 0.946813        | 200.0000                    |

Consequences for the witness: the near-constant columns of `protocol_9b` (`lambda_star` moving
by two lattice steps over a factor of 170 in `Gamma`) and of `protocol_9e` (FPR 0.0485, 0.0485,
0.0490, 0.0485) are identities of the generator, not measurements of a detector. `Table 3` is
captioned `Gamma ~ 11.6` and was produced at `Gamma = 1.105`.

This repository solves `beta` with the documented argument order and **verifies the realised
penalty against the target before measuring**. The check is a deterministic identity — solve for
a target, evaluate the closed form back on the solved pair — so it has no probability of firing
under any null, and it would have caught the defect on the first run:

```
Gamma grid check: at alpha = 0.05 the attainable floor is Gamma(alpha, beta=0) = 1.105263;
target 1.0 -> beta = 0.000000 -> realised 1.1053, target 11.58 -> beta = 0.930072 -> realised 11.5800,
target 50.0 -> beta = 0.942467 -> realised 50.0000, target 200.0 -> beta = 0.946813 -> realised 200.0000
```

### The counterfactual (preamble §S4.5)

The attribution is measured, not asserted. Pinning `beta` back to 0 on the same seeds, changing
nothing else:

```
Counterfactual (S4.5) on the efficiency crossing: with beta pinned to 0, as the submitted
generator produced it, and the same seeds, nu*(Eco-L1) = 4.9482, nu*(Oracle) = 4.7134,
estimation cost = 0.2348. On the genuinely spanned grid the same quantities are 8.5180, 4.4659
and 4.0520. v87 prints 4.9, 4.6 and 0.3.
```

```
M4 counterfactual (beta pinned to 0): Gamma=1.0: CUSUM FPR=0.0670, Gamma=11.58: 0.0570,
Gamma=50.0: 0.0630, Gamma=200.0: 0.0650; spread = 0.010000.
```

The published `4.9`, `4.6`, `0.3` and the flat family control are recovered by the degraded
generator and by it alone. The discrepancy is located in the submitted script, not in this
reimplementation.

---

## 2. Qualitative register

Transcribed from the log. `CONFIRMED` means the printed value is reproduced at its printing
precision, `D2` that the value moved while the assertion it supports still holds, `D3` that the
assertion itself is falsified.

```
claim of v87                                         | published        | regenerated                            | verdict
Recalib runs 2 to 19x behind the first-order arms    | 2 to 19x         | 7 to 81x                               | D3 FALSIFIED
Recalib blind zone persists even at the lowest Gamma | collapse present | DetRate 0.1790 at Gamma = 1.1053       | CONFIRMED
efficiency ratio crosses unity at nu* ~ 4.9          | 4.9              | (7, 30)                                | D3 FALSIFIED
oracle arm crosses unity at 4.6                      | 4.6              | 4.47                                   | D2
finite warm-up costs 0.3 degrees of freedom          | 0.3              | undefined                              | D3 FALSIFIED
parametric route is 1.66x faster at c = 1            | 1.66x            | 1.38x                                  | D2
ratio never exceeds the Gaussian ceiling pi/2        | <= 1.5708        | max 1.2006                             | CONFIRMED
ratio is monotone increasing in nu                   | monotone         | min diff +0.0724                       | CONFIRMED
Concept threshold is flat in Gamma                   | [10.6, 10.7]     | [10.50, 10.74], homogeneity p = 0.260  | D2
blind-zone onset c* ~ 0.43                           | 0.43             | 0.4321                                 | CONFIRMED
family control: both levels flat in Gamma            | CUSUM ~0.05, ADWIN ~0.006 flat | CUSUM 0.3609 spread 0.4905 | D3 FALSIFIED
```

**Qualification of the `nu*` crossing D3:** The measured grid runs `nu` in `{3, 4, 4.5, 5, 7, 30}`. The regenerated crossing falls strictly between 7 and 30, a gap of 23 units without a single measurement point. The preliminary figure `8.52` was a linear interpolation over this void on a highly non-linear curve ($1/(4f_z(0)^2)$), and must not be published as a measurement. The falsification holds because 4.9 is explicitly outside this bracket (hence D3 on the localization), but the exact crossing value and the resulting estimation cost are indeterminate. A dedicated `R04b` sweep is required to resolve it.

**The four D3 verdicts share one mechanism.** At `Gamma = 1.105` a 500-step warm-up identifies a
nearly i.i.d. process almost exactly, so `Eco_L1` performs like the oracle and estimation is
almost free. At the `Gamma = 11.58` v87 claims to be running at, the warm-up must identify a
persistent GARCH from 500 observations; `Eco_L1` degrades, its delay rises, the ratio
`ADD_Concept / ADD_Eco_L1` falls at every `nu`, and the crossing moves up. The estimation cost
of the parametric route grows with the persistence of the volatility process, and v87 reports
the value it takes where there is almost no persistence to estimate.

**The whitening-side claims are unaffected**, and two of them stand on firmer ground here than
in the submitted campaign, because they are now measured on a grid that varies:

```
Concept invariance check (d): at the common threshold lambda = 10.621107, false-alarm counts
across the Gamma grid are Gamma=1.0: 89/2000, Gamma=11.58: 103/2000, Gamma=50.0: 117/2000,
Gamma=200.0: 103/2000; chi-square homogeneity = 4.0125, p = 0.2601.
```

---

## 3. Deviation classification against the submitted campaign

Read from the vendored witness with `float_precision='round_trip'` on both sides, at the
printing precision of v87.

```
quantity                               |    published |  regenerated | degree
Table 3 ADD Recalib at c = 0.25        |  2293.457219 |  2746.329897 |     D2
Table 3 ADD Eco-L1 at c = 0.25         |   389.309500 |   409.219500 |     D2
Table 3 ADD Concept at c = 0.25        |   460.290000 |   381.935500 |     D2
Table 3 ADD Recalib at c = 0.5         |  1336.727426 |  2622.018789 |     D2
Table 3 ADD Eco-L1 at c = 0.5          |    72.002000 |    77.128500 |     D2
Table 3 ADD Concept at c = 0.5         |   100.639000 |    96.859500 |     D2
Table 3 ADD Recalib at c = 1.0         |   202.627814 |  1986.673764 |     D2
Table 3 ADD Eco-L1 at c = 1.0          |    26.393500 |    30.886500 |     D2
Table 3 ADD Concept at c = 1.0         |    43.831500 |    42.628500 |     D2
Table 3 ADD Recalib at c = 2.0         |    55.909000 |  1311.240964 |     D2
Table 3 ADD Eco-L1 at c = 2.0          |    12.579000 |    16.096000 |     D2
Table 3 ADD Concept at c = 2.0         |    28.881500 |    28.572000 |     D2
Table 3 DetRate Recalib at c = 0.25    |     0.187000 |     0.097000 |     D2
Table 3 DetRate Recalib at c = 0.5     |     0.891500 |     0.239500 |     D2
Efficiency ratio at nu = 3.0           |     0.407263 |     0.331177 |     D2
Efficiency ratio at nu = 4.0           |     0.778229 |     0.622199 |     D2
Efficiency ratio at nu = 4.5           |     0.921953 |     0.694563 |     D2
Efficiency ratio at nu = 5.0           |     1.022764 |     0.788887 |     D2
Efficiency ratio at nu = 7.0           |     1.236853 |     0.985825 |     D2
Efficiency ratio at nu = 30.0          |     1.489896 |     1.200608 |     D2
Concept lambda* minimum over Gamma     |    10.621107 |    10.499036 |     D2
Concept lambda* maximum over Gamma     |    10.743177 |    10.743177 |     D0
M0 constant-threshold FPR              |     0.075000 |     0.077200 |     D2
Family control CUSUM mean FPR          |     0.048625 |     0.360875 |     D2
Family control ADWIN mean FPR          |     0.005750 |     0.107250 |     D2
```

The Concept arm is the one that barely moves — its maximum threshold is bit-identical to the
witness — which is what the Whitening theorem predicts and what the `Gamma` defect could not
disturb, since the sign stream is insensitive to the volatility path either way. The Recalib and
Eco-L1 columns move by factors, and those are the columns the defect governs.

---

## 4. Other defects of the submitted script

**Seed derivation (A2).** Seeds were 32-bit sequential integers built by arithmetic on the
parameters, `20000*int(gamma) + int(c*100)`, which truncates — `Gamma = 11.58` and
`Gamma = 11.99` map to the same key — and whose blocks overlap: at each `Gamma` the four `c`
values start 25, 50, 100 and 200 apart with 2000 consecutive seeds each, so they share about 90%
of their pool, misaligned. The six `nu` points of M3 share 1730 of 2000; the four `Gamma` points
of M4 share 1801 of 2000 *with identical innovations*. Replaced by a 128-bit MD5 condensate of
the semantic coordinates, injected as a scalar integer, with a blocking uniqueness assertion:

```
Seed uniqueness check (A2): 84000 distinct 128-bit seeds over 84000 tasks, zero collisions.
```

Common random numbers are deliberately **not** used across `Gamma` or `c`. The claims under test
are invariance claims, and sharing innovations across `Gamma` would make the sign stream
identical by construction, turning the Concept control into an identity rather than a
measurement.

**The QMLE guard discards its best fits.** `_generate_one` reverts to
`(alpha, beta) = (0.05, 0.90)` whenever `a + b >= 0.999`. That predicate does not test
stationarity — `0.999 < 1` — it re-tests the optimiser's own feasibility constraint,
`a + b <= 0.999`, with a strict inequality, and so rejects precisely the boundary SLSQP is
entitled to return. It fires where the true persistence is highest: **1.07% of warm-ups
overall, 5.3% at `Gamma = 200`**. Those streams were monitored under a materially different
volatility model, silently and uncounted.

Diagnosed rather than assumed: over 1600 instrumented fits SLSQP reported success on every one
and never landed on its own initial point, so nothing was failing to converge.

This repository tests stationarity, keeps the boundary fits, projects a genuine constraint
violation back onto the feasible boundary along its own ray instead of substituting a default,
and retries from a fixed three-point ladder when SLSQP does fail. Result:

```
QMLE non-convergence: 0 of 64000 fitted warm-ups (0.0000%) failed on all 3 starts of the
multistart ladder and reverted to (alpha, beta) = (0.05, 0.9); budget 0.5%.
QMLE stationarity guard: 0 of 64000 (0.0000%); budget 0%.
QMLE constraint boundary: 699 of 64000 warm-ups (1.0922%) returned alpha + beta >= 0.999 ... KEPT here.
```

No Eco-L1 or Oracle number in this campaign rests on a substituted model.

**The ADWIN arm was never calibrated.** `calibrate_nominal()` searches `delta = 10^-x` over
`x` in `[0.1, 10]`, i.e. `delta <= 0.794`. Measured directly: at that loosest reachable value the
detector's i.i.d. rate over 5000 steps is 0.5%; 5% would need `delta ~ 2.5`, outside the
admissible `(0,1)` of a confidence parameter. The search saturates at its boundary, never meets
its tolerance, and returns the last midpoint tried — and `best_delta` was assigned on every
iteration *before* the tolerance test, so the failure was silent. The same search is retained so
the threshold stays comparable, but the ceiling is logged, emitted as
`\RFourAdwinAttainableFpr` (**0.7%**, against the 5% target), and the arm is marked
`iso_fpr_calibrated = False` in the CSV.

**Conditional means reported as ADD.** `np.mean(adds)` averages only the streams that alarmed
inside the horizon. Renamed `ADD_conditional` and accompanied on every row by `DetRate`,
`n_detected`, `n_censored` and `horizon`. The artefact is real: at `Gamma = 200` the Recalib
conditional mean *rises* from 2804.6 at `c = 0.25` to 2842.6 at `c = 0.5`, because the larger
drift admits streams that were previously censored and those are the slow ones.

**A CSV round-trip used as a memory bridge.** `generate_figure()` re-read `protocol_9c` and
`protocol_9d` from disk to plot them. Figure 4 is drawn from the in-memory frames.

**Fabricated column.** `n_bisection_iter: 15` was written on every row regardless of early
termination. The column now records the iterations actually consumed, which range from 1 to 13.

**Form.** `PYTHONHASHSEED` set to `"0"` from inside the interpreter (inert, and the wrong
value); `logging.basicConfig` without a stdout handler and without `mode='w'`, so the shipped
log holds two concatenated runs — SPECS §4.1 proscribes it by name; legacy global seeding;
`mp.Pool` instead of `ProcessPoolExecutor`; CSVs written into a directory named `figures/`; no
`float_format`, no SHA-256, no version logging, no specification check; figure titles neither
bold nor panel-lettered; confirmatory comments ("Flawless dynamic unpacking", "perfectly
replicate").

**One suspicion investigated and dismissed.** The oracle arm filters its variance path from the
pre-shift series while `Eco_L1` filters from the observed one, which reads as an advantage
granted to the oracle. It is not. The GARCH recursion is driven by the innovations, not by the
returns, so a location shift added to the returns leaves the latent variance path untouched and
the pre-shift filtration *is* the true `sigma_t`. The implementation is kept verbatim.

---

## 5. Control design

**What was kept blocking.** Cardinalities; the realised-`Gamma` identity; the equivalence of the
memoised bisection with `strict_cusum`; seed uniqueness; the QMLE budgets; the in-sample
calibration check; the ordering of Recalib against both first-order arms; monotonicity of the
efficiency ratio in `nu`; the Gaussian ceiling; the existence of both crossings. None of these
is a hypothesis test on a draw: each is a deterministic identity, a convergence check, or a
structural ordering.

**Control (c) is in-sample, and that is why it is admissible.** The bisection selects
`lambda*` on the very null set whose rate it reports, so the gate fires if and only if the
bisection failed to converge. It has no probability of firing under a null and falls outside the
multiple-testing rule of §S4bis. A held-out level would turn it into 16 simultaneous binomial
tests whose family-wise firing probability under `H_0` is 0.56 — a coin flip, and an invitation
to re-draw.

**Control (d) was reformulated, and the reason is structural.** The prompt asks
`lambda_C*` to lie in `[10.5, 10.8]` at all four `Gamma`. The bisection halves `[0.001, 1000]`,
so `lambda*` lives on a lattice of step `0.122` at the depth reached; the published band
`[10.6, 10.7]` is *narrower than one lattice cell* and the admissible band spans barely two. A
containment gate therefore tests which cell an empirical quantile fell into and fires with
substantial probability under its own null, which §S4bis forbids. The regenerated span is
`[10.499036, 10.743177]`, three adjacent lattice points, missing the band by `0.00096` — one
part in ten thousand, less than one lattice step.

What Proposition `prop:whitening` asserts is stronger and lattice-free: the sign stream is
i.i.d. Bernoulli(1/2) *exactly*, for every `Gamma`, so read at one common threshold the four
false-alarm counts are four draws from one binomial. That is the blocking gate, and it holds at
`p = 0.26`. The band is reported as a diagnostic with its lattice explanation.

**Control (g) was demoted to a reported verdict.** It asks both family levels to stay flat in
`Gamma`. They do on the submitted campaign — because that campaign ran one process at four
labels. Blocking on it would make reproducing the defect the only way to emit an artefact, which
is the mirror image of widening a tolerance until a control passes. It is computed, logged with
its counterfactual, and carries an explicit D3 verdict.

**One tolerance was investigated rather than widened.** An early revision gated QMLE fallbacks
at 1% and measured 1.0953%. Under §S6bis the response is to interrogate the mechanism, not the
threshold. The mechanism turned out to be the boundary guard described above; the guard was
wrong, and the budget was not too tight. After the correction the rate is 0.0000%.

---

## 6. Reproducibility

Two consecutive runs at **different worker counts** produce byte-identical artefacts, which
establishes determinism and invariance to `--n-jobs` in one comparison. Digests from the log:

```
R04_bernoulli_constant.csv  : 5735644c3f4d1819a6a0b98a0d1756409bf536a38178c9445c1c23ff28069ee8
R04_isofpr_calibration.csv  : 3788c496e70dd2e092e35332d55113ac1fb3fc0559d7baa01aa409463dfaa3af
R04_isofpr_race.csv         : 7a038bd628c54d663bc87681732c656222cdf8a01e1a584aa2ca2b9832404a22
R04_relative_efficiency.csv : c024cf43d6b2abf1e1ea1385f88b159cd0e06467c46d1c0647365ab042ed2b6f
R04_cusum_vs_adwin.csv      : ea54dc9d62dc474d99e8cfd8f76f8b4fe9f2ea21959d4d75cff6834a93bc809b
fig04_isofpr_race.png       : 52b8fb9619dfba284dee0f61dd66f345d6bbe94ccbe7a0ab059f3614611b187a
tab03_isofpr_race.tex       : 9847c3fb98174ea78a1b5e449dbfe901215a685aa451039d55d3c502a0b32d7b
R04_claims.tex              : eac7da6efffbb002c97ac07ca367f30ffec5d47053c83d3a2672142efaf6466e
```

Verified over two runs at 48 and at 20 workers: all eight artefacts identical.

Measured cost 225.9 s on 48 workers, 289.4 s on 20. v87 reports about 25 min on 24 cores. The campaign is not
smaller: the bisection's inner false-alarm count is memoised through the per-stream CUSUM
supremum, which answers `strict_cusum(stream, delta, lambda) != -1` at every `lambda` in one
pass. The bisection is otherwise untouched, and the equivalence is asserted at four probe
thresholds before any threshold is used.

`run_all.sh` and `run_tests.sh` are unmodified; `run_experiment_R04.sh` is discovered by sorted
enumeration and sorts last. The whole suite passes, 61 tests over R01 to R04.

---

## 7. Impact on the manuscript and next actions

`sec:magnitude`, the caption of `fig:isofpr`, `Table 3` and the estimation-cost sentence of
`sec:discussion` are all affected. Nothing in the manuscript has been touched: preamble §S4.1
forbids it, and the numbers a corrected campaign should carry are a decision for the authors,
not for this repository.

The whitening result itself is not in question. It rests on the Concept arm, whose threshold and
level are invariant in `Gamma` — and this campaign supports that more strongly than the
submitted one did, because it is the first to measure it on a grid that actually varies.

Recommended next actions:

1. Decide whether `sec:magnitude` and `fig:isofpr` should be regenerated at the `Gamma ~ 11.6`
   they claim, in which case the numbers of this repository stand, or restated at the
   `Gamma ~ 1.1` they were computed at, in which case the caption and the section text must say
   so and the `Gamma` grid of `protocol_9b`/`9e` must be withdrawn.
2. Refine the `nu` grid between 7 and 30 before quoting `\RFourNuStarMeasured`. The regenerated
   crossing falls inside that gap, so it is located above 7 but not precisely.
3. Re-examine whether the same transposed call appears in the other `Priorite_*` scripts of
   `/home/m53/08_articleB/` that build a `Gamma` grid through `StreamGenerator`. This audit
   covers R04 only.

Files to transmit for review: `experiments/R04_isofpr_race/exp_R04_isofpr_race.py`,
`tests/test_R04_claims.py`, `run_experiment_R04.sh`, `docs/sections/R04.md`,
`requirements/R04.txt`, `logs/R04_isofpr_race/exp_R04_isofpr_race.log`, the five CSVs, the
figure and the two `.tex` artefacts under `results/R04_isofpr_race/`.
