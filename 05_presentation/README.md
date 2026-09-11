# 05_presentation

Les supports de présentation du sujet 39. Les rédactions restent dans
`04_experimentations/`, c'est ici que va ce qui se projette.

## `presentation_pitch_3min.tex`

Pitch de 3 minutes **pour un auditoire qui ne connaît pas le sujet**.
Huit slides, 522 mots de texte parlé : **196 s à 160 mots/min**. Les schémas
portent assez pour que les notes restent brèves.
C'est au-dessus de la cible, et c'est un arbitrage assumé — poser le drift, la
forêt et le détecteur avant de s'en servir coûte une minute qu'on ne récupère
pas ailleurs. La coupe la moins chère, si les trois minutes sont fermes, est la
slide 6 (le compromis de réglage) : elle vaut 62 mots et ne porte aucun résultat
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
| 3 | **l'arbre, la forêt, l'ARF** : l'escalier d'un arbre, puis dix arbres dont un remplacé |
| 4 | **le détecteur** : la pile d'erreurs qui retombe à zéro, puis monte et franchit |
| 5 | **le paradoxe, et la course** : la réparation a une date, l'alarme n'en a jamais |
| 6 | **le compromis de réglage** : le seuil décide tout, et aucun ne convient |
| 7 | **l'avancée** : la date admise compte 1 arbre sur 10, la réparation en demande 8 |
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

### Cinq schémas plutôt que des listes à puces

Six des huit slides portent une figure, et quatre sont des schémas dessinés :
l'espace du drift, l'escalier d'un arbre et les dix arbres, la pile du
détecteur, et l'annulation des deux. Les trois derniers sont **stylisés, sans
données**, ce que la légende dit à chaque fois.

Deux points de fidélité qui ne sont pas cosmétiques :

- l'escalier de `Fig_slide_foret` est tracé dans **le même espace et sur la même
  frontière** que `Fig_slide_drift` : un arbre ne coupe que parallèlement aux
  axes, c'est aussi la raison du socle d'erreur de `0,0231` mesuré pour une
  erreur de Bayes nulle (`JOURNAL.md` § 2 a) ;
- la pile de `Fig_slide_watchdog` **et** celle de `Fig_slide_mecanisme` suivent
  la même récurrence `S_t = max(0, S_{t−1} + x_t)`, celle que C.2 démontre, et
  non un cumul tronqué après coup. C'est la seule forme qui **retombe à zéro**
  quand les erreurs cessent. Les deux schémas seraient sinon en contradiction :
  la pile plafonnerait sur l'un et redescendrait sur l'autre. Ils se répondent
  maintenant — slide 4, le détecteur qui franchit ; slide 5, le même qui
  culmine sous le seuil et voit la preuve se vider ;
- `Fig_slide_deux_horloges` reprend les **pictogrammes d'arbres** de la slide 3,
  un sur dix contre huit sur dix. Sans eux la slide tombait du ciel : rien ne
  disait ce que « la date de réparation » compte au juste.

### Pourquoi la slide 7 ne tombe pas du ciel

La date de réparation n'est pas une mesure parmi d'autres : **c'est la course
qui l'exige**. Le paradoxe s'énonce « la réparation arrive avant l'alarme », et
une course ne se tranche qu'en datant les deux coureurs. Dater l'alarme est
trivial, elle part ou non ; dater la réparation demande une convention, et toute
la quantification de l'article repose sur celle qu'elle a choisie.

C'est pour cela que la slide 5 porte maintenant un repère `repaired` sur la
courbe d'erreur et un `no alarm, ever` en regard : le premier coureur a une date
d'arrivée, le second n'en a pas. Sans ce repérage, la slide 7 mesurait un temps
dont personne n'avait dit à quoi il sert.

### Les deux dates ne font pas le même métier

C'est la confusion la plus facile à faire, et la slide 7 la lève désormais en
une ligne : **l'alarme est ce qu'on veut, `τ_ARF` mesure ce qui l'empêche.**

- `τ_det` est un **outil** : elle prévient un humain, elle déclenche l'audit, le
  réentraînement, la pause. C'est la seule sortie visible du dispositif.
- `τ_ARF` n'alerte personne. C'est un **instrument de mesure**, et il n'existe
  que parce que le paradoxe est une course : pour dire que la réparation bat
  l'alarme, il faut chronométrer la réparation.

Conséquence à avoir en tête pour les questions, et qui n'est pas sur les slides :
`τ_ARF` étant une borne inférieure unilatérale, il fait paraître la forêt **plus
rapide qu'elle n'est**. La course est donc arbitrée en faveur de la forêt plus
facilement qu'elle ne devrait l'être, et le paradoxe tel que l'article le
quantifie est exagéré par son propre instrument. Le phénomène, lui, tient : les
3 alarmes sur 2 000 se mesurent sans passer par `τ_ARF`.

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
