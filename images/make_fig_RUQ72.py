"""Figure TEST-72 : RUQ-3 fusion -> séparation (t=400)."""
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
d = json.load(open(f"{R}/exp72.json"))
fig, (ax, axb) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
ax.plot(d["R"], color=TEAL, lw=1.5, label="R phase")
ax.set_ylabel("R phase", color=TEAL)
ax2 = ax.twinx()
ax2.plot(d["varq"], color=ORANGE, lw=1.5, label="var(charge)")
ax2.set_ylabel("var(charge)", color=ORANGE)
axb.plot(d["corr_thq"], color=CYAN, lw=1.2)
axb.set_ylabel("corr(θ,q)", color=CYAN)
axb.set_xlabel("pas (séparation brusque à t=400, graphe fixe conservé)")
for a in (ax, axb):
    a.axvline(400, color="white", ls="--", lw=2)
    a.set_xlim(0, 700)
    a.grid(True, alpha=0.3)
ax.text(200, 0.9, "GROUPÉS\n(R=0.99, λ2=12)", color=CYAN, ha="center",
        fontsize=11, fontweight="bold")
ax.text(550, 0.9, "SÉPARÉS\n(chute→0.05→R=0.73, λ2=2)", color=ORANGE,
        ha="center", fontsize=11, fontweight="bold")
ax.set_title("TEST-72 RUQ-3 : H2 HYSTÉRÉSIS — le graphe fixe resynchronise "
             "l'essaim dispersé (corr −0.76)", color="white")
fig.tight_layout()
fig.savefig(f"{HERE}/plot_RUQ72.png", dpi=110)
print("plot_RUQ72.png ok")
