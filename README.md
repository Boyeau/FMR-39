# FMR-39 — Le paradoxe du point aveugle

Filière Métiers de la Recherche, sujet 39, encadrant Raphaël Minato.

Groupe : Alexandre Boyer, Melaine Gouillou, Salomé Fonvielle, Ulysse Petit-Tichanné.

## Contenu du dépôt

- **`Sujet39.pdf`** — l'énoncé officiel (4 questions A-D).
- **`Consignes_études_de_cas_2026-2027.pdf`** — cadre général de la filière (calendrier, livrables, grille d'évaluation).
- **`Doc_compagnon/`** — introduction progressive au sujet, rédigée pour être lue sans prérequis (12 chapitres : vocabulaire, formalisation, une section par question A-D, planning à 14 jours, biblio commentée).
- **`Biblio/`** — synthèse bibliographique (13 références, `Bibliographie_Sujet39.docx`) + PDF des articles en accès libre ou récupérés via la bibliothèque.
- **`Repo_officiel_TheBlindSpotParadox-ICDM2026/`** — copie du dépôt d'expériences de l'article source (*The Blind Spot Paradox*, soumis IEEE ICDM 2026), récupérée le 2026-09-03 au commit `9d28823976c0563ef955eb95a5efeccd7d7c4492`.
  Dépôt original : https://github.com/TheBlindSpot-ICDM2026/The-Blind-Spot-Paradox-Experiments
  À l'intérieur : `experiments/R1` à `R9` + `run_all.sh` sont la cible du sujet (chaque script reproduit une figure du manuscrit). `docs/` et `results/R01`-`R18` sont le journal de recherche interne des auteurs (audits, écarts entre code et manuscrit) — à consulter en second, après avoir fait son propre raisonnement.

## Environnement (pipeline `Repo_officiel_...`)

Python 3.12 requis. `river==0.23.0` n'a pas de wheel précompilé pour macOS x86_64/Python 3.12 : `pip install -r requirements.txt` compile depuis les sources et nécessite un compilateur Rust (`brew install rust` si absent). Voir `Repo_officiel_TheBlindSpotParadox-ICDM2026/MODIFICATIONS_GROUPE.md` pour les écarts constatés par rapport au dépôt officiel (ex. `typing_extensions` manquant dans leur `requirements.txt`).
