# Camera-ready candidate — the Figure 17 caption's `r \ge 0.99` holds under neither sign convention

| Field               | Value                                                                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                                                |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), Figure 17 caption, `fig:cross_section`                                       |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                |
| Evidence            | `results/R15_cross_sectional/data/R15_scatter_correlation.csv`; `logs/R15_cross_sectional/exp_R15_cross_sectional_b.log`, "THE CAPTION'S INEQUALITY, EVALUATED AS PRINTED" |
| Register entry      | `docs/DEVIATIONS.md`, `R15-scatter-sign` — Class A, **D2**                                                                                |
| Cost                | +14 words in one parenthetical; one printed relation changes                                                                             |
| Blocking dependency | shares the caption with `R15_v87_scatter_attribution.md` and `R15_v87_budget_bound_referent.md`; the three search strings are **disjoint** and the three edits commute |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being corrected.** The caption prints a *relation*, not a value: `r \ge 0.99`. The
relation is false on both campaigns, and it is false for a mechanical reason that the correction
should state rather than hide.

**The measurement.** Neither witness script computes a correlation, so R15 defines one and fixes
its referent on the text. "With bootstrap threshold" names `lambda_boot`; "scatter" names panel
B's ordinate, which the delivered plotting code (line 378) fixes as `budget_reduction` at
`c = C_GRID[1] = 0.25`, one curve and no other. Pearson `r` between those two over the ten `K`:

| campaign                          | `r` at `c = 0.25` | `|r|`    | `r \ge 0.99` | `|r| \ge 0.99` |
| --------------------------------- | ----------------- | -------- | ------------ | -------------- |
| submitted (`protocol_25d`)        | `-0.9894`         | `0.9894` | false        | **false**      |
| regenerated (`R15_...race.csv`)   | `-0.9962`         | `0.9962` | false        | true           |

The sign is negative at **every** magnitude on the grid — `-0.9907`, `-0.9962`, `-0.9912`,
`-0.9896`, `-0.9876` at `c = 0.10, 0.25, 0.50, 0.75, 1.0` — so it is a property of the mechanism
and not of the one magnitude the figure draws.

**Why the sign is negative.** `budget_reduction` is `ADD_single / ADD_K`. A larger bootstrap
threshold makes the pooled monitor slower, which *lengthens* `ADD_K` and therefore *shrinks* the
ratio. `r` between a ratio and the quantity in its denominator is negative by construction. The
positive reading the caption's sign suggests belongs to a different pair: `r` between `ADD_K`
itself and `lambda_boot` is `+0.9931` regenerated and `+0.9947` on the witness. Both readings are
persisted in `R15_scatter_correlation.csv`; the first was selected on the textual referent — panel
B's ordinate — before either value was compared to the caption, and that ordering is recorded in
`docs/audits/AUDIT_R15.md` §4.

**Why `|r| \approx 0.99` and not `|r| \ge 0.99`.** The absolute bound holds on the regenerated
campaign (`0.9962`) and **fails** on the submitted one (`0.9894`). A camera-ready text that
printed `|r| \ge 0.99` would be true of this repository and false of the campaign the manuscript
reports. `\approx` is the only form both support.

**What does not change.** The qualitative content of the clause — the point-to-point scatter of
panel B is almost entirely explained by variation in the bootstrap threshold — holds on both
campaigns at `|r| \approx 0.99`. Nothing about the escape, the plateau or the effective panel size
depends on the sign.

## Edit 1 — Figure 17 caption, correct the printed relation

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` verbatim and occurs **exactly once** in the file (`grep -Fc` returns
`1`). It is disjoint from the strings the two sibling candidates search. Verify once more before
applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
($r \ge 0.99$ with bootstrap threshold)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
($|r| \approx 0.99$ against the bootstrap threshold; the sign is negative, a higher threshold lengthening the pooled delay and so shrinking the ratio)
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**Do not drop the sign and print `|r|` alone.** The reason the coefficient is negative is the
definition of the ordinate, and a reader who is told only the magnitude has to rediscover it.

**Do not print `-0.99` as a value.** The caption states a bound over a scatter, not a point
estimate, and the two campaigns give `-0.9894` and `-0.9962`. `\approx 0.99` on the magnitude
covers both; a signed numeral would have to be re-derived for whichever campaign the camera-ready
prints.

**Do not read this as a failure of panel B.** The correlation is a *description of the scatter*,
which is what the caption uses it for. Its strength is what the sentence claims and its strength
reproduces.

**Do not conflate this with the attribution clause in the same sentence.** Whether the scatter is
caused by *panel composition* is a separate question that this design cannot answer;
`R15_v87_scatter_attribution.md` handles it and opens no register entry.
