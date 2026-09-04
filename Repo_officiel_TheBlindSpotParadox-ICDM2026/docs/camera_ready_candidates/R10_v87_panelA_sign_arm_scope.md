# Camera-ready candidate — NO DEVIATION, clarification only: Figure 10 panel (A) carries one curve that is i.i.d. by construction and one that is evidence

| Field               | Value                                                                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply** <br> *NO DEVIATION — clarification only*                                                                    |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), Figure 10 caption (`fig:skew_robustness`), **line 567**                  |
| Trigger             | Acceptance notification, 14 November 2026                                                                                             |
| Evidence            | control C4 in `logs/R10_skew_robustness/exp_R10_skew_robustness.log`; `R10_skew_streams.csv`, columns `sign_identity` and `min_h`     |
| Register entry      | **none.** The caption's sentence is true; §perimeter keeps a formulation that is incomplete but not false out of `docs/DEVIATIONS.md` |
| Cost                | one clause in one caption; no numeral changes                                                                                         |
| Blocking dependency | shares line 567 with `R10_v87_caption_fpr_envelope.md`; the two search strings are **disjoint** and the two edits commute             |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being clarified — and what is *not* being corrected.** The caption reads

> \textbf{(A)} Conditional whiteness is preserved across extreme skewness.

and the statement is **true**: both curves of panel A sit at the nominal level across the whole
`xi` grid. What the caption does not say is that its two curves carry evidence of two different
strengths.

**The raw-sign curve is i.i.d. `Bernoulli(q)` by construction of the delivered code.** In
`Priorite_9_skew_robustness.py` the innovations are built as `eps_t = sqrt(h_t) · z_t` with
`h_t = max(ω + α eps_{t-1}² + β h_{t-1}, 1e-12) > 0` and the `z_t` drawn independently by
`fs_skew_t_standardized`, which the GARCH recursion never enters. Multiplying by a strictly
positive float cannot change a sign, so

```
1{eps_t > 0} == 1{z_t > 0}    bit-exactly
```

Control C4 asserts that identity on all **4 000** streams of the regenerated campaign: **0
disagreements**, with the smallest conditional variance observed at `7.27 × 10⁻³`, nine orders of
magnitude above the `1e-12` floor and `9.09` times the derived bound `ω = 8 × 10⁻⁴`. The raw sign
stream is therefore a sequence of independent Bernoulli draws whatever the volatility path does,
and its Ljung–Box rejection rate measures the **calibration of the Ljung–Box test**, not a property
of the data-generating process. It cannot fail, and a curve that cannot fail is not a stress test.

**The HoeffdingTree error curve is the proposition, and its evidence is a non-rejection.** That arm
runs a real online learner over the stream, so its whiteness is a claim about the pipeline rather
than an identity of the simulator. A non-rejection bounds nothing without the power of the
instrument, and the repository has already bounded it at this exact configuration: at `n = 8000`
and lag 20, `docs/DEVIATIONS.md` `R18-ljungbox-power` fixes the lag-1 autocorrelation the test
resolves with probability `0.8`. R10 opens no duplicate entry and cross-references R18 instead.

**Why this does not reach the register.** The perimeter filter admits an entry only when a printed
statement is **formally contradicted**. Panel A's sentence is not contradicted: whiteness *is*
preserved, on both arms, at every grid point. What is incomplete is the strength attributed to the
figure, and an incomplete-but-true formulation is a camera-ready matter, not a register matter.
The measurement is reported in `docs/sections/R10.md` and in `docs/audits/AUDIT_R10.md`.

## Edit — Figure 10 caption, line 567

**Verification of the search string.** The block below is quoted from `articleB_whitening_v87.tex`
**line 567** verbatim and occurs **exactly once** in the file (`grep -Fc` returns `1`). It is
disjoint from the string `R10_v87_caption_fpr_envelope.md` searches in the same caption. Verify
once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
\textbf{(A)} Conditional whiteness is preserved across extreme skewness.
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
\textbf{(A)} Conditional whiteness is preserved across extreme skewness. The raw-sign curve is i.i.d.\ by construction of the simulator ($\varepsilon_t = \sqrt{h_t}\,z_t$ with $h_t > 0$, so $\mathbf{1}\{\varepsilon_t > 0\} = \mathbf{1}\{z_t > 0\}$) and reads as a calibration check; the classifier-error curve is the stress test.
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**This is not a claim that panel A is wrong.** Both curves are correctly measured and correctly
plotted, and the sentence the caption prints is true. The clause added above names which of the two
carries the stress test.

**This is not a claim about the theorem.** The identity `1{eps_t > 0} = 1{z_t > 0}` is a property
of the *simulator*, which implements exactly the scale model the proposition assumes. It says
nothing about whether the proposition holds on data, and no text derived from this candidate may
say that it does.

**The clause must not be applied together with a weakening of panel A.** The panel stays as it is:
removing the raw-sign curve would remove the calibration check that makes the other curve readable.
