"""TEST-25 (M7) : PLV séries LONGUES (N=1000, fenêtres de 50) = CONTRÔLE POSITIF.
Drive = boucle injectée/retirée en alternance (onde carrée commune, ne sature
pas) + bruit indépendant. Collapse 30 % natif. Ce qu'on teste : la sync est
STABLE (var) et SURVIT au collapse (tryperposition longue).
Critères INCHANGÉS : moyenne > 0.3, var < 0.05.
(M5 respiration : P_sig insensible par construction. M6 mémoire : saturait.)"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import couches as L
import conteneur as C

rng = np.random.default_rng(25)
NT, NS, T, W = 50, 30, 1000, 50
fond_pts = C.fond(n_tore=NT, n_sphere=NS, seed=24)
macro0 = fond_pts[:NT].copy()
micro0 = fond_pts[NT:NT + NS].copy()
bits = np.random.default_rng(101).integers(0, 2, 4000)


def boucle(centre, k):
    a = bits[k * 2:(k + 1) * 2]
    ang = np.linspace(0, 2 * np.pi, 8, endpoint=False) + a[0]
    r = 0.2 + 0.02 * a[1]
    return np.column_stack([centre[0] + r * np.cos(ang),
                            centre[1] + r * np.sin(ang),
                            np.full(8, centre[2])])


def serie(macro_nat):
    sm, sn = [], []
    for t in range(T):
        k = t // 5
        if k % 2 == 0:  # boucle PRÉSENTE (les 2 couches ensemble)
            mem_mac = boucle((1.5, 0, 0), k)
            mem_mic = boucle((2.6, 0, 0), k)
        else:           # boucle ABSENTE (les 2 couches ensemble)
            mem_mac = np.zeros((0, 3))
            mem_mic = np.zeros((0, 3))
        mac = np.vstack([macro_nat, mem_mac]) + rng.normal(
            0, 0.008, (len(macro_nat) + len(mem_mac), 3))
        mic = np.vstack([micro0, mem_mic]) + rng.normal(
            0, 0.008, (len(micro0) + len(mem_mic), 3))
        sm.append(L.p_couche(mac))
        sn.append(L.p_couche(mic))
        if (t + 1) % 250 == 0:
            print(f"[25] ... pas {t + 1}/1000 (macro natif {len(macro_nat)})",
                  flush=True)
    return sm, sn


def plv_fenetres(a, b):
    return [round(L.plv(a[i:i + W], b[i:i + W]), 4) for i in range(0, T, W)]


pre_m, pre_n = serie(macro0)
idx = rng.choice(len(macro0), int(len(macro0) * 0.7), replace=False)
post_m, post_n = serie(macro0[idx])
plv_pre, plv_post = plv_fenetres(pre_m, pre_n), plv_fenetres(post_m, post_n)
moy, var = float(np.mean(plv_pre)), float(np.var(plv_pre))
res = {"plv_pre": plv_pre, "plv_post": plv_post,
       "moyenne_pre": round(moy, 4), "variance_pre": round(var, 5),
       "moyenne_post": round(float(np.mean(plv_post)), 4),
       "preservation": round(float(np.mean(plv_post) / max(moy, 1e-9)), 3),
       "critere": bool(moy > 0.3 and var < 0.05)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp25.json"), "w"), indent=1)
print(f"[25] RESULTAT moy={moy:.4f} var={var:.5f} post={res['moyenne_post']} "
      f"critere={res['critere']}")
