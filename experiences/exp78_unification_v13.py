"""TEST-78 : unification V13 (singularité caractérisée ?). Fusion
TEST-73..77 -> univers/unifie_v13.json. Score /5."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(HERE)
R = os.path.join(HERE, "resultats")
d = {n: json.load(open(os.path.join(R, f"exp{n}.json"))) for n in range(73, 78)}
check = {"S1_horizon": bool(d[73]["critere"]),
         "S2_loi": bool(d[74]["critere"]),
         "S3_horloges": bool(d[75]["critere"]),
         "S4_U": bool(d[76]["critere"]),
         "S5_Q": bool(d[77]["critere"])}
n = sum(check.values())
verdict = (f"Singularite : exces central (A:R2={d[73]['R2']}, "
           f"expo:R2={d[73]['R2_expo']}), loi {d[74]['gagnant_global']} "
           f"({d[74]['compte']}/12, p={d[74]['loi']['p']}), horloges "
           f"{d[75]['classe']}, U {d[76]['classe']} ({d[76]['partage']}), "
           f"Q {d[77]['classe']}.")
res = {"univers": "Unifié-v13", "check": check, "score": f"{n}/5",
       "verdict": verdict}
json.dump(res, open(os.path.join(R, "exp78.json"), "w"), indent=1)
json.dump(res, open(os.path.join(RACINE, "univers", "unifie_v13.json"), "w"),
          indent=1)
print(f"[78] RESULTAT score={n}/5 :: {verdict}")
