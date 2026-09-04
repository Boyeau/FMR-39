# Camera-ready candidate — the four delays of Figure 15B were measured under two onset conventions

| Field               | Value                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                 |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), caption of `fig:multi_detector` |
| Trigger             | Acceptance notification, 14 November 2026                                                 |
| Evidence            | `data/reference/R11/Priorite_12_multi_detector.py` l.308-321; `R11_concept_add_vs_gamma.csv`, three arms |
| Register entry      | `docs/DEVIATIONS.md`, `R11-onset-convention`                                              |
| Cost                | +11 words against the submitted caption                                                   |
| Blocking dependency | none — the claim the caption makes is flatness, and flatness holds                        |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being corrected.** Not a value — all four reproduce — but the fact that the four
values printed side by side are not mutually comparable, because the submitted script gave the
CUSUM one onset convention and the other four detectors another.

`worker_exp_b_h1` builds two streams. The CUSUM receives the post-onset stream alone, with its
statistic at zero:

```python
eps_shifted_only = eps[2000:].copy() + Delta                     # l.308
e_bin_centered = (eps_shifted_only > 0).astype(int) - 0.5         # l.309
al_cusum = strict_cusum(e_bin_centered, 0.1, 10.0)                # l.310
```

while PHT, ADWIN, DDM and EDDM receive the whole stream, warm-up included, with `onset=2000`:

```python
al_pht   = strict_pht(e_bin_full_centered, 0.1, lambda_ph_iid, onset=2000)   # l.318
al_adwin = run_river_detector("ADWIN", e_bin_full, onset=2000, delta=0.002)  # l.319
al_ddm   = run_river_detector("DDM",   e_bin_full, onset=2000)               # l.320
al_eddm  = run_river_detector("EDDM",  e_bin_full, onset=2000)               # l.321
```

The difference is not cosmetic. Under `warmstart` the detector carries 2,000 steps of
pre-onset statistic into the monitored window: `strict_pht` tests
`if m - M > threshold and t >= onset`, so a threshold crossing during warm-up is **not
returned and does not reset the statistic**, and the detector can cross again at `t = onset`
and return a delay of zero. R11 measures how often that happens — the `n_preonset_leak` column,
counted per detector and per grid point — and it is not rare.

**R11 runs all three arms and the finding is the contrast between them.** `reset` and
`warmstart` put every detector on one convention; `as_submitted` reproduces the per-detector
mixture above, and it is the only arm that reproduces the caption's four numerals.

| detector | published | `as_submitted` | its convention there | `reset` | `warmstart` |
| -------- | --------- | -------------- | -------------------- | ------- | ----------- |
| CUSUM    | ≈ 28.3    | see `R11_concept_add_vs_gamma.csv` | `reset`     | —       | —           |
| PHT      | ≈ 27.1    | idem           | `warmstart`          | —       | —           |
| ADWIN    | ≈ 61      | idem           | `warmstart`          | —       | —           |
| DDM      | ≈ 250     | idem           | `warmstart`          | —       | —           |

*(the measured cells are in `docs/sections/R11.md`, which carries the same table filled; this
file states the design fact, not the campaign's numbers)*

**The consequence is quantified.** Placing the CUSUM and the PHT on the *same* convention
reverses their published order, at a separation of many standard errors of the paired,
seed-clustered difference. That does not falsify anything the manuscript says: the caption
asserts flat delays, and the delays are flat; neither the caption nor the body asserts in words
an ordering between detectors. What it establishes is that **a reader who compares the four
numerals is comparing across two conventions**, and nothing in the caption says so.

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` line 627 verbatim and occurs exactly once in the file. Verify once
more before applying.

<<< RECHERCHER
~~~~~~~~~latex
flat delays across CUSUM ($\approx 28.3$), PHT ($\approx 27.1$), ADWIN ($\approx 61$), DDM ($\approx 250$)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
flat delays across CUSUM ($\approx 28.3$; monitored from the onset), PHT ($\approx 27.1$), ADWIN ($\approx 61$), DDM ($\approx 250$; the latter three warm-started on the pre-onset stream, so the delays are not comparable across detectors)
~~~~~~~~~
>>> FIN DU BLOC

**The alternative is to unify the convention rather than to declare it**, which would change all
four numerals and require re-running the campaign. That is a larger edit than a camera-ready
revision usually absorbs, and it is not what this candidate proposes; it is recorded here as the
option the authors may prefer, with `R11_concept_add_vs_gamma.csv` supplying the numbers either
unification would produce.
