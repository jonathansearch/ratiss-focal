"""TEST-64 : sonde endogène (6 runs). Agent infodynamique LÂCHÉ dans
l'univers focal : il capte UN signal brut, le binarise (bit=1 si >
médiane causale 32 pas), mesure la complexité Lempel-Ziv sur fenêtre
glissante W=64 -> nouveauté propre (0..1), et ÉMET son train binaire
(1 = "nouveau pour moi" si nouveauté > mu_base + 2*sigma_base).
AUCUNE étiquette humaine : seuil = sa propre baseline (pas 50-150).
6 runs : 3 signaux (syncQ Kuramoto R(t) / Phi concentration porteurs /
P_sig tore G) x {calme, choc au pas 200-202}. Par signal : CHOC_DETECTÉ
si taux_post >= 0.10 ET (taux_base==0 ou ratio>=5) ; CALME_PROPRE si
taux <= 0.05. PASS signal = les deux. Critère : sonde VALIDE si >=2/3."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import porteurs as P

T, CHOC = 400, (200, 203)


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
    W = 64
    nov, flags = [], []
    base = []
    for t in range(T):
        if t < W:
            nov.append(0.0)
            flags.append(0)
            continue
        win = x[t - W:t]
        med = float(np.median(x[max(0, t - 32):t]))
        bits = (win > med).astype(int)
        n = lz76(bits) / (W / np.log2(W))
        nov.append(round(float(n), 4))
        if 50 <= t < 150:
            base.append(n)
    mu = float(np.mean(base))
    sd = float(np.std(base)) or 1e-9
    thr = mu + 2 * sd if sd > 1e-9 else mu + 0.01
    for t in range(W, T):
        flags.append(0)  # placeholder remplacé ci-dessous
    flags = [0] * W + [int(nov[t] > thr) for t in range(W, T)]
    taux_base = float(np.mean(flags[50:150]))
    taux_post = float(np.mean(flags[203:]))
    pic = int(W + int(np.argmax(nov[W:])))
    return {"nouveaute": nov, "bits": "".join(str(b) for b in flags),
            "seuil": round(thr, 4), "taux_base": round(taux_base, 4),
            "taux_post": round(taux_post, 4), "pic": pic}


# ---- signal 1 : syncQ R(t) ----
def run_syncq(choc):
    rng = np.random.default_rng(6401)
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


# ---- signal 2 : Phi concentration ----
def run_phi(choc):
    rng = np.random.default_rng(6402)
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


# ---- signal 3 : P_sig tore G ----
def run_psig(choc):
    rng = np.random.default_rng(6403)
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
        serie = fn(regime)
        r = sonde(serie)
        r["signal_fin"] = round(float(np.mean(serie[-10:])), 4)
        runs[tag] = r
        print(f"[64] {tag} : seuil={r['seuil']} base={r['taux_base']} "
              f"post={r['taux_post']} pic={r['pic']}", flush=True)
verdicts = {}
for nom in ("syncQ", "Phi", "Psig"):
    ch, ca = runs[f"{nom}_choc"], runs[f"{nom}_calme"]
    detect = ch["taux_post"] >= 0.10 and (
        ch["taux_base"] == 0 or ch["taux_post"] / max(ch["taux_base"], 1e-9) >= 5)
    propre = ca["taux_post"] <= 0.05
    verdicts[nom] = {"CHOC_DETECTÉ": bool(detect), "CALME_PROPRE": bool(propre),
                     "PASS": bool(detect and propre)}
n = sum(v["PASS"] for v in verdicts.values())
res = {"runs": runs, "verdicts": verdicts,
       "classe": "VALIDE" if n >= 2 else "AVEUGLE",
       "critere": bool(n >= 2)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp64.json"), "w"))
print(f"[64] RESULTAT {verdicts} -> {res['classe']} critere={res['critere']}")
