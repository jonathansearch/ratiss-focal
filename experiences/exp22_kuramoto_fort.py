"""TEST-22 (05b) : Kuramoto fort (K x1.5 = 3.0, T x2 = 24). Point de bascule exact.
Critère : sync stable > 0.1 en <= 12 pas, sans effondrer P_sig."""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import porteurs as P

cfg = json.load(open(os.path.join(os.path.dirname(HERE), "univers", "B.json")))
T, N, K = 24, cfg["noeuds"], cfg["K_kuramoto"] * 1.5
fond_pts = C.fond(seed=cfg["graine_fond"])
P_ref = C.p_sig(fond_pts)
rng = np.random.default_rng(cfg["graine_reseau"])
ang = np.linspace(0, 2 * np.pi, N, endpoint=False)
ancres0 = np.column_stack([2.2 * np.cos(ang), 2.2 * np.sin(ang), np.zeros(N)])
adj = np.zeros((N, N))
for i in range(N):
    adj[i, (i - 1) % N] = adj[i, (i + 1) % N] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
theta = rng.uniform(0, 2 * np.pi, N)
omega = rng.normal(0, 0.2, N)
port = P.creer_porteurs(cfg["n_bits_structure"], cfg["n_porteurs"], "S", seed=9)
serie, syncs, focal, bascule = [], [], None, None
for t in range(T):
    theta = theta + cfg["dt"] * (omega + (K / N)
                                 * (adj * np.sin(theta[None, :] - theta[:, None])).sum(1))
    radial = ancres0 / np.linalg.norm(ancres0, axis=1, keepdims=True)
    pts = np.vstack([fond_pts, ancres0 + radial * (0.15 * np.sin(theta))[:, None]])
    P.transporter(port, cfg["point_focal"], cfg["alpha_transport"])
    if focal is None and P.concentration(port, t + 1) >= cfg["phi_c"]:
        focal = t + 1
        pts = np.vstack([pts, C.boucle_focale(cfg["point_focal"])])
    serie.append(C.p_sig(pts) / P_ref)
    syncs.append(float(np.abs(np.exp(1j * theta).mean())))
    if bascule is None and syncs[-1] > 0.1:
        bascule = t + 1
    print(f"[22] pas {t + 1:02d} sync={syncs[-1]:.3f} P/P_ref={serie[-1]:.4f}", flush=True)
stable = float(np.mean(syncs[-6:])) > 0.1
res = {"K": K, "T": T, "sync_serie": [round(x, 4) for x in syncs],
       "bascule_etape": bascule, "sync_finale": round(syncs[-1], 4),
       "P_final_norme": round(float(serie[-1]), 4), "focalisation_etape": focal,
       "critere": bool(bascule is not None and bascule <= 12 and stable
                        and serie[-1] > 0.5)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp22.json"), "w"), indent=1)
print(f"[22] RESULTAT bascule={bascule} sync_finale={syncs[-1]:.3f} "
      f"critere={res['critere']}")
