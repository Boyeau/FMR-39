# Camera-ready candidate — the Figure 7 caption calls "exact" a level L241 sources to Monte-Carlo

| Field               | Value                                                                                                                              |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Status**          | **PARKED — do not apply**                                                                                                          |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), Figure 7 caption, **line 543**, inside `\caption{…\label{fig:estmean}}` |
| Trigger             | Acceptance notification, 14 November 2026                                                                                          |
| Evidence            | `results/R07_estimated_mean/data/R07_lattice_exact_law.csv`, `record_type = exact_survival`                                         |
| Register entry      | **none in R07.** The two numerals belong to R08 — see "What this candidate does not do"                                            |
| Cost                | one word in the caption; no number changes                                                                                         |
| Blocking dependency | shares the caption with `R07_v87_panelB_operating_level.md`; the two search strings are **disjoint** and the two edits commute      |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed: R08 owns the campaign behind the two numerals and may revise
them, in which case this edit and R08's must be merged rather than applied in sequence.

**What is being corrected.** One word. The Figure 7 caption reads

> \textbf{(B)} \textsc{Concept} FPR at threshold $\lambda^{\star} = 11.4$ (**exact lattice level**
> $4.29\%$, $5.03\%$ at $\lambda = 11.2$; shaded band = the two attainable levels bracketing $5\%$).

while L241, which is where those two numerals are established, sources them to a **Monte-Carlo**:

> the levels bracketing $5\%$ are $5.03\%$ at $\lambda = 11.2$ and $4.29\%$ at $\lambda = 11.4$
> (**$2 \times 10^5$ fair-coin streams**)

A level measured on `2 × 10⁵` streams is not an exact level, and the caption is the only place in
the manuscript that says it is. One or the other word has to go.

**The lattice law *is* exactly computable, and R07 computed it.** With `δ = 0.1` the two CUSUM
branches move by `+0.4` and `−0.6`, i.e. by `+2` and `−3` in units of `2δ = 0.2`, so `(S⁺, S⁻)` is
a Markov chain on the non-negative integer quadrant and an absorbing-chain dynamic program returns
`P(M_H > λ)` exactly, consuming no entropy at all. Validated against exhaustive enumeration of all
`2^H` paths at `H ∈ {8, 10, 12}` — exact agreement to the last bit, twelve `(H, λ)` pairs:

| `λ`    | exact `P(M_H > λ)` at `H = 5 000` | v87 prints | v87's stated basis        |
| ------ | --------------------------------- | ---------- | ------------------------- |
| `11.0` | `5.9900 %`                        | —          | —                         |
| `11.2` | **`5.1021 %`**                    | `5.03 %`   | `2 × 10⁵` fair-coin streams |
| `11.4` | **`4.3428 %`**                    | `4.29 %`   | `2 × 10⁵` fair-coin streams |

The printed pair sits `1.24` and `1.50` Monte-Carlo standard errors below the exact values, which
is what a Monte-Carlo of the stated basis does. **The caption's adjective is what is wrong, not the
numerals.**

## Edit — Figure 7 caption, line 543

**Verification of the search string.** The block below is quoted from `articleB_whitening_v87.tex`
**line 543** verbatim and occurs **exactly once** in the file (`grep -Fc` returns `1`). It lies
inside `\caption{…}` of the float carrying `\label{fig:estmean}`. It is disjoint from the string
`R07_v87_panelB_operating_level.md` searches in the same caption, and from the L241 sentence that
carries the same two numerals. Verify once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
(exact lattice level $4.29\%$, $5.03\%$ at $\lambda = 11.2$; shaded band = the two attainable levels bracketing $5\%$)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
(attainable lattice levels $4.29\%$ at $\lambda^{\star}$ and $5.03\%$ at $\lambda = 11.2$, as measured in Section~\ref{sec:exactness}; shaded band = the two levels bracketing $5\%$)
~~~~~~~~~
>>> FIN DU BLOC

The replacement removes the word "exact", keeps both numerals untouched, and points the reader at
the place where their basis is stated.

## What this candidate does not do

**It does not touch L241, and it does not correct either numeral.** The `4.29 %` / `5.03 %` pair
lives in `protocol_21d_null_law_lattice.csv`, produced by
`Priorite_21b_adverse_bias_and_null_law.py`, which the repository's stream map assigns to **R08**
(v87 Figure 8, `fig:adverse`, panel C, whose own caption states the `2 × 10⁵` basis). Re-running
that campaign in R07 would put two competing CSV sources behind one published numeral, against
the repository's one-cell-per-number rule. R07 therefore opens no register entry on those values
and consumes no search string on L241; the exact law and its validation are handed to R08 in
`R07_v87_lattice_handoff_to_R08.md`, so that R08 can file its own candidate.

**If R08 replaces the two numerals with the exact ones, this edit must be merged with R08's, not
applied before it.** Applying this one first leaves the caption pointing at
`Section~\ref{sec:exactness}` for numerals R08 is about to change.

**Nothing here licenses calling `4.29 %` the level the panel operates at.** It is the level of the
mathematical `M_H > λ*`; the panel operates near the other one. That is the separate subject of
`R07_v87_panelB_operating_level.md`.
