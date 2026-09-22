"""TEST-38 : ligne invisible sous volatilité Q native. M22 (seuil sha256,
alpha=0.12, T=20) + jitter 0.04 indépendant par région à chaque pas. 30+30.
Critère : partage>=20 ET partage-indep>=10 (la capsule survit au bruit)."""
import hashlib
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import porteurs as P

T = 20


def phic(msg: bytes) -> float:
    h = int(hashlib.sha256(msg).hexdigest(), 16)
    return 100 + 1900 * ((h % 1000) / 1000)


def etape_focale(seuil, cible, seed_jit):
    rng = np.random.default_rng(seed_jit)
    port = P.creer_porteurs(2048, 8, "I", seed=3)
    for p in port:
        p.position += np.array(cible, float)
    for t in range(T):
        P.transporter(port, cible, 0.12)
        for p in port:
            p.position += rng.normal(0, 0.04, 3)
        if P.concentration(port, t + 1) >= seuil:
            return t + 1
    return None


def msg(graine):
    return np.random.default_rng(graine).integers(0, 2, 2048).astype(
        np.uint8).tobytes()


part, indep = 0, 0
for i in range(30):
    m = msg(500 + i)
    sA = etape_focale(phic(m), [0, 0, 0], 3800 + i)
    sB = etape_focale(phic(m), [6, 0, 0], 3900 + i)
    part += (sA == sB)
    sB2 = etape_focale(phic(msg(9000 + i)), [6, 0, 0], 3900 + i)
    indep += (sA == sB2)
res = {"partage": f"{part}/30", "indep": f"{indep}/30",
       "separation": part - indep,
       "reference_sans_bruit": {"partage": "30/30", "indep": "10/30"},
       "critere": bool(part >= 20 and (part - indep) >= 10)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp38.json"), "w"), indent=1)
print(f"[38] RESULTAT partage={part}/30 indep={indep}/30 "
      f"separation={part - indep} critere={res['critere']}")
