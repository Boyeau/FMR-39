# Camera-ready candidate — NO DEVIATION, clarification only: Synthetic Control Evidential Strength, Section "Discussion"

| Field               | Value                                                                                                                                  |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply** <br> *NO DEVIATION — clarification only*                                                                     |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), `sec:discussion`, **line 345**                                            |
| Trigger             | Acceptance notification, 14 November 2026                                                                                              |
| Evidence            | `results/R14_crypto_isofpr/data/R14_crypto_isofpr_race.csv` (Paired bootstrap interval of the `Synth_BTC` mean)                        |
| Register entry      | **none.** The statement is true of the point estimate; §S8 perimeter policy keeps incomplete-but-true formulations out of the register |
| Cost                | one clause; no numeral changes                                                                                                         |
| Blocking dependency | none                                                                                                                                   |

**Why this is not applied now.** The manuscript is under review and cannot be edited.

**What is being clarified — and what is *not* being corrected.**
The text currently claims the quasi-Gaussian synthetic control "inverts the ordering to Eco-L1-faster". This claim is factually true of the point estimate (the regenerated mean is `1.04`). However, the 95% paired bootstrap interval of this mean is `[0.9793, 1.0688]`. Because this interval contains `1` (parity), the evidential weight supporting the inversion is weaker than the categorical formulation implies.

This candidate appends a clarification to acknowledge the overlap with parity without retracting the point estimate finding.

## Edit — `sec:discussion` line 345

**Verification of the search string.** The block below is quoted from `articleB_whitening_v87.tex`
verbatim.

<<< RECHERCHER
~~~~~~~~~latex
inverts the ordering to \textsc{Eco-L1}-faster
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
inverts the point-estimate ordering to \textsc{Eco-L1}-faster, though its $95\%$ interval spans parity
~~~~~~~~~
>>> FIN DU BLOC