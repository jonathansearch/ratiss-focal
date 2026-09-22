"""TEST-37 : volatilité Q (F8) = signal ou bruit ? Anneau 24 + Kuramoto +
bruit 0.04 + lissage 0.5 (réglage exp30-fort), T=100. Post burn-in : spectre
(pente log-log), distribution (skew/kurt), bursts (>3σ), autocorr lag-1.
Règles : BLANC si |pente|<0.3 ET |kurt-3|<1 ET bursts<=1% ; sinon STRUCTURÉE."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

NQ, KQ, DTQ, T, SIG = 24, 3.0, 0.3, 100, 0.04
rng = np.random.default_rng(37)
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
ANG = np.linspace(0, 2 * np.pi, NQ, endpoint=False)
PREF = C.p_sig(np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG),
                                np.zeros(NQ)]))
th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
serie = []
for step in range(T):
    th = th + DTQ * (OMEGA + (KQ / NQ) * (
        adj * np.sin(th[None, :] - th[:, None])).sum(1))
    anc = np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG), np.zeros(NQ)])
    anc = anc + (anc / 2.2) * (0.15 * np.sin(th))[:, None]
    anc = anc + rng.normal(0, SIG, anc.shape)
    for i in range(NQ):
        anc[i] += 0.5 * ((anc[(i - 1) % NQ] + anc[(i + 1) % NQ]) / 2 - anc[i])
    serie.append(C.p_sig(anc) / PREF)
    if (step + 1) % 25 == 0:
        print(f"[37] ... pas {step + 1}/100", flush=True)
s = np.array(serie[10:])
m, sd = float(s.mean()), float(s.std())
z = (s - m) / sd
skew, kurt = float((z ** 3).mean()), float((z ** 4).mean())
Y = np.abs(np.fft.rfft(s - m))[1:] ** 2
f = np.fft.rfftfreq(len(s), 1.0)[1:]
pente = float(np.polyfit(np.log(f), np.log(Y + 1e-12), 1)[0])
bursts = float((np.abs(z) > 3).mean())
ac1 = float(np.corrcoef(s[:-1], s[1:])[0, 1])
motifs = []
if abs(pente) >= 0.3:
    motifs.append(f"spectre_pente={pente:.2f}")
if abs(kurt - 3) >= 1:
    motifs.append(f"kurt={kurt:.2f}")
if bursts > 0.01:
    motifs.append(f"bursts={bursts:.3f}")
classe = "BLANC (non structuré)" if not motifs else "STRUCTURÉE: " + ",".join(motifs)
res = {"std": round(sd, 4), "skew": round(skew, 3), "kurt": round(kurt, 3),
       "pente_spectre": round(pente, 3), "bursts_frac": round(bursts, 4),
       "autocorr_lag1": round(ac1, 3), "classe": classe,
       "structurelle": bool(motifs),
       "integration": ("composante signal : mémoire spectrale pente "
                       f"{pente:.2f} + autocorr {ac1:.2f}") if motifs else "néant",
       "critere": True}
json.dump(res, open(os.path.join(HERE, "resultats", "exp37.json"), "w"), indent=1)
print(f"[37] RESULTAT std={sd:.4f} kurt={kurt:.2f} pente={pente:.2f} "
      f"bursts={bursts:.3f} ac1={ac1:.2f} -> {classe}")
