# Camera-ready candidate — the census is not the output of the dating algorithm the sentence names

| Field               | Value                                                                                                          |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                      |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:real_world` L329                             |
| Trigger             | Acceptance notification, 14 November 2026                                                                      |
| Evidence            | `results/R16_regime_census/data/R16_regime_census_strict_ps.csv` (48 rows), `R16_regime_census.csv` (66 rows)  |
| Register entry      | `docs/DEVIATIONS.md`, `R16-dating-misdescription` — Class A, **D3**                                            |
| Cost                | +21 words in one sentence; **no number in the paper changes**                                                  |
| Blocking dependency | none — the edit corrects a method description and touches no value                                             |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed: streams after R16 may touch the same sentence, and applying a
correction before the inventory closes guarantees reapplying it later.

**What is being corrected.** The description of the dating, not a result. Every number the
sentence introduces reproduces exactly — 66 phases, 53 of 66 at the permissive budget, 52 on the
sign arm, 64 at one false alarm per year — and the regenerated census is bit-identical to the
submitted campaign's `protocol_10b_regime_census_refined.csv` on all 19 shared columns.

What does not hold is that a Pagan–Sossounov dating of the four streams produces those 66 phases.

| dating actually run on the four streams                                       | phases | out of budget, `gamma = 20` |
| ------------------------------------------------------------------------------ | ------ | --------------------------- |
| Pagan–Sossounov on all four, no substitution (`--dating strict_ps`)            | **48** | 38 (79.2 %)                 |
| **Pagan–Sossounov on PFF, VNQ, BWX; Lunde–Timmermann on SPY** — the published  | **66** | **53 (80.3 %)**             |
| Lunde–Timmermann wherever `check_sanity` fails, i.e. all four (`--dating symmetric`) | 102 | 75 (73.5 %)                 |

The mechanism is in the delivered code, at `Priorite_16_regime_census.py:233-238`: `check_sanity`
is evaluated on SPY's Pagan–Sossounov MACRO dating, it fails, and the MACRO turning points of
that one stream are replaced by `lunde_timmermann(lambda_1=0.15, lambda_2=0.15)`. The delivered
script logs it —
`WARNING | [SPY] Sanity check P-S failed. Fallback to Lunde-Timmermann for MACRO.`, line 3 of
`data/reference/R16/Priorite_16_regime_census.log`. **The script is not silent; the sentence
is.** Two of its clauses are affected:

- "**Pagan--Sossounov** … dating … **of the four streams**" — the dating of one of the four
  streams, the one that contributes 30 of the 66 phases, is Lunde–Timmermann.
- "$66$ phases **after duration censoring**" — Lunde–Timmermann applies no duration censoring.
  Its shortest phase on SPY is **6** trading days; under strict Pagan–Sossounov the shortest SPY
  phase is **49**, and **21** across all four streams.

**What the sentence already gets right, and what this candidate keeps.** The same sentence
carries "the COVID-19 crash---too brief for the filter---**dated at the raw scale**". The raw
scale *is* the uncensored Lunde–Timmermann dating, and the COVID phase of L331 exists only under
it — strict Pagan–Sossounov censors it at `min_phase = 84`. The exception is therefore named;
the algorithm is not. **Whether that phrasing was meant to carry the substitution is not
established by any measurement, and this repository does not decide it.**

## Edit 1 — `sec:real_world`, the dating clause

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 329** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`). Verify once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
A retrospective multi-scale Pagan--Sossounov bull/bear dating~\cite{pagan_sossounov_2003} of the four streams (2000--2025; $66$ phases after duration censoring, the COVID-19 crash---too brief for the filter---dated at the raw scale)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
A retrospective multi-scale Pagan--Sossounov bull/bear dating~\cite{pagan_sossounov_2003} of PFF, VNQ and BWX, with SPY dated by the uncensored Lunde--Timmermann filter~\cite{lunde_timmermann_2004} at $\lambda_1 = \lambda_2 = 0.15$ because the Pagan--Sossounov dating of that stream censors the COVID-19 crash at its $84$-day minimum-phase rule (2000--2025; $66$ phases in all)
~~~~~~~~~
>>> FIN DU BLOC

The replacement states the two datings, names the stream each applies to, gives the reason the
code gives, and drops "after duration censoring" — which is true of the Pagan–Sossounov streams
and false of the substituted one. It adds a citation key, `lunde_timmermann_2004`, which must be
present in `articleB_biblio_v69.bib` before this edit is applied; the reference is already listed
in the header of `Priorite_16_regime_census.py`:

> Lunde, A. & Timmermann, A. (2004). "Duration dependence in stock prices: an analysis of bull
> and bear markets", *Journal of Business & Economic Statistics* 22(3), 253–273.

**No numeral in the sentence moves.** `66`, `53`, `80\%`, `52`, `64` and `97\%` are unchanged
and remain correct under the dating the replacement describes.

## A second option, if the substitution is to be removed rather than described

The alternative is to run strict Pagan–Sossounov on all four streams and republish the census.
This repository has computed that arm and ships it as
`results/R16_regime_census/data/R16_regime_census_strict_ps.csv`. It costs:

- the phase count moves `66 -> 48` and the out-of-budget count `53 -> 38`;
- the headline fraction moves `80.3\% -> 79.2\%`, which still prints as `80\%` at one
  significant figure but not at three;
- **the COVID paragraph L331 loses its subject.** The 23-day SPY crash is censored by
  `min_phase = 84`, so `\Delta q \approx -0.28`, the annualized Sharpe of `-6.0`, the divergence
  of `0.162` nats/day and the floors of `18.5` and `34` days all disappear with it, and the
  paragraph would have to be rewritten around a different phase or removed.

That is a substantially larger revision than Edit 1 and it is **not** what this candidate
proposes. It is stated so that the choice between describing the substitution and removing it is
made with both costs visible.

## What must not be done with this candidate

The 48-phase arm is a counterfactual, not a correction of the published numbers. It must not be
quoted as "the true census": it is what the dating algorithm the sentence names produces, and
that is exactly the point. Nor may the discrepancy be characterised as deliberate. Preamble
§S4.5 forbids attributing a cause or an intent that the measurement does not establish, and the
evidence is equally consistent with a description written from the design as intended rather
than as executed. `docs/sections/R16.md` states that limit and any camera-ready sentence derived
from this file inherits it.
