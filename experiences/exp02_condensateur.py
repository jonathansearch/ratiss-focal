"""TEST-02 : condensateur Q_info. L'info pure se charge ? R7: python3 experiences/exp02_condensateur.py"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import condensateur as Q

fond_pts = C.fond(seed=24)
P_ref = C.p_sig(fond_pts)
bits = Q.charge(2048, seed=101)
H = Q.entropie(bits)
comp = Q.taille_compressee(bits.tobytes())
nuage = Q.injecter(fond_pts, bits, 60, seed=7)
P_apres = C.p_sig(nuage) / P_ref
res = {"n_bits": 2048, "entropie_bit_par_bit": round(H, 4),
       "octets": 2048, "compresse_octets": comp,
       "P_apres_injection_norme": round(P_apres, 4),
       "info_pure": bool(H > 0.95), "pas_effondre": bool(P_apres > 0.5)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp02.json"), "w"), indent=1)
print(f"[02] RESULTAT entropie={H:.4f} compresse={comp}o P/P_ref={P_apres:.4f} "
      f"info_pure={res['info_pure']} pas_effondre={res['pas_effondre']}")
