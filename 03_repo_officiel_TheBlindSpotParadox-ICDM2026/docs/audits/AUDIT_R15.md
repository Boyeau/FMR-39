# AUDIT — R15, cross-sectional escape on a real equity panel

This is the only document transmitted to the orchestrator. It contains: what R15 establishes and
what it does not; the ten controls with their margins and their trigger probability under their own
null; the complete D0–D3 classification with the source cell for every value, including two **D2**;
the reproducibility evidence with both SHA-256 sets pasted as-is and the `pytest -v` output; the
design decisions taken outside the plan — including **one assertion that was re-specified after it
fired, and why the replacement is stronger**; the findings that revise the plan's own premises,
including one that was wrong about which of two vendored files is authoritative; and the open
questions, left open.

R15 measures v87 Figure 17 (`fig:cross_section`, caption L643) and every numeral of **L376**, the
paragraph that closes the Discussion with the only structural escape left to the univariate Sharpe
ceiling. It also discharges **L389**, which prints a public fetcher for the 97 equities as a
promise the repository did not previously keep.

---

## 1. What R15 establishes, in one paragraph

Running the delivered cross-sectional campaign on the vendored 97-equity panel — 5 154 common
trading days, ten panel sizes from `K = 1` to `K = 97`, five drift magnitudes, `H_ref = 500`,
`H_det = 750`, 20 000 calibration windows and 2 000 evaluation windows per cell — **every
qualitative claim of L376 reproduces and six of the eight printed quantities reproduce at v87's 
own printing precision**: from L376, the panel (`97 × 5154`, D0), the sign correlation 
(`0.2610` → `0.26`, D1), the saturating effective panel (`K_eff = 3.7370`, D0 against the witness), 
the budget plateau (`2.0299` → `2×`, D1), the whiteness switch point (`K = 10`, D0), and the COVID 
non-detection (`0` of `10`, D0).  **Two printed quantities from the Figure 17 caption move.** 
The bootstrap false-alarm envelope, `4.8`–`6.4%`, becomes **`4.0`–`5.9%`** under the 128-bit re-keying 
— `R15-campaign-redraw`, Class A, D2 — while the level the clause actually asserts is still held at every `K`. 
The caption's `r ≥ 0.99` is **falsified**: the coefficient between panel B's ordinate and the bootstrap 
threshold is `−0.9962` regenerated and `−0.9894` on the submitted campaign, so the printed relation holds
under neither sign convention on either campaign — `R15-scatter-sign`, Class A, D2 — while the qualitative 
content, that the scatter is almost entirely threshold variation, holds at `|r| ≈ 0.99` on both.

**No control fired.** The one live D3 risk — C7, "the pooled monitor still never flags the 2020
crash", where `lambda_boot` is redrawn by the migration and a lower threshold would detect — holds:
`delay_boot = −1` at all ten `K`.

**One environment difference was isolated to a single variable, and one planned assertion was
re-specified because of it.** `MKL_CBWR=COMPATIBLE`, set by this repository's canonical determinism
bootstrap and never set by the submitted campaign, moves `rho_sign_meas` by at most `3.2e-15` on 7
of the 9 cells where it is defined. Removing that one variable and nothing else recovers the
submitted values **bit for bit, on all four RNG-free columns, at all ten `K`**. Class B, D0, cause
identified: `R15-mkl-cbwr-rho`. §5 records what was re-specified and why.

---

## 2. Five things the reader must not take from this stream

**1. The agreement on the four RNG-free columns is guaranteed, not corroborating.** The panel
composition is frozen — carried verbatim from the delivered script, `% (2**32)` truncation included
— so `rho_sign_meas`, `K_eff_meas`, `K_eff_ana` and `ljungbox_p_Pt` carry no RNG at all and are
deterministic functions of the panel. Their reproduction is evidence of **port fidelity and of
nothing else**. It says nothing whatever about the sampling behaviour of `ρ` or `K_eff`, whose only
draw was frozen before the campaign began. The epistemic-asymmetry rule applies at full force, and
it is why control C1 asserts the *integer* composition rather than observing a float.

**2. The freeze is not licensed by §S6's *règle de partage*.** That clause covers analytic
constants of the apparatus. `assets_idx` is a uniform draw over subsets of size `K`. It is carried
because it selects *which real series enter the experiment* — the same category as R01's four ETFs,
R16's four streams and R14's 106 monthly onsets, none of which is redrawn — and on that ground
alone. Invoking the sharing clause here would licence freezing any inconvenient draw later.

**3. The panel is survivorship-biased by construction, and the direction matters.** `UNIVERSE` is a
fixed list of currently-listed US large caps applied backwards to 2005. v87 says so twice and reads
the panel as an upper-bound co-movement benchmark. The bias *inflates* cross-sectional correlation,
so `ρ̂` is an upper bound and the escape it prices is optimistic — the direction that does not
flatter the manuscript's thesis.

**4. The caption's composition attribution is untestable here.** "Point-to-point scatter reflects
threshold variations **across panel compositions**" names compositions as the source. The design
draws exactly one composition per `K`, so panel size and membership change together along the
abscissa and the two are confounded. Nothing in this stream separates them, and no
composition-resampling arm was added: v87 describes none and the scope filter is strictly v87's
content.

**5. `FPR_naive` is not wholly a correlation effect.** At `K = 1`, control C1 establishes `ρ = 0`
and `K_eff = 1` **exactly** — identities of the median split of an even sample, not estimates — so
no cross-sectional correlation exists there to be ignored. The independence threshold nonetheless
fires at `10.4%`, `2.1×` nominal. The decomposition into a marginal and a cross-sectional channel
is **not identifiable** under v87's design, and §6 says so rather than asserting a mechanism.

---

## 3. Controls, with their margins and their trigger probabilities

Every gate below is stated with its firing probability under **its own** null, never under the
witness's numbers (the lesson of `AUDIT_R14.md` §7). **No gate rests on a continuous Monte-Carlo
value.**

### C1 — the frozen composition, in three legs

**Leg 1 (the gate).** The three statements of `run_real_experiment` that define `assets_idx` are
extracted from `data/reference/R15/Priorite_25c_real_cross_sectional_escape_UPDATED.py` by `ast`,
compiled, and **executed** in a namespace holding nothing but `hashlib`, `np`, `K`, `K_max` and
`MASTER_SEED`. The integer array they produce is compared to this port's with `np.array_equal`,
dtype included. Bit-identical at all ten `K`. `sys.exit(1)` on any difference. **The frozen object
is an integer array**, so the comparison is exact in any BLAS regime — and it is the only thing that
has to be frozen, because everything downstream is a deterministic function of it given a fixed
summation order. Deterministic; **P(fire) = 0**.

**Leg 2 (source identity).** The same three statements are compared as **text**, byte for byte, so
leg 1 cannot pass on a coincidence of a rewritten derivation that happens to agree numerically:

```
cell_seed_base = int(hashlib.md5(f"real_{K}_{MASTER_SEED}".encode()).hexdigest(), 16) % (2**32)
rng_diag = np.random.default_rng(cell_seed_base)
assets_idx = rng_diag.choice(K_max, size=K, replace=False)
```

`tests/test_R15_claims.py` re-derives the composition by an **independent second `ast` pass** and
compares it to `R15_panel_composition.csv`, so a defect in the experiment's own extraction would
have to be reproduced identically in the test to escape.

**Leg 3 (the four floats, against a bound derived from the mechanism).** Each entry of
`np.corrcoef(signs)` is a BLAS inner product over `T = 5154` days and the statistic averages
`K(K−1)/2` of them, so the count of additions whose order the BLAS may permute scales as `T·K`. A
reordered double-precision summation of `N` terms differs by at most about `N·ε` in relative terms
(Higham 2002, ch. 4). The bound `T·K·ε` is stated in the source **above** the run and is not read
off any residual; exceeding it is a real finding and stops the run.

| `K` | bound `T·K·ε` | `rho_sign_meas` | as a fraction of bound | `K_eff_ana` | `K_eff_meas` | `ljungbox_p_Pt` |
| --- | ------------- | --------------- | ---------------------- | ----------- | ------------ | --------------- |
| 1   | `1.144e-12`   | `0`             | —                      | `0`         | `0`          | `0`             |
| 5   | `5.722e-12`   | `0`             | —                      | `0`         | `0`          | `0`             |
| 10  | `1.144e-11`   | `3.214e-15`     | `2.81e-04`             | `2.367e-15` | `0`          | `0`             |
| 20  | `2.289e-11`   | `1.927e-15`     | `8.42e-05`             | `1.581e-15` | `0`          | `0`             |
| 30  | `3.433e-11`   | `0`             | —                      | `0`         | `0`          | `0`             |
| 40  | `4.578e-11`   | `4.287e-16`     | `9.37e-06`             | `4.929e-16` | `0`          | `0`             |
| 50  | `5.722e-11`   | `4.378e-16`     | `7.65e-06`             | `4.770e-16` | `0`          | `0`             |
| 60  | `6.867e-11`   | `1.280e-15`     | `1.86e-05`             | `1.089e-15` | `0`          | `0`             |
| 75  | `8.583e-11`   | `6.540e-16`     | `7.62e-06`             | `5.875e-16` | `0`          | `0`             |
| 97  | `1.110e-10`   | `8.533e-16`     | `7.69e-06`             | `8.327e-16` | `0`          | `0`             |

Worst realised margin: **`2.81e-4` of the bound**. The bound is therefore roughly 3,500 times 
the observed error. While this complies with the requirement for a worst-case mechanism-derived 
limit, a bound this loose lacks the power to detect small porting defects. The compliance of 
Leg 3 only establishes that the gap is *compatible* with a summation reordering; it is the 
**`--witness-blas`** arm that provides the actual discriminatory power by showing the columns 
return to bit-for-bit equality once the instruction-set constraint is lifted. `K_eff_meas` and 
`ljungbox_p_Pt` are bit-identical at every `K` — neither dispatches to BLAS.

**The `K = 1` degeneracy, derived and asserted.** The panel carries `T = 5154` days, an even
number, so the median is the mean of the two central order statistics and subtracting it leaves
exactly `2577` strictly positive returns **provided none ties the median** — which is asserted,
`n_zero = 0`. At `K = 1`, `fraction_stream` is `(ε > 0) − ½`, i.e. `±0.5` with mean `0`, variance
`0.25`, and `K_eff = 1/(4·0.25) = 1` exactly. Both `rho_sign_meas == 0.0` and `K_eff_meas == 1.0`
are asserted as exact equalities. Deterministic; **P(fire | H0) = 0**. The test re-derives the whole
chain from the panel CSV, touching no value the experiment computed.

### C2 — the two `K_eff` estimators, measured and not gated

Max relative gap `|K_eff_meas − K_eff_ana| / K_eff_ana = 1.5205e-03` at `K = 10`. **An extremum over
a grid has no sampling distribution, so it gates nothing** (§S4bis, fourth corollary). Its envelope
is derived from the sampling error of the input, never from the observed gap:
`SE(ρ) ≈ 1/√T = 1.393e-02`, and `d log K_eff_ana / dρ = −(K−1)/(1 + (K−1)ρ)` gives a relative
displacement of `4.9e-02` at its widest (`K = 20`). The measured gap is **`0.031` of one sampling
standard error** of the quantity it is a function of.

### C3 — the standard error of `FPR_boot`, re-derived from the mechanism

**The plan's `√2` rule is not imported.** R04b established a variance doubling for
`n_cal = n_eval`; here `N_CAL = 20 000` and `N_RACE = 2 000`, so the first-order delta-method
multiplier would be `√(1 + n_r/n_c) = 1.0488`, not `1.4142`, and §S4bis's fifth corollary forbids
importing R04b's rule un-re-derived in any case. **Neither multiplier is correct**, for a reason the
plan states and this run confirms numerically: `H_ref + H_det = 1250` on `T = 5154` admits exactly
**3 905** distinct window starts, so 20 000 calibration draws enumerate the population `5.1×` over
and two windows can share up to `1249` of their `1250` days. The calibration and evaluation sets are
disjoint *in seed* and drawn from the *same* 3 905 windows. What is published:

`SE = √(deff_r · p(1−p)/n_r + deff_c · α(1−α)/n_c)`

with both design effects measured on the `t_start`-ordered exceedance indicators, over a
mechanism-fixed lag count `⌈n · (2(H_ref+H_det) − 1) / n_distinct⌉`.

| quantity                    | range over the ten `K` |
| --------------------------- | ---------------------- |
| `deff_eval` (`n = 2000`)    | `7.45` – `53.12`       |
| `n_eff_eval`                | `37.7` – `268.4`       |
| `deff_calib` (`n = 20000`)  | `65` – `505`           |
| `SE_design`                 | `0.0170` – `0.0505`    |
| `SE` from the literal `√2`  | `0.0062` – `0.0074`    |
| `SE` from the bare binomial | `0.0044` – `0.0052`    |

The design-corrected standard error is **three to ten times** the one either fixed multiplier would
give. **It gates nothing**, and the value the literal `√2` rule would have produced is reported
beside it in the log at every `K`, as the plan requires.

### C4 — whiteness, with the family-wise arithmetic logged before the result

`1 − 0.95¹⁰ = 40.1%` is logged **before** any p-value is interpreted. The publishable statistic is
the switch point `max{K : p ≥ 0.05} = 10`, which reads one boundary rather than ten tests and is
RNG-free. Whiteness holds at `K = 1, 5, 10` (`p = 0.984`, `0.195`, `0.147`) and fails from `K = 20`
(`p = 4.27e-03`) onward — v87's "temporal whiteness fails beyond `K = 10`", reproduced exactly.

**The KS substitute the plan names has no `Uniform(0,1)` null on this design.** The ten p-values
come from nested-in-distribution asset subsets of one panel over one common 5 154-day index; the
`K = 5` subset is drawn from the same 97 series as `K = 97`. They are strongly dependent, so a KS
test against `U(0,1)` tests a null that does not hold **even under perfect whiteness**. The
statistic is computed and persisted with that sentence attached and **is never a gate**.

### C5 — the plateau, announced before it is read

The provenance of the statistic was logged, with the witness value, **before** the regenerated
number was computed: the delivered script computes `budget_reduction` per `(K, c)` cell at line 311
and **aggregates nowhere**; the only selection of a magnitude in the whole file is the plotting line
378, `c_target = C_GRID[1]`, and lines 379–380 draw exactly one curve, at `c = 0.25`. The published
"plateaus near `2×` (`K ≥ 20`)" is therefore the mean of that plotted series over `K ≥ 20`. It is
**established by reading the plotting code, not selected among candidates**, and it is neither the
maximum nor the minimum over `c`.

Witness `2.008637`. Regenerated **`2.029907`**, over the seven cells `K = 20, 30, 40, 50, 60, 75, 97`
(`2.0581`, `1.9072`, `1.7650`, `2.2026`, `2.0766`, `2.1070`, `2.0927`), with a delta-method standard
error of **`0.0499`** propagated from the design-corrected SEMs of the seven panel cells and of the
shared reference arm. The reference arm is shared, so the cells are not independent and a naive sum
of variances would understate. A moving-block bootstrap envelope of each cell's `ADD` is logged
beside it.

### C6 — the reliability flag, and what it does not cover

Two of fifty cells are unreliable, both at `c = 0.10`: `K = 1` (`DetRate = 0.6405`) and `K = 5`
(`0.7380`). No macro and no published aggregate reads either; asserted structurally, **P(fire) = 0**.

**Extended, and this is a finding.** `add_reliable` describes the **panel** arm of a cell and says
nothing about the **reference** arm its `budget_reduction` divides by. At `c = 0.10` the reference
arm itself detects at `0.6115`, below the `0.90` floor, so `ADD_single = 469.04` is **censored** — a
mean over the detected subset of a cell that mostly does not detect — and all eight `c = 0.10` cells
that inherit it are nonetheless flagged reliable. Reported, not repaired. It does not touch the
published `c = 0.25` macro, whose reference arm detects at `0.9995`. The port persists
`ADD_single_DetRate` and `ADD_single_reliable` on every row so the defect is **measurable** rather
than inferred; those two columns are an addition to the delivered schema.

### C7 — the COVID sentinel, a live D3 gate

v87 L376: "The pooled monitor still never flags the 2020 crash." `−1` is a sentinel **by
construction** — `bilateral_delay` returns it iff neither one-sided CUSUM crosses — so the claim is
the assertion `delay_boot == −1` at every `K`, and the sentinel enters no mean anywhere in the file.

`lambda_boot` **is redrawn** by the entropy migration, so a lower regenerated threshold would
detect and this is not a formality. Result: `delay_boot = −1` at all ten `K`. Deterministic given
the regenerated thresholds; the run halts and reports in full if any `K` detects, reconciling
nothing.

The **naive** threshold fires at 8 of 10 `K` (`5, 20, 30, 40, 50, 60, 75, 97`), at delays from 15 to
655 days. Those are false alarms of a threshold that already runs at up to `100%` false-alarm rate
under the null, not detections. **No macro reads `delay_naive`.**

### C8 — the design effect before any pooled interval

Per race cell, on the `t_start`-ordered delays: `deff` ranges `1.00`–`49.06` at `c = 0.25`, `n_eff`
`40.8`–`2000`. On the calibration/evaluation overlap: §C3 above.

On the `K` grid, **before** the two pooled readings. `\RFifteenRhoSign` pools nine cells and the
plateau pools seven. The mechanism makes every pair dependent: all ten compositions are subsets of
**one** 97-asset panel over one common index, with mean pairwise Jaccard overlap `0.2235` (range
`0.0000`–`0.7732`) among the pooled cells, so the lag count is the full eight and not a
mechanism-derived subset. The Kish estimate over the `K`-ordered `ρ` series is `1.000000`, **clamped
from below** (the raw estimate fell under 1, which would advertise more independent readings than
nine cells hold). **Consequence, applied rather than noted:** `\RFifteenRhoSign` ships as a point
statistic with its dispersion — min `0.253588`, max `0.288102`, s.d. `0.010425` — and **no
interval**.

### C9 — `ast` source identity

Eight primitives byte-identical to the files that own them, `1 168` characters compared:
`strict_cusum`, `bilateral_delay`, `cusum_max_bilateral`, `wilson_ci` and `fraction_stream` against
`Priorite_25c_real_cross_sectional_escape_UPDATED.py`; `get_deterministic_seed`,
`seed_sequence_for` and `rng_for` against `exp_R13_oracle_ceiling_a.py`. §S4.2 forbids hoisting any
of them into `experiments/common/`: `strict_cusum`, `bilateral_delay` and `wilson_ci` all differ
between this witness and the R01/R03/R04/R11/R13/R14 copies. Deterministic; **P(fire) = 0**.

Two workers are **adapted** on exactly one line each — the internal
`rng = np.random.default_rng(seed)` becomes an injected generator — so byte identity is not
assertable and the witness source of each is quoted in full in the log, with its SHA-256:
`worker_null_window_real` `4bd74fdd…`, `worker_race_h1_real` `435269f5…`.

Nine routines are **superseded** and pinned by the SHA-256 of their witness segment without
quotation, which is §S4.2's treatment.

### C10 — determinism across `--n-jobs`

`./run_experiment_R15.sh` at 48 workers and `./run_experiment_R15.sh --n-jobs 1`: **all 16
artefacts byte-identical**, both arms, CSVs, figure and macro file. The sub-panel travels once
through a pool initialiser and never per task, `executor.map` preserves submission order
(never `as_completed`, SPECS §1.5), and workers return values only and never write to the log.
`_a --stage ingest` is excluded from the comparison because it is a network path; `--stage analyse`
alone is certified bit-for-bit, and that is the reviewer's nominal path. **P(fire) = 0**, a
determinism assertion.

---

## 4. Deviation classification against v87

### The complete D0–D3 table, with the source cell of every value

| v87 location           | printed                        | witness cell                                     | witness value         | regenerated value              | class      |
| ---------------------- | ------------------------------ | ------------------------------------------------ | --------------------- | ------------------------------ | ---------- |
| L376 + caption         | `97` equities                  | panel shape                                      | `97 × 5154`           | `97 × 5154`                    | D0         |
| L376 + caption         | `ρ̂ ≈ 0.26`                     | `protocol_25c`, `rho_sign_meas`, mean `K ≥ 5`    | `0.26100272704442673` | `0.2610027270444267`           | **D1**     |
| L376                   | `1/ρ̂ ≈ 3.8`                    | `protocol_25c`, `K_eff_meas`, `K = 97`           | `3.7370099487341837`  | `3.7370099487341837`           | D0         |
| L376 + caption **(B)** | `2×`, `K ≥ 20`                 | `protocol_25d`, `budget_reduction`, `c = 0.25`   | `2.008637287531487`   | `2.0299065255254365`           | **D1**     |
| L376                   | fails beyond `K = 10`          | `protocol_25c`, `ljungbox_p_Pt`                  | `10`                  | `10`                           | D0         |
| L376                   | `∼100%` at `K = 40`            | `protocol_25c`, `FPR_naive`, `K = 40`            | `0.9975`              | `0.9955`                       | holds      |
| caption **(A)**        | `4.8`–`6.4%`                   | `protocol_25c`, `FPR_boot` min/max               | `4.75`–`6.35%`        | **`3.95`–`5.85%`**             | **D2**     |
| caption **(B)**        | `r ≥ 0.99`                     | derived: `r(budget_reduction, λ_boot)`, `c=0.25` | `−0.9893771840917368` | **`−0.9962104605839599`**      | **D2**     |
| L376                   | never flags 2020               | `protocol_25e`, `delay_boot`                     | `0` of `10`           | `0` of `10`                    | D0         |
| L389                   | public fetcher for 97 equities | —                                                | absent                | `exp_R15_cross_sectional_a.py` | discharged |

The `D1` on `ρ̂` is the `MKL_CBWR` residual of §5 and nothing else: the two values differ in their
last digit and both print `0.26`.

### `R15-scatter-sign` — Class A, D2

No line of either witness script computes a correlation, so R15 had to define one, and the referent
was fixed **on the text**: "with bootstrap threshold" names `lambda_boot`; "scatter" names panel B's
ordinate, which the delivered plotting code fixes as `budget_reduction` at `c = C_GRID[1] = 0.25`.

**Order of operations, recorded as sequence and not offered as a defence.** Both candidate readings
were computed during planning, on the witness campaign, **before** the referent was fixed: reading 1
(`budget_reduction` against `λ_boot`) gives `−0.9894` and reading 2 (`ADD` against `λ_boot`) gives
`+0.9947`. The selection was made on the textual referent and on nothing else. Choosing after seeing
which sign matched the caption would be selection on the outcome, which §S4 bans. Both readings are
persisted at all five `c` in `R15_scatter_correlation.csv`; reading 2 carries no macro and no
register entry.

The sign is negative at every `c` — `−0.9907`, `−0.9962`, `−0.9912`, `−0.9896`, `−0.9876` — and it
is negative **by construction**: `budget_reduction` is `ADD_single / ADD_K`, so a higher threshold
lengthens `ADD_K` and shrinks the ratio. `−0.9894 ≥ 0.99` is false and so is `−0.9894 ≤ −0.99`: the
printed relation holds under neither convention **on the campaign the manuscript reports**.

`|r| ≥ 0.99` is **not** the correction: it holds on the regenerated campaign (`0.9962`) and fails on
the submitted one (`0.9894`). `|r| ≈ 0.99` is the only form both support, and it is what
`docs/camera_ready_candidates/R15_v87_scatter_sign.md` proposes. Both macros ship at four decimals,
because rounding the magnitude to two prints `1.00` and hides that it sits just above the caption's
bound while the witness sits just below.

### `R15-campaign-redraw` — Class A, D2

Five draw families migrate to 128-bit keys carrying role and integer grid index. One printed pair
moves: `4.8`–`6.4%` → `4.0`–`5.9%`. Both endpoints are **extrema over a ten-point grid** — reading
the wider as a 95% statement over ten cells triggers at `1 − 0.95¹⁰ = 40.1%` under its own null —
and their design-corrected standard errors (`0.0407` at the minimum, `0.0391` at the maximum) are
larger than the move. **The clause's actual assertion, that the bootstrap holds the nominal level,
is unaffected**: every one of the ten values sits in `[3.95%, 5.85%]` against a `5%` target while
`FPR_naive` reaches `100%` by `K = 60`.

One structural consequence is reported and carries no separate severity: the delivered reference-arm
seed string and the delivered panel-arm string at `K = 1` are the **same string** on the **same**
sub-panel, so the submitted `budget_reduction(K = 1)` is exactly `1.0` by construction rather than
by measurement. The migrated keys separate the two roles and the regenerated `K = 1` cell becomes an
honest estimate of 1 with sampling error (`0.9902`, `0.9986`, `0.9785`, `0.9965`). Same class of
finding as `R12-concept-crn-degeneracy`. No published aggregate reads `K = 1`.

### What does **not** reach the register

Three clarifications, each with a camera-ready candidate headed `NO DEVIATION`:

- **The composition attribution** (`R15_v87_scatter_attribution.md`). Confounded with `K`;
  untestable here. The caption is not false — compositions do vary.
- **The bound's referent** (`R15_v87_budget_bound_referent.md`). The caption names `K_eff` and the
  delivered figure draws `√K_eff` (line 381). The regenerated reduction exceeds `√K_eff = 1.9331` at
  **six of ten** plotted cells and exceeds `K_eff = 3.7370` at **none**, so the caption's literal
  reading holds and the figure's own reference line does not bound the curve. Also recorded there:
  `K_eff ≈ 3.8` is `1/ρ̂ = 3.8314`, whereas the measured `K_eff` at `K = 97` is `3.7370`; the gap is
  the finite-panel term and the caption's `≈` covers it. The regenerated figure draws **both** lines.
- **The naive baseline** (`R15_v87_naive_baseline.md`). §6 below.

---

## 5. The one assertion that was re-specified, and why the replacement is stronger

The plan for this stream required the four RNG-free columns to be asserted **exactly** equal to the
witness at all ten `K`, with `sys.exit(1)` otherwise and no tolerance. Under this repository's
canonical bootstrap that gate **fires**, on 7 of 9 `K`, at a worst relative difference of
`3.214e-15`.

**The cause was isolated by controlled variation before anything was changed.**

| environment                                                                                    | `rho_sign_meas` vs witness |
| ---------------------------------------------------------------------------------------------- | -------------------------- |
| four thread pins + `MKL_CBWR=COMPATIBLE` + `VECLIB_MAXIMUM_THREADS` (the repository bootstrap) | 7 of 9 differ              |
| four thread pins + `VECLIB_MAXIMUM_THREADS`, no `MKL_CBWR`                                     | **0 of 9 differ**          |
| four thread pins + `MKL_CBWR`, no `VECLIB_MAXIMUM_THREADS`                                     | 7 of 9 differ              |
| four thread pins only (the submitted campaign's environment)                                   | **0 of 9 differ**          |
| no pins at all (`legacy_blas=True`)                                                            | 8 of 9 differ              |

`MKL_CBWR=COMPATIBLE` is the single cause; `VECLIB_MAXIMUM_THREADS` is inert; `legacy_blas=True`
does **not** serve as a recovery mode, because it lifts the thread pins as well and the submitted
campaign ran with them.

**Why the planned gate was mis-specified.** Bit identity of a BLAS reduction is not a property of
the port; it is a property of the instruction-set constraint the environment imposes. A gate that
fires on it reports the environment and calls it a transcription error. What must be frozen is the
**integer composition**, and everything downstream is a deterministic function of it *given a fixed
summation order* — the qualifier the planned assertion omitted.

**What replaced it, and why it asserts more.**

1. **Leg 1 is now exact and BLAS-independent**: the integer composition, bit-identical at all ten
   `K`, replayed by executing the witness's own statements. It gates. It is achievable in any BLAS
   regime, and it is the assertion that actually protects the stream — if the composition moved,
   nothing here would be comparable to v87 at all.
2. **Leg 3 holds the four floats to a bound derived from the mechanism**, `T·K·ε` from the classical
   reordering bound (Higham 2002, ch. 4), stated in the source above the run and **not** read off
   the measured residual. A bound derived from the observation would assert nothing; this one is
   exceeded by nothing here at a worst margin of `2.81e-4`, and being exceeded would be a real
   finding.
3. **`--witness-blas` keeps its purpose, which is attribution and not passing.** It removes
   `MKL_CBWR` before NumPy loads, runs **unconditionally** after the default arm, and stamps every
   output. It answers one question: does the residual come from the reordering or from the port?
   It comes from the reordering — with `MKL_CBWR` gone, all four columns are bit-identical to the
   witness at all ten `K`. R01's `--legacy-blas` **refuted** its hypothesis and R14's
   `--legacy-seeds` confirmed its own; either outcome is information, which is why the arm cannot be
   conditional on a result.

**`experiments/common/fair_env.py` is not touched.** It is shared by every stream, and the removal is
three lines local to `exp_R15_cross_sectional_b.py`, executed before NumPy exists because `MKL_CBWR`
is read once when the BLAS loads.

**Registered as `R15-mkl-cbwr-rho`, Class B, D0, cause identified.** Class B is the repository's
category for "the submitted code was correct; the environment was not reproducible; the submitted
values remain exactly recoverable, and the command that recovers them is given" — all four clauses
hold. It is worth having beside `R01-variance-target`, which records the same **shape** of drift with
the cause **not** identified and is therefore left unclassified: two entries of the same shape, one
explained and one not, is what tells a reader which is which. The R01 hypothesis that BLAS pinning
was responsible was tested and refuted there, on a one-dimensional reduction that does not dispatch
to BLAS; here the counterpart hypothesis is tested and confirmed, on a statistic that does.

**Blast radius, measured.** Between the two arms, `R15_race_windows.csv` (every `t_start`, every
delay), `R15_covid_natural.csv`, `R15_panel_composition.csv` and the figure are **byte-identical**,
and every published race column — `DetRate`, `ADD`, `SEM`, `ADD_single`, `budget_reduction`,
`add_reliable`, `n_detected` — is identical to the last bit. Only the design-effect columns move
(`deff` `≤ 2.8e-14`, `n_eff` `≤ 2.6e-13`, `SEM_design` `≤ 1.1e-14`), because the Kish estimator uses
`np.dot`.

---

## 6. Design decisions taken outside the plan

**1. The delivered `Control (c)` is demoted from gate to measurement.** The delivered script
`sys.exit(1)`s when `FPR_boot` leaves `[0.03, 0.07]`. §S4bis forbids gating a campaign on a
continuous redrawn quantity: the band becomes an instrument of selection over seeds. The band is
measured and logged at every `K` — all ten sit inside it — and it halts nothing. This is a
behavioural change against the delivered script and it is declared here rather than in a footnote.

**2. `q_hat` is measured, and the decomposition it would support is declared unidentifiable.** The
naive calibration fixes `P(z > 0) = ½` by assumption. Measured on the held-out null windows against
the `H_ref` median: `0.5006 ± 0.0231` at `K = 1`, `0.5027 ± 0.0124` at `K = 97`. At `K = 1` the
cross-sectional channel is **exactly** empty and `FPR_naive = 10.4%` is entirely marginal. Beyond
`K = 1`, `q̂` and `ρ` move together along a single arm and no contrast holds one fixed; **the
marginal and cross-sectional contributions are not separable from these ten cells**, and the section
says so rather than printing a split. What is reportable is the boundary case and the increment
`FPR_naive(K) − FPR_naive(1)`, which reaches `+0.896` at `K = 97` against a `K = 1` excess of `0.054`
over nominal: the caption's mechanism is the right one and dominates by more than an order of
magnitude.

**3. Three artefacts beyond the prompt's output list**, each because a control needs it:
`R15_panel_composition.csv` (the frozen draw, inspectable rather than implicit),
`R15_race_windows.csv` (110 000 rows: `t_start` and delay per replicate, the input of every design
effect), `R15_scatter_correlation.csv` (both readings of a caption clause no witness computes).

**4. Two columns beyond the delivered race schema**: `ADD_single_DetRate` and
`ADD_single_reliable`, which make the C6 propagation defect measurable instead of inferred.

**5. `auto_adjust=True` is carried against `SPECS_REPRO_FAIR.md` §1.12.** v87 specifies "public
adjusted closes"; with `auto_adjust=True` yfinance returns the adjusted price in `Close` and emits
no `Adj Close` column at all, so the delivered call is the one that satisfies the manuscript. §S1
makes the manuscript the source of truth for experimental specification. The conflict is logged once
in `exp_R15_cross_sectional_a.py` and recorded once here; it is not resolved silently in either
direction.

**6. The `--fast` branch and the `--source synthetic` branch are not carried.** A second grid is a
second campaign and v87 publishes one; the synthetic branch produces Figure 29, which is not in v87.
The synthetic branch's constants (`α = 0.08`, `β = 0.90`, `ν = 7.0`, `H_det = 2000`, its two grids)
are logged as the specification of a branch this port does not run, so the omission is legible.

**7. The confirmatory-language scan carries word boundaries on the two proof-verbs of §S4.4.** The
repository's canonical `grep -Ein` does not, and without a boundary the shorter of the two is a
substring of the ordinary word for *where an artefact came from* — a word this stream, the register
under `data/reference/` and v87's own reproducibility appendix all use in its plain sense. Adding
`\b` narrows the pattern to what §S4.4 means and exempts no actual use of either verb. The canonical
grep was run as the plan prescribes; its **only** hits across
`experiments/R15_cross_sectional/*.py`, `logs/R15_cross_sectional/*.log` and `docs/sections/R15.md`
are that substring, and `tests/test_R15_claims.py` enforces the narrowed pattern on those files plus
this one.

---

## 7. Findings that revise the plan's own premises

**F1 was wrong about which of two vendored files is authoritative, and the correction is
`R15-grid-provenance`.** The plan states that the delivered script's full real branch declares
`K_GRID = [1, 20, 50, K_max]` — four points against the ten Figure 17 publishes — and concludes that
the published grid must be read off the artefact rather than recovered from a source line. That is
true of `Priorite_25c_real_cross_sectional_escape.py`, and the R15 prompt's §2.1 says the same,
having read the same file. It is **not** true of
`Priorite_25c_real_cross_sectional_escape_UPDATED.py`, which declares the ten-point grid at the same
line number 167 and whose log runs `K = 5` and `K = 10`. Three facts settle it, each checkable with
this repository alone: the `_UPDATED` log runs `K` values no four-point grid can produce; v87 embeds
`Fig30_RealCrossSectional_Escape_UPDATED.png`; and the two runs agree **exactly** at every shared
`K`, so they are one code path on two grids, with the coarse log timestamped `19:25` against the
ten-point `14:16` of the same day — a later, coarser re-run, not a predecessor. Both scripts and
both logs are vendored, and `exp_R15_cross_sectional_b.py` asserts both source lines and both logs
at start-up.

**The lesson is not that the prompt was careless.** Its account was internally coherent and
consistent with everything visible in the file it read. What neither party did was **enumerate the
candidate files before asserting which one was authoritative**, and a provenance claim has to name
the digest of the file it rests on. `R15-grid-provenance` is Class A, no severity — no printed value
is contradicted — and exists to record that the grid is recovered from a source line.

**F2 stands.** The survival rule is the coverage filter `cov >= MIN_COVERAGE`, not
`dropna(how="any")`, which drops dates and here drops none. The chain
`103 → 102 → 100 → 97 → 5154 dates` is recounted from the fetch log by the test suite, line by line.

**F3 stands and is now measured.** §3, control C3.

**F4 stands.** §3, control C4.

**F5 stands.** §3, control C5. The plotted `c` is `C_GRID[1] = 0.25` and the witness plateau is
`2.0086`, both confirmed by reading the delivered plotting code.

**F6 stands and is closed.** The silent drop is removed; §S4.3.

**F7 stands.** Nothing in either witness computes the caption's `r`; §4.

**F8 stands and is reported rather than settled.** `simulate_panel` and `standardized_t` have no
call site in scope. §8.

**F9 stands and is closed.** `data/reference/README.md` was deleted in the working tree by an
earlier pass; it is restored from `HEAD` with the R15 rows appended. §9.

**One premise of the plan's own entropy table is confirmed to have a consequence the table does not
state**: separating `("race_h1", k_index, c_index, i)` from `("race_h1_ref", c_index, i)` breaks a
degeneracy the delivered seed strings created at `K = 1`. §4, `R15-campaign-redraw`.

---

## 8. Open questions, left open

**1. The R15 prompt's C9 over-specifies the carried primitives.** It names `simulate_panel` and
`standardized_t` among the routines to carry byte-identically. Neither has a call site in v87's
scope: both serve the `--source synthetic` branch, which produces Figure 29, and Figure 29 is not in
v87. They are pinned by the SHA-256 of their witness segments (`1dd81b4c…`, `bbe1b63b…`) and not
quoted, which is §S4.2's treatment for a superseded routine. Whether the prompt intended a wider
scope than the manuscript, or whether the synthetic branch should be ported as a separate stream, is
**not settled here**.

**2. `add_reliable` does not propagate to the reference arm.** §3, C6. The flag describes one arm of
a ratio. Whether the delivered schema should carry a pairwise flag — as R14's C1 derived for its own
two-arm race — is a question about the delivered design, not about this port, and is left open.

**3. The composition attribution of the Figure 17 caption is confounded with `K`.** §2, item 4.
Answering it needs a composition-resampling arm that v87 does not describe.

**4. `FPR_naive` is not fully attributable to the mechanism the caption names.** §6, item 2. The
decomposition is unidentifiable under this design; the boundary case at `K = 1` is what is
established.

**5. Whether the camera-ready prints the submitted or the regenerated bootstrap envelope.**
`R15-campaign-redraw` records both; no candidate is filed, because which campaign a camera-ready
prints is a decision the register informs rather than pre-empts.

**6. Whether an executable belongs under `data/reference/`.** `AUDIT_R06.md` §8.4 poses the question
and `data/reference/R11/`, `R16/` and now `R15/` all depend on the answer being yes — all three are
read at run time by their experiments. Not settled here.

---

## 9. Reproducibility and the whole suite

### Environment

Python 3.12.9; `numpy` 1.26.4, `pandas` 2.3.2, `scipy` 1.16.2, `statsmodels` 0.14.5,
`matplotlib` 3.10.6, `yfinance` 1.2.0, `pytest` 9.0.3. `requirements/R15.txt` is transcribed from
`importlib.metadata` at run time and never written from memory. Single-threaded BLAS,
`MKL_CBWR=COMPATIBLE`, `PYTHONHASHSEED=42` exported by the orchestrator and verified in each stage.

### Cost, measured and not estimated

| stage                                   | 48 workers  | 1 worker    |
| --------------------------------------- | ----------- | ----------- |
| `_a --stage analyse` (offline, nominal) | `0.2 s`     | `0.2 s`     |
| `_b` default arm                        | `112.6 s`   | `446.7 s`   |
| `_b --witness-blas`                     | `111.1 s`   | `442.8 s`   |
| **total**                               | **`224 s`** | **`890 s`** |

The witness wall clock for the real branch was 1 min 43 s (`14:16:05` → `14:17:48`) plus the COVID
control, on a campaign that did not compute design effects, `q̂`, the correlations or the bootstrap
envelopes.

### Control C10, both digest sets pasted as-is

Run 1, `./run_experiment_R15.sh` (48 workers):

```
087636db3d8fc018895fd13702de408eb75a486fc7c31015319cb61eb79a7e7a  data/R15_covid_natural.csv
087636db3d8fc018895fd13702de408eb75a486fc7c31015319cb61eb79a7e7a  data/R15_covid_natural_witness_blas.csv
7c0483a05b471f563b71ae4376b04103212fe2d405245c928b31a08e458b85ca  data/R15_cross_sectional_race.csv
e12c876b5148526ee30e7606b171aa5f16f18081dd242bd7889a783070c10c44  data/R15_cross_sectional_race_witness_blas.csv
828d646f7204358480d90208f120214df7600294192f35d7314b18923a0e9503  data/R15_panel_composition.csv
828d646f7204358480d90208f120214df7600294192f35d7314b18923a0e9503  data/R15_panel_composition_witness_blas.csv
af306e051875a06af5f7c52c1e1f53411d8133916e30a8eaa4766f197ab7b639  data/R15_panel_diagnostics.csv
fdb311ff941eccc175cd21d803596c1193ac43d378d66d0b65357b06a6bce32a  data/R15_panel_diagnostics_witness_blas.csv
610deddba45517e0c08dd8f9560103135c8b431a980a50e7db3090840ca0057d  data/R15_race_windows.csv
610deddba45517e0c08dd8f9560103135c8b431a980a50e7db3090840ca0057d  data/R15_race_windows_witness_blas.csv
13b16bdf8cd504f79b69c437ca111823c2f6179c25f04bd8d084f70012ed9e71  data/R15_scatter_correlation.csv
1fb69fea76d2f66cfcc84adcc6d7af76345f63dd063969cd9ae18b63c462aa8c  data/R15_scatter_correlation_witness_blas.csv
60837f64636bc71c8e1e032ca178152eefbb96a5a6585bd957844cddd43693be  figures/fig17_cross_section.png
60837f64636bc71c8e1e032ca178152eefbb96a5a6585bd957844cddd43693be  figures/fig17_cross_section_witness_blas.png
043d7e80ebfcfb0964ec21a0a4202d7b28cdecfa2c4c9d972d2618fdc2933993  tables/R15_claims.tex
8b60606a8cd5294b3bb5134ef27c2f8cdc2294905a1d521fa787579ca06fe0ac  tables/R15_claims_witness_blas.tex
```

Run 2, `./run_experiment_R15.sh --n-jobs 1`: `diff` against the above is **empty**. All 16 artefacts
byte-identical.

Two facts are visible in that block and both are established, not incidental. The figure, the COVID
table, the composition table and the 110 000-row window table are **byte-identical between the two
arms**, so the campaign itself is untouched by `MKL_CBWR`; the diagnostics, race and scatter tables
differ, and §5 measures by how much and in which columns.

### The network path, run once, as L389's promise requires

`./run_experiment_R15.sh --data-source yfinance --stage ingest`, executed 2026-08-11, 102 tickers
sequentially at `SLEEP_S = 2.0`, elapsed `4 min 18 s`. **The survival chain reproduces exactly**,
seven months after the submitted fetch:

```
SURVIVAL CHAIN, every step named: 103 listed entries -> 102 unique -> 100 fetched -> 97 retained -> 5154 dates.
  ABANDONED MMC: 3 attempts exhausted, reasons ['ValueError: empty frame', ...]
  ABANDONED K:   3 attempts exhausted, reasons ['ValueError: empty frame', ...]
  LOW COVERAGE V:  4347/5154 = 84.3% < 98%.  LOW COVERAGE MA: 4803/5154 = 93.2% < 98%.
  LOW COVERAGE GM: 3673/5154 = 71.3% < 98%.
INGEST verification: the fetched panel matches the committed R15_panel_logreturns.csv on its 97
columns in order and its 5154 dates. Values bit-identical: False; worst absolute difference
2.1631744715252393e-06. The committed file is NOT overwritten.
```

Same two abandonments, same three coverage failures at the same row counts, same 97 columns **in
the same order**, same 5 154 dates. The *values* differ by at most `2.16e-06` in absolute
log-return, which is the provider restating history — and is exactly why the committed CSV is the
frozen input and why the ingest branch **verifies and refuses to overwrite** it. A campaign keyed to
a panel that silently changes under it would not be reproducible at all. This limitation is registered 
as **`R15-panel-vendor-drift`** (Class B, D0).

This also closes F6 empirically rather than by argument: had `MMC` or `K` fetched successfully
today, `K_max` would have become 98 or 99, the last element of the published `K_GRID` would have
moved, and the delivered fetcher would have absorbed that silently. This port stops with the reason
named.

### `data/reference/README.md`

The file was **deleted in the working tree** by an earlier pass — a pre-existing condition outside
R15's scope. It is restored from `HEAD` and the three R15 rows are appended, with a paragraph
explaining why `data/reference/R15/` holds two cross-sectional scripts and why the pair is the
point. The register it carries is therefore the one current at its last commit plus R15; streams
R07, R09, R10, R12, R13 and R14 hold vendored witnesses whose rows were never added to it. That gap
is **reported here and not repaired**: adding six rows for six streams this audit has not verified
would put unchecked claims into a file whose whole function is to be checkable.

### The test suite

`pytest tests/test_R15_claims.py -v`, pasted verbatim:

```
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-9.0.3, pluggy-1.6.0 -- /home/m53/miniforge3/envs/Trading/bin/python3
cachedir: .pytest_cache
rootdir: /home/m53/The-Whitening-Advantage-Experiments
plugins: anyio-4.8.0
collecting ... collected 28 items

tests/test_R15_claims.py::test_R15_the_panel_is_the_one_v87_describes PASSED [  3%]
tests/test_R15_claims.py::test_R15_the_survival_chain_is_recounted_from_the_submitted_fetch_log PASSED [  7%]
tests/test_R15_claims.py::test_R15_the_k_one_degeneracy_is_an_identity_of_the_median_split PASSED [ 10%]
tests/test_R15_claims.py::test_R15_every_persisted_interval_is_a_wilson_interval_inside_the_unit_square PASSED [ 14%]
tests/test_R15_claims.py::test_R15_the_frozen_composition_is_the_delivered_one PASSED [ 17%]
tests/test_R15_claims.py::test_R15_the_sentinel_never_enters_a_mean PASSED [ 21%]
tests/test_R15_claims.py::test_R15_the_carried_primitives_are_byte_identical_to_the_files_that_own_them PASSED [ 25%]
tests/test_R15_claims.py::test_R15_no_draw_reaches_the_global_numpy_stream PASSED [ 28%]
tests/test_R15_claims.py::test_R15_every_square_root_of_a_sample_size_follows_a_design_effect PASSED [ 32%]
tests/test_R15_claims.py::test_R15_the_design_effect_is_computed_from_the_mechanism_and_never_below_one PASSED [ 35%]
tests/test_R15_claims.py::test_R15_the_numerals_of_L376_that_reproduce_do_reproduce PASSED [ 39%]
tests/test_R15_claims.py::test_R15_the_independence_calibration_loses_its_level_and_the_bootstrap_holds_one PASSED [ 42%]
tests/test_R15_claims.py::test_R15_no_aggregate_reads_a_cell_below_the_reliability_floor PASSED [ 46%]
tests/test_R15_claims.py::test_R15_the_effective_panel_saturates_and_the_two_estimators_agree PASSED [ 50%]
tests/test_R15_claims.py::test_R15_the_scatter_correlation_of_the_figure_caption_is_negative PASSED [ 53%]
tests/test_R15_claims.py::test_R15_the_bootstrap_fpr_envelope_of_the_caption_does_not_reproduce PASSED [ 57%]
tests/test_R15_claims.py::test_R15_the_sign_correlation_drifts_under_MKL_CBWR_and_not_otherwise PASSED [ 60%]
tests/test_R15_claims.py::test_R15_the_published_grid_is_declared_by_the_updated_witness_alone PASSED [ 64%]
tests/test_R15_claims.py::test_R15_every_artefact_the_plan_lists_exists_with_its_prescribed_schema PASSED [ 67%]
tests/test_R15_claims.py::test_R15_the_macro_file_is_a_bare_newcommand_list_under_the_cardinal_prefix PASSED [ 71%]
tests/test_R15_claims.py::test_R15_the_witness_blas_artefacts_declare_that_they_certify_no_published_value PASSED [ 75%]
tests/test_R15_claims.py::test_R15_every_produced_text_file_ends_in_a_newline PASSED [ 78%]
tests/test_R15_claims.py::test_R15_the_produced_sources_and_logs_carry_no_confirmatory_language PASSED [ 82%]
tests/test_R15_claims.py::test_R15_the_produced_sources_carry_no_banned_construct PASSED [ 85%]
tests/test_R15_claims.py::test_R15_report_the_campaign_against_its_witness PASSED [ 89%]
tests/test_R15_claims.py::test_R15_report_the_design_effects_and_what_they_cost PASSED [ 92%]
tests/test_R15_claims.py::test_R15_report_the_two_readings_of_the_caption_correlation PASSED [ 96%]
tests/test_R15_claims.py::test_R15_report_the_marginal_channel_the_caption_does_not_name PASSED [100%]

============================== 28 passed in 0.87s ==============================
```

Blocking assertions rest on values v87 **prints**, at v87's printing precision, or on relations
reimplemented independently of the experiment: the `K = 1` degeneracy re-derived from the panel CSV;
`wilson_ci` written from a second algebraic form (the roots of `(p̂ − p)² = z²p(1−p)/n`); the frozen
composition re-extracted by a **second** `ast` pass and re-executed; the survival chain recounted
from the fetch log line by line; the `−1` sentinel arithmetic recomputed from the per-replicate
windows. **None rests on a continuous value R15 produced**, and the witness is a classification
column rather than a blocking anchor — as `data/reference/README.md` requires — with the single
exception of the integer composition, which is not a Monte-Carlo replicate and whose movement would
make nothing in this stream comparable to v87 at all.

Four assertions are **self-invalidating**, one per register entry. If a later campaign brings the
scatter coefficient above `+0.99`, restores the `4.8`–`6.4%` envelope at one decimal, makes the
default arm bit-identical to the witness on `rho_sign_meas`, or changes what the two vendored
scripts declare, the corresponding test fires — and what must change then is `docs/DEVIATIONS.md`,
never the assertion.
