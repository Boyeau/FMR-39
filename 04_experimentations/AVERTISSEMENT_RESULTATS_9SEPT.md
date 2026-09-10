# Avertissement : cinq résultats qui touchent le travail des autres pistes

**Écrit le 9 septembre 2026 par Ulysse (piste socle / C·D).**
À lire avant de rédiger A, B ou C.1. Tout est vérifié sur la campagne
`resultats_R2/resultats/data/` et reproductible par
`resultats_R2/scripts/chiffres_QD.py`.

Trois de ces cinq points **corrigent des affirmations qui circulaient déjà** dans le
`JOURNAL.md` et qui étaient fausses ou mal cadrées. Si vous avez rédigé quelque chose à
partir d'elles entre le 7 et le 9 septembre, c'est à relire.

---

## 1. Question A — le point aveugle dépend du couple (λ, Δe), pas de λ seul

**Ce qu'on peut écrire :** à `λ = 8`, le détecteur bat la forêt (`τ_det < τ_ARF`) dans
**95,44 %** des 1 906 exécutions non censurées, **90,95 %** si on impute les censurées en
défaites. À `λ = 25` : **6,56 %**. À `λ = 50` : **0 %** (sur la seule exécution non
censurée).

**⚠️ Le piège.** Ce taux n'est pas stationnaire en `Δe`. À `λ = 8` :

| `Δe` | non censurées | le détecteur gagne |
|---|---|---|
| 0,028 | 10/100 | **0 %** |
| 0,085 | 96/100 | 62 % |
| 0,141 | 100/100 | 88 % |
| ≥ 0,194 | 100/100 | 94 à 99 % |

Le 95,44 % est une moyenne dominée par 18 amplitudes faciles sur 20. **À `Δe = 0,028`, le
détecteur ne gagne jamais, même au seuil le plus sensible testé.** Écrire « le point
aveugle est une propriété du réglage » est donc incomplet : abaisser `λ` ne le supprime
pas en bas de grille.

**Pour A :** la course a un vainqueur qui dépend de deux paramètres. Une carte
`P(τ_ARF < τ_det)` en fonction de (`λ`, `Δe`) est directement calculable depuis
`QCD_indicateurs_full.parquet`, sans relancer quoi que ce soit.

---

## 2. Question B — 🚫 la conclusion sur la dépendance entre arbres est RETIRÉE

Le `JOURNAL.md` § 2 (test C1) concluait : « quasi-indépendance sous bruit, forte
dépendance sous drift franc », en s'appuyant sur le rapport `τ_ARF(M)/τ_ARF(M=5)` qui vaut
0,054 à `Δe = 0,028` et 0,831 à `Δe = 0,498`.

**Le test correct inverse la conclusion.** Le rapport brut n'est pas un test
d'indépendance. Sous indépendance, la médiane attendue à `M` se prédit depuis la
distribution empirique à `M = 5` par `S₅^(M/5)`. Le rapport observé sur prédit vaut alors :

| `Δe` | observé / prédit sous indépendance |
|---|---|
| 0,028 | 1,31 |
| **0,243** | **1,71** (maximum) |
| haut de grille | 1,09 à 1,20 |

L'écart maximal à l'indépendance est **au milieu de la grille**, pas sous drift franc. Le
0,831 du haut de grille vient d'un **plancher de délai** (15 à 25 pas, quand `τ` à `M = 5`
va de 0 à 60), pas d'une dépendance forte.

**S'ajoute un problème de puissance :** ces cellules ne portent que **20 exécutions**
chacune. IC [0,034 ; 0,215] et [0,774 ; 1,000].

**Pour B : ne rien bâtir sur ce point sans une campagne dédiée.** Le sens de la variation
de la dépendance avec l'amplitude n'est pas établi par ce dispositif. L'argument PQD de B
reste entier par ailleurs : il ne dépendait pas de ce résultat.

---

## 3. Question B — le périmètre de l'effondrement à forte amplitude était mal cité

Le `JOURNAL.md` § 9.1 e écrivait « à `Δe ≥ 0,45`, 1 505 runs sur 2 000 sont signalés et 654
dégénèrent définitivement ». **Les deux comptes portent sur la grille entière**, pas sur la
bande haute.

Chiffres corrects :

- sur les 2 000 runs : 1 505 signalés, 654 dégénérés définitifs ;
- le signalement commence dès `Δe = 0,194` et sature à 100/100 dès `Δe = 0,391` ;
- **restreint à `Δe ≥ 0,45`** (9 amplitudes sur 20, 900 runs) : **900/900 signalés,
  652/900 définitifs** — soit 99,7 % des dégénérés définitifs.

La conclusion se durcit sur la bande haute, mais « 1 505 sur 2 000 » ne se cite pas comme
un chiffre de cette bande. **Le domaine de validité de toute la grille haute est concerné :
à `Δe ≥ 0,45`, la forêt ne s'adapte pas, elle répond « toujours 0 ».**

---

## 4. Questions A et B — `τ_ARF` n'est PAS monotone en `Δe`

Médiane de `τ_ARF` : **118** pas à `Δe = 0,028`, **346** à `Δe = 0,085`, puis décroissance
jusqu'à **28** en haut de grille. Étendue réelle 28 à 346, facteur **12,4**.

Ce n'est pas un artefact de la médiane : les moyennes font le même chemin (162,7 puis
385,9), et les IC bootstrap des deux médianes sont **disjoints** ([93,5 ; 158] contre
[281 ; 451], 10 000 tirages, Mann-Whitney p = 5·10⁻⁷).

> **Précisé le 10 septembre.** Ces deux IC n'étaient émis par aucun script. Recalculés par
> `derives_QD.py` (percentile, graine 0, 10 000 tirages, témoins passés) et écrits dans
> `QCD_ic_medianes_tau_arf.parquet` : **[92,5 ; 158,5] contre [281 ; 455]**. Toujours
> disjoints, la conclusion ne bouge pas ; ce sont ces valeurs qui sont dans QD2.

En revanche la **position** du pic n'est pas établie : 346 (`Δe = 0,085`) et 263
(`Δe = 0,141`) ne sont pas séparables (p = 0,24). On peut écrire qu'un pic existe à basse
amplitude, pas qu'il est à une cellule précise.

**Conséquence :** toute formule du type « `τ_ARF` décroît en `Δe` » est fausse en bas de
grille, et l'ajustement `18,5·Δe^(−0,98)` de l'article s'y trompe d'un facteur 5 (rapport
mesuré/prédit = 0,19 à `Δe = 0,028`, 2,08 à `Δe = 0,141`).

---

## 5. Question C.1 — Alexandre : tes deux figures restent bonnes, leur lecture change

Le merge du 9 septembre a produit un conflit sur `redaction_QC1_hierarchie.tex`, tranché
sur les données (`QCD_tau_err_full.parquet`) et non sur l'ancienneté.

**Ce que disent les données**, vérifié deux fois :

- **4 violations** de la conjecture sans condition de persistance, à
  `Δe = 0,028 / 0,085 / 0,141 / 0,194` ;
- dont **2 seulement** sont à des amplitudes non interprétables (0,028 et 0,085) ;
- les **2 autres** (0,141 et 0,194) sont à des amplitudes où le test **a** la puissance de
  trancher : elles ne tombent que par la condition de persistance de 20 pas, le
  franchissement étant relevé au pas 101 dans les deux cas ;
- avec persistance : **0 violation**.

La version qui annonçait « 2 violations, toutes là où le test est aveugle » venait d'avant
le correctif `a6f7bd5` du 8 septembre 17h03. C'est précisément l'affirmation que le
`JOURNAL.md` § 4 documente comme fausse : *« dire que les violations se situent exactement
là où le test est aveugle affaiblit le résultat plutôt que de le renforcer : c'est la
persistance qui fait le travail, pas le manque de puissance »*.

**Tes deux figures sont conservées et restent correctes.** Vérifié : elles ne lisent que
`interpretable`, `seuil` et `sigma_courbe`, et le champ `interpretable` est bien
`seuil > 2·sigma_courbe` (exact sur les 20 lignes). Seules leurs légendes ont été
rectifiées : elles situent la **frontière de puissance**, elles ne localisent pas les
violations.

*Réserve mineure signalée au passage :* `Fig_QC_tauerr_power_full` trace une bande
±2·√(ē(1−ē)/n) ≈ 0,018 alors que le critère d'interprétabilité utilise le σ empirique de
queue (0,0153). Deux estimateurs de bruit différents sur la même figure. Sans conséquence
sur le verdict, mais à harmoniser si la figure part au rapport.

---

## Ce qui a changé dans la réponse de la question D

Pour information, puisque cela touche la formulation générale du paradoxe.

Le `JOURNAL.md` affirmait que `τ_ARF` ne porte « aucune information sur la quantité de
preuve offerte au détecteur, qui est pourtant la seule grandeur décidant de l'alarme ». La
phrase est accrochée au mauvais objet :

- sur `A(H)` (aire d'erreur excédentaire) : **0/18 discernable**, médiane +0,053 — le
  journal a raison ;
- sur `S_max(H)` : **15/18 discernable**, médiane **+0,213**, IC entièrement au-dessus de
  zéro à toutes les amplitudes à partir de `Δe = 0,287`.

Or **c'est `S_max(H)` qui décide l'alarme**, pas `A(H)` : l'alarme *est* le franchissement
de `S_max` par `λ`. Réponse tranchée en deux temps, détaillée dans
`redaction_QD3_stratification_amplitude.tex`.

---

## Deux chiffres versionnés qui étaient faux, désormais corrigés

- **« 18 à 48 % de l'adaptation acquise à `τ_ARF` »** (`JOURNAL.md` § 1 et
  `resultats_R2/README.md`) : non reproductible sous aucune restriction. `R` va de
  **−0,188 à +0,885**, est négatif sur 5 amplitudes et n'est pas monotone. La formule qui
  en découlait — « tôt dans l'adaptation, tard dans la course » — est retirée.
- **« une trentaine de remplacements » sans drift** (`JOURNAL.md` § 2 b) : recompté sur
  **100 exécutions** au lieu de 12, c'est **14 en médiane**, pour 9 arbres distincts sur
  10. L'erreur de base 0,0228 est confirmée (0,0226). Le **0,0125** de la forêt sans
  remplacement reste **non recalculable** depuis les tables versionnées.

---

## Méthode, pour mémoire

Ces cinq points sortent de deux relectures adverses en contexte vierge, plus une
vérification dédiée. Le protocole vaut d'être réutilisé : **faire réfuter un résultat par
quelqu'un qui n'a pas participé à sa production, avant de le transmettre.** Les deux
objections les plus graves de la session ont été trouvées indépendamment par les deux
relecteurs, et aucune ne portait sur un calcul faux : toutes portaient sur un **périmètre**
mal déclaré ou une **règle** appliquée après en avoir adopté une autre.

Questions ou désaccord : ouvrir le sujet avant de rédiger, pas après. Les tables sont dans
`resultats_R2/resultats/data/`, et `chiffres_QD.py` réimprime tout.
