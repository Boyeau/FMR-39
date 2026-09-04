# Camera-ready candidate — the two load-bearing non-rejections do not state the power of the test that produced them

| Field               | Value                                                                                                     |
| ------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                                 |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-26, frozen), `sec:validity_map` L290 and `sec:real_world` L318 |
| Trigger             | Acceptance notification, 14 November 2026                                                                 |
| Evidence            | `results/R18_ljungbox_power/data/R18_detectable_amplitude.csv`, `R18_applied_to_sign_streams.csv`          |
| Register entry      | `docs/DEVIATIONS.md`, `R18-ljungbox-power`                                                                |
| Cost                | +45 words across two sentences; no number in the body text changes                                        |
| Blocking dependency | none — both edits add a qualification and remove no claim                                                 |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed: streams after R18 may touch the same two sentences, and
applying a correction before the inventory closes guarantees reapplying it later.

**What is being corrected.** Not a number and not a claim: the absence of the quantity that
gives a non-rejection its weight. Both sentences below rest on a Ljung–Box test failing to
reject, and neither states what that test could have rejected. R18 measures it:

| configuration                              | `rho_80`, the lag-1 autocorrelation detected with probability 0.8 |
| ------------------------------------------ | ------------------------------------------------------------------ |
| `n = 8000`, lag 20, level 5% (Figure 6)    | **0.051** (measured `0.0506`, 95% CI `[0.0494, 0.0518]`)          |
| `n = 2000`, lag 20, level 5%               | **0.102** (measured `0.1023`, 95% CI `[0.0992, 0.1050]`)          |
| `n = 32000` / `n = 128000`                 | `0.0256` / `0.0128`                                               |

The measured lag-1 autocorrelation of the streams these sentences describe is `0.0008` at worst
over 33 GARCH penalties and 33,000 streams — between 60 and 70 times below `rho_80`, at which
amplitude the instrument's power is `0.050`, its own level. **The non-rejections are therefore
consistent with the property the manuscript states and equally consistent with any
autocorrelation below `0.051`**, and the sentences as written do not let a reader tell the two
apart.

R18 neither supports nor contradicts the whitening property. What it removes is the reading
under which these two sentences bound the autocorrelation of a binary stream by something
smaller than `rho_80`.

## Edit 1 — `sec:validity_map`, the strict-whiteness sentence

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 290** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`). Verify once more before applying, as a matter of routine.

<<< RECHERCHER
~~~~~~~~~latex
yet the binary error stream stays strictly white up to $\Gamma = 200$
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
yet the binary error stream shows no detectable autocorrelation up to $\Gamma = 200$, at a lag-20 Ljung--Box test whose power against a lag-1 autocorrelation of $0.051$ is $0.8$ at this horizon
~~~~~~~~~
>>> FIN DU BLOC

"Stays strictly white" states a property; the measurement supporting it is a non-rejection, and
"shows no detectable autocorrelation" is what the measurement licenses. The replacement is also
the wording the Figure 6 caption already uses at line 286, so the two sites become consistent
with each other.

## Edit 2 — `sec:real_world`, the licensing sentence

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` **line 318** verbatim and occurs **exactly once** in the file
(`grep -Fc` returns `1`). The leading comma is part of the match and is what makes it unique.

<<< RECHERCHER
~~~~~~~~~latex
, licensing the filter.
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
, licensing the filter at a resolution of $0.05$--$0.10$ in lag-1 autocorrelation, which is the amplitude a single lag-20 test detects with probability $0.8$ on warm-up windows of this length.
~~~~~~~~~
>>> FIN DU BLOC

The four ETF tests run on pre-2020 daily warm-up windows, which are bracketed by the two
shortest horizons R18 measures (`n = 2000` and `n = 8000`), so `rho_80` at those sites lies
between `0.051` and `0.102`. Each asset is read **once**, not over 1,000 streams, so the
per-asset statement is a single draw from the power curve rather than a rate on it.

## A second site is named and deliberately not bundled

L278 and the Figure 6 caption at L286 report the **size** of the same test — "the binary errors
hold the nominal level in every regime ($3.3$--$5.0\%$; $4.4\%$ pooled)" and "show no detectable
autocorrelation in any GARCH regime". A size statement is not a non-rejection, and qualifying it
would mean adding the power figure to a caption that currently carries a rate; that is a
question about what the figure reports, not about what these two sentences claim, and it should
be decided together with whatever revision Figure 6 receives. `R11_v87_figure11_caption.md`
treats a separable edit the same way.

## What must not be done with this candidate

The bound is stated for one family of alternatives, `rho(k) = rho_1^k`, which is the family the
symmetric two-state chain generates. It must not be quoted as a bound on dependence in general:
a departure concentrated at a single high lag, or one that leaves the linear autocorrelations at
zero, has a different power curve and R18 does not measure it. `docs/sections/R18.md` states
that limit and any camera-ready sentence derived from this file inherits it.
