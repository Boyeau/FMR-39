# Questions C et D — τARF est-il un bon indicateur de l'adaptation réelle ?

*Énoncés (Sujet39.pdf) :*
- **Q C.** Le temps τARF est-il un bon indicateur de l'adaptation réelle de la forêt ?
- **Q D.** Tracez conjointement, sur un même axe temporel, les trois métriques suivantes pour les comparer : la fraction d'arbres remplacés, l'erreur globale de l'ensemble, et l'état interne du détecteur. Évaluez formellement la corrélation de τARF avec la quantité d'erreur résiduelle et le temps effectif de retour à la normale.

**Comment les deux s'articulent :** Q D demande explicitement le tracé des 3 courbes et le calcul de corrélation — c'est le **protocole empirique**, la preuve. Q C pose la question d'interprétation ("est-ce un bon indicateur ?") — sa réponse **s'appuie sur** le résultat de Q D, plus une explication théorique du pourquoi (statistiques d'ordre). Les deux questions partagent la même instrumentation et le même script ; on ne les sépare pas en deux dossiers.

## Ce qui est commun aux deux questions

### Le mécanisme réel de remplacement d'un arbre (vérifié dans le code source de `river`)

Contrairement à une image simple ("un arbre remplacé = un arbre vide"), le remplacement se fait en **deux temps**, confirmé dans `river/forest/adaptive_random_forest.py` (`BaseForest.learn_one`) :

1. **Avertissement** (ligne ~183) : un arbre franchit un premier seuil de dégradation → un **arbre de secours** est créé, **vide** à ce moment précis (`self._background[i] = self._new_base_model()`), et un compteur est incrémenté (`self._warning_tracker[i] += 1`).
2. **Confirmation du drift** (ligne ~199) : l'arbre de secours, qui s'est entraîné en coulisses depuis l'avertissement (ligne ~174, à chaque pas), **prend la place** de l'arbre original (`self.data[i] = self._background[i]`), et un autre compteur est incrémenté (`self._drift_tracker[i] += 1` — c'est celui déjà utilisé par `exp_R2` pour τARF).

Conséquence : un arbre "remplacé" (au sens de τARF) n'est pas vide au moment du remplacement — il a déjà appris depuis l'avertissement. L'explication d'un éventuel mauvais τARF doit plutôt s'appuyer sur le fait qu'**un seul arbre remplacé sur M ne change presque rien au vote majoritaire de toute la forêt**, pas sur l'idée d'un arbre reparti de zéro.

### Ce qu'apporte Gama et al. 2014 (survey concept drift)

- **Confirme la définition du concept drift** (P(y|X) change, P(X) stable) déjà utilisée pour décrire le script — cohérent avec la distinction concept drift / data drift du Sujet39.
- **"Delay of detection"** (§4.1) est le terme standard du domaine pour ce qu'on appelle τARF/τdet : *"le nombre de nouvelles instances nécessaires pour détecter un changement après sa survenue réelle"*. Notre mesure s'inscrit donc dans une métrique reconnue, pas une invention.
- **Évaluation préquentielle** (§4.2.1, "Interleaved Test-Then-Train") : tester le modèle *avant* de l'entraîner sur chaque instance — exactement la boucle `predict_one` puis `learn_one` du script. Valide la méthodologie de R2 comme standard du domaine.
- **Lissage par fenêtre glissante** (§3.4, "Loss Estimation — Sliding Window") : technique reconnue pour estimer un taux d'erreur récent — justifie notre ē_t (moyenne glissante) plutôt qu'un choix arbitraire.
- **Point clé : aucune métrique standard de "temps de retour à la normale" n'existe dans ce survey.** Les 3 critères standards pour évaluer un détecteur sont : probabilité de vraie détection, taux de fausses alarmes, délai de détection — rien sur le retour de performance après adaptation. **Confirme que τ_rec est une vraie lacune à combler nous-mêmes**, pas une métrique existante qu'on aurait pu simplement citer.

### Définitions des grandeurs à mesurer

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

### Script à écrire : `scripts/exp_QC_instrumented_recovery.py`

Copié depuis `exp_R2_instrumented_blind_spot.py`, à modifier :

1. **Retirer le `break` anticipé** (ligne 101 de l'original) — laisser la boucle courir jusqu'à `N_STEPS` au lieu de s'arrêter dès que τARF et τdet sont trouvés.
2. **Ajouter le suivi de τ_warning**, en parallèle de τARF, via `arf._warning_tracker`.
3. **Enregistrer 3 séries temporelles après le drift** : φ(t) (fraction remplacée), ē_t (erreur lissée), état du détecteur (`ext_pht.S / cfg['lambda']`, normalisé 0-1).
4. **Calculer τ_rec** à partir de ē_t (seuil + persistance, voir tableau ci-dessus).
5. **Renvoyer par run** : `tau_warning`, `tau_arf`, `tau_50pct`, `tau_rec`, `R`, `tau_det` (au lieu de seulement `tau_arf`, `tau_det`).

**Deux modes d'exécution**, pour éviter de stocker inutilement des dizaines de millions de valeurs :
- **Mode statistiques** — la grille complète (boundary shifts × seeds, ~2000 runs comme dans R2), on ne garde que les grandeurs résumées par run.
- **Mode illustration** — un seul run représentatif, on garde les 3 courbes complètes.

## Question D — le protocole empirique (ce que le script doit produire)

1. **Le graphique conjoint** — les 3 courbes (φ(t), ē_t, état du détecteur normalisé) sur un même axe temporel, pour un run représentatif (mode illustration).
2. **La corrélation formelle** — sur la grille complète (mode statistiques) : corrélation de Spearman (+ intervalle de confiance bootstrap) entre τARF et R (erreur résiduelle), et entre τARF et τ_rec (temps de retour effectif). C'est la réponse directe, chiffrée, à la phrase de l'énoncé *"évaluez formellement la corrélation de τARF avec..."*.
3. Attention aux runs où τ_rec n'est jamais atteint avant la fin de la simulation (censure à droite) — à traiter séparément ou avec un outil adapté aux durées censurées plutôt qu'une corrélation naïve.

## Question C — l'interprétation (ce qu'on en conclut)

La réponse à "τARF est-il un bon indicateur ?" se construit à partir du résultat de Q D :

- **Si la corrélation τARF ↔ τ_rec (et τARF ↔ R) est faible** → τARF n'est pas un bon indicateur : le premier remplacement d'arbre n'annonce pas fiablement quand l'erreur redevient normale, ni combien elle aura coûté.
- **Comparer aussi τ_warning et τ50% à τ_rec** — pour savoir si un autre candidat serait meilleur que τARF (question sous-jacente utile pour la discussion, pas explicitement demandée par l'énoncé mais qui enrichit la réponse).
- **Expliquer *pourquoi*, avec les statistiques d'ordre sous dépendance** (voir ci-dessous) plutôt que de s'arrêter au constat empirique.

### Statistiques d'ordre sous dépendance (théorie, pour Q C — et réutilisable pour Q B)

David & Nagaraja (2003), *Order Statistics*, chap. 5, est **un livre** — non disponible dans `Biblio/`, nécessite un emprunt bibliothèque (signalé dans `Bibliographie_Sujet39.docx`, référence #10, statut "payant"). En attendant, on a récupéré une alternative en libre accès qui contient le résultat mathématique dont on a besoin :

`Biblio/12_EsaryProschanWalkup1967_Association_AnnMathStat.pdf` — Esary, Proschan & Walkup (1967), *"Association of Random Variables, with Applications"*, Annals of Mathematical Statistics. Article source du concept d'**association** (dépendance positive) que David & Nagaraja réutilisent probablement dans leur chapitre sur les statistiques d'ordre.

**Le résultat clé (à vérifier/citer précisément une fois l'article lu en détail) :** pour des variables aléatoires positivement associées X1,...,Xn, P(X1>t1,...,Xn>tn) ≥ ∏ P(Xi>ti) — l'inégalité va dans le sens inverse de l'indépendance.

**Application :** les τ_i (temps d'adaptation de chaque arbre) sont positivement associés (même flux de données). Donc P(tous les τ_i > t) est plus grand sous dépendance que sous indépendance ⟹ P(τARF ≤ t) est plus petit sous dépendance ⟹ **τARF arrive statistiquement plus tard sous dépendance**. La formule de l'article (calculée sous indépendance) **surestime donc P_miss** — elle est trop pessimiste, pas trop optimiste. Cohérent avec ce que dit déjà le manuscrit v63/v64 (L244-248, cf. exploration précédente) sans démonstration formelle — c'est cette démonstration qu'on peut maintenant construire (et réutiliser pour Q B, qui pose exactement cette question).

## En suspens

- David & Nagaraja reste à emprunter en bibliothèque si on veut la version "officielle" citée par le sujet — Esary/Proschan/Walkup 1967 comble le trou en attendant.
- Le script n'est pas encore modifié (copie brute de `exp_R2` pour l'instant) — lecture ciblée terminée, prochaine étape : écrire le code.
