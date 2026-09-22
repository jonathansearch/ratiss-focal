"""TEST-54 : attracteur Q <-> sanctuaire U. Étape 1 : 12 runs Q
(settle60+choc+relâche300, seed 5400+j), classés HIGH/LOW (bandes
TEST-50 : >=0.84 / <=0.82), écart-type des fluctuations (250 derniers)
-> sigma_high, sigma_low. Barrière : >=2 runs/attracteur et écart
relatif >=10%, sinon SANS_OBJET. Étape 2 : ligne TEST-38 (T=20, mêmes
graines/messages, jitter=sigma_mesuré), 30+30 par cas. Critère :
INDÉPENDANT si partage identique (ΔS_U=0), sinon CORRÉLÉ + Δ chiffré."""
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


stds = {"HIGH": [], "LOW": []}
for j in range(12):
    seg = run_q(5400 + j)
    qf = float(np.mean(seg[-50:]))
    sd = float(np.std(seg[-250:]))
    if qf >= 0.84:
        stds["HIGH"].append(sd)
    elif qf <= 0.82:
        stds["LOW"].append(sd)
print(f"[54] runs HIGH={len(stds['HIGH'])} LOW={len(stds['LOW'])}", flush=True)
if len(stds["HIGH"]) >= 2 and len(stds["LOW"]) >= 2:
    sh, sl = float(np.mean(stds["HIGH"])), float(np.mean(stds["LOW"]))
    rel = abs(sh - sl) / max((sh + sl) / 2, 1e-9)
else:
    sh, sl, rel = None, None, 0.0
print(f"[54] sigma_high={sh} sigma_low={sl} écart_rel={rel:.3f}", flush=True)


def phic(msg: bytes) -> float:
    h = int(hashlib.sha256(msg).hexdigest(), 16)
    return 100 + 1900 * ((h % 1000) / 1000)


def etape(seuil, cible, seed_jit, jit):
    rng = np.random.default_rng(seed_jit)
    port = P.creer_porteurs(2048, 8, "I", seed=3)
    for p in port:
        p.position += np.array(cible, float)
    for t in range(20):
        P.transporter(port, cible, 0.12)
        for p in port:
            p.position += rng.normal(0, jit, 3)
        if P.concentration(port, t + 1) >= seuil:
            return t + 1
    return None


def msg(graine):
    return np.random.default_rng(graine).integers(0, 2, 2048).astype(
        np.uint8).tobytes()


def ligne(jit):
    part, indep = 0, 0
    for i in range(30):
        m = msg(500 + i)
        sA = etape(phic(m), [0, 0, 0], 3800 + i, jit)
        sB = etape(phic(m), [6, 0, 0], 3900 + i, jit)
        part += (sA == sB)
        sB2 = etape(phic(msg(9000 + i)), [6, 0, 0], 3900 + i, jit)
        indep += (sA == sB2)
    return part, indep


if sh is None or rel < 0.10:
    res = {"sigma_high": sh, "sigma_low": sl, "classe": "SANS_OBJET",
           "critere": False}
else:
    ph, ih = ligne(sh)
    pl, il = ligne(sl)
    d = abs(ph - pl)
    classe = "INDÉPENDANT" if d == 0 else f"CORRÉLÉ_delta={d}"
    res = {"sigma_high": round(sh, 5), "sigma_low": round(sl, 5),
           "HIGH": {"partage": ph, "indep": ih},
           "LOW": {"partage": pl, "indep": il}, "delta": d,
           "classe": classe, "critere": bool(d == 0)}
    print(f"[54] HIGH-jitter: {ph}/30 vs {ih}/30 | LOW-jitter: {pl}/30 vs "
          f"{il}/30", flush=True)
json.dump(res, open(os.path.join(HERE, "resultats", "exp54.json"), "w"), indent=1)
print(f"[54] RESULTAT classe={res['classe']} critere={res['critere']}")
