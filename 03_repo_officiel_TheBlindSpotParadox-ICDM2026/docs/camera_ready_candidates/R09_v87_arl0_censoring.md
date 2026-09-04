# Camera-ready candidate — panel C's CUSUM and MIX curves sit on the simulation horizon

| Field               | Value                                                                                                                                                            |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Status**          | **PARKED — do not apply**                                                                                                                                        |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), Figure 9 caption L559, panel **(C)**                                                                 |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                                        |
| Evidence            | `results/R09_eprocess_anytime/data/R09_arl0.csv` (`censored_frac`, `arl0_implied_lower_bound`), control C1 and C2 in `logs/R09_eprocess_anytime/exp_R09_eprocess_anytime.log` |
| Register entry      | `docs/DEVIATIONS.md`, `R09-arl0-censoring` — Class A, no severity                                                                                                |
| Cost                | +22 words in one clause; **no number changes**, and the figure is replaced by the repository's own                                                                |
| Blocking dependency | shares L559 with `R09_v87_stream_counts.md` and `R09_v87_delay_parity_scope.md`; the search strings are **disjoint** and the three edits commute                  |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being corrected — and what is not.** Panel C's caption reads "Average run length vs.\
$\alpha$: e-CUSUM satisfies $\mathrm{ARL}_0 \ge 1/\alpha$". **That sentence is exact and this
candidate does not touch its truth.** e-CUSUM's run lengths are right-censored on `0.00%` of
replicates at six of the seven levels and on `0.055%` at the seventh, so its `ARL₀` is a
measurement, and it clears `1/α` by a factor of at least `20.5`.

What the caption does not say is that the **other two curves in the same panel are not
measurements at all.** The panel plots three arms; the caption names one. For CUSUM and MIX the
run length is right-censored at the simulation horizon on the great majority of streams:

| arm      | censored fraction across the seven levels | `ARL₀` range          | the horizon |
| -------- | ------------------------------------------ | --------------------- | ----------- |
| CUSUM    | `65.1%` – `95.5%`                          | `16 250` – `19 553`   | `20 000`    |
| MIX      | `90.5%` – `99.1%`                          | `18 384` – `19 842`   | `20 000`    |
| e-CUSUM  | `0.00%` – `0.055%`                         | `205` – `2 751`       | `20 000`    |

A mean of `min(fa, T_ext)` over a sample censored at fraction `c` is bounded below by
`c · T_ext` **by arithmetic**, with no reference to the detector: at `c = 0.99` that floor is
already `19 800`. The MIX curve at `α = 0.01` reads `19 842` against a floor of `19 811`. Those
points are the simulation horizon drawn on a log axis, not the average run length of a mixture
martingale, and a reader who takes the CUSUM and MIX curves as measurements will read a
`2 000×`-conservative `ARL₀` where the experiment measured nothing but `4H`.

**This is a legibility correction and it falsifies nothing.** Because the caption names e-CUSUM
alone, every printed claim about panel C survives intact. The repository's own figure
(`results/R09_eprocess_anytime/figures/fig09_anytime_valid.png`) draws the censored arms with
hollow markers on a lighter dashed line, rules the horizon at `4H` and prints the per-arm censoring
range in the legend; the caption below it should say the same thing in words.

## Edit 1 — Figure 9 caption L559, qualify panel C

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 559** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`). It is disjoint from the strings the two sibling candidates search.
Verify once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
e-CUSUM satisfies $\mathrm{ARL}_0 \ge 1/\alpha$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
e-CUSUM satisfies $\mathrm{ARL}_0 \ge 1/\alpha$ (right-censoring below $0.1\%$). The CUSUM and MIX curves are hollow because their run lengths are right-censored at the $4H$ simulation horizon on $65$--$99\%$ of streams: those points are lower bounds pinned to the horizon, not measured run lengths
~~~~~~~~~
>>> FIN DU BLOC

## Action required for the figure

Replace the binary `Fig27_Eprocess_AnytimeValid.png` with the generated artefact
`results/R09_eprocess_anytime/figures/fig09_anytime_valid.png`.

**Grounds.** The submitted panel C draws all three arms as solid lines with filled markers, which
gives the CUSUM and MIX curves the same visual status as the e-CUSUM curve the caption is about.
The replacement marks the censored arms hollow, adds a horizontal rule at `4H = 20 000` labelled
as the right-censoring ceiling, and carries the per-arm censoring range in the legend. **No
numerical value moves on this account**; the register row `ALL-figure-presentation` already covers
the bold lettered panel titles.

## What must not be done with this candidate

**Do not weaken the e-CUSUM claim.** It is the claim the caption makes, it is the one arm whose
`ARL₀` is a measurement, and it holds with a minimum margin of `20.5×` over `1/α` across the level
grid. The edit adds a parenthetical about its censoring only so that the contrast with the hollow
curves is legible.

**Do not report the CUSUM or MIX `ARL₀` as a number in running text.** The repository refuses to
emit a LaTeX macro for any `ARL₀` whose source row is censored above `50%`, and that guard exists
precisely so a censored mean cannot reach the manuscript by a copy-paste. The three
`\RNine...CensoredFracMax` macros are what a camera-ready sentence about panel C should cite.

**Do not extend the horizon to "fix" it.** Removing the censoring on the MIX arm at `α = 0.01`
would require a horizon of order `1/α` times the mixture's own scale, which is not the experiment
v87 describes and not a variant the manuscript contains. The correct response is to say what the
curves are, which is what this edit does.
