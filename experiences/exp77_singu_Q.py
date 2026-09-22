"""TEST-77 : singularité vs sync Q (capture d'oscillateurs). Anneau
NQ=24 + hubs (K=3, DT=0.3, graines 55/100). Singularité à angle 0 :
les k oscillateurs les plus proches voient leur phase re-tirée
uniforme à chaque pas (avalés). R = moy. 20 derniers (100 pas).
k dans {0,2,4,6,8,10}. k_c = 1er k avec R<0.5 (sync détruite) ;
RÉSISTANT si R(10)>=0.5. Critère : k_c identifié (la capture peut
tuer la sync)."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NQ, KQ, DTQ = 24, 3.0, 0.3
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
ANG = np.linspace(0, 2 * np.pi, NQ, endpoint=False)
prox = np.argsort(np.abs((ANG + np.pi) % (2 * np.pi) - np.pi))


def run(k):
    rng = np.random.default_rng(7700 + k)
    th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
    cap = set(prox[:k].tolist())
    R = []
    for _ in range(100):
        th = th + DTQ * (OMEGA + (KQ / NQ) * (
            adj * np.sin(th[None, :] - th[:, None])).sum(1))
        for i in cap:
            th[i] = rng.uniform(0, 2 * np.pi)
        R.append(float(np.abs(np.exp(1j * th).mean())))
    return round(float(np.mean(R[-20:])), 4)


pts = []
for k in (0, 2, 4, 6, 8, 10):
    r = run(k)
    pts.append({"k": k, "R": r})
    print(f"[77] k={k} : R={r}", flush=True)
kc = next((p["k"] for p in pts if p["R"] < 0.5), None)
classe = f"K_C={kc}" if kc is not None else "RÉSISTANT"
res = {"points": pts, "k_c": kc, "classe": classe,
       "critere": bool(kc is not None)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp77.json"), "w"), indent=1)
print(f"[77] RESULTAT {classe} critere={res['critere']}")
