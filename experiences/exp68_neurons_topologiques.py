"""TEST-68 : neurones UKTZ-T (topologiques) — EXPLORATION OUVERTE.
12 neurones en graphe FIXE (anneau + 2 hubs, comme l'anneau Q), phases
Kuramoto : th += dt*(w + (K/N)*A*sin(dth)) + gamma*(s-0.5)*dt (le champ
local module la fréquence). Positions forcées (balade 300 + groupés
300, même monde tore graine 24). La topologie est indépendante de la
géométrie : la question est si le partage sensoriel (groupés) change
la synchronisation. OBSERVABLES (aucun critère) : ordre R(t), R_balade
vs R_groupé, histogramme phases final. Aucun verdict."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

N, T1, T2 = 12, 300, 300
K, DT, GAM = 2.0, 0.3, 1.0
rng = np.random.default_rng(6801)
g = C.fond(seed=24)[:160].copy()


def etape(g):
    d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
    g = g + 0.1 * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
    return g + rng.normal(0, 0.005, g.shape)


A = np.zeros((N, N))
for i in range(N):
    A[i, (i - 1) % N] = A[i, (i + 1) % N] = 1.0
A[0, :] = A[:, 0] = 1.0
A[6, :] = A[:, 6] = 1.0
np.fill_diagonal(A, 0.0)
bb0, bb1 = g.min(0), g.max(0)
DIAG = float(np.linalg.norm(bb1 - bb0))
STEP = DIAG / 150
X = rng.uniform(bb0, bb1, (N, 3))
th = rng.uniform(0, 2 * np.pi, N)
W0 = rng.normal(0, 0.2, N)
PH = rng.uniform(0, 2 * np.pi, N)
W = 0.05


def densites(X, g):
    d = np.sqrt(((g[None, :, :] - X[:, None, :]) ** 2).sum(-1))
    dd = 1 / (np.sort(d, axis=1)[:, :5].mean(1) + 1e-9)
    lo, hi = dd.min(), dd.max()
    return (dd - lo) / max(hi - lo, 1e-9)


R = []
for t in range(T1 + T2):
    g = etape(g)
    s = densites(X, g)
    th = th + DT * (W0 + (K / N) * (A * np.sin(th[None, :] - th[:, None])
                                       ).sum(1)) + GAM * (s - 0.5) * DT
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
    R.append(round(float(np.abs(np.exp(1j * th).mean())), 4))
    if (t + 1) % 150 == 0:
        print(f"[68] ... pas {t + 1}/600 R={R[-1]:.3f}", flush=True)
hist, _ = np.histogram(np.angle(np.exp(1j * th)), bins=6,
                       range=(-np.pi, np.pi))
res = {"R": R, "R_balade": round(float(np.mean(R[T1 - 50:T1])), 4),
       "R_groupe": round(float(np.mean(R[-50:])), 4),
       "phases_finales": [round(float(x), 3) for x in th],
       "histo_final": [int(x) for x in hist],
       "classe": "EXPLORATION", "critere": None}
json.dump(res, open(os.path.join(HERE, "resultats", "exp68.json"), "w"))
print(f"[68] RESULTAT R_balade={res['R_balade']} R_groupe={res['R_groupe']} "
      f"(exploration, aucun verdict)")
