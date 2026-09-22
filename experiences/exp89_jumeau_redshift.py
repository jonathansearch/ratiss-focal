"""TEST-89 : JUMEAU exact du firmware Wokwi (redshift gradué).
Même logique que outils_en_ligne/wokwi_redshift/sketch.ino (anneau N=12,
K=3.0, DT=0.1, T=3000, om_i = -1.0*exp(-i/3), init LCG graine 84).
Prédit les 12 fréquences que le téléphone affichera. Écart = bug.
Observation pure, zéro verdict."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
N, K, DT, T = 12, 3.0, 0.1, 3000
OM = np.array([-1.0 * np.exp(-i / 3.0) for i in range(N)])
adj = np.zeros((N, N))
for i in range(N):
    adj[i, (i - 1) % N] = adj[i, (i + 1) % N] = 1.0

_state = [0]


def arand():
    _state[0] = (1103515245 * _state[0] + 12345) & 0x7fffffff
    return _state[0] / 0x7fffffff


_state[0] = 84
th = np.array([arand() * 2 * np.pi for _ in range(N)])
traj = []
for t in range(T):
    th = th + DT * (OM + (K / N) *
                    (adj * np.sin(th[None, :] - th[:, None])).sum(1))
    if t >= T - 500:
        traj.append(th.copy())
traj = np.array(traj)
freqs = []
for i in range(N):
    dp = np.unwrap(traj[:, i])
    freqs.append(round(float((dp[-1] - dp[0]) / (len(dp) * DT)), 4))
    print(f"[89] osc{i} : freq={freqs[-1]}", flush=True)
json.dump({"freqs": freqs},
          open(os.path.join(HERE, "resultats", "exp89.json"), "w"), indent=1)
print("[89] OBSERVÉ : 12 fréquences prédites archivées.")
