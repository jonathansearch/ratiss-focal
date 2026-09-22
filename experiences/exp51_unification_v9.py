"""TEST-51 : unification V9 (sanctuaire éternel ?). Fusion TEST-48/49/50
-> univers/unifie_v9.json. Score /3."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(HERE)
R = os.path.join(HERE, "resultats")
d48 = json.load(open(os.path.join(R, "exp48.json")))
d49 = json.load(open(os.path.join(R, "exp49.json")))
d50 = json.load(open(os.path.join(R, "exp50.json")))
check = {"H1_escalier": bool(d48["critere"]),
         "H2_sanctuaire": bool(d49["critere"]),
         "H3_fatigue": bool(d50["critere"])}
n = sum(check.values())
verdict = (f"Hystérésis cumulée : escalier {d48['gagnant']} "
           f"(R2={d48['R2']}), U {d49['classe']} "
           f"(parts={[x['partage'] for x in d49['niveaux']]})"
           f", Q {d50['classe']} (dérive={d50['derive_max']}).")
res = {"univers": "Unifié-v9", "check": check, "score": f"{n}/3",
       "verdict": verdict}
json.dump(res, open(os.path.join(R, "exp51.json"), "w"), indent=1)
json.dump(res, open(os.path.join(RACINE, "univers", "unifie_v9.json"), "w"),
          indent=1)
print(f"[51] RESULTAT score={n}/3 :: {verdict}")
