"""Figure sonde v3 : 3 signaux x {calme, choc} — volatilité + flags."""
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
                     "font.size": 9})
TEAL, CYAN, ORANGE = "#39d0d8", "#7ff0f5", "#ffa94d"
d = json.load(open(f"{R}/exp66.json"))
fig, axes = plt.subplots(3, 2, figsize=(11, 8), sharex=True)
for i, nom in enumerate(("syncQ", "Phi", "Psig")):
    for j, regime in enumerate(("calme", "choc")):
        ax = axes[i][j]
        r = d["runs"][f"{nom}_{regime}"]
        v = np.array(r["volatilite"])
        f = np.array([int(b) for b in r["bits"]])
        ax.plot(v, color=TEAL, lw=1)
        ax.axhline(r["seuils"][1], color=ORANGE, ls="--", lw=1.2)
        ax.scatter(np.where(f)[0], v[f == 1], color=CYAN, s=12, zorder=3)
        if regime == "choc":
            ax.axvspan(200, 203, color=ORANGE, alpha=0.25)
        vstat = d["verdicts"][nom]
        tag = f"rafale={vstat['rafale_choc']} pire={vstat['pire_calme']} " \
            f"{'PASS' if vstat['PASS'] else 'FAIL'}" if regime == "choc" else ""
        ax.set_title(f"{nom} {regime} {tag}", fontsize=10)
        ax.grid(True, alpha=0.3)
        if i == 2:
            ax.set_xlabel("pas (choc = bande orange, pas 200-202)")
        if j == 0:
            ax.set_ylabel("volatilité + flags")
fig.suptitle("TEST-66 sonde v3 : la sonde sent les chocs (rafales 11-13) "
             "mais la dérive calme rafale aussi — horizon de mémoire trop court",
             fontsize=11, color="white")
fig.tight_layout()
fig.savefig(f"{HERE}/plot_sonde_v3.png", dpi=110)
print("plot_sonde_v3.png ok")
