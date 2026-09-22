"""TEST-81 : déflexion balistique par le puits exponentiel (lentille ?).
128 particules, x=-8, vitesses +x (v=1.5), paramètres d'impact b dans
[-6, 6]. Accélération centrale attractive a = -A*exp(-r/l)*r_hat avec
A=2.0, l=1.5 (ordre de grandeur TEST-74). Intégration Euler DT=0.02,
T=1200 pas. On regarde : angle de déflexion asymptotique vs b, et
fraction capturée (r<0.3 en fin de vol).
Note honnête : balistique maison, pas l'organe porteurs (qui n'a pas
de vitesse) — mesure de la courbure du potentiel, rien de plus.
Observation pure, zéro verdict."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
A, L, V, DT, T = 2.0, 1.5, 1.5, 0.02, 1200


def vol(b):
    p = np.array([-8.0, b])
    v = np.array([V, 0.0])
    for _ in range(T):
        r = float(np.linalg.norm(p))
        if r < 1e-9:
            break
        v += -A * np.exp(-r / L) * (p / r) * DT
        p += v * DT
        if p[0] > 9:
            break
    if float(np.linalg.norm(p)) < 0.3:
        return None
    return float(np.degrees(np.arctan2(v[1], v[0])))


bs = np.linspace(-6, 6, 25)
lignes = []
for b in bs:
    a = vol(float(b))
    lignes.append({"b": round(float(b), 2), "deflexion_deg": a})
capt = sum(1 for x in lignes if x["deflexion_deg"] is None)
print(f"[81] capturés : {capt}/25", flush=True)
for x in lignes[::4]:
    print(f"[81] b={x['b']} -> {x['deflexion_deg']}", flush=True)
json.dump({"A": A, "l": L, "lignes": lignes, "captures": capt},
          open(os.path.join(HERE, "resultats", "exp81.json"), "w"), indent=1)
print("[81] OBSERVÉ : courbe de déflexion archivée.")
