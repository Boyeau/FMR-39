# Campagne instrumentée Q C/D — Ulysse

Campagne unique de 2 000 exécutions et son analyse hors ligne, cadrées sur la version
du business case du 07/09 (`01_consignes/Business_case_Filiere_Recherche_Blind_Spot_FIN.md`).

> **Rapport de lecture des résultats** (démonstrations + mesures, question C complète) :
> https://claude.ai/code/artifact/db553b7a-2b47-4d49-8e4b-926005bcefc5

## Pourquoi un second jeu de scripts

`question_C_indicateur_adaptation/` (Salomé) et ce dossier partent tous deux de
`exp_R2_instrumented_blind_spot.py` et convergent sur les mêmes paramètres corrigés
(`H = 2000`, grille à 20 points, socle à 1 000 et 3 000 pas). **Ils ne font pas doublon** :
la différence est structurelle.

Le script de Salomé fixe `lambda = 50` dans la boucle de simulation et décide `tau_det`
en ligne. Or `lambda` n'agit **pas** sur la dynamique — le détecteur externe lit la
trajectoire d'erreur, il n'agit jamais sur la forêt. Le figer impose une campagne par
seuil, et à `lambda = 50` le détecteur n'alarme jamais : `tau_det` est censuré à 100 %,
donc aucune corrélation ne peut l'impliquer.

Ici, aucun `lambda` n'apparaît dans la campagne. On enregistre la matière première, et
`S_t`, `tau_det`, `S_max` se recalculent hors ligne pour les trois seuils d'un coup — et
pour n'importe quel `delta_P`. Une campagne remplace les trois.

## Contenu

```
scripts/
  exp_QCD_campagne.py    simulation — n'écrit que e_t, les événements de remplacement
                         et les 3 000 pas pré-rupture. Aucun indicateur, aucun seuil.
  analyse_QCD.py         tout le reste, sans resimuler : indicateurs, certificats,
                         corrélations, figures.
resultats/data/          4 Parquet de campagne + 8 tables d'analyse
resultats/figures/       5 figures
```

## Relancer

```bash
# environnement : Python 3.12 arm64 + river 0.23.0 (wheel native, ni Rust ni compilation)
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python "river==0.23.0" "numpy==1.26.4" "pandas<3" \
    scipy joblib tqdm pyarrow matplotlib typing_extensions

cd scripts
PYTHONHASHSEED=0 python exp_QCD_campagne.py            # prototype 5 x 20, ~40 s
PYTHONHASHSEED=0 python exp_QCD_campagne.py --full     # campagne 20 x 100, ~15 min
PYTHONHASHSEED=0 python analyse_QCD.py --tag full      # analyse, ~2 min
PYTHONHASHSEED=0 python analyse_QCD.py --self-check    # contrôle de S_t seul, instantané
```

`typing_extensions` manque dans le `requirements.txt` du dépôt officiel (déjà noté dans
son `MODIFICATIONS_GROUPE.md`). Le README de ce dépôt annonce qu'il faut Rust pour
compiler river : **c'est faux sur Apple Silicon**, une wheel `cp312-macosx_11_0_arm64`
existe. L'affirmation vaut pour un Homebrew x86_64 sous Rosetta.

## Résultats principaux

| Question | Résultat | Où |
|---|---|---|
| C.1 | `tau_ARF = tau_swap(1/M)`, donc `tau_ARF <= tau_swap(q)` sur chaque exécution. Zéro violation sur 6 000 comparaisons. Les 3/4 de la forêt sont renouvelés 7 à 15 fois plus tard que le 1er arbre. | `Fig_QC_ecarts_full.png` |
| C.1c | La conjecture (erreur résorbée avant tout remplacement) **n'est pas confirmée** : les 2 apparentes violations disparaissent dès qu'on exige 20 pas de persistance. | `QCD_tau_err_full.parquet` |
| C.2 | `S_max(H) = max[A(k,j) - (j-k) delta_P]` (Lindley), vérifiée à 1e-10. Certificat en fenêtre courte : **jamais** au-dessus de la détection observée, sur 60 cellules. | `QCD_budget_preuve_full.parquet` |
| C.3 | Invariance confirmée dans son sens (aire × 1,8 quand l'amplitude × 5,8), **mais** l'ajustement `18,5·de^-0,98` n'est valide qu'au milieu de la grille. | `Fig_QC_budget_full.png` |
| D.1 | À `tau_ARF`, seulement **18–48 %** de l'adaptation est acquise, mais **49–75 %** de la preuve est déjà accumulée. | `Fig_QD_R_et_G_full.png` |
| Point aveugle | À `lambda = 50` : **1 exécution sur 2 000** déclenche l'alarme. À `lambda = 25` : 61 % de silence. | `QCD_indicateurs_full.parquet` |

## Contrôles

- **Déterminisme** : deux campagnes complètes indépendantes produisent des fichiers
  strictement identiques (trajectoires, socles, événements).
- **Reconstruction de `S_t`** : forme close contre récurrence naïve, écart max 1,07e-10.
  `analyse_QCD.py` refuse de continuer si ce contrôle échoue.
- **Socle** : 1 000 pas → sigma 0,00501 ; 3 000 pas → sigma 0,00298 (bruit ÷ 1,68, attendu
  sqrt(3) = 1,73). Le socle théorique est **exactement 0** — la cible pré-rupture est une
  fonction déterministe des entrées, donc les 0,023 mesurés sont entièrement de l'erreur
  d'approximation de la forêt.

## Deux réserves à déclarer dans le rapport

1. **C.1b** — le critère d'acceptabilité (« l'écart est décisif s'il dépasse `tau_det` »)
   a été formulé *après* avoir vu les mesures, ce que le sujet proscrit pour les critères
   de décision. Il est ancré sur une grandeur du dispositif, pas choisi pour produire un
   résultat, mais cela doit être dit.
2. **C.1c** — le test perd tout pouvoir aux deux plus faibles amplitudes, là où la
   conjecture serait la plus plausible. Elle n'est pas réfutée, elle est **non testable**
   sur ce dispositif : il faudrait davantage de graines, le bruit décroissant en `1/sqrt(n)`.

## Ce qui reste à faire

La rédaction de D.2 (invalidité de Pearson, le « filet » des trois raisons dont une tombe
après stratification, définition de `tau_b`), le critère de décision de D.4, et les
conclusions à tirer des tables de corrélation.
