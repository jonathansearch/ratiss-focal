"""TEST-48 : escalier de planchers G (6 chocs cumulés). Appareil TEST-42/46
(tore 160, graines 24/42). 14 baseline + 6x(3 choc + 1000 relâche).
Gmin(k) = moy. 50 derniers de chaque relâche (k=0..6). Candidats :
H1 linéaire / H2 exponentielle / H3 saturante (grille numpy).
Critère : meilleur R² > 0.95 -> f(N) identifiée (H3 = noyau absolu)."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

NT = 160
tore0 = C.fond(seed=24)[:NT].copy()
PREF = C.p_sig(tore0)
rng = np.random.default_rng(42)
g = tore0.copy()


def etape(g, al, sg):
    d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
    g = g + al * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
    return g + rng.normal(0, sg, g.shape)


serie = []
for _ in range(14):
    g = etape(g, 0.1, 0.005)
    serie.append(C.p_sig(g) / PREF)
gmin = [float(np.mean(serie[11:14]))]
print(f"[48] Gmin(0)={gmin[0]:.4f} (baseline)", flush=True)
for k in range(1, 7):
    for _ in range(3):
        g = etape(g, -0.15, 0.05)
        serie.append(C.p_sig(g) / PREF)
    for _ in range(1000):
        g = etape(g, 0.1, 0.005)
        serie.append(C.p_sig(g) / PREF)
    gmin.append(float(np.mean(serie[-50:])))
    print(f"[48] choc {k}/6 : Gmin({k})={gmin[-1]:.4f}", flush=True)

N = np.arange(7, dtype=float)
y = np.array(gmin)


def r2(pred):
    pred = np.array(pred)
    ss = float(((y - pred) ** 2).sum())
    return 1 - ss / max(float(((y - y.mean()) ** 2).sum()), 1e-12)


def cherche(fn, bornes, n=11, rondes=3):
    lo = np.array([b[0] for b in bornes], float)
    hi = np.array([b[1] for b in bornes], float)
    best, bestp = -1e9, None
    for _ in range(rondes):
        grilles = [np.linspace(lo[i], hi[i], n) for i in range(len(bornes))]
        for combo in np.array(np.meshgrid(*grilles)).T.reshape(-1, len(bornes)):
            try:
                s = r2(fn(combo))
            except Exception:
                continue
            if s > best:
                best, bestp = s, combo.copy()
        span = (hi - lo) * 0.2
        lo = np.maximum([b[0] for b in bornes], bestp - span)
        hi = np.minimum([b[1] for b in bornes], bestp + span)
    return best, [round(float(x), 5) for x in bestp]


cands = {
    "H1_lineaire": (lambda p: p[0] - N * p[1], [(0.1, 0.5), (-0.05, 0.15)]),
    "H2_exponentielle": (lambda p: p[0] * np.exp(-p[1] * N),
                         [(0.1, 0.5), (0.05, 3.0)]),
    "H3_saturante": (lambda p: p[0] + p[1] * np.exp(-p[2] * N),
                     [(0.0, 0.2), (0.0, 0.5), (0.05, 3.0)]),
}
out = {}
for nom, (fn, bornes) in cands.items():
    s, p = cherche(fn, bornes)
    out[nom] = {"R2": round(s, 4), "params": p}
    print(f"[48] {nom}: R2={s:.4f} params={p}", flush=True)
gagnant = max(out, key=lambda k: out[k]["R2"])
extra = {}
if gagnant == "H1_lineaire" and out[gagnant]["params"][1] > 0:
    extra["rupture_extrapolee_N"] = round(
        out[gagnant]["params"][0] / out[gagnant]["params"][1], 2)
if gagnant == "H3_saturante":
    extra["noyau_absolu"] = out[gagnant]["params"][0]
ok = bool(out[gagnant]["R2"] > 0.95)
res = {"Gmin": [round(x, 4) for x in gmin], "candidats": out,
       "gagnant": gagnant, "R2": out[gagnant]["R2"], "extra": extra,
       "critere": ok}
json.dump(res, open(os.path.join(HERE, "resultats", "exp48.json"), "w"), indent=1)
print(f"[48] RESULTAT gagnant={gagnant} R2={out[gagnant]['R2']} "
      f"extra={extra} critere={ok}")
