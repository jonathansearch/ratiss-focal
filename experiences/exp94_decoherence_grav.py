#!/usr/bin/env python3
"""TEST-94 : DECOHERENCE GRAVITATIONNELLE — le calcul qui exige les DEUX
échelles à la fois (Pikovski et al., Nat. Phys. 2015, version focale).
N paires = N superpositions : branche A à r0, branche B à r0+dh.
Fréquence interne ω par paire, spread sw (degrés internes = pilier QM).
Horloge locale f(r) = 1 - G0*exp(-r/sig) (redshift TEST-84 = pilier GR).
Cohérence mutuelle C(t) = |moy exp(i(thA-thB))|, intégrée pas à pas.
Prédit : C = exp(-(t/tau)^2), tau = sqrt(2)/(sw*|Df|).
Controles : G0=0 ou dh=0 ou sw=0 -> tau=infini (effet mort).
Si 1/tau proportionnel à Df*sw : l'effet N'EXISTE que par QM x GR.
Zéro verdict, observation pure.
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "resultats", "exp94.json")

N, T, DT = 400, 1000.0, 1.0
W0, SIG, R0 = 1.0, 3.0, 2.0


def f(r, g0):
    return 1.0 - g0 * math.exp(-r / SIG)


def run_case(dh, g0, sw, seed=7, courbe=False):
    rng = np.random.default_rng(seed)
    w = rng.normal(W0, sw, N) if sw > 0 else np.full(N, W0)
    df = f(R0, g0) - f(R0 + dh, g0)
    dphi = w * df * DT
    steps = int(T / DT)
    phi = np.zeros(N)
    ts, cs = [], []
    for s in range(steps + 1):
        if s % 10 == 0:
            ts.append(s * DT)
            cs.append(float(abs(np.mean(np.exp(1j * phi)))))
        phi = phi + dphi
    cs = np.array(cs)
    m = cs > 0.3
    if m.sum() > 5 and cs[m][-1] < 0.95:
        slope = np.polyfit((np.array(ts)[m]) ** 2, np.log(cs[m]), 1)[0]
        tau = float(math.sqrt(-1 / slope)) if slope < 0 else float("inf")
    else:
        tau = float("inf")
    theo = (float(math.sqrt(2) / (sw * abs(df)))
            if (sw > 0 and abs(df) > 1e-12) else float("inf"))
    res = {"dh": dh, "g0": g0, "sw": sw, "Df": round(df, 6),
           "tau_mes": round(tau, 1) if tau != float("inf") else "inf",
           "tau_theo": round(theo, 1) if theo != float("inf") else "inf",
           "C_fin": round(float(cs[-1]), 4)}
    if courbe:
        res["t"] = ts
        res["C"] = [round(c, 4) for c in cs]
    return res


if __name__ == "__main__":
    print("dh    g0    sw    Df        tau_mes  tau_theo C_fin", flush=True)
    cas = []
    for dh in (0, 2, 5, 10):
        for g0 in (0, 0.05, 0.1, 0.2):
            for sw in (0.0, 0.05, 0.1):
                courbe = (g0 == 0.1 and sw == 0.1)
                r = run_case(dh, g0, sw, courbe=courbe)
                cas.append(r)
                print(f"{dh:<5} {g0:<5} {sw:<5} {r['Df']:<9} "
                      f"{r['tau_mes']!s:<8} {r['tau_theo']!s:<8} {r['C_fin']}",
                      flush=True)
    json.dump({"cas": cas}, open(OUT, "w"), indent=0)
    print(f"[94] archivé : {OUT}")
