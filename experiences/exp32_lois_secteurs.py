"""TEST-32 (M23) : lois de secteurs, forme FINALE. S_grav (proto) : décroissance
LINÉAIRE puis NOYAU RÉSIDUEL. S_quant (proto) : saturation EXPONENTIELLE
r = 1 - a.e^(-kt) (pas logit : Kuramoto n'a pas de démarrage lent en S)."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

rng = np.random.default_rng(32)
tore0 = C.fond(seed=24)[:160].copy()
PREF_G = C.p_sig(tore0)
g = tore0.copy()
PG = []
for _ in range(16):
    d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
    g = g + 0.1 * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
    g = g + rng.normal(0, 0.005, g.shape)
    PG.append(C.p_sig(g) / PREF_G)
NQ, KQ, DTQ = 24, 3.0, 0.3
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
RQ = []
for _ in range(60):
    th = th + DTQ * (OMEGA + (KQ / NQ) * (
        adj * np.sin(th[None, :] - th[:, None])).sum(1))
    RQ.append(float(np.abs(np.exp(1j * th).mean())))
print(f"[32] G : {PG[0]:.3f} -> {PG[-1]:.3f} | Q : {RQ[0]:.3f} -> {RQ[-1]:.3f}",
      flush=True)


def r2_line(x, y):
    a, b = np.polyfit(x, y, 1)
    pred = a * np.array(x) + b
    y = np.array(y)
    return 1 - float(((y - pred) ** 2).sum()) / max(
        float(((y - y.mean()) ** 2).sum()), 1e-12)


PGa = np.array(PG)
r2_lin10 = r2_line(range(10), PGa[:10])
noyau = float(PGa[-4:].mean())
pente_noyau = abs(float(np.polyfit(range(4), PGa[-4:], 1)[0]))
rq = np.clip(RQ, 0.02, 0.999)
r2_sat = r2_line(range(60), np.log(1 - rq))
p1, _ = np.polyfit(range(15), RQ[:15], 1)
p2, _ = np.polyfit(range(15), RQ[-15:], 1)
sat = float(p2 / max(p1, 1e-9))
opposes = bool((PGa[-1] - PGa[0]) * (rq[-1] - rq[0]) < 0)
res = {"S_grav_lin_R2": round(r2_lin10, 4),
       "S_quant_expsat_R2": round(r2_sat, 4),
       "noyau_residuel": round(noyau, 4),
       "pente_noyau": round(pente_noyau, 4),
       "saturation_ratio_Q": round(sat, 4),
       "sens_opposes": opposes,
       "critere": bool(r2_lin10 > 0.9 and pente_noyau < 0.02
                       and r2_sat > 0.9 and sat < 0.5 and opposes)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp32.json"), "w"), indent=1)
print(f"[32] RESULTAT lin10={r2_lin10:.3f} noyau={noyau:.3f} "
      f"pente={pente_noyau:.4f} expsat={r2_sat:.3f} sat={sat:.3f} "
      f"critere={res['critere']}")
