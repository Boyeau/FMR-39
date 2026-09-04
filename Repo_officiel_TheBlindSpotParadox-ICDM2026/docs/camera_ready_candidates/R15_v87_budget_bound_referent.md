# Camera-ready candidate — NO DEVIATION, clarification only: the caption's bound is `K_eff`, the figure's reference line is `sqrt(K_eff)`

| Field               | Value                                                                                                                        |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Status**          | **PARKED — do not apply**                                                                                                    |
| Kind                | **NO DEVIATION — clarification only.** The caption's literal reading holds; no register entry is opened.                     |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), Figure 17 caption, `fig:cross_section`                           |
| Trigger             | Acceptance notification, 14 November 2026                                                                                    |
| Evidence            | `results/R15_cross_sectional/data/{R15_panel_diagnostics,R15_cross_sectional_race}.csv`; `logs/R15_cross_sectional/exp_R15_cross_sectional_b.log`, "THE TWO CANDIDATE CEILINGS OF PANEL B, MEASURED" and "THE CAPTION'S `K_eff ~ 3.8` IS 1/rho_hat AND NOT K_eff" |
| Register entry      | **none.** Both printed relations hold.                                                                                       |
| Cost                | +9 words; no number changes                                                                                                  |
| Blocking dependency | shares the caption with `R15_v87_scatter_sign.md` and `R15_v87_scatter_attribution.md`; the three search strings are **disjoint** |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being clarified.** The caption says the realized budget reduction is "bounded by the
effective panel size `K_eff \approx 1/\hat\rho \approx 3.8`". Panel B of the figure draws a
different curve as its reference: the delivered plotting code, line 381, plots
`np.sqrt(df_a['K_eff_meas'])`. Two candidate ceilings, and the regenerated campaign shows that
only one of them is a ceiling.

**The measurement.**

| quantity                                             | value at `K = 97` |
| ---------------------------------------------------- | ------------------ |
| `K_eff_meas`                                          | `3.7370`          |
| `sqrt(K_eff_meas)`                                    | `1.9331`          |
| realized `budget_reduction`, `c = 0.25`, mean `K >= 20` | `2.0299`          |

Over the ten plotted cells at `c = 0.25`, the realized reduction **exceeds** `sqrt(K_eff)` at six
of them (`K = 20, 30, 50, 60, 75, 97`) and **never** exceeds `K_eff` — zero of ten. The caption's
literal statement therefore holds; the reference line the figure actually draws does not bound the
curve it is drawn beside. On the submitted campaign the picture is the same in kind: plateau
`2.0086` against `sqrt(K_eff) = 1.9331`.

**Why the two are not interchangeable, and why neither is an error.** `sqrt(K_eff)` is the natural
scale for a *detection-delay ratio* under a fixed drift, because a CUSUM delay falls like the
inverse squared signal-to-noise; `K_eff` is the ceiling on the *information* pooling recovers. The
delivered figure plots the first as the commensurable comparator and the caption states the
second as the bound. Both are defensible; they are simply not the same line, and a reader who
matches the caption's `3.8` to the black dotted curve at `1.93` will conclude the figure
contradicts its own caption. The regenerated Figure 17 draws **both**, which removes the ambiguity
without changing either claim.

**A second, smaller referent slip in the same clause.** L376 reads "saturates the effective panel
near `1/\hat\rho \approx 3.8`". `1/\hat\rho` on this campaign is `3.8314`, which does round to
`3.8`; the **measured** effective panel size at `K = 97` is `K_eff_meas = 3.7370`, which rounds to
`3.7`. The two are different quantities — `1/\rho` is the `K \to \infty` limit of
`K/(1 + (K-1)\rho)` and `K_eff` is its value at a finite `K` — and the gap between them is the
finite-panel term, not a discrepancy. The caption's `\approx` covers it. It is recorded here so
that a camera-ready that wants to print a measured `K_eff` knows the numeral is `3.7`, not `3.8`.

## Edit 1 — Figure 17 caption, name the reference line the figure draws

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` verbatim and occurs **exactly once** in the file (`grep -Fc` returns
`1`). It is disjoint from the strings the two sibling candidates search.

<<< RECHERCHER
~~~~~~~~~latex
bounded by the effective panel size $K_{\mathrm{eff}} \approx 1/\hat\rho \approx 3.8$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
bounded by the effective panel size $K_{\mathrm{eff}} \approx 1/\hat\rho \approx 3.8$ (measured $3.7$ at $K = 97$); the dotted reference is $\sqrt{K_{\mathrm{eff}}}$, the delay-ratio scale, which the realized curve exceeds
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**Do not delete the `sqrt(K_eff)` line from the figure.** It is the comparator commensurable with
a ratio of delays and it is the delivered script's own choice. What was missing is its name in the
caption, not the line.

**Do not restate the caption's bound as `sqrt(K_eff)`.** That would convert a true statement into
a false one: the realized reduction exceeds `sqrt(K_eff)` at six of ten plotted cells.

**Do not read "exceeds `sqrt(K_eff)`" as evidence of a super-efficient escape.** The plateau is
`2.03` with a delta-method standard error of `0.0499` propagated from design-corrected SEMs, on
seven cells drawn from one panel of 97 assets; it sits between the two candidate ceilings and
far below `K_eff`. The claim L376 makes — a real but small escape, a measured `2x` — is what the
number supports, and nothing more.
