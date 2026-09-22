"""TEST-71 : RUQ-2 à rétroaction charge<->phase — EXPLORATION OUVERTE.
RUQ-1 + boucle : dth += ALPHA*(q-qbar)*DT (la charge module la
fréquence) ET dq += BETA*sin(th-Psi) (la phase redistribue la charge ;
formulation circulaire-safe de la spec chef `dq += beta*phi`, les angles
bruts ayant des sauts 2π). ALPHA=0.5, BETA=0.05, graine 7101.
Protocole TEST-70 : 400 pas groupés (barrière R>=0.85 sinon INVALIDE)
-> séparation brusque -> 300 pas. OBSERVABLES : R(t), var(q)(t),
corr circulaire-linéaire (th,q) post-séparation, tau_relax (ajustement
exp de R), q min/max (stabilité). Classes descriptives H1/H2/H3
(mêmes seuils 0.45/0.85). Zéro critère de succès : on regarde, on
raconte. Même H1 est une donnée (feedback local insuffisant ?)."""
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
FB_A, FB_B = 0.5, 0.05
rng = np.random.default_rng(7101)
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


def pas_ruq2(X, th, q, g):
    s = densites(X, g)
    dmat = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
    for i in range(N):
        vois = [j for j in range(N) if j != i and dmat[i, j] < RAYON]
        if vois:
            th[i] += DT * (K / N) * float(np.sin(th[vois] - th[i]).sum())
            q[i] += BETA * (float(q[vois].mean()) - q[i])
    Psi = float(np.angle(np.exp(1j * th).mean()))
    th = th + DT * W0 + GAM * (s - 0.5) * DT + FB_A * (q - q.mean()) * DT
    q = q + ALPHA * (s - q) + FB_B * np.sin(th - Psi)
    return th, q


Rs, Vq = [], []
for t in range(TA):
    g = etape(g)
    th, q = pas_ruq2(X, th, q, g)
    c = g.mean(0)
    X = X + rng.normal(0, DIAG / 100, (N, 3))
    rel = X - c
    nrm = np.linalg.norm(rel, axis=1, keepdims=True)
    X = np.where(nrm > DIAG / 20, c + rel / nrm * DIAG / 20, X)
    Rs.append(round(float(np.abs(np.exp(1j * th).mean())), 4))
    Vq.append(round(float(q.var()), 5))
R_A = float(np.mean(Rs[-50:]))
print(f"[71] phase A : R_conv={R_A:.4f} varq={np.mean(Vq[-50:]):.5f} "
      f"q_range=[{q.min():.3f},{q.max():.3f}]", flush=True)
if R_A < 0.85:
    res = {"classe": "INVALIDE", "critere": None,
           "raison": f"non-convergence A (R={R_A:.3f})"}
    json.dump(res, open(os.path.join(HERE, "resultats", "exp71.json"), "w"))
    print(f"[71] RESULTAT INVALIDE (R_A={R_A:.3f})")
    raise SystemExit
X = rng.uniform(bb0, bb1, (N, 3))
print("[71] séparation brusque (positions dispersées, th/q intacts)", flush=True)
for t in range(TB):
    g = etape(g)
    th, q = pas_ruq2(X, th, q, g)
    X = X + STEP * np.column_stack(
        [np.cos(W * t + PH), np.sin(1.3 * W * t + PH),
         np.cos(0.7 * W * t + 2 * PH)]) + rng.normal(0, STEP / 3, (N, 3))
    X = np.clip(X, bb0 - DIAG * 0.25, bb1 + DIAG * 0.25)
    Rs.append(round(float(np.abs(np.exp(1j * th).mean())), 4))
    Vq.append(round(float(q.var()), 5))
    if (t + 1) % 100 == 0:
        print(f"[71] ... B+{t + 1}/300 R={Rs[-1]:.3f} varq={Vq[-1]:.4f} "
              f"q_range=[{q.min():.3f},{q.max():.3f}]", flush=True)
R_fin = float(np.mean(Rs[-50:]))
Rb = np.array(Rs[TA:])
tau = np.arange(TB, dtype=float)
best, tau_relax = -1e9, None
for tc in np.linspace(5, 400, 40):
    for Rf in np.linspace(0, 1, 21):
        for A0 in np.linspace(-1, 1, 21):
            pred = Rf + A0 * np.exp(-tau / tc)
            ss = float(((Rb - pred) ** 2).sum())
            s = 1 - ss / max(float(((Rb - Rb.mean()) ** 2).sum()), 1e-12)
            if s > best:
                best, tau_relax = s, round(float(tc), 1)
thB = np.angle(np.exp(1j * th))
cc = float(np.corrcoef(np.sin(thB - thB.mean()), q - q.mean())[0, 1]) \
    if q.std() > 1e-9 else 0.0
if R_fin <= 0.45:
    classe = "H1_RÉVERSIBLE"
elif R_fin < 0.85:
    classe = "H2_HYSTÉRÉSIS"
else:
    classe = "H3_IRRÉVERSIBLE"
res = {"R": Rs, "varq": Vq, "R_conv_A": round(R_A, 4),
       "R_final_B": round(R_fin, 4), "tau_relax": tau_relax,
       "R2_relax": round(float(best), 4),
       "corr_thq_post": round(cc, 4),
       "q_range_final": [round(float(q.min()), 3), round(float(q.max()), 3)],
       "classe": classe, "critere": None}
json.dump(res, open(os.path.join(HERE, "resultats", "exp71.json"), "w"))
print(f"[71] RESULTAT {classe} R_fin={R_fin:.4f} tau={tau_relax} "
      f"corr_thq={cc:.3f} (exploration, aucun verdict)")
