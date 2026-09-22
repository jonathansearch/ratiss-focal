"""TEST-53 : profondeur du bassin d'attraction Q. Bandes TEST-50 :
HIGH Qf>=0.84, LOW Qf<=0.82 (entre = ambigu, rejeté). Par essai :
settle60+choc+relâche300 -> si HIGH, sonde (K=0, 3 pas, sigma=I) +
relâche300 -> HIGH ou LOW ? Intensités I=sigma_sonde/0.4 :
{0.25,0.5,1,2,4}. Par niveau : 30 tentatives max, 12 valides visés.
P_switch(I), I_50 (1er I avec P>=0.5). ROBUSTE si I_50>1 ou aucun ;
FRAGILE si I_50<=1 ; MIXTE si <3 niveaux avec >=8 valides.
Critère : ROBUSTE ou FRAGILE (classe nette + E_a identifiée)."""
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


def make_run(seed):
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


def etat(qf):
    if qf >= 0.84:
        return "HIGH"
    if qf <= 0.82:
        return "LOW"
    return "AMBIGU"


INTENS = [0.25, 0.5, 1.0, 2.0, 4.0]
courbe = []
for li, I in enumerate(INTENS):
    sg_sonde = 0.4 * I
    valides, switch = 0, 0
    for t in range(30):
        if valides >= 12:
            break
        pas = make_run(53000 + li * 100 + t)
        for _ in range(60):
            pas(KQ, SIG)
        for _ in range(3):
            pas(0.0, SIG * 10)
        qf0 = float(np.mean([pas(KQ, SIG) for _ in range(300)][-50:]))
        if etat(qf0) != "HIGH":
            continue
        for _ in range(3):
            pas(0.0, sg_sonde)
        qf1 = float(np.mean([pas(KQ, SIG) for _ in range(300)][-50:]))
        e1 = etat(qf1)
        if e1 == "AMBIGU":
            continue
        valides += 1
        switch += (e1 == "LOW")
    p = switch / valides if valides else None
    courbe.append({"I": I, "valides": valides, "switch": switch,
                  "P": round(p, 3) if p is not None else None})
    print(f"[53] I={I} : {switch}/{valides} P={courbe[-1]['P']}", flush=True)
bons = [c for c in courbe if c["valides"] >= 8]
if len(bons) < 3:
    classe, I50 = "MIXTE", None
else:
    I50 = next((c["I"] for c in courbe
                if c["P"] is not None and c["P"] >= 0.5), None)
    classe = "ROBUSTE" if (I50 is None or I50 > 1) else "FRAGILE"
res = {"courbe": courbe, "I_50_Ea": I50, "classe": classe,
       "critere": bool(classe in ("ROBUSTE", "FRAGILE"))}
json.dump(res, open(os.path.join(HERE, "resultats", "exp53.json"), "w"), indent=1)
print(f"[53] RESULTAT I_50={I50} classe={classe} critere={res['critere']}")
