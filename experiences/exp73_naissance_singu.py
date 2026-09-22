#!/usr/bin/env python3
"""TEST-73 V13 SINGULARITE : naissance d'une singularite + horizon (CORRIGE v2).

Fix : q_max(T=250)=0.22 < TH=0.30 -> le tueur ne declenchait jamais.
v2 : T=600 (q_centre -> 0.45 > TH), source rayures entretenue loin du centre
(lignes 32-39repinglees), trou = cellules a < 0.5*a_loin.
Deficit d(r) = a_loin - a(r) ajuste en A/(r+eps) ; R_h = eps_ajuste.
"""
import json
import numpy as np

N = 40; D = 0.05; TH = 0.30
MU = 0.02 * D          # impose chef
SIG = 0.05 * D         # impose chef
T = 600

th = np.zeros((N, N))
xs = np.arange(N)
stripes = 0.6 * (0.5 + 0.5 * np.sin(2 * np.pi * xs / 8))
th[N // 2:, :] = stripes[None, :]
q = np.zeros((N, N))
cx = cy = N // 2

ii, jj = np.mgrid[0:N, 0:N]
ddx = np.minimum(np.abs(ii - cx), N - np.abs(ii - cx))
ddy = np.minimum(np.abs(jj - cy), N - np.abs(jj - cy))
G = np.exp(-(ddx * ddx + ddy * ddy) * D * D / (2 * SIG * SIG))
rr = np.sqrt((ddx * D) ** 2 + (ddy * D) ** 2)

RMAX = float(rr.max())
mass_hist = []
for t in range(1, T + 1):
    q = q + MU * G * (1 - q)
    lap = (np.roll(th, 1, 0) + np.roll(th, -1, 0) +
           np.roll(th, 1, 1) + np.roll(th, -1, 1) - 4 * th)
    th = th + D * lap
    kill = q > TH
    th[kill] -= q[kill]
    th[32:, :] = stripes[None, :]  # source entretenue loin du trou
    if t % 50 == 0 or t == T:
        a = np.abs(th)
        a_far = float(a[rr > 0.5 * RMAX].mean())
        mass = int((a < 0.5 * a_far).sum())
        mass_hist.append([t, mass])
        print(f"[73] pas {t}/{T} masse(trou)={mass} qmax={q.max():.3f}", flush=True)

a = np.abs(th)
a_far = float(a[rr > 0.5 * RMAX].mean())
print(f"[73] a_loin={a_far:.4f} a_centre={float(a[cx, cy]):.4f} qmax={q.max():.3f}", flush=True)

# --- profil radial de l'EXCES e(r) = a(r) - a_loin (puits, pas ombre) ---
nbins = 20
edges = np.linspace(0, RMAX, nbins + 1)
rc, ec = [], []
for b in range(nbins):
    m = (rr >= edges[b]) & (rr < edges[b + 1])
    if m.sum() > 0:
        rc.append(float(0.5 * (edges[b] + edges[b + 1])))
        ec.append(float(a[m].mean() - a_far))
rc = np.array(rc); ec = np.array(ec)

# --- ajustement e = A/(r+eps) : balayage eps, moindres carres sur A ---
best = (1e18, 0.0, 0.0)
for eps in np.linspace(0.001, RMAX, 400):
    X = 1.0 / (rc + eps)
    A = float((X @ ec) / (X @ X))
    res = float(((A * X - ec) ** 2).sum())
    if res < best[0]:
        best = (res, eps, A)
_, eps_fit, A_fit = best
pred = A_fit / (rc + eps_fit)
ss = float(((ec - pred) ** 2).sum())
st = float(((ec - ec.mean()) ** 2).sum())
R2 = 1 - ss / st if st > 0 else 0.0
R_h = float(eps_fit)
print(f"[73] exces: A={A_fit:.4f} R_h=eps={R_h:.4f} R2={R2:.4f} (RMAX={RMAX:.3f})", flush=True)
# --- modele exponentiel C*exp(-r/l) pour comparaison honnete ---
bestC = (1e18, 0.0, 0.0)
for l in np.linspace(0.01, RMAX, 400):
    X = np.exp(-rc / l)
    C = float((X @ ec) / (X @ X))
    res = float(((C * X - ec) ** 2).sum())
    if res < bestC[0]:
        bestC = (res, l, C)
R2C = 1 - bestC[0] / st if st > 0 else 0.0
print(f"[73] expo: C={bestC[2]:.4f} l={bestC[1]:.4f} R2={R2C:.4f}", flush=True)

res = {"test": 73, "MU": MU, "EPS": SIG, "T": T,
       "masse_hist": mass_hist, "masse_finale": mass_hist[-1][1],
       "qmax": float(q.max()), "a_loin": a_far,
       "A": A_fit, "R_h": R_h, "R2": R2, "RMAX": RMAX,
       "C": bestC[2], "l": bestC[1], "R2_expo": R2C,
       "critere": bool(R2 > 0.9 and 0 < R_h < RMAX)}
json.dump(res, open("resultats/exp73.json", "w"), indent=1)
print("[73] RESULTAT R_h=%.4f R2=%.4f (expo R2=%.4f) critere=%s" % (R_h, R2, R2C, res["critere"]))
