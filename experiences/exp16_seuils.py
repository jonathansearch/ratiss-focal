"""TEST-16 : seuils Phi_c par structure (boucle compacte vs nuage diffus)."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import couches as L

rng = np.random.default_rng(16)
a = np.linspace(0, 2 * np.pi, 10, endpoint=False)
boucle = np.column_stack([0.25 * np.cos(a), 0.25 * np.sin(a), np.zeros(10)])
diffus = rng.normal(0, 0.5, (40, 3))
structs = {"boucle": boucle, "diffus": diffus}
sigmas = [0.02, 0.05, 0.1, 0.2]
sigma_c = {}
for nom, s in structs.items():
    p0 = L.p_couche(s)
    surv = {}
    for sig in sigmas:
        rs = [L.p_couche(s + rng.normal(0, sig, s.shape)) / max(p0, 1e-9)
              for _ in range(4)]
        surv[str(sig)] = round(float(np.mean(rs)), 3)
    survit = [float(k) for k, v in surv.items() if v > 0.5]
    sigma_c[nom] = max(survit) if survit else 0.0
    print(f"[16] {nom}: survie={surv} -> sigma_c={sigma_c[nom]}", flush=True)
res = {"sigma_c": sigma_c, "seuils_differents": bool(sigma_c["boucle"] != sigma_c["diffus"])}
json.dump(res, open(os.path.join(HERE, "resultats", "exp16.json"), "w"), indent=1)
print(f"[16] RESULTAT seuils_differents={res['seuils_differents']}")
