# AUDIT — R08, the adverse direction and the discrete null law

This is the only document transmitted to the orchestrator. It contains: what R08 establishes and
what it does not; the verdict on the status of the second delivered log, established by digest; the
eight controls with their margins and their trigger probability under their own null; the deviation
classification, including one **D3**; the reproducibility evidence with the SHA-256 digests of both
runs pasted as-is and the full `pytest tests/ -v` output; the design decisions taken outside the
plan; the findings that revise the plan's own premises; and the open questions, left open.

R08 measures v87 **Figure 8** (`fig:adverse`), **L241** — the discrete null law and its two
bracketing levels — and **L311** — the adverse direction of a centring bias.

---

## 1. What R08 establishes, in one paragraph

Running the injected-bias campaign (`10 000` trajectories per `b`, `φ = 0`, `n_ols = 250`,
`H = 5 000`) beside the lattice null law (`2 × 10⁵` fair-coin streams at the same horizon),
**every qualitative claim of L311 reproduces.** The whiteness loss of the two arms stays within
`2.21` points of a bound the body sets at three; the over-centred arm's false-alarm rate is
monotonically falling in `b` and the under-centred arm's monotonically rising, over the whole grid,
with **zero inversions in ten consecutive steps**; and the two separate by a factor of `22` at
`b = 0.15`. **One claim of L241 does not, and it is the finding of this stream.** **Scope bound: 
the exact null law is correct and free of nuisance parameters; the contradiction is strictly on 
the threshold selected and the level reported.** L241 promises "the nearest attainable level 
**at or below** nominal", its own footnote states that the implemented test `M_H > λ*` **is** 
the mathematical `M_H ≥ λ*`, and the level that weak operator delivers at `λ* = 11.4` is 
`P(M_H ≥ 11.4) = P(M_H > 11.2) = 5.1021 %` **exactly** — above nominal. That is a **Class A, D3**, 
registered as `R08-delivered-level-above-nominal` and traced in §4. No parameter, tolerance, seed 
or bound was moved to reconcile it. Note that this discovery cross-propagates to R07 Figure 7 
caption, and the candidate `R07_v87_figure7_exactness.md` is reached by this same D3.

**The control the prompt was built around resolves, and it resolves the prompt's own §C6
divergence.** The R08 prompt observes that the witness's two `b = 0` values, `0.0546` and `0.0535`,
bracket `5 %` and not the `4.29 %` the threshold is supposed to attain, and calls that "a divergence
to instruct before anything else". It is not a threshold error: `λ* = 11.4` on both paths, and the
witness's own log records `lambda_star = 11.400000`. It is an **operator** difference, and control
C1 measures which operator each module implements rather than inferring it. Module A compares the
raw accumulated float against `λ*` (`'fpr_exceed': m_val > lambda_star`, witness line 193) and
therefore delivers the **weak** level `5.1021 %`; the delivered module B rounds to six decimals
before comparing (`np.round(M, 6)`, witness lines 337 and 369) and therefore reports the **strict**
level `4.29 %`. `4.287 %` and `5.10 %` are two *operators* at the *same* `λ = 11.4`, not two
estimates of one quantity. R08's own `b = 0` cell lands at `5.20 %`, `+0.45` standard errors from
the weak exact level and `+4.21` from the strict one.

---

## 2. The status of the second delivered log, established by digest and not assumed

The R08 prompt (§0bis) reports `Priorite_21c_plot_adverse_lattice.py` as "reputed never to have
been executed in this project", notes that a log for it exists in the materials, and asks for a
verdict rather than an assumption. **The log corresponds to the delivered script and to the
delivered CSVs; the script was executed.** Four digests and two timestamps establish it.

| claim in the delivered log                             | recomputed now                                                     | verdict |
| ------------------------------------------------------ | ------------------------------------------------------------------ | ------- |
| `21c` log, MD5 `protocol_21c_adverse_bias.csv`         | `150cf30022916afbfd1aa13f386ae294`                                 | matches |
| `21c` log, MD5 `protocol_21d_null_law_lattice.csv`     | `e83647394c8607c1a6b231d377511d72`                                 | matches |
| `21b` log, SHA-256 `protocol_21c_adverse_bias.csv`     | `eb2d706f7ed3864590d766a014aeaa5113a75a0cc38d6b68d4f890c9fb47d897` | matches |
| `21b` log, SHA-256 `protocol_21d_null_law_lattice.csv` | `19570985b8fe8b4ebcacfbb04c886e9441eb6da4c492e52d9c1efb854b395892` | matches |

Both logs pin the **same two files**, one by MD5 and one by SHA-256, and both digest sets match the
vendored CSVs. The timestamps are consistent with the stated execution order: `21b` finishes
`2026-07-27 07:23:57` and `21c` runs `2026-07-27 07:25:37`, one hundred seconds later, on the same
day. The `21c` log also carries the line the script emits after `savefig`, so the figure was
written. Digests of the six vendored files are in §5.

**What this does not establish.** It does not establish that the PNG in the materials is the one
that run produced — no digest of it appears in either log — and R08 does not claim it. Preamble §S6
says the witness PNGs are not systematically transmitted and that the comparison is justified by
examining the plotting code, which is what §6 below does.

---

## 3. Controls, with their margins and their trigger probabilities

Every control logs its trigger probability **under its own null** before its result is read. The
family-wise arithmetic of the only multi-test control is logged before any p-value is looked at:
`1 − (1 − 0.05)⁶ = 26.4908 %`.

| control | statement                                                                                           | margin                                       | trigger probability under its own null  |
| ------- | --------------------------------------------------------------------------------------------------- | -------------------------------------------- | --------------------------------------- |
| **C1**  | one operator, asserted by `ast` over **both** modules; the boundary counted; both exact levels      | 137 comparisons, 3 whitelisted, 0 offending  | **0**, deterministic                    |
| **C2a** | R08's exact survival at `H = 5 000` equals R07's cell by cell                                       | 16/16 bit-identical, worst difference `0.0`  | **0**, deterministic                    |
| **C2b** | R08's path enumeration equals R07's and R10's on the cells they share                               | 8 three-way + 4 R07-only + 4 R10-only, exact | **0**, deterministic                    |
| **C3**  | `bracket_role` from the exact law; the same roles required of the measured strict levels            | exact leg exact; measured leg agrees         | **0** exact leg / **1.9017 %** measured |
| **C4**  | the three-point bound against the extremum's own law; KS calibration against a sign-flip null       | `2.21` pt, envelope `[1.56, 3.61]`           | not a gate (§S4bis.1, §S4bis.8)         |
| **C5**  | `fpr_biased` non-increasing and `fpr_naive_ref` non-decreasing over the whole grid                  | 10 steps, **0** inversions                   | **0**, deterministic                    |
| **C6**  | R08's `b = 0` arm **is** R07's `OLS-250` at `φ = 0`; its diagnostic **is** R07's `NAIVE` at `φ = b` | 14 cells, 0 differences                      | **0**, exact by construction            |
| **C7**  | `ast` source identity of 18 carried primitives; the normalized-AST leg across the two owners        | 10 585 characters, 0 differences             | **0** unless a copy has drifted         |
| **C8**  | two runs at different worker counts, SHA-256 identical on every artefact                            | 7 artefacts, 0 differences                   | **0**, deterministic                    |

### C1 — the comparison operator, asserted and then measured

**Three assertions, by `ast`, over both modules of the stream.** (i) `exceeds` is a single
`ast.Compare` carrying `ast.Gt`. (ii) Of the `137` comparisons in
`exp_R08_adverse_lattice_a.py` and `exp_R08_adverse_lattice_b.py`, the `3` inside the declared
helpers are the only ones that may ORDER a threshold name against anything, and none of the others
does. (iii) `worker_mod_A` calls `exceeds`; `operator_levels_at` calls all three helpers;
`lattice_exceedance_enumerated` calls `exceeds_units_strict`. `λ*` itself comes from
`lambda_star_from_rule` on the exact law, so the selection path and module A's evaluation path test
the same operator **by construction**, and the assertion verifies it rather than asserting it from a
comment. Trigger probability `0`.

**Three measurements, over all `2 × 10⁵` streams.**

| `λ`    | units | `float M > λ` | `M_units > λ` | `M_units ≥ λ` | disagreements vs strict | vs weak |
| ------ | ----- | ------------- | ------------- | ------------- | ----------------------- | ------- |
| `11.0` | `55`  | `0.070360`    | `0.060200`    | `0.070360`    | `2 032`                 | **`0`** |
| `11.2` | `56`  | `0.060200`    | `0.050815`    | `0.060200`    | `1 877`                 | **`0`** |
| `11.4` | `57`  | `0.050815`    | `0.043230`    | `0.050815`    | `1 517`                 | **`0`** |
| `11.6` | `58`  | `0.043230`    | `0.036705`    | `0.043230`    | `1 305`                 | **`0`** |
| `11.8` | `59`  | `0.036705`    | `0.031170`    | `0.036705`    | `1 107`                 | **`0`** |
| `12.0` | `60`  | `0.031170`    | `0.026320`    | `0.031170`    | `970`                   | **`0`** |

The ULP boundary counter, logged even at zero: the accumulated float sits **above** its exact
lattice value on `192 842` streams, **below** on `2 776`, exactly **on** it on `4 382`; `78 971`
streams lie within `4 ulp` of their exact lattice point; `1 517` streams have their exact maximum
equal to `λ*` itself, which is the configuration the L241 footnote describes. The two exact levels
at `λ*` and their difference: strict `4.3428 %`, weak `5.1021 %`, gap `0.7592` points — `15.2 %` of
the nominal level itself, which is what `\REightOperatorDelta` carries.

**The identity is empirical, not structural, and the section says so wherever it is used.** The
float lands *below* its exact lattice value on `2 776` streams, so a stream whose exact maximum
equals `λ*` can in principle be missed. Zero disagreements with the weak comparison were observed at
this horizon, this dead band and this accumulation order, and no wider statement is made. R10
measured the same coincidence on its own apparatus (38 disagreements with strict, 0 with weak); R08
did not presume it, it measured it.

### C2 — lattice concordance, and the re-derivation the prompt's version required

**The prompt's C2 as written is not satisfiable, and the re-derivation is recorded here.** §5 of the
R08 prompt asks the levels at `λ ∈ {11.2, 11.4}`, `δ = 0.1`, `H = 5 000` to coincide with **both**
`R07_lattice_exact_law.csv` and `R10_lattice_exact_law.csv`. `R10_lattice_exact_law.csv` carries
**zero** rows at `H = 5 000`: its own campaign runs at `H = 8 000` (`lambda_units 74/75/76`) and it
validates its dynamic program on small-`H` enumerations at `q = 1/2`. No level at either threshold
can be looked up in it. The control is therefore split:

- **C2a** — R08's `lattice_exceedance_exact(5000, u)` against R07's `exact_survival` cells, on all
  `16` units of the scanned region `50..65`: **bit-identical on 16 of 16**, largest absolute
  difference `0.0`, both sides read at `float_precision='round_trip'`.
- **C2b** — R08's exhaustive path enumeration against R07's and R10's, on every cell either carries:
  `8` shared by all three (`H ∈ {10, 12}` × `λ ∈ {4, 5, 6, 7}` lattice units at `q = 1/2`), `4` more
  with R07 alone (`H = 8`), `4` with R10 alone (`H = 14`). **Bit-identical on all 16.** R08 also
  agrees with its *own* dynamic program to the last bit on all 16.

Two independently written absorbing-chain programs at the same horizon over the same state space:
agreement is a statement about the transcription, not about the model. Trigger probability `0`.

### C3 — bracketing of nominal, computed and never read

`bracket_role` is computed from the **exact** law, where the statement has trigger probability `0`:
the exact survival function is strictly decreasing over the grid, exactly one adjacent pair
straddles `5 %`, and it is `(11.2, 11.4)`. `is_lattice_point` is computed in exact rational
arithmetic on the decimal v87 prints — `λ` is attainable exactly when `5λ` is an integer — because
neither float route decides it: `11.2 / 0.2` returns `55.99999999999999` and `56 × 0.2` returns
`11.200000000000001`. A probe at `λ = 11.3` returns `False`, so the column is a computation with two
possible answers and not a tautology.

**Requiring the same roles of the MEASURED strict levels is a second, weaker leg, and its trigger
probability was computed before the streams were drawn.** The exact level at `λ = 11.2` sits only
`2.07` binomial standard errors above nominal at `2 × 10⁵` streams, so a Monte-Carlo realisation on
the wrong side of nominal is an ordinary event; summed over the six grid points the probability that
at least one lands on the wrong side is **`1.9017 %`**. §S4bis forbids reading a gate at that rate,
so the measured leg logs and reports and only the exact leg exits. Both agree on this run.

### C4 — the symmetry of the whiteness loss, with no binary gate anywhere

The family-wise arithmetic is logged before any p-value is read: six simultaneous proportion tests
at the `5 %` level reject at least once with probability `1 − 0.95⁶ = 26.4908 %` under equality
itself. **Three of the six reject** here (`b = 0.05` at `2.67e-4`, `b = 0.075` at `1.77e-3`,
`b = 0.10` at `3.32e-4`); the witness campaign had two (`5.9e-5` at `b = 0.075`, `0.0243` at
`b = 0.05`). Neither count is used as evidence in either direction.

**The substitute, and the null it is read against.** The KS calibration of the six p-values against
`Uniform(0,1)` gives `D = 0.5584`, tabulated `p = 0.0274`. **The tabulated value does not apply**:
the six p-values are dependent twice over — the six `b` share the same `10 000` trajectories, and at
each `b` the two arms share the same innovation stream — and the Kolmogorov distribution assumes
neither. The null of `D` is built by sign-flip resampling on the trajectory index (one Rademacher
sign per trajectory, **shared across the six columns** so their dependence is carried into the null),
`2 000` replicates: the observed `D` sits at a null exceedance probability of `0.038`. Reported,
gates nothing (§S4bis.8).

**The body's three-point bound, asserted separately against the extremum's own law (§S4bis.4).** The
largest `|Δ lb|` over the six `b` is `2.21` points at `b = 0.075`, against the three L311 states:
**RESPECTED**. Its 95 % bootstrap envelope over `2 000` resamplings of the trajectory index is
`[1.56, 3.61]` points, which **includes** three; preamble §S3 makes a printed bound crossed at D3
only when that interval excludes it, and it does not. Separately, the null law of the same maximum
under exchangeability of the two arms puts the observed `0.0221` just inside its own `99.9 %`
quantile, `0.0223`, i.e. at a null exceedance probability of `0.0011` against a criterion level of
`0.001`. **The criterion is met, and narrowly.** Read with the KS result and the three rejecting
proportion tests, the reading is that the two arms are close and that this campaign has nearly
enough resolution to separate them — which is why "identical" is not presented as established and
why no gate is built on any count.

**The live D3 risk the plan flagged did not fire.** The plan recorded that the witness's maximum gap
of `2.84` points left only `0.16` points of margin under a three-point bound and that the redraw
might cross it. It moved the other way, to `2.21`.

### C5 — sign asymmetry

`fpr_biased` over the grid: `0.052, 0.0429, 0.0309, 0.0238, 0.0175, 0.0095` — non-increasing.
`fpr_naive_ref`: `0.0516, 0.0644, 0.0854, 0.1094, 0.1377, 0.2100` — non-decreasing. **Zero
inversions over the ten consecutive steps of the two arms.** Each step's paired standard error is
computed from the per-trajectory differences on the shared trajectories, never as the sum of two
independent binomial variances; had any inversion appeared it would have been characterised against
that standard error and not corrected (§S4.10). None did.

### C6 — the degenerate witness, upgraded to an exact cross-stream identity

`generate_dgp` draws `z`, `h` and `eps` without ever referencing `phi` — only `r[t] = φ r[t−1] +
eps[t]` uses it — and R08 keys its trajectories on `seed_sequence_for("trajectory", i)`, which is
R07's own key. Therefore R08's `b = 0` arm **is** R07's `OLS-250` arm at `φ = 0`, and R08's pairing
diagnostic at `φ = b` **is** R07's `NAIVE` arm at `φ = b`, by construction. What licenses the word
"therefore" is C7's normalized-AST leg: R07's copies of `generate_dgp` and
`compute_phi_hat_vectorized` differ from the R08 witness's in **blank lines only** and parse to the
same tree.

Measured, both sides read at `round_trip`: `b = 0` Ljung–Box `0.0478` against R07's `0.0478`, FPR
`0.0520` against `0.0520`, **bit-identical**; the pairing diagnostic **6/6 bit-identical on
Ljung–Box and 6/6 on FPR**. Fourteen cells, zero differences, trigger probability `0`.

**The key-namespace crossing is declared, because an unexplained reuse would read as an entropy
collision.** Module A's trajectories key on **R07's** namespace, deliberately; module B keys on
`("lattice_stream", index)`, which is R08's own and is disjoint from it. Every resampling key is
`("resample", <name>)`. `R08_pairing_diagnostic.csv` certifies no published value.

### C7 — source identity

Six primitives byte-identical to `data/reference/R08/Priorite_21b_adverse_bias_and_null_law.py`
(`wilson_ci`, `prop_test`, `lb_pvalue`, `compute_phi_hat_vectorized`, `cusum_concept_fast`,
`generate_dgp`) and twelve byte-identical to
`experiments/R07_estimated_mean/exp_R07_estimated_mean.py` (`exceeds`, `exceeds_units_strict`,
`exceeds_units_weak`, `cusum_concept_lattice_units`, `lattice_exceedance_exact`,
`lattice_exceedance_enumerated`, `lattice_survival`, `lambda_star_from_rule`,
`get_deterministic_seed`, `seed_sequence_for`, `rng_for`, `sign_flip_null_max`): **10 585 characters
compared, 0 differences**. Preamble §S4.2 forbids hoisting any of them into `experiments/common/`,
so the duplication is deliberate and this is what stops it drifting; `source_segments` is duplicated
locally for the same reason.

**The normalized-AST leg, which underwrites C6.** `generate_dgp` and `compute_phi_hat_vectorized`
are byte-identical to the R08 witness and **not** to R07's copy: R07's carries five and four blank
lines respectively that the witness does not. Byte identity across the two owners would fail and is
**not** asserted. What is asserted is `ast.dump(ast.parse(segment))` equality — the two files
compile the same instructions — with the whitespace-only difference logged and every non-blank line
verified identical.

**Adapted and superseded routines, and one disposal that is not the plan's.** `worker_mod_A`,
`worker_mod_B` and `plot_adverse_and_lattice` are ADAPTED: each is quoted in full in the log after
the §S4.4 grep returns empty on its segment. **`main` is not quoted**, and the reason is the grep
itself: the witness `main` carries proscribed wording at its line 123, and §S4.2 makes the grep a
*precondition* of the citation precisely so that a quotation cannot import that wording into the
log. It is pinned by SHA-256 (`ba4a2bb3…ee4d`) and its adaptation is described in the module
docstring and in §6 below. `setup_logging`, `get_sha256`, `dump_requirements` and `get_md5` are
SUPERSEDED and pinned by SHA-256 without being quoted.

### C8 — reproducibility

Two runs at different worker counts. Both digest sets are pasted in §5.

---

## 4. Deviation classification against v87

Read at the manuscript's own printing precision, with the source CSV cell of every value.

| site                                        | v87 prints     | regenerated | degree | source cell                                                    |
| ------------------------------------------- | -------------- | ----------- | ------ | -------------------------------------------------------------- |
| L241 level bracketing `5\%` from above      | `5.03\%`       | `5.0815 \%` | **D2** | `R08_null_law_lattice.csv`, `λ = 11.2`, `P_exceed_strict`      |
| L241 level bracketing `5\%` from below      | `4.29\%`       | `4.3230 \%` | **D2** | `R08_null_law_lattice.csv`, `λ = 11.4`, `P_exceed_strict`      |
| L241 `λ^{\star}`                            | `11.4`         | `11.4`      | **D0** | `R08_null_law_lattice.csv`, `bracket_role = below_nominal`     |
| Fig. 8 (B) / L311 FPR collapses to          | `0.86\%`       | `0.95 \%`   | **D2** | `R08_adverse_bias.csv`, `b = 0.15`, `fpr_biased`               |
| Fig. 8 (B) / L311 FPR inflates to           | `20.8\%`       | `21.0 \%`   | **D2** | `R07_estmean_lb_fpr.csv`, `NAIVE`, `phi = 0.15`, `fpr_concept` |
| L311 whiteness gap bound                    | `3` pt         | `2.21` pt   | holds  | `R08_pairing_diagnostic.csv`, `whiteness_bound`                |
| L311 penalty at residual momentum `0.02`    | `1.1` pt       | `1.3` pt    | **D2** | `R07_estmean_lb_fpr.csv`, `NAIVE`, `phi ∈ {0, 0.02}`           |
| L311 whiteness range, low end               | `5`            | `4.78 \%`   | **D1** | `R08_adverse_bias.csv`, min over both arms                     |
| L311 whiteness range, high end              | `100\%`        | `99.84 \%`  | **D1** | `R08_adverse_bias.csv`, max over both arms                     |
| Fig. 8 caption: `10 000` trajectories/point | `10{,}000`     | `10 000`    | exact  | `R08_adverse_bias.csv`, `N_seeds`                              |
| Fig. 8 caption: `2 × 10^5` streams for (C)  | `2\times 10^5` | `200 000`   | exact  | `R08_null_law_lattice.csv`, `N_streams`                        |

Each moved numeral is read against the standard error of the **difference between two campaigns of
the same design** — the printed value is itself one Monte-Carlo realisation of that design — and
none exceeds three:

| numeral            | printed  | regenerated | paired SE | `z`     |
| ------------------ | -------- | ----------- | --------- | ------- |
| L241 at `λ = 11.2` | `0.0503` | `0.050815`  | `6.93e-4` | `+0.74` |
| L241 at `λ = 11.4` | `0.0429` | `0.043230`  | `6.42e-4` | `+0.51` |
| FPR collapse       | `0.0086` | `0.0095`    | `1.34e-3` | `+0.67` |
| FPR inflation      | `0.208`  | `0.2100`    | `5.75e-3` | `+0.35` |

### `R08-delivered-level-above-nominal` — Class A, **D3**

**Scope of the D3:** This contradiction is strictly about which threshold was chosen and which level was reported. 
The exact null law itself remains valid and free of nuisance parameters, which is the core contribution of the section.

The full account is in `docs/DEVIATIONS.md` under that identifier and in `docs/sections/R08.md`.
In summary: L241's selection rule promises a delivered level at or below nominal; its own footnote
makes the implemented test the weak comparison; C1 measures the footnote to hold on every one of the
`200 000` streams; and on the integer lattice `P(M ≥ u) = P(M > u − 1)`, so the level `λ* = 11.4`
delivers is `5.1021 %` exactly, above nominal. Under the weak comparison the strictly conservative
threshold is `λ = 11.6` at `4.3428 %` — one lattice step.

**Cross-propagation to R07:** The Figure 7 caption prints "exact lattice level `4.29 %`, `5.03 %` at `λ = 11.2`" 
and R07 operates at the same `λ* = 11.4`. The delivered level there is therefore affected by this same discovery 
(R07 measures weak `5.16 %`, strict `4.28 %`). The candidate `R07_v87_figure7_exactness.md` and the Figure 7 caption 
are reached by this same D3.

**Two legs, and the classification rests on the first.** The **exact** leg is decisive: `5.1021 %`
comes from an absorbing-chain program that consumes no entropy, is validated against exhaustive path
enumeration and is bit-identical to R07's independent table, so it carries no sampling interval and
the trigger probability of the statement is `0`. The **Monte-Carlo** leg is reported beside it and is
*not* decisive: the measured weak level is `5.0815 %` with a Wilson interval of
`[4.9861 %, 5.1786 %]`, which **includes** `5 %`, so on the Monte-Carlo evidence alone preamble §S3's
interval criterion would leave this at D2. At the exact level that interval clears `5 %` in
expectation from about `1.8 × 10⁵` streams, so the `2 × 10⁵` basis L241 states is right at the
boundary of its own resolution and this draw came in `0.42` standard errors low. Resolving the excess
with `90 %` power would take about `4.9 × 10⁵` streams.

**No printed numeral of L241 is itself wrong.** `5.03 %` and `4.29 %` are correct strict-comparison
Monte-Carlo estimates of the basis the sentence states, and `λ* = 11.4` **is** the threshold that
rule selects under the strict comparison. What is falsified is the conjunction, and the footnote's
closing clause — "we report the level actually delivered" — is not honoured by the numerals printed
beside it. Camera-ready candidate: `R08_v87_delivered_level.md`, two edits, both search strings
`grep -Fc` = 1.

### `R08-campaign-redraw` — Class A, D2, pre-classified before the first run

Preamble §S6's 128-bit re-keying on role and index alone replaces three delivered entropy
constructions: the positional `SeedSequence(424242).spawn(7 * 10000)` of module A, the
`SeedSequence(555555).spawn(N)` of module B, and `np.random.default_rng(100)` on the calibration.
Every Monte-Carlo value of both modules is redrawn by construction. Pre-classified Class A / D2 by
the `R05/R07/R09/R10/R13-campaign-redraw` precedents. The printed numerals that move are the three
in the table above; the unprinted maximum whiteness gap moves `2.84 → 2.21` points and stays at
`b = 0.075`. Every qualitative claim holds. Candidates: `R08_v87_adverse_numerals.md` (the collapse
numeral) and `R08_v87_lattice_exact_basis.md` (the two levels, reported beside their closed form
rather than replaced).

### What does **not** reach the register

**`20.8 % → 21.0 %` and the `1.1 → 1.3` point penalty are not R08's to register.** Both are cells of
`results/R07_estimated_mean/data/R07_estmean_lb_fpr.csv`, arm `NAIVE`, whose redraw
`R07-campaign-redraw` already registers. Control C6 asserts R08's own recomputation of that arm is
**bit-identical** to those cells on all six values of `b`, so there is one cell behind each number
and not two. The *sites* — L311 and the Figure 8 caption — are R08's, and no R07 candidate consumes a
search string on either, so R08 files the numeral edit while opening no new entry.

**The Figure 8 caption's "identical whiteness loss" does not reach the register.** The body's claim
is the measurable one and it holds at `2.21` points; the caption's parenthetical is a statement of
mechanism, symmetric by construction, and is not contradicted by a difference in measured rate.
§S8's channel 1 takes only formal contradictions. Channel 3 candidate:
`R08_v87_whiteness_identity.md`, header `NO DEVIATION — clarification only`.

**`is_lattice_point` does not reach the register.**
`data/reference/R08/Priorite_21b_adverse_bias_and_null_law.py:373` is the bare assignment
`is_lattice = True`, established by parsing to a single `ast.Constant` and not by reading. It is a
defect of the delivered CSV — a boolean column that is a literal — but v87 publishes no numeral from
it, so §S8's scope filter keeps it here.

**The delivered `λ*` estimator does not reach the register from R08.** `np.quantile(Ms_cal, 0.95)`
on 20 000 streams sits astride a lattice boundary; `docs/DEVIATIONS.md` `R07-lambda-star-estimator`
already registers it with the exact probability that it returns `11.4`. R08 cites it and opens no
duplicate.

**The constant `2.5` of L311 is traced and no macro is emitted for it.** L311's "residual momentum
`+2.5 φ/n`" is the same coefficient **L308 of the same manuscript** prints as "the classical
small-sample AR bias `E[φ̂] − φ ≈ −2.5 φ/n`, stays under `2.9e-3`". It is not orphaned, R07 owns that
sentence, and R07 registers `R07-bias-bound-not-a-bound`. "Seven times the largest we measure" is
`0.02` over a denominator R07 holds: `6.90` against v87's own printed bound, `6.40` against the
largest `|E[φ̂] − φ|` R07's 28 diagnostic cells carry (`0.0031269`). **R08 emits no macro for `2.5`,
for that ratio, or for `eta_rmse_over_sigma`**, and `R08_claims.tex` says so in its comment block.

---

## 5. Reproducibility and the whole suite

```bash
./run_experiment_R08.sh                 # 154 s total, 48 workers: _a 77 s (module A 60.7 s,
                                        #   module B 8.8 s), _b 78 s
./run_experiment_R08.sh --n-jobs 1      # 3534 s total, 1 worker: _a 1775 s (module A 1555 s,
                                        #   module B 213 s), _b 1759 s
pytest tests/ -v
```

`run_all.sh` discovers `run_experiment_R08.sh` by sorted enumeration. **Neither `run_all.sh` nor
`run_tests.sh` nor `logs/all_tests.log` is modified** — `git status --porcelain` shows the first two
untouched and the third carrying only the change it already had before this stream started.

### C8, both digest sets pasted as-is

Run 1, default (48 workers):

```
167bc67f6913ebea6fe5023c62a9638259a1036028821d0fa051339ea772f675  results/R08_adverse_lattice/data/R08_adverse_bias.csv
7134ae5e2cc683f18fbbf7efb0c32dbebd68cabbf36e06fc5b880d1710e00893  results/R08_adverse_lattice/data/R08_lattice_exact_law.csv
01abacb1f055f2006d4cf32f3f630003813180f0bdb3da5bb3b839c76e7df611  results/R08_adverse_lattice/data/R08_null_law_lattice.csv
f80e06d2d24de02b0878a840e89acfd6aa622c633468a0032c0cce93141913d6  results/R08_adverse_lattice/data/R08_operator_levels.csv
0492b16f924e68779a22bfdb60820ef1c531483b09c211e425c06422f895b917  results/R08_adverse_lattice/data/R08_pairing_diagnostic.csv
74966cbc8610970f25dc7597664002b7c34d4d2c75a1a5106689543b7fc277f5  results/R08_adverse_lattice/figures/fig08_adverse_lattice.png
6a5f743e5920c8043358e20a3013026f994a94f5e019f186fca52e0a4c1dc9c6  results/R08_adverse_lattice/tables/R08_claims.tex
```

Run 2, `--n-jobs 1`:

```
167bc67f6913ebea6fe5023c62a9638259a1036028821d0fa051339ea772f675  results/R08_adverse_lattice/data/R08_adverse_bias.csv
7134ae5e2cc683f18fbbf7efb0c32dbebd68cabbf36e06fc5b880d1710e00893  results/R08_adverse_lattice/data/R08_lattice_exact_law.csv
01abacb1f055f2006d4cf32f3f630003813180f0bdb3da5bb3b839c76e7df611  results/R08_adverse_lattice/data/R08_null_law_lattice.csv
f80e06d2d24de02b0878a840e89acfd6aa622c633468a0032c0cce93141913d6  results/R08_adverse_lattice/data/R08_operator_levels.csv
0492b16f924e68779a22bfdb60820ef1c531483b09c211e425c06422f895b917  results/R08_adverse_lattice/data/R08_pairing_diagnostic.csv
74966cbc8610970f25dc7597664002b7c34d4d2c75a1a5106689543b7fc277f5  results/R08_adverse_lattice/figures/fig08_adverse_lattice.png
6a5f743e5920c8043358e20a3013026f994a94f5e019f186fca52e0a4c1dc9c6  results/R08_adverse_lattice/tables/R08_claims.tex
```

`diff` between the two sets is **empty on all seven artefacts**. Every task of this stream is keyed
on its role and index alone — `("trajectory", i)` for module A, `("lattice_stream", index)` for
module B, `("resample", <name>)` for every null — and the chunk boundaries are fixed constants
(`CHUNK_SIZE = 50`, `LATTICE_CHUNK_SIZE = 2000`), so the worker count cannot reach any draw and
cannot move a reassembly order. That is what this axis tests.

**`_b` certifies the same identity a third way.** It re-runs the campaign in memory rather than
reloading `_a`'s CSVs (preamble §S7 forbids a disk round trip as a memory bridge, and the delivered
`Priorite_21c` used exactly that bridge without `float_precision='round_trip'`), then re-serialises
the five frames it holds through `save_fair_csv` into a `tempfile.TemporaryDirectory()` and compares
their digests with the files `_a` wrote. All five match on both runs, so the figure and the macros
are certified to describe the persisted campaign rather than assumed to.

### The whole suite, `pytest tests/ -v`, pasted verbatim

**412 tests collected, 412 passed, 0 failures**, of which **26 are R08's**.

```
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-9.0.3, pluggy-1.6.0 -- /home/m53/miniforge3/envs/Trading/bin/python3
rootdir: /home/m53/The-Whitening-Advantage-Experiments
plugins: anyio-4.8.0
collecting ... collected 412 items

tests/test_R01_claims.py::test_r01_models PASSED                         [  0%]
tests/test_R01_claims.py::test_r01_trajectories PASSED                   [  0%]
tests/test_R01_claims.py::test_r01_injection_summary PASSED              [  0%]
tests/test_R01_claims.py::test_r01_placebo PASSED                        [  0%]
tests/test_R01_claims.py::test_r01_magnitude_and_symmetry PASSED         [  1%]
tests/test_R02_claims.py::test_stream_counts PASSED                      [  1%]
tests/test_R02_claims.py::test_classifier_integrity PASSED               [  1%]
tests/test_R02_claims.py::test_data_rejection_rates PASSED               [  1%]
tests/test_R02_claims.py::test_distinct_p_concept PASSED                 [  2%]
tests/test_R02_claims.py::test_independence_diagnostics PASSED           [  2%]
tests/test_R02_claims.py::test_iid_arm_rejection_is_reported_not_asserted PASSED [  2%]
tests/test_R02_claims.py::test_concept_level_covered_by_wilson PASSED    [  2%]
tests/test_R02_claims.py::test_max_clustered_pvalue_below_manuscript_bound PASSED [  3%]
tests/test_R02b_claims.py::test_negative_control_integrity PASSED        [  3%]
tests/test_R02b_claims.py::test_nu_seven_is_indistinguishable_from_nominal PASSED [  3%]
tests/test_R02b_claims.py::test_heavy_tail_arms_exclude_nominal PASSED   [  3%]
tests/test_R02b_claims.py::test_rate_ordering_heavy_versus_light PASSED  [  4%]
tests/test_R02b_claims.py::test_negative_control_matches_squared_at_light_tails PASSED [  4%]
tests/test_R02c_claims.py::test_R02c_seed_uniqueness PASSED              [  4%]
tests/test_R02c_claims.py::test_R02c_negative_control_calibration PASSED [  4%]
tests/test_R02c_claims.py::test_R02c_eighth_moment_account_is_refuted PASSED [  5%]
tests/test_R02c_claims.py::test_R02c_slope_test_power_is_declared PASSED [  5%]
tests/test_R02c_claims.py::test_R02c_control_arm_integrity PASSED        [  5%]
tests/test_R02c_claims.py::test_R02c_continuity PASSED                   [  5%]
tests/test_R02c_claims.py::test_R02c_mechanism_slope_logic PASSED        [  6%]
tests/test_R03_claims.py::test_R03_grid_cardinality PASSED               [  6%]
tests/test_R03_claims.py::test_R03_grid_is_unchanged PASSED              [  6%]
tests/test_R03_claims.py::test_R03_threshold_ordering_is_structural PASSED [  6%]
tests/test_R03_claims.py::test_R03_monotonicity_beyond_gamma_six PASSED  [  7%]
tests/test_R03_claims.py::test_R03_aggregate_certification_gates PASSED  [  7%]
tests/test_R03_claims.py::test_R03_gamma_rule_holds_the_nominal_level PASSED [  7%]
tests/test_R03_claims.py::test_R03_iid_calibration_arm_is_well_formed PASSED [  7%]
tests/test_R03_claims.py::test_R03_deviation_classification_against_witness PASSED [  8%]
tests/test_R03_claims.py::test_R03_macros_are_emitted PASSED             [  8%]
tests/test_R04_claims.py::test_R04_cardinalities PASSED                  [  8%]
tests/test_R04_claims.py::test_R04_grids_match_v87 PASSED                [  8%]
tests/test_R04_claims.py::test_R04_horizon_and_sample_size PASSED        [  8%]
tests/test_R04_claims.py::test_R04_reference_drifts_are_coherent PASSED  [  9%]
tests/test_R04_claims.py::test_R04_all_arms_are_iso_fpr PASSED           [  9%]
tests/test_R04_claims.py::test_R04_concept_threshold_is_flat_in_gamma PASSED [  9%]
tests/test_R04_claims.py::test_R04_concept_level_is_homogeneous_in_gamma PASSED [  9%]
tests/test_R04_claims.py::test_R04_recalib_blind_zone_persists_at_lowest_gamma PASSED [ 10%]
tests/test_R04_claims.py::test_R04_recalib_is_slower_than_both_first_order_arms PASSED [ 10%]
tests/test_R04_claims.py::test_R04_add_decreases_with_drift_magnitude PASSED [ 10%]
tests/test_R04_claims.py::test_R04_conditional_mean_is_labelled_and_accompanied PASSED [ 10%]
tests/test_R04_claims.py::test_R04_efficiency_ratio_is_monotone_in_nu PASSED [ 11%]
tests/test_R04_claims.py::test_R04_ratio_respects_the_gaussian_ceiling PASSED [ 11%]
tests/test_R04_claims.py::test_R04_predicted_ratio_is_the_pitman_constant PASSED [ 11%]
tests/test_R04_claims.py::test_R04_oracle_is_never_slower_than_the_fitted_arm PASSED [ 11%]
tests/test_R04_claims.py::test_R04_analytic_crossing_matches_v87 PASSED  [ 12%]
tests/test_R04_claims.py::test_R04_blind_zone_onset_matches_v87 PASSED   [ 12%]
tests/test_R04_claims.py::test_R04_macros_are_emitted_and_computed PASSED [ 12%]
tests/test_R04_claims.py::test_R04_crossings_agree_with_the_interpolation_rule PASSED [ 12%]
tests/test_R04_claims.py::test_R04_emitted_crossing_brackets_contain_the_crossing PASSED [ 13%]
tests/test_R04_claims.py::test_R04_table3_printing_rule_reproduces_v87 PASSED [ 13%]
tests/test_R04_claims.py::test_R04_table3_is_generated_from_the_csv PASSED [ 13%]
tests/test_R04_claims.py::test_R04_table3_shows_detrate_exactly_when_below_one PASSED [ 13%]
tests/test_R04_claims.py::test_R04_intervals_are_clamped_and_ordered PASSED [ 14%]
tests/test_R04_claims.py::test_R04_no_nan_in_reported_delays PASSED      [ 14%]
tests/test_R04_claims.py::test_R04_m0_universality_arm_matches_the_garch_arm PASSED [ 14%]
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
PASSED       [ 14%]
tests/test_R04b_claims.py::test_R04b_cardinality_and_grid PASSED         [ 15%]
tests/test_R04b_claims.py::test_R04b_protocol_constants_match_v87 PASSED [ 15%]
tests/test_R04b_claims.py::test_R04b_gamma_target_is_attainable_and_realised PASSED [ 15%]
tests/test_R04b_claims.py::test_R04b_analytic_prediction_is_the_pitman_constant PASSED [ 15%]
tests/test_R04b_claims.py::test_R04b_in_sample_bisection_converged PASSED [ 16%]
tests/test_R04b_claims.py::test_R04b_pooled_holdout_level_meets_the_promised_band PASSED [ 16%]
tests/test_R04b_claims.py::test_R04b_conditional_calibration_pvalues_are_uniform PASSED [ 16%]
tests/test_R04b_claims.py::test_R04b_rates_are_consistent_and_clamped PASSED [ 16%]
tests/test_R04b_claims.py::test_R04b_continuity_anchors_are_read_from_R04 PASSED [ 16%]
tests/test_R04b_claims.py::test_R04b_is_compatible_with_R04_at_the_common_points PASSED [ 17%]
tests/test_R04b_claims.py::test_R04b_grid_bracket_straddles_unity_and_the_interpolation_lies_inside_it PASSED [ 17%]
tests/test_R04b_claims.py::test_R04b_inferential_bracket_is_recomputable_from_the_csv PASSED [ 17%]
tests/test_R04b_claims.py::test_R04b_bootstrap_error_exceeds_the_conditional_one PASSED [ 17%]
tests/test_R04b_claims.py::test_R04b_shape_fit_is_reported_with_its_goodness PASSED [ 18%]
tests/test_R04b_claims.py::test_R04b_analytic_crossing_matches_v87 PASSED [ 18%]
tests/test_R04b_claims.py::test_R04b_estimation_cost_interval_arithmetic PASSED [ 18%]
tests/test_R04b_claims.py::test_R04b_ratio_respects_the_gaussian_ceiling PASSED [ 18%]
tests/test_R04b_claims.py::test_R04b_oracle_ratio_does_not_cross_again_above_seven PASSED [ 19%]
tests/test_R04b_claims.py::test_R04b_macros_are_emitted_and_computed PASSED [ 19%]
tests/test_R04b_claims.py::test_R04b_no_nan_in_reported_quantities PASSED [ 19%]
tests/test_R04b_claims.py::test_R04b_report_against_v87 PASSED           [ 19%]
tests/test_R05_claims.py::test_abrupt_cardinality PASSED                 [ 20%]
tests/test_R05_claims.py::test_ramp_cardinalities PASSED                 [ 20%]
tests/test_R05_claims.py::test_protocol_constants PASSED                 [ 20%]
tests/test_R05_claims.py::test_horizons_are_the_two_published_budgets PASSED [ 20%]
tests/test_R05_claims.py::test_common_horizon_is_constant_across_gamma PASSED [ 21%]
tests/test_R05_claims.py::test_null_levels_are_homogeneous_across_gamma PASSED [ 21%]
tests/test_R05_claims.py::test_concept_branch_is_gamma_invariant_by_construction PASSED [ 21%]
tests/test_R05_claims.py::test_concept_is_blind_to_the_scale_pathology PASSED [ 21%]
tests/test_R05_claims.py::test_positive_control_shows_the_monitor_responsive PASSED [ 22%]
tests/test_R05_claims.py::test_both_crossovers_are_emitted_and_are_distinct PASSED [ 22%]
tests/test_R05_claims.py::test_scaling_law_branches_meet_at_the_crossover PASSED [ 22%]
tests/test_R05_claims.py::test_ladder_visits_the_three_published_horizons PASSED [ 22%]
tests/test_R05_claims.py::test_ladder_is_monotone_in_the_horizon PASSED  [ 23%]
tests/test_R05_claims.py::test_ladder_agrees_with_the_campaigns_it_overlaps PASSED [ 23%]
tests/test_R05_claims.py::test_sixth_moment_boundary_matches_the_published_gamma PASSED [ 23%]
tests/test_R05_claims.py::test_moment_margin_macro_matches_the_published_bound PASSED [ 23%]
tests/test_R05_claims.py::test_macro_file_is_well_formed PASSED          [ 24%]
tests/test_R05_claims.py::test_required_macros_are_present PASSED        [ 24%]
tests/test_R05_claims.py::test_figure_exists PASSED                      [ 24%]
tests/test_R05_claims.py::test_text_artefacts_end_with_a_newline PASSED  [ 24%]
tests/test_R05_claims.py::test_superseded_witness_is_documented_not_regenerated PASSED [ 25%]
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
PASSED    [ 25%]
tests/test_R06_claims.py::test_R06_cardinalities_and_grid PASSED         [ 25%]
tests/test_R06_claims.py::test_R06_gamma_grid_is_realised_in_closed_form PASSED [ 25%]
tests/test_R06_claims.py::test_R06_fourth_moment_boundary_is_computed_not_hard_coded PASSED [ 25%]
tests/test_R06_claims.py::test_R06_boundary_is_not_confused_with_the_nearest_grid_point PASSED [ 26%]
tests/test_R06_claims.py::test_R06_panel_A_design_is_paired_and_declared PASSED [ 26%]
tests/test_R06_claims.py::test_R06_pooled_binary_level_covers_nominal_at_cluster_precision PASSED [ 26%]
tests/test_R06_claims.py::test_R06_counterfactual_arm_removes_the_pairing PASSED [ 26%]
tests/test_R06_claims.py::test_R06_no_per_gamma_gate_is_possible PASSED  [ 27%]
tests/test_R06_claims.py::test_R06_squared_stream_rejects_massively PASSED [ 27%]
tests/test_R06_claims.py::test_R06_task_boundaries_saturate PASSED       [ 27%]
tests/test_R06_claims.py::test_R06_intermediate_threshold_is_reported_and_labelled PASSED [ 27%]
tests/test_R06_claims.py::test_R06_median_task_control_covers_nominal_and_is_weakly_resolved PASSED [ 28%]
tests/test_R06_claims.py::test_R06_no_silent_fallback_survived_into_the_artefacts PASSED [ 28%]
tests/test_R06_claims.py::test_R06_reproduces_the_witness_byte_for_byte PASSED [ 28%]
tests/test_R06_claims.py::test_R06_macros_are_emitted_and_computed PASSED [ 28%]
tests/test_R06_claims.py::test_R06_report_against_the_witness PASSED     [ 29%]
tests/test_R07_claims.py::test_R07_every_artefact_the_plan_lists_exists_with_its_prescribed_schema PASSED [ 29%]
tests/test_R07_claims.py::test_R07_the_lattice_law_reproduces_under_an_independent_dynamic_program PASSED [ 29%]
tests/test_R07_claims.py::test_R07_the_two_attainable_levels_bracket_five_percent_and_fix_lambda_star PASSED [ 29%]
tests/test_R07_claims.py::test_R07_the_dynamic_program_agrees_with_exhaustive_enumeration PASSED [ 30%]
tests/test_R07_claims.py::test_R07_the_fourth_moment_product_of_L308_reproduces_in_closed_form PASSED [ 30%]
tests/test_R07_claims.py::test_R07_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 30%]
tests/test_R07_claims.py::test_R07_the_naive_arm_and_the_oracle_arm_coincide_at_phi_zero PASSED [ 30%]
tests/test_R07_claims.py::test_R07_the_oracle_arm_is_exactly_phi_invariant PASSED [ 31%]
tests/test_R07_claims.py::test_R07_the_design_effect_is_measured_on_every_pooled_quantity PASSED [ 31%]
tests/test_R07_claims.py::test_R07_the_ljungbox_rejection_of_L308_climbs_monotonically_in_phi PASSED [ 31%]
tests/test_R07_claims.py::test_R07_every_ols_cell_matches_the_oracle_band_of_the_figure7_caption PASSED [ 31%]
tests/test_R07_claims.py::test_R07_the_ols_envelopes_stay_inside_the_two_bands_L308_prints PASSED [ 32%]
tests/test_R07_claims.py::test_R07_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 32%]
tests/test_R07_claims.py::test_R07_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 32%]
tests/test_R07_claims.py::test_R07_every_produced_text_file_ends_in_a_newline PASSED [ 32%]
tests/test_R07_claims.py::test_R07_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 33%]
tests/test_R07_claims.py::test_R07_the_produced_sources_carry_no_banned_construct PASSED [ 33%]
tests/test_R07_claims.py::test_R07_the_comparison_operator_is_the_same_on_both_paths PASSED [ 33%]
tests/test_R07_claims.py::test_R07_the_seven_carried_primitives_are_byte_identical_to_the_witness PASSED [ 33%]
tests/test_R07_claims.py::test_R07_the_three_monte_carlo_numerals_of_L308_move_within_their_own_sampling_error PASSED [ 33%]
tests/test_R07_claims.py::test_R07_the_bias_bound_of_L308_is_exceeded_by_the_regenerated_campaign PASSED [ 34%]
tests/test_R07_claims.py::test_R07_the_exact_lattice_levels_differ_from_the_two_numerals_v87_prints PASSED [ 34%]
tests/test_R07_claims.py::test_R07_the_eta_decay_is_not_one_over_root_n PASSED [ 34%]
tests/test_R07_claims.py::test_R07_report_the_campaign_against_its_witness PASSED [ 34%]
tests/test_R07_claims.py::test_R07_report_the_design_effect_of_every_pooled_quantity PASSED [ 35%]
tests/test_R07_claims.py::test_R07_report_the_counterfactual_ladder PASSED [ 35%]
tests/test_R07_claims.py::test_R07_report_the_candidate_readings_of_the_dispersion_cost_numeral PASSED [ 35%]
tests/test_R07_claims.py::test_R07_report_the_float_drift_on_the_lattice_boundary PASSED [ 35%]
tests/test_R08_claims.py::test_R08_every_artefact_the_plan_lists_exists_with_its_prescribed_schema PASSED [ 36%]
tests/test_R08_claims.py::test_R08_the_operating_threshold_is_fifty_seven_lattice_units PASSED [ 36%]
tests/test_R08_claims.py::test_R08_the_exact_lattice_law_reproduces_under_an_independent_dynamic_program PASSED [ 36%]
tests/test_R08_claims.py::test_R08_the_enumeration_validation_agrees_with_an_independent_enumeration PASSED [ 36%]
tests/test_R08_claims.py::test_R08_the_three_streams_agree_on_the_cells_they_share PASSED [ 37%]
tests/test_R08_claims.py::test_R08_the_bracketing_of_the_nominal_level_is_the_one_L241_states PASSED [ 37%]
tests/test_R08_claims.py::test_R08_the_wilson_intervals_reproduce_from_a_second_algebraic_form PASSED [ 37%]
tests/test_R08_claims.py::test_R08_one_comparison_operator_is_shared_by_both_modules PASSED [ 37%]
tests/test_R08_claims.py::test_R08_the_carried_primitives_are_byte_identical_to_both_owning_files PASSED [ 38%]
tests/test_R08_claims.py::test_R08_the_two_dgp_primitives_are_ast_identical_across_their_two_owners PASSED [ 38%]
tests/test_R08_claims.py::test_R08_the_cross_stream_identity_with_R07_is_exact PASSED [ 38%]
tests/test_R08_claims.py::test_R08_the_sign_asymmetry_of_L311_holds_in_both_directions PASSED [ 38%]
tests/test_R08_claims.py::test_R08_the_three_point_bound_of_L311_holds_with_its_extremum_envelope PASSED [ 39%]
tests/test_R08_claims.py::test_R08_the_family_wise_arithmetic_is_logged_before_any_gate_is_read PASSED [ 39%]
tests/test_R08_claims.py::test_R08_macros_are_emitted_and_agree_with_the_frames PASSED [ 39%]
tests/test_R08_claims.py::test_R08_text_artefacts_end_with_a_newline PASSED [ 39%]
tests/test_R08_claims.py::test_R08_no_confirmatory_language_in_the_scripts_the_logs_or_the_section PASSED [ 40%]
tests/test_R08_claims.py::test_R08_the_scripts_own_S4_4_pattern_accepts_the_preambles_language PASSED [ 40%]
tests/test_R08_claims.py::test_R08_the_produced_sources_carry_no_banned_construct PASSED [ 40%]
tests/test_R08_claims.py::test_R08_the_monte_carlo_numerals_of_L241_and_L311_move_within_their_own_sampling_error PASSED [ 40%]
tests/test_R08_claims.py::test_R08_the_level_the_implemented_operator_delivers_at_lambda_star_is_above_nominal PASSED [ 41%]
tests/test_R08_claims.py::test_R08_the_implemented_float_test_coincides_with_the_weak_operator PASSED [ 41%]
tests/test_R08_claims.py::test_R08_the_whiteness_gap_maximum_has_moved_from_the_witness_campaign PASSED [ 41%]
tests/test_R08_claims.py::test_R08_report_deviation_classification 
  R08 deviation classification against v87, at the manuscript's printing precision
  site                                       printed   regenerated  degree  source cell
  L241 level at lambda = 11.2                 0.0503      0.050815  D2      R08_null_law_lattice.csv, lambda=11.2, P_exceed_strict
  L241 level at lambda = 11.4                 0.0429       0.04323  D2      R08_null_law_lattice.csv, lambda=11.4, P_exceed_strict
  L241 lambda*                                  11.4          11.4  D0      R08_null_law_lattice.csv, bracket_role=below_nominal
  Fig. 8 (B) FPR collapses to                 0.0086        0.0095  D2      R08_adverse_bias.csv, b=0.15, fpr_biased
  Fig. 8 (B) FPR inflates to                   0.208          0.21  D2      R07_estmean_lb_fpr.csv, NAIVE, phi=0.15, fpr_concept
  L311 whiteness gap bound (points)                3          2.21  D2      R08_pairing_diagnostic.csv, whiteness_bound
  L311 penalty at momentum 0.02 (points)         1.1          1.28  D2      R07_estmean_lb_fpr.csv, NAIVE, phi in (0, 0.02)
  L311 whiteness range, low end                 0.05        0.0478  D1      R08_adverse_bias.csv, min over both arms
  L311 whiteness range, high end                   1        0.9984  D1      R08_adverse_bias.csv, max over both arms
  The witness is a record of the submitted campaign, not a target; see data/reference/README.md.
  witness [21c] b = 0.0   : lb 0.0485 -> 0.0478, fpr 0.0546 -> 0.0520, naive lb 0.0509 -> 0.0492, naive fpr 0.0535 -> 0.0516
  witness [21c] b = 0.02  : lb 0.0642 -> 0.0647, fpr 0.0441 -> 0.0429, naive lb 0.0685 -> 0.0704, naive fpr 0.0640 -> 0.0644
  witness [21c] b = 0.05  : lb 0.1918 -> 0.1943, fpr 0.0307 -> 0.0309, naive lb 0.2045 -> 0.2151, naive fpr 0.0836 -> 0.0854
  witness [21c] b = 0.075 : lb 0.4700 -> 0.4815, fpr 0.0235 -> 0.0238, naive lb 0.4984 -> 0.5036, naive fpr 0.1134 -> 0.1094
  witness [21c] b = 0.1   : lb 0.8031 -> 0.8003, fpr 0.0168 -> 0.0175, naive lb 0.8076 -> 0.8202, naive fpr 0.1369 -> 0.1377
  witness [21c] b = 0.15  : lb 0.9984 -> 0.9984, fpr 0.0086 -> 0.0095, naive lb 0.9979 -> 0.9979, naive fpr 0.2076 -> 0.2100
  witness [21d] lambda = 11     (55 units): P_exceed 0.059150 -> strict 0.060200, weak 0.070360, exact strict 0.059900
  witness [21d] lambda = 11.2   (56 units): P_exceed 0.050270 -> strict 0.050815, weak 0.060200, exact strict 0.051021
  witness [21d] lambda = 11.4   (57 units): P_exceed 0.042870 -> strict 0.043230, weak 0.050815, exact strict 0.043428
  witness [21d] lambda = 11.6   (58 units): P_exceed 0.036470 -> strict 0.036705, weak 0.043230, exact strict 0.036945
  witness [21d] lambda = 11.8   (59 units): P_exceed 0.031075 -> strict 0.031170, weak 0.036705, exact strict 0.031414
  witness [21d] lambda = 12     (60 units): P_exceed 0.026540 -> strict 0.026320, weak 0.031170, exact strict 0.026700
PASSED [ 41%]
tests/test_R08_claims.py::test_R08_report_the_operator_levels_and_the_boundary_counter 
  R08 the level each comparison operator delivers (control C1)
    lambda  units  float M > l   units > l  units >= l  d(strict)  d(weak)  boundary
        11     55     0.070360    0.060200    0.070360       2032        0      2032
      11.2     56     0.060200    0.050815    0.060200       1877        0      1877
      11.4     57     0.050815    0.043230    0.050815       1517        0      1517
      11.6     58     0.043230    0.036705    0.043230       1305        0      1305
      11.8     59     0.036705    0.031170    0.036705       1107        0      1107
        12     60     0.031170    0.026320    0.031170        970        0       970
  Float position against the exact lattice point over 200000 streams: above 192842, below 2776, exactly on 4382; within 4 ulp 78971.
  The four exact levels L241's two thresholds carry: strict(11.2) = 5.1021%, weak(11.2) = 5.9900%, strict(11.4) = 4.3428%, weak(11.4) = 5.1021%. The rule L241 states promises 'at or below nominal' and the operator the code implements delivers the last of the four.
PASSED [ 41%]
tests/test_R08_claims.py::test_R08_report_the_pairing_diagnostic_and_the_control_nulls 
  R08 the paired design behind panels A and B (controls C4, C5, C6)
        b  lb biased  lb naive   gap pt  discord   rho_lb  deff_lb  fpr biased  fpr naive  rho_fpr
    0.000     0.0478    0.0492    -0.14      454   0.5082   1.5082      0.0520     0.0516   0.5684
    0.020     0.0647    0.0704    -0.57      739   0.4139   1.4139      0.0429     0.0644   0.5396
    0.050     0.1943    0.2151    -2.08     2630   0.1932   1.1932      0.0309     0.0854   0.4706
    0.075     0.4815    0.5036    -2.21     4889   0.0225   1.0225      0.0238     0.1094   0.3425
    0.100     0.8003    0.8202    -1.99     3211  -0.0437   0.9563      0.0175     0.1377   0.2565
    0.150     0.9984    0.9979     0.05       37  -0.0018   0.9982      0.0095     0.2100   0.1393
  Family-wise arithmetic: gating on all 6 proportion tests at 0.05 would trigger with probability 26.4908% under equality itself, which is why it is not a gate.
  3 of 6 proportion tests reject: [(0.05, 0.00026716158404238577), (0.075, 0.0017734684466137463), (0.1, 0.0003323256056320112)]. The Figure 8 caption's parenthetical is a statement of mechanism, symmetric by construction; it is not contradicted by a difference in measured rate.
  [ks_calibration] KS of the six pval_lb against Uniform(0,1): observed 0.558384, tabulated p 0.027418, null quantile 0.535964, null p 0.038000, 2000 replicates
  [sign_flip_null_max] max |delta_lb_pp| over the b grid: observed 0.022100, null quantile 0.022300, null p 0.001100, 10000 replicates
  [sign_flip_null_max] max |delta_fpr_pp| over the b grid: observed 0.200500, null quantile 0.015100, null p 0.000000, 10000 replicates
  [whiteness_bound] max |delta_lb_pp| in points, against L311s three-point bound: observed 2.210000, null quantile 3.000000, 95% envelope [1.5600, 3.6100], 2000 replicates
PASSED [ 42%]
tests/test_R09_claims.py::test_R09_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 42%]
tests/test_R09_claims.py::test_R09_every_sample_size_the_campaign_used_is_carried_on_the_row PASSED [ 42%]
tests/test_R09_claims.py::test_R09_the_mixture_martingale_remains_bounded_by_alpha_under_continuous_monitoring PASSED [ 42%]
tests/test_R09_claims.py::test_R09_only_the_mixture_controls_the_time_uniform_rate PASSED [ 43%]
tests/test_R09_claims.py::test_R09_the_ecusum_arl0_satisfies_the_reciprocal_of_alpha PASSED [ 43%]
tests/test_R09_claims.py::test_R09_the_peeking_horizon_is_four_times_the_calibration_horizon PASSED [ 43%]
tests/test_R09_claims.py::test_R09_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 43%]
tests/test_R09_claims.py::test_R09_the_mixture_threshold_is_villes_threshold_on_the_mixture_value PASSED [ 44%]
tests/test_R09_claims.py::test_R09_the_cusum_statistic_lives_on_the_two_delta_lattice PASSED [ 44%]
tests/test_R09_claims.py::test_R09_the_one_sided_kolmogorov_statistic_is_the_supremum_it_names PASSED [ 44%]
tests/test_R09_claims.py::test_R09_the_arl0_lower_bound_is_recomputed_from_the_persisted_columns PASSED [ 44%]
tests/test_R09_claims.py::test_R09_no_arl0_is_persisted_without_its_censored_fraction PASSED [ 45%]
tests/test_R09_claims.py::test_R09_the_macro_emitter_refuses_a_censored_arl0 PASSED [ 45%]
tests/test_R09_claims.py::test_R09_the_bound_flag_is_a_computed_comparison_not_a_literal PASSED [ 45%]
tests/test_R09_claims.py::test_R09_the_level_granularity_column_states_the_lattice_it_names PASSED [ 45%]
tests/test_R09_claims.py::test_R09_the_descriptive_binomial_p_values_are_the_exact_one_sided_tail PASSED [ 46%]
tests/test_R09_claims.py::test_R09_the_add_column_is_conditional_and_the_detection_rate_says_so PASSED [ 46%]
tests/test_R09_claims.py::test_R09_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 46%]
tests/test_R09_claims.py::test_R09_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 46%]
tests/test_R09_claims.py::test_R09_the_ecusum_censored_fraction_is_not_zero PASSED [ 47%]
tests/test_R09_claims.py::test_R09_every_produced_text_file_ends_in_a_newline PASSED [ 47%]
tests/test_R09_claims.py::test_R09_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 47%]
tests/test_R09_claims.py::test_R09_the_produced_sources_carry_no_banned_construct PASSED [ 47%]
tests/test_R09_claims.py::test_R09_the_orchestrator_passes_the_control_arm_and_never_calls_pytest PASSED [ 48%]
tests/test_R09_claims.py::test_R09_the_shared_orchestrators_are_untouched PASSED [ 48%]
tests/test_R09_claims.py::test_R09_the_three_monte_carlo_numerals_of_L243_does_not_reproduce_at_printed_precision PASSED [ 48%]
tests/test_R09_claims.py::test_R09_the_calibrated_level_and_the_stream_count_still_reproduces_v87s_numerals PASSED [ 48%]
tests/test_R09_claims.py::test_R09_report_the_campaign_against_its_witness PASSED [ 49%]
tests/test_R09_claims.py::test_R09_report_the_published_numerals_at_their_printed_precision PASSED [ 49%]
tests/test_R09_claims.py::test_R09_report_the_censoring_that_makes_panel_c_a_horizon_artefact PASSED [ 49%]
tests/test_R09_claims.py::test_R09_report_the_control_outcomes_the_log_records PASSED [ 49%]
tests/test_R10_claims.py::test_R10_every_artefact_the_plan_lists_exists_with_its_prescribed_schema PASSED [ 50%]
tests/test_R10_claims.py::test_R10_the_operating_threshold_is_seventy_five_lattice_units PASSED [ 50%]
tests/test_R10_claims.py::test_R10_the_half_arm_law_reproduces_under_an_independent_dynamic_program PASSED [ 50%]
tests/test_R10_claims.py::test_R10_the_bernoulli_twin_reduces_to_the_fair_coin_at_one_half PASSED [ 50%]
tests/test_R10_claims.py::test_R10_the_enumeration_validation_agrees_with_an_independent_enumeration PASSED [ 50%]
tests/test_R10_claims.py::test_R10_the_wilson_intervals_reproduce_from_a_second_algebraic_form PASSED [ 51%]
tests/test_R10_claims.py::test_R10_q_star_reproduces_from_the_student_t_survival_function PASSED [ 51%]
tests/test_R10_claims.py::test_R10_the_caption_stream_count_is_one_thousand_per_point PASSED [ 51%]
tests/test_R10_claims.py::test_R10_the_sign_stream_is_bit_identically_the_innovation_sign PASSED [ 51%]
tests/test_R10_claims.py::test_R10_no_degraded_path_is_taken PASSED      [ 52%]
tests/test_R10_claims.py::test_R10_the_standardisation_constants_are_one_deterministic_input PASSED [ 52%]
tests/test_R10_claims.py::test_R10_the_fixed_half_cusum_explodes_with_asymmetry PASSED [ 52%]
tests/test_R10_claims.py::test_R10_recentering_restores_false_alarm_control PASSED [ 52%]
tests/test_R10_claims.py::test_R10_the_carried_primitives_are_byte_identical_to_both_owning_files PASSED [ 53%]
tests/test_R10_claims.py::test_R10_the_family_wise_arithmetic_is_logged_before_any_gate_is_read PASSED [ 53%]
tests/test_R10_claims.py::test_R10_macros_are_emitted_and_agree_with_the_frames PASSED [ 53%]
tests/test_R10_claims.py::test_R10_text_artefacts_end_with_a_newline PASSED [ 53%]
tests/test_R10_claims.py::test_R10_no_confirmatory_language_in_the_script_the_log_or_the_section PASSED [ 54%]
tests/test_R10_claims.py::test_R10_the_three_monte_carlo_numerals_of_L290_move_within_their_own_sampling_error PASSED [ 54%]
tests/test_R10_claims.py::test_R10_the_caption_fpr_envelope_has_moved_at_its_upper_end PASSED [ 54%]
tests/test_R10_claims.py::test_R10_the_symmetric_grid_point_is_not_centred_on_one_half PASSED [ 54%]
tests/test_R10_claims.py::test_R10_the_implemented_threshold_test_coincides_with_the_weak_operator PASSED [ 55%]
tests/test_R10_claims.py::test_R10_report_deviation_classification 
  R10 deviation classification against v87, at the manuscript's printing precision
  site                                 printed   regenerated  z_paired  degree  source cell
  L290 realized skewness                 -1.44      -1.42796      1.95  D2      R10_skew_diagnostics.csv, xi=0.5, skewness
  L290 marginal rate q                    0.58      0.582191      8.76  D1      R10_skew_diagnostics.csv, xi=0.5, q
  L290 fixed-1/2 CUSUM fires at           0.97         0.966     -0.49  D1      R10_skew_fpr.csv, xi=0.5, fpr_half_rate
  Fig. 10 caption FPR lower end           0.01          0.01       nan  D0      R10_skew_fpr.csv, min fpr_qhat_rate
  Fig. 10 caption FPR upper end          0.018         0.015       nan  D2      R10_skew_fpr.csv, max fpr_qhat_rate
  The witness is a record of the submitted campaign, not a target; see data/reference/README.md.
  witness [diagnostics] xi = 1.0  : skewness 0.00286738 -> -0.000229514, q 0.499682 -> 0.499485
  witness [diagnostics] xi = 0.85 : skewness -0.47769 -> -0.474218, q 0.529572 -> 0.52947
  witness [diagnostics] xi = 0.65 : skewness -1.09725 -> -1.08484, q 0.564269 -> 0.564079
  witness [diagnostics] xi = 0.5  : skewness -1.44285 -> -1.42796, q 0.5823 -> 0.582191
  witness [fpr] xi = 1.0  : lb_ebin_rate 0.051 -> 0.047, lb_sign_rate 0.051 -> 0.05, fpr_half_rate 0.006 -> 0.005, fpr_oracle_rate 0.005 -> 0.004, fpr_qhat_rate 0.018 -> 0.01
  witness [fpr] xi = 0.85 : lb_ebin_rate 0.045 -> 0.048, lb_sign_rate 0.055 -> 0.063, fpr_half_rate 0.047 -> 0.041, fpr_oracle_rate 0.002 -> 0.009, fpr_qhat_rate 0.018 -> 0.014
  witness [fpr] xi = 0.65 : lb_ebin_rate 0.055 -> 0.048, lb_sign_rate 0.053 -> 0.046, fpr_half_rate 0.63 -> 0.596, fpr_oracle_rate 0.002 -> 0.005, fpr_qhat_rate 0.01 -> 0.011
  witness [fpr] xi = 0.5  : lb_ebin_rate 0.058 -> 0.057, lb_sign_rate 0.056 -> 0.05, fpr_half_rate 0.969 -> 0.966, fpr_oracle_rate 0.003 -> 0.004, fpr_qhat_rate 0.011 -> 0.015
PASSED [ 55%]
tests/test_R10_claims.py::test_R10_report_design_effect_and_extremum_envelopes 
  R10 design effect of every quantity pooled across the xi grid (control C9)
  statistic    cells   rho_bar     deff     n_eff    pooled  SE inflation
  lb_sign          4    0.0624   1.1872    3369.4   0.05225        1.0896
  lb_ebin          4    0.0072   1.0216    3915.4   0.05000        1.0107
  fpr_half         4    0.0435   1.1305    3538.2   0.40200        1.0633
  fpr_oracle       4    0.0696   1.2087    3309.3   0.00550        1.0994
  fpr_qhat         4    0.0142   1.0426    3836.5   0.01250        1.0211
  Extremum envelopes: an extremum over four correlated cells has neither the distribution nor the interval of one cell (S4bis.4).
  RTenLbSignMin      point 0.0460  bootstrap 95% [0.0330, 0.0520]  bootstrap mean 0.042653
  RTenLbSignMax      point 0.0630  bootstrap 95% [0.0510, 0.0790]  bootstrap mean 0.063880
  RTenFprQhatMin     point 0.0100  bootstrap 95% [0.0040, 0.0130]  bootstrap mean 0.008393
  RTenFprQhatMax     point 0.0150  bootstrap 95% [0.0120, 0.0240]  bootstrap mean 0.017001
PASSED [ 55%]
tests/test_R10_claims.py::test_R10_report_the_operator_null_level_and_the_exact_half_arm_law 
  R10 the level this CUSUM delivers under perfect centring (control C8)
  xi = 1.0   ref = 0.499674     64 alarms on 20000 streams -> 0.3200% [0.2507%, 0.4084%]; fair-coin exact 0.3677%; nominal 5.0%
  xi = 0.85  ref = 0.529604     72 alarms on 20000 streams -> 0.3600% [0.2860%, 0.4531%]; fair-coin exact 0.3677%; nominal 5.0%
  xi = 0.65  ref = 0.564281     72 alarms on 20000 streams -> 0.3600% [0.2860%, 0.4531%]; fair-coin exact 0.3677%; nominal 5.0%
  xi = 0.5   ref = 0.582348     68 alarms on 20000 streams -> 0.3400% [0.2683%, 0.4308%]; fair-coin exact 0.3677%; nominal 5.0%
  The exact Bernoulli(q) law of the fixed-1/2 arm (control C7), both operators:
  xi=0.5 strict  q = 0.582348  lambda = 75 units  exact 96.6487%  observed 96.6000%
  xi=0.5 weak    q = 0.582348  lambda = 74 units  exact 97.0993%  observed 96.6000%
  xi=0.65 strict q = 0.564281  lambda = 75 units  exact 59.7223%  observed 59.6000%
  xi=0.65 weak   q = 0.564281  lambda = 74 units  exact 62.0532%  observed 59.6000%
  xi=0.85 strict q = 0.529604  lambda = 75 units  exact 3.8869%  observed 4.1000%
  xi=0.85 weak   q = 0.529604  lambda = 74 units  exact 4.3572%  observed 4.1000%
  xi=1.0 strict  q = 0.499674  lambda = 75 units  exact 0.3680%  observed 0.5000%
  xi=1.0 weak    q = 0.499674  lambda = 74 units  exact 0.4337%  observed 0.5000%
  What the float comparison implements on the lattice boundary (control C7c):
  float M > lambda           realised level 0.402000 on 4000 streams, 38 disagreements with the strict operator
  exact M_units > lambda     realised level 0.392500 on 4000 streams, 0 disagreements with the strict operator
  exact M_units >= lambda    realised level 0.402000 on 4000 streams, 38 disagreements with the strict operator
  Panel B is read against both references: nominal 5.0% and the operator's own 0.3450%. The recentred arm spans 1.0-1.5%.
PASSED [ 55%]
tests/test_R10_claims.py::test_R10_report_the_ljungbox_calibration_and_its_power_bound 
  R10 Ljung-Box calibration, per cell (control C2a; only the xi = 1 row is a gate)
      xi  lb_sign rate      KS D      KS p  lb_ebin rate      KS D      KS p
     1.0        0.0500   0.02302   0.65566        0.0470   0.03745   0.11802
    0.85        0.0630   0.01852   0.87626        0.0480   0.03802   0.10818
    0.65        0.0460   0.04344   0.04459        0.0480   0.04188   0.05826
     0.5        0.0500   0.03875   0.09671        0.0570   0.03896   0.09361
  Family-wise arithmetic: gating on all 8 cells at 0.05 would trigger with probability 33.6580% under a perfectly calibrated null, which is why it is not a gate.
  Smallest p-value over the 4000 streams: raw sign 0.000377338, HT error 0.000262061.
  The HT-error arm's evidence is a NON-REJECTION; its power at n = 8000, lag 20 is bounded by docs/DEVIATIONS.md R18-ljungbox-power, and R10 opens no duplicate entry.
PASSED [ 56%]
tests/test_R11_claims.py::test_R11_cardinalities_and_arms PASSED         [ 56%]
tests/test_R11_claims.py::test_R11_gamma_grid_is_the_target_grid_and_its_floor_is_respected PASSED [ 56%]
tests/test_R11_claims.py::test_R11_gamma_range_matches_the_published_multiplier PASSED [ 56%]
tests/test_R11_claims.py::test_R11_as_submitted_arm_is_the_per_detector_mixture PASSED [ 57%]
tests/test_R11_claims.py::test_R11_putting_both_detectors_on_one_convention_moves_the_cusum PASSED [ 57%]
tests/test_R11_claims.py::test_R11_the_published_ordering_holds_on_the_arm_that_produced_it PASSED [ 57%]
tests/test_R11_claims.py::test_R11_crn_h0_arm_is_degenerate_and_the_independent_arm_is_not PASSED [ 57%]
tests/test_R11_claims.py::test_R11_kish_design_effect_of_a_degenerate_grid_is_its_width PASSED [ 58%]
tests/test_R11_claims.py::test_R11_pht_intervals_carry_the_calibration_variance_factor PASSED [ 58%]
tests/test_R11_claims.py::test_R11_every_interval_bound_is_clamped PASSED [ 58%]
tests/test_R11_claims.py::test_R11_data_loglog_slopes_reproduce_by_an_independent_fit PASSED [ 58%]
tests/test_R11_claims.py::test_R11_pht_data_slope_is_fitted_on_a_restricted_domain PASSED [ 58%]
tests/test_R11_claims.py::test_R11_low_gamma_sensitivity_arm_excludes_exactly_the_unattainable_point PASSED [ 59%]
tests/test_R11_claims.py::test_R11_bootstrap_standard_errors_are_present_and_the_ratio_is_reported PASSED [ 59%]
tests/test_R11_claims.py::test_R11_no_macro_restates_the_cusum_scaling_law PASSED [ 59%]
tests/test_R11_claims.py::test_R11_submitted_linear_fits_are_reproduced_for_traceability PASSED [ 59%]
tests/test_R11_claims.py::test_R11_peak_to_peak_spread_is_descriptive_and_arithmetically_correct PASSED [ 60%]
tests/test_R11_claims.py::test_R11_preonset_leak_is_recorded_for_every_detector_even_at_zero PASSED [ 60%]
tests/test_R11_claims.py::test_R11_onset_table_carries_a_paired_error PASSED [ 60%]
tests/test_R11_claims.py::test_R11_the_two_adwin_implementations_are_labelled PASSED [ 60%]
tests/test_R11_claims.py::test_R11_river_version_is_recorded_in_the_artefacts PASSED [ 61%]
tests/test_R11_claims.py::test_R11_macros_are_emitted_with_the_preamble_ordinal PASSED [ 61%]
tests/test_R11_claims.py::test_R11_concept_add_macros_match_their_arm PASSED [ 61%]
tests/test_R11_claims.py::test_R11_eddm_macros_come_from_the_independent_seed_arm PASSED [ 61%]
tests/test_R11_claims.py::test_R11_report_against_v87 PASSED             [ 62%]
tests/test_R12_claims.py::test_R12_every_artefact_the_plan_lists_exists PASSED [ 62%]
tests/test_R12_claims.py::test_R12_the_grids_and_stream_counts_are_the_ones_v87_specifies PASSED [ 62%]
tests/test_R12_claims.py::test_R12_the_published_concept_arm_is_the_independent_key_on_every_row PASSED [ 62%]
tests/test_R12_claims.py::test_R12_the_three_carried_primitives_are_byte_identical_to_the_witness PASSED [ 63%]
tests/test_R12_claims.py::test_R12_det_rate_concept_is_computed_and_not_a_literal PASSED [ 63%]
tests/test_R12_claims.py::test_R12_the_concept_detection_rate_is_a_full_count_and_not_a_rounded_one PASSED [ 63%]
tests/test_R12_claims.py::test_R12_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 63%]
tests/test_R12_claims.py::test_R12_the_fourth_moment_boundary_and_the_exact_penalty_are_their_own_closed_forms PASSED [ 64%]
tests/test_R12_claims.py::test_R12_the_leverage_grid_runs_to_the_edge_of_the_stationary_region PASSED [ 64%]
tests/test_R12_claims.py::test_R12_the_censoring_rule_is_the_one_stated_before_the_frame_was_read PASSED [ 64%]
tests/test_R12_claims.py::test_R12_the_baseline_false_alarm_rate_explodes_with_leverage PASSED [ 64%]
tests/test_R12_claims.py::test_R12_the_sign_pipeline_holds_a_leverage_invariant_rate PASSED [ 65%]
tests/test_R12_claims.py::test_R12_detection_decays_monotonically_on_the_uncensored_domain PASSED [ 65%]
tests/test_R12_claims.py::test_R12_the_collapse_threshold_is_the_one_L353_prints PASSED [ 65%]
tests/test_R12_claims.py::test_R12_the_concept_delay_stays_flat_at_the_printed_range PASSED [ 65%]
tests/test_R12_claims.py::test_R12_the_concept_false_alarm_envelope_has_moved_at_both_ends PASSED [ 66%]
tests/test_R12_claims.py::test_R12_the_censored_delay_minimum_has_moved_but_stays_in_its_rounding_bracket PASSED [ 66%]
tests/test_R12_claims.py::test_R12_the_detection_rate_at_nu_ten_is_a_count_whose_printed_rounding_moved PASSED [ 66%]
tests/test_R12_claims.py::test_R12_the_crn_concept_arm_is_one_number_repeated_fifteen_times PASSED [ 66%]
tests/test_R12_claims.py::test_R12_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 66%]
tests/test_R12_claims.py::test_R12_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 67%]
tests/test_R12_claims.py::test_R12_every_produced_text_file_ends_in_a_newline PASSED [ 67%]
tests/test_R12_claims.py::test_R12_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 67%]
tests/test_R12_claims.py::test_R12_the_produced_sources_carry_no_banned_construct PASSED [ 67%]
tests/test_R12_claims.py::test_R12_report_the_campaign_against_its_witness PASSED [ 68%]
tests/test_R12_claims.py::test_R12_report_the_control_layer PASSED       [ 68%]
tests/test_R13_claims.py::test_R13_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 68%]
tests/test_R13_claims.py::test_R13_the_detector_labels_carry_the_families_the_manuscript_fixes PASSED [ 68%]
tests/test_R13_claims.py::test_R13_the_published_delay_and_false_alarm_probability_come_from_one_row PASSED [ 69%]
tests/test_R13_claims.py::test_R13_the_two_covid_detection_delays_v87_prints_reproduce PASSED [ 69%]
tests/test_R13_claims.py::test_R13_the_jensen_ratio_v87_prints_reproduces_and_is_specific_to_one_oracle PASSED [ 69%]
tests/test_R13_claims.py::test_R13_the_phase_false_alarm_probability_of_L331_does_not_reproduce_at_its_printed_precision PASSED [ 69%]
tests/test_R13_claims.py::test_R13_the_census_verdicts_of_L331_reproduce_at_the_matched_operating_point PASSED [ 70%]
tests/test_R13_claims.py::test_R13_the_2011_correction_alarms_at_dead_bands_the_caption_does_not_name PASSED [ 70%]
tests/test_R13_claims.py::test_R13_the_D2_increment_is_the_gaussian_log_likelihood_ratio PASSED [ 70%]
tests/test_R13_claims.py::test_R13_the_frozen_volatility_path_recomputes_from_the_persisted_parameters PASSED [ 70%]
tests/test_R13_claims.py::test_R13_the_four_operating_points_are_the_rules_they_name PASSED [ 71%]
tests/test_R13_claims.py::test_R13_no_arl0_is_persisted_without_its_censored_fraction PASSED [ 71%]
tests/test_R13_claims.py::test_R13_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 71%]
tests/test_R13_claims.py::test_R13_the_certification_gates_are_equivalence_statements_with_a_null_law PASSED [ 71%]
tests/test_R13_claims.py::test_R13_the_census_quantities_are_r16s_canonical_arm PASSED [ 72%]
tests/test_R13_claims.py::test_R13_the_oracle_verdict_and_the_clairvoyant_column_are_their_own_definitions PASSED [ 72%]
tests/test_R13_claims.py::test_R13_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 72%]
tests/test_R13_claims.py::test_R13_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 72%]
tests/test_R13_claims.py::test_R13_every_produced_text_file_ends_in_a_newline PASSED [ 73%]
tests/test_R13_claims.py::test_R13_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 73%]
tests/test_R13_claims.py::test_R13_the_produced_sources_carry_no_banned_construct PASSED [ 73%]
tests/test_R13_claims.py::test_R13_report_the_campaign_against_its_witness PASSED [ 73%]
tests/test_R13_claims.py::test_R13_report_the_threshold_neighbourhood_of_the_published_operating_point PASSED [ 74%]
tests/test_R13_claims.py::test_R13_report_the_certification_status_of_every_oracle PASSED [ 74%]
tests/test_R14_claims.py::test_R14_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 74%]
tests/test_R14_claims.py::test_R14_the_onset_delays_reproduce_every_aggregate_of_the_race PASSED [ 74%]
tests/test_R14_claims.py::test_R14_the_bisection_tolerance_admits_one_count_at_106_onsets_and_none_at_72 PASSED [ 75%]
tests/test_R14_claims.py::test_R14_the_two_arms_realize_one_false_alarm_rate_on_every_published_source PASSED [ 75%]
tests/test_R14_claims.py::test_R14_the_iso_fpr_match_on_real_ethereum_is_lost_under_the_re_keying PASSED [ 75%]
tests/test_R14_claims.py::test_R14_no_aggregate_reads_a_cell_the_caption_draws_hollow PASSED [ 75%]
tests/test_R14_claims.py::test_R14_the_derived_reliability_rule_reproduces_the_delivered_literal PASSED [ 75%]
tests/test_R14_claims.py::test_R14_the_bitcoin_numerals_of_L345_and_the_caption_reproduce PASSED [ 76%]
tests/test_R14_claims.py::test_R14_the_ethereum_boundary_of_L345_reproduces PASSED [ 76%]
tests/test_R14_claims.py::test_R14_the_synthetic_control_numerals_of_L345_do_not_reproduce_at_their_printed_precision PASSED [ 76%]
tests/test_R14_claims.py::test_R14_the_real_bitcoin_race_is_untouched_by_the_re_keying PASSED [ 76%]
tests/test_R14_claims.py::test_R14_the_design_effect_is_computed_from_the_mechanism_and_never_below_one PASSED [ 77%]
tests/test_R14_claims.py::test_R14_every_persisted_interval_is_a_wilson_interval_inside_the_unit_square PASSED [ 77%]
tests/test_R14_claims.py::test_R14_the_qmle_fallback_counters_are_reported_even_at_zero PASSED [ 77%]
tests/test_R14_claims.py::test_R14_the_legacy_seed_arm_reproduces_every_discrete_quantity_of_the_witness PASSED [ 77%]
tests/test_R14_claims.py::test_R14_the_legacy_seed_artefacts_declare_that_they_certify_no_published_value PASSED [ 78%]
tests/test_R14_claims.py::test_R14_the_carried_primitives_are_byte_identical_to_the_files_that_own_them PASSED [ 78%]
tests/test_R14_claims.py::test_R14_no_draw_reaches_the_global_numpy_stream PASSED [ 78%]
tests/test_R14_claims.py::test_R14_every_square_root_of_a_sample_size_follows_a_design_effect PASSED [ 78%]
tests/test_R14_claims.py::test_R14_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 79%]
tests/test_R14_claims.py::test_R14_every_produced_text_file_ends_in_a_newline PASSED [ 79%]
tests/test_R14_claims.py::test_R14_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 79%]
tests/test_R14_claims.py::test_R14_the_produced_sources_carry_no_banned_construct PASSED [ 79%]
tests/test_R14_claims.py::test_R14_report_the_campaign_against_its_witness PASSED [ 80%]
tests/test_R14_claims.py::test_R14_report_the_design_effect_and_the_reliable_grids PASSED [ 80%]
tests/test_R14_claims.py::test_R14_report_the_ratio_series_of_every_source PASSED [ 80%]
tests/test_R15_claims.py::test_R15_the_panel_is_the_one_v87_describes PASSED [ 80%]
tests/test_R15_claims.py::test_R15_the_survival_chain_is_recounted_from_the_submitted_fetch_log PASSED [ 81%]
tests/test_R15_claims.py::test_R15_the_k_one_degeneracy_is_an_identity_of_the_median_split PASSED [ 81%]
tests/test_R15_claims.py::test_R15_every_persisted_interval_is_a_wilson_interval_inside_the_unit_square PASSED [ 81%]
tests/test_R15_claims.py::test_R15_the_frozen_composition_is_the_delivered_one PASSED [ 81%]
tests/test_R15_claims.py::test_R15_the_sentinel_never_enters_a_mean PASSED [ 82%]
tests/test_R15_claims.py::test_R15_the_carried_primitives_are_byte_identical_to_the_files_that_own_them PASSED [ 82%]
tests/test_R15_claims.py::test_R15_no_draw_reaches_the_global_numpy_stream PASSED [ 82%]
tests/test_R15_claims.py::test_R15_every_square_root_of_a_sample_size_follows_a_design_effect PASSED [ 82%]
tests/test_R15_claims.py::test_R15_the_design_effect_is_computed_from_the_mechanism_and_never_below_one PASSED [ 83%]
tests/test_R15_claims.py::test_R15_the_numerals_of_L376_that_reproduce_do_reproduce PASSED [ 83%]
tests/test_R15_claims.py::test_R15_the_independence_calibration_loses_its_level_and_the_bootstrap_holds_one PASSED [ 83%]
tests/test_R15_claims.py::test_R15_no_aggregate_reads_a_cell_below_the_reliability_floor PASSED [ 83%]
tests/test_R15_claims.py::test_R15_the_effective_panel_saturates_and_the_two_estimators_agree PASSED [ 83%]
tests/test_R15_claims.py::test_R15_the_scatter_correlation_of_the_figure_caption_is_negative PASSED [ 84%]
tests/test_R15_claims.py::test_R15_the_bootstrap_fpr_envelope_of_the_caption_does_not_reproduce PASSED [ 84%]
tests/test_R15_claims.py::test_R15_the_sign_correlation_drifts_under_MKL_CBWR_and_not_otherwise PASSED [ 84%]
tests/test_R15_claims.py::test_R15_the_published_grid_is_declared_by_the_updated_witness_alone PASSED [ 84%]
tests/test_R15_claims.py::test_R15_every_artefact_the_plan_lists_exists_with_its_prescribed_schema PASSED [ 85%]
tests/test_R15_claims.py::test_R15_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 85%]
tests/test_R15_claims.py::test_R15_the_witness_blas_artefacts_declare_that_they_certify_no_published_value PASSED [ 85%]
tests/test_R15_claims.py::test_R15_every_produced_text_file_ends_in_a_newline PASSED [ 85%]
tests/test_R15_claims.py::test_R15_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 86%]
tests/test_R15_claims.py::test_R15_the_produced_sources_carry_no_banned_construct PASSED [ 86%]
tests/test_R15_claims.py::test_R15_report_the_campaign_against_its_witness PASSED [ 86%]
tests/test_R15_claims.py::test_R15_report_the_design_effects_and_what_they_cost PASSED [ 86%]
tests/test_R15_claims.py::test_R15_report_the_two_readings_of_the_caption_correlation PASSED [ 87%]
tests/test_R15_claims.py::test_R15_report_the_marginal_channel_the_caption_does_not_name PASSED [ 87%]
tests/test_R16_claims.py::test_R16_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_census_carries_the_phase_count_v87_prints PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_dating_algorithm_column_names_the_algorithm_of_every_row PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_out_of_budget_counts_reproduce_the_three_v87_prints PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_step_of_one_holds_on_the_count_and_fails_on_the_set PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_boundary_convention_flips_run_in_one_direction_only PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_unconditional_floor_is_the_sharpe_ceiling_of_the_corollary PASSED [ 89%]
tests/test_R16_claims.py::test_R16_the_sign_floor_is_the_bernoulli_divergence_of_the_manuscript PASSED [ 89%]
tests/test_R16_claims.py::test_R16_every_detectability_flag_is_its_own_floor_against_its_own_duration PASSED [ 89%]
tests/test_R16_claims.py::test_R16_the_census_statistics_recompute_from_the_raw_return_series PASSED [ 89%]
tests/test_R16_claims.py::test_R16_the_phases_partition_the_return_series_of_every_ticker PASSED [ 90%]
tests/test_R16_claims.py::test_R16_no_degenerate_phase_reaches_a_detectability_flag_without_measurement PASSED [ 90%]
tests/test_R16_claims.py::test_R16_the_turning_point_return_v87_cites_falls_where_the_convention_puts_it PASSED [ 90%]
tests/test_R16_claims.py::test_R16_the_long_secular_advance_v87_prints_reproduces PASSED [ 90%]
tests/test_R16_claims.py::test_R16_the_covid_phase_v87_prints_reproduces_to_its_printed_precision PASSED [ 91%]
tests/test_R16_claims.py::test_R16_the_two_numerical_evaluations_of_the_bound_reproduce_L260 PASSED [ 91%]
tests/test_R16_claims.py::test_R16_the_floor_fraction_envelope_of_L329_does_not_reproduce_at_its_lower_end PASSED [ 91%]
tests/test_R16_claims.py::test_R16_the_published_dating_description_is_unreachable_by_strict_pagan_sossounov PASSED [ 91%]
tests/test_R16_claims.py::test_R16_the_counterfactual_arms_are_the_rules_they_claim_to_be PASSED [ 91%]
tests/test_R16_claims.py::test_R16_the_macros_price_the_counterfactuals_they_name PASSED [ 92%]
tests/test_R16_claims.py::test_R16_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 92%]
tests/test_R16_claims.py::test_R16_the_headline_macros_agree_with_the_frames_they_are_computed_from PASSED [ 92%]
tests/test_R16_claims.py::test_R16_every_produced_text_file_ends_in_a_newline PASSED [ 92%]
tests/test_R16_claims.py::test_R16_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 93%]
tests/test_R16_claims.py::test_R16_the_produced_sources_carry_no_banned_construct PASSED [ 93%]
tests/test_R16_claims.py::test_R16_report_the_census_against_its_witness PASSED [ 93%]
tests/test_R16_claims.py::test_R16_report_the_three_dating_arms PASSED   [ 93%]
tests/test_R16_claims.py::test_R16_report_the_set_behind_the_step_of_one PASSED [ 94%]
tests/test_R18_claims.py::test_R18_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_grids_have_the_cardinality_their_specification_fixes PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_amplitude_grid_is_the_one_the_design_specifies PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_lag_one_autocorrelation_column_is_twice_the_amplitude PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_non_centrality_column_closes_its_own_geometric_sum PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_analytic_power_column_is_the_non_central_chi_square_tail PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_analytic_power_is_monotone_in_both_of_its_arguments PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_deviation_column_is_the_difference_it_names PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_wilson_intervals_agree_with_the_roots_of_the_score_equation PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_size_of_the_test_covers_the_nominal_level_at_every_horizon PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_null_p_values_are_calibrated_against_the_kolmogorov_limit PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_empirical_curve_matches_the_analytic_one_inside_the_local_domain PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_detectable_amplitude_solves_its_own_analytic_equation PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_detectable_amplitude_halves_when_the_horizon_quadruples PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_non_centrality_at_eighty_percent_power_is_a_constant_of_the_test PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_application_arms_carry_the_two_grids_they_borrow PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_realised_penalty_matches_its_target_where_the_target_is_attainable PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_measured_sign_streams_sit_below_the_detectable_amplitude PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_power_at_the_measured_autocorrelation_is_the_analytic_one PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_ljung_box_rejection_of_both_arms_covers_the_nominal_level PASSED [ 99%]
tests/test_R18_claims.py::test_R18_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 99%]
tests/test_R18_claims.py::test_R18_the_headline_macros_agree_with_the_frames_they_are_computed_from PASSED [ 99%]
tests/test_R18_claims.py::test_R18_the_reported_detectable_amplitude_is_the_one_the_analytic_law_gives PASSED [ 99%]
tests/test_R18_claims.py::test_R18_report_the_bound_the_repository_can_state PASSED [100%]

======================= 412 passed in 112.99s (0:01:52) ========================
```

---

## 6. Design decisions taken outside the plan

1. **`main` is pinned, not quoted (C7).** The plan classes `worker_mod_A`, `worker_mod_B`,
   `plot_adverse_and_lattice` and `main` as ADAPTED, "source quoted in full in the log, preceded by
   the §S4.4 grep". The grep is not empty on `main`: its line 123 carries proscribed wording. §S4.2
   makes the grep a precondition of the citation, so the citation is withheld and `main` is pinned by
   SHA-256 with the reason logged. Quoting it would have made the stream's own log fail the grep the
   preamble imposes on it.
2. **The script's own §S4.4 pattern is written without its literals.** `exp_R08_adverse_lattice_a.py`
   needs the pattern at run time for decision 1. Written verbatim it would make the file fail the
   grep it implements. Every alternative therefore carries one of its own characters inside a
   single-character class, which leaves the accepted language unchanged; `tests/test_R08_claims.py`
   asserts the two patterns agree on eighteen probes, including the neutral technical uses §S4.4
   leaves licit.
3. **C2 split into C2a and C2b (recorded as the plan requires).** The prompt's three-way comparison
   at `H = 5 000` is not satisfiable because `R10_lattice_exact_law.csv` holds no cell at that
   horizon. C2a compares against R07, which has it; C2b compares the path enumeration against both
   streams on the cells they actually share. The test suite asserts R10 *still* has no `H = 5 000`
   cell, so the re-derivation cannot silently expire.
4. **`bracket_role` is persisted from the EXACT law, and the measured leg is a reported control.**
   The delivered script computed the column from its Monte-Carlo. Persisting the exact law's roles
   makes the column deterministic; requiring the same roles of the measured levels is kept, with its
   trigger probability (`1.9017 %`) computed before the streams were drawn, and it logs rather than
   exits because §S4bis forbids a gate at that rate. Both agree on this run.
5. **The two-sample `prop_test` is kept and the paired McNemar statistic is added beside it.** The
   witness's instrument prices a variance the design does not have: the two arms share the
   trajectory at every `b`. Both are persisted, the Kish design effect of the two-cell block is
   persisted with them, and the KS calibration is run on the witness's own six p-values so that the
   reported statistic is the null of the statistic the witness computed.
6. **`--fast` artefacts are not shipped.** §S4.3 requires the degraded path to be stamped, which it
   is (`R08_*_fast.csv`, `.png`, `.tex`). `run_experiment_R08.sh` does not invoke it and no `_fast`
   artefact is left in `results/`, because a file the documented command does not produce would
   misdescribe the reproduction.
7. **`data/reference/README.md` restored from `HEAD` with only the R08 rows added.** The file was
   deleted in the worktree. It is restored from `git show HEAD:data/reference/README.md` and only the
   two R08 rows and the R08 paragraph are added; the rows of other streams are left exactly as `HEAD`
   has them, including the streams whose directories exist in the worktree but not in that register.
   Reconciling those is not R08's to do.
8. **Two macros beyond the prompt's list are NOT emitted, and one prompt macro is bound to a
   reading.** The prompt's `\REightBoundaryCases` is glossed only as "compteur ULP, même à zéro"; it
   is bound to the literal reading of §2.1's item 2 — the number of module-B streams whose float `M`
   lies within `4 ulp` of its exact lattice point (`78 971`) — and the boundary-specific count
   (`1 517` streams whose exact maximum equals `λ*`) is logged and persisted beside it in
   `R08_operator_levels.csv` rather than macro-ised.

---

## 7. Findings that revise the plan's own premises

1. **The plan's conditional branch resolves to the register-bearing side, and the plan's own
   expectation of the numeral is confirmed by measurement rather than assumed.** The plan states:
   "If it is above `5 %` (which R07's artefacts lead one to expect, at `5.1021 %`) … register entry
   plus a candidate on the rule, severity assessed against §S3 with the Monte-Carlo interval and not
   a point estimate." R08 measured `5.1021 %` exactly and `5.0815 %` on its own `2 × 10⁵` streams.
   **The plan's instruction to assess severity with the Monte-Carlo interval, taken alone, would
   yield D2**: that interval includes `5 %`. The exact leg does not, and it has no interval. The
   entry is filed at **D3** with both legs stated and with the explicit note that the Monte-Carlo
   leg alone would not carry it.
2. **The three-point bound moved away from the D3 the plan flagged as live.** The plan recorded
   `0.16` points of margin in the witness and warned the redraw might cross it. It moved to `2.21`
   points, `0.79` below the bound, and the sampling envelope of the maximum — which the plan
   correctly required — reaches `3.61`, so the margin is smaller than the point value suggests.
3. **The float-vs-weak coincidence is uniform over the whole grid, not only at `λ*`.** The plan asks
   for the disagreement counts at `λ*`. They are `0` against the weak comparison at **all six** grid
   thresholds and between `970` and `2 032` against the strict one, which is a stronger statement
   than the plan anticipated and is what makes the D3 a property of the operator rather than of one
   threshold.
4. **The rejection count of the proportion tests moved from two to three.** The plan records the
   witness's two rejections and instructs that they not be presented as establishing or refuting
   "identical". Three reject in the regenerated campaign. The instruction is followed unchanged: the
   count is reported, the family-wise arithmetic is logged before it, and neither count is used as
   evidence.
5. **The KS calibration is close to its own null quantile, and so is the sign-flip null of the
   maximum.** `D = 0.5584` against a `95 %` null quantile of `0.5360` (null `p = 0.038`), and the
   observed maximum `0.0221` against a `99.9 %` null quantile of `0.0223` (null `p = 0.0011`). The
   plan treats C4 as a reported measurement, which is what these numbers require: both sit within a
   hair of their criterion and neither would support a verdict.

---

## 8. Open questions, left open

1. **Whether L241's numerals should be the Monte-Carlo estimates or the exact levels is not R08's
   to settle.** `protocol_21d_null_law_lattice.csv` supports Figure 8 panel C *and* the L241
   sentence, and `R07_v87_figure7_exactness.md` rewrites a Figure 7 caption that quotes the same
   pair. R08 files a clarification that reports the closed form beside the estimates and declares the
   merge dependency; which of the two a camera-ready should print is an editorial decision the
   repository does not take.
2. **`docs/DEVIATIONS.md` carries the R07 bias-bound entry under two identifiers.** The register row
   is `R07-bias-bound-not-a-bound` and the detailed entry heading is `R07-bias-bound-exceeded`. R08
   cites the register row, because that is the identifier the index carries. Reconciling the two is
   R07's, and it is left open here rather than fixed in another stream's entry.
3. **Whether `4 ulp` is the right budget for the boundary counter is not established.** The number
   comes from the R08 prompt's §2.1 and from the L241 footnote's "a few ulps", not from a derivation.
   At `4 ulp`, `78 971` of `200 000` streams qualify; the counter is a REPORTING quantity, nothing
   exits on it, and the decomposition (above / below / exactly on) is persisted so that a different
   budget can be applied to the same data without re-running anything.
4. **The witness PNG is not compared byte-for-byte and no digest of it exists in either delivered
   log.** The comparison is justified by reading `plot_adverse_and_lattice`, whose source is quoted
   in full in the `_a` log. Whether that is sufficient for a figure is the question preamble §S6
   already leaves open for the repository as a whole.
5. **The two arms are close and this campaign is near the resolution at which it could say they are
   not identical.** Three of six proportion tests reject, the KS null `p` is `0.038` and the
   sign-flip null `p` of the maximum is `0.0011` against a `0.001` criterion. A larger campaign would
   settle whether the residual difference is a real asymmetry of the two mis-centrings or a property
   of the Ljung–Box test's finite-sample behaviour at these rejection rates. R08 does not run it: the
   trajectory count is v87's own specification and §S4's perimeter filter forbids the variant.
