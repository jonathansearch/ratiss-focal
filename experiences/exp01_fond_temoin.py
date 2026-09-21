"""TEST-01 : fond + témoin. Le conteneur tient ? R7: python3 experiences/exp01_fond_temoin.py"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

SEED, T = 24, 12
rng = np.random.default_rng(SEED)
fond_pts = C.fond(seed=SEED)
P_ref = C.p_sig(fond_pts)
print(f"[01] P_ref (fond seul) = {P_ref:.4f}", flush=True)
serie = []
for t in range(T):
    pts = fond_pts + rng.normal(0, 0.008, fond_pts.shape)
    serie.append(C.p_sig(pts) / P_ref)
    print(f"[01] pas {t + 1:02d} P/P_ref = {serie[-1]:.4f}", flush=True)
serie = np.array(serie)
res = {"P_ref": P_ref, "serie_normee": [round(float(x), 4) for x in serie],
       "moyenne": round(float(serie.mean()), 4), "ecart_type": round(float(serie.std()), 4),
       "stable": bool(serie.std() < 0.15 * serie.mean()),
       "graine": SEED, "criterion": "ecart < 15%"}
os.makedirs(os.path.join(HERE, "resultats"), exist_ok=True)
json.dump(res, open(os.path.join(HERE, "resultats", "exp01.json"), "w"), indent=1)
print(f"[01] RESULTAT stable={res['stable']} moyenne={res['moyenne']} ecart={res['ecart_type']}")
