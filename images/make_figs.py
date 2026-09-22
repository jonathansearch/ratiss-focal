"""Figures README (données réelles TEST-48/52/58/60/61). Style dark teal."""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
R = "/home/user/ratiss-focal-local/experiences/resultats"
plt.rcParams.update({"figure.facecolor": "#0b1e24", "axes.facecolor": "#0e2830",
                     "text.color": "white", "axes.labelcolor": "white",
                     "xtick.color": "white", "ytick.color": "white",
                     "axes.edgecolor": "#2a5a66", "grid.color": "#1d4049",
                     "font.size": 11})
TEAL, CYAN, ORANGE, GREY = "#39d0d8", "#7ff0f5", "#ffa94d", "#8aa6ad"

# ---- 1. Sanctuaire U : courbe S(σ) combinée TEST-58 + TEST-61 ----
d58 = json.load(open(f"{R}/exp58.json"))
d61 = json.load(open(f"{R}/exp61.json"))
fig, ax = plt.subplots(figsize=(9, 5))
s58 = [p["sigma"] for p in d58["points"]]
y58 = [p["partage"] / 30 for p in d58["points"]]
i58 = [p["indep"] / 30 for p in d58["points"]]
s61 = [p["sigma"] for p in d61["points"]]
y61 = [p["partage"] / 50 for p in d61["points"]]
i61 = [p["indep"] / 50 for p in d61["points"]]
ax.plot(s58, y58, "o-", color=TEAL, lw=2.5, ms=6, label="Partage U (TEST-58, n=30)")
ax.plot(s61, y61, "s-", color=CYAN, lw=2.5, ms=6, label="Partage U (TEST-61, n=50)")
ax.plot(s58, i58, ":", color=GREY, lw=1.5, label="Contrôle indépendant")
ax.plot(s61, i61, ":", color=GREY, lw=1.5)
ax.axvline(0.06, color=ORANGE, ls="--", lw=2, label="σc = 0.06 (sigmoïde R²=0.964)")
ax.axvspan(0.008, 0.03, color=TEAL, alpha=0.12)
ax.text(0.019, 0.97, "sanctuaire\nparfait", color=TEAL, ha="center", va="top", fontsize=10)
ax.set_xlabel("Bruit ambiant σ")
ax.set_ylabel("Taux de partage S_U")
ax.set_title("Le sanctuaire U : robuste sous σc, érosion douce au-delà (pas de mort à 0.30)")
ax.set_xlim(0.005, 0.305)
ax.legend(loc="lower left", fontsize=9)
ax.grid(True, alpha=0.4)
fig.tight_layout()
fig.savefig(f"{HERE}/plot_sanctuaire.png", dpi=110)
print("plot_sanctuaire.png ok")

# ---- 2. Escalier G : H3 saturante ----
d48 = json.load(open(f"{R}/exp48.json"))
g = np.array(d48["Gmin"])
p = d48["candidats"]["H3_saturante"]["params"]
N = np.arange(7)
fit = p[0] + p[1] * np.exp(-p[2] * N)
Nf = np.linspace(0, 6, 200)
fitf = p[0] + p[1] * np.exp(-p[2] * Nf)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(N, g, "o", color=TEAL, ms=9, label="Gmin mesuré (6 chocs + baseline)")
ax.plot(Nf, fitf, "-", color=CYAN, lw=2.5,
        label=f"H3 : 0.083 + 0.26·e^(−3N), R²=0.978")
ax.axhline(p[0], color=ORANGE, ls="--", lw=2, label=f"Noyau absolu = {p[0]}")
ax.fill_between([0, 6.3], 0.06, 0.11, color=TEAL, alpha=0.10)
ax.text(5.2, 0.105, "bande\n[0.06, 0.11]", color=TEAL, fontsize=10)
ax.set_xlabel("Nombre de chocs N")
ax.set_ylabel("Plancher Gmin(N)")
ax.set_title("Escalier G : le premier choc effondre, les suivants brassent (H1/H2 réfutés)")
ax.set_xlim(-0.2, 6.4)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.4)
fig.tight_layout()
fig.savefig(f"{HERE}/plot_escalier_H3.png", dpi=110)
print("plot_escalier_H3.png ok")

# ---- 3. Flip pilotable : carte φ × pré ----
d60 = json.load(open(f"{R}/exp60.json"))
phis = sorted(set(c["phi"] for c in d60["carte"]))
mat = np.array([[next(c["P_HIGH"] if c["P_HIGH"] is not None else 0.5
                 for c in d60["carte"] if c["phi"] == ph and c["pre"] == pre)
                 for ph in phis] for pre in ("HIGH", "LOW")])
fig, ax = plt.subplots(figsize=(9, 4.2))
im = ax.imshow(mat, cmap="cool", vmin=0, vmax=1, aspect="auto")
ax.set_xticks(range(len(phis)))
ax.set_xticklabels([f"{p:.2f}" for p in phis], rotation=30)
ax.set_yticks([0, 1])
ax.set_yticklabels(["pré-HIGH", "pré-LOW"])
for i in range(2):
    for j in range(len(phis)):
        ax.text(j, i, f"{mat[i, j]:.1f}", ha="center", va="center",
                color="white" if 0.25 < mat[i, j] < 0.75 else "black",
                fontsize=10, fontweight="bold")
ax.set_xlabel("Phase injectée φ (rad) — [0,π]→LOW · {5π/4, 3π/2}→HIGH · 7π/4 transition")
ax.set_title("TEST-60 : P(HIGH | φ) — la phase pilote le flip à P=1.0 (CONTRÔLABLE, 14/16)")
fig.colorbar(im, ax=ax, label="P(HIGH)")
fig.tight_layout()
fig.savefig(f"{HERE}/plot_flip_phase.png", dpi=110)
print("plot_flip_phase.png ok")

# ---- 4. Continuum Q : histogramme n=40 ----
d52 = json.load(open(f"{R}/exp52.json"))
qfs = np.array(d52["Qf"])
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(qfs, bins=12, color=TEAL, edgecolor="#0b1e24", alpha=0.9)
ax.axvline(qfs.mean(), color=ORANGE, ls="--", lw=2,
           label=f"moyenne {qfs.mean():.3f}")
ax.set_xlabel("Q-final post-choc")
ax.set_ylabel("Runs (n=40)")
ax.set_title("TEST-52 : continuum [0.76, 0.91], trou max 0.018 — MONOSTABLE (bistabilité réfutée)")
ax.legend(fontsize=10)
ax.grid(True, alpha=0.4, axis="y")
fig.tight_layout()
fig.savefig(f"{HERE}/plot_continuum_Q.png", dpi=110)
print("plot_continuum_Q.png ok")
