"""Figure UKTZ : 3 essaims, balade (0-299) puis groupés (300-599)."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = "/home/user/ratiss-focal-local/experiences/resultats"
HERE = "/home/user/ratiss-focal-local/images"
plt.rcParams.update({"figure.facecolor": "#0b1e24", "axes.facecolor": "#0e2830",
                     "text.color": "white", "axes.labelcolor": "white",
                     "xtick.color": "white", "ytick.color": "white",
                     "axes.edgecolor": "#2a5a66", "grid.color": "#1d4049",
                     "font.size": 10})
TEAL, CYAN, ORANGE = "#39d0d8", "#7ff0f5", "#ffa94d"
d67 = json.load(open(f"{R}/exp67.json"))
d68 = json.load(open(f"{R}/exp68.json"))
d69 = json.load(open(f"{R}/exp69.json"))
fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)
axes[0].plot(d67["S"], color=TEAL, lw=1.5)
axes[0].set_title(f"UKTZ-S sémantique : similarité des codes "
                  f"{d67['S_balade']} → {d67['S_groupe']} (code partagé)")
axes[0].set_ylabel("sim. cosinus")
axes[1].plot(d68["R"], color=CYAN, lw=1.5)
axes[1].set_title(f"UKTZ-T topologique : ordre R "
                  f"{d68['R_balade']} → {d68['R_groupe']} (topologie fixe domine)")
axes[1].set_ylabel("ordre R")
ax = axes[2]
ax.plot(d69["R"], color=TEAL, lw=1.5, label="R phase")
ax.set_ylabel("R phase", color=TEAL)
ax2 = ax.twinx()
ax2.plot(d69["varq"], color=ORANGE, lw=1.5, label="var(charge)")
ax2.set_ylabel("var(charge)", color=ORANGE)
ax.set_title(f"RUQ-1 (invention) : R {d69['R_balade']} → {d69['R_groupe']}, "
             f"var(q) {d69['varq_balade']} → {d69['varq_groupe']} (transition)")
for a in axes:
    a.axvline(300, color=ORANGE, ls="--", lw=1.5)
    a.grid(True, alpha=0.3)
    a.set_xlim(0, 600)
axes[0].text(150, axes[0].get_ylim()[1] * 0.92, "BALADE", color="white",
             ha="center", fontsize=11, fontweight="bold")
axes[0].text(450, axes[0].get_ylim()[1] * 0.92, "GROUPÉS", color=ORANGE,
             ha="center", fontsize=11, fontweight="bold")
axes[2].set_xlabel("pas")
fig.suptitle("Programme UKTZ : trois essaims lâchés dans le tore, puis regroupés "
             "(exploration ouverte, aucun verdict)", fontsize=11, color="white")
fig.tight_layout()
fig.savefig(f"{HERE}/plot_neurons_uktz.png", dpi=110)
print("plot_neurons_uktz.png ok")
