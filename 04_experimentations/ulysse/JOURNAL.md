# Journal de recherche — questions C et D

Ce qui a été établi, ce qui a surpris, et les pièges dans lesquels il ne faut pas
retomber. Tenu au fil de l'eau plutôt que reconstitué.

Pour les réponses rédigées, voir `../redaction_QC3_invariance.tex` et
`../pistes_remplacement_tauARF.md`. Ce journal contient ce qui ne rentre dans aucun
des deux : les surprises sur le dispositif, les erreurs commises, et les contrôles
qui ont servi.

---

## 1. Ce qui est établi

### Question C

| | Résultat | Preuve |
|---|---|---|
| **C.1 a** | `τ_ARF = τ_swap(1/M)`, donc inférieur ou égal à tous les autres quotas | déterministe ; 0 violation sur 6 000 comparaisons |
| **C.1 b** | Les 3/4 de la forêt sont renouvelés **7 à 15 fois plus tard** que le 1er arbre | mesuré, 2 000 exécutions |
| **C.1 c** | La conjecture d'une résorption précédant tout remplacement **n'est pas confirmée** | 2 violations apparentes tombent avec 20 pas de persistance |
| **C.2 b** | `S_max(H) = max [A(k,j) − (j−k)·δ_P]` (forme de Lindley) | démontré ; vérifié à 1,07e−10 contre la récurrence |
| **C.2 d** | Version quantifiée nécessaire et suffisante ; version en fenêtre entière suffisante seulement | démontré |
| **C.2 f** | Le certificat en fenêtre courte ne dépasse **jamais** la détection observée | 60 cellules, 0 violation |
| **C.3 b** | Le budget de preuve varie de **5,9 %** quand l'amplitude varie d'un facteur 17,7 | calcul |
| **C.3 f** | Mesuré : l'aire varie d'un facteur **1,78** contre 5,8 attendus sans adaptation | 2 000 exécutions |

### Question D

- `τ_b(τ_ARF, A(H))` est **indiscernable de zéro sur les 18 amplitudes** du domaine de
  décision. `τ_ARF` ne porte aucune information sur la quantité de preuve offerte au
  détecteur, qui est pourtant la seule grandeur décidant de l'alarme.
- **Effondrement par agrégation** : `+0,397` sur l'empilement contre `+0,053` en médiane
  stratifiée. Le coefficient global ne confirme pas un lien faible, il en fabrique un.
- À l'instant `τ_ARF`, seulement **18 à 48 %** de l'adaptation est acquise, mais déjà
  **49 à 75 %** de la preuve est accumulée. L'indicateur arrive tôt dans l'adaptation et
  tard dans la course.
- **Le point aveugle, chiffré** : avec `λ = 50`, une seule exécution sur 2 000 déclenche
  l'alarme. Avec `λ = 25`, 61 % restent muettes.

---

## 2. Ce qu'on a découvert sans le chercher

Ces cinq points ne figurent pas dans l'énoncé et ne sont pas dans l'article. Ce sont eux
qui feraient la différence entre exécuter le sujet et y contribuer.

### a. Le socle théorique vaut exactement zéro

La cible pré-rupture `y = 1{x₀+x₁ > 0}` est une fonction **déterministe** des entrées :
aucun bruit d'étiquetage, donc erreur de Bayes nulle. Les 0,023 mesurés sont
**intégralement** de l'erreur d'approximation — les arbres découpent par coupes
perpendiculaires aux axes une frontière oblique.

Conséquence : le détecteur surveille les écarts à un niveau de référence qui est un
artefact du classifieur, pas une propriété du problème.

### b. Le mécanisme de remplacement double l'erreur en régime stationnaire

Sans le moindre drift, la forêt procède à une **trentaine de remplacements** pendant le
rodage, par pur bruit — ADWIN à horloge 1 est très réactif. Son erreur de base vaut alors
**0,0228**, contre **0,0125** pour une forêt qui ne remplace jamais rien.

Le socle du point (a) est donc en partie fabriqué par le mécanisme d'adaptation lui-même.
C'est le résultat le plus original sorti de cette exploration, et il ne dépend d'aucune
des pistes qui ont échoué.

### c. À forte amplitude, la nouvelle tâche est plus facile que l'ancienne

À `b = 4`, la frontière est si loin que la classe 1 devient quasi absente : prédire
toujours 0 suffit. L'erreur tombe de 0,024 à 0,007, c'est-à-dire **sous le socle
d'avant la rupture**, et l'aire d'erreur excédentaire sur l'horizon complet devient
**négative**, jusqu'à −20,8.

Deux conséquences. Le modèle stylisé du sujet (« l'erreur retombe au socle ») est en
défaut sur le haut de la grille. Et tout indicateur défini comme « retour de l'erreur à
l'acceptable » est franchi dès le pas 92 à `Δe = 0,498` — non parce que la forêt a
compris quoi que ce soit, mais parce que le problème s'est simplifié.

### d. L'ajustement `18,5 · Δe^(−0,98)` de l'article n'est valide qu'au milieu de la grille

Rapport entre `τ_ARF` mesuré et prédit :

| Δe | 0,028 | 0,141 | 0,287 | 0,436 | 0,498 |
|---|---|---|---|---|---|
| mesuré / prédit | **0,19** | **2,08** | 1,02 | 0,81 | 0,76 |

À la plus faible amplitude, l'ajustement prédit le premier remplacement au pas 611 ; il
survient au pas 118. La conclusion d'invariance survit, mais elle ne peut plus être
**justifiée** par l'exposant 0,02 qui en dérive : il faut l'appuyer sur la mesure directe.

### e. λ n'intervient pas dans la dynamique

Le détecteur externe lit la trajectoire d'erreur et n'agit jamais sur la forêt. Les trois
scénarios de `R2` produisent, une fois le `break` retiré, des exécutions identiques au bit
près. **Une seule campagne remplace donc les trois**, et `λ` comme `δ_P` se balayent hors
ligne. C'est ce qui fait tenir tout le travail en 15 minutes de calcul.

### Tests de validation de la métrique

Deux des quatre familles de tests du protocole ont été passées. Les deux disqualifient
`τ_ARF`, par des voies indépendantes.

**A1, le drift nul** — 100 exécutions sans aucune rupture. `τ_ARF` vaut 105 en médiane,
la forêt renouvelle 9 arbres sur 10, et 24 % des forêts sont **entièrement** renouvelées
en 2 000 pas. Comparé aux exécutions avec drift, la forêt sans drift réagit plus vite
dans **54 %** des paires à `Δe = 0,028` : à cette amplitude, l'indicateur ne distingue
pas un vrai drift de son absence. À forte amplitude il discrimine partiellement (21 %).

**C1, la taille de la forêt** — `M` = 5, 10, 20, 50. Rapport de `τ_ARF` à sa valeur pour
`M = 5` : **0,05** à `Δe = 0,028`, **0,83** à `Δe = 0,498`. L'indicateur n'est donc pas
comparable entre configurations, et le degré de dépendance entre les délais d'arbres
varie avec l'amplitude — quasi-indépendance sous bruit, forte dépendance sous drift
franc. Ce dernier point déborde sur la question B, dont l'hypothèse d'indépendance ne
prévoit pas cette variation.

---

## 3. Pistes explorées et abandonnées

Détail dans `../pistes_remplacement_tauARF.md`. En bref :

| Piste | Verdict |
|---|---|
| désaccord fonctionnel `D(t)` avec une forêt gelée | relation à l'erreur **infirmée** (corrélations 0,28 à 0,49) |
| masse de vote renouvelée | **sature** comme le comptage : 2 valeurs distinctes sur 20 exécutions |
| forêt témoin comme étalon | **invalide en l'état** : le témoin s'adapte quand même, et part avec un avantage de 0,0103 |
| retour de l'erreur à l'acceptable | **écarté** : échoue au test de la tâche facilitée |

Reste ouvert : `τ_erase`, jamais testé, alors qu'il est dans l'énoncé et calculable depuis
les traces existantes sans relancer une campagne.

---

## 4. Les pièges méthodologiques rencontrés

Cette section est la plus utile pour la suite du projet. Chacun de ces pièges a
effectivement produit un résultat faux avant d'être repéré.

### Chercher un premier franchissement sur une courbe bruitée

`τ_err(ρ)` calculé comme premier instant où l'erreur passe sous un seuil donnait
2 violations apparentes de la relation d'ordre. En exigeant que la condition tienne
**20 pas consécutifs**, il n'en reste aucune. Le bruit de la courbe moyennée sur
100 graines vaut `σ ≈ 0,011` : une fluctuation isolée suffit à déclencher un premier
franchissement bien avant la vraie résorption.

**Règle :** tout instant défini par un franchissement de seuil sur une grandeur bruitée
doit exiger une persistance, et le seuil doit dominer `2σ`.

### Une fenêtre d'estimation qui empiète sur ce qu'elle mesure

`R(τ_ARF)` exige d'estimer le palier d'erreur juste après la rupture, sur une courte
fenêtre. Avec une fenêtre fixe de 50 pas et un `τ_ARF` qui tombe à 28 à forte amplitude,
la fenêtre englobait l'adaptation elle-même : le palier était sous-estimé et `R` partait
dans le négatif (−0,201). Corrigé en bornant la fenêtre à `τ_ARF/2`.

### Comparer à un témoin sans vérifier qu'il part à égalité

La forêt témoin sans remplacement semblait montrer que le remplacement est
contre-productif. En mesurant l'erreur **avant** la rupture, on découvre qu'elle part
déjà avec 0,0103 d'avance, pour la raison du §2 b. L'essentiel de l'effet observé était
ce handicap initial, pas un effet du drift.

**Règle :** tout étalon fondé sur un modèle de référence doit être contrôlé en régime
stationnaire avant d'être utilisé après la rupture.

### Valider une métrique en la comparant à une autre

Deux mauvaises métriques peuvent parfaitement s'accorder. Il faut des contrôles où la
réponse est connue d'avance — d'où le protocole de benchmark, dont les deux premiers
tests suffisent déjà à écarter deux candidats.

### Construire un contre-exemple qui ne montre rien

Pour illustrer l'artefact de censure sur Spearman (question D.2), un premier jeu de
10 points fictifs a donné `ρ = τ_b = 1,000` : aucun écart, donc aucune démonstration.
L'artefact n'apparaît que si les points observés ne sont **pas** parfaitement ordonnés
entre eux. Avec 4 observés anti-ordonnés, l'écart devient 0,846 contre 0,600.

---

## 5. Contrôles effectués

- **Déterminisme** : deux campagnes complètes indépendantes de 2 000 exécutions donnent
  des fichiers strictement identiques — trajectoires, socles, événements.
- **Reconstruction de `S_t`** : la forme close confrontée à la récurrence naïve sur
  200 trajectoires, écart maximal 1,07e−10. `analyse_QCD.py` refuse de continuer si ce
  contrôle échoue.
- **Socle sur deux fenêtres** : 1 000 pas donne `σ = 0,00501`, 3 000 pas donne
  `σ = 0,00298`, soit un bruit divisé par 1,68 pour `√3 = 1,73` attendu. Les conclusions
  agrégées ne bougent pas, seule la mesure par exécution gagne.
- **Grille** : vérifié identique à celle de `R2` (`linspace(0.1, 4.0, 20)`). La grille à
  21 points utilisée un temps ne partageait que 2 points sur 20 avec la référence.

---

## 6. Environnement

Deux points qui contredisent la documentation du dépôt et font gagner du temps.

**river 0.23.0 a une wheel `cp312-macosx_11_0_arm64`.** Ni Rust ni compilation ne sont
nécessaires sur Apple Silicon. Le README affirme le contraire parce qu'il raisonnait sur
un Homebrew x86_64 sous Rosetta.

**`typing_extensions` manque** dans le `requirements.txt` du dépôt officiel, déjà noté
dans son `MODIFICATIONS_GROUPE.md`.

Installation qui fonctionne :

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python "river==0.23.0" "numpy==1.26.4" "pandas<3" \
    scipy joblib tqdm pyarrow matplotlib typing_extensions
```

Coûts mesurés : campagne complète 15 min sur 10 cœurs, analyse 2 min, sonde à trois
forêts 20 min pour 100 exécutions (l'appel à `_metrics` à chaque pas est le goulot, il
gagnerait à être échantillonné).

---

## 7. Ce qui reste ouvert

1. **Le coût permanent du remplacement** (§2 b) mérite mieux que 12 exécutions.
2. **`τ_erase`**, calculable sans relancer quoi que ce soit.
3. **La conjecture de C.1 c** reste non testable aux deux plus faibles amplitudes : il
   faudrait de l'ordre de 1 800 graines à `Δe = 0,028` pour que le seuil domine le bruit.

## 8. Réserves à déclarer dans le rapport

- Le critère d'acceptabilité de C.1 b a été formulé **après** avoir vu les mesures, ce que
  le protocole proscrit pour un critère de décision. Il est ancré sur une grandeur du
  dispositif plutôt que choisi pour produire un résultat, mais cela doit être dit.
- La conjecture de C.1 c n'est **pas réfutée**, seulement non testable là où elle serait
  la plus plausible.
