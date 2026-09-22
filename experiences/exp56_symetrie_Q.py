"""TEST-56 : symétrie LOW->HIGH (miroir TEST-53). Deux bras, sonde
standard (K=0, 3 pas, sigma x10) + 300 relâche : bras HIGH (départ
Qf>=0.84) et bras LOW (départ Qf<=0.82), 15 valides visés par bras.
M25 : cap tentatives 40->80 (1er run : HIGH n=13/40, médiane déjà hors
bande ; complément de puissance, pas pêche). Médianes post-sonde
med_H, med_L. Classes :
SYMÉTRIQUE (med_H<=0.82 ET med_L>=0.84) / CONVERGENT (|med_H-med_L|
<=0.03 -> équilibre Qbar=moyenne poolée) / DÉRIVE_BAS (les deux <=0.82)
/ DÉRIVE_HAUT (les deux >=0.84) / MIXTE. Critère : classe nette
(>=15 valides par bras)."""
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


def make_pas(seed):
    rng = np.random.default_rng(seed)
    th = rng.uniform(0, 2 * np.pi, NQ)

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

    return pas


def bras(voulu, seed0):
    res = []
    for t in range(80):
        if len(res) >= 15:
            break
        pas = make_pas(seed0 + t)
        for _ in range(60):
            pas(KQ, SIG)
        for _ in range(3):
            pas(0.0, SIG * 10)
        qf0 = float(np.mean([pas(KQ, SIG) for _ in range(300)][-50:]))
        if voulu == "HIGH" and qf0 < 0.84:
            continue
        if voulu == "LOW" and qf0 > 0.82:
            continue
        for _ in range(3):
            pas(0.0, SIG * 10)
        qf1 = float(np.mean([pas(KQ, SIG) for _ in range(300)][-50:]))
        res.append(round(qf1, 4))
    return res


h = bras("HIGH", 56000)
l = bras("LOW", 57000)
print(f"[56] bras HIGH: n={len(h)} bras LOW: n={len(l)}", flush=True)
med_h = float(np.median(h)) if h else None
med_l = float(np.median(l)) if l else None
print(f"[56] med_H={med_h} med_L={med_l}", flush=True)
qbar = None
if len(h) >= 15 and len(l) >= 15:
    if med_h <= 0.82 and med_l >= 0.84:
        classe = "SYMÉTRIQUE"
    elif abs(med_h - med_l) <= 0.03:
        classe = "CONVERGENT"
        qbar = round(float(np.mean(h + l)), 4)
    elif med_h <= 0.82 and med_l <= 0.82:
        classe = "DÉRIVE_BAS"
    elif med_h >= 0.84 and med_l >= 0.84:
        classe = "DÉRIVE_HAUT"
    else:
        classe = "MIXTE"
else:
    classe = "MIXTE"
res = {"post_HIGH": h, "post_LOW": l, "med_H": med_h, "med_L": med_l,
       "Qbar": qbar, "classe": classe,
       "critere": bool(classe != "MIXTE")}
json.dump(res, open(os.path.join(HERE, "resultats", "exp56.json"), "w"), indent=1)
print(f"[56] RESULTAT classe={classe} Qbar={qbar} critere={res['critere']}")
