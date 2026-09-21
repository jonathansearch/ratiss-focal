"""TEST-03 : porteurs. Le transport concentre ? R7: python3 experiences/exp03_porteurs.py"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import porteurs as P

T, PHI_C, PF = 12, 500.0, [0.0, 0.0, 0.0]
out = {}
for ptype, n_bits in (("I", 2048), ("S", 512)):
    port = P.creer_porteurs(n_bits, 8, ptype)
    tranches = [set(p.tranche) for p in port]
    disj = all(a.isdisjoint(b) for i, a in enumerate(tranches)
               for b in tranches[i + 1:])
    phis, franchi = [], None
    for t in range(T):
        P.transporter(port, PF, 0.25)
        phis.append(P.concentration(port, t + 1))
        if franchi is None and phis[-1] >= PHI_C:
            franchi = t + 1
    out[ptype] = {"disjointes": bool(disj),
                  "phi": [round(float(x), 1) for x in phis],
                  "franchissement_etape": franchi}
    print(f"[03] type {ptype}: disjointes={disj} franchissement={franchi} "
          f"phi_final={phis[-1]:.1f}", flush=True)
res = {"phi_c_lab": PHI_C, "types": out,
       "critere_ok": bool(out["I"]["disjointes"] and out["S"]["disjointes"]
                           and out["I"]["franchissement_etape"] is not None)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp03.json"), "w"), indent=1)
print(f"[03] RESULTAT critere_ok={res['critere_ok']}")
