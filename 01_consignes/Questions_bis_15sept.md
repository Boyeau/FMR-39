# Questions complémentaires de l'encadrant — mail du 15 septembre 2026

> Reçu le 15 septembre 2026 ; seule pièce jointe reçue, les énoncés complets annoncés
> n'ont pas été transmis. Le fichier reçu (`Email_Questions_C1bis_C2bis_C3bis_D1bis_D3bis.html`)
> est le corps du mail rendu en HTML.
>
> Texte reproduit tel quel. Seule modification : les formules, rendues trois fois par
> l'export KaTeX du client de messagerie (`SmaxS_{max}Smax`), sont réduites à une notation
> lisible (`S_max`). Aucune reformulation.

**Objet :** Suite à notre point de cet après-midi — pistes de réflexion et questions optionnelles

---

Bonjour à tous,

Suite à nos échanges de cet après-midi et après avoir pris un peu de recul sur les résultats
obtenus et sur nos discussions, j'ai rédigé quelques questions optionnelles supplémentaires
pour guider la fin de votre projet. Il n'y a pas d'obligation de traiter ces questions dans le
temps qu'il vous reste avant votre présentation. Nous pourrons en discuter en séance mercredi
et vous pourrez les utiliser pour la suite et fin de votre projet.

J'aimerais en revanche que vous m'envoyiez le draft actuel de votre rapport en l'état (ou les
brouillons si plusieurs documents, sans aucun travail supplémentaire de votre part : quel que
soit son avancement, la mise en page, les paragraphes incomplet, les fautes d'orthographe, les
erreurs à corriger etc.) car je n'ai pas pu voir tout ce que vous aviez fait aujourd'hui et que
ça me permettra d'être plus pertinent pour voir si les guides de l'énoncé ont été utiles et pour
suivre votre présentation mercredi. C'est à titre purement indicatif et vous ne serez absolument
pas évalués dessus.

En réfléchissant un peu plus en profondeur à la "métrique de référence" pour évaluer
l'adaptation de la forêt : si la métrique `S_max` réplique la statistique du détecteur (avec sa
tolérance `δ_P` et son blocage à zéro), c'est l'aire d'erreur `A` qui est la métrique de
référence pour évaluer l'adaptation du classifieur indépendamment du détecteur. C'est d'ailleurs
pour ça que dans l'énoncé je vous demande de l'étudier sous deux formes :

- `A(H)` (questions C.2 et C.3) sur l'horizon complet de 2 000 pas, qui devrait montrer les
  limites d'une accumulation prolongée en noyant les marques de l'adaptation dans le bruit
  statistique post-guérison ;

- `A(0, w)` (introduite en C.2 et reprise en D) sur la fenêtre courte, qui isole parfaitement la
  quantité d'erreur brute que le classifieur laisse fuiter coupant l'intégration exactement à la
  fin du transitoire (guérison complète de la forêt).

Voici en tout cas les questions que je considère prioritaires :

## 1. Le profil d'évolution de l'erreur (Priorité 1 et 2)

Nous nous sommes posés la question du profil d'évolution de l'erreur après la rupture. Ce qui est
intéressant c'est que cela doit pouvoir permettre de faire le pont avec la fenêtre transitoire
moyenne de l'article (`E[τ_ARF] ≈ 18,5 · Δe^−0,98` des questions C.2 et C.3), j'ai rédigé pour
cela deux questions :

La question **C.3.bis** est la priorité 1. Si vous n'avez le temps d'en traiter qu'une seule
d'ici la fin du projet, faites celle-ci (si ce n'est pas déjà fait).

La question **C.2.bis** est à traiter juste avant si vous en avez le temps (priorité 2). Elle
pose le cadre théorique de l'optimisation qui éclaircit la C.3.bis.

## 2. La matrice de corrélation et le paradoxe de Simpson (Priorité 3)

Comme discuté, j'ai ajouté une question **D.3.bis** qui demande de construire la matrice de
corrélation complète de toutes vos métriques, en version globale et ensuite détaillée par
amplitude du drift. Ce petit exercice permet au passage de visualiser pourquoi empiler toutes les
amplitudes détruit l'information (paradoxe de Simpson) et de valider définitivement la métrique
d'aire pure `A(0,w)`. C'est la suite logique de la question C.3.bis.

## 3. L'évolution interne de la forêt (Priorité 4)

L'idée que vous avez émise de regarder la variance des erreurs en coupe transversale (entre les
arbres) est une excellente idée pour comprendre ce qui se passe vraiment à l'intérieur de la forêt
après un drift. J'ai rédigé pour cela une question **D.1.bis**. Elle est surtout utile pour votre
compréhension de l'effet Hydre, bien que ce ne soit pas la métrique la plus critique à produire
(priorité 4).

## 4. Le Z-score de la baisse d'erreur (Priorité 5 — 100 % optionnel)

Concernant mon idée de calculer un Z-score sur la baisse du niveau d'erreur : si l'intuition
visuelle sur des trajectoires individuelles semblait séduisante, le bruit la rend en fait
mathématiquement inapplicable. Si on veut faire le calcul, il doit être impérativement moyenné sur
les graines. C'est ce que j'ai détaillé dans la question **C.1.bis**. Je la place en priorité 5
car, en réalité, elle recoupe largement le `τ_swap` sur un quantile élevé (question C.1) et la fin
de la fenêtre d'accumulation optimale (question C.2.bis). Ne la traitez qu'en tout dernier si vous
le souhaitez.

Vous trouverez les énoncés complets de ces questions en pièce jointe.

Bon courage pour la fin de votre projet.
