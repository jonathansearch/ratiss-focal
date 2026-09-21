"""TEST-18 : H2' (kappa = f(D, I)). Grille distance x interaction -> carte de R."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

rng = np.random.default_rng(18)
fond_pts = C.fond(seed=24)
P_ref = C.p_sig(fond_pts)
table = {}
for D in (1.6, 2.6, 3.6):
    for I_ in (4, 8, 16):
        rs = []
        for _ in range(2):
            ang = rng.uniform(0, 2 * np.pi, I_)
            inj = np.column_stack([D * np.cos(ang), D * np.sin(ang),
                                   rng.normal(0, 0.1, I_)])
            rs.append(C.p_sig(np.vstack([fond_pts, inj])) / P_ref)
        table[f"D={D}_I={I_}"] = round(float(np.mean(rs)), 4)
        print(f"[18] D={D} I={I_} R={table[f'D={D}_I={I_}']}", flush=True)
bascule = any(v < 0.9 for v in table.values())
res = {"table_R": table, "bascule_observee": bool(bascule)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp18.json"), "w"), indent=1)
print(f"[18] RESULTAT bascule={bascule}")
