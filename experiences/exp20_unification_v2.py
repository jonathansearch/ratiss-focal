"""TEST-20 : unification v2. TOUTE la théorie (exp + formel) en un univers."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(HERE)
R = lambda n: json.load(open(os.path.join(HERE, "resultats", n)))
e1, e3 = R("exp01.json"), R("exp03.json")
e8, e9, e10 = R("exp08.json"), R("exp09.json"), R("exp10.json")
e11, e12, e13 = R("exp11.json"), R("exp12.json"), R("exp13.json")
e14, e15, e16 = R("exp14.json"), R("exp15.json"), R("exp16.json")
e17, e18, e19 = R("exp17.json"), R("exp18.json"), R("exp19.json")

unifie = {
    "nom": "Univers-Unifié-v2",
    "constantes_mesurees": {
        "P_ref": e1["P_ref"], "phi_c_lab": 500.0,
        "psi_sync_final": e8["psi_final"], "X": e9["X"],
        "U_fond": e10["U_fond"], "U_charge": e10["U_charge"],
        "I_sans_contact": e12["I_sans_contact"],
        "I_avec_contact": e12["I_avec_contact"],
        "I_min_independant": e12["I_min_independant"],
        "I_min_commun": e12["I_min_commun"], "K": e13["K"],
        "Pi": {"concentration": e15["Pi_concentration"],
               "coherence": e15["Pi_coherence"],
               "information": e15["Pi_information"]},
        "sigma_c": e16["sigma_c"],
        "F0_cout_bits": e17["cout_bits"]},
    "mecanismes_valides": ["fond", "filet_info", "transport", "seuil_focalisation",
                           "stine24", "X", "U", "tryperposition", "K", "secteurs",
                           "seuils_structures", "F0", "correspondance"],
    "graines": {"fond": 24, "info": 101, "injection": 7, "porteurs": 3}}
json.dump(unifie, open(os.path.join(RACINE, "univers", "unifie_v2.json"), "w"), indent=1)
check = {"08_stine": e8["aligne"], "09_X": e9["couple"],
         "10_U": e10["lie_par_info"], "11_tryperposition": e11["preservée"],
         "12_couplage": e12["couplage_reel"], "13_K": e13["sain"],
         "14_secteurs": e14["secteurs_requis"], "15_constantes": e15["stable"],
         "16_seuils": e16["seuils_differents"], "17_F0": e17["F0_tient"],
         "19_correspondance": bool(e19["limite_temoin"] and e19["monotone"])}
res = {"univers": "Unifié-v2", "check": check,
       "score": f"{sum(check.values())}/{len(check)}",
       "H2prime_table": e18["table_R"],
       "H2prime_bascule": e18["bascule_observee"]}
json.dump(res, open(os.path.join(HERE, "resultats", "exp20.json"), "w"), indent=1)
for k, v in check.items():
    print(f"[20] {k}: {'OK' if v else 'NON'}")
print(f"[20] RESULTAT score={res['score']} H2prime_bascule={res['H2prime_bascule']}")
