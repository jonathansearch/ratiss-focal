"""TEST-39 : unification V6 (Q durci sans trahison). Fusion 36-38."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(HERE)
R = lambda n: json.load(open(os.path.join(HERE, "resultats", n)))
e36, e37, e38 = R("exp36.json"), R("exp37.json"), R("exp38.json")

unifie = {
    "nom": "Univers-Unifié-v6 (Q révélé)",
    "forme_Q": {"meilleur": e36["meilleur"], "R2": e36["R2"],
                "params": e36["params"], "candidats": e36["candidats"]},
    "volatilite": {"classe": e37["classe"], "std": e37["std"],
                   "pente_spectre": e37["pente_spectre"],
                   "bursts": e37["bursts_frac"],
                   "autocorr": e37["autocorr_lag1"],
                   "integration": e37["integration"]},
    "ligne_bruit": {"partage": e38["partage"], "indep": e38["indep"],
                    "separation": e38["separation"]},
    "base_v5": "univers/unifie_v5.json (inchangée)"}
json.dump(unifie, open(os.path.join(RACINE, "univers", "unifie_v6.json"), "w"), indent=1)
check = {"Q1_forme": e36["critere"], "Q2_volatilite": e37["critere"],
         "Q3_ligne_bruit": e38["critere"]}
n = sum(check.values())
verdict = ("Q RÉVÉLÉ : forme " + e36["meilleur"] + " (R2=" + str(e36["R2"]) +
           "), volatilité " + e37["classe"] + ", ligne robuste.") if n == 3 else (
               f"V6 partielle ({n}/3)")
res = {"univers": "Unifié-v6", "check": check, "score": f"{n}/3",
       "verdict": verdict}
json.dump(res, open(os.path.join(HERE, "resultats", "exp39.json"), "w"), indent=1)
for k, v in check.items():
    print(f"[39] {k}: {'OK' if v else 'NON'}")
print(f"[39] VERDICT : {verdict}")
