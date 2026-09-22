"""TEST-34 (M20) : marqueurs de coexistence (sur le couplé exp30).
(1) Limites douces : pas de falaise après burn-in (1er pas exclu :
transitoire d'allumage). (2) Causalité Q->G. (3) Référence partagée :
même échelle (moyennes dans [0.4, 1.2])."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
e30 = json.load(open(os.path.join(HERE, "resultats", "exp30.json")))
G = np.array(e30["coup_G"])
Q = np.array(e30["coup_Q"])


def doux(s):
    j = np.abs(np.diff(s))[1:]  # burn-in : 1er saut exclu
    portee = float(s.max() - s.min()) + 1e-9
    return bool(float(j.max()) < 0.2 and float(j.max()) < 0.5 * portee)


dG, dQ = doux(G), doux(Q)
causal = float(np.corrcoef(G[1:], Q[:-1])[0, 1])
mG, mQ = float(G.mean()), float(Q.mean())
ref = bool(0.4 <= mG <= 1.2 and 0.4 <= mQ <= 1.2)
res = {"limites_douces_G": dG, "limites_douces_Q": dQ,
       "saut_max_G_burnin": round(float(np.abs(np.diff(G))[1:].max()), 4),
       "saut_max_Q_burnin": round(float(np.abs(np.diff(Q))[1:].max()), 4),
       "moyenne_G": round(mG, 4), "moyenne_Q": round(mQ, 4),
       "causalite_QversG": round(causal, 4),
       "reference_partagee": ref,
       "critere": bool(dG and dQ and causal > 0.3 and ref)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp34.json"), "w"), indent=1)
print(f"[34] RESULTAT douceur=({dG},{dQ}) causal={causal:.3f} "
      f"moy=({mG:.3f},{mQ:.3f}) ref={ref} critere={res['critere']}")
