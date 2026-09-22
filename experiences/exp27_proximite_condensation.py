"""TEST-27 (M10c) : loi de Proximité-Condensation, niveau CORRECT (local).
(A) Gate doux -> rho_c. (B) Interrupteur dur bilatéral -> sync CONDITIONNELLE :
actifs (rho>=rho_c) vs inactifs. La loi est locale, le mètre est local.
Critère : contraste actifs-inactifs > 0.3 loin + actifs syncés près + contrôles."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

INFO = np.random.default_rng(27).normal(0, 2.0, (400, 3))
N, K_SCAN, K_HAUT, T, DT, SIG_K = 24, 4.0, 6.0, 24, 0.3, 1.0
rng = np.random.default_rng(55)
OMEGA = rng.normal(0, 0.2, N)
DS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

adj = np.zeros((N, N))
for i in range(N):
    adj[i, (i - 1) % N] = adj[i, (i + 1) % N] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)


def rho_noeuds(D):
    ang = np.linspace(0, 2 * np.pi, N, endpoint=False)
    noeuds = np.column_stack([2.2 * np.cos(ang) + D, 2.2 * np.sin(ang),
                              np.zeros(N)])
    d2 = ((noeuds[:, None, :] - INFO[None, :, :]) ** 2).sum(-1)
    return noeuds, np.exp(-d2 / (2 * SIG_K ** 2)).sum(1)


RHOS = {D: rho_noeuds(D)[1] for D in DS}
RHO_MAX = max(v.max() for v in RHOS.values())
fond_pts = C.fond(seed=24)
P_ref = C.p_sig(fond_pts)


def ordre(theta):
    return float(np.abs(np.exp(1j * theta).mean()))


def run(D, K, mode, rho_c=0.0, detail=False):
    r = np.random.default_rng(100)
    theta = r.uniform(0, 2 * np.pi, N)
    rho = RHOS[D]
    if mode == "doux":
        keff = K * (rho / RHO_MAX)
    elif mode == "dur":
        keff = np.where(rho >= rho_c, K, 0.0)
    else:
        keff = np.full(N, K)
    for _ in range(T):
        if mode == "dur":
            km = np.minimum(keff[:, None], keff[None, :])  # bilatéral
        else:
            km = (keff[:, None] + keff[None, :]) / 2
        theta = theta + DT * (OMEGA + (1.0 / N) * (
            adj * km * np.sin(theta[None, :] - theta[:, None])).sum(1))
    noeuds, _ = rho_noeuds(D)
    rad = noeuds / np.linalg.norm(noeuds, axis=1, keepdims=True)
    pts = np.vstack([fond_pts, noeuds + rad * (0.15 * np.sin(theta))[:, None]])
    s, p = ordre(theta), C.p_sig(pts) / P_ref
    if detail and mode == "dur":
        act = rho >= rho_c
        sa = ordre(theta[act]) if act.sum() >= 3 else None
        si = ordre(theta[~act]) if (~act).sum() >= 3 else None
        return s, p, sa, si, int(act.sum())
    return s, p


print("--- (A) gate doux : mesure ---", flush=True)
tableA = {}
for D in DS:
    s, p = run(D, K_SCAN, "doux")
    tableA[str(D)] = {"rho_bar": round(float(RHOS[D].mean()), 2),
                      "sync": round(s, 4)}
    print(f"[27A] D={D} rho={tableA[str(D)]['rho_bar']} sync={s:.4f}", flush=True)
paires = sorted(((tableA[str(D)]["rho_bar"], tableA[str(D)]["sync"]) for D in DS),
                reverse=True)
rho_c = None
for (r1, s1), (r2, s2) in zip(paires, paires[1:]):
    if s1 >= 0.3 >= s2:
        f = (0.3 - s2) / max(s1 - s2, 1e-9)
        rho_c = round(r2 + f * (r1 - r2), 3)
        break
print(f"[27A] rho_c extrait = {rho_c}", flush=True)
print("--- (B) interrupteur dur : sync conditionnelle ---", flush=True)
tableB, ok = {}, rho_c is not None
if ok:
    for D in DS:
        s, p, sa, si, na = run(D, K_SCAN, "dur", rho_c, detail=True)
        tableB[str(D)] = {"sync": round(s, 4), "sync_actifs": sa,
                          "sync_inactifs": si, "n_actifs": na,
                          "P_norme": round(float(p), 4)}
        print(f"[27B] D={D} n_act={na} sync_act={sa} sync_inact={si}", flush=True)
s_gate, _ = run(5.0, K_HAUT, "dur", rho_c or 0.0)
s_pur, _ = run(5.0, K_SCAN, "pur")
frac = [tableB[str(D)]["n_actifs"] / N for D in DS] if ok else []
glb = [tableB[str(D)]["sync"] for D in DS] if ok else []
corr_fs = round(float(np.corrcoef(frac, glb)[0, 1]), 4) if ok else None
b5 = tableB.get("5.0", {})
leg_loin = ok and (b5.get("n_actifs", N) <= 3 or (
    b5.get("sync_actifs") is not None and b5.get("sync_inactifs") is not None
    and b5["sync_actifs"] - b5["sync_inactifs"] > 0.3))
b05 = tableB.get("0.5", {})
leg_pres = ok and b05.get("sync_actifs") is not None and b05["sync_actifs"] > 0.5
res = {"table_doux": tableA, "rho_c": rho_c, "table_dur": tableB, "D_c": None,
       "corr_fraction_sync": corr_fs,
       "controle_D5_gate_K6": round(s_gate, 4),
       "controle_D5_pur_K4": round(s_pur, 4),
       "critere": bool(leg_loin and leg_pres and s_pur > 0.3
                       and s_gate < s_pur - 0.2)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp27.json"), "w"), indent=1)
print(f"[27] RESULTAT rho_c={rho_c} corr_frac_sync={corr_fs} leg_loin={leg_loin} "
      f"leg_pres={leg_pres} critere={res['critere']}")
