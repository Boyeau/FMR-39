"""Le temoin NoDrift est-il deja meilleur AVANT la rupture ?

Si oui, la comparaison post-drift est biaisee : la foret normale a remplace des arbres
pendant le rodage (par bruit), elle arrive donc a tau* avec des arbres jeunes, tandis
que le temoin garde 10 arbres matures ayant vu 4000 exemples.
"""
import copy, random, warnings, numpy as np
from joblib import Parallel, delayed
from river import drift
from river.forest import ARFClassifier
warnings.filterwarnings('ignore')
T_DRIFT, H, M = 4000, 800, 10

def run(b, seed):
    ss=int(seed); random.seed(ss); np.random.seed(ss); rng=np.random.default_rng(ss)
    mk=lambda d: ARFClassifier(n_models=M, seed=ss, drift_detector=d, warning_detector=copy.deepcopy(d))
    arf, tem = mk(drift.ADWIN(clock=1)), mk(drift.NoDrift())
    pre_n=[]; pre_t=[]; post_n=[]; post_t=[]
    for t in range(T_DRIFT+H):
        x0,x1=rng.normal(),rng.normal(); x={0:x0,1:x1}
        y=int(x0+x1>0.0) if t<T_DRIFT else int(x0+x1>b)
        en=int((arf.predict_one(x) or 0)!=y); et=int((tem.predict_one(x) or 0)!=y)
        if T_DRIFT-1000<=t<T_DRIFT: pre_n.append(en); pre_t.append(et)
        elif t>=T_DRIFT: post_n.append(en); post_t.append(et)
        arf.learn_one(x,y); tem.learn_one(x,y)
    swaps=sum(arf._drift_tracker.values())
    return np.mean(pre_n),np.mean(pre_t),np.mean(post_n),np.mean(post_t),swaps

if __name__=="__main__":
    for b,lab in ((4.0,'drift fort'),(0.0,'AUCUN drift')):
        r=np.array(Parallel(n_jobs=-1)(delayed(run)(b,s) for s in range(1,13)))
        print("=== %s (b=%.1f), 12 executions ==="%(lab,b))
        print("  AVANT la rupture  : normale %.4f | temoin %.4f | ecart %+.4f"%(r[:,0].mean(),r[:,1].mean(),r[:,1].mean()-r[:,0].mean()))
        print("  APRES la rupture  : normale %.4f | temoin %.4f | ecart %+.4f"%(r[:,2].mean(),r[:,3].mean(),r[:,3].mean()-r[:,2].mean()))
        print("  remplacements cumules dans la foret normale : %.1f"%r[:,4].mean())
        print()
