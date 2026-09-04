# Camera-ready candidate — L331 prints three numerals without naming their calibration, and calls a different calibration "the matched operating point"

| Field               | Value                                                                                            |
| ------------------- | -------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                        |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:real_world` L331               |
| Trigger             | Acceptance notification, 14 November 2026                                                        |
| Evidence            | `results/R13_oracle_ceiling/data/R13_oracle_operating_points.csv`                                |
| Register entries    | `docs/DEVIATIONS.md`, `R13-operating-points-unnamed` and `R13-negative-control-scope` — Class A, no severity |
| Cost                | +32 words in one sentence; no number in the body text changes                                    |
| Blocking dependency | shares L331 with `R13_v87_covid_delay_numerals.md` and `R13_v87_frozen_null_scope.md`; the three search strings are **disjoint** and the three edits commute |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed: streams after R13 may touch the same sentence, and applying a
correction before the inventory closes guarantees reapplying it later.

**What is being corrected.** No number is wrong. One sentence of L331 reports quantities from
**two different operating points** and names neither, so a reader holding the artefacts cannot
locate either.

The oracle frontier is a curve, not a point: `R13_oracle_frontier.csv` sweeps 200 thresholds per
cell and `R13_oracle_operating_points.csv` reads four calibrations off each sweep. L331 uses two
of them in one sentence.

| L331 clause                                                              | operating point actually read | rule                                        |
| -------------------------------------------------------------------------- | ------------------------------- | --------------------------------------------- |
| "detects it in `3` trading days … phase false-alarm probability `1.3\%`"  | `OP2b_ARL0_252`               | first `λ` whose bootstrap `ARL₀` reaches 252 |
| "to `16` days (standardized-mean CUSUM)"                                  | `OP2b_ARL0_252`               | the same                                     |
| "no alarm on the 2011 correction at **the matched operating point**"      | `OP1_isoFPR5_H`               | first `λ` whose bootstrap `FPR_H` ≤ `5\%`    |

The consequence is concrete. At the iso-FPR point the same COVID row gives a **6**-day
standardized-mean delay, not 3 and not 16; at `OP2b` the 2011 correction **does** alarm, on all
ten dead bands, at `FPR_H` between `0.23` and `0.34`. Either number read at the other point
contradicts the sentence, and the sentence does not say which is which.

`ARL₀ ≥ 252` is moreover not an arbitrary choice: it is *one false alarm per trading year*, which
is the calibration the two sentences immediately preceding L331 already use for the sign floor
("a floor of `≈34` trading days at one false alarm per year"). Naming it costs a clause and ties
the oracle paragraph to the budget the census paragraph already fixed.

**A second, narrower point about the same sentence.** "no alarm on the 2011 correction at the
matched operating point" is true of the two dead-band settings Figure 14's caption names — `δ = 0`
and `δ_opt` — and of no others. Inside the *same* iso-FPR band, four larger dead bands alarm at 69
days of a 108-day phase:

| `δ`    | `FPR_H`   | `τ`  | `T`  |
| ------ | --------- | ---- | ---- |
| `0.25` | `0.04325` | 69   | 108  |
| `0.30` | `0.04480` | 69   | 108  |
| `0.40` | `0.04350` | 69   | 108  |
| `0.50` | `0.03520` | 69   | 108  |

The **caption is exact** because it names its settings; the body sentence is not, because it does
not. The distinction is one of dead band, not one of calibration, and both edits below are needed
for a reader to check the claim.

## Edit 1 — `sec:real_world` L331, name the calibration of the two delays

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 331** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`). It is disjoint from the strings the two sibling candidates search.
Verify once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
to $16$ days (standardized-mean CUSUM)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
to $16$ days (standardized-mean CUSUM), both read at the threshold whose bootstrap in-control average run length reaches $252$ trading days---one false alarm per year, the calibration used for the sign floor above
~~~~~~~~~
>>> FIN DU BLOC

## Edit 2 — `sec:real_world` L331, name the matched operating point and its two settings

**Verification of the search string.** Quoted from **line 331** verbatim, `grep -Fc` returns `1`,
and disjoint from Edit 1.

<<< RECHERCHER
~~~~~~~~~latex
no alarm on the 2011 correction at the matched operating point
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
no alarm on the 2011 correction at the matched iso-FPR operating point ($\mathrm{FPR}_H \le 5\%$), at the two dead bands of Figure~\ref{fig:oracle_frontier}
~~~~~~~~~
>>> FIN DU BLOC

The second edit does two things at once: it names the operating point, which is *not* the one the
first half of the sentence uses, and it restricts the claim to the settings under which it holds —
which is what the figure caption already does and what the body sentence omits.

## What must not be done with this candidate

**This is not a correction of a value.** Every quantity L331 prints reproduces except the
false-alarm probability, which is the separate deviation `R13-campaign-redraw` and has its own
candidate. Merging the two edits would attach a numerical correction to a clarification and make
the reason for each unreadable.

**The `69`-day alarm on the 2011 correction must not be attributed to `OP2b`.** It is an iso-FPR
alarm, at `FPR_H` between `0.035` and `0.045`. The alarms `OP2b` produces on the same episode sit
at `FPR_H` between `0.23` and `0.34`, which is not an iso-FPR point at all, and writing the 69 days
there would be refuted by one `pandas` filter on
`results/R13_oracle_ceiling/data/R13_oracle_operating_points.csv`.

**Neither edit licenses a claim about `δ_opt` being the right dead band.** `δ_opt = |Δ_std| / 2`
is the delivered protocol's own choice and R13 measures it; nothing in this stream establishes
that it is optimal for anything, and no camera-ready text derived from this file may say so.
