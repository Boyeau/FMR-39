# Camera-ready candidate — the Figure 10 caption's measured FPR envelope moves from 1.0–1.8 % to 1.0–1.5 %

| Field               | Value                                                                                                                              |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Status**          | **PARKED — do not apply**                                                                                                          |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), Figure 10 caption (`fig:skew_robustness`), **line 567**                |
| Trigger             | Acceptance notification, 14 November 2026                                                                                          |
| Evidence            | `results/R10_skew_robustness/data/R10_skew_fpr.csv`, column `fpr_qhat_rate`, min and max over the four rows                        |
| Register entry      | `docs/DEVIATIONS.md`, `R10-campaign-redraw` — Class A, **D2**                                                                       |
| Cost                | one numeral in one parenthesis; no other number in the caption or in the body text changes                                          |
| Blocking dependency | shares line 567 with `R10_v87_panelA_sign_arm_scope.md`; the two search strings are **disjoint** and the two edits commute          |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed: streams after R10 may touch the same caption, and applying a
correction before the inventory closes guarantees reapplying it later.

**What is being corrected.** The caption prints a measured envelope:

> \textbf{(B)} Asymmetry shifts the marginal rate; recentering on warm-up estimate $\hat{q}$
> restores false-alarm control (**measured FPR $1.0$--$1.8\%$**).

Preamble §S6 requires the entropy of every Monte-Carlo draw to be migrated to a 128-bit
`SeedSequence` keyed on the **role and index alone**. The delivered
`Priorite_9_skew_robustness.py` keyed each stream on a bare integer `seed ∈ 1..1000` and built
`np.random.RandomState(seed)` inside the DGP. The migration is required by the specification, not
by any observed failure, and it redraws all 4 000 streams. Every Monte-Carlo value of the campaign
therefore moves; this is the `R11-regenerated`, `R05-campaign-redraw`, `R13-campaign-redraw` and
`R07-campaign-redraw` situation and it was acknowledged in advance.

**One published numeral moves at v87's own printing precision.**

| `xi` | submitted `fpr_qhat_rate` | regenerated |
| ---- | ------------------------- | ----------- |
| 1.00 | `0.018`                   | `0.010`     |
| 0.85 | `0.018`                   | `0.014`     |
| 0.65 | `0.010`                   | `0.011`     |
| 0.50 | `0.011`                   | `0.015`     |

The envelope `1.0`–`1.8 %` becomes **`1.0`–`1.5 %`**. The lower end is unchanged at the caption's
printing precision; the upper end moves by three tenths of a point.

**The maximum carries its own law, not the interval of one cell.** A maximum over four cells that
share all 1 000 streams is an extremum statistic (§S4bis, fourth corollary). Its law is built by
resampling the 1 000 stream indices with replacement, 2 000 replicates, recomputing all four rates
on each and taking the maximum there:

| quantity                     | point value | bootstrap 95 %      | bootstrap mean |
| ---------------------------- | ----------- | ------------------- | -------------- |
| `max fpr_qhat_rate`          | `0.015`     | `[0.012, 0.024]`    | `0.017001`     |
| `min fpr_qhat_rate`          | `0.010`     | `[0.004, 0.013]`    | `0.008393`     |

**The submitted `0.018` sits inside the bootstrap envelope of the regenerated maximum.** The two
campaigns are two draws of the same design and this candidate does not claim the submitted numeral
was wrong; it records which draw the repository's artefacts contain.

**Nothing qualitative moves.** "Recentering on warm-up estimate $\hat{q}$ restores false-alarm
control" holds at every grid point: the recentred arm stays below the 5 % nominal everywhere,
against a fixed-`1/2` arm that reaches `96.6 %` at `xi = 0.5`.

## Edit — Figure 10 caption, line 567

**Verification of the search string.** The block below is quoted from `articleB_whitening_v87.tex`
**line 567** verbatim and occurs **exactly once** in the file (`grep -Fc` returns `1`). It is
disjoint from the string `R10_v87_panelA_sign_arm_scope.md` searches in the same caption. Verify
once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
measured FPR $1.0$--$1.8\%$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
measured FPR $1.0$--$1.5\%$
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**The envelope must not be quoted as a calibration to 5 %.** It is not one, and the caption does
not claim it is. The recentred arm is **conservative** against the nominal by a factor of three to
five — and, more to the point, it sits three to four times **above** the level this detector
reaches under perfect centring, which control C8 measures at `0.345 %` on 80 000 keyed
`Bernoulli(q)` streams. Both readings belong beside the numeral and `docs/sections/R10.md` gives
them; neither is registered, because the caption prints no nominal level for this detector and a
formulation that is incomplete but not false does not reach the register.

**The envelope must not be widened to cover both campaigns.** `1.0`–`1.8 %` and `1.0`–`1.5 %` are
two draws; printing `1.0`–`1.8 %` "to be safe" would be a tolerance chosen on the observed spread,
which preamble §S4.8 bans.

**No tolerance was widened and no seed was chosen.** The re-keying is required by the
specification, was fixed before the campaign ran, and the movement was classified afterwards.
