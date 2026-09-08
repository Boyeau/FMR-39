"""
exposants_fonctionnelles.py
===================================================================
Taxonomie des detecteurs par leur exposant en Delta_e — entierement HORS LIGNE,
sur `QCD_traces_error_full.parquet` seul. Aucune simulation.

LA QUESTION
    Le budget de preuve offert a un moniteur ne depend pas seulement de
    l'amplitude du drift, mais de la FONCTIONNELLE que ce moniteur calcule sur la
    trajectoire d'erreur. Deux detecteurs lisant la meme trajectoire peuvent avoir
    des sensibilites opposees. On les classe donc par leur exposant.

LE MODELE, ET SA PREDICTION
    Apres la rupture, l'ecart au socle vaut xi_t ~ Delta_e pendant une duree
    d'adaptation W ~ Delta_e^(-alpha). Une fonctionnelle qui integre xi^p sur une
    fenetre de duree ~W^q se comporte donc en

        Delta_e^p * W^q  ~  Delta_e^(p - q*alpha)

    d'ou un exposant PREDIT de `p - q*alpha` pour chaque famille, avec
    alpha = 0,857 — l'exposant GLOBAL de tau_ARF, fige avant mesure.

    L'alpha LOCAL est mesure en regard, et son instabilite est un resultat en soi :
    selon la duree d'adaptation retenue et le segment, il vaut de 0,12 a 3,24. Le
    modele a alpha unique ne decrit donc pas ce dispositif. Le verdict d'accord
    porte sur la prediction pre-enregistree, jamais sur une prediction recalculee
    apres coup avec l'alpha local — ce serait deplacer la cible apres le tir.

PREDICTIONS PRE-ENREGISTREES, ecrites avant la mesure
    sup             (p,q) = (1,0)   exposant  1
    aire            (1,1)           1 - alpha    ~ +0,14
    energie         (2,1)           2 - alpha    ~ +1,14   robuste
    GLR fenetre     (2,1)           2 - alpha    ~ +1,14   robuste
    MMD^2 fenetre   (2,2)           2 - 2*alpha  ~ +0,29   condamne comme l'aire
    ADWIN           --              1 - alpha/2  ~ +0,57   sa statistique
                                    normalisee est Delta_e*sqrt(W), pas Delta_e
    duree > delta_P (0,1)           -alpha
    pente max                       DEJA REFUTEE : +0,71 mesure contre +1,86
                                    predit. Le drift est un ECHELON, sa derivee
                                    vaut Delta_e et non Delta_e/W. Ecrit comme
                                    resultat negatif, pas remesure en esperant
                                    mieux.

CONTRAINTE DE GRILLE — a declarer avec tout exposant
    `b` varie d'un facteur 40 mais Delta_e d'un facteur 17,7 seulement, et les SIX
    dernieres cellules ne couvrent que 3,2 % de variation en Delta_e. Une
    regression log-log GLOBALE est donc dominee par le bas de grille et ne decrit
    rien. Les exposants se lisent LOCALEMENT, sur trois segments declares.

LISSAGE — pourquoi il faut le declarer
    e_t est binaire : `sup e_t` vaut 1 dans tous les runs et ne mesure rien. Les
    fonctionnelles portent donc sur xi_t = (moyenne glissante de e sur L pas) - p0,
    avec L = 50 declare ici. Ce choix ne touche ni l'aire ni le CUSUM, qui somment
    de toute facon ; il ne concerne que sup, la pente et le MMD.

USAGE
    PYTHONHASHSEED=0 python exposants_fonctionnelles.py
"""

import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA = ROOT_DIR / "resultats" / "data"
FIGURES = ROOT_DIR / "resultats" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

H = 2000
N_MODELS_DEFAUT = 10           # M de la campagne full ; absent de sa table meta
DELTA_P = 0.01
L_LISSAGE = 50                  # fenetre de moyenne glissante, declaree
W_GLR = 200                     # fenetre la plus longue du GLR et du MMD, declaree
# Le GLR prend le sup sur un jeu de fenetres. Il DOIT contenir des fenetres courtes :
# sans elles, aucune detection n'est possible avant la plus courte disponible, et le
# delai mesure plancherait a cette valeur — un artefact de maillage qu'on lirait
# comme « le GLR detecte moins vite que le CUSUM » a forte amplitude.
FENETRES_GLR = (10, 20, 50, 100, 200)
PAS_SCAN = 10
N_BOOT = 2000
SEED_BOOT = 20260908
P0_MMD = None                   # rempli par run

# Segments de grille : bas / milieu / haut, declares avant mesure.
SEGMENTS = {'bas': slice(0, 6), 'milieu': slice(6, 14), 'haut': slice(14, 20)}

# alpha PRE-ENREGISTRE : |exposant global de tau_ARF| = 0,857. C'est lui, et lui
# seul, qui fixe les predictions contre lesquelles le verdict est prononce.
# Recalculer les predictions avec l'alpha local reviendrait a deplacer la cible
# apres le tir. L'alpha local est mesure et publie, mais comme DIAGNOSTIC : son
# instabilite (0,12 en bas de grille, 3,24 au milieu, selon la duree choisie) est
# elle-meme un resultat — le modele « W ~ Delta_e^(-alpha) a alpha unique » ne
# tient pas sur ce dispositif.
ALPHA_PREENREGISTRE = 0.857

# (p, q) de chaque fonctionnelle, d'ou son exposant predit p - q*alpha.
FAMILLES = {
    'sup': (1, 0),
    'aire': (1, 1),
    'aire_delta_p': (1, 1),
    'S_max': (1, 1),
    'energie': (2, 1),
    'pente_max': (1, 0),
    'duree_sup_delta_p': (0, 1),
    'GLR': (2, 1),
    'MMD2': (2, 2),
    'ADWIN': None,              # cas particulier : 1 - alpha/2
}


def lisser(mat, L=L_LISSAGE):
    """Moyenne glissante causale de longueur L, sur chaque ligne."""
    noyau = np.ones(L) / L
    return np.apply_along_axis(lambda r: np.convolve(r, noyau, mode='valid'), 1, mat)


def fonctionnelles(error_mat, p0):
    """Toutes les fonctionnelles, par run. Aucune n'est un seuil : ce sont des mesures."""
    xi_brut = error_mat - p0[:, None]
    xi = lisser(error_mat) - p0[:, None]
    n = xi.shape[0]
    out = {}

    out['sup'] = xi.max(axis=1)
    out['aire'] = xi_brut.sum(axis=1)
    out['aire_delta_p'] = np.maximum(xi_brut - DELTA_P, 0).sum(axis=1)
    out['energie'] = (xi ** 2).sum(axis=1)
    # La difference PAS A PAS d'une moyenne glissante de longueur L sur une serie
    # binaire est bornee par 1/L, et vaut 1/L dans presque tous les runs : elle
    # sature, donne un exposant nul et ne mesure rien. La pente se prend donc sur
    # un ecart de L pas, ce qui en fait une vraie derivee de la courbe lissee.
    out['pente_max'] = (xi[:, L_LISSAGE:] - xi[:, :-L_LISSAGE]).max(axis=1) / L_LISSAGE
    out['duree_sup_delta_p'] = (xi > DELTA_P).sum(axis=1).astype(float)

    # S_max : forme de Lindley, la meme recurrence que analyse_QCD.py.
    s = np.zeros(n)
    s_max = np.zeros(n)
    for t in range(xi_brut.shape[1]):
        s = np.maximum(0.0, s + xi_brut[:, t] - DELTA_P)
        s_max = np.maximum(s_max, s)
    out['S_max'] = s_max

    # GLR fenetre : sup_n n * KL(p1_chapeau || p0). Contrairement au CUSUM, qui fixe
    # p1 d'avance, le GLR l'ESTIME sur la fenetre — d'ou une statistique quadratique
    # en l'ecart et non lineaire. C'est la prediction la plus falsifiable du volet.
    glr = np.zeros(n)
    mmd = np.zeros(n)
    cum = np.cumsum(np.concatenate([np.zeros((n, 1)), error_mat], axis=1), axis=1)
    for fin in range(min(FENETRES_GLR), H + 1, PAS_SCAN):
        for w in FENETRES_GLR:
            if fin - w < 0:
                continue
            p1 = (cum[:, fin] - cum[:, fin - w]) / w
            p0c = np.clip(p0, 1e-6, 1 - 1e-6)
            p1c = np.clip(p1, 1e-6, 1 - 1e-6)
            kl = (p1c * np.log(p1c / p0c) + (1 - p1c) * np.log((1 - p1c) / (1 - p0c)))
            glr = np.maximum(glr, w * kl)
            # MMD^2 a noyau lineaire sur une variable binaire : (p1 - p0)^2, moyenne
            # sur la fenetre — d'ou (p,q) = (2,2), donc condamne comme l'aire.
            mmd = np.maximum(mmd, (p1 - p0) ** 2 * w / H)
    out['GLR'] = glr
    out['MMD2'] = mmd

    # ADWIN : sa statistique de coupe normalisee vaut |delta_mu| / sqrt(2 sigma^2 / m),
    # donc croit en Delta_e * sqrt(W) et NON en Delta_e. C'est ce qui donne
    # 1 - alpha/2 au lieu de 1.
    adwin = np.zeros(n)
    for fin in range(100, H + 1, 25):
        for w in (50, 100, 200, 400):
            if fin - w < 0:
                continue
            p1 = (cum[:, fin] - cum[:, fin - w]) / w
            var = np.clip(p0 * (1 - p0), 1e-9, None)
            adwin = np.maximum(adwin, np.abs(p1 - p0) * np.sqrt(w) / np.sqrt(2 * var))
    out['ADWIN'] = adwin
    return out


def pente_log_log(x, y, seeds, rng, n_boot=N_BOOT):
    """Regression log-log et IC bootstrap APPARIE sur la graine.

    On reechantillonne la GRAINE, pas la paire (amplitude, run) : les amplitudes
    partagent leurs graines, et les traiter comme independantes surestimerait l'IC.
    """
    ok = (x > 0) & (y > 0) & np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 4:
        return np.nan, np.nan, np.nan
    lx, ly = np.log(x[ok]), np.log(y[ok])
    pente = float(np.polyfit(lx, ly, 1)[0])
    graines = np.unique(seeds[ok])
    vals = []
    s_ok = seeds[ok]
    for _ in range(n_boot):
        tir = rng.choice(graines, size=len(graines), replace=True)
        masque = np.concatenate([np.flatnonzero(s_ok == g) for g in tir])
        if len(masque) < 4:
            continue
        vals.append(np.polyfit(lx[masque], ly[masque], 1)[0])
    if not vals:
        return pente, np.nan, np.nan
    return pente, float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def main():
    rng = np.random.default_rng(SEED_BOOT)
    print("=" * 78)
    print("EXPOSANTS DES FONCTIONNELLES — hors ligne, sur les traces existantes")
    print("=" * 78)

    meta = pd.read_parquet(DATA / "QCD_runs_meta_full.parquet").sort_values('run_id')
    traces = pd.read_parquet(DATA / "QCD_traces_error_full.parquet")
    mat = (traces.pivot(index='run_id', columns='t', values='e')
           .reindex(meta['run_id'].to_numpy()).to_numpy(dtype=float))
    p0 = meta['p_hat_0'].to_numpy(dtype=float)
    print(f"[INFO] {mat.shape[0]} runs x {mat.shape[1]} pas | "
          f"{meta.delta_e.nunique()} amplitudes")

    F = fonctionnelles(mat, p0)
    # Graine ET tous les parametres de grille dans la table : une ligne qui ne les
    # porte pas n'est pas rejouable (regle du projet).
    df = meta[['run_id', 'delta_e', 'boundary_shift', 'seed',
               'baseline_window', 'p_hat_0']].copy()
    # `QCD_runs_meta_full` n'a pas de colonne n_models : la campagne est anterieure
    # a son ajout. M vaut 10 (valeur par defaut de exp_QCD_campagne.py, confirmee
    # par QCD_runs_meta_C1_M10 qui porte les memes graines).
    df['n_models'] = N_MODELS_DEFAUT
    df['L_lissage'] = L_LISSAGE
    df['delta_p'] = DELTA_P
    df['W_glr'] = W_GLR
    for k, v in F.items():
        df[k] = v

    # alpha local : exposant de la duree d'adaptation W ~ Delta_e^(-alpha).
    #
    # Il ne peut PAS se lire sur tau_ARF. Le volet 2 etablit lui-meme que tau_ARF
    # est non monotone (118 -> 346 -> 28) et qu'« aucune loi de puissance ne decrit
    # une cloche » : en tirer une pente log-log locale donne 0,12 en bas de grille,
    # ou l'ajustement de l'article annonce 0,98. On prend donc tau_swap(50 %), le
    # renouvellement de la moitie de la foret, qui est monotone. L'alpha issu de
    # tau_ARF est publie a cote, comme diagnostic de cet ecart.
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")[
        ['run_id', 'tau_arf', 'tau_swap_50']]
    df = df.merge(ind, on='run_id')

    amplitudes = np.sort(df.delta_e.unique())
    lignes = []
    for nom_seg, sl in SEGMENTS.items():
        amp_seg = amplitudes[sl]
        sous = df[df.delta_e.isin(amp_seg)]
        a_pente, _, _ = pente_log_log(sous.delta_e.to_numpy(),
                                      sous.tau_swap_50.to_numpy(),
                                      sous.seed.to_numpy(), rng, n_boot=200)
        alpha = -a_pente if np.isfinite(a_pente) else np.nan
        a_arf, _, _ = pente_log_log(sous.delta_e.to_numpy(), sous.tau_arf.to_numpy(),
                                    sous.seed.to_numpy(), rng, n_boot=200)
        # Etendue relative du segment en Delta_e : sous 10 %, une regression log-log
        # n'estime plus rien — le bruit en y est amplifie par l'etroitesse en x.
        # Les six dernieres cellules ne couvrent que 3,2 % : leurs exposants sont
        # calcules mais marques NON ESTIMABLES, et ne se citent pas.
        etendue = float(amp_seg.max() / amp_seg.min() - 1.0)
        estimable = etendue >= 0.10
        for fam, pq in FAMILLES.items():
            pente, lo, hi = pente_log_log(sous.delta_e.to_numpy(), sous[fam].to_numpy(),
                                          sous.seed.to_numpy(), rng)
            if pq is None:
                predit = 1 - ALPHA_PREENREGISTRE / 2
                predit_local = 1 - alpha / 2
            else:
                p, q = pq
                predit = p - q * ALPHA_PREENREGISTRE
                predit_local = p - q * alpha
            lignes.append({
                'segment': nom_seg, 'fonctionnelle': fam,
                'delta_e_min': float(amp_seg.min()), 'delta_e_max': float(amp_seg.max()),
                'alpha_local': float(alpha),
                'alpha_si_tau_arf': float(-a_arf) if np.isfinite(a_arf) else np.nan,
                'etendue_relative': etendue, 'estimable': bool(estimable),
                'exposant': pente,
                'ic_bas': lo, 'ic_haut': hi, 'exposant_predit': float(predit),
                'exposant_predit_alpha_local': float(predit_local),
                'accord': bool(estimable and np.isfinite(lo) and lo <= predit <= hi),
            })
    res = pd.DataFrame(lignes)
    res.to_parquet(DATA / "QCD_exposants_fonctionnelles.parquet", index=False)
    df.to_parquet(DATA / "QCD_fonctionnelles_par_run.parquet", index=False)

    for seg in SEGMENTS:
        s = res[res.segment == seg]
        a = s['alpha_local'].iloc[0]
        print(f"\nSEGMENT {seg.upper()} — Delta_e de {s.delta_e_min.iloc[0]:.3f} a "
              f"{s.delta_e_max.iloc[0]:.3f} (etendue {100 * s.etendue_relative.iloc[0]:.0f} %) "
              f"| alpha = {a:.3f} (sur tau_ARF il vaudrait "
              f"{s.alpha_si_tau_arf.iloc[0]:.3f})")
        if not s['estimable'].iloc[0]:
            print("  NON ESTIMABLE : l'etendue en Delta_e est inferieure a 10 %. "
                  "Les exposants ci-dessous\n  sont calcules pour memoire et ne se "
                  "citent pas — le bruit en y y est amplifie sans borne.")
        print(s[['fonctionnelle', 'exposant', 'ic_bas', 'ic_haut',
                 'exposant_predit', 'accord']]
              .to_string(index=False, float_format=lambda v: f"{v:+.3f}"))
        print("  (exposant_predit = prediction PRE-ENREGISTREE, alpha = "
              f"{ALPHA_PREENREGISTRE})")

    seuil_adwin(df, rng)
    glr_contre_cusum(mat, meta, rng)
    print(f"\n[SUCCESS] ecrit : QCD_exposants_fonctionnelles.parquet")


# ============================================================================ #
#  Tache 8 — le seuil critique d'ADWIN, en forme close
# ============================================================================ #
#
# La regle de coupe de river 0.23 est, litteralement (adwin_c.pyx:302-311) :
#     delta' = ln(2 * ln(width) / delta)
#     1/m    = 1/(n0 - 4) + 1/(n1 - 4)
#     eps    = sqrt(2 * (1/m) * var_W * delta') + (2/3) * delta' * (1/m)
#     coupe si |delta_mu| > eps,  avec delta = 0,002
#
# ADWIN teste TOUTES les coupes : la sous-fenetre recente isole le transitoire, il
# n'y a donc pas de dilution Delta_e * W / w. La condition s'ecrit
# Delta_e^2 * W > 2 sigma^2 delta', d'ou
#
#     Delta_e* = [ 2 p0 (1 - p0) ln(2 ln n / delta) / K ]^(1/(2 - alpha))
#
# C'est la forme close que l'article laisse aux travaux futurs.

DELTA_ADWIN = 0.002


def seuil_adwin(df, rng):
    """Delta_e* predit, et la frontiere effectivement observee entre les regimes."""
    print("\n" + "=" * 78)
    print("SEUIL CRITIQUE D'ADWIN — forme close, confrontee a la frontiere observee")
    print("=" * 78)
    ind = pd.read_parquet(DATA / "QCD_indicateurs_full.parquet")
    meta = pd.read_parquet(DATA / "QCD_runs_meta_full.parquet")
    p0 = float(meta['p_hat_0'].mean())
    n = H
    delta_prime = np.log(2 * np.log(n) / DELTA_ADWIN)

    # K : constante de la duree d'adaptation W = K * Delta_e^(-alpha), calibree sur
    # tau_swap(50 %) et non postulee.
    d = ind.dropna(subset=['tau_swap_50'])
    pente, ordonnee = np.polyfit(np.log(d.delta_e), np.log(d.tau_swap_50), 1)
    K = float(np.exp(ordonnee))
    alpha_obs = float(-pente)
    de_etoile = (2 * p0 * (1 - p0) * delta_prime / K) ** (1.0 / (2 - alpha_obs))
    # A alpha PRE-ENREGISTRE, K doit etre recalibre sous la meme contrainte : on ne
    # melange pas le K d'un ajustement libre avec l'alpha d'un autre.
    K_pre = float(np.exp(np.mean(np.log(d.tau_swap_50)
                                 + ALPHA_PREENREGISTRE * np.log(d.delta_e))))
    de_pre = (2 * p0 * (1 - p0) * delta_prime / K_pre) ** (1.0 / (2 - ALPHA_PREENREGISTRE))
    print(f"  p0 = {p0:.4f} | delta' = {delta_prime:.3f}")
    print(f"  ajustement libre      : alpha = {alpha_obs:.3f}, K = {K:.1f} "
          f"-> Delta_e* = {de_etoile:.4f}")
    print(f"  alpha PRE-ENREGISTRE  : alpha = {ALPHA_PREENREGISTRE}, K = {K_pre:.1f} "
          f"-> Delta_e* = {de_pre:.4f}")

    # Frontiere observee : premiere amplitude ou le taux de non-alarme decroche.
    taux = ind.groupby('delta_e')['censored_det_25'].mean()
    amplitudes = np.sort(ind.delta_e.unique())
    print(f"\n  taux de NON-alarme (lambda = 25) par amplitude :")
    print("   " + taux.head(6).round(3).to_string().replace(chr(10), chr(10) + "   "))
    sous = taux[taux < 0.95]
    frontiere = float(sous.index[0]) if len(sous) else np.nan
    print(f"\n  frontiere OBSERVEE (1re amplitude sous 95 % de non-alarme) : "
          f"{frontiere:.4f}")
    print(f"  la plus petite amplitude de la grille vaut {amplitudes[0]:.4f}, "
          f"la deuxieme {amplitudes[1]:.4f}")
    dans = [nom for nom, v in (('libre', de_etoile), ('pre-enregistre', de_pre))
            if amplitudes[0] <= v <= amplitudes[2]]
    if dans:
        print(f"  -> la transition tombe DANS la grille pour l'ajustement {', '.join(dans)}")
    else:
        print("  -> AUCUNE des deux formes closes ne place Delta_e* dans la grille.")
        print("     La forme close n'est donc PAS validee ici. L'exposant 1/(2 - alpha)")
        print("     amplifie tout ecart sur alpha : de 0,857 a 1,361, Delta_e* passe de")
        print(f"     {de_pre:.4f} a {de_etoile:.4f}, soit un facteur "
              f"{max(de_pre, de_etoile) / max(min(de_pre, de_etoile), 1e-12):.0f}.")
        print("     Le resultat a retenir est cette SENSIBILITE, pas une valeur de "
              "Delta_e*.")

    pd.DataFrame([{'p0': p0, 'delta_prime': delta_prime, 'K': K,
                   'alpha': alpha_obs, 'delta_e_etoile': de_etoile,
                   'K_preenregistre': K_pre, 'alpha_preenregistre': ALPHA_PREENREGISTRE,
                   'delta_e_etoile_preenregistre': de_pre,
                   'frontiere_observee': frontiere}]).to_parquet(
        DATA / "QCD_seuil_adwin.parquet", index=False)

    # Resultat connexe : a faible amplitude, le drift RETARDE le premier
    # remplacement. Mecanisme candidat : il augmente p, donc sigma^2 = p(1-p),
    # donc eps_cut ~ sigma — le seuil monte plus vite que le signal.
    try:
        mnd = pd.read_parquet(DATA / "QCD_runs_meta_A1_nodrift.parquet")
        evnd = pd.read_parquet(DATA / "QCD_events_swap_A1_nodrift.parquet")
        tau_nd = evnd.groupby('run_id')['t'].min().median()
        bas = ind[ind.delta_e == amplitudes[0]]['tau_arf'].median()
        print(f"\n  tau_ARF median : {bas:.0f} avec drift (Delta_e = {amplitudes[0]:.3f}) "
              f"contre {tau_nd:.0f} SANS drift")
        print(f"  -> a faible amplitude le drift RETARDE le premier remplacement "
              f"d'un facteur {bas / tau_nd:.2f}")
        eps = lambda p: np.sqrt(2 * p * (1 - p) * delta_prime / 50)
        print(f"  mecanisme : eps_cut ~ sigma. De p0 = {p0:.4f} a "
              f"p0 + Delta_e = {p0 + amplitudes[0]:.4f}, le seuil monte de "
              f"{100 * (eps(p0 + amplitudes[0]) / eps(p0) - 1):.0f} % quand le signal "
              f"monte de {100 * amplitudes[0] / p0:.0f} %")
    except FileNotFoundError:
        pass


# ============================================================================ #
#  Tache 9 — le GLR comme reparation minimale d'un moniteur cumulatif
# ============================================================================ #
#
# Un CUSUM a p1 FIXE est lineaire en e_t (exposant 1 - alpha). Un GLR qui ESTIME
# p1 est quadratique (2 - alpha). Prediction : le CUSUM plafonne quand l'amplitude
# croit, le GLR continue de croitre. Si le GLR plafonne aussi, la taxonomie tombe
# et c'est le resultat.
#
# Les deux sont calibres AU MEME TAUX DE FAUSSE ALARME sur la campagne b = 0 :
# sans cela, comparer leurs taux de detection n'a aucun sens.

FAUSSE_ALARME = 0.05


def delai_franchissement(mat, p0, cle, seuil):
    """Premier instant ou la statistique depasse le seuil. NaN si jamais.

    Une duree qui peut ne pas etre atteinte porte sa censure : elle est publiee
    avec le resultat, jamais retiree en silence.
    """
    n, T = mat.shape
    xi = mat - p0[:, None]
    out = np.full(n, np.nan)
    if cle == 'S_max':
        s = np.zeros(n)
        for t in range(T):
            s = np.maximum(0.0, s + xi[:, t] - DELTA_P)
            neuf = np.isnan(out) & (s > seuil)
            out[neuf] = t
    else:
        cum = np.cumsum(np.concatenate([np.zeros((n, 1)), mat], axis=1), axis=1)
        p0c = np.clip(p0, 1e-6, 1 - 1e-6)
        # Le CUSUM est scanne pas a pas ; scanner le GLR tous les PAS_SCAN pas lui
        # imposerait une resolution dix fois plus grossiere et un plancher egal a sa
        # plus petite fenetre. Comparer deux delais mesures a des resolutions
        # differentes n'a pas de sens : ici, resolution 1 pour les deux.
        for fin in range(min(FENETRES_GLR), T + 1, 1):
            for w in FENETRES_GLR:
                if fin - w < 0:
                    continue
                p1 = np.clip((cum[:, fin] - cum[:, fin - w]) / w, 1e-6, 1 - 1e-6)
                kl = p1 * np.log(p1 / p0c) + (1 - p1) * np.log((1 - p1) / (1 - p0c))
                neuf = np.isnan(out) & (w * kl > seuil)
                out[neuf] = fin
    return out


def glr_contre_cusum(mat_drift, meta_drift, rng):
    print("\n" + "=" * 78)
    print("GLR CONTRE CUSUM — a taux de fausse alarme egal (5 % sur b = 0)")
    print("=" * 78)
    m0 = pd.read_parquet(DATA / "QCD_runs_meta_A1_nodrift.parquet").sort_values('run_id')
    t0 = pd.read_parquet(DATA / "QCD_traces_error_A1_nodrift.parquet")
    mat0 = (t0.pivot(index='run_id', columns='t', values='e')
            .reindex(m0['run_id'].to_numpy()).to_numpy(dtype=float))
    p0_0 = m0['p_hat_0'].to_numpy(dtype=float)
    p0_d = meta_drift['p_hat_0'].to_numpy(dtype=float)

    F0 = fonctionnelles(mat0, p0_0)
    Fd = fonctionnelles(mat_drift, p0_d)

    lignes = []
    for nom, cle in (('CUSUM (p1 fixe)', 'S_max'), ('GLR (p1 estime)', 'GLR')):
        seuil = float(np.quantile(F0[cle], 1 - FAUSSE_ALARME))
        detect = pd.DataFrame({'delta_e': meta_drift['delta_e'].to_numpy(),
                               'stat': Fd[cle]})
        taux = detect.assign(alarme=detect.stat > seuil).groupby('delta_e')['alarme'].mean()
        for de, v in taux.items():
            lignes.append({'detecteur': nom, 'delta_e': de, 'taux_detection': float(v),
                           'seuil': seuil, 'fausse_alarme_cible': FAUSSE_ALARME})
        print(f"\n  {nom} — seuil calibre a {seuil:.4g}")
        print("   " + taux.round(3).to_string().replace(chr(10), chr(10) + "   "))

    # Le taux de detection sature a 1 des Delta_e = 0,14 : les deux detecteurs y
    # plafonnent MECANIQUEMENT, et comparer deux plafonds ne dit rien. On mesure
    # donc aussi le DELAI median de franchissement, qui lui ne sature pas.
    print("\n  Le taux de detection sature a 100 % des Delta_e ~ 0,14 pour les deux :")
    print("  a 5 % de fausse alarme, il ne discrimine que le BAS de grille. On")
    print("  compare donc aussi le delai de detection, non borne.")
    delais = []
    for nom, cle in (('CUSUM (p1 fixe)', 'S_max'), ('GLR (p1 estime)', 'GLR')):
        seuil = float(np.quantile(F0[cle], 1 - FAUSSE_ALARME))
        d_run = delai_franchissement(mat_drift, p0_d, cle, seuil)
        tmp = pd.DataFrame({'delta_e': meta_drift['delta_e'].to_numpy(), 'delai': d_run})
        for de, g in tmp.groupby('delta_e'):
            cens = float(np.isnan(g.delai).mean())
            # Une mediane calculee sur les seuls detectes exclut les plus lents : au
            # dela de 50 % de censure elle n'est pas definie et ne se publie pas.
            med = float(np.nanmedian(g.delai)) if cens <= 0.5 else np.nan
            delais.append({'detecteur': nom, 'delta_e': float(de),
                           'delai_median': med, 'censure': cens,
                           'plancher_maillage': float(min(FENETRES_GLR))
                           if nom.startswith('GLR') else 1.0})
    dl = pd.DataFrame(delais)
    dl.to_parquet(DATA / "QCD_glr_cusum_delais.parquet", index=False)
    pv = dl.pivot(index='delta_e', columns='detecteur', values='delai_median')
    print("\n  delai median de detection (NaN = jamais atteint) :")
    print("   " + pv.round(1).to_string().replace(chr(10), chr(10) + "   "))
    cens = dl.pivot(index='delta_e', columns='detecteur', values='censure')
    print("\n  taux de censure (jamais detecte) :")
    print("   " + cens.round(3).head(3).to_string().replace(chr(10), chr(10) + "   "))

    res = pd.DataFrame(lignes)
    res.to_parquet(DATA / "QCD_glr_contre_cusum.parquet", index=False)
    piv = res.pivot(index='delta_e', columns='detecteur', values='taux_detection')
    print("\n  taux de detection compares :")
    print("   " + piv.round(3).to_string().replace(chr(10), chr(10) + "   "))
    croit = lambda c: float(piv[c].iloc[-1] - piv[c].iloc[len(piv) // 2])
    print(f"\n  progression du haut de grille (2e moitie) : "
          f"CUSUM {croit('CUSUM (p1 fixe)'):+.3f} | GLR {croit('GLR (p1 estime)'):+.3f}")


if __name__ == "__main__":
    main()
