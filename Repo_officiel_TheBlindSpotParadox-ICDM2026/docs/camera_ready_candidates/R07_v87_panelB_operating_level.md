# Camera-ready candidate — Figure 7 panel B operates at the upper attainable level, not at the one its parenthetical names

| Field               | Value                                                                                                                         |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                                     |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), Figure 7 caption, **line 543**                                    |
| Trigger             | Acceptance notification, 14 November 2026                                                                                     |
| Evidence            | `results/R07_estimated_mean/data/R07_lattice_exact_law.csv` (`record_type = float_drift`) and `R07_estmean_lb_fpr.csv`         |
| Register entry      | `docs/DEVIATIONS.md`, `R07-panelB-operating-level` — Class A, no severity                                                     |
| Cost                | +14 words in one clause; no number in the body text changes                                                                   |
| Blocking dependency | shares the caption with `R07_v87_figure7_exactness.md`; the two search strings are **disjoint** and the two edits commute      |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being corrected.** No number is wrong. The caption places two true statements next to
each other and a reader joins them into a false one.

> \textbf{(B)} \textsc{Concept} FPR at threshold $\lambda^{\star} = 11.4$ (exact lattice level
> $4.29\%$ …). … **while all rolling-OLS arms ($n \in [125, 1000]$) match oracle false-alarm
> control.**

`λ* = 11.4` does carry a lattice level of `4.29 %` — under the *mathematical* `M_H > λ*`. Panel B
does not operate there. L241's own footnote already says why:

> The boundary case is not cosmetic: floating-point accumulation leaves $M_H$ a few ulps above its
> exact lattice value, so the implemented test $M_H > \lambda^{\star}$ is the mathematical
> $M_H \geq \lambda^{\star}$; we report the level actually delivered.

R07 measured that statement instead of assuming it. On R07's own `10 000` `ORACLE` sign streams —
fair coins under H₀ by the proposition the paragraph is testing — the accumulated `M` sits **above**
its exact lattice value on `9 652` streams, **below** on `137` and **exactly on it** on `211`. Of
the `88` streams landing exactly on `λ*`, all `88` are counted as exceedances. Over the `35 000`
fair-coin streams measured — the `ORACLE`, calibration and validation sets — the implemented test
**coincides exactly** with `M ≥ λ*`, with `0` disagreements against `267` against `M > λ*`, so the
footnote holds as written. **What the footnote does not say is which of the two attainable levels
the panel therefore operates at**, and that is what this candidate adds.

| operator                             | realised level, `10 000` `ORACLE` streams | exact law |
| ------------------------------------ | ------------------------------------------ | --------- |
| float `M > λ*`, i.e. what runs        | **`5.16 %`**                               | —         |
| exact `M > λ*` on the lattice         | `4.28 %`                                   | `4.3428 %` |
| exact `M ≥ λ*` on the lattice         | `5.16 %`                                   | `5.1021 %` |

On `25 000` independent fair-coin calibration and validation streams the delivered level is
`5.064 %`. The `ORACLE` arm of panel B sits at `5.16 %`, which is `+0.26` standard errors from the
delivered level and `+3.69` from the `4.29 %` the parenthetical names. **Panel B operates above the
`5 %` nominal that L241's stated rule — "the nearest attainable level at or below nominal" —
promises**, and the caption gives the reader the level below it.

**A second fact about the same band, which the same clause invites.** Under the mandated
common-random-numbers plan the `ORACLE` arm is *exactly* `φ`-invariant — in the DGP, `h[t]` and
`ε[t]` never reference `φ`, so the oracle residual is `ε_curr` at every `φ` — and the seven
`ORACLE` cells are bit-identical. The reference band against which "all rolling-OLS arms match
oracle false-alarm control" is asserted is carried by `10 000` effective trajectories, not `70 000`
(`R07-oracle-band-precision`). That does not weaken the claim, which holds at `4` paired standard
errors on every one of the 28 OLS cells, but it is what the band is worth.

## Edit — Figure 7 caption, line 543

**Verification of the search string.** The block below is quoted from `articleB_whitening_v87.tex`
**line 543** verbatim and occurs **exactly once** in the file (`grep -Fc` returns `1`). It is
disjoint from the string `R07_v87_figure7_exactness.md` searches in the same caption. Verify once
more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
while all rolling-OLS arms ($n \in [125, 1000]$) match oracle false-alarm control
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
while all rolling-OLS arms ($n \in [125, 1000]$) match oracle false-alarm control, both at the level the implemented test delivers on the lattice boundary---$5.2\%$ here, the upper of the two attainable levels, not the $4.29\%$ of the mathematical $M_H > \lambda^{\star}$
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**The threshold must not be moved to recover `4.29 %`.** `λ* = 11.4` is what L241's stated rule
selects on the exact law, and it is bit-identical to the literal v87 prints. What differs is the
comparison the implementation performs on the boundary, and changing the threshold to compensate
for a floating-point artefact would hide the artefact rather than report it.

**The `5.2 %` must not be presented as the level of the arms.** It is the level of the *operator*,
measured on fair-coin streams; the `ORACLE` and rolling-OLS arms happen to sit there because the
proposition holds, which is the point of the figure.

**This candidate does not correct the `4.29 %` numeral.** That numeral is R08's — L241 sources it
to a `2 × 10⁵`-stream campaign the repository's stream map assigns to R08 — and the separate
question of whether the caption should call it "exact" is
`R07_v87_figure7_exactness.md`.
