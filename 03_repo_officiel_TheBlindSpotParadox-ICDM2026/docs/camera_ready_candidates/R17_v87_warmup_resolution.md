# Camera-ready candidate — NO DEVIATION, clarification only: the two numerals of L341 are read at 200 streams, and the sign envelope is a min–max over four cells

| Field               | Value                                                                                                                                                                                                                                      |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Status**          | **PARKED — do not apply**                                                                                                                                                                                                                  |
|                     | **NO DEVIATION — clarification only**                                                                                                                                                                                                      |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), `sec:misspecification` L341                                                                                                                                                   |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                                                                                                                  |
| Evidence            | `results/R17_econometric_baseline/data/R17_warmup_sensitivity.csv` (`FPR_Eco`, `FPR_ML` and their Wilson bounds, `n_streams`); witness `data/reference/R17/protocol_3d_warmup_sensitivity.csv`; `Priorite_6_econometric_baseline.py` l.515 |
| Register entries    | **none** — no printed value is contradicted by the resolution statement; §S8's scope filter keeps this out of `docs/DEVIATIONS.md`                                                                                                         |
| Cost                | +14 words in the body; no number changes                                                                                                                                                                                                   |
| Blocking dependency | shares L341 with `R17_v87_warmup_restoration_scope.md`; the two search strings are **disjoint** and the two edits commute                                                                                                                  |

**Why this is not applied now.** The manuscript is under review and cannot be edited.

**Nothing here is false.** `9.5 %` is exactly what the submitted campaign measured, and `3`–`8 %` is
exactly the span of its four sign-arm cells. What the sentence omits is the sample behind each: both
are read on **200 streams per cell**, which fixes their resolution at half a point and makes the
envelope a min–max over four readings rather than a range with a sampling distribution of its own.

**The resolution of `9.5 %`.** `__main__` passes `n_str = 200` to `protocol_3d_warmup_sensitivity`
(`Priorite_6_econometric_baseline.py` l.515), so the rate can only take the values `k/200`. The
numeral `9.5 %` is `19/200`, and it is the only value in the neighbourhood the design can produce:
the lattice runs `9.0 %`, `9.5 %`, `10.0 %`. Its 95 % Wilson interval at that count is
**`[6.2 %, 14.4 %]`**, which contains the `5 %` nominal level as well as the `3.0 %` the same
sentence quotes at `n = 500`. The interval is what "nearly doubles" is measured against; the point
is what the sentence prints.

**The `3`–`8 %` envelope is an extremum over a grid.** `protocol_3d` reports eight cells, and its
sign column takes four values across them: `7.5 %`, `3.0 %`, `5.5 %`, `8.0 %` in the submitted
campaign. Preamble §S4bis's fourth corollary is explicit that a min or a max over `m` points is an
extremum statistic with no stable sampling distribution, and reading four 95 % cell intervals as one
simultaneous statement would trigger with probability `1 − 0.95⁴ = 18.6 %` under its own null. The
regenerated campaign carries the envelope with a paired stream bootstrap over the 200 stream indices
— `[5.5 %, 13.0 %]` around its minimum and `[7.5 %, 15.5 %]` around its maximum — and gates nothing
on it. **The invariance the sentence asserts is tested instead by a statistic that has a
distribution:** a weighted least-squares slope of the rate on `log(n_warmup)`, binomial weights at
200 streams, whose paired-bootstrap interval `[−0.0153, +0.0195]` covers zero at `p = 0.84`.

**The eight cells hold four readings, not eight.** `simulate_gjr11` draws its whole innovation
vector before the variance recursion and every conditional variance is strictly positive, so
`sign(ε_t) = sign(z_t)` exactly and the monitored binary stream carries no process parameter. The
two `gamma_lev` of a warm-up length therefore read the **same** stream — the regenerated campaign
asserts it by SHA-256 — and the submitted campaign exhibits the same identity in its own table:
`FPR_ML` is equal at the two leverage settings for every warm-up length (`0.075/0.075`,
`0.030/0.030`, `0.055/0.055`, `0.080/0.080`). A mean over the eight cells carries a Kish design
effect of exactly `2.0`.

## Edit 1 — `sec:misspecification` L341, give the false-alarm numeral its resolution

**Verification of the search string.** Quoted from **line 341** verbatim; `grep -Fc` returns `1`,
and it is disjoint from Edit 2 and from the string `R17_v87_warmup_restoration_scope.md` searches on
the same line.

<<< RECHERCHER
~~~~~~~~~latex
the FPR nearly doubles to $9.5\%$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
the FPR nearly doubles to $9.5\%$ ($19/200$ streams, Wilson $[6.2, 14.4]\%$)
~~~~~~~~~
>>> FIN DU BLOC

## Edit 2 — `sec:misspecification` L341, say what the sign envelope is a min–max over

**Verification of the search string.** Quoted from **line 341** verbatim; `grep -Fc` returns `1`,
and disjoint from Edit 1.

<<< RECHERCHER
~~~~~~~~~latex
(measured FPR $3$--$8\%$ across all warm-up lengths)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
(measured FPR $3$--$8\%$, the range of four warm-up lengths at $200$ streams each)
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**This candidate opens no register entry and must not acquire one.** The resolution statement
contradicts nothing printed: it names the sample behind two numerals the sentence gives without one.
Preamble §S8 admits exactly this kind of clarification on the condition that it carries no register
row, and the displacement of the numerals themselves is a separate matter carried by
`R17-campaign-redraw`.

**The envelope must not be re-presented as an interval.** A min–max over four cells is not a
confidence statement, and substituting a bootstrap envelope for the printed range would replace one
descriptive object by another without saying which is which. If a revision wants an inferential
statement about warm-up independence, the slope and its interval are the object to quote, not the
extrema.

**No revision may claim the four cells are four independent measurements.** They are read on the
same 200 streams over evaluation windows that overlap by 65 % to 95 %, which is why the envelope and
the slope both carry a **paired** bootstrap over stream indices and not a binomial one.
