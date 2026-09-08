# Remplacer τ_ARF — pistes testées, et ce qu'elles donnent

Note de travail, 7 septembre 2026. Fait suite à la question C, qui établit que
`τ_ARF` ne mesure pas ce qu'il prétend mais ne dit pas par quoi le remplacer.

**Trois pistes ont été formulées puis testées. Deux sont infirmées, une reste ouverte.**
Le principal résultat de cette note n'était pas prévu : il porte sur le coût permanent
du mécanisme de remplacement lui-même.

Scripts : `resultats_R2/scripts/`, où `probe_metriques.py` et `verif_biais.py` rejouent
les mesures de cette note.

---

## 1. D'abord, séparer deux usages

`τ_ARF` sert à deux choses incompatibles dans l'article : dater l'adaptation de la
forêt, et alimenter la course contre le détecteur. La question C.2 a montré que le
second usage est illicite pour un temps, puisque le seuil `λ` est un volume de preuve.

Il faut donc **deux objets distincts, pas un remplaçant unique**. Pour la course, C a
déjà désigné les candidats : `A(H)` et `S_max(H)`, homogènes au seuil et jamais
censurés. Ce qui suit ne concerne que le premier usage, mesurer l'adaptation.

Critères qu'un tel indicateur devrait remplir, tels que C permet de les formuler :

1. **granularité suffisante** — critère relatif, « au moins autant de valeurs distinctes que
   `τ_ARF` sur la même strate », et non un seuil absolu.
   > **Correction du 8 septembre 2026.** Ce critère affirmait : « continu — `τ_ARF` compte des
   > arbres, donc ne prend que 11 valeurs avec `M = 10` ». C'est faux. `τ_ARF` est un **instant**
   > (`analyse_QCD.py:137`), pas un comptage : il prend 30 à 93 valeurs distinctes par amplitude
   > sur 100 graines, 321 au total. C'est `φ(t)` qui a `M+1` états. La motivation « il faut un
   > indicateur continu » était donc mal fondée et est retirée. `τ_ARF` reste disqualifié par
   > A1 et C1, **pas** par sa granularité ;
2. **jamais censuré** — `τ_swap(75 %)` l'est jusqu'à 78 % du temps en bas de grille ;
3. **indépendant de `M`** — sinon on mesure la taille de la forêt ;
4. **regarde la forêt, pas son erreur** — sinon on explique le phénomène par lui-même ;
5. **calculable en ligne**.

---

## 2. Les trois pistes testées

### Piste A — le désaccord fonctionnel avec une forêt gelée

On garde une copie de la forêt figée à `τ*`, et on mesure la fraction du flux sur
laquelle les deux forêts ne disent plus la même chose :

```
D(t) = P( forêt_t(x) ≠ forêt_gelée(x) )
```

Chaque `x` du flux sert de sonde, donc pas de jeu de test séparé. Le raisonnement était
le suivant : après la rupture, les deux forêts ne peuvent différer que sur la bande
entre les deux frontières, de masse `Δe`. Donc `D(t)` devait monter de 0 vers `Δe`, et
l'erreur excédentaire valoir ce qui reste, c'est-à-dire :

```
H1 :   e_t − p̂₀  ≈  Δe − D(t)        d'où   A(H) ≈ Σ (Δe − D(t))
```

Si H1 tenait, le budget de preuve du détecteur serait l'intégrale du déficit
d'adaptation, ce qui relierait d'un trait C.1 et C.3.

**H1 est infirmée.** Mesuré sur 100 exécutions (5 amplitudes × 20 graines) :

| Δe | moyenne de `e − p̂₀` | moyenne de `Δe − D` | corrélation des deux courbes |
|---|---|---|---|
| 0,028 | 0,0015 | −0,0056 | −0,29 |
| 0,243 | 0,0175 | 0,0128 | 0,28 |
| 0,416 | 0,0066 | −0,0011 | 0,37 |
| 0,498 | −0,0119 | 0,0048 | 0,49 |

Les aires ne se correspondent pas non plus : à `Δe = 0,028`, `A(H)` mesurée vaut 3,02
quand la somme des déficits vaut −11,18.

Résumer ces quatre valeurs par « corrélations de 0,28 à 0,49 » escamote la première, qui est
**négative** (−0,29). L'écart à H1 n'est donc pas un lien faible mais positif : à la plus faible
amplitude, les deux courbes vont en sens **opposé**. La formulation correcte est « corrélations
de −0,29 à 0,49, de signe non constant ».

**Pourquoi ça échoue.** Le raisonnement supposait que les deux forêts ne peuvent
diverger que dans la bande. C'est faux : la forêt vivante continue d'apprendre partout,
et modifie sa frontière ailleurs que sur la zone touchée par le drift. Le désaccord
mesuré mélange donc « elle a changé d'avis à cause du drift » et « elle a simplement
continué d'apprendre ». S'ajoute que la forêt gelée porte elle-même 2,3 % d'erreur
d'approximation, qui entre dans `D` sans rien signifier.

`D(t)` atteint bien `Δe` en fin d'horizon (rapport `D/Δe` entre 1,00 et 1,03 sur les
quatre amplitudes hautes), donc l'ordre de grandeur est juste. C'est la dynamique
intermédiaire qui ne suit pas.

### Piste B — la masse de vote renouvelée

Plutôt que compter les arbres remplacés, pondérer par la performance de chacun :
`_metrics` expose la performance courante par arbre dans river, donc la fraction du
poids total détenue par des arbres nés après `τ*` est calculable sans coût.

**Peu concluant.** L'indicateur sature comme celui qu'il devait corriger :

| Δe | arbres renouvelés (sur 10) | masse de vote | valeurs distinctes sur 20 graines |
|---|---|---|---|
| 0,028 | 7,5 | 0,728 | 20 |
| 0,243 | 9,6 | 0,954 | 8 |
| 0,416 | 9,8 | 0,985 | 4 |
| 0,498 | 9,9 | 0,995 | **2** |

Au-delà de `Δe ≈ 0,4`, presque tous les arbres sont renouvelés et la masse de vote
plafonne à 0,99. Elle ne prend plus que deux valeurs distinctes sur vingt exécutions,
ce qui ne vaut pas mieux que les onze états du comptage. Le gain de granularité n'existe
qu'en bas de grille, là où la censure pose déjà problème.

### Piste C — la forêt témoin comme étalon

Pour valider une métrique il faut un étalon, c'est-à-dire une définition de l'adaptation
qui ne dépende d'aucune métrique testée. Le dispositif permet d'en fabriquer un : faire
tourner en parallèle une seconde forêt, même graine et mêmes données, mais avec
`river.drift.NoDrift` comme détecteur — elle **ne remplace jamais un arbre**, tout en
continuant d'apprendre.

L'idée était que son erreur reste à `p₀ + Δe`, matérialisant « ce qui se passerait sans
adaptation », et que l'écart entre les deux courbes mesure ce que le remplacement
apporte.

**L'étalon dans cette forme naïve est invalide.** L'erreur du témoin ne reste pas du
tout au niveau attendu :

| Δe | `p̂₀ + Δe` attendu | erreur du témoin | écart |
|---|---|---|---|
| 0,028 | 0,052 | 0,011 | −0,041 |
| 0,243 | 0,267 | 0,048 | −0,219 |
| 0,498 | 0,522 | 0,050 | −0,472 |

**Le témoin s'adapte quand même**, et presque complètement. Les arbres de Hoeffding
continuent d'apprendre et se réajustent à la nouvelle frontière sans qu'aucun
remplacement n'ait lieu.

C'est en soi un résultat, et il touche la conjecture de C.1 c : **le remplacement
d'arbres n'est pas nécessaire à l'adaptation**. L'apprentissage incrémental suffit à
ramener l'erreur près de son socle.

---

## 3. Le résultat non prévu, et le plus intéressant

En vérifiant si le témoin n'était pas avantagé au départ, on trouve ceci — 12 exécutions,
horizon court de 800 pas :

| | erreur avant la rupture | erreur après | remplacements pendant le rodage |
|---|---|---|---|
| **drift fort** (`b = 4`) | normale 0,0228 · témoin 0,0125 | normale 0,0265 · témoin 0,1766 | 34,2 |
| **aucun drift** (`b = 0`) | normale 0,0228 · témoin 0,0125 | normale 0,0231 · témoin 0,0083 | 29,7 |

Trois lectures, dans l'ordre d'importance.

**a. Le mécanisme de remplacement a un coût permanent.** Avant même la rupture, et sans
aucun drift, la forêt normale a déjà procédé à une trentaine de remplacements — par pur
bruit, ADWIN à horloge 1 étant très réactif. Résultat : son erreur de base vaut 0,0228
contre 0,0125 pour une forêt qui ne remplace rien. **Le mécanisme d'adaptation double
l'erreur de base en régime stationnaire.**

C'est un coût que l'article ne discute pas, et il est directement pertinent pour la
question C : le socle `p̂₀` sur lequel le détecteur se règle n'est pas seulement un
artefact d'approximation, il est en partie fabriqué par le mécanisme d'adaptation
lui-même.

**b. Le remplacement fonctionne bel et bien après un drift.** À 800 pas, la forêt
normale est à 0,0265 quand le témoin est encore à 0,1766. L'écart, +0,15, est quinze
fois supérieur au handicap initial. Le mécanisme ARF fait donc son travail, et rapidement.

**c. L'avantage s'efface.** Sur l'horizon complet de 2 000 pas, le témoin rattrape et
finit au même niveau, voire légèrement en dessous. Ce que j'avais d'abord lu comme
« le remplacement est contre-productif » s'explique en réalité par le handicap initial
du point (a), et non par un effet du drift. **Sans cette vérification, la note aurait
figé une conclusion fausse.**

---

## 4. Où en sont les pistes

| Piste | Statut | Ce qui reste |
|---|---|---|
| désaccord `D(t)` | relation H1 infirmée | l'indicateur reste continu et non censuré ; il faudrait le corriger du désaccord de fond, mesurable sous `b = 0` |
| masse de vote | peu utile | sature à forte amplitude, comme le comptage |
| forêt témoin | invalide en l'état | utilisable si l'on corrige le handicap initial, mesurable et stable (−0,0103) |
| `τ_erase` | non testé | date l'instant où plus aucun arbre d'avant la rupture ne subsiste. Ne prétend pas mesurer l'adaptation. Il ne date **pas** « la fin de l'alimentation du détecteur » : par le remplacement en deux temps de Gomes et al. (2017), un arbre qui substitue a déjà appris depuis son avertissement, et l'erreur continue d'alimenter le détecteur après `τ_erase` |
| retour de l'erreur | écarté | échoue au test de la tâche facilitée (voir §5, test A2) |

---

## 5. Comment valider une métrique d'adaptation

Le point de méthode, qui vaut indépendamment des pistes ci-dessus : **comparer deux
métriques entre elles ne prouve rien**, puisque deux mauvaises métriques peuvent
parfaitement s'accorder. Il faut des contrôles où la bonne réponse est connue d'avance.

### Famille A — contrôles négatifs : la métrique se tait-elle quand elle doit ?

**A1, le drift nul.** Relancer avec `b = 0` : la règle ne change jamais, donc aucune
adaptation n'est possible. Une métrique d'adaptation ne doit rien signaler.

> **Mesuré sur 100 exécutions.** Sans le moindre drift, `τ_ARF` vaut **105 en médiane**
> (quartiles 43 à 172), et n'est jamais censuré. La forêt renouvelle **9 arbres sur 10**
> en médiane, et **24 % des forêts sont entièrement renouvelées** en 2 000 pas — sans
> qu'aucune règle n'ait changé.
>
> Pour situer, `τ_ARF` sous drift vaut 118 à la plus faible amplitude et 28 à la plus
> forte. Le recouvrement des distributions se lit comme suit : la proportion de paires où
> la forêt **sans** drift réagit plus vite que la forêt **avec** drift vaut
>
> | contre | Δe = 0,028 | Δe = 0,436 | Δe = 0,498 |
> |---|---|---|---|
> | proportion | **54 %** | 23 % | 21 % |
>
> À faible amplitude, 54 % équivaut au tirage à pile ou face : **`τ_ARF` ne distingue pas
> un vrai drift de l'absence totale de drift.** À forte amplitude il discrimine
> partiellement, mais une exécution sur cinq réagit plus vite sans drift qu'avec.
> Commande : `python exp_QCD_campagne.py --no-drift --seeds 100`.

**A2, la tâche facilitée.** Pousser `b` jusqu'à ce que la classe 1 disparaisse. La forêt
n'a presque rien à apprendre, l'erreur tombe d'elle-même : une bonne métrique ne doit pas
conclure à une adaptation rapide.

> **Le retour de l'erreur à l'acceptable échoue à ce test**, ce qui suffit à l'écarter.
> À `Δe = 0,498`, l'erreur repasse durablement sous le socle dès le pas 92 alors que
> `τ_ARF` vaut 28 : le critère est franchi parce que la nouvelle tâche est plus facile,
> pas parce que la forêt a compris quoi que ce soit.

### Famille B — étalonnage : la métrique suit-elle la vérité ?

**B1, accord avec un étalon.** Voir §2 piste C : l'étalon par forêt témoin doit être
corrigé de son handicap initial avant d'être utilisable.

**B2, validité prédictive.** À amplitude fixée, la métrique sépare-t-elle les exécutions
où l'alarme part de celles où elle ne part pas ? C'est l'usage que l'article fait de
`τ_ARF`. Mesure : aire sous la courbe ROC, à `λ = 8` et 25 — à `λ = 50` il n'y a rien à
séparer, une seule exécution sur 2 000 détecte.

### Famille C — robustesse : la métrique est-elle un artefact du dispositif ?

**C1, sensibilité au nombre d'arbres.** Mesuré sur `M` = 5, 10, 20, 50, cinq amplitudes,
20 graines chacune. Médiane de `τ_ARF`, en rapport à `M = 5` :

| Δe | M=5 | M=10 | M=20 | M=50 |
|---|---|---|---|---|
| 0,028 | 1,00 | 0,35 | 0,13 | **0,05** |
| 0,243 | 1,00 | 0,86 | 0,73 | 0,73 |
| 0,416 | 1,00 | 1,06 | 0,96 | 0,86 |
| 0,498 | 1,00 | 0,97 | 0,90 | **0,83** |

**`τ_ARF` dépend bien de `M`, mais d'une façon qui change complètement selon
l'amplitude.** À la plus faible, multiplier la forêt par dix divise `τ_ARF` par vingt ;
à la plus forte, il ne bouge presque pas. Deux conséquences.

D'abord, l'indicateur **n'est pas comparable entre configurations** : une forêt de
50 arbres paraît s'adapter vingt fois plus vite qu'une de 5 sur un drift faible, sans
qu'aucune preuve n'existe qu'elle s'adapte réellement mieux.

Ensuite, et c'est un résultat qui déborde sur la question B : sous indépendance des
délais, le minimum de `M` variables décroîtrait en `1/M`, soit un rapport de 0,10 entre
`M = 5` et `M = 50`. On mesure 0,05 à faible amplitude — donc quasi-indépendance, les
remplacements y étant surtout du bruit — mais 0,83 à forte amplitude, ce qui traduit une
**dépendance très forte** entre arbres. Tous voient le même drift franc et réagissent
presque ensemble. **Le degré de dépendance entre les `τ_i` varie donc avec l'amplitude**,
ce que l'hypothèse d'indépendance du manuscrit ne prévoit pas.
Commande : `python exp_QCD_campagne.py --models 20`.

**C2, forme du drift.** Remplacer le saut brutal par une rampe. Une métrique qui ne
fonctionne que sur un drift abrupt a un domaine de validité étroit, à déclarer comme tel.
Coûteux, à réserver si le temps le permet.

### Famille D — qualités métrologiques

- **D1, fidélité** : dispersion inter-graines à amplitude fixée, rapportée à la médiane.
- **D2, taux de définition** : fraction d'exécutions où la métrique est finie. Repère,
  `τ_swap(75 %)` monte à 78 % de censure.
- **D3, granularité** : nombre de valeurs distinctes atteignables. C'est ce test qui
  disqualifie la masse de vote (2 valeurs sur 20 exécutions à forte amplitude).

---

## 6. Ce qui reste à faire

1. ~~A1 sur 100 graines~~ — **fait**, voir §5.
2. ~~C1 sur quatre tailles de forêt~~ — **fait**, voir §5.
3. **Mesurer le coût permanent du remplacement** proprement : l'écart de 0,0103 entre
   forêt normale et forêt témoin en régime stationnaire mérite mieux que 12 exécutions.
   C'est le résultat le plus original sorti de cette exploration, et il ne dépend
   d'aucune des pistes qui ont échoué.
4. **`τ_erase`**, jamais testé, alors qu'il est déjà dans l'énoncé et calculable depuis
   les traces existantes sans relancer aucune campagne.

## 7. Reproductibilité

`probe_metriques.py` fait tourner trois forêts sur le même flux (normale, témoin sans
remplacement, copie gelée) et enregistre erreur, désaccord et masse de vote pas à pas.
Compter environ 20 minutes pour 100 exécutions : l'appel à `_metrics` à chaque pas est
coûteux, et gagnerait à être échantillonné tous les 10 pas si l'on rejoue l'expérience.

`verif_biais.py` compare les erreurs avant et après rupture entre forêt normale et
témoin, sur horizon court. C'est ce script qui a évité de figer une conclusion fausse ;
tout étalon fondé sur une forêt de référence doit passer par cette vérification.

---

## 8. Critères de succès du banc — figés le 8 septembre 2026, avant toute mesure

Cette section est recopiée du plan `candidats-metrique-reaction-foret.md` (v2, après double
audit adverse) **avant** que le moindre chiffre du banc ait été calculé, et committée telle
quelle. C'est ce commit qui rend le verdict opposable : sans lui, tout seuil pourrait être
soupçonné d'avoir été choisi après avoir vu les résultats — reproche que le `JOURNAL.md` § 8
porte déjà, à raison, sur le critère d'acceptabilité de C.1 b.

### L'étalon

L'adaptation réelle est mesurée contre la **vérité analytique**, que le dispositif connaît :
après la rupture, `y*(x) = 1{x₀+x₁ > b}` et l'erreur de Bayes est nulle (`JOURNAL.md` § 2a).
Aucune forêt de référence n'intervient. Trois jeux de sondes fixes, tirés d'avance par un
générateur séparé, jamais appris, échantillonnés conditionnellement à leur région :

| Région | Condition | Vérité avant | Vérité après | Ce qu'elle mesure |
|---|---|---|---|---|
| `R_bande` | `0 < x₀+x₁ ≤ b` | 1 | **0** | ce que la forêt doit réapprendre |
| `R_haut` | `x₀+x₁ > b` | 1 | 1 | compétence à **conserver** |
| `R_bas` | `x₀+x₁ ≤ 0` | 0 | 0 | compétence à **conserver** |

**Étalon scalaire par run** : `Étalon = aire sous acc_bande(t) sur [0, W_e]`, avec `W_e = 500`
pas, déclaré ici et jamais une date. Publiés à côté, jamais agrégés dedans :
`min_t acc_haut(t)` et `min_t acc_bas(t)`. Un run dont la compétence conservée chute de plus de
10 points est **signalé**, pas silencieusement compté — c'est ce contrôle qui rend visible
l'effondrement dégénéré sur « toujours 0 », lequel saturerait `acc_bande` à 1.

Le critère 5 du § 1 (« calculable en ligne ») est **explicitement abandonné pour l'étalon**,
qui exige `b` ; il reste exigé des candidats.

### Déclarations préalables, par candidat

- son **orientation** (valeur haute = plus réactif, ou valeur basse) — sans quoi « AUC ≤ x »
  n'a pas le même sens pour un temps et pour une aire ;
- son **domaine de validité en Δe**, choisi *a priori* sur un argument de construction, jamais
  d'après les résultats. Un domaine restreint après coup annule le pré-enregistrement.

### Les huit tests, tous stratifiés par amplitude, tous avec IC bootstrap apparié sur les graines

| Test | Critère figé |
|---|---|
| **A1 — se tait sans drift** | AUC contre `b = 0`, rapportée avec son plancher mécanique `0,5 × taux d'ex-æquo`. Disqualifie si `AUC > plancher + 10 points` |
| **A2 — insensible à la facilitation** | le candidat ne doit pas indiquer une adaptation plus forte ou plus rapide en haut de grille (Δe ≥ 0,45) qu'au milieu (0,25–0,40), alors que l'étalon montre une compétence conservée qui chute. Opérationnalisé par le signe de la pente en Δe, comparé à celui de la pente de l'étalon |
| **B1 — suit l'étalon** | Kendall τ-b avec l'étalon, à amplitude fixée, IC bootstrap excluant 0. Rapporté deux fois : imputation à l'horizon **et** cas complets seuls, avec le taux de censure. Un τ-b dont l'IC contient 0 disqualifie. Les candidats ne sont **pas** classés par τ-b brut entre eux : la censure le tire vers 0 et les régimes de censure diffèrent |
| **B2 — validité prédictive** | `λ = 25` seulement. Test **secondaire et non disqualifiant** : bien prédire l'alarme récompense la contamination par la trajectoire d'erreur, motif exact pour lequel « retour de l'erreur » a été écarté comme circulaire |
| **C1 — indépendant de M** | grandeurs extensives normalisées par `M` avant le test. Rapport des médianes M=5 → M=50 dans **[0,7 ; 1,4]**, avec IC bootstrap sur le rapport ; un IC qui chevauche la borne est déclaré **indécis**, pas disqualifié |
| **D1 — fidélité** | écart interquartile rapporté à la médiane, à amplitude fixée. Rapporté **sans seuil** : sert à départager deux candidats qui passent le reste |
| **D2 — censure** | ≤ 5 % sur le domaine déclaré |
| **D3 — granularité** | nombre de valeurs distinctes sur 100 graines, par amplitude. Critère **relatif** : au moins autant que `τ_ARF` sur la même strate |

**« Non disqualifié » ne se lit jamais « validé ».** Seul B1 stratifié départage ; les sept
autres tests ne font qu'éliminer.

### Livrable minimal, même si tous les candidats tombent

La table de synthèse « candidat × test » avec IC, deux mesures alternatives définies et
caractérisées, et un verdict écrit. Le sujet pose qu'un résultat négatif rigoureusement établi
vaut une confirmation.

### Interprétation pré-enregistrée du scénario le plus probable

Le § 2 piste C ci-dessus établit que la forêt témoin, qui ne remplace **jamais** d'arbre,
ramène son erreur de 0,522 attendu à 0,050 mesuré : l'adaptation passe surtout par
l'apprentissage incrémental. Si tous les candidats fondés sur le comptage de remplacements
échouent B1, ce n'est donc **pas** un échec de la recherche : c'est la confirmation
quantitative, contre un étalon fonctionnel, que *le remplacement d'arbres n'est pas le
mécanisme de l'adaptation*. C'est écrit ici avant mesure pour que ce résultat ne puisse pas
être présenté après coup comme une trouvaille.
