# Camera-ready candidate — the delay comparison of Figure 9B is conditional on detection

| Field               | Value                                                                                                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Status**          | **PARKED — do not apply**                                                                                                                                         |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), Figure 9 caption L559 panel **(B)** and `sec:exactness` L243                                          |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                                         |
| Evidence            | `results/R09_eprocess_anytime/data/R09_eprocess_race.csv` (`DetRate` beside `ADD`), control C4 in `logs/R09_eprocess_anytime/exp_R09_eprocess_anytime.log`         |
| Register entry      | `docs/DEVIATIONS.md`, `R09-add-conditioning` — Class A, **no severity**                                                                                           |
| Cost                | +9 words in the caption, +6 in the body; no number changes                                                                                                        |
| Blocking dependency | shares L559 with `R09_v87_stream_counts.md` and `R09_v87_arl0_censoring.md`; the search strings are **disjoint** and the three edits commute                       |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being corrected.** Both delay claims survive, and this candidate does not challenge
either. Panel B's caption reads "MIX matches CUSUM speed for moderate drifts ($\eta \le 0.10$)";
L243 reads "at matched false-alarm rate and moderate drift the mixture detects at least as fast as
the fixed-horizon CUSUM ($409$ vs.\ $539$ steps at $\eta = 0.10$), ceding ground only for abrupt
shifts". What neither says is that the delay plotted is a **conditional** mean — over the streams
that alarmed inside `(TAU, H]` — and that the two arms condition on **different events**.

**The rates the conditioning hides.** At `α = 0.05`, the detection rate over the drift grid:

| `η`    | CUSUM `DetRate` | MIX `DetRate` | ratio  |
| ------ | --------------- | ------------- | ------ |
| `0.02` | `0.0570`        | `0.1615`      | `2.83` |
| `0.04` | `0.2000`        | `0.7385`      | `3.69` |
| `0.06` | `0.5380`        | `0.9715`      | `1.81` |
| `0.10` | `0.9710`        | `0.9760`      | `1.01` |

At `η = 0.04` the mixture detects `73.9%` of streams and the CUSUM `20.0%`. The mixture's
conditional mean therefore averages over the hard streams the CUSUM never reaches at all, and it
comes out **higher** — `+129` steps — while the mixture is the arm that found them. Reading panel B
at the two smallest drifts as "CUSUM is faster" inverts the ordering the data support.

**The selection-free comparison, and the direction it gives.** The repository's control C4 fixes
this by measurement rather than by argument, with a matched-detection-rate quantile: at each `η`,
set `q = min(p_CUSUM, p_MIX)` and compare the `q`-quantile of each arm's alarm-time distribution
with non-detections at `+∞`. This asks "to reach the same detection rate, which arm needs fewer
steps", conditions on nothing, and is the same iso-rate logic the paper's own iso-FPR race uses.
The answer is the caption's, and more strongly than the caption claims:

| `η`    | `q`      | CUSUM `q`-quantile | MIX `q`-quantile | MIX − CUSUM | paired bootstrap 95% |
| ------ | -------- | ------------------ | ---------------- | ----------- | --------------------- |
| `0.02` | `0.0570` | `2404`             | `1292`           | **`−1112`** | `[−1242, −964]`       |
| `0.04` | `0.2000` | `2485`             | `981`            | **`−1504`** | `[−1562, −1427]`      |
| `0.06` | `0.5380` | `2473`             | `902`            | **`−1571`** | `[−1601, −1541]`      |
| `0.10` | `0.9710` | `2420`             | `959`            | **`−1461`** | `[−1583, −1076]`      |

The mixture is faster at every drift on the grid, and at `η = 0.02` and `0.04` — the two points
where the *marginal* conditional mean says the opposite — the paired bootstrap interval excludes
zero. **The caption's claim holds; the marginal curve panel B plots is what does not show it.**

**A second reading disagrees at the smallest drift, and that is reported rather than resolved.**
On the common-detection subset — the `70` of `2 000` streams both arms find at `η = 0.02` — the
paired mean difference is `+114` steps in the CUSUM's favour (paired SE `53`). That subset is the
intersection of two detection events whose rates differ by a factor of `2.8`; its composition
depends on both detectors, so it is itself a selected sample and cannot settle the question. Both
readings ship; the disagreement is the finding, and it is another reason to say in the caption what
the delay is conditional on.

## Edit 1 — Figure 9 caption L559, say what the delay is conditional on

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 559** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`). It is disjoint from the strings the two sibling candidates search.

<<< RECHERCHER
~~~~~~~~~latex
MIX matches CUSUM speed for moderate drifts ($\eta \le 0.10$)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
MIX matches CUSUM speed for moderate drifts ($\eta \le 0.10$); delays are conditional on detection within $(\tau, H]$, and at $\eta \le 0.04$ the two arms detect at rates differing by a factor of three, so the curves there are not comparable point by point
~~~~~~~~~
>>> FIN DU BLOC

## Edit 2 — `sec:exactness` L243, scope "ceding ground"

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 243** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`).

<<< RECHERCHER
~~~~~~~~~latex
ceding ground only for abrupt shifts
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
ceding ground only for abrupt shifts, where both arms detect nearly every stream and the conditional delay is therefore comparable
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**This is not a claim that the mixture is slower anywhere.** Under the selection-free instrument it
is faster at every drift on the grid. What is corrected is that panel B's curve is a conditional
mean, and that at the two smallest drifts the conditioning is severe enough to invert the visual
ordering.

**Do not replace panel B's curve with the matched-rate quantile.** That would be a different
figure from the one v87 published, and the perimeter of this repository is strictly the content of
v87. The matched-rate reading belongs in `AUDIT_R09.md` and in the caption's qualifier, not in the
plotted series.

**Do not cite the common-detection subset as the correction.** It is a second reading and it
disagrees with the primary one at `η = 0.02`. A camera-ready sentence that leaned on it would be
resting on a sample selected by both detectors at once.

**`ADD` is conditional in the submitted campaign too.** `add_c` and `add_m` are means over
`(fa > TAU) & (fa <= H)` in `data/reference/R09/Priorite_22_eprocess_anytime.py` l.461-462, at a
detection rate of `0.9855` for the `409` figure — a `1.5%` censoring rate at the published operating
point. The `409` and `539` v87 prints are delays conditional on detection within the horizon. That
is what v87 measured; this candidate says so, it does not change it.
