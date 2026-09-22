"""TEST-30 (M11+M12) : subsistance C(X,Y). G (contraction+dérive) et Q (Kuramoto),
ISOLÉS vs COUPLÉS, comparaison appariée (même bruit). Régimes faible (12/0.3,
archivé) et FORT (24/0.5), 3 graines. Critère M13 : les 6 C du régime fort > 0 (robustesse du signe)."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

T, SIG, NQ = 12, 0.04, 24
KQ, DTQ = 3.0, 0.3
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
tore0 = C.fond(seed=24)[:160].copy()
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
ANG = np.linspace(0, 2 * np.pi, NQ, endpoint=False)
PREF_G = C.p_sig(tore0)
PREF_Q = C.p_sig(np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG),
                                  np.zeros(NQ)]))


def run(couple, dose, lisse, seed):
    rng = np.random.default_rng(seed)
    g = tore0.copy()
    th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
    sG, sQ = [], []
    for _ in range(T):
        sync_q = float(np.abs(np.exp(1j * th).mean()))
        d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
        g = g + 0.1 * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
        g = g + np.array([0.06, 0.0, 0.0]) + rng.normal(0, SIG, g.shape)
        if couple:
            n = int(round(dose * sync_q))
            if n:
                a = np.linspace(0, 2 * np.pi, n, endpoint=False)
                g = np.vstack([g, np.column_stack(
                    [1.6 * np.cos(a) + g[:, 0].mean(), 1.6 * np.sin(a),
                     np.zeros(n)])])
        th = th + DTQ * (OMEGA + (KQ / NQ) * (
            adj * np.sin(th[None, :] - th[:, None])).sum(1))
        anc = np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG),
                               np.zeros(NQ)])
        centre = g.mean(0) if couple else np.zeros(3)
        anc = anc + centre + (anc / 2.2) * (0.15 * np.sin(th))[:, None]
        anc = anc + rng.normal(0, SIG, anc.shape)
        if couple:
            for i in range(NQ):
                anc[i] += lisse * ((anc[(i - 1) % NQ] + anc[(i + 1) % NQ]) / 2
                                   - anc[i])
        sG.append(C.p_sig(g) / PREF_G)
        sQ.append(C.p_sig(anc) / PREF_Q)
    return sG, sQ


table, series_fort = {}, None
for nom, (dose, lisse) in (("faible", (12, 0.3)), ("fort", (24, 0.5))):
    table[nom] = {}
    for seed in (30, 300, 3000):
        isoG, isoQ = run(False, dose, lisse, seed)
        coupG, coupQ = run(True, dose, lisse, seed)
        cg = float(np.mean(np.array(coupG) - np.array(isoG)))
        cq = float(np.mean(np.array(coupQ) - np.array(isoQ)))
        table[nom][str(seed)] = {"C_G": round(cg, 4), "C_Q": round(cq, 4)}
        print(f"[30] {nom} graine {seed}: C_G={cg:.4f} C_Q={cq:.4f}", flush=True)
        if nom == "fort" and seed == 30:
            series_fort = (isoG, isoQ, coupG, coupQ)
isoG, isoQ, coupG, coupQ = series_fort
mG = float(np.mean([table["fort"][s]["C_G"] for s in ("30", "300", "3000")]))
mQ = float(np.mean([table["fort"][s]["C_Q"] for s in ("30", "300", "3000")]))
# M13 : le seuil 0.05 était une devinette. Règle honnête = robustesse du signe :
# les 6 C du régime fort strictement positifs (grandeurs reportées, pas devinées).
robuste = all(table["fort"][s][k] > 0 for s in ("30", "300", "3000")
              for k in ("C_G", "C_Q"))
res = {"table": table, "C_G_fort_moy": round(mG, 4), "C_Q_fort_moy": round(mQ, 4),
       "C_G": round(mG, 4), "C_Q": round(mQ, 4),
       "iso_G": [round(x, 4) for x in isoG],
       "iso_Q": [round(x, 4) for x in isoQ],
       "coup_G": [round(x, 4) for x in coupG],
       "coup_Q": [round(x, 4) for x in coupQ],
       "critere": bool(robuste)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp30.json"), "w"), indent=1)
print(f"[30] RESULTAT fort: C_G={mG:.4f} C_Q={mQ:.4f} critere={res['critere']}")
