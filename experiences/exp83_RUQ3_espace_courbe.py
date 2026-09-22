"""TEST-83 : RUQ-3 (mémoire de graphe) en espace courbe.
Reprise exacte de TEST-72 (graine 7201, TA=400 groupés + 300 séparés),
plus une question à moi : si la moitié de l'essaim vit RALENTIE
(désaccord -G0 sur les W0 des indices pairs = côté puits), le graphe
tient-il encore la mémoire après séparation ? G0 dans {0, 0.5, 1.0}.
On regarde : R_conv_A, R_final_B, var(q), corr(th,q), lambda2/entropie.
Observation pure, zéro verdict, zéro classe."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

N, TA, TB = 12, 400, 300
K, KFIX, DT, GAM = 2.0, 2.0, 0.3, 1.0
ALPHA, BETA = 0.05, 0.1
FB_A, FB_B = 0.5, 0.05
A = np.zeros((N, N))
for i in range(N):
    A[i, (i - 1) % N] = A[i, (i + 1) % N] = 1.0
A[0, :] = A[:, 0] = 1.0
A[6, :] = A[:, 6] = 1.0
np.fill_diagonal(A, 0.0)


def run(G0):
    rng = np.random.default_rng(7201)
    g = C.fond(seed=24)[:160].copy()
    bb0, bb1 = g.min(0), g.max(0)
    DIAG = float(np.linalg.norm(bb1 - bb0))
    STEP, RAYON, W = DIAG / 150, DIAG / 8, 0.05
    X = rng.uniform(bb0, bb1, (N, 3))
    th = rng.uniform(0, 2 * np.pi, N)
    q = np.zeros(N)
    W0 = rng.normal(0, 0.2, N)
    W0[::2] -= G0
    PH = rng.uniform(0, 2 * np.pi, N)

    def densites(X, g):
        d = np.sqrt(((g[None, :, :] - X[:, None, :]) ** 2).sum(-1))
        dd = 1 / (np.sort(d, axis=1)[:, :5].mean(1) + 1e-9)
        lo, hi = dd.min(), dd.max()
        return (dd - lo) / max(hi - lo, 1e-9)

    def etape(g):
        d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
        g = g + 0.1 * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
        return g + rng.normal(0, 0.005, g.shape)

    def pas(X, th, q, g):
        s = densites(X, g)
        dmat = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
        for i in range(N):
            vois = [j for j in range(N) if j != i and dmat[i, j] < RAYON]
            if vois:
                th[i] += DT * (K / N) * float(np.sin(th[vois] - th[i]).sum())
                q[i] += BETA * (float(q[vois].mean()) - q[i])
        th = th + DT * (KFIX / N) * (A * np.sin(th[None, :] - th[:, None])).sum(1)
        Psi = float(np.angle(np.exp(1j * th).mean()))
        th = th + DT * W0 + GAM * (s - 0.5) * DT + FB_A * (q - q.mean()) * DT
        q = q + ALPHA * (s - q) + FB_B * np.sin(th - Psi)
        return th, q

    def snap(X, th):
        dmat = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
        Asp = ((dmat < RAYON) & (np.eye(N) == 0)).astype(float)
        L = np.diag(np.clip(A + Asp, 0, 1).sum(1)) - np.clip(A + Asp, 0, 1)
        lam2 = round(float(sorted(np.linalg.eigvalsh(L))[1]), 4)
        h, _ = np.histogram(np.angle(np.exp(1j * th)), bins=6,
                            range=(-np.pi, np.pi))
        p = h / h.sum()
        return lam2, round(float(-(p[p > 0] * np.log(p[p > 0])).sum()), 4)

    Rs, Vq, Cq = [], [], []
    for t in range(TA):
        g = etape(g)
        th, q = pas(X, th, q, g)
        c = g.mean(0)
        X = X + rng.normal(0, DIAG / 100, (N, 3))
        rel = X - c
        nrm = np.linalg.norm(rel, axis=1, keepdims=True)
        X = np.where(nrm > DIAG / 20, c + rel / nrm * DIAG / 20, X)
        Rs.append(float(np.abs(np.exp(1j * th).mean())))
        Vq.append(float(q.var()))
        Cq.append(float(np.corrcoef(np.sin(th - th.mean()), q - q.mean())[0, 1])
                  if q.std() > 1e-9 else 0.0)
    R_A = float(np.mean(Rs[-50:]))
    X = rng.uniform(bb0, bb1, (N, 3))
    for t in range(TB):
        g = etape(g)
        th, q = pas(X, th, q, g)
        X = X + STEP * np.column_stack(
            [np.cos(W * t + PH), np.sin(1.3 * W * t + PH),
             np.cos(0.7 * W * t + 2 * PH)]) + rng.normal(0, STEP / 3, (N, 3))
        X = np.clip(X, bb0 - DIAG * 0.25, bb1 + DIAG * 0.25)
        Rs.append(float(np.abs(np.exp(1j * th).mean())))
        Vq.append(float(q.var()))
        Cq.append(float(np.corrcoef(np.sin(th - th.mean()), q - q.mean())[0, 1])
                  if q.std() > 1e-9 else 0.0)
    lam2, ent = snap(X, th)
    return {"G0": G0, "R_conv_A": round(R_A, 4),
            "R_final_B": round(float(np.mean(Rs[-50:])), 4),
            "R_chute": round(float(np.min(Rs[TA:])), 4),
            "varq_finale": round(float(np.mean(Vq[-50:])), 5),
            "corr_finale": round(Cq[-1], 4),
            "lambda2_fin": lam2, "entropie_fin": ent,
            "R_serie": [round(x, 4) for x in Rs[::10]]}


lignes = []
for G0 in (0, 0.5, 1.0):
    r = run(G0)
    lignes.append(r)
    print(f"[83] G0={G0} : A={r['R_conv_A']} chute={r['R_chute']} "
          f"finB={r['R_final_B']} varq={r['varq_finale']}", flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "resultats", "exp83.json"), "w"), indent=1)
print("[83] OBSERVÉ : 3 courbures, séries archivées.")
