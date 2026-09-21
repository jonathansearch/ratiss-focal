"""TEST-14 : secteurs S_i. Une seule loi ne suffit pas, il faut une loi par couche."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import condensateur as Q
import couches as L

T = 8
fond_pts = C.fond(seed=24)
bits = Q.charge(2048, seed=101)
gouttes = Q.injecter(np.zeros((0, 3)), bits, 60, seed=7)
apports = {"macro": [2] * T, "micro": [6, 3, 1, 1, 0, 0, 0, 0], "info": [0] * T}
nuages = {"macro": fond_pts[:160].copy(), "micro": fond_pts[160:250].copy(),
          "info": gouttes[:8].copy()}
gi = 8
series = {"macro": [], "micro": [], "info": []}
for t in range(T):
    for k in ("macro", "micro"):
        n = apports[k][t]
        if n:
            nuages[k] = np.vstack([nuages[k], gouttes[gi:gi + n]])
            gi += n
    for k in series:
        series[k].append(L.p_couche(nuages[k]))
    print(f"[14] pas {t} " + " ".join(f"{k}={series[k][-1]:.3f}" for k in series),
          flush=True)


def residus(x, y):
    a, b = np.polyfit(x, y, 1)
    return float(((np.array(y) - (a * np.array(x) + b)) ** 2).sum())


x = list(range(T))
r_global = residus(x * 3, series["macro"] + series["micro"] + series["info"])
r_sect = sum(residus(x, series[k]) for k in series)
ratio = round(r_sect / max(r_global, 1e-9), 3)
res = {"residu_global": round(r_global, 4), "residu_secteurs": round(r_sect, 4),
       "ratio": ratio, "secteurs_requis": bool(ratio < 0.5)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp14.json"), "w"), indent=1)
print(f"[14] RESULTAT ratio={ratio} secteurs_requis={res['secteurs_requis']}")
