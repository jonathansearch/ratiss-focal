"""TEST-92 : holonomie — un puits qui fait le tour imprime-t-il une phase ?
Anneau NQ=24 + hubs (K=3, DT=0.3, graines 55/100), UN puits (s=0.5, G0=1.0)
dont le centre tourne : c(t) = s_dir * 2pi * t/TLOOP, TLOOP=600.
3 runs (même init) : statique (c=0 fixe), +tour, -tour.
Sonde = oscillateur 0 : phase déroulée accumulée sur le run.
On regarde : PHI_stat, PHI_plus, PHI_moins ; si (plus-stat) = -(moins-stat)
non nul -> phase géométrique (le pli). + R finaux.
Observation pure, zéro verdict."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NQ, KQ, DTQ, TLOOP, G0 = 24, 3.0, 0.3, 600, 1.0
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
ANG = np.linspace(0, 2 * np.pi, NQ, endpoint=False)


def dist(a, c):
    return np.abs(((a - c + np.pi) % (2 * np.pi)) - np.pi)


def run(mode):
    th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
    om0 = OMEGA.copy()
    acc = 0.0
    prev = th[0]
    R = []
    for t in range(TLOOP):
        if mode == "stat":
            c = 0.0
        elif mode == "plus":
            c = 2 * np.pi * t / TLOOP
        else:
            c = -2 * np.pi * t / TLOOP
        prof = np.exp(-dist(ANG, c) ** 2 / 0.5)
        om = om0 - G0 * prof
        th = th + DTQ * (om + (KQ / NQ) *
                         (adj * np.sin(th[None, :] - th[:, None])).sum(1))
        d = th[0] - prev
        acc += (d + np.pi) % (2 * np.pi) - np.pi
        prev = th[0]
        R.append(float(np.abs(np.exp(1j * th).mean())))
    return {"mode": mode, "PHI_sonde": round(float(acc), 3),
            "R_final": round(float(np.mean(R[-50:])), 4)}


res = [run(m) for m in ("stat", "plus", "moins")]
for r in res:
    print(f"[92] {r['mode']} : PHI={r['PHI_sonde']} R_fin={r['R_final']}",
          flush=True)
dp = round(res[1]["PHI_sonde"] - res[0]["PHI_sonde"], 3)
dm = round(res[2]["PHI_sonde"] - res[0]["PHI_sonde"], 3)
print(f"[92] delta_plus={dp} delta_moins={dm} (somme={round(dp + dm, 3)})",
      flush=True)
json.dump({"runs": res, "delta_plus": dp, "delta_moins": dm},
          open(os.path.join(HERE, "resultats", "exp92.json"), "w"), indent=1)
print("[92] OBSERVÉ : 3 runs archivés.")
