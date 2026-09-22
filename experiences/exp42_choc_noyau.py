"""TEST-42 : noyau sous CHOC extrême. 14 pas baseline (α=0.1 σ=0.005) -> 3 pas
choc (α=-0.15 expansion + σ=0.05 x10) -> 10 pas relâche. Classification :
DÉTRUIT (final<0.1) / ÉLASTIQUE (|final-pré|<=0.05 et std<=0.05) /
HYSTÉRÉTIQUE (std>0.05) / PLASTIQUE (nouveau plancher). Critère : survit."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

NT = 160
tore0 = C.fond(seed=24)[:NT].copy()
PREF = C.p_sig(tore0)
rng = np.random.default_rng(42)
g = tore0.copy()
serie = []


def etape(g, al, sg):
    d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
    g = g + al * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
    return g + rng.normal(0, sg, g.shape)


for _ in range(14):
    g = etape(g, 0.1, 0.005)
    serie.append(C.p_sig(g) / PREF)
print(f"[42] pré-choc : {serie[-1]:.4f}", flush=True)
for _ in range(3):
    g = etape(g, -0.15, 0.05)
    serie.append(C.p_sig(g) / PREF)
print(f"[42] choc : {[round(x, 3) for x in serie[14:17]]}", flush=True)
for _ in range(10):
    g = etape(g, 0.1, 0.005)
    serie.append(C.p_sig(g) / PREF)
s = np.array(serie)
pre, final, std5 = float(s[11:14].mean()), float(s[-3:].mean()), float(s[-5:].std())
if final < 0.1:
    classe = "DÉTRUIT"
elif abs(final - pre) <= 0.05 and std5 <= 0.05:
    classe = "ÉLASTIQUE"
elif std5 > 0.05:
    classe = "HYSTÉRÉTIQUE"
else:
    classe = "PLASTIQUE"
res = {"serie": [round(float(x), 4) for x in serie],
       "G_pre": round(pre, 4), "final": round(final, 4),
       "std5": round(std5, 4), "classe": classe,
       "critere": bool(classe != "DÉTRUIT")}
json.dump(res, open(os.path.join(HERE, "resultats", "exp42.json"), "w"), indent=1)
print(f"[42] RESULTAT pré={pre:.4f} final={final:.4f} std5={std5:.4f} "
      f"classe={classe} critere={res['critere']}")
