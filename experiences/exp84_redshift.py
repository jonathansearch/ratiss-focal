"""TEST-84 : redshift direct — la fréquence d'un anneau dépend-elle de
sa distance au puits ? 6 mini-anneaux (8 oscillateurs, K=3, DT=0.3)
posés à d = 2, 4, 6, 8, 10, 12 cellules d'un puits. Chaque oscillateur
subit delta = -G0*exp(-d_osc/w), G0=1.0, w=3 (chaque oscillateur a sa
vraie distance : cisaillement intra-anneau). T=400, brouillage commun
des phases à t=200. On regarde : fréquence moyenne <dPsi/dt> par anneau
(100 derniers pas) vs d, R final par anneau, temps de resync après
brouillage (retour à R>=0.8, None si jamais).
Observation pure, zéro verdict."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NQ, KQ, DTQ, T, TBROU = 8, 3.0, 0.3, 400, 200
G0, W = 1.0, 3.0
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0


def run(d):
    rng = np.random.default_rng(8400 + d)
    om0 = rng.normal(0, 0.2, NQ)
    angs = np.linspace(0, 2 * np.pi, NQ, endpoint=False)
    dosc = np.sqrt(d ** 2 + 1.0 - 2 * d * 1.0 * np.cos(angs))
    om = om0 - G0 * np.exp(-dosc / W)
    th = rng.uniform(0, 2 * np.pi, NQ)
    R, Psi = [], []
    resync = None
    for t in range(T):
        if t == TBROU:
            th = rng.uniform(0, 2 * np.pi, NQ)
        th = th + DTQ * (om + (KQ / NQ) *
                         (adj * np.sin(th[None, :] - th[:, None])).sum(1))
        R.append(float(np.abs(np.exp(1j * th).mean())))
        Psi.append(float(np.angle(np.exp(1j * th).mean())))
        if t > TBROU and resync is None and R[-1] >= 0.8:
            resync = t - TBROU
    dp = np.unwrap(np.array(Psi[-100:]))
    freq = float((dp[-1] - dp[0]) / (len(dp) * DTQ))
    return {"d": d, "freq": round(freq, 4),
            "R_final": round(float(np.mean(R[-20:])), 4),
            "resync_pas": resync}


lignes = []
for d in (2, 4, 6, 8, 10, 12):
    r = run(d)
    lignes.append(r)
    print(f"[84] d={d} : freq={r['freq']} R_fin={r['R_final']} "
          f"resync={r['resync_pas']}", flush=True)
json.dump({"G0": G0, "w": W, "lignes": lignes},
          open(os.path.join(HERE, "resultats", "exp84.json"), "w"), indent=1)
print("[84] OBSERVÉ : 6 distances, fréquences archivées.")
