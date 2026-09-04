# Camera-ready candidate — the phase false-alarm probability beside the 3-day detection moves from 1.3 % to 1.1 %

| Field               | Value                                                                                            |
| ------------------- | -------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                        |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:real_world` L331               |
| Trigger             | Acceptance notification, 14 November 2026                                                        |
| Evidence            | `results/R13_oracle_ceiling/data/R13_oracle_operating_points.csv` (`E1 / D2 / V1 / OP2b_ARL0_252`) and `R13_oracle_frontier.csv` (its threshold neighbourhood) |
| Register entry      | `docs/DEVIATIONS.md`, `R13-campaign-redraw` — Class A, **D2**                                    |
| Cost                | one numeral                                                                                      |
| Blocking dependency | shares L331 with `R13_v87_operating_points.md` and `R13_v87_frozen_null_scope.md`; the three search strings are **disjoint** and the three edits commute |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being corrected.** Prompt §2.6 requires migrating off the delivered
`np.random.default_rng(20260716)` — a generator keyed on nothing — to a 128-bit `SeedSequence`
derived from the semantic coordinates of each task. That redraws the 20 000-replicate `FPR_H`
bootstrap and the 5 000-replicate `ARL₀` null, and it is required by the specification rather than
by any observed failure. Every Monte-Carlo value of the campaign therefore moves; this is the
`R11-regenerated` and `R05-campaign-redraw` situation and is acknowledged in advance.

**One published numeral moves at v87's printing precision.** The phase false-alarm probability of
the 3-day likelihood-ratio detection is `0.01275` in the submitted campaign and **`0.01105`** in
the regenerated one: `1.3\%` becomes **`1.1\%`**.

**Nothing else in the sentence moves.** The 3-day delay is unchanged, the 16-day standardized-mean
delay is unchanged, the order of the two arms is unchanged, and the `10.6×` Jensen ratio — which
has no Monte Carlo in it — reproduces to the last digit.

**Two mechanisms, both readable from the shipped CSV rather than inferred.**
`OP2b_ARL0_252` selects the first threshold whose bootstrap `ARL₀` reaches 252, and that `ARL₀` is
a mean over 5 000 regenerated GARCH paths:

| grid index | `λ`         | `FPR_H`   | `ARL₀`     | `τ` |
| ---------- | ----------- | --------- | ---------- | --- |
| 145        | `7.287181`  | `0.01485` | `226.0884` | 3   |
| 146        | `7.748148`  | `0.01140` | `250.2844` | 3   |
| **147**    | `8.238274`  | `0.01105` | `293.1022` | 3   |
| 148        | `8.759404`  | `0.00945` | `321.3612` | 3   |
| 149        | `9.313500`  | `0.00895` | `350.9762` | 4   |

Index 146 is the threshold the submitted campaign selected. Its regenerated `ARL₀` is `250.28`,
just below the 252 the operating point requires, so the selection moves one grid step to index
147. But at index 146 itself the regenerated `FPR_H` is already `0.01140`, i.e. `1.1\%`: **the
bootstrap redraw accounts for most of the movement and the one-step threshold shift for the
rest.** The binomial standard error at `p = 0.0127` over `N = 20 000` replicates is `0.00079`, so
`0.01275 → 0.01140` is `1.7` standard errors — an ordinary draw, not a defect in either campaign.

**The delay is robust across the whole neighbourhood.** `τ = 3` holds at four consecutive grid
indices spanning `FPR_H` from `1.49\%` down to `0.95\%`, which is why the numeral the sentence is
built around does not move while the probability beside it does.

## Edit 1 — `sec:real_world` L331, the numeral

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 331** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`). It is disjoint from the strings the two sibling candidates search.
Verify once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
phase false-alarm probability $1.3\%$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
phase false-alarm probability $1.1\%$
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**The numeral must not be quoted without its operating point.** `1.1\%` is the bootstrap
false-alarm probability at `OP2b_ARL0_252` on the certified parametric oracle `V1`. At the
iso-FPR point the same detector sits at `4.7\%` with the same 3-day delay, and at index 148 of the
same sweep at `0.95\%`. The companion candidate `R13_v87_operating_points.md` supplies the clause
that names the calibration, and applying this edit without that one leaves the corrected numeral
as unlocatable as the original.

**This is not evidence that the submitted value was wrong.** Two draws of the same 20 000-replicate
bootstrap separated by `1.7` standard errors are two ordinary draws. What the repository can say
is which draw its own artefacts contain; it cannot and does not say which is closer to the true
probability.

**No tolerance was widened and no seed was chosen.** The re-keying is required by the
specification, was fixed before the campaign ran, and the movement was classified afterwards.
Preamble §S4.7 forbids the reverse order and nothing here reverses it.
