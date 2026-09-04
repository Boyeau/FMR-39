# AUDIT — R13, oracle ceiling and the clairvoyant frontier

This is the only document transmitted to the orchestrator. It contains: what R13 establishes and
what it does not; the central control the prompt was built around and how it resolves; the eight
controls with their margins and their trigger probability under their own null; the deviation
classification, including one **D2**; the reproducibility evidence with the SHA-256 digests of
both runs pasted as-is and the full `run_tests.sh` output; the design decisions taken outside the
plan; the findings that revise the plan's own premises; and the open questions, left open.

R13 measures v87 Figure 14 (`fig:oracle_frontier`) and every numeral of **L331**, the paragraph
that separates the two readings of the Sharpe ceiling and asks what a clairvoyant monitor could
reach.

---

## 1. What R13 establishes, in one paragraph

Running the look-ahead oracle campaign on the four SPY episodes R16 dated — a CUSUM on returns
standardized by the conditional volatility of a GARCH(1,1) fitted on a window *including* the
crash, read against a bootstrap null that freezes that volatility path — **seven of the eight
published quantities of L331 reproduce**: the `3`-day likelihood-ratio detection of the 2020
crash, the `16`-day standardized-mean detection, the `10.6x` path divergence (`10.644703`, to the
last digit of the witness), the `220` certified and `176` contaminated oracle rows, and the three
census verdicts — 2009 recovery detected, 2019 advance missed, no alarm on the 2011 correction at
the matched operating point. Figure 14's caption holds at both settings it names. **The eighth
does not**: the phase false-alarm probability beside the 3-day delay is `1.3\%` in the manuscript
and **`1.1\%`** here, which is a **Class A, D2** registered as `R13-campaign-redraw` and traced
to its mechanism in §4.

**The control the prompt was built around resolves in the manuscript's favour.** §2.1 of the R13
prompt flags "`3` trading days … phase false-alarm probability `1.3\%`" as a possible conflation
of two operating points — a would-be D3 — because the twelve rows it inspected paired `tau = 3`
with `FPR_H = 0.68` and `tau = 6` with `FPR_H = 0.0408`. It is not a conflation. Those rows are
`E1 / D1`, the **standardized-mean** arm; the pair belongs to `E1 / D2 / V1 /
OP2b_ARL0_252`, a single row of `R13_oracle_operating_points.csv` carrying `tau = 3` and
`FPR_H = 0.01105` together. The prompt's §6 notation gloss reverses the two detector families,
which is why its search looked on the wrong arm. **No halt, no D3.**

---

## 2. Four things the reader must not take from this stream

**The oracle is not a monitor, and the 3 days are not a delay anyone can achieve.** The GARCH
parameters are fitted on a window containing the crash. v87 says so — "the `3`-day figure is an
upper envelope no online monitor attains" — and nothing measured here weakens that sentence or
strengthens it.

**The `10.6x` is a property of one oracle, not of the COVID phase.** On the same episode the
leave-one-out realized-volatility oracle gives `1.5505` and the contaminated one `1.5833`. The
ratio measures how much the *conditional* variance path lags the shock; a reader who quotes it as
a property of the crash has quoted the wrong object. The test suite asserts the separation so
that a future change cannot dissolve it silently.

**The D2 does not touch a qualitative claim.** `1.3\% -> 1.1\%` moves a printed numeral. The
delay it accompanies is unmoved, the standardized-mean delay is unmoved, the order of the two
detector arms is unmoved, and the sentence's assertion — that a variance-aware monitor is not
bounded by the sign floor — is unaffected. The census verdicts, the Jensen ratio and the figure's
caption reproduce.

**`tau` has no sampling interval.** Each episode contributes ONE realized crossing time. The
horizontal axis of Figure 14 carries a Wilson interval on every point; the vertical axis carries
none, and none can be constructed from one path. Two campaigns can differ by a whole grid step in
`tau` without either being wrong, which is why §4 prints the threshold neighbourhood rather than
the selected row alone.

---

## 3. Controls, with their margins and their trigger probabilities

**Which rows each control reads.** C1, C2, C5 and C6 read the certified parametric oracle `V1`,
which is what every published number of L331 is carried by. C2 additionally reports `V2` and `V3`,
because one published clause describes them. C3, C4 and C7 are structural and read everything.
C8 is a reproducibility axis over the whole artefact set.

### C1 — one published pair, one row

Deterministic assertion; **trigger probability 0** if the manuscript and the campaign agree. A
pair needing two rows would be a conflation of operating points and a D3, and the run stops.

| v87 quantity                  | row                                      | `lambda*`   | value(s)                      |
| ----------------------------- | ---------------------------------------- | ----------- | ----------------------------- |
| `3` days **and** `1.3\%`      | `E1 / D2 / V1 / OP2b_ARL0_252`           | `8.238274`  | `tau = 3`, `FPR_H = 0.01105`  |
| `16` days (standardized-mean) | `E1 / D1 / delta=0 / V1 / OP2b_ARL0_252` | `15.213167` | `tau = 16`, `FPR_H = 0.00405` |
| `10.6x`                       | `R13_oracle_diagnostics`, `E1 / V1`      | —           | `jensen_ratio = 10.644703`    |

All three rows are `oracle_certified = True` and `oracle_contaminated = False`. The threshold
neighbourhood of each is logged (§4) so that the one-grid-step sensitivity of `OP2b` is visible
rather than inferred.

### C2 — certification, measured and not gated

The admissibility check is `p_lb_z2 >= 0.01 and 0.8 <= std_z_ref <= 1.25` on the standardized
reference window, evaluated per (episode, oracle). **220 of 528** operating-point rows are
certified and **176** contaminated, reproducing the witness counts exactly. Five (episode, oracle)
pairs are certified — `E1/V1`, `E1/V2`, `E2/V1`, `E3/V1`, `E4/V1` — at 44 rows each; the four `V3`
pairs are contaminated by construction.

| ep / oracle | `p_lb_z2`  | `std_z_ref` | certified | contaminated |
| ----------- | ---------- | ----------- | --------- | ------------ |
| E1 / V1     | `0.614823` | `0.973817`  | **yes**   | no           |
| E1 / V2     | `0.031229` | `1.061074`  | **yes**   | no           |
| E1 / V3     | `1.93e-04` | `0.974828`  | no        | **yes**      |
| E2 / V1     | `0.777953` | `0.990713`  | **yes**   | no           |
| E3 / V1     | `0.645456` | `0.965097`  | **yes**   | no           |
| E4 / V1     | `0.088739` | `1.001967`  | **yes**   | no           |

**One published clause rests on a non-certified oracle, and survives on certified evidence.** "a
look-ahead *centered realized* volatility, pricing the crash into `sigma_t` contemporaneously,
yields no alarm at iso-FPR" describes `V3`, whose own check fails at `p_lb_z2 = 1.93e-4`. The
certified leave-one-out oracle `V2` returns the same verdict — `0` of `10` standardized-mean
settings alarm within `T` at `OP1_isoFPR5_H` — so the clause holds on certified evidence. Both are
reported; neither is suppressed.

**Every other published number is carried by `V1` rows, all certified.**

### C3 — no `ARL0` without its censored fraction

Structural assertion; **trigger probability 0**. The mean of a right-censored run length is biased
**downward**, so an `ARL0` published without its censored fraction understates the time between
false alarms by an amount the reader cannot bound. `protocol_19b` carries `ARL0` and no censored
fraction at all; the port adds `arl0_censored_frac` to the operating-point table.

| quantity                                           | value                              |
| -------------------------------------------------- | ---------------------------------- |
| frontier rows where the `ARL0` null was run        | `8800` (the `V1` rows)             |
| rows whose mean survived the 5 % censoring rule    | `6750`                             |
| rows suppressed to `NaN` rather than published low | `2050`                             |
| worst censored fraction among the survivors        | `0.0496`                           |
| mean censored fraction over all evaluated rows     | `0.2053`                           |
| operating-point rows carrying a finite `ARL0`      | `136`, every one with its fraction |

The published row's own fraction is `0.0000`, which the macro `\RThirteenArlZeroCensoredFrac`
carries; the campaign-wide distribution is logged beside it so the macro cannot be read as a
property of the campaign.

### C4 — the frozen-volatility null, and the two limits of the phrase

Deterministic assertion; **trigger probability 0**. The SHA-256 of the `sigma_t` vector
multiplying the resampled innovations under `H0`, taken on its IEEE-754 bytes, equals the digest of
the vector dividing the observed returns under `H1`, over `[0, H_ep)`, on **all twelve** (episode,
oracle) pairs. The comparison runs inside each worker and stops the episode on any difference.

**Two limits are stated because the phrase does not carry them.**

1. On the **standardized-mean** arm the frozen path cancels:
   `sign(Delta) * (mu_0 + sigma_t Z* - mu_0) / sigma_t = sign(Delta) * Z*`. `FPR_H` there is a
   property of the resampled innovations alone, and freezing the path, redrawing it or replacing
   it by a constant would give the same axis. The freeze binds only on the likelihood-ratio arm,
   where `sigma_t` enters squared. The residual measured per episode is float64 rounding of the
   cancellation and is logged as such, not as a dependence.
2. The **`ARL0` null is not frozen**. It regenerates 5,000 GARCH paths of 5,000 steps from the
   fitted `(omega, alpha, beta)` after a 500-step burn-in, and it is the null that *selects*
   `lambda` at `OP2b_ARL0_252` — the operating point behind every numeral of L331.

Registered as `R13-frozen-null-scope`, Class A, no severity.

### C5 — the negative control, asserted at the settings the caption names and characterised elsewhere

Deterministic assertion on the two named settings; **trigger probability 0**. At
`OP1_isoFPR5_H` on `V1`, the 2011 correction does not alarm at `delta = 0` (`FPR_H = 0.04015`,
`lambda* = 23.371578`) nor at `delta_opt = 0.079738` (`FPR_H = 0.0465`,
`lambda* = 17.198728`). **Figure 14's caption holds as written.**

**Four larger dead bands inside the same iso-FPR band do alarm**, at 69 days of a 108-day phase:
`delta = 0.25` at `FPR_H = 0.04325`, `0.30` at `0.04480`, `0.40` at `0.04350`, `0.50` at
`0.03520`. Every one is inside the 5 % band the operating point defines, so the distinction is one
of **dead band**, not one of calibration. The caption is exact *because* it names its two
settings; the L331 body sentence does not name them and is true only of those two. Nothing is
adjusted and the four rows ship. Registered as `R13-negative-control-scope`.

**The alarm must not be attributed to `OP2b`.** At `OP2b_ARL0_252` the same episode alarms on all
ten dead bands, but at `FPR_H` between `0.2307` and `0.3366`, which is not an iso-FPR point at
all. Writing the 69 days there would be refuted by one `pandas` filter on a CSV this stream ships.

**The four census verdicts at the matched operating point**, standardized-mean CUSUM on `V1`:

| ep  | event            | `delta = 0`                                 | `delta_opt`                 | v87            |
| --- | ---------------- | ------------------------------------------- | --------------------------- | -------------- |
| E1  | COVID crash 2020 | `FPR_H .04405`, `tau 6` / 23 ✓              | `tau 4` / 23 ✓              | detected       |
| E2  | 2009 recovery    | `FPR_H .03525`, `tau 210` / 284 ✓           | `tau 485` / 284, beyond `T` | **detected** ✓ |
| E3  | 2019 advance     | `FPR_H .03605`, `tau 423` / 289, beyond `T` | no alarm                    | **missed** ✓   |
| E4  | 2011 correction  | `FPR_H .04015`, no alarm                    | no alarm                    | **no alarm** ✓ |

E2's and E3's verdicts are **setting-dependent** in the same way E4's is, and the verdict macros
carry both settings for that reason. v87 claims neither more nor less than the table's third and
fourth columns support.

### C6 — coherence with R16

Deterministic assertion; **trigger probability 0**. `ADD_min_census`, `T_days_phase` and
`detectable_flag_census` are read from `results/R16_regime_census/data/R16_regime_census.csv`, the
**default-run canonical arm**, with `float_precision='round_trip'` on both sides, under the
mapping `AUDIT_R16.md` §5 fixes (`ADD_min_days -> ADD_min_census`,
`detectable_flag -> detectable_flag_census`). All four episodes are identical, margin `0`.

| ep  | SPY phase | dates                   | `T_days` | `ADD_min_census` | `detectable_flag_census` |
| --- | --------- | ----------------------- | -------- | ---------------- | ------------------------ |
| E1  | 22        | 2020-02-19 → 2020-03-23 | 23       | `42.075066`      | `False`                  |
| E2  | 15        | 2009-03-09 → 2010-04-23 | 284      | `227.280121`     | `True`                   |
| E3  | 21        | 2018-12-24 → 2020-02-19 | 289      | `223.040113`     | `True`                   |
| E4  | 18        | 2011-04-29 → 2011-10-03 | 108      | `462.293761`     | `False`                  |

**A second half of C6 is the branch the port removed.** The delivered `process_episode`
recomputes `T_days` and the Sharpe from the return series and, on divergence, **overwrites the
census values in place** under the banner "P16/P3 INCOMMENSURABILITY … SEQUENTIAL OVERRIDE". It
never fired in the submitted campaign, and it does not fire here — `T_days` agrees exactly on all
four episodes and the Sharpe to at most `8.9e-16` absolute, against a branch threshold of `1e-3` —
but a silent substitution of the census R13 exists to consume is exactly the degraded path §S4.3
bans. Both columns are kept and divergence is fatal.

**R16's D3 is on the description of its dating, not on its values.** R13 inherits no numerical
displacement, and no text of this stream repeats v87's "Pagan--Sossounov dating of the four
streams" phrasing.

### C7 — source identity of the carried primitives

Deterministic assertion; **trigger probability 0** unless a copy has drifted. Six primitives are
extracted by `ast` at run time and compared byte for byte against the files that own them:
`wilson_ci`, `compute_oracle_v2_v3` and `check_monotonicity` against
`data/reference/R13/Priorite_19_oracle_ceiling_parallel.py`; `_garch_nll`, `fit_garch_qmle` and
`compute_gamma_exact` against `experiments/R01_real_world_backtest/exp_R01_real_world_backtest.py`.
**2 645 characters compared, 0 differences.** Preamble §S4.2 forbids hoisting any of them into
`experiments/common/`, so the duplication is deliberate and this control is what keeps it from
drifting. The control caught two real transcription defects before the first run: the trailing
whitespace of two lines inside `compute_oracle_v2_v3` and one inside `fit_garch_qmle`.

Three routines are **adapted** rather than carried — `run_qmle_recovery`, `run_detector_recovery`
and `process_episode`, each of which takes an injected generator where the delivered script builds
one from a bare integer seed. Byte identity is not assertable on them, so the witness source of
each is quoted **in full** in the log with its SHA-256, which is the treatment
`exp_R11_multi_detector.py` gives `simulate_garch11`.

### C8 — reproducibility, two runs at different worker counts

See §5. Eight artefacts, two runs, **0 differences**.

### Every multi-test control logs `1 - (1 - p)^m` before its result is read

Two gates carry a family of tests and both log the family-wise trigger probability first:
the QMLE recovery family (`m = 2`, `1 - (1 - 0.001)^2 = 0.19990\%`) and the detector-recovery
family (`m = 12`, `1 - (1 - 0.001)^12 = 1.19342\%`). §7 explains why the per-condition level is
`0.001` and where it comes from.

---

## 4. Deviation classification against v87

### The eight published quantities

| v87 L331 / Figure 14 caption                                   | witness       | regenerated       | class                      |
| -------------------------------------------------------------- | ------------- | ----------------- | -------------------------- |
| `3` trading days, likelihood-ratio increments                  | `3`           | **`3`**           | reproduces                 |
| phase false-alarm probability `1.3\%`                          | `0.01275`     | **`0.01105`**     | **D2**                     |
| `16` days, standardized-mean CUSUM                             | `16`          | **`16`**          | reproduces                 |
| path divergence `10.6x` the unconditional budget               | `10.644703`   | **`10.644703`**   | reproduces (deterministic) |
| 2009 recovery detected                                         | `tau 210`/284 | **`tau 210`/284** | reproduces                 |
| 2019 advance missed                                            | `tau 423`/289 | **`tau 423`/289** | reproduces                 |
| no alarm on the 2011 correction at the matched operating point | no alarm      | **no alarm**      | reproduces                 |
| the 2011 correction is not detected at either setting          | no alarm      | **no alarm**      | reproduces                 |

The whole `R13_oracle_diagnostics.csv` reproduces the witness to a worst numeric difference of
`8.9e-16` (on `KL_corollary`, a float64 reassociation of a deterministic quantity), and
`R13_clairvoyant_floor.csv` to `2.8e-14` on `ADD_min_census`, which is the witness's non-round-trip
CSV formatting and is **D0**. `R13_oracle_frontier.csv` and `R13_oracle_operating_points.csv` move
as the re-keying requires: worst `|difference|` `74.05` and `157.38` on `ARL0`, which is a mean of
5,000 regenerated run lengths.

### `R13-campaign-redraw` — Class A, D2, pre-classified

Prompt §2.6 requires the migration from `np.random.default_rng(20260716)` to a 128-bit
`SeedSequence` keyed on role and index. Every Monte-Carlo value moves; one printed numeral moves
at v87's precision. **Two mechanisms, both readable from the shipped CSV rather than inferred:**

| grid index | `lambda`   | `FPR_H`   | `ARL0`     | `tau` |
| ---------- | ---------- | --------- | ---------- | ----- |
| 145        | `7.287181` | `0.01485` | `226.0884` | 3     |
| 146        | `7.748148` | `0.01140` | `250.2844` | 3     |
| **147**    | `8.238274` | `0.01105` | `293.1022` | 3     |
| 148        | `8.759404` | `0.00945` | `321.3612` | 3     |
| 149        | `9.313500` | `0.00895` | `350.9762` | 4     |

Index 146 is the threshold the submitted campaign selected. Its regenerated `ARL0` is `250.28`,
just under the 252 the operating point requires, so the selection moves one grid step — the
sensitivity the plan's second risk anticipated. But at index 146 itself `FPR_H` is already
`0.01140`, i.e. `1.1\%`: **the bootstrap redraw accounts for most of the movement and the
threshold shift for the rest.** The binomial standard error at `p = 0.0127`, `N = 20 000` is
`0.00079`, so `0.01275 -> 0.01140` is `1.7` standard errors — an ordinary draw. `tau = 3` holds at
four consecutive grid indices spanning `FPR_H` from `1.49\%` to `0.95\%`, which is why the delay
does not move while the probability beside it does.

The standardized-mean arm's own `OP2b` selection did **not** move: `lambda* = 15.213167` is the
witness's threshold to the last digit, and `tau = 16` with it.

Candidate: `docs/camera_ready_candidates/R13_v87_covid_delay_numerals.md`.

### `R13-operating-points-unnamed` — Class A, no severity

L331 reports `3` days, `1.3\%` and `16` days at `OP2b_ARL0_252` and then, in the same sentence,
says "at the matched operating point" for `OP1_isoFPR5_H`. It names neither. The consequence is
concrete: at iso-FPR the same COVID row gives a **`6`**-day standardized-mean delay
(`FPR_H = 0.04405`), and the likelihood-ratio arm gives `tau = 3` at `FPR_H = 0.0451` — so a
reader looking for "3 days at 1.3 %" on the iso-FPR page finds 3 days at 4.5 %, and a reader
looking on the `OP2b` page for the 2011 verdict finds an alarm. Candidate:
`docs/camera_ready_candidates/R13_v87_operating_points.md`.

### `R13-frozen-null-scope` and `R13-negative-control-scope` — Class A, no severity

Both are stated in §3 under C4 and C5. Neither moves a value; each records a gap between what a
sentence says and what the campaign it describes does.

### What does **not** reach the register

**`anticonservative` is a defect, not a tautology, and it is reported here only.**
`data/reference/R13/Priorite_19_oracle_ceiling_parallel.py:411` writes the literal
`'anticonservative': True` into every row of the clairvoyant-floor table. Nothing in that script
ever reads `n_star_realized` against `n_star_analytic`, and the comparison the name asserts runs
**both ways** in the data: `E1/V1` gives 2 against 1 and `E4/V1` 69 against 64 (realized ABOVE
analytic), while `E2/V1` gives 1 against 103 and `E3/V1` 1 against 120 (below). The column is
therefore false on four of the twelve rows and undefined on two more, where the realized floor was
never crossed. The port replaces it with `n_star_realized_below_analytic`, which performs the
comparison and carries `NaN` where the crossing never happened — a floor that was never crossed is
not a floor that was crossed early.

**No entry reaches `docs/DEVIATIONS.md`**, because v87 publishes no numeral from
`protocol_19d` and §8's scope filter keeps a defect with no manuscript consequence inside the
audit. The prompt's §2.4 asked which of the two it is; the answer is *defect*, and this paragraph
is where it is recorded.

**The plan's expectation about the published censored fraction was wrong, harmlessly.** The plan
notes "(Published row: `0.0004`.)". The witness's own `OP2b` row for `E1 / D2 / V1` carries
`arl0_censored_frac = 0.0`, and so does the regenerated one. No macro is affected: the value is
computed from the row, never typed.

---

## 5. Reproducibility and the whole suite

```bash
./run_experiment_R13.sh                 # 160 s total, 4 workers: _a 79 s, _b 80 s
./run_experiment_R13.sh --n-jobs 1      # 540 s total, 1 worker
./run_tests.sh
```

`run_all.sh` discovers `run_experiment_R13.sh` by sorted enumeration. **Neither `run_all.sh` nor
`run_tests.sh` is modified** — `git diff --stat` shows both untouched.

### C8, both digest sets pasted as-is

Run 1, default `--n-jobs 4`:

```
8539d7002750fe4e940114040b5239e2cf7c171e803cfb013507a0356b3993db  results/R13_oracle_ceiling/data/R13_clairvoyant_floor.csv
44765f6dd83e96d432bf4f296e1c61300d79db14262bce21fa46e54437d2e6c5  results/R13_oracle_ceiling/data/R13_detector_recovery.csv
380b5fadf0e383c18fc6351089ea8c56dde9a7fe7b1e8f16edce8e4de8320861  results/R13_oracle_ceiling/data/R13_oracle_diagnostics.csv
4fbf6b7d1786a3afc400961dc214573fb7fc7c561c08df97f4c72cc3ad72230d  results/R13_oracle_ceiling/data/R13_oracle_frontier.csv
c6b90ea9ad55b8d33b5966561021b1b9cf893bedefe2dc726a6bfb2481eff546  results/R13_oracle_ceiling/data/R13_oracle_operating_points.csv
058b583a8c7ceb54dd2512bc05fa26900ad1cba7398016bcae49c804ef28d897  results/R13_oracle_ceiling/data/R13_qmle_recovery.csv
249954c3168fbcb2532c999b0406da20414f5bfccfbd7c8efca266fdf4fd0c18  results/R13_oracle_ceiling/tables/R13_claims.tex
f23c8411dbb882ee2d62ef5843007af7d5d8ecff094eecf0ca8acfd725a80c3c  results/R13_oracle_ceiling/figures/fig14_oracle_frontier.png
```

Run 2, `--n-jobs 1`:

```
8539d7002750fe4e940114040b5239e2cf7c171e803cfb013507a0356b3993db  results/R13_oracle_ceiling/data/R13_clairvoyant_floor.csv
44765f6dd83e96d432bf4f296e1c61300d79db14262bce21fa46e54437d2e6c5  results/R13_oracle_ceiling/data/R13_detector_recovery.csv
380b5fadf0e383c18fc6351089ea8c56dde9a7fe7b1e8f16edce8e4de8320861  results/R13_oracle_ceiling/data/R13_oracle_diagnostics.csv
4fbf6b7d1786a3afc400961dc214573fb7fc7c561c08df97f4c72cc3ad72230d  results/R13_oracle_ceiling/data/R13_oracle_frontier.csv
c6b90ea9ad55b8d33b5966561021b1b9cf893bedefe2dc726a6bfb2481eff546  results/R13_oracle_ceiling/data/R13_oracle_operating_points.csv
058b583a8c7ceb54dd2512bc05fa26900ad1cba7398016bcae49c804ef28d897  results/R13_oracle_ceiling/data/R13_qmle_recovery.csv
249954c3168fbcb2532c999b0406da20414f5bfccfbd7c8efca266fdf4fd0c18  results/R13_oracle_ceiling/tables/R13_claims.tex
f23c8411dbb882ee2d62ef5843007af7d5d8ecff094eecf0ca8acfd725a80c3c  results/R13_oracle_ceiling/figures/fig14_oracle_frontier.png
```

`diff` between the two sets is empty on all eight artefacts. The campaign is keyed per episode
through a 128-bit `SeedSequence`, so the worker count cannot reach any draw; that is what this
axis tests, and it is a stronger axis than R16's arm isolation because R13 does have a stochastic
surface and does run in parallel.

**`_b` certifies the same identity a third way.** It re-runs the campaign in memory rather than
reloading `_a`'s CSVs (preamble §S7 forbids a disk round trip as a memory bridge), then
re-serialises the frames it holds and compares their digests with the files `_a` wrote. All six
match, so the figure and the macros are certified to describe the persisted campaign rather than
assumed to.

### The test suite

`./run_tests.sh` — **221 tests collected, 221 passed, 0 failures in 2.41 s**, of which
**24 are R13's**. Collected counts per file, from `pytest tests/ --collect-only -q`:

```
platform linux -- Python 3.12.9, pytest-9.0.3, pluggy-1.6.0
rootdir: /home/m53/The-Whitening-Advantage-Experiments
collected 221 items

  5  tests/test_R01_claims.py       27  tests/test_R04_claims.py       25  tests/test_R11_claims.py
  8  tests/test_R02_claims.py       21  tests/test_R04b_claims.py      24  tests/test_R13_claims.py
  5  tests/test_R02b_claims.py      22  tests/test_R05_claims.py       28  tests/test_R16_claims.py
  7  tests/test_R02c_claims.py      16  tests/test_R06_claims.py       24  tests/test_R18_claims.py
  9  tests/test_R03_claims.py

============================= 221 passed in 2.41s ==============================
Tests Passed.
```

**No blocking assertion of `tests/test_R13_claims.py` rests on a value R13 produced.** Every one
rests either on a value v87 prints, compared at v87's own printing precision, or on a relation
reimplemented in the test file independently of the experiment:

- the **likelihood-ratio increment identity**, written as a difference of two
  `scipy.stats.norm.logpdf` calls rather than as the algebraic cancellation the campaign applies,
  with a tolerance derived from the cancellation itself (`8 * eps * max|logpdf|`) and from no
  observed deviation — this is what establishes that `D2` is the likelihood-ratio arm and `D1` the
  standardized-mean one, against the prompt's inverted gloss;
- the **frozen volatility path**, rebuilt from the persisted `(omega, alpha, beta)` and the raw
  return series under the reference-window and survival-cap rules, then re-digested: the SHA-256
  matches on all four episodes, so the digest C4 asserts is a digest of the path the manuscript
  describes;
- the **four operating points**, re-selected from the frontier grid by the rule each name states,
  on all 132 cells;
- the **Wilson intervals**, recomputed from the second algebraic form R02 owns;
- the whole **census consumption**, re-read from R16's canonical arm.

The **witness is deliberately not a gate** (`data/reference/README.md`): a cell-by-cell equality
assertion against a campaign the specification requires to be redrawn would fail on the first run
and its only exit would be a widened tolerance. The comparison is *printed* by three reporting
tests and asserted nowhere.

**Two assertions are self-invalidating** and are the ones to watch. If a future change ever
splits the `(3 d, 1.3\%)` pair across two rows, or ever brings the regenerated false-alarm
probability back to `1.3\%`, the corresponding test fires — and what must then be revised is the
prose and `docs/DEVIATIONS.md`, never the assertion. A third watches the negative control: if no
dead band of the matched operating point alarms on the 2011 correction any more,
`R13-negative-control-scope` has dissolved and its register entry is withdrawn.

**The preamble §S4.4 grep is empty** on `experiments/R13_oracle_ceiling/*.py`,
`logs/R13_oracle_ceiling/*.log`, `docs/sections/R13.md` and this audit — the ten-alternative
pattern of §S4.4, which this file deliberately does not quote because quoting it would put it in
its own scope. The suite runs the same pattern over the same five paths, so the check is executed
rather than reported. Also empty: `iterrows`, bare `except:`, and absolute paths — the last three asserted by the test suite
rather than checked by hand. Every produced text file ends in `\n`, asserted by the suite over the
macro file, `requirements/R13.txt`, `docs/sections/R13.md` and this audit.

---

## 6. Design decisions taken outside the plan

1. **The QMLE gate is an equivalence statement, not a bias test.** The plan specifies "the mean of
   `(alpha_hat - alpha)` and `(beta_hat - beta)` over the 88 cells against their Monte-Carlo
   standard error". Two readings are available: a test of `E[margin] = 0`, or a test that the mean
   margin plus its sampling margin still sits inside the delivered per-cell tolerance. **The
   second is implemented**, because the first has a null that is false by construction — the
   quasi-likelihood estimator has a finite-sample bias, which is a property of the estimator and
   not a port error — and a gate whose null is false is the empty-ringing control §S4bis exists to
   forbid. **The justification is a design one and this measurement does not add to it:** at the
   design-effect-corrected variance of §7.2 the bias statistic on `beta` is `t = -1.25`, two-sided
   `p = 0.235`, so a bias gate would **not** have fired — neither at the `0.001` level this
   stream's families use nor at any conventional one. An earlier revision of this audit reported
   `t = -3.38`, `p = 0.0011` and drew the opposite conclusion; that figure divided by the square
   root of 88 correlated cells and is withdrawn. The statistic is logged descriptively and gates
   nothing.
2. **The per-condition level `0.001` is derived from §S4bis's own ceiling.** The larger family has
   `m = 12`, and `1 - (1 - 0.001)^12 = 1.19\%` while `1 - (1 - 0.005)^12 = 5.84\%` would breach
   the 5 % ceiling §S4bis fixes. The same level governs the QMLE family so that one number governs
   both. No level was chosen after seeing a result.
3. **`n_star_realized_below_analytic` carries `NaN`, not `False`, where the realized floor was
   never crossed.** Two of the twelve rows are in that state. Coercing them to `False` would
   reproduce, in a new column, the same defect the old column had: asserting a comparison that was
   never made.
4. **`oracle_verdict` is added to every operating-point row**, not only to the matched one, with
   four values — `not_attainable`, `no_alarm`, `detected_within_T`, `alarm_beyond_T`. A verdict
   defined only where a macro reads it would be a column whose meaning depends on the reader.
5. **The verdict macros carry both settings**, as `<verdict at delta = 0> / <verdict at
   delta_opt>`. E2's and E3's verdicts are setting-dependent, and a single word would hide which
   setting the reader is given.
6. **`data/reference/README.md` gains its two register rows** for the vendored R13 witnesses. The
   file is the register of that directory and leaving it stale would make the origin of eight new
   read-only files unstated. `run_all.sh` and `run_tests.sh` are untouched.

---

## 7. Findings that revise the plan's own premises

1. **The delivered QMLE gate would have stopped this run.** `passes == 88` is the delivered
   criterion; under the re-keyed draw **86 of 88** cells satisfy the per-cell tolerances, so
   `sys.exit(1)` would have fired and no artefact of this stream would exist. The plan classified
   the redesign as required by §S4bis's third corollary and priced the risk of a firing gate; what
   the run adds is that the *delivered* gate is the one that fires, and the redesigned one — whose
   statistic has a null law — passes with `|mean| + z*SE = 0.0110` against a tolerance of `0.03` on
   `alpha` and `0.0166` against `0.05` on `beta`, at the corrected variance of §7.2. The two
   failing cells are the same replicate at the same target: `(alpha, beta) = (0.10, 0.85)`,
   replicate 1, both unconditional scales, where `alpha_hat = 0.133868` misses `0.03` by `0.0039`.
2. **The 88 comparisons carry about 11 independent readings, and the first estimate of that
   number was the wrong one.** Two dependence sources coexist. The visible one: `alpha_hat` and
   `beta_hat` are scale-invariant, so the two unconditional scales of a target return the same
   fit — 44 exact fits, which float non-invariance renders as **47 distinct pairs over 88 cells**
   and which alone would give `n_eff ~ 46`. The dominant one: the replicate key carries no
   parameter — common random numbers, SPECS §1.4 — so **one** innovation stream serves all eight
   configurations. Measured on the `11 x 8` matrix of per-replicate margins: mean pairwise
   correlation `rho_bar = 0.9611` on `alpha` and `0.8957` on `beta`, Kish design effects `7.7275`
   and `7.2697`, hence **`n_eff = 11.39` and `12.11`** — the 11 streams the design contains, not
   88 and not 47. The gate's standard error is inflated by `sqrt(deff)` accordingly; an earlier
   revision divided by `sqrt(88)` and understated it by a factor of `2.78` and `2.70`. Both
   verdicts are unchanged. A max-statistic over 88 comparisons this correlated has neither the
   distribution of its point nor that of 88 independent ones, which is the sharpest available
   statement of why the delivered gate could not be kept.
3. **The threshold grid never took its data-dependent branch.** The plan's third risk is that
   `geomspace(1e-3, 1.1 * max(M_nb), 200)` fires when the bootstrap maximum exceeds 200 and moves
   the grid itself under a redraw. **Zero of 132 cells took it**, in the witness and here; the
   branch is persisted per row in `lambda_grid_rescaled` so the fact is checkable rather than
   asserted.
4. **The Figure 14 caption's "sub-percent false alarms" holds, but not at the operating point the
   sentence's numerals come from.** At `OP2b_ARL0_252` the likelihood-ratio arm sits at
   `FPR_H = 1.105\%`, which is not sub-percent; the standardized-mean arm at the same operating
   point sits at `0.405\%` with `tau = 16 < 23`, and the likelihood-ratio arm reaches `0.945\%`
   with `tau = 3` one grid step further out. The caption is a statement about the *curve* and it
   holds on the curve. It is recorded here because a reader who reads the caption as describing
   the row the body sentence quotes would be reading `1.1\%` as sub-percent.
5. **The plan's premise about the witness's censored fraction is wrong and harmless** (§4).

---

## 8. Open questions, left open

1. **Why the `OP2b` selection moved on the likelihood-ratio arm and not on the standardized-mean
   arm is not established.** The `ARL0` at index 146 of the `D2` sweep is `250.28` against the
   witness's `258.70`, and `250.28` sits below 252 while `258.70` sits above; the `D1` sweep's
   selection is unmoved. Whether the `D2` arm's `ARL0` is systematically more variable near the
   252 crossing, or whether this is a single draw landing on the wrong side of a boundary, would
   need a repeated-`ARL0` experiment this stream does not run and the manuscript does not
   describe. Under the scope filter it is not run. Preamble §S4.5 forbids attributing a mechanism
   the measurement does not establish, and none is attributed.
2. **`delta_opt = |Delta_std| / 2` is the delivered protocol's choice and nothing here evaluates
   it.** It is the dead band that would be optimal for a Gaussian mean shift of size `Delta_std`
   in the CUSUM's own asymptotics, but the campaign runs it on one realized path per episode and
   measures no optimality. Figure 14's caption names it as a setting, not as an optimum, and so
   does this repository.
3. **`tau` has no interval and this stream cannot give it one.** A sampling distribution for the
   realized delay would need either a resampling scheme over the phase — which changes the object
   being measured — or several crash episodes of the same kind, which the census does not contain.
   The one-grid-step sensitivity in §4 is the honest substitute and is not a confidence interval.
4. **Whether `E3`'s role label is right is a question about the census, not about R13.** The
   witnesses label `E3` POSITIVE CONTROL B while v87 gives the 2019 advance as *missed*, and both
   the submitted campaign and this one measure it missed at the matched operating point. The label
   is a description in the delivered script's episode table, it reaches no CSV column that any
   claim reads, and preamble §S4.5 forbids inferring an intention from it. It is recorded and not
   corrected.
5. **The oracle admissibility check is not calibrated.** `p_lb_z2 >= 0.01 and 0.8 <= std_z_ref <=
   1.25` is the delivered rule; nothing measures how often it would reject an oracle that is in
   fact adequate, so its verdicts license the certified/contaminated split and nothing more. `E1 /
   V2` passes at `p_lb_z2 = 0.031`, which is inside a factor of three of the threshold, and a
   different reference window could move it across. That fragility is stated rather than resolved.
