"""TEST-45 : ligne invisible (U4) sous choc plastique. Appareil TEST-38
(M22, jitter 0.04, mêmes graines/messages) + fenêtre choc aux pas 11-13
(transport inversé alpha=-0.12, jitter x10) + 20 pas relâche (T=33).
30 partagé + 30 indépendant. Classification : SANCTUAIRE (barre TEST-38
tenue : part>=20 et sép>=10) / SATELLITE (10<=part<20) / EFFONDREE
(part<10). Critère : SANCTUAIRE (U survit au choc)."""
import hashlib
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import porteurs as P

T = 33


def phic(msg: bytes) -> float:
    h = int(hashlib.sha256(msg).hexdigest(), 16)
    return 100 + 1900 * ((h % 1000) / 1000)


def etape_choc(seuil, cible, seed_jit):
    rng = np.random.default_rng(seed_jit)
    port = P.creer_porteurs(2048, 8, "I", seed=3)
    for p in port:
        p.position += np.array(cible, float)
    for t in range(T):
        if 10 <= t <= 12:
            P.transporter(port, cible, -0.12)
            jit = 0.4
        else:
            P.transporter(port, cible, 0.12)
            jit = 0.04
        for p in port:
            p.position += rng.normal(0, jit, 3)
        if P.concentration(port, t + 1) >= seuil:
            return t + 1
    return None


def msg(graine):
    return np.random.default_rng(graine).integers(0, 2, 2048).astype(
        np.uint8).tobytes()


part, indep = 0, 0
for i in range(30):
    m = msg(500 + i)
    sA = etape_choc(phic(m), [0, 0, 0], 3800 + i)
    sB = etape_choc(phic(m), [6, 0, 0], 3900 + i)
    part += (sA == sB)
    sB2 = etape_choc(phic(msg(9000 + i)), [6, 0, 0], 3900 + i)
    indep += (sA == sB2)
    if (i + 1) % 10 == 0:
        print(f"[45] ... {i + 1}/30", flush=True)
sep = part - indep
if part >= 20 and sep >= 10:
    classe = "SANCTUAIRE"
elif part >= 10:
    classe = "SATELLITE"
else:
    classe = "EFFONDREE"
res = {"partage": f"{part}/30", "indep": f"{indep}/30", "separation": sep,
       "reference_TEST38": {"partage": "28/30", "indep": "9/30"},
       "classe": classe, "critere": bool(classe == "SANCTUAIRE")}
json.dump(res, open(os.path.join(HERE, "resultats", "exp45.json"), "w"), indent=1)
print(f"[45] RESULTAT partage={part}/30 indep={indep}/30 separation={sep} "
      f"classe={classe} critere={res['critere']}")
