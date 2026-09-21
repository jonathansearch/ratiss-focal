"""TEST-07 : unification en un univers virtuel cohérent. R7: python3 experiences/exp07_unification.py"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RACINE, "organes"))
import conteneur as C
import condensateur as Q
import porteurs as P

R = lambda n: json.load(open(os.path.join(HERE, "resultats", n)))
e1, e3, e6 = R("exp01.json"), R("exp03.json"), R("exp06.json")

unifie = {
    "nom": "Univers-Unifié-v1",
    "constantes_mesurees": {
        "P_ref": e1["P_ref"], "phi_c_lab": 500.0,
        "franchissement_I_etape": e3["types"]["I"]["franchissement_etape"],
        "franchissement_S_etape": e3["types"]["S"]["franchissement_etape"]},
    "mecanismes_valides": ["fond", "filet_info", "transport", "seuil_focalisation"],
    "verdict_origine": e6["verdict"],
    "graines": {"fond": 24, "info": 101, "injection": 7, "porteurs": 3},
    "T": 12}
json.dump(unifie, open(os.path.join(RACINE, "univers", "unifie.json"), "w"), indent=1)

fond_pts = C.fond(seed=24)
P_ref = e1["P_ref"]
bits = Q.charge(2048, seed=101)
gouttes = Q.injecter(np.zeros((0, 3)), bits, 48, seed=7)
port = P.creer_porteurs(2048, 8, "I", seed=3)
pts, serie, focal = fond_pts.copy(), [], None
for t in range(12):
    pts = np.vstack([pts, gouttes[t * 4:(t + 1) * 4]])
    P.transporter(port, [0, 0, 0], 0.25)
    if focal is None and P.concentration(port, t + 1) >= 500.0:
        focal = t + 1
        pts = np.vstack([pts, C.boucle_focale([0, 0, 0])])
    serie.append(C.p_sig(pts) / P_ref)
    print(f"[07] pas {t + 1:02d} P/P_ref={serie[-1]:.4f}", flush=True)
serie = np.array(serie)
coherent = bool(focal is not None and serie[-1] > 1.0 and serie.min() > 0.5)
res = {"univers": "Unifié-v1",
       "serie_P_normee": [round(float(x), 4) for x in serie],
       "focalisation_etape": focal, "coherent": coherent}
json.dump(res, open(os.path.join(HERE, "resultats", "exp07.json"), "w"), indent=1)
print(f"[07] RESULTAT focalisation={focal} coherent={coherent}")
