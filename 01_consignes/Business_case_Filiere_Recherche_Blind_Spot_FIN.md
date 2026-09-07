# Étude de cas — Le paradoxe du point aveugle « Blind Spot »

**Filière Recherche · 3e année · Groupe de 4 à 5 étudiants · 2 semaines**

---

## 1. Contexte: la course entre adaptation et détection

Un modèle de machine learning déployé en production apprend sur des données qui changent. En finance, un modèle calibré sur un marché calme continue de produire des signaux quand le marché devient turbulent — sauf qu'ils sont devenus faux. Ce changement temporel de la relation conditionnelle `P(y | X)` entre les variables d'entrée `X` et la cible `y` s'appelle un [concept drift](#concept-drift) ([Gama et al., 2014](#bibliographie)). Il se distingue du [data drift](#data-drift), qui ne concerne que l'évolution de la distribution des entrées `P(X)` ([Moreno-Torres et al., 2012](#bibliographie)).

Cette distinction modifie radicalement l'architecture de surveillance.

```
DATA DRIFT — le détecteur regarde les entrées

    X ──┬──► [ Détecteur ] ──► Alarme
        └──► [ Modèle ]    ──► prédictions

    Pas besoin d'étiquettes. Pas de boucle : le détecteur ignore le modèle.
```

```
CONCEPT DRIFT — le détecteur regarde les erreurs du modèle

    X ──► [ Modèle adaptatif ] ──► ŷ ──► erreur e = 1(ŷ ≠ y) ──► [ Détecteur externe ] ──► Alarme
                  ▲                                │
                  └──────── se répare tout seul ───┘
                            (et fait retomber e)

    Il faut les étiquettes y. Et il y a une boucle.
```

C'est cette boucle qui pose problème.

L'architecture standard en flux de données associe deux briques. Un **classifieur adaptatif**, qui se répare tout seul : l'[ARF](#arf-adaptive-random-forest) est une forêt d'arbres où chaque arbre possède son propre détecteur interne à fenêtre adaptative, [ADWIN](#adwin), et se fait remplacer quand il se dégrade. Et un **détecteur externe cumulatif** comme [CUSUM / Page-Hinkley](#cusum--page-hinkley), qui accumule l'excès d'erreur au fil du temps et alarme quand le cumul dépasse un seuil.

La première brique répare. La seconde prévient l'humain : elle déclenche un réentraînement, un audit, une mise en pause de la stratégie.

**Le problème.** L'ARF se répare continuellement, ce qui fait redescendre son taux d'erreur. Si cette réparation est plus rapide que le temps d'accumulation de la preuve par le détecteur externe, le signal d'erreur disparaît avant que l'alarme ne se déclenche. Le modèle va bien, l'opérateur n'a rien vu, et personne ne sait que le monde a changé. C'est le *paradoxe du point aveugle*.

Contre-intuitivement, **plus le drift est violent, plus il risque de passer inaperçu** : un gros choc déclenche une réparation plus rapide, donc un signal plus bref.

C'est ce phénomène que décrit l'article [*The Blind Spot Paradox: When Adaptive Classifiers Defeat Drift Detectors*](https://github.com/TheBlindSpot-ICDM2026/The-Blind-Spot-Paradox-Experiments/blob/main/docs/manuscript/articleA_blindspot_v64_camera_ready.pdf), soumis à IEEE ICDM 2026.

---

## 2. Etat de l'article de référence

Quatre experts internationaux l'ont évalué. Ils reconnaissent l'intérêt du phénomène et la qualité du dispositif expérimental — le code est public, les expériences sont rejouables. Ils pointent en revanche des faiblesses dans la partie théorique. L'une d'elles, une simplification dans une majoration de probabilité, a déjà été corrigée : c'est la version **v64** que vous allez lire.

**Il reste la partie que nous vous confions**, et qui est la plus ouverte : décrire correctement la **course entre le classifieur et le détecteur** quand le classifieur est une forêt.

---

## 3. Un enjeu majeur en Finance

Le phénomène est général — il apparaîtrait sur n'importe quel flux. Il a été découvert sur des données financières, pour une raison simple : ce sont les séries où le drift est à la fois le plus fréquent, le plus brutal et le plus coûteux. En salle de marché, identifier les concept drifts, ou « changements de régime », constitue un défi majeur : lorsqu'un choc macroéconomique se produit, les dynamiques des prix de nombreux actifs et les relations entre ces actifs peuvent être profondément affectées.

**Un exemple concret.** *On cherche à prédire le signe du rendement du CAC 40 le lendemain. La variable cible `y` vaut 1 si le rendement est positif, 0 sinon. Les variables explicatives `X` sont les rendements des cinq derniers jours, la volatilité réalisée sur vingt jours, le volume échangé et un indice de volatilité implicite.*

En régime calme, les tendances persistent : une série de hausses récentes annonce plutôt une hausse. Le modèle apprend cette relation. Survient un choc — annonce macroéconomique, tension géopolitique — et le marché bascule en régime de stress. Les mêmes valeurs de `X` ne prédisent plus le même `y` : le momentum s'inverse, les hausses récentes annoncent désormais des corrections brutales. La loi `P(y | X)` a changé alors que `X` peut très bien avoir gardé la même allure. C'est un [concept drift](#concept-drift). Si seule la volatilité de `X` avait augmenté sans que la relation change, on aurait un simple [data drift](#data-drift), sans conséquence sur la qualité des prédictions.

Trois caractéristiques rendent ces séries difficiles:
1. **Les régimes** : un marché alterne des phases calmes et des phases turbulentes, et chaque bascule est un drift.
2. **L'[hétéroscédasticité](#hétéroscédasticité)** : la volatilité se regroupe en paquets, et un détecteur réglé sur une phase calme se met à alarmer en continu dès qu'elle monte.
3. **L'absence de vérité terrain** : sur des données de marché réelles, il est difficile voire impossible de déterminer à quel instant exact le régime a changé, donc personne ne peut mesurer si un détecteur a raison.

C'est pour cette dernière raison que l'article utilise en partie [ProteuS](#proteus), un générateur de flux financiers synthétiques qui reproduit l'hétéroscédasticité et les changements de régime **avec des instants de rupture connus**. On peut donc compter les détections manquées et les fausses alarmes.

On a alors besoin de l'un ou de l'autre — un modèle prédictif robuste au concept drift par construction, ou un objectif intermédiaire : un détecteur fiable qui dise quand recalibrer nos modèles, qu'il s'agisse de modèles prédictifs des prix ou de modèles de pricing de produits financiers « dérivés ». L'architecture standard vise le second. Paradoxalement, c'est le bon fonctionnement du classifieur adaptatif qui casse la surveillance : en se réparant, il efface lui-même la preuve que le détecteur attendait.

Le résultat obtenu sur ProteuS est le plus parlant de l'article. Pour éviter les fausses alarmes causées par la volatilité, il faut un seuil de détection élevé (`λ ≥ 15`). Pour attraper le drift avant que la forêt ne l'efface, il faut un seuil bas (`λ ≤ 12,4`). Les deux contraintes ne se recouvrent pas : aucun réglage ne fonctionne. Un détecteur à fenêtres comme [KSWIN](#kswin) — qui compare deux fenêtres du flux d'erreur au lieu d'y accumuler de la preuve — résiste mieux sur les réglages testés, sans que son immunité soit établie en général.

### Le dispositif expérimental de référence (R2)

Pour valider et étendre la théorie, votre travail s'appuiera sur l'expérience instrumentée **R2**. Afin de dissocier les effets mécaniques purs des artefacts liés à la complexité des données financières, cette expérience emploie un flux synthétique contrôlé. Il est crucial de maîtriser les trois mécaniques suivantes :

**1. Définition du drift et génération des données**
Dans l'expérience de référence **R2**, le flux de données est synthétique et traité de façon séquentielle. À chaque pas de temps $t$, on observe deux caractéristiques continues tirées aléatoirement et indépendamment : $x_0, x_1 \sim \mathcal{N}(0, 1)$.
La variable cible à prédire $y \in \{0, 1\}$ dépend de $X$ selon une frontière linéaire, translatée d'une quantité $b > 0$ à l'instant de rupture :
- **Régime initial** ($t < \tau^*$) : $y = \mathbf{1}_{\{x_0 + x_1 > 0\}}$.
- **Régime post-rupture** ($t \ge \tau^*$) : $y = \mathbf{1}_{\{x_0 + x_1 > b\}}$.

Le paramètre effectivement balayé dans le code est $b$ (`BOUNDARY_SHIFTS = np.linspace(0.1, 4.0, 20)`). **Ce n'est pas l'amplitude du saut d'erreur.** Un modèle parfaitement calé sur l'ancienne frontière se trompe exactement sur les points tombés entre les deux frontières ; comme $x_0 + x_1 \sim \mathcal{N}(0, 2)$, son erreur augmente de $\Delta e = \mathbb{P}(0 < x_0 + x_1 \le b) = \Phi(b/\sqrt{2}) - 0{,}5$, où $\Phi$ est la fonction de répartition de la loi normale centrée réduite. Les 20 valeurs de $b$ couvrent ainsi $\Delta e \in [0{,}028\,;\,0{,}498]$. **Toutes les questions raisonnent en $\Delta e$ et jamais en $b$** : c'est $\Delta e$ qui alimente le détecteur.

Le *concept drift* étudié est donc **abrupt** (instantané à l'instant $\tau^*$) et consiste en une translation de la frontière de décision. Les entrées $X$ restent strictement stationnaires (aucun *data drift*). L'horizon d'observation post-rupture $H$ désigne le nombre maximal de pas pendant lesquels on observe le flux après $\tau^*$ avant de déclarer un échec si aucune alarme n'a retenti (censure temporelle administrative).

**2. Mécanique du détecteur externe (CUSUM)**
Le détecteur externe est un algorithme **CUSUM (Page-Hinkley)**. Il surveille la trajectoire d'erreur du modèle en accumulant la preuve. À chaque pas, si l'erreur instantanée dépasse le socle historique d'une tolérance $\delta_P$, cet excès s'ajoute à un compteur cumulatif $S_t$. Si ce compteur retombe sous zéro, il est réinitialisé. L'alarme est déclenchée uniquement si $S_t$ franchit un seuil critique $\lambda$. Par construction, CUSUM est insensible aux erreurs isolées, mais il est vulnérable si l'erreur redescend trop vite, affamant le compteur avant que $\lambda$ ne soit atteint.

Trois détails d'implémentation de R2 comptent pour la suite. Le détecteur est **créé à l'instant $\tau^*$ et jamais avant** : il part donc de $S_{\tau^*} = 0$, aucune fausse alarme pré-rupture n'est mesurable, et le délai $\tau_{det}$ peut valoir $0$. Le socle n'est pas connu : il est estimé par la moyenne des erreurs sur les **1 000 derniers pas avant la rupture**, et c'est cette estimation $\hat{p}_0$ qui remplace le socle vrai $p_0$ dans toutes les formules. L'alarme est enfin *latchée* : une fois levée, elle le reste.

**3. Mécanique du modèle adaptatif (ARF et ADWIN)**
Le modèle prédictif est l'**Adaptive Random Forest (ARF)**. Chaque arbre de cette forêt possède son propre détecteur interne, **ADWIN**, qui maintient une fenêtre glissante sur les erreurs de cet arbre. Si ADWIN détecte une variation significative entre deux sous-fenêtres, l'arbre est considéré comme obsolète. Il est alors détruit et instantanément remplacé par un arbre neuf entraîné en arrière-plan. C'est l'**effet Hydre** : la forêt se répare par morceaux continuellement. En se réparant, l'ARF fait chuter l'erreur globale, ce qui coupe l'alimentation du compteur CUSUM externe.

La forêt compte $M = 10$ arbres. L'horloge des ADWIN internes vaut $c = 1$ dans R2 : chaque arbre teste son erreur **à chaque pas**, ce qui place la forêt à sa réactivité maximale. C'est la configuration la plus défavorable au détecteur externe, et c'est délibéré.

---

## 4. Votre mission

### Origine des quatre questions qui vous sont posées

L'article a été évalué par quatre relecteurs. Le dispositif expérimental et la reproductibilité sont salués ; le raisonnement théorique est incomplet. Trois demandes de correction ont été formulées, et **deux d'entre elles sont exactement votre sujet** :

- **Amélioration n° 1** — le manuscrit compare une variable aléatoire à une constante, et suppose une indépendance sans la démontrer → **[Questions A et B.](#41-versant-théorique--une-course-entre-deux-horloges-aléatoires)**
- **Amélioration n° 2** — le manuscrit date l'adaptation de la forêt au premier arbre remplacé, sans montrer que cet instant a le moindre rapport avec la disparition du signal → **[Questions C et D.](#42-versant-expérimental--mesurer-la-véritable-adaptation)**

**Votre objectif est de construire ces deux pièces manquantes** : une formalisation propre de la course entre les deux mécanismes, et une mesure de ce que vaut réellement l'indicateur qui a été utilisé.

### Vue d'ensemble des quatre questions

L'article mesure la vitesse de réparation de la forêt par **le temps écoulé jusqu'au premier arbre remplacé**, noté `τ_ARF` (Définition 2 du manuscrit). Il compare ce temps à celui qu'il faut au détecteur pour alarmer. Deux choses clochent dans cette comparaison. Ce sont vos deux versants:

| Question | Ce qui cloche dans l'article                                                                               | Ce que votre réponse doit établir                                                                         | Par quel chemin                                                                    |
| -------- | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **A**    | Le temps d'alarme du détecteur est remplacé par une constante, et les exécutions sans alarme sont écartées | La probabilité que la forêt gagne la course, **correctement définie malgré des observations incomplètes** | Conditionnement sous horizon fini, puis encadrement de Fréchet dans le cas général |
| **B**    | L'indépendance entre les arbres est supposée sans preuve                                                   | Le **sens** de l'erreur que cette hypothèse introduit                                                     | Conditionnement par le flux, puis inégalité de convexité — ou contre-exemple       |
| **C**    | Le premier arbre remplacé est présenté comme la date d'adaptation de la forêt                              | Si cet instant mesure ce qu'il prétend mesurer, et sinon, **par quoi le remplacer**                       | Construction d'une famille d'indicateurs, et comparaison de leurs unités           |
| **D**    | Aucune trajectoire synchronisée n'existe ; le lien entre l'ancien indicateur et la réalité n'est pas testé | La **force du lien** entre l'indicateur de l'article et vos indicateurs alternatifs                       | Instrumentation du code, puis corrélation de rang par amplitude                    |

Les questions A et B forment le **versant théorique**, C et D le **versant expérimental**. Les deux versants se répondent : C et D fournissent les lois que A et B manipulent, A et B disent quoi mesurer.

### Notations proposées

| Symbole      | Définition                                                                                                                                                                                                                                                                                                                       |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `τ*`         | Instant de rupture, **connu** par construction (`T_DRIFT = 4 000` dans [**R2**](https://github.com/TheBlindSpot-ICDM2026/The-Blind-Spot-Paradox-Experiments/blob/main/experiments/R2_instrumented_blind_spot/exp_R2_instrumented_blind_spot.py), ou point de saut sous ProteuS dans R4)                                          |
| `M`          | Nombre d'arbres de la forêt (`M = 10` dans les expériences)                                                                                                                                                                                                                                                                      |
| `τ_i`        | Délai, compté depuis `τ*`, du premier remplacement de l'arbre `i`                                                                                                                                                                                                                                                                |
| `τ_ARF`      | `min_i τ_i` — délai du premier remplacement dans la forêt                                                                                                                                                                                                                                                                        |
| `τ_det`      | Délai, compté depuis `τ*`, de la première alarme du détecteur externe. **Valeur `+∞` admise** (censure si non détecté avant `H`)                                                                                                                                                                                                 |
| `Miss`       | Événement constitutif du Point Aveugle, conventionnellement `{τ_ARF < τ_det}` (convention à justifier empiriquement en Question A).                                                                                                                                                                                              |
| `P_miss`     | Probabilité de l'événement Point Aveugle : `P(Miss)`.                                                                                                                                                                                                                                                                            |
| `τ_det*`     | `λ / (Δe − δ_P)` pour `Δe > δ_P` (`+∞` si `Δe ≤ δ_P`) — temps d'accumulation nominal déterministe (au premier ordre)                                                                                                                                                                                                             |
| `S`          | Réalisation complète du flux `(x_t, y_t)` pour une graine donnée (flux gaussien 2D avec rupture d'hyperplan dans [**R2**](https://github.com/TheBlindSpot-ICDM2026/The-Blind-Spot-Paradox-Experiments/blob/main/experiments/R2_instrumented_blind_spot/exp_R2_instrumented_blind_spot.py), ou série ARMA-GARCH dans R4)          |
| `U_i`        | Aléa **propre** à l'arbre `i` : tirages de Poisson du bagging en ligne, sous-espaces aléatoires de variables aux nœuds                                                                                                                                                                                                           |
| `F(s)`       | `P(τ_1 ≤ s)` — loi **marginale** du temps d'un arbre                                                                                                                                                                                                                                                                             |
| `G_S(s)`     | `P(τ_1 > s ∣ S)` — survie **conditionnelle au flux** d'un arbre                                                                                                                                                                                                                                                                  |
| `F_A`, `F_D` | Fonctions de répartition de `τ_ARF` et `τ_det` (`F_D` étant sous-stochastique si `P(τ_det = +∞) > 0`)                                                                                                                                                                                                                            |
| `H`          | Horizon d'observation post-rupture. **`H = 2 000` partout dans ce sujet** (voir l'encadré ci-dessous)                                                                                                                                                                                                                            |
| `λ`, `δ_P`   | Seuil et tolérance du détecteur cumulatif. (`δ_P = 0,01` voir `StrictCUSUM(delta=0.01)` dans [**R2**](https://github.com/TheBlindSpot-ICDM2026/The-Blind-Spot-Paradox-Experiments/blob/main/experiments/R2_instrumented_blind_spot/exp_R2_instrumented_blind_spot.py) ; `λ ∈ {8, 25, 50}` selon le scénario)                     |
| `Δe`         | Amplitude théorique du saut d'erreur au drift. (`Δe = Φ(b/√2) − 0,5` avec `b ∈ linspace(0.1, 4.0, 20)`, soit `Δe ∈ [0,028 ; 0,498]` sur 20 points dans [**R2**](https://github.com/TheBlindSpot-ICDM2026/The-Blind-Spot-Paradox-Experiments/blob/main/experiments/R2_instrumented_blind_spot/exp_R2_instrumented_blind_spot.py)) |

*Tous ces temps sont des **entiers** : le flux est discret.*

> **L'horizon d'observation est fixé pour tout le projet : `H = 2 000` pas après la rupture.** Vous n'avez aucune valeur à choisir, et les quatre questions emploient celle-là.
>
> Pourquoi 2 000. L'horizon doit couvrir la résorption de l'erreur, sinon vous mesurez une troncature au lieu d'un phénomène. Le transitoire moyen vaut environ `18,5 / Δe` pas, et il faut le couvrir largement — disons trois fois. L'amplitude la plus faible de la grille est `Δe = 0,028`, ce qui donne `3 × 18,5 / 0,028 ≈ 1 982`. Deux mille est le premier nombre rond au-dessus : il couvre donc **toute** la grille, de l'amplitude la plus faible à la plus forte.
>
> R2 dispose de 4 000 pas après la rupture (`N_STEPS = 8000`, `T_DRIFT = 4000`). Vous n'en gardez que la moitié : les 2 000 derniers n'apportent rien et doublent le coût de calcul. En revanche, **ne descendez pas sous 2 000**. Un horizon plus court ne coupe le transitoire qu'aux faibles amplitudes, ce qui fabrique une fausse dépendance en `Δe` dans absolument tous vos résultats — et cette fausse dépendance ressemble beaucoup à un vrai résultat.

### 4.1 Versant théorique — La course entre deux horloges aléatoires

Le manuscrit compare le temps d'adaptation `τ_ARF` (variable aléatoire) à une quantité déterministe `τ_det* = λ / (Δe − δ_P)`, qui représente le temps moyen nominal d'accumulation (Proposition 9). 

Dans la réalité, le moniteur externe alarme à un instant aléatoire `τ_det` qui peut être précoce, tardif, ou valoir `+∞` si la dérive n'est jamais détectée. Deux approximations majeures du manuscrit doivent être rigoureusement formalisées :
1. Le remplacement du temps d'arrêt stochastique `τ_det` par la constante `τ_det*`.
2. L'hypothèse d'indépendance mutuelle entre les `M` arbres pour modéliser `τ_ARF = min(τ_1, ..., τ_M)`.

> **Question A. Formalisation et encadrement de la course aléatoire**
>
> On étudie la probabilité d'échec de détection $P_{miss} = P(Miss)$. Le flux d'observation s'arrête à l'horizon fini $H = 2\,000$.
>
> 1. **Espace probabiliste et cas limites :**
>    - À quoi correspond l'événement $\{\tau_{ARF} < +\infty, \tau_{det} = +\infty\}$ ? Doit-il être comptabilisé parmi les points aveugles $Miss$ ?
>    - En temps discret, $P(\tau_{ARF} = \tau_{det}) > 0$. Justifiez physiquement votre choix normatif entre inégalité stricte ($\tau_{ARF} < \tau_{det}$) ou large ($\tau_{ARF} \le \tau_{det}$) pour définir l'événement $Miss$. Évaluez sur vos trajectoires l'impact matériel de cette convention (proportion d'ex æquo finis). Traitez formellement et séparément le cas de double famine $\{\tau_{ARF} = +\infty, \tau_{det} = +\infty\}$ : cet événement doit-il être comptabilisé ?
>
> 2. **Identification sous horizon fini $H$ :**
>    - L'événement de censure temporelle absolue est défini par $C_H := \{\min(\tau_{ARF}, \tau_{det}) > H\}$. Cet événement rend le vainqueur de la course inobservable. A contrario, les événements sont observables s'ils se produisent en horizon fini : c'est le cas de $\{\tau_{ARF} \le H\}$ et $\{\tau_{det} \le H\}$.
>    - Essayez de conditionner l'événement de point aveugle par l'un ou l'autre de ces événements observables afin d'aboutir à un encadrement de la probabilité inconditionnelle $P_{miss}$ par des probabilités d'événements observables (identification partielle). Calculez la proportion de vos exécutions doublement censurées sur vos données pour quantifier la largeur exacte de cet encadrement.
>
> 3. **Encadrement universel de Fréchet en temps discret :**
>    - On suppose connues les fonctions de répartition marginales $F_A$ et $F_D$, sans hypothèse sur leur dépendance. Pour encadrer $P(\tau_{ARF} < \tau_{det})$ :
>      - **Borne inférieure :** pour un entier déterministe $s \in \mathbb{N}$ fixé, minorez la probabilité de l'événement $\{\tau_{ARF} \le s < \tau_{det}\}$ via l'inégalité de Fréchet pour l'intersection, puis optimisez par rapport à $s$ en tenant compte du caractère positif d'une probabilité.
>      - **Borne supérieure :** pour un entier déterministe $s \in \mathbb{N}$ fixé, décomposez selon la partition $\{\tau_{ARF} \le s\}$ et $\{\tau_{ARF} \ge s+1\}$ pour établir l'inclusion $\{\tau_{ARF} < \tau_{det}\} \subseteq \{\tau_{ARF} \le s\} \cup \{\tau_{det} > s+1\}$ (en exploitant que les temps sont à valeurs entières), appliquez la sous-additivité de Boole, puis optimisez par rapport à $s$ en tronquant à 1.
>    - *Attention :* vérifiez la validité de votre formule sur un cas simple "jouet" uniforme discret à support $\{1, 2\}$.

> **Question B. Impact structurel de l'hypothèse d'indépendance inter-arbres**
>
> Pour modéliser l'effet Hydre, le manuscrit pose que les temps d'arbres $\tau_1, ..., \tau_M$ sont indépendants. Or, les $M$ arbres apprennent sur le même flux $S$.
>
> 1. **Factorisation et échangeabilité conditionnelle :**
>    - Sachant le flux $S$, qu'est-ce qui distingue un arbre d'un autre ? Est-il légitime de considérer que conditionnellement au flux $S$, les arbres sont indépendants ? Déduisez-en la loi de survie conditionnelle $G_S(s) = P(\tau_1 > s \mid S)$.
>
> 2. **Démonstration du sens du biais par convexité :**
>    - À l'aide de l'inégalité de Jensen appliquée à $G_S(s)$, démontrez formellement si l'hypothèse d'indépendance surestime ou sous-estime la probabilité que l'adaptation de la forêt soit rapide.
>    - Établissez la condition exacte d'égalité et donnez son sens physique vis-à-vis du flux.
>
> 3. **Conséquence opérationnelle :**
>    - Déduisez-en l'impact formel sur la probabilité d'échec de détection $P_{miss}$ : le manuscrit surestime-t-il ou sous-estime-t-il cette probabilité ? Le corollaire de l'article sur la taille critique d'ensemble $M_{crit}$ est-il infirmé, ou requalifié en certificat conservateur ?
>
> 4. **Le piège de la corrélation (Contre-exemple) :**
>    - Reprenez le cas jouet de la question **A.3** avec $M = 2$ et des marginales uniformes sur $\{1, 2\}$ ($\mathbb{P}(\tau_i = 1) = 1/2$). Définissez un couplage anti-monotone ($\tau_1 = 1 \iff \tau_2 = 2$) et montrez que $\mathbb{P}(\tau_{ARF} \le 1)$ est strictement plus élevée que sous indépendance.
>    - À l'aide de la factorisation conditionnelle de **B.1**, montrez que $\operatorname{Cov}(\mathbf{1}_{\{\tau_1 > 1\}}, \mathbf{1}_{\{\tau_2 > 1\}}) = \operatorname{Var}(G_S(1))$. Pourquoi cette identité interdit-elle le couplage anti-monotone dans l'ARF ?

### 4.2 Versant expérimental — mesurer la véritable adaptation

Le manuscrit date l'adaptation de la forêt au premier remplacement d'arbre `τ_ARF = min_i τ_i` (Définition 2). Or, remplacer un unique arbre sur `M = 10` n'altère qu'un dixième des votes dans l'ensemble : le premier remplacement marque le début d'une réaction interne, non la guérison effective du modèle ni la disparition systématique du signal d'erreur.

L'évaluation empirique exige de lever deux faiblesses méthodologiques :
1. L'absence de validité de construit de `τ_ARF` face à des grandeurs mesurant directement la résorption de l'erreur ou l'accumulation de preuve.
2. L'absence de trajectoires synchronisées permettant de quantifier le couplage réel entre l'état interne de la forêt et celui du détecteur.

Vous travaillerez sur la famille d'indicateurs ci-dessous. Les quatre premiers sont des **temps**, mesurés en pas ; les deux derniers sont des **quantités de preuve**, mesurées en erreur cumulée. Cette différence d'unité est le cœur de la question C.

| Indicateur  | Définition formelle                                  | Unité                | Censurable à `H` ?                                                                  |
| ----------- | ---------------------------------------------------- | -------------------- | ----------------------------------------------------------------------------------- |
| `τ_ARF`     | `inf{ t > τ* : N_t ≥ 1 } − τ*`                       | Temps (pas)          | Oui                                                                                 |
| `τ_swap(q)` | `inf{ t > τ* : N_t / M ≥ q } − τ*`                   | Temps (pas)          | Oui                                                                                 |
| `τ_err(ρ)`  | `inf{ t > τ* : ē_t − p̂_0 ≤ ρ · Δe } − τ*`            | Temps (pas)          | Oui, mais **grandeur d'ensemble** : une valeur par amplitude, pas une par exécution |
| `τ_erase`   | `inf{ t > τ* : ē_t − p̂_0 ≤ δ_P } − τ*` *(optionnel)* | Temps (pas)          | Oui, **grandeur d'ensemble** également                                              |
| `A(H)`      | `Σ_{t=τ*+1}^{τ*+H} (e_t − p̂_0)` sur fenêtre fixe     | Preuve (cumul d'err) | Non                                                                                 |
| `S_max(H)`  | `max_{τ* ≤ t ≤ τ*+H} S_t`                            | Preuve (cumul d'err) | Non                                                                                 |

Notations : `N_t` est le nombre d'**arbres distincts** déjà remplacés à l'instant `t`, `M = 10` le nombre d'arbres, `q ∈ (0, 1]` un quota d'arbres renouvelés, `e_t ∈ {0, 1}` l'erreur de l'ensemble au pas `t`, `ē_t` cette même erreur moyennée sur les graines, `p̂_0` le socle d'erreur pré-rupture estimé, `ρ ∈ (0, 1)` une fraction de résorption résiduelle que vous choisissez, et `S_t` la statistique du CUSUM. `τ_erase` est l'instant où l'excès d'erreur repasse sous la tolérance du détecteur : mécaniquement, c'est l'instant où le CUSUM cesse d'être alimenté.

> **Question C. Validité de construit et budget de preuve**
>
> 1. **Hiérarchie déterministe des temps de bascule :**
>    - On pose $\tau_{swap}(q) = \inf\{ t > \tau^* : N_t / M \ge q \} - \tau^*$. Établissez la relation déterministe liant $\tau_{ARF}$ et la famille $\tau_{swap}(q)$ pour tout $q \ge 1/M$. *Point de départ : $N_t$ ne peut que croître, donc $q \mapsto \tau_{swap}(q)$ est monotone ; et $\tau_{ARF}$ est lui-même un $\tau_{swap}(q)$ pour une valeur particulière de $q$ — laquelle ?* La relation obtenue vaut **sur chaque exécution**, sans aucune hypothèse probabiliste. Déduisez-en le sens du biais introduit par l'usage de $\tau_{ARF}$, et comparez ce sens à celui du biais établi en question B.
>    - L'inégalité seule ne prouve rien d'intéressant : ce qui compte est **l'écart**. Mesurez $\tau_{swap}(q) - \tau_{ARF}$ pour $q \in \{0{,}10 ; 0{,}25 ; 0{,}50 ; 0{,}75\}$, tracez-le en fonction de $\Delta e$, et annoncez à partir de quel écart vous considérez que $\tau_{ARF}$ cesse d'être un substitut acceptable.
>    - Par ailleurs, la relation $\tau_{ARF} \le \tau_{err}(\rho)$ est-elle toujours vérifiée ? Formulez une conjecture appuyée sur la nature incrémentale de l'apprentissage des arbres de Hoeffding, qui continuent d'apprendre entre deux remplacements donc sans être remplacés. **Attention à la définition avant de tester :** $e_t$ vaut $0$ ou $1$, donc $\tau_{err}(\rho)$ n'a de sens que sur la courbe moyennée sur les graines. Comparez donc **amplitude par amplitude** le $\tau_{err}(\rho)$ calculé sur la courbe moyenne à la médiane inter-graines de $\tau_{ARF}$, et rapportez pour combien d'amplitudes l'erreur se résorbe avant le premier remplacement.
>
> 2. **Analyse dimensionnelle et dynamique d'accumulation :**
>    - Quelle est l'unité physique de $\tau_{ARF}$ et celle du seuil $\lambda$ ? En quoi leur comparaison directe contourne-t-elle la nature séquentielle du détecteur ?
>    - Pour rétablir l'homogénéité, notez $A(k, j) = \sum_{t=k+1}^{j} (e_t - \hat{p}_0)$ l'aire d'erreur excédentaire brute sur la sous-fenêtre $]k, j]$, et montrez que la statistique culminante du CUSUM vaut $S_{max}(H) = \max_{0 \le k \le j \le H} [\, A(k, j) - (j-k)\,\delta_P \,]$, le maximum portant sur toutes les sous-fenêtres $]k, j] \subseteq [0, H]$. *Méthode : posez $X_t = e_t - \hat{p}_0 - \delta_P$ et $S_{\tau^*} = 0$, écrivez la récurrence $S_t = \max(0,\, S_{t-1} + X_t)$, et raisonnez par récurrence sur $t$ — le terme $0$ du maximum correspond au choix $k = t$.*
>    - Déduisez-en un **certificat déterministe** : s'il existe une sous-fenêtre $]k, j]$ telle que $A(k, j) \ge \lambda + (j-k)\,\delta_P$, alors l'alarme se déclenche nécessairement avant l'horizon. Ce certificat est vrai **sur chaque exécution prise isolément**, sans aucune moyenne ni hypothèse probabiliste.
>    - Ce certificat est-il aussi une condition **nécessaire** ? Distinguez soigneusement deux énoncés : (a) la version quantifiée ci-dessus, « il existe une sous-fenêtre telle que… » ; (b) l'instance particulière obtenue en prenant la fenêtre entière, soit $A(H) \ge \lambda + H\,\delta_P$. L'un des deux est nécessaire et suffisant, l'autre seulement suffisant. Dites lequel, et démontrez-le en une ligne à partir de l'égalité précédente.
>    - **Exploitez le certificat, dans les deux sens.** Calculez d'abord l'instance en fenêtre entière avec $H = 2\,000$ et $\delta_P = 0{,}01$, pour les trois seuils $\lambda \in \{8, 25, 50\}$ : vous obtenez trois nombres, et vous constaterez en C.3 pourquoi ils sont inatteignables. Recommencez ensuite sur une fenêtre **courte** ancrée à la rupture, $]0, w]$ avec $w = 3 \times 18{,}5 / \Delta e$ arrondi, c'est-à-dire une fenêtre taillée sur le transitoire de l'amplitude considérée. Rapportez alors, amplitude par amplitude et pour chacun des trois seuils, la fraction d'exécutions qui franchissent ce second certificat. C'est une borne inférieure **démontrée** du taux de détection, pas une estimation — et c'est la seule chose de tout le projet que vous pourrez affirmer sans marge d'erreur.
>    - En une phrase : pourquoi la fenêtre courte donne-t-elle un certificat plus fort que la fenêtre entière, alors qu'elle contient moins de preuve ?
>
> 3. **Invariance du budget de preuve :**
>    - Adoptez le modèle stylisé de l'article : après la rupture, l'erreur excède son socle de $\Delta e$ pendant un transitoire de longueur $W = \tau_{ARF}$, puis retombe au socle. En supposant que l'horizon couvre entièrement ce transitoire ($H \ge \tau_{ARF}$, ce que $H = 2\,000$ garantit sur toute la grille), exprimez $\mathbb{E}[A]$ en fonction de $\Delta e$ et de $\mathbb{E}[\tau_{ARF}]$, puis injectez l'ajustement empirique de l'article $\mathbb{E}[\tau_{ARF}] \approx 18{,}5 \cdot \Delta e^{-0,98}$.
>    - Calculez l'exposant résiduel de $\Delta e$ dans ce budget. Quantifiez la variation relative (en pourcentage) de $\mathbb{E}[A]$ sur l'intégralité de la grille expérimentale ($\Delta e \in [0{,}028 ; 0{,}498]$).
>    - Reprenez le calcul avec le budget réellement **utilisable** par le détecteur, $(\Delta e - \delta_P) \cdot W$, et non l'aire brute. À quelle extrémité de la grille la tolérance $\delta_P$ prélève-t-elle une part non négligeable du budget ? Chiffrez cette part.
>    - Concluez formellement : pourquoi un choc macroéconomique violent ne laisse-t-il pas plus de preuve au détecteur qu'une dérive lente ?
>    - Confrontez maintenant ce budget aux trois nombres calculés en C.2 pour la fenêtre entière. Que devient un certificat en fenêtre entière quand l'horizon s'allonge, et pourquoi ? C'est exactement ce qui justifie la version en fenêtre courte.
>    - Vérifiez enfin le résultat sur vos propres mesures : tracez $A(H)$ mesurée en fonction de $\Delta e$, à $H = 2\,000$, et comparez à la constante prédite. Un écart systématique n'invalide pas forcément le modèle stylisé — regardez d'abord du côté du socle $\hat{p}_0$ (voir les contraintes méthodologiques ci-dessous).

> **Question D. Auscultation des trajectoires et corrélation de rang conditionnelle**
>
> Cette question mesure la **force du lien** entre $\tau_{ARF}$ et les indicateurs alternatifs construits en question C. Deux comparaisons sont demandées, et leur structure diffère :
> - **(i)** $\tau_{ARF}$ contre $\tau_{swap}(q)$ — deux temps, tous deux censurables à $H$ ;
> - **(ii)** $\tau_{ARF}$ contre $A(H)$, puis contre $S_{max}(H)$ — un temps contre une quantité de preuve, cette dernière étant définie sur toutes les exécutions et donc jamais censurée.
>
> Toutes les corrélations se calculent **exécution par exécution, à amplitude fixée**. Les grandeurs d'ensemble ($\tau_{err}$, $\tau_{erase}$) sont par construction exclues de cette partie.
>
> 1. **Instrumentation conjointe :**
>    - Enregistrez pour chaque exécution **deux choses seulement** : la trajectoire d'erreur $e_t$ sur les $2\,000$ pas post-rupture, et les **événements de remplacement** sous la forme de couples (pas de temps, identifiant d'arbre). N'enregistrez pas le dictionnaire complet à chaque pas : il contient vingt fois plus de lignes pour exactement la même information.
>    - Tout le reste se calcule **hors ligne**, sans relancer une seule exécution : $\tau_{ARF}$, $\tau_{swap}(q)$, la trajectoire $S_t$ pour n'importe quel $\lambda$ et n'importe quel $\delta_P$, $\tau_{det}$, $A(H)$ et $S_{max}(H)$.
>    - Extrayez et tracez sur un axe temporel commun synchronisé sur $\tau^*$ :
>      1. la fraction d'arbres renouvelés $N_t / M$ (médiane et écart interquartile inter-graines) ;
>      2. l'erreur globale empirique $\bar{e}_t$ (**moyennée pas à pas sur les graines**, sans aucun lissage temporel) ;
>      3. la statistique interne cumulée $S_t$ confrontée au seuil critique $\lambda$, pour les trois valeurs de $\lambda$ sur le même graphique.
>    - Évaluez à l'instant $\tau_{ARF}$ la fraction d'adaptation déjà acquise $R(\tau_{ARF}) = [\bar{e}(\tau^*) - \bar{e}(\tau^* + \tau_{ARF})] / [\bar{e}(\tau^*) - \hat{p}_0]$ ainsi que la fraction de preuve accumulée $G(\tau_{ARF}) = S_{\tau^* + \tau_{ARF}} / S_{max}(H)$.
>    - **Précisions de calcul, sans lesquelles ces deux nombres ne veulent rien dire.** $G$ se calcule **par exécution** : $S_t$ est une grandeur continue, définie sur un run isolé. $R$ se calcule **par amplitude**, sur la courbe moyennée, en prenant pour $\tau_{ARF}$ la médiane inter-graines. Pour $\bar{e}(\tau^*)$, un seul pas de temps est bien trop bruité : estimez le palier post-rupture sur une courte fenêtre suivant $\tau^*$, et vérifiez qu'il est cohérent avec la valeur théorique $\hat{p}_0 + \Delta e$.
>    - Tracez $R$ et $G$ en fonction de $\Delta e$, et concluez sur la pertinence mécanique de $\tau_{ARF}$.
>
> 2. **Justification statistique du coefficient d'association :**
>    - Justifiez l'invalidité du coefficient de corrélation linéaire de Pearson pour ce dispositif, en vous appuyant sur trois caractéristiques physiques de l'expérience : la non-linéarité de la relation (loi de puissance), la présence de valeurs extrêmes à faible amplitude, et la censure administrative à l'horizon $H$.
>    - **Filet — ces trois raisons n'ont pas le même statut, et c'est là que les rapports dérapent.** Vous allez stratifier par amplitude en D.3, et à l'intérieur d'une strate $\Delta e$ est **constant**. Reprenez donc les trois raisons une par une et dites, pour chacune, si elle tient encore une fois la strate fixée. **L'une des trois ne tient plus** : identifiez-la et expliquez en deux phrases pourquoi. Classez ensuite les deux survivantes : l'une est une raison d'**efficacité** — Pearson se calcule mais devient instable ; l'autre est une raison de **définition** — Pearson ne peut littéralement pas se calculer, faute de valeur numérique. Dites laquelle est laquelle. C'est la seconde qui porte l'argument.
>    - Rappelez la définition du $\tau_b$ de Kendall en posant explicitement toutes ses quantités : paires concordantes, paires discordantes, et blocs d'ex æquo de chaque côté. Implémentation : `scipy.stats.kendalltau`, qui renvoie le $\tau_b$ par défaut.
>    - Face aux ex æquo massifs générés par les exécutions inachevées, démontrez pourquoi le $\rho$ de Spearman surestime artificiellement l'association, et pourquoi le $\tau_b$ de Kendall neutralise proprement cet artefact de censure. *Traitez séparément les comparaisons (i) et (ii) : dans la première les ex æquo tombent des deux côtés, dans la seconde d'un seul. La correction opérée par $\tau_b$ n'agit donc pas de la même façon — dites laquelle des deux est pleinement compensée, et dans quel sens le coefficient est déplacé dans l'autre cas.*
>    - **Vérification à faire à la main, avant d'écrire du code.** Construisez un jeu de dix exécutions fictives : six censurées des deux côtés — donc ex æquo au rang maximal sur les deux variables — et quatre observées, parfaitement ordonnées. Calculez $\rho$ de Spearman et $\tau_b$ de Kendall sur ces dix points, d'abord à la main, puis avec `scipy` pour contrôler. L'écart entre les deux valeurs **est** l'artefact que vous devez expliquer, et dix points suffisent à le voir.
>
> 3. **Stratification par amplitude et analyse de dépendance :**
>    - Calculez le coefficient $\tau_b$ avec son intervalle de confiance bootstrap séparément *à l'intérieur* de chaque strate d'amplitude $\Delta e$. Le rééchantillonnage porte sur les **graines** de la strate ; 2 000 tirages suffisent, et l'intervalle se lit sur les quantiles 2,5 % et 97,5 %.
>    - Confrontez ces résultats à un unique $\tau_b$ global calculé sur l'empilement de toutes les amplitudes confondues. En mobilisant obligatoirement votre conclusion de la question C.3 (comportement de l'aire totale), expliquez l'effondrement mécanique du coefficient global (artefact d'agrégation).
>    - Vos deux comparateurs, déclinés sur quatre valeurs de $q$ et vingt amplitudes, produisent plus d'une centaine de coefficients — dont quelques-uns paraîtront significatifs par pur hasard. Publiez-les **tous**, sous forme de carte de chaleur (amplitudes en abscisse, comparateurs en ordonnée), ou contrôlez le taux de fausses découvertes. Une sélection opérée après avoir vu les résultats n'est pas recevable, et se repère immédiatement en soutenance.
>
> 4. **Protocole de décision et sensibilité à la censure :**
>    - Définissez formellement votre critère de décision **avant de regarder la moindre corrélation**, et rendez-le à la fin de la première semaine. Il doit fixer : l'indicateur évalué, ses comparateurs, le domaine de validité ($\Delta e \ge 0{,}10$, afin d'exclure les remplacements de bruit sous stationnarité), le seuil de $\tau_b$ au-delà duquel vous concluez au lien, et la règle appliquée aux bornes des intervalles de confiance. Les valeurs exactes importent moins que le fait qu'elles aient été écrites avant.
>    - Précisez votre traitement des exécutions censurées. L'horizon $H$ est **identique pour toutes les exécutions** : une valeur censurée dépasse donc effectivement toute valeur observée, ce qui autorise à leur attribuer les derniers rangs *ex æquo*. Expliquez pourquoi cet argument tomberait si l'horizon variait d'une exécution à l'autre.
>    - Rapportez systématiquement la proportion de runs censurés par amplitude, et comparez le coefficient obtenu sur l'échantillon complet ainsi imputé à celui calculé sur les seuls cas complets. Un écart marqué entre les deux signifie que c'est la censure qui pilote le résultat, et doit être signalé comme tel plutôt que masqué.

#### Contraintes méthodologiques et métrologiques d'évaluation

- **Non-lissage temporel de l'erreur :** Le signal binaire $e_t \in \{0, 1\}$ impose d'estimer la dynamique par moyenne inter-graines à chaque pas $t$. Tout filtrage temporel décale artificiellement le front de drift d'un demi-support de fenêtre et détruit la synchronisation avec $\tau^*$.
- **Horizon post-rupture, fixé :** $H = 2\,000$, partout, sans exception. La justification et la mise en garde figurent dans l'encadré du §4. Aucune étude de sensibilité à $H$ n'est demandée : elle coûterait cher et ne produirait qu'un artefact de troncature aux faibles amplitudes.
- **Propagation de la variance du socle :** L'erreur d'estimation du socle $\hat{p}_0$ se propage de manière parfaitement corrélée sur l'intégralité de l'aire $A(H)$, induisant un biais systématique de $-H(\hat{p}_0 - p_0)$. R2 n'estime ce socle que sur les 1 000 derniers pas pré-rupture, et l'erreur-type qui en résulte est du même ordre que le budget de preuve total. **Portez la fenêtre d'estimation sur les 3 000 derniers pas pré-rupture** : le bruit est divisé par $\sqrt{3}$, et les 4 000 pas de rodage sont de toute façon déjà calculés. Deux points à retenir. Cette modification ne change **pas** $\tau_{ARF}$ : le socle n'est lu que par le détecteur externe, jamais par la forêt, donc vos temps d'adaptation restent comparables aux valeurs publiées. Elle change en revanche $\tau_{det}$ — reproduisez donc R2 à l'identique (1 000 pas) une première fois pour valider votre chaîne, puis basculez à 3 000 pas pour l'analyse, et rapportez les deux. Comparez enfin au socle théorique, que vous connaissez.
- **Sanctuarisation du rodage :** Le script effectue la rupture à $T_{DRIFT} = 4000$. **Ne réduisez pas le pré-rodage de 4000 pas** pour économiser du temps de calcul. Cette phase détermine la maturité de la forêt et la valeur du socle $p_0$. La modifier invalide toute comparaison avec l'article.
- **Seuil de détectabilité statistique :** Sous l'hypothèse nulle d'indépendance avec $n = 100$ graines, l'écart-type de $\tau_b$ est de $\sqrt{2(2n+5)/(9n(n-1))} \approx 0{,}068$. Un coefficient expérimental tel que $|\tau_b| \le 0{,}13$ n'est pas statistiquement discernable de zéro au seuil de 5 %.

---

## 5. Ressources

**Le code** : [The-Blind-Spot-Paradox-Experiments](https://github.com/TheBlindSpot-ICDM2026/The-Blind-Spot-Paradox-Experiments) — scripts des expériences `R1` à `R9`, résultats stockés, dépendances figées, tests.

**Le manuscrit** : [`articleA_blindspot_v64_camera_ready.pdf`](https://github.com/TheBlindSpot-ICDM2026/The-Blind-Spot-Paradox-Experiments/blob/main/docs/manuscript/articleA_blindspot_v64_camera_ready.pdf), dans `docs/manuscript/` du dépôt. À lire dans cet ordre, et rien de plus pour démarrer.

| Passage                                     | Page | Contenu                                                                          |
| ------------------------------------------- | ---- | -------------------------------------------------------------------------------- |
| Résumé                                      | 1    | Le phénomène en dix lignes                                                       |
| Définition 2 — Adaptation Time & Blind Spot | 2    | La définition de `τ_ARF` que vous allez remettre en cause                        |
| §III-C — The Hydra Effect                   | 3    | `τ_ARF = min(τ_1, ..., τ_M)` et l'hypothèse d'indépendance                       |
| Proposition 3 — Starvation                  | 3    | Ce qu'un détecteur cumulatif peut voir d'un signal bref (partie corrigée en v64) |
| Figure 1                                    | 4    | Remplacements internes et détections externes sur un axe commun                  |
| Proposition 9 et Corollaire 10              | 5    | La course, et la taille critique d'ensemble                                      |
| Figure 2                                    | 5    | Les trois régimes : détecteur gagnant, alarme tardive, détection manquée         |
| Table I                                     | 7    | Échec complet de CUSUM avec ARF, récupération avec KSWIN                         |
| §V-B — Limitations                          | 9    | Les auteurs y reconnaissent eux-mêmes l'hypothèse d'indépendance                 |

Le reste de l'article traite d'autres aspects. Vous pouvez l'ignorer.

### Quelle expérience produit quoi

Chaque expérience se relance seule par `./run_experiment_R<n>.sh`, ou toutes d'un coup par `./run_all.sh`. Le tableau donne la correspondance entre le script, ce qu'il mesure, et l'endroit du manuscrit où le résultat apparaît.

| Exp.   | Script                              | Ce qu'elle mesure                                                          | Où ça sort dans l'article |
| ------ | ----------------------------------- | -------------------------------------------------------------------------- | ------------------------- |
| R1     | `exp_R1_generate_data.py`           | Diagnostic de la course, balayage du seuil `λ`, alarmes tardives           | §III, Figure 1            |
| **R2** | `exp_R2_instrumented_blind_spot.py` | **Le point aveugle instrumenté** : remplacements internes vs alarmes       | §IV, Figure 2             |
| R3     | `exp_R3_regime_crossover.py`        | Bascule de régime, forêt statique vs adaptative, coût en précision         | §IV                       |
| R4     | `exp_R4_main_table.py`              | Comparatif détecteurs × classifieurs sur ProteuS                           | **Table I**               |
| R5     | `run_experiment_R5.sh`              | Évaluation sur données réelles, inondation de fausses alarmes              | **Table II**              |
| R6     | `exp_R6_generate_data.py`           | Arbre seul (HAT) de référence — donne l'accélération apportée par la forêt | §III-C                    |
| R7     | `run_experiment_R7.sh`              | Taux de détections manquées en fonction de l'amplitude du drift            | §IV                       |
| R8     | `exp_R8_lambda_op_sweep.py`         | Seuil maximal admissible `λ_op` en fonction de l'amplitude                 | §V-A                      |
| R9     | `exp_R9_compute_mcrit.py`           | Taille critique d'ensemble `M_crit`                                        | Corollaire 10             |

**Par où commencer.** `R2` est votre point d'entrée : c'est la seule expérience déjà instrumentée sur les remplacements d'arbres, et c'est celle que vous allez étendre pour la [question D](#42-versant-expérimental--mesurer-la-véritable-adaptation).

Pour la [question B](#41-versant-théorique--une-course-entre-deux-horloges-aléatoires), la comparaison à faire est **arbre seul contre forêt**, et voici où trouver chacun des deux termes. `R6` et `R9` mesurent tous deux le temps d'adaptation d'un **arbre unique** (un Hoeffding Adaptive Tree, `M = 1`) — ce n'est pas la forêt. Le temps d'adaptation de la **forêt** vient de `R2`. `R6` va d'ailleurs lire les résultats de `R2` : **il faut donc exécuter `R2` avant `R6`**, sans quoi vous obtiendrez une erreur de fichier manquant.

**Où sont les résultats.** Chaque expérience écrit dans `results/R<n>_<nom>/`, avec un sous-dossier `data/` (Parquet ou CSV) et un sous-dossier `figures/` ou `tables/`. Pour `R2` : `results/R2_instrumented_blind_spot/data/` et `.../figures/`. Des tests de non-régression existent pour `R6` à `R9` uniquement : ils vérifient que vos ré-exécutions retrouvent les valeurs publiées, mais ils supposent que les expériences correspondantes ont déjà tourné. Lancez-les avant de modifier quoi que ce soit, puis après.

**Bibliothèque** : [River](https://riverml.xyz), version 0.23.0 exactement ([Montiel et al., 2021](#bibliographie)). Le compteur interne des remplacements d'arbres est accessible via `ARFClassifier._drift_tracker`.

---

## 6. Livrables et calendrier

**Organisation suggérée** : deux à trois personnes sur le versant théorique, deux à trois sur le versant expérimental, avec au moins un point de synchronisation au milieu. Les deux versants interagissent : les mesures orientent le modèle, le modèle dit quoi mesurer.

**Semaine 1** — prise en main du dépôt et une expérience rejouée à l'identique ; formalisation écrite des questions A et B (quel est exactement l'objet aléatoire, quelles sont les hypothèses) ; première instrumentation sur une configuration simple.

**Semaine 2** — runs de mesures sur plusieurs amplitudes de drift et plusieurs graines ; démonstration de la question B, ou contre-exemple documenté ; rédaction.

**À rendre** : un rapport synthétique de 10 à 15 pages (15 pages est un maximum, 10 pages n'est pas un minimum: quelques pages suffisent si le rapport répond à tous les points du projet), un code source strictement reproductible en une commande unique, et une soutenance de 20 minutes.

**Évaluation** : clarté de la formalisation, reproductibilité du code, honnêteté sur ce qui n'a pas marché. Pas la quantité de résultats positifs.

*Un résultat négatif rigoureusement établi possède la même valeur qu'une confirmation des travaux de l'article.*

**Ce que devient votre travail.** L'article est en cours de réécriture pour une nouvelle soumission. Vos quatre réponses alimentent directement deux des corrections en cours. Vous travaillez donc sur un vrai projet de recherche.

---

<div style="page-break-before: always; break-before: page;"></div>

## 7. Glossaire

### Concept drift
Changement, au cours du temps, de la relation entre les variables d'entrée et la variable à prédire — formellement, la loi conditionnelle `P(y | X)` change ([définition générale](https://en.wikipedia.org/wiki/Concept_drift)). Un modèle entraîné avant le changement devient faux après. Référence : [Gama et al. (2014)](#bibliographie).

### Data drift
Changement de la distribution des seules variables d'entrée, `P(X)`, sans que la relation à prédire soit nécessairement affectée — on parle aussi de [*dataset shift*](https://en.wikipedia.org/wiki/Dataset_shift). Un data drift n'entraîne pas forcément une perte de performance ; un [concept drift](#concept-drift) si. Les deux se détectent avec des architectures différentes, comparées au §1. Référence : [Moreno-Torres et al. (2012)](#bibliographie).

### ARF (Adaptive Random Forest)
Forêt aléatoire conçue pour l'apprentissage en flux. Chaque arbre est entraîné en continu et possède son propre détecteur interne ([ADWIN](#adwin)) qui surveille ses erreurs. Quand un arbre se dégrade, un arbre de remplacement entraîné en arrière-plan prend sa place. C'est ce **remplacement** qui rend la forêt capable de se réparer — et qui efface le signal que le détecteur externe attendait. Référence : [Gomes et al. (2017)](#bibliographie).

### ADWIN
Détecteur de changement à fenêtre adaptative. Il maintient une fenêtre de données récentes, la coupe en deux, et déclare un changement quand les moyennes des deux moitiés s'écartent trop. Il ne teste pas à chaque pas de temps mais tous les `c` pas : ce paramètre est son « horloge ». Dans l'[ARF](#arf-adaptive-random-forest), chaque arbre en possède un. Référence : [Bifet et Gavaldà (2007)](#bibliographie).

### CUSUM / Page-Hinkley
Famille de détecteurs à **accumulation de preuve**. À chaque pas de temps on ajoute à un compteur l'excès d'erreur au-delà d'une tolérance `δ_P`, et on remet le compteur à zéro s'il devient négatif. L'alarme est levée quand le compteur dépasse un seuil `λ`. Conséquence directe : ces détecteurs ont besoin d'un signal **persistant**, et un signal fort mais bref ne les fait pas alarmer. C'est le cœur du problème étudié. Référence : [Page (1954)](#bibliographie).

### KSWIN
Détecteur qui compare la distribution d'une fenêtre récente à celle d'une fenêtre de référence, par un test de Kolmogorov-Smirnov. Il ne cumule pas de preuve dans le temps, ce qui le rend moins sensible aux signaux brefs — mais il échoue à son tour si le signal est plus court que sa fenêtre. Référence : [Raab, Heusinger et Schleif (2020)](#bibliographie).

### Instrumenter
Ajouter des points de mesure **à l'intérieur** d'un système pour observer directement son fonctionnement interne, au lieu de le déduire de son comportement extérieur. Ici : lire à chaque pas de temps le compteur interne de remplacements d'arbres de la forêt, plutôt que de simuler la course entre classifieur et détecteur avec deux processus indépendants.

C'est le standard académique sur ce sujet précis, pour une raison de fond. La plupart des comparaisons de détecteurs les évaluent sur des flux d'erreurs pré-générés, sans classifieur dans la boucle : l'interaction entre les deux devient invisible, et le phénomène étudié ici ne peut littéralement pas être observé. Instrumenter est ce qui le rend mesurable plutôt que simplement plausible — et réfutable, puisque chaque instant mesuré est vérifiable dans le code.

### Hétéroscédasticité
Propriété d'une série dont la variance change au cours du temps. En finance, la volatilité se regroupe en paquets : des périodes calmes alternent avec des périodes agitées. Un détecteur qui suppose une variance constante interprète ces variations comme des drifts et produit des fausses alarmes en rafale.

### ProteuS
Générateur de flux financiers synthétiques utilisé dans l'article. Il reproduit l'[hétéroscédasticité](#hétéroscédasticité) et les changements de régime des séries de marché, avec des instants de rupture **connus**, ce qui permet de compter les détections manquées et les fausses alarmes. Référence : [Suárez-Cetrulo, Cervantes et Quintana (2025)](#bibliographie).

### Statistiques d'ordre
Branche des probabilités qui étudie la loi du minimum, du maximum et des valeurs classées d'un échantillon ([définition](https://fr.wikipedia.org/wiki/Statistique_d%27ordre)). Si `M` variables indépendantes ont pour fonction de répartition `F`, le minimum a pour fonction de survie `(1 − F)^M`. Tout l'enjeu de la [question B](#41-versant-théorique--une-course-entre-deux-horloges-aléatoires) est de savoir ce que devient ce résultat quand l'indépendance tombe. Référence : [David et Nagaraja (2003)](#bibliographie).

### Censure sous horizon fini
Situation où l'observation s'interrompt à l'horizon `H` sans qu'un événement ne soit survenu — ici, les exécutions où ni le détecteur ni la forêt ne réagissent avant `H`. Contrairement au cadre médical classique de l'analyse de survie, les deux processus sont observés conjointement sur chaque exécution. L'incertitude induite par les exécutions doublement inachevées relève de l'identification partielle (bornes de Manski) et se traite rigoureusement par imputation extrême.

---

## Bibliographie

Les principales références sont fournies ci-dessous. Les autres sont dans la bibliographie du manuscrit.

- Gama, Žliobaitė, Bifet, Pechenizkiy, Bouchachia (2014). [*A survey on concept drift adaptation*](https://doi.org/10.1145/2523813). ACM Computing Surveys 46(4). — L'entrée en matière sur le [concept drift](#concept-drift).
- Gomes, Bifet, Read et al. (2017). [*Adaptive random forests for evolving data stream classification*](https://doi.org/10.1007/s10994-017-5642-8). Machine Learning 106. — Le classifieur étudié, [ARF](#arf-adaptive-random-forest).
- Montiel, Halford, Mastelini et al. (2021). [*River: machine learning for streaming data in Python*](https://jmlr.org/papers/v22/20-1380.html). JMLR 22. — La bibliothèque utilisée.
- Bifet, Gavaldà (2007). [*Learning from time-changing data with adaptive windowing*](https://doi.org/10.1137/1.9781611972771.42). SIAM SDM. — Le détecteur interne, [ADWIN](#adwin).
- Page (1954). [*Continuous inspection schemes*](https://doi.org/10.1093/biomet/41.1-2.100). Biometrika 41. — L'origine de [CUSUM](#cusum--page-hinkley).

Compléments selon le versant que vous prenez :

- Moreno-Torres, Raeder, Alaiz-Rodríguez, Chawla, Herrera (2012). [*A unifying view on dataset shift in classification*](https://doi.org/10.1016/j.patcog.2011.06.019). Pattern Recognition 45(1), 521–530. — La référence sur le [data drift](#data-drift) et sa taxonomie.
- Suárez-Cetrulo, Cervantes, Quintana (2025). [*ProteuS: A Generative Approach for Simulating Concept Drift in Financial Markets*](https://arxiv.org/abs/2509.11844). arXiv:2509.11844. — Le générateur de flux financiers, [ProteuS](#proteus).
- Raab, Heusinger, Schleif (2020). [*Reactive soft prototype computing for concept drift streams*](https://doi.org/10.1016/j.neucom.2019.11.111). Neurocomputing 416, 340–351. — [KSWIN](#kswin).
- Lu, Liu, Dong, Gu, Gama, Zhang (2018). [*Learning under concept drift: A review*](https://doi.org/10.1109/TKDE.2018.2876857). IEEE TKDE 31(12). — Revue générale du [concept drift](#concept-drift), en complément de Gama et al.
- David, Nagaraja (2003). *Order Statistics*, 3e édition. Wiley. — [Statistiques d'ordre](#statistiques-dordre).

---

<div style="page-break-before: always; break-before: page;"></div>

## Annexe — Démarrage rapide

**1. Cloner le [dépôt](https://github.com/TheBlindSpot-ICDM2026/The-Blind-Spot-Paradox-Experiments/) et installer les dépendances.** Ne mettez pas River à jour : le comportement interne de l'[ARF](#arf-adaptive-random-forest) a changé entre versions, et les résultats publiés ne se reproduisent qu'en 0.23.0.

```bash
git clone https://github.com/TheBlindSpot-ICDM2026/The-Blind-Spot-Paradox-Experiments.git
cd The-Blind-Spot-Paradox-Experiments
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt      # ou la commande indiquée dans le README

# Environnement de référence — à vérifier avant toute exécution
python -c "import sys, river, numpy; print(sys.version); print(river.__version__, numpy.__version__)"
# attendu : Python 3.12.x · river 0.23.0 · numpy 1.26.x

export PYTHONHASHSEED=0   # indispensable : sans cela vos résultats ne sont pas reproductibles
```

**2. [Rejouer l'expérience `R2`](https://github.com/TheBlindSpot-ICDM2026/The-Blind-Spot-Paradox-Experiments/blob/main/run_experiment_R2.sh) telle quelle** et vérifier que vous retrouvez les résultats stockés. Si ce n'est pas le cas, arrêtez-vous là et signalez-le : rien de ce qui suit n'aura de sens.

```bash
bash run_experiment_R2.sh
ls -l results/R2_instrumented_blind_spot/

# Les tests de non-régression comparent vos ré-exécutions aux valeurs publiées
pytest -q tests/
```

**3. Copier le script de R2 et en faire sortir les trajectoires.** Le script est [`exp_R2_instrumented_blind_spot.py`](https://github.com/TheBlindSpot-ICDM2026/The-Blind-Spot-Paradox-Experiments/blob/main/experiments/R2_instrumented_blind_spot/exp_R2_instrumented_blind_spot.py).

```bash
cp experiments/R2_instrumented_blind_spot/exp_R2_instrumented_blind_spot.py \
   experiments/R2_instrumented_blind_spot/exp_S1_traces.py
```

**Lisez le script avant de coder.** L'appel à `predict_one()` est **déjà** dans la boucle, et l'erreur de l'ensemble y est calculée à chaque pas pour alimenter le détecteur externe. Il y a quatre modifications à réaliser dans cet ordre :

1. **Retirer le `break`.** La boucle s'interrompt aujourd'hui dès que `τ_ARF` et `τ_det` sont connus. Remplacez cette condition par une borne explicite : `for t in range(T_DRIFT + H)` avec `H = 2000`. Sans cela, aucune trajectoire n'existe.
2. **Enregistrer l'erreur.** Accumulez `error` dans une liste, et écrivez-la. C'est le fichier dont tout le reste découle.
3. **Enregistrer l'état interne du détecteur** (`ext_pht.S`) au même pas de temps. Cette trajectoire ne vous servira qu'une fois, comme témoin de contrôle (étape 4 ci-dessous) : vous recalculerez `S_t` hors ligne pour tous les seuils.
4. **Enregistrer les remplacements arbre par arbre.** Le script détecte `τ_ARF` en comparant le **total** des remplacements avant et après `learn_one()`. C'est correct pour `τ_ARF`, mais insuffisant pour `τ_swap(q)` : il vous faut différencier le dictionnaire **clé par clé** (voir l'encadré sur le piège d'API ci-dessous), et écrire une ligne par remplacement — pas le dictionnaire entier à chaque pas.

*Optionnel, mais utile si vous voulez explorer l'effet du flux commun sur la [question B](#41-versant-théorique--une-course-entre-deux-horloges-aléatoires) : le script attribue actuellement **la même graine** au générateur du flux et à la forêt, ce qui interdit de faire varier l'un en gelant l'autre. Scinder ce paramètre en deux prend trois lignes.*

**4. Vérifier votre recalcul hors ligne.** Reconstruisez `S_t` depuis la seule trajectoire d'erreur, en repartant de `S = 0` au pas de rupture et en appliquant `S = max(0, S + (e_t − p̂_0) − δ_P)`. Avec le **même** `p̂_0` que celui du run, la courbe recalculée doit coïncider exactement, pas à pas, avec celle que vous avez enregistrée. Si elle ne coïncide pas, c'est votre recalcul qui est faux, et tout ce qui suit le serait aussi. Ce contrôle prend cinq minutes et vous évite de découvrir le problème en semaine 2.

**5. Lancer la campagne. Gardez la grille de `R2` : 20 amplitudes, 100 graines.** C'est celle sur laquelle les courbes que vous venez de reproduire ont été tracées, donc la seule qui rende vos résultats directement comparables. Vous pouvez monter à 200 graines — cela réduit d'un tiers l'incertitude sur vos moyennes inter-graines, et c'est d'autant plus accessible que vous n'avez qu'**une seule** campagne à lancer. Ne changez ni la plage d'amplitudes ni le paramétrage temporel.

> **UNE SEULE CAMPAGNE SUFFIT. C'est l'information la plus utile de cette annexe.**
>
> Le script d'origine lance trois campagnes, une par seuil `λ`. C'est du gaspillage : `λ` n'intervient **nulle part** dans la dynamique. Le détecteur externe ne fait que lire l'erreur, il n'agit jamais sur la forêt, et `λ` ne sert qu'à comparer `S_t` à un nombre. Les trois scénarios partagent la même graine, le même flux, la même forêt (`c_int = 1` dans les trois) : une fois le `break` retiré, ils produisent **exactement les mêmes exécutions**, au bit près.
>
> Votre campagne, donc : **20 amplitudes × 100 graines = 2 000 exécutions**, chacune de `4 000 + 2 000 = 6 000` pas. Vous balaierez ensuite `λ ∈ {8, 25, 50}` — et n'importe quelle autre valeur, et n'importe quel `δ_P` — sur les trajectoires enregistrées, en quelques secondes.
>
> Quatre règles :
> 1. **Bornez l'horizon post-drift, ne touchez jamais au pré-drift.** La borne `T_DRIFT + 2000` ramène chaque exécution à 6 000 pas et vous garantit une trajectoire complète sur toute la grille. **Ne réduisez pas les 4 000 pas de rodage** : ils déterminent la maturité de la forêt et l'estimation du socle. Les diminuer change `τ_ARF` et rend vos résultats incomparables à ceux de l'article. Conséquence à accepter : le rodage représente les deux tiers du coût d'une exécution, et il est incompressible.
> 2. **Prototypez sur sous-grille.** Validez toute votre chaîne d'analyse sur 5 amplitudes × 20 graines, soit 100 runs, avant de lancer la campagne complète. Chronométrez ce lot : multiplié par vingt, il vous donne le temps total à prévoir. Rappel : **à 20 graines, on ne conclut pas.**
> 3. **Parallélisez sur les graines.** Le script le fait déjà via `joblib`. Vérifiez seulement que vos modifications n'ont pas cassé le déterminisme : relancez deux fois le même lot et comparez les fichiers produits octet par octet.
> 4. **Écrivez petit.** La trajectoire d'erreur représente `2 000 × 2 000 = 4 millions` de lignes. Stockez l'erreur en entier 8 bits et le pas de temps en entier 16 bits, au format Parquet ; les remplacements vont dans une table d'événements séparée, une ligne par remplacement. En flottants 64 bits, avec le dictionnaire complet écrit à chaque pas, le même contenu occuperait plusieurs gigaoctets pour rien.

> **ATTENTION AU PIÈGE D'API (`ARFClassifier._drift_tracker`) :** Cet attribut interne est un dictionnaire cumulatif `{id_arbre: total_remplacements}` (un **stock**), et non un flux d'événements. Ne faites jamais `cumul += sum(_drift_tracker.values())` dans votre boucle temporelle, sous peine d'intégrer le passé à chaque pas :
> - Pour **`τ_ARF`** : détectez simplement le premier pas où `any(v > 0 for v in _drift_tracker.values())`.
> - Pour **`τ_swap(q)`** : comptez la fraction d'arbres **distincts** renouvelés : `sum(1 for v in _drift_tracker.values() if v > 0) / n_models`. Si le même arbre est remplacé trois fois de suite, il ne compte que pour un seul arbre renouvelé dans la forêt.