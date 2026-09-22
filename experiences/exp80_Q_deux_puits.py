"""TEST-80 : Q entre deux puits (0 et pi).
Même anneau que TEST-79, deux gaussiennes de ralentissement (s=0.5).
G0 dans {0, 0.2, 0.5, 1.0}, T=300. On regarde : R final, twist, R par
moitié (gauche/droite) pour voir un éventuel motif à deux domaines.
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
d0 = np.abs((ANG + np.pi) % (2 * np.pi) - np.pi)
d1 = np.abs(((ANG - np.pi + np.pi) % (2 * np.pi)) - np.pi)
PROF = np.exp(-d0 ** 2 / (2 * 0.5 ** 2)) + np.exp(-d1 ** 2 / (2 * 0.5 ** 2))


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
            "R_moitie_A": round(float(np.abs(g[:12].mean())), 4),
            "R_moitie_B": round(float(np.abs(g[12:].mean())), 4),
            "phases": [round(float(x), 3) for x in np.angle(g)]}


lignes = []
for G0 in (0, 0.2, 0.5, 1.0):
    r = run(G0)
    lignes.append(r)
    print(f"[80] G0={G0} : R_fin={r['R_final']} twist={r['twist']} "
          f"RA={r['R_moitie_A']} RB={r['R_moitie_B']}", flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "resultats", "exp80.json"), "w"), indent=1)
print("[80] OBSERVÉ : 4 doubles-puits, motifs archivés.")
