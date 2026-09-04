# Camera-ready candidate — Figure 6 Caption and Boundary, Section "Empirical Boundaries"

| Field               | Value                                                                   |
| ------------------- | ----------------------------------------------------------------------- |
| **Status**          | **PARKED — do not apply**                                               |
| Target file         | `articleB_whitening_v87.tex` and `figures/fig11_validity_map.png`       |
| Trigger             | Acceptance notification only                                            |
| Evidence            | R06 (paired design effect measurement, computed fourth-moment boundary) |
| Register entry      | `docs/DEVIATIONS.md`, entry `R06-fourth-moment-boundary`                |
| Blocking dependency | none                                                                    |

**Why this is not applied now.** The manuscript is under review and cannot be edited.

**What is being corrected.** The caption claims "100 streams per configuration" without mentioning they are paired across $\Gamma$, making the effective sample size 405, not 1300. Additionally, the fourth-moment boundary is exactly computed as $41.58$, not $41.6$, and the plot update visually detaches this analytic boundary from the nearest grid point ($41$).

<<< RECHERCHER
~~~~~~~~~latex
\caption{\textbf{Empirical validity map of the whitening property} ($100$ streams per configuration). \textbf{(A)} $\Gamma$-insensitivity holds past the loss of the fourth moment ($\Gamma \approx 41.6$). \textbf{(B)} Shifted threshold ($c>0$) or continuous MSE loss breaks whitening, mapping the boundaries of Remark~\ref{rem:scope}.}
~~~~~~~~~
=== REMPLACER PAR >>>
~~~~~~~~~latex
\caption{\textbf{Empirical validity map of the whitening property} ($100$ paired streams per configuration, effective sample size $405$). \textbf{(A)} $\Gamma$-insensitivity holds past the loss of the fourth moment ($\Gamma \approx 41.58$). \textbf{(B)} Shifted threshold ($c>0$) or continuous MSE loss breaks whitening, mapping the boundaries of Remark~\ref{rem:scope}.}
~~~~~~~~~
>>> FIN DU BLOC

### Action requise pour les figures :
Remplacer le fichier binaire `figures/Fig11_Whitening_Boundary.png` par l'artefact généré `results/R06_validity_map/figures/fig06_validity_map.png`.

**Justification :** La figure soumise plaçait une graduation d'axe à la frontière analytique du quatrième moment en superposant le marqueur `Γ = 41`, induisant visuellement en erreur quant à la localisation de la mesure. La nouvelle figure sépare la grille des graduations et place la frontière sur sa propre règle isolée.