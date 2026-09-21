"""TEST-17 : F0 (focalisation dynamique). Entretenu vs abandonné sous fort bruit."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

rng = np.random.default_rng(17)
base = np.vstack([C.fond(seed=24), C.boucle_focale([0, 0, 0])])
P0 = C.p_sig(base)
T, SIG = 8, 0.06
ent, aba = base.copy(), base.copy()
se, sa = [], []
for t in range(T):
    ent = ent + rng.normal(0, SIG, ent.shape)
    ent = np.vstack([ent, C.boucle_focale([0, 0, 0])])  # entretien : on réinjecte
    aba = aba + rng.normal(0, SIG, aba.shape)           # abandonné : dérive
    se.append(C.p_sig(ent) / P0)
    sa.append(C.p_sig(aba) / P0)
    print(f"[17] pas {t + 1} entretenu={se[-1]:.3f} abandonné={sa[-1]:.3f}", flush=True)
res = {"entretenu_final": round(se[-1], 4), "abandonne_final": round(sa[-1], 4),
       "cout_bits": T * 10 * 3 * 8,
       "F0_tient": bool(se[-1] > 0.7 and se[-1] > sa[-1])}
json.dump(res, open(os.path.join(HERE, "resultats", "exp17.json"), "w"), indent=1)
print(f"[17] RESULTAT F0_tient={res['F0_tient']} cout={res['cout_bits']} bits")
