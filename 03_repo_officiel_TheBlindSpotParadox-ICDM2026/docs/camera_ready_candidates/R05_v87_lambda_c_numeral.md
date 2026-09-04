# Camera-ready candidate — the `lambda_C` numeral, Section "Scaling Validation"

| Field               | Value                                                                          |
| ------------------- | ------------------------------------------------------------------------------ |
| **Status**          | **PARKED — do not apply**                                                      |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:scaling_validation` |
| Trigger             | Acceptance notification only                                                   |
| Evidence            | R05 steps a and b; the three vendored witnesses under `data/reference/R05/`     |
| Register entry      | `docs/DEVIATIONS.md`, entry 9                                                  |
| Cost                | +9 words against the submitted sentence                                        |
| Blocking dependency | none — no figure, table or theorem depends on the numeral                      |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is incomplete: streams R06 onwards may touch the same section, and
applying a correction before the inventory closes guarantees reapplying it later.

**What is being corrected.** A numeral, not a claim. The submitted text states that the
Concept CUSUM was "fixed once and for all, `lambda_C = 10`, `delta_C = 0.1`". Read in
`float_precision='round_trip'`, the numeral 10 matches no campaign of the submitted study:

| Campaign                                          | `mon_len` | `lambda_star_Concept` | realised FPR |
| ------------------------------------------------- | --------- | --------------------- | ------------ |
| `protocol_17a` (abrupt, Figure 5A)                | 5,000     | **10.8**              | 0.095        |
| `protocol_18b` 2e5 (ramps, Figure 5B)             | 200,000   | **15.81**             | 0.0525       |
| `protocol_18b` 3e6 (ramps, Appendix B boundary)   | 3,000,000 | **19.02**             | 0.055        |
| `protocol_18a` (retired before submission)        | —         | **13.6**              | 0.030        |

The threshold was calibrated per horizon, exactly as the Data arm's `lambda_iid_H` was
(129.48 at `H = 2e5`, 303.02 at `H = 3e6`). `delta_C = 0.1` is correct and is not touched.

**The substance of the sentence is exact and must be preserved.** `lambda_star_Concept` is
rigorously constant *within* each campaign — one value across the thirteen penalties of the
abrupt grid, one across the sixty rows of the 2e5 ramp grid, one across the eighty-five rows
of the 3e6 grid — while `lambda_star_Data` runs from 43.9 to 847.7 on the same rows. "Fixed
once and for all" is true in the sense that carries Proposition `prop:orthogonality`: the
Concept threshold requires **no recalibration in `Gamma`**, where the Data arm requires one of
a factor of nineteen. Only the numeral is wrong, and it should be replaced rather than
removed.

**A second observation, in the manuscript's favour.** Correcting the seed derivation to
128-bit entropy moves the regenerated abrupt-campaign threshold to **`lambda_star_Concept =
11.4`**, which is precisely the value v87 names elsewhere, in the paragraph "What ``exact''
means here": *"the levels bracketing 5% are 5.03% at `lambda = 11.2` and 4.29% at
`lambda = 11.4`; we take the nearest attainable level at or below nominal,
`lambda_star = 11.4`."* The submitted campaign's 10.8 was inconsistent with the manuscript's
own attainable-level analysis; the corrected campaign is not. The realised hold-out level
moves from 9.5% to 5.5% accordingly. This is an argument for the correction, not against the
paper.

**Verification of the search string.** Unlike the R03 candidate, the frozen `.tex` *was*
available to the run that produced this file, and the block below is quoted from
`articleB_whitening_v87.tex` line 270 verbatim. No reconstruction was needed. Verify once
more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
the \textsc{Concept} CUSUM fixed once and for all, $\lambda_C = 10$, $\delta_C = 0.1$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
the \textsc{Concept} CUSUM threshold fixed with respect to $\Gamma$ and calibrated once per horizon ($\lambda_C = 11.4$ at $H = 5{,}000$, $\delta_C = 0.1$)
~~~~~~~~~
>>> FIN DU BLOC

**If a fuller correction is wanted**, the Appendix B sentence that reports the ramp campaigns
could carry the two remaining values, since it is the passage where the horizon dependence is
already the subject. That is a second, independent edit and is deliberately not bundled here:
the block above is the minimum that removes a false numeral without touching a claim.
