"""TEST-09 : facteur X (couplage externe entre couches). R7: exp09_X.py"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import couches as L

s = json.load(open(os.path.join(HERE, "resultats", "exp08.json")))["series"]
paires = {}
cles = ["macro", "micro", "info"]
for i in range(3):
    for j in range(i + 1, 3):
        paires[f"{cles[i]}-{cles[j]}"] = round(abs(L.corr(s[cles[i]], s[cles[j]])), 4)
X = round(sum(paires.values()) / 3, 4)
res = {"correlations": paires, "X": X, "couple": bool(X > 0.1)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp09.json"), "w"), indent=1)
print(f"[09] RESULTAT X={X} couple={res['couple']} paires={paires}")
