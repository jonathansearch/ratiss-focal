"""TEST-36 : forme LIBRE de S_quant. 4 candidats (stretched-exp, Hill,
double-exp, power), grille grossière->fine (numpy seul), post-transitoire.
Critère : meilleur R² > 0.9, forme simple (<=3 params)."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NQ, KQ, DTQ = 24, 3.0, 0.3
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
RQ = []
for _ in range(60):
    th = th + DTQ * (OMEGA + (KQ / NQ) * (
        adj * np.sin(th[None, :] - th[:, None])).sum(1))
    RQ.append(float(np.abs(np.exp(1j * th).mean())))
t = np.arange(10, 60, dtype=float)
y = np.array(RQ[10:])
TAU = t - 10
C0 = 1 - y[0]


def r2(pred):
    pred = np.array(pred)
    ss = float(((y - pred) ** 2).sum())
    return 1 - ss / max(float(((y - y.mean()) ** 2).sum()), 1e-12)


def cherche(fn, bornes, n=9, rondes=3):
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
    "stretched": (lambda p: 1 - p[0] * np.exp(-(p[1] * TAU) ** p[2]),
                  [(0.2, 1.2), (0.005, 0.3), (0.3, 2.5)]),
    "hill": (lambda p: (TAU / p[0]) ** p[1] / (1 + (TAU / p[0]) ** p[1]),
             [(3, 60), (0.4, 6)]),
    "double_exp": (lambda p: 1 - p[0] * np.exp(-p[1] * TAU)
                   - (C0 - p[0]) * np.exp(-p[2] * TAU),
                   [(0.02, C0 - 0.02), (0.01, 0.5), (0.001, 0.1)]),
    "power": (lambda p: 1 - p[0] * (TAU + 1) ** (-p[1]),
              [(0.1, 2.0), (0.1, 3.0)]),
}
res_c = {}
for nom, (fn, bornes) in cands.items():
    s, p = cherche(fn, bornes)
    res_c[nom] = {"R2": round(s, 4), "params": p}
    print(f"[36] {nom}: R2={s:.4f} params={p}", flush=True)
meilleur = max(res_c, key=lambda k: res_c[k]["R2"])
fn = cands[meilleur][0]
pred = np.array(fn(res_c[meilleur]["params"]))
res = {"candidats": res_c, "meilleur": meilleur,
       "R2": res_c[meilleur]["R2"], "params": res_c[meilleur]["params"],
       "residu_std": round(float((y - pred).std()), 5),
       "critere": bool(res_c[meilleur]["R2"] > 0.9)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp36.json"), "w"), indent=1)
print(f"[36] RESULTAT meilleur={meilleur} R2={res['R2']} critere={res['critere']}")
