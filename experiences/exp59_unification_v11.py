"""TEST-59 : unification V11 (nord magnétique ?). Fusion TEST-56/57/58
-> univers/unifie_v11.json. Score /3."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(HERE)
R = os.path.join(HERE, "resultats")
d56 = json.load(open(os.path.join(R, "exp56.json")))
d57 = json.load(open(os.path.join(R, "exp57.json")))
d58 = json.load(open(os.path.join(R, "exp58.json")))
check = {"A1_symetrie": bool(d56["critere"]),
         "A2_distribution": bool(d57["critere"]),
         "A3_courbeU": bool(d58["critere"])}
n = sum(check.values())
verdict = (f"Anti-persistence : symétrie {d56['classe']} "
           f"(med {d56['med_H']}/{d56['med_L']}), distribution "
           f"{d57['meilleur']} (R2={d57['R2']}), U {d58['classe']} "
           f"(sigma_c={d58['sigma_c']}, {d58['forme']} R2={d58['R2']}).")
res = {"univers": "Unifié-v11", "check": check, "score": f"{n}/3",
       "verdict": verdict}
json.dump(res, open(os.path.join(R, "exp59.json"), "w"), indent=1)
json.dump(res, open(os.path.join(RACINE, "univers", "unifie_v11.json"), "w"),
          indent=1)
print(f"[59] RESULTAT score={n}/3 :: {verdict}")
