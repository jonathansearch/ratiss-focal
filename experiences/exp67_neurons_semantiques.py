"""TEST-67 : neurones UKTZ-S (sémantiques) — EXPLORATION OUVERTE.
12 neurones, chacun avec embedding e (R^8) + position forcée (drive de
Lissajous + bruit). Monde = tore G (graine 24, calme). Sensation :
densité locale relative (kNN tore, normalisée entre neurones).
Dynamique : e <- norm(e + eta*s*u + kappa*(moy_voisins - e)) avec u
direction propre fixe (pression divergente) + couplage spatial (rayon
adaptatif, actif surtout groupés). 300 pas balade + 300 pas groupés
(boule commune, toujours mobiles). OBSERVABLES (aucun critère) :
similarité cosinus moyenne S(t), S_balade vs S_groupé, matrices.
Question : la proximité crée-t-elle un code partagé ?"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

N, D, T1, T2 = 12, 8, 300, 300
ETA, KAP = 0.05, 0.1
rng = np.random.default_rng(6701)
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
E = rng.normal(0, 1, (N, D))
E = E / np.linalg.norm(E, axis=1, keepdims=True)
U = rng.normal(0, 1, (N, D))
U = U / np.linalg.norm(U, axis=1, keepdims=True)
PH = rng.uniform(0, 2 * np.pi, N)
W = 0.05


def densites(X, g):
    d = np.sqrt(((g[None, :, :] - X[:, None, :]) ** 2).sum(-1))
    dd = 1 / (np.sort(d, axis=1)[:, :5].mean(1) + 1e-9)
    lo, hi = dd.min(), dd.max()
    return (dd - lo) / max(hi - lo, 1e-9)


def sim_moy(E):
    n = E / np.linalg.norm(E, axis=1, keepdims=True)
    M = n @ n.T
    iu = np.triu_indices(N, 1)
    return float(M[iu].mean()), [[round(float(x), 3) for x in row] for row in M]


S, snaps = [], {}
for t in range(T1 + T2):
    g = etape(g)
    s = densites(X, g)
    dmat = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
    for i in range(N):
        vois = [j for j in range(N) if j != i and dmat[i, j] < RAYON]
        e = E[i] + ETA * s[i] * U[i]
        if vois:
            e = e + KAP * (E[vois].mean(0) - E[i])
        E[i] = e / max(np.linalg.norm(e), 1e-9)
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
    sm, _ = sim_moy(E)
    S.append(round(sm, 4))
    if t in (T1 - 1, T1 + T2 - 1):
        _, M = sim_moy(E)
        snaps[str(t)] = M
    if (t + 1) % 150 == 0:
        print(f"[67] ... pas {t + 1}/600 S={S[-1]:.3f}", flush=True)
res = {"S": S, "S_balade": round(float(np.mean(S[T1 - 50:T1])), 4),
       "S_groupe": round(float(np.mean(S[-50:])), 4),
       "matrices": snaps, "classe": "EXPLORATION", "critere": None}
json.dump(res, open(os.path.join(HERE, "resultats", "exp67.json"), "w"))
print(f"[67] RESULTAT S_balade={res['S_balade']} S_groupe={res['S_groupe']} "
      f"(exploration, aucun verdict)")
