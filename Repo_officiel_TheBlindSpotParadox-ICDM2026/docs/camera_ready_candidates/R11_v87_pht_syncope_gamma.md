# Camera-ready candidate — the numeral locating the stochastic syncope

| Field               | Value                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                                                 |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen), `sec:universality`            |
| Trigger             | Acceptance notification, 14 November 2026                                                 |
| Evidence            | `R11_data_add_vs_gamma.csv`, `arm=as_submitted`, column `DetRate_PHT`                     |
| Register entry      | `docs/DEVIATIONS.md`, `R11-pht-syncope`                                                   |
| Cost                | one numeral                                                                               |
| Blocking dependency | none                                                                                      |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
deviation inventory is not closed.

**Why this is a separate candidate from `R11_v87_pht_gamma_rule.md`.** That file concerns the
`λ × Γ` rule's residual on the `Data` arm under `H_0` — a false-alarm quantity measured in
experiment A. This one concerns the *detection* collapse under `H_1` in experiment D. They are
different sentences of v87, different experiments and different hypotheses, and folding them
together would make one correction look like evidence for the other.

**What is being corrected.** A locating numeral. v87 says the PHT's detection collapses "beyond
`Γ ≈ 75`". On the regenerated grid the first point whose detection rate falls below `50%` sits
higher; the exact value is in `docs/sections/R11.md` and in the CSV cell named above.

**The phenomenon itself reproduces, and its mechanism is v87's own.** The PHT subtracts a running
mean of the stream it is watching. On a `Data` stream whose threshold has been inflated by `Γ`,
that reference absorbs the post-onset shift faster than the inflated threshold can react, so
detection degrades as `Γ` grows. R11 measures the degradation, and the detector's detection rate
stays above `50%` over a longer stretch of the grid than the submitted campaign found — which
moves the numeral, not the claim.

**Read the numeral as a grid point, not as a boundary.** The collapse is not a step: the
detection rate declines across several grid points and crosses `50%` between two of them. `≈ 75`
and the regenerated value are both **the first grid point at which the crossing has already
happened**, so both are upper bounds on a crossing that the grid does not resolve. A revision
should say which grid point is meant, or give the two points that bracket the crossing, rather
than replace one unbracketed numeral with another.

**Verification of the search string.** The block below is quoted from
`articleB_whitening_v87.tex` line 298 verbatim and occurs exactly once in the file. Verify once
more before applying.

<<< RECHERCHER
~~~~~~~~~latex
beyond $\Gamma \approx 75$ its adaptive reference absorbs the shift faster than the inflated threshold reacts, collapsing detection below $50\%$ (a \emph{stochastic syncope})
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
beyond the middle of the $\Gamma$ grid its adaptive reference absorbs the shift faster than the inflated threshold reacts, collapsing detection below $50\%$ (a \emph{stochastic syncope}); the grid brackets the crossing between its two adjacent penalties rather than resolving it
~~~~~~~~~
>>> FIN DU BLOC

**If the authors prefer to keep a numeral**, the regenerated first-below-50% grid point is in
`docs/sections/R11.md`, and the bracketing pair is the two adjacent rows of
`R11_data_add_vs_gamma.csv` at `arm=as_submitted`. This repository does not choose between the
two formulations; it supplies both.
