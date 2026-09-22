"""TEST-66 : sonde endogène v3 deux-canaux (graines fraîches 6601-6603).
Leçons assumées : TEST-64 AVEUGLE (W=64 sent la pointe Phi mais gates
voulaient un plateau) ; TEST-65 AVEUGLE (W=16 : LZ sans dynamique,
silence total). Flaw principiel : la binarisation vs médiane EFFACE les
sauts de niveau (transitoire constant = LZ BASSE). Sonde v3 : canal
TEXTURE (LZ76 W=64 normalisé, seuil propre mu+2sigma, base 50-150) +
canal VOLATILITÉ (|x - médiane causale 32|, seuil propre mu+2sigma).
Flag = texture OU volatilité. 100% endogène : aucun seuil humain.
Critère COMPARATIF (cf. TEST-65) : PASS signal si rafale_choc[198,213]
>= 4 ET >= 2x pire rafale du run calme (fenêtres 15 pas, [150,400]).
Critère : VALIDE si >=2/3 signaux (syncQ / Phi / Psig)."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import porteurs as P

T, CHOC = 400, (200, 203)
W = 64


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
    tex, vol = [0.0] * W, [0.0] * W
    for t in range(W, T):
        win = x[t - W:t]
        med = float(np.median(x[max(0, t - 32):t]))
        tex.append(lz76(((win > med).astype(int))) / (W / np.log2(W)))
        vol.append(abs(float(x[t]) - med))
    bt, bv = tex[50:150], vol[50:150]
    mt, st = float(np.mean(bt)), float(np.std(bt))
    mv, sv = float(np.mean(bv)), float(np.std(bv))
    tht = mt + 2 * st if st > 1e-9 else mt + 0.01
    thv = mv + 2 * sv if sv > 1e-9 else mv + 1e-9
    flags = [0] * W + [int(tex[t] > tht or vol[t] > thv)
                       for t in range(W, T)]
    return {"texture": [round(n, 3) for n in tex],
            "volatilite": [round(n, 5) for n in vol],
            "bits": "".join(str(b) for b in flags),
            "seuils": [round(tht, 3), round(thv, 5)]}


def run_syncq(choc):
    rng = np.random.default_rng(6601)
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
    rng = np.random.default_rng(6602)
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
    rng = np.random.default_rng(6603)
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
        runs[f"{nom}_{'choc' if regime else 'calme'}"] = sonde(fn(regime))
verdicts = {}
for nom in ("syncQ", "Phi", "Psig"):
    fch = [int(b) for b in runs[f"{nom}_choc"]["bits"]]
    fca = [int(b) for b in runs[f"{nom}_calme"]["bits"]]
    rc = sum(fch[198:213])
    pire = max(sum(fca[t:t + 15]) for t in range(150, 386))
    ok = rc >= 4 and rc >= 2 * max(pire, 1)
    verdicts[nom] = {"rafale_choc": rc, "pire_calme": pire,
                     "PASS": bool(ok)}
    print(f"[66] {nom} : rafale_choc={rc} pire_calme={pire} PASS={ok}",
          flush=True)
n = sum(v["PASS"] for v in verdicts.values())
res = {"runs": runs, "verdicts": verdicts,
       "classe": "VALIDE" if n >= 2 else "AVEUGLE",
       "critere": bool(n >= 2)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp66.json"), "w"))
print(f"[66] RESULTAT -> {res['classe']} critere={res['critere']}")
