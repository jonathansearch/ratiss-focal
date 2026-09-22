"""TEST-43 : unification V7 (noyau révélé). Fusion 40-42."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(HERE)
R = lambda n: json.load(open(os.path.join(HERE, "resultats", n)))
e40, e41, e42 = R("exp40.json"), R("exp41.json"), R("exp42.json")

unifie = {
    "nom": "Univers-Unifié-v7 (noyau)",
    "loi_noyau": {"meilleur": e40["meilleur"], "R2": e40["R2"],
                  "fits": e40["fits"], "table": e40["table"]},
    "collapse_noyau": {"G_pre": e41["G_pre"], "classe": e41["classe"],
                       "corr": e41["corr_intensite"]},
    "choc": {"G_pre": e42["G_pre"], "final": e42["final"],
             "classe": e42["classe"]},
    "base_v6": "univers/unifie_v6.json (inchangée)"}
json.dump(unifie, open(os.path.join(RACINE, "univers", "unifie_v7.json"), "w"), indent=1)
check = {"N1_loi": e40["critere"], "N2_collapse": e41["critere"],
         "N3_choc": e42["critere"]}
n = sum(check.values())
verdict = (f"Noyau : loi {e40['meilleur']} (R2={e40['R2']}), collapse "
           f"{e41['classe']}, choc {e42['classe']}.") if n == 3 else f"V7 ({n}/3)"
res = {"univers": "Unifié-v7", "check": check, "score": f"{n}/3",
       "verdict": verdict}
json.dump(res, open(os.path.join(HERE, "resultats", "exp43.json"), "w"), indent=1)
for k, v in check.items():
    print(f"[43] {k}: {'OK' if v else 'NON'}")
print(f"[43] VERDICT : {verdict}")
