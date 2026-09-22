"""TEST-76 : singularité vs sanctuaire U. Ligne TEST-38 (T=20, mêmes
graines/messages), région A propre, région B trouée : singularité en
[6,0,0], r_cap=1.0 — porteur dedans = kick N(0,1.0) par pas
(spaghettification). 30 partagé + 30 indépendant. Classes : TIENT
(barre TEST-38 : part>=20 et sép>=10) / ÉRODÉ (part>=10 sinon) /
ROMPU (part<10). Critère : TIENT (U survit au trou noir local)."""
import hashlib
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import porteurs as P


def phic(msg: bytes) -> float:
    h = int(hashlib.sha256(msg).hexdigest(), 16)
    return 100 + 1900 * ((h % 1000) / 1000)


def etape(seuil, cible, seed_jit, trou):
    rng = np.random.default_rng(seed_jit)
    port = P.creer_porteurs(2048, 8, "I", seed=3)
    for p in port:
        p.position += np.array(cible, float)
    cb = np.array([6, 0, 0], float)
    for t in range(20):
        P.transporter(port, cible, 0.12)
        for p in port:
            p.position += rng.normal(0, 0.04, 3)
            if trou and np.linalg.norm(p.position - cb) < 1.0:
                p.position += rng.normal(0, 1.0, 3)
        if P.concentration(port, t + 1) >= seuil:
            return t + 1
    return None


def msg(graine):
    return np.random.default_rng(graine).integers(0, 2, 2048).astype(
        np.uint8).tobytes()


part, indep = 0, 0
for i in range(30):
    m = msg(500 + i)
    sA = etape(phic(m), [0, 0, 0], 3800 + i, False)
    sB = etape(phic(m), [6, 0, 0], 3900 + i, True)
    part += (sA == sB)
    sB2 = etape(phic(msg(9000 + i)), [6, 0, 0], 3900 + i, True)
    indep += (sA == sB2)
sep = part - indep
if part >= 20 and sep >= 10:
    classe = "TIENT"
elif part >= 10:
    classe = "ÉRODÉ"
else:
    classe = "ROMPU"
res = {"partage": f"{part}/30", "indep": f"{indep}/30", "separation": sep,
       "reference_TEST38": "28/30 vs 9/30",
       "classe": classe, "critere": bool(classe == "TIENT")}
json.dump(res, open(os.path.join(HERE, "resultats", "exp76.json"), "w"), indent=1)
print(f"[76] RESULTAT partage={part}/30 indep={indep}/30 sep={sep} "
      f"classe={classe} critere={res['critere']}")
