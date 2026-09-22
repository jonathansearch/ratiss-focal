"""TEST-86 : ombre d'un disque absorbant — moteur d'ondes indépendant.
Validation croisée de TEST-82 (contraste ~0.66) avec l'équation de d'Alembert
(différences finies, PAS la règle focale) = jumeau du bac à ondes Falstad.
Grille 120x120, source plane en bas (période 20 pas), disque absorbant
(u=0 épinglé) de rayon rd dans {0, 4, 8, 12}, 900 pas. On regarde :
amplitude sur l'axe derrière le disque vs latérale (contraste).
Protocole téléphone Falstad : voir OUTILS-EN-LIGNE.md.
Observation pure, zéro verdict."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
N, C, PER, T = 120, 0.5, 8, 900
cx, cy = N // 2, N // 2
ii, jj = np.mgrid[0:N, 0:N]
dd = np.sqrt((ii - cx) ** 2 + (jj - cy) ** 2)


def run(rd):
    u = np.zeros((N, N))
    up = np.zeros((N, N))
    trou = dd < rd
    amp = np.zeros((N, N))
    for t in range(T):
        lap = (np.roll(u, 1, 0) + np.roll(u, -1, 0) +
               np.roll(u, 1, 1) + np.roll(u, -1, 1) - 4 * u)
        un = 2 * u - up + C * C * lap
        un[100, :] += 0.5 * np.sin(2 * np.pi * t / PER)
        un[trou] = 0.0
        un[:3, :] *= 0.9; un[-3:, :] *= 0.9
        un[:, :3] *= 0.9; un[:, -3:] *= 0.9
        up, u = u, un
        if t >= T - PER:
            amp = np.maximum(amp, np.abs(u))
    ligne = cy - rd - 12
    axe = float(amp[ligne, cx - 2:cx + 3].mean())
    lat = float(np.concatenate([amp[ligne, cx - 50:cx - 30],
                                amp[ligne, cx + 30:cx + 50]]).mean())
    return {"rd": rd, "a_axe": round(axe, 4), "a_lat": round(lat, 4),
            "contraste": round(1 - axe / lat, 4) if lat > 0 else 0.0}


lignes = []
for rd in (0, 8, 16, 24):
    r = run(rd)
    lignes.append(r)
ref = lignes[0]["a_axe"] / lignes[0]["a_lat"]
for r in lignes:
    r["contraste"] = round(1 - (r["a_axe"] / r["a_lat"]) / ref, 4)
    print(f"[86] rd={r['rd']} : axe={r['a_axe']} lat={r['a_lat']} "
          f"contraste={r['contraste']}", flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "resultats", "exp86.json"), "w"), indent=1)
print("[86] OBSERVÉ : 4 disques, jumeau Falstad archivé.")
