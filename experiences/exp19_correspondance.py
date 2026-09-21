"""TEST-19 : correspondance. Injection -> 0 = retour au témoin (limite classique)."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import condensateur as Q

fond_pts = C.fond(seed=24)
P_ref = C.p_sig(fond_pts)
gouttes = Q.injecter(np.zeros((0, 3)), Q.charge(2048, seed=101), 16, seed=7)
finaux = {}
for niv in (0, 2, 4):
    pts = fond_pts.copy()
    for t in range(4):
        if niv:
            pts = np.vstack([pts, gouttes[t * niv:(t + 1) * niv]])
    finaux[str(niv)] = round(C.p_sig(pts) / P_ref, 4)
    print(f"[19] injection={niv}/pas -> P_final={finaux[str(niv)]}", flush=True)
vals = [finaux["0"], finaux["2"], finaux["4"]]
res = {"P_finaux": finaux,
       "limite_temoin": bool(abs(vals[0] - 1.0) < 0.1),
       "monotone": bool(vals[0] <= vals[1] <= vals[2])}
json.dump(res, open(os.path.join(HERE, "resultats", "exp19.json"), "w"), indent=1)
print(f"[19] RESULTAT limite={res['limite_temoin']} monotone={res['monotone']}")
