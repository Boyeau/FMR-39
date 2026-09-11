# 05_presentation

Les supports de présentation du sujet 39. Les rédactions restent dans
`04_experimentations/`, c'est ici que va ce qui se projette.

## `presentation_pitch_3min.tex`

Pitch de 3 minutes **pour un auditoire qui ne connaît pas le sujet**.
Sept slides, 439 mots de texte parlé, soit environ 176 s de débit. C'est la
limite haute : toute phrase ajoutée se paie sur une autre.

**Parti pris : expliquer les concepts et l'avancement, pas énumérer des
résultats.** Chaque slide pose une notion avant de s'en servir, et chaque
chiffre arrive après le dispositif qui le produit. Les chiffres détaillés de
C.1, C.2 et C.3 sont volontairement absents : chacun exige sa définition
préalable, et trois minutes ne les financent pas.
`Fig_slide_ecarts_swap.png` reste produite pour les questions, elle n'est
plus projetée.

| Slide | Ce qu'elle pose |
|---|---|
| 2 | ce qu'est un **changement de concept**, sur la frontière même que simule le banc |
| 3 | les **deux défenses** : le modèle qui se répare, le détecteur qui alerte |
| 4 | le **paradoxe** : mises ensemble, elles s'annulent |
| 5 | **le dispositif** et son chiffre : 2 000 exécutions, 3 alarmes |
| 6 | **l'avancée** : l'horloge admise date le premier arbre, pas la réparation |
| 7 | où on en est, et la suite |

Le texte parlé est dans les `\note{}` du `.tex`, jamais sur les slides.

### Compiler

```bash
latexmk -lualatex presentation_pitch_3min.tex
```

**lualatex, pas pdflatex** : le thème `metropolis` charge les fontes Fira.
Avec `pdflatex` le document compile mais retombe sur les fontes par défaut.

Le texte parlé se sort en PDF séparé, une page par slide, miniature en regard :

```bash
lualatex -jobname=notes_conferencier "\def\NOTESSEULES{}\input{presentation_pitch_3min}"
```

Même fichier source dans les deux cas : le texte parlé vit dans les `\note{}`
du `.tex` et nulle part ailleurs, il ne peut donc pas diverger des slides.

Les figures sont lues dans `../04_experimentations/resultats_R2/resultats/figures/`
par `\graphicspath`, elles ne sont pas recopiées ici : un doublon finirait par
diverger de la table qui le produit.

### D'où viennent les chiffres

| Slide | Chiffre | Source |
|---|---|---|
| 3 | le détecteur a tiré **3 fois sur 2 000 runs** | `03_repo_officiel_.../results/R2_instrumented_blind_spot/data/` |
| 4 | `86` pas contre `1 225`, médiane à `Δe = 0,24` | `04_experimentations/resultats_R2/resultats/data/QCD_indicateurs_full.parquet` |

La slide 2 est un **schéma stylisé, sans données** : pour un auditoire qui
découvre le sujet, une vraie trajectoire est trop bruitée pour montrer que la
preuve monte puis s'arrête sous le seuil. La légende de la figure le dit.

```bash
cd ../04_experimentations/resultats_R2/scripts
PYTHONHASHSEED=0 python chiffres_slides.py    # les comptes R2 et les six chiffres de C.1
PYTHONHASHSEED=0 python figures_slides.py     # les deux figures projetées
```

`verif_chiffres_tex.py` signale `2014` comme introuvable : c'est l'année de la
citation Gama, pas une mesure. Aucun littéral n'a été ajouté à sa liste `EXCLUS`.

### Deux pièges à ne pas rouvrir

- **Le panneau du bas des figures `Fig_R2_*` ne montre pas le taux de silence
  du détecteur.** Il vaut `P(τ_det absent OU τ_ARF ≤ τ_det)`, soit 97,35 % sur le
  régime B quand le silence y est de 59,95 %. La figure de la slide 3 est
  régénérée sans ce panneau : le reprendre ferait dire à l'image le contraire de
  la voix.
- **La campagne R2 des auteurs et la nôtre ne sont pas la même.** Même grille de
  20 `boundary_shift`, mêmes 100 graines, mais `τ_ARF` ne coïncide que sur
  96,65 % des runs. La slide 3 dit « we re-ran the authors' experiment », la
  slide 5 « our own instrumented campaign ». Les confondre serait une faute.
