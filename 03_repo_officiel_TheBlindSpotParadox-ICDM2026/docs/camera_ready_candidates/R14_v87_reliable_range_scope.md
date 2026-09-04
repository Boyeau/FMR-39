# Camera-ready candidate — NO DEVIATION, clarification only: "the reliable range" is never defined, and the mean is taken over seven grid points

| Field               | Value                                                                                                                       |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                                   |
|                     | **NO DEVIATION — clarification only**                                                                                       |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:misspecification` L345 and the Figure 16 caption L635     |
| Trigger             | Acceptance notification, 14 November 2026                                                                                   |
| Evidence            | `results/R14_crypto_isofpr/data/R14_crypto_isofpr_race.csv`, columns `DetRate` and `add_reliable`                           |
| Register entries    | **none** — no printed value is contradicted; §S8's scope filter keeps this out of `docs/DEVIATIONS.md`                      |
| Cost                | +17 words in the body, +9 in the caption; no number changes                                                                 |
| Blocking dependency | shares L345 with `R14_v87_synthetic_control_numerals.md`; the two search strings are **disjoint** and the two edits commute |

**Why this is not applied now.** The manuscript is under review and cannot be edited.

**Nothing here is false.** Both sentences are true as written. What they omit is the definition of
the set the aggregate is taken over, and a reader holding the artefacts cannot reproduce `mean 0.87`
without guessing it.

**What the caption defines, and what it does not.** The L635 caption defines the *marker*
convention — "hollow markers are unreliable points, $\mathrm{DetRate} < 0.9$" — which is a rule on a
single arm at a single magnitude. The body then reports a mean of a **ratio of two arms**, and a
ratio is only computable where *both* arms detect. The operative set is therefore the magnitudes at
which both arms reach `DetRate ≥ 0.9`, which is a different rule from the one the caption states,
and the manuscript never says so. The distinction is not academic on this figure:

| `c`    | `Concept` `DetRate` | `Eco-L1` `DetRate` | hollow by the caption's rule | enters the mean |
| ------ | ------------------- | ------------------ | ---------------------------- | --------------- |
| `0.20` | `0.8396`            | `0.7925`           | both                         | no              |
| `0.25` | **`0.9811`**        | `0.8962`           | `Eco-L1` only                | **no**          |
| `0.35` | `1.0000`            | `1.0000`           | neither                      | yes             |

At `c = 0.25` the `Concept` arm is drawn **filled** — it clears the caption's threshold — while the
magnitude contributes nothing to the mean, because its `Eco-L1` counterpart does not. A reader who
takes "the reliable range" to be "the magnitudes with filled markers" reads a range that begins at
`c = 0.25` and computes a different mean from the one printed.

**The set the published numbers use is seven magnitudes**, `c ∈ {0.35, 0.5, 0.6, 0.75, 1.0, 1.25,
1.5}`, on both `Real_BTC` and the `t₃₀` control. That is exactly the set the submitted script
hard-codes as the literal `c >= 0.35` in its own certification block, and the length of the seven
reference vectors it carries; the repository derives it from the `DetRate ≥ 0.9` rule instead and
verifies against the submitted CSV that the two selections coincide.

## Edit 1 — `sec:misspecification` L345, name the set the mean is taken over

**Verification of the search string.** Quoted from `articleB_whitening_v87.tex` **line 345**
verbatim; `grep -Fc` returns `1`. It is disjoint from the string
`R14_v87_synthetic_control_numerals.md` searches on the same line. Verify once more before
applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
the sign filter leads across the reliable range: the delay ratio runs from $0.74$ at $c = 0.35$ to parity ($1.01$) at $c = 1.5$, mean $0.87$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
the sign filter leads across the reliable range---the seven magnitudes $c \ge 0.35$ at which \emph{both} arms detect in at least $90\%$ of onsets: the delay ratio runs from $0.74$ at $c = 0.35$ to parity ($1.01$) at $c = 1.5$, mean $0.87$ over those seven
~~~~~~~~~
>>> FIN DU BLOC

## Edit 2 — Figure 16 caption L635, distinguish the marker rule from the aggregation rule

**Verification of the search string.** Quoted from **line 635** verbatim; `grep -Fc` returns `1`,
and disjoint from Edit 1.

<<< RECHERCHER
~~~~~~~~~latex
leads the honestly standardized residual (\textsc{Eco-L1}) across the reliable range, converging to parity at $c = 1.5$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
leads the honestly standardized residual (\textsc{Eco-L1}) across the reliable range---the magnitudes at which \emph{both} arms are filled---converging to parity at $c = 1.5$
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**This candidate opens no register entry and must not acquire one.** Preamble §S8 admits a
clarification of a true but incomplete formulation into this directory on the explicit condition
that it carries none; the wording is imprecise, not false, and the pairwise rule is forced by
arithmetic rather than chosen — a ratio of two delays does not exist where one arm does not detect.

**It must not be merged with `R14_v87_synthetic_control_numerals.md`.** That candidate corrects
three numerals under a registered D2. Attaching a numerical correction to a clarification makes the
reason for each unreadable, and the two carry different evidential status.

**No revision may claim the unreliable cells were excluded to improve the result.** They are
excluded because an `ADD` conditional on a detection rate below `0.9` is an average over a
selected subset of onsets, and the direction of that selection is not signed: on `Real_BTC` the
excluded magnitudes are the four smallest drifts, where **both** arms are censored. Their rows ship
in the CSV and are drawn on the figure.
