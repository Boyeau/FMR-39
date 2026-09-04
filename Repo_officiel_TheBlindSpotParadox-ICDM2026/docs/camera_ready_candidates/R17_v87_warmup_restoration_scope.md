# Camera-ready candidate — NO DEVIATION, clarification only: "restored from n = 500 onward" is stated without conditioning on the leverage, and rests on an interval rather than on a point

| Field               | Value                                                                                                                                                                                                           |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                                                                                                                       |
|                     | **NO DEVIATION — clarification only**                                                                                                                                                                           |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), `sec:misspecification` L341                                                                                                                        |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                                                                                       |
| Evidence            | `results/R17_econometric_baseline/data/R17_warmup_sensitivity.csv`, columns `FPR_Eco`, `FPR_Eco_CI_low`, `FPR_Eco_CI_high` at both `gamma_lev`; witness `data/reference/R17/protocol_3d_warmup_sensitivity.csv` |
| Register entries    | **none** — the claim is not falsified; §S8's scope filter keeps this out of `docs/DEVIATIONS.md`                                                                                                                |
| Cost                | +21 words in the body; no number changes                                                                                                                                                                        |
| Blocking dependency | shares L341 with `R17_v87_warmup_resolution.md`; the two search strings are **disjoint** and the two edits commute                                                                                              |

**Why this is not applied now.** The manuscript is under review and cannot be edited.

**Nothing here is false.** The sentence is true as written under the falsification rule preamble §S3
fixes for a printed level: a bound is crossed only when the 95 % interval of the regenerated value
excludes it, and at `n = 500` the interval covers the nominal `5 %` on **both** leverage settings, in
the submitted campaign and in the regenerated one alike. What the sentence omits is that
`protocol_3d` runs **two** columns and that the restoration is read on one of them.

**The two columns, in both campaigns.** `protocol_3d` sweeps `n_warmup ∈ {250, 500, 1000, 2000}`
against `gamma_lev ∈ {0.00, 0.28}` at 200 streams per cell. L341 quotes one pair of cells.

| `n_warmup` | witness `γ_lev = 0.00` | witness `γ_lev = 0.28` | regenerated `γ_lev = 0.00` | regenerated `γ_lev = 0.28` |
| ---------- | ---------------------- | ---------------------- | -------------------------- | -------------------------- |
| `250`      | `9.5 %`                | `11.5 %`               | `10.5 %`  `[7.0, 15.5]`    | `10.0 %`  `[6.6, 14.9]`    |
| `500`      | `3.0 %`                | **`6.0 %`**            | **`7.0 %`**  `[4.2, 11.4]` | **`7.5 %`**  `[4.6, 12.0]` |
| `1000`     | `3.0 %`                | `4.5 %`                | `3.5 %`  `[1.7, 7.0]`      | `4.0 %`  `[2.0, 7.7]`      |
| `2000`     | `3.0 %`                | `3.5 %`                | `2.0 %`  `[0.8, 5.0]`      | `2.0 %`  `[0.8, 5.0]`      |

Intervals are Wilson score intervals at 200 streams, the delivered `wilson_ci` with `z = 1.96`.

**What the two campaigns agree on, and what only the regenerated one shows.** Both agree that the
rate falls monotonically with the warm-up on both columns, with no inversion beyond two paired
standard errors, and that the `n = 500` cell covers the nominal level on both columns. The submitted
campaign shows the restoration as a **point** at `3.0 %` on the symmetric column and as `6.0 %` on
the leverage column, which is where the asymmetry the sentence does not mention is visible; the
128-bit re-keying moves the symmetric column to `7.0 %`, so in the regenerated campaign the two
columns sit within half a point of each other at `n = 500` and neither is at the nominal level. The
asymmetry is therefore a feature of the submitted draw, and what survives both draws is the weaker
and more defensible statement: **at `n = 500` the interval covers the level; the point estimate does
not sit on it.**

## Edit — `sec:misspecification` L341, name the column and the basis

**Verification of the search string.** Quoted from `articleB_whitening_v87.tex` **line 341**
verbatim; `grep -Fc` returns `1`. It is disjoint from the two strings
`R17_v87_warmup_resolution.md` searches on the same line. Verify once more before applying, as a
matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
the level is restored from $n = 500$ onward
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
the level is restored from $n = 500$ onward, in the sense that its $95\%$ Wilson interval covers the nominal rate from that window on, at both leverage settings of the sweep
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**This candidate opens no register entry and must not acquire one.** Preamble §S8 admits a
clarification of a true but incomplete formulation into this directory on the explicit condition
that it carries none. The claim survives its own falsification rule on both columns and in both
campaigns; what is added is the basis on which it survives.

**It must not be merged with `R17_v87_warmup_resolution.md`.** That candidate reports the resolution
of the two numerals L341 prints. Attaching a scope clarification to a resolution statement makes the
reason for each unreadable.

**No revision may present the `γ_lev = 0.28` column as a robustness check the manuscript performed.**
L341 makes no leverage-conditional statement, and `protocol_3d`'s second column is not cited
anywhere in v87. It is reported here because the sweep produced it, not because the sentence claims
it.

**No revision may quote the regenerated numerals in place of the submitted ones without the register
entry that carries them.** Their displacement is `R17-campaign-redraw`, Class A / D2, and the
numeral edits belong to that entry and not to this clarification.
