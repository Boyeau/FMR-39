# Camera-ready candidate — L290's realized skewness moves from −1.44 to −1.43

| Field               | Value                                                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                                |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), `sec:validity_map` **line 290**                              |
| Trigger             | Acceptance notification, 14 November 2026                                                                                |
| Evidence            | `results/R10_skew_robustness/data/R10_skew_diagnostics.csv`, row `xi = 0.5`, columns `skewness` and `skewness_se`        |
| Register entry      | `docs/DEVIATIONS.md`, `R10-campaign-redraw` — Class A, **D2**                                                             |
| Cost                | one numeral in one parenthesis                                                                                           |
| Blocking dependency | line 290 also carries `$q \approx 0.58$` and `${\approx}97\%$`, and **neither moves**; the search string below touches only the skewness |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being corrected.** L290 prints the realized skewness of the innovations at the extreme
grid point:

> conditional asymmetry is benign but not free: skew-$t$ innovations (**realized skewness to
> $-1.44$**) leave conditional independence intact yet shift the null rate to $q \approx 0.58$,
> making a fixed-$1/2$ CUSUM fire at ${\approx}97\%$

The mandated 128-bit re-keying (preamble §S6) redraws all 4 000 streams. The realized skewness is
the mean of `scipy.stats.skew(z)` over the 1 000 streams at `xi = 0.5`:

| quantity                                    | value                       |
| ------------------------------------------- | --------------------------- |
| printed                                     | `-1.44`                     |
| regenerated, mean over 1 000 streams        | **`-1.4279594830035083`**   |
| its standard error (design effect `1.0`)    | `4.36 × 10⁻³`               |
| distance, in standard errors of one campaign| `+2.76`                     |
| distance, in standard errors of the difference between two campaigns | **`+1.95`** |

**The second reading is the one a comparison of two campaigns supports.** The printed value is
itself one Monte-Carlo realisation of the same design, so the standard error of the difference is
`sqrt(2)` times the standard error of either. At `1.95` standard errors the two campaigns are two
ordinary draws, and this candidate does not claim the submitted numeral was wrong.

**The two other numerals of the same sentence do not move at v87's printing precision.**

| L290 numeral                        | printed | regenerated | at printed precision |
| ----------------------------------- | ------- | ----------- | -------------------- |
| `q \approx 0.58`                    | `0.58`  | `0.582191`  | unchanged — **D1**   |
| fixed-`1/2` CUSUM fires at `≈97\%`  | `0.97`  | `0.966`     | unchanged — **D1**   |
| realized skewness                   | `-1.44` | `-1.42796`  | **moves — D2**       |

**Nothing qualitative moves.** The sentence's claim — conditional asymmetry leaves conditional
independence intact while displacing the marginal rate — holds at every grid point: the two
Ljung–Box arms stay within `4.6`–`6.3 %` of the `5 %` nominal across the whole `xi` grid while the
fixed-`1/2` false-alarm rate climbs monotonically from `0.5 %` to `96.6 %`.

## Edit — `sec:validity_map` line 290

**Verification of the search string.** The block below is quoted from `articleB_whitening_v87.tex`
**line 290** verbatim and occurs **exactly once** in the file (`grep -Fc` returns `1`). It is
disjoint from `shift the null rate to $q \approx 0.58$` and from
`making a fixed-$1/2$ CUSUM fire at ${\approx}97\%$`, neither of which this candidate touches.
Verify once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
realized skewness to $-1.44$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
realized skewness to $-1.43$
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**The numeral must not be read as a property of the Fernández–Steel law at `xi = 0.5`.** It is the
realized skewness of a finite sample of 8 000 draws, averaged over 1 000 streams; the population
skewness of the standardized law is a different quantity and R10 does not compute it.

**The direction of the change must not be attributed to a mechanism.** `-1.44 → -1.43` is a
`1.95`-standard-error move between two draws of the same design. No mechanism is identified and
none is asserted.

**No tolerance was widened and no seed was chosen.** The re-keying is required by the
specification, was fixed before the campaign ran, and the movement was classified afterwards.
Preamble §S4.10 forbids the reverse order and nothing here reverses it.
