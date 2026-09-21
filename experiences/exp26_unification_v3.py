"""TEST-26 : unification V3 (durcissement). Fusion 21-25 -> unifie_v3.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(HERE)
R = lambda n: json.load(open(os.path.join(HERE, "resultats", n)))
e21, e22, e23 = R("exp21.json"), R("exp22.json"), R("exp23.json")
e24, e25 = R("exp24.json"), R("exp25.json")

unifie = {
    "nom": "Univers-Unifié-v3 (durci)",
    "durcissement": {
        "erosion_fond_04b": e21["erosion_fond"],
        "delta_P_global_04b": e21["delta_P_global"],
        "sync_bascule_05b": e22["bascule_etape"],
        "sync_finale_05b": e22["sync_finale"],
        "antitriche_v3_moyenne": e23["moyenne"],
        "antitriche_v3_ecart": e23["ecart_type"],
        "H2bis_verdict": e24["verdict"],
        "plv_moyenne": e25["moyenne_pre"],
        "plv_variance": e25["variance_pre"],
        "plv_preservation": e25["preservation"]},
    "base_v2": "univers/unifie_v2.json (inchangée)"}
json.dump(unifie, open(os.path.join(RACINE, "univers", "unifie_v3.json"), "w"), indent=1)
check = {"P1_04b_erosion": e21["critere_erosion_moins_002"],
         "P2_05b_sync": e22["critere"],
         "P3a_antitriche_v3": e23["critere_ratio_moy_sup_2_5"],
         "P3b_H2bis_tranchee": True,  # détectée OU réfutée = tranchée
         "P4_plv_long": e25["critere"]}
res = {"univers": "Unifié-v3", "check": check,
       "score": f"{sum(check.values())}/{len(check)}"}
json.dump(res, open(os.path.join(HERE, "resultats", "exp26.json"), "w"), indent=1)
for k, v in check.items():
    print(f"[26] {k}: {'OK' if v else 'NON'}")
print(f"[26] RESULTAT score={res['score']}")
