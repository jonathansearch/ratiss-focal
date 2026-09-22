"""TEST-29 : unification V4 (deux lois). Fusion 27-28 -> unifie_v4.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(HERE)
R = lambda n: json.load(open(os.path.join(HERE, "resultats", n)))
e27, e28 = R("exp27.json"), R("exp28.json")

unifie = {
    "nom": "Univers-Unifié-v4 (deux lois)",
    "loi_proximite_condensation": {
        "D_c": e27["D_c"], "rho_c": e27["rho_c"],
        "table_doux": e27["table_doux"], "table_dur": e27["table_dur"],
        "controle_D5_gate_K6": e27["controle_D5_gate_K6"],
        "controle_D5_pur_K4": e27["controle_D5_pur_K4"]},
    "principe_resilience": {
        "R_neutre": e28["R_neutre"], "R_selectif": e28["R_selectif"],
        "zone_purification": e28["zone_purification"],
        "rupture_haute": e28["rupture_haute"], "verdict": e28["verdict"]},
    "base_v3": "univers/unifie_v3.json (inchangée)"}
json.dump(unifie, open(os.path.join(RACINE, "univers", "unifie_v4.json"), "w"), indent=1)
check = {"L1_proximite": e27["critere"], "L2_resilience": e28["critere"]}
res = {"univers": "Unifié-v4", "check": check,
       "score": f"{sum(check.values())}/{len(check)}"}
json.dump(res, open(os.path.join(HERE, "resultats", "exp29.json"), "w"), indent=1)
for k, v in check.items():
    print(f"[29] {k}: {'OK' if v else 'NON'}")
print(f"[29] RESULTAT score={res['score']}")
