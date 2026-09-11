# 05_presentation

Les supports de présentation du sujet 39. Les rédactions restent dans
`04_experimentations/`, c'est ici que va ce qui se projette.

## `presentation_pitch_3min.tex`

Pitch de 3 minutes **pour un auditoire qui ne connaît pas le sujet**.
Huit slides, 469 mots de texte parlé : **176 s à 160 mots/min, 188 s à 150**.
C'est au-dessus de la cible, et c'est un arbitrage assumé — poser le drift, la
forêt et le détecteur avant de s'en servir coûte une minute qu'on ne récupère
pas ailleurs. La coupe la moins chère, si les trois minutes sont fermes, est la
slide 5 (le compromis de réglage) : elle vaut 62 mots et ne porte aucun résultat
du groupe.

**Parti pris : rien n'est employé avant d'avoir été posé.** Un audit des slides
a montré six notions utilisées sans définition — arbre de décision, la raison
d'être d'une *forêt*, `λ`, `Δe`, `M`, et l'unité de temps. Les trois notations
ont disparu des figures (l'axe dit « threshold the watchdog must cross », plus
`λ` ; « observations seen since the change », plus « steps » ; « forest of 10
trees, change size 0.24 », plus `M` ni `Δe`), et l'arbre de décision a
maintenant sa slide. Les chiffres détaillés de C.1, C.2 et C.3 restent absents.
`Fig_slide_ecarts_swap.png` est produite pour les questions, pas projetée.

| Slide | Ce qu'elle pose |
|---|---|
| 2 | ce qu'est un **changement de concept**, sur la frontière même que simule le banc |
| 3 | **l'arbre, la forêt, l'ARF** : dix arbres qui votent, remplacés un par un |
| 4 | **le détecteur** : il empile les erreurs et alerte au franchissement d'un seuil |
| 5 | **le paradoxe** : mis ensemble, les deux s'annulent |
| 6 | **le compromis de réglage** : le seuil décide tout, et aucun ne convient |
| 7 | **l'avancée** : l'horloge admise date le premier arbre, pas la réparation |
| 8 | où on en est, et la suite |

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
| 6 | **3 / 2 000** à `λ = 50`, **801 / 2 000** à `λ = 25`, **1 926 / 2 000** à `λ = 8` | `03_repo_officiel_.../results/R2_instrumented_blind_spot/data/` |
| 7 | `86` observations contre `1 225`, médiane à `Δe = 0,24` | `04_experimentations/resultats_R2/resultats/data/QCD_indicateurs_full.parquet` |

La slide 5 est un **schéma stylisé, sans données** : pour un auditoire qui
découvre le sujet, une vraie trajectoire est trop bruitée pour montrer que la
preuve monte puis s'arrête sous le seuil. La légende de la figure le dit.

```bash
cd ../04_experimentations/resultats_R2/scripts
PYTHONHASHSEED=0 python chiffres_slides.py    # les comptes R2 et les six chiffres de C.1
PYTHONHASHSEED=0 python figures_slides.py     # les deux figures projetées
```

`verif_chiffres_tex.py` signale `2014` comme introuvable : c'est l'année de la
citation Gama, pas une mesure. Aucun littéral n'a été ajouté à sa liste `EXCLUS`.

### Un chiffre qui ne se cite jamais seul

**Le « 3 alarmes sur 2 000 » est le régime `λ = 50`, et rien d'autre.** Au même
banc, sur les mêmes dérives et les mêmes graines, l'alarme part 801 fois sur
2 000 à `λ = 25` et 1 926 fois sur 2 000 à `λ = 8`. Montrer le seul `λ = 50`
revient à choisir le réglage le plus favorable à la thèse et à le donner pour le
cas général. La slide 6 montre les trois, parce que **c'est la dépendance au
réglage qui est le résultat** : il n'existe pas de seuil à la fois assez discret
pour qu'on lui fasse confiance et assez sensible pour voir la dérive.

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
