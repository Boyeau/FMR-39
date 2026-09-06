# Confirmation expérimentale — pour la réunion du lundi 15h30

Livrable demandé par Raphael Minato (email du 2026-09-05) : *"confirmation que vous aurez pu cloner le dépôt, installer l'environnement à l'identique (River 0.23.0) et rejouer le script R2 sans erreur."*

## 1. Clone du dépôt

Testé deux fois : notre copie de travail (`03_repo_officiel_TheBlindSpotParadox-ICDM2026/`, récupérée le 2026-09-03) et un **clone `git` frais** du dépôt officiel dans un dossier séparé, pour validation indépendante.

**Découverte en clonant à nouveau** : le dépôt officiel a évolué depuis notre récupération (3 nouveaux commits, dont un du 2026-09-03 même jour : *"chore: remove artifacts imported from The-Whitening-Advantage (contamination 8debd1c)"*). Les auteurs ont retiré `docs/DEVIATIONS.md`, `docs/MAPPING.md`, `docs/audits/`, `docs/camera_ready_candidates/` — exactement la couche qu'on avait identifiée comme appartenant à un autre article ("Article B", économétrie/whitening) et non au papier Blind Spot Paradox du sujet. **Confirmation externe, par les auteurs eux-mêmes, de notre lecture précédente.**

Vérifié : `git diff` entre l'ancien commit et le nouveau ne montre **aucun changement** dans `experiments/`, `run_all.sh` ni aucun `run_experiment_R*.sh` — le code qu'on utilise réellement (R1-R9) est identique à l'octet près. Aucun impact sur nos expérimentations en cours.

**Action à prendre** : mettre à jour `03_repo_officiel_TheBlindSpotParadox-ICDM2026/` vers le dernier commit pour se débarrasser de la contamination (aucun risque, pas de changement fonctionnel).

## 2. Installation de l'environnement (River 0.23.0, à l'identique)

- Python 3.12 requis.
- `river==0.23.0` n'a pas de wheel précompilé pour macOS x86_64/Python 3.12 → compilation depuis les sources → nécessite un compilateur Rust (`brew install rust`, absent par défaut).
- **Bug reproductible, confirmé sur un clone indépendant** : `pip install -r requirements.txt` officiel échoue à l'import (`ModuleNotFoundError: No module named 'typing_extensions'`) — `river` importe ce module en interne sans le déclarer dans ses dépendances. Vérifié que ce n'est pas spécifique à notre machine : reproduit à l'identique sur un venv neuf, sur un clone `git` séparé du dépôt officiel.
- **Correctif appliqué** : ajout de `typing_extensions==4.16.0` (seule addition — aucune version pinnée par les auteurs n'a été modifiée). Documenté dans `03_repo_officiel_TheBlindSpotParadox-ICDM2026/MODIFICATIONS_GROUPE.md`.
- Après correctif : `from river.forest import ARFClassifier` fonctionne, `river.__version__ == '0.23.0'` — environnement identique à celui spécifié par les auteurs.

## 3. Exécution de R2 — ✅ terminée sans erreur

`run_experiment_R2.sh` (3 scénarios × 20 intensités de drift × 100 seeds = 6000 runs) lancé le 2026-09-05, terminé le 2026-09-06 dans notre environnement principal. Message final : `[SUCCESS] Pipeline R2 completed.`

Artefacts produits, tous présents :
- `results/R2_instrumented_blind_spot/figures/Fig_R2_A_PHT_ARF.png`, `Fig_R2_B_PHT_ARF.png`, `Fig_R2_C_PHT_ARF.png`
- `results/R2_instrumented_blind_spot/data/R2_instrumented_A_PHT_ARF.parquet`, `..._B_...parquet`, `..._C_...parquet`

**Les 3 livrables demandés par le prof sont donc validés : clone ✅, environnement identique ✅, R2 rejoué sans erreur ✅.**

## À vérifier / compléter avant lundi

- [ ] Mettre à jour `03_repo_officiel_...` vers le dernier commit upstream (nettoyage de la contamination Article B) — optionnel, aucun risque, pas urgent.
