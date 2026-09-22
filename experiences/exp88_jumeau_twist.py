"""TEST-88 : JUMEAU exact du firmware Wokwi (twist, 2 puits).
Même logique que outils_en_ligne/wokwi_twist/sketch.ino au pas près
(N=24, anneau + hubs 0/12, K=3, DT=0.3, T=300, s=0.5, G0 dans {0, 1.0},
graines Arduino 100/55 émulées). Prédit ce que le téléphone affichera
sur wokwi.com : R final + twist. Écart = bug (pas physique).
Observation pure, zéro verdict."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NQ, KQ, DTQ, T = 24, 3.0, 0.3, 300
# émutation Arduino : LCG glibc (random() Arduino AVR)
_state = [0]


def arduino_random_seed(s):
    _state[0] = s & 0x7fffffff


def arduino_random():
    _state[0] = (1103515245 * _state[0] + 12345) & 0x7fffffff
    return _state[0] / 0x7fffffff


def arduino_phase_init():
    arduino_random_seed(100)
    return np.array([arduino_random() * 2 * np.pi for _ in range(NQ)])


def arduino_omega():
    arduino_random_seed(55)
    # Box-Muller sur random() x2, sigma 0.2
    om = []
    for _ in range(NQ):
        u1 = max(arduino_random(), 1e-9)
        u2 = arduino_random()
        om.append(0.2 * np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2))
    return np.array(om)


adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
ANG = np.linspace(0, 2 * np.pi, NQ, endpoint=False)
d0 = np.abs((ANG + np.pi) % (2 * np.pi) - np.pi)
d1 = np.abs(((ANG - np.pi + np.pi) % (2 * np.pi)) - np.pi)
PROF = np.exp(-d0 ** 2 / (2 * 0.5 ** 2)) + np.exp(-d1 ** 2 / (2 * 0.5 ** 2))


def run(G0):
    th = arduino_phase_init()
    om = arduino_omega() - G0 * PROF
    R = []
    for _ in range(T):
        th = th + DTQ * (om + (KQ / NQ) *
                         (adj * np.sin(th[None, :] - th[:, None])).sum(1))
        R.append(float(np.abs(np.exp(1j * th).mean())))
    dth = np.angle(np.exp(1j * (np.roll(th, -1) - th)))
    return {"G0": G0, "R_final": round(float(np.mean(R[-50:])), 4),
            "twist": round(float(dth.sum() / (2 * np.pi)), 3)}


lignes = []
for G0 in (0, 1.0):
    r = run(G0)
    lignes.append(r)
    print(f"[88] G0={G0} : R_fin={r['R_final']} twist={r['twist']}",
          flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "resultats", "exp88.json"), "w"), indent=1)
print("[88] OBSERVÉ : prédiction firmware archivée.")
