"""TEST-12 v2 : influence = terme d'interaction (non-additivité).
Sans contact (loin) vs avec contact (pont). I_min : bruit indépendant vs commun."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import couches as L
import conteneur as C

rng = np.random.default_rng(12)
fond_pts = C.fond(seed=24)
Y0 = fond_pts[160:250]
loin = np.column_stack([np.cos(np.linspace(0, 2 * np.pi, 20, endpoint=False)) * 1.5,
                        np.sin(np.linspace(0, 2 * np.pi, 20, endpoint=False)) * 1.5,
                        np.zeros(20)])
xx = np.linspace(1.4, 2.1, 20)  # pont : comble le vide tore->sphère
pont = np.column_stack([xx, np.zeros(20), np.zeros(20)])


def interaction(ajout):
    pY = np.mean([L.p_couche(Y0 + rng.normal(0, 0.01, Y0.shape)) for _ in range(4)])
    pA = np.mean([L.p_couche(ajout + rng.normal(0, 0.01, ajout.shape)) for _ in range(4)])
    ens = np.vstack([Y0, ajout])
    pJ = np.mean([L.p_couche(ens + rng.normal(0, 0.01, ens.shape)) for _ in range(4)])
    return (pJ - pY - pA) / len(ajout)


I_loin = interaction(loin)
I_pont = interaction(pont)
sx = [L.p_couche(fond_pts[:160] + rng.normal(0, 0.01, (160, 3))) for _ in range(8)]
sy = [L.p_couche(Y0 + rng.normal(0, 0.01, Y0.shape)) for _ in range(8)]
i_indep = abs(L.corr(sx, sy))
facteurs = 1 + rng.normal(0, 0.02, 8)  # dilatation COMMUNE (translation = invisible)
sx2 = [L.p_couche(fond_pts[:160] * facteurs[i]) for i in range(8)]
sy2 = [L.p_couche(Y0 * facteurs[i]) for i in range(8)]
i_commun = abs(L.corr(sx2, sy2))
res = {"I_sans_contact": round(I_loin, 5), "I_avec_contact": round(I_pont, 5),
       "contact_compte": bool(I_pont > I_loin + 0.001),
       "I_min_independant": round(i_indep, 4),
       "I_min_commun": round(i_commun, 4),
       "couplage_reel": bool(i_commun > i_indep)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp12.json"), "w"), indent=1)
print(f"[12] RESULTAT I_loin={I_loin:.5f} I_pont={I_pont:.5f} "
      f"contact={res['contact_compte']} Imin {i_indep:.3f}->{i_commun:.3f}")
