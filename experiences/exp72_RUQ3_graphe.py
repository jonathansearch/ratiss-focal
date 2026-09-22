"""TEST-72 : RUQ-3 = RUQ-2 + graphe fixe (non-localité topologique).
dth += spatial Kuramoto (K=2, rayon) + FIXE Kuramoto (KFIX=2.0, graphe
UKTZ-T : anneau + 2 hubs, indépendant de la distance) + DT*W0 +
GAM*(s-0.5)*DT + FB_A*(q-qbar)*DT ; dq identique RUQ-2 (ALPHA=0.05,
BETA spatial=0.1, FB_B=0.05*sin(th-Psi)). Graine 7201, tore 24.
Protocole TEST-70 : 400 groupés (barrière R>=0.85 sinon INVALIDE) ->
séparation brusque -> 300 pas. OBSERVABLES : R(t), var(q)(t),
corr(th,q)(t) par pas, lambda2 (connectivité algébrique du graphe
UNION fixe+spatial) + entropie config (histo 6 phases) aux snapshots
fin-A / début-B / fin-B. Classes descriptives H1/H2/H3 (0.45/0.85).
Zéro critère : on regarde, on raconte."""
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
rng = np.random.default_rng(7201)
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


def snapshot(X, th, tag, snaps):
    dmat = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
    Asp = ((dmat < RAYON) & (np.eye(N) == 0)).astype(float)
    U = np.clip(A + Asp, 0, 1)
    L = np.diag(U.sum(1)) - U
    lam2 = round(float(sorted(np.linalg.eigvalsh(L))[1]), 4)
    h, _ = np.histogram(np.angle(np.exp(1j * th)), bins=6,
                        range=(-np.pi, np.pi))
    p = h / h.sum()
    ent = round(float(-(p[p > 0] * np.log(p[p > 0])).sum()), 4)
    snaps[tag] = {"lambda2": lam2, "entropie": ent,
                  "aretes_spatiales": int(Asp.sum() / 2)}
    print(f"[72] snapshot {tag} : lambda2={lam2} entropie={ent}", flush=True)


def pas_ruq3(X, th, q, g):
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


Rs, Vq, Cq, snaps = [], [], [], {}
for t in range(TA):
    g = etape(g)
    th, q = pas_ruq3(X, th, q, g)
    c = g.mean(0)
    X = X + rng.normal(0, DIAG / 100, (N, 3))
    rel = X - c
    nrm = np.linalg.norm(rel, axis=1, keepdims=True)
    X = np.where(nrm > DIAG / 20, c + rel / nrm * DIAG / 20, X)
    Rs.append(round(float(np.abs(np.exp(1j * th).mean())), 4))
    Vq.append(round(float(q.var()), 5))
    Cq.append(round(float(np.corrcoef(np.sin(th - th.mean()), q - q.mean())[0, 1])
                    if q.std() > 1e-9 else 0.0, 4))
    if t == TA - 1:
        snapshot(X, th, "fin_A", snaps)
R_A = float(np.mean(Rs[-50:]))
print(f"[72] phase A : R_conv={R_A:.4f} varq={np.mean(Vq[-50:]):.5f}", flush=True)
if R_A < 0.85:
    res = {"classe": "INVALIDE", "critere": None,
           "raison": f"non-convergence A (R={R_A:.3f})"}
    json.dump(res, open(os.path.join(HERE, "resultats", "exp72.json"), "w"))
    print(f"[72] RESULTAT INVALIDE (R_A={R_A:.3f})")
    raise SystemExit
X = rng.uniform(bb0, bb1, (N, 3))
print("[72] séparation brusque (graphe fixe conservé, th/q intacts)", flush=True)
for t in range(TB):
    g = etape(g)
    th, q = pas_ruq3(X, th, q, g)
    X = X + STEP * np.column_stack(
        [np.cos(W * t + PH), np.sin(1.3 * W * t + PH),
         np.cos(0.7 * W * t + 2 * PH)]) + rng.normal(0, STEP / 3, (N, 3))
    X = np.clip(X, bb0 - DIAG * 0.25, bb1 + DIAG * 0.25)
    Rs.append(round(float(np.abs(np.exp(1j * th).mean())), 4))
    Vq.append(round(float(q.var()), 5))
    Cq.append(round(float(np.corrcoef(np.sin(th - th.mean()), q - q.mean())[0, 1])
                    if q.std() > 1e-9 else 0.0, 4))
    if t == 0:
        snapshot(X, th, "debut_B", snaps)
    if t == TB - 1:
        snapshot(X, th, "fin_B", snaps)
    if (t + 1) % 100 == 0:
        print(f"[72] ... B+{t + 1}/300 R={Rs[-1]:.3f} varq={Vq[-1]:.4f} "
              f"corr={Cq[-1]:.3f}", flush=True)
R_fin = float(np.mean(Rs[-50:]))
if R_fin <= 0.45:
    classe = "H1_RÉVERSIBLE"
elif R_fin < 0.85:
    classe = "H2_HYSTÉRÉSIS"
else:
    classe = "H3_IRRÉVERSIBLE"
res = {"R": Rs, "varq": Vq, "corr_thq": Cq, "snapshots": snaps,
       "R_conv_A": round(R_A, 4), "R_final_B": round(R_fin, 4),
       "varq_finale": round(float(np.mean(Vq[-50:])), 5),
       "corr_finale": Cq[-1], "classe": classe, "critere": None}
json.dump(res, open(os.path.join(HERE, "resultats", "exp72.json"), "w"))
print(f"[72] RESULTAT {classe} R_fin={R_fin:.4f} varq_fin={res['varq_finale']} "
      f"corr_fin={Cq[-1]:.3f} (exploration, aucun verdict)")
