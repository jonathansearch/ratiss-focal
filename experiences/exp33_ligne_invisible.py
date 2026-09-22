"""TEST-33 (M22) : ligne invisible, seuil UNIFORME. Phi_c = 100 + 1900 x u où
u = sha256(message) mod 1000 / 1000 (tirage uniforme du contenu). Les clés
brutes se concentraient à 0.5 (binomial) -> pas trop grumeleux. Même géométrie
relative (cibles A=0 / B=6 disjointes), alpha=0.12, T=20. 30+30 essais.
Critère : 30/30 ET proportion indep < 0.5."""
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


def etape_focale(seuil, cible):
    port = P.creer_porteurs(2048, 8, "I", seed=3)
    for p in port:
        p.position += np.array(cible, float)
    for t in range(T):
        P.transporter(port, cible, 0.12)
        if P.concentration(port, t + 1) >= seuil:
            return t + 1
    return None


def msg(graine):
    return np.random.default_rng(graine).integers(0, 2, 2048).astype(
        np.uint8).tobytes()


part, indep = 0, 0
dstep, steps_p, steps_i = [], [], []
for i in range(30):
    m = msg(500 + i)
    sA, sB = etape_focale(phic(m), [0, 0, 0]), etape_focale(phic(m), [6, 0, 0])
    part += (sA == sB)
    steps_p.append(sA)
    sB2 = etape_focale(phic(msg(9000 + i)), [6, 0, 0])
    indep += (sA == sB2)
    steps_i.append([sA, sB2])
    if sA is not None and sB2 is not None:
        dstep.append(abs(sA - sB2))
prop = indep / 30
res = {"partage_coincidences": f"{part}/30",
       "indep_coincidences": f"{indep}/30",
       "indep_proportion": round(prop, 3),
       "indep_ecart_moyen": round(float(np.mean(dstep)), 2) if dstep else None,
       "etapes_partage": steps_p,
       "etapes_indep": steps_i,
       "critere": bool(part == 30 and prop < 0.5)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp33.json"), "w"), indent=1)
print(f"[33] RESULTAT partage={part}/30 indep={indep}/30 (prop={prop:.3f}) "
      f"critere={res['critere']}")
