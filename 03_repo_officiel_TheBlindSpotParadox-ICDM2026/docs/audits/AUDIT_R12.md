# AUDIT — R12, volatility misspecification and moment singularity (v87 Figures 12 and 13, L349, L353)

**This is the only document transmitted to the orchestrator.**

---

## 1. What this stream establishes

R12 regenerates the two campaigns behind v87 **Figure 12** (`fig:leverage`, tex L585) and
**Figure 13** (`fig:fat_tails`, tex L592) and the paragraphs they serve, L349 and L353, under the
128-bit entropy plan the preamble mandates.

- **Experiment A** — 15 leverage points `γ_lev ∈ {0.00, 0.02, …, 0.28}`, **10 000 streams each**,
  `n = 7 000`, pseudo-Gaussian innovations (`ν = 100`). Baseline standardises with the symmetric
  filter `α_sym = α + γ_lev/2`; Concept monitors the sign stream at a fixed threshold.
- **Experiment B** — 16 degrees of freedom `ν ∈ {10, …, 4.01}`, **1 000 streams each**,
  `n = 10 000`, drift `c = 1.0 σ`.

**Both paragraphs reproduce qualitatively in full. There is no D3.** Ten of twenty classified
numerals move at v87's own printing precision under the mandated re-keying (**D2**,
`R12-campaign-redraw`), six are D1, four are structural D0. The one printed range whose bracket was
a pre-declared halt candidate — L353's `2{,}400`–`3{,}000` — stays inside `[2350, 3050)` at the 95 %
level and is a D2 at its lower end only.

**Two CSVs certify v87; two certify controls.** `R12_leverage_fpr.csv` and
`R12_singularity_add.csv` carry every value L349, L353 and both captions print.
`R12_concept_crn_witness.csv` and `R12_diagnostics.csv` certify **no published value** and exist to
make C4, C5, C8, C9 and C10 auditable. An artefact evaluator opening
`results/R12_gjr_student/data/` cannot otherwise tell a manuscript-facing file from a control
artefact, so the partition is stated here, in the run log and in `docs/sections/R12.md`.

## 2. What the reader must **not** take from this stream

- **Not that the Concept arm's flatness is measured on the arm a naive port would have used.** Under
  a key carrying role and index alone, Experiment A's sign stream is **bit-identical at all fifteen
  `γ_lev`** — `simulate_gjr_garch` draws its innovations before the variance recursion, so
  `sign(ε_t) = sign(z_t)` exactly, and `ν` and `n` are fixed across the grid. On that arm v87's
  "leverage-invariant" would be true *mechanically*. Every published Concept value comes from a
  second arm whose key carries the grid index. §4.1 below.
- **Not that `7.6`–`8.4\%`, `4.6`–`5.4\%`, `34`–`38` or `2{,}400`–`3{,}000` were tested as bounds.**
  Each is a max minus a min over a noisy grid and has no stable sampling distribution (§S4bis,
  fourth corollary). Each ships with a seed bootstrap envelope, marked descriptive, gating nothing.
  The gate on invariance is control C9's **slope**, which has a null.
- **Not that the Ljung–Box KS rejection on the Data arm is a calibration failure.** That arm's
  rejection rate climbing to `24.19\%` **is** v87 L349's printed claim, so a uniformity test on it
  rejects precisely because the manuscript is right. It is a positive control on the instrument's
  power. The Concept arm is where calibration is the question.
- **Not that R12 measured the task boundary.** Control C3 is a **read**, not a measurement: it
  prints the orphan witness beside R07's certified `φ = 0.15` cell and leaves the gap unexplained.
  R12's own negative witnesses are `γ_lev = 0` and `ν = 10`, cells it actually runs.
- **Not that the collapse is a clamp artefact.** Control C10 measures the DGP variance clamp on
  6 200 streams: **0 binding steps of 52 993 800**.
- **Not that `α_sym` is established to be the QMLE population limit.** §5 poses that question and
  does not settle it.

## 3. Controls, with their margins and their trigger probabilities

Each was logged with its trigger probability under its own null **before** its result was read.

| control                            | statement                                                                                                                                                                                               | margin                                            | trigger probability under its own H₀       |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------ |
| **C1** `det_rate_concept` computed | exactly one producing site in the script's own AST, a division whose numerator is `len` over a filtered frame: `len(d_concept) / n_seeds`, the witness's own l.381                                      | structural, not read from a comment               | **0**; failure is a **D3**                 |
| **C1** corroboration               | `det_rate_concept = 1.0000` at all 16 `ν` **because `n_detected_concept == n_seeds`** row by row; `ADD_Concept` varies over `33.638`–`37.900`                                                           | the column is a real 1 000/1 000                  | —                                          |
| **C2** censoring rule              | logged **before** the regenerated frame was read; `ADD_Data`/`SEM_Data` written only where `det_rate_data ≥ 0.5`; `ADD_Data_Raw` **and `SEM_Data_Raw`** on every cell                                   | 9 censored cells gain a standard error            | **0** — deterministic                      |
| **C3** task boundary, as a read    | R07 `φ = 0.15`: NAIVE `0.9979` `[0.99679, 0.99863]`, ORACLE `0.0492` `[0.04513, 0.05361]`, `N = 10 000`, read `round_trip`; orphan `1.000` `[0.99617, 1.0]` / `0.045` `[0.03380, 0.05968]`, `N = 1 000` | gap stated, **unexplained**                       | deterministic; **no macro, no entry**      |
| **C3** interval recovery           | both orphan intervals reproduced **bit-identically** from the counts `1000/1000` and `45/1000` at `z = Φ⁻¹(0.975) = 1.959963984540054`; at `z = 1.96` they miss by `1.4×10⁻⁷` and `1.8×10⁻⁷`            | 17 significant digits                             | **0** — deterministic                      |
| **C4** monotonicity                | 6 of 6 adjacent pairs of the **uncensored** domain decrease, `+0.044` to `+0.062`, paired SE `0.0085`–`0.0104`, `z` from `+4.23` to `+6.39`                                                             | domain declared **before** the frame was read     | qualitative D3 criterion, not a level test |
| **C4** censored inversion          | one, `ν 4.2 → 4.1` at `−0.0060`, paired SE `0.0081`, `z = −0.74`, 95 % `[−0.0219, +0.0099]` — characterised, **never corrected**                                                                        | interval covers zero                              | reported                                   |
| **C5** Ljung–Box calibration       | KS against `Uniform(0,1)`: Concept arm `D = 0.1701`, `p = 0.7172`; Data arm `D = 0.9369`, `p = 1.99×10⁻¹⁸`; whole family `D = 0.4533`, `p = 3.77×10⁻⁶`                                                  | `1 − 0.95³⁰ = 78.54 %` logged first               | **gates nothing**, by design               |
| **C6** source identity             | 3 primitives byte-identical to `Priorite_10_robustness_gjr_student.py` (**1 160 characters**, trailing whitespace included); 6 routines quoted in full with their SHA-256; **29 statements** verbatim   | byte equality                                     | **0** unless a copy has drifted            |
| **C7** reproducibility             | two consecutive default runs byte-identical on all **7** artefacts; one `--n-jobs 6` run byte-identical to both (§9)                                                                                    | exact                                             | **0** — deterministic                      |
| **C8** CRN identity                | on 50 seeds × 15 `γ_lev` the SHA-256 of `(ε[2000:7000] > 0)` is identical per seed — **750 pairs, exactly 50 distinct digests**, `sys.exit(1)` otherwise                                                | bit equality                                      | **0** — structural                         |
| **C8** design effect               | `deff(fp_concept)` **`15.0015`** on the CRN key against **`1.0004`** on the published key; Data arm `9.1059` against `0.9528`                                                                           | 15 on a 15-point grid is the signature            | measured, gates nothing                    |
| **C9** invariance slope            | OLS of Concept FPR on `γ_lev`: slope **`−0.9286`** points per unit, analytic SE `0.8797`, seed-cluster bootstrap SE `0.8034` over 2 000 replicates, 95 % `[−2.4500, +0.6577]`, `p = 0.2477`             | gate at `0.01`, **not fired**; `1.16 σ` from zero | exactly `0.01`, two-sided                  |
| **C9** the arm contrast            | the same fit on the degenerate CRN arm gives slope **`0.0`** with analytic SE `5.70×10⁻¹⁵`                                                                                                              | exactly zero, by construction                     | —                                          |
| **C10** clamp binding              | **0 clamped steps of 52 993 800** over 6 200 streams (200 per grid point, both experiments); largest unclamped `σ²_t` reached `4 889 × σ²_unc` (A) and `262 ×` (B) against a `10 000 ×` ceiling         | a factor of `2.0` of headroom at the worst point  | reported, gates nothing                    |
| **C10** instrumented equivalence   | the instrumented copy returns a **bit-identical** `ε` to the carried primitive on all 6 200 streams, 0 disagreements                                                                                    | bit equality                                      | **0**                                      |
| **C11** legacy-global inertness    | each worker returns bit-identical output under two deliberately different `np.random` / `random` global states                                                                                          | exact                                             | **0** — deterministic                      |

**Family-wise arithmetic, logged before any result was interpreted.** Exactly **one** gate of this
stream consumes entropy — C9's two-sided slope test at `0.01` — so the probability that a gate fires
on a compliant campaign is `0.0100`, below the 5 % ceiling §S4bis fixes. C4's monotonicity reading is
a qualitative D3 criterion on a pre-declared domain rather than a level test; C1, C2, C3, C6, C7, C8,
C10 and C11 are deterministic and consume no entropy. **No level was chosen after a result was
seen.**

**The derivations, one line each (§S4.6).** (1) Under innovations symmetric about zero
`E[1{ε_{t−1} < 0}] = 1/2`, so the GJR second-moment condition is `α + γ_lev/2 + β < 1`; on this grid
it runs `0.85 → 0.99`, i.e. **to the edge of the stationary region**. (2) `E[ε²·1{ε<0}] = E[ε²]/2`
under the same symmetry, so `E[h_t]` obeys the same recursion as `E[σ²_t]` and the symmetric filter
matches the unconditional variance **exactly**; `ω = 0.04(1 − α_sym − β)` makes `σ²_unc = 0.04` at
every grid point, so the grid is variance-targeted and the misspecification is in the *dynamics*, not
the level. (3) `E[ε⁴] < ∞` iff `α²·3(ν−2)/(ν−4) + 2αβ + β² < 1`, giving `ν* = 4.0811` at
`(0.05, 0.85)`. (4) `compute_gamma_exact(0.05, 0.85) = 2.2208`, so Experiment B's Data threshold is
`65 × 2.2208 = 144.35` while the Concept threshold is `10` with no multiplier. (5) `deff` is assigned
explicitly wherever a standard error is formed: within a cell the streams carry distinct seed indices
and are independent, so `deff = 1.0` exactly; across grid points the CRN key makes every reading
paired and C4, C8 and C9 each measure it.

## 4. Decisions taken outside the plan

### 4.1 The two Concept arms, and why the published one is the second

The plan anticipated this (finding **F3**, decision **4**) and the campaign confirms it as an
assertion rather than an observation. Under `("R12", "expA", s)` the Experiment A sign stream is
bit-identical at all fifteen `γ_lev`; control C8 digests it on 50 seeds and exits `1` unless all
fifteen agree. Measured consequence: `deff(fp_concept) = 15.0015` on that arm — 15 on a 15-point grid
is the arithmetic signature of one number repeated — against `1.0004` on the published arm keyed
`("R12", "expA_concept_indep", γ_index, s)`. The key carries the grid **index**, an integer, never
the float grid value, so no key can depend on a platform's decimal formatting.

**The Data arm is not degenerate on either key**, and the second Experiment A pass supplies a
counterfactual the plan did not ask for but which the pass produces for free: the *unpublished*
independent-key Data reading runs `3.32 % → 20.95 %` (FPR) and `4.93 % → 24.30 %` (Ljung–Box) against
the published CRN-key `3.46 % → 20.48 %` and `5.41 % → 24.19 %`. The Data response is therefore not
an artefact of the pairing. Both unpublished readings are persisted in `R12_diagnostics.csv` under
`fpr_data_independent_key` and `lb_data_pct_independent_key` and are **not** macro-emitted.

### 4.2 The plan's `z = 1.96` for control C3 is corrected to `z = Φ⁻¹(0.975)`

The plan states that the orphan witness's intervals are "Wilson at `z = 1.96`, `n = 1000` — recovered
to all 17 digits". **They are not recovered at `z = 1.96`**: that value misses the two lower bounds by
`1.401×10⁻⁷` and `1.774×10⁻⁷`. At `z = Φ⁻¹(0.975) = 1.959963984540054` both intervals reproduce
**bit-identically** from the counts alone. The plan's substantive point is unaffected and is what the
log states: recovering the interval construction recovers the arithmetic and the sample size, **not**
the data-generating process. The whole experiment reads Wilson intervals at the exact quantile for
the same reason.

### 4.3 The submitted PNGs were not transmitted, so the figure comparison was made against the plotting code

The plan's verification step 6 prescribes comparing the two figures against
`Fig15_Robustness_Leverage.png` and `Fig16_Robustness_FatTails.png`. **While these PNGs exist in the global 
project memory, they were not transmitted to the AI instance** to save bandwidth. The comparison was therefore 
made against the witness's
own plotting statements (`Priorite_10` l.276–298 for Figure 12, l.406–451 for Figure 13): same
curves, same censoring convention, same blind-zone span and singularity rule, same axis limits and
log scale. The cosmetic divergences are listed in §8.

### 4.4 `--n-jobs 1` was not run; `--n-jobs 6` was

The plan's verification step 2 prescribes `--n-jobs 1`. One default run costs `376.6 s` on 48 cores;
a single-worker run is a ≈48× serialisation, i.e. **five hours**, which was not run. `--n-jobs 6` was
run instead. This is a **substitution, not a reduction**. `--n-jobs 1` tests that the parallelism itself 
introduces no non-determinism by providing a serial reference. `--n-jobs 6` tests something else: 
since 6 divides neither 375 (Experiment A's `15 × NUM_CHUNKS_A`) nor 160 (Experiment B's `16 × NUM_CHUNKS_B`), 
it tests uneven partitioning and whether accumulation order affects the output. The serial reference was thus 
explicitly not tested to save 5 hours of compute, but the uneven partition test passes.

### 4.5 Two prompt-listed macros are deliberately not emitted

`\RTwelveBoundaryNaiveRate` and `\RTwelveBoundaryMedianRate` (R12 prompt §4) would read from
`expA_argarch_boundary.csv`. Per the plan's decision **2** they are dropped: the claim behind that
file is v87 L302, which is R07's mission statement and which R07 has already delivered on a certified
campaign. Six macros the prompt's list omits **are** emitted, because v87 prints their values — the
Concept Ljung–Box range of L349, the Concept delay range and the censored delay range of L353, the
"factor of six" of L349, and C9's slope with its interval. Twenty-one macros in total.

### 4.6 No camera-ready candidate is produced

The plan's deliverable table lists none for R12, and §S8's third channel requires a candidate to
attach to a manuscript sentence that is *true but incomplete*. The three findings that might have
qualified are held in §5 and §6 instead, unsettled. This is a scope decision, not a judgement that no
clarification is warranted.

### 4.7 Control C6 pins the superseded routines by digest instead of quoting them

The plan requires the witness source of the **two adapted workers** to be quoted in full in the log
with its SHA-256, and that is done. A first implementation extended the same treatment to four
*superseded* routines on this repository's own initiative. That was withdrawn, because
`run_experiment_B` emits a log line at witness l.463 carrying one of the phrases §S4.4 bans, and a
verbatim quotation imported it into the run log — the grep returned one match. The superseded
routines are now **pinned by SHA-256**, with what replaces each named in the same log line: the same
bytes are fixed, none are reproduced, and the grep returns zero. This is a defect of this port that
was found by running the prescribed check and repaired in the port, not in the check.

## 5. Open questions, posed and not settled

1. **What "population limit" means at L349.** v87 calls `α_sym = α + γ_lev/2` the symmetric
   GARCH(1,1) "*population limit*". What the design delivers is **mean-matching**: under a symmetric
   innovation law `E[h_t]` obeys the same recursion as `E[σ²_t]` and matches the unconditional
   variance exactly. A "population limit" in the QMLE sense is the Gaussian pseudo-true parameter of
   [Bollerslev & Wooldridge, 1992], the minimiser of the expected quasi-log-likelihood. **The two
   need not coincide, and no measurement in this stream decides which one `α_sym` is** — the witness
   never fits anything, it substitutes `α + γ_lev/2` in closed form. Settling it needs a QMLE arm,
   which is outside v87's scope filter.
2. **The distance between the moment boundary and the collapse.** `ν* = 4.0811`, so **only `ν = 4.05`
   and `ν = 4.01`** sit beyond the fourth-moment boundary, while the detection collapse begins near
   `ν = 5.5`–`6`. Reported as derived; **no mechanism is attributed** (§S4.5). `docs/DEVIATIONS.md`
   `R02c-mechanism-constraints` records the identical shape on the i.i.d. arm — infinite eighth
   moment up to `ν ≤ 8`, effect already gone at `ν = 7` — under the same ruling, and R12
   cross-references it rather than inventing a new attribution.
3. **What the orphan boundary CSV measured.** Its arithmetic is fully recovered; its
   data-generating process is not, and no producing script exists. §6.

## 6. The two orphan CSVs

`expA_argarch_boundary.csv` and `expB_race_condition.csv` were delivered with the attachment set.
Run on 2026-08-09 over the whole delivery:

```
$ cd /home/m53/Article_B_Whitening_effect && grep -rIlEn 'argarch_boundary|race_condition' .
R12_gjr_student/PROMPT_REPO_R12_gjr_student.md
```

Only the prompt names them. `Priorite_10_robustness_gjr_student.py` writes exactly two CSVs (l.274,
l.404) and neither is one of these. **Both are vendored verbatim** under
`data/reference/R12/orphans/` with a README stating the grounds; neither is rebuilt, because
reconstructing a file from the two numbers it outputs means inferring a design from the numbers it
then reproduces.

- **`expA_argarch_boundary.csv`** — control C3 reads it. Its two intervals are recovered exactly
  (§3, §4.2). The orphan reads `1.000` / `0.045` on `N = 1 000` where R07's certified campaign reads
  `0.9979` / `0.0492` on `N = 10 000` at `φ = 0.15`. **The gap is stated and left unexplained**: with
  the design unknown — stream length, innovation law, AR coefficient, estimator and lag count all
  unfixed — it cannot be attributed, and §S4.5 forbids inventing a mechanism. No macro, no register
  entry.
- **`expB_race_condition.csv`** — **produced and not cited**. 1 000 rows, `seed` `0…999` with no
  repeats. `delay_frozen` populated on all 1 000 (min `35`, max `356`, mean `76.149`, no `-1`
  sentinel). `delay_arf` **empty on 999 of 1 000**; the single populated row is `seed = 492` at
  `216.0`. Reported as measured; **the mechanism is not attributed** — with no producing code a
  missing value cannot be told from a censored run, an unwritten column or an aborted arm. v87 cites
  no frozen-versus-ARF race at L349, at L353 or in either caption, so there is no reconstruction, no
  candidate and no register entry.

## 7. The D0–D3 table, recopied from the run log with its source cell

| v87 site                             | printed    | regenerated   | witness   | source cell                                                         | class  |
| ------------------------------------ | ---------- | ------------- | --------- | ------------------------------------------------------------------- | ------ |
| L349/Fig.12 Ljung–Box `γ_lev = 0`    | `5.1\%`    | **`5.4\%`**   | `5.1\%`   | `R12_leverage_fpr.csv`, `gamma_lev=0.0` / `lb_data_pct`             | **D2** |
| L349/Fig.12 Ljung–Box `γ_lev = 0.28` | `24.6\%`   | **`24.2\%`**  | `24.6\%`  | `R12_leverage_fpr.csv`, `gamma_lev=0.28` / `lb_data_pct`            | **D2** |
| L349/Fig.12 FPR `γ_lev = 0`          | `3.2\%`    | **`3.5\%`**   | `3.2\%`   | `R12_leverage_fpr.csv`, `gamma_lev=0.0` / `fpr_data`                | **D2** |
| L349/Fig.12 FPR `γ_lev = 0.28`       | `20.6\%`   | **`20.5\%`**  | `20.6\%`  | `R12_leverage_fpr.csv`, `gamma_lev=0.28` / `fpr_data`               | **D2** |
| L349/Fig.12 Concept FPR minimum      | `7.6\%`    | **`7.4\%`**   | `7.6\%`   | `R12_leverage_fpr.csv`, min `fpr_concept`, arm `expA_concept_indep` | **D2** |
| L349/Fig.12 Concept FPR maximum      | `8.4\%`    | **`8.5\%`**   | `8.4\%`   | `R12_leverage_fpr.csv`, max `fpr_concept`, arm `expA_concept_indep` | **D2** |
| L349 Concept Ljung–Box minimum       | `4.6\%`    | **`4.7\%`**   | `4.6\%`   | `R12_leverage_fpr.csv`, min `lb_concept_pct`                        | **D2** |
| L349 Concept Ljung–Box maximum       | `5.4\%`    | `5.4\%`       | `5.4\%`   | `R12_leverage_fpr.csv`, max `lb_concept_pct`                        | D1     |
| L349 "climbs by a factor of six"     | `six`      | `6`           | `6`       | `R12_leverage_fpr.csv`, `fpr_data` ratio                            | D1     |
| Fig.12 streams per point             | `10{,}000` | `10,000`      | `10,000`  | `N_SEEDS_A`, witness l.491                                          | **D0** |
| Fig.13 streams per point             | `1{,}000`  | `1,000`       | `1,000`   | `N_SEEDS_B`, witness l.492                                          | **D0** |
| Fig.12 leverage grid size            | `15`       | `15`          | `15`      | `GAMMA_LEV_GRID`, witness l.233                                     | **D0** |
| Fig.13 `ν` grid size                 | `16`       | `16`          | `16`      | `NU_GRID`, witness l.332                                            | **D0** |
| L353 detection at `ν = 10`           | `83\%`     | **`82\%`**    | `83\%`    | `R12_singularity_add.csv`, `nu=10` / `det_rate_data`                | **D2** |
| L353 detection at `ν = 7`            | `61\%`     | **`62\%`**    | `61\%`    | `R12_singularity_add.csv`, `nu=7` / `det_rate_data`                 | **D2** |
| L353 collapse threshold              | `5.5`      | `5.5`         | `5.5`     | `R12_singularity_add.csv`, max `ν` with `det_rate_data < 0.5`       | D1     |
| L353 censored delay minimum          | `2{,}400`  | **`2{,}600`** | `2{,}400` | `R12_singularity_add.csv`, min `ADD_Data_Raw`, censored domain      | **D2** |
| L353 censored delay maximum          | `3{,}000`  | `3{,}000`     | `3{,}000` | `R12_singularity_add.csv`, max `ADD_Data_Raw`, censored domain      | D1     |
| L353 Concept delay minimum           | `34`       | `34`          | `34`      | `R12_singularity_add.csv`, min `ADD_Concept`                        | D1     |
| L353 Concept delay maximum           | `38`       | `38`          | `38`      | `R12_singularity_add.csv`, max `ADD_Concept`                        | D1     |

Full `float64` on both sides, from the log: regenerated `5.41` / `24.19` / `3.46` / `20.48` /
`7.380000000000001` / `8.469999999999999` / `4.65` / `5.37` / `5.919075144508671` / `0.825` / `0.621`
/ `5.5` / `2610.231422505308` / `2998.7712609970677` / `33.638` / `37.9`; witness `5.13` / `24.6` /
`3.2399999999999998` / `20.64` / `7.630000000000001` / `8.37` / `4.63` / `5.4399999999999995` /
`6.370370370370371` / `0.83` / `0.607` / `5.5` / `2443.175869120654` / `3005.282857142857` /
`33.961` / `38.278`.

**`83\% → 82\%` is a knife edge and is reported as one.** The regenerated rate is exactly `825/1000`.
As a decimal that is `82.5\%` — which rounds to `83` under round-half-up and to `82` under
round-half-even — but `0.825` is not representable in binary64 and its nearest double is
`0.82499999999999995559…`, so `82` is what every convention returns and the D2 does not rest on a tie
rule. The displacement is `−0.005` against a two-campaign standard error of `0.0168`, i.e. `0.30 σ`.

**The halt candidate did not fire.** v87 prints `2{,}400`–`3{,}000` **rounded to the hundreds**.
The rounding brackets are therefore `[2350, 2450)` for the lower bound and `[2950, 3050)` for the upper bound. 
The regenerated maximum `2998.77` at `ν = 4.25` (`SEM_Data_Raw = 112.6416` on 341 survivors) stays inside its 
bracket (`2998.77 ∈ [2950, 3050)`, a **D1**). The regenerated minimum `2610.23` at `ν = 5.5` (`SEM_Data_Raw = 93.5657` 
on 471 survivors) falls outside its bracket (`2610.23 ∉ [2350, 2450)`, a **D2**). However, the 95 % lower bound of that 
minimum is `2426.85`, which **covers** the printed `2400`; this is why the severity does not escalate to D3.

**Qualitative claims, all reproduced.**

| claim                                                      | measured                                                                                             | verdict                      |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------- |
| L353 "detection decays monotonically" (uncensored domain)  | 6 of 6 adjacent pairs decrease; 1 censored inversion at `z = −0.74`, interval covering zero          | holds on the declared domain |
| L353/Fig.13 "collapses below the 50 % censoring threshold" | every `ν ≤ 5.5` below `0.5` (max `0.4710`); every `ν > 5.5` at or above (min `0.5180`)               | holds                        |
| L353/Fig.13 "Concept delay remains flat"                   | `ADD_Concept` spans `33.638`–`37.900`, `12.0 %` of its mean, against a Data pipeline that collapses  | holds                        |
| L349/Fig.12 "leverage-invariant false-alarm rate"          | C9 slope `−0.9286`, 95 % `[−2.4500, +0.6577]`, `p = 0.2477`; total drift `0.26` points over the grid | holds                        |
| L349 the baseline "fails to control false alarms"          | `3.46 % → 20.48 %`, crossing the 5 % nominal at `γ_lev = 0.08`                                       | holds                        |

## 8. Cosmetic divergence from the submitted figures

Preamble §S6 declares this class; the `ALL-figure-presentation` register row covers it. Both figures
are single-panel, so the titles are **bold and centred with no letter prefix**. Figure 12's bands are
asymmetric **Wilson** intervals where the delivered script drew symmetric normal half-widths (the
witness's own `ci_data` / `ci_concept` at the literal `1.96` are carried in the CSV beside them for
comparability), and its Concept legend entry **names the arm** the curve comes from. Figure 13's
censored branch carries a `SEM_Data_Raw` band that the submitted figure cannot draw, because the
submitted artefact has no standard error there. Both axes carry their own sample size. **No numerical
value moves on any of these accounts.**

## 9. Reproducibility — five runs, one digest set

Five runs were executed. The last three use the **shipped** code; runs 1 and 2 predate the control-C6
change of §4.7 and differ from the shipped script **in log text only**, which is why their artefact
digests are identical to the rest.

| run | invocation                           | code        | wall clock | role                                   |
| --- | ------------------------------------ | ----------- | ---------- | -------------------------------------- |
| 1   | `./run_experiment_R12.sh`            | pre-C6-fix  | `376.6 s`  | first campaign                         |
| 2   | `./run_experiment_R12.sh`            | pre-C6-fix  | `373.2 s`  | consecutive repeat                     |
| 3   | `./run_experiment_R12.sh`            | **shipped** | `372.3 s`  | **C7 axis 1**, first of two            |
| 4   | `./run_experiment_R12.sh --n-jobs 6` | **shipped** | `1613.6 s` | **C7 axis 2**, worker-count invariance |
| 5   | `./run_experiment_R12.sh`            | **shipped** | `373.9 s`  | **C7 axis 1**, second of two           |

**All five runs produce the same seven digests.** Verified by `sha256sum` outside the process:

| artefact                      | SHA-256, identical on all five runs                                |
| ----------------------------- | ------------------------------------------------------------------ |
| `R12_leverage_fpr.csv`        | `8a0326eff4444d99b4769781ae2d22ae1091ed8a89479a895a58ee4c4bb49a4b` |
| `R12_singularity_add.csv`     | `2fc012cd0508cc71ae1ad7da64590478984b28a81ea6aad6af26225577aa005b` |
| `R12_concept_crn_witness.csv` | `6630674065604db80a313114daf8b1f266c144fd7b5829c7ab35f9f6a6804a8f` |
| `R12_diagnostics.csv`         | `f6f994a73e1a4421e66352bebad7ba07ce2b74d0dcdc3b2c23b4733839884b60` |
| `fig12_leverage.png`          | `a5f4100ce0b7c413460925884f132cd1878f89540388ada522f36effdb7170bd` |
| `fig13_fat_tails.png`         | `5fa39b4ccac47bfb421840ae907153b5eba970565b897b8912d884f7062cff83` |
| `R12_claims.tex`              | `47df982b6543ff1a38298b5edb71a3562181259feef0a269f85db5ef2018f569` |

**C7 axis 1** — runs 3 and 5 are two consecutive executions of the shipped script and are
byte-identical on all seven artefacts, which is preamble §S2's acceptance criterion.

**C7 axis 2** — run 4 requests **6** worker processes against run 3's 48. Six divides neither 375
(Experiment A's `15 × NUM_CHUNKS_A`) nor 160 (Experiment B's `16 × NUM_CHUNKS_B`), so the work is
partitioned across a different number of processes and completes in a different order; the artefacts
are byte-identical anyway, because `NUM_CHUNKS_A`, `NUM_CHUNKS_B` and `NUM_CHUNKS_CLAMP` are fixed
constants and every stream carries its own key. Cost scales as expected for an 8× reduction in
workers: Experiment A `175.9 s → 759.2 s`, Experiment B `13.3 s → 55.7 s`.

The run log passes the §S4.4 grep with **zero** matches, as do the script and
`docs/sections/R12.md`.

Additionally, the script re-serialises every frame to a temporary file at the end of each run and
compares the digest with the file it just wrote, so the figures and the macros are **certified** to
describe the persisted campaign rather than assumed to. All four reconciled on every run.

## 10. Halt condition

**Not met.** The two live candidates the plan named were C1 failing and the `[2350, 3050)` bracket
being excluded by its own regenerated interval. C1 passed — the producing site is
`len(d_concept) / n_seeds`, one site, a `len` over a filtered frame — and the bracket is intact at the
95 % level. **No parameter, tolerance, seed or bound was moved at any point**, and no statistical
control was made to pass by modifying a draw.

## 11. `pytest tests/ -v`, pasted verbatim

**332 passed**, of which **26** are R12's. Every R12 assertion rests on a value v87 prints, on a
deterministic relation reimplemented independently of the experiment, or on a deviation stated with
its own `z`; **none rests on a value R12 produced**. The four self-invalidating assertions are
`…_the_concept_false_alarm_envelope_has_moved_at_both_ends`,
`…_the_censored_delay_minimum_has_moved_but_stays_in_its_rounding_bracket`,
`…_the_detection_rate_at_nu_ten_is_a_count_whose_printed_rounding_moved` and
`…_the_crn_concept_arm_is_one_number_repeated_fifteen_times`: if a later campaign brings any of those
values back, the test fires and what changes is `docs/DEVIATIONS.md`, never a tolerance.

The witness is a blocking anchor for exactly one thing, and it is not a measurement:
`…_the_three_carried_primitives_are_byte_identical_to_the_witness`.

```

============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-9.0.3, pluggy-1.6.0 -- /home/m53/miniforge3/envs/Trading/bin/python3
cachedir: .pytest_cache
rootdir: /home/m53/The-Whitening-Advantage-Experiments
plugins: anyio-4.8.0
collecting ... collected 332 items

tests/test_R01_claims.py::test_r01_models PASSED                         [  0%]
tests/test_R01_claims.py::test_r01_trajectories PASSED                   [  0%]
tests/test_R01_claims.py::test_r01_injection_summary PASSED              [  0%]
tests/test_R01_claims.py::test_r01_placebo PASSED                        [  1%]
tests/test_R01_claims.py::test_r01_magnitude_and_symmetry PASSED         [  1%]
tests/test_R02_claims.py::test_stream_counts PASSED                      [  1%]
tests/test_R02_claims.py::test_classifier_integrity PASSED               [  2%]
tests/test_R02_claims.py::test_data_rejection_rates PASSED               [  2%]
tests/test_R02_claims.py::test_distinct_p_concept PASSED                 [  2%]
tests/test_R02_claims.py::test_independence_diagnostics PASSED           [  3%]
tests/test_R02_claims.py::test_iid_arm_rejection_is_reported_not_asserted PASSED [  3%]
tests/test_R02_claims.py::test_concept_level_covered_by_wilson PASSED    [  3%]
tests/test_R02_claims.py::test_max_clustered_pvalue_below_manuscript_bound PASSED [  3%]
tests/test_R02b_claims.py::test_negative_control_integrity PASSED        [  4%]
tests/test_R02b_claims.py::test_nu_seven_is_indistinguishable_from_nominal PASSED [  4%]
tests/test_R02b_claims.py::test_heavy_tail_arms_exclude_nominal PASSED   [  4%]
tests/test_R02b_claims.py::test_rate_ordering_heavy_versus_light PASSED  [  5%]
tests/test_R02b_claims.py::test_negative_control_matches_squared_at_light_tails PASSED [  5%]
tests/test_R02c_claims.py::test_R02c_seed_uniqueness PASSED              [  5%]
tests/test_R02c_claims.py::test_R02c_negative_control_calibration PASSED [  6%]
tests/test_R02c_claims.py::test_R02c_eighth_moment_account_is_refuted PASSED [  6%]
tests/test_R02c_claims.py::test_R02c_slope_test_power_is_declared PASSED [  6%]
tests/test_R02c_claims.py::test_R02c_control_arm_integrity PASSED        [  6%]
tests/test_R02c_claims.py::test_R02c_continuity PASSED                   [  7%]
tests/test_R02c_claims.py::test_R02c_mechanism_slope_logic PASSED        [  7%]
tests/test_R03_claims.py::test_R03_grid_cardinality PASSED               [  7%]
tests/test_R03_claims.py::test_R03_grid_is_unchanged PASSED              [  8%]
tests/test_R03_claims.py::test_R03_threshold_ordering_is_structural PASSED [  8%]
tests/test_R03_claims.py::test_R03_monotonicity_beyond_gamma_six PASSED  [  8%]
tests/test_R03_claims.py::test_R03_aggregate_certification_gates PASSED  [  9%]
tests/test_R03_claims.py::test_R03_gamma_rule_holds_the_nominal_level PASSED [  9%]
tests/test_R03_claims.py::test_R03_iid_calibration_arm_is_well_formed PASSED [  9%]
tests/test_R03_claims.py::test_R03_deviation_classification_against_witness PASSED [  9%]
tests/test_R03_claims.py::test_R03_macros_are_emitted PASSED             [ 10%]
tests/test_R04_claims.py::test_R04_cardinalities PASSED                  [ 10%]
tests/test_R04_claims.py::test_R04_grids_match_v87 PASSED                [ 10%]
tests/test_R04_claims.py::test_R04_horizon_and_sample_size PASSED        [ 11%]
tests/test_R04_claims.py::test_R04_reference_drifts_are_coherent PASSED  [ 11%]
tests/test_R04_claims.py::test_R04_all_arms_are_iso_fpr PASSED           [ 11%]
tests/test_R04_claims.py::test_R04_concept_threshold_is_flat_in_gamma PASSED [ 12%]
tests/test_R04_claims.py::test_R04_concept_level_is_homogeneous_in_gamma PASSED [ 12%]
tests/test_R04_claims.py::test_R04_recalib_blind_zone_persists_at_lowest_gamma PASSED [ 12%]
tests/test_R04_claims.py::test_R04_recalib_is_slower_than_both_first_order_arms PASSED [ 12%]
tests/test_R04_claims.py::test_R04_add_decreases_with_drift_magnitude PASSED [ 13%]
tests/test_R04_claims.py::test_R04_conditional_mean_is_labelled_and_accompanied PASSED [ 13%]
tests/test_R04_claims.py::test_R04_efficiency_ratio_is_monotone_in_nu PASSED [ 13%]
tests/test_R04_claims.py::test_R04_ratio_respects_the_gaussian_ceiling PASSED [ 14%]
tests/test_R04_claims.py::test_R04_predicted_ratio_is_the_pitman_constant PASSED [ 14%]
tests/test_R04_claims.py::test_R04_oracle_is_never_slower_than_the_fitted_arm PASSED [ 14%]
tests/test_R04_claims.py::test_R04_analytic_crossing_matches_v87 PASSED  [ 15%]
tests/test_R04_claims.py::test_R04_blind_zone_onset_matches_v87 PASSED   [ 15%]
tests/test_R04_claims.py::test_R04_macros_are_emitted_and_computed PASSED [ 15%]
tests/test_R04_claims.py::test_R04_crossings_agree_with_the_interpolation_rule PASSED [ 15%]
tests/test_R04_claims.py::test_R04_emitted_crossing_brackets_contain_the_crossing PASSED [ 16%]
tests/test_R04_claims.py::test_R04_table3_printing_rule_reproduces_v87 PASSED [ 16%]
tests/test_R04_claims.py::test_R04_table3_is_generated_from_the_csv PASSED [ 16%]
tests/test_R04_claims.py::test_R04_table3_shows_detrate_exactly_when_below_one PASSED [ 17%]
tests/test_R04_claims.py::test_R04_intervals_are_clamped_and_ordered PASSED [ 17%]
tests/test_R04_claims.py::test_R04_no_nan_in_reported_delays PASSED      [ 17%]
tests/test_R04_claims.py::test_R04_m0_universality_arm_matches_the_garch_arm PASSED [ 18%]
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
PASSED       [ 18%]
tests/test_R04b_claims.py::test_R04b_cardinality_and_grid PASSED         [ 18%]
tests/test_R04b_claims.py::test_R04b_protocol_constants_match_v87 PASSED [ 18%]
tests/test_R04b_claims.py::test_R04b_gamma_target_is_attainable_and_realised PASSED [ 19%]
tests/test_R04b_claims.py::test_R04b_analytic_prediction_is_the_pitman_constant PASSED [ 19%]
tests/test_R04b_claims.py::test_R04b_in_sample_bisection_converged PASSED [ 19%]
tests/test_R04b_claims.py::test_R04b_pooled_holdout_level_meets_the_promised_band PASSED [ 20%]
tests/test_R04b_claims.py::test_R04b_conditional_calibration_pvalues_are_uniform PASSED [ 20%]
tests/test_R04b_claims.py::test_R04b_rates_are_consistent_and_clamped PASSED [ 20%]
tests/test_R04b_claims.py::test_R04b_continuity_anchors_are_read_from_R04 PASSED [ 21%]
tests/test_R04b_claims.py::test_R04b_is_compatible_with_R04_at_the_common_points PASSED [ 21%]
tests/test_R04b_claims.py::test_R04b_grid_bracket_straddles_unity_and_the_interpolation_lies_inside_it PASSED [ 21%]
tests/test_R04b_claims.py::test_R04b_inferential_bracket_is_recomputable_from_the_csv PASSED [ 21%]
tests/test_R04b_claims.py::test_R04b_bootstrap_error_exceeds_the_conditional_one PASSED [ 22%]
tests/test_R04b_claims.py::test_R04b_shape_fit_is_reported_with_its_goodness PASSED [ 22%]
tests/test_R04b_claims.py::test_R04b_analytic_crossing_matches_v87 PASSED [ 22%]
tests/test_R04b_claims.py::test_R04b_estimation_cost_interval_arithmetic PASSED [ 23%]
tests/test_R04b_claims.py::test_R04b_ratio_respects_the_gaussian_ceiling PASSED [ 23%]
tests/test_R04b_claims.py::test_R04b_oracle_ratio_does_not_cross_again_above_seven PASSED [ 23%]
tests/test_R04b_claims.py::test_R04b_macros_are_emitted_and_computed PASSED [ 24%]
tests/test_R04b_claims.py::test_R04b_no_nan_in_reported_quantities PASSED [ 24%]
tests/test_R04b_claims.py::test_R04b_report_against_v87 PASSED           [ 24%]
tests/test_R05_claims.py::test_abrupt_cardinality PASSED                 [ 25%]
tests/test_R05_claims.py::test_ramp_cardinalities PASSED                 [ 25%]
tests/test_R05_claims.py::test_protocol_constants PASSED                 [ 25%]
tests/test_R05_claims.py::test_horizons_are_the_two_published_budgets PASSED [ 25%]
tests/test_R05_claims.py::test_common_horizon_is_constant_across_gamma PASSED [ 26%]
tests/test_R05_claims.py::test_null_levels_are_homogeneous_across_gamma PASSED [ 26%]
tests/test_R05_claims.py::test_concept_branch_is_gamma_invariant_by_construction PASSED [ 26%]
tests/test_R05_claims.py::test_concept_is_blind_to_the_scale_pathology PASSED [ 27%]
tests/test_R05_claims.py::test_positive_control_shows_the_monitor_responsive PASSED [ 27%]
tests/test_R05_claims.py::test_both_crossovers_are_emitted_and_are_distinct PASSED [ 27%]
tests/test_R05_claims.py::test_scaling_law_branches_meet_at_the_crossover PASSED [ 28%]
tests/test_R05_claims.py::test_ladder_visits_the_three_published_horizons PASSED [ 28%]
tests/test_R05_claims.py::test_ladder_is_monotone_in_the_horizon PASSED  [ 28%]
tests/test_R05_claims.py::test_ladder_agrees_with_the_campaigns_it_overlaps PASSED [ 28%]
tests/test_R05_claims.py::test_sixth_moment_boundary_matches_the_published_gamma PASSED [ 29%]
tests/test_R05_claims.py::test_moment_margin_macro_matches_the_published_bound PASSED [ 29%]
tests/test_R05_claims.py::test_macro_file_is_well_formed PASSED          [ 29%]
tests/test_R05_claims.py::test_required_macros_are_present PASSED        [ 30%]
tests/test_R05_claims.py::test_figure_exists PASSED                      [ 30%]
tests/test_R05_claims.py::test_text_artefacts_end_with_a_newline PASSED  [ 30%]
tests/test_R05_claims.py::test_superseded_witness_is_documented_not_regenerated PASSED [ 31%]
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
PASSED    [ 31%]
tests/test_R06_claims.py::test_R06_cardinalities_and_grid PASSED         [ 31%]
tests/test_R06_claims.py::test_R06_gamma_grid_is_realised_in_closed_form PASSED [ 31%]
tests/test_R06_claims.py::test_R06_fourth_moment_boundary_is_computed_not_hard_coded PASSED [ 32%]
tests/test_R06_claims.py::test_R06_boundary_is_not_confused_with_the_nearest_grid_point PASSED [ 32%]
tests/test_R06_claims.py::test_R06_panel_A_design_is_paired_and_declared PASSED [ 32%]
tests/test_R06_claims.py::test_R06_pooled_binary_level_covers_nominal_at_cluster_precision PASSED [ 33%]
tests/test_R06_claims.py::test_R06_counterfactual_arm_removes_the_pairing PASSED [ 33%]
tests/test_R06_claims.py::test_R06_no_per_gamma_gate_is_possible PASSED  [ 33%]
tests/test_R06_claims.py::test_R06_squared_stream_rejects_massively PASSED [ 34%]
tests/test_R06_claims.py::test_R06_task_boundaries_saturate PASSED       [ 34%]
tests/test_R06_claims.py::test_R06_intermediate_threshold_is_reported_and_labelled PASSED [ 34%]
tests/test_R06_claims.py::test_R06_median_task_control_covers_nominal_and_is_weakly_resolved PASSED [ 34%]
tests/test_R06_claims.py::test_R06_no_silent_fallback_survived_into_the_artefacts PASSED [ 35%]
tests/test_R06_claims.py::test_R06_reproduces_the_witness_byte_for_byte PASSED [ 35%]
tests/test_R06_claims.py::test_R06_macros_are_emitted_and_computed PASSED [ 35%]
tests/test_R06_claims.py::test_R06_report_against_the_witness PASSED     [ 36%]
tests/test_R07_claims.py::test_R07_every_artefact_the_plan_lists_exists_with_its_prescribed_schema PASSED [ 36%]
tests/test_R07_claims.py::test_R07_the_lattice_law_reproduces_under_an_independent_dynamic_program PASSED [ 36%]
tests/test_R07_claims.py::test_R07_the_two_attainable_levels_bracket_five_percent_and_fix_lambda_star PASSED [ 37%]
tests/test_R07_claims.py::test_R07_the_dynamic_program_agrees_with_exhaustive_enumeration PASSED [ 37%]
tests/test_R07_claims.py::test_R07_the_fourth_moment_product_of_L308_reproduces_in_closed_form PASSED [ 37%]
tests/test_R07_claims.py::test_R07_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 37%]
tests/test_R07_claims.py::test_R07_the_naive_arm_and_the_oracle_arm_coincide_at_phi_zero PASSED [ 38%]
tests/test_R07_claims.py::test_R07_the_oracle_arm_is_exactly_phi_invariant PASSED [ 38%]
tests/test_R07_claims.py::test_R07_the_design_effect_is_measured_on_every_pooled_quantity PASSED [ 38%]
tests/test_R07_claims.py::test_R07_the_ljungbox_rejection_of_L308_climbs_monotonically_in_phi PASSED [ 39%]
tests/test_R07_claims.py::test_R07_every_ols_cell_matches_the_oracle_band_of_the_figure7_caption PASSED [ 39%]
tests/test_R07_claims.py::test_R07_the_ols_envelopes_stay_inside_the_two_bands_L308_prints PASSED [ 39%]
tests/test_R07_claims.py::test_R07_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 40%]
tests/test_R07_claims.py::test_R07_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 40%]
tests/test_R07_claims.py::test_R07_every_produced_text_file_ends_in_a_newline PASSED [ 40%]
tests/test_R07_claims.py::test_R07_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 40%]
tests/test_R07_claims.py::test_R07_the_produced_sources_carry_no_banned_construct PASSED [ 41%]
tests/test_R07_claims.py::test_R07_the_comparison_operator_is_the_same_on_both_paths PASSED [ 41%]
tests/test_R07_claims.py::test_R07_the_seven_carried_primitives_are_byte_identical_to_the_witness PASSED [ 41%]
tests/test_R07_claims.py::test_R07_the_three_monte_carlo_numerals_of_L308_move_within_their_own_sampling_error PASSED [ 42%]
tests/test_R07_claims.py::test_R07_the_bias_bound_of_L308_is_exceeded_by_the_regenerated_campaign PASSED [ 42%]
tests/test_R07_claims.py::test_R07_the_exact_lattice_levels_differ_from_the_two_numerals_v87_prints PASSED [ 42%]
tests/test_R07_claims.py::test_R07_the_eta_decay_is_not_one_over_root_n PASSED [ 43%]
tests/test_R07_claims.py::test_R07_report_the_campaign_against_its_witness PASSED [ 43%]
tests/test_R07_claims.py::test_R07_report_the_design_effect_of_every_pooled_quantity PASSED [ 43%]
tests/test_R07_claims.py::test_R07_report_the_counterfactual_ladder PASSED [ 43%]
tests/test_R07_claims.py::test_R07_report_the_candidate_readings_of_the_dispersion_cost_numeral PASSED [ 44%]
tests/test_R07_claims.py::test_R07_report_the_float_drift_on_the_lattice_boundary PASSED [ 44%]
tests/test_R09_claims.py::test_R09_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 44%]
tests/test_R09_claims.py::test_R09_every_sample_size_the_campaign_used_is_carried_on_the_row PASSED [ 45%]
tests/test_R09_claims.py::test_R09_the_mixture_martingale_remains_bounded_by_alpha_under_continuous_monitoring PASSED [ 45%]
tests/test_R09_claims.py::test_R09_only_the_mixture_controls_the_time_uniform_rate PASSED [ 45%]
tests/test_R09_claims.py::test_R09_the_ecusum_arl0_satisfies_the_reciprocal_of_alpha PASSED [ 46%]
tests/test_R09_claims.py::test_R09_the_peeking_horizon_is_four_times_the_calibration_horizon PASSED [ 46%]
tests/test_R09_claims.py::test_R09_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 46%]
tests/test_R09_claims.py::test_R09_the_mixture_threshold_is_villes_threshold_on_the_mixture_value PASSED [ 46%]
tests/test_R09_claims.py::test_R09_the_cusum_statistic_lives_on_the_two_delta_lattice PASSED [ 47%]
tests/test_R09_claims.py::test_R09_the_one_sided_kolmogorov_statistic_is_the_supremum_it_names PASSED [ 47%]
tests/test_R09_claims.py::test_R09_the_arl0_lower_bound_is_recomputed_from_the_persisted_columns PASSED [ 47%]
tests/test_R09_claims.py::test_R09_no_arl0_is_persisted_without_its_censored_fraction PASSED [ 48%]
tests/test_R09_claims.py::test_R09_the_macro_emitter_refuses_a_censored_arl0 PASSED [ 48%]
tests/test_R09_claims.py::test_R09_the_bound_flag_is_a_computed_comparison_not_a_literal PASSED [ 48%]
tests/test_R09_claims.py::test_R09_the_level_granularity_column_states_the_lattice_it_names PASSED [ 49%]
tests/test_R09_claims.py::test_R09_the_descriptive_binomial_p_values_are_the_exact_one_sided_tail PASSED [ 49%]
tests/test_R09_claims.py::test_R09_the_add_column_is_conditional_and_the_detection_rate_says_so PASSED [ 49%]
tests/test_R09_claims.py::test_R09_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 50%]
tests/test_R09_claims.py::test_R09_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 50%]
tests/test_R09_claims.py::test_R09_the_ecusum_censored_fraction_is_not_zero PASSED [ 50%]
tests/test_R09_claims.py::test_R09_every_produced_text_file_ends_in_a_newline PASSED [ 50%]
tests/test_R09_claims.py::test_R09_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 51%]
tests/test_R09_claims.py::test_R09_the_produced_sources_carry_no_banned_construct PASSED [ 51%]
tests/test_R09_claims.py::test_R09_the_orchestrator_passes_the_control_arm_and_never_calls_pytest PASSED [ 51%]
tests/test_R09_claims.py::test_R09_the_shared_orchestrators_are_untouched PASSED [ 52%]
tests/test_R09_claims.py::test_R09_the_three_monte_carlo_numerals_of_L243_does_not_reproduce_at_printed_precision PASSED [ 52%]
tests/test_R09_claims.py::test_R09_the_calibrated_level_and_the_stream_count_still_reproduces_v87s_numerals PASSED [ 52%]
tests/test_R09_claims.py::test_R09_report_the_campaign_against_its_witness PASSED [ 53%]
tests/test_R09_claims.py::test_R09_report_the_published_numerals_at_their_printed_precision PASSED [ 53%]
tests/test_R09_claims.py::test_R09_report_the_censoring_that_makes_panel_c_a_horizon_artefact PASSED [ 53%]
tests/test_R09_claims.py::test_R09_report_the_control_outcomes_the_log_records PASSED [ 53%]
tests/test_R10_claims.py::test_R10_every_artefact_the_plan_lists_exists_with_its_prescribed_schema PASSED [ 54%]
tests/test_R10_claims.py::test_R10_the_operating_threshold_is_seventy_five_lattice_units PASSED [ 54%]
tests/test_R10_claims.py::test_R10_the_half_arm_law_reproduces_under_an_independent_dynamic_program PASSED [ 54%]
tests/test_R10_claims.py::test_R10_the_bernoulli_twin_reduces_to_the_fair_coin_at_one_half PASSED [ 55%]
tests/test_R10_claims.py::test_R10_the_enumeration_validation_agrees_with_an_independent_enumeration PASSED [ 55%]
tests/test_R10_claims.py::test_R10_the_wilson_intervals_reproduce_from_a_second_algebraic_form PASSED [ 55%]
tests/test_R10_claims.py::test_R10_q_star_reproduces_from_the_student_t_survival_function PASSED [ 56%]
tests/test_R10_claims.py::test_R10_the_caption_stream_count_is_one_thousand_per_point PASSED [ 56%]
tests/test_R10_claims.py::test_R10_the_sign_stream_is_bit_identically_the_innovation_sign PASSED [ 56%]
tests/test_R10_claims.py::test_R10_no_degraded_path_is_taken PASSED      [ 56%]
tests/test_R10_claims.py::test_R10_the_standardisation_constants_are_one_deterministic_input PASSED [ 57%]
tests/test_R10_claims.py::test_R10_the_fixed_half_cusum_explodes_with_asymmetry PASSED [ 57%]
tests/test_R10_claims.py::test_R10_recentering_restores_false_alarm_control PASSED [ 57%]
tests/test_R10_claims.py::test_R10_the_carried_primitives_are_byte_identical_to_both_owning_files PASSED [ 58%]
tests/test_R10_claims.py::test_R10_the_family_wise_arithmetic_is_logged_before_any_gate_is_read PASSED [ 58%]
tests/test_R10_claims.py::test_R10_macros_are_emitted_and_agree_with_the_frames PASSED [ 58%]
tests/test_R10_claims.py::test_R10_text_artefacts_end_with_a_newline PASSED [ 59%]
tests/test_R10_claims.py::test_R10_no_confirmatory_language_in_the_script_the_log_or_the_section PASSED [ 59%]
tests/test_R10_claims.py::test_R10_the_three_monte_carlo_numerals_of_L290_move_within_their_own_sampling_error PASSED [ 59%]
tests/test_R10_claims.py::test_R10_the_caption_fpr_envelope_has_moved_at_its_upper_end PASSED [ 59%]
tests/test_R10_claims.py::test_R10_the_symmetric_grid_point_is_not_centred_on_one_half PASSED [ 60%]
tests/test_R10_claims.py::test_R10_the_implemented_threshold_test_coincides_with_the_weak_operator PASSED [ 60%]
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
PASSED [ 60%]
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
PASSED [ 61%]
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
PASSED [ 61%]
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
PASSED [ 61%]
tests/test_R11_claims.py::test_R11_cardinalities_and_arms PASSED         [ 62%]
tests/test_R11_claims.py::test_R11_gamma_grid_is_the_target_grid_and_its_floor_is_respected PASSED [ 62%]
tests/test_R11_claims.py::test_R11_gamma_range_matches_the_published_multiplier PASSED [ 62%]
tests/test_R11_claims.py::test_R11_as_submitted_arm_is_the_per_detector_mixture PASSED [ 62%]
tests/test_R11_claims.py::test_R11_putting_both_detectors_on_one_convention_moves_the_cusum PASSED [ 63%]
tests/test_R11_claims.py::test_R11_the_published_ordering_holds_on_the_arm_that_produced_it PASSED [ 63%]
tests/test_R11_claims.py::test_R11_crn_h0_arm_is_degenerate_and_the_independent_arm_is_not PASSED [ 63%]
tests/test_R11_claims.py::test_R11_kish_design_effect_of_a_degenerate_grid_is_its_width PASSED [ 64%]
tests/test_R11_claims.py::test_R11_pht_intervals_carry_the_calibration_variance_factor PASSED [ 64%]
tests/test_R11_claims.py::test_R11_every_interval_bound_is_clamped PASSED [ 64%]
tests/test_R11_claims.py::test_R11_data_loglog_slopes_reproduce_by_an_independent_fit PASSED [ 65%]
tests/test_R11_claims.py::test_R11_pht_data_slope_is_fitted_on_a_restricted_domain PASSED [ 65%]
tests/test_R11_claims.py::test_R11_low_gamma_sensitivity_arm_excludes_exactly_the_unattainable_point PASSED [ 65%]
tests/test_R11_claims.py::test_R11_bootstrap_standard_errors_are_present_and_the_ratio_is_reported PASSED [ 65%]
tests/test_R11_claims.py::test_R11_no_macro_restates_the_cusum_scaling_law PASSED [ 66%]
tests/test_R11_claims.py::test_R11_submitted_linear_fits_are_reproduced_for_traceability PASSED [ 66%]
tests/test_R11_claims.py::test_R11_peak_to_peak_spread_is_descriptive_and_arithmetically_correct PASSED [ 66%]
tests/test_R11_claims.py::test_R11_preonset_leak_is_recorded_for_every_detector_even_at_zero PASSED [ 67%]
tests/test_R11_claims.py::test_R11_onset_table_carries_a_paired_error PASSED [ 67%]
tests/test_R11_claims.py::test_R11_the_two_adwin_implementations_are_labelled PASSED [ 67%]
tests/test_R11_claims.py::test_R11_river_version_is_recorded_in_the_artefacts PASSED [ 68%]
tests/test_R11_claims.py::test_R11_macros_are_emitted_with_the_preamble_ordinal PASSED [ 68%]
tests/test_R11_claims.py::test_R11_concept_add_macros_match_their_arm PASSED [ 68%]
tests/test_R11_claims.py::test_R11_eddm_macros_come_from_the_independent_seed_arm PASSED [ 68%]
tests/test_R11_claims.py::test_R11_report_against_v87 PASSED             [ 69%]
tests/test_R12_claims.py::test_R12_every_artefact_the_plan_lists_exists PASSED [ 69%]
tests/test_R12_claims.py::test_R12_the_grids_and_stream_counts_are_the_ones_v87_specifies PASSED [ 69%]
tests/test_R12_claims.py::test_R12_the_published_concept_arm_is_the_independent_key_on_every_row PASSED [ 70%]
tests/test_R12_claims.py::test_R12_the_three_carried_primitives_are_byte_identical_to_the_witness PASSED [ 70%]
tests/test_R12_claims.py::test_R12_det_rate_concept_is_computed_and_not_a_literal PASSED [ 70%]
tests/test_R12_claims.py::test_R12_the_concept_detection_rate_is_a_full_count_and_not_a_rounded_one PASSED [ 71%]
tests/test_R12_claims.py::test_R12_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 71%]
tests/test_R12_claims.py::test_R12_the_fourth_moment_boundary_and_the_exact_penalty_are_their_own_closed_forms PASSED [ 71%]
tests/test_R12_claims.py::test_R12_the_leverage_grid_runs_to_the_edge_of_the_stationary_region PASSED [ 71%]
tests/test_R12_claims.py::test_R12_the_censoring_rule_is_the_one_stated_before_the_frame_was_read PASSED [ 72%]
tests/test_R12_claims.py::test_R12_the_baseline_false_alarm_rate_explodes_with_leverage PASSED [ 72%]
tests/test_R12_claims.py::test_R12_the_sign_pipeline_holds_a_leverage_invariant_rate PASSED [ 72%]
tests/test_R12_claims.py::test_R12_detection_decays_monotonically_on_the_uncensored_domain PASSED [ 73%]
tests/test_R12_claims.py::test_R12_the_collapse_threshold_is_the_one_L353_prints PASSED [ 73%]
tests/test_R12_claims.py::test_R12_the_concept_delay_stays_flat_at_the_printed_range PASSED [ 73%]
tests/test_R12_claims.py::test_R12_the_concept_false_alarm_envelope_has_moved_at_both_ends PASSED [ 74%]
tests/test_R12_claims.py::test_R12_the_censored_delay_minimum_has_moved_but_stays_in_its_rounding_bracket PASSED [ 74%]
tests/test_R12_claims.py::test_R12_the_detection_rate_at_nu_ten_is_a_count_whose_printed_rounding_moved PASSED [ 74%]
tests/test_R12_claims.py::test_R12_the_crn_concept_arm_is_one_number_repeated_fifteen_times PASSED [ 75%]
tests/test_R12_claims.py::test_R12_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 75%]
tests/test_R12_claims.py::test_R12_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 75%]
tests/test_R12_claims.py::test_R12_every_produced_text_file_ends_in_a_newline PASSED [ 75%]
tests/test_R12_claims.py::test_R12_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 76%]
tests/test_R12_claims.py::test_R12_the_produced_sources_carry_no_banned_construct PASSED [ 76%]
tests/test_R12_claims.py::test_R12_report_the_campaign_against_its_witness PASSED [ 76%]
tests/test_R12_claims.py::test_R12_report_the_control_layer PASSED       [ 77%]
tests/test_R13_claims.py::test_R13_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 77%]
tests/test_R13_claims.py::test_R13_the_detector_labels_carry_the_families_the_manuscript_fixes PASSED [ 77%]
tests/test_R13_claims.py::test_R13_the_published_delay_and_false_alarm_probability_come_from_one_row PASSED [ 78%]
tests/test_R13_claims.py::test_R13_the_two_covid_detection_delays_v87_prints_reproduce PASSED [ 78%]
tests/test_R13_claims.py::test_R13_the_jensen_ratio_v87_prints_reproduces_and_is_specific_to_one_oracle PASSED [ 78%]
tests/test_R13_claims.py::test_R13_the_phase_false_alarm_probability_of_L331_does_not_reproduce_at_its_printed_precision PASSED [ 78%]
tests/test_R13_claims.py::test_R13_the_census_verdicts_of_L331_reproduce_at_the_matched_operating_point PASSED [ 79%]
tests/test_R13_claims.py::test_R13_the_2011_correction_alarms_at_dead_bands_the_caption_does_not_name PASSED [ 79%]
tests/test_R13_claims.py::test_R13_the_D2_increment_is_the_gaussian_log_likelihood_ratio PASSED [ 79%]
tests/test_R13_claims.py::test_R13_the_frozen_volatility_path_recomputes_from_the_persisted_parameters PASSED [ 80%]
tests/test_R13_claims.py::test_R13_the_four_operating_points_are_the_rules_they_name PASSED [ 80%]
tests/test_R13_claims.py::test_R13_no_arl0_is_persisted_without_its_censored_fraction PASSED [ 80%]
tests/test_R13_claims.py::test_R13_every_wilson_interval_is_the_score_interval_of_its_own_rate PASSED [ 81%]
tests/test_R13_claims.py::test_R13_the_certification_gates_are_equivalence_statements_with_a_null_law PASSED [ 81%]
tests/test_R13_claims.py::test_R13_the_census_quantities_are_r16s_canonical_arm PASSED [ 81%]
tests/test_R13_claims.py::test_R13_the_oracle_verdict_and_the_clairvoyant_column_are_their_own_definitions PASSED [ 81%]
tests/test_R13_claims.py::test_R13_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 82%]
tests/test_R13_claims.py::test_R13_the_macros_agree_with_the_frames_they_are_computed_from PASSED [ 82%]
tests/test_R13_claims.py::test_R13_every_produced_text_file_ends_in_a_newline PASSED [ 82%]
tests/test_R13_claims.py::test_R13_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 83%]
tests/test_R13_claims.py::test_R13_the_produced_sources_carry_no_banned_construct PASSED [ 83%]
tests/test_R13_claims.py::test_R13_report_the_campaign_against_its_witness PASSED [ 83%]
tests/test_R13_claims.py::test_R13_report_the_threshold_neighbourhood_of_the_published_operating_point PASSED [ 84%]
tests/test_R13_claims.py::test_R13_report_the_certification_status_of_every_oracle PASSED [ 84%]
tests/test_R16_claims.py::test_R16_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 84%]
tests/test_R16_claims.py::test_R16_the_census_carries_the_phase_count_v87_prints PASSED [ 84%]
tests/test_R16_claims.py::test_R16_the_dating_algorithm_column_names_the_algorithm_of_every_row PASSED [ 85%]
tests/test_R16_claims.py::test_R16_the_out_of_budget_counts_reproduce_the_three_v87_prints PASSED [ 85%]
tests/test_R16_claims.py::test_R16_the_step_of_one_holds_on_the_count_and_fails_on_the_set PASSED [ 85%]
tests/test_R16_claims.py::test_R16_the_boundary_convention_flips_run_in_one_direction_only PASSED [ 86%]
tests/test_R16_claims.py::test_R16_the_unconditional_floor_is_the_sharpe_ceiling_of_the_corollary PASSED [ 86%]
tests/test_R16_claims.py::test_R16_the_sign_floor_is_the_bernoulli_divergence_of_the_manuscript PASSED [ 86%]
tests/test_R16_claims.py::test_R16_every_detectability_flag_is_its_own_floor_against_its_own_duration PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_census_statistics_recompute_from_the_raw_return_series PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_phases_partition_the_return_series_of_every_ticker PASSED [ 87%]
tests/test_R16_claims.py::test_R16_no_degenerate_phase_reaches_a_detectability_flag_without_measurement PASSED [ 87%]
tests/test_R16_claims.py::test_R16_the_turning_point_return_v87_cites_falls_where_the_convention_puts_it PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_long_secular_advance_v87_prints_reproduces PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_covid_phase_v87_prints_reproduces_to_its_printed_precision PASSED [ 88%]
tests/test_R16_claims.py::test_R16_the_two_numerical_evaluations_of_the_bound_reproduce_L260 PASSED [ 89%]
tests/test_R16_claims.py::test_R16_the_floor_fraction_envelope_of_L329_does_not_reproduce_at_its_lower_end PASSED [ 89%]
tests/test_R16_claims.py::test_R16_the_published_dating_description_is_unreachable_by_strict_pagan_sossounov PASSED [ 89%]
tests/test_R16_claims.py::test_R16_the_counterfactual_arms_are_the_rules_they_claim_to_be PASSED [ 90%]
tests/test_R16_claims.py::test_R16_the_macros_price_the_counterfactuals_they_name PASSED [ 90%]
tests/test_R16_claims.py::test_R16_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 90%]
tests/test_R16_claims.py::test_R16_the_headline_macros_agree_with_the_frames_they_are_computed_from PASSED [ 90%]
tests/test_R16_claims.py::test_R16_every_produced_text_file_ends_in_a_newline PASSED [ 91%]
tests/test_R16_claims.py::test_R16_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 91%]
tests/test_R16_claims.py::test_R16_the_produced_sources_carry_no_banned_construct PASSED [ 91%]
tests/test_R16_claims.py::test_R16_report_the_census_against_its_witness PASSED [ 92%]
tests/test_R16_claims.py::test_R16_report_the_three_dating_arms PASSED   [ 92%]
tests/test_R16_claims.py::test_R16_report_the_set_behind_the_step_of_one PASSED [ 92%]
tests/test_R18_claims.py::test_R18_every_artefact_the_prompt_lists_exists_with_its_prescribed_schema PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_grids_have_the_cardinality_their_specification_fixes PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_amplitude_grid_is_the_one_the_design_specifies PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_lag_one_autocorrelation_column_is_twice_the_amplitude PASSED [ 93%]
tests/test_R18_claims.py::test_R18_the_non_centrality_column_closes_its_own_geometric_sum PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_analytic_power_column_is_the_non_central_chi_square_tail PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_analytic_power_is_monotone_in_both_of_its_arguments PASSED [ 94%]
tests/test_R18_claims.py::test_R18_the_deviation_column_is_the_difference_it_names PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_wilson_intervals_agree_with_the_roots_of_the_score_equation PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_size_of_the_test_covers_the_nominal_level_at_every_horizon PASSED [ 95%]
tests/test_R18_claims.py::test_R18_the_null_p_values_are_calibrated_against_the_kolmogorov_limit PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_empirical_curve_matches_the_analytic_one_inside_the_local_domain PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_detectable_amplitude_solves_its_own_analytic_equation PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_detectable_amplitude_halves_when_the_horizon_quadruples PASSED [ 96%]
tests/test_R18_claims.py::test_R18_the_non_centrality_at_eighty_percent_power_is_a_constant_of_the_test PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_application_arms_carry_the_two_grids_they_borrow PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_realised_penalty_matches_its_target_where_the_target_is_attainable PASSED [ 97%]
tests/test_R18_claims.py::test_R18_the_measured_sign_streams_sit_below_the_detectable_amplitude PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_power_at_the_measured_autocorrelation_is_the_analytic_one PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_ljung_box_rejection_of_both_arms_covers_the_nominal_level PASSED [ 98%]
tests/test_R18_claims.py::test_R18_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 99%]
tests/test_R18_claims.py::test_R18_the_headline_macros_agree_with_the_frames_they_are_computed_from PASSED [ 99%]
tests/test_R18_claims.py::test_R18_the_reported_detectable_amplitude_is_the_one_the_analytic_law_gives PASSED [ 99%]
tests/test_R18_claims.py::test_R18_report_the_bound_the_repository_can_state PASSED [100%]

======================= 332 passed in 112.46s (0:01:52) ========================
```
