"""TEST-62 : couplage structure Q -> robustesse U. NOTE DESIGN : le test
naïf (jitter=sigma_Q_état) est CIRCULAIRE (TEST-58 donne déjà S_U(jit)).
Vrai test : la STRUCTURE temporelle des fluctuations Q (HIGH vs LOW)
affecte-t-elle U à sigma IDENTIQUE ? Collecte 5 séries HIGH + 5 LOW
(250 pas détrendés, seed 6200+j), renormalisées à sigma=0.04, injectées
comme bruit corrélé (jitter_t = q_tilde[t] |.| N(0,1)) dans ligne T=20.
2 blocs indépendants (graines A/B) x 30+30 par état. DÉCOUPLÉ si
comptes identiques aux 2 blocs ; COUPLÉ_STRUCTUREL si même signe et
|Δ|>=2 aux 2 blocs ; MIXTE sinon. Critère : DÉCOUPLÉ."""
import hashlib
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import porteurs as P

NQ, KQ, DTQ, SIG = 24, 3.0, 0.3, 0.04
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


def run_q(seed):
    rng = np.random.default_rng(seed)
    th = rng.uniform(0, 2 * np.pi, NQ)

    def pas(K, sg):
        nonlocal th
        th = th + DTQ * (OMEGA + (K / NQ) * (
            adj * np.sin(th[None, :] - th[:, None])).sum(1))
        anc = np.column_stack([2.2 * np.cos(ANG), 2.2 * np.sin(ANG),
                               np.zeros(NQ)])
        anc = anc + (anc / 2.2) * (0.15 * np.sin(th))[:, None]
        anc = anc + rng.normal(0, sg, anc.shape)
        for i in range(NQ):
            anc[i] += 0.5 * ((anc[(i - 1) % NQ] + anc[(i + 1) % NQ]) / 2
                             - anc[i])
        return C.p_sig(anc) / PREF

    for _ in range(60):
        pas(KQ, SIG)
    for _ in range(3):
        pas(0.0, SIG * 10)
    return [pas(KQ, SIG) for _ in range(300)]


series = {"HIGH": [], "LOW": []}
j = 0
while (len(series["HIGH"]) < 5 or len(series["LOW"]) < 5) and j < 40:
    seg = np.array(run_q(6200 + j)[-250:])
    qf = float(seg[-50:].mean())
    z = seg - seg.mean()
    z = z / max(z.std(), 1e-9) * 0.04
    if qf >= 0.84 and len(series["HIGH"]) < 5:
        series["HIGH"].append(z)
    elif qf <= 0.82 and len(series["LOW"]) < 5:
        series["LOW"].append(z)
    j += 1
print(f"[62] séries : HIGH={len(series['HIGH'])} LOW={len(series['LOW'])}",
      flush=True)


def phic(msg: bytes) -> float:
    h = int(hashlib.sha256(msg).hexdigest(), 16)
    return 100 + 1900 * ((h % 1000) / 1000)


def etape_q(seuil, cible, seed_jit, serie):
    rng = np.random.default_rng(seed_jit)
    port = P.creer_porteurs(2048, 8, "I", seed=3)
    for p in port:
        p.position += np.array(cible, float)
    for t in range(20):
        P.transporter(port, cible, 0.12)
        amp = abs(float(serie[t % len(serie)]))
        for p in port:
            p.position += rng.normal(0, amp, 3)
        if P.concentration(port, t + 1) >= seuil:
            return t + 1
    return None


def msg(graine):
    return np.random.default_rng(graine).integers(0, 2, 2048).astype(
        np.uint8).tobytes()


def bloc(etat, dA, dB):
    part, indep = 0, 0
    for i in range(30):
        m = msg(500 + i)
        sA = etape_q(phic(m), [0, 0, 0], dA + i, series[etat][i % 5])
        sB = etape_q(phic(m), [6, 0, 0], dB + i, series[etat][(i + 2) % 5])
        part += (sA == sB)
        sB2 = etape_q(phic(msg(9000 + i)), [6, 0, 0], dB + i,
                      series[etat][(i + 2) % 5])
        indep += (sA == sB2)
    return part, indep


if len(series["HIGH"]) < 5 or len(series["LOW"]) < 5:
    res = {"classe": "MIXTE", "critere": False, "raison": "séries incomplètes"}
else:
    hA, ihA = bloc("HIGH", 3800, 3900)
    lA, ilA = bloc("LOW", 3800, 3900)
    hB, ihB = bloc("HIGH", 4800, 4900)
    lB, ilB = bloc("LOW", 4800, 4900)
    dA, dB = hA - lA, hB - lB
    print(f"[62] blocA HIGH={hA} LOW={lA} d={dA} | blocB HIGH={hB} "
          f"LOW={lB} d={dB}", flush=True)
    if dA == 0 and dB == 0:
        classe = "DÉCOUPLÉ"
    elif dA * dB > 0 and abs(dA) >= 2 and abs(dB) >= 2:
        classe = "COUPLÉ_STRUCTUREL"
    else:
        classe = "MIXTE"
    res = {"blocA": {"HIGH": hA, "LOW": lA, "delta": dA},
           "blocB": {"HIGH": hB, "LOW": lB, "delta": dB},
           "classe": classe, "critere": bool(classe == "DÉCOUPLÉ")}
json.dump(res, open(os.path.join(HERE, "resultats", "exp62.json"), "w"), indent=1)
print(f"[62] RESULTAT classe={res['classe']} critere={res['critere']}")
