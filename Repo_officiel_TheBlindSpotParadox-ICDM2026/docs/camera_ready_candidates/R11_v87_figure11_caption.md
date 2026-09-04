# Camera-ready candidate — the Figure 11 caption states one panel's parameters for both

| Field               | Value                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                 |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), caption of `fig:data_vs_concept` |
| Trigger             | Acceptance notification, 14 November 2026                                                 |
| Evidence            | `data/reference/R11/Priorite_12_multi_detector.py`, lines 604-613; R11 experiments B and D |
| Register entry      | `docs/DEVIATIONS.md`, entry 19                                                             |
| Cost                | +6 words against the submitted caption                                                    |
| Blocking dependency | none — no number in the body text changes                                                 |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed: streams after R11 may touch the same figure, and applying a
correction before the inventory closes guarantees reapplying it later.

**What is being corrected.** A caption, not a claim. Figure 11 carries two panels produced by two
different calls of the submitted script, at two different drift magnitudes and two different
sample sizes, and the caption states only the first pair:

| Panel | Produced by                                             | drift `c` | streams per point |
| ----- | ------------------------------------------------------- | --------- | ----------------- |
| **A** | `run_experiment_d(n_seeds=1000, ...)`, `Delta = 2.0*σ`  | **2.0**   | **1,000**         |
| **B** | `run_experiment_b(n_seeds=5000, ...)`, `c = 1.5` passed | **1.5**   | **5,000**         |

`plot_figure_20(df_d, df_b)` is called with those two frames at
`Priorite_12_multi_detector.py:613`; `df_b` is the return value of `run_experiment_b`, whose
`tasks_h1` are built with the literal `1.5` at line 337, and whose `n_seeds` is `args.n_seeds_b`,
defaulting to 5000 at line 592. `df_d` comes from `run_experiment_d(n_seeds=1000, ...)` at line
609, with `Delta = 2.0 * sigma_unc` at line 451.

**The manuscript corroborates the correction twice, in its own text.** The body sentence that
Figure 11B illustrates says the delays are measured "under a physical shift ($c=1.5$)", and the
caption of Figure 15 says "Universality of the whitening filter ($c=1.5$)" for the same Concept
campaign. Only the Figure 11 caption carries `c=2` across both panels.

**The claim the caption supports is unaffected.** "Whitened Concept: flat delays for all
detectors" is a statement about panel B, and panel B is the `c=1.5`, 5,000-stream campaign
throughout. What the caption misstates is the parameters a reader would use to reproduce it.

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` line 575 verbatim and occurs exactly once in the file. Verify once
more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
\textbf{The Lethargy Tax vs.\ GARCH immunity} (abrupt drift $c=2$, $1{,}000$ streams per point)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
\textbf{The Lethargy Tax vs.\ GARCH immunity} (\textbf{(A)} abrupt drift $c=2$, $1{,}000$ streams per point; \textbf{(B)} $c=1.5$, $5{,}000$ streams per point)
~~~~~~~~~
>>> FIN DU BLOC

**A second, independent edit is deliberately not bundled here.** The same figure's panel A and
panel B use two different ADWIN implementations under one legend entry — a local prefix-sum
window detector on the `Data` statistic (`delta = 5e-4`, `min_window = 30`) and river's ADWIN on
the `Concept` stream (`delta = 0.002`). That is a separate question about what the figure
compares, not about what its caption says, and it is treated in
`R11_v87_detector_comparability.md`.
