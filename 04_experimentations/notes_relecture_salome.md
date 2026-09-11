# Notes de relecture — Salomé

Remarques relevées en relisant le business case et les rédactions, du 8 au 11 septembre 2026.
Chaque entrée indique si elle est traitée ou encore ouverte.

---

## A. Business case — points ouverts

Ces trois remarques portent sur `01_consignes/Business_case_Filiere_Recherche_Blind_Spot_FIN.md`.
Le document est l'énoncé du prof, donc rien n'y a été modifié : ce sont des points à
soulever, ou à contourner dans nos rédactions.

### A.1 — « chaque bascule est un drift » (§ Trois caractéristiques, point 1)

Le mot « drift » est employé sans qualificatif juste après un paragraphe qui distingue
soigneusement concept drift et data drift. L'affirmation devient soit triviale (tout
changement est un changement), soit fausse : passer d'un régime calme à un régime agité
change la volatilité, rien n'oblige `P(y | X)` à changer.

Dans l'exemple du CAC 40 le momentum s'inverse effectivement — mais c'est une
observation empirique sur les marchés, pas une nécessité logique.

### A.2 — Les points 1 et 2 décrivent le même événement

« Un marché alterne des phases calmes et des phases turbulentes » (point 1) et « la
volatilité se regroupe en paquets » (point 2) énoncent **la même alternance**, avec deux
vocabulaires. Le recouvrement est en partie lexical : volatilité est la grandeur
mesurée, turbulence le mot qualitatif pour une période où elle est élevée.

Ce qui distingue réellement les deux points, c'est ce qu'on en déduit — le point 1 porte
sur les vrais drifts que la bascule provoque, le point 2 sur les fausses alarmes que la
turbulence entretient **ensuite**, une fois le modèle adapté. Le premier est un instant,
le second une phase.

Reformulation possible :

> Un marché alterne des phases calmes et des phases turbulentes. Trois caractéristiques
> de cette alternance rendent la détection difficile :
> 1. **Les vraies ruptures sont fréquentes** : une bascule change souvent la relation
>    prédictive elle-même — le momentum s'inverse. C'est alors un vrai concept drift.
> 2. **L'hétéroscédasticité produit de fausses alertes** : une fois le nouveau régime
>    installé, la forte volatilité maintient le taux d'erreur élevé alors que la relation
>    ne bouge plus. Un détecteur réglé sur une phase calme continue donc d'alarmer
>    longtemps après que le modèle s'est adapté.
> 3. **L'absence de vérité terrain empêche de trancher** : on ne sait pas à quel instant
>    exact le régime a changé, donc lesquelles de ces alarmes étaient justifiées.

### A.3 — Tension entre la ligne 61 et le point 2

La ligne 61 affirme qu'un data drift est « sans conséquence sur la qualité des
prédictions ». Le point 2 décrit précisément une situation où le taux d'erreur monte sans
concept drift. Les deux énoncés se contredisent en apparence.

La résolution : l'affirmation de la ligne 61 n'est vraie qu'**à difficulté de tâche
constante**. Quand la volatilité monte, `y` devient intrinsèquement moins prévisible —
même un modèle parfait se tromperait davantage. Au sens strict c'est d'ailleurs un
concept drift, puisque `P(y | X)` change ; mais un concept drift contre lequel
réentraîner ne sert à rien, la frontière optimale n'ayant pas bougé.

### A.4 — « L'architecture standard vise le second »

Se lit comme « ne retient que le second », alors que l'architecture déploie bien les deux
briques. La distinction à faire : l'ARF n'est pas l'option 1 (robuste par construction),
il est **réactif** — il se dégrade d'abord, se répare ensuite, et ne prévient personne.
Seul le détecteur externe poursuit l'objectif de surveillance.

Formulation possible : « L'architecture standard poursuit ce second objectif : elle
associe un classifieur adaptatif, qui garde les prédictions justes, et un détecteur
externe, chargé de prévenir. »

---

## B. Question A — point ouvert

### B.1 — L'événement `{τ_ARF < +∞, τ_det = +∞}` n'est pas traité

L'énoncé demande explicitement (ligne 166) : « À quoi correspond l'événement
`{τ_ARF < +∞, τ_det = +∞}` ? Doit-il être comptabilisé parmi les points aveugles ? »

La section *Probability Space and Boundary Cases* de `redaction_QA_course_concurrente.tex`
traite la double famine `{+∞, +∞}` et le choix strict/large, mais pas cet événement-là.

La réponse découle de leur propre définition : avec `Miss := {τ_ARF < τ_det}` sur les
réels étendus, un `τ_ARF` fini est strictement inférieur à `+∞`, donc l'événement **est**
compté dans `Miss`. Et c'est la forme la plus pure du point aveugle — la forêt a réparé,
le détecteur n'a jamais parlé. Plus grave que `τ_ARF < τ_det < +∞`, où l'alarme finit par
arriver.

Il manque une phrase le disant, et disant pourquoi ce choix est le bon : l'exclure
reviendrait à ne compter que les exécutions où le détecteur a fini par parler,
c'est-à-dire à réintroduire le biais de sélection que la question A reproche au manuscrit.
À placer **avant** le cas de la double famine, qui se comprend par contraste.

---

## C. Question C.2 — corrigé

Toutes les entrées de cette section ont été appliquées à
`redaction_QC2_certificat_deterministe.tex` (commits `afc6f4d` et `fa720b2`).

### C.1 — « le compteur monte de `Δe − δ_P` par pas » était faux

À chaque pas le compteur monte de `+0,97` ou descend de `0,03` ; jamais de `Δe − δ_P`.
C'est l'**espérance** de l'incrément qui vaut `Δe − δ_P`. La formulation initiale
réintroduisait exactement le mélange des niveaux que le document reproche au manuscrit.

Nuance supplémentaire : à cause du `max(0, ·)`, la hausse moyenne réelle de `S` est
même *supérieure* à `Δe − δ_P` juste après la rupture, puisque `S` part de la barrière.
Simulation à `Δe = 0,25` : 0,264 au pas 1, convergence vers 0,240.

### C.2 — « `A(H)` n'atteint jamais 45 » était faux

Vrai de la médiane par amplitude, faux des exécutions. Sur les 2 000 exécutions,
`A(0,H)` atteint **28 dans 473 cas**, **45 dans 66 cas**, **70 dans aucun**. Seul 70
n'est réellement jamais atteint.

Le certificat en fenêtre entière démontre donc la détection pour 24 % des exécutions à
`λ = 8`, 3 % à `λ = 25`, aucune à `λ = 50`. À la plus faible amplitude
(`Δe = 0,028`), pour aucune.

### C.3 — `cert.` et `obs.` ne s'opposent pas comme preuve et mesure

Les deux colonnes sont **le même calcul** — « le compteur atteint-il `λ` ? » — sur deux
fenêtres différentes, `]0,w]` et `]0,H]`. Recalculé depuis les traces : 0,79 et 0,94 à
`Δe = 0,287`, `λ = 25`, avec le même code au seul paramètre de fenêtre près.

Conséquences :
- `cert. ≤ obs.` est **mécanique** puisque `w ≤ H`, ce n'est pas un contrôle de
  cohérence ;
- `obs.` n'est pas une estimation avec intervalle de confiance, c'est un décompte exact
  comme `cert.` ;
- ce qui renseigne, c'est leur **écart** : 11 points à `λ = 25`, soit autant d'alarmes
  déclenchées après le transitoire, donc non attribuables à la dérive.

### C.4 — Trois quantités étaient confondues sous « fenêtre entière »

| | condition | portée |
|---|---|---|
| instance en un bloc | `A(0,H) ≥ λ + H·δ_P` | une seule fenêtre |
| `cert.` | `∃` sous-fenêtre de `]0,w]` | toutes les sous-fenêtres du transitoire |
| `obs.` | `∃` sous-fenêtre de `]0,H]` | toutes les sous-fenêtres de l'horizon |

L'instance implique `obs.` sans être impliquée par `cert.`, et c'est de loin la plus
faible des trois. Le contre-exemple des dix erreurs oppose l'instance à `obs.`, pas
`cert.` à `obs.` — rien ne le disait.

### C.5 — Le texte décrivait une condition, le tableau en calculait une autre

La version anglaise écrivait `A(0,w) ≥ λ + w·δ_P` (la fenêtre `]0,w]` prise d'un bloc)
alors que les chiffres publiés sont la version quantifiée `S_max(w) ≥ λ`. Écart mesuré
jusqu'à 10 points :

| `Δe` | tableau | ce que disait le texte |
|---|---|---|
| 0,141 | 0,44 | 0,39 |
| 0,243 | 0,78 | 0,76 |
| 0,416 | 0,40 | 0,30 |

Contrôle : la reconstruction de la version quantifiée reproduit `certificat_court_l25`
exactement, écart `0` sur les 20 amplitudes.

### C.6 — Sources manquantes

- L'équation du CUSUM : équation (3) du manuscrit, section III-D. Le manuscrit écrit
  `p_0` (socle fixe), l'énoncé `p̂_0` (socle estimé).
- `S_{τ*} = 0` : imposé par le protocole R2 et par l'énoncé, mais la Proposition 3 du
  manuscrit conserve au contraire `S_{τ*} = s_0 ≥ 0` et souligne que la valeur pré-rupture
  « enters explicitly rather than being set to zero ». Poser `s_0 = 0` est une
  spécialisation du protocole, pas une reprise de la simplification corrigée en v64.
- `w = 3 × 18,5/Δe` : règle imposée par l'énoncé ; `18,5` est le préfacteur `K_ARF` de
  l'ajustement du manuscrit (section III-C), le facteur 3 est la marge de couverture.

---

## D. Point ouvert, hérité de C.2

### D.1 — La fenêtre courte est mal dimensionnée aux faibles amplitudes

`w` est calculé depuis l'ajustement `18,5 · Δe^(−0,98)`, dont C.3 établit qu'il n'est
valide qu'au milieu de la grille. À `Δe = 0,028` il prédit `τ_ARF = 611` alors que la
mesure donne **118** — un facteur 5.

La fenêtre prescrite y vaut donc 1 969 pas pour un transitoire réel de ~118. Elle paie un
péage de 19,69 au lieu des ~3,5 qu'une fenêtre de `3 × 118 = 354` pas coûterait. C'est
très probablement pourquoi le certificat s'effondre à 0,10 sur cette ligne : pas par
manque de preuve, mais par mauvais dimensionnement hérité d'un ajustement invalide à cet
endroit.

La règle est imposée, donc on l'applique — mais le signaler montre qu'on a compris
pourquoi la dernière ligne du tableau décroche, et relie proprement C.2 à C.3.
