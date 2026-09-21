"""TEST-04 : univers A (émergence). R7: python3 experiences/exp04_univers_A.py"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import condensateur as Q
import porteurs as P

cfg = json.load(open(os.path.join(os.path.dirname(HERE), "univers", "A.json")))
T = cfg["T"]
fond_pts = C.fond(seed=cfg["graine_fond"])
P_ref = C.p_sig(fond_pts)
bits = Q.charge(cfg["n_bits"], seed=cfg["graine_info"])
gouttes = Q.injecter(np.zeros((0, 3)), bits, cfg["filet"] * T,
                      seed=cfg["graine_injection"])
port = P.creer_porteurs(cfg["n_bits"], cfg["n_porteurs"], "I",
                        seed=cfg["graine_porteurs"])
pts, serie, phis, focal = fond_pts.copy(), [], [], None
for t in range(T):
    pts = np.vstack([pts, gouttes[t * cfg["filet"]:(t + 1) * cfg["filet"]]])
    d2 = ((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1)
    voisins = np.argsort(d2, axis=1)[:, 1:4]
    pts = pts + cfg["lissage"] * (pts[voisins].mean(1) - pts)
    P.transporter(port, cfg["point_focal"], cfg["alpha_transport"])
    phis.append(P.concentration(port, t + 1))
    if focal is None and phis[-1] >= cfg["phi_c"]:
        focal = t + 1
        pts = np.vstack([pts, C.boucle_focale(cfg["point_focal"])])
    serie.append(C.p_sig(pts) / P_ref)
    print(f"[04] pas {t + 1:02d} P/P_ref={serie[-1]:.4f} phi={phis[-1]:.1f}", flush=True)
res = {"univers": "A-émergence",
       "serie_P_normee": [round(float(x), 4) for x in serie],
       "focalisation_etape": focal,
       "delta_P": round(float(serie[-1] - 1.0), 4)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp04.json"), "w"), indent=1)
print(f"[04] RESULTAT focalisation={focal} delta_P={res['delta_P']}")
