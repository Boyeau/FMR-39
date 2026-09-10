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
parties 1 et 2 ci-dessous) ; Alexandre Boyer sur les questions A et B (versant théorique)
et sur la traduction en anglais des rédactions — **partie 3 à rédiger par lui**, cette
déclaration étant incomplète tant qu'elle manque.

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

## Partie 4 — audit de C.1 / C.2 et révision de C.3 à D.4 (Ulysse Petit-Tichanné, 10 septembre)

Modèle : Claude Fable 5.1 (Claude Code). Session en deux prompts, le reste étant produit
par l'assistant sous le contrôle du plan.

**Prompts, tels que saisis :**

1. `/prime` : commande locale de début de session, qui charge le contexte du projet
   (feuille de route, journal, historique git, état du dépôt officiel) via trois
   sub-agents et rend un briefing de moins de 200 mots.
2. `/execute .claude/plans/audit-qc12-revision-qc3-qd4.md` : exécuter un plan écrit la
   veille au soir (lui-même issu de `/plan-task` et de deux passes de critique adverse,
   qui avaient produit 7 objections bloquantes et 24 mineures, toutes intégrées avant
   exécution). Le plan fixe onze tâches, les critères de succès, les tables à lire, les
   chiffres à ne surtout pas citer, et les impasses à ne pas rouvrir.

**Ce que l'assistant a fait sous ce plan, dans l'ordre :**

**1. Rejeu de chaque constat avant écriture.** Le plan portait des constats d'audit sur
les rédactions de C.1 et C.2 (écrites par Alexandre et Salomé) et sur les cinq rédactions
d'Ulysse. Consigne : un constat qui ne se reproduit pas par script est retiré, pas ajusté.
Deux scripts ont été écrits, l'un qui produit la seule table manquante (l'erreur de fin
d'horizon par amplitude et par fenêtre), l'autre en lecture seule qui imprime, pour chaque
constat, la ligne du `.tex`, la valeur écrite, la valeur mesurée et la table source. Tous
les constats se sont reproduits.

**2. Note d'audit pour les coéquipiers, sans toucher à leurs fichiers.** Les constats sur
C.1 et C.2 sont consignés dans une note en français, écrite pour être exécutée par
l'assistant IA d'Alexandre : chaque item porte le chemin, la ligne, le texte exact à
remplacer, la proposition et la commande de vérification, et distingue « à corriger » de
« solide, à ne pas toucher ». Les fichiers de C.1 et C.2 et leurs figures n'ont pas été
modifiés.

**3. Révision des cinq rédactions d'Ulysse.** Sept chiffres corrigés, chacun remplacé par
la valeur d'une table ; deux tables et neuf figures ajoutées, lisibles en noir et blanc ;
notation et acronymes définis à la première occurrence dans chaque fichier. Un estimateur
nouveau (l'intervalle bootstrap d'une médiane) a passé trois témoins sur cas connu avant
d'être appliqué, et sa reproduction bit à bit a été vérifiée sur deux exécutions.

**4. Cohérence et traçabilité.** Les sept `.tex` compilés sans artefact périmé ; un
contrôle de traçabilité versionné (`verif_chiffres_tex.py`) rejoue les deux scripts de
chiffres et vérifie que chaque littéral numérique des cinq rédactions révisées se retrouve
dans leur sortie ou dans une table : 453 contrôlés, aucun introuvable. Une première version
de ce contrôle tournait depuis un script jetable, hors dépôt ; la critique adverse l'a
relevé, et c'est en le versionnant qu'un chiffre manquant est apparu. Le journal de recherche, le README et la
feuille de route ont été resynchronisés, avec une section nouvelle sur le piège rencontré :
un chiffre hérité du journal sans amplitude ni fenêtre, que le premier audit avait
« corrigé » par un autre chiffre sans fenêtre, et que seule la reproduction a arrêté.

**5. Double critique adverse.** Deux sub-agents en contexte vierge ont reçu mission de
réfuter, l'un la fidélité au plan et la correction du code, l'autre la plausibilité des
résultats contre les acquis du journal. Ils ont produit deux objections bloquantes, cinq
majeures et une quinzaine de mineures, toutes traitées ; les deux bloquantes ont été
trouvées indépendamment par les deux critiques. Le détail et les corrections sont au § 11.7
du journal de recherche. Les deux plus instructives : un contrôle annoncé dans un livrable
alors qu'il n'existait que dans un script de session, et une phrase fausse produite en
confondant deux définitions d'un même instant — le piège que la session avait précisément
pour objet de refermer.

Comme les jours précédents, l'assistant a servi autant à réfuter qu'à produire.
