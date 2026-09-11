# Campagne instrumentée Q C/D — Ulysse

Campagne unique de 2 000 exécutions et son analyse hors ligne, cadrées sur la version
du business case du 07/09 (`01_consignes/Business_case_Filiere_Recherche_Blind_Spot_FIN.md`).

> **Rapport de lecture des résultats** (démonstrations + mesures, question C complète) :
> https://claude.ai/code/artifact/db553b7a-2b47-4d49-8e4b-926005bcefc5

## Pourquoi cette campagne remplace la première

Un premier jeu de scripts (`question_C_indicateur_adaptation/`, Salomé) partait comme
celui-ci de `exp_R2_instrumented_blind_spot.py`, avec les mêmes paramètres corrigés
(`H = 2000`, grille à 20 points, socle à 1 000 et 3 000 pas). Il a été retiré du dépôt
le 8 septembre (commit `9a32361`) au profit de cette campagne unique ; ce qui suit dit
pourquoi, et vaut comme justification de ce choix.

Ce premier script fixait `lambda = 50` dans la boucle de simulation et décidait `tau_det`
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

  # banc de qualification des remplaçants de τ_ARF (8 septembre)
  controle_api_structure.py  contrôles d'API préalables, chaque échec arrête le plan :
                         `arf.data`, arbre neuf muet, `predict_one` sans aléa, surcoût.
  exp_QCD_etalon.py      même campagne, plus l'étalon analytique : sondes fixes dans
                         trois régions dont la vérité est connue. Toujours aucun seuil.
  bench_candidats.py     le banc : validation de l'étalon, puis A1/A2/B1/B2/C1/D1/D2/D3.
  exposants_fonctionnelles.py  taxonomie des détecteurs par exposant, seuil d'ADWIN,
                         GLR contre CUSUM. Entièrement hors ligne.
  bench_analyse.py       première version du banc, obsolète, gardée pour l'historique.
  probe_metriques.py     sonde exploratoire à trois forêts (ARF / sans drift / gelée).
  verif_biais.py         témoin sans remplacement, 12 exécutions, sortie non persistée.

  # rédactions de D (9 septembre) et révision de C.3 à D.4 (10 septembre)
  derives_QD.py          dérivés hors ligne : phi(t) médiane + IQR, socle sur deux
                         fenêtres, IC bootstrap des médianes de tau_ARF (avec témoins).
  chiffres_QD.py         LECTURE SEULE : chaque chiffre des quatre rédactions de D.
  contre_exemple_kendall.py  contre-exemple de D.2, calculé à la main et par scipy.
  derives_QC.py          écrit QCD_fin_horizon_full (erreur de fin d'horizon par
                         amplitude et fenêtre, pour C.3).
  chiffres_QC.py         LECTURE SEULE : rejeu des constats d'audit de C.1 / C.2 et des
                         chiffres de C.3.
  figures_revision_QCD.py  les 9 figures ajoutées à C.3 et D.1-D.4 le 10 septembre.

  # pitch de 3 minutes (11 septembre), arrêté à la fin de C
  figures_slides.py      les 2 figures projetées de `presentation_pitch_3min.tex`,
                         regénérées et non recadrées (taille de police, panneau bas
                         de R2 qui mesure autre chose, em-dashes dans les pixels).
  chiffres_slides.py     LECTURE SEULE : les 3 comptes d'alarmes de la campagne R2
                         des auteurs, que `verif_chiffres_tex.py` ne peut pas
                         atteindre, et le contrôle qui établit que leur campagne
                         et la nôtre sont distinctes (tau_arf commun sur 96,65 %).
resultats/data/          75 Parquet : 4 de campagne, 6 d'étalon, 9 tables de banc, le
                         reste en tables d'analyse et de dérivés
resultats/figures/       22 figures (11 d'`analyse_QCD.py` et du banc, 9 de
                         `figures_revision_QCD.py`, 2 de `figures_slides.py`)
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

# banc de qualification — l'ordre compte, chaque étape est une porte
PYTHONHASHSEED=0 python controle_api_structure.py            # ~1 min, bloquant
PYTHONHASHSEED=0 python exp_QCD_etalon.py --jobs 10          # pilote 100 runs, ~1,5 min
PYTHONHASHSEED=0 python exp_QCD_etalon.py --jobs 10 --no-drift        # ligne de base
PYTHONHASHSEED=0 python exp_QCD_etalon.py --jobs 10 --seed-sondes 777 # 2e tirage
PYTHONHASHSEED=0 python bench_candidats.py --valider-etalon  # 5 contrôles, bloquants
PYTHONHASHSEED=0 python exp_QCD_etalon.py --jobs 10 --full   # 2 000 runs, ~27 min
PYTHONHASHSEED=0 python bench_candidats.py                   # banc sans étalon
PYTHONHASHSEED=0 python bench_candidats.py --banc-etalon     # banc contre l'étalon
PYTHONHASHSEED=0 python bench_candidats.py --synthese        # table candidat × test
PYTHONHASHSEED=0 python exposants_fonctionnelles.py          # volet 2, ~3 min

# rédactions et révision (tout hors ligne, quelques secondes chacun)
PYTHONHASHSEED=0 python derives_QD.py --tag full     # dérivés de D + IC bootstrap
PYTHONHASHSEED=0 python derives_QC.py --tag full     # fin d'horizon pour C.3
PYTHONHASHSEED=0 python chiffres_QD.py               # traçabilité de D
PYTHONHASHSEED=0 python chiffres_QC.py               # traçabilité de C, audit de C.1/C.2
PYTHONHASHSEED=0 python figures_revision_QCD.py      # 9 figures

# pitch de 3 minutes (11 septembre)
PYTHONHASHSEED=0 python figures_slides.py            # 2 figures projetées
PYTHONHASHSEED=0 python chiffres_slides.py           # traçabilité de l'accroche R2
```

Les traces pré-rupture `QCD_etalon_traces_pre_*` ne sont pas versionnées : elles sont
**identiques bit à bit** à celles de la campagne d'origine (contrôle de non-régression :
4 000 000 de pas comparés, 0 écart, et les 21 561 événements de remplacement identiques),
aucun script du banc ne les lit, et les reversionner dupliquerait 3 Mo pour rien. Les
traces post-rupture, elles, sont versionnées : `bench_candidats.py --banc-etalon` en a
besoin pour recalculer `A(H)` et `S_max(H)`.

`typing_extensions` manque dans le `requirements.txt` du dépôt officiel (déjà noté dans
son `MODIFICATIONS_GROUPE.md`). Le README de ce dépôt annonce qu'il faut Rust pour
compiler river : **c'est faux sur Apple Silicon**, une wheel `cp312-macosx_11_0_arm64`
existe. L'affirmation vaut pour un Homebrew x86_64 sous Rosetta.

## Résultats principaux

| Question | Résultat | Où |
|---|---|---|
| C.1 | `tau_ARF = tau_swap(1/M)`, donc `tau_ARF <= tau_swap(q)` sur chaque exécution. Zéro violation sur 5 795 comparaisons non censurées. Les 3/4 de la forêt sont renouvelés 6,0 à 14,3 fois plus tard que le 1er arbre. | `Fig_QC_ecarts_full.png` |
| C.1c | La conjecture (erreur résorbée avant tout remplacement) **n'est pas confirmée** : les 4 apparentes violations disparaissent dès qu'on exige 20 pas de persistance. | `QCD_tau_err_full.parquet` |
| C.2 | `S_max(H) = max[A(k,j) - (j-k) delta_P]` (Lindley), vérifiée à 1e-10. Certificat en fenêtre courte : **jamais** au-dessus de la détection observée, sur 60 cellules. | `QCD_budget_preuve_full.parquet` |
| C.3 | Invariance confirmée dans son sens (aire × 1,8 quand l'amplitude × 5,8), **mais** l'ajustement `18,5·de^-0,98` n'est valide qu'au milieu de la grille. | `Fig_QC_budget_full.png` |
| D.1 | À `tau_ARF`, **49–76 %** de la preuve est déjà accumulée (domaine de décision ; 0,102 sur la grille entière). `R` va de **−0,188 à +0,885**, négatif sur 5 amplitudes et non monotone : le « 18–48 % » annoncé jusqu'au 8 septembre est faux, cf. `JOURNAL.md` § 1. | `Fig_QD_R_et_G_full.png` |
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
