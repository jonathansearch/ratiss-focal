#!/usr/bin/env python3
"""TEST-74 V13 : loi de gravite focale (CORRIGE v2 : source entretenue, deficit).

Balayage 4 MU x 3 sigma ; 4 candidats sur d(r)=a_loin-a(r) ; meilleur = R2 max.
Loi R_h = k*MU^p ; critere : meme gagnant >=9/12 ET R2 moyen du gagnant > 0.9.
"""
import json
import numpy as np

N = 40; D = 0.05; TH = 0.30; T = 400
MUS = [0.5 * D, D, 2 * D, 4 * D]
SIGS = [0.02 * D, 0.05 * D, 0.1 * D]

cx = cy = N // 2
ii, jj = np.mgrid[0:N, 0:N]
ddx = np.minimum(np.abs(ii - cx), N - np.abs(ii - cx))
ddy = np.minimum(np.abs(jj - cy), N - np.abs(jj - cy))
rr = np.sqrt((ddx * D) ** 2 + (ddy * D) ** 2)
RMAX = float(rr.max())
xs = np.arange(N)
stripes = 0.6 * (0.5 + 0.5 * np.sin(2 * np.pi * xs / 8))


def profil(MU, SIG):
    th = np.zeros((N, N))
    th[N // 2:, :] = stripes[None, :]
    q = np.zeros((N, N))
    G = np.exp(-(ddx * ddx + ddy * ddy) * D * D / (2 * SIG * SIG))
    for _ in range(T):
        q = q + MU * G * (1 - q)
        lap = (np.roll(th, 1, 0) + np.roll(th, -1, 0) +
               np.roll(th, 1, 1) + np.roll(th, -1, 1) - 4 * th)
        th = th + D * lap
        kill = q > TH
        th[kill] -= q[kill]
        th[32:, :] = stripes[None, :]
    a = np.abs(th)
    a_far = float(a[rr > 0.5 * RMAX].mean())
    nb = 20
    edges = np.linspace(0, RMAX, nb + 1)
    rc, dc = [], []
    for b in range(nb):
        m = (rr >= edges[b]) & (rr < edges[b + 1])
        if m.sum() > 0:
            rc.append(float(0.5 * (edges[b] + edges[b + 1])))
            dc.append(float(a_far - a[m].mean()))
    return np.array(rc), np.array(dc), a_far


def r2(y, p):
    ss = float(((y - p) ** 2).sum()); st = float(((y - y.mean()) ** 2).sum())
    return 1 - ss / st if st > 0 else 0.0


def fits(rc, dc):
    out = {}
    # A : A/(r+eps)
    b = (1e18, 0.0, 0.0)
    for eps in np.linspace(0.001, RMAX, 200):
        X = 1.0 / (rc + eps)
        A = float((X @ dc) / (X @ X))
        res = float(((A * X - dc) ** 2).sum())
        if res < b[0]:
            b = (res, eps, A)
    out["A"] = (r2(dc, b[2] / (rc + b[1])), {"A": b[2], "eps": b[1]})
    # B : B/r^2
    X = 1.0 / np.maximum(rc, 1e-6) ** 2
    B = float((X @ dc) / (X @ X))
    out["B"] = (r2(dc, B * X), {"B": B})
    # C : C*exp(-r/l)
    b = (1e18, 0.0, 0.0)
    for l in np.linspace(0.01, RMAX, 200):
        X = np.exp(-rc / l)
        C = float((X @ dc) / (X @ X))
        res = float(((C * X - dc) ** 2).sum())
        if res < b[0]:
            b = (res, l, C)
    out["C"] = (r2(dc, b[2] * np.exp(-rc / b[1])), {"C": b[2], "l": b[1]})
    # D : constante
    out["D"] = (0.0, {"c": float(dc.mean())})
    return out


rows = []
for MU in MUS:
    for SIG in SIGS:
        rc, dc, a_far = profil(MU, SIG)
        fs = fits(rc, dc)
        win = max(fs, key=lambda k: fs[k][0])
        rows.append({"MU": MU, "SIG": SIG, "a_loin": a_far,
                     "R2": {k: round(v[0], 4) for k, v in fs.items()},
                     "gagnant": win, "params": fs[win][1]})
        print(f"[74] MU={MU / D:.1f}D SIG={SIG / D:.2f}D -> {win} "
              f"R2={fs[win][0]:.4f} a_loin={a_far:.3f}", flush=True)

from collections import Counter
c = Counter(r["gagnant"] for r in rows)
top, ntop = c.most_common(1)[0]
r2moy = float(np.mean([r["R2"][top] for r in rows if r["gagnant"] == top]))

# loi R_h = k*MU^p via l du modele C (gagnant) pour chaque MU (moyenne sur SIG)
Rh, MUl = [], []
for MU in MUS:
    ls = [r["params"]["l"] for r in rows
          if r["MU"] == MU and "l" in r["params"]]
    if ls:
        MUl.append(MU); Rh.append(float(np.mean(ls)))
p = k = None
if len(MUl) >= 3 and all(v > 0 for v in Rh):
    p, lnk = np.polyfit(np.log(MUl), np.log(Rh), 1)
    p, k = float(p), float(np.exp(lnk))

res = {"test": 74, "lignes": rows, "gagnant_global": top,
       "compte": ntop, "R2_moyen_gagnant": r2moy,
       "loi": {"k": k, "p": p, "Rh_par_MU": Rh},
       "critere": bool(ntop >= 9 and r2moy > 0.9)}
json.dump(res, open("resultats/exp74.json", "w"), indent=1)
print("[74] RESULTAT gagnant=%s %d/12 R2moy=%.4f loi p=%s critere=%s"
      % (top, ntop, r2moy, p, res["critere"]))
