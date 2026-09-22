#!/usr/bin/env python3
"""TEST-75 V13 : horloges pres de la singularite (CORRIGE v2 : horloges libres).

v1 imposait l'oscillation aux sondes (frequence mesuree = frequence imposee).
v2 honnete : 24 sondes LIBRES (regle focale pure), frappees UNE fois a t=50 ;
chaque sonde relaxe ; on ajuste |th-base| ~ exp(-t/tau) -> tau(r) = periode
de l'horloge locale. DILATEE : tau augmente pres du centre.
"""
import json
import numpy as np

N = 40; D = 0.05; TH = 0.30
MU = 0.02 * D; SIG = 0.05 * D
T = 600; TKICK = 100

th = np.zeros((N, N))
q = np.zeros((N, N))
cx = cy = N // 2
ii, jj = np.mgrid[0:N, 0:N]
ddx = np.minimum(np.abs(ii - cx), N - np.abs(ii - cx))
ddy = np.minimum(np.abs(jj - cy), N - np.abs(jj - cy))
G = np.exp(-(ddx * ddx + ddy * ddy) * D * D / (2 * SIG * SIG))
rr = np.sqrt((ddx * D) ** 2 + (ddy * D) ** 2)

sondes = [(2 + 2 * i, cy) for i in range(12)] + [(cx, 2 + 2 * i) for i in range(12)]
series = {s: [] for s in sondes}
for t in range(1, T + 1):
    q = q + MU * G * (1 - q)
    lap = (np.roll(th, 1, 0) + np.roll(th, -1, 0) +
           np.roll(th, 1, 1) + np.roll(th, -1, 1) - 4 * th)
    th = th + D * lap
    kill = q > TH
    th[kill] -= q[kill]
    if t == TKICK:
        for s in sondes:
            th[s] += 1.0
    if t >= TKICK:
        for s in sondes:
            series[s].append(float(th[s]))
    if t % 150 == 0:
        print(f"[75] pas {t}/{T} qmax={q.max():.3f}", flush=True)

taus = {}
for s in sondes:
    y = np.abs(np.array(series[s][-300:]))
    y = y - y[-50:].mean() + 1e-9
    y = np.maximum(y, 1e-9)
    tt = np.arange(len(y))
    try:
        slope = np.polyfit(tt, np.log(y), 1)[0]
        tau = float(-1 / slope) if slope < 0 else float("inf")
    except Exception:
        tau = float("inf")
    if not np.isfinite(tau) or tau <= 0 or tau > 1e6:
        tau = None
    taus[s] = tau

lignes = [(s, float(rr[s]), taus[s]) for s in sondes]
valides = [(s, r, t) for (s, r, t) in lignes if t is not None]
valides.sort(key=lambda x: x[1])
print(f"[75] sondes valides {len(valides)}/24 qmax={q.max():.3f}", flush=True)
for s, r, t in valides:
    print(f"[75] sonde {s} r={r:.3f} tau={t:.1f}", flush=True)

if len(valides) >= 8:
    inner = [t for _, _, t in valides[:8]]
    outer = [t for _, _, t in valides[-8:]]
    mi, mo = float(np.mean(inner)), float(np.mean(outer))
    if mi > 1.2 * mo:
        classe = "DILATEE"
    elif mi < 0.8 * mo:
        classe = "INVERSEE"
    else:
        classe = "PLATE"
else:
    mi = mo = None; classe = "PLATE"

res = {"test": 75, "classe": classe, "tau_inner": mi, "tau_outer": mo,
       "valides": len(valides),
       "taus": [{"sonde": list(s), "r": r, "tau": t} for s, r, t in lignes],
       "critere": bool(classe == "DILATEE")}
json.dump(res, open("resultats/exp75.json", "w"), indent=1)
print("[75] RESULTAT classe=%s tau_in=%s tau_out=%s critere=%s"
      % (classe, mi, mo, res["critere"]))
