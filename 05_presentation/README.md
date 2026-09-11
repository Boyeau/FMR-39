# 05_presentation

Les supports de présentation du sujet 39. Les rédactions restent dans
`04_experimentations/`, c'est ici que va ce qui se projette.

## `presentation_pitch_3min.tex`

Pitch de 3 minutes **pour un auditoire qui ne connaît pas le sujet**.
Six slides, 405 mots de texte parlé, soit environ 162 s de débit.

**Parti pris : montrer le mécanisme, pas énumérer des résultats.** Un schéma
porte le paradoxe (slide 2), un chiffre porte sa réalité (slide 3), une mesure
porte l'avancée (slide 4). Les chiffres détaillés de C.1, C.2 et C.3 sont
volontairement absents : chacun exige sa définition préalable, et trois minutes
ne les financent pas. `Fig_slide_ecarts_swap.png` reste produite et disponible
pour les questions, elle n'est plus projetée.

**Périmètre : les résultats s'arrêtent à la fin de la question C.** La question D
est annoncée comme le travail suivant, et aucun chiffre des `redaction_QD*.tex`
n'apparaît. C'est un choix de cadrage, pas l'état réel du projet.

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
