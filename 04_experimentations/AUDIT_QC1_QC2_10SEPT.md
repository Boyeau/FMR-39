# Audit de Q C.1 et Q C.2 : constats, sans modification

**Écrit le 10 septembre 2026 par Ulysse (piste socle / C·D).**
Destinataires : Alexandre (premier relecteur de C.1, traducteur et assembleur de C.2) et
Salomé (autrice initiale des deux). **Rien n'a été modifié** dans
`redaction_QC1_hierarchie.tex`, `redaction_QC2_certificat_deterministe.tex` ni dans les
quatre figures que QC1 cite. Cette note dit ce que j'ai trouvé, et laisse la correction à
celui qui a écrit le texte.

Cette note est écrite pour être **exécutée par un assistant IA** aussi bien que lue par
une personne : chaque item porte le chemin du fichier dans `repo/`, la ligne au 10
septembre, le texte exact à remplacer entre guillemets, une proposition de remplacement
(en français, à traduire), et la commande qui permet de vérifier. Les items « solide »
sont **à ne pas toucher** : ils sont listés pour que personne ne « corrige » ce qui est
juste.

**Comment rejouer chaque chiffre :**

```bash
cd repo/04_experimentations/resultats_R2/scripts
PYTHONHASHSEED=0 ../../../../.venv/bin/python chiffres_QC.py --sous QC1
PYTHONHASHSEED=0 ../../../../.venv/bin/python chiffres_QC.py --sous QC2
```

Chaque ligne de sortie est de la forme `[QCx l.N] ecrit = … | mesure = … | table = …`.
Tout ce qui suit en sort ; aucun chiffre ne vient de mémoire ni du `JOURNAL.md`.

Les comptes d'occurrences (`~:`, `---`, guillemets, symboles de notation) se vérifient par
les `grep` donnés item par item, pas par ce script.

---

## 1. `redaction_QC1_hierarchie.tex`

Fichier : `repo/04_experimentations/redaction_QC1_hierarchie.tex` (218 lignes, `\author{Salomé
Fonvielle}` ; les figures et la section 3 ont été retravaillées par Alexandre les 8 et 9
septembre, commits `503e831`, `dfa3a32`, `30336b1`, `7a5d74e`).

### Bloquant

Aucun. Le PDF compile sans référence indéfinie et **tous les chiffres empiriques sont
retrouvés à l'unité** dans les tables.

### Mineur (chiffres et périmètre)

**QC1-M1. Ligne 210, « nearly 1 800 » et « the order of 200 ».**
Texte : `the order of $200$ seeds at $\Delta e = 0.085$, but nearly $1\,800$ at`.
La formule que le texte lui-même invoque, `n·(2σ/ρΔe)²` avec n = 100, donne **1 874** à
`Δe = 0,0282` (σ = 0,015252, ρΔe = 0,007046) et **194** à `Δe = 0,0854`. Le chiffre est
hérité de `JOURNAL.md` § 7 (« de l'ordre de 1 800 »). Ordre de grandeur juste, valeur non
calculée.
Proposition : « de l'ordre de 190 graines à Δe = 0,085, mais près de 1 900 (1 874 par la
formule) à Δe = 0,028 ».
Vérification : `chiffres_QC.py --sous QC1`, bloc « l. 210 ».

**QC1-M2. Lignes 132 et 213, deux ensembles différents de « 18 amplitudes » sous le même
mot *interpretable*.**
Ligne 132 : `Across the 18 amplitudes where its median is interpretable` : ce sont les
amplitudes où la **censure** de `τ_swap(75 %)` est ≤ 50 %, donc tout sauf **0,085 et
0,141**.
Ligne 213 : `Across the 18 amplitudes where the test is interpretable` : ce sont les
amplitudes où le test a la **puissance** (`ρΔe > 2σ`, colonne `interpretable` de
`QCD_tau_err_full`), donc tout sauf **0,028 et 0,085**.
Les deux ensembles ont 18 éléments mais diffèrent sur {0,028 ; 0,141}. Un lecteur qui
retient « les 18 amplitudes interprétables » croit qu'il n'y en a qu'un.
Proposition : ligne 132, écrire « the 18 amplitudes where fewer than half of the runs are
censored for q = 75 % » ; ligne 213, écrire « the 18 amplitudes where the test has power
(ρΔe > 2σ) », et ne pas employer *interpretable* pour les deux.
Vérification : bloc « l. 132 et l. 213 ».

**QC1-M3. Ligne 50, « (also used in Q C.2/D) ».**
Texte : `consistency with the quotas fixed for the campaign (also used in Q~C.2/D), but should`.
Les quotas `τ_swap(q)` apparaissent **30 fois** dans QD1, QD3 et QD4 (25 avant la
révision du 10 septembre, qui en a ajouté cinq), et **zéro fois** dans QC2. La moitié
« D » est juste, la moitié « C.2 » est fausse.
Proposition : « (also used in Q D) ».
Vérification : `grep -c 'tau_{\\mathrm{swap}}' redaction_QC2_certificat_deterministe.tex` → 0.

**QC1-M4. Lignes 188-192, légende de `Fig_QC_tauerr_power_full` : deux estimateurs de
bruit sous un seul nom.**
Texte : `with its $\pm 2\sigma$ band` puis `($\rho\Delta e \le 2\sigma$). The noise band covers the threshold`.
La bande tracée par la figure est `2·√(ē_t(1−ē_t)/n)`, un écart-type **binomial par pas**
(en moyenne 0,0164 sur les 400 pas tracés à Δe = 0,028, 0,0239 à Δe = 0,085). Le critère
`interpretable` lit `sigma_courbe`, l'écart-type **empirique de queue** (500 derniers pas :
0,0153 et 0,0149). La légende les assimile. Sans conséquence sur le verdict (la réserve
est déjà au point 5 de l'`AVERTISSEMENT_RESULTATS_9SEPT.md`), mais si la figure part au
rapport, dire lequel des deux est tracé.
Proposition : « with a ±2σ band where σ is the binomial standard error √(ē_t(1−ē_t)/n) at
each step ; the interpretability criterion uses instead the empirical tail standard
deviation of the mean curve (0.0153 and 0.0149), of the same order ».
Vérification : bloc « l. 188-192 ».

**QC1-M5. Notation : `τ_err(ρ)` et `τ*` sans définition ni lien avec `τ_rec`.**
Texte, ligne 28 : `$N_t$ be the number of distinct trees replaced at time $t$ since the drift`
suivi ligne 28-29 de `$\tau^*$, and`. Texte, ligne 140 :
`$\tau_{\mathrm{err}}(\rho)$ is therefore computed only on the mean curve`.
`τ_err` apparaît 4 fois, `τ*` 3 fois (lignes 28, 30). Aucune des deux n'est dans la liste
de notation du projet (`τ_ARF, τ_det, τ_rec, τ_i, τ_50%, Δe, M, λ`). QD1 (ligne 66 au
9 septembre) écrit : « Q C.1 writes it τ_err(ρ), and the two names denote the same object
throughout ». QC3 révisé fait de même. **Je ne modifie pas QC1** : c'est votre fichier. Mais
tant que QC1 n'écrit pas ce lien une fois, l'incohérence entre QC1 (`τ_err`) et QC3/QD1
(`τ_rec`) existe, et elle est déclarée comme telle au § 11 du `JOURNAL.md`.
Proposition : à la première occurrence (section 3), « τ_err(ρ), which the other sections
write τ_rec » ; et à la ligne 28, « the drift instant τ* ».
Vérification : `grep -c 'tau_{\\mathrm{err}}' redaction_QC1_hierarchie.tex` → 4 ;
`grep -c 'tau\^\*' redaction_QC1_hierarchie.tex` → 3 ;
`grep -c 'tau_{\\mathrm{rec}}' redaction_QC1_hierarchie.tex` → 0.

### Mineur (forme, à trancher par vous)

**QC1-F1.** Fichiers : `repo/04_experimentations/resultats_R2/resultats/figures/Fig_QC_ecarts_full.png`,
`Fig_QC_tauerr_signal_bruit_full.png`, `Fig_QC_dispersion_swap_full.png`, produites par
`resultats_R2/scripts/analyse_QCD.py` (fonctions `figure_ecarts`, `figure_signal_bruit`,
`figure_dispersion_swap`). `Fig_QC_ecarts_full.png` : quatre courbes distinguées par la **couleur seule**.
Illisible en noir et blanc, ce que `redaction.md` exige. `Fig_QC_tauerr_signal_bruit_full`,
même remarque. `Fig_QC_dispersion_swap_full` : axes sans unité (steps). Des em-dashes
(`—`) et des `---` littéraux figurent dans des labels. Ces figures sortent
d'`analyse_QCD.py` (mon script) : **je ne les ai pas régénérées**, cela changerait le rendu
de votre texte sans votre accord. Si vous voulez que je le fasse, dites-le : c'est une
fonction chacune, marqueurs + styles de trait distincts.
Vérification : ouvrir les trois PNG, ou
`grep -n "color=" resultats_R2/scripts/analyse_QCD.py` dans les fonctions citées, qui
montre que la distinction repose sur `color` sans `ls` ni `marker` différenciés.
⚠️ Ne PAS relancer `analyse_QCD.py --tag full` pour les régénérer sans décision explicite :
cela réécrit les onze figures d'un coup, dont celles que QC1 cite.

**QC1-F2.** Recomptés le 10 septembre : **20** occurrences de `~:`, **2** de `~;` et
**10** de `---` hors titre, dans le texte anglais. Le grep de `redaction.md` les cible.
Remplacement : `~:` par `:`, `~;` par `;`, et `---` par une ponctuation sans em-dash (une
virgule ou un point-virgule selon la phrase ; c'est ce qui a été fait dans les cinq
rédactions révisées).
Commandes :
```bash
grep -c '~:' redaction_QC1_hierarchie.tex                                   # 20
grep -c '~;' redaction_QC1_hierarchie.tex                                   #  2
grep -n -- '---' redaction_QC1_hierarchie.tex | grep -vc '\\title'          # 10
```

### Solide, à ne pas toucher

- Ligne 55-57 : `τ_ARF = τ_swap(10 %)` sur 2 000/2 000 runs ; **0 violation** sur les
  **5 795** comparaisons non censurées (1 999 + 1 978 + 1 818). Retrouvé exactement.
  ⚠️ Le `JOURNAL.md` § 1 dit « 6 000 » : c'est le journal qui a tort (3 × 2 000 avant
  censure), pas le texte. Je corrige le journal (voir § 3 ci-dessous).
- Ligne 132-133 : écart médian `τ_swap(75 %) − τ_ARF` de **167 à 1 368** pas, soit **6,0 à
  14,3** fois `τ_ARF`, sur les 18 amplitudes à censure ≤ 50 %. Retrouvé exactement, par la
  médiane des écarts par run.
- Ligne 134 : le maximum apparent à Δe = 0,141 est 1 392,5 (arrondi 1 393), censure 54 %.
- Section 3 : 4 violations sans persistance à 0,028 / 0,085 / 0,141 / 0,194 ; les deux
  interprétables franchissent au pas **101** (τ_ARF médian 263 et 143) et passent à **626**
  et **322** avec 20 pas de persistance ; **0 violation** avec persistance ; σ de 0,0154 à
  0,0047. Tout retrouvé à l'unité.
- Ligne 43-52, quotas atteignables (3 arbres pour 25 %, 8 pour 75 %) : juste, et QD3 le
  reprend avec la même convention.

---

## 2. `redaction_QC2_certificat_deterministe.tex`

Fichier : `repo/04_experimentations/redaction_QC2_certificat_deterministe.tex` (281 lignes,
`\author{Salomé Fonvielle}`, fusion et traduction par Alexandre le 8, section empirique par
Alexandre le 9 (`87dd262`), deux corrections de Salomé le 9 (`fa720b2`)).

### Bloquant (le PDF est faux ou incomplet)

**QC2-B1. Ligne 241, `\eqref{eq:certificate}` référence un label qui n'existe pas.**
Texte : `satisfies~\eqref{eq:certificate} », equivalently $S_{\max}(w) \ge \lambda$, gives a very`.
Les seuls labels d'équation du fichier sont `eq:cusum` (l. 39) et `eq:lindley` (l. 116). Au
PDF cela rend « (??) », et `latexmk` signale `Reference 'eq:certificate' undefined`.
Proposition : soit poser `\label{eq:certificate}` sur l'inégalité `A(k,j) ≥ λ + (j−k)δ_P`
du corollaire (elle n'a pas de label aujourd'hui), soit renvoyer à
`Corollary~\ref{cor:certificate}` qui, lui, existe.
Vérification : `latexmk -pdf -interaction=nonstopmode redaction_QC2_certificat_deterministe.tex ; grep undefined redaction_QC2_certificat_deterministe.log`.

**QC2-B2. Lignes 214-216, « checked … over every trajectory of the campaign : maximal
deviation 1.07 × 10⁻¹⁰ ».**
Le 1,07e−10 est le contrôle `--self-check` d'`analyse_QCD.py`, qui porte sur **200
trajectoires Bernoulli synthétiques** (graine 12345), pas sur la campagne. Sur les **2 000
trajectoires de la campagne**, l'écart maximal entre forme close et récurrence est
**1,26e−11**. Les deux sont de la précision machine, le verdict ne bouge pas, mais la
phrase attribue un chiffre à un jeu de données qui n'est pas le sien. `JOURNAL.md` § 5 le
dit correctement (« 200 trajectoires »).
Proposition : « checked against the naive recurrence on 200 synthetic Bernoulli
trajectories (maximal deviation 1.07 × 10⁻¹⁰) and on the 2 000 trajectories of the
campaign (1.26 × 10⁻¹¹), i.e. machine precision in both cases ».
Vérification : bloc « l. 215 » de `chiffres_QC.py --sous QC2` (recalcule les deux).

**QC2-B3. Lignes 249-262 (table) et 231-232 : des fractions sur 100 graines publiées sans
intervalle de confiance.** `redaction.md` : « chaque probabilité arrive avec son intervalle
de confiance ». La table donne 35 fractions sur n = 100, aucune n'a d'IC. Voici la table
avec l'IC de Wilson à 95 % (formule fermée, contrôlée sur 50/100 → [0,4038 ; 0,5962]),
prête à coller. Les valeurs ponctuelles sont **identiques** aux vôtres.

```latex
\begin{tabular}{rrlllll}
\toprule
& & \multicolumn{2}{c}{$\lambda=8$} & \multicolumn{2}{c}{$\lambda=25$} & $\lambda=50$ \\
$\Delta e$ & $w$ & certificate & detected & certificate & detected & certificate \\
\midrule
0.028 & 1\,969 & 0.10 [0.06;0.17] & 0.10 [0.06;0.17] & 0.00 [0.00;0.04] & 0.00 [0.00;0.04] & 0.00 [0.00;0.04] \\
0.085 &   650 & 0.95 [0.89;0.98] & 0.96 [0.90;0.98] & 0.09 [0.05;0.16] & 0.15 [0.09;0.23] & 0.00 [0.00;0.04] \\
0.141 &   394 & 1.00 [0.96;1.00] & 1.00 [0.96;1.00] & 0.44 [0.35;0.54] & 0.70 [0.60;0.78] & 0.00 [0.00;0.04] \\
0.194 &   287 & 1.00 [0.96;1.00] & 1.00 [0.96;1.00] & 0.73 [0.64;0.81] & 0.91 [0.84;0.95] & 0.00 [0.00;0.04] \\
0.243 &   229 & 1.00 [0.96;1.00] & 1.00 [0.96;1.00] & 0.78 [0.69;0.85] & 0.94 [0.88;0.97] & 0.00 [0.00;0.04] \\
0.361 &   154 & 1.00 [0.96;1.00] & 1.00 [0.96;1.00] & 0.57 [0.47;0.66] & 0.83 [0.74;0.89] & 0.00 [0.00;0.04] \\
0.498 &   112 & 1.00 [0.96;1.00] & 1.00 [0.96;1.00] & 0.02 [0.01;0.07] & 0.02 [0.01;0.07] & 0.00 [0.00;0.04] \\
\bottomrule
\end{tabular}
```

Légende à ajouter : « brackets : Wilson 95 % interval, n = 100 seeds per amplitude ».
Pour la ligne 231 (« 473 cases, 45 in 66, 70 in none » sur 2 000 runs) : 473/2 000 =
23,65 % [Wilson 21,8 ; 25,6], 66/2 000 = 3,3 % [2,6 ; 4,2].
Vérification : bloc « l. 247-253 » (imprime ces lignes LaTeX).

### Mineur

**QC2-M1. Ligne 272-273, « (mean gap 0.037 over all cells, median 0) » dans une phrase
sur λ = 8.**
Texte : `for $\lambda = 8$ it very nearly \emph{equals} it (mean gap $0.037$ over all cells, median $0$)`.
Le 0,0375 est bien la moyenne des **60** cellules (les trois λ), et « over all cells » le
dit ; mais la parenthèse est enchâssée dans une proposition dont le sujet est λ = 8, où la
moyenne vaut **0,0005** (et la médiane 0). Le lecteur pressé attribue 0,037 à λ = 8.
Proposition : « for λ = 8 it very nearly equals it (mean gap 0.0005, median 0 over the 20
amplitudes) ; over the 60 cells of the three thresholds the mean gap is 0.037 ».
Vérification : bloc « l. 272 ».

**QC2-M2. Ligne 238, `w = ⌈3 × 18.5/Δe⌉`.** Le script fait `round()`, pas `ceil` : à
Δe = 0,0282, 3 × 18,5/Δe = 1 969,06, la table dit **1 969** et `ceil` donnerait 1 970 ;
`ceil` s'écarte de la table sur 7 amplitudes sur 20. La table (col. `w`) est juste, c'est
la formule affichée qui ne l'est pas.
Proposition : `w = \mathrm{round}(3 \times 18.5/\Delta e)`, ou « the nearest integer to ».
Vérification : bloc « l. 238 ».

**QC2-M3. Ligne 223, « two-directional short-window » : trompeur.**
Texte à remplacer : `one-directional full-window certificate first, then the two-directional short-window`. L'équivalence du
corollaire est `S_max(w) ≥ λ ⇔ ∃ (k,j) ⊂ ]0,w], A(k,j) ≥ λ + (j−k)δ_P`. Elle ne dit pas que
l'alarme tombe **avant** w : la colonne « detected » compte les alarmes sur tout H. C'est
pourquoi certificat ≤ détection est bien une inégalité et pas une égalité, ce que le
paragraphe « Reading the table » explique correctement deux lignes plus bas. Le mot
« two-directional » en tête de section contredit donc la lecture qu'il annonce.
Proposition : « the short-window certificate, which the corollary makes necessary and
sufficient for S_max(w) ≥ λ, hence sufficient for detection within H ».
Vérification : bloc « l. 223 » de `chiffres_QC.py --sous QC2`, et la colonne
`detection_observee_H_l*` de `QCD_budget_preuve_full`, qui compte les alarmes sur tout
l'horizon et non sur `]0,w]`.

**QC2-M4. Lignes 240-241, guillemets français « » dans un texte anglais.** Deux
occurrences. Remplacer par ``…''.
Vérification : `grep -c '[«»]' redaction_QC2_certificat_deterministe.tex` → 2.

**QC2-M5. Le préambule est en `10pt` avec des marges de 1 cm / 1,5 cm, alors que les huit
autres rédactions sont en `11pt` et 1,2 / 2 cm.** Ligne 1 :
` \documentclass[10pt,a4paper]{article}` (noter l'espace initial parasite) et ligne 7 :
`\usepackage[top=1cm,bottom=1.2cm,left=1.5cm,right=1.5cm]{geometry}`. Les huit autres ont
`\documentclass[11pt,a4paper]{article}` et
`\usepackage[top=1.2cm,bottom=1.5cm,left=2cm,right=2cm]{geometry}`. **Ne rien changer
maintenant** : question d'assemblage, notée pour mémoire.
Vérification : `head -1 redaction_Q*.tex | grep documentclass`.

**QC2-M6. Un `.aux` périmé du 8 septembre (labels français) faisait échouer la
compilation en place.** Aucun `.aux`, `.log` ni `.out` n'est versionné (vérifié :
`git -C repo ls-files | grep -E '04_experimentations/redaction_.*\.(aux|log|out)$'` est
vide). Ceux du 8 septembre ont été supprimés le 10. Si la compilation échoue chez vous :
`cd repo/04_experimentations && latexmk -C redaction_QC2_certificat_deterministe.tex`
puis recompiler.

### Solide, à ne pas toucher

- Preuve de la forme de Lindley, corollaire, et les citations du manuscrit (Définition 2,
  éq. (3), § III-D, Prop. 3 et 9) : vérifiées exactes contre
  `02_biblio/00_BlindSpotParadox_article_source.pdf`.
- Lignes 221-228 : seuils 28 / 45 / 70 ; A(0,H) ≥ 28 dans **473** runs, ≥ 45 dans **66**,
  ≥ 70 dans **0** ; aucun run à Δe = 0,028. Retrouvé exactement.
- Ligne 261-263 : « the certificate never exceeds observed detection », 60 cellules :
  **0 cellule** avec certificat > détection (le pire écart est −2,8e−17, bruit flottant).
- La table (valeurs ponctuelles) : les 35 fractions sont celles de
  `QCD_budget_preuve_full`.
- Les deux corrections de Salomé du 9 septembre (`fa720b2`, fractions atteignables) sont
  justes.

---

## 3. Ce que je change de mon côté, et qui vous concerne

**C'est le message au groupe** exigé par la parade du risque « travail parallèle bâti sur
une version périmée » (`ROADMAP.md` § 7) : tout chiffre déjà rédigé qui change est listé
ici, le jour où il est commité. Si vous avez cité l'une de ces valeurs depuis le 9
septembre, c'est à relire.

| Fichier | Ancien | Nouveau | Table / script |
|---|---|---|---|
| QC3 l. 34 | « ≈ 1 982 » pour `w` à Δe = 0,028 | **1 969** à Δe = 0,0282 (la grille n'est pas à 0,028) | `QCD_budget_preuve_full.w_fenetre_courte` |
| QC3 l. 134-136 | « error falls from 0.024 to 0.007 at the end of the horizon », « subtracts about thirty units » | erreur de fin d'horizon **par amplitude et par fenêtre** : 0,0084 (0,482) → 0,0028 (0,498) sur les 50 derniers pas, non monotone ; déficit `A(H) − A(w) = −38,15` à Δe = 0,498 | `QCD_fin_horizon_full` (nouvelle), `QCD_budget_preuve_full` |
| QC3 l. 178-179 | « underestimates it by 20 % to 41 % above 0.19 » | **−6,9 %** à Δe = 0,194, puis −19,5 % à −41,1 % au-delà ; les « 23 % à 43 % » sous 0,19 restent | `QCD_diagnostic_ajustement_full` |
| QC3 l. 186 | « 6 to 14 times later » | « 6,0 to 14,3 » (chiffre de QC1) | `QCD_indicateurs_full` |
| QD1 l. 183, QD4 l. 209 | « 62 % at Δe = 0.085 » | **64,6 %** (62 victoires sur 96 non censurés, Wilson [54,6 ; 73,4]) : 62 était le numérateur | `QCD_indicateurs_full`, `chiffres_QD.py` |
| QD2 l. 36 | IC « [93,5 ; 158] vs [281 ; 451], 10 000 rééchantillons », qu'aucun script n'émettait | **[92,5 ; 158,5] vs [281 ; 455]**, graine 0, n_boot 10 000, écrits dans une table | `QCD_ic_medianes_tau_arf` (nouvelle), `derives_QD.py` |
| QD4 l. 118 | censure `τ_det` à λ = 25 « 1,0000 » dans le domaine | **0,9900** (à Δe = 0,492/0,494/0,496) ; le 1,00 est à 0,028, hors domaine | `QCD_indicateurs_full` |
| QD4 l. 119 | λ = 50 : « 1,0000 » sans amplitude | 1,0000 à toute amplitude **sauf 0,194**, où tombe l'unique alarme | idem |
| QD4 l. 178-179 | « agreement to two decimal places » | les écarts eux-mêmes : **0,0306** et **0,0403** (ils diffèrent à la 2ᵉ décimale) | `QCD_cas_complets_full` |
| `JOURNAL.md` § 1 C.1 a | « 0 violation sur **6 000** comparaisons » | **5 795** non censurées (chiffre de QC1) | `QCD_indicateurs_full` |
| `JOURNAL.md` § 1 D | « τ_ARF ne porte aucune information sur la quantité de preuve … seule grandeur décidant de l'alarme » | réécrit en deux temps : 0/18 sur `A(H)`, **15/18** sur `S_max(H)` qui décide l'alarme (déjà dans QD3 depuis le 9) | `QCD_correlations_stratifiees_full` |
| `AVERTISSEMENT_RESULTATS_9SEPT.md` point 4 | IC « [93,5 ; 158] contre [281 ; 451] » | ligne de correction ajoutée sous le point : [92,5 ; 158,5] contre [281 ; 455] | `QCD_ic_medianes_tau_arf` |
| `resultats_R2/README.md` | « 6 000 comparaisons », « 7 à 15 fois plus tard », « 8 figures » | 5 795, « 6,0 à 14,3 fois », 20 figures, carte des scripts complétée | |
| QC3, figure du budget | embarquait `Fig_QC_budget_full` | embarque `Fig_QC_budget_utilisable_full`, à deux panneaux, avec `A(H)` : l'ancienne se lit par la couleur (« in blue / in red ») et son titre porte des `---` littéraux. **Le PNG d'origine n'est pas touché** | `QCD_budget_preuve_full` |
| QD1 et QD2 | rien sur les `τ_ARF` nuls | **34 exécutions ont `τ_ARF = 0`** (arbre remplacé au pas de la rupture), à toutes les amplitudes ; ce sont des défaites automatiques du détecteur. Un axe log les effaçait silencieusement de la figure de QD2 | `QCD_indicateurs_full` |
| QD2 | « 346 et 263 ne sont pas séparables » sans statistique | les deux IC se recouvrent sur [281 ; 307], **et** la puissance de la règle à ce rapport (1,32) vaut **0,234** : la non-séparation est presque ininformative, et c'est écrit | `QCD_ic_medianes_tau_arf`, `QCD_ic_medianes_temoins` |
| QD1, total de la course | 95,44 % et 90,95 % sans intervalle | IC de Wilson [94,4 ; 96,3] et [89,6 ; 92,1], avec la réserve qu'un total agrège des cellules de difficulté très inégale | `QCD_indicateurs_full` |

Deux tables neuves dans les `.tex` : **QD1** (course par amplitude à λ = 8, avec IC de
Wilson ; c'est la table qui porte le 95,44 % et le 90,95 %) et **QD2** (IC bootstrap des
trois médianes de `τ_ARF`, avec ses trois témoins). Neuf figures neuves
(`figures_revision_QCD.py`), toutes lisibles en noir et blanc.

**Pour Alexandre, question A.** `Fig_QD_course_lambda_full.png` (et la table 2 de QD1)
donne, par amplitude et pour λ ∈ {8, 25, 50}, la fraction de runs où `τ_det < τ_ARF`, avec
IC de Wilson et le taux de censure de chaque cellule : c'est `P(τ_ARF < τ_det)` lue sur
cette campagne en fonction de (λ, Δe), le point 1 de l'AVERTISSEMENT. Elle est produite dans
QD1 mais elle **est à toi** : je ne l'insère pas dans `redaction_QA_*`, c'est ta décision.

**Incohérence résiduelle de notation, déclarée.** QC1 emploie `τ_err(ρ)` et `τ*` sans les
définir. QC3 révisé et QD1 emploient `τ_rec` et écrivent une fois le lien
`τ_rec = τ_err(ρ)`. Tant que QC1 n'écrit pas ce lien (item QC1-M5), la notation n'est pas
unique sur les sept fichiers. C'est écrit au § 11 du `JOURNAL.md`, pas absorbé.

---

## 4. Ce que cet audit n'a pas fait

- Les **figures de QC1** n'ont pas été régénérées (QC1-F1) : leur lisibilité en noir et
  blanc reste à décider par Alexandre.
- **QC2 n'a pas été corrigé**, même pour le `\eqref` cassé (QC2-B1) : consigne explicite
  d'Ulysse, le fichier est à Salomé et Alexandre.
- La **lecture des sources de river** (remplacement en place ou nouvel objet, attribut
  interne de Page-Hinkley) n'a pas été refaite : `controle_api_structure.py` du 8 septembre
  fait foi, et le risque ne se rouvre que si la version de river change.
- Les **préambules** (10pt / 11pt, `\author{}` vide dans QC3 à QD4) sont une question
  d'assemblage, hors de cet audit.
- Aucune campagne n'a été relancée. Les 1 874 graines de QC1-M1 ne se comblent pas ici :
  la limite se déclare.

**Ce que la double critique adverse a changé dans cette note** (10 septembre, après une
première version) : le compte d'occurrences de `τ_swap` (25 → 30, périmé par la révision du
même jour), les comptes de `~:` et de `---` de QC1-F2 (17 et 8 → **20** et **10**, plus 2
`~;`), et six items qui ne portaient pas leur commande de vérification. Les constats
eux-mêmes n'ont pas bougé : les deux critiques ont rejoué huit des items chiffrés et
confirmé les items « solide ».

Questions ou désaccord : ouvrir le sujet avant de corriger, pas après. Tout se rejoue par
`chiffres_QC.py`.
