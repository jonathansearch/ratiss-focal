"""TEST-21 (04b) : lissage RESTREINT. On ne lisse que l'injecté, JAMAIS le fond natif.
Critère : érosion du fond < 0.02 (F1 : stopper l'hémorragie de -10 %)."""
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
N_FOND = len(fond_pts)
P_ref = C.p_sig(fond_pts)
bits = Q.charge(cfg["n_bits"], seed=cfg["graine_info"])
gouttes = Q.injecter(np.zeros((0, 3)), bits, cfg["filet"] * T,
                      seed=cfg["graine_injection"])
port = P.creer_porteurs(cfg["n_bits"], cfg["n_porteurs"], "I",
                        seed=cfg["graine_porteurs"])
pts, serie, focal = fond_pts.copy(), [], None
for t in range(T):
    pts = np.vstack([pts, gouttes[t * cfg["filet"]:(t + 1) * cfg["filet"]]])
    d2 = ((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1)
    voisins = np.argsort(d2, axis=1)[:, 1:4]
    masque = np.zeros(len(pts), bool)  # MASQUE : injecté seul (indices >= fond)
    masque[N_FOND:] = True
    depl = np.zeros_like(pts)
    depl[masque] = cfg["lissage"] * (pts[voisins[masque]].mean(1) - pts[masque])
    pts = pts + depl
    P.transporter(port, cfg["point_focal"], cfg["alpha_transport"])
    if focal is None and P.concentration(port, t + 1) >= cfg["phi_c"]:
        focal = t + 1
        pts = np.vstack([pts, C.boucle_focale(cfg["point_focal"])])
    serie.append(C.p_sig(pts) / P_ref)
    print(f"[21] pas {t + 1:02d} P/P_ref={serie[-1]:.4f}", flush=True)
erosion = abs(C.p_sig(pts[:N_FOND]) / P_ref - 1.0)
res = {"univers": "A-durci",
       "serie_P_normee": [round(float(x), 4) for x in serie],
       "focalisation_etape": focal,
       "delta_P_global": round(float(serie[-1] - 1.0), 4),
       "erosion_fond": round(float(erosion), 4),
       "critere_erosion_moins_002": bool(erosion < 0.02)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp21.json"), "w"), indent=1)
print(f"[21] RESULTAT erosion={erosion:.4f} critere={res['critere_erosion_moins_002']}")
