"""TEST-49 : sanctuaire U sous chocs cumulés. Appareil TEST-45 (M22,
mêmes graines/messages). Niveaux k=0..6 : k=0 -> T=20 normal (réplique
TEST-38) ; k>=1 -> 10 normaux + k x (3 choc + 20 relâche).
30 partagé + 30 indépendant par niveau. Critère : SANCTUAIRE_ABSOLU si
partage identique sur les 7 niveaux (ΔS_U=0) ; sinon N_c = premier k où
partage <= niveau0 - 2 (seuil d'érosion)."""
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


def choc(t):
    if t < 10:
        return False
    return (t - 10) % 23 < 3


def etape(seuil, cible, seed_jit, k):
    rng = np.random.default_rng(seed_jit)
    port = P.creer_porteurs(2048, 8, "I", seed=3)
    for p in port:
        p.position += np.array(cible, float)
    T = 20 if k == 0 else 10 + k * 23
    for t in range(T):
        if k > 0 and choc(t):
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


niveaux = []
for k in range(7):
    part, indep = 0, 0
    for i in range(30):
        m = msg(500 + i)
        sA = etape(phic(m), [0, 0, 0], 3800 + i, k)
        sB = etape(phic(m), [6, 0, 0], 3900 + i, k)
        part += (sA == sB)
        sB2 = etape(phic(msg(9000 + i)), [6, 0, 0], 3900 + i, k)
        indep += (sA == sB2)
    niveaux.append({"k": k, "partage": part, "indep": indep,
                    "separation": part - indep})
    print(f"[49] niveau k={k} : {part}/30 vs {indep}/30", flush=True)
parts = [n["partage"] for n in niveaux]
delta = max(parts) - min(parts)
nc = next((n["k"] for n in niveaux if n["partage"] <= parts[0] - 2), None)
if delta == 0:
    classe = "SANCTUAIRE_ABSOLU"
elif nc is not None:
    classe = f"EROSION_A_Nc={nc}"
else:
    classe = "DERIVE_FAIBLE"
res = {"niveaux": niveaux, "delta_max": delta, "Nc": nc, "classe": classe,
       "critere": bool(delta == 0)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp49.json"), "w"), indent=1)
print(f"[49] RESULTAT parts={parts} delta={delta} Nc={nc} "
      f"classe={classe} critere={res['critere']}")
