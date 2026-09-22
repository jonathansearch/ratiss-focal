"""TEST-87 : lentille par zone lente — moteur d'ondes indépendant.
Pont avec TEST-81 (lentille balistique en S, ±47°) : ici ondes de d'Alembert
traversant un disque où c est réduit (x0.6, rayon 15) = jumeau de la
lentille Falstad (zone peu profonde). Témoin : c uniforme. 900 pas.
On regarde : gain de focalisation (amplitude max sur l'axe derrière la
zone / amplitude incidente) lentille vs témoin + position du foyer.
Observation pure, zéro verdict."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
N, C, PER, T = 120, 0.5, 20, 900
cx, cy = N // 2, N // 2
ii, jj = np.mgrid[0:N, 0:N]
dd = np.sqrt((ii - cx) ** 2 + (jj - cy) ** 2)


def run(lentille):
    u = np.zeros((N, N))
    up = np.zeros((N, N))
    cc = np.full((N, N), C)
    if lentille:
        cc[dd < 15] = C * 0.6
    amp = np.zeros((N, N))
    for t in range(T):
        lap = (np.roll(u, 1, 0) + np.roll(u, -1, 0) +
               np.roll(u, 1, 1) + np.roll(u, -1, 1) - 4 * u)
        un = 2 * u - up + cc * cc * lap
        un[100, :] += 0.5 * np.sin(2 * np.pi * t / PER)
        un[:3, :] *= 0.9; un[-3:, :] *= 0.9
        un[:, :3] *= 0.9; un[:, -3:] *= 0.9
        up, u = u, un
        if t >= T - PER:
            amp = np.maximum(amp, np.abs(u))
    incident = float(amp[105, cx - 10:cx + 10].mean())
    # focalisation = pic sur l'axe vs moyenne latérale, par ligne ; max sur zone
    focus = []
    for r in range(25, cy - 15):
        lat = float(np.concatenate([amp[r, cx - 45:cx - 25],
                                    amp[r, cx + 25:cx + 45]]).mean())
        focus.append(float(amp[r, cx] / lat) if lat > 0 else 0.0)
    imax = int(np.argmax(focus))
    return {"lentille": lentille, "incident": round(incident, 4),
            "focus_max": round(float(focus[imax]), 3),
            "foyer_ligne": int(25 + imax)}


lignes = []
for lentille in (False, True):
    r = run(lentille)
    lignes.append(r)
    print(f"[87] lentille={lentille} : focus={r['focus_max']} "
          f"foyer_ligne={r['foyer_ligne']}", flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "resultats", "exp87.json"), "w"), indent=1)
print("[87] OBSERVÉ : lentille vs témoin archivés.")
