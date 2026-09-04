# Hand-off note from R07 to R08 — the exact law of the 2δ lattice, and why R07 files no candidate on L241

| Field               | Value                                                                                                                     |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **NOT A CANDIDATE — no edit is proposed here, and no search string is consumed**                                           |
| Addressed to        | the stream that owns v87 Figure 8 (`fig:adverse`, panel C) and `sec:exactness` **L241** — the repository's map assigns it to R08 |
| Produced by         | R07, control C1                                                                                                           |
| Evidence            | `results/R07_estimated_mean/data/R07_lattice_exact_law.csv`, `record_type ∈ {exact_survival, enumeration_validation}`     |
| Register entry      | **none.** R07 opens no entry on another stream's published values                                                         |

## Why this note exists instead of a candidate

`sec:exactness` L241 prints:

> At $\delta = 0.1$, $H = 5{,}000$, the levels bracketing $5\%$ are $5.03\%$ at $\lambda = 11.2$
> and $4.29\%$ at $\lambda = 11.4$ (**$2 \times 10^5$ fair-coin streams**); we take the nearest
> attainable level at or below nominal, $\lambda^{\star} = 11.4$.

Those two numerals are cells of `protocol_21d_null_law_lattice.csv` — `P_exceed = 0.05027` at
`λ = 11.2` and `0.04287` at `λ = 11.4`, `N_streams = 200000` — produced by
`Priorite_21b_adverse_bias_and_null_law.py`, which the repository's stream map assigns to **R08**,
whose Figure 8 panel C caption states the same `2 × 10⁵` basis.

R07 does **not** re-run that campaign. Doing so would put two competing CSV sources behind one
published numeral, against the repository's one-cell-per-number rule, and it is a variant of R08's
experiment that v87 does not describe for R07 (preamble §S4, perimeter filter). The R13/R16
precedent is the same: a stream does not macro-ise or correct what another stream owns. **R07
therefore opens no register entry on L241 and consumes no `RECHERCHER` string there**, so that R08
can file its own candidate against a line R07 has left untouched.

What R07 does own is the *Figure 7 caption*, which calls `4.29 %` an "exact lattice level" while
L241 sources it to Monte-Carlo. That is `R07_v87_figure7_exactness.md`, and it touches the word,
not the values.

## What R07 measured, and how

R07's control C1 needs a deterministic assertion with zero trigger probability, and no Monte-Carlo
delivers one. The exact law is computable in closed form.

**The lattice.** With `δ = 0.1` the two branches of the bilateral sign-CUSUM move by `+0.4` and
`−0.6`, i.e. by `+2` and `−3` in units of `2δ = 0.2`, each clamped at `0`. `(S⁺, S⁻)` is therefore
a Markov chain on the non-negative integer quadrant and `M_H` is an integer multiple of `0.2`.

**The program.** An absorbing-chain forward recursion over `{0..L}² ∪ {absorbed}` with
`L = λ/2δ`, `H = 5 000` steps, each splitting the mass in half. It consumes **no entropy at all**.

**The validation.** Against exhaustive enumeration of all `2^H` sign paths at `H ∈ {8, 10, 12}` and
`λ ∈ {4, 5, 6, 7}` lattice units — twelve `(H, λ)` pairs, **exact agreement to the last bit**,
largest absolute difference `0.0`. The test suite re-derives the same law from an independently
written explicit transition matrix and agrees within `4 H ε = 4.4 × 10⁻¹²`.

## The values

| `λ`    | `λ` in `2δ` units | exact `P(M_H > λ)` at `H = 5 000` | v87 prints (L241) | difference   |
| ------ | ----------------- | --------------------------------- | ----------------- | ------------ |
| `11.0` | `55`              | `5.9900 %`                        | —                 | —            |
| `11.2` | `56`              | **`5.1021 %`**                    | `5.03 %`          | `+0.072` pt  |
| `11.4` | `57`              | **`4.3428 %`**                    | `4.29 %`          | `+0.053` pt  |

A `2 × 10⁵`-stream Monte-Carlo has a binomial standard error of `0.045` points on a `4.3 %` level
and `0.049` on a `5.1 %` one. The two printed numerals sit `1.50` and `1.24` of those below the
exact values — **consistent with a Monte-Carlo fluctuation of the basis L241 itself states.** There
is no defect here to correct; there is a choice between reporting a Monte-Carlo estimate and
reporting the exact law that is available.

**`λ* = 11.4` does not move under either.** L241's own rule — "the nearest attainable level at or
below nominal" — selects the same threshold on the exact law as on the Monte-Carlo, and the value
is bit-identical to the float64 of the literal v87 prints.

## Three things R08 will want that R07 established

1. **`Priorite_21b` and `Priorite_21` do not measure the same operator.** `Priorite_21b` compares
   `rounded_M > λ` (its lines 358–359), which is why its Monte-Carlo lands on the exact lattice
   law. `Priorite_21`'s float CUSUM does not round, and its accumulated `M` sits **above** its
   exact lattice value on `9 652` of R07's `10 000` fair-coin `ORACLE` streams, below on `137`,
   exactly on it on `211`. The two scripts are not two estimates of one quantity.
2. **L241's footnote holds at this threshold, and it is empirical.** The footnote states that
   "the implemented test $M_H > \lambda^{\star}$ **is** the mathematical
   $M_H \geq \lambda^{\star}$". Over `35 000` fair-coin streams — R07's `ORACLE`, calibration and
   validation sets — the implemented test coincides with `M ≥ λ*` on **all** of them and differs
   from `M > λ*` on `267`. But the float `M` lands *below* its exact lattice value on `480` of
   those streams, so the coincidence is a property of this threshold, this horizon and this
   accumulation order, not a theorem. The realised level on the `25 000` independent streams is
   `5.064 %`, against the exact `5.1021 %`. R08's `Priorite_21b`, which rounds before comparing,
   implements `M ≥ λ*` structurally and is not exposed to this at all.
3. **The exact law is reusable.** `lattice_exceedance_exact(horizon, lam_units)` in
   `experiments/R07_estimated_mean/exp_R07_estimated_mean.py` is parameter-free apart from
   `(H, λ)`, deterministic, and takes under a second per threshold at `H = 5 000`. R08 can call it
   or re-derive it; it is not a primitive R07 asks anyone to share, since preamble §S4.2 keeps
   scientific primitives duplicated per experiment.

## What must not be done with this note

**It is not a licence to edit L241.** No `RECHERCHER` block appears in this file, deliberately.

**R07's exact values must not be substituted into L241 without re-running R08's own classification.**
`protocol_21d_null_law_lattice.csv` supports Figure 8 panel C as well as the sentence at L241, and
whether the figure and the sentence should quote the same numbers is R08's question, not R07's.
