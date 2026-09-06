# Usage de LLM — déclaration

Conformément à la consigne de la filière (*"Toute utilisation de LLM doit être signalée et la liste des prompts fournie"*, `01_consignes/Consignes_études_de_cas_2026-2027.pdf`).

**Outil :** Claude Code (Anthropic), modèle Claude Sonnet 5, en session interactive dans l'éditeur. Les commits git portent la mention `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`, visible dans l'historique du dépôt.

**Périmètre :** Questions C et D (versant expérimental) du Sujet 39, portées par Salomé Fonvielle au sein du groupe.

## Résumé de la collaboration

L'outil a été utilisé en mode guidage : dès le deuxième échange, la consigne donnée à l'assistant a été explicite — construire ensemble, pas à pas, plutôt que produire une solution clé en main. Le travail s'est déroulé en cinq temps, sur trois jours (4-6 septembre 2026).

**1. Cadrage du sujet et audit critique du dépôt officiel.** Lecture du sujet, puis exploration du dépôt d'expériences de l'article source. L'assistant a identifié qu'une partie du dépôt (`docs/`, `results/R01-R18`) appartenait en réalité à un autre article que celui visé par le sujet — une confusion écartée avant de s'appuyer dessus à tort, et confirmée a posteriori par un commit des auteurs eux-mêmes ("contamination" retirée du dépôt officiel).

**2. Mise en place et fiabilisation de l'environnement.** Installation de Python/River 0.23.0 à l'identique de la référence, avec deux correctifs documentés et journalisés (`MODIFICATIONS_GROUPE.md`) : une dépendance manquante dans le `requirements.txt` officiel (`typing_extensions`), et un compilateur Rust nécessaire à la compilation de River. Chaque correctif a été vérifié indépendamment (clone `git` séparé) pour s'assurer qu'il ne s'agissait pas d'un problème local. Reproduction réussie des expériences R1 et R2 du dépôt officiel.

**3. Construction du protocole de réponse aux Questions C et D.** Discussion approfondie, question par question, pour bâtir une compréhension solide du mécanisme étudié (course entre l'auto-réparation de la forêt et le détecteur externe) avant d'écrire du code — l'assistant a été sollicité à plusieurs reprises pour reformuler plus simplement des notions mal comprises (mécanisme de remplacement d'arbre, définition de τARF, rôle des statistiques d'ordre). Un premier protocole a été bâti collectivement, puis entièrement revu après réception des consignes détaillées de l'encadrant.

**4. Intégration des consignes détaillées de l'encadrant.** Relecture du document complet transmis par M. Minato, correction du protocole en conséquence (définitions précises des 4 indicateurs à mesurer, méthode de corrélation à utiliser), et vérification critique d'une affirmation du document contredite par le code réel du dépôt (signalée pour clarification).

**5. Implémentation, débogage et exécution.** Écriture assistée du script d'instrumentation, exécution d'un premier essai révélant une erreur de mesure (des arbres remplacés avant même le drift, à cause du bruit), correction, validation sur un petit échantillon, puis lancement de la campagne de mesure complète (4200 simulations).

Tout au long de l'échange, l'assistant a été repris à plusieurs reprises pour simplifier ses explications, vérifier ses affirmations avant de les présenter comme acquises, et respecter le périmètre de travail de l'utilisatrice (Questions C/D uniquement, pas A/B).

*Résumé reconstruit par Claude à partir du journal de la session — fidèle sur le fond ; la formulation exacte de quelques échanges courts peut différer à la marge du texte original.*
