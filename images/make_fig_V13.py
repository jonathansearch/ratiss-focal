#!/usr/bin/env python3
"""Figure V13 SINGULARITE : 3 panneaux (73 profil, 75 horloges, 77 capture)."""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RAC = os.path.dirname(HERE)
R = os.path.join(RAC, "experiences", "resultats")
d73 = json.load(open(os.path.join(R, "exp73.json")))
d75 = json.load(open(os.path.join(R, "exp75.json")))
d77 = json.load(open(os.path.join(R, "exp77.json")))

# --- panneau A : profil radial TEST-73 (recalcule, rapide) ---
N = 40; D = 0.05; TH = 0.30; MU = 0.02 * D; SIG = 0.05 * D; T = 600
th = np.zeros((N, N))
xs = np.arange(N)
stripes = 0.6 * (0.5 + 0.5 * np.sin(2 * np.pi * xs / 8))
th[N // 2:, :] = stripes[None, :]
q = np.zeros((N, N)); cx = cy = N // 2
ii, jj = np.mgrid[0:N, 0:N]
ddx = np.minimum(np.abs(ii - cx), N - np.abs(ii - cx))
ddy = np.minimum(np.abs(jj - cy), N - np.abs(jj - cy))
G = np.exp(-(ddx * ddx + ddy * ddy) * D * D / (2 * SIG * SIG))
rr = np.sqrt((ddx * D) ** 2 + (ddy * D) ** 2)
RMAX = float(rr.max())
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
nb = 20; edges = np.linspace(0, RMAX, nb + 1)
rc, ec = [], []
for b in range(nb):
    m = (rr >= edges[b]) & (rr < edges[b + 1])
    if m.sum() > 0:
        rc.append(float(0.5 * (edges[b] + edges[b + 1])))
        ec.append(float(a[m].mean() - a_far))
rc = np.array(rc); ec = np.array(ec)

fig, ax = plt.subplots(1, 3, figsize=(12, 3.6))
ax[0].plot(rc, ec, "ko", ms=4, label="excès mesuré")
A, e = d73["A"], d73["R_h"]
ax[0].plot(rc, A / (rc + e), "b--", label=f"A/(r+eps) R²={d73['R2']:.2f}")
C, l = d73["C"], d73["l"]
ax[0].plot(rc, C * np.exp(-rc / l), "r-", label=f"expo R²={d73['R2_expo']:.2f}")
ax[0].axhline(0, color="gray", lw=0.8)
ax[0].set_xlabel("r"); ax[0].set_ylabel("excès a(r)−a_loin")
ax[0].set_title("(a) TEST-73 : puits + anneau → expo, pas Newton")
ax[0].legend(fontsize=8)

# --- panneau B : horloges TEST-75 ---
val = [(p["r"], p["tau"]) for p in d75["taus"] if p["tau"] is not None]
rv = np.array([v[0] for v in val]); tv = np.array([v[1] for v in val])
ax[1].plot(rv, tv, "ko", ms=5)
ax[1].axhline(d75["tau_inner"], color="r", ls="--", label=f"tau_in={d75['tau_inner']:.1f}")
ax[1].axhline(d75["tau_outer"], color="b", ls="--", label=f"tau_out={d75['tau_outer']:.1f}")
ax[1].set_xlabel("r"); ax[1].set_ylabel("tau (pas)")
ax[1].set_title(f"(b) TEST-75 : horloges {d75['classe']} ({d75['valides']}/24)")
ax[1].legend(fontsize=8)

# --- panneau C : capture Q TEST-77 ---
ks = [p["k"] for p in d77["points"]]; Rs = [p["R"] for p in d77["points"]]
ax[2].plot(ks, Rs, "ko-", ms=6)
ax[2].axhline(0.5, color="r", ls="--", label="seuil R=0.5")
if d77["k_c"] is not None:
    ax[2].axvline(d77["k_c"], color="r", ls=":", label=f"k_c={d77['k_c']}")
ax[2].set_xlabel("k (oscillateurs avalés)"); ax[2].set_ylabel("R sync")
ax[2].set_title(f"(c) TEST-77 : capture → {d77['classe']}")
ax[2].legend(fontsize=8)

fig.suptitle("V13 SINGULARITÉ — le trou focal est un puits exponentiel (pas une ombre newtonienne)")
fig.tight_layout()
out = os.path.join(HERE, "plot_V13.png")
fig.savefig(out, dpi=110)
print("figure :", out)
