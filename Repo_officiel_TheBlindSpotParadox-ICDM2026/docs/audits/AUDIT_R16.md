# AUDIT — R16, regime census and sign floor

This is the only document transmitted to the orchestrator. It contains: what R16 establishes and
what it does not; the nine controls with their margins and their trigger probability under their
own null; the deviation classification, including one **D3**; the reproducibility evidence with
the SHA-256 digests of every run pasted as-is and the full `run_tests.sh` output; a section
addressed to stream **R13**, which consumes this census; the design decisions taken outside the
plan; the findings that revise the plan's own premises; and the open questions, left open.

R16 carries the **most-cited empirical claim of `articleB_whitening_v87.tex`** — 80% of dated
directional episodes out of budget — which appears at L57 (abstract), L87 (contributions), L329
(body) and L374 (conclusion).

---

## 1. What R16 establishes, in one paragraph

Dating the bull and bear phases of SPY, PFF, VNQ and BWX over 2000–2025 with the delivered
multi-scale filter and pricing each phase against the Sharpe ceiling
`ADD_min >= 504 ln(1/alpha_0) / SR^2`, **every published value reproduces exactly**: `66` phases
(SPY 30, PFF 7, VNQ 18, BWX 11), `53` of `66` out of budget at `gamma = 20` (`80.3%`), `52` on
the exactly-priced sign arm, `64` at `gamma = 252` (`97.0%`), `504 ln 20 = 1509.85`,
`504 ln 252 = 2786.83`, SPY 2011–2018 at `0.541 -> 0.554` over `1753` days, and every numeral of
the COVID paragraph (`delta_q = -0.2803`, SR `-5.9904`, `23` days, `kl = 0.162042`, floors
`18.49` and `34.12`, `80.4%` of the phase). Read with `float_precision='round_trip'` on both
sides, the regenerated census is **bit-identical** to the submitted
`protocol_10b_regime_census_refined.csv` on all 19 shared columns and all 66 rows — worst numeric
difference `0` — and the same holds for the sign floor, the feasibility grid, the MESO split
report and the boundary-convention delta.

**What does not reproduce is v87 L329's account of how the 66 phases were dated.** L329 reads "A
retrospective multi-scale **Pagan--Sossounov** bull/bear dating … **of the four streams**
(2000--2025; `$66$` phases **after duration censoring** …)". A Pagan–Sossounov dating of the four
streams yields **48** phases. The 66 require substituting `lunde_timmermann(0.15, 0.15)` for
SPY's MACRO dating — SPY contributes 30 of the 66 — and Lunde–Timmermann applies no duration
censoring. That is a **Class A, D3** contradiction, registered as `R16-dating-misdescription`,
and the 48-phase counterfactual ships as its proof artefact.

The 66 **values** are not falsified. What is falsified is the description of the method.

---

## 2. Three things the reader must not take from this stream

**The D3 does not touch a number.** No count, no floor and no fraction of L260, L329 or L331
moves. A reader who takes `R16-dating-misdescription` as a correction of the 80% has misread it:
the 80% reproduces to the last bit. What is unreachable is the sentence that says the census
comes from a Pagan–Sossounov dating of four streams.

**No cause and no intent is attributed to the discrepancy.** Preamble §S4.5 forbids attributing a
mechanism the measurement does not establish. The evidence is equally consistent with a
description written from the design as intended rather than as executed, and this audit does not
choose between those readings. Two facts bear on it and are stated without being resolved: the
delivered script **announces** the substitution in its log (`data/reference/R16/Priorite_16_regime_census.log`,
line 3: `WARNING | [SPY] Sanity check P-S failed. Fallback to Lunde-Timmermann for MACRO.`), and
L329 itself flags the exception — "the COVID-19 crash---too brief for the filter---dated at the
*raw scale*", the raw scale being the uncensored Lunde–Timmermann dating. **The manuscript names
the exception; it does not name the algorithm.**

**The dating is an input, not a result, and it is the largest source of movement in the
headline.** The three arms give 80.3%, 79.2% and 73.5% on the same four price series and the
same ceiling. R16 establishes that the ceiling excludes most of what any of these three datings
finds; it does not establish that 80% is what a different reasonable dating would give. The
boundary-convention envelope (`[80.3%, 84.8%]`) is narrower than the dating spread and must not
be quoted as a total uncertainty.

---

## 3. Controls, with their margins and their trigger probabilities

**Which arm each control reads.** C1, C2, C3, C4, C5 and C7 read the **canonical 66-phase arm**,
which is the published configuration and the repository's baseline. C5 additionally recounts on
the two counterfactual arms, since its own statement is about all three. C6 reads **both
datings**, which are computed for every ticker on every run by construction — `check_sanity`
cannot be evaluated without the Pagan–Sossounov points, and the canonical arm cannot be built
without the Lunde–Timmermann points. C8 and C9 are structural. **The counterfactual arms are
measured and reported and they gate nothing.**

### C1 — partition of the return series, asserted and not observed

Per ticker: consecutive phases contiguous (`end_date[k] == start_date[k+1]`),
`sum(T_days) == idx(last end) − idx(first start)`, and the phase ids consecutive from zero so
that no phase can have been dropped between the dating and the census. The post-onset convention
of v87 L392 imposes it by construction.

| ticker | phases | contiguous | `sum(T_days)` | covered span | margin | head / tail outside |
| ------ | ------ | ---------- | ------------- | ------------ | ------ | ------------------- |
| SPY    | 30     | yes        | **6356**      | 6356         | **0**  | 56 / 1              |
| PFF    | 7      | yes        | **3930**      | 3930         | **0**  | 294 / 178           |
| VNQ    | 18     | yes        | **4483**      | 4483         | **0**  | 382 / 148           |
| BWX    | 11     | yes        | **4009**      | 4009         | **0**  | 243 / 198           |

The returns outside the covered span are the `min_edge = 126` edge censoring of the dating
filter, and they are logged as that rather than as a hole in the partition.

**Trigger probability under its own null: 0.** The control is a deterministic identity on integer
counts, not a statistical test. Failure means the double counting the post-onset convention
removes has survived, which would put a D3 on the 80%, and it exits `1`.

**A latent hole was closed rather than inherited.** `Priorite_16_regime_census.py:321` reads
`if T_a < 2: continue`, which drops a phase silently and tears the partition C1 asserts. It never
fires on this data — the shortest canonical phase is 6 trading days — and it is replaced by a
logged `sys.exit(1)`. A skipped phase is precisely what C1 exists to catch, and a control that
can be defeated by the code it audits is not a control.

The same identity holds on both counterfactual arms — margin `0` on all four tickers of each —
and is logged descriptively, without gating.

### C2 — reconstruction of the published counts

The comparison values are **read from the vendored witness**, `data/reference/R16/protocol_20b_census_feasibility_vs_gamma.csv`,
with `float_precision='round_trip'`, rather than typed into the producing script. Preamble §S7
requires anchors to come from v87 or from the reference CSV; §S6 forbids a hard-coded value.

| budget                        | regenerated | witness | displacement |
| ----------------------------- | ----------- | ------- | ------------ |
| `gamma = 20`, unconditional   | **53 / 66** | 53 / 66 | **+0**       |
| `gamma = 20`, sign            | **52 / 66** | 52 / 66 | **+0**       |
| `gamma = 252`, unconditional  | **64 / 66** | 64 / 66 | **+0**       |

The full feasibility grid reproduces as well: `n_detectable` = 13 / 14 / 2 / 2 / 0 / 1 across
`(gamma, budget)` in `{20, 252, 1260} x {unc, sign}`.

**Trigger probability under its own null: 0**, deterministic. **This is a portage check, not a
target.** A displaced count is logged with its displacement *before* being classified and is a
deviation to register, never a parameter to adjust; the script warns and continues rather than
exiting, so that a displacement cannot be hidden by a failed run.

### C3 — the step of one, and the set behind it

v87 L329: pricing the binarisation exactly "moves that count by one phase (`$52$` of `$66$`)".

**The step holds:** `sum(detectable_sign_g20) − sum(detectable_unc_g20) = 14 − 13 = 1`.

**The set does not.** The two arms disagree on **19 of the 66 phases** — 10 detectable on the
sign arm only, 9 on the unconditional arm only. The step of one is their **net**. There is no
single flipping phase to name, and a claim of "one phase" without one to name is not traceable,
which is why all 19 are persisted in the `arm_disagreement` column of `R16_sign_floor.csv`.

| arm         | ticker | phase                     | `T`  | SR      | `kl`     | floor unc | floor sign |
| ----------- | ------ | ------------------------- | ---- | ------- | -------- | --------- | ---------- |
| `sign_only` | SPY    | 2000-03-24 → 2001-04-04   | 259  | −1.4107 | 0.013380 | 758.72    | 223.89     |
| `sign_only` | SPY    | 2001-12-05 → 2002-07-23   | 157  | −2.9827 | 0.029270 | 169.72    | 102.35     |
| `sign_only` | SPY    | 2002-11-27 → 2003-03-11   | 69   | −2.8419 | 0.054393 | 186.95    | 55.08      |
| `sign_only` | SPY    | 2020-02-19 → 2020-03-23   | 23   | −5.9904 | 0.162042 | 42.08     | 18.49      |
| `sign_only` | SPY    | 2022-08-16 → 2022-10-12   | 40   | −4.7357 | 0.094843 | 67.32     | 31.59      |
| `sign_only` | PFF    | 2021-12-31 → 2022-10-21   | 203  | −2.1888 | 0.031503 | 315.16    | 95.09      |
| `sign_only` | VNQ    | 2007-02-07 → 2008-01-18   | 239  | −1.5846 | 0.014204 | 601.29    | 210.90     |
| `sign_only` | VNQ    | 2013-05-21 → 2013-08-19   | 62   | −3.8053 | 0.049541 | 104.27    | 60.47      |
| `sign_only` | VNQ    | 2021-12-31 → 2022-10-14   | 198  | −2.1176 | 0.021472 | 336.72    | 139.52     |
| `sign_only` | VNQ    | 2023-02-02 → 2023-10-25   | 183  | −1.8402 | 0.020652 | 445.85    | 145.06     |
| `unc_only`  | SPY    | 2001-05-21 → 2001-09-21   | 82   | −5.0262 | 0.032133 | 59.77     | 93.23      |
| `unc_only`  | SPY    | 2003-03-11 → 2007-10-09   | 1154 | +1.3300 | 0.000318 | 853.56    | 9407.22    |
| `unc_only`  | SPY    | 2011-10-03 → 2018-09-20   | 1753 | +1.2537 | 0.000328 | 960.55    | 9141.16    |
| `unc_only`  | SPY    | 2018-12-24 → 2020-02-19   | 289  | +2.6018 | 0.004493 | 223.04    | 666.81     |
| `unc_only`  | SPY    | 2020-03-23 → 2022-01-03   | 450  | +2.3037 | 0.005061 | 284.50    | 591.94     |
| `unc_only`  | SPY    | 2022-10-12 → 2025-02-19   | 589  | +1.7516 | 0.001735 | 492.09    | 1726.50    |
| `unc_only`  | PFF    | 2020-03-18 → 2021-12-31   | 452  | +1.9046 | 0.000003 | 416.22    | 1047138.90 |
| `unc_only`  | VNQ    | 2013-08-19 → 2015-01-26   | 361  | +2.2538 | 0.002410 | 297.25    | 1242.80    |
| `unc_only`  | BWX    | 2020-03-18 → 2021-01-05   | 201  | +3.1323 | 0.011679 | 153.89    | 256.52     |

The two sets separate by phase type and duration — **all 10** sign-only phases are bear phases
(median 170 days) and **8 of the 9** unc-only phases are bull phases (median 450 days). That is a
description of what was measured; no mechanism is asserted for it.

**Trigger probability under its own null: 0**, deterministic. Registered as
`R16-sign-arm-disagreement`, Class A, no severity: v87's sentence is true of the count and false
of the set, and no published value moves.

### C4 — convention sensitivity, with its direction. Not a gate

Three of the 66 phases change detectability with the boundary convention, and **all three change
in the same direction**: they *gain* detectability under the post-onset cut v87 L392 imposes.

| ticker | phase                     | boundary return | Sharpe, incl. → post-onset | floor, incl. → post-onset |
| ------ | ------------------------- | --------------- | -------------------------- | ------------------------- |
| PFF    | 2011-08-08 → 2013-05-08   | −0.098942       | `1.0254 → 1.9800`          | `1435.8 → 385.1`          |
| PFF    | 2020-03-18 → 2021-12-31   | −0.185834       | `0.9132 → 1.9046`          | `1810.7 → 416.2`          |
| BWX    | 2020-03-18 → 2021-01-05   | −0.054576       | `1.8179 → 3.1323`          | `456.9 → 153.9`           |

Envelope of the published count: **`[53, 56]` = `[80.3%, 84.8%]`**. The published figure is the
**conservative end** of its own sensitivity interval, so the sensitivity can only strengthen the
claim. `T_days` shortens by exactly 1 on all 66 phases, which is what "the return dated at a
turning point closes the regime it ends" means and is asserted as such.

**Not a gate**, by design: three flips in sixty-six is a measurement, not a failure.
Registered as `R16-boundary-sensitivity`, Class A, no severity — v87 declares the convention and
states its mechanism correctly at L392, and never reports the count. Camera-ready candidate
parked.

### C5 — degeneracies, counted even at zero, on all three arms

A phase whose Sharpe or divergence is non-finite would reach a detectability flag **without
measurement**: `NaN < T_days` is `False`, so the phase counts out of budget by default, which
inflates the very fraction the manuscript publishes. That is the degraded path preamble §S3's
asymmetry rule targets, and it is why the gate is on the mechanism rather than on an observed
count.

| count                                    | `canonical` | `strict_ps` | `symmetric` |
| ---------------------------------------- | ----------- | ----------- | ----------- |
| `sharpe` non-finite                      | **0**       | **0**       | **0**       |
| `ann_vol == 0`                           | **0**       | **0**       | **0**       |
| `sharpe` below `1e-12` (→ infinite floor)| **0**       | **0**       | **0**       |
| `ADD_min_days` non-finite                | **0**       | **0**       | **0**       |
| `kl_sign_nats_day` non-finite            | **0**       | **0**       | **0**       |
| `kl_sign_nats_day == 0` (→ infinite floor)| **0**      | **0**       | **0**       |
| `T_days == 0`                            | **0**       | **0**       | **0**       |
| `q_phase in {0, 1}`                      | **0**       | **0**       | **7**       |

**One count is non-zero, and it revises the plan.** The plan predicted all zeros on all three
arms. Seven phases of the `symmetric` arm have `q_phase` exactly 0 or 1 — PFF 2008-07-15→23 (6
days), PFF 2008-09-17→19 (2), PFF 2009-02-23→26 (3), VNQ 2008-10-09→13 (2), VNQ 2008-11-20→26
(4), VNQ 2008-11-26→12-01 (2), VNQ 2009-03-18→20 (2). All seven are 2-to-6-day episodes of the
2008–2009 crisis, which Lunde–Timmermann admits **because it applies no duration censoring** —
the same property that carries the D3. Their defined treatment is the clip to
`[1e-6, 1 − 1e-6]` inside the carried `compute_kl_sign`, so the divergence stays finite and the
detectability flag is decided by measurement. Four of the seven are counted **detectable**, which
moves the symmetric headline *down*, i.e. against the manuscript's thesis. The canonical arm,
which is the only arm anything downstream reads, carries zero degeneracies of every kind.

**Trigger probability under its own null: 0**, deterministic. The gate fires only on a non-finite
Sharpe or divergence reaching a flag, and it fires on any arm.

### C6 — concordance of the two datings. Not a gate, descriptive per §S4bis

Both datings are computed for every ticker on every run by construction. Concordance is the
fraction of one algorithm's turning points that have a turning point **of the same type** in the
other within a tolerance, on a ladder derived from the filters' own resolution — `0` (exact),
`42` (MESO `min_phase`), `84` (MACRO `min_phase`) trading days. **No rung is derived from an
observed agreement.** Wilson 95% intervals.

| ticker | `n_PS` | `n_LT` | PS→LT at 0 | at 42 | at 84 | LT→PS at 0 | at 42 | at 84 |
| ------ | ------ | ------ | ---------- | ----- | ----- | ---------- | ----- | ----- |
| SPY    | 9      | 31     | 7 (0.778)  | 0.778 | 0.778 | 7 (0.226)  | 0.226 | 0.323 |
| PFF    | 6      | 21     | 5 (0.833)  | 0.833 | 0.833 | 5 (0.238)  | 0.286 | 0.333 |
| VNQ    | 11     | 47     | 11 (1.000) | 1.000 | 1.000 | 11 (0.234) | 0.277 | 0.340 |
| BWX    | 12     | 7      | 5 (0.417)  | 0.417 | 0.417 | 5 (0.714)  | 0.714 | 0.714 |
| pooled | 38     | 106    | 28 (0.737) | 0.737 | 0.737 | 28 (0.264) | 0.292 | 0.358 |

Wilson intervals, exact rung: SPY `[0.453, 0.937]` / `[0.114, 0.398]`; PFF `[0.436, 0.970]` /
`[0.106, 0.451]`; VNQ `[0.741, 1.000]` / `[0.136, 0.372]`; BWX `[0.193, 0.680]` /
`[0.359, 0.918]`; pooled `[0.580, 0.850]` / `[0.190, 0.355]`. **The pooled row is description
only** and is logged as such: the four streams are not exchangeable, and a pooled interval
assumes an independence the turning points of one price series do not have.

**Restatement, required.** Under the canonical arm **SPY's census *is* the Lunde–Timmermann
dating**, so SPY's concordance *with the census* is 100% by construction and must be read as an
identity, not as corroboration. The table above compares the two **algorithms** on SPY's prices
and is informative in that sense only. **PFF, VNQ and BWX are where Pagan–Sossounov survives into
the canonical census, and they are where this control carries information about the dating the
census actually uses.**

What the table shows is asymmetric and worth naming: Lunde–Timmermann at `lambda = 0.15` finds
between 2 and 4 times as many turning points as Pagan–Sossounov on three of the four streams
(BWX is the exception, 7 against 12), and the Pagan–Sossounov points are largely a **subset** of
the Lunde–Timmermann ones (78–100% recovered exactly on SPY, PFF, VNQ) while the converse rate
runs at 23–34%. The two filters are not disagreeing about where the turning points are on those
three streams; they are disagreeing about how many of them survive censoring.

**Not a gate**, by design: two dating algorithms do not coincide, and a gate on their agreement
would ring empty (§S4bis). Descriptive only.

### C7 — the example v87 cites

v87 L392: "at troughs following a crash the turning-point return is an outlier (e.g. `$-18.6\%$`
on PFF, 2020-03-18) that both depresses the mean and inflates the variance of the phase that
follows, biasing its floor upward."

- The PFF log return dated 2020-03-18 is `-0.18583434620279932`, which prints as **`-18.6%`** at
  v87's precision.
- It **closes** PFF phase 3 (2013-05-08 → 2020-03-18) and is **excluded** from PFF phase 4
  (2020-03-18 → 2021-12-31). Both memberships are asserted, since a convention that assigned it
  to neither or to both would satisfy neither L392 nor C1.
- Excluding it moves phase 4's Sharpe `0.9132 -> 1.9046` and its floor `1810.7 -> 416.2` trading
  days. The outlier therefore biases the floor **upward**, which is the mechanism L392 states,
  measured.

**Trigger probability under its own null: 0**, deterministic.

### C8 — `ast` source-segment identity

Seven primitives, extracted **by position and never by import** — importing the legacy script
would execute its environment block, its logger, its output-directory creation and its
`try/except ImportError` data-loading fallback — and compared byte for byte:

| primitive               | owner                                                       |
| ----------------------- | ----------------------------------------------------------- |
| `enforce_alternance`    | `data/reference/R16/Priorite_16_regime_census.py`           |
| `pagan_sossounov`       | idem                                                        |
| `lunde_timmermann`      | idem                                                        |
| `get_episodes`          | idem                                                        |
| `check_sanity`          | idem                                                        |
| `compute_kl_sign`       | idem (carried by **both** `_a` and `_b`)                    |
| `wilson_score_interval` | `experiments/R02_whitening_ljungbox/exp_R02_whitening_ljungbox.py` |

**5 696 characters compared in `_a`, 0 differences; 241 in `_b`, 0 differences.** Preamble §S4.2
forbids hoisting any of them into `experiments/common/`, so the duplication is deliberate and it
cannot drift. The check covers the five primitives the plan names plus `check_sanity`, which is
carried and therefore owes the same guarantee, plus the Wilson interval, which is carried from
the experiment that owns this repository's copy.

**Vendoring is what makes the control possible.** Preamble §S7 bans absolute paths, so the
witness has to be repo-relative; `data/reference/R16/` is an **input** of this experiment, not an
archive.

**Trigger probability under its own null: 0** unless a copy has drifted, in which case it exits
`1`. The same control intercepted three transcription errors on R06 before any execution.

### C9 — reproducibility, on the only two axes that exist here

**The worker-count axis is vacuous and is stated as such rather than staged.** R16 has no
parallelism and no stochastic component: it draws no random number anywhere, and `--n-jobs` would
be a flag with no referent. Manufacturing one to satisfy the letter of the requirement would be
theatre.

**Axis 1 — two successive runs.** All eight artefacts identical, run to run:

```
62368994ccd2ef3ed79b594fd36579c342519b80e1e7ee3d006b8dbc43b56c3a  data/R16_boundary_convention_delta.csv
2c05ae6fe1a59b239899b5efc87c39903a065082cadefcdc2bd8d59f7ac1f2cc  data/R16_feasibility_vs_gamma.csv
128aa42d418ce400f931f4a62eb40fc6edd76d18a1226cf670b2ccedd57943c3  data/R16_meso_split_report.csv
e20112aad86f3227f683ae47587ff9771351db3cfe4343c35e7ffa8b099691d3  data/R16_regime_census.csv
739f14a148e2352ed8a16a75e35d6aa4366689cee1fa46e0ee2191b28263383d  data/R16_regime_census_strict_ps.csv
463f51aa26daf6241b12a0bccbcbea9844b67707a3050561beb9e04a2a6a6d00  data/R16_regime_census_symmetric.csv
dcbedf979a67558c09f2d412a814528b4119a8578b97cdca114a81144ff1a7cf  data/R16_sign_floor.csv
bf0a43cfa1bb5542f6734aec16a036ea48ec1d685be46f799ed801c554fb22a2  tables/R16_claims.tex
```

Run 2 produced the same eight digests, byte for byte; `diff` on the two digest sets is empty.

**Axis 2 — arm isolation.** Each arm invoked **alone** must reproduce, byte for byte, the CSV the
default `all` run wrote. This proves that no arm leaks state into another, which is the
meaningful substitute for the worker-count axis. `--dating` governs which arms are *computed*,
not merely which are persisted, so a single-arm invocation genuinely exercises a shorter path.

```
--dating strict_ps  → 739f14a148e2352ed8a16a75e35d6aa4366689cee1fa46e0ee2191b28263383d  R16_regime_census_strict_ps.csv
--dating symmetric  → 463f51aa26daf6241b12a0bccbcbea9844b67707a3050561beb9e04a2a6a6d00  R16_regime_census_symmetric.csv
--dating canonical  → e20112aad86f3227f683ae47587ff9771351db3cfe4343c35e7ffa8b099691d3  R16_regime_census.csv
                      128aa42d418ce400f931f4a62eb40fc6edd76d18a1226cf670b2ccedd57943c3  R16_meso_split_report.csv
                      62368994ccd2ef3ed79b594fd36579c342519b80e1e7ee3d006b8dbc43b56c3a  R16_boundary_convention_delta.csv
```

All five match the default run's digests exactly. A third full `./run_experiment_R16.sh`
afterwards restored all eight digests unchanged.

**Trigger probability under its own null: 0**, deterministic. A divergence would be a determinism
defect to correct, not a measurement.

### Figure verdict

Grepping `articleB_whitening_v87.tex` for `\includegraphics` and `\ref{fig:` in the census
paragraphs: **L329 and L331 carry no `\includegraphics` and reference only
`\ref{fig:oracle_frontier}`**, which belongs to R01's look-ahead oracle backtest.
**R16 renders no figure.** The verdict is logged at start-up rather than assumed, and
`results/R16_regime_census/figures/` is not created.

---

## 4. Deviation classification against v87

Every published quantity R16 regenerates, classified at v87's own printing precision (§S3):

| v87 site | published                      | regenerated                    | severity |
| -------- | ------------------------------ | ------------------------------ | -------- |
| L329     | `66` phases                    | 66                             | **D0**   |
| L329     | `53` of `66` (`80\%`)          | 53 of 66 (80.3%)               | **D0**   |
| L329     | `52` of `66`                   | 52 of 66                       | **D0**   |
| L329     | `64` of `66` (`97\%`)          | 64 of 66 (97.0%)               | **D0**   |
| L329     | SPY `0.541 \to 0.554`          | 0.541160 → 0.553908            | **D0**   |
| L329     | over `1{,}753` days            | 1753                           | **D0**   |
| L329     | floor consumes `55`--`92\%`    | **[50.1%, 92.1%]**             | **D2**   |
| L260     | `{\approx}1{,}510`             | 1509.85                        | **D0**   |
| L260     | `{\approx}2{,}790`             | 2786.83                        | **D0**   |
| L331     | `\Delta q \approx -0.28`       | −0.2803                        | **D0**   |
| L331     | Sharpe `{\approx}{-6.0}`       | −5.9904                        | **D0**   |
| L331     | `23` trading days              | 23                             | **D0**   |
| L331     | `\mathrm{kl} = 0.162`          | 0.162042                       | **D0**   |
| L331     | `{\approx}34` days             | 34.12                          | **D0**   |
| L331     | `18.5` days                    | 18.49                          | **D0**   |
| L331     | "four fifths of the phase"     | 80.4%                          | **D0**   |
| L392     | `-18.6\%` on PFF, 2020-03-18   | −0.18583434620279932 → −18.6%  | **D0**   |
| L329     | dating: "**Pagan--Sossounov** … of the four streams … after duration censoring" | strict PS gives **48** phases | **D3** |

**Seventeen of eighteen are D0. One is D2. One is D3, and it falls on a method description rather
than on a value.**

Six entries are registered in `docs/DEVIATIONS.md` with stable identifiers; existing entries are
not renumbered.

| id                            | location | class | severity | summary                                                                                                |
| ----------------------------- | -------- | ----- | -------- | ------------------------------------------------------------------------------------------------------ |
| `R16-dating-misdescription`   | L329     | A     | **D3**   | strict Pagan–Sossounov yields 48, not 66; the 66 need the SPY substitution, which censors no duration  |
| `R16-covid-phase-conditional` | L331     | A     | —        | L331's four numerals reproduce exactly; the phase exists only under that substitution                  |
| `R16-floor-frac-envelope`     | L329     | A     | D2       | `55--92\%` → `50--92\%`; cause **not identified**                                                      |
| `R16-boundary-sensitivity`    | L392     | A     | —        | 3 of 66 flip, all one way; the count is `[53, 56]`, never reported by v87                              |
| `R16-sign-arm-disagreement`   | L329     | A     | —        | "moves that count by one phase" is a net of 10 and 9; the arms disagree on 19 of 66                    |
| `R16-substitution-scope`      | L329     | A     | —        | the published fraction is conditional on the substitution reaching one ticker of four: 80.3% → 73.5%   |

### Why the COVID row is not a second D3

One measured fact must produce one register entry. L331's numerals are **not** falsified — they
reproduce to their printed precision — and the substitution that produces the phase is already
registered at `R16-dating-misdescription`. Entering it twice at D3 doubles the manuscript's
apparent exposure on a single finding, which is the over-declaration this campaign corrected on
R11's deviation table. The row cross-references the D3 and registers no second severity.

### On §S3's halt obligation

A D3 requires stopping, not reconciling. Here the halt lands on the **manuscript**, which is
frozen and cannot be edited. The obligation is discharged by three things: the register entry,
the camera-ready candidate `docs/camera_ready_candidates/R16_v87_dating_algorithm.md`, and the
persisted 48-phase counterfactual `R16_regime_census_strict_ps.csv` that makes the claim
checkable by a third party without rerunning anything.

**Nothing is suppressed and no parameter, tolerance, seed or bound was moved to reconcile
anything.** The pipeline runs to completion because the regenerated *values* are not in
contradiction — 53 of 66 reproduces exactly — and what is in contradiction is L329's account of
how the 66 were obtained. There is no `sys.exit(1)` gate on the canonical path, by explicit
decision: the 66-phase configuration is the repository's baseline, and a gate that stopped the
default run would make the D3 unreadable by making the artefact that documents it unbuildable.

---

## 5. For stream R13, which consumes this census

**The columns.** R13 reads what its prompt calls `ADD_min_census` and `detectable_flag_census`.
They are, verbatim in the CSV:

| R13's name              | column in `R16_regime_census.csv` | definition                                                       |
| ----------------------- | --------------------------------- | ---------------------------------------------------------------- |
| `ADD_min_census`        | **`ADD_min_days`**                | `504 * ln(1/alpha) / SR^2` at `alpha = 0.05`, i.e. `gamma = 20`, in trading days |
| `detectable_flag_census`| **`detectable_flag`**             | `ADD_min_days < T_days`, strict                                  |

**The names are not changed, deliberately.** Renaming them would break the cell-for-cell witness
comparison against `data/reference/R16/protocol_10b_regime_census_refined.csv`, which is what
classifies every deviation in §4. The mapping is stated here instead.

**The file R13 reads is the default-run canonical arm**,
`results/R16_regime_census/data/R16_regime_census.csv`, 66 rows. It is produced by
`./run_experiment_R16.sh` with no flags. Do **not** read a `_strict_ps` or `_symmetric` file: they
are counterfactual artefacts that price a deviation and are not the published census.

**Other gammas.** If R13 needs a budget other than `gamma = 20`, the same two quantities are in
`R16_sign_floor.csv` at all three budgets as `ADD_min_unc_g{20,252,1260}` and
`detectable_unc_g{20,252,1260}`, plus the exactly-priced sign-stream counterparts
`ADD_min_sign_g*` / `detectable_sign_g*`. `detectable_unc_g20` is bit-identical to the census's
`detectable_flag`, which the test suite asserts.

**No movement to propagate.** Every value R13 consumes reproduces the submitted campaign **bit
for bit**: worst numeric difference `0` over 66 rows and 19 columns. R13 inherits no numerical
displacement from R16.

**One thing R13 must carry forward.** The census rests on a dating whose *description* in v87 is
registered **D3** (`R16-dating-misdescription`). **The census values R13 consumes are unaffected
— the D3 falls on the manuscript's account of the method, not on the numbers.** But any R13 text
that repeats v87's "Pagan--Sossounov dating of the four streams" inherits the same
misdescription, and any R13 sensitivity analysis over the census should know that the dating is
the largest lever on it: 80.3% / 79.2% / 73.5% across the three arms. A new column,
`dating_algorithm`, carries `pagan_sossounov` or `lunde_timmermann` on every row and is the
row-by-row form of that fact.

---

## 6. Reproducibility and the whole suite

```bash
./run_experiment_R16.sh          # 1.4 s total: _a 0.2 s, _b 0.0 s, no parallelism
./run_tests.sh
```

`run_all.sh` discovers `run_experiment_R16.sh` by sorted enumeration. **Neither `run_all.sh` nor
`run_tests.sh` is modified** — `git diff --stat` shows both untouched.

Environment, recorded by `importlib.metadata.version()` at run time and copied verbatim into
`requirements/R16.txt`: Python 3.12.9, `numpy==1.26.4`, `pandas==2.3.2`, `scipy==1.16.2`,
`pytest==9.0.3`. Single-thread BLAS and `MKL_CBWR=COMPATIBLE` are pinned by
`experiments/common/fair_env.py` before NumPy loads; `PYTHONHASHSEED=42` is exported by the
orchestrator and verified at start-up by both scripts, which exit if it is absent.

`./run_tests.sh` — **197 tests collected, 197 passed, 0 failures in 1.51 s**, of which **28 are
R16's**. Collected counts per file, from `pytest tests/ --collect-only -q`:

```
platform linux -- Python 3.12.9, pytest-9.0.3, pluggy-1.6.0
rootdir: /home/m53/The-Whitening-Advantage-Experiments
collected 197 items

  5  tests/test_R01_claims.py        27  tests/test_R04_claims.py       16  tests/test_R06_claims.py
  8  tests/test_R02_claims.py        21  tests/test_R04b_claims.py      25  tests/test_R11_claims.py
  5  tests/test_R02b_claims.py       22  tests/test_R05_claims.py       28  tests/test_R16_claims.py
  7  tests/test_R02c_claims.py        9  tests/test_R03_claims.py       24  tests/test_R18_claims.py

============================= 197 passed in 1.51s ==============================
Tests Passed.
```

**No blocking assertion of `tests/test_R16_claims.py` rests on a value R16 produced.** Every one
rests either on a value v87 prints, compared at v87's own printing precision, or on a
deterministic relation reimplemented in the test file independently of the experiment — the
Sharpe ceiling written from `ln(gamma)/KL` with `KL = SR^2/504` rather than from
`504 ln(gamma)/SR^2`, the Bernoulli divergence accumulated term by term, and the whole census
recomputed from `data/derived_firstrate/` under the post-onset convention. The **witness is
deliberately not a gate**: `data/reference/README.md` forbids a cell-by-cell equality assertion
against it, so the bit-identity reported in §1 and §4 is *printed* by a reporting test and not
asserted.

Three assertions are **self-invalidating** and are the ones to watch. If strict Pagan–Sossounov
ever reaches 66 phases, if the canonical census ever becomes a pure Pagan–Sossounov dating, or if
a boundary-convention flip ever runs the other way, the corresponding test fires — and what must
then be revised is `docs/DEVIATIONS.md`, whose entry has dissolved, never the assertion.

**Preamble greps, all empty** on `experiments/R16_regime_census/*.py`,
`logs/R16_regime_census/*.log` and `docs/sections/R16.md`:
`proves|proven|perfectly valid|validates the (theorem|thesis|claim)|confirms the|as expected|triumph|victory|irrefutable|brilliant`;
plus `iterrows`, bare `except:`, and absolute paths — the last three asserted by the test suite
rather than checked by hand. `grep -c RSixteenth R16_claims.tex` returns `0`. Every produced text
file ends in `\n`, asserted by the suite over the macro file, `requirements/R16.txt`,
`docs/sections/R16.md`, this audit and the superseded README.

---

## 7. Design decisions taken outside the plan

1. **`check_sanity` is evaluated on all four tickers, on every run.** The delivered script
   initialises `sanity_ok = True` and reassigns it only inside `if ticker == 'SPY'`, so PFF, VNQ
   and BWX are never tested. Evaluating it on all four costs nothing and establishes by
   measurement — rather than by inference — that **all four fail**, which is what makes the
   `symmetric` arm a defined object rather than a speculation.

2. **`--dating` governs which arms are computed, not only which are persisted.** The weaker
   reading (compute all three, persist one) would have made C9's arm-isolation axis vacuous,
   since the same code path would run either way. The stronger reading gives the axis something
   to prove. Both datings are nevertheless computed for all four tickers on every run, because
   C6 requires it and because `check_sanity` cannot be evaluated otherwise.

3. **`--dating canonical` writes three files, not one.** The plan says a single-arm invocation
   writes "that arm's CSV only". The MESO split report and the boundary-convention delta are
   canonical-arm artefacts with no counterfactual counterpart, so they are written with the
   canonical census and their digests are part of the arm-isolation check. `strict_ps` and
   `symmetric` write exactly one file each, as specified.

4. **C2's comparison values are read from the vendored witness rather than typed.** The plan
   gives them as `53 / 52 / 64`. Typing them into the producing script would be the same
   hard-coded target that `Priorite_20`'s `EXPECTED_FRAC_OUT = 0.803` was, which §S6 forbids and
   which this port removes. Reading them from `protocol_20b_census_feasibility_vs_gamma.csv` with
   `float_precision='round_trip'` is the preamble's own anchor rule.

5. **C8 covers seven primitives, not five.** `check_sanity` is carried and therefore owes the
   same guarantee as the five the plan names; `wilson_score_interval` is carried from R02 for
   C6's intervals, and R18 set the precedent of asserting a carried primitive against the
   experiment that owns it. Extending the control is strictly more assurance.

6. **`census_source` keeps its witness value `refined`.** The legacy `protocol_20a` writes
   `refined`, meaning the MESO-refined census, which *is* the canonical arm. Renaming it to
   `canonical` would have broken the cell-for-cell witness comparison that classifies §4's
   deviations, for a cosmetic gain.

7. **The COVID phase and the long secular advance are selected by property, never by date.** The
   COVID anchor is the phase of SPY carrying the `COVID_2020` label the dating's own
   `get_episodes` assigns; the long advance is the **longest phase of the detectable set**, which
   is the property v87 L329's own sentence asserts ("they nonetheless dominate the detectable set
   on duration alone"). Typing `2011-10-03` would have hard-coded an output into the producer.

8. **`set_seed(42)` is deleted and no `SeedSequence` helper replaces it.** Neither delivered
   script draws a random number. R16 has **no stochastic surface and therefore no
   seed-derivation surface**, and adding an unused 128-bit seed helper to look conformant would
   assert a property the code does not have. The absence is logged at start-up, recorded in
   `docs/sections/R16.md`, and is why C9's second axis is arm isolation.

9. **The `if T_a < 2: continue` branch exits instead of skipping.** See C1. It never fires on
   this data; it is closed because a control that the audited code can silently defeat is not a
   control.

10. **`_a` reads the derived series directly.** The delivered
    `try: from Priorite_14_real_world_backtest import get_daily_data / except ImportError: ...
    NotImplementedError` block is a fallback of exactly the kind §S4.3 bans — an absent module
    left the script running with a stub. It is replaced by a direct read of
    `data/derived_firstrate/R01_daily_<TICKER>.csv` with `float_precision='round_trip'`, which
    exits `1` if the file or the `log_ret` column is missing.

11. **Three vectorisations, each asserted to preserve the original branch order.**
    `classify_pathology` becomes `np.select` with the if-chain's conditions in the same order
    (first true wins, exactly as the chain returns); `refined_episode_label` becomes a masked
    `where` that strips the token only when it is present, which is the original's `else` branch;
    the flipped-phase report drops `iterrows()` for a frame filter. All three are covered by the
    bit-identity of the regenerated CSV against the witness.

12. **`data/reference/README.md` gained three register rows and a paragraph.** Vendoring a
    directory that the file's own register purports to enumerate, without registering it, would
    leave the index wrong. The edit is additive; no existing row changed. `run_all.sh` and
    `run_tests.sh` are untouched.

---

## 8. Findings that revise the plan's own premises

Four, all measurements rather than opinions. Three were anticipated by the plan and are confirmed
here; the fourth was not.

1. **The R16 prompt states the double-counting direction backwards.** Its §2.1 asserts that
   counting the turning-point return twice "gonfle le Sharpe … donc augmente la fraction
   détectable et diminue le 80 % publié". Measured: the inclusive convention gives **56/66
   (84.8%)** and the post-onset convention gives **53/66 (80.3%)**. The defect *inflated* the
   published fraction; the correction *lowered* it. **v87 L392 states the mechanism correctly** —
   the trough return is a large negative outlier that depresses the mean and inflates the
   variance of the phase that follows, biasing its floor **upward**. The prompt is wrong here,
   the manuscript is right, and the correction the manuscript adopted runs against its own
   headline.

2. **The prompt's convention envelope is not `[50, 56]`.** All three flips run one way, so the
   reachable envelope is **`[53, 56]`** and 50/66 is unreachable under either convention.

3. **The prompt's first "defect" is already corrected in the delivered code.** The header of
   `Priorite_16_regime_census.py` reads `CORRECTED VERSION: STRICT POST-ONSET BOUNDARY
   CONVENTION`, and the inclusive arm survives only inside `protocol_10d` as the sensitivity
   measurement. There was nothing to re-fix; what R16 does is regenerate the measurement.

4. **The `symmetric` arm carries seven degenerate phases, which the plan predicted at zero.**
   See C5. Seven 2-to-6-day phases of the 2008–2009 crisis have `q_phase` exactly 0 or 1. They
   are counted, logged with their defined treatment, and they change no gate: the mechanism C5
   protects against — a non-finite statistic reaching a detectability flag — is at zero on all
   three arms. Four of the seven are counted detectable, so the effect moves the symmetric
   headline *down*, against the manuscript's thesis, and §S3's asymmetry rule accordingly assigns
   it the lighter examination. It is reported because the plan's expectation was explicit and
   measurement contradicted it.

**And the `symmetric` arm itself is reported rather than dropped.** Applying the substitution to
every ticker whose `check_sanity` fails — the rule the delivered script writes for SPY, applied
consistently — moves the headline from 80.3% to **73.5%** (75 of 102). That is 6.8 points: four
times the displacement strict Pagan–Sossounov produces and more than twice the
boundary-convention envelope. An evaluator who reads `if ticker == 'SPY'` will ask exactly this
question, and finding the answer already computed in the repository but absent from the register
would be worse than finding it stated. It is registered as `R16-substitution-scope`, Class A, no
severity. Its direction is against the thesis, so it earns the lighter examination, not the
heavier — but it owes a sentence, and it has one.

---

## 9. Open questions, left open

1. **What produced `55` in "the floor consumes `55`--`92\%` of the phase"?** Measured
   `[50.1%, 92.1%]`. Five definitional variants were enumerated and logged — bull phases only,
   `T_days >= 250`, both together, the sign arm at `gamma = 20`, and the superseded
   `protocol_10a` census — and **none yields 55–92**. SPY 2011–2018 is at `54.79%`, which rounds
   to 55 and is the phase the same sentence names two clauses earlier, which *suggests* the bound
   was read off that one phase rather than off the set minimum. **No measurement establishes it**,
   and §S4.5 forbids asserting it. Classified D2 with the cause **not identified**.

2. **Is `check_sanity` an adequate criterion for choosing a dating?** It asks whether four named
   historical episodes appear, and it fails on all four tickers — including the three whose
   dating the canonical arm nevertheless keeps. Nothing here measures how often it would fail on
   a dating that is in fact adequate, so its verdicts license the arms and nothing more. Whether
   a criterion that rejects every stream it is applied to should select among algorithms is a
   design question this audit poses and does not settle.

3. **Which dating is right?** R16 does not answer it and does not attempt to. There is no
   ground-truth turning point in this data. What the three arms establish is the *sensitivity* of
   the published fraction to that choice — 80.3%, 79.2%, 73.5% — and that the ceiling excludes
   most of what any of them finds.

4. **`q_ref` is estimated over each ticker's whole history, including the phase being tested.**
   The divergence `kl(q_phase || q_ref)` is therefore measured against a reference the phase
   itself contributes to. On a 23-day phase inside a 6 414-day history the contribution is
   negligible; on the `symmetric` arm's 102-phase partition, where several phases run 2 days, the
   same statement is weaker. The size of the resulting bias is **not quantified here**, and it
   would need a leave-one-phase-out reference to be.

5. **The Sharpe ceiling is a first-order asymptotic bound** (`gamma -> infinity`), stated by the
   manuscript under a homoscedastic Gaussian location alternative. R16 evaluates it on phases as
   short as 6 trading days, which is far from the regime that derives it. Whether the bound is
   conservative or anti-conservative there is a question about `cor:sharpe_ceiling`, not about
   this census, and R16 does not measure it.

6. **Whether an executable belongs under `data/reference/`** is the question `AUDIT_R06.md` §8.4
   already poses for `data/reference/R06/` and `data/reference/README.md` restates for
   `data/reference/R11/`. R16 adds two more scripts there because control C8 needs a
   repo-relative witness and §S7 bans absolute paths. It is not settled here either.
