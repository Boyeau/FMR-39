# 05_presentation

Les supports de présentation du sujet 39. Les rédactions restent dans
`04_experimentations/`, c'est ici que va ce qui se projette.

## `presentation_pitch_3min.tex`

Pitch de 3 minutes : domaine, problématique, état de l'art, résultats.
Six slides, 397 mots de texte parlé, soit environ 160 s de débit plus les
transitions et la page de titre.

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

Les figures sont lues dans `../04_experimentations/resultats_R2/resultats/figures/`
par `\graphicspath`, elles ne sont pas recopiées ici : un doublon finirait par
diverger de la table qui le produit.

### D'où viennent les chiffres

| Slide | Chiffre | Source |
|---|---|---|
| 3 | le détecteur a tiré **3 fois sur 2 000 runs** à `λ = 50` | `03_repo_officiel_.../results/R2_instrumented_blind_spot/data/` |
| 4 | `λ ≥ 15` contre `λ ≤ 12,4` | article source, cité comme tel sur la slide |
| 5 | `6,0` à `14,3` fois `τ_ARF` | `04_experimentations/resultats_R2/resultats/data/QCD_indicateurs_full.parquet` |

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
