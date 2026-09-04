# Camera-ready candidate — NO DEVIATION, clarification only: "identical whiteness loss" is a mechanism, and the caption states it as a measurement

| Field               | Value                                                                                                                                                            |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply. NO DEVIATION — clarification only**                                                                                                     |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), Figure 8 caption, **line 551**, inside `\caption{…\label{fig:adverse}}`                             |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                                        |
| Evidence            | `results/R08_adverse_lattice/data/R08_adverse_bias.csv` and `R08_pairing_diagnostic.csv`; control C4 in `logs/R08_adverse_lattice/exp_R08_adverse_lattice_a.log` |
| Register entry      | **none.** The body's claim holds and the caption states a mechanism, not a measurement; §S8's scope filter keeps this out of `docs/DEVIATIONS.md`                |
| Cost                | four words replaced by five; no number changes                                                                                                                   |
| Blocking dependency | shares the Figure 8 caption with `R08_v87_adverse_numerals.md`; the search strings are **disjoint** and the edits commute                                        |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The deviation
inventory is not closed.

**What is being clarified, and what is not being corrected.** The Figure 8 caption reads

> \textbf{(A)} Ljung--Box rejection: injected over-centering bias $b$ and naive under-centering at
> $\phi = b$ **yield identical whiteness loss** ($|\mathrm{Cov}(y_t, y_{t+k})|$ response).

while the body, L311, says something weaker and measurable:

> the injected-bias arm and the naive arm at $\phi = b$ **reject within three points of each other**
> across a range spanning $5$ to $100\%$.

**These are not the same claim, and only one of them is measurable.** The body's is, and **it
holds**: the largest `|Δ lb|` over the six values of `b` is `2.21` points, attained at `b = 0.075`,
against the three the sentence states. The caption's is not a measurement at all — it is a statement
about the mechanism, that both mis-centrings act on the sign stream only through
`|Cov(y_t, y_{t+k})|`, which is symmetric in the sign of the bias by construction. Nothing here
contradicts that mechanism.

**What the data do say about equality of the two RATES.** They are close and they are not equal.
Three of the six paired proportion tests separate the two arms at the `5 %` level in the regenerated
campaign (`b = 0.05`, `0.075`, `0.10`); the submitted campaign's witness had two (`5.9e-5` at
`b = 0.075`, `0.0243` at `b = 0.05`). **Neither count is evidence either way**, and the repository
says so before reading either: six simultaneous tests at the `5 %` level reject at least once with
probability `1 − 0.95⁶ = 26.49 %` under equality itself. The instrument that does carry information
is a calibration of the six p-values against `Uniform(0,1)`, read against a null that carries the
dependence the design creates — the six `b` share the same 10 000 trajectories and at each `b` the
two arms share the same innovation stream. That gives `D = 0.5584` at a null exceedance probability
of `0.038` under sign-flip resampling on the trajectory index, and the null law of the maximum
paired gap puts the observed `0.0221` just inside its own `99.9 %` quantile, `0.0223`.

**The reading, stated once and without overclaiming in either direction.** The two arms lose
whiteness through the same mechanism and by amounts that agree within the three points the body
states. They are not measurably identical in rate, and the campaign has close to enough resolution
to say so. The caption's word "identical" invites the stronger reading, and it is the only place in
the manuscript that does.

## Edit — Figure 8 caption, line 551

**Verification of the search string.** The block below is quoted from `articleB_whitening_v87.tex`
**line 551** verbatim and occurs **exactly once** in the file (`grep -Fc` returns `1`). It lies
inside `\caption{…}` of the float carrying `\label{fig:adverse}`, and it is disjoint from every
string `R08_v87_adverse_numerals.md` searches in the same caption. Verify once more before applying,
as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
yield identical whiteness loss
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
yield whiteness loss agreeing within three points
~~~~~~~~~
>>> FIN DU BLOC

The replacement keeps the parenthetical that follows it — `($|\mathrm{Cov}(y_t, y_{t+k})|$
response)` — untouched, so the mechanism is still stated; what changes is that the caption now
states the body's measurable claim instead of a stronger one the data do not support.

## What must not be done with this candidate

**It is not a claim that the mechanism is wrong.** Both mis-centrings act through the sign stream's
autocovariance and the response is symmetric in the sign of the bias. That is what panel A shows and
it is not in question.

**It is not a register entry, and it must not become one.** The body is true, the caption states a
mechanism rather than a measurement, and a formulation that is imprecise but not false does not
reach `docs/DEVIATIONS.md` (preamble §S8, channel 1). This candidate lives in channel 3 only.

**The three-point bound must not be quoted as a bound that was tested at its edge.** The maximum gap
is an extremum over six correlated cells and has neither the distribution nor the interval of one
cell: its 95 % bootstrap envelope over 2 000 resamplings of the trajectory index is
`[1.56, 3.61]` points, which **includes** three. Preamble §S3 makes a printed bound crossed only when
that interval excludes it, and it does not; but a camera-ready text must not present `2.21` as
comfortably inside a bound whose sampling envelope reaches `3.61`.
