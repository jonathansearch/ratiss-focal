"""TEST-79 : Q à côté d'un puits (désaccord fréquentiel, pas de capture).
Anneau NQ=24 + hubs (K=3, DT=0.3, graines 55/100). Le puits à l'angle 0
RALENTIT les oscillateurs proches : delta_i = -G0*exp(-dang²/2s²), s=0.5.
G0 dans {0, 0.1, 0.2, 0.5, 1.0}, T=300. On regarde : R final (50 derniers),
twist (enroulement de phase sur l'anneau), profil de phase.
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
dang = np.abs((ANG + np.pi) % (2 * np.pi) - np.pi)
PROF = np.exp(-dang ** 2 / (2 * 0.5 ** 2))


def run(G0):
    th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
    om = OMEGA - G0 * PROF
    R = []
    for _ in range(T):
        th = th + DTQ * (om + (KQ / NQ) *
                         (adj * np.sin(th[None, :] - th[:, None])).sum(1))
        R.append(float(np.abs(np.exp(1j * th).mean())))
    dth = np.angle(np.exp(1j * (np.roll(th, -1) - th)))
    twist = float(dth.sum() / (2 * np.pi))
    return {"G0": G0, "R_final": round(float(np.mean(R[-50:])), 4),
            "R_min": round(float(np.min(R)), 4),
            "twist": round(twist, 3),
            "phases": [round(float(x), 3) for x in np.angle(np.exp(1j * th))]}


lignes = []
for G0 in (0, 0.1, 0.2, 0.5, 1.0):
    r = run(G0)
    lignes.append(r)
    print(f"[79] G0={G0} : R_fin={r['R_final']} R_min={r['R_min']} "
          f"twist={r['twist']}", flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "resultats", "exp79.json"), "w"), indent=1)
print("[79] OBSERVÉ : 5 désaccords, profils de phase archivés.")
