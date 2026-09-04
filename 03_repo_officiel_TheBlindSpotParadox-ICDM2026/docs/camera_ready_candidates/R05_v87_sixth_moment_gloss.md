# Camera-ready candidate — Sixth moment gloss, Appendix B

| Field               | Value                                                       |
| ------------------- | ----------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                   |
| Target file         | `articleB_whitening_v87.tex` (submitted 2026-07-27, frozen) |
| Trigger             | Acceptance notification only                                |
| Evidence            | R05 moment boundary analysis                                |
| Register entry      | `docs/DEVIATIONS.md`, entry 12                              |
| Cost                | +0 words against the submitted sentence                     |
| Blocking dependency | none — this is a descriptive error, not a numerical finding |

**Why this is not applied now.** The manuscript is under review and cannot be edited.

**What is being corrected.** The manuscript describes $\mathbb{E}[\varepsilon_t^6]$ as the second moment of the monitored statistic $\varepsilon_t^2$. It is in fact the third moment. The second moment of $\varepsilon_t^2$ is $\mathbb{E}[\varepsilon_t^4]$, whose boundary for $t_7$ innovations occurs at $\Gamma = 41.6$, far outside the measured grid.

<<< RECHERCHER
~~~~~~~~~latex
loss of $\mathbb{E}[\varepsilon_t^6]$---the second moment of the \emph{monitored} statistic $\varepsilon_t^2$---which
~~~~~~~~~

=== REMPLACER PAR >>>
~~~~~~~~~latex
loss of $\mathbb{E}[\varepsilon_t^6]$---the third moment of the \emph{monitored} statistic $\varepsilon_t^2$---which
~~~~~~~~~
>>> FIN DU BLOC