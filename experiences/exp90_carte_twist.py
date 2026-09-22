"""TEST-90 : carte du twist — 2 puits, écart x force (chasse au pli).
Anneau NQ=24 + hubs (K=3, DT=0.3, graines 55/100). Puits gaussiens (s=0.5)
en 0 et DELTA. DELTA dans {pi/4, pi/2, 3pi/4, pi}, G0 de 0 à 1.5 (16 pts),
T=300. On regarde : carte R_final et carte twist (lignes de pli ?).
Observation pure, zéro verdict — tout effet pris au sérieux."""
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


def run(delta, G0):
    prof = (np.exp(-dist(ANG, 0) ** 2 / 0.5) +
            np.exp(-dist(ANG, delta) ** 2 / 0.5))
    th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
    om = OMEGA - G0 * prof
    R = []
    for _ in range(T):
        th = th + DTQ * (om + (KQ / NQ) *
                         (adj * np.sin(th[None, :] - th[:, None])).sum(1))
        R.append(float(np.abs(np.exp(1j * th).mean())))
    dth = np.angle(np.exp(1j * (np.roll(th, -1) - th)))
    return (round(float(np.mean(R[-50:])), 4),
            round(float(dth.sum() / (2 * np.pi)), 3))


G0S = [round(float(x), 3) for x in np.linspace(0, 1.5, 16)]
carte = []
for nom, delta in (("pi/4", np.pi / 4), ("pi/2", np.pi / 2),
                   ("3pi/4", 3 * np.pi / 4), ("pi", np.pi)):
    ligne = []
    for G0 in G0S:
        r, tw = run(delta, G0)
        ligne.append({"G0": G0, "R": r, "twist": tw})
    carte.append({"delta": nom, "ligne": ligne})
    print(f"[90] delta={nom} : twists=" +
          " ".join(f"{x['twist']:g}" for x in ligne), flush=True)
json.dump({"G0s": G0S, "carte": carte},
          open(os.path.join(HERE, "resultats", "exp90.json"), "w"), indent=1)
print("[90] OBSERVÉ : carte 4x16 archivée.")
