"""TEST-52 : phase Kuramoto initiale vs attracteur final. 40 runs Q
(60 settle + 3 choc + 300 relâche, phases init uniformes seed 5200+j).
Prédicteurs : phase moyenne circulaire <phi0>, synchronie initiale R0.
Bimodalité : trou max > 0.04 avec >=8 runs de chaque côté.
Classes : DÉTERMINISTE (seuil sur prédicteur, exactitude >=85%) /
STOCHASTIQUE (bimodal sans seuil) / MONOSTABLE. Critère : DÉTERMINISTE."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

NQ, KQ, DTQ, SIG = 24, 3.0, 0.3, 0.04
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
ANG = np.linspace(0, 2 * np.pi, NQ, endpoint=False)
PREF = C.p_sig(np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG),
                                np.zeros(NQ)]))


def run(seed):
    rng = np.random.default_rng(seed)
    th0 = rng.uniform(0, 2 * np.pi, NQ)
    z0 = np.exp(1j * th0).mean()
    circ, R0 = float(np.angle(z0)), float(abs(z0))
    th = th0.copy()

    def pas(K, sg):
        nonlocal th
        th = th + DTQ * (OMEGA + (K / NQ) * (
            adj * np.sin(th[None, :] - th[:, None])).sum(1))
        anc = np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG),
                               np.zeros(NQ)])
        anc = anc + (anc / 2.2) * (0.15 * np.sin(th))[:, None]
        anc = anc + rng.normal(0, sg, anc.shape)
        for i in range(NQ):
            anc[i] += 0.5 * ((anc[(i - 1) % NQ] + anc[(i + 1) % NQ]) / 2
                             - anc[i])
        return C.p_sig(anc) / PREF

    for _ in range(60):
        pas(KQ, SIG)
    for _ in range(3):
        pas(0.0, SIG * 10)
    seg = [pas(KQ, SIG) for _ in range(300)]
    return {"circ": round(circ, 4), "R0": round(R0, 4),
            "Qf": round(float(np.mean(seg[-50:])), 4)}


runs = [run(5200 + j) for j in range(40)]
qfs = sorted(r["Qf"] for r in runs)
gaps = [(qfs[i + 1] - qfs[i], i) for i in range(len(qfs) - 1)]
gmax, imax = max(gaps)
bimodal = bool(gmax > 0.04 and imax + 1 >= 8 and 40 - imax - 1 >= 8)
print(f"[52] Qf min={qfs[0]:.4f} max={qfs[-1]:.4f} trou_max={gmax:.4f} "
      f"bimodal={bimodal}", flush=True)
classe, seuil, exact = "MONOSTABLE", None, None
centres = None
if bimodal:
    seuil_q = (qfs[imax] + qfs[imax + 1]) / 2
    bas = [r for r in runs if r["Qf"] <= seuil_q]
    haut = [r for r in runs if r["Qf"] > seuil_q]
    centres = [round(float(np.mean([r["Qf"] for r in bas])), 4),
               round(float(np.mean([r["Qf"] for r in haut])), 4)]
    labels = [0 if r["Qf"] <= seuil_q else 1 for r in runs]
    best = (0, None, None)
    for pred in ("circ", "R0"):
        vals = sorted(set(r[pred] for r in runs))
        for a, b in zip(vals[:-1], vals[1:]):
            t = (a + b) / 2
            for sens in (0, 1):
                pred_l = [sens if r[pred] > t else 1 - sens for r in runs]
                acc = sum(p == l for p, l in zip(pred_l, labels)) / 40
                if acc > best[0]:
                    best = (acc, pred, round(t, 4))
    exact, pred_nom, seuil = best[0], best[1], best[2]
    classe = "DÉTERMINISTE" if exact >= 0.85 else "STOCHASTIQUE"
    print(f"[52] centres={centres} seuil_Q={seuil_q:.4f} meilleur: "
          f"{pred_nom}={seuil} exact={exact:.3f}", flush=True)
res = {"Qf": [r["Qf"] for r in runs], "trou_max": round(gmax, 4),
       "bimodal": bimodal, "centres": centres, "classe": classe,
       "predicteur": pred_nom if bimodal else None, "seuil": seuil,
       "exactitude": round(exact, 3) if exact is not None else None,
       "critere": bool(classe == "DÉTERMINISTE")}
pred_nom = res["predicteur"]
json.dump(res, open(os.path.join(HERE, "resultats", "exp52.json"), "w"), indent=1)
print(f"[52] RESULTAT classe={classe} critere={res['critere']}")
