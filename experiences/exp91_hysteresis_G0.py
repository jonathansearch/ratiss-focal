"""TEST-91 : boucle G0 monte-descend — la courbure écrit-elle dans le QM ?
Anneau NQ=24 + hubs (K=3, DT=0.3, graines 55/100), 2 puits en 0 et pi
(s=0.5). G0 : 0 -> 1.2 (13 paliers) puis 1.2 -> 0 (13 paliers), 60 pas de
relaxation par palier (th continué, pas réinitialisé). On regarde :
R par palier sur chaque branche, twist par palier, aire de boucle
(sum |R_up - R_down| * dG0), écart max.
Observation pure, zéro verdict."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NQ, KQ, DTQ, PAL = 24, 3.0, 0.3, 60
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
ANG = np.linspace(0, 2 * np.pi, NQ, endpoint=False)
d0 = np.abs((ANG + np.pi) % (2 * np.pi) - np.pi)
d1 = np.abs(((ANG - np.pi + np.pi) % (2 * np.pi)) - np.pi)
PROF = np.exp(-d0 ** 2 / 0.5) + np.exp(-d1 ** 2 / 0.5)

G0S = [round(float(x), 3) for x in np.linspace(0, 1.2, 13)]
th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)


def palier(G0):
    global th
    om = OMEGA - G0 * PROF
    R = []
    for _ in range(PAL):
        th = th + DTQ * (om + (KQ / NQ) *
                         (adj * np.sin(th[None, :] - th[:, None])).sum(1))
        R.append(float(np.abs(np.exp(1j * th).mean())))
    dth = np.angle(np.exp(1j * (np.roll(th, -1) - th)))
    return (round(float(np.mean(R[-20:])), 4),
            round(float(dth.sum() / (2 * np.pi)), 3))


up, down = [], []
for G0 in G0S:
    r, tw = palier(G0)
    up.append({"G0": G0, "R": r, "twist": tw})
for G0 in reversed(G0S):
    r, tw = palier(G0)
    down.append({"G0": G0, "R": r, "twist": tw})
down.reverse()
dG = G0S[1] - G0S[0]
aire = round(float(sum(abs(u["R"] - d["R"]) for u, d in zip(up, down)) * dG), 5)
gap = round(float(max(abs(u["R"] - d["R"]) for u, d in zip(up, down))), 4)
print(f"[91] aire_boucle={aire} écart_max={gap}", flush=True)
print("[91] up  : " + " ".join(f"{x['R']:.2f}" for x in up), flush=True)
print("[91] down: " + " ".join(f"{x['R']:.2f}" for x in down), flush=True)
print("[91] twist_up  : " + " ".join(f"{x['twist']:g}" for x in up), flush=True)
print("[91] twist_down: " + " ".join(f"{x['twist']:g}" for x in down), flush=True)
json.dump({"up": up, "down": down, "aire_boucle": aire, "ecart_max": gap},
          open(os.path.join(HERE, "resultats", "exp91.json"), "w"), indent=1)
print("[91] OBSERVÉ : boucle archivée.")
