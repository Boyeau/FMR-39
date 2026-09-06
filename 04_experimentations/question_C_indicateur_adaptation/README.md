# Questions C et D — τARF est-il un bon indicateur de l'adaptation réelle ?

*Énoncés (version détaillée du prof, `01_consignes/Business_case_Filiere_Recherche_Blind_Spot_FIN.pdf`/`.md`) :*
- **Q C.** Le temps τARF est-il un bon indicateur de l'adaptation réelle de la forêt ? Définissez au moins deux mesures alternatives.
- **Q D.** Tracez sur un même axe temporel la fraction d'arbres remplacés, l'erreur globale de l'ensemble, et l'état interne du détecteur externe. Mesurez le lien entre τARF et vos mesures alternatives par une **corrélation de rang** (pas Pearson).

**Comment les deux s'articulent :** Q D fournit le protocole empirique (3 courbes + corrélation formelle) ; Q C interprète ce résultat pour conclure. Un seul script sert aux deux.

> ⚠️ Cette section a été entièrement réécrite le 2026-09-06 après réception du document détaillé du prof, qui donne des définitions et un protocole précis — plus contraignants et plus utiles que ce qu'on avait improvisé avant. Les anciennes définitions (τ_warning, τ50%, τ_rec "jusqu'au retour à la normale", R "jusqu'à τ_rec") sont **remplacées** par celles ci-dessous.

## Point vérifié : l'erreur de l'ensemble EST déjà observable dans nos scripts

Le document du prof affirme : *"dans les expériences actuelles, l'appel à `predict_one()` a été retiré... l'erreur de l'ensemble n'est jamais observée dans ces scripts."* **Vérifié faux sur notre copie et sur un clone frais du 2026-09-06** : `exp_R2_instrumented_blind_spot.py` (et R1, R6, R7, R8, R9) appellent tous `predict_one()` et calculent `error`. R2 en a d'ailleurs besoin pour nourrir son propre CUSUM externe (`ext_pht.update(error)`) — sans ça, aucun signal n'existerait pour l'alarme externe.

**Conséquence pratique :** pas besoin d'ajouter `predict_one()`, il est déjà là. Notre travail est d'ajouter **notre propre instrumentation par-dessus** (φ(t), les 4 indicateurs, l'état du détecteur) sans casser ce qui existe. **À signaler au prof en réunion** — imprécision de son document, ou version du dépôt qu'on n'a pas.

## Les 4 indicateurs à mesurer (remplace nos anciennes définitions)

| Indicateur | Définition | Calcul |
|---|---|---|
| **τARF** | 1er pas où au moins un arbre est remplacé | `any(v > 0 for v in arf._drift_tracker.values())` |
| **τ_swap(q)** | 1er instant où une proportion q d'arbres a été remplacée (q ∈ {10%, 25%, 50%, 75%}) | run par run — voir piège API ci-dessous |
| **τ_err(ρ)** | instant où l'erreur d'ensemble redescend sous ρ du niveau pré-drift | **exclusivement sur la moyenne inter-graines**, jamais sur un run isolé — sert au graphique Q D, pas à la corrélation |
| **A(H)** | erreur excédentaire cumulée sur fenêtre **fixe** de H pas post-drift : `A(H) = Σ(e_t − p̂_0)` | run par run, sans lissage. Tester H ∈ {50, 100, 200, 500} — la sensibilité à H est un résultat à part entière |
| **S_max(H)** | valeur maximale de la statistique interne du détecteur (`ext_pht.S`) sur la même fenêtre H | run par run |

On peut ajouter d'autres candidats (le sujet le permet explicitement) — τ_warning (1er avertissement, via `arf._warning_tracker`) reste un candidat bonus intéressant, mais les 4 ci-dessus sont le socle attendu.

### Piège API à éviter absolument (signalé explicitement par le prof)

`ARFClassifier._drift_tracker` est un dictionnaire **cumulatif** `{id_arbre: nb_remplacements_total}` — un **stock**, pas un flux d'événements.

- ❌ **Ne jamais faire** `cumul += sum(_drift_tracker.values())` dans la boucle temporelle (ça intègre le passé à chaque pas, résultat faux).
- ✅ **Pour τARF** : `any(v > 0 for v in _drift_tracker.values())` au premier pas où c'est vrai.
- ✅ **Pour τ_swap(q)** : compter les arbres **distincts** renouvelés, pas la somme des remplacements : `sum(1 for v in _drift_tracker.values() if v > 0) / n_models`. Un arbre remplacé 3 fois de suite ne compte que pour 1 arbre renouvelé.

### Sur τ_err(ρ) — pourquoi jamais sur un run isolé

`e_t` vaut 0 ou 1 : sur un run isolé, ce n'est pas une courbe mais une suite de sauts. Lisser avec une fenêtre W retarde le signal d'environ W/2 pas — du même ordre que le transitoire qu'on cherche à observer. **Solution : moyenner sur les graines à chaque instant t**, pas de lissage temporel. Avec 200 graines, l'incertitude sur la proportion d'erreur descend à ~0,035 (suffisant pour des sauts de 0,10 à 0,50) ; avec 20 graines (sous-grille de prototypage), elle remonte à ~0,11 — ne rien conclure à ce stade sur les petites amplitudes.

## Corrélation : Kendall tau-b, pas Spearman, pas Pearson

**Pearson exclu** : relation attendue monotone mais pas linéaire (loi de puissance `τARF ≈ 18,5·Δe^(−0,98)` dans l'article), distributions à queues lourdes, et surtout — Pearson n'est pas défini avec des données censurées (run où aucun arbre n'est jamais remplacé avant la fin de l'horizon).

**Kendall tau-b (`scipy.stats.kendalltau`) plutôt que Spearman**, à cause de la gestion des ex-aequo :

- **τARF contre τ_swap(q)** — ex-aequo des deux côtés (deux temps d'atteinte, tous deux censurables à l'horizon). Spearman donnerait le rang maximal aux deux, formant un bloc qui tire artificiellement le coefficient vers +1 sans information réelle. Le tau-b écarte ces paires de son calcul, correctement.
- **τARF contre A(H) ou S_max(H)** — ex-aequo d'un seul côté (A(H)/S_max(H) existent toujours, jamais censurés ; seul τARF l'est). Le tau-b tire alors le coefficient vers 0 sur les petites amplitudes (beaucoup d'arbres jamais remplacés) — c'est un effet de la censure, pas une absence de lien réel.

**Toujours rapporter le taux de censure**, et refaire le calcul sur les seules exécutions complètes (si les deux résultats divergent nettement, c'est la censure qui pilote, pas le phénomène). **Ne jamais supprimer les runs censurés** pour forcer un calcul — biais de survie qui ruinerait l'analyse.

## Grille expérimentale (reprendre celle de R8)

- **21 amplitudes de drift** Δe de 0,10 à 0,50, **200 graines** — le même cadre que l'article, pour rester comparable.
- **Tronquer l'horizon** : contrairement à R8 (52 000 pas, dont 50 000 post-drift, dédiés à sa propre analyse de censure), garder les 2 000 pas pré-drift (rodage + estimation de p̂₀) mais limiter l'observation post-drift à **1 000 pas** (couvre largement H=500). Facteur ~17 de gain de calcul.
- **Prototyper d'abord sur sous-grille** : 5 amplitudes × 20 graines = 100 runs, chronométrer, extrapoler avant de lancer les 4 200 runs complets.
- **Paralléliser sur les graines** (`joblib`), strictement indépendantes.
- Réinsérer `predict_one()` double le temps de calcul (chaque instance traverse la forêt une fois pour l'inférence, une fois pour l'apprentissage) — mais comme il est déjà présent dans notre base R2, ce coût est déjà payé.

## Ce mécanisme réel de remplacement d'un arbre (vérifié dans le code source de `river`)

Contrairement à une image simple ("un arbre remplacé = un arbre vide"), le remplacement se fait en **deux temps**, confirmé dans `river/forest/adaptive_random_forest.py` (`BaseForest.learn_one`) :

1. **Avertissement** (ligne ~183) : un arbre franchit un premier seuil de dégradation → un **arbre de secours** est créé, **vide** à ce moment précis (`self._background[i] = self._new_base_model()`), et un compteur est incrémenté (`self._warning_tracker[i] += 1`).
2. **Confirmation du drift** (ligne ~199) : l'arbre de secours, entraîné en coulisses depuis l'avertissement, **prend la place** de l'arbre original (`self.data[i] = self._background[i]`), et `self._drift_tracker[i] += 1`.

Conséquence pour Q C : un arbre "remplacé" n'est pas vide au moment du remplacement. L'explication d'un éventuel mauvais τARF s'appuie plutôt sur le fait qu'**un seul arbre remplacé sur M ne change presque rien au vote majoritaire de toute la forêt**.

## Ce qu'apporte Gama et al. 2014 (survey concept drift)

- Confirme la définition du concept drift (P(y|X) change, P(X) stable).
- **"Delay of detection"** (§4.1) est le terme standard pour τARF/τdet.
- **Évaluation préquentielle** (§4.2.1) : tester avant d'entraîner — exactement la boucle du script.
- **Lissage par fenêtre glissante** (§3.4) : technique reconnue, mais voir plus haut pourquoi elle est proscrite pour τ_err(ρ) run par run (le prof est plus précis que le survey général sur ce point).

## Script à écrire : `scripts/exp_QC_instrumented_recovery.py`

Copié depuis `exp_R2_instrumented_blind_spot.py`, à modifier :

1. **Retirer le `break` anticipé** — laisser la boucle courir jusqu'à la fin de l'horizon tronqué (2000 pré-drift + 1000 post-drift).
2. **Enregistrer à chaque pas post-drift** : `error` (déjà calculé), fraction d'arbres distincts renouvelés (φ(t)), état du détecteur (`ext_pht.S`).
3. **Calculer par run** : τARF, τ_swap(10/25/50/75%), A(H) pour H ∈ {50,100,200,500}, S_max(H) pour les mêmes H.
4. **τ_err(ρ) séparément**, en post-traitement sur la moyenne inter-graines de la courbe d'erreur — pas dans la boucle par run.
5. **Renvoyer par run** : toutes les grandeurs run-par-run ci-dessus, plus un flag de censure (arbre jamais remplacé / quota jamais atteint avant l'horizon).

**Deux modes** : mode statistiques (grille complète, valeurs résumées seulement) et mode illustration (un run représentatif, courbes complètes pour le graphique Q D).

## Théorie associée (pour interpréter les résultats de Q C, réutilisable pour Q B)

Le prof donne la piste de démonstration pour Q B (conditionner par le flux + Jensen sur x↦x^M) — voir la formalisation théorique A/B, traitée dans le rapport. Pour Q C, l'intuition mécanique est cohérente : τARF est un minimum sur M arbres, statistiquement peu variable (dominé par l'arbre le plus nerveux), donc a priori peu corrélé aux grandeurs d'ensemble comme A(H) — à confirmer empiriquement, pas supposé.

Référence complémentaire en libre accès (en plus de David & Nagaraja 2003, cité par le sujet mais non disponible dans `Biblio/`, emprunt requis) : `02_biblio/12_EsaryProschanWalkup1967_Association_AnnMathStat.pdf` — donne le résultat général sur les variables positivement associées, dont l'argument conditionnement+Jensen du prof est un cas particulier.

## En suspens

- Le script n'est pas encore réécrit avec les nouvelles définitions (copie brute de `exp_R2` pour l'instant).
- Vérifier avec le prof l'incohérence sur `predict_one()` (voir plus haut).
- Décider qui (théorique vs expérimental) prend en charge la piste conditionnement+Jensen pour Q B — directement liée à ce dossier mais documentée dans le rapport, pas ici.
