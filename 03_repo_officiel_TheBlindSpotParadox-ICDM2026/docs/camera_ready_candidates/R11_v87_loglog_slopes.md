# Camera-ready candidate — the three log-log slopes have no traceable origin and no stated domain

| Field               | Value                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                 |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:universality`            |
| Trigger             | Acceptance notification, 14 November 2026                                                 |
| Evidence            | `data/reference/R11/Priorite_12_multi_detector.py` l.514-531, its log; `R11_slope_fits.csv` |
| Register entry      | `docs/DEVIATIONS.md`, `R11-pht-slope`                                                     |
| Cost                | +14 words against the submitted sentence                                                  |
| Blocking dependency | none — Figure 11 is unaffected, only the numerals in the body text                        |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being corrected.** Two things about three numerals: where they come from, and what
they are fitted on.

**They are not in the submitted chain.** `plot_figure_20` computes a **linear** regression:

```python
slope, intercept, _, _, _ = stats.linregress(valid["Gamma"], valid[f"ADD_{det}"])   # l.524
print(f"  {det}: {slope:.3f}")                                                       # l.525
```

and the submitted log prints only what that produced:

```
Data ADD ~ Gamma slopes (OLS):
  CUSUM: 26.602
  PHT: 37.228
  ADWIN: 4.747
```

The published `0.86 / 1.09 / 0.47` are **log-log** slopes. They appear in no CSV, no log and no
script of the submitted campaign; they were computed outside the chain. R11 reproduces the
linear fit as well, so the two quantities cannot be confused: the linear slopes come back close
to the submitted ones, which is what makes the port credible, and the log-log slopes are emitted
as macros computed in memory with a seed-cluster standard error and an explicit domain.

**The PHT slope is fitted on a strict subset of the grid, and the manuscript does not say so.**
v87's own next sentence explains why — "beyond `Γ ≈ 75` its adaptive reference absorbs the shift
faster than the inflated threshold reacts, collapsing detection below `50%`" — so the PHT has no
usable delay at the top of the range. Its slope is therefore fitted on the points that survive
the `DetRate ≥ 0.5` censor, and **the delays retained there are conditional on detection and
biased downward by selection on survival**. The CUSUM and ADWIN are not censored anywhere on the
grid, so the restriction is specific to the running-mean detector and not a property of the
campaign. No extrapolation outside that domain is admissible, and the exact counts are in
`R11_slope_fits.csv` (`n_points`, `domain`).

**A sensitivity arm is also emitted.** The grid's lowest point is an ARCH(1) process at the
attainable penalty floor rather than an i.i.d. one, and R05 recorded a scaling-law intercept
hooked on exactly such a point. The macros `\RElevenDataSlope{Cusum,Pht,Adwin}ExLowGamma` refit
above `Γ > 1.5`, which removes that point and nothing else.

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` line 298 verbatim and occurs exactly once in the file. Verify once
more before applying.

<<< RECHERCHER
~~~~~~~~~latex
(log-log slopes $0.86$ CUSUM, $1.09$ PHT, $0.47$ ADWIN)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
(log-log slopes $0.86$ CUSUM and $0.47$ ADWIN over the full $\Gamma$ grid; $1.09$ PHT over the points where its detection rate stays above $50\%$, where the delays are conditional on detection)
~~~~~~~~~
>>> FIN DU BLOC

**The regenerated values are in `docs/sections/R11.md`** with their standard errors and domains.
They are not proposed as replacements here: re-keying the entropy to 128 bits redraws the whole
campaign, so every Monte-Carlo value moves, and which campaign a camera-ready revision should
quote is an authors' decision rather than this repository's.
