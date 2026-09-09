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
- À l'instant `τ_ARF`, **49 à 76 %** de la preuve est déjà accumulée — sur le domaine de
  décision (18 amplitudes) ; sur la grille entière `G` descend à **0,102**, et la
  restriction se publie avec le chiffre.
  > **Correction du 9 septembre 2026.** Cette ligne annonçait « seulement 18 à 48 % de
  > l'adaptation est acquise », et concluait « l'indicateur arrive tôt dans l'adaptation et
  > tard dans la course ». Les deux sont faux. `QCD_R_et_G_full` donne
  > `R_tau_arf ∈ [−0,188 ; +0,885]` sur la grille et `[−0,188 ; +0,588]` sur le domaine de
  > décision : **négatif sur 5 amplitudes**, et **non monotone** en `Δe`. Le « 18 à 48 % »
  > n'est reproductible sous aucune restriction. À `Δe = 0,085`, `R = 0,885` : l'essentiel
  > de l'adaptation est déjà acquis à `τ_ARF`, l'inverse du verdict annoncé. La formule
  > « tôt dans l'adaptation, tard dans la course » est retirée ; ce que la table soutient
  > est plus étroit et figure en `redaction_QD1_*.tex`. Le même chiffre faux était dans
  > `README.md`, corrigé au même endroit.
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

Sans le moindre drift, la forêt renouvelle quand même ses arbres, par pur bruit — ADWIN à
horloge 1 est très réactif. Son erreur de base vaut alors **0,0228**, contre **0,0125**
pour une forêt qui ne remplace jamais rien.

> **Précisé le 9 septembre.** Le comptage « une trentaine de remplacements » venait de
> `verif_biais.py` sur 12 exécutions, sortie non persistée. Recompté sur la campagne
> `A1_nodrift` (**100 exécutions**, table versionnée) : **14 remplacements en médiane**,
> pour **9 arbres distincts sur 10** renouvelés sur l'horizon, erreur moyenne **0,0226**.
> L'erreur de base est confirmée à trois décimales ; le comptage, lui, était surestimé
> d'un facteur 2. Le **0,0125** de la forêt sans remplacement reste **non recalculable**
> depuis les tables versionnées : il ne se cite qu'avec sa réserve, et le § 7.1 en fait
> déjà un point ouvert.

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

> **Corrigé le 9 septembre, § 10.7 et § 10.9.** Cette entrée disait que « l'artefact
> n'apparaît que si les points observés ne sont pas parfaitement ordonnés entre eux », et
> donnait « 0,846 contre 0,600 ». Les deux sont faux. Ce qui annule l'écart n'est pas
> l'ordre des observés mais des **ex æquo des deux côtés**, donc un `τ_ARF` lui-même
> censuré — ce qui n'arrive jamais (`censored_arf = 0,0000`). Avec `τ_ARF` non censuré et
> les observés **ordonnés**, l'écart vaut déjà **0,071129** ; anti-ordonnés, **0,261170**.
> L'ordre amplifie l'artefact, il ne le crée pas. Chiffres dans
> `QCD_contre_exemple_kendall.parquet`, calculés à la main et par `scipy`.

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

## 10. Les rédactions de la question D (9 septembre)

Quatre `.tex` écrits d'un coup depuis les tables existantes, sans relancer la campagne.
Trois dérivés manquaient et ont été produits hors ligne (`derives_QD.py`), trois figures
ont été refaites, et quatre choses découvertes en chemin méritent d'être écrites.

### 10.1 Ce que la rédaction a changé au verdict de D

**Le résultat central de D était accroché au mauvais objet.** Le § 1 ci-dessus affirme que
`τ_ARF` ne porte « aucune information sur la quantité de preuve offerte au détecteur, qui
est pourtant la seule grandeur décidant de l'alarme ». Les deux moitiés de la phrase ne
parlent pas du même objet :

- sur `A(H)` — l'aire d'erreur excédentaire — le journal a raison : **0/18 discernable**,
  médiane `+0,0526`, tous les IC contiennent zéro ;
- mais la grandeur qui **décide** l'alarme est `S_max(H)`, pas `A(H)` : le § 8 le dit
  lui-même, « l'alarme *est* le franchissement de `S_max` par `λ` ». Et sur `S_max(H)` :
  **15/18 discernable**, médiane `+0,2129` — les 15 amplitudes à partir de
  `Δe = 0,287`, sans exception.

> **Attention au compte, relevé par l'audit.** La colonne `discernable` des tables
> implémente la règle du **seuil** (`|τ_b| > 0,13295637`) et donne **14/18**. La règle
> retenue dans D est celle de l'**IC** (§ 10.8), qui donne **15/18** : les deux ne
> diffèrent que sur `Δe = 0,287`, dont l'IC `[+0,0027 ; +0,2519]` exclut zéro alors que
> son `τ_b = 0,1308` passe juste sous le seuil. Lire `discernable` après avoir adopté la
> règle de l'IC était une incohérence interne — les deux critiques adverses l'ont levée
> indépendamment. **Le compte publié est 15.** Sur `A(H)` les deux règles coïncident
> (0/18), le verdict n'y est pas affecté.

La réponse tranchée de D se lit donc en deux temps, et c'est ce qui est écrit dans
`redaction_QD3_*.tex` : `τ_ARF` ne dit **rien** de `A(H)`, et porte une association
**faible mais réelle** avec `S_max(H)` au-dessus de `Δe ≈ 0,29`.

Le sens du biais résiduel renforce les deux : `A(H)` et `S_max(H)` ne sont jamais censurés
et ne portent aucun bloc d'ex æquo, donc la correction du `τ_b` ne s'applique que du côté
de `τ_ARF` et déplace les deux coefficients **vers zéro**. Le nul de `A(H)` n'est pas un
artefact d'ex æquo, et le signal de `S_max(H)` est plutôt sous-estimé.

### 10.2 Une tautologie qui allait être publiée comme une mesure

`tau_swap_10` a un `τ_b` de **1,000000 sur 20/20 amplitudes, IC [1,000 ; 1,000]**. C'est
une **identité** : à `M = 10`, un quota de 10 % exige un arbre, donc
`τ_swap(10 %) = τ_ARF`, ce que le § 1 (C.1 a) établit déjà. La ligne restait dans la table
et sur la heatmap sans marque, où elle se lit comme une association parfaite mesurée.
Elle est désormais **hachurée sur la figure** et déclarée tautologique dans le texte, sur
le précédent de `S_max(H)` en B2 (§ 8). Elle est conservée plutôt que supprimée : elle
vérifie que l'instrumentation reproduit une identité qu'elle doit reproduire.

### 10.3 Le piège de la fenêtre n'est pas refermé

Le § 4 dit « corrigé en bornant la fenêtre à `τ_ARF/2` ». La borne **est** appliquée
(`fenetre_palier` tombe à 43, 25, 18, 14…) et `R` reste **négatif sur 5 amplitudes**,
jusqu'à `−0,188` à `Δe = 0,243` où le bornage est actif. Ce n'est donc pas un artefact
d'estimation réparé : un `R` négatif signifie que l'erreur moyenne à `τ_ARF` est
**au-dessus** du palier estimé juste après la rupture, c'est-à-dire qu'elle monte encore
quand le premier arbre est remplacé. Écrire « corrigé » serait faux, et c'est écrit tel
quel dans `redaction_QD1_*.tex`.

Dans la même veine : `ecart_palier_theorie` est négatif sur **20/20** amplitudes
(`−0,0271` à `−0,0080`), jamais positif une seule fois. Le palier mesuré est
systématiquement sous `p̂₀ + Δe`. Les deux mécanismes sont déjà au § 2 (a et b, c) — socle
gonflé par le mécanisme de remplacement, et tâche facilitée en haut de grille.

### 10.4 `Fig_QD_series_internes.png` est inutilisable pour D.1

Son panneau supérieur est une **moyenne glissante de 50 pas** tracée sur
`np.arange(len(e)-L+1)`, donc décalée d'environ 24,5 pas. À `τ_ARF` médiane = 28 pas en
haut de grille, le décalage est **du même ordre que la grandeur mesurée**, et le business
case interdit explicitement ce filtrage (« détruit la synchronisation avec `τ*` »). Son
troisième panneau trace `acc_bande/haut/bas`, c'est-à-dire **l'étalon** et non l'état
interne du détecteur, ce qui importerait dans D toutes les réserves du § 8 sur l'étalon.
La figure reste au dépôt pour le banc, elle **ne sert pas** D.1.

`Fig_QD_trajectoires_full.png` a été refaite à la place : quatre marqueurs
(`τ_det`, `τ_ARF`, `τ_50%`, `τ_rec`) au lieu d'un, **trois amplitudes** au lieu d'une
(§ 4 : « une relation vérifiée à une amplitude se vérifie sur toute la grille »), et
labels en anglais.

**Piège nouveau, à ajouter au § 4 — une échelle qui rend la figure muette.** En axe
linéaire, les quatre marqueurs du haut de grille tombent tous dans les cinquante premiers
pas d'un axe qui en compte 2 000 : ils se superposent en quelques pixels et la figure ne
se lit plus, alors qu'elle est censée montrer leur ordre. L'axe est passé en échelle
logarithmique. Une figure qui « marche » n'est pas une figure qui montre.

### 10.5 Le point aveugle est une propriété du réglage, pas du dispositif

Mesuré sur les runs non censurés : `τ_det < τ_ARF` dans **95,44 %** des cas à `λ = 8`,
**6,56 %** à `λ = 25`, **0 %** à `λ = 50`. À `λ = 8` le détecteur gagne la course presque
toujours ; à `λ = 50` il ne part jamais (1 exécution sur 2 000). La bascule tient
entièrement dans la plage `λ ∈ [8 ; 50]`. C'est la course de la question A relue depuis
cette campagne, et cela nuance la formulation du paradoxe : il n'y a pas de point aveugle
en soi, il y en a un à partir d'un certain seuil.

### 10.6 Le socle sur deux fenêtres

Le business case exige de rapporter le socle à 1 000 **et** à 3 000 pas.
`QCD_indicateurs_full.baseline_window` n'en contenait qu'un (3000). Recalculé hors ligne
depuis `QCD_traces_pre_full` — la campagne avait été conçue pour cela. Contrôle : le socle
recalculé à 3 000 pas reproduit celui de la campagne à **exactement 0** d'écart.

Résultat : `p̂₀` passe de 0,022 à 0,023, et la censure de `τ_det` de 0,0405 à 0,0470
(λ = 8), 0,6045 à 0,6110 (λ = 25), 0,9990 à 0,9995 (λ = 50). **Aucun verdict ne bouge**,
mais le sens de l'écart est systématique : une fenêtre plus longue donne un socle plus
haut, donc moins de preuve accumulée et moins d'alarmes.

### 10.7 L'exercice du contre-exemple de D.2 est mal posé

Le business case prescrit quatre observées « parfaitement ordonnées » pour illustrer
l'artefact de Spearman. Lu littéralement — censurés ex æquo **des deux côtés** — on obtient
`ρ = τ_b = 1,000000` exactement : aucun écart, aucune démonstration. La raison est plus
précise que « exemple mal choisi » : des ex æquo des deux côtés exigent que `τ_ARF` soit
lui-même censuré, or `censored_arf = 0,0000` sur les 2 000 exécutions. **La configuration
sous laquelle l'exercice ne montre rien est une configuration qui ne peut pas se produire
dans les données qu'il illustre.**

Les trois configurations sont calculées et publiées
(`QCD_contre_exemple_kendall.parquet`) : écart `ρ − τ_b` de 0,000000 (prescription
littérale), 0,071129 (observées ordonnées, `τ_ARF` non censuré), **0,261170** (observées
anti-ordonnées). Chaque coefficient est calculé à la main **et** par `scipy`, les deux
coïncidant à 2,2e−16 près : c'est le contrôle sur cas connu.

### 10.8 Deux règles de significativité incompatibles, tranchées

`discernable` applique `|τ_b| > 0,13295637` ; le critère pré-enregistré du banc (B1)
applique « IC bootstrap excluant 0 ». Les deux divergent sur **exactement 3 cellules** sur
108. **C'est la règle de l'IC qui est retenue** dans D, pour trois raisons écrites dans
`redaction_QD4_*.tex` — dont la plus solide : le seuil fixe ne dépend que de `n` et ignore
la structure d'ex æquo de la paire testée, alors que le § 10.1 montre que cette structure
diffère systématiquement entre les `τ_swap(q)` et les grandeurs jamais censurées.

**Réserve déclarée :** l'antériorité du critère de D **n'est pas revendiquée**. Le § 8 de
`pistes_remplacement_tauARF.md` fige les critères **du banc** (A1/A2/B1/B2/C1/D1-D3), pas
ceux de D : ni l'indicateur évalué, ni ses comparateurs, ni le domaine `Δe ≥ 0,10`, ni le
seuil. Les colonnes `dans_domaine_decision`, `seuil_detectabilite` et `discernable` sont
produites par le même passage d'analyse que les coefficients. C'est le reproche jumeau de
celui déjà porté au § 8 sur le domaine de validité.

### 10.9 Ce que le double audit a corrigé (9 septembre)

Deux critiques adverses en contexte vierge, l'une sur la fidélité au plan et le code,
l'autre sur la plausibilité des résultats. **Deux objections bloquantes, six majeures.**
Les deux bloquantes ont été trouvées **indépendamment par les deux critiques**.

1. **Adopter une règle puis publier le compte de l'autre.** D.4 fixe la règle de l'IC,
   puis D.3 annonçait « 14/18 » — le compte de la colonne `discernable`, qui implémente
   la règle du seuil, celle qui vient d'être écartée. Le bon compte est **15/18**.
   La faute est instructive : une colonne pré-calculée porte une règle implicite, et la
   lire après en avoir adopté une autre passe inaperçu parce que le chiffre *existe*.
   **Règle : quand deux critères coexistent, le compte se recalcule depuis le critère
   retenu, jamais depuis une colonne héritée.**
2. **Un chiffre hors domaine opposé à un critère in-domaine.** D.4 reprochait à
   `τ_swap(75 %)` de dépasser d'un facteur 16 le critère de censure de 5 %, sur la foi
   des 78 % mesurés à `Δe = 0,085` — amplitude qui est **hors** du domaine de décision
   (`dans_domaine_decision = False`). Dans le domaine, le pire est 54 % à `Δe = 0,141`,
   soit un facteur **10,8**. Le reproche tenait, sa magnitude était fausse.
3. **Un marqueur publié là où le test est aveugle.** `τ_rec` était tracé à
   `Δe = 0,085`, amplitude déclarée `interpretable = False` par le même script quelques
   fonctions plus haut. Le marqueur est désormais **en pointillé et étiqueté comme tel**.
4. **Deux comptes confondus.** « quatre amplitudes franchissent au premier pas » : non,
   **deux** (`tau_err_p1 == 1`) ; les deux autres franchissent au **pas 101**. Quatre est
   le compte des *violations*, pas celui des franchissements immédiats.
5. **Un chiffre hérité sous une autre définition.** « seuil franchi au pas 92 » à
   `Δe = 0,498` venait du § 2 c, où il désigne le franchissement de `p̂₀` **seul**. Sous
   la définition utilisée en D (`p̂₀ + ρ·Δe`), c'est **46**.
6. **Une monotonie supposée.** D.2 écrivait que `τ_ARF` « tombe de 118 à 28, rapport
   4,2 ». `τ_ARF` **monte d'abord** à 346 à `Δe = 0,085` : étendue réelle 28–346,
   facteur 12,4, **non monotone**. L'argument contre Pearson en sort renforcé, pas
   affaibli — mais il était appuyé sur une description fausse.
7. **Une conclusion réfutée par sa propre table.** D.2 concluait que l'artefact
   n'apparaît « que si les observées ne sont pas ordonnées ». Sa ligne 2 montre un écart
   de 0,071 avec des observées **ordonnées**. Ce qui sépare vraiment les lignes 1 et 2
   est la **censure de `τ_ARF`**, pas l'ordre. ⚠️ Le § 4 de ce journal porte la même
   confusion et ses chiffres « 0,846 contre 0,600 » sont périmés : voir § 10.7.
8. **Traçabilité.** Les chiffres 95,44 % / 6,56 %, les fenêtres de palier et les comptes
   de franchissement étaient exacts mais **n'étaient émis par aucun script**. Ajoutés à
   `chiffres_QD.py`. Les deux contrôles du socle, qui n'existaient que dans un `print`,
   sont écrits dans `QCD_socle_controles.parquet` — un contrôle qui n'est pas relisable
   n'est pas un contrôle.
9. **`n_models`, `delta_P`, graine et `n_boot`** sont désormais écrits dans **toutes**
   les tables d'analyse, pas seulement les deux nouvelles.

### 10.10 Ce qui n'est pas traité, et pourquoi

L'énoncé officiel de D demande la corrélation de `τ_ARF` avec l'erreur résiduelle **et
avec le temps effectif de retour à la normale**. Le second n'est pas calculé comme
corrélation par exécution, et la raison est écrite dans `redaction_QD1_*.tex` plutôt que
tue : `τ_err(ρ)` n'est défini que sur la courbe moyennée, une valeur par amplitude, alors
que les corrélations de D se calculent exécution par exécution — les deux objets ne sont
pas commensurables. Indépendamment, « retour de l'erreur à l'acceptable » échoue au test de
la tâche facilitée (§ 2 c, § 3).

Également non traité : tout `M` autre que 10 ; toute corrélation impliquant `τ_det` à
`λ = 25` ou `λ = 50`, pour cause de censure ; l'indice C de Harrell, inutile ici puisque
l'horizon est commun et que la comparaison imputé / cas complets montre que le choix ne
change rien (écart max 0,0403).

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
