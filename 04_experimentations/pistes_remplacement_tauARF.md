# Remplacer τ_ARF — pistes testées, et ce qu'elles donnent

Note de travail, 7 septembre 2026. Fait suite à la question C, qui établit que
`τ_ARF` ne mesure pas ce qu'il prétend mais ne dit pas par quoi le remplacer.

**Trois pistes ont été formulées puis testées. Deux sont infirmées, une reste ouverte.**
Le principal résultat de cette note n'était pas prévu : il porte sur le coût permanent
du mécanisme de remplacement lui-même.

Scripts : `ulysse/scripts/`, où `probe_metriques.py` et `verif_biais.py` rejouent
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

1. **continu** — `τ_ARF` compte des arbres, donc ne prend que 11 valeurs avec `M = 10` ;
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
| `τ_erase` | non testé | reste le candidat le plus honnête : il ne prétend pas mesurer l'adaptation, il date la fin de l'alimentation du détecteur |
| retour de l'erreur | écarté | échoue au test de la tâche facilitée (voir §5, test A2) |

---

## 5. Comment valider une métrique d'adaptation

Le point de méthode, qui vaut indépendamment des pistes ci-dessus : **comparer deux
métriques entre elles ne prouve rien**, puisque deux mauvaises métriques peuvent
parfaitement s'accorder. Il faut des contrôles où la bonne réponse est connue d'avance.

### Famille A — contrôles négatifs : la métrique se tait-elle quand elle doit ?

**A1, le drift nul.** Relancer avec `b = 0` : la règle ne change jamais, donc aucune
adaptation n'est possible. Une métrique d'adaptation ne doit rien signaler.

> **Déjà mesuré, et concluant.** Sans le moindre drift, la forêt renouvelle 6 à 9 arbres
> sur 10 en 2 000 pas, et `τ_ARF` vaut 54, 105, 108 et 560 selon la graine — contre 30
> sous un drift fort. `τ_ARF` signale une adaptation du même ordre qu'il y ait rupture ou
> non. C'est l'argument le plus court contre lui, et le plus difficile à contester.
> Mesuré sur 4 exécutions seulement : à refaire sur 100 avant de l'écrire au rapport.
> Commande : `python exp_QCD_campagne.py --no-drift`.

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

**C1, sensibilité au nombre d'arbres.** Refaire avec `M` = 5, 10, 20, 50 à amplitude
fixée. `τ_ARF` étant le minimum de `M` délais, il décroît mécaniquement quand la forêt
grandit, sans qu'elle s'adapte plus vite. C'est le test qui devrait le disqualifier le
plus nettement. Commande : `python exp_QCD_campagne.py --models 20`.

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

1. **A1 sur 100 graines** plutôt que 4, pour pouvoir l'écrire au rapport. Quelques
   minutes de calcul, l'option existe déjà.
2. **C1 sur quatre tailles de forêt.** Devrait disqualifier `τ_ARF` de façon simple à
   défendre en soutenance.
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
