# Camera-ready candidate — Figure 9's "$2\times10^4$ streams per cell" describes one arm of three

| Field               | Value                                                                                                                                                           |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                                                                       |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), Figure 9 caption L559 and `sec:exactness` L243                                                     |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                                       |
| Evidence            | `results/R09_eprocess_anytime/data/R09_*.csv` (`N_streams` column), `logs/R09_eprocess_anytime/exp_R09_eprocess_anytime.log`                                    |
| Register entry      | **none** — the formulation is imprecise, not false, and the R09 prompt's perimeter filter bars an imprecise-but-not-false formulation from `docs/DEVIATIONS.md` |
| Cost                | +14 words in the caption, +7 in the body; no number changes                                                                                                     |
| Blocking dependency | shares L559 with `R09_v87_arl0_censoring.md` and `R09_v87_delay_parity_scope.md`; the search strings are **disjoint** and the three edits commute               |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being corrected.** Figure 9's caption opens with "($2\times10^4$ streams per cell)" and
L243 writes "$2\times10^4$ fair-coin streams per level". The second is exact: a fair-coin stream is
by definition an H₀ stream, and the H₀ campaign runs `N_NULL = 20 000` streams at every level. The
first is not, because "per cell" reaches across all three panels and the three panels are drawn
from three different samples:

| panel | what it shows                                | sample                                            |
| ----- | -------------------------------------------- | ------------------------------------------------- |
| (A)   | realized false-alarm rate, three protocols   | `N_NULL = 20 000` fair-coin streams               |
| (B)   | detection delay vs. drift `η`                | **`N_ALT = 2 000` drift streams per cell**        |
| (C)   | average run length vs. `α`                   | `N_NULL = 20 000` fair-coin streams               |
| —     | the CUSUM threshold `λ*` both panels A and B use | **`N_CAL = 50 000` calibration streams**       |

Panel B carries a quarter of the resolution the caption's single number implies: its standard
errors are `sqrt(20000/2000) = 3.16×` wider than panels A and C's for the same underlying
dispersion. A reader who prices panel B's error bars against `2×10⁴` under-reads them by that
factor.

**Nothing is falsified, and no register entry is opened.** The caption is a compression, not a
false statement, and `docs/DEVIATIONS.md` is reserved for formulations that contradict a printed
claim. The repository's own artefacts carry the three counts explicitly — the `N_streams` column of
every CSV, the per-panel `n` annotated on each axis of
`results/R09_eprocess_anytime/figures/fig09_anytime_valid.png` — so the correction below is the
caption catching up with the data it describes.

**`N_ALT` was not raised to match the caption.** L243's "$409$ vs.\ $539$ steps at $\eta = 0.10$"
is itself a 2 000-stream measurement: the delivered `simulate_h1` loops on `N_ALT` and the
submitted log line `Control (g): ... ADD=409.11` is that loop's output. Raising `N_ALT` would
displace two printed numerals in order to make a parenthetical true, which is a self-inflicted
deviation against the non-regression role preamble §S1 gives v87's results. The caption is what
moves.

## Edit 1 — Figure 9 caption L559, name the three sample sizes

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 559** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`). It is disjoint from the strings the two sibling candidates search.
Verify once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
($2\times10^4$ streams per cell)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
($2\times10^4$ fair-coin streams per level in \textbf{(A)} and \textbf{(C)}; $2\times10^3$ drift streams per cell in \textbf{(B)}; the CUSUM threshold is calibrated on a separate $5\times10^4$ fair-coin streams)
~~~~~~~~~
>>> FIN DU BLOC

## Edit 2 — `sec:exactness` L243, name the calibration sample beside the H₀ one

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 243** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`).

<<< RECHERCHER
~~~~~~~~~latex
$2\times10^4$ fair-coin streams per level
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
$2\times10^4$ fair-coin streams per level, the CUSUM threshold calibrated on a separate $5\times10^4$
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**This is not a claim that the campaign is under-powered.** Panel B's `2 000` streams are what
produced the `409` and `539` the body prints, and those two numerals are the reason `N_ALT` is not
raised. The correction is to the caption's description of the design, never to the design.

**Edit 2 is optional and Edit 1 is not.** L243's sentence is already exact as written — "fair-coin
streams per level" scopes the count to the H₀ arm correctly. Edit 2 adds the calibration sample
because the same sentence names the `5\%` calibration two clauses earlier and a reader cannot
otherwise tell which sample fixed `λ*`. If the page budget is tight, drop Edit 2 and keep Edit 1.

**The word "cell" must not be reused for panel B.** In panel B a cell is an `(α, η)` pair, in
panels A and C it is an `(arm, α, protocol)` triple, and the two do not have the same sample size.
The replacement text above says "per cell" only where the count is `2×10³`.
