"""TEST-57 : distribution du re-tirage Q (n=200). 200 runs indépendants
(60+3 choc+300, seed 5700+j), Qf=moy. 50 derniers. Histogramme 12
classes (densité) ajusté : gaussienne / bêta / uniforme (nulle).
Critère : meilleur R² > 0.95 (gaussienne ou bêta) + paramètres
(moyenne, variance, skewness)."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

NQ, KQ, DTQ, SIG = 24, 3.0, 0.3, 0.04
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
ANG = np.linspace(0, 2 * np.pi, NQ, endpoint=False)
PREF = C.p_sig(np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG),
                                np.zeros(NQ)]))


def run(seed):
    rng = np.random.default_rng(seed)
    th = rng.uniform(0, 2 * np.pi, NQ)

    def pas(K, sg):
        nonlocal th
        th = th + DTQ * (OMEGA + (K / NQ) * (
            adj * np.sin(th[None, :] - th[:, None])).sum(1))
        anc = np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG),
                               np.zeros(NQ)])
        anc = anc + (anc / 2.2) * (0.15 * np.sin(th))[:, None]
        anc = anc + rng.normal(0, sg, anc.shape)
        for i in range(NQ):
            anc[i] += 0.5 * ((anc[(i - 1) % NQ] + anc[(i + 1) % NQ]) / 2
                             - anc[i])
        return C.p_sig(anc) / PREF

    for _ in range(60):
        pas(KQ, SIG)
    for _ in range(3):
        pas(0.0, SIG * 10)
    return float(np.mean([pas(KQ, SIG) for _ in range(300)][-50:]))


qfs = np.array([run(5700 + j) for j in range(200)])
print(f"[57] n=200 min={qfs.min():.4f} max={qfs.max():.4f} "
      f"moy={qfs.mean():.4f} std={qfs.std():.4f}", flush=True)
H, E = np.histogram(qfs, bins=12, density=True)
xc = (E[:-1] + E[1:]) / 2
lo, hi = float(qfs.min()), float(qfs.max())


def r2(h, m):
    m = np.array(m)
    amp = float((h * m).sum() / max((m * m).sum(), 1e-12))
    pred = amp * m
    ss = float(((h - pred) ** 2).sum())
    return 1 - ss / max(float(((h - h.mean()) ** 2).sum()), 1e-12), amp


best = {"R2": -1e9}
for mu in np.linspace(lo, hi, 15):
    for sg in np.linspace(0.005, 0.08, 12):
        m = np.exp(-0.5 * ((xc - mu) / sg) ** 2)
        s, amp = r2(H, m)
        if s > best["R2"]:
            best = {"nom": "gaussienne", "R2": s,
                    "params": {"mu": round(float(mu), 4),
                               "sigma": round(float(sg), 4),
                               "amp": round(float(amp), 4)}}
xn = (xc - lo) / (hi - lo + 1e-12)
for a in np.linspace(0.7, 6, 12):
    for b in np.linspace(0.7, 6, 12):
        m = xn ** (a - 1) * (1 - xn) ** (b - 1)
        s, amp = r2(H, m)
        if s > best["R2"]:
            best = {"nom": "beta", "R2": s,
                    "params": {"a": round(float(a), 3),
                               "b": round(float(b), 3),
                               "amp": round(float(amp), 4)}}
z = (qfs - qfs.mean()) / qfs.std()
skew = float((z ** 3).mean())
print(f"[57] meilleur={best['nom']} R2={best['R2']:.4f} params={best['params']} "
      f"skew={skew:.3f}", flush=True)
ok = bool(best["R2"] > 0.95)
res = {"n": 200, "min": round(lo, 4), "max": round(hi, 4),
       "moyenne": round(float(qfs.mean()), 4),
       "variance": round(float(qfs.var()), 5),
       "skewness": round(skew, 3), "meilleur": best["nom"],
       "R2": round(float(best["R2"]), 4), "params": best["params"],
       "critere": ok}
json.dump(res, open(os.path.join(HERE, "resultats", "exp57.json"), "w"), indent=1)
print(f"[57] RESULTAT {best['nom']} R2={best['R2']:.4f} critere={ok}")
