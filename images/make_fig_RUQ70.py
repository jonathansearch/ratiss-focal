"""Figure TEST-70 : fusion puis séparation brusque (t=400)."""
import json
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
d = json.load(open(f"{R}/exp70.json"))
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(d["R"], color=TEAL, lw=1.5, label="R phase")
ax.set_ylabel("R phase", color=TEAL)
ax2 = ax.twinx()
ax2.plot(d["varq"], color=ORANGE, lw=1.5, label="var(charge)")
ax2.set_ylabel("var(charge)", color=ORANGE)
ax.axvline(400, color="white", ls="--", lw=2)
ax.text(200, 0.95, "GROUPÉS\n(fusion R=0.98)", color=CYAN, ha="center",
        fontsize=11, fontweight="bold")
ax.text(550, 0.95, "SÉPARÉS\n(R→0.31, t_half=11)", color=ORANGE, ha="center",
        fontsize=11, fontweight="bold")
ax.set_xlabel("pas (séparation brusque à t=400)")
ax.set_title("TEST-70 : H1 RÉVERSIBLE — l'unité se dissout en ~11 pas, "
             "var(q) récupère (0.048). Pas de cicatrice.", color="white")
ax.set_xlim(0, 700)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(f"{HERE}/plot_RUQ70.png", dpi=110)
print("plot_RUQ70.png ok")
