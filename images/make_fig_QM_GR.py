#!/usr/bin/env python3
"""Figure QM-GR : 6 observations (79-84), 2x3 panneaux, zéro verdict."""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(os.path.dirname(HERE), "experiences", "resultats")
d = {n: json.load(open(os.path.join(R, f"exp{n}.json"))) for n in range(79, 85)}

fig, ax = plt.subplots(2, 3, figsize=(12, 7))

# 79 : R vs desaccord, un puits
L = d[79]["lignes"]
ax[0, 0].plot([x["G0"] for x in L], [x["R_final"] for x in L], "ko-")
for x in L:
    ax[0, 0].text(x["G0"], x["R_final"] + 0.02, f"t={x['twist']:g}", fontsize=7,
                  ha="center")
ax[0, 0].set_xlabel("G0 (ralentissement)")
ax[0, 0].set_ylabel("R final")
ax[0, 0].set_title("(79) Q pres d'un puits : R baisse, twist 0/1")

# 80 : R vs desaccord, deux puits
L = d[80]["lignes"]
ax[0, 1].plot([x["G0"] for x in L], [x["R_final"] for x in L], "ko-")
for x in L:
    ax[0, 1].text(x["G0"], x["R_final"] + 0.03, f"t={x['twist']:g}", fontsize=7,
                  ha="center")
ax[0, 1].set_xlabel("G0")
ax[0, 1].set_ylabel("R final")
ax[0, 1].set_title("(80) Q entre deux puits : twist -2 a G0=1")

# 81 : lentille
L = d[81]["lignes"]
bs = [x["b"] for x in L if x["deflexion_deg"] is not None]
an = [x["deflexion_deg"] for x in L if x["deflexion_deg"] is not None]
ax[0, 2].plot(bs, an, "ko-", ms=4)
ax[0, 2].axhline(0, color="gray", lw=0.8)
ax[0, 2].set_xlabel("b (impact)")
ax[0, 2].set_ylabel("deflexion (deg)")
ax[0, 2].set_title("(81) lentille : S antisymetrique, 0 capture")

# 82 : ombres
for x in d[82]["lignes"]:
    ax[1, 0].plot(x["profil"], label=f"r_h={x['r_h']} c={x['contraste']}")
ax[1, 0].set_xlabel("r (cellules)")
ax[1, 0].set_ylabel("a(r)")
ax[1, 0].set_title("(82) horizon absorbant : l'ombre apparait")
ax[1, 0].legend(fontsize=7)

# 83 : memoire en espace courbe
for x in d[83]["lignes"]:
    s = np.array(x["R_serie"])
    ax[1, 1].plot(np.arange(len(s)) * 10, s, label=f"G0={x['G0']}")
ax[1, 1].axvline(400, color="gray", ls="--", lw=1)
ax[1, 1].set_xlabel("pas (separation a 400)")
ax[1, 1].set_ylabel("R")
ax[1, 1].set_title("(83) memoire RUQ-3 : finB 0.73 -> 0.25")
ax[1, 1].legend(fontsize=7)

# 84 : redshift
L = d[84]["lignes"]
ax[1, 2].plot([x["d"] for x in L], [x["freq"] for x in L], "ko-")
ax[1, 2].set_xlabel("d (distance au puits)")
ax[1, 2].set_ylabel("frequence moyenne")
ax[1, 2].set_title("(84) redshift : freq monte avec d")

fig.suptitle("QM-virtuel + relativite : ce qu'on voit quand ils cohabitent (TEST-79 a 84)")
fig.tight_layout()
out = os.path.join(HERE, "plot_QM_GR.png")
fig.savefig(out, dpi=110)
print("figure :", out)
