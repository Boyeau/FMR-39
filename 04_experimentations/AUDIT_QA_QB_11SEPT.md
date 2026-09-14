# Audit de Q A et Q B : constats, sans modification

**Écrit le 11 septembre 2026 par Ulysse (piste socle / C·D).**
Destinataire : Alexandre, auteur des deux fichiers. **Rien n'a été modifié** dans
`redaction_QA_course_concurrente.tex` ni `redaction_QB_biais_independance.tex`, ni dans
les PDF, ni dans les scripts. Cette note dit ce que j'ai trouvé et laisse la correction à
celui qui a écrit le texte.

Même format que `AUDIT_QC1_QC2_10SEPT.md` : chaque item porte le chemin dans `repo/`, la
ligne au 11 septembre, le texte exact entre guillemets, une proposition de remplacement
(en français, à traduire) et la commande de vérification. Les items « solide » sont **à ne
pas toucher** : ils sont listés pour que personne ne « corrige » ce qui est juste.

**Comment rejouer les chiffres :**

```bash
cd repo/04_experimentations/resultats_R2/scripts
PYTHONHASHSEED=0 ../../../../.venv/bin/python chiffres_QA.py   # QA, sections 3 et 4
PYTHONHASHSEED=0 ../../../../.venv/bin/python chiffres_QC.py --sous QC1   # le 5 795 de QB
```

Tout ce qui suit sort de là, de `QCD_indicateurs_full.parquet` lu directement, ou d'un
`grep` donné item par item. Aucun chiffre ne vient de mémoire ni du `JOURNAL.md`.

---

## 0. Bloquant

### **AB-B1. Les deux PDF sont périmés — celui de Q A ampute deux pages — et aucune des neuf rédactions n'a son PDF versionné, contrairement à ce que le `.gitignore` annonce.**

Fichiers : `repo/04_experimentations/redaction_QA_course_concurrente.pdf` et
`redaction_QB_biais_independance.pdf`, tous deux datés du **8 septembre 15h28**, alors que
les `.tex` datent du 11 septembre. Trois commits sont passés entre-temps :
`de4ad76` (« QA : ajoute la section empirique que l'énoncé demande »), `ba0f260`
(« QB : « 2 000 runs » -> les 5 795 comparaisons non censurées ») et `64a86ae`
(« QA : évalue la borne de Fréchet sur les marginales estimées »).

Conséquences mesurées :

- **Q A** : le PDF sur disque fait **3 pages**, le `.tex` actuel en fait **5**. Le PDF ne
  contient ni la section 4 « The Race, Measured », ni le paragraphe « The bound on the
  estimated marginals ». Autrement dit, **toute la partie empirique que le sujet réclame
  est absente du PDF** que lit un relecteur, ou l'encadrant si le fichier part par mail.
- **Q B** : le PDF contient encore « 2 000 runs » et **pas** « 5 795 ». Il affiche donc
  toujours le chiffre que `ba0f260` a explicitement corrigé.

Les deux sources compilent proprement (`pdflatex`, 0 warning, 0 référence indéfinie ;
seul un `Overfull \hbox` de 3,05 pt en Q B lignes 123–127). Il n'y a donc rien à réparer
dans le texte : il faut recompiler.

**Et il faut décider si ces PDF entrent dans le dépôt.** Le `.gitignore` du dépôt dit en
toutes lettres : `# artefacts de compilation LaTeX (les .pdf restent visibles : livrables)`.
L'intention est donc de versionner les PDF. Or `git status` montre que **les neuf
`redaction_*.pdf` sont non suivis** — aucun n'est dans l'index. Les 22 PDF versionnés du
dépôt sont tous dans `01_consignes/` et `02_biblio/`, c'est-à-dire de la matière reçue.
Concrètement : les trois autres n'ont jamais vu un seul PDF de rédaction, seulement les
`.tex`. Ce n'est pas un problème tant que chacun compile — les deux fichiers compilent —
mais l'écart entre l'intention écrite dans le `.gitignore` et l'état réel se tranche à
quatre, une fois, pour les neuf fichiers.

Vérification :
```bash
cd repo/04_experimentations
ls -l redaction_QA_course_concurrente.{tex,pdf} redaction_QB_biais_independance.{tex,pdf}
pdftotext redaction_QB_biais_independance.pdf - | grep -c "5 795"   # -> 0
pdflatex -interaction=nonstopmode redaction_QA_course_concurrente.tex >/dev/null
pdfinfo redaction_QA_course_concurrente.pdf | grep Pages            # -> 5, pas 3
git -C .. ls-files | grep -c '04_experimentations/.*\.pdf'          # -> 0
grep -n 'pdf restent visibles' ../.gitignore
```

---

### **AB-B2. Q A ligne 272 : « the detector never alarms at all » est faux, et contredit la table 2 de Q D.1 citée une ligne plus bas.**

Fichier : `redaction_QA_course_concurrente.tex`, lignes 271–272.
Texte : `runs from $0.01$ at the top of the grid to $1.00$ at $\Delta e=0.028$, where the`
puis `detector never alarms at all within the horizon:`.

**Ce que disent les données.** À `Δe = 0,0282`, `λ = 8` : sur 100 exécutions, le détecteur
alarme dans **10** d'entre elles (taux de censure 90 %, pas 100 %). Les dix `τ_det`
observés valent 121, 230, 272, 400, 455, 468, 560, 569, 690 et 1 620 pas. Le détecteur
**alarme mais perd toujours** : le plus grand `τ_ARF` de la cellule vaut 805, et
`P_miss = 1,00` parce que chacune de ces dix alarmes arrive après la réparation, pas parce
qu'aucune n'arrive.

C'est exactement ce qu'écrit **la table 2 de Q D.1**, que la phrase suivante de Q A cite :
ligne `$0.028$ & $10$ & $0$ & not reported (censoring $90\%$) & $0.0$`. Dix non censurées,
zéro victoires. Le point 1 de `AVERTISSEMENT_RESULTATS_9SEPT.md` dit la même chose :
« à `Δe = 0,028`, le détecteur **ne gagne jamais** ». *Ne gagne jamais* est devenu
*n'alarme jamais* : c'est là qu'est la bascule.

Il y a une conséquence interne : si `F̂_D` était plate à 0 sur cette cellule, la borne
inférieure de Fréchet vaudrait 1,00. La table de la section 3 du même fichier affiche
**0,91** — donc le texte de la section 4 contredit la table de la section 3.

Proposition : « … à Δe = 0,028, où le détecteur n'alarme que dans 10 exécutions sur 100
et toujours après la réparation de la forêt : l'agrégat de 9,05 % est porté presque
entièrement par cette seule amplitude ».

Vérification :
```bash
cd repo/04_experimentations/resultats_R2/scripts
../../../../.venv/bin/python -c "
import pandas as pd
d=pd.read_parquet('../resultats/data/QCD_indicateurs_full.parquet')
s=d[d.delta_e==sorted(d.delta_e.unique())[0]]
print('alarmes observees :', int((~s.censored_det_8.astype(bool)).sum()), '/', len(s))
print('tau_det observes  :', sorted(s.loc[~s.censored_det_8.astype(bool),'tau_det_8']))
print('tau_arf max       :', s.tau_arf.max())"
grep -n '0.028. & .10.' ../../redaction_QD1_instrumentation_conjointe.tex
```

---

### **QB-B3. Ligne 23 : `S` est défini comme « one seed », or dans la campagne la graine pilote aussi les arbres — `G_S` devient dégénéré et la mesure proposée en conclusion n'estime pas ce qu'elle prétend.**

Fichier : `redaction_QB_biais_independance.tex`, ligne 23.
Texte : `$S$ is the complete realization of the stream (one seed) ; $U_i$ the randomness`.

La théorie des sections 1 et 2 est juste **si `S` est la seule trajectoire `(x_t, y_t)`**
et si les `U_i` sont tirés indépendamment d'elle. Mais la parenthèse identifie `S` à la
graine de la campagne, et cette identification est fausse ici :
`resultats_R2/scripts/exp_QCD_campagne.py` lignes 94–100 donne **la même** `safe_seed` au
flux (`rng = np.random.default_rng(safe_seed)`, ligne 97, qui tire `x0, x1`) **et** au
modèle (`ARFClassifier(n_models=..., seed=safe_seed)`, lignes 99–100).

Conditionner sur la graine fixe donc aussi `U_1, …, U_M` : il ne reste aucun aléa,
`G_S(s) ∈ {0, 1}` presque sûrement, et `Var(G_S) ` est maximale par construction. La
factorisation reste vraie, mais vide.

La conclusion en hérite. Ligne 182 : `What remains is to measure $G_S(s)$ empirically on
the campaign's runs (inter-seed` / ligne 183 `variance of a single tree's survival at a
fixed $s$)`. Une variance **inter-graines** de la survie d'un seul arbre mélange
`Var(G_S)` et le tirage binomial interne ; elle ne peut pas les séparer. Le bon estimateur
est **intra-exécution** : pour chaque run `r`, la fraction `p̂_r(s)` des `M = 10` arbres
non encore remplacés à `s`, puis

```
Var(p̂) = Var(G_S) + E[G_S(1−G_S)] / M      d'où      Var̂(G_S) = Var(p̂) − Ê[G_S(1−G_S)]/M
```

(décomposition de variance à un facteur, le terme intra s'estimant sans biais par
`p̂(1−p̂)·M/(M−1)` moyenné sur les runs).

C'est directement calculable, sans relancer quoi que ce soit :
`resultats_R2/resultats/data/QCD_events_swap_full.parquet` porte `(run_id, t, tree_id)`
avec `t` **déjà compté en pas post-rupture** (`exp_QCD_campagne.py` ligne 136,
`idx = t - T_DRIFT`), soit 21 561 événements. `τ_i` est le `min t` par `(run_id, tree_id)`,
censuré à `H = 2000` pour les arbres jamais remplacés — et son taux de censure est à
publier avec le résultat.

Proposition, en deux temps : ligne 23, retirer « (one seed) » et écrire « S est la
trajectoire (x_t, y_t) seule » ; puis une phrase de réserve — « dans la campagne R2 une
graine unique pilote à la fois le flux et les tirages internes des arbres, de sorte que
G_S ne s'estime pas entre graines mais à l'intérieur d'une exécution, sur la fraction des
M arbres encore en place » ; et ligne 182, remplacer l'estimateur inter-graines par
l'estimateur intra-exécution ci-dessus.

Vérification :
```bash
sed -n '94,100p;136p' repo/04_experimentations/resultats_R2/scripts/exp_QCD_campagne.py
../../.venv/bin/python -c "
import pandas as pd; e=pd.read_parquet('resultats_R2/resultats/data/QCD_events_swap_full.parquet')
print(e.shape, e.columns.tolist()); print(e.groupby('run_id').t.min().describe())"
```

---

### **QB-B4. Ligne 98 : « `P_miss` — Too pessimistic » est un saut des marginales vers la loi jointe, c'est-à-dire exactement ce que la section 3 de Q A démontre illégitime.**

Fichier : `redaction_QB_biais_independance.tex`, ligne 98.
Texte : `$P_{\mathrm{miss}}$ & Too pessimistic --- overestimates the blind-spot risk \\`.

La section 2 établit un ordre **stochastique sur la marginale** de `τ_ARF`. Or
`P_miss = P(τ_ARF < τ_det)` dépend de la **loi jointe** des deux horloges : c'est la thèse
centrale de Q A section 3, qui montre que les marginales seules laissent une plage de
0,09 à 0,34 de masse de probabilité à `λ = 8`. Un `τ_ARF` stochastiquement plus lent ne
donne un `P_miss` plus petit que si l'on ajoute une hypothèse sur le couplage — la plus
simple étant `τ_ARF ⊥ τ_det`. Sans elle, l'énoncé du tableau n'est pas démontré, et les
deux rédactions du même auteur se contredisent.

La réparation est courte et ne coûte rien au résultat, parce que le manuscrit fait déjà
cette hypothèse : l'énoncé correct porte sur **deux calculs**, pas sur la réalité.
Proposition : « `P_miss` — trop pessimiste *sous l'hypothèse d'indépendance entre les deux
horloges que le manuscrit pose par ailleurs* : à `τ_det` inchangé et indépendant, une
réparation stochastiquement plus lente donne moins de Miss. Sans cette seconde hypothèse,
les marginales seules ne fixent pas `P_miss` (Q A, section 3). »

Vérification : `grep -n 'Valid for any dependence structure' redaction_QA_course_concurrente.tex`
(ligne 138) — c'est la phrase de Q A que cette ligne de Q B enjambe.

---

## 1. Mineur (chiffres et périmètre)

**QA-M1. Section 3, table des lignes 169–185 : aucun taux de censure, alors qu'il monte à 90 % et 98 %.**
`redaction.md` : « Chaque durée censurable arrive avec son taux de censure. » Le texte
lignes 165–167 dit bien que `F̂_D` est sous-stochastique « so its plateau sits at one minus
the cell's censoring rate » — mais ne donne jamais ce taux. Il est spectaculaire :

| `Δe` | censure `τ_det` à `λ = 8` | à `λ = 25` |
|---|---|---|
| 0,028 | **90 %** | **100 %** |
| 0,085 | 4 % | 85 % |
| 0,141 | 0 % | 30 % |
| 0,194 | 0 % | 9 % |
| 0,243 | 0 % | 6 % |
| 0,361 | 0 % | 17 % |
| 0,498 | 0 % | 98 % |

Proposition : une colonne « censure » par bloc `λ`, ou une ligne de légende sous la table.
Vérification : `chiffres_QA.py`, section 3 ; ou le script de AB-B2 avec `censored_det_25`.

**QA-M2. Ligne 273, « Figure~2 of Q~D.1 » désigne la mauvaise figure.**
Texte : `almost entirely by that single weakest amplitude. Table~2 and Figure~2 of Q~D.1 give the`.
Dans `redaction_QD1_instrumentation_conjointe.tex`, la figure 2 est `fig:rg`
(`Fig_QD_R_et_G_full.png`, « R et G contre Δe »). La ventilation par cellule de la course
est la **figure 4**, `fig:course` (`Fig_QD_course_lambda_full.png`) — celle-là même que Q A
inclut vingt lignes plus bas, ligne 278. La table 2 est juste.
Proposition : « Table 2 and Figure 4 of Q D.1 ».
Vérification : `grep -n 'includegraphics\|label{fig:' redaction_QD1_instrumentation_conjointe.tex`
→ ordre `fig:joint`, `tab:socle`, `fig:rg`, `fig:palier`, `tab:course`, `fig:course`.

**QA-M3. `chiffres_QA.py` ne rejoue que 4 des 7 lignes de la table de la section 3.**
Le script n'imprime que les amplitudes d'indice 0, 1, 2 et 19 (ligne 199 de
`chiffres_QA.py` : `if de in (grille[0], grille[1], grille[2], grille[19])`). Les lignes
`0.194`, `0.243` et `0.361` de la table du `.tex` ne sortent d'aucune impression. Je les ai
recalculées : elles sont **exactes** (voir « solide » plus bas), mais un chiffre du rapport
doit être réimprimable par le script qui le revendique.
Proposition : remplacer la condition par la liste des sept amplitudes citées.
Vérification : `grep -n 'grille\[19\]' resultats_R2/scripts/chiffres_QA.py`.

**QA-M4. La bande dégénérée `Δe ≥ 0,45` n'est déclarée nulle part, alors qu'elle pèse 9 des 20 amplitudes moyennées.**
Le point 3 de `AVERTISSEMENT_RESULTATS_9SEPT.md` : « à `Δe ≥ 0,45`, la forêt ne s'adapte
pas, elle répond « toujours 0 » » — 900/900 signalés, 652/900 dégénérés définitifs. Or les
trois chiffres de synthèse de la section 3 (« mean width per amplitude is 0.195 … 0.106 …
0.001 », lignes 194–195) sont des moyennes sur les 20 amplitudes, dont ces 9. Le sujet
exige la liste explicite de ce qui n'a pas été fait ; un domaine de validité amputé de
moitié se déclare.
Proposition : une phrase après la table — « les neuf amplitudes `Δe ≥ 0,45` sont dans le
régime de dégénérescence documenté au point 3 de l'avertissement du 9 septembre ; les
moyennes par amplitude les incluent ».
Vérification : `grep -n '0,45' AVERTISSEMENT_RESULTATS_9SEPT.md`.

**QA-M5. « Q~B.1 » (ligne 300) et « Q~B.2 » (QC1, ×4) renvoient à des documents qui n'existent pas.**
Texte : `therefore to ask how much of this gap the conditional factorization of Q~B.1 actually`.
La convention du dossier est « Q X.n = le n-ième fichier de la question X » : `Q~C.1` →
`redaction_QC1_*`, `Q~D.4` → `redaction_QD4_*`. Il n'y a **qu'un** fichier Q B, à six
sections. « Q B.1 » et « Q B.2 » sont donc soit des renvois à des sections (et il faut
écrire « Q B, section 1 »), soit le vestige d'un découpage abandonné. `redaction_QC1_hierarchie.tex`
écrit « Q~B.2 » quatre fois (lignes 80, 81, 86, 94). À trancher **une fois pour les deux
fichiers**, avant l'assemblage.
Au passage : **aucun document ne cite Q~A**. Le renvoi est à sens unique — Q A pointe
quatre fois vers Q D.1, Q D.1 ne revient jamais. La section 3 de Q A (borne de Fréchet) est
pourtant l'outil qui manque aux totaux de grille de Q D.1 et Q D.4.
Vérification : `grep -on 'Q~[ABCD]\(\.[0-9]\)\?' redaction_*.tex | sort -u`.

**QA-M6 (occasion, pas défaut). La colonne `λ = 25` de la table de la section 3 affiche la non-monotonie du point 4 de l'avertissement, et le texte ne la relève pas.**
`P_miss` à `λ = 25` fait 1,00 → 0,95 → **0,77** → 0,82 → 0,94 → 1,00 → 1,00 : un creux net
à `Δe = 0,141`. C'est le point 4 de l'avertissement (médiane de `τ_ARF` : 118 pas à 0,028,
**346** à 0,085, puis décroissance jusqu'à 28) vu du côté de la course : là où la forêt est
la plus lente, le détecteur gagne le plus. Deux phrases, rien à recalculer, et cela lie Q A
à un résultat déjà établi et déjà chiffré ailleurs.

**QB-M7. Ligne 27, « the R2 campaign » est ambigu.**
`M = 10` est le paramètre de la campagne **du groupe** (`exp_QCD_campagne.py`, `n_models`
vérifié à 10 sur les 2 000 lignes de `QCD_indicateurs_full`), pas du R2 des auteurs —
même si le dossier s'appelle `resultats_R2` et que `exp_R2_instrumented_blind_spot.py`
utilise lui aussi `N_MODELS = 10`. Pour un lecteur extérieur, « R2 » désigne
l'expérience du dépôt officiel.
Proposition : « the group's instrumented campaign (`resultats_R2`, M = 10) ».

**QB-M8. La section 5 duplique quasi mot pour mot un paragraphe de Q C.1.**
Q B lignes 156–178 et `redaction_QC1_hierarchie.tex` lignes 80–96 disent la même chose
dans les mêmes termes (« purely combinatorial fact », « model misspecification »,
« compounding, not the same fact observed twice »). Deux documents qui iront dans le même
rapport de 10 à 15 pages. Ce n'est pas une faute — c'était même l'objet du commit
`f531a2a` — mais à l'assemblage il en restera **un seul**, et il faut décider lequel.
Même remarque pour la figure : Q A ligne 278 inclut `Fig_QD_course_lambda_full.png`, qui
est déjà la figure 4 de Q D.1.

**QB-M9. `τ_swap(q)` est employé ligne 168 sans définition, et sans la réserve de Q C.1 sur les quotas.**
Q C.1 lignes 43–52 : avec `M = 10`, les étiquettes 25 % et 75 % désignent en fait **3
arbres (30 %)** et **8 arbres (80 %)**, par arrondi entier. Q B parle de « a genuinely
significant fraction of the forest » sans chiffre. Un renvoi suffit.

**QB-M10. La comparaison R6/R9 contre R2 proposée en conclusion est celle que le point 2 de l'avertissement a disqualifiée sous sa forme brute.**
Lignes 184–186 : `Also compare R6/R9 (single tree, $M=1$) against R2 (forest, $M=10$)`.
Le fait est juste — `R6_hydra_factor/exp_R6_generate_data.py` ligne 28 et
`R9_mcrit/exp_R9_generate_data.py` ligne 25 posent bien `N_MODELS = 1`, contre 10 pour R2.
Mais le point 2 de `AVERTISSEMENT_RESULTATS_9SEPT.md` a retiré la conclusion tirée du
rapport brut `τ_ARF(M)/τ_ARF(M')` : ce rapport **n'est pas un test d'indépendance**. Sous
indépendance, la médiane attendue à `M` se prédit depuis la distribution empirique à `M'`
par `S_{M'}^{(M/M')}`, et c'est l'écart observé/prédit qu'il faut lire. Ajouter que R6 pose
en plus `C_INT = 1`, donc le contraste `M = 1` contre `M = 10` n'est pas toutes choses
égales par ailleurs.
Proposition : conserver la piste en nommant le test correct, et renvoyer au point 2.

**QB-M11. Le corollaire `M_crit` peut être plus fort que « borne inférieure » : il peut être inatteignable à tout `M` fini.**
Lignes 106–109. « `M ≥ M_crit` » est juste. Mais
`lim_{M→∞} E[G_S(s)^M] = P(G_S(s) = 1)` par convergence dominée : la confiance maximale
atteignable, **quel que soit le nombre d'arbres**, vaut `1 − P(G_S(s) = 1)`. S'il existe
une fraction de flux sur lesquels aucun arbre n'adapte avant `s`, et si cette fraction
dépasse `1 − β`, alors **aucun `M` fini** n'atteint `β` — le certificat n'est pas seulement
conservateur, il est vide. C'est un résultat plus tranché que celui écrit, gratuit
(trois lignes), et vérifiable sur `QCD_events_swap_full.parquet` par le même comptage
qu'en QB-B3.

**QB-M12. Aucun script ne rejoue Q B.**
Il existe `chiffres_QA.py`, `chiffres_QC.py`, `chiffres_QD.py` ; pas de `chiffres_QB.py`.
Le 5 795 de la ligne 162 est réimprimé par `chiffres_QC.py` sous l'étiquette « QC1 l.56 »,
donc traçable — mais le **205** censurées, lui, n'est imprimé par aucun script (je l'ai
recalculé : 1 + 22 + 182 pour `q = 25/50/75 %`, total 205, et 5 795 + 205 = 6 000 = 3 × 2 000).
Proposition : soit trois lignes ajoutées à `chiffres_QC.py`, soit un `chiffres_QB.py` qui
portera aussi la mesure de `Var(G_S)` de QB-B3.

**QB-M13. « Oza \& Russell, 2001 » (ligne 33) est cité sans bibliographie.**
Aucun `\cite`, aucun `\bibliography` dans le fichier. À harmoniser au moment de
l'assemblage, avec `02_biblio/`.

---

## 2. Mineur (forme, à trancher par vous)

**AB-F1. Em-dashes : 22 en Q A, 18 en Q B, contre 1 dans chacun des quatre Q D.**
`redaction.md` : « les em-dashes (—) … se traquent au grep avant tout envoi ». Le nettoyage
a manifestement été fait sur Q C.3 et Q D, pas sur Q A ni Q B :

```
redaction_QA_course_concurrente.tex          22 --- /  303 lignes
redaction_QB_biais_independance.tex          18 --- /  188 lignes
redaction_QC1_hierarchie.tex                 11 --- /  224 lignes
redaction_QC2_certificat_deterministe.tex    16 --- /  289 lignes
redaction_QC3_invariance.tex                  3 --- /  307 lignes
redaction_QD1_instrumentation_conjointe.tex   1 --- /  307 lignes
redaction_QD2_coefficient_association.tex     1 --- /  231 lignes
redaction_QD3_stratification_amplitude.tex    1 --- /  199 lignes
redaction_QD4_protocole_decision.tex          1 --- /  267 lignes
```

Q B est le plus dense du dossier : un em-dash toutes les dix lignes. Aucune tournure de la
liste noire (*moreover*, *furthermore*, *notably*, *it is worth noting*) en revanche : zéro
occurrence dans les deux fichiers.
Vérification : `for f in redaction_*.tex; do echo -n "$f "; grep -o -- '---' "$f" | wc -l; done`

**AB-F2. Prénoms dans un livrable en anglais.**
Q B ligne 158 : `Salomé's instrumented campaign`. Les `\author{}` porteront les noms ; dans
le corps, « Q C.1 » suffit. Même remarque pour « as suggested by Minato » ligne 185–186 :
à garder dans le `JOURNAL.md`, pas dans le rapport.

**AB-F3. `Overfull \hbox` de 3,05 pt en Q B, lignes 123–127** (le paragraphe du
contre-exemple). Seul défaut de composition des deux fichiers.

---

## 3. Solide — ne pas toucher

**La totalité des mathématiques de Q A est juste**, vérifiée à la main :

- Section 1 : `∞ < ∞` faux sur les réels étendus, donc la double famine sort de `Miss`
  sans traitement particulier — correct, et la convention stricte est explicitement posée.
- Section 2 : la partition en quatre régions est exhaustive et l'exclusion de la région 3
  de `Miss` est juste ; la largeur `P(C_H)` est atteinte aux deux extrémités.
- Section 3, borne inférieure : `{τ_A ≤ s < τ_D} ⊆ Miss` pour tout `s`, et Fréchet donne
  bien `max(0, F_A(s) − F_D(s))`.
- Section 3, borne supérieure : `Miss ⊆ {τ_A ≤ s} ∪ {τ_D > s+1}` est correcte (si
  `τ_A ≥ s+1` et `τ_D > τ_A`, alors `τ_D > s+1`), et Boole donne la forme écrite.
- Cas jouet : `sup = 0` atteint par le couplage comonotone, `inf = 0,5` atteint en `s = 0`
  et `s = 1` par l'antimonotone. Recalculé : les deux bornes sont atteintes, la table
  lignes 145–155 est exacte.

**Les 42 nombres de la table des lignes 169–185 sont exacts**, y compris les trois lignes
que `chiffres_QA.py` n'imprime pas (`0.194` → 0,05 / 0,06 / 0,23 et 0,49 / 0,82 / 1,00 ;
`0.243` → 0,03 / 0,03 / 0,23 et 0,71 / 0,94 / 1,00 ; `0.361` → 0,02 / 0,02 / 0,25 et
0,92 / 1,00 / 1,00).

**Les chiffres de synthèse de la section 3 sont exacts** : encadrement valide sur 20/20
amplitudes à chacun des trois seuils ; largeur par amplitude min 0,090, max 0,340, moyenne
**0,195** à `λ = 8` ; **0,106** à `λ = 25` ; **0,001** à `λ = 50` ; en agrégeant les 20
amplitudes `[0,048 ; 0,485]`, largeur **0,437**. Le « between 0.09 and 0.34 » de la
conclusion (ligne 296) est bien le min et le max des largeurs, pas une approximation.

**Tous les chiffres de la section 4 sont exacts** : 0/2 000 censures de `τ_ARF`, maximum
observé 1 293 ; régions 1 906 / 94, 778 / 1 222, 1 / 1 999 ; `C_H = 0` aux trois seuils ;
`P_miss` 0,0905 / 0,9715 / 1,0000 ; les trois intervalles de Wilson au dix-millième
(`[0,0787 ; 0,1039]`, `[0,9633 ; 0,9779]`, `[0,9981 ; 1,0000]`) ; ex aequo 0 / 6 sur 778
(0,77 % et 0,30 %) / 0, et le « at most 0.003 » qui s'en déduit. Le contrôle croisé avec
Q D.1 tombe juste : 181 + 1 819 = 2 000, et Q D.1 écrit bien `1\,819` dans sa table 2.

**Côté Q B** :

- La factorisation conditionnelle de la section 1 est le bon argument, et la remarque sur
  l'arbre neuf qui « n'hérite ni des poids ni de la structure » est exacte pour ARF.
- Jensen sur `x ↦ x^M` et la condition d'égalité (`G_S` p.s. constante) : correct.
- La section 4 est juste de bout en bout : covariance totale, terme intra nul par
  indépendance conditionnelle, terme inter égal à `Var(G_S(1)) ≥ 0`, donc le couplage
  antimonotone à `−1/4` est structurellement impossible. C'est le meilleur passage des deux
  fichiers.
- `5 795` comparaisons non censurées et **0 violation** de `τ_ARF ≤ τ_swap(q)` :
  recalculé, exact, et cohérent au chiffre près avec la ligne 56 de Q C.1. Le **205**
  censurées que Q B ajoute et que Q C.1 n'écrit pas est exact lui aussi (1 + 22 + 182) —
  c'est le taux de censure que `redaction.md` réclame, et il est du bon côté.
- `M = 10` sur les 2 000 lignes de la campagne ; `N_MODELS = 1` pour R6 et R9. Les deux
  affirmations de la conclusion sont vérifiées.
- Le corollaire `M_crit` reclassé en « certificat conservateur » est juste (la loi d'un
  arbre seul ne dépend pas de `M` dans ARF, chaque arbre s'entraînant sur le flux et son
  propre détecteur).

---

## 4. Ce que je n'ai pas fait

- Je n'ai **rien modifié** : ni `.tex`, ni `.pdf`, ni script, ni figure.
- Je n'ai **pas mesuré `Var(G_S)`**. L'estimateur est posé en QB-B3 et la table nécessaire
  existe, mais un résultat neuf ne s'écrit pas avant que son analyse soit close, et c'est
  la vôtre.
- Je n'ai **pas relancé de campagne**. Tout sort de `QCD_indicateurs_full.parquet` et
  `QCD_events_swap_full.parquet` déjà versionnés.
- Je n'ai **pas tranché** la numérotation « Q B.1 / Q B.2 » (QA-M5) ni le doublon Q B
  section 5 / Q C.1 (QB-M8) : ils touchent deux fichiers dont vous et Salomé êtes
  responsables, et la répartition du `ROADMAP.md` § 6 dit que cela ne se tranche pas seul.
