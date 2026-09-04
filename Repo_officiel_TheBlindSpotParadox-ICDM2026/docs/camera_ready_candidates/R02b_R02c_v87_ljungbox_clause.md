# Camera-ready candidate — Ljung-Box clause, Section "Empirical Boundaries"

| Field               | Value                                                         |
| ------------------- | ------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                     |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen)   |
| Trigger             | Acceptance notification only                                  |
| Evidence            | R02b (n=1000 sweep over nu), R02c (horizon sweep to n=128000) |
| Register entry      | `docs/DEVIATIONS.md`, entry 3                                 |
| Cost                | +2 words against the submitted sentence                       |
| Blocking dependency | none — R03..R17 do not touch this clause                      |

**Why this is not applied now.** The manuscript is under review and cannot be edited. The
KDD 2027 Research Track allocates one additional content page to accepted papers for exactly
this kind of revision, so budget is not the constraint; timing is. Applying a correction
before the deviation inventory is complete guarantees reapplying it later.

**What is being corrected.** Not the published number: 11 rejections out of 120 is an
ordinary draw under a true rate of 5.8% (probability 8.9%). What is corrected is the
subordinate clause asserting a mechanism that is wrong independently of any sample.

<<< RECHERCHER
~~~~~~~~~latex
and already over-reject on the i.i.d.\ arm ($9.2\%$), where $t_7$ innovations deprive $\varepsilon_t^2$ of a fourth moment and the $\chi^2$ approximation fails;
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
and reject at $9.2\%$ on the i.i.d.\ arm, a rate that $120$ streams cannot separate from nominal; a dedicated sweep ($1{,}000$ streams per point, horizons to $n = 1.28\times10^5$) places $t_7$ at nominal and the over-rejection beyond the sixth-moment boundary ($7.7\%$ at $\nu \le 6$, excluding nominal at every horizon), where the autocovariance summand loses its third absolute moment;
~~~~~~~~~
>>> FIN DU BLOC