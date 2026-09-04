# Question C — τARF est-il un bon indicateur de l'adaptation réelle ?

*Rappel de l'énoncé (Sujet39.pdf) :* le remplacement d'un arbre ne signifie pas que l'erreur globale de la forêt est résorbée — il faut instrumenter le système pour observer directement son comportement interne.

## Plan en 3 étapes

1. **Lecture ciblée** — Gomes et al. 2017 (mécanisme de remplacement d'arbre dans l'ARF) + Gama et al. 2014 (définition standard de l'adaptation en flux). Fait pour les deux, voir sections dédiées ci-dessous.
2. **Expérimentation** — instrumenter le code pour mesurer plusieurs candidats-indicateurs et comparer au retour réel à la normale (voir "Script à écrire" ci-dessous).
3. **Résultats confrontés à la théorie** — corréler les indicateurs au retour réel, interpréter à la lumière des statistiques d'ordre (David & Nagaraja — référence à retrouver, absente du dossier `Biblio/`).

## Le mécanisme réel de remplacement d'un arbre (vérifié dans le code source de `river`)

Contrairement à une image simple ("un arbre remplacé = un arbre vide"), le remplacement se fait en **deux temps**, confirmé dans `river/forest/adaptive_random_forest.py` (`BaseForest.learn_one`) :

1. **Avertissement** (ligne ~183) : un arbre franchit un premier seuil de dégradation → un **arbre de secours** est créé, **vide** à ce moment précis (`self._background[i] = self._new_base_model()`), et un compteur est incrémenté (`self._warning_tracker[i] += 1`).
2. **Confirmation du drift** (ligne ~199) : l'arbre de secours, qui s'est entraîné en coulisses depuis l'avertissement (ligne ~174, à chaque pas), **prend la place** de l'arbre original (`self.data[i] = self._background[i]`), et un autre compteur est incrémenté (`self._drift_tracker[i] += 1` — c'est celui déjà utilisé par `exp_R2` pour τARF).

Conséquence pour Q C : un arbre "remplacé" (au sens de τARF) n'est pas vide au moment du remplacement — il a déjà appris depuis l'avertissement. L'explication d'un éventuel mauvais τARF doit plutôt s'appuyer sur le fait qu'**un seul arbre remplacé sur M ne change presque rien au vote majoritaire de toute la forêt**, pas sur l'idée d'un arbre reparti de zéro.

## Ce qu'apporte Gama et al. 2014 (survey concept drift)

- **Confirme la définition du concept drift** (P(y|X) change, P(X) stable) déjà utilisée pour décrire le script — cohérent avec la distinction concept drift / data drift du Sujet39.
- **"Delay of detection"** (§4.1) est le terme standard du domaine pour ce qu'on appelle τARF/τdet : *"le nombre de nouvelles instances nécessaires pour détecter un changement après sa survenue réelle"*. Notre mesure s'inscrit donc dans une métrique reconnue, pas une invention.
- **Évaluation préquentielle** (§4.2.1, "Interleaved Test-Then-Train") : tester le modèle *avant* de l'entraîner sur chaque instance — exactement la boucle `predict_one` puis `learn_one` du script. Valide la méthodologie de R2 comme standard du domaine.
- **Lissage par fenêtre glissante** (§3.4, "Loss Estimation — Sliding Window") : technique reconnue pour estimer un taux d'erreur récent — justifie notre ē_t (moyenne glissante) plutôt qu'un choix arbitraire.
- **Point clé : aucune métrique standard de "temps de retour à la normale" n'existe dans ce survey.** Les 3 critères standards pour évaluer un détecteur sont : probabilité de vraie détection, taux de fausses alarmes, délai de détection — rien sur le retour de performance après adaptation. **Confirme que τ_rec est une vraie lacune à combler nous-mêmes**, pas une métrique existante qu'on aurait pu simplement citer.

## Définitions des grandeurs à mesurer

| Symbole | Définition | Comment l'obtenir |
|---|---|---|
| τ_warning | 1er avertissement après le drift | `sum(arf._warning_tracker.values())` augmente |
| τARF | 1er remplacement confirmé après le drift | `sum(arf._drift_tracker.values())` augmente (déjà présent dans le script) |
| φ(t) | fraction d'arbres remplacés au temps t | `swaps_after / N_MODELS`, suivi en continu |
| τ50% | 1er instant où φ(t) atteint 0,5 | lu sur la courbe φ(t) |
| erreur lissée ē_t | moyenne glissante de l'erreur (ex. fenêtre de 100 pas) | lissage de `error` (0/1) déjà calculé |
| τ_rec | temps de retour à la normale | 1er instant où ē_t repasse sous `p_pre_empirical × 1,1` et y reste (ex. 200 pas) |
| R | erreur résiduelle cumulée | somme de l'excès d'erreur (ē_t − p_pre_empirical) entre le drift et τ_rec |
| τdet | 1er déclenchement du CUSUM externe | déjà présent dans le script |

Trois candidats (τ_warning, τARF, τ50%) seront comparés à τ_rec (la vraie mesure de "adaptation réelle") pour répondre à Q C — pas seulement τARF isolément.

## Script à écrire : `scripts/exp_QC_instrumented_recovery.py`

Copié depuis `exp_R2_instrumented_blind_spot.py`, à modifier :

1. **Retirer le `break` anticipé** (ligne 101 de l'original) — laisser la boucle courir jusqu'à `N_STEPS` au lieu de s'arrêter dès que τARF et τdet sont trouvés.
2. **Ajouter le suivi de τ_warning**, en parallèle de τARF, via `arf._warning_tracker`.
3. **Enregistrer 3 séries temporelles après le drift** : φ(t) (fraction remplacée), ē_t (erreur lissée), état du détecteur (`ext_pht.S / cfg['lambda']`, normalisé 0-1).
4. **Calculer τ_rec** à partir de ē_t (seuil + persistance, voir tableau ci-dessus).
5. **Renvoyer par run** : `tau_warning`, `tau_arf`, `tau_50pct`, `tau_rec`, `R`, `tau_det` (au lieu de seulement `tau_arf`, `tau_det`).

**Deux modes d'exécution**, pour éviter de stocker inutilement des dizaines de millions de valeurs :
- **Mode statistiques** — la grille complète (boundary shifts × seeds, ~2000 runs comme dans R2), on ne garde que les grandeurs résumées par run → sert au calcul de corrélation (Spearman + bootstrap) pour Q C.
- **Mode illustration** — un seul run représentatif, on garde les 3 courbes complètes → sert au graphique conjoint de Q D.

## En suspens

- David & Nagaraja (statistiques d'ordre) absent de `Biblio/` — à retrouver avant l'étape 3.
- Le script n'est pas encore modifié (copie brute de `exp_R2` pour l'instant) — lecture ciblée terminée, prochaine étape : écrire le code.
