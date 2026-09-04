# AUDIT — R14, efficiency reversal on real Bitcoin

This is the only document transmitted to the orchestrator. It contains: what R14 establishes and
what it does not; the ten controls with their margins and their trigger probability under their own
null, including the one that **fired**; the complete D0–D3 classification with the source CSV cell
for every value, including one **D2**; the reproducibility evidence with both SHA-256 sets pasted
as-is and the `pytest tests/ -v` output; the design decisions taken outside the plan; the findings
that revise the plan's own premises, including a defect in the R14 prompt's §2.3; and the open
questions, left open.

R14 measures v87 Figure 16 (`fig:crypto_race`, caption L635) and every numeral of **L345**, the
paragraph that carries the efficiency reversal from the synthetic Student-`t` sweep of
Figure~`fig:isofpr`B onto a real heavy-tailed stream.

---

## 1. What R14 establishes, in one paragraph

Running the delivered iso-FPR race on the two vendored daily crypto series — 106 monthly onsets on
Bitcoin, 72 on Ethereum, `H_ref = H_det = 500` trading days, eleven drift magnitudes, both arms
bisected to a common realized false-alarm rate on real placebo windows — **every quantity v87
publishes about Bitcoin reproduces bit for bit**: the iso-FPR `4.7\%` (`5/106`), the `106` onsets,
`\hat\nu = 2.78`, the delay ratio `0.74` at `c = 0.35`, parity `1.01` at `c = 1.5` and the mean
`0.87`. The whole `Real_BTC` block of the race table matches the submitted campaign on all thirteen
shared columns with a worst difference of exactly `0`. **The quasi-Gaussian control does not**: the
128-bit re-keying redraws the `t₃₀` series outright and its three numerals move from
`0.98`–`1.14`, mean `1.06` to **`0.95`–`1.24`, mean `1.04`** — a **Class A, D2** registered as
`R14-campaign-redraw`. The qualitative claim that the control **inverts** the ordering holds, and 
the paired bootstrap interval of the regenerated mean, `[0.9793, 1.0688]`, still covers the published 
`1.06`. However, this interval contains `1` (parity): the claim of inversion rests on a point estimate 
whose 95% confidence interval enjambs parity. The statement is true of the point estimate but its 
evidential weight is weaker than formulated (this requires a clarification but no registry entry). 
On Ethereum, both self-critical statements of L345 reproduce: the recentred sign
stream fails whiteness at `p = 0.0188` and the synthetic control does not recover the light-tailed
ordering (mean ratio `0.9189`, 95 % `[0.7877, 0.9616]`, entirely below parity).

**One control fired.** C2 — the two arms of a source must realize the same false-alarm rate —
holds on the three sources whose speed comparison v87 publishes and **fails on `Real_ETH`**, where
the re-keyed dither moves the `Concept` calibration to `4/72` while `Eco` stays at `3/72`. The
handling was fixed before the run: v87 makes no delay and no ordering claim about real Ethereum, so
the source is stamped `iso_fpr_matched = False`, read by no macro, and reported. Nothing was
reseeded, retuned or re-toleranced.

---

## 2. Five things the reader must not take from this stream

**The `_legacy_seeds` artefacts certify no v87 value.** They exist to separate "the re-keying moved
panel B" from "the transcription broke panel B". They restore the delivered
`RandomState(100 / 200 / 201 / 300)` draws and nothing else, they ship under stamped names, and
their macro file says so in its own header. Nothing in the manuscript may be checked against them.

**`ADD` is conditional on detection at every cell, including the reliable ones.** `DetRate ≥ 0.9`
is not `1`. A delay average at a reliable magnitude still averages over between 90 % and 100 % of
onsets, and the direction of that selection is not signed. This is the same conditioning
`R09-add-conditioning` registers for Figure 9B. The per-cell `DetRate`, `n_detected` and the full
7 832-row per-onset table ship so that a reader can price it rather than take it on trust.

**The real Ethereum ratios are not a speed comparison.** Under the migrated draw the two arms run
at different realized false-alarm rates, so the ratio compares two detectors at two operating
points. It is persisted and printed as description only, and no macro reads it.

**The synthetic controls are a control, not a second dataset.** They are `t₃₀` GARCH(1,1) paths
matched on one moment of their real counterpart and read at the same onsets. They establish what
the same machinery does under light tails and nothing whatever about crypto markets.

**`28` of `88` unreliable cells is not a v87 numeral.** v87 prints the *rule* — hollow markers,
`DetRate < 0.9` — and no count. The count is a property of the redrawn synthetic controls; the
legacy arm returns the submitted `25`. The macro `\RFourteenUnreliableCells` exists because the R14
prompt §2.1 asks for it, not because the manuscript prints it.

---

## 3. Controls, with their margins and their trigger probabilities

**Which rows each control reads.** C1, C2 and C5 read all four sources and gate on the three whose
speed comparison v87 publishes. C3, C8 and C9 are per-source or per-cell and read everything. C4
reads the two diagnostic rows. C6, C7 and C10 read no data at all: they are static or
reproducibility controls.

### C1 — no aggregate reads a cell the caption draws hollow

Structural; **trigger probability 0**. The pairwise-reliable grid is computed once, every published
aggregate is taken over it, and the grid is then **re-derived from the persisted CSV** and compared
with the in-memory one. `28` of `88` cells carry `add_reliable == False` and none enters an
aggregate.

The rule is `both arms at DetRate ≥ 0.9` and not the delivered literal `c >= 0.35`. That the two
coincide is a statement about the **submitted** campaign and is asserted against the witness by the
test suite: on `protocol_24b_crypto_isofpr_race.csv` the derived rule selects exactly
`{0.35, 0.5, 0.6, 0.75, 1.0, 1.25, 1.5}` for `Real_BTC` and for `Synth_BTC`, seven magnitudes,
which is the length of the seven-element reference vectors the delivered `verify_invariants`
carries. That agreement is what licenses replacing the literal.

The rule is also **forced by arithmetic** rather than chosen: a ratio of two delays does not exist
where one arm does not detect. At `c = 0.25` on `Real_BTC` the `Concept` arm reaches `0.9811` and
would be drawn filled, while `Eco-L1` reaches `0.8962`; the magnitude therefore contributes no
ratio. That asymmetry is the subject of the clarification candidate.

### C2 — one realized false-alarm rate per source — **FIRED on `Real_ETH`**

Deterministic given the data; **trigger probability 0** once the draw is fixed. The scope was fixed
before the run, read clause by clause off v87: `Real_BTC` ("the sign filter leads across the
reliable range"), `Synth_BTC` ("inverts the ordering to Eco-L1-faster") and `Synth_ETH` ("the
synthetic control does not recover the light-tailed ordering at its 72 onsets") carry a published
speed comparison and stop the run if their match fails; real Ethereum carries none.

| source      | `Concept`  | `Eco`      | realized rate         | matched |
| ----------- | ---------- | ---------- | --------------------- | ------- |
| `Real_BTC`  | `5/106`    | `5/106`    | `0.04716981132075472` | yes     |
| `Synth_BTC` | `5/106`    | `5/106`    | `0.04716981132075472` | yes     |
| `Synth_ETH` | `4/72`     | `4/72`     | `0.05555555555555555` | yes     |
| `Real_ETH`  | **`4/72`** | **`3/72`** | `0.0555…` / `0.0417…` | **no**  |

**The fragility was logged before the outcome was read, and it is arithmetic, not a draw.**
`bisect_fpr` breaks when `|k/N − 0.05| ≤ 0.005`, and a realized rate can only take the values
`k/N`. At `N = 106` exactly one integer qualifies, `k = 5` — which *is* v87's `4.7\%` — so the two
BTC arms are **forced** onto the same rate by the tolerance. At `N = 72` **no** integer qualifies:
`3/72 = 4.167\%` and `4/72 = 5.556\%` straddle the band, the bisection exhausts all forty
iterations, and the submitted campaign's ETH agreement at `3/72` was an outcome of the bisection
dynamics rather than a constraint the calibration enforces. The test suite asserts that arithmetic
independently of any run.

**What was done about it: nothing to the draw.** The `Real_ETH` rows carry
`iso_fpr_matched = False`, no macro reads a speed comparison from that source, its ratio series is
logged with the caveat attached, and the audit reports it. The delivered admissibility band
survives the event by a small margin — `|0.05556 − 0.04167| = 0.013889` against the delivered
`0.015` — which is recorded here because it means the delivered script would **not** have halted
either, and would have shipped a non-iso-FPR ETH race silently.

### C3 — the QMLE fallback counters, reported even at zero

Reporting obligation, no gate on the counters themselves.

| site                           | fits | non-converged | frozen to `(0.05, 0.90)` | fallback fraction |
| ------------------------------ | ---- | ------------- | ------------------------ | ----------------- |
| recovery test (`protocol_24c`) | 20   | 0             | 0                        | `0.0000`          |
| `Real_BTC` pre-onset fits      | 106  | 0             | 0                        | `0.0000`          |
| `Real_ETH` pre-onset fits      | 72   | 0             | 0                        | `0.0000`          |
| `Synth_BTC` pre-onset fits     | 106  | 0             | 0                        | `0.0000`          |
| `Synth_ETH` pre-onset fits     | 72   | 0             | 0                        | `0.0000`          |
| whole-sample diagnostic fits   | 2    | 0             | 0                        | `0.0000`          |
| C8 non-anticipativity fits     | 8    | 0             | 0                        | `0.0000`          |

`fit_garch_qmle` is carried byte-identically, including its `except Exception` branch that returns
the `(0.05, 0.90)` initialiser with `converged = False`, so it cannot be edited without breaking
C6. **Every one of the 386 fits asserts** `converged is True` **and**
`(alpha, beta) != (0.05, 0.90)` and exits otherwise. The delivered script halts on frozen fits
inside `evaluate_arm` and `run_diagnostics`; the assertion makes the guarantee uniform and explicit
rather than a consequence of an incidental branch.

**The G2 band is a band on the instrument and its limit is stated.** The delivered gate is
`median bias < 0.05` and `fallback fraction < 0.10`. The null distribution of a median over twenty
simulations has no closed form, so **no trigger probability is quoted for it**; the gate is kept
because it guards the measuring instrument and not a published claim, and the log states before
reading it that a firing would be characterised and reported, never reconciled by reseeding
(§S4.10). Measured: median bias `0.0228`, worst `0.0911`, best `0.0072`.

### C4 — the moment condition, derived at run time from the fitted `ν̂`

Derivation, not a gate. For a Student-`t` standardized to unit variance,
`E|z|^p < ∞ ⟺ p < ν`; hence the variance exists iff `ν > 2` and the fourth moment iff `ν > 4`. The
script evaluates that one line **at the value just measured** rather than reciting a conclusion:

| asset | `ν̂`                  | variance exists | fourth moment exists |
| ----- | -------------------- | --------------- | -------------------- |
| BTC   | `2.7791143512276766` | yes             | **no**               |
| ETH   | `3.2497912498017185` | yes             | **no**               |

Consequence, logged: with `E[z⁴]` infinite, the GARCH penalty `Γ` — a functional of the
autocorrelation of `ε²`, which needs a finite fourth moment of `z` — and the `χ²` limit of a
Ljung–Box on **squared** residuals are both unjustified on the `Data` pipeline v87 contrasts
against. **Stated precisely, because the imprecise version would be wrong**: the Ljung–Box actually
computed in this stream is on the *sign* stream, which is bounded, so its own `χ²` approximation is
untouched by this. The caveat is about the `Data` pipeline, and the regime it describes is what
Figure 16 illustrates rather than a defect of the protocol.

### C5 — direction, measured and not gated

The delivered `Control (d)` reads the synthetic ratio at `min(reliable c)` and calls `sys.exit(1)`
when it is at or below `1.05`. A minimum over a grid is an extremum statistic with no sampling
distribution, which the fourth corollary of §S4bis bans outright, and the R14 prompt's own C5 says
*characterise, do not correct*. It is replaced by a measurement.

| source      | mean ratio | 95 % paired block bootstrap | below parity | interpretable |
| ----------- | ---------- | --------------------------- | ------------ | ------------- |
| `Real_BTC`  | `0.868229` | `[0.835080, 0.893661]`      | 6 of 7       | yes           |
| `Synth_BTC` | `1.041042` | `[0.979295, 1.068778]`      | 3 of 7       | yes           |
| `Synth_ETH` | `0.918920` | `[0.787652, 0.961575]`      | 6 of 7       | yes           |
| `Real_ETH`  | `0.544440` | `[0.506701, 0.555608]`      | 7 of 7       | **no — C2**   |

**Family-wise arithmetic, logged before the result was read.** Over the seven paired magnitudes of
`Real_BTC` a sign test has trigger probability `2 × 0.5⁷ = 1.5625 %` under exchangeability of the
two arms. Reading a 95 % band as a maximum over the same seven points would trigger with
probability `1 − 0.95⁷ = 30.2 %` under its own null, which is why the two extrema ship as
descriptive quantities that gate nothing.

**The bootstrap.** Paired moving-block over onsets, `B = 2000`, block `24` onsets. One resampled
index vector serves both arms and all seven magnitudes, so the pairing the common-random-numbers
design creates is preserved and the interval is an interval on the difference. The block length is
the same `24` the design effect uses and comes from the same mechanism. No replicate was dropped on
any source.

### C6 — `ast` source identity

Static; **trigger probability 0** unless a copy has drifted. Ten segments, **3 675 characters
compared, 0 differences**: `_garch_nll`, `fit_garch_qmle`, `strict_cusum`, `bilateral_delay`,
`bisect_fpr`, `wilson_ci` and `compute_onsets` against
`data/reference/R14/Priorite_24d_crypto_isofpr_race.py`, and `get_deterministic_seed`,
`seed_sequence_for` and `rng_for` against `experiments/R13_oracle_ceiling/exp_R13_oracle_ceiling_a.py`.

**The duplication is deliberate and the evidence is machine-checked.** A diff against this
repository's other copies shows `_garch_nll`, `fit_garch_qmle`, `strict_cusum` and `wilson_ci` all
differ between R14's witness and the R01/R03/R04/R04b/R11/R13 copies — R04's `fit_garch_qmle`
carries a multistart ladder and a persistence projection R14's does not, and R01's carries
`tol=1e-8`, `maxiter=1000` and a `round(·, 6)` R14's does not. Hoisting or borrowing any of them
would move published values, which is what §S4.2 forbids. The test suite asserts the *inequality*
against R01 as well as the equality against the witness, so a future convergence of the two cannot
dissolve the justification silently.

**Two routines are adapted and cannot be byte-compared**, so the witness source of each is quoted
in full in the log with its SHA-256: `generate_synthetic_garch`
(`b20144303db1b2bc0a8dfec3f04ddaf1b9cd0f4b998511ba867f45915349c9d4`), which takes an injected
generator where the witness builds a `RandomState` from a bare integer seed, and `parse_crypto_csv`
(`39436975808d724212497c69fa9dc71442b8d7d6e842528e617d51216f67f05e`), which gains
`float_precision='round_trip'`. Ten further routines are **superseded** rather than adapted and are
named in the log with the reason for each.

### C7 — two consecutive runs, identical SHA-256

Deterministic; **trigger probability 0**. Twelve artefacts, both sets in §5, `diff` empty.

### C8 — non-anticipativity, on the full pre-onset parameter vector

Structural and **tautological by slicing**; **trigger probability 0**. The delivered check compares
`mu_hat` before and after `r[onset:] += 100`. It is extended to the eight quantities the detector
actually consumes — `mu_hat`, `med_hat`, `q_hat_ref`, `omega`, `alpha`, `beta`, `eps_last`,
`s2_last` — because a leak through any one of them would be invisible to a comparison on the mean
alone. All eight are bit-identical on all four sources. The identity holds because
`r[onset − 500 : onset]` cannot reach past `onset`; it is recorded as a structural assertion that a
future reordering of the slicing cannot pass silently, and **not** as evidence of anything.

### C9 — the design effect, computed and logged before every `sqrt(n)`

Reporting obligation, mechanically enforced. `K = ⌈H_det / 21⌉ = 24` comes from the **mechanism**:
consecutive onsets are the first trading days of consecutive months, about 21 trading days apart,
and a detection window is 500 trading days, so two onsets more than 24 monthly steps apart share no
observation. §S4 rule 8 forbids reading `K` off the observed autocorrelation, and it is not.

The delivered `SEM`, `CI_low` and `CI_high` are **kept unchanged** for witness comparability and
`deff`, `deff_clamped`, `deff_lags`, `n_eff`, `SEM_design`, `CI_low_design` and `CI_high_design`
are added beside them. **No printed v87 numeral depends on either.** The figure's band is
`SEM_design`.

On the `Real_BTC` reliable grid the dependence sits almost entirely on the `Eco-L1` arm:

| `c`    | `Concept` `deff` | `Eco-L1` `deff` | `Eco-L1` `n_eff` of 106 |
| ------ | ---------------- | --------------- | ----------------------- |
| `0.35` | `1.0000`         | `1.0000`        | `106.0`                 |
| `0.75` | `1.2160`         | `1.0000`        | `106.0`                 |
| `1.00` | `1.0888`         | `2.6271`        | `40.3`                  |
| `1.25` | `1.0936`         | `4.2500`        | `24.9`                  |
| `1.50` | `1.4794`         | `6.5511`        | `16.2`                  |

At `c = 1.5` the 106 detections of the `Eco-L1` arm buy `16.2` independent readings and a naive
standard error would understate the dispersion of the mean by a factor `2.56`. **54 of the 88
cells** return a Kish sum below `1`, which would claim more independent readings than the cell
contains; each is clamped to `1.0` with its own log line. Whether those negative sums are
finite-sample noise or a genuine negative dependence is left open in §8.

A mechanical check in the test suite scans the experiment for `np.sqrt(len(…))` or `np.sqrt(n…)`
outside the module docstring and comments, and requires `design_effect(` in the twelve lines above
each. There is exactly one such division and it passes.

### C10 — the dropped global seeds are provably unconsumed

Static; **trigger probability 0**. The delivered script sets `np.random.seed(42)` and
`random.seed(42)` at module level and this port drops both, which is admissible only if no draw
consumed them. An `ast` walk over the witness establishes that **no `np.random.<distribution>` call
exists anywhere in it** — the only `np.random` members it touches are `RandomState` and `seed` —
and that it constructs exactly three `RandomState` instances. The same walk over this script
requires that no draw reach the global stream and that `np.random.RandomState` appear only inside
the three legacy-seed brokers. The test suite re-runs both walks with an independent
implementation.

### Every multi-test control logs `1 − (1 − p)^m` before its result is read

The two families of this stream are C5's sign test over `m = 7` paired magnitudes
(`2 × 0.5⁷ = 1.5625 %`) and the per-magnitude envelope read as a maximum over the same seven
(`1 − 0.95⁷ = 30.17 %`). Both are logged before the ratios are read, and the second is the reason
`\RFourteenRatioSynthMin` and `\RFourteenRatioSynthMax` gate nothing. C1, C6, C7, C8 and C10 are
structural or static and carry no null to arithmetise; C2 is deterministic once the draw is fixed;
C3, C4 and C9 are reporting obligations.

---

## 4. Deviation classification against v87

### The complete D0–D3 table, with the source cell of every value

Classification is at v87's own printing precision (§S3). "Witness" is
`data/reference/R14/protocol_24*.csv` read at `float_precision='round_trip'` by the script itself;
no reference literal is transcribed by hand.

| #   | v87 location  | printed                                                                            | source cell                                                      | witness                 | regenerated                           | class     |
| --- | ------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------- | ------------------------------------- | --------- |
| 1   | L635, L345    | `4.7\%`                                                                            | `R14_crypto_diagnostics.csv`, `BTC`, `FPR_C_real` = `FPR_E_real` | `0.04716981132075472`   | `0.04716981132075472`                 | **D0**    |
| 2   | L635, L345    | `106`                                                                              | `R14_crypto_isofpr_race.csv`, `Real_BTC`, `n_onsets`             | `106`                   | `106`                                 | **D0**    |
| 3   | L635, L345    | `2.78`                                                                             | `R14_crypto_diagnostics.csv`, `BTC`, `nu_hat`                    | `2.7791143512276766`    | `2.7791143512276766`                  | **D0**    |
| 4   | L345          | `0.74`                                                                             | race, `Real_BTC`, `c = 0.35`, `ADD` ratio                        | `0.7407126611068993`    | `0.7407126611068993`                  | **D0**    |
| 5   | L635, L345    | `1.01`                                                                             | race, `Real_BTC`, `c = 1.5`, `ADD` ratio                         | `1.0074285714285713`    | `1.0074285714285713`                  | **D0**    |
| 6   | L345          | `0.87`                                                                             | race, `Real_BTC`, mean over 7 pairwise-reliable `c`              | `0.8682292705270857`    | `0.8682292705270857`                  | **D0**    |
| 7   | L345          | `0.98`                                                                             | race, `Synth_BTC`, minimum over the same 7                       | `0.9818435754189944`    | `0.9544910179640719` → `0.95`         | **D2**    |
| 8   | L345          | `1.14`                                                                             | race, `Synth_BTC`, maximum over the same 7                       | `1.1426127128069126`    | `1.2384142067139186` → `1.24`         | **D2**    |
| 9   | L345          | `1.06`                                                                             | race, `Synth_BTC`, mean over the same 7                          | `1.0603026678597007`    | `1.041041514153539` → `1.04`          | **D2**    |
| 10  | L345          | `0.019`                                                                            | `R14_crypto_diagnostics.csv`, `ETH`, `lb_pvalue`                 | `0.018785617996181257`  | `0.018785617996181257`                | **D0**    |
| 11  | L345          | `72`                                                                               | race, `Real_ETH`, `n_onsets`                                     | `72`                    | `72`                                  | **D0**    |
| 12  | L345          | *(qualitative)* the `t₃₀` control inverts the ordering                             | race, `Synth_BTC`, mean ratio `> 1`                              | `1.0603`                | `1.0410`, 95 % `[0.9793, 1.0688]`     | **holds** |
| 13  | L345          | *(qualitative)* the sign filter leads across the reliable range                    | race, `Real_BTC`, mean ratio `< 1`                               | `0.8682`                | `0.8682`, 95 % `[0.8351, 0.8937]`     | **holds** |
| 14  | L345          | *(qualitative)* ETH's sign stream fails whiteness                                  | `R14_crypto_diagnostics.csv`, `ETH`, `lb_pvalue < 0.05`          | `0.018786`              | `0.018786`                            | **holds** |
| 15  | L345          | *(qualitative)* ETH's synthetic control does not recover the light-tailed ordering | race, `Synth_ETH`, mean ratio `< 1`                              | `0.5418` (8 magnitudes) | `0.9189` (7), 95 % `[0.7877, 0.9616]` | **holds** |
| 16  | L635          | `DetRate < 0.9` hollow                                                             | race, `add_reliable`                                             | `25` of `88`            | `28` of `88`                          | —         |
| 17  | prompt §2.4   | `Fallback_Frac` `0.0`                                                              | `R14_qmle_recovery.csv`, `Fallback_Frac`                         | `0.0`                   | `0.0`                                 | **D0**    |
| 18  | *(unprinted)* | —                                                                                  | `R14_qmle_recovery.csv`, `Median_Bias`                           | `0.033618304213452764`  | `0.022842375390446375`                | —         |

Rows 1–6, 10, 11 and 17 are **bit-identical**, not merely equal at printing precision. Rows 16 and
18 carry no severity because v87 prints neither quantity. Rows 12–15 are the four qualitative
claims and each is asserted by the test suite against the condition that would falsify it.

### `R14-campaign-redraw` — Class A, D2

The single register entry. Preamble §S6 requires migrating the delivered
`RandomState(100 / 200 / 201 / 300)` draws onto a 128-bit `SeedSequence` keyed on role and index
alone. Three numerals of the quasi-Gaussian control move at v87's printing precision (rows 7–9).

**The mechanism is established by a counterfactual that was run.** The `--legacy-seeds` arm
restores the delivered integer seeds and keeps every other change of this port — the `round_trip`
parser, the BLAS pinning, the assertion at every QMLE call site, the derived reliability rule, the
extended non-anticipativity check. It reproduces the witness on **all 88 cells** of `ADD`,
`DetRate`, `SEM`, `FPR_achieved`, `n_onsets` and `add_reliable`, and on both diagnostic rows of
`nu_hat`, `lb_pvalue`, `FPR_C_real` and `FPR_E_real`. Exactly two quantities drift in it:

| quantity                           | drift     | mechanism                                                                                                |
| ---------------------------------- | --------- | -------------------------------------------------------------------------------------------------------- |
| `lambda_star`, `Real_ETH` / `Eco`  | `7.7e-07` | the only two bisections that never break early, so `λ` is the endpoint of forty full halvings            |
| `lambda_star`, `Synth_ETH` / `Eco` | `3.4e-07` | the same                                                                                                 |
| `Var_z_hat`, both assets           | `4.7e-09` | `float_precision='round_trip'` moves the parsed returns by about one ULP, amplified by SLSQP's tolerance |

Neither perturbation changes a single delay: `ADD` moves on `0` of `88` cells in that arm. A
transcription error is therefore excluded, and the whole movement of the default arm is the
re-keying.

**Why the severity is D2 and not more.** L345's qualitative claim about panel B is that the `t₃₀`
control *inverts the ordering to* `Eco-L1`*-faster*. Its falsification condition, fixed before the
run, is that the 95 % interval of the regenerated mean lie **entirely below 1**. It is
`[0.9793, 1.0688]`, so the claim stands, and the interval additionally **covers the published
`1.06`**: the move is not distinguishable from the redraw's own noise. Note that this interval 
contains `1` (parity), which means the evidence for the inversion is statistically weak, though 
the point estimate claim remains true. Camera-ready candidate:
`docs/camera_ready_candidates/R14_v87_synthetic_control_numerals.md` 
(and a separate clarification candidate for the parity overlap).

**Three consequences of the same re-keying carry no separate severity**, because none contradicts a
printed value: the loss of the `Real_ETH` iso-FPR match (§3, C2), the unreliable-cell count moving
from `25` to `28`, and the QMLE median bias moving from `0.0336` to `0.0228`. All three are
described inside the register entry rather than given rows of their own, so that one measured
cause produces one register entry.

### What does **not** reach the register

**The undefined "reliable range".** L345 and the L635 caption both say "across the reliable range"
without defining it, while the aggregate attached to it is taken over the magnitudes at which
**both** arms reach `DetRate ≥ 0.9`. The caption defines the *marker* rule, which is per arm; the
body reports a *ratio*, which needs both. At `c = 0.25` on `Real_BTC` the `Concept` arm is drawn
filled (`DetRate = 0.9811`) while the magnitude enters no mean, because `Eco-L1` reaches `0.8962`.
The formulation is imprecise and **not false** — the pairwise rule is forced by arithmetic — so
§S8's scope filter keeps it out of `docs/DEVIATIONS.md`. It is parked as
`docs/camera_ready_candidates/R14_v87_reliable_range_scope.md` under the mandatory
`NO DEVIATION — clarification only` header, with two `RECHERCHER` blocks verified by `grep -Fc`
against the frozen `.tex` (line 345 and line 635, `1` occurrence each, disjoint from each other and
from the numerals candidate).

**The delivered script would not have halted on the ETH mismatch either.** `|0.05556 − 0.04167| =
0.013889` sits under the delivered `0.015` band, so `Control (c)` passes and the delivered pipeline
would have shipped a non-iso-FPR ETH race with no warning. That is a property of the delivered
control's design, it contradicts nothing printed, and it is reported here rather than registered.

**The delivered self-certification is anchored on literals the delivered run produced, and one of
them is now out of tolerance.** `verify_invariants` asserts
`abs(Var_z_hat − 1.0475457277090305) < 1e-9` on BTC. Under `float_precision='round_trip'` the value
moves by `4.7e-09` and that assertion would fail — on a quantity v87 does not print, at a tolerance
tighter than the reading protocol §S3 mandates warrants. This port does not reproduce that gate; it
classifies the quantity instead. Same family as the self-anchored gates `AUDIT_R10.md` and
`AUDIT_R12.md` already record. No entry.

**ETH's Ljung–Box rejection is a reproduced published claim, not a finding.** The R14 prompt §3
asks that it be reported in the audit as an observation and excluded from the camera-ready
candidates by the scope filter. It is reported (row 14) and generates no candidate. See §7 for why
its status in the prompt is nevertheless wrong.

---

## 5. Reproducibility and the whole suite

```bash
chmod +x run_experiment_R14.sh && ./run_experiment_R14.sh   # 23 s: migrated 11.8 s, legacy 11.2 s
./run_experiment_R14.sh                                     # second run, C7
./run_tests.sh
```

`run_all.sh` discovers `run_experiment_R14.sh` by sorted enumeration. **`run_all.sh`,
`run_tests.sh`, `logs/all_tests.log`, `README.md` and every `.tex`/`.bib` of the manuscript are
untouched** — `git status` and `git diff --stat` show no modification to any of them.

### C7, both digest sets pasted as-is

Run 1:

```
e598dd2d4b0d58f09d704dc65d960db9cb169d9e27bdbfc39a36815c8f629bf7  results/R14_crypto_isofpr/data/R14_crypto_diagnostics.csv
dae40d534e9f8a42b8b3cbe7147c617d238bdfcabda54b8653ce52f53e4988bc  results/R14_crypto_isofpr/data/R14_crypto_diagnostics_legacy_seeds.csv
f6d037d6e0316d3ff494459fd92debc878ec518f831bab8c20bd1f99302e681e  results/R14_crypto_isofpr/data/R14_crypto_isofpr_race.csv
46dcd8e95252fe18050665df7fb320ff2d419640e99686117411dc57aa8ae0fa  results/R14_crypto_isofpr/data/R14_crypto_isofpr_race_legacy_seeds.csv
8c763481cf351213824b7ae844fdc3cff763e7d501164c054533cd85d9214d31  results/R14_crypto_isofpr/data/R14_onset_delays.csv
b3ac6a3fac1ecc56afc4dc07709b69a3e2376150be6007f6dd29378b025efc89  results/R14_crypto_isofpr/data/R14_onset_delays_legacy_seeds.csv
671bc7377c69ed8aacf9ceb336255d15df1ef0e92d38e39fd39b804afbf574db  results/R14_crypto_isofpr/data/R14_qmle_recovery.csv
e269fbaa9c90d965cb132d4cd8ce3dc9e772ab3c7195dbe10b99f7102fc2019b  results/R14_crypto_isofpr/data/R14_qmle_recovery_legacy_seeds.csv
96d3c9f381c4f91aafb52456df207f08769f4b3a914a2e3b8f8830cfc8f7187d  results/R14_crypto_isofpr/figures/fig16_crypto_race.png
69965f7ef2069591439c5c482b2dfb434dec0a599f2a753a845f92bb44d31bb6  results/R14_crypto_isofpr/figures/fig16_crypto_race_legacy_seeds.png
2fe6fd0a43004c72e46b2f8f6397bfa39cc220cd98c102a2f4b2d3679a257544  results/R14_crypto_isofpr/tables/R14_claims.tex
08a8b822f9af3df720ea97708de9be2994a044251428c86d8e06f57eef82b2ae  results/R14_crypto_isofpr/tables/R14_claims_legacy_seeds.tex
```

Run 2:

```
e598dd2d4b0d58f09d704dc65d960db9cb169d9e27bdbfc39a36815c8f629bf7  results/R14_crypto_isofpr/data/R14_crypto_diagnostics.csv
dae40d534e9f8a42b8b3cbe7147c617d238bdfcabda54b8653ce52f53e4988bc  results/R14_crypto_isofpr/data/R14_crypto_diagnostics_legacy_seeds.csv
f6d037d6e0316d3ff494459fd92debc878ec518f831bab8c20bd1f99302e681e  results/R14_crypto_isofpr/data/R14_crypto_isofpr_race.csv
46dcd8e95252fe18050665df7fb320ff2d419640e99686117411dc57aa8ae0fa  results/R14_crypto_isofpr/data/R14_crypto_isofpr_race_legacy_seeds.csv
8c763481cf351213824b7ae844fdc3cff763e7d501164c054533cd85d9214d31  results/R14_crypto_isofpr/data/R14_onset_delays.csv
b3ac6a3fac1ecc56afc4dc07709b69a3e2376150be6007f6dd29378b025efc89  results/R14_crypto_isofpr/data/R14_onset_delays_legacy_seeds.csv
671bc7377c69ed8aacf9ceb336255d15df1ef0e92d38e39fd39b804afbf574db  results/R14_crypto_isofpr/data/R14_qmle_recovery.csv
e269fbaa9c90d965cb132d4cd8ce3dc9e772ab3c7195dbe10b99f7102fc2019b  results/R14_crypto_isofpr/data/R14_qmle_recovery_legacy_seeds.csv
96d3c9f381c4f91aafb52456df207f08769f4b3a914a2e3b8f8830cfc8f7187d  results/R14_crypto_isofpr/figures/fig16_crypto_race.png
69965f7ef2069591439c5c482b2dfb434dec0a599f2a753a845f92bb44d31bb6  results/R14_crypto_isofpr/figures/fig16_crypto_race_legacy_seeds.png
2fe6fd0a43004c72e46b2f8f6397bfa39cc220cd98c102a2f4b2d3679a257544  results/R14_crypto_isofpr/tables/R14_claims.tex
08a8b822f9af3df720ea97708de9be2994a044251428c86d8e06f57eef82b2ae  results/R14_crypto_isofpr/tables/R14_claims_legacy_seeds.tex
```

`diff` between the two sets is empty on all twelve artefacts.

The two vendored input series are digest-asserted at start-up against the values the submitted log
recorded at its lines 7 and 8:

```
a9c84c890cac7284f6330e3ab4d4aed70a9a5e01ec04a8fc0c9ba8999e79c3f4  data/derived_crypto/btc_usd_daily.csv
f44703a75e4510e906ab1cda6e0a50d96e232bc80aba4ef5105ce6ae94c049f1  data/derived_crypto/eth_usd_daily.csv
```

### The test suite

`pytest tests/ -v` — **358 tests collected, 358 passed, 0 failures**, of which **26 are R14's**.
The R14 block is pasted verbatim below with the session header and the final line; the 332 omitted
lines are one `PASSED` per test of the other sixteen streams, and the per-file collected counts
follow.

```
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-9.0.3, pluggy-1.6.0 -- /home/m53/miniforge3/envs/Trading/bin/python3
cachedir: .pytest_cache
rootdir: /home/m53/The-Whitening-Advantage-Experiments
plugins: anyio-4.8.0
collecting ... collected 358 items

tests/test_R14_claims.py::test_R14_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 78%]
tests/test_R14_claims.py::test_R14_the_onset_delays_reproduce_every_aggregate_of_the_race PASSED [ 78%]
tests/test_R14_claims.py::test_R14_the_bisection_tolerance_admits_one_count_at_106_onsets_and_none_at_72 PASSED [ 79%]
tests/test_R14_claims.py::test_R14_the_two_arms_realize_one_false_alarm_rate_on_every_published_source PASSED [ 79%]
tests/test_R14_claims.py::test_R14_the_iso_fpr_match_on_real_ethereum_is_lost_under_the_re_keying PASSED [ 79%]
tests/test_R14_claims.py::test_R14_no_aggregate_reads_a_cell_the_caption_draws_hollow PASSED [ 79%]
tests/test_R14_claims.py::test_R14_the_derived_reliability_rule_reproduces_the_delivered_literal PASSED [ 80%]
tests/test_R14_claims.py::test_R14_the_bitcoin_numerals_of_L345_and_the_caption_reproduce PASSED [ 80%]
tests/test_R14_claims.py::test_R14_the_ethereum_boundary_of_L345_reproduces PASSED [ 80%]
tests/test_R14_claims.py::test_R14_the_synthetic_control_numerals_of_L345_do_not_reproduce_at_their_printed_precision PASSED [ 81%]
tests/test_R14_claims.py::test_R14_the_real_bitcoin_race_is_untouched_by_the_re_keying PASSED [ 81%]
tests/test_R14_claims.py::test_R14_the_design_effect_is_computed_from_the_mechanism_and_never_below_one PASSED [ 81%]
tests/test_R14_claims.py::test_R14_every_persisted_interval_is_a_wilson_interval_inside_the_unit_square PASSED [ 81%]
tests/test_R14_claims.py::test_R14_the_qmle_fallback_counters_are_reported_even_at_zero PASSED [ 82%]
tests/test_R14_claims.py::test_R14_the_legacy_seed_arm_reproduces_every_discrete_quantity_of_the_witness PASSED [ 82%]
tests/test_R14_claims.py::test_R14_the_legacy_seed_artefacts_declare_that_they_certify_no_published_value PASSED [ 82%]
tests/test_R14_claims.py::test_R14_the_carried_primitives_are_byte_identical_to_the_files_that_own_them PASSED [ 82%]
tests/test_R14_claims.py::test_R14_no_draw_reaches_the_global_numpy_stream PASSED [ 83%]
tests/test_R14_claims.py::test_R14_every_square_root_of_a_sample_size_follows_a_design_effect PASSED [ 83%]
tests/test_R14_claims.py::test_R14_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 83%]
tests/test_R14_claims.py::test_R14_every_produced_text_file_ends_in_a_newline PASSED [ 84%]
tests/test_R14_claims.py::test_R14_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 84%]
tests/test_R14_claims.py::test_R14_the_produced_sources_carry_no_banned_construct PASSED [ 84%]
tests/test_R14_claims.py::test_R14_report_the_campaign_against_its_witness PASSED [ 84%]
tests/test_R14_claims.py::test_R14_report_the_design_effect_and_the_reliable_grids PASSED [ 85%]
tests/test_R14_claims.py::test_R14_report_the_ratio_series_of_every_source PASSED [ 85%]

======================= 358 passed in 112.51s (0:01:52) ========================
```

Collected counts per file, from `pytest tests/ --collect-only -q`:

```
  5  tests/test_R01_claims.py     22  tests/test_R05_claims.py     26  tests/test_R12_claims.py
  8  tests/test_R02_claims.py     16  tests/test_R06_claims.py     24  tests/test_R13_claims.py
  5  tests/test_R02b_claims.py    28  tests/test_R07_claims.py     26  tests/test_R14_claims.py
  7  tests/test_R02c_claims.py    31  tests/test_R09_claims.py     28  tests/test_R16_claims.py
  9  tests/test_R03_claims.py     26  tests/test_R10_claims.py     24  tests/test_R18_claims.py
 27  tests/test_R04_claims.py     25  tests/test_R11_claims.py
 21  tests/test_R04b_claims.py                                    358  total
```

**No blocking assertion of `tests/test_R14_claims.py` rests on a continuous value R14 produced.**
Each rests on one of four things: a value v87 prints, compared at v87's printing precision; an
arithmetic fact independent of any run (the attainable lattice of the bisection tolerance, the
mechanism-fixed `K = 24`); a relation reimplemented in the test file independently of the
experiment (the Wilson interval from the second algebraic form R02 owns, the pairwise-reliable grid
re-derived from the persisted CSV, the `ast` segment extraction rerun); or, on the `_legacy_seeds`
arm alone, a **discrete** quantity of the witness.

**The witness is deliberately not a gate on the default arm** (`data/reference/README.md`): a
cell-by-cell equality assertion against a campaign the specification requires to be redrawn would
fail on the first run and its only exit would be a widened tolerance. On the `_legacy_seeds` arm it
is a gate, on discrete quantities only, because that arm shares the witness's seeds and the only
admissible drift there is one ULP from the parser change — which cannot move a count. **`ADD` is
given no tolerance on either arm**: a CUSUM crossing is a discontinuous function of its stream, so
a 1-ULP input change legitimately moves a delay by a whole trading day. The reporting test prints
how many cells moved (`0` of `88` on the legacy arm) and asserts nothing on it.

**Two assertions are self-invalidating** and are the ones to watch. If a later campaign brings the
`t₃₀` mean ratio back to `1.06`, or restores the `Real_ETH` iso-FPR match, the corresponding test
fires — and what must then be revised is `docs/DEVIATIONS.md` and this audit, never the assertion.

**The §S4.4 grep is empty** on `experiments/R14_crypto_isofpr/exp_R14_crypto_isofpr.py`, both
`logs/R14_crypto_isofpr/*.log`, `docs/sections/R14.md` and this audit — the ten-alternative pattern
of §S4.4, which this file deliberately does not quote because quoting it would put it in its own
scope. The suite runs the same pattern over five of those paths, so the check is executed rather
than reported. Also empty: `iterrows`, bare `except:`, absolute paths, `pytest` in the orchestrator,
and `np.sqrt` of a sample size without a preceding design effect. Every produced text file ends in
`\n`, asserted by the suite over both macro files, `requirements/R14.txt`, `docs/sections/R14.md`
and this audit.

---

## 6. Design decisions taken outside the plan

1. **C2's blocking scope.** The plan states C2 as "an exact equality assertion, per source" and,
   separately, that if the two ETH arms land on different counts "the ETH race is not iso-FPR and
   no ETH speed comparison is interpretable; that is **reported, not repaired**". Those two are
   only jointly satisfiable if the assertion halts on the sources whose speed comparison v87
   publishes and records the failure elsewhere. The set `{Real_BTC, Synth_BTC, Synth_ETH}` was read
   clause by clause off L345 — real Ethereum carries no delay and no ordering claim there — and is
   written into the source with that derivation beside it. **It is a scope fixed by what the
   manuscript says, not by which source turned out to fail**, and the run would have stopped had
   the mismatch landed on any of the three.
2. **A mirror D3 test on `Real_BTC`.** The plan fixes the D3 falsification condition for panel B
   only. §S3 requires halting on *any* falsified qualitative claim, and L345 makes one about
   Bitcoin too ("the sign filter leads across the reliable range"), so the symmetric test — the
   interval lying entirely **above** 1 — is implemented and evaluated. It does not fire.
3. **The onset bootstrap carries no legacy keying.** The plan's entropy table marks it "— (new)",
   and `--legacy-seeds` restores "the delivered `RandomState(100/200/201/300)` draws **and nothing
   else**". A draw with no delivered counterpart therefore has no legacy form, and the bootstrap
   uses `rng_for("R14", "onset_bootstrap", source, b)` in both arms. This also keeps
   `np.random.RandomState` confined to the three brokers, which is what control C10 asserts.
4. **Four delivered gates are kept as they stand.** The plan lists six non-negotiable corrections
   and none of them touches `Control (c)` (iso-FPR band `[0.03, 0.07]`, `|diff| ≤ 0.015`),
   `Control (f)` (`max |dev| ≤ 1.0`), G1 (`nu_hat < 4.7` on at least one asset) or G2 (the QMLE
   recovery band). All four are kept, all four pass, and G2's missing trigger probability is
   declared rather than papered over (§3, C3).
5. **`requirements/R14.txt` carries `pytest`.** The script does not import it; `tests/test_R14_claims.py`
   does, and it is a deliverable of the same stream. `requirements/R13.txt` sets the precedent. All
   six versions are read by `importlib.metadata.version()` at run time and written by the script.
6. **Columns beyond the plan's list.** `FPR_count`, `iso_fpr_matched`, `n_detected`, `deff_clamped`,
   `deff_lags`, `qmle_n_non_converged`, `qmle_n_frozen` and `qmle_fallback_frac` were added to the
   race CSV so that C2's integer counts, C1's flag, C3's obligation and C9's clamp are each
   checkable from the file alone rather than from the log.
7. **The figure's band is `SEM_design`, and the delivered `SEM` still ships.** The plan requires
   both; this records that the visible band is the honest one and the witness-comparable column is
   the persisted one, so a reader comparing the PNG with `protocol_24b` is comparing different
   quantities by design.

---

## 7. Findings that revise the plan's own premises

**1. The R14 prompt's §2.3 is wrong, and the direction of the error matters.** §2.3 states: "La
légende ne mentionne qu'ETH nulle part et ne revendique rien sur lui : **aucune affirmation publiée
n'est menacée**", and instructs that ETH be reported as an observation. The *caption* indeed says
nothing about Ethereum. **L345 does.** It publishes five ETH statements: the Ljung–Box
`p = 0.019`, the `72` onsets, that the recentred sign stream fails whiteness, that the fair-coin
pivot does not hold exactly, and that the synthetic control does not recover the light-tailed
ordering. ETH is therefore a **published claim to be reproduced and classified**, and rows 10, 11,
14 and 15 of §4 do that. The direction matters for §S3's asymmetry rule: v87 states its *own*
limitation here, so reproducing the failure reproduces a self-critical claim and takes ordinary
scrutiny rather than the heavier examination reserved for results that favour the manuscript. The
prompt's instruction to raise no camera-ready candidate is nevertheless followed, for the reason
the scope filter gives and not the reason §2.3 gives.

**2. C2's trigger probability was quoted as "0 given the data", and the control fired.** The plan's
own C2 row logged the fragility that caused it — the tolerance admits one count at `N = 106` and
none at `N = 72` — and its "Known risks" section pre-declared the handling. The measured event is
the anticipated branch, not a surprise; what the plan did not anticipate is that "0 given the data"
was conditional on a draw the plan itself required to be replaced. **A trigger probability
conditional on the draw being kept is not a trigger probability for a stream whose specification
redraws.** That is a general lesson for the remaining streams and is recorded as such.

**3. The plan's row-count estimate for the added artefact is wrong.** It states "~9.3k rows" for
`R14_onset_delays.csv`. The design gives `11 magnitudes × 2 arms × (106 + 72 + 106 + 72) onsets =
7 832` rows, and that is what ships. The test suite asserts the arithmetic rather than the
estimate.

**4. `Synth_ETH` carries seven pairwise-reliable magnitudes, not eight.** The plan's witness table
records "Synth_ETH mean ratio `0.5418` (< 1), **8** pairwise-reliable c". That is the *witness*
figure and the legacy arm reproduces it exactly. Under the migrated draw `c = 0.25` loses
reliability and the grid is seven long, which is why the regenerated mean is `0.9189` rather than
`0.5418`. The claim it supports — that the control does not recover the light-tailed ordering —
holds on both grids, and the interval `[0.7877, 0.9616]` lies entirely below parity.

**5. The plan's D2 criterion is stricter than §S3's, and §S3 prevails.** The plan writes: "A
printed numeral moving is D2: the condition is that the 95 % interval of the regenerated mean
excludes the printed `1.06`." The interval does **not** exclude `1.06`, while the printed rounding
does change (`1.06 → 1.04`). §S3 defines D2 as the rounding at the manuscript's printing precision
differing while the qualitative claim holds, and the preamble prevails over the plan without
exception. The entry is therefore registered as D2, and the fact that the interval covers the
published value is reported as the reason the severity is not more — which is the strongest reading
available to the manuscript.

**6. The real arm moved even less than the plan predicted.** The plan states that the real BTC/ETH
results "depend on the migration only through the ±1e-6 dither". On BTC the dependence is not merely
small: **not one of the 22 `Real_BTC` cells moves in any of the thirteen shared columns**. On ETH
the same dither does move a calibration, which is finding 2 above; the two outcomes differ because
the tolerance forces the BTC count and leaves the ETH one free.

---

## 8. Open questions, left open

1. **Why does `round_trip` parsing move `Var_z_hat` by `4.7e-09` while `nu_hat` and `lb_pvalue` are
   bit-identical?** The traced route is that a one-ULP change in the parsed returns propagates
   through a 2 800-step variance recursion into SLSQP, whose finite convergence tolerance returns a
   parameter vector differing at the ninth digit; `np.var(z_hat)` is a direct sum and shows it,
   while `stats.t.fit` and the Ljung–Box are optimiser and rank statistics that absorb it. The
   route is plausible and **not measured**, so §S4.5 forbids asserting it. What is measured is that
   no delay moves.
2. **Is the loss of the `Real_ETH` iso-FPR match a property of this particular key, or of most
   keys?** Answering it means running many re-keyings and reading a control's outcome across them,
   which is precisely the selection surface §S4.10 closes. The question is posed and not settled;
   what can be said without opening that surface is the arithmetic in §3, which shows the match was
   never enforced at `N = 72`.
3. **The design effect is measured on the delay series and applied to the detection-rate
   interval.** `CI_low_design` and `CI_high_design` evaluate the carried Wilson interval at
   `n_eff = n_det / deff`, where `deff` is the Kish factor of the *delay* mean. Whether the
   detection indicator carries the same dependence is not measured. No published numeral depends on
   it, and the plan prescribes this construction, but the two are different statistics and the
   substitution is an assumption.
4. **54 of 88 cells return a Kish sum below 1.** Whether that is finite-sample noise in the 24
   autocorrelation estimates or a genuine negative dependence between overlapping detection windows
   is not settled here. The clamp is conservative in the direction that matters — it never narrows
   an interval below the independent one — but a negative dependence, if real, would mean the
   independent interval is itself too wide on those cells.
5. **Should `\RFourteenUnreliableCells` be published at all?** v87 prints the rule and not the
   count, and the count is a property of the redrawn synthetic controls: it is `28` here and `25`
   in the submitted campaign. The macro exists because the R14 prompt §4 lists it. Whether a
   camera-ready revision should quote a count that moves with the draw is a question for the
   orchestrator, not for this stream.
6. **Is `Real_ETH`'s lost iso-FPR match the same phenomenon L345 calls "the fair-coin pivot does not
   hold exactly"?** The two are consistent — a non-white recentred sign stream is exactly what makes
   the `Concept` arm's placebo crossing count refuse to sit where the calibration wants — but this
   stream measures no link between the Ljung–Box rejection and the bisection outcome. The
   association is recorded and no mechanism is attributed.
