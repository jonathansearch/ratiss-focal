"""TEST-50 : fatigue Q sous chocs cumulés. Appareil TEST-37 (graine 50).
60 settle + 6 x (3 choc K=0/sigma x10 + 300 relâche). Chaque segment
post-choc ajusté (single/double-exp) -> tau_lent(k), Q_final(k).
Classification : FATIGUE si dérive>5% ou tau x2 (N_bascule = premier k
avec Q_final<0.95xQ_final(1)) / INFATIGABLE si dérive<=5% et tau stable
+-50% / MIXTE sinon. Critère : classe nette (FATIGUE ou INFATIGABLE)."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

NQ, KQ, DTQ, SIG = 24, 3.0, 0.3, 0.04
rng = np.random.default_rng(50)
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
th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)


def pas_q(K, sg):
    global th
    th = th + DTQ * (OMEGA + (K / NQ) * (
        adj * np.sin(th[None, :] - th[:, None])).sum(1))
    anc = np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG), np.zeros(NQ)])
    anc = anc + (anc / 2.2) * (0.15 * np.sin(th))[:, None]
    anc = anc + rng.normal(0, sg, anc.shape)
    for i in range(NQ):
        anc[i] += 0.5 * ((anc[(i - 1) % NQ] + anc[(i + 1) % NQ]) / 2 - anc[i])
    return C.p_sig(anc) / PREF


serie = []
for _ in range(60):
    serie.append(pas_q(KQ, SIG))
segments = []
for k in range(1, 7):
    for _ in range(3):
        serie.append(pas_q(0.0, SIG * 10))
    seg = []
    for _ in range(300):
        v = pas_q(KQ, SIG)
        serie.append(v)
        seg.append(v)
    segments.append(seg)
    print(f"[50] choc {k}/6 : Q_final={np.mean(seg[-50:]):.4f}", flush=True)


def ajuste(y):
    y = np.array(y, float)
    TAU = np.arange(len(y), dtype=float)

    def r2(pred):
        pred = np.array(pred)
        ss = float(((y - pred) ** 2).sum())
        return 1 - ss / max(float(((y - y.mean()) ** 2).sum()), 1e-12)

    def cherche(fn, bornes, n=9, rondes=3):
        lo = np.array([b[0] for b in bornes], float)
        hi = np.array([b[1] for b in bornes], float)
        best, bestp = -1e9, None
        for _ in range(rondes):
            grilles = [np.linspace(lo[i], hi[i], n) for i in range(len(bornes))]
            for combo in np.array(np.meshgrid(*grilles)).T.reshape(-1, len(bornes)):
                try:
                    s = r2(fn(combo))
                except Exception:
                    continue
                if s > best:
                    best, bestp = s, combo.copy()
            span = (hi - lo) * 0.2
            lo = np.maximum([b[0] for b in bornes], bestp - span)
            hi = np.minimum([b[1] for b in bornes], bestp + span)
        return best, [round(float(x), 5) for x in bestp]

    cands = {
        "single_exp": (lambda p: p[0] + p[1] * np.exp(-TAU / p[2]),
                       [(0.3, 1.0), (-0.5, 0.5), (1, 300)]),
        "double_exp": (lambda p: p[0] + p[1] * np.exp(-TAU / p[2]) + p[3] * np.exp(-TAU / p[4]),
                       [(0.3, 1.0), (-0.5, 0.5), (1, 60), (-0.5, 0.5), (60, 1500)]),
    }
    out = {}
    for nom, (fn, bornes) in cands.items():
        s, p = cherche(fn, bornes)
        out[nom] = {"R2": round(s, 4), "params": p}
    gagnant = max(out, key=lambda k: out[k]["R2"])
    pr = out[gagnant]["params"]
    tau = pr[2] if gagnant == "single_exp" else max(pr[2], pr[4])
    return {"gagnant": gagnant, "R2": out[gagnant]["R2"], "tau_lent": tau,
            "Q_final": round(float(y[-50:].mean()), 4)}


carte = [ajuste(seg) for seg in segments]
for k, c in enumerate(carte, 1):
    print(f"[50] k={k} : {c['gagnant']} R2={c['R2']} tau={c['tau_lent']} "
          f"Qf={c['Q_final']}", flush=True)
qfs = [c["Q_final"] for c in carte]
taus = [c["tau_lent"] for c in carte]
derive = max(abs(q - qfs[0]) / qfs[0] for q in qfs)
tau_ratio = max(taus) / max(min(taus), 1e-9)
n_bas = next((k + 1 for k, q in enumerate(qfs) if q < 0.95 * qfs[0]), None)
if derive > 0.05 or tau_ratio >= 2:
    classe = "FATIGUE"
elif tau_ratio <= 1.5:
    classe = "INFATIGABLE"
else:
    classe = "MIXTE"
res = {"carte": carte, "derive_max": round(float(derive), 4),
       "tau_ratio": round(float(tau_ratio), 3), "N_bascule": n_bas,
       "classe": classe, "critere": bool(classe != "MIXTE")}
json.dump(res, open(os.path.join(HERE, "resultats", "exp50.json"), "w"), indent=1)
print(f"[50] RESULTAT derive={derive:.4f} tau_ratio={tau_ratio:.3f} "
      f"N_bas={n_bas} classe={classe} critere={res['critere']}")
