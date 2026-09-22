"""TEST-41 : collapse <-> noyau. 1 run pré (14 pas, baseline α=0.1 σ=0.005
N=160) puis branches : fractions {0.1,0.2,0.3,0.5} x 3 masques, 6 pas post.
Classification : INVARIANT (tous |ΔG|<0.01) vs COUPLÉ (|corr|>0.7) vs MIXTE.
Critère : classe nette (pas MIXTE)."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

NT, AL, SG = 160, 0.1, 0.005
tore0 = C.fond(seed=24)[:NT].copy()
PREF = C.p_sig(tore0)


def pas(g, rng):
    d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
    g = g + AL * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
    return g + rng.normal(0, SG, g.shape)


rng = np.random.default_rng(41)
g = tore0.copy()
pre = []
for _ in range(14):
    g = pas(g, rng)
    pre.append(C.p_sig(g) / PREF)
G_pre = float(np.mean(pre[-3:]))
print(f"[41] pré : plancher G_pre={G_pre:.4f}", flush=True)
deltas, rec = {}, []
for frac in (0.1, 0.2, 0.3, 0.5):
    for rep in range(3):
        r2 = np.random.default_rng(4100 + int(frac * 10) + rep)
        idx = r2.choice(len(g), int(len(g) * (1 - frac)), replace=False)
        h = g[idx].copy()
        post = []
        for _ in range(6):
            h = pas(h, r2)
            post.append(C.p_sig(h) / PREF)
        d = float(np.mean(post[-3:])) - G_pre
        deltas[f"f={frac}_r={rep}"] = round(d, 4)
        rec.append((frac, d))
        print(f"[41] frac={frac} rep={rep} ΔG={d:+.4f}", flush=True)
alld = np.array([d for _, d in rec])
invariant = bool(np.all(np.abs(alld) < 0.01))
corr = float(np.corrcoef([f for f, _ in rec], alld)[0, 1])
classe = "INVARIANT" if invariant else ("COUPLÉ" if abs(corr) > 0.7 else "MIXTE")
res = {"G_pre": round(G_pre, 4), "deltas": deltas,
       "corr_intensite": round(corr, 4), "classe": classe,
       "critere": bool(classe != "MIXTE")}
json.dump(res, open(os.path.join(HERE, "resultats", "exp41.json"), "w"), indent=1)
print(f"[41] RESULTAT classe={classe} corr={corr:.3f} critere={res['critere']}")
