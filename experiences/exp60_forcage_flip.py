"""TEST-60 : forçage du flip par impulsion de phase. Protocole : settle60
+ choc standard 3 pas -> mesure Qf0 (pré : HIGH>=0.84 / LOW<=0.82) ->
INJECTION : th = phi_inj + N(0,0.05) (resync forcée, K restauré) ->
relâche 300 -> Qf. phi_inj dans {k*pi/4, k=0..7}, 2 bras pré (HIGH/LOW),
8 valides visés/cellule. M26 : cap tentatives 25->60 (1er run : 13/16
cellules valides, motif déterministe déjà visible ; complément de
puissance) + fix NameError ctrl. P_HIGH par cellule (ambigu exclu du
ratio, >30% ambigu = cellule invalide). Classes : CONTRÔLABLE (un phi
avec P_HIGH>=0.9 dans LES 2 bras, ou P_LOW>=0.9 dans les 2) / PARTIEL
(>=0.9 dans 1 seul bras) / STOCHASTIQUE / MIXTE (<14/16 valides).
Critère : CONTRÔLABLE."""
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
PHIS = [round(k * np.pi / 4, 4) for k in range(8)]


def essai(seed, phi):
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

    for _ in range(60):
        pas(KQ, SIG)
    for _ in range(3):
        pas(0.0, SIG * 10)
    qf0 = float(np.mean([pas(KQ, SIG) for _ in range(60)][-50:]))
    th = phi + rng.normal(0, 0.05, NQ)
    qf = float(np.mean([pas(KQ, SIG) for _ in range(300)][-50:]))
    return qf0, qf


def etat(q):
    if q >= 0.84:
        return "HIGH"
    if q <= 0.82:
        return "LOW"
    return "AMBIGU"


carte = []
for pi, phi in enumerate(PHIS):
    for bi, pre in enumerate(("HIGH", "LOW")):
        hs, ls, amb = 0, 0, 0
        for t in range(60):
            if hs + ls + amb >= 8:
                break
            qf0, qf = essai(60000 + pi * 1000 + bi * 500 + t, phi)
            if etat(qf0) != pre:
                continue
            e = etat(qf)
            if e == "HIGH":
                hs += 1
            elif e == "LOW":
                ls += 1
            else:
                amb += 1
        n = hs + ls + amb
        valide = n >= 6 and (amb / n <= 0.3 if n else False)
        denom = hs + ls
        carte.append({"phi": phi, "pre": pre, "HIGH": hs, "LOW": ls,
                      "AMBIGU": amb, "valide": valide,
                      "P_HIGH": round(hs / denom, 3) if denom else None})
        print(f"[60] phi={phi:.3f} pre={pre} : H={hs} L={ls} A={amb} "
              f"P_HIGH={carte[-1]['P_HIGH']}", flush=True)
val = [c for c in carte if c["valide"]]
classe, ctrl = "MIXTE", None
if len(val) >= 14:
    for phi in PHIS:
        cells = [c for c in val if c["phi"] == phi]
        if len(cells) == 2:
            ph = [c["P_HIGH"] for c in cells]
            if all(p is not None and p >= 0.9 for p in ph):
                ctrl = "HIGH"
            if all(p is not None and p <= 0.1 for p in ph):
                ctrl = "LOW"
    if ctrl:
        classe = "CONTRÔLABLE"
    elif any(c["P_HIGH"] is not None and (c["P_HIGH"] >= 0.9 or c["P_HIGH"] <= 0.1) for c in val):
        classe = "PARTIEL"
    else:
        classe = "STOCHASTIQUE"
res = {"carte": carte, "cellules_valides": f"{len(val)}/16",
       "direction": ctrl, "classe": classe,
       "critere": bool(classe == "CONTRÔLABLE")}
json.dump(res, open(os.path.join(HERE, "resultats", "exp60.json"), "w"), indent=1)
print(f"[60] RESULTAT valides={len(val)}/16 classe={classe} "
      f"direction={ctrl} critere={res['critere']}")
