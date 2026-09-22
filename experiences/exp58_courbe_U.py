"""TEST-58 : courbe S_U(sigma). Ligne TEST-38 (T=20, mêmes graines/
messages), jitter sigma dans [0.01,0.10] pas 0.005 (19 points),
30+30 essais/point. sigma_c = 1er sigma avec partage <= plateau-4
(plateau = max). Formes : linéaire / exponentielle / sigmoïde (grille).
Classes : SEUIL (sigma_c trouvé + forme R²>0.9) / ROBUSTE (chute <=3
partout) / MIXTE. Critère : SEUIL ou ROBUSTE."""
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


def etape(seuil, cible, seed_jit, jit):
    rng = np.random.default_rng(seed_jit)
    port = P.creer_porteurs(2048, 8, "I", seed=3)
    for p in port:
        p.position += np.array(cible, float)
    for t in range(20):
        P.transporter(port, cible, 0.12)
        for p in port:
            p.position += rng.normal(0, jit, 3)
        if P.concentration(port, t + 1) >= seuil:
            return t + 1
    return None


def msg(graine):
    return np.random.default_rng(graine).integers(0, 2, 2048).astype(
        np.uint8).tobytes()


def ligne(jit):
    part, indep = 0, 0
    for i in range(30):
        m = msg(500 + i)
        sA = etape(phic(m), [0, 0, 0], 3800 + i, jit)
        sB = etape(phic(m), [6, 0, 0], 3900 + i, jit)
        part += (sA == sB)
        sB2 = etape(phic(msg(9000 + i)), [6, 0, 0], 3900 + i, jit)
        indep += (sA == sB2)
    return part, indep


sigmas = [round(0.01 + 0.005 * k, 4) for k in range(19)]
pts = []
for sg in sigmas:
    p, iq = ligne(sg)
    pts.append({"sigma": sg, "partage": p, "indep": iq})
    print(f"[58] sigma={sg:.3f} : {p}/30 vs {iq}/30", flush=True)
parts = np.array([x["partage"] for x in pts], float)
sg = np.array(sigmas, float)
plateau = float(parts.max())
chute = plateau - parts.min()
sigc = next((x["sigma"] for x in pts if x["partage"] <= plateau - 4), None)


def r2(pred):
    pred = np.array(pred)
    ss = float(((parts - pred) ** 2).sum())
    return 1 - ss / max(float(((parts - parts.mean()) ** 2).sum()), 1e-12)


cands = {}
bl, bh = float(parts.min()) - 1, float(parts.max()) + 1
grid_lin = [(a, b) for a in np.linspace(bl, bh, 15)
            for b in np.linspace(-300, 50, 15)]
cands["lineaire"] = max((r2(a + b * sg), (a, b)) for a, b in grid_lin)
grid_exp = [(a, b, c) for a in np.linspace(bl, bh, 9)
            for b in np.linspace(-30, 30, 9)
            for c in np.linspace(1, 120, 9)]
cands["exponentielle"] = max(
    (r2(a + b * np.exp(-c * sg)), (a, b, c)) for a, b, c in grid_exp)
grid_sig = [(a, b, c, d) for a in np.linspace(bl, bh, 7)
            for b in np.linspace(0, 30, 7) for c in np.linspace(10, 200, 7)
            for d in np.linspace(0.01, 0.10, 7)]
cands["sigmoide"] = max(
    (r2(a + b / (1 + np.exp(c * (sg - d)))), (a, b, c, d))
    for a, b, c, d in grid_sig)
forme = max(cands, key=lambda k: cands[k][0])
R2f = float(cands[forme][0])
print(f"[58] plateau={plateau} chute={chute} sigma_c={sigc} forme={forme} "
      f"R2={R2f:.4f}", flush=True)
if sigc is not None and R2f > 0.9:
    classe = "SEUIL"
elif chute <= 3:
    classe = "ROBUSTE"
else:
    classe = "MIXTE"
res = {"points": pts, "plateau": plateau, "sigma_c": sigc, "forme": forme,
       "R2": round(R2f, 4),
       "params": [round(float(x), 4) for x in cands[forme][1]],
       "classe": classe, "critere": bool(classe in ("SEUIL", "ROBUSTE"))}
json.dump(res, open(os.path.join(HERE, "resultats", "exp58.json"), "w"), indent=1)
print(f"[58] RESULTAT classe={classe} critere={res['critere']}")
