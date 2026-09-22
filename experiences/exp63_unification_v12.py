"""TEST-63 : unification V12 (dompter le flip ?). Fusion TEST-60/61/62
-> univers/unifie_v12.json. Score /3."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(HERE)
R = os.path.join(HERE, "resultats")
d60 = json.load(open(os.path.join(R, "exp60.json")))
d61 = json.load(open(os.path.join(R, "exp61.json")))
d62 = json.load(open(os.path.join(R, "exp62.json")))
check = {"D1_forcage": bool(d60["critere"]),
         "D2_rupture": bool(d61["critere"]),
         "D3_couplage": bool(d62["critere"])}
n = sum(check.values())
verdict = (f"Flip et rupture : forçage {d60['classe']} "
           f"({d60['cellules_valides']}), U {d61['classe']} "
           f"(sigma_r={d61['sigma_rupture']}, U_min={d61['U_min']}, "
           f"rev={d61['reversibilite']['classe']}), Q/U {d62['classe']}.")
res = {"univers": "Unifié-v12", "check": check, "score": f"{n}/3",
       "verdict": verdict}
json.dump(res, open(os.path.join(R, "exp63.json"), "w"), indent=1)
json.dump(res, open(os.path.join(RACINE, "univers", "unifie_v12.json"), "w"),
          indent=1)
print(f"[63] RESULTAT score={n}/3 :: {verdict}")
