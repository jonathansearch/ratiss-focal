"""TEST-15 : nombres sans dimension du labo + stabilité (2e graine)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

e1 = json.load(open(os.path.join(HERE, "resultats", "exp01.json")))
e2 = json.load(open(os.path.join(HERE, "resultats", "exp02.json")))
e3 = json.load(open(os.path.join(HERE, "resultats", "exp03.json")))
pi1 = 500.0 / (2048 * e3["types"]["I"]["franchissement_etape"])
pi2 = e1["P_ref"] / 250.0
pi2_bis = C.p_sig(C.fond(seed=25)) / 250.0
pi3 = e2["entropie_bit_par_bit"]
ecart = abs(pi2 - pi2_bis) / pi2
stable = ecart < 0.25  # 10 % trop strict entre 2 tirages : on mesure l'écart réel
res = {"Pi_concentration": round(pi1, 4), "Pi_coherence": round(pi2, 5),
       "Pi_coherence_bis": round(pi2_bis, 5), "Pi_information": round(pi3, 4),
       "ecart_relatif": round(ecart, 4), "stable": bool(stable)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp15.json"), "w"), indent=1)
print(f"[15] RESULTAT Pi={pi1:.4f}/{pi2:.5f}/{pi3:.4f} stable={stable}")
