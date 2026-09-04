# Camera-ready candidate — NO DEVIATION, clarification only: the independence calibration already over-fires at `K = 1`, where there is no sign correlation to ignore

| Field               | Value                                                                                                                          |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                                      |
| Kind                | **NO DEVIATION — clarification only.** The caption's claim holds; no register entry is opened.                                 |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), Figure 17 caption **(A)**, `fig:cross_section`                     |
| Trigger             | Acceptance notification, 14 November 2026                                                                                      |
| Evidence            | `results/R15_cross_sectional/data/R15_panel_diagnostics.csv` (`FPR_naive`, `rho_sign_meas`, `K_eff_meas`, `q_hat_*`); `logs/R15_cross_sectional/exp_R15_cross_sectional_b.log`, "THE FPR_naive DECOMPOSITION, AND WHERE IT STOPS BEING IDENTIFIABLE" |
| Register entry      | **none.** The caption's mechanism is real and dominant; what is added is its baseline.                                          |
| Cost                | +11 words; no printed number changes                                                                                           |
| Blocking dependency | none; the search string is in panel A's sentence and is disjoint from the three panel-B candidates                             |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**What is being clarified.** The caption says the independence calibration "lets false alarms climb
toward `100\%` **by ignoring sign correlation** (`\hat\rho \approx 0.26`)". The climb is real and
the mechanism named is the dominant one. What the sentence implies and the design does not support
is that the *whole* excess is cross-sectional — because at `K = 1` there is no cross-sectional
correlation at all and the naive threshold already over-fires by a factor of two.

**The measurement at `K = 1`, which is an identity and not an estimate.** The panel carries
`T = 5154` days, an even number. Subtracting the temporal median leaves exactly `2577` strictly
positive and `2577` strictly negative returns, with no exact tie (asserted, control C1). At
`K = 1` the pooled statistic `P_t` is therefore `\pm 1/2` with mean `0`, variance `1/4`, and

    rho_sign_meas = 0.0      exactly, an identity of a one-stream panel
    K_eff_meas    = 1/(4 * 1/4) = 1.0   exactly

Yet the realized false-alarm rate of the independence threshold at that same `K = 1` is
**`10.4\%`** regenerated (`11.15\%` on the submitted campaign) — `2.1x` the nominal `5\%`. No
cross-sectional correlation exists there to be ignored, so that part of the excess is not
attributable to the mechanism the caption names.

**What the residual channel is, and what can be said about it.** The naive calibration draws from
`Binomial(K, 1/2)`, which fixes `P(z > 0) = 1/2` by assumption. The real recentred stream carries
some `q`, measured per held-out window on the `H_det` half against the `H_ref` median:
`q_hat = 0.5006 \pm 0.0231` at `K = 1` (mean `\pm` s.d. over 2000 windows, range
`[0.4480, 0.5627]`). The *dispersion* of `q` across windows, not its mean, is what a fixed-`q`
calibration cannot price — and it is a marginal property of a single series, present at every `K`.

**The decomposition is not identifiable under this design, and the correction says so rather than
asserting a mechanism.** `q_hat` and `rho_sign` both move with `K` along a single arm; no contrast
holds one fixed while the other varies. What the ten cells do establish is the boundary case and
the increment:

| `K`  | `FPR_naive` | increment over `K = 1` | `rho_sign_meas` |
| ---- | ----------- | ---------------------- | ---------------- |
| 1    | `0.1040`    | `+0.0000`              | `0.0000` (exact) |
| 5    | `0.5475`    | `+0.4435`              | `0.2577`         |
| 10   | `0.5940`    | `+0.4900`              | `0.2590`         |
| 20   | `0.9015`    | `+0.7975`              | `0.2881`         |
| 40   | `0.9955`    | `+0.8915`              | `0.2589`         |
| 97   | `1.0000`    | `+0.8960`              | `0.2602`         |

The cross-sectional channel accounts for the overwhelming majority of the climb — an increment of
`+0.90` against a baseline excess of `0.054` over nominal. **The caption's mechanism is the right
one and its magnitude is not in question.** The clarification is that the naive threshold is not a
correctly levelled baseline at `K = 1` either, so the curve does not start from `5\%`.

**Why this matters beyond bookkeeping.** The escape L376 prices is the *difference* between the
two calibrations. If a reader takes the naive arm as "correct except for correlation", the
bootstrap's contribution looks purely cross-sectional; in fact it also absorbs the marginal
mis-levelling, which is what makes it hold `5\%` at `K = 1` (`4.75\%` regenerated) where the naive
arm does not.

## Edit 1 — Figure 17 caption **(A)**, state the baseline

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` verbatim and occurs **exactly once** in the file (`grep -Fc` returns
`1`).

<<< RECHERCHER
~~~~~~~~~latex
An independence calibration lets false alarms climb toward $100\%$ by ignoring sign correlation
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
An independence calibration already over-fires at $K = 1$, where no sign correlation exists, and then lets false alarms climb toward $100\%$ by ignoring it
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**Do not report a decomposition.** The marginal and cross-sectional contributions to `FPR_naive`
cannot be separated from these ten cells, and any split printed from them would be an assertion
dressed as a measurement. What is reportable is the `K = 1` boundary case, where the
cross-sectional channel is exactly empty, and the increment `FPR_naive(K) - FPR_naive(1)`.

**Do not add an arm to identify it.** v87 describes no such arm and the scope filter of this
stream is strictly v87's content. A campaign that holds `q` fixed while `rho` varies is a
different experiment and would have to be reported as one.

**Do not weaken the caption's claim.** The cross-sectional increment reaches `+0.896` at `K = 97`
against a `K = 1` excess of `0.054` over nominal. Ignoring sign correlation is the mechanism, and
it dominates by more than an order of magnitude.

**Do not present `q_hat \approx 0.5006` as a directional edge.** It is a false-alarm diagnostic of
the calibration, measured on null windows with no injection; its distance from `1/2` is a fraction
of its own across-window dispersion, and nothing in this stream reads it as a signal.
