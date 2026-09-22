"""TEST-70 : réversibilité de la fusion RUQ-1 (hystérésis collective ?).
Même RUQ-1 que TEST-69 (graine 7001). Phase A : 400 pas GROUPÉS
(convergence attendue R~0.98 ; barrière : R_50fin >= 0.85 sinon test
INVALIDE). Séparation BRUSQUE : téléportation dispersée (positions
uniformes), états internes (th, q) INCHANGÉS. Phase B : 300 pas balade,
on observe R(t), var(q)(t). Classification pré-enregistrée (R_fin =
moy. 50 derniers B) : H1 RÉVERSIBLE si R_fin <= 0.45 ; H2 HYSTÉRÉSIS
si 0.45 < R_fin < 0.85 ; H3 IRRÉVERSIBLE si R_fin >= 0.85.
Secondaire : t_half (1er t sous (R_A+R_fin)/2), varq finale vs 0.047.
Critère : convergence A atteinte ET classe nette (H1/H2/H3)."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

N, TA, TB = 12, 400, 300
K, DT, GAM = 2.0, 0.3, 1.0
ALPHA, BETA = 0.05, 0.1
rng = np.random.default_rng(7001)
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


def pas_ruq(X, th, q, g):
    s = densites(X, g)
    dmat = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
    for i in range(N):
        vois = [j for j in range(N) if j != i and dmat[i, j] < RAYON]
        if vois:
            th[i] += DT * (K / N) * float(np.sin(th[vois] - th[i]).sum())
            q[i] += BETA * (float(q[vois].mean()) - q[i])
    th = th + DT * W0 + GAM * (s - 0.5) * DT
    q = q + ALPHA * (s - q)
    return th, q


Rs, Vq = [], []
for t in range(TA):
    g = etape(g)
    th, q = pas_ruq(X, th, q, g)
    c = g.mean(0)
    X = X + rng.normal(0, DIAG / 100, (N, 3))
    rel = X - c
    nrm = np.linalg.norm(rel, axis=1, keepdims=True)
    X = np.where(nrm > DIAG / 20, c + rel / nrm * DIAG / 20, X)
    Rs.append(round(float(np.abs(np.exp(1j * th).mean())), 4))
    Vq.append(round(float(q.var()), 5))
R_A = float(np.mean(Rs[-50:]))
print(f"[70] phase A : R_conv={R_A:.4f} varq={np.mean(Vq[-50:]):.5f}", flush=True)
if R_A < 0.85:
    res = {"classe": "INVALIDE", "critere": False,
           "raison": f"non-convergence A (R={R_A:.3f})"}
    json.dump(res, open(os.path.join(HERE, "resultats", "exp70.json"), "w"))
    print(f"[70] RESULTAT INVALIDE (R_A={R_A:.3f})")
    raise SystemExit
X = rng.uniform(bb0, bb1, (N, 3))
print("[70] séparation brusque (positions dispersées, th/q intacts)", flush=True)
for t in range(TB):
    g = etape(g)
    th, q = pas_ruq(X, th, q, g)
    X = X + STEP * np.column_stack(
        [np.cos(W * t + PH), np.sin(1.3 * W * t + PH),
         np.cos(0.7 * W * t + 2 * PH)]) + rng.normal(0, STEP / 3, (N, 3))
    X = np.clip(X, bb0 - DIAG * 0.25, bb1 + DIAG * 0.25)
    Rs.append(round(float(np.abs(np.exp(1j * th).mean())), 4))
    Vq.append(round(float(q.var()), 5))
    if (t + 1) % 100 == 0:
        print(f"[70] ... B+{t + 1}/300 R={Rs[-1]:.3f} varq={Vq[-1]:.4f}", flush=True)
R_fin = float(np.mean(Rs[-50:]))
mi = (R_A + R_fin) / 2
t_half = next((k for k in range(TB) if Rs[TA + k] < mi), None)
varq_fin = float(np.mean(Vq[-50:]))
if R_fin <= 0.45:
    classe = "H1_RÉVERSIBLE"
elif R_fin < 0.85:
    classe = "H2_HYSTÉRÉSIS"
else:
    classe = "H3_IRRÉVERSIBLE"
res = {"R": Rs, "varq": Vq, "R_conv_A": round(R_A, 4),
       "R_final_B": round(R_fin, 4), "t_half": t_half,
       "varq_finale": round(varq_fin, 5), "classe": classe, "critere": True}
json.dump(res, open(os.path.join(HERE, "resultats", "exp70.json"), "w"))
print(f"[70] RESULTAT {classe} R_fin={R_fin:.4f} t_half={t_half} "
      f"varq_fin={varq_fin:.5f} critere=True")
