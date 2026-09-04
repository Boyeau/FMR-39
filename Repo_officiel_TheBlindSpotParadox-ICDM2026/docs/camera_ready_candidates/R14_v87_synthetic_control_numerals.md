# Camera-ready candidate — L345's three quasi-Gaussian control numerals move under the 128-bit re-keying

| Field               | Value                                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                          |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:misspecification` L345           |
| Trigger             | Acceptance notification, 14 November 2026                                                          |
| Evidence            | `results/R14_crypto_isofpr/data/R14_crypto_isofpr_race.csv`, source `Synth_BTC`                    |
| Register entry      | `docs/DEVIATIONS.md`, `R14-campaign-redraw` — Class A, D2                                          |
| Cost                | three numerals inside one parenthesis; no other number and no claim in the body text changes       |
| Blocking dependency | shares L345 with `R14_v87_reliable_range_scope.md`; the two search strings are **disjoint** and the two edits commute |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The deviation
inventory is not closed: streams after R14 may touch the same sentence, and applying a correction
before the inventory closes guarantees reapplying it later.

**What is being corrected, and what is not.** Only the three numerals of the *synthetic* control.
Every Bitcoin quantity in the same sentence — the `106` onsets, the `4.7\%` iso-FPR, `\hat\nu =
2.78`, `0.74` at `c = 0.35`, parity `1.01` at `c = 1.5`, mean `0.87` — is **bit-identical** to the
submitted campaign and must not be touched. So is the ETH clause.

Preamble §S6 of the repository contract requires the delivered `RandomState(200 / 201)` synthetic
generators to be re-keyed onto a 128-bit `SeedSequence` carrying role and index alone. That redraws
the `t₃₀` series outright:

| L345, the `t₃₀` control      | printed | submitted campaign     | this repository        |
| ---------------------------- | ------- | ---------------------- | ---------------------- |
| lower end of the range       | `0.98`  | `0.9818435754189944`   | `0.9544910179640719`   |
| upper end of the range       | `1.14`  | `1.1426127128069126`   | `1.2384142067139186`   |
| mean over the reliable range | `1.06`  | `1.0603026678597007`   | `1.041041514153539`    |

**The claim the numerals support is unaffected, and the interval says how comfortably.** L345 says
the control "inverts the ordering to \textsc{Eco-L1}-faster". The regenerated mean is above parity,
and a paired moving-block bootstrap over onsets (`B = 2000`, block `24` monthly steps, one
resampled index vector shared by both arms and all seven magnitudes) gives `[0.9793, 1.0688]` — an
interval that still **covers the published `1.06`**. The condition that would have falsified the
inversion, fixed before the run, is that this interval lie entirely below `1`; it does not.

**The cause is established by a counterfactual that was run, not argued.** The repository ships a
`--legacy-seeds` arm that restores the delivered integer seeds and keeps every other change of the
port. It reproduces the submitted campaign on all 88 cells of `ADD`, `DetRate`, `SEM`,
`FPR_achieved` and `add_reliable`, and returns `1.0603026678597007` for the mean. The movement is
the re-keying and nothing else.

## Edit 1 — `sec:misspecification` L345, the three synthetic-control numerals

**Verification of the search string.** The block below is quoted from `articleB_whitening_v87.tex`
**line 345** verbatim and occurs **exactly once** in the file (`grep -Fc` returns `1`). It is
disjoint from the string the sibling candidate searches. Verify once more before applying, as a
matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
inverts the ordering to \textsc{Eco-L1}-faster ($0.98$--$1.14$, mean $1.06$)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
inverts the ordering to \textsc{Eco-L1}-faster ($0.95$--$1.24$, mean $1.04$)
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**This is not a correction of the Bitcoin result.** Every real-BTC numeral of L345 reproduces at
D0. An edit that touched them would introduce an error the repository can refute with one `pandas`
filter on `results/R14_crypto_isofpr/data/R14_crypto_isofpr_race.csv`.

**The range must not be presented as a confidence interval.** `0.95`–`1.24` is the minimum and the
maximum of seven grid points. An extremum over a grid has no stable sampling distribution
(§S4bis, fourth corollary): the two endpoints are descriptive, they are read in the manuscript as
descriptive, and any revision that attached a coverage statement to them would claim more than the
design supports. The mean is the quantity that carries the bootstrap interval.

**No revision may say the two campaigns disagree about the control.** They do not: the published
mean lies inside the regenerated interval. What changed is which draw was taken, and the repository
records both.
