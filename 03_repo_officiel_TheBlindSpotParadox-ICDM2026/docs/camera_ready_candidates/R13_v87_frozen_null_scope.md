# Camera-ready candidate — "a bootstrap null freezing the same volatility path" describes one arm of one axis

| Field               | Value                                                                                            |
| ------------------- | -------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                        |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:real_world` L331               |
| Trigger             | Acceptance notification, 14 November 2026                                                        |
| Evidence            | `results/R13_oracle_ceiling/data/R13_oracle_diagnostics.csv` (`sigma_path_sha256`), control C4 in `logs/R13_oracle_ceiling/exp_R13_oracle_ceiling_a.log` |
| Register entry      | `docs/DEVIATIONS.md`, `R13-frozen-null-scope` — Class A, no severity                             |
| Cost                | +19 words in one clause; no number changes                                                       |
| Blocking dependency | shares L331 with `R13_v87_operating_points.md` and `R13_v87_covid_delay_numerals.md`; the three search strings are **disjoint** and the three edits commute |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being corrected.** The clause is true of what it literally names and is read as being
true of two further things it does not name. Both are measured by control C4 rather than argued.

**The freeze is real, and R13 asserts it.** The `σ_t` vector that multiplies the resampled
innovations under H₀ is byte-identical to the one that divides the observed returns under H₁:
`R13_oracle_diagnostics.csv` carries a SHA-256 of that vector on each of the twelve (episode,
oracle) pairs, taken on its IEEE-754 bytes, and the campaign stops if the two ever differ. The
caption of Figure 14 is therefore accurate as a description of what the false-alarm axis is.

**First limit: on the standardized-mean arm the frozen path cancels.** The `H₀` increment of the
standardized-mean CUSUM is

    sign(Δ) · (μ₀ + σ_t Z* − μ₀) / σ_t  =  sign(Δ) · Z*,

so the volatility path drops out of the null increment altogether and `FPR_H` on that arm is a
property of the resampled innovations alone. Freezing it, redrawing it, or replacing it by a
constant would give the same false-alarm axis. The freeze binds only on the **likelihood-ratio**
arm, where `σ_t` enters squared and does not cancel — which is the arm the `3`-day figure comes
from, so the sentence's own headline number is on the right side of the distinction. What the
clause does not convey is that the *other* number in the same sentence, the `16`-day
standardized-mean delay, is read against a null the freeze does not touch.

**Second limit: the null that selects the threshold is not frozen.** Both delays L331 prints are
read at `OP2b_ARL0_252`, whose threshold is chosen as the first `λ` whose in-control average run
length reaches 252 trading days. That average is taken over **5 000 regenerated GARCH paths**,
simulated forward from the fitted `(ω̂, α̂, β̂)` after a 500-step burn-in. It is a parametric
null, not a frozen-path one, and it is the null that fixes the operating point behind every
numeral of the sentence. The frozen-path null fixes the horizontal axis of Figure 14 and nothing
else.

Neither limit falsifies anything. The correction is one clause, and it makes the sentence
describe the experiment the repository runs.

## Edit 1 — `sec:real_world` L331, qualify the null

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 331** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`). It is disjoint from the strings the two sibling candidates search.
Verify once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
against a bootstrap null freezing the same volatility path
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
against a bootstrap null freezing the same volatility path, which binds on the likelihood-ratio increments and cancels on the standardized-mean ones; the threshold itself is calibrated on a parametric null regenerated from the fitted GARCH parameters
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**This is not a claim that the frozen null is wrong.** It is the null the caption describes, it is
implemented as described, and control C4 asserts the identity of the two `σ_t` vectors on every
episode and every oracle. What is corrected is the *reach* of the description.

**The cancellation is algebraic, not numerical.** In float64,
`(μ₀ + σ_t Z* − μ₀) / σ_t` differs from `Z*` by rounding; the campaign measures that residual per
episode and logs it, and it is of the order of `1e-16` relative. No camera-ready text may say the
two are bit-identical.

**Nothing here bears on the `10.6×` Jensen ratio.** That quantity has no null in it at all: it is
`Σ Δ²/(2σ_t²)` over the phase divided by the unconditional budget, a deterministic function of the
return series and the oracle fit, and it reproduces the submitted campaign to the last digit.
