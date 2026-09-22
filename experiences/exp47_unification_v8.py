"""TEST-47 : unification V8 (mémoire Q post-choc ?). Fusion TEST-44/45/46
-> univers/unifie_v8.json. Score /3."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "resultats")
d44 = json.load(open(os.path.join(R, "exp44.json")))
d45 = json.load(open(os.path.join(R, "exp45.json")))
d46 = json.load(open(os.path.join(R, "exp46.json")))
check = {"M1_spectre": bool(d44["critere"]), "M2_ligne": bool(d45["critere"]),
         "M3_reconstruction": bool(d46["critere"])}
n = sum(check.values())
verdict = (f"Mémoire Q : spectre {d44['verdict']} "
           f"(R:centroïde {d44['pre']['centroide']}->{d44['post']['centroide']}), "
           f"ligne {d45['classe']} ({d45['partage']}), "
           f"reconstruction {d46['G']['gagnant']} (R2={d46['G']['R2']}, "
           f"tau_cicat={d46['tau_cicatrisation']}).")
res = {"univers": "Unifié-v8", "check": check, "score": f"{n}/3",
       "verdict": verdict}
json.dump(res, open(os.path.join(R, "exp47.json"), "w"), indent=1)
U = os.path.join(os.path.dirname(HERE), "univers", "unifie_v8.json")
json.dump(res, open(U, "w"), indent=1)
print(f"[47] RESULTAT score={n}/3 :: {verdict}")
