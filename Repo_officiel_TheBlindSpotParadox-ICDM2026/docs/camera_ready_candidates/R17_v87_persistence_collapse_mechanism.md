# Camera-ready candidate — NO DEVIATION, clarification only: a third of the persistence collapse is a corner solution at the optimiser's bound

| Field               | Value                                                                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                                                |
|                     | **NO DEVIATION — clarification only**                                                                                                    |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), `sec:misspecification` L341                                                 |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                |
| Evidence            | `results/R17_econometric_baseline/data/R17_warmup_fits.csv`, column `at_lower_bound` at `(250, 0.00)`                                    |
| Register entries    | **none** — no printed claim is contradicted; §S8's scope filter keeps this out of `docs/DEVIATIONS.md`                                   |
| Cost                | +13 words in the body; no number changes                                                                                                 |
| Blocking dependency | shares L341 with `R17_v87_warmup_resolution.md` and `R17_v87_warmup_restoration_scope.md`; search strings are disjoint and edits commute |

**Why this is not applied now.** The manuscript is under review and cannot be edited.

**Nothing here is false.** The persistence does collapse from 0.85 to 0.62 at $n=250$, exactly as L341 states. However, the text attributes the collapse entirely 
to finite-sample estimation variance. The per-fit measurement shows that 29% of the fits at that cell sit exactly on the optimiser's lower bound (`1e-6`, essentially 
zero persistence, no GARCH at all). The collapse is therefore significantly driven by a corner solution of the optimiser.

## Edit — `sec:misspecification` L341, specify the mechanism

**Verification of the search string.** Quoted from `articleB_whitening_v87.tex` **line 341** verbatim; `grep -Fc` returns `1`.

<<< RECHERCHER
~~~~~~~~~latex
on a $250$-step window the estimated persistence collapses to a median $\hat\alpha+\hat\beta = 0.62$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
on a $250$-step window the estimated persistence collapses to a median $\hat\alpha+\hat\beta = 0.62$ (with $29\%$ of fits falling to a corner solution of zero)
~~~~~~~~~
>>> FIN DU BLOC