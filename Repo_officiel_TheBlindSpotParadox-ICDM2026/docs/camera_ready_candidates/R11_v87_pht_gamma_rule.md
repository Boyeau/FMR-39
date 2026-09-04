# Camera-ready candidate — the PHT's `λ × Γ` rule does not hold the nominal level, it drifts across it

| Field               | Value                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                 |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:fpr_explosion` and the caption of `fig:multi_detector` |
| Trigger             | Acceptance notification, 14 November 2026                                                 |
| Evidence            | `R11_pht_fpr_vs_gamma.csv`, column `FPR_gamma` with its Wilson bounds                     |
| Register entry      | `docs/DEVIATIONS.md`, `R11-pht-gamma-rule`                                                |
| Cost                | +12 words against the submitted clause                                                    |
| Blocking dependency | none — Figure 15A already plots the curve this describes                                  |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being corrected.** The word "same". v87 says the PHT "needs the same `λ × Γ` inflation"
as the CUSUM, and the Figure 15 caption calls it the "same `λ × Γ` cure". The CUSUM's cure is
described a few lines earlier as one that "holds the nominal level". The PHT's does not hold a
level at all — it crosses it.

Measured over the 20-point grid, at 5,000 streams per point, with the `sqrt(2)` inflation that a
threshold calibrated on a finite sample requires (`docs/DEVIATIONS.md` entry 16):

| `Γ` (realised)     | `FPR` at `λ × Γ` | 95% interval          |
| ------------------ | ---------------- | --------------------- |
| 1.174 (ARCH(1) floor) | **14.46%**    | `[13.14%, 15.89%]`    |
| 6.44               | 3.40%            | `[2.76%, 4.19%]`      |
| 50.0               | 2.28%            | `[1.76%, 2.94%]`      |
| 200.0              | **1.62%**        | `[1.19%, 2.19%]`      |

The rate falls monotonically across the grid. It is **2.9× the nominal level** at the lowest
penalty and **3.1× conservative** at the highest, and the two extreme intervals do not overlap,
so the drift is not a sampling artefact. There is no plateau at 5% anywhere.

**The cure works; it is the word "same" that does not.** False alarms *are* controlled — the raw
threshold runs above 80% over the same range — so the qualitative point of `sec:fpr_explosion`
stands. What does not survive is the implication that `λ × Γ` gives the PHT the nominal level the
CUSUM gets. It over-corrects at large `Γ` and under-corrects at the bottom of the grid, which is
what a rule derived for a pure cumulative statistic does to a detector that also subtracts a
running mean.

**This repository has recorded the identical situation once before.** `docs/DEVIATIONS.md`
entry 7 found the StrictCUSUM's i.i.d. level to be 2.0% rather than the 5% the text ascribes to
it, and classified it **D2**: a conservative threshold is a legitimate design choice, and what is
inexact is calling it calibrated to 5%. The same reading applies here, and the same severity, so
this candidate follows that precedent rather than opening a new one. **No figure, table or
theorem depends on the descriptor.**

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` line 171 verbatim and occurs exactly once in the file. Verify once
more before applying.

<<< RECHERCHER
~~~~~~~~~latex
The Page--Hinkley Test (PHT), a cumulative statistic despite its running-mean reference, suffers the same explosion, needs the same $\lambda \times \Gamma$ inflation, and plateaus near $30\%$ under $\sqrt{\Gamma}$ scaling
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
The Page--Hinkley Test (PHT), a cumulative statistic despite its running-mean reference, suffers the same explosion and plateaus near $30\%$ under $\sqrt{\Gamma}$ scaling; the $\lambda \times \Gamma$ inflation contains it throughout but does not hold a fixed level, over-correcting as $\Gamma$ grows
~~~~~~~~~
>>> FIN DU BLOC

**The Figure 15 caption carries the same word and is a second, independent edit**, deliberately
not bundled here: `same $\lambda \times \Gamma$ cure` at line 627. Applying only the body edit
leaves the caption inconsistent with it, so the two should be applied together or not at all —
but they are separate search strings and separate decisions, and this file scopes the minimum
that removes the inexact claim from the running text.
