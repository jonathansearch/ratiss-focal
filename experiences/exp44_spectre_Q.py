"""TEST-44 : spectre mémoire Q post-choc. Appareil TEST-37 (anneau 24 Kuramoto
+ bruit 0.04 + lissage 0.5). 300 baseline -> 3 choc (K=0, sigma x10) ->
300 relâche. Comparaison spectre pré/post (250 pts chacun, burn-in 50).
Hypothèse : filtre passe-bas (basses fréquences conservées, hautes
dissipées). Critère : part_basse_post>=part_basse_pré ET
part_haute_post<=0.5xpart_haute_pré ET centroïde_post<centroïde_pré."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

NQ, KQ, DTQ, SIG = 24, 3.0, 0.3, 0.04
rng = np.random.default_rng(44)
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


def pas_q(K, sg):
    global th
    th = th + DTQ * (OMEGA + (K / NQ) * (
        adj * np.sin(th[None, :] - th[:, None])).sum(1))
    anc = np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG), np.zeros(NQ)])
    anc = anc + (anc / 2.2) * (0.15 * np.sin(th))[:, None]
    anc = anc + rng.normal(0, sg, anc.shape)
    for i in range(NQ):
        anc[i] += 0.5 * ((anc[(i - 1) % NQ] + anc[(i + 1) % NQ]) / 2 - anc[i])
    return C.p_sig(anc) / PREF


serie = []
for _ in range(300):
    serie.append(pas_q(KQ, SIG))
print(f"[44] fin baseline : {serie[-1]:.4f}", flush=True)
for _ in range(3):
    serie.append(pas_q(0.0, SIG * 10))
print(f"[44] choc : {[round(x, 3) for x in serie[300:303]]}", flush=True)
for _ in range(300):
    serie.append(pas_q(KQ, SIG))
print(f"[44] fin relâche : {serie[-1]:.4f}", flush=True)


def spectre(seg):
    s = np.array(seg)
    m = float(s.mean())
    Y = np.abs(np.fft.rfft(s - m))[1:] ** 2
    tot = float(Y.sum())
    n = len(Y)
    tiers = [float(Y[:n // 3].sum()) / tot, float(Y[n // 3:2 * n // 3].sum()) / tot,
             float(Y[2 * n // 3:].sum()) / tot]
    f = np.fft.rfftfreq(len(s), 1.0)[1:]
    centro = float((f * Y).sum() / tot)
    ac1 = float(np.corrcoef(s[:-1], s[1:])[0, 1])
    return {"parts": [round(x, 4) for x in tiers], "centroide": round(centro, 4),
            "ac1": round(ac1, 4), "niveau": round(m, 4)}


pre = spectre(serie[50:300])
post = spectre(serie[353:603])
ok = (post["parts"][0] >= pre["parts"][0]
      and post["parts"][2] <= 0.5 * pre["parts"][2]
      and post["centroide"] < pre["centroide"])
perte_Q = (post["niveau"] - pre["niveau"]) / pre["niveau"]
res = {"pre": pre, "post": post,
       "perte_niveau_Q": round(float(perte_Q), 4),
       "rappel_perte_G_TEST42": -0.21,
       "verdict": "FILTRE PASSE-BAS" if ok else "PAS DE FILTRAGE",
       "critere": bool(ok)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp44.json"), "w"), indent=1)
print(f"[44] RESULTAT pre={pre} post={post} perte_Q={perte_Q:.3f} "
      f"verdict={res['verdict']} critere={ok}")
