# Camera-ready candidate — L308's "0.4 points of rejection" matches no reading of the campaign that produced the figure

| Field               | Value                                                                                                            |
| ------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                        |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), `sec:ar_garch` **L308**                              |
| Trigger             | Acceptance notification, 14 November 2026                                                                        |
| Evidence            | `results/R07_estimated_mean/data/R07_estmean_lb_fpr.csv` and `data/reference/R07/protocol_21a_estmean_lb_fpr.csv` |
| Register entry      | `docs/DEVIATIONS.md`, `R07-dispersion-cost-numeral` — Class A, no severity                                       |
| Cost                | one clause; the sentence gains the quantity it was missing                                                       |
| Blocking dependency | shares L308 with `R07_v87_bias_bound.md`; the two search strings are **disjoint** and the two edits commute      |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being corrected.** L308 reads:

> the dispersion channel, whose RMSE reaches $11.4\%$ of $\sigma_{\mathrm{unc}}$ at $n = 125$,
> **costs at most $0.4$ points of rejection**

The sentence does not name the quantity `0.4` measures — points of *what*, above *what*. The
campaign script enumerates the six readings a reader could plausibly try and logs each. **None
returns `0.4`, in the regenerated campaign or in the submitted witness.**

| reading                                                    | regenerated | witness (`protocol_21a`) |
| ---------------------------------------------------------- | ----------- | ------------------------ |
| max over `φ` of (max OLS − `ORACLE`) at the same `φ`       | `0.71` pt   | `0.62` pt                |
| max OLS anywhere − max `ORACLE` anywhere                    | `0.71` pt   | `0.29` pt                |
| max OLS anywhere − mean `ORACLE` over the grid              | `0.71` pt   | `0.54` pt                |
| max over `φ` of the spread across the four windows          | `0.89` pt   | `0.64` pt                |
| max OLS anywhere − the `5 %` nominal level                  | `0.63` pt   | `0.57` pt                |
| max OLS anywhere − min OLS anywhere                         | `0.93` pt   | `0.96` pt                |

**The numeral is not a casualty of the re-keying.** It is unlocatable in the campaign that produced
the published figure as well as in the regenerated one, which is why the register entry is opened
against the manuscript rather than against the redraw.

**The claim the numeral supports is not in doubt.** Whichever reading is meant, the dispersion
channel costs under one point of Ljung–Box rejection across the whole `7 × 4` grid, against the
`94.9` points the naive arm loses between `φ = 0` and `φ = 0.15`. What is missing is the
definition, and a reader holding `R07_estmean_lb_fpr.csv` cannot reconstruct the number.

## Edit — `sec:ar_garch` L308, name the quantity and state its value

**Verification of the search string.** The block below is quoted from `articleB_whitening_v87.tex`
**line 308** verbatim and occurs **exactly once** in the file (`grep -Fc` returns `1`). It is
disjoint from the string `R07_v87_bias_bound.md` searches in the same sentence. Verify once more
before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
costs at most $0.4$ points of rejection
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
costs at most $0.8$ points of Ljung--Box rejection, measured as the largest gap between a rolling-OLS arm and the oracle arm at the same $\phi$ on the same paths
~~~~~~~~~
>>> FIN DU BLOC

The replacement names the reading (the paired gap against the oracle at matched `φ`), which is the
one the surrounding sentence's "matching the oracle bands on the same paths" already implies, and
states a bound that both the witness (`0.62` pt) and the regenerated campaign (`0.71` pt) respect.

## What must not be done with this candidate

**The `0.4` must not be kept by choosing whichever reading happens to be closest.** The closest
reading in the witness is `0.29` pt and in the regenerated campaign `0.63` pt; neither rounds to
`0.4`, and selecting a definition to fit a printed digit is the same manoeuvre as widening a
tolerance until a test passes.

**`0.8` is a bound, not a measurement to quote.** The per-cell gaps are extrema over a `7 × 4`
grid of correlated cells and have no per-cell sampling distribution; control C9 of R07 supplies the
trajectory-bootstrap law of the envelope, and any camera-ready text that quotes a single gap must
quote that law with it.

**This candidate says nothing about the bias channel.** The neighbouring clause carries its own,
separate correction in `R07_v87_bias_bound.md`, which is a **D3**; merging the two would attach a
falsified bound to a clarification and make the reason for each unreadable.
