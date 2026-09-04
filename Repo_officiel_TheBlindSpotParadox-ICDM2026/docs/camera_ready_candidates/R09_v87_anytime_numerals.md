# Camera-ready candidate — the three Monte-Carlo numerals of L243 and Figure 9A move under the re-keying

| Field               | Value                                                                                                                                                     |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                                                                 |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), `sec:exactness` L243 and the Figure 9 caption L559 panel **(A)**                              |
| Trigger             | Acceptance notification, 14 November 2026                                                                                                                 |
| Evidence            | `results/R09_eprocess_anytime/data/R09_validity_stopping.csv`, `results/R09_eprocess_anytime/data/R09_eprocess_race.csv`, `logs/R09_eprocess_anytime/exp_R09_eprocess_anytime.log` |
| Register entry      | `docs/DEVIATIONS.md`, `R09-campaign-redraw` — Class A, **D2**                                                                                              |
| Cost                | three numerals; no sentence is restructured and no claim changes                                                                                          |
| Blocking dependency | shares L243 with `R09_v87_stream_counts.md` and `R09_v87_delay_parity_scope.md`, and L559 with all three siblings; the search strings are **disjoint** and the edits commute |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**Why this candidate exists at all.** Preamble §S6 requires the entropy of every campaign to be
derived from a 128-bit key on the **role and index alone**, and the submitted script keys its whole
campaign off `master_seed = 42027` through a `SeedSequence.spawn` tree. Migrating to
`get_deterministic_seed` / `seed_sequence_for` / `rng_for` redraws the campaign by construction, so
every Monte-Carlo numeral is expected to move. This file records the three that move **at v87's own
printing precision**; the ones that do not are in `AUDIT_R09.md`'s classification table. This is the
`R05-campaign-redraw`, `R11-regenerated`, `R13-campaign-redraw` and `R07-campaign-redraw` situation
and nothing else.

## What moved, and by how much

| v87 site                    | printed | regenerated              | witness                  | z of the difference     |
| --------------------------- | ------- | ------------------------ | ------------------------ | ----------------------- |
| L243 / Fig. 9A peeking FPR  | `18\%`  | **`19.9\%`** (`0.1988`)  | `18.0\%` (`0.1801`)      | `+4.77` — see below     |
| L243 MIX delay at `η = 0.10`| `409`   | **`410`** (`410.4027`)   | `409` (`409.1131`)       | `+0.24`                 |
| L243 CUSUM delay at `η=0.10`| `539`   | **`533`** (`532.8512`)   | `539` (`538.8052`)       | `−0.44`                 |

The two delays move by a quarter and by four tenths of the standard error of their own difference —
an ordinary redraw of a 2 000-stream conditional mean. The false-alarm rate does not, and the
mechanism is identified rather than guessed.

**The `18\%` moves because `λ*` moved one lattice step.** The CUSUM statistic increments by
`+0.4` or `−0.6`, so `max_M` lives on a `0.2` lattice and the calibrated threshold can only sit on
that lattice. `np.quantile(max_M, 0.95)` returned `11.4` on the submitted campaign's
`N_CAL = 50 000` calibration streams and `11.2` on the regenerated ones — **adjacent lattice
points**, both legitimate outputs of the same estimator on its own sample. The two thresholds
realise almost the same level at the horizon they were calibrated for (`0.0504` submitted,
`0.05034` regenerated), which is why L243's `5\%` reproduces; peeking to `4H` is where a one-step
difference in the threshold is amplified:

| quantity                                  | submitted | regenerated | ratio   |
| ----------------------------------------- | --------- | ----------- | ------- |
| `λ*` at `α = 0.05`                        | `11.4`    | `11.2`      | one step|
| level achieved on the calibration sample  | `0.0504`  | `0.05034`   | `0.999` |
| level over `[1, H]` on the held-out sample| `0.0493`  | `0.05345`   | `1.084` |
| peeking rate over `[1, 4H]`               | `0.1801`  | `0.1988`    | `1.104` |

Four of the seven levels moved one lattice step (`α =` `0.07`, `0.05`, `0.035`, `0.01`); three did
not. **R09 does not separate the threshold channel from the fresh-draw channel** — that would need
the regenerated `H₀` sample replayed at the submitted threshold, which is not an experiment v87
contains — and preamble §S4.5 forbids asserting a decomposition the measurement does not establish.
What is established is that the two campaigns calibrate to the same level and place the threshold
one lattice step apart, and that `R03-cusum-nominal-level` and `R07-lambda-star-estimator` already
record the same estimator behaviour on the same statistic.

**Every claim the three numerals support holds.** The fixed-horizon CUSUM's realised rate still
climbs by roughly a factor of four under continued watching; the mixture still sits at or below `α`
at all seven levels (ratios `0.945`–`1.000`); the mixture is still the faster arm at `η = 0.10`; and
the CUSUM peeking rate still exceeds the mixture's at all seven levels, at `22.9`–`68.5` paired
standard errors. **The direction of every comparison is unchanged and only the digits move.**

## Edit 1 — `sec:exactness` L243, the peeking rate

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 243** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`). It is disjoint from the strings the sibling candidates search.

<<< RECHERCHER
~~~~~~~~~latex
realized false-alarm rate to $18\%$ by $4H$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
realized false-alarm rate to $20\%$ by $4H$
~~~~~~~~~
>>> FIN DU BLOC

## Edit 2 — Figure 9 caption L559, panel (A)

**Verification of the search string.** Quoted from `articleB_whitening_v87.tex` **line 559**
verbatim; `grep -Fc` returns `1`.

<<< RECHERCHER
~~~~~~~~~latex
fixed-horizon CUSUM climbs to $18\%$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
fixed-horizon CUSUM climbs to $20\%$
~~~~~~~~~
>>> FIN DU BLOC

## Edit 3 — `sec:exactness` L243, the two delays

**Verification of the search string.** Quoted from `articleB_whitening_v87.tex` **line 243**
verbatim; `grep -Fc` returns `1`. Note the escaped space `vs.\ ` — the string must be searched
literally, not retyped.

<<< RECHERCHER
~~~~~~~~~latex
($409$ vs.\ $539$ steps at $\eta = 0.10$)
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
($410$ vs.\ $533$ steps at $\eta = 0.10$)
~~~~~~~~~
>>> FIN DU BLOC

## What must not be done with this candidate

**Do not apply Edit 1 without Edit 2, or the reverse.** They are the same quantity printed twice,
in the body and in the caption, and a manuscript that prints `18\%` in one and `20\%` in the other
is worse than one that prints the stale value in both.

**Do not restate `20\%` as an exact figure.** `0.1988` on `20 000` streams carries a Wilson interval
of `[0.1933, 0.2044]`, and one lattice step in `λ*` moves it by two points. The sentence is about a
fourfold climb under continued watching, and the rounded numeral is an illustration of it.

**Do not "restore" `λ* = 11.4` to recover `18\%`.** The threshold is the output of the estimator
the manuscript describes, applied to the calibration sample the re-keyed campaign drew. Choosing
the lattice point that reproduces a published numeral would be the tolerance-widening preamble §S4.8
bans, in its most direct form.

**Do not read the `409 → 410` and `539 → 533` moves as a change in the race.** Both are conditional
means over the streams that alarmed in `(τ, H]`, at detection rates of `97.60%` and `97.10%`; the
mixture is the faster arm in both campaigns and by a larger margin in the regenerated one. The
conditioning itself is the subject of `R09_v87_delay_parity_scope.md`, not of this file.
