# Camera-ready candidate — the level L241's threshold actually delivers is above nominal, not below it

| Field               | Value                                                                                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Status**          | **PARKED — do not apply**                                                                                                                                      |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:exactness` **L241** and its footnote                                                          |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                                     |
| Evidence            | `results/R08_adverse_lattice/data/R08_operator_levels.csv` and `R08_null_law_lattice.csv`; control C1 in `logs/R08_adverse_lattice/exp_R08_adverse_lattice_a.log` |
| Register entry      | `docs/DEVIATIONS.md`, `R08-delivered-level-above-nominal` — Class A, **D3**                                                                                    |
| Cost                | +33 words in the main sentence, +14 in the footnote; **no printed numeral is removed**                                                                          |
| Blocking dependency | shares L241 with `R08_v87_lattice_exact_basis.md`; the two search strings are **disjoint** and the two edits commute                                            |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The deviation
inventory is not closed.

## What is falsified, and what is not

**Not falsified: any printed numeral of L241.** `5.03 %` and `4.29 %` are correct Monte-Carlo
estimates of `P(M_H > λ)` at the two thresholds, on the `2 × 10⁵`-stream basis the sentence itself
states; the regenerated campaign gives `5.08 %` and `4.32 %` and the exact law gives `5.1021 %` and
`4.3428 %`. And `λ* = 11.4` **is** the threshold L241's rule selects: it is the smallest lattice
point whose strict-comparison level is at or below nominal.

**Falsified: the conjunction of the rule and the footnote.** L241 states a selection rule,

> we take the nearest attainable level **at or below nominal**, $\lambda^{\star} = 11.4$

and its own footnote states which comparison the code performs,

> the implemented test $M_H > \lambda^{\star}$ **is** the mathematical $M_H \geq \lambda^{\star}$;
> we report the level actually delivered.

R08 **measures the footnote to hold**, on every one of the `2 × 10⁵` fair-coin streams and at every
one of the six grid thresholds: `float M > λ` disagrees with the exact `M_units ≥ λ` on **zero**
streams and with the exact `M_units > λ` on between `970` and `2 032`. But on the integer lattice
`P(M ≥ u) = P(M > u − 1)`, so the level the weak comparison delivers at `λ* = 11.4` is

| operator at `λ* = 11.4`   | equals survival index | exact level    | measured (`2 × 10⁵` streams) |
| ------------------------- | --------------------- | -------------- | ---------------------------- |
| strict `M_H > 11.4`       | `P(m > 57)`           | `4.3428 %`     | `4.3230 %`                   |
| **weak `M_H ≥ 11.4`**     | `P(m > 56)`           | **`5.1021 %`** | **`5.0815 %`**               |

`5.1021 %` is **above** the `5 %` the rule promises to stay at or below. The two sentences cannot
both hold with the delivered level at or below nominal, and the numeral the sentence prints beside
`λ*` — `4.29 %` — is not the level actually delivered, which is what the footnote's closing clause
undertakes to report.

**Under the weak comparison, the threshold the rule selects is `λ = 11.6`.** Requiring
`P(M_H ≥ λ) ≤ 5 %` requires `P(M_H > λ/2δ − 1) ≤ 5 %`, hence `λ/2δ − 1 ≥ 57`, hence `λ ≥ 11.6`,
where the delivered level is `4.3428 %`. One lattice step.

## The two legs of the classification, and which one carries it

- **Exact leg — decisive.** `5.1021 %` comes from an absorbing-chain dynamic program that consumes
  no entropy. It carries no sampling interval and the trigger probability of the statement is `0`.
  It exceeds nominal by `0.1021` points, i.e. by `2.0 %` of the nominal level itself.
- **Monte-Carlo leg — reported, and *not* decisive.** The measured weak level is `5.0815 %` with a
  Wilson interval of `[4.9861 %, 5.1786 %]`, which **includes** `5 %`. On the Monte-Carlo evidence
  alone, preamble §S3's interval criterion would leave this at D2, and the register entry says so.

The classification rests on the exact leg, and the Monte-Carlo leg is at the edge of its own
resolution rather than against it. At the exact level `5.1021 %` the Wilson lower bound clears `5 %`
in expectation from about `1.8 × 10⁵` streams, so the `2 × 10⁵` basis L241 states is right at that
boundary; this particular draw came in `0.42` standard errors below the exact level and its interval
therefore straddles nominal. Resolving the excess with `90 %` power would take about `4.9 × 10⁵`
streams. **None of that bears on the exact leg**, which is a closed-form computation.

## Edit 1 — `sec:exactness` L241, state the level the threshold delivers

**Verification of the search string.** The block below is quoted from `articleB_whitening_v87.tex`
**line 241** verbatim and occurs **exactly once** in the file (`grep -Fc` returns `1`). It is
disjoint from the string `R08_v87_lattice_exact_basis.md` searches earlier in the same sentence.
Verify once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
we take the nearest attainable level at or below nominal, $\lambda^{\star} = 11.4$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
we take the nearest attainable level at or below nominal under the strict comparison, $\lambda^{\star} = 11.4$; because the implemented comparison is the weak one (see the footnote), the level this threshold actually delivers is $P(M_H \geq 11.4) = P(M_H > 11.2) = 5.10\%$, just above nominal, and the strictly conservative choice would be $\lambda = 11.6$ at $4.34\%$
~~~~~~~~~
>>> FIN DU BLOC

## Edit 2 — the L241 footnote, report the level it undertakes to report

**Verification of the search string.** The block below is quoted from the footnote attached to
`articleB_whitening_v87.tex` **line 241** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`). It is disjoint from Edit 1's string and from every string the sibling
candidates search. Verify once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
so the implemented test $M_H > \lambda^{\star}$ is the mathematical $M_H \geq \lambda^{\star}$; we report the level actually delivered.
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
so the implemented test $M_H > \lambda^{\star}$ is the mathematical $M_H \geq \lambda^{\star}$, which we verify on $2 \times 10^5$ streams; the level actually delivered at $\lambda^{\star}$ is therefore $5.10\%$ and not the $4.29\%$ of the strict comparison.
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**It is not a claim that the threshold is wrong or that the pipeline is miscalibrated.** `λ* = 11.4`
delivers `5.10 %` against a `5 %` nominal — a `0.10`-point excess on a level whose two adjacent
attainable values are `4.34 %` and `5.99 %`. The paper's thesis, that the `Concept` null law is
known without a nuisance parameter, is what makes this computable at all; the finding is that the
sentence describing the *choice* does not describe the *delivered* level.

**It must not be used to change `5.03 %` or `4.29 %`.** Those are correct strict-comparison
Monte-Carlo estimates. What is added is the level of the other comparison at the same threshold.

**The operator identity is empirical and the camera-ready text must not state it as a theorem.** The
accumulated float lands *below* its exact lattice value on `2 776` of the `200 000` streams, so a
stream whose exact maximum equals `λ*` can in principle be missed. Zero disagreements with the weak
comparison were observed at this horizon, this dead band and this accumulation order, and Edit 2
says "which we verify on `2 × 10⁵` streams" for exactly that reason.

**It does not touch Figure 8 or its caption.** Panel C's step function and its two marked levels are
strict-comparison quantities and are correct as drawn; the repository's own figure draws both
operator levels on panel B and records that as a deliberate divergence in
`docs/sections/R08.md`.
