# Camera-ready candidate — StrictCUSUM nominal level, Section "FPR explosion"

| Field               | Value                                                           |
| ------------------- | --------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                       |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen)     |
| Trigger             | Acceptance notification only                                    |
| Evidence            | R03 i.i.d. calibration arm (300 streams at `Gamma = 1` exactly) |
| Register entry      | `docs/DEVIATIONS.md`, entry 7                                   |
| Cost                | +0 words against the submitted sentence                         |
| Blocking dependency | none — no figure, table or theorem depends on the descriptor    |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is incomplete: streams R04 onwards may touch the same sentence, and
applying a correction before the inventory closes guarantees reapplying it later.

**What is being corrected.** Not a measured quantity and not a conclusion: the descriptor
attached to the StrictCUSUM threshold. The submitted text presents `lambda_iid = 65` as
calibrating the detector to a 5% nominal level under i.i.d. noise. A dedicated arm at
`Gamma = 1` exactly (`alpha = beta = 0`, 300 streams of 5000 steps, same innovations, same
standardisation chain, same threshold) measures **2.0%**, 95% Wilson interval **[0.9%, 4.3%]**,
which excludes 5%. The same arm measures **5.0%** for the ADWIN-like detector, Wilson
[3.1%, 8.1%], so the description is accurate for the window-mean detector and inaccurate only
for the CUSUM.

No output of the submitted campaign could have caught this: its lowest grid point sits at
`Gamma = 1.174` with `alpha = 0.08`, which is an ARCH(1) stream, not an i.i.d. one.

**The claim is unaffected and slightly strengthened.** `lambda_iid = 65` is a conservative
threshold, which is a legitimate design choice. A conservative i.i.d. level means the
explosion documented in the section starts from 2.0% and reaches 80.7% on average beyond
`Gamma = 20`, a wider excursion than the submitted wording implies.

**Caution on the search block.** The frozen `.tex` was not available to the run that produced
this candidate, so the LaTeX below is reconstructed from the sentence as quoted in the R03
experiment brief. **Verify the exact source string against `articleB_whitening_v87.tex` before
applying.**

**Verified against the frozen source.** The search block below is the literal text of
`articleB_whitening_v87.tex` line 171, read from the manuscript, not reconstructed. Note the
wording is "a nominal $5\%$ under IID noise", and that the sentence closes with "ADWIN behaves
similarly" — which the R03 i.i.d. arm supports for the explosion but not for the calibration:
at `Gamma = 1.0` exact, ADWIN realises 5.0% (15/300, Wilson [3.1, 8.1]%) while the StrictCUSUM
realises 2.0% (6/300, Wilson [0.9, 4.3]%, excluding 5%).

<<< RECHERCHER
~~~~~~~~~latex
a StrictCUSUM calibrated to a nominal $5\%$ under IID noise fires close to or above $80\%$ once $\Gamma > 20$; ADWIN behaves similarly.
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
a StrictCUSUM whose threshold holds a $2.0\%$ level under i.i.d.\ noise ($95\%$ Wilson $[0.9, 4.3]\%$) fires at close to $80\%$ or above once $\Gamma > 20$
~~~~~~~~~
>>> FIN DU BLOC
