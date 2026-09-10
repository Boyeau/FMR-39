# Usage de LLM — déclaration

Conformément à la consigne de la filière (*"Toute utilisation de LLM doit être signalée et la liste des prompts fournie"*, `01_consignes/Consignes_études_de_cas_2026-2027.pdf`).

**Outil :** Claude Code (Anthropic), en session interactive dans l'éditeur. Deux modèles ont été utilisés selon les sessions, dans trois déclinaisons, et les commits en portent la trace :

| Modèle | Commits | Auteur | Dates |
|---|---|---|---|
| Claude Sonnet 5 | 7 | Salomé Fonvielle | 4 et 6 septembre |
| Claude Sonnet 5 | 3 | Alexandre Boyer | 7 septembre |
| Claude Opus 5 | 3 | Salomé Fonvielle | 7 et 8 septembre |
| Claude Opus 5 (1M context) | 10 | Ulysse Petit-Tichanné | 7 et 8 septembre |

Soit 23 des 47 commits de l’historique. Le décompte se recalcule par croisement de
`%an` et du `Co-Authored-By:` de chaque corps de commit.

**Périmètre :** trois des quatre membres ont utilisé l'outil, sur trois versants du sujet.
Salomé Fonvielle et Ulysse Petit-Tichanné sur les questions C et D (versant expérimental,
parties 1 à 3 ci-dessous) ; Alexandre Boyer sur les questions A et B (versant théorique),
sur la bibliographie et sur la mise en anglais des rédactions (partie 4).

## Partie 1 — prototype et cadrage (Salomé Fonvielle, 4–6 septembre)

L'outil a été utilisé en mode guidage : dès le deuxième échange, la consigne donnée à l'assistant a été explicite — construire ensemble, pas à pas, plutôt que produire une solution clé en main. Le travail s'est déroulé en cinq temps, sur trois jours (4-6 septembre 2026).

**1. Cadrage du sujet et audit critique du dépôt officiel.** Lecture du sujet, puis exploration du dépôt d'expériences de l'article source. L'assistant a identifié qu'une partie du dépôt (`docs/`, `results/R01-R18`) appartenait en réalité à un autre article que celui visé par le sujet — une confusion écartée avant de s'appuyer dessus à tort, et confirmée a posteriori par un commit des auteurs eux-mêmes ("contamination" retirée du dépôt officiel).

**2. Mise en place et fiabilisation de l'environnement.** Installation de Python/River 0.23.0 à l'identique de la référence, avec deux correctifs documentés et journalisés (`MODIFICATIONS_GROUPE.md`) : une dépendance manquante dans le `requirements.txt` officiel (`typing_extensions`), et un compilateur Rust nécessaire à la compilation de River. Chaque correctif a été vérifié indépendamment (clone `git` séparé) pour s'assurer qu'il ne s'agissait pas d'un problème local. Reproduction réussie des expériences R1 et R2 du dépôt officiel.

**3. Construction du protocole de réponse aux Questions C et D.** Discussion approfondie, question par question, pour bâtir une compréhension solide du mécanisme étudié (course entre l'auto-réparation de la forêt et le détecteur externe) avant d'écrire du code — l'assistant a été sollicité à plusieurs reprises pour reformuler plus simplement des notions mal comprises (mécanisme de remplacement d'arbre, définition de τARF, rôle des statistiques d'ordre). Un premier protocole a été bâti collectivement, puis entièrement revu après réception des consignes détaillées de l'encadrant.

**4. Intégration des consignes détaillées de l'encadrant.** Relecture du document complet transmis par M. Minato, correction du protocole en conséquence (définitions précises des 4 indicateurs à mesurer, méthode de corrélation à utiliser), et vérification critique d'une affirmation du document contredite par le code réel du dépôt (signalée pour clarification).

**5. Implémentation, débogage et exécution.** Écriture assistée du script d'instrumentation, exécution d'un premier essai révélant une erreur de mesure (des arbres remplacés avant même le drift, à cause du bruit), correction, validation sur un petit échantillon, puis lancement de la campagne de mesure complète (4200 simulations).

Tout au long de l'échange, l'assistant a été repris à plusieurs reprises pour simplifier ses explications, vérifier ses affirmations avant de les présenter comme acquises, et respecter le périmètre de travail de l'utilisatrice (Questions C/D uniquement, pas A/B).

*Résumé reconstruit par Claude à partir du journal de la session — fidèle sur le fond ; la formulation exacte de quelques échanges courts peut différer à la marge du texte original.*

---

## Partie 2 — campagne unique et rédactions (Ulysse Petit-Tichanné, 7–8 septembre)

*Section à compléter par Ulysse avec le détail des échanges. Ce qui suit est établi à
partir de l'historique du dépôt seul, et ne remplace pas la liste des prompts.*

Le travail de cette période, lisible dans les commits `56a48c5` à `c948a5e`, a porté sur
quatre points.

**1. Refonte du dispositif de campagne.** Constat que `lambda` n'agit pas sur la dynamique
— le détecteur lit la trajectoire d'erreur sans jamais agir sur la forêt — donc qu'une
campagne unique remplace les trois scénarios du dépôt officiel, les seuils se balayant hors
ligne (`75eba29`). La simulation n'écrit plus que la matière première ; tout le dérivé se
recalcule depuis les Parquet.

**2. Rédaction de la question C.3** (invariance du budget de preuve) et du journal de
recherche des questions C et D.

**3. Protocole de validation de la métrique, et disqualification de `τ_ARF`** par deux voies
indépendantes — le test à drift nul et la sensibilité à la taille de la forêt (`bbc4b9f`).

**4. Critères du banc de candidats figés et commités avant toute mesure** (`c948a5e`), pour
qu'ils soient datables d'avant les chiffres. Ce commit acte aussi la correction de trois
affirmations antérieures qui s'étaient révélées fausses à la vérification.

L'assistant a été employé en vérification adverse autant qu'en production : plusieurs de ses
propres conclusions ont été infirmées par des contrôles ultérieurs et corrigées dans
l'historique plutôt que retirées silencieusement.

## Partie 3 — rédactions de la question D (Ulysse Petit-Tichanné, 9 septembre)

Session conduite à partir d'un plan écrit et audité avant exécution
(`redactions-latex-question-D.md`, local), puis soumise à deux relectures adverses en
contexte vierge. Quatre points.

**1. Résolution d'un conflit de fusion sur les données plutôt que sur l'ancienneté.** La
fusion d'`origin/main` a opposé deux versions de la question C.1 : l'une annonçant deux
violations de la conjecture, toutes deux situées là où le test n'a pas de puissance,
l'autre quatre violations dont deux à des amplitudes interprétables. L'assistant a été
chargé de trancher en interrogeant la table `QCD_tau_err_full` plutôt qu'en arbitrant entre
les auteurs : les données donnent quatre violations, dont deux qui ne tombent que par la
condition de persistance. Le texte corrigé a été conservé et les deux figures de la version
concurrente réintégrées avec des légendes rectifiées, de sorte qu'aucun travail ne soit
perdu.

**2. Production des dérivés manquants, sans relancer la campagne.** Trois grandeurs exigées
par l'énoncé n'existaient dans aucune table : la fraction d'arbres remplacés avec sa
médiane et son écart interquartile, le socle estimé sur deux fenêtres (1 000 et 3 000 pas
avant la rupture), et la colonne consignant la taille de la forêt. Toutes trois ont été
recalculées hors ligne depuis les Parquet existants. Le contrôle exigé avant usage — le
socle recalculé à 3 000 pas doit reproduire celui de la campagne — passe à un écart
exactement nul.

**3. Correction de chiffres faux publiés dans des fichiers versionnés.** L'assistant a
vérifié un par un les chiffres que les rédactions allaient citer, contre les tables. Deux
valeurs annoncées dans le journal de recherche et dans un `README` depuis la veille se sont
révélées non reproductibles, ainsi qu'une formulation trop forte dans la feuille de route.
Les trois sont corrigées, avec la trace de ce qu'elles disaient. Une tautologie
algébrique — un coefficient valant exactement 1 parce qu'il compare une grandeur à
elle-même — a été repérée avant publication et marquée comme telle dans la table et sur la
figure, plutôt que présentée comme une association mesurée.

**4. Révision du résultat central de la question.** Le journal affirmait que l'indicateur
étudié ne porte aucune information sur la quantité de preuve offerte au détecteur. La
vérification montre que l'affirmation est exacte pour l'une des deux grandeurs candidates
et fausse pour l'autre — précisément celle qui décide de l'alarme. La réponse a été
réécrite en deux temps, avec le sens du biais résiduel qui la renforce.

Comme dans la partie 2, l'assistant a servi autant à réfuter qu'à produire : les deux
relectures adverses de fin de session portaient sur son propre travail.

---

## Partie 4 — bibliographie, questions A et B, mise en anglais (Alexandre Boyer, 3–10 septembre)

Sessions interactives en continu, d'abord avec Claude Sonnet 5 puis avec Claude Opus 5 à
partir du 10 septembre. Le mode de travail a été constant : l'assistant produit, puis doit
re-justifier ou recalculer avant que ce soit accepté. Plusieurs corrections du dépôt
viennent de cette insistance plutôt que d'une vérification spontanée de l'outil, et sont
signalées comme telles ci-dessous. Six points.

**1. Choix du sujet et bibliographie.** L'assistant a surtout servi ici à chercher et à
regrouper : identification des références citées par l'énoncé — y compris celles présentes
uniquement dans les hyperliens du PDF, invisibles dans le texte —, recherche des articles
correspondants, relevé des DOI et tenue de la table de suivi. Trois références absentes de
l'énoncé ont été identifiées et ajoutées en cours de lecture (Moreno-Torres et al. 2012,
Domingos & Hulten 2000, Aalen & Johansen 1978). La synthèse bibliographique a ensuite été
reprise plusieurs fois sur demande, d'un format Word vers un format IEEE à citations
numérotées, puis en LaTeX ; le choix du format, du niveau de détail et des références à
conserver ou écarter a été tranché par l'utilisateur à chaque étape — deux ouvrages
inaccessibles ont notamment été maintenus dans la table mais écartés de la synthèse.

**2. Environnement et reproduction.** Installation de l'environnement épinglé
(Python 3.12, River 0.23.0, `PYTHONHASHSEED=0`) et exécution de l'expérience R2 du dépôt
officiel, vérifiée sur les trois régimes de seuil publiés.

**3. Démonstrations des questions A et B.** C'est le cœur de la contribution. Pour A :
traitement de la double famine, choix et justification de l'inégalité stricte définissant
l'événement Miss, encadrement par identification partielle sous horizon fini, puis
encadrement universel de Fréchet vérifié sur un cas jouet. Pour B : indépendance
conditionnelle des arbres sachant le flux, inégalité de Jensen sur `x → x^M` pour
établir le sens du biais, condition d'égalité et son interprétation, requalification du
corollaire sur `M_crit` en certificat conservateur, et contre-exemple
anti-monotone montré structurellement impossible dans le modèle réel par la formule de
covariance totale.

Ces démonstrations ont été construites par allers-retours, avec pour consigne explicite de
ne rien accepter avant de pouvoir le redémontrer sans support. Ont notamment fait l'objet
de demandes de réexplication successives : le rôle des poids de Poisson dans ce qui
distingue deux arbres à flux fixé, la nature exacte de la variable aléatoire `G_S`, le sens
physique du cas d'égalité de Jensen, et la raison pour laquelle un contre-exemple à
covariance négative reste constructible alors que le modèle réel l'interdit.

Une erreur de signe produite par l'assistant sur la covariance du couplage anti-monotone a
été détectée par cette voie : sur demande de refaire le calcul depuis le début, la valeur
est passée de « strictement plus élevée » à `−1/4`, strictement plus basse, ce qui inverse
la lecture. La note de projet a été corrigée en conséquence, et le point signalé comme le
plus facile à confondre à l'oral.

**4. Mise en anglais et harmonisation.** Traduction en anglais des rédactions A, B, C.1,
C.3 et C.2, cette dernière étant au passage fusionnée en un fichier unique — les deux
parties de C.2 étant deux sections d'une même démonstration. Traduction également du texte
inscrit dans les figures générées par script (titres, axes, légendes), oublié au premier
passage et signalé comme tel.

**5. Compléments apportés aux rédactions expérimentales.** Trois figures ajoutées à C.1 (le
nuage `τ_ARF` contre `τ_swap(q)` run par run, la bande de bruit contre le seuil aux
amplitudes non interprétables, et le rapport signal sur bruit sur toute la grille), un
défaut de rendu corrigé dans une figure existante, et pour C.2 l'énoncé
explicite du certificat sous forme de corollaire, la distinction nécessaire/suffisant
demandée par l'énoncé, et une section confrontant le certificat aux mesures.

Quatre de ces compléments ne viennent pas de l'assistant mais de remarques de
l'utilisateur, qui n'avaient pas été relevées spontanément : que les quotas de 25 % et 75 %
ne tombent pas sur un nombre entier d'arbres avec `M = 10` (ils valent en réalité 3 et 8
arbres, soit 30 % et 80 %) ; qu'un segment détaché flottait dans une figure ; que la
section centrale de C.1 était la seule sans illustration ; et que la courbe d'aire mesurée
contredit visiblement l'invariance annoncée en bas de grille, ce qui a conduit à écrire
pourquoi l'amplitude la plus faible est écartée du calcul au lieu de l'omettre en silence.

**6. Vérification croisée par les coéquipiers.** Comme dans les parties 2 et 3, l'assistant
a servi autant à réfuter qu'à produire, et plusieurs de ses conclusions n'ont pas tenu :
des affirmations issues de ces sessions ont été infirmées par les relectures d'Ulysse et de
Salomé, aucune pour cause de calcul faux, toutes pour avoir généralisé depuis un contrôle
trop étroit. Elles sont corrigées dans l'historique du dépôt, avec la trace de ce qu'elles
disaient, plutôt que retirées silencieusement.

*Résumé reconstruit à partir du journal des sessions. À relire et amender par l'auteur
avant remise : la liste des prompts eux-mêmes n'y figure pas.*
