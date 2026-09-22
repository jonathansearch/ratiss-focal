"""TEST-85 : Q entre TROIS puits (le twist compte-t-il les puits ?).
Question née de TEST-79/80 (twist 1 avec un puits, -2 avec deux).
Anneau NQ=24 + hubs (K=3, DT=0.3, graines 55/100), trois gaussiennes
de ralentissement en 0, 2pi/3, 4pi/3 (s=0.5). G0 dans {0, 0.2, 0.5, 1.0},
T=300. On regarde : R final, twist, R par tiers.
Observation pure, zéro verdict."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NQ, KQ, DTQ, T = 24, 3.0, 0.3, 300
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
ANG = np.linspace(0, 2 * np.pi, NQ, endpoint=False)


def dist(a, c):
    return np.abs(((a - c + np.pi) % (2 * np.pi)) - np.pi)


PROF = sum(np.exp(-dist(ANG, c) ** 2 / (2 * 0.5 ** 2))
           for c in (0, 2 * np.pi / 3, 4 * np.pi / 3))


def run(G0):
    th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
    om = OMEGA - G0 * PROF
    R = []
    for _ in range(T):
        th = th + DTQ * (om + (KQ / NQ) *
                         (adj * np.sin(th[None, :] - th[:, None])).sum(1))
        R.append(float(np.abs(np.exp(1j * th).mean())))
    dth = np.angle(np.exp(1j * (np.roll(th, -1) - th)))
    g = np.exp(1j * th)
    return {"G0": G0, "R_final": round(float(np.mean(R[-50:])), 4),
            "twist": round(float(dth.sum() / (2 * np.pi)), 3),
            "R_tiers": [round(float(np.abs(g[i * 8:(i + 1) * 8].mean())), 4)
                        for i in range(3)]}


lignes = []
for G0 in (0, 0.2, 0.5, 1.0):
    r = run(G0)
    lignes.append(r)
    print(f"[85] G0={G0} : R_fin={r['R_final']} twist={r['twist']} "
          f"tiers={r['R_tiers']}", flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "resultats", "exp85.json"), "w"), indent=1)
print("[85] OBSERVÉ : 4 triples-puits archivés.")
