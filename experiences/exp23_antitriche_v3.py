"""TEST-23 : anti-triche V3. Diagrammes de persistance COMPLETS (plus les séries).
Marge statistique : 3 graines. Critère : ratio moyen > 2.5."""
import json
import os
import sys
import zlib
import numpy as np
from ripser import ripser

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import condensateur as Q
import porteurs as P

cfg = json.load(open(os.path.join(os.path.dirname(HERE), "univers", "A.json")))
T = cfg["T"]
N_FOND = 250
ratios = {}
for graine_inj in (7, 77, 777):
    fond_pts = C.fond(seed=24)
    bits = Q.charge(2048, seed=101)
    gouttes = Q.injecter(np.zeros((0, 3)), bits, cfg["filet"] * T, seed=graine_inj)
    port = P.creer_porteurs(2048, 8, "I", seed=3)
    pts, dossier, focal = fond_pts.copy(), [], None
    for t in range(T):
        pts = np.vstack([pts, gouttes[t * cfg["filet"]:(t + 1) * cfg["filet"]]])
        d2 = ((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1)
        voisins = np.argsort(d2, axis=1)[:, 1:4]
        masque = np.zeros(len(pts), bool)
        masque[N_FOND:] = True
        depl = np.zeros_like(pts)
        depl[masque] = cfg["lissage"] * (pts[voisins[masque]].mean(1) - pts[masque])
        pts = pts + depl
        P.transporter(port, cfg["point_focal"], cfg["alpha_transport"])
        if focal is None and P.concentration(port, t + 1) >= cfg["phi_c"]:
            focal = t + 1
            pts = np.vstack([pts, C.boucle_focale(cfg["point_focal"])])
        dgms = ripser(pts, maxdim=2)["dgms"]
        paires = []
        for d in (1, 2):
            if d < len(dgms):
                for n, m in dgms[d]:
                    mf = "inf" if not np.isfinite(m) else f"{m:.4f}"
                    paires.append(f"{n:.4f},{mf}")
        dossier.append(f"H1H2@{t}:" + ";".join(paires))
    json.dump(dossier, open(os.path.join(
        HERE, "resultats", f"diagrammes_A_v3_g{graine_inj}.json"), "w"))
    regles = (f"fond+filet4+lissage_restraint.03+transport.25+seuil500"
              f"|graines24-101-{graine_inj}-3")
    blob = "|".join(dossier).encode()
    ratios[str(graine_inj)] = round(len(zlib.compress(blob, 9))
                                    / len(zlib.compress(regles.encode(), 9)), 2)
    print(f"[23] graine {graine_inj}: ratio={ratios[str(graine_inj)]} "
          f"(dossier brut {len(blob)} o)", flush=True)
vals = list(ratios.values())
res = {"ratios": ratios, "moyenne": round(float(np.mean(vals)), 2),
       "ecart_type": round(float(np.std(vals)), 2),
       "critere_ratio_moy_sup_2_5": bool(np.mean(vals) > 2.5)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp23.json"), "w"), indent=1)
print(f"[23] RESULTAT moyenne={res['moyenne']} ± {res['ecart_type']} "
      f"critere={res['critere_ratio_moy_sup_2_5']}")
