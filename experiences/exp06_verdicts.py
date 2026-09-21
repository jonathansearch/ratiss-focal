"""TEST-06 : fil + anti-triche + verdicts. R7: python3 experiences/exp06_verdicts.py
Anti-triche v2 (corrigée) : le DOSSIER observé complet (séries P + Phi +
événements) vs les règles. Si le dossier dépasse les règles -> émergence."""
import json
import os
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
R = lambda n: json.load(open(os.path.join(HERE, "resultats", n)))
e1, e3, e4, e5 = R("exp01.json"), R("exp03.json"), R("exp04.json"), R("exp05.json")

regles_A = "fond+filet4+lissage.03+transport.25+seuil500|graines24-101-7-3"
dossier_A = ("P=" + ",".join(str(x) for x in e4["serie_P_normee"])
             + "|Phi=" + ",".join(str(x) for x in e3["types"]["I"]["phi"])
             + f"|focal={e4['focalisation_etape']}|delta={e4['delta_P']}")
c_regles = len(zlib.compress(regles_A.encode(), 9))
c_dossier = len(zlib.compress(dossier_A.encode(), 9))
ratio = round(c_dossier / c_regles, 2)

fA, fB = e4["focalisation_etape"], e5["focalisation_etape"]
if fA and fB:
    verdict = "A+B sœurs : convergence émergence/implantation."
elif fA:
    verdict = "A seul : l'information suffit."
elif fB:
    verdict = "B seul : la structure est requise."
else:
    verdict = "Aucun : revoir seuils/conteneur."
res = {"comparatif": {
        "P_ref": e1["P_ref"],
        "A": {"focalisation": fA, "delta_P": e4["delta_P"]},
        "B": {"focalisation": fB, "delta_P": e5["delta_P"],
              "sync_finale": e5["sync_finale"]}},
       "antitriche_v2": {"regles_A_octets": c_regles,
                         "dossier_A_octets": c_dossier,
                         "dossier_A_brut_caracteres": len(dossier_A),
                         "ratio": ratio,
                         "emergence": bool(ratio > 2.0)},
       "verdict": verdict}
json.dump(res, open(os.path.join(HERE, "resultats", "exp06.json"), "w"), indent=1)
print(f"[06] RESULTAT ratio_antitriche={ratio} emergence={res['antitriche_v2']['emergence']}")
print(f"[06] VERDICT : {verdict}")
