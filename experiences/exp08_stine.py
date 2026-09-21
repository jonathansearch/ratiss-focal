"""TEST-08 : Stine-24, loi accompagnatrice. Psi_sync -> 1 = couches accordées."""
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
rng = np.random.default_rng(8)
fond_pts = C.fond(seed=24)
bits = Q.charge(2048, seed=101)
gouttes = Q.injecter(np.zeros((0, 3)), bits, 4 * (T + 1), seed=7)
drips = gouttes[:4].copy()
series = {"macro": [], "micro": [], "info": []}
dims = []
for t in range(T + 1):
    if t > 0:
        drips = np.vstack([drips, gouttes[t * 4:(t + 1) * 4]])
    pts = np.vstack([fond_pts + rng.normal(0, 0.008, fond_pts.shape), drips])
    couches = L.decouper(pts)
    for k in series:
        series[k].append(L.p_couche(couches[k]))
    dims.append(L.dim_boites(pts))
    print(f"[08] pas {t} macro={series['macro'][-1]:.3f} "
          f"micro={series['micro'][-1]:.3f} info={series['info'][-1]:.3f} "
          f"D={dims[-1]:.3f}", flush=True)
P = np.array([series["macro"], series["micro"], series["info"]])
shares = P / P.sum(0)
f = 1 - np.minimum(np.abs(shares - shares[:, [0]]), 1)
psi = (f[0] * f[1] * f[2]) ** (1 / 3)
res = {"series": {k: [round(float(x), 4) for x in v] for k, v in series.items()},
       "dims": [round(float(x), 4) for x in dims],
       "psi": [round(float(x), 4) for x in psi],
       "psi_final": round(float(psi[-1]), 4),
       "aligne": bool(psi[-1] > 0.8)}
os.makedirs(os.path.join(HERE, "resultats"), exist_ok=True)
json.dump(res, open(os.path.join(HERE, "resultats", "exp08.json"), "w"), indent=1)
print(f"[08] RESULTAT psi_final={res['psi_final']} aligne={res['aligne']}")
