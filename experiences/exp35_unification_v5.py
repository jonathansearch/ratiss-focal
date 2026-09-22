"""TEST-35 : VERDICT D'UNIFICATION V5. Fusion 30-34 -> unifie_v5.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(HERE)
R = lambda n: json.load(open(os.path.join(HERE, "resultats", n)))
e30, e31, e32 = R("exp30.json"), R("exp31.json"), R("exp32.json")
e33, e34 = R("exp33.json"), R("exp34.json")

unifie = {
    "nom": "Univers-Unifié-v5 (unification)",
    "subsistance": {"C_G": e30["C_G"], "C_Q": e30["C_Q"]},
    "non_reduction": {"RED_R2": [e31["RED_Q_par_G"]["R2"],
                                 e31["RED_G_par_Q"]["R2"]],
                      "COH_R2": [e31["COH_Q"]["R2"], e31["COH_G"]["R2"]],
                      "ratios": [e31["ratio_Q"], e31["ratio_G"]]},
    "secteurs": {"S_grav_lin_R2": e32["S_grav_lin_R2"],
                 "S_quant_expsat_R2": e32["S_quant_expsat_R2"],
                 "noyau_residuel": e32["noyau_residuel"],
                 "pente_noyau": e32["pente_noyau"],
                 "saturation_Q": e32["saturation_ratio_Q"]},
    "ligne_invisible": {"partage": e33["partage_coincidences"],
                        "indep": e33["indep_coincidences"],
                        "indep_proportion": e33["indep_proportion"]},
    "marqueurs": {"douceur": [e34["limites_douces_G"],
                               e34["limites_douces_Q"]],
                  "causalite": e34["causalite_QversG"],
                  "reference": e34["reference_partagee"]},
    "base_v4": "univers/unifie_v4.json (inchangée)"}
json.dump(unifie, open(os.path.join(RACINE, "univers", "unifie_v5.json"), "w"), indent=1)
check = {"U1_subsistance": e30["critere"], "U2_non_reduction": e31["critere"],
         "U3_secteurs": e32["critere"], "U4_ligne": e33["critere"],
         "U5_marqueurs": e34["critere"]}
n = sum(check.values())
verdict = ("UNIFICATION VALIDÉE : les lois subsistent entre elles par cohérence, "
           "sans se réduire.") if n == 5 else (
               f"Unification PARTIELLE ({n}/5) : " + ", ".join(
                   f"{k}={'OK' if v else 'NON'}" for k, v in check.items()))
res = {"univers": "Unifié-v5", "check": check, "score": f"{n}/5",
       "verdict": verdict}
json.dump(res, open(os.path.join(HERE, "resultats", "exp35.json"), "w"), indent=1)
for k, v in check.items():
    print(f"[35] {k}: {'OK' if v else 'NON'}")
print(f"[35] VERDICT : {verdict}")
