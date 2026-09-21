"""TEST-11 : tryperposition. Collapse d'une couche -> la sync survit ?"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import couches as L
import conteneur as C

rng = np.random.default_rng(11)
fond_pts = C.fond(seed=24)
N = 20  # tirages (6 = trop peu pour juger, corrigé)
pre = {"macro": [], "micro": []}
for _ in range(N):
    c = L.decouper(fond_pts + rng.normal(0, 0.01, fond_pts.shape))
    pre["macro"].append(L.p_couche(c["macro"]))
    pre["micro"].append(L.p_couche(c["micro"]))
macro_ampute = fond_pts[:160][rng.choice(160, 112, replace=False)]  # -30% (collapse)
post = {"macro": [], "micro": []}
for _ in range(6):
    bruits = rng.normal(0, 0.01, fond_pts.shape)
    c = {"macro": macro_ampute + bruits[:112] * 0 + rng.normal(0, 0.01, (112, 3)),
         "micro": fond_pts[160:250] + bruits[160:250]}
    post["macro"].append(L.p_couche(c["macro"]))
    post["micro"].append(L.p_couche(c["micro"]))
c_pre = abs(L.corr(pre["macro"], pre["micro"]))
c_post = abs(L.corr(post["macro"], post["micro"]))
ratio = round(c_post / max(c_pre, 1e-9), 3)
res = {"sync_avant": round(c_pre, 4), "sync_apres": round(c_post, 4),
       "ratio": ratio, "preservée": bool(ratio > 0.7)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp11.json"), "w"), indent=1)
print(f"[11] RESULTAT avant={c_pre:.3f} apres={c_post:.3f} preservée={res['preservée']}")
