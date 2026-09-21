"""TEST-05 : univers B (implantation, réseau Kuramoto). R7: python3 experiences/exp05_univers_B.py"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import porteurs as P

cfg = json.load(open(os.path.join(os.path.dirname(HERE), "univers", "B.json")))
T, N = cfg["T"], cfg["noeuds"]
fond_pts = C.fond(seed=cfg["graine_fond"])
P_ref = C.p_sig(fond_pts)
rng = np.random.default_rng(cfg["graine_reseau"])
ang = np.linspace(0, 2 * np.pi, N, endpoint=False)
ancres0 = np.column_stack([2.2 * np.cos(ang), 2.2 * np.sin(ang), np.zeros(N)])
adj = np.zeros((N, N))
for i in range(N):
    adj[i, (i - 1) % N] = adj[i, (i + 1) % N] = 1.0
adj[0, :] = adj[:, 0] = 1.0          # hubs implantés
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
theta = rng.uniform(0, 2 * np.pi, N)
omega = rng.normal(0, 0.2, N)
port = P.creer_porteurs(cfg["n_bits_structure"], cfg["n_porteurs"], "S", seed=9)
serie, phis, focal = [], [], None
for t in range(T):
    theta = theta + cfg["dt"] * (omega + (cfg["K_kuramoto"] / N)
                                 * (adj * np.sin(theta[None, :] - theta[:, None])).sum(1))
    radial = ancres0 / np.linalg.norm(ancres0, axis=1, keepdims=True)
    ancres = ancres0 + radial * (0.15 * np.sin(theta))[:, None]
    P.transporter(port, cfg["point_focal"], cfg["alpha_transport"])
    phis.append(P.concentration(port, t + 1))
    pts = np.vstack([fond_pts, ancres])
    if focal is None and phis[-1] >= cfg["phi_c"]:
        focal = t + 1
        pts = np.vstack([pts, C.boucle_focale(cfg["point_focal"])])
    serie.append(C.p_sig(pts) / P_ref)
    sync = float(np.abs(np.exp(1j * theta).mean()))
    print(f"[05] pas {t + 1:02d} P/P_ref={serie[-1]:.4f} phi={phis[-1]:.1f} sync={sync:.3f}",
          flush=True)
res = {"univers": "B-implantation",
       "serie_P_normee": [round(float(x), 4) for x in serie],
       "focalisation_etape": focal,
       "delta_P": round(float(serie[-1] - 1.0), 4),
       "sync_finale": round(sync, 4)}
json.dump(res, open(os.path.join(HERE, "resultats", "exp05.json"), "w"), indent=1)
print(f"[05] RESULTAT focalisation={focal} delta_P={res['delta_P']} sync={res['sync_finale']}")
