"""TEST-31 : non-réduction. RED (Q expliqué par G seul) vs COH (loi propre +
couplage), dans les deux sens. RED échoue + COH gagne = unification par
cohérence, pas par réduction. Recoupe exp30 (12 premiers pas identiques)."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

T, SIG, NQ = 30, 0.04, 24
KQ, DTQ = 3.0, 0.3
rng = np.random.default_rng(30)
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
g = tore0.copy()
th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
PG, PQ = [], []
for t in range(T):
    sync_q = float(np.abs(np.exp(1j * th).mean()))
    d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
    g = g + 0.1 * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
    g = g + np.array([0.06, 0.0, 0.0]) + rng.normal(0, SIG, g.shape)
    n = int(round(24 * sync_q))
    if n:
        a = np.linspace(0, 2 * np.pi, n, endpoint=False)
        g = np.vstack([g, np.column_stack(
            [1.6 * np.cos(a) + g[:, 0].mean(), 1.6 * np.sin(a), np.zeros(n)])])
    th = th + DTQ * (OMEGA + (KQ / NQ) * (
        adj * np.sin(th[None, :] - th[:, None])).sum(1))
    anc = np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG), np.zeros(NQ)])
    anc = anc + g.mean(0) + (anc / 2.2) * (0.15 * np.sin(th))[:, None]
    anc = anc + rng.normal(0, SIG, anc.shape)
    for i in range(NQ):
        anc[i] += 0.5 * ((anc[(i - 1) % NQ] + anc[(i + 1) % NQ]) / 2 - anc[i])
    PG.append(C.p_sig(g) / PREF_G)
    PQ.append(C.p_sig(anc) / PREF_Q)
    if (t + 1) % 10 == 0:
        print(f"[31] ... pas {t + 1}/30", flush=True)
e30 = json.load(open(os.path.join(HERE, "resultats", "exp30.json")))
assert np.allclose(PG[:12], e30["coup_G"], atol=1e-3), "dérive vs exp30 (G) !"
assert np.allclose(PQ[:12], e30["coup_Q"], atol=1e-3), "dérive vs exp30 (Q) !"
print("[31] recoupe exp30 : OK (12 pas identiques)", flush=True)


def fit(X, y):
    X = np.column_stack([X, np.ones(len(y))])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ b
    ss = float(((y - pred) ** 2).sum())
    r2 = 1 - ss / max(float(((y - y.mean()) ** 2).sum()), 1e-12)
    return ss, round(r2, 4)


PGa, PQa = np.array(PG), np.array(PQ)
ss_rQ, r2_rQ = fit(PGa[:-1], PQa[1:])
ss_cQ, r2_cQ = fit(np.column_stack([PQa[:-1], PGa[:-1]]), PQa[1:])
ss_rG, r2_rG = fit(PQa[:-1], PGa[1:])
ss_cG, r2_cG = fit(np.column_stack([PGa[:-1], PQa[:-1]]), PGa[1:])
ratioQ, ratioG = ss_cQ / max(ss_rQ, 1e-12), ss_cG / max(ss_rG, 1e-12)
res = {"RED_Q_par_G": {"R2": r2_rQ}, "COH_Q": {"R2": r2_cQ},
       "ratio_Q": round(ratioQ, 3),
       "RED_G_par_Q": {"R2": r2_rG}, "COH_G": {"R2": r2_cG},
       "ratio_G": round(ratioG, 3),
       "critere": bool(r2_rQ < 0.1 and r2_rG < 0.1  # M14 : RED morte...
                       and ratioQ < 1.0 and ratioG < 1.0),  # ...+ joint meilleur
       "note": "décisif côté G (0.454), indicatif côté Q (0.836, observable bruitée)"}
json.dump(res, open(os.path.join(HERE, "resultats", "exp31.json"), "w"), indent=1)
print(f"[31] RESULTAT RED R2=({r2_rQ},{r2_rG}) COH R2=({r2_cQ},{r2_cG}) "
      f"ratios=({ratioQ:.3f},{ratioG:.3f}) critere={res['critere']}")
