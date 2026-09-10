"""
controle_api_structure.py
===================================================================
Controles d'API prealables a la campagne instrumentee (etalon analytique).

POURQUOI CE SCRIPT EXISTE
    La campagne de la tache 3 lit l'interieur de `ARFClassifier` a des endroits
    que river ne documente pas : la liste des arbres actifs, la prediction d'un
    arbre isole, sa taille. Une hypothese fausse sur l'un de ces trois points ne
    produit pas d'erreur : elle produit une trace PLATE, qu'on lit ensuite comme
    un resultat. C'est le mode d'echec numero un du projet (ROADMAP § 7,
    « l'instrumentation ne voit rien »).

    Chaque controle ci-dessous est donc BLOQUANT : si l'un echoue, la campagne ne
    se lance pas. Le script sort en code 1 et dit lequel.

CE QUI EST VERIFIE
    1. `arf.data` est bien la liste des arbres actifs, et `arf.models` designe le
       MEME objet (sinon on instrumente une copie, et phi(t) reste plat).
    2. Un arbre neuf ne predit pas : `predict_one` renvoie None. La convention de
       vote est arretee ici et appliquee partout : un arbre sans prediction est
       EXCLU du vote, et le denominateur est le nombre d'arbres AYANT vote.
    3. `predict_one` ne consomme aucun alea. Sonder la foret a chaque pas ne doit
       pas decaler le flux : sans cette garantie, la campagne instrumentee n'est
       plus comparable a la campagne existante, et le controle de non-regression
       bit a bit de la tache 4 echouerait sans qu'on sache pourquoi.
    4. Le surcout reel du sondage, chronometre, pour annoncer une ETA avant de
       lancer plutot qu'apres.

USAGE
    PYTHONHASHSEED=0 python controle_api_structure.py
"""

import random
import sys
import time
import warnings

import numpy as np

from river import drift
from river.forest import ARFClassifier

warnings.filterwarnings('ignore')

# Parametres du dispositif, identiques a exp_QCD_campagne.py.
N_MODELS = 10
C_INT = 1
N_SONDES = 200

ECHECS = []


def verdict(nom, ok, detail):
    """Consigne un controle. Un echec est bloquant, pas un avertissement."""
    print(f"  [{'OK  ' if ok else 'ECHEC'}] {nom} : {detail}")
    if not ok:
        ECHECS.append(nom)
    return ok


def foret_rodee(n_pas=600, seed=1, n_models=N_MODELS):
    """Une foret entrainee sur la tache pre-rupture, et son generateur de flux."""
    random.seed(seed)
    np.random.seed(seed)
    rng = np.random.default_rng(seed)
    arf = ARFClassifier(
        n_models=n_models, seed=seed,
        drift_detector=drift.ADWIN(clock=C_INT),
        warning_detector=drift.ADWIN(clock=C_INT),
    )
    for _ in range(n_pas):
        x0, x1 = rng.normal(), rng.normal()
        x = {0: x0, 1: x1}
        arf.predict_one(x)
        arf.learn_one(x, int(x0 + x1 > 0.0))
    return arf, rng


def controle_1_liste_arbres():
    """`arf.data` est-il la liste des arbres actifs, et `arf.models` le meme objet ?"""
    print("\n1. LA LISTE DES ARBRES ACTIFS")
    arf, _ = foret_rodee()

    verdict("arf.data existe et a la bonne longueur",
            hasattr(arf, 'data') and len(arf.data) == N_MODELS,
            f"len(arf.data) = {len(getattr(arf, 'data', []))} pour M = {N_MODELS}")

    # `models` est la propriete publique ; `data` l'attribut sous-jacent. On exige
    # l'IDENTITE des objets, pas l'egalite : instrumenter une copie donnerait une
    # trace plate sans lever d'erreur.
    meme_objet = all(a is b for a, b in zip(arf.data, arf.models))
    verdict("arf.models designe les memes objets que arf.data",
            meme_objet and len(arf.models) == len(arf.data),
            "identite verifiee arbre par arbre" if meme_objet else "objets DIFFERENTS")

    a_predire = all(hasattr(a, 'predict_one') for a in arf.data)
    verdict("chaque element expose predict_one", a_predire,
            f"type du premier : {type(arf.data[0]).__name__}")

    # Un remplacement doit se voir. On force le drift et on verifie qu'au moins un
    # arbre change d'identite : si river reinitialisait EN PLACE, le test par id()
    # serait muet et toute l'instrumentation de phi(t) serait fausse.
    ids_avant = [id(a) for a in arf.data]
    rng = np.random.default_rng(999)
    for _ in range(3000):
        x0, x1 = rng.normal(), rng.normal()
        x = {0: x0, 1: x1}
        arf.predict_one(x)
        arf.learn_one(x, int(x0 + x1 > 4.0))     # rupture franche
    n_change = sum(1 for i, a in zip(ids_avant, arf.data) if id(a) != i)
    verdict("un remplacement cree un nouvel objet (id() n'est pas muet)",
            n_change > 0, f"{n_change}/{N_MODELS} arbres ont change d'identite")


def controle_2_arbre_neuf():
    """Que renvoient predict_one et n_nodes sur un arbre qui n'a rien appris ?"""
    print("\n2. L'ARBRE DE SECOURS NEUF, ET LA CONVENTION DE VOTE")
    arf, _ = foret_rodee()
    modele_neuf = arf._new_base_model()
    x = {0: 0.3, 1: 0.4}

    p_neuf = modele_neuf.predict_one(x)
    verdict("predict_one d'un arbre neuf renvoie None",
            p_neuf is None, f"renvoie {p_neuf!r}")

    n_neuf = getattr(modele_neuf, 'n_nodes', 'ABSENT')
    verdict("n_nodes d'un arbre neuf est None ou absent",
            n_neuf is None or n_neuf == 'ABSENT', f"vaut {n_neuf!r}")

    # CONVENTION ARRETEE ICI, appliquee partout ensuite : un arbre qui ne predit
    # pas est exclu du vote, et le denominateur est le nombre d'arbres ayant vote.
    # L'alternative — compter None comme un vote pour la classe 0 — biaiserait
    # acc_bande vers le haut juste apres un remplacement, c'est-a-dire exactement
    # au moment que la mesure doit decrire.
    votes = [a.predict_one(x) for a in arf.data] + [p_neuf]
    exprimes = [v for v in votes if v is not None]
    verdict("la convention de vote est applicable",
            len(exprimes) > 0,
            f"{len(exprimes)}/{len(votes)} arbres votent ; denominateur = {len(exprimes)}")

    if exprimes:
        frac_1 = sum(int(v) for v in exprimes) / len(exprimes)
        print(f"         exemple : fraction votant 1 = {frac_1:.3f} "
              f"(les {len(votes) - len(exprimes)} arbres muets sont exclus, pas comptes 0)")


def controle_3_predict_sans_alea():
    """Sonder la foret decale-t-il le flux ? Si oui, la campagne n'est plus comparable."""
    print("\n3. PREDICT_ONE NE CONSOMME PAS D'ALEA")
    sondes = np.random.default_rng(12345).normal(size=(N_SONDES, 2))

    def trajectoire(avec_sondage):
        random.seed(7)
        np.random.seed(7)
        rng = np.random.default_rng(7)
        arf = ARFClassifier(
            n_models=N_MODELS, seed=7,
            drift_detector=drift.ADWIN(clock=C_INT),
            warning_detector=drift.ADWIN(clock=C_INT),
        )
        erreurs = []
        for t in range(1200):
            x0, x1 = rng.normal(), rng.normal()
            x = {0: x0, 1: x1}
            y = int(x0 + x1 > 0.0)
            erreurs.append(int((arf.predict_one(x) or 0) != y))
            arf.learn_one(x, y)
            if avec_sondage and t % 25 == 0:
                for s0, s1 in sondes:              # sondes fixes, jamais apprises
                    for arbre in arf.data:
                        arbre.predict_one({0: float(s0), 1: float(s1)})
        return erreurs

    sans, avec = trajectoire(False), trajectoire(True)
    identique = sans == avec
    verdict("la trajectoire d'erreur est identique avec et sans sondage",
            identique,
            "bit a bit" if identique
            else f"{sum(a != b for a, b in zip(sans, avec))}/{len(sans)} pas different")


def controle_4_surcout():
    """Chronometrer le surcout du sondage, pour annoncer une ETA avant de lancer."""
    print("\n4. SURCOUT DU SONDAGE (pour l'ETA)")
    sondes = np.random.default_rng(12345).normal(size=(N_SONDES, 2))
    n_pas = 1500

    def chrono(avec_sondage):
        random.seed(3)
        np.random.seed(3)
        rng = np.random.default_rng(3)
        arf = ARFClassifier(
            n_models=N_MODELS, seed=3,
            drift_detector=drift.ADWIN(clock=C_INT),
            warning_detector=drift.ADWIN(clock=C_INT),
        )
        t0 = time.perf_counter()
        for t in range(n_pas):
            x0, x1 = rng.normal(), rng.normal()
            x = {0: x0, 1: x1}
            arf.predict_one(x)
            arf.learn_one(x, int(x0 + x1 > 0.0))
            if avec_sondage and t % 25 == 0:
                for s0, s1 in sondes:
                    for arbre in arf.data:
                        arbre.predict_one({0: float(s0), 1: float(s1)})
        return time.perf_counter() - t0

    t_sans, t_avec = chrono(False), chrono(True)
    surcout = 100 * (t_avec - t_sans) / t_sans
    print(f"  [INFO ] {n_pas} pas : {t_sans:.2f} s sans sondage, {t_avec:.2f} s avec "
          f"-> surcout {surcout:+.0f} %")
    # Le surcout n'est pas un critere de reussite : c'est une mesure pour l'ETA.
    # Seule la campagne post-rupture est sondee (H = 2000 des 6000 pas), donc le
    # surcout effectif sur un run complet vaut environ un tiers de celui mesure ici.
    print(f"  [INFO ] sondage sur les 2000 pas post-rupture seulement "
          f"-> surcout attendu par run : ~{surcout / 3:.0f} %")
    return surcout


def main():
    print("=" * 76)
    print("CONTROLES D'API — chaque echec arrete le plan")
    print("=" * 76)
    controle_1_liste_arbres()
    controle_2_arbre_neuf()
    controle_3_predict_sans_alea()
    controle_4_surcout()

    print("\n" + "=" * 76)
    if ECHECS:
        print(f"BLOQUANT — {len(ECHECS)} controle(s) en echec :")
        for nom in ECHECS:
            print(f"  - {nom}")
        print("La campagne instrumentee ne doit pas etre lancee en l'etat.")
        sys.exit(1)
    print("Tous les controles passent. La campagne instrumentee peut etre lancee.")
    print("=" * 76)


if __name__ == "__main__":
    main()
