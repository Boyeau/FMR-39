# AUDIT — R09, anytime-valid detection on the fair-coin stream (v87 Figure 9, `fig:anytime`, L243)

This file is the sole handover for the R09 stream. It records what was measured, what each control
is a control **of**, the trigger probability of every gate under its own null, the decisions taken
outside the plan, the findings that revise the prompt's own premises, the three reproducibility
axes with both digest sets, and the questions left open.

`docs/sections/R09.md` is the reader-facing report and `docs/DEVIATIONS.md` carries the three
register entries; where they overlap with this file, this is the one with the arithmetic.

---

## 1. What R09 establishes

The submitted campaign is `Priorite_22_eprocess_anytime.py`, which writes `protocol_22a`–`22d`.
R09 ports it into the FAIR harness under a 128-bit re-keying and classifies every published numeral
D0–D3.

**Every qualitative claim of L243 and of the Figure 9 caption reproduces.** The mixture martingale
stays at or below `α` under monitoring to `4H` at all seven levels; the fixed-horizon CUSUM does
not, and exceeds the mixture at every level by `22.9`–`68.5` **paired** standard errors on the same
20 000 streams; e-CUSUM clears `ARL₀ ≥ 1/α` with a minimum margin of `20.54×`; and the mixture is
the faster arm at `η = 0.10` in the marginal reading and at **every** `η` on the grid under the
selection-free one.

**Three printed numerals move at v87's own printing precision** — `18\% → 20\%`, `409 → 410`,
`539 → 533` — under the entropy migration §S6 requires. That is the D2 `R09-campaign-redraw`, and
§5 gives the arithmetic of each.

**The stream's one substantive readability problem is `protocol_22d`.** `ARL0_mean` for CUSUM and
MIX is a horizon artefact and not a measurement, at `65.10%`–`95.54%` and `90.52%`–`99.06%`
right-censoring respectively. The published caption names **only** e-CUSUM in panel C, whose
censoring is `0` at six of seven levels and `0.00055` at the seventh, so **no printed claim is
falsified**. The task was to make the censoring legible in the artefacts, not to correct a claim,
and that is what C1, the macro-emitter guard and panel C's hollow markers do.

---

## 2. Four things the reader must not take from this stream

**(i) `\RNineCusumPeekingFprMax` is not a maximum over the level grid.** It is the maximum over the
**three stopping protocols at `α = 0.05`**, which is the tallest CUSUM bar of panel A and exactly
what "climbs to 18%" names. Over the whole `α` grid the CUSUM peeking rate reaches `0.34905` at
`α = 0.10`, and MIX's reaches `0.0948`. Both grid maxima are in the log and in the `.tex` header
comment. Peeking dominates the other two protocols **by construction** — `{fa ≤ H}` and
`{cross at 4H}` are subsets of `{fa ≤ 4H}` — so the maximum is always the peeking bar; that is
structural, not empirical.

**(ii) The CUSUM and MIX curves of panel C are not average run lengths.** They are
`mean(min(fa, 4H))` over samples censored above `65%` and `90%`, and such a mean is bounded below by
`censored_frac · 4H` **by arithmetic**, with no reference to the detector. The MIX point at
`α = 0.01` reads `19 842` against a floor of `19 811`. No `ARL₀`-derived macro is emitted from those
rows, and the emitter exits `1` rather than emit one.

**(iii) Panel B's `ADD` is not a marginal delay.** It is conditional on an alarm inside `(τ, H]`,
and the two arms condition on different events at rates that differ by a factor of `2.8` at
`η = 0.02`. At the two smallest drifts the marginal curve inverts the ordering the data support;
§3 C4 gives the selection-free reading.

**(iv) The e-CUSUM H1 file reproduces nothing v87 prints.**
`R09_eprocess_race_control_ecusum.csv` is audit-only. v87 draws panel B with two curves and its
caption names CUSUM and MIX; the file exists because a positive control on the delay response is
worth having, and its filename and its `arm` column both stamp the branch.

---

## 3. Controls, with their margins and their trigger probabilities

Every gate below was written with its null law and its trigger probability **logged before the
first number was read**. No level was chosen after a result was seen.

### C1 — censoring is inseparable from every `ARL₀`

Structural. No `ARL0_mean` is written to a frame, plotted, or passed to the macro emitter without
`censored_frac` on the same row; asserted on the frame schema and on the emitter's input, and again
independently in `tests/test_R09_claims.py`. All 21 rows carry a finite mean with its fraction;
`0` offending. Two further columns make the arithmetic legible: `arl0_implied_lower_bound`
(`censored_frac · T_ext`) and `bound_flag_carried_information`. **Deterministic; trigger probability
0.**

### C2 — `arl0_bound_respected` is a computed comparison, and it is uninformative on 14 of 21 rows

The R09 prompt §2.1 asks whether the flag is "une tautologie de définition" or "un littéral".
**It is neither.** `Priorite_22:613` writes `"arl0_bound_respected": arl0 >= (1.0/a)`, a genuine
comparison; the port carries the same expression and locates it in its own AST, asserting that it is
a single `>=` whose right-hand side carries `1.0 / a` and that exactly one producing site exists.
The test file re-evaluates the column against an independently written comparison.

What the flag is, precisely, is a computed comparison that is **arithmetically necessary** on the
censored arms: `arl0 = mean(min(fa, T_ext)) ≥ censored_frac · T_ext ≥ 0.65 × 20 000 = 13 000`,
against a `1/α` of at most `100`. The port logs the implied lower bound beside every row and states,
per row, whether the flag carried information:

| arm     | rows | implied lower bound `censored_frac · T_ext` | `1/α`      | flag informative |
| ------- | ---- | ------------------------------------------- | ---------- | ---------------- |
| CUSUM   | 7    | `13 019` – `19 107`                         | `10`–`100` | **no**           |
| MIX     | 7    | `18 104` – `19 811`                         | `10`–`100` | **no**           |
| e-CUSUM | 7    | `0` – `11`                                  | `10`–`100` | **yes**          |

**The flag carries information on 7 of 21 rows, all of them e-CUSUM.** On the other 14 it could not
have been `False` whatever the campaign measured. **Deterministic; trigger probability 0.**

### C3 — the martingale bound as one statistic with an exact null

**Why the obvious designs are unusable, computed before the run.** Seven per-`α` binary gates at 5%
ring on a compliant campaign with probability `1 − 0.95⁷ = 30.17%`. Worse at the point that matters:
the mixture's peeking rate sits at `0.945`–`1.000` of `α`, so at `α = 0.05` the margin to the bound
is `0.00055` against a binomial SE of `0.00154` — **`0.36σ`**, roughly a `36%` chance of a spurious
exceedance at that level alone. A two-sided KS test of the seven p-values against `Uniform(0,1)` is
also the wrong instrument: under Ville those p-values are *stochastically large* by construction, so
a uniformity test would reject precisely **because** the bound is conservative. The claim is
one-sided domination.

**Design.** Let `Z = sup_{1≤t≤4H} E_t` per H₀ stream and `U = min(1, 1/Z)`. Ville gives
`P(Z ≥ 1/α) ≤ α` for every `α`, i.e. `F_U(α) ≤ α` over the whole range — a stochastic-dominance
statement, not seven points. Tested with the one-sided Kolmogorov statistic `D⁺ = sup(F_n(α) − α)`
on `n = 20 000`, exact null `scipy.stats.ksone.sf(D⁺, n)` at the least-favourable boundary
`F_U = Id`. **Gate at `0.01`; trigger probability under its own null exactly `0.01`, and strictly
below it because the true `F_U` is bounded away from the identity and `U` has atoms.**

*Derivation, one line as §S4.6 requires:* each mixture component is a non-negative martingale with
`E₀ = 1` (a component not yet started holds value 1), a convex combination of martingales is a
martingale, and Ville's inequality on a non-negative martingale gives `P(sup_t E_t ≥ c) ≤ E₀/c = 1/c`.

| replicate                               | `D⁺`        | exact one-sided `p` | verdict      |
| --------------------------------------- | ----------- | ------------------- | ------------ |
| MIX, H₀ campaign, `n = 20 000`          | `2.4249e-4` | `0.99749`           | no rejection |
| MIX, M1(ii), disjoint key, `n = 20 000` | `7.5431e-4` | `0.97701`           | no rejection |
| **CUSUM, negative control**             | `0.4775`    | `0.0`               | rejects      |

`U` has an atom at `1` of mass `0.0046` — the streams whose mixture never exceeds `1` — which sits
above every `α` and cannot inflate `D⁺`. The two MIX replicates are reported side by side and
neither is averaged into the other (see §9, open question 1).

**The negative control is what establishes the instrument has power against the alternative it is
used on**, and two caveats travel with it, neither repaired: `U_cusum` is read off an **estimated**
survival function on `N_CAL = 50 000` draws, which carries the double variance of §S4bis's second
corollary; and the CUSUM statistic lives on a lattice, so `U_cusum` has heavy ties, under which the
`ksone` tail is not exact. The effect size (`0.05 → 0.20`) dwarfs both. This direction is a control
on power, not an acceptance gate.

**The seven per-`α` exact one-sided binomial p-values are computed, logged and persisted** as the
`binom_p_one_sided` column of `R09_validity_stopping.csv`, descriptively and not as an acceptance
criterion (§S4bis point 3). For the MIX peeking rows they run `0.508`–`0.993`.

### C4 — the positive control, and the conditioning confounder

**Why nine adjacent gates are unusable.** `1 − (1 − 0.01)⁹ = 8.65%` family-wise, and strict adjacent
monotonicity is not a property the data have: in the submitted campaign the CUSUM pair
`η = 0.02 → 0.04` moves `1244.36 → 1234.90`, `−9.5` steps against a difference SE of order `77`,
which inverts roughly half the time. Replaced by one **one-sided Spearman of `ADD` against `η` over
the ten grid points, with its exact permutation null** — all `10! = 3 628 800` permutations
enumerated, not sampled. **Gate at `0.01` per arm.**

| arm     | `ρ`  | exact one-sided `p` (decreasing) | ties | WLS slope (steps per unit `η`) | verdict           |
| ------- | ---- | -------------------------------- | ---- | ------------------------------ | ----------------- |
| CUSUM   | `−1` | `2.7557e-7`                      | 0    | `−2666.7 ± 31.2`               | monotone decrease |
| MIX     | `−1` | `2.7557e-7`                      | 0    | `−2763.9 ± 22.3`               | monotone decrease |
| e-CUSUM | `−1` | `2.7557e-7`                      | 0    | `−558.6 ± 78.9`                | monotone decrease |

The same test on detection rate against `η`, one-sided increasing, is reported and **not** gated:
CUSUM `ρ = 0.937`, `p = 3.31e-5`; MIX `ρ = 0.813`, `p = 1.39e-3`; e-CUSUM `ρ = NaN` with **nine
tied rates** — see §6, finding 3. The nine adjacent z-margins per arm are logged descriptively and
gate nothing.

**The confounder, named and measured.** `ADD` is conditional on `(fa > τ) & (fa ≤ H)`, and at
`α = 0.05` the detection rates run from `0.0570` to `0.9760`. At `η = 0.02` the CUSUM detects
`5.70%` and the mixture `16.15%`, so the mixture's conditional mean necessarily averages over slower
streams and comes out higher.

**The primary instrument is a matched-detection-rate quantile, not the common-detection subset.**
The subset is the intersection of two detection events whose rates differ by `2.8×`; it is dominated
by the streams both arms find easy, its composition depends on both detectors, and it is therefore
itself a selected sample that cannot carry a D3. The selection-free comparison sets
`q = min(p_CUSUM, p_MIX)` at each `η` and compares the `q`-quantile of each arm's alarm-time
distribution with non-detections placed at `+∞`. It is well defined for every `q ≤ min(p)`,
conditions on nothing, and is the same iso-rate logic the paper's own iso-FPR race uses. Paired
bootstrap over the 2 000 trajectory indices, 2 000 replicates, 95%:

| `η`    | `q`      | CUSUM `q`-quantile | MIX `q`-quantile | MIX − CUSUM | paired bootstrap 95% | common-detection paired mean ± SE | `n` common |
| ------ | -------- | ------------------ | ---------------- | ----------- | -------------------- | --------------------------------- | ---------- |
| `0.02` | `0.0570` | `2404`             | `1292`           | **`−1112`** | `[−1242, −964]`      | `+114.17 ± 53.01`                 | `70`       |
| `0.04` | `0.2000` | `2485`             | `981`            | **`−1504`** | `[−1562, −1427]`     | `−53.48 ± 31.77`                  | `380`      |
| `0.06` | `0.5380` | `2473`             | `902`            | `−1571`     | `[−1601, −1541]`     | `−360.54 ± 18.05`                 | `1057`     |
| `0.08` | `0.8700` | `2495`             | `912`            | `−1583`     | `[−1616, −1533]`     | `−332.35 ± 13.28`                 | `1711`     |
| `0.10` | `0.9710` | `2420`             | `959`            | `−1461`     | `[−1583, −1076]`     | `−124.17 ± 8.42`                  | `1913`     |
| `0.12` | `0.9725` | `2328`             | `711`            | `−1617`     | `[−1692, −401]`      | `+8.24 ± 4.29`                    | `1916`     |
| `0.14` | `0.9725` | `1061`             | `575`            | `−486`      | `[−568, −53]`        | `+54.27 ± 2.44`                   | `1916`     |
| `0.16` | `0.9725` | `773`              | `451`            | `−322`      | `[−371, +106]`       | `+69.89 ± 1.71`                   | `1916`     |
| `0.18` | `0.9725` | `472`              | `374`            | `−98`       | `[−125, +97]`        | `+72.62 ± 1.36`                   | `1916`     |
| `0.20` | `0.9725` | `382`              | `332`            | `−50`       | `[−82, +104]`        | `+71.08 ± 1.18`                   | `1916`     |

**Decision rule, fixed before the first number and applied as written:** the mixture's matched-rate
quantile is at or below the CUSUM's at `η = 0.02` **and** `η = 0.04`, with both bootstrap intervals
excluding zero, so **case (1) applies**: the marginal `ADD` reversal is an artefact of conditioning,
L243's "ceding ground only for abrupt shifts" and the caption's "matches … for `η ≤ 0.10`" stand,
and `R09-add-conditioning` is a Class A entry with **no severity**. The halt condition was not met.

**The two instruments disagree at `η = 0.02` and that disagreement is the finding.** The
common-detection subset there puts the CUSUM ahead by `+114` steps on `70` streams; the matched-rate
quantile puts the mixture ahead by `1 112` on all `2 000`. Both ship. From `η = 0.04` onward the two
agree in sign through `η = 0.10`. The Kish design effect of the paired comparison runs `0.48`–`0.76`
with within-pair correlations of `0.47`–`0.76`, so the pairing buys between a `24%` and a `52%`
variance reduction and no pooled interval is published without it.

### C5 — `ast` source identity, in three layers, run before any compute

Extracted **by position and never by import**: importing the witness would execute its environment
block, its `mode='w'` logger and its directory creation.

| layer | statement                                                              | margin                     |
| ----- | ---------------------------------------------------------------------- | -------------------------- |
| (i)   | byte identity of the carried primitive `wilson_ci` against the witness | 442 characters, 0 diffs    |
| (ii)  | the five adapted routines quoted in full with their SHA-256            | 10 047 characters logged   |
| (iii) | **statement-level identity of the recursions**                         | **27 statements, 0 diffs** |

Layer (ii) covers `_process_m1_chunk`, `_process_h0_chunk`, `calibrate_cusum`, `simulate_h1` and
`run_m1_certificate`. Byte identity is not assertable on them because each takes an injected
generator where the witness spawns one from a master `SeedSequence`, and each replaces
`rng.binomial(1, p, size)` by a threshold on a shared uniform. R13's treatment applies: the witness
source of each is quoted in full in the log with its digest.

Layer (iii) is what actually catches a transcription error. The exact source text of every
assignment to a recursion target is extracted from the witness AST and must appear **verbatim** in
the port: the three CUSUM lines (`dev`, `S_pos`/`S_neg`, `M_cusum`), the four MIX lines
(`active_idx`, `inc_mix`, `logM_mix`, `logE_mix`), the five e-CUSUM lines (`ip`, `im`, `logMp`,
`logMm`, `M_ecusum`), the two mixture log-increments, the four e-CUSUM increment definitions and
`l_star = np.quantile(max_M, 1 - a)`. **Deterministic; trigger probability 0 unless a copy has
drifted.**

**The vendored witness is itself verified.** All four `protocol_22*.csv` under `data/reference/R09/`
reproduce the SHA-256 digests the submitted run recorded in its own log
(`4dfe5a34…`, `0a3e63dd…`, `82c1c7ed…`, `90cb8994…`).

### C6 — reproducibility, three axes

See §7 for the digest sets.

### Additional gates, each with a derived tolerance

| gate                   | statistic                                             | measured                          | tolerance            | trigger probability     |
| ---------------------- | ----------------------------------------------------- | --------------------------------- | -------------------- | ----------------------- |
| calibration coherence  | `                                                     | level([1,H]) − level(calibration) | ` at `α = 0.05`      | `0.003110` = `1.706` SE | `0.006000` = `3.29` SE | `0.001`     |
| M1(i)                  | `                                                     | E[λ_t] − 1                        | ` over `2×10⁶` draws | `1.483` SE              | `19.6` SE              | `7.094e-86` |
| structural cross-check | alarm indicator ≡ running-maximum indicator, 21 cells | 0 disagreements                   | exact                | `0`                     |

The coherence gate is the replacement for the delivered `(b)` and `(e)`, both of which ignore that
`λ*` is **itself estimated** on `N_CAL = 50 000`. The correct variance of the difference is
`α(1−α)(1/N_NULL + 1/N_CAL) = 3.325e-06` at `α = 0.05`, an SE of `0.001823` against the delivered
`0.001541` — understated by a factor `1.183`. The tolerance is `z(1 − 0.001/2)` times that SE and is
derived from the mechanism, never from an observed gap.

### Stream-level family-wise trigger probability

C3 gates at `0.01` on one arm; C4 gates on a one-sided Spearman at `0.01` on each of three arms.
Four gates whose nulls are exact or conservative by construction, so
`1 − (1 − 0.01)⁴ = 3.9404%` bounds the probability that at least one fires on a compliant campaign —
below the 5% ceiling §S4bis fixes. Including the coherence gate at `0.001` and the M1(i) gate, the
full figure is `4.0365%`. **Logged once, before any result was read.**

---

## 4. Decisions taken outside the plan, and decisions the plan fixed

**D1 — `N_ALT` stays at 2 000, and nothing is registered for the caption's "per cell".** L243's
`409` and `539` are themselves 2 000-stream measurements: `simulate_h1` loops on `N_ALT` and the
delivered log line `Control (g): … ADD=409.11` is that loop's output. Raising `N_ALT` to 20 000
would displace two printed numerals in order to make a parenthetical true — a self-inflicted D2
against the non-regression role §S1 gives v87's results. L243's "`2×10⁴` fair-coin streams per
level" scopes the count to the H₀ arm correctly, and a fair-coin stream is by definition an H₀
stream. The Figure 9 caption's "(`2×10⁴` streams per cell)" is **imprecise, not false**, and §Filtre
de périmètre bars an imprecise-but-not-false formulation from the register; it travels as
`docs/camera_ready_candidates/R09_v87_stream_counts.md`, which names all three sample sizes per
panel. The resolution the decision buys is logged panel by panel: panels A and C carry Wilson
intervals at `n = 20 000`, panel B carries SEMs at `n = 2 000`, `3.16×` wider, and panel B's axis
carries its own `n`.

**D2 — the prompt's §5 C4 carries a specification defect, recorded and not silently repaired.** See
§6, finding 1.

**D3 — C4 runs on all three arms and the third is persisted outside the published path.** See §2
(iv) and §6, finding 3.

**D4 — `arl0_bound_respected` is neither a tautology nor a literal.** See §3, C2.

**Outside the plan: `\RNineMixDriftParityThreshold` ships with its own null.** It is an extremum over
a grid, which §S4bis's fourth corollary requires to carry one. The threshold is `0.10`. The first
non-parity point above it is `η = 0.12` at `ADD_MIX − ADD_CUSUM = +8.20` steps against an unpaired
SE of `5.75` (`z = +1.43`) and a paired SE of `4.29`, so **a redraw can move the threshold one grid
step**. Moving it *up* leaves the caption's `η ≤ 0.10` true. The paired difference, paired SE and
design effect at every `η` are logged.

**Outside the plan: three delivered gates removed, and one floor.** `Priorite_22:619` and `:631`
are equality tests at `1e-9` on Monte-Carlo values the script itself produced; §S7 forbids anchoring
an assertion on such a value, and the re-keying redraws the campaign by construction, so all three
would fail on the first run and their only exit would be a widened tolerance. They become D0–D3
classification against the witness CSVs, read with `float_precision='round_trip'` on both sides. The
delivered `if fpr > a + 0.005` of M1(ii) goes the same way — `0.005` is derived from nothing — and
C3 replaces it. The delivered `(c)` floor of `0.80` on the e-CUSUM peeking rate is reported with its
Wilson interval (`1.0`, `[0.99981, 1.0]`) and gates nothing.

**Outside the plan: the draw mechanism changes, deliberately and in the log.** Every Bernoulli draw
is `y_t = (rng.random(size) < p)` rather than `rng.binomial(1, p, size)`. Exact Bernoulli either
way, but with a threshold on a shared uniform two `η` values consume the identical uniform stream
and differ only where the threshold moves, which makes the common-random-numbers plan **structural
rather than incidental**. `Generator.binomial`'s consumption pattern for `n = 1` is an
implementation detail that must not be relied upon. This change contributes to
`R09-campaign-redraw` alongside the re-keying and the two are not separated.

**Outside the plan: `--fast` is dropped.** A second, unstamped parameter set reachable by a flag is
not a configuration the repository can certify.

**Outside the plan: three assertions of `tests/test_R09_claims.py` were mis-specified and were
repaired.** They are recorded here rather than quietly corrected,
because a repaired test is exactly the thing §S4.8 warns about and the direction of each repair is
what distinguishes a correction from a widened tolerance. **No parameter, seed, tolerance or bound
of the experiment moved**, and the campaign was not re-run on their account.

| assertion, as delivered                         | why it fired                                                                                                   | what replaced it                                                                                                                                                                                                                                                                                        |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frame["ADD"].notna().all()` on **both** frames | applies a published-path invariant to the audit-only frame, where `ADD` is a mean over an empty set on 20 rows | **Stricter:** the **equivalence** `ADD isna ⟺ DetRate == 0`, asserted in both directions, on `ADD` and `SEM`                                                                                                                                                                                            |
| `"--fast" not in text`                          | fires on the module docstring recording that the delivered flag was **dropped**                                | **Stricter:** the parser's option set read out of the AST, asserted equal to `{--n-jobs, --control-arms}`                                                                                                                                                                                               |
| `"pytest" not in script`                        | fires on the orchestrator's header comment recording that it never calls pytest                                | **Correctly scoped (reduced coverage):** the same test over the script's **executable lines**, comments stripped. The coverage is reduced — a mention in a comment stops triggering it — which is justified because the preamble requires checking the *call* to pytest, not its mere mention in prose. |

The first is the substantive one. e-CUSUM's H₀ `ARL₀` is `206` and `319` steps at `α = 0.10` and
`0.07` against a change point at `τ = 2500`, so **no** stream survives to `τ` un-alarmed at those two
levels, `DetRate = 0` on all 20 of their rows, and the delay is undefined rather than zero. Writing
a number into an empty cell is the failure mode the column exists to prevent, so the frame is right
and the assertion was wrong. The published frame's minimum detection rate is `0.0165` and it carries
no missing value.

**Outside the plan: the two self-invalidating tests §9 requires were absent and were added.** The
plan fixes that "if a later campaign restores `409`/`539`/`18\%`, the test fires and
`docs/DEVIATIONS.md` is what changes, not the assertion". The delivered file carried the three
numerals in a **reporting** test only, which asserts nothing.
`test_R09_the_three_monte_carlo_numerals_of_L243_does_not_reproduce_at_printed_precision` now
asserts the displacement itself, and
`test_R09_the_calibrated_level_and_the_stream_count_still_reproduces_v87s_numerals` asserts the two
numerals that survive — which is why the register entry names three and not five. **Neither asserts
a tolerance on the size of a move.** R07's precedent gates `|z| ≤ 3` on its redrawn numerals; here
the peeking rate sits at `+4.77`, so importing that gate would mean choosing a bound after seeing
the number. The displacement is asserted, its magnitude is characterised in §5, and nothing is
gated on it.

**Outside the plan: import safety.** `Priorite_22` calls `setup_logging(...)` and
`log_requirements()` at **module level** with `mode='w'`. Under joblib's `loky` backend every worker
re-imports the module and would truncate the log. All side effects moved inside `main()` under
`if __name__ == "__main__"`; the chunk workers are pure module-level functions with no logging.

---

## 5. Deviation classification D0–D3, with the source cell of every value

| v87 site                              | printed         | regenerated            | witness            | class  | source cell                                                    |
| ------------------------------------- | --------------- | ---------------------- | ------------------ | ------ | -------------------------------------------------------------- |
| L243 / Fig. 9(A) CUSUM peeking FPR    | `18\%`          | **`20%`** (`0.1988`)   | `18%` (`0.1801`)   | **D2** | `R09_validity_stopping.csv`, CUSUM / `0.05` / peeking / `FPR`  |
| L243 CUSUM calibrated to `5\%` at `H` | `5\%`           | `5%` (`0.05345`)       | `5%` (`0.0493`)    | D1     | `R09_level_granularity.csv`, CUSUM / `0.05` / `achieved_level` |
| L243 MIX `ADD` at `η = 0.10`          | `409`           | **`410`** (`410.4027`) | `409` (`409.1131`) | **D2** | `R09_eprocess_race.csv`, MIX / `0.05` / `0.10` / `ADD`         |
| L243 CUSUM `ADD` at `η = 0.10`        | `539`           | **`533`** (`532.8512`) | `539` (`538.8052`) | **D2** | `R09_eprocess_race.csv`, CUSUM / `0.05` / `0.10` / `ADD`       |
| L243/L559 fair-coin streams per level | `$2\times10^4$` | `20000`                | `20000`            | D0     | `N_NULL`, the H₀ arm of panels A and C                         |

### The three qualitative claims, each with the measurement that carries it

| v87 clause                                                   | measurement                                                                  | verdict |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------- | ------- |
| MIX "remains bounded by `α`" under peeking                   | 7 of 7 levels; `FPR/α` = `0.948, 0.966, 0.982, 0.970, 0.962, 1.000, 0.945`   | holds   |
| "e-CUSUM satisfies `ARL₀ ≥ 1/α`"                             | 7 of 7 rows; minimum ratio `20.54` at `α = 0.10`                             | holds   |
| "Only MIX controls the time-uniform false-alarm probability" | CUSUM exceeds MIX at 7 of 7 levels; e-CUSUM peeking `= 1.0000` at `α = 0.05` | holds   |

**The `α = 0.015` cell sits exactly on the bound.** MIX's peeking rate there is `0.01500`, a ratio
of `1.000` with an exact one-sided binomial `p` of `0.508`. It is at the bound, not above it, so the
claim holds as written; it is recorded because a reader of the ratio column should know that one of
the seven cells has no margin at all. This is precisely why C3 does not gate on seven point
estimates.

### The `18\%` displacement, in full

`0.1801 → 0.1988` is `+4.77` standard errors of its own difference (binomial SEs `0.002717` and
`0.002822`). That is not an ordinary redraw. The channel is documented and traceable: the calibration 
threshold is estimated by an empirical quantile on a finite sample, so it lands on one or the other 
attainable point of a discrete support.

`max_M` lives on a `0.2` lattice — `dev − δ_CUSUM` takes `+0.4` or `−0.6`. Measured over the 50 000
calibration streams, the largest distance from a lattice point is `6.253e-13` in lattice units, i.e.
floating-point accumulation and not a second support, and `1 628` distinct values are realised,
giving `1 628` attainable levels. As certified by R07 and read at `float_precision='round_trip'` from 
`results/R07_estimated_mean/data/R07_lattice_exact_law.csv`, the exact lattice levels around the 5% 
target are `4.29%` at `λ = 11.4` and `5.03%` at `λ = 11.2`. `np.quantile(max_M, 1 − α)` therefore 
returns a lattice point, and it returned different ones on the two campaigns at four of the seven levels:

| `α`     | witness `λ*` | regenerated `λ*` | witness level on its calibration sample | regenerated level on its calibration sample |
| ------- | ------------ | ---------------- | --------------------------------------- | ------------------------------------------- |
| `0.10`  | `10.4`       | `10.4`           | `0.1005`                                | `0.1003`                                    |
| `0.07`  | `11.0`       | **`10.8`**       | `0.0707`                                | `0.0701`                                    |
| `0.05`  | `11.4`       | **`11.2`**       | `0.0504`                                | `0.0503`                                    |
| `0.035` | `11.8`       | **`11.6`**       | `0.0352`                                | `0.0351`                                    |
| `0.025` | `12.2`       | `12.2`           | `0.0250`                                | `0.0253`                                    |
| `0.015` | `12.8`       | `12.8`           | `0.0150`                                | `0.0151`                                    |
| `0.01`  | `13.4`       | **`13.2`**       | `0.0101`                                | `0.0101`                                    |

Both thresholds are legitimate outputs of the same estimator on their own `N_CAL = 50 000` sample,
and they achieve the same level at the horizon they were calibrated for. Peeking to `4H` amplifies
the one-step difference: the held-out level over `[1, H]` moves `0.0493 → 0.05345` (`×1.084`) and
the peeking rate `0.1801 → 0.1988` (`×1.104`).

**R09 does not separate the threshold channel from the fresh-draw channel.** Doing so would require
replaying the regenerated H₀ sample at `λ* = 11.4`, which is not an experiment v87 contains. §S4.5
forbids asserting a decomposition the measurement does not establish, so the two channels are
reported together and the separation is carried as open question 5 in §9.
`R03-cusum-nominal-level` and `R07-lambda-star-estimator` record the same estimator behaviour on the
same statistic; `level_is_attainable` is `False` on all seven CUSUM rows and `True` on all seven MIX
rows, and it is computed from the lattice rather than typed.

### What does **not** reach the register

- **The caption's "`2×10⁴` streams per cell"** — imprecise, not false (§4, D1).
- **The e-CUSUM H1 control arm** — reproduces nothing v87 prints (§2 iv).
- **The e-CUSUM peeking rate of `1.0`** — v87 prints no e-CUSUM false-alarm rate; panel A shows the
  bar and the caption's "only MIX" is what it supports.
- **The "extended" stopping protocol** — v87 does not describe it and panel A plots it; §9, open
  question 3.

---

## 6. Findings that revise the prompt's own premises

**1. The prompt's §5 C4 transposes panel C's three arms onto panel B.** Prompt §1 reads three arms
out of `protocol_22d`, which is the **`ARL₀` file — H₀, panel C**. §5 C4 then requires the delay
monotonicity control on "the three arms" of panel B. v87 draws panel B with **two** curves; its
caption names CUSUM and MIX; e-CUSUM appears in panel C's caption alone; and the delivered
`simulate_h1` returns keys for `"CUSUM"` and `"MIX"` only, matching the manuscript. This is a
specification defect of the prompt, not of the manuscript, and it is recorded rather than silently
repaired: `R09_eprocess_race.csv` keeps exactly two arms and panel B keeps two curves, while the
third arm runs under an explicit flag into a separately named file.

**2. `\RNineEcusumCensoredFracMax` is not zero, and it was not zero in the submitted campaign
either.** The prompt's parenthetical "(0 attendu)" and its §2 "contre `0.0000` pour eCUSUM" are
wrong about the **witness**, before any regeneration: `protocol_22d` carries `censored_frac =
0.0006` at `α = 0.01`. The regenerated campaign gives `0.00055` at the same level and `0` at the
other six. **No manuscript claim is affected** — v87 prints no censored fraction — and the macro
ships the measured value rather than the expected one. `tests/test_R09_claims.py` asserts the
witness is non-zero, so if that ever became false this finding would be withdrawn rather than
quietly kept.

**3. e-CUSUM's H1 arm is not blind, and it is not slow either — it has already alarmed.** The plan
anticipated that the positive control might show a delay that does not respond to `η`, and fixed in
advance that such a finding would be reported in full with no parameter moved. The measurement is
different and more specific. e-CUSUM's conditional delay **falls monotonically** from `145.7` to
`45.0` steps across the grid (`ρ = −1`, exact `p = 2.76e-7`), so the arm responds to the drift. Its
detection rate inside `(τ, H]` is `0.003` at **every one of the ten drifts** — nine tied rates, which
is why the detection-rate Spearman returns `NaN`. The reason is arithmetic: at `α = 0.05` e-CUSUM's
H₀ `ARL₀` is `480` steps against a change point at `τ = 2500`, so on `99.7%` of streams the first
alarm does not land in `(τ, H]` at all — it has already occurred before the change — and only the
`6` survivors per cell are counted. The rate is *identical*
across `η` because the pre-change data are shared by common random numbers, so the surviving set does
not depend on the drift — an incidental but clean exhibit of the CRN design. e-CUSUM is an `ARL₀`
device, not a level-`α` test, and its panel A bar of `1.0000` is the same fact seen from the H₀ side.

**4. The prompt's `18\%` premise understates the displacement's mechanism.** The prompt treats the
peeking rate as a Monte-Carlo value that the re-keying will move. It does, but at `+4.77` SE the
dominant visible channel is the one lattice step in `λ*`, which is a property of the estimator rather
than of the draw. See §5.

---

## 7. Reproducibility, three axes

### Axis 1 — two successive `./run_experiment_R09.sh`

Both digest sets pasted as-is, run A then run B. **Identical on all seven artefacts.**

```
# run A, 2026-08-08T00:45:02Z → 00:50:17Z, 315 s wall, 10 workers
27e296087afa6369ce93b3f9aaf402eec3c6b78c8c734202e910742d02f7c6df  data/R09_validity_stopping.csv
dad44f3d05e14863c8fbbd9e91ba38a5298457255f02980891b56ad0ed544264  data/R09_eprocess_race.csv
af880acfcbe2136b4ccd10a17ff6f8058b72fe669a44e9acc6e2d3f7729c5c70  data/R09_level_granularity.csv
b0b486eca9404c8bc7c96799d20af9cf783ad4ec299ff7a2d7eedec623dbbcaa  data/R09_arl0.csv
90f7dd73e8d8f811113ddc629d88894d295cff05c9e481b9c7dbe629ada718f6  data/R09_eprocess_race_control_ecusum.csv
95dadf2706062b7b7ab406da6f97f13d5057849869e0dac4db7cae64836927ee  figures/fig09_anytime_valid.png
34b92176ccefee604f8034a97463efe72a760b7f5326a6fb655b511d20e80cfe  tables/R09_claims.tex

# run B, 2026-08-08T00:50:17Z → 00:55:09Z, 292 s wall, 10 workers
27e296087afa6369ce93b3f9aaf402eec3c6b78c8c734202e910742d02f7c6df  data/R09_validity_stopping.csv
dad44f3d05e14863c8fbbd9e91ba38a5298457255f02980891b56ad0ed544264  data/R09_eprocess_race.csv
af880acfcbe2136b4ccd10a17ff6f8058b72fe669a44e9acc6e2d3f7729c5c70  data/R09_level_granularity.csv
b0b486eca9404c8bc7c96799d20af9cf783ad4ec299ff7a2d7eedec623dbbcaa  data/R09_arl0.csv
90f7dd73e8d8f811113ddc629d88894d295cff05c9e481b9c7dbe629ada718f6  data/R09_eprocess_race_control_ecusum.csv
95dadf2706062b7b7ab406da6f97f13d5057849869e0dac4db7cae64836927ee  figures/fig09_anytime_valid.png
34b92176ccefee604f8034a97463efe72a760b7f5326a6fb655b511d20e80cfe  tables/R09_claims.tex
```

### Axis 2 — `./run_experiment_R09.sh --n-jobs 1`

`NUM_CHUNKS = 10` fixes the chunk decomposition, so the number of worker processes cannot move a
number. Run C, `2026-08-08T00:55:09Z → 01:15:43Z`, `1233.6 s` wall at **one** worker against
`314.0 s` at ten. **All seven digests are byte-identical to the axis-1 set above:**

```
27e296087afa6369ce93b3f9aaf402eec3c6b78c8c734202e910742d02f7c6df  data/R09_validity_stopping.csv
dad44f3d05e14863c8fbbd9e91ba38a5298457255f02980891b56ad0ed544264  data/R09_eprocess_race.csv
af880acfcbe2136b4ccd10a17ff6f8058b72fe669a44e9acc6e2d3f7729c5c70  data/R09_level_granularity.csv
b0b486eca9404c8bc7c96799d20af9cf783ad4ec299ff7a2d7eedec623dbbcaa  data/R09_arl0.csv
90f7dd73e8d8f811113ddc629d88894d295cff05c9e481b9c7dbe629ada718f6  data/R09_eprocess_race_control_ecusum.csv
95dadf2706062b7b7ab406da6f97f13d5057849869e0dac4db7cae64836927ee  figures/fig09_anytime_valid.png
34b92176ccefee604f8034a97463efe72a760b7f5326a6fb655b511d20e80cfe  tables/R09_claims.tex
```

### Axis 3 — the run **without** `--control-arms`

The e-CUSUM H1 arm recurses on the same per-chunk `y_t` and consumes no additional randomness, so a
run that does not compute it must produce byte-identical published CSVs. `--control-arms` governs
what is **computed**, not merely what is persisted (the R16 `--dating` precedent), so this axis is
what shows the control branch leaks no state into the published path. Run D,
`2026-08-08T01:15:43Z → 01:20:56Z`, `311.2 s` wall at ten workers, `control arm computed: False`.
**The four published CSVs, the figure and the macro table are byte-identical to the axis-1 set:**

```
27e296087afa6369ce93b3f9aaf402eec3c6b78c8c734202e910742d02f7c6df  data/R09_validity_stopping.csv
dad44f3d05e14863c8fbbd9e91ba38a5298457255f02980891b56ad0ed544264  data/R09_eprocess_race.csv
af880acfcbe2136b4ccd10a17ff6f8058b72fe669a44e9acc6e2d3f7729c5c70  data/R09_level_granularity.csv
b0b486eca9404c8bc7c96799d20af9cf783ad4ec299ff7a2d7eedec623dbbcaa  data/R09_arl0.csv
95dadf2706062b7b7ab406da6f97f13d5057849869e0dac4db7cae64836927ee  figures/fig09_anytime_valid.png
34b92176ccefee604f8034a97463efe72a760b7f5326a6fb655b511d20e80cfe  tables/R09_claims.tex
```

`R09_eprocess_race_control_ecusum.csv` is **not written by this run** and retains the digest the
certified runs gave it (`90f7dd73…`), which is the point of the axis.

A **fifth run** of the certified command follows the four the plan's §10 lists, so the delivered
`logs/R09_eprocess_anytime/exp_R09_eprocess_anytime.log` is the certified configuration's own log
rather than run D's. Its digests are the axis-1 set again.

### The re-serialisation reconciliation, inside the process

The figure and the seven macros are computed from the in-memory frames, never from a reloaded CSV
(§S7, SPECS §1.6). The frames are then re-serialised to a scratch file and their digests compared
with the files just written; a mismatch exits `1`. All five CSVs reconcile, so **the figure and the
macros are certified to describe the persisted campaign rather than assumed to.**

---

## 8. Figure verdict

`fig09_anytime_valid.png` is the 9th `\caption` in document order — `fig:leverage` and
`fig:fat_tails` are two captions inside one `figure*`, which is why `fig:oracle_frontier` is 14 and
R13 ships `fig14_*`. Three panels, drawn from the in-memory frames.

- **(A)** grouped bars, three arms × three stopping protocols at `α = 0.05`, Wilson error bars,
  a dashed rule at `α`, `n = 20 000` on the axis.
- **(B)** `ADD` vs `η` at `α = 0.05`, **CUSUM and MIX only**, SEM error bars, `n = 2 000` on the
  axis, and an annotation stating that `ADD` is conditional on an alarm in `(τ, H]`.
- **(C)** `ARL₀` vs `α`, log–log, three arms plus the `1/α` reference; a dotted rule at
  `4H = 20 000` labelled "simulation horizon — right-censoring ceiling"; hollow markers on a lighter
  dashed line for the two arms above `50%` censoring; the per-arm censoring range in each legend
  entry; and a legend line reading "hollow: >50% right-censored (horizon artefact)".

Divergence from the submitted `Fig27_Eprocess_AnytimeValid.png` is **presentational only** — bold
lettered panel titles, the per-panel `n` on each axis, and panel C's censoring markers — and is
covered by the existing `ALL-figure-presentation` register row. No numerical content changes on that
account.

---

## 9. Open questions, left open

1. **Why does M1(ii) measure `0.0478` at `α = 0.05` in the submitted campaign while the H₀ campaign's
   MIX peeking gives `0.04945` on the same `n`?** Two independent replicates differing by `1.1` SE is
   unremarkable, and the port reproduces the same structure (M1(ii) and the H₀ campaign are keyed
   disjointly and both are reported). The audit states it rather than averaging them, and both
   replicates ship.

2. **Is the mixture's conservatism attributable to the discrete `16 × 3 × 2` support, to the finite
   peeking horizon, or to both?** `FPR/α` sits between `0.945` and `1.000`. Nothing in this stream
   separates the two mechanisms, and §S4.5 forbids asserting one the measurement does not establish.

3. **Does a single-look-at-`4H` protocol belong in the published panel?** The "extended" protocol is
   the crossing state at exactly `t = 4H`, not a cumulative probability. v87 does not describe it and
   panel A plots it. The question is posed, not settled.

4. **Whether an executable belongs under `data/reference/`.** Already open at `AUDIT_R06.md` §8.4 and
   restated for R11, R16, R13 and R07. R09 adds one more, because C5 needs a repo-relative witness
   and §S7 bans absolute paths. Not settled here either.

5. **What fraction of the `18\% → 20\%` displacement is the lattice step in `λ*` and what fraction
   is the fresh H₀ draw?** Separating them needs the regenerated H₀ running maxima replayed at
   `λ* = 11.4`. The running maxima exist in memory during the run — the structural cross-check reads
   them — but they are not persisted, so the decomposition is not recoverable from the shipped
   artefacts. Whether to persist them is a design question this stream does not settle.

6. **Where does this file belong?** The plan places `AUDIT_R09.md` at the repository root and
   `tests/test_R09_claims.py` asserts it there; every other stream's audit has since been
   consolidated under `docs/audits/`. Consolidating this one is a one-line move plus the matching
   path in the test, and it is left to whoever closes the register.

---

## 10. `pytest tests/ -v`, pasted verbatim

The suite was run in full after the final certified campaign, on the artefacts this
repository ships. **280 passed, 0 failed.** The R09 file contributes **31** tests: 25 blocking,
2 self-invalidating, 4 reporting-only. Four of the 25 blocking ones additionally carry a
self-invalidation clause in their failure message, naming the document that must change if they ever
fire — `test_R09_the_macro_emitter_refuses_a_censored_arl0` (if CUSUM or MIX censoring fell below the
`50%` ceiling, the reason their `ARL₀` means are withheld would have changed),
`test_R09_the_level_granularity_column_states_the_lattice_it_names` (if a CUSUM level became exactly
attainable, the `R03-cusum-nominal-level` reading would have changed),
`test_R09_the_add_column_is_conditional_and_the_detection_rate_says_so` (if the two arms came to
detect at comparable rates at the smallest drift, §3 C4's reading would change), and
`test_R09_the_ecusum_censored_fraction_is_not_zero` (if the witness's e-CUSUM censoring became zero,
§6 finding 2 would be withdrawn).

**No blocking assertion rests on a value R09 produced.** Each rests either on a value v87 prints,
compared at v87's own printing precision, or on a relation reimplemented in the test file
independently of the experiment: the Wilson interval from the closed-form roots of the score
equation rather than from a centre plus margin; Ville's threshold with `logsumexp` written out as
`log(sum(exp(...)))` on a small case; the CUSUM recursion stepped through on a hand-built binary
sequence; `D⁺` from a counting formula rather than from `ksone`; and the `ARL₀` lower bound
`censored_frac · T_ext` recomputed from the persisted columns. **The witness is never a blocking
anchor** — `data/reference/README.md` fixes that rule, and R09's re-keying redraws every
Monte-Carlo value by construction, which is exactly what the three delivered literal gates at
`Priorite_22` l.619 and l.631 would have collided with.

```
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-9.0.3, pluggy-1.6.0 -- /home/m53/miniforge3/envs/Trading/bin/python3
cachedir: .pytest_cache
rootdir: /home/m53/The-Whitening-Advantage-Experiments
plugins: anyio-4.8.0
collecting ... collected 280 items

tests/test_R01_claims.py::test_r01_models PASSED                         [  0%]
tests/test_R01_claims.py::test_r01_trajectories PASSED                   [  0%]
tests/test_R01_claims.py::test_r01_injection_summary PASSED              [  1%]
tests/test_R01_claims.py::test_r01_placebo PASSED                        [  1%]
tests/test_R01_claims.py::test_r01_magnitude_and_symmetry PASSED         [  1%]
tests/test_R02_claims.py::test_stream_counts PASSED                      [  2%]
tests/test_R02_claims.py::test_classifier_integrity PASSED               [  2%]
tests/test_R02_claims.py::test_data_rejection_rates PASSED               [  2%]
tests/test_R02_claims.py::test_distinct_p_concept PASSED                 [  3%]
tests/test_R02_claims.py::test_independence_diagnostics PASSED           [  3%]
tests/test_R02_claims.py::test_iid_arm_rejection_is_reported_not_asserted PASSED [  3%]
tests/test_R02_claims.py::test_concept_level_covered_by_wilson PASSED    [  4%]
tests/test_R02_claims.py::test_max_clustered_pvalue_below_manuscript_bound PASSED [  4%]
tests/test_R02b_claims.py::test_negative_control_integrity PASSED        [  5%]
tests/test_R02b_claims.py::test_nu_seven_is_indistinguishable_from_nominal PASSED [  5%]
tests/test_R02b_claims.py::test_heavy_tail_arms_exclude_nominal PASSED   [  5%]
tests/test_R02b_claims.py::test_rate_ordering_heavy_versus_light PASSED  [  6%]
tests/test_R02b_claims.py::test_negative_control_matches_squared_at_light_tails PASSED [  6%]
tests/test_R02c_claims.py::test_R02c_seed_uniqueness PASSED              [  6%]
tests/test_R02c_claims.py::test_R02c_negative_control_calibration PASSED [  7%]
tests/test_R02c_claims.py::test_R02c_eighth_moment_account_is_refuted PASSED [  7%]
tests/test_R02c_claims.py::test_R02c_slope_test_power_is_declared PASSED [  7%]
tests/test_R02c_claims.py::test_R02c_control_arm_integrity PASSED        [  8%]
tests/test_R02c_claims.py::test_R02c_continuity PASSED                   [  8%]
tests/test_R02c_claims.py::test_R02c_mechanism_slope_logic PASSED        [  8%]
tests/test_R03_claims.py::test_R03_grid_cardinality PASSED               [  9%]
tests/test_R03_claims.py::test_R03_grid_is_unchanged PASSED              [  9%]
tests/test_R03_claims.py::test_R03_threshold_ordering_is_structural PASSED [ 10%]
tests/test_R03_claims.py::test_R03_monotonicity_beyond_gamma_six PASSED  [ 10%]
tests/test_R03_claims.py::test_R03_aggregate_certification_gates PASSED  [ 10%]
tests/test_R03_claims.py::test_R03_gamma_rule_holds_the_nominal_level PASSED [ 11%]
tests/test_R03_claims.py::test_R03_iid_calibration_arm_is_well_formed PASSED [ 11%]
tests/test_R03_claims.py::test_R03_deviation_classification_against_witness PASSED [ 11%]
tests/test_R03_claims.py::test_R03_macros_are_emitted PASSED             [ 12%]
tests/test_R04_claims.py::test_R04_cardinalities PASSED                  [ 12%]
tests/test_R04_claims.py::test_R04_grids_match_v87 PASSED                [ 12%]
tests/test_R04_claims.py::test_R04_horizon_and_sample_size PASSED        [ 13%]
tests/test_R04_claims.py::test_R04_reference_drifts_are_coherent PASSED  [ 13%]
tests/test_R04_claims.py::test_R04_all_arms_are_iso_fpr PASSED           [ 13%]
tests/test_R04_claims.py::test_R04_concept_threshold_is_flat_in_gamma PASSED [ 14%]
tests/test_R04_claims.py::test_R04_concept_level_is_homogeneous_in_gamma PASSED [ 14%]
tests/test_R04_claims.py::test_R04_recalib_blind_zone_persists_at_lowest_gamma PASSED [ 15%]
tests/test_R04_claims.py::test_R04_recalib_is_slower_than_both_first_order_arms PASSED [ 15%]
tests/test_R04_claims.py::test_R04_add_decreases_with_drift_magnitude PASSED [ 15%]
tests/test_R04_claims.py::test_R04_conditional_mean_is_labelled_and_accompanied PASSED [ 16%]
tests/test_R04_claims.py::test_R04_efficiency_ratio_is_monotone_in_nu PASSED [ 16%]
tests/test_R04_claims.py::test_R04_ratio_respects_the_gaussian_ceiling PASSED [ 16%]
tests/test_R04_claims.py::test_R04_predicted_ratio_is_the_pitman_constant PASSED [ 17%]
tests/test_R04_claims.py::test_R04_oracle_is_never_slower_than_the_fitted_arm PASSED [ 17%]
tests/test_R04_claims.py::test_R04_analytic_crossing_matches_v87 PASSED  [ 17%]
tests/test_R04_claims.py::test_R04_blind_zone_onset_matches_v87 PASSED   [ 18%]
tests/test_R04_claims.py::test_R04_macros_are_emitted_and_computed PASSED [ 18%]
tests/test_R04_claims.py::test_R04_crossings_agree_with_the_interpolation_rule PASSED [ 18%]
tests/test_R04_claims.py::test_R04_emitted_crossing_brackets_contain_the_crossing PASSED [ 19%]
tests/test_R04_claims.py::test_R04_table3_printing_rule_reproduces_v87 PASSED [ 19%]
tests/test_R04_claims.py::test_R04_table3_is_generated_from_the_csv PASSED [ 20%]
tests/test_R04_claims.py::test_R04_table3_shows_detrate_exactly_when_below_one PASSED [ 20%]
tests/test_R04_claims.py::test_R04_intervals_are_clamped_and_ordered PASSED [ 20%]
tests/test_R04_claims.py::test_R04_no_nan_in_reported_delays PASSED      [ 21%]
tests/test_R04_claims.py::test_R04_m0_universality_arm_matches_the_garch_arm PASSED [ 21%]
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
PASSED       [ 21%]
tests/test_R04b_claims.py::test_R04b_cardinality_and_grid PASSED         [ 22%]
tests/test_R04b_claims.py::test_R04b_protocol_constants_match_v87 PASSED [ 22%]
tests/test_R04b_claims.py::test_R04b_gamma_target_is_attainable_and_realised PASSED [ 22%]
tests/test_R04b_claims.py::test_R04b_analytic_prediction_is_the_pitman_constant PASSED [ 23%]
tests/test_R04b_claims.py::test_R04b_in_sample_bisection_converged PASSED [ 23%]
tests/test_R04b_claims.py::test_R04b_pooled_holdout_level_meets_the_promised_band PASSED [ 23%]
tests/test_R04b_claims.py::test_R04b_conditional_calibration_pvalues_are_uniform PASSED [ 24%]
tests/test_R04b_claims.py::test_R04b_rates_are_consistent_and_clamped PASSED [ 24%]
tests/test_R04b_claims.py::test_R04b_continuity_anchors_are_read_from_R04 PASSED [ 25%]
tests/test_R04b_claims.py::test_R04b_is_compatible_with_R04_at_the_common_points PASSED [ 25%]
tests/test_R04b_claims.py::test_R04b_grid_bracket_straddles_unity_and_the_interpolation_lies_inside_it PASSED [ 25%]
tests/test_R04b_claims.py::test_R04b_inferential_bracket_is_recomputable_from_the_csv PASSED [ 26%]
tests/test_R04b_claims.py::test_R04b_bootstrap_error_exceeds_the_conditional_one PASSED [ 26%]
tests/test_R04b_claims.py::test_R04b_shape_fit_is_reported_with_its_goodness PASSED [ 26%]
tests/test_R04b_claims.py::test_R04b_analytic_crossing_matches_v87 PASSED [ 27%]
tests/test_R04b_claims.py::test_R04b_estimation_cost_interval_arithmetic PASSED [ 27%]
tests/test_R04b_claims.py::test_R04b_ratio_respects_the_gaussian_ceiling PASSED [ 27%]
tests/test_R04b_claims.py::test_R04b_oracle_ratio_does_not_cross_again_above_seven PASSED [ 28%]
tests/test_R04b_claims.py::test_R04b_macros_are_emitted_and_computed PASSED [ 28%]
tests/test_R04b_claims.py::test_R04b_no_nan_in_reported_quantities PASSED [ 28%]
tests/test_R04b_claims.py::test_R04b_report_against_v87 PASSED           [ 29%]
tests/test_R05_claims.py::test_abrupt_cardinality PASSED                 [ 29%]
tests/test_R05_claims.py::test_ramp_cardinalities PASSED                 [ 30%]
tests/test_R05_claims.py::test_protocol_constants PASSED                 [ 30%]
tests/test_R05_claims.py::test_horizons_are_the_two_published_budgets PASSED [ 30%]
tests/test_R05_claims.py::test_common_horizon_is_constant_across_gamma PASSED [ 31%]
tests/test_R05_claims.py::test_null_levels_are_homogeneous_across_gamma PASSED [ 31%]
tests/test_R05_claims.py::test_concept_branch_is_gamma_invariant_by_construction PASSED [ 31%]
tests/test_R05_claims.py::test_concept_is_blind_to_the_scale_pathology PASSED [ 32%]
tests/test_R05_claims.py::test_positive_control_shows_the_monitor_responsive PASSED [ 32%]
tests/test_R05_claims.py::test_both_crossovers_are_emitted_and_are_distinct PASSED [ 32%]
tests/test_R05_claims.py::test_scaling_law_branches_meet_at_the_crossover PASSED [ 33%]
tests/test_R05_claims.py::test_ladder_visits_the_three_published_horizons PASSED [ 33%]
tests/test_R05_claims.py::test_ladder_is_monotone_in_the_horizon PASSED  [ 33%]
tests/test_R05_claims.py::test_ladder_agrees_with_the_campaigns_it_overlaps PASSED [ 34%]
tests/test_R05_claims.py::test_sixth_moment_boundary_matches_the_published_gamma PASSED [ 34%]
tests/test_R05_claims.py::test_moment_margin_macro_matches_the_published_bound PASSED [ 35%]
tests/test_R05_claims.py::test_macro_file_is_well_formed PASSED          [ 35%]
tests/test_R05_claims.py::test_required_macros_are_present PASSED        [ 35%]
tests/test_R05_claims.py::test_figure_exists PASSED                      [ 36%]
tests/test_R05_claims.py::test_text_artefacts_end_with_a_newline PASSED  [ 36%]
tests/test_R05_claims.py::test_superseded_witness_is_documented_not_regenerated PASSED [ 36%]
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
PASSED    [ 37%]
tests/test_R06_claims.py::test_R06_cardinalities_and_grid PASSED         [ 37%]
tests/test_R06_claims.py::test_R06_gamma_grid_is_realised_in_closed_form PASSED [ 37%]
tests/test_R06_claims.py::test_R06_fourth_moment_boundary_is_computed_not_hard_coded PASSED [ 38%]
tests/test_R06_claims.py::test_R06_boundary_is_not_confused_with_the_nearest_grid_point PASSED [ 38%]
tests/test_R06_claims.py::test_R06_panel_A_design_is_paired_and_declared PASSED [ 38%]
tests/test_R06_claims.py::test_R06_pooled_binary_level_covers_nominal_at_cluster_precision PASSED [ 39%]
tests/test_R06_claims.py::test_R06_counterfactual_arm_removes_the_pairing PASSED [ 39%]
tests/test_R06_claims.py::test_R06_no_per_gamma_gate_is_possible PASSED  [ 40%]
tests/test_R06_claims.py::test_R06_squared_stream_rejects_massively PASSED [ 40%]
tests/test_R06_claims.py::test_R06_task_boundaries_saturate PASSED       [ 40%]
tests/test_R06_claims.py::test_R06_intermediate_threshold_is_reported_and_labelled PASSED [ 41%]
tests/test_R06_claims.py::test_R06_median_task_control_covers_nominal_and_is_weakly_resolved PASSED [ 41%]
tests/test_R06_claims.py::test_R06_no_silent_fallback_survived_into_the_artefacts PASSED [ 41%]
tests/test_R06_claims.py::test_R06_reproduces_the_witness_byte_for_byte PASSED [ 42%]
tests/test_R06_claims.py::test_R06_macros_are_emitted_and_computed PASSED [ 42%]
tests/test_R06_claims.py::test_R06_report_against_the_witness PASSED     [ 42%]
tests/test_R07_claims.py::test_R07_every_artefact_the_plan_lists_exists_with_its_prescribed_schema PASSED [ 43%]
tests/test_R07_claims.py::test_R07_the_lattice_law_reproduces_under_an_independent_dynamic_program PASSED [ 43%]
tests/test_R07_claims.py::test_R07_the_two_attainable_levels_bracket_five_percent_and_fix_lambda_star PASSED [ 43%]
tests/test_R07_claims.py::test_R07_the_dynamic_program_agrees_with_exhaustive_enumeration PASSED [ 44%]
tests/test_R07_claims.py::test_R07_the_fourth_moment_product_of_L308_reproduces_in_closed_form PASSED [ 44%]
tests/test_R07_claims.py::test_R07_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 45%]
tests/test_R07_claims.py::test_R07_the_naive_arm_and_the_oracle_arm_coincide_at_phi_zero PASSED [ 45%]
tests/test_R07_claims.py::test_R07_the_oracle_arm_is_exactly_phi_invariant PASSED [ 45%]
tests/test_R07_claims.py::test_R07_the_design_effect_is_measured_on_every_pooled_quantity PASSED [ 46%]
tests/test_R07_claims.py::test_R07_the_ljungbox_rejection_of_L308_climbs_monotonically_in_phi PASSED [ 46%]
tests/test_R07_claims.py::test_R07_every_ols_cell_matches_the_oracle_band_of_the_figure7_caption PASSED [ 46%]
tests/test_R07_claims.py::test_R07_the_ols_envelopes_stay_inside_the_two_bands_L308_prints PASSED [ 47%]
tests/test_R07_claims.py::test_R07_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 47%]
tests/test_R07_claims.py::test_R07_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 47%]
tests/test_R07_claims.py::test_R07_every_produced_text_file_ends_in_a_newline PASSED [ 48%]
tests/test_R07_claims.py::test_R07_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 48%]
tests/test_R07_claims.py::test_R07_the_produced_sources_carry_no_banned_construct PASSED [ 48%]
tests/test_R07_claims.py::test_R07_the_comparison_operator_is_the_same_on_both_paths PASSED [ 49%]
tests/test_R07_claims.py::test_R07_the_seven_carried_primitives_are_byte_identical_to_the_witness PASSED [ 49%]
tests/test_R07_claims.py::test_R07_the_three_monte_carlo_numerals_of_L308_move_within_their_own_sampling_error PASSED [ 50%]
tests/test_R07_claims.py::test_R07_the_bias_bound_of_L308_is_exceeded_by_the_regenerated_campaign PASSED [ 50%]
tests/test_R07_claims.py::test_R07_the_exact_lattice_levels_differ_from_the_two_numerals_v87_prints PASSED [ 50%]
tests/test_R07_claims.py::test_R07_the_eta_decay_is_not_one_over_root_n PASSED [ 51%]
tests/test_R07_claims.py::test_R07_report_the_campaign_against_its_witness PASSED [ 51%]
tests/test_R07_claims.py::test_R07_report_the_design_effect_of_every_pooled_quantity PASSED [ 51%]
tests/test_R07_claims.py::test_R07_report_the_counterfactual_ladder PASSED [ 52%]
tests/test_R07_claims.py::test_R07_report_the_candidate_readings_of_the_dispersion_cost_numeral PASSED [ 52%]
tests/test_R07_claims.py::test_R07_report_the_float_drift_on_the_lattice_boundary PASSED [ 52%]
tests/test_R09_claims.py::test_R09_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 53%]
tests/test_R09_claims.py::test_R09_every_sample_size_the_campaign_used_is_carried_on_the_row PASSED [ 53%]
tests/test_R09_claims.py::test_R09_the_mixture_martingale_remains_bounded_by_alpha_under_continuous_monitoring PASSED [ 53%]
tests/test_R09_claims.py::test_R09_only_the_mixture_controls_the_time_uniform_rate PASSED [ 54%]
tests/test_R09_claims.py::test_R09_the_ecusum_arl0_satisfies_the_reciprocal_of_alpha PASSED [ 54%]
tests/test_R09_claims.py::test_R09_the_peeking_horizon_is_four_times_the_calibration_horizon PASSED [ 55%]
tests/test_R09_claims.py::test_R09_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 55%]
tests/test_R09_claims.py::test_R09_the_mixture_threshold_is_villes_threshold_on_the_mixture_value PASSED [ 55%]
tests/test_R09_claims.py::test_R09_the_cusum_statistic_lives_on_the_two_delta_lattice PASSED [ 56%]
tests/test_R09_claims.py::test_R09_the_one_sided_kolmogorov_statistic_is_the_supremum_it_names PASSED [ 56%]
tests/test_R09_claims.py::test_R09_the_arl0_lower_bound_is_recomputed_from_the_persisted_columns PASSED [ 56%]
tests/test_R09_claims.py::test_R09_no_arl0_is_persisted_without_its_censored_fraction PASSED [ 57%]
tests/test_R09_claims.py::test_R09_the_macro_emitter_refuses_a_censored_arl0 PASSED [ 57%]
tests/test_R09_claims.py::test_R09_the_bound_flag_is_a_computed_comparison_not_a_literal PASSED [ 57%]
tests/test_R09_claims.py::test_R09_the_level_granularity_column_states_the_lattice_it_names PASSED [ 58%]
tests/test_R09_claims.py::test_R09_the_descriptive_binomial_p_values_are_the_exact_one_sided_tail PASSED [ 58%]
tests/test_R09_claims.py::test_R09_the_add_column_is_conditional_and_the_detection_rate_says_so PASSED [ 58%]
tests/test_R09_claims.py::test_R09_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 59%]
tests/test_R09_claims.py::test_R09_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 59%]
tests/test_R09_claims.py::test_R09_the_ecusum_censored_fraction_is_not_zero PASSED [ 60%]
tests/test_R09_claims.py::test_R09_every_produced_text_file_ends_in_a_newline PASSED [ 60%]
tests/test_R09_claims.py::test_R09_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 60%]
tests/test_R09_claims.py::test_R09_the_produced_sources_carry_no_banned_construct PASSED [ 61%]
tests/test_R09_claims.py::test_R09_the_orchestrator_passes_the_control_arm_and_never_calls_pytest PASSED [ 61%]
tests/test_R09_claims.py::test_R09_the_shared_orchestrators_are_untouched PASSED [ 61%]
tests/test_R09_claims.py::test_R09_the_three_monte_carlo_numerals_of_L243_does_not_reproduce_at_printed_precision PASSED [ 62%]
tests/test_R09_claims.py::test_R09_the_calibrated_level_and_the_stream_count_still_reproduces_v87s_numerals PASSED [ 62%]
tests/test_R09_claims.py::test_R09_report_the_campaign_against_its_witness PASSED [ 62%]
tests/test_R09_claims.py::test_R09_report_the_published_numerals_at_their_printed_precision PASSED [ 63%]
tests/test_R09_claims.py::test_R09_report_the_censoring_that_makes_panel_c_a_horizon_artefact PASSED [ 63%]
tests/test_R09_claims.py::test_R09_report_the_control_outcomes_the_log_records PASSED [ 63%]
tests/test_R11_claims.py::test_R11_cardinalities_and_arms PASSED         [ 64%]
tests/test_R11_claims.py::test_R11_gamma_grid_is_the_target_grid_and_its_floor_is_respected PASSED [ 64%]
tests/test_R11_claims.py::test_R11_gamma_range_matches_the_published_multiplier PASSED [ 65%]
tests/test_R11_claims.py::test_R11_as_submitted_arm_is_the_per_detector_mixture PASSED [ 65%]
tests/test_R11_claims.py::test_R11_putting_both_detectors_on_one_convention_moves_the_cusum PASSED [ 65%]
tests/test_R11_claims.py::test_R11_the_published_ordering_holds_on_the_arm_that_produced_it PASSED [ 66%]
tests/test_R11_claims.py::test_R11_crn_h0_arm_is_degenerate_and_the_independent_arm_is_not PASSED [ 66%]
tests/test_R11_claims.py::test_R11_kish_design_effect_of_a_degenerate_grid_is_its_width PASSED [ 66%]
tests/test_R11_claims.py::test_R11_pht_intervals_carry_the_calibration_variance_factor PASSED [ 67%]
tests/test_R11_claims.py::test_R11_every_interval_bound_is_clamped PASSED [ 67%]
tests/test_R11_claims.py::test_R11_data_loglog_slopes_reproduce_by_an_independent_fit PASSED [ 67%]
tests/test_R11_claims.py::test_R11_pht_data_slope_is_fitted_on_a_restricted_domain PASSED [ 68%]
tests/test_R11_claims.py::test_R11_low_gamma_sensitivity_arm_excludes_exactly_the_unattainable_point PASSED [ 68%]
tests/test_R11_claims.py::test_R11_bootstrap_standard_errors_are_present_and_the_ratio_is_reported PASSED [ 68%]
tests/test_R11_claims.py::test_R11_no_macro_restates_the_cusum_scaling_law PASSED [ 69%]
tests/test_R11_claims.py::test_R11_submitted_linear_fits_are_reproduced_for_traceability PASSED [ 69%]
tests/test_R11_claims.py::test_R11_peak_to_peak_spread_is_descriptive_and_arithmetically_correct PASSED [ 70%]
tests/test_R11_claims.py::test_R11_preonset_leak_is_recorded_for_every_detector_even_at_zero PASSED [ 70%]
tests/test_R11_claims.py::test_R11_onset_table_carries_a_paired_error PASSED [ 70%]
tests/test_R11_claims.py::test_R11_the_two_adwin_implementations_are_labelled PASSED [ 71%]
tests/test_R11_claims.py::test_R11_river_version_is_recorded_in_the_artefacts PASSED [ 71%]
tests/test_R11_claims.py::test_R11_macros_are_emitted_with_the_preamble_ordinal PASSED [ 71%]
tests/test_R11_claims.py::test_R11_concept_add_macros_match_their_arm PASSED [ 72%]
tests/test_R11_claims.py::test_R11_eddm_macros_come_from_the_independent_seed_arm PASSED [ 72%]
tests/test_R11_claims.py::test_R11_report_against_v87 PASSED             [ 72%]
tests/test_R13_claims.py::test_R13_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 73%]
tests/test_R13_claims.py::test_R13_the_detector_labels_carry_the_families_the_manuscript_fixes PASSED [ 73%]
tests/test_R13_claims.py::test_R13_the_published_delay_and_false_alarm_probability_come_from_one_row PASSED [ 73%]
tests/test_R13_claims.py::test_R13_the_two_covid_detection_delays_v87_prints_reproduce PASSED [ 74%]
tests/test_R13_claims.py::test_R13_the_jensen_ratio_v87_prints_reproduces_and_is_specific_to_one_oracle PASSED [ 74%]
tests/test_R13_claims.py::test_R13_the_phase_false_alarm_probability_of_L331_does_not_reproduce_at_its_printed_precision PASSED [ 75%]
tests/test_R13_claims.py::test_R13_the_census_verdicts_of_L331_reproduce_at_the_matched_operating_point PASSED [ 75%]
tests/test_R13_claims.py::test_R13_the_2011_correction_alarms_at_dead_bands_the_caption_does_not_name PASSED [ 75%]
tests/test_R13_claims.py::test_R13_the_D2_increment_is_the_gaussian_log_likelihood_ratio PASSED [ 76%]
tests/test_R13_claims.py::test_R13_the_frozen_volatility_path_recomputes_from_the_persisted_parameters PASSED [ 76%]
tests/test_R13_claims.py::test_R13_the_four_operating_points_are_the_rules_they_name PASSED [ 76%]
tests/test_R13_claims.py::test_R13_no_arl0_is_persisted_without_its_censored_fraction PASSED [ 77%]
tests/test_R13_claims.py::test_R13_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 77%]
tests/test_R13_claims.py::test_R13_the_certification_gates_are_equivalence_statements_with_a_null_law PASSED [ 77%]
tests/test_R13_claims.py::test_R13_the_census_quantities_are_r16s_canonical_arm PASSED [ 78%]
tests/test_R13_claims.py::test_R13_the_oracle_verdict_and_the_clairvoyant_column_are_their_own_definitions PASSED [ 78%]
tests/test_R13_claims.py::test_R13_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 78%]
tests/test_R13_claims.py::test_R13_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 79%]
tests/test_R13_claims.py::test_R13_every_produced_text_file_ends_in_a_newline PASSED [ 79%]
tests/test_R13_claims.py::test_R13_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 80%]
tests/test_R13_claims.py::test_R13_the_produced_sources_carry_no_banned_construct PASSED [ 80%]
tests/test_R13_claims.py::test_R13_report_the_campaign_against_its_witness PASSED [ 80%]
tests/test_R13_claims.py::test_R13_report_the_threshold_neighbourhood_of_the_published_operating_point PASSED [ 81%]
tests/test_R13_claims.py::test_R13_report_the_certification_status_of_every_oracle PASSED [ 81%]
tests/test_R16_claims.py::test_R16_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 81%]
tests/test_R16_claims.py::test_R16_the_census_carries_the_phase_count_v87_prints PASSED [ 82%]
tests/test_R16_claims.py::test_R16_the_dating_algorithm_column_names_the_algorithm_of_every_row PASSED [ 82%]
tests/test_R16_claims.py::test_R16_the_out_of_budget_counts_reproduce_the_three_v87_prints PASSED [ 82%]
tests/test_R16_claims.py::test_R16_the_step_of_one_holds_on_the_count_and_fails_on_the_set PASSED [ 83%]
tests/test_R16_claims.py::test_R16_the_boundary_convention_flips_run_in_one_direction_only PASSED [ 83%]
tests/test_R16_claims.py::test_R16_the_unconditional_floor_is_the_sharpe_ceiling_of_the_corollary PASSED [ 83%]
tests/test_R16_claims.py::test_R16_the_sign_floor_is_the_bernoulli_divergence_of_the_manuscript PASSED [ 84%]
tests/test_R16_claims.py::test_R16_every_detectability_flag_is_its_own_floor_against_its_own_duration PASSED [ 84%]
tests/test_R16_claims.py::test_R16_the_census_statistics_recompute_from_the_raw_return_series PASSED [ 85%]
tests/test_R16_claims.py::test_R16_the_phases_partition_the_return_series_of_every_ticker PASSED [ 85%]
tests/test_R16_claims.py::test_R16_no_degenerate_phase_reaches_a_detectability_flag_without_measurement PASSED [ 85%]
tests/test_R16_claims.py::test_R16_the_turning_point_return_v87_cites_falls_where_the_convention_puts_it PASSED [ 86%]
tests/test_R16_claims.py::test_R16_the_long_secular_advance_v87_prints_reproduces PASSED [ 86%]
tests/test_R16_claims.py::test_R16_the_covid_phase_v87_prints_reproduces_to_its_printed_precision PASSED [ 86%]
tests/test_R16_claims.py::test_R16_the_two_numerical_evaluations_of_the_bound_reproduce_L260 PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_floor_fraction_envelope_of_L329_does_not_reproduce_at_its_lower_end PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_published_dating_description_is_unreachable_by_strict_pagan_sossounov PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_counterfactual_arms_are_the_rules_they_claim_to_be PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_macros_price_the_counterfactuals_they_name PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_headline_macros_agree_with_the_frames_they_are_computed_from PASSED [ 89%]
tests/test_R16_claims.py::test_R16_every_produced_text_file_ends_in_a_newline PASSED [ 89%]
tests/test_R16_claims.py::test_R16_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 90%]
tests/test_R16_claims.py::test_R16_the_produced_sources_carry_no_banned_construct PASSED [ 90%]
tests/test_R16_claims.py::test_R16_report_the_census_against_its_witness PASSED [ 90%]
tests/test_R16_claims.py::test_R16_report_the_three_dating_arms PASSED   [ 91%]
tests/test_R16_claims.py::test_R16_report_the_set_behind_the_step_of_one PASSED [ 91%]
tests/test_R18_claims.py::test_R18_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 91%]
tests/test_R18_claims.py::test_R18_the_grids_have_the_cardinality_their_specification_fixes PASSED [ 92%]
tests/test_R18_claims.py::test_R18_the_amplitude_grid_is_the_one_the_design_specifies PASSED [ 92%]
tests/test_R18_claims.py::test_R18_the_lag_one_autocorrelation_column_is_twice_the_amplitude PASSED [ 92%]
tests/test_R18_claims.py::test_R18_the_non_centrality_column_closes_its_own_geometric_sum PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_analytic_power_column_is_the_non_central_chi_square_tail PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_analytic_power_is_monotone_in_both_of_its_arguments PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_deviation_column_is_the_difference_it_names PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_wilson_intervals_agree_with_the_roots_of_the_score_equation PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_size_of_the_test_covers_the_nominal_level_at_every_horizon PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_null_p_values_are_calibrated_against_the_kolmogorov_limit PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_empirical_curve_matches_the_analytic_one_inside_the_local_domain PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_detectable_amplitude_solves_its_own_analytic_equation PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_detectable_amplitude_halves_when_the_horizon_quadruples PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_non_centrality_at_eighty_percent_power_is_a_constant_of_the_test PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_application_arms_carry_the_two_grids_they_borrow PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_realised_penalty_matches_its_target_where_the_target_is_attainable PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_measured_sign_streams_sit_below_the_detectable_amplitude PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_power_at_the_measured_autocorrelation_is_the_analytic_one PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_ljung_box_rejection_of_both_arms_covers_the_nominal_level PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_headline_macros_agree_with_the_frames_they_are_computed_from PASSED [ 99%]
tests/test_R18_claims.py::test_R18_the_reported_detectable_amplitude_is_the_one_the_analytic_law_gives PASSED [ 99%]
tests/test_R18_claims.py::test_R18_report_the_bound_the_repository_can_state PASSED [100%]

======================= 280 passed in 109.90s (0:01:49) ========================
```
