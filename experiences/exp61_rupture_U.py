"""TEST-61 : rupture de U au-delà de sigma_c. Ligne TEST-38 (T=20, mêmes
graines/messages étendues), sigma dans [0.10,0.30] pas 0.02 (11 pts),
50+50 essais/point. sigma_rupture = 1er sigma avec partage <= indep+3
(mort = indistinguable du contrôle). Si aucune : ASYMPTOTIQUE si les
3 derniers points ont |pente|<=1/pt (U_min=moy. 3 derniers) et restent
>= indep_max+5, sinon MIXTE. Réversibilité (secondaire) : T=40, 20 pas
à sigma=0.20 puis 20 pas à sigma=0.02, 30+30 -> RÉVERSIBLE (à ±2 du
pur-bas TEST-58 29/30) / PARTIEL / IRRÉVERSIBLE (à ±2 du pur-haut).
Critère : MORT ou ASYMPTOTIQUE (rupture caractérisée)."""
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


def etape(seuil, cible, seed_jit, jit, T=20):
    rng = np.random.default_rng(seed_jit)
    port = P.creer_porteurs(2048, 8, "I", seed=3)
    for p in port:
        p.position += np.array(cible, float)
    for t in range(T):
        P.transporter(port, cible, 0.12)
        for p in port:
            p.position += rng.normal(0, jit, 3)
        if P.concentration(port, t + 1) >= seuil:
            return t + 1
    return None


def etape_rev(seuil, cible, seed_jit):
    rng = np.random.default_rng(seed_jit)
    port = P.creer_porteurs(2048, 8, "I", seed=3)
    for p in port:
        p.position += np.array(cible, float)
    for t in range(40):
        jit = 0.20 if t < 20 else 0.02
        P.transporter(port, cible, 0.12)
        for p in port:
            p.position += rng.normal(0, jit, 3)
        if P.concentration(port, t + 1) >= seuil:
            return t + 1
    return None


def msg(graine):
    return np.random.default_rng(graine).integers(0, 2, 2048).astype(
        np.uint8).tobytes()


def ligne(jit, n=50):
    part, indep = 0, 0
    for i in range(n):
        m = msg(500 + i)
        sA = etape(phic(m), [0, 0, 0], 3800 + i, jit)
        sB = etape(phic(m), [6, 0, 0], 3900 + i, jit)
        part += (sA == sB)
        sB2 = etape(phic(msg(9000 + i)), [6, 0, 0], 3900 + i, jit)
        indep += (sA == sB2)
    return part, indep


sigmas = [round(0.10 + 0.02 * k, 4) for k in range(11)]
pts = []
for sg in sigmas:
    p, iq = ligne(sg)
    pts.append({"sigma": sg, "partage": p, "indep": iq})
    print(f"[61] sigma={sg:.2f} : {p}/50 vs {iq}/50", flush=True)
mort = next((x for x in pts if x["partage"] <= x["indep"] + 3), None)
last3 = pts[-3:]
pente = (last3[-1]["partage"] - last3[0]["partage"]) / 2
imax = max(x["indep"] for x in pts)
if mort is not None:
    classe, umin = "MORT", None
    sig_r = mort["sigma"]
elif abs(pente) <= 1.0 and min(x["partage"] for x in last3) >= imax + 5:
    classe, umin = "ASYMPTOTIQUE", round(float(np.mean(
        [x["partage"] for x in last3])), 1)
    sig_r = None
else:
    classe, umin, sig_r = "MIXTE", None, None
pr, ir = 0, 0
for i in range(30):
    m = msg(500 + i)
    sA = etape_rev(phic(m), [0, 0, 0], 3800 + i)
    sB = etape_rev(phic(m), [6, 0, 0], 3900 + i)
    pr += (sA == sB)
    sB2 = etape_rev(phic(msg(9000 + i)), [6, 0, 0], 3900 + i)
    ir += (sA == sB2)
pur_haut = next(x["partage"] for x in pts if x["sigma"] == 0.20) * 30 / 50
if abs(pr - 29) <= 2:
    rev = "RÉVERSIBLE"
elif abs(pr - pur_haut) <= 2:
    rev = "IRRÉVERSIBLE"
else:
    rev = "PARTIEL"
print(f"[61] reversibilité : {pr}/30 (pur-bas 29, pur-haut~{pur_haut:.0f}) "
      f"-> {rev}", flush=True)
res = {"points": pts, "sigma_rupture": sig_r, "U_min": umin,
       "classe": classe, "reversibilite": {"partage": pr, "indep": ir,
                                           "classe": rev},
       "critere": bool(classe in ("MORT", "ASYMPTOTIQUE"))}
json.dump(res, open(os.path.join(HERE, "resultats", "exp61.json"), "w"), indent=1)
print(f"[61] RESULTAT classe={classe} sigma_r={sig_r} U_min={umin} "
      f"rev={rev} critere={res['critere']}")
