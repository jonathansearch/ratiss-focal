"""TEST-55 : unification V10 (porte ou mur ?). Fusion TEST-52/53/54
-> univers/unifie_v10.json. Score /3."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(HERE)
R = os.path.join(HERE, "resultats")
d52 = json.load(open(os.path.join(R, "exp52.json")))
d53 = json.load(open(os.path.join(R, "exp53.json")))
d54 = json.load(open(os.path.join(R, "exp54.json")))
check = {"B1_phase": bool(d52["critere"]), "B2_bassin": bool(d53["critere"]),
         "B3_QU": bool(d54["critere"])}
n = sum(check.values())
verdict = (f"Bistabilité Q : phase {d52['classe']} "
           f"(exact={d52['exactitude']}), bassin {d53['classe']} "
           f"(I_50={d53['I_50_Ea']}), Q/U {d54['classe']}.")
res = {"univers": "Unifié-v10", "check": check, "score": f"{n}/3",
       "verdict": verdict}
json.dump(res, open(os.path.join(R, "exp55.json"), "w"), indent=1)
json.dump(res, open(os.path.join(RACINE, "univers", "unifie_v10.json"), "w"),
          indent=1)
print(f"[55] RESULTAT score={n}/3 :: {verdict}")
