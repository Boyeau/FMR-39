# Camera-ready candidate — NO DEVIATION, clarification only: the caption's composition attribution is confounded with `K`

| Field               | Value                                                                                                                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                                                                                          |
| Kind                | **NO DEVIATION — clarification only.** Nothing printed is contradicted and no register entry is opened.                                                                            |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), Figure 17 caption, `fig:cross_section`                                                                                |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                                                          |
| Evidence            | `results/R15_cross_sectional/data/R15_panel_composition.csv`; `logs/R15_cross_sectional/exp_R15_cross_sectional_b.log`, "THE CAPTION'S ATTRIBUTION IS NOT TESTABLE BY THIS DESIGN" |
| Register entry      | **none.** The caption is not false: compositions do vary along the abscissa.                                                                                                       |
| Cost                | +6 words, or nothing at all                                                                                                                                                        |
| Blocking dependency | shares the caption with `R15_v87_scatter_sign.md` and `R15_v87_budget_bound_referent.md`; the three search strings are **disjoint**                                                |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being clarified.** The caption reads "Point-to-point scatter reflects threshold
variations **across panel compositions**". Two things are named: a *quantity* (threshold
variation) and a *source* (varying panel composition). The first reproduces —
`R15_v87_scatter_sign.md` measures it at `|r| \approx 0.99`. The second is **not testable under
this design**, and the caption should not be read as reporting a measurement of it.

**Why it is not testable.** The delivered script draws **exactly one composition per `K`**:

    cell_seed_base = int(hashlib.md5(f"real_{K}_{MASTER_SEED}".encode()).hexdigest(), 16) % (2**32)
    assets_idx     = np.random.default_rng(cell_seed_base).choice(K_max, size=K, replace=False)

so the ten points of panel B carry ten values of `K` and ten compositions, changing **together**.
Moving one point to the next changes the panel size and the identity of its members at the same
time. The two are confounded by construction, and no contrast in the design holds one fixed while
the other varies. `R15_panel_composition.csv` makes the ten draws inspectable — their mean
pairwise Jaccard overlap is `0.2235`, ranging from `0.0000` (the `K = 1` singleton against `K = 5`)
to `0.7732` — but an overlap statistic is not an identification strategy.

**The caption is nonetheless true as written.** The compositions *do* vary from point to point,
and the threshold *does* vary with them. What the sentence does not — and, on this design, cannot
— establish is that composition rather than panel size is what drives the variation. The
clarification separates a description from a causal attribution.

**No composition-resampling arm is added.** v87 describes none, and the scope filter of this
stream is strictly v87's content. Adding one would answer a question the manuscript does not ask,
with a campaign the manuscript does not report, and its result would then have to be reconciled
with a figure that was drawn without it. The gap is reported instead.

## Edit 1 — Figure 17 caption, mark the attribution as a reading rather than a measurement

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` verbatim and occurs **exactly once** in the file (`grep -Fc` returns
`1`). It is disjoint from the strings the two sibling candidates search.

<<< RECHERCHER
~~~~~~~~~latex
Point-to-point scatter reflects threshold variations across panel compositions
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
Point-to-point scatter tracks threshold variation; panel size and composition change together along the abscissa, so the two are not separated here
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**This is not a correction.** Applying the edit changes no number and withdraws no claim. If the
camera-ready keeps the original sentence, nothing in the manuscript becomes false.

**Do not present the Jaccard overlap as evidence for or against the attribution.** It describes
how much the ten frozen draws share; it says nothing about what causes the scatter.

**Do not use this to argue the frozen composition is a defect.** Freezing it is the correct
treatment of a nuisance draw over *which real series enter the experiment* — the same treatment
R01 gives its four ETFs and R14 its 106 onsets — and it is the only reason four columns of
`R15_panel_diagnostics.csv` are comparable to the submitted campaign at all. What the freeze costs
is exactly this one attribution, and that cost is what this file records.
