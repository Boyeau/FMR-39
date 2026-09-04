# Camera-ready candidate — NO DEVIATION, clarification only: the lattice law L241 sources to Monte-Carlo is computable in closed form

| Field               | Value                                                                                                                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply. NO DEVIATION — clarification only**                                                                                                                       |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:exactness` **L241**                                                                                              |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                                                          |
| Evidence            | `results/R08_adverse_lattice/data/R08_lattice_exact_law.csv` and `R08_null_law_lattice.csv`; controls C1 and C2 in `logs/R08_adverse_lattice/exp_R08_adverse_lattice_a.log`        |
| Register entry      | **none.** The two printed numerals are correct Monte-Carlo estimates of the basis L241 itself states                                                                               |
| Cost                | +18 words inside one parenthetical; **no printed number changes**                                                                                                                  |
| Blocking dependency | **MERGES WITH `R07_v87_figure7_exactness.md`, it does not follow it.** See below. Shares L241 with `R08_v87_delivered_level.md`; those two search strings are disjoint and commute |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The deviation
inventory is not closed.

**Why this is a clarification and not a correction.** L241 prints

> the levels bracketing $5\%$ are $5.03\%$ at $\lambda = 11.2$ and $4.29\%$ at $\lambda = 11.4$
> ($2 \times 10^5$ fair-coin streams)

and sources both to a Monte-Carlo of a stated size. As Monte-Carlo estimates of that basis **they
are correct**, and R08 does not propose replacing them. Under the 128-bit re-keying preamble §S6
mandates, the same campaign returns `5.08 %` and `4.32 %`; the movement is registered as
`R08-campaign-redraw` and the numeral edits live in `R08_v87_adverse_numerals.md`, not here.

**What is worth saying beside them is that the law is not a Monte-Carlo question at all.** With
`δ = 0.1` the two CUSUM branches move by `+0.4` and `−0.6`, i.e. by `+2` and `−3` in units of
`2δ = 0.2`, so `(S⁺, S⁻)` is a Markov chain on the non-negative integer quadrant, `M_H` is an
integer multiple of `0.2`, and an absorbing-chain forward recursion over `{0..L}² ∪ {absorbed}`
returns `P(M_H > λ)` **exactly**, consuming no entropy at all. R08 computes it, validates it against
exhaustive enumeration of all `2^H` sign paths at `H ∈ {8, 10, 12, 14}` — exact agreement to the last
bit on all sixteen `(H, λ)` pairs — and finds it identical **bit for bit** to the table R07
independently computed for its own control C1, on all sixteen scanned lattice points:

| `λ`    | `λ` in `2δ` units | exact `P(M_H > λ)` at `H = 5 000` | v87 prints | R08 measures (`2 × 10⁵` streams) |
| ------ | ----------------- | --------------------------------- | ---------- | -------------------------------- |
| `11.0` | `55`              | `5.9900 %`                        | —          | `6.0200 %`                       |
| `11.2` | `56`              | **`5.1021 %`**                    | `5.03 %`   | `5.0815 %`                       |
| `11.4` | `57`              | **`4.3428 %`**                    | `4.29 %`   | `4.3230 %`                       |
| `11.6` | `58`              | `3.6945 %`                        | —          | `3.6705 %`                       |

The two printed values sit `1.47` and `1.16` binomial standard errors below the exact ones at
`2 × 10⁵` streams. **That is what a Monte-Carlo of the stated basis does, and there is no defect
here to correct** — only a choice between reporting an estimate and reporting the law that is
available in closed form.

**Three streams agree on that law and the agreement is asserted, not assumed.** R08's exact survival
table equals R07's cell by cell at `H = 5 000` (16/16 bit-identical). On the small-horizon path
enumeration, R08 agrees bit for bit with R07 and R10 on every cell either of them carries: eight
cells shared by all three (`H ∈ {10, 12}` × `λ ∈ {4, 5, 6, 7}` lattice units at `q = 1/2`), four
more shared with R07 alone (`H = 8`), four with R10 alone (`H = 14`). `R10_lattice_exact_law.csv`
holds **no** `H = 5 000` cell — its campaign runs at `H = 8 000` — which is why the three-way
comparison is stated on the cells the three streams actually share.

## Edit — `sec:exactness` L241, name the closed form beside the estimate

**Verification of the search string.** The block below is quoted from `articleB_whitening_v87.tex`
**line 241** verbatim and occurs **exactly once** in the file (`grep -Fc` returns `1`). It is
disjoint from the string `R08_v87_delivered_level.md` searches later in the same sentence and from
the footnote string that candidate also searches. Verify once more before applying, as a matter of
routine.

<<< RECHERCHER
~~~~~~~~~latex
the levels bracketing $5\%$ are $5.03\%$ at $\lambda = 11.2$ and $4.29\%$ at $\lambda = 11.4$ ($2 \times 10^5$ fair-coin streams)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
the levels bracketing $5\%$ are $5.03\%$ at $\lambda = 11.2$ and $4.29\%$ at $\lambda = 11.4$ ($2 \times 10^5$ fair-coin streams; the law is a finite absorbing chain on the lattice and is computable in closed form, giving $5.1021\%$ and $4.3428\%$ exactly)
~~~~~~~~~
>>> FIN DU BLOC

## The blocking dependency, stated as a merge and not as an order

`R07_v87_figure7_exactness.md` rewrites the **Figure 7 caption**, which calls `4.29 %` an "exact
lattice level", and its replacement text points the reader at `Section~\ref{sec:exactness}` with the
words "as measured". That file's own blocking note says the two edits must be **merged** rather than
applied in sequence, and this candidate is the reason: after this edit, L241 both *measures* the two
levels and *states the closed form*, so "as measured" is no longer the whole of what the section
says. **The two edits must be composed into one pass over the two sites**, with the Figure 7 caption
pointing at a sentence that already carries both. Applying either alone leaves the manuscript
internally consistent but under-describes the other site.

## What must not be done with this candidate

**It does not replace the two printed numerals and must not be used to.** Replacing a correct
Monte-Carlo estimate by an exact value is not a correction; the estimate and the exact value are
answers to two different questions and the sentence can carry both.

**It does not license calling `4.29 %` the level the test operates at.** `4.3428 %` is the level of
the *strict* comparison `M_H > λ*`. R08's control C1 measures the implemented float test to
implement the *weak* comparison on every one of the `2 × 10⁵` streams, which delivers `5.1021 %` at
the same threshold. That is the separate — and register-bearing — subject of
`R08_v87_delivered_level.md`, and this candidate must not be read as settling it.

**It opens no register entry.** The printed numerals are correct estimates of the basis the sentence
states, so nothing here is a formal contradiction and §S8's channel 1 is not involved.
