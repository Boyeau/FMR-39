# Modifications apportées par le groupe au dépôt officiel

Ce fichier journalise tout écart entre cette copie locale et le dépôt officiel
tel que récupéré le 2026-09-03 (commit `9d28823976c0563ef955eb95a5efeccd7d7c4492`,
cf. `README.md` racine du projet FMR-39). Objectif : pouvoir distinguer dans le
rapport ce qui vient des auteurs de ce que nous avons dû corriger/ajouter pour
que le pipeline tourne réellement, et pour préparer la phase expérimentale
(Questions C et D du sujet).

## 2026-09-04

- **`requirements.txt`** — ajout de `typing_extensions==4.16.0`.
  Cause : `river==0.23.0` importe `typing_extensions` directement dans
  `river/base/base.py` mais ne le déclare pas dans ses dépendances de package
  (`pip show river` ne liste que `numpy, pandas, scipy`). C'est un oubli
  d'empaquetage côté `river`, pas un problème de notre environnement — vérifié
  en confirmant qu'aucune autre dépendance pinnée ne l'installe
  transitivement. Sans ce correctif, `pip install -r requirements.txt` suivi
  d'un `import river` échoue sur `ModuleNotFoundError: No module named
  'typing_extensions'` dans un venv neuf.

- **`.gitignore`** — ajout de `blindspot_env/` (notre venv local, ~500 Mo, non
  portable, ne doit jamais être versionné).

<!-- Prochaine entrée : instrumentation R2 pour Q C/D, une fois écrite -->
