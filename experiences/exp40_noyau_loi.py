"""TEST-40 : loi du NOYAU RÉSIDUEL G. Scan alpha x sigma x N (3x3x3=27),
T=14, plancher = moyenne 4 derniers pas. Candidats : linéaire(α,σ,N),
(α,σ,logN), (α,σ,1/N). Critère : meilleur R² > 0.9."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

ALPHAS, SIGMAS, NS, T = [0.05, 0.1, 0.2], [0.0, 0.005, 0.02], [80, 160, 240], 14
table, rows = {}, []
for Nt in NS:
    tore0 = C.fond(n_tore=Nt, seed=24)[:Nt].copy()
    pref = C.p_sig(tore0)
    for al in ALPHAS:
        for sg in SIGMAS:
            rng = np.random.default_rng(4000 + int(al * 1000)
                                        + int(sg * 100000) + Nt)
            g = tore0.copy()
            serie = []
            for _ in range(T):
                d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
                g = g + al * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
                if sg > 0:
                    g = g + rng.normal(0, sg, g.shape)
                serie.append(C.p_sig(g) / pref)
            floor = float(np.mean(serie[-4:]))
            table[f"a={al}_s={sg}_N={Nt}"] = round(floor, 4)
            rows.append((al, sg, Nt, floor))
            print(f"[40] a={al} s={sg} N={Nt} plancher={floor:.4f}", flush=True)


def r2_fit(X, y):
    X = np.column_stack([X, np.ones(len(y))])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ b
    y = np.array(y)
    ss = float(((y - pred) ** 2).sum())
    return 1 - ss / max(float(((y - y.mean()) ** 2).sum()), 1e-12), \
        [round(float(x), 5) for x in b]


A = np.array([[al, sg] for al, sg, _, _ in rows])
y = np.array([f for _, _, _, f in rows])
fits = {}
cands = [("N", [Nt for _, _, Nt, _ in rows], y),  # M24 : + logF, invA
         ("logN", [np.log(Nt) for _, _, Nt, _ in rows], y),
         ("invN", [1 / Nt for _, _, Nt, _ in rows], y),
         ("logF", [Nt for _, _, Nt, _ in rows], np.log(y))]
for nom, col, yy in cands:
    r2, coef = r2_fit(np.column_stack([A, col]), yy)
    fits[nom] = {"R2": round(r2, 4), "coef": coef}
    print(f"[40] fit {nom}: R2={r2:.4f}", flush=True)
XA = np.column_stack([[1 / al for al, _, _, _ in rows], A[:, 1],
                      [Nt for _, _, Nt, _ in rows]])
r2a, coefa = r2_fit(XA, y)
fits["invA"] = {"R2": round(r2a, 4), "coef": coefa}
print(f"[40] fit invA: R2={r2a:.4f}", flush=True)
meilleur = max(fits, key=lambda k: fits[k]["R2"])
res = {"table": table, "fits": fits, "meilleur": meilleur,
       "R2": fits[meilleur]["R2"], "critere": bool(fits[meilleur]["R2"] > 0.9)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp40.json"), "w"), indent=1)
print(f"[40] RESULTAT meilleur={meilleur} R2={res['R2']} critere={res['critere']}")
