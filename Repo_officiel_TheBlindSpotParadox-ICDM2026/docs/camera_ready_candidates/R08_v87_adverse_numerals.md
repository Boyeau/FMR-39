# Camera-ready candidate — the four adverse-direction numerals of L311 and the Figure 8 caption

| Field               | Value                                                                                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Status**          | **PARKED — do not apply**                                                                                                                                      |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:ar_garch` **L311** and the Figure 8 caption, **line 551**                                     |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                                     |
| Evidence            | `results/R08_adverse_lattice/data/R08_adverse_bias.csv` (`fpr_biased`) and `results/R07_estimated_mean/data/R07_estmean_lb_fpr.csv` (arm `NAIVE`), read at `round_trip` |
| Register entries    | `docs/DEVIATIONS.md`, `R08-campaign-redraw` (Class A, D2) for the collapse numeral; `R07-campaign-redraw` (Class A, D2) for the inflation numeral and the penalty — **R08 opens no entry on the latter two** |
| Cost                | five numerals; no clause changes                                                                                                                              |
| Blocking dependency | shares the Figure 8 caption with `R08_v87_whiteness_identity.md`; shares L311 with nothing else. All search strings are pairwise **disjoint** and the edits commute |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The deviation
inventory is not closed.

## What moves, and whose cell each one is

Preamble §S6 requires migrating the campaign off the delivered
`SeedSequence(424242).spawn(7 * 10000)` positional key — and off `np.random.default_rng(100)` on the
calibration — to a 128-bit key on the role and the index alone. Every Monte-Carlo value of both
modules is redrawn by construction, which is pre-classified Class A / D2 by the
`R05/R07/R09/R10/R13-campaign-redraw` precedents.

| site                                  | v87 prints | regenerated | source cell                                                | register entry        |
| ------------------------------------- | ---------- | ----------- | ---------------------------------------------------------- | --------------------- |
| L311, Fig. 8 (B): FPR collapses to    | `0.86\%`   | **`0.95\%`** | `R08_adverse_bias.csv`, `b = 0.15`, `fpr_biased`           | `R08-campaign-redraw` |
| L311, Fig. 8 (B): FPR inflates to     | `20.8\%`   | **`21.0\%`** | `R07_estmean_lb_fpr.csv`, `NAIVE`, `phi = 0.15`            | `R07-campaign-redraw` |
| L311: under-centering penalty         | `1.1` pt   | **`1.3` pt** | `R07_estmean_lb_fpr.csv`, `NAIVE`, `phi ∈ {0, 0.02}`       | `R07-campaign-redraw` |

**The sites are R08's and two of the three cells are not.** The inflation numeral and the penalty
are differences of `fpr_concept` cells of R07's own campaign, whose redraw `R07-campaign-redraw`
already registers; R08 reads them at `round_trip`, macro-ises them because the *sentence* is R08's,
and **opens no new register entry on their movement**. No R07 candidate consumes a search string on
either site, which is why R08 may file the edit here.

**Every qualitative claim of the sentence holds.** The collapse is still an order of magnitude below
the inflation — `0.95 %` against `21.0 %`, a factor of `22` — the direction of each arm is unchanged
and monotone over the whole grid (control C5: ten consecutive steps, zero inversions), and the
under-centering penalty at a residual momentum of `0.02` is still "only" about a point of
false-alarm rate. What moves is the printing precision of three numerals.

**The margin behind the penalty numeral, since the sentence uses it as a safety argument.** L311
reads it against `0.02`, "seven times the largest we measure". The denominator of that ratio is R07's
and R08 emits no macro for it: the largest `|E[φ̂] − φ|` over R07's 28 diagnostic cells is
`0.0031269`, giving `6.40`, and against the `2.9e-3` v87 itself prints as the bound the ratio is
`6.90`. Both round to "seven times"; `docs/DEVIATIONS.md` `R07-bias-bound-not-a-bound` records that
the printed bound is contradicted by the approximation printed beside it, and that entry is R07's.

## Edit 1 — Figure 8 caption, line 551, the collapse numeral

**Verification of the search string.** Quoted from `articleB_whitening_v87.tex` **line 551**
verbatim; occurs **exactly once** (`grep -Fc` returns `1`). Disjoint from Edit 2's string in the same
caption and from the string `R08_v87_whiteness_identity.md` searches. Verify once more before
applying.

<<< RECHERCHER
~~~~~~~~~latex
FPR collapses to $0.86\%$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
FPR collapses to $0.95\%$
~~~~~~~~~
>>> FIN DU BLOC

## Edit 2 — Figure 8 caption, line 551, the inflation numeral

**Verification of the search string.** Quoted from `articleB_whitening_v87.tex` **line 551**
verbatim; occurs **exactly once** (`grep -Fc` returns `1`). Disjoint from Edit 1's string.

<<< RECHERCHER
~~~~~~~~~latex
FPR inflates to $20.8\%$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
FPR inflates to $21.0\%$
~~~~~~~~~
>>> FIN DU BLOC

## Edit 3 — `sec:ar_garch` L311, the collapse numeral

**Verification of the search string.** Quoted from `articleB_whitening_v87.tex` **line 311**
verbatim; occurs **exactly once** (`grep -Fc` returns `1`). Disjoint from Edits 1, 2, 4 and 5.

<<< RECHERCHER
~~~~~~~~~latex
collapses to $0.86\%$ at $b = 0.15$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
collapses to $0.95\%$ at $b = 0.15$
~~~~~~~~~
>>> FIN DU BLOC

## Edit 4 — `sec:ar_garch` L311, the inflation numeral

**Verification of the search string.** Quoted from `articleB_whitening_v87.tex` **line 311**
verbatim; occurs **exactly once** (`grep -Fc` returns `1`). Disjoint from Edits 1, 2, 3 and 5.

<<< RECHERCHER
~~~~~~~~~latex
inflates it to $20.8\%$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
inflates it to $21.0\%$
~~~~~~~~~
>>> FIN DU BLOC

## Edit 5 — `sec:ar_garch` L311, the under-centering penalty

**Verification of the search string.** Quoted from `articleB_whitening_v87.tex` **line 311**
verbatim; occurs **exactly once** (`grep -Fc` returns `1`). Disjoint from Edits 1, 2, 3 and 4.

<<< RECHERCHER
~~~~~~~~~latex
the under-centering penalty is still only $1.1$ points of false-alarm rate
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
the under-centering penalty is still only $1.3$ points of false-alarm rate
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**It must not be read as R08 registering R07's cells.** Two of the three numerals are differences of
`R07_estmean_lb_fpr.csv` cells and their movement is `R07-campaign-redraw`. R08 owns the sentence
and the figure caption; it does not own the campaign behind `20.8 %` or behind the penalty, and it
opens no register entry on either.

**It must not be applied together with a re-run that changes the numerals again.** Every value here
is a cell of a specific run, whose SHA-256 is in `docs/audits/AUDIT_R08.md` §5. A later campaign of
this repository would move them again, and the edit is to be regenerated from the frames, not
transcribed from this file.

**It must not be extended to `5.03 %` and `4.29 %`.** Those numerals also move under the redraw, to
`5.08 %` and `4.32 %`, and they are deliberately **not** edited: they are correct Monte-Carlo
estimates of the basis L241 states, and `R08_v87_lattice_exact_basis.md` reports the closed form
beside them instead of replacing them.

**Nothing here bears on the sentence's whiteness clause.** "Reject within three points of each
other" holds, at `2.21` points; that is the subject of `R08_v87_whiteness_identity.md` and no
numeral of it changes.
