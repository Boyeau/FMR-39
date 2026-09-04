# Camera-ready candidate — the boundary convention is declared but its effect on the headline is never reported

| Field               | Value                                                                                            |
| ------------------- | -------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                        |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `app:repro` L392                    |
| Trigger             | Acceptance notification, 14 November 2026                                                        |
| Evidence            | `results/R16_regime_census/data/R16_boundary_convention_delta.csv`                               |
| Register entry      | `docs/DEVIATIONS.md`, `R16-boundary-sensitivity` — Class A, no severity                          |
| Cost                | +25 words at the end of one appendix sentence; no number in the body text changes                |
| Blocking dependency | none — the edit adds a measurement and removes no claim                                          |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed: streams after R16 may touch the same sentence, and applying a
correction before the inventory closes guarantees reapplying it later.

**What is being corrected.** Nothing is wrong. v87 declares the convention at L392, states its
mechanism correctly, and cites the right example. What is missing is the size of the effect on
the number the paper is most cited for.

The manuscript's most-cited claim, `53` of `66` phases out of budget (`80\%`), is computed under
the post-onset convention L392 declares. Under the inclusive convention — the turning-point
return counted in both adjacent phases — the same census gives `56` of `66` (`84.8\%`). Three
phases of the sixty-six change detectability, and **all three change in the same direction**:

| ticker | phase                     | Sharpe, inclusive → post-onset | floor, inclusive → post-onset | detectable   |
| ------ | ------------------------- | ------------------------------ | ----------------------------- | ------------ |
| PFF    | 2011-08-08 → 2013-05-08   | `1.0254 → 1.9800`              | `1435.8 → 385.1`              | no → **yes** |
| PFF    | 2020-03-18 → 2021-12-31   | `0.9132 → 1.9046`              | `1810.7 → 416.2`              | no → **yes** |
| BWX    | 2020-03-18 → 2021-01-05   | `1.8179 → 3.1323`              | `456.9 → 153.9`               | no → **yes** |

Because every flip runs one way, the count's convention envelope is `[53, 56]` and the published
figure is its **conservative end**: the sensitivity can only strengthen the claim, never weaken
it. That is worth one sentence, and it is the sentence the appendix is missing.

Two of the three flips are the 2020-03-18 turning point itself, which is the example L392
already cites — so the flip count is not an unrelated statistic but the quantification of the
example the paragraph is built around.

**The direction of the correction runs against the thesis, and the manuscript's own text has it
right.** The `R16` prompt's section 2.1 asserts that counting the turning-point return twice
"gonfle le Sharpe … donc augmente la fraction détectable et diminue le 80 % publié". Measured,
the inclusive convention gives `56/66` (`84.8\%`) and the post-onset one `53/66` (`80.3\%`): the
defect *inflated* the published fraction and the correction *lowered* it. v87 L392 states the
mechanism correctly — the trough return is a large negative outlier that depresses the mean and
inflates the variance of the phase that follows, biasing its floor **upward** — and the
correction the manuscript adopted therefore runs against its own headline. Nothing in this
candidate is needed to fix that; it is stated here because the effect is the one being reported.

## Edit 1 — `app:repro`, the end of the boundary-convention sentence

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 392** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`). Verify once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
that both depresses the mean and inflates the variance of the phase that follows, biasing its floor upward.
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
that both depresses the mean and inflates the variance of the phase that follows, biasing its floor upward. Three of the $66$ census phases change detectability with this convention, all three in the same direction, so the published count of $53$ is the conservative end of the interval $[53, 56]$ that the two conventions bracket.
~~~~~~~~~
>>> FIN DU BLOC

The addition states the count, its direction and the resulting interval, and places the
published figure inside it. It is a measurement of the convention the sentence already declares,
so nothing in the body of the paper needs to move with it.

## What must not be done with this candidate

The interval `[53, 56]` brackets **the convention only**. It is not a confidence interval, not a
sensitivity envelope over the dating, and not an uncertainty on the census. The dating is by far
the larger source of movement in the same count — `docs/DEVIATIONS.md` `R16-dating-misdescription`
and `R16-substitution-scope` record `48` phases with `38` out of budget under strict
Pagan–Sossounov and `102` with `75` under a consistently applied substitution — and this
sentence must not be read as bounding that. Any camera-ready text derived from this file
inherits that limit, which `docs/sections/R16.md` states.
