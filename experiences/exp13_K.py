"""TEST-13 : séparateur K (global/individuel). K(L) = 1 - P_L/P_joint."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import condensateur as Q
import couches as L

fond_pts = C.fond(seed=24)
charge = Q.injecter(fond_pts, Q.charge(2048, seed=101), 40, seed=7)
joint = C.p_sig(charge)
K = {k: round(1 - L.p_couche(v) / joint, 4)
     for k, v in L.decouper(charge).items()}
res = {"P_joint": round(joint, 4), "K": K,
       "sain": bool(all(0.0 <= x <= 1.0 for x in K.values()))}
json.dump(res, open(os.path.join(HERE, "resultats", "exp13.json"), "w"), indent=1)
print(f"[13] RESULTAT K={K} sain={res['sain']}")
