"""TEST-93 : cycle FERMÉ ± dans (G0, position puits) — le sens compte-t-il ?
PRIORITÉ ABSOLUE (ordre chef) : le pli orienté exige un cycle fermé.
Anneau NQ=24 + hubs (K=3, DT=0.3, graines 55/100). Chemin gamma(t) fermé :
A: G0 0->1 (c=0) ; B: c 0->pi (G0=1) ; C: G0 1->0 (c=pi) ; D: c pi->2pi
(G0=0). 150 pas/patte (600/run). Sens - : pattes inversées.
Observables pré-enregistrées : PHI sonde 0 (déroulée) ±, PHI moyen Psi ±,
DELTA_PHI, fidélité de fermeture R_diff±, R finaux. Zéro critère.
Observation pure."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NQ, KQ, DTQ, LEG = 24, 3.0, 0.3, 150
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
ANG = np.linspace(0, 2 * np.pi, NQ, endpoint=False)


def dist(a, c):
    return np.abs(((a - c + np.pi) % (2 * np.pi)) - np.pi)


def pattes(sens):
    A = [(g, 0.0) for g in np.linspace(0, 1, LEG)]
    B = [(1.0, c) for c in np.linspace(0, np.pi, LEG)]
    C = [(g, np.pi) for g in np.linspace(1, 0, LEG)]
    D = [(0.0, c) for c in np.linspace(np.pi, 2 * np.pi, LEG)]
    seq = A + B + C + D
    return seq if sens == "plus" else list(reversed(seq))


def run(sens):
    th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
    th0 = th.copy()
    acc0, accP, prev0, prevP = 0.0, 0.0, th[0], float(np.angle(np.exp(1j * th).mean()))
    R = []
    for G0, c in pattes(sens):
        prof = np.exp(-dist(ANG, c) ** 2 / 0.5)
        om = OMEGA - G0 * prof
        th = th + DTQ * (om + (KQ / NQ) *
                         (adj * np.sin(th[None, :] - th[:, None])).sum(1))
        d0 = th[0] - prev0
        acc0 += (d0 + np.pi) % (2 * np.pi) - np.pi
        prev0 = th[0]
        Psi = float(np.angle(np.exp(1j * th).mean()))
        dp = Psi - prevP
        accP += (dp + np.pi) % (2 * np.pi) - np.pi
        prevP = Psi
        R.append(float(np.abs(np.exp(1j * th).mean())))
    rdiff = float(np.abs(np.exp(1j * (th - th0)).mean()))
    return {"sens": sens, "PHI_sonde": round(float(acc0), 3),
            "PHI_Psi": round(float(accP), 3),
            "R_diff": round(rdiff, 4),
            "R_final": round(float(np.mean(R[-50:])), 4)}


plus = run("plus")
moins = run("moins")
d_sonde = round(plus["PHI_sonde"] - moins["PHI_sonde"], 3)
d_psi = round(plus["PHI_Psi"] - moins["PHI_Psi"], 3)
print(f"[93] plus  : sonde={plus['PHI_sonde']} Psi={plus['PHI_Psi']} "
      f"Rdiff={plus['R_diff']} Rfin={plus['R_final']}", flush=True)
print(f"[93] moins : sonde={moins['PHI_sonde']} Psi={moins['PHI_Psi']} "
      f"Rdiff={moins['R_diff']} Rfin={moins['R_final']}", flush=True)
print(f"[93] DELTA sonde={d_sonde} DELTA Psi={d_psi}", flush=True)
json.dump({"plus": plus, "moins": moins, "DELTA_sonde": d_sonde,
           "DELTA_Psi": d_psi},
          open(os.path.join(HERE, "resultats", "exp93.json"), "w"), indent=1)
print("[93] OBSERVÉ : cycle fermé ± archivé.")
