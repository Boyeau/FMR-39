# Camera-ready candidate — Oracle arm analytic crossing, Section "Discussion"

| Field               | Value                                                       |
| ------------------- | ----------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                   |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen) |
| Trigger             | Acceptance notification only                                |
| Evidence            | R04b (measurement of the oracle ratio systematic offset)    |
| Register entry      | `docs/DEVIATIONS.md`, entry `R04b-oracle-ratio-offset`      |
| Blocking dependency | none                                                        |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
KDD 2027 Research Track allocates one additional content page to accepted papers for exactly
this kind of revision, so budget is not the constraint; timing is.

**What is being corrected.** The original text states that the oracle arm crosses "on the analytic prediction". While it crosses near the analytic root, it does not track the prediction; it exhibits a systematic $+5\%$ offset across all twelve grid points. The text is amended to reflect the actual mechanism of intersection.

<<< RECHERCHER
~~~~~~~~~latex
an \emph{oracle} arm standardized by the true GARCH parameters crosses at 4.6, on the analytic prediction, so the extra
~~~~~~~~~
=== REMPLACER PAR >>>
~~~~~~~~~latex
an \emph{oracle} arm standardized by the true GARCH parameters crosses at 4.6 (not strictly on the analytic prediction, but intersecting near it due to a systematic $+5\%$ offset), so the extra
~~~~~~~~~
>>> FIN DU BLOC