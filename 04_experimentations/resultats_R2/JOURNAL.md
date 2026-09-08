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
| **C.1 b** | Les 3/4 de la forêt sont renouvelés **6 à 14 fois plus tard** que le 1er arbre | mesuré, 2 000 exécutions, 18 amplitudes interprétables |
| **C.1 c** | La conjecture d'une résorption précédant tout remplacement **n'est pas confirmée** | 4 violations apparentes tombent avec 20 pas de persistance |
| **C.2 b** | `S_max(H) = max [A(k,j) − (j−k)·δ_P]` (forme de Lindley) | démontré ; vérifié à 1,07e−10 contre la récurrence |
| **C.2 d** | Version quantifiée nécessaire et suffisante ; version en fenêtre entière suffisante seulement | démontré |
| **C.2 f** | Le certificat en fenêtre courte ne dépasse **jamais** la détection observée | 60 cellules, 0 violation |
| **C.3 b** | Le budget de preuve varie de **5,9 %** quand l'amplitude varie d'un facteur 17,7 | calcul |
| **C.3 f** | Mesuré : l'aire varie d'un facteur **1,78** contre 5,8 attendus sans adaptation — sur `Δe ∈ [0,085 ; 0,498]` ; **11,4** si on inclut le bas de grille | 2 000 exécutions |

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
| désaccord fonctionnel `D(t)` avec une forêt gelée | relation à l'erreur **infirmée** (corrélations de −0,29 à 0,49, de signe non constant) |
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
4 violations apparentes de la relation d'ordre (`Δe` = 0,028, 0,085, 0,141 et 0,194). En
exigeant que la condition tienne **20 pas consécutifs**, il n'en reste aucune. Le bruit de
la courbe moyennée sur 100 graines dépend de l'amplitude — `σ` va de 0,0154 à 0,0047, il
ne vaut pas 0,011 partout : une fluctuation isolée suffit à déclencher un premier
franchissement bien avant la vraie résorption.

Deux de ces quatre violations sont à des amplitudes où le test n'a aucune puissance
(`ρΔe < 2σ`) ; **les deux autres sont à des amplitudes interprétables** et ne tombent que
par la persistance. Dire, comme une version antérieure de ce journal, que les violations
se situent exactement là où le test est aveugle est faux, et affaiblit le résultat plutôt
que de le renforcer : c'est la persistance qui fait le travail, pas le manque de puissance.

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

### Conclure d'un point de la grille que le modèle tient

`C.3` isolait deux hypothèses empilées — le rectangle `A = Δe · τ_ARF`, et l'ajustement en
loi de puissance — puis concluait, sur la seule amplitude `Δe = 0,028`, que le rectangle
était confirmé et que seul l'ajustement fautait. Recalculé sur les 20 amplitudes, le
rectangle se trompe de **−41 % à +43 %** et **change de signe** vers `Δe ≈ 0,19` : il ne
coïncide avec la mesure qu'à cet endroit précis, celui-là même où l'écart avait été
évalué.

La raison était sous nos yeux dans `C.1` : `τ_ARF` date le **premier** remplacement, alors
que les 3/4 de la forêt sont renouvelés 6 à 14 fois plus tard. Poser `W = τ_ARF` comme
largeur du plateau d'erreur contredit directement la hiérarchie démontrée en `C.1`. Deux
sections du même travail se contredisaient sans que personne ne s'en aperçoive.

**Règle :** une relation vérifiée à une amplitude se vérifie sur toute la grille avant
d'être écrite, et une section se relit contre les sections voisines — la contradiction
interne ne se voit pas depuis l'intérieur d'une section.

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

---

## 9. Le banc de qualification des remplaçants de `τ_ARF` (8 septembre)

Critères et seuils figés dans `../pistes_remplacement_tauARF.md` § 8, **committés avant
le premier calcul** (`c948a5e`). Étalon adossé à la vérité analytique : trois jeux de
200 sondes fixes par région (`R_bande`, `R_haut`, `R_bas`), échantillonnées
conditionnellement à leur région, relevées tous les 25 pas. Aucune forêt de référence,
donc plus de circularité par comparaison de la forêt à elle-même.

Les chiffres ci-dessous sont ceux **d'après** le double audit adverse, qui a corrigé
quatre erreurs changeant des verdicts (§ 9.4).

### 9.1 Ce que le banc établit

| | Résultat | Preuve |
|---|---|---|
| **9 a** | L'instrumentation ne déplace rien : trajectoires et événements **identiques bit à bit** à la campagne d'origine | 4 000 000 de pas comparés, 0 écart ; 21 561 événements, identiques |
| **9 b** | `τ_ARF` est **anti-informatif** de `Δe` = 0,028 à 0,194 : la forêt *sans* drift réagit plus vite que celle *avec* drift dans 55 à 76 % des paires, IC entièrement au-dessus de 50 % | AUC A1, 2 000 runs, IC bootstrap apparié |
| **9 c** | Maximum de l'anomalie : **76 % à `Δe` = 0,141** [IC 70 ; 82]. L'AUC A1 n'est donc **pas monotone** — le § 2 n'avait mesuré que trois amplitudes et n'avait pas vu ce régime | 20 amplitudes |
| **9 d** | **Aucun** candidat ne passe A2, *y compris l'étalon lui-même* : en haut de grille toutes les mesures montent alors que la compétence conservée s'effondre | 13 échecs sur 15 |
| **9 e** | À `Δe ≥ 0,45`, **1 505 runs sur 2 000 sont signalés** et **654 dégénèrent définitivement** : `acc_bande` sature à 1 pendant que `acc_haut` tombe à 0,000 en fin d'horizon. La forêt ne s'adapte pas, elle répond « toujours 0 » | contrôle 3 de l'étalon, campagne complète |
| **9 f** | À taux de fausse alarme égal (5 % sur `b = 0`), le **GLR détecte plus vite que le CUSUM sur tout le domaine mesurable** : 103 contre 156 pas à `Δe` = 0,085, 10 contre 17 en haut de grille | délais, censure publiée |

### 9.2 Ce qui contredit l'attente, et qu'il faut écrire tel quel

Le plan pré-enregistrait que les candidats par comptage **échoueraient** B1, ce qui aurait
confirmé que le remplacement d'arbres n'est pas le mécanisme de l'adaptation.
**C'est l'inverse qui est mesuré** : `τ_ARF` a un τ-b positif et significatif avec
l'étalon sur les **20 amplitudes** (médiane **+0,310**), `τ_swap(25 %)` aussi (**+0,398**),
`N(W = 50)` atteint **+0,430**. Le lien existe, il est modéré, il va dans le bon sens, et
il survit à l'exclusion des runs dégénérés.

`τ_ARF` reste disqualifié — mais par **A1**, pas par B1. La nuance change la rédaction de
la question C : on ne peut pas écrire que `τ_ARF` ne mesure rien de l'adaptation. Il en
mesure une part, tout en étant incapable de distinguer un drift de son absence en bas de
grille. **La réponse tranchée est donc : `τ_ARF` est un indicateur d'adaptation faible mais
réel, et un discriminateur de drift nul voire négatif en dessous de `Δe` ≈ 0,2.**

Attention à la lecture de la table de synthèse : `A1 0/20` et `B1 20/20` sur la même ligne
ne se contredisent pas. A1 compare deux **conditions** (drift contre pas de drift) ; B1
classe les runs **à l'intérieur** d'une strate d'amplitude. Une métrique peut ordonner
correctement les runs d'une strate sans distinguer un drift de son absence.

### 9.3 Le volet 2 : la taxonomie par exposant ne tient pas

Sur le seul segment estimable (bas de grille, 919 % d'étendue en `Δe`), **aucune des dix
prédictions pré-enregistrées** `p − qα` n'est vérifiée. La plus proche est le GLR :
+1,017 [0,990 ; 1,046] contre +1,143 prédit. Le modèle « fenêtre d'adaptation
`W ~ Δe^(−α)` à `α` unique » est réfuté sur ce dispositif — `α` local vaut de 0,12 à 3,24
selon la durée retenue et le segment.

La forme close du seuil d'ADWIN n'est pas validée : `Δe*` vaut 0,0143 avec `α = 0,857` et
0,0013 avec l'ajustement libre, quand la frontière observée est à 0,085. L'exposant
`1/(2 − α)` amplifie tout écart sur `α` d'un facteur 11. **C'est cette sensibilité qui est
le résultat, pas une valeur de `Δe*`.**

### 9.4 Les quatre erreurs corrigées par l'audit, et ce qu'elles changeaient

Chacune avait produit un chiffre faux publié. Elles valent d'être écrites : ce sont les
mêmes familles de pièges que le § 4.

1. **`τ_ARF` confondu avec `τ_swap(10 %)`.** Un quota de 10 % exige 1 arbre à `M = 10` mais
   5 à `M = 50` : le test C1 mesurait alors une autre grandeur et donnait un rapport de
   **0,483** là où la note établit **0,05**. Deux fichiers du dépôt se contredisaient.
   Corrigé : `τ_ARF` est le **premier** remplacement, un arbre, quel que soit `M` — et le
   rapport retrouve **0,054**. Les quotas portent désormais leur nombre d'arbres requis.
2. **Imputation de censure du mauvais côté.** Dans B1, le candidat est d'abord orienté
   (`x ← −x`) puis les censurés imputés à `+20 000` : un quota jamais atteint, c'est-à-dire
   la non-réaction maximale, se retrouvait classé comme l'adaptation la plus rapide. Le
   signe du τ-b de `τ_swap(75 %)` s'en trouvait inversé sur trois amplitudes (−0,333 au
   lieu de +0,326 à `Δe` = 0,085). Corrigé : imputation au rang le moins réactif **après**
   orientation.
3. **Orientation sémantiquement fausse de `A(H)` et `S_max(H)`.** Déclarés « valeur haute =
   réaction plus forte », alors qu'une aire d'erreur excédentaire **grande** signale une
   adaptation **lente**. Le verdict A1 de `S_max(H)` passe de **19/20 à 0/20**, et son τ-b
   de −0,330 à +0,330 : ce qui était lu comme une « réfutation de l'orientation » était
   l'orientation correcte. C'est une erreur de spécification, corrigée et déclarée — pas un
   ajustement après coup.
4. **Un contrôle bloquant qui ne pouvait pas échouer.** Le contrôle 3 de l'étalon testait
   `rho est un nombre` : il passait quoi qu'il arrive. Remplacé par un vrai critère —
   l'étalon des runs dégénérés doit être **inférieur** à celui des runs sains.

### 9.5 Pièges nouveaux, à ajouter au § 4

- **Un plancher de maillage lu comme une propriété.** Le GLR semblait détecter moins vite
  que le CUSUM à forte amplitude : son délai butait sur 50, la plus petite fenêtre de ma
  grille, et il était scanné dix fois plus grossièrement que le CUSUM. À résolution égale
  et avec des fenêtres de 10 pas, le classement s'inverse. Toute statistique définie comme
  un `sup` sur une grille hérite des bornes de cette grille.
- **Une saturation lue comme un plafonnement théorique.** Le taux de détection atteint
  100 % dès `Δe ≈ 0,14` pour les deux détecteurs : comparer deux plafonds ne dit rien. Il a
  fallu passer au délai, qui n'est pas borné.
- **Une médiane calculée sur les seuls survivants.** Le délai médian excluait les runs
  jamais détectés, donc les plus lents : à `Δe` = 0,028, 88 % de censure rendaient la
  médiane indéfinie. Elle n'est plus publiée au-delà de 50 % de censure.
- **Une pente qui sature à `1/L`.** La différence pas à pas d'une moyenne glissante de
  longueur `L` sur une série binaire vaut `1/L` presque partout : exposant nul, IC nul,
  rien de mesuré. La pente se prend sur un écart de `L` pas.
- **Recalculer une prédiction avec le paramètre qu'on vient de mesurer.** Tentant quand
  `α` local diffère du `α` pré-enregistré — et c'est déplacer la cible après le tir. Les
  deux colonnes sont publiées, le verdict porte sur la prédiction figée.
- **Un test dont la référence échoue son propre critère.** A2 disqualifie 13 candidats sur
  15, mais **l'étalon lui-même en fait partie**. A2 ne sépare donc pas les métriques
  honnêtes des contaminées : il sépare les grandeurs croissantes des décroissantes. Un test
  doit être passé à sa propre référence avant qu'on lise ses verdicts.

---

## 8. Réserves à déclarer dans le rapport

- Le critère d'acceptabilité de C.1 b a été formulé **après** avoir vu les mesures, ce que
  le protocole proscrit pour un critère de décision. Il est ancré sur une grandeur du
  dispositif plutôt que choisi pour produire un résultat, mais cela doit être dit.
- La conjecture de C.1 c n'est **pas réfutée**, seulement non testable aux deux plus
  faibles amplitudes, là où elle serait la plus plausible. Aux deux amplitudes suivantes,
  le test a bien la puissance de trancher et les violations apparentes tombent par la
  seule persistance.
- L'invariance de C.3 est établie **sur `Δe ∈ [0,085 ; 0,498]`**, le bas de grille étant
  écarté parce que la fenêtre courte y couvre presque tout l'horizon. La restriction se
  publie avec le facteur 1,78, faute de quoi le chiffre n'est pas reproductible : sur la
  grille entière le même calcul donne 11,4.
- Le rectangle `A = Δe · τ_ARF` de l'article est **infirmé** par nos mesures, pas seulement
  son ajustement en loi de puissance. La thèse d'invariance survit, mais elle repose
  désormais sur la mesure directe de l'aire, et non plus sur la dérivation de l'article.
- L'étalon mesure la reconquête de la zone dont la vérité a changé, sous contrainte de ne
  pas sacrifier le reste. Ce n'est pas « l'adaptation » dans l'absolu : c'est une
  définition, opposable, et elle doit être écrite telle quelle dans le rapport.
- L'étalon n'est **pas calculable en ligne** : il exige de connaître `b`. Le critère 5 du
  § 1 de la note (« calculable en ligne ») est explicitement abandonné pour lui, et
  conservé pour les candidats.
- Les sondes sont communes à tous les runs d'une amplitude : leur erreur d'échantillonnage
  est un **biais partagé** que le bootstrap sur les graines ne capture pas. Mesuré par un
  second tirage : 1,4 % par run, au pire **3,1 %** sur la moyenne par amplitude.
- À `Δe = 0,028`, la bande est si étroite que l'étalon lui-même discrimine mal :
  `acc_bande(0)` vaut 0,344 avec drift contre 0,330 sans. Les conclusions à cette
  amplitude reposent donc sur un étalon peu contrasté, ce qui doit être dit.
- Le segment haut de grille (six dernières cellules, 3,2 % d'étendue en `Δe`) ne permet
  **aucune** estimation d'exposant : les valeurs calculées y atteignent −49 et ne se
  citent pas. Elles sont conservées dans la table, marquées `estimable = False`.
- Le test B2 est rapporté mais **non disqualifiant** : bien prédire l'alarme récompense la
  contamination par la trajectoire d'erreur, motif exact pour lequel « retour de l'erreur »
  a été écarté comme circulaire. Le cas de `S_max(H)` y est **tautologique** — l'alarme
  *est* le franchissement de `S_max` par `λ`, donc son AUC vaut 1,000 par identité et non
  par performance. La colonne `tautologique` de la table le dit.
- **Le domaine de validité en `Δe` n'a pas été déclaré *a priori*** pour chaque candidat,
  alors que le § 8 l'exige. Les tests portent donc sur les 20 amplitudes pour tout le monde.
  C'est une lacune du pré-enregistrement, pas une restriction faite après coup : aucun
  domaine n'a été rétréci au vu des résultats.
- **`A(H)`, `S_max(H)` et l'étalon ne sont pas indépendants.** Par construction
  `e_t − p̂₀ ≈ Δe · (1 − acc_bande(t))` ; vérifié sur la campagne, l'identité tient à 5–10 %
  près au milieu de la grille. Leur τ-b avec l'étalon relève donc en partie d'une identité
  algébrique. Même remarque, plus forte, pour `V(t)` : il est calculé sur **les mêmes votes,
  les mêmes sondes et la même fenêtre** que `acc_bande`. Son « B1 19/20 » n'est pas une
  validation externe et ne doit pas être présenté comme telle.
- **L'étalon sature sur la moitié de sa fenêtre.** `acc_bande` atteint son plateau vers
  `t ≈ 200` alors que `W_e = 500` : le coefficient de variation de l'étalon tombe de 16,8 %
  à `Δe` = 0,028 à 2,1 % à `Δe` = 0,498. En haut de grille il ne discrimine presque plus, et
  les τ-b y mesurent surtout du bruit. `W_e` avait été déclaré avant mesure, ce qui est
  régulier, mais la perte de résolution se publie avec le verdict.
- **Le plancher sans drift n'est pas soustrait de l'étalon.** À `Δe` = 0,028, l'étalon vaut
  259,8 avec drift contre **170,3 sans aucun drift** : 65 % de sa valeur y est atteignable
  sans qu'il se passe quoi que ce soit. L'étalon passe malgré tout son propre contrôle A1
  (AUC 0,085 en bas de grille, 0,000 ailleurs).
- **`N(W = 2000)` est anti-informatif sur les 20 amplitudes** (AUC A1 = 0,913) : sur
  l'horizon complet, le drift produit **moins** de remplacements que son absence — 14 en
  médiane sans drift contre 8 à 13 avec. Soit le drift éteint le renouvellement de fond
  après la rafale initiale, soit c'est un artefact d'horizon. **Non tranché**, et à ne pas
  présenter comme un résultat avant de l'avoir instruit.
- **Multiplicité non corrigée** : B1 compte 260 tests à 5 %, dont 191 significatifs. Le
  signal domine largement, mais les cellules dont le `|τ-b|` avoisine 0,15 ne se citent pas
  individuellement sans correction.
