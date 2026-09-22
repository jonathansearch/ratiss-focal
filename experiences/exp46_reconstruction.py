"""TEST-46 : reconstruction post-choc (1000 pas). G : appareil TEST-42
(14 baseline + 3 choc + 1000 relâche). Q : appareil TEST-37 (60 + 3
choc K=0/sigma x10 + 1000 relâche). Ajustement segment post-choc :
single-exp / double-exp / linéaire (grille numpy). Hypothèse :
double-exp inverse (relaxation rapide + verrouillage lent).
Critère : double_exp gagne avec R²>0.9 sur G (Q = secondaire reporté).
Oscillations : pic spectral résiduel >10x moyenne -> OUI."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

# ---- G (tore, TEST-42) ----
NT = 160
tore0 = C.fond(seed=24)[:NT].copy()
PREFG = C.p_sig(tore0)
rng = np.random.default_rng(42)
g = tore0.copy()
serieG = []


def etape_g(g, al, sg):
    d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
    g = g + al * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
    return g + rng.normal(0, sg, g.shape)


for _ in range(14):
    g = etape_g(g, 0.1, 0.005)
    serieG.append(C.p_sig(g) / PREFG)
for _ in range(3):
    g = etape_g(g, -0.15, 0.05)
    serieG.append(C.p_sig(g) / PREFG)
print(f"[46] G pré-choc={np.mean(serieG[11:14]):.4f} choc={[round(x, 3) for x in serieG[14:17]]}", flush=True)
for k in range(1000):
    g = etape_g(g, 0.1, 0.005)
    serieG.append(C.p_sig(g) / PREFG)
    if (k + 1) % 250 == 0:
        print(f"[46] G ... relâche {k + 1}/1000 : {serieG[-1]:.4f}", flush=True)

# ---- Q (anneau Kuramoto, TEST-37) ----
NQ, KQ, DTQ, SIG = 24, 3.0, 0.3, 0.04
rngq = np.random.default_rng(46)
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
ANG = np.linspace(0, 2 * np.pi, NQ, endpoint=False)
PREFQ = C.p_sig(np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG),
                                 np.zeros(NQ)]))
th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)


def pas_q(K, sg):
    global th
    th = th + DTQ * (OMEGA + (K / NQ) * (
        adj * np.sin(th[None, :] - th[:, None])).sum(1))
    anc = np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG), np.zeros(NQ)])
    anc = anc + (anc / 2.2) * (0.15 * np.sin(th))[:, None]
    anc = anc + rngq.normal(0, sg, anc.shape)
    for i in range(NQ):
        anc[i] += 0.5 * ((anc[(i - 1) % NQ] + anc[(i + 1) % NQ]) / 2 - anc[i])
    return C.p_sig(anc) / PREFQ


serieQ = []
for _ in range(60):
    serieQ.append(pas_q(KQ, SIG))
for _ in range(3):
    serieQ.append(pas_q(0.0, SIG * 10))
for _ in range(1000):
    serieQ.append(pas_q(KQ, SIG))
print(f"[46] Q pré-choc={np.mean(serieQ[57:60]):.4f} final={np.mean(serieQ[-50:]):.4f}", flush=True)


# ---- ajustements ----
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
                       [(0.05, 0.6), (-0.5, 0.5), (1, 500)]),
        "double_exp": (lambda p: p[0] + p[1] * np.exp(-TAU / p[2]) + p[3] * np.exp(-TAU / p[4]),
                       [(0.05, 0.6), (-0.5, 0.5), (1, 60), (-0.5, 0.5), (60, 2000)]),
        "lineaire": (lambda p: p[0] + p[1] * TAU, [(0.05, 0.6), (-0.001, 0.001)]),
    }
    out = {}
    for nom, (fn, bornes) in cands.items():
        s, p = cherche(fn, bornes)
        out[nom] = {"R2": round(s, 4), "params": p}
    gagnant = max(out, key=lambda k: out[k]["R2"])
    Y = np.abs(np.fft.rfft(y - y.mean()))[1:] ** 2
    pic = float(Y.max() / Y.mean())
    return {"candidats": out, "gagnant": gagnant, "R2": out[gagnant]["R2"],
            "params": out[gagnant]["params"], "pic_spectral": round(pic, 2),
            "oscillations": bool(pic > 10)}


fitG = ajuste(serieG[17:])
fitQ = ajuste(serieQ[63:])
for nom, f in (("G", fitG), ("Q", fitQ)):
    print(f"[46] {nom}: " + " ".join(f"{k}={v['R2']}" for k, v in f["candidats"].items())
      + f" -> {f['gagnant']} pic={f['pic_spectral']}", flush=True)
plancher = float(np.mean(serieG[-50:]))
tau_cicat = None
if fitG["gagnant"] == "double_exp":
    tau_cicat = max(fitG["params"][2], fitG["params"][4])
ok = bool(fitG["gagnant"] == "double_exp" and fitG["R2"] > 0.9)
res = {"G": fitG, "Q_secondaire": fitQ, "plancher_final_G": round(plancher, 4),
       "rappel_TEST42": 0.2727, "tau_cicatrisation": tau_cicat,
       "hypothese": "double-exp inverse (rapide + verrouillage lent)",
       "critere": ok}
json.dump(res, open(os.path.join(HERE, "resultats", "exp46.json"), "w"), indent=1)
print(f"[46] RESULTAT gagnant_G={fitG['gagnant']} R2={fitG['R2']} "
      f"plancher={plancher:.4f} tau_cicat={tau_cicat} "
      f"oscillations_G={fitG['oscillations']} critere={ok}")
