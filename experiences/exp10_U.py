"""TEST-10 : intrication universelle U. L'info lie les couches (U_charge > U_fond)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import condensateur as Q
import couches as L

fond_pts = C.fond(seed=24)
bits = Q.charge(2048, seed=101)
charge = Q.injecter(fond_pts, bits, 40, seed=7)


def U(pts):
    couches = L.decouper(pts)
    joint = C.p_sig(pts) if len(pts) >= 4 else 0.0
    somme = sum(L.p_couche(c) for c in couches.values())
    return joint - somme


u_fond, u_charge = U(fond_pts), U(charge)
s = json.load(open(os.path.join(HERE, "resultats", "exp08.json")))["series"]
res = {"U_fond": round(u_fond, 4), "U_charge": round(u_charge, 4),
       "lie_par_info": bool(abs(u_charge) > abs(u_fond) + 0.05),
       "plv_macro_micro": round(L.plv(s["macro"], s["micro"]), 4),
       "corr_macro_micro": round(L.corr(s["macro"], s["micro"]), 4)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp10.json"), "w"), indent=1)
print(f"[10] RESULTAT U_fond={res['U_fond']} U_charge={res['U_charge']} "
      f"lie={res['lie_par_info']} plv={res['plv_macro_micro']}")
