# Camera-ready candidate — L308 states a bound on the estimator bias that the campaign does not respect

| Field               | Value                                                                                                            |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                        |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), `sec:ar_garch` **L308**                             |
| Trigger             | Acceptance notification, 14 November 2026                                                                        |
| Evidence            | `results/R07_estimated_mean/data/R07_estmean_diagnostics.csv`, row `phi = 0.15, n_ols = 125`                     |
| Register entry      | `docs/DEVIATIONS.md`, `R07-bias-bound-not-a-bound` — Class A, **D2**                                             |
| Cost                | one numeral in one clause; no other number in the body text changes                                              |
| Blocking dependency | shares L308 with `R07_v87_dispersion_cost.md`; the two search strings are **disjoint** and the two edits commute |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed: streams after R07 may touch the same sentence, and applying a
correction before the inventory closes guarantees reapplying it later.

**What is being corrected.** L308 states a **bound** that the regenerated campaign violates:

> the systematic one, the classical small-sample AR bias $\mathbb{E}[\hat{\phi}] - \phi \approx
> -2.5\,\phi/n$, **stays under $2.9 \times 10^{-3}$**

| quantity                                                | value                   |
| ------------------------------------------------------- | ----------------------- |
| printed bound                                           | `2.9 × 10⁻³`            |
| largest \|`E[φ̂] − φ`\|, regenerated, at (`0.15`, `125`) | **`3.1269 × 10⁻³`**     |
| its standard error over 10 000 trajectories             | `1.5755 × 10⁻⁴`         |
| distance past the printed bound                         | `+1.44` standard errors |
| `−2.5 φ/n` at the same grid corner, v87's own formula   | `−3.0 × 10⁻³`           |
| distance from that prediction                           | `+0.81` standard errors |
| the submitted campaign's own witness at the same cell   | `2.8697 × 10⁻³`         |

Three things make this a wording problem and not a modelling problem.

1. **The maximum is where the printed formula says it should be.** `−2.5 φ/n` is largest at the
   largest `φ` and the shortest window; that is exactly the cell the maximum occupies. The
   extremum is structurally determined, so it carries the standard error of its own cell and not
   the law of a maximum over 28 correlated cells.
2. **The printed formula already exceeds the printed bound.** `−2.5 × 0.15 / 125 = −3.0 × 10⁻³`,
   which is larger in magnitude than the `2.9 × 10⁻³` written eleven words later. The sentence
   contradicts itself at its own grid corner, independently of any campaign.
3. **The bound is a Monte-Carlo realisation.** The submitted campaign measured `2.8697 × 10⁻³`
   there — `0.19` standard errors below the bound — and the delivered script's certification block
   gated on `max_bias < 2.9e-3`, a literal read off the output it had just produced.

**What is *not* being corrected.** The claim the sentence carries — that the systematic channel is
small, and that calibration depends on estimator *bias* rather than dispersion — is untouched.
`3.1 × 10⁻³` is three orders of magnitude below the momentum coefficients being estimated, Figure 7
panel B is unaffected, and every rolling-OLS arm still matches oracle false-alarm control.

## Edit — `sec:ar_garch` L308, state the bound the formula supports

**Verification of the search string.** The block below is quoted from `articleB_whitening_v87.tex`
**line 308** verbatim and occurs **exactly once** in the file (`grep -Fc` returns `1`). It is
disjoint from the string `R07_v87_dispersion_cost.md` searches in the same sentence. Verify once
more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
stays under $2.9 \times 10^{-3}$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
which predicts $3.0 \times 10^{-3}$ at the grid's worst corner ($\phi = 0.15$, $n = 125$), where we measure $3.1 \times 10^{-3}$
~~~~~~~~~
>>> FIN DU BLOC

The replacement does three things at once: it states a bound the campaign respects, it names the
cell that attains it, and it ties the measured value to the approximation printed beside it rather
than leaving the two silently inconsistent.

## What must not be done with this candidate

**The bound must not be restored by narrowing the grid.** `n = 125` and `φ = 0.15` are corners of
the `7 × 4` grid L308 itself announces ("across the full $7 \times 4$ grid … $n \in \{125, 250,
500, 1000\}$"). Dropping the corner to recover `2.9 × 10⁻³` would be selection on the outcome of a
control, which preamble §S4.10 bans outright.

**The bound must not be widened to a round number that the next redraw also exceeds.**
`3.2 × 10⁻³` is the observed maximum rounded up at the manuscript's own printing precision, and the
approximation predicts `3.0 × 10⁻³` at that corner; any future campaign that exceeds `3.2 × 10⁻³`
by more than a standard error is a finding about the estimator, not a licence to widen again.

**This is not a correction of the `−2.5 φ/n` approximation.** R07 measures the bias; it does not
test the constant `2.5`, and no camera-ready text derived from this file may claim it does.
