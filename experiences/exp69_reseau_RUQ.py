"""TEST-69 : RUQ-1 / Réseau Universel Q (invention) — EXPLORATION OUVERTE.
Mon design : 12 neurones phase+charge. th_i : Kuramoto SPATIAL (voisins
par proximité, rayon adaptatif) + modulation de fréquence par le champ
local. q_i (charge) : dq = alpha*(s-q) + beta*(moy_voisins-q) — la
charge BOIT le champ local et DIFFUSE par proximité. Positions forcées
(Lissajous + bruit, balade 300 + groupés 300, tore graine 24).
Idée : la charge est une mémoire collective du champ ; la phase son
rythme. OBSERVABLES (aucun critère) : R(t), var(q)(t), corr(q,s)(t),
nuage (th,q) final. Questions : la charge se répartit ? la phase suit ?
le groupe fait-il émerger un régime propre ? Aucun verdict."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

N, T1, T2 = 12, 300, 300
K, DT, GAM = 2.0, 0.3, 1.0
ALPHA, BETA = 0.05, 0.1
rng = np.random.default_rng(6901)
g = C.fond(seed=24)[:160].copy()


def etape(g):
    d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
    g = g + 0.1 * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
    return g + rng.normal(0, 0.005, g.shape)


bb0, bb1 = g.min(0), g.max(0)
DIAG = float(np.linalg.norm(bb1 - bb0))
STEP = DIAG / 150
RAYON = DIAG / 8
X = rng.uniform(bb0, bb1, (N, 3))
th = rng.uniform(0, 2 * np.pi, N)
q = np.zeros(N)
W0 = rng.normal(0, 0.2, N)
PH = rng.uniform(0, 2 * np.pi, N)
W = 0.05


def densites(X, g):
    d = np.sqrt(((g[None, :, :] - X[:, None, :]) ** 2).sum(-1))
    dd = 1 / (np.sort(d, axis=1)[:, :5].mean(1) + 1e-9)
    lo, hi = dd.min(), dd.max()
    return (dd - lo) / max(hi - lo, 1e-9)


Rs, Vq, Cq = [], [], []
for t in range(T1 + T2):
    g = etape(g)
    s = densites(X, g)
    dmat = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
    for i in range(N):
        vois = [j for j in range(N) if j != i and dmat[i, j] < RAYON]
        if vois:
            th[i] += DT * (K / N) * float(np.sin(th[vois] - th[i]).sum())
            q[i] += BETA * (float(q[vois].mean()) - q[i])
    th = th + DT * W0 + GAM * (s - 0.5) * DT
    q = q + ALPHA * (s - q)
    Rs.append(round(float(np.abs(np.exp(1j * th).mean())), 4))
    Vq.append(round(float(q.var()), 5))
    Cq.append(round(float(np.corrcoef(q, s)[0, 1])
                    if q.std() > 1e-9 and s.std() > 1e-9 else 0.0, 4))
    if t < T1:
        X = X + STEP * np.column_stack(
            [np.cos(W * t + PH), np.sin(1.3 * W * t + PH),
             np.cos(0.7 * W * t + 2 * PH)]) + rng.normal(0, STEP / 3, (N, 3))
        X = np.clip(X, bb0 - DIAG * 0.25, bb1 + DIAG * 0.25)
    else:
        c = g.mean(0)
        X = X + rng.normal(0, DIAG / 100, (N, 3))
        rel = X - c
        nrm = np.linalg.norm(rel, axis=1, keepdims=True)
        X = np.where(nrm > DIAG / 20, c + rel / nrm * DIAG / 20, X)
    if (t + 1) % 150 == 0:
        print(f"[69] ... pas {t + 1}/600 R={Rs[-1]:.3f} varq={Vq[-1]:.4f}",
              flush=True)
res = {"R": Rs, "varq": Vq, "corr_qs": Cq,
       "R_balade": round(float(np.mean(Rs[T1 - 50:T1])), 4),
       "R_groupe": round(float(np.mean(Rs[-50:])), 4),
       "varq_balade": round(float(np.mean(Vq[T1 - 50:T1])), 5),
       "varq_groupe": round(float(np.mean(Vq[-50:])), 5),
       "nuage_final": [[round(float(a), 3), round(float(b), 4)]
                       for a, b in zip(np.angle(np.exp(1j * th)), q)],
       "classe": "EXPLORATION", "critere": None}
json.dump(res, open(os.path.join(HERE, "resultats", "exp69.json"), "w"))
print(f"[69] RESULTAT R {res['R_balade']}->{res['R_groupe']} varq "
      f"{res['varq_balade']}->{res['varq_groupe']} (exploration, aucun verdict)")
