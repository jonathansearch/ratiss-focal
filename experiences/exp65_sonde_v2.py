"""TEST-65 : sonde endogène v2 (6 runs, graines fraîches 6501-6503).
Leçon TEST-64 (AVEUGLE assumé) : un choc de 3 pas fait des pointes,
pas des plateaux. Sonde v2 : fenêtre courte W=16 (sensible aux
transitoires), LZ76 brut (sans normalisation saturante), binarisation
vs médiane causale 16 pas, seuil = mu_base+2*sigma_base (pas 50-150).
Rafale = nb de flags dans une fenêtre. Critère COMPARATIF (zéro ligne
absolue) : PASS signal si rafale_choc[198,212] >= 4 ET >= 2x pire
rafale du run calme (fenêtres 15 pas sur [150,400]). Critère : sonde
VALIDE si >=2/3 signaux PASS (syncQ / Phi / Psig, mêmes appareils)."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import porteurs as P

T, CHOC = 400, (200, 203)
W = 16


def lz76(bits):
    s = "".join(str(int(b)) for b in bits)
    n, i, c = len(s), 0, 0
    while i < n:
        j = i + 1
        while j <= n and s[i:j] in s[:i]:
            j += 1
        c += 1
        i = j
    return c


def sonde(serie):
    x = np.array(serie, float)
    nov = [0.0] * W
    for t in range(W, T):
        win = x[t - W:t]
        med = float(np.median(x[max(0, t - W):t]))
        nov.append(float(lz76((win > med).astype(int))))
    base = nov[50:150]
    mu, sd = float(np.mean(base)), float(np.std(base))
    thr = mu + 2 * sd if sd > 1e-9 else mu + 0.5
    flags = [0] * W + [int(n > thr) for n in nov[W:]]
    return {"nouveaute": [round(n, 3) for n in nov],
            "bits": "".join(str(b) for b in flags),
            "seuil": round(thr, 3)}


def rafale(flags, a, b):
    return sum(flags[a:b])


def pire_rafale_calme(flags):
    return max(sum(flags[t:t + 15]) for t in range(150, 386))


def run_syncq(choc):
    rng = np.random.default_rng(6501)
    NQ, KQ, DTQ = 24, 3.0, 0.3
    OM = np.random.default_rng(55).normal(0, 0.2, NQ)
    adj = np.zeros((NQ, NQ))
    for i in range(NQ):
        adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
    adj[0, :] = adj[:, 0] = 1.0
    adj[12, :] = adj[:, 12] = 1.0
    np.fill_diagonal(adj, 0.0)
    th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
    out = []
    for t in range(T):
        if choc and CHOC[0] <= t < CHOC[1]:
            th = th + rng.normal(0, 1.0, NQ)
        else:
            th = th + DTQ * (OM + (KQ / NQ) * (
                adj * np.sin(th[None, :] - th[:, None])).sum(1))
        out.append(float(np.abs(np.exp(1j * th).mean())))
    return out


def run_phi(choc):
    rng = np.random.default_rng(6502)
    port = P.creer_porteurs(2048, 8, "I", seed=3)
    out = []
    for t in range(T):
        if choc and CHOC[0] <= t < CHOC[1]:
            P.transporter(port, [0, 0, 0], -0.12)
            jit = 0.4
        else:
            P.transporter(port, [0, 0, 0], 0.12)
            jit = 0.04
        for p in port:
            p.position += rng.normal(0, jit, 3)
        out.append(float(P.concentration(port, t + 1)))
    return out


def run_psig(choc):
    rng = np.random.default_rng(6503)
    g = C.fond(seed=24)[:160].copy()
    pref = C.p_sig(g)
    out = []
    for t in range(T):
        if choc and CHOC[0] <= t < CHOC[1]:
            al, sg = -0.15, 0.05
        else:
            al, sg = 0.1, 0.005
        d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
        g = g + al * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
        g = g + rng.normal(0, sg, g.shape)
        out.append(float(C.p_sig(g) / pref))
    return out


runs = {}
for nom, fn in (("syncQ", run_syncq), ("Phi", run_phi), ("Psig", run_psig)):
    for regime in (False, True):
        tag = f"{nom}_{'choc' if regime else 'calme'}"
        runs[tag] = sonde(fn(regime))
verdicts = {}
for nom in ("syncQ", "Phi", "Psig"):
    ch = runs[f"{nom}_choc"]
    ca = runs[f"{nom}_calme"]
    fch = [int(b) for b in ch["bits"]]
    fca = [int(b) for b in ca["bits"]]
    rc = rafale(fch, 198, 213)
    pire = pire_rafale_calme(fca)
    ok = rc >= 4 and rc >= 2 * max(pire, 1)
    verdicts[nom] = {"rafale_choc": rc, "pire_calme": pire,
                     "PASS": bool(ok)}
    print(f"[65] {nom} : rafale_choc={rc} pire_calme={pire} PASS={ok}",
          flush=True)
n = sum(v["PASS"] for v in verdicts.values())
res = {"runs": runs, "verdicts": verdicts,
       "classe": "VALIDE" if n >= 2 else "AVEUGLE",
       "critere": bool(n >= 2)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp65.json"), "w"))
print(f"[65] RESULTAT -> {res['classe']} critere={res['critere']}")
