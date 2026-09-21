"""TEST-24 (H2'-bis) : grille resserrée D x I (zone du pont), 3 tirages/cellule.
Bascule formelle : |R-1| > 0.03 avec 1 hors [R-2s, R+2s]. Sinon réfutée dans la plage."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

rng = np.random.default_rng(24)
fond_pts = C.fond(seed=24)
P_ref = C.p_sig(fond_pts)
moy, ect = {}, {}
for D in (1.8, 2.0, 2.2, 2.4, 2.6):
    for I_ in (4, 8, 12, 16, 20):
        rs = []
        for _ in range(3):
            ang = rng.uniform(0, 2 * np.pi, I_)
            inj = np.column_stack([D * np.cos(ang), D * np.sin(ang),
                                   rng.normal(0, 0.1, I_)])
            rs.append(C.p_sig(np.vstack([fond_pts, inj])) / P_ref)
        moy[f"D={D}_I={I_}"] = round(float(np.mean(rs)), 4)
        ect[f"D={D}_I={I_}"] = round(float(np.std(rs)), 4)
        print(f"[24] D={D} I={I_} R={moy[f'D={D}_I={I_}']} ± {ect[f'D={D}_I={I_}']}",
              flush=True)
trouvees = [k for k in moy
            if abs(moy[k] - 1.0) > 0.03
            and not (moy[k] - 2 * ect[k] <= 1.0 <= moy[k] + 2 * ect[k])]
res = {"R_moyens": moy, "R_ecarts": ect,
       "bascule_detectee": bool(trouvees), "cellules": trouvees,
       "verdict": ("BASCULE détectée en " + ",".join(trouvees)) if trouvees
       else "RÉFUTÉE formellement dans D∈[1.8,2.6], I∈[4,20] (R≈1 partout)"}
json.dump(res, open(os.path.join(HERE, "resultats", "exp24.json"), "w"), indent=1)
print(f"[24] RESULTAT {res['verdict']}")
