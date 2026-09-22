"""TEST-82 : trou noir v2 — horizon ABSORBANT (itération sur TEST-73).
Question que je me pose : le tueur a fait un puits parce qu'il
SOUSTRAIT sans borne ; et si l'horizon était une condition limite
(th=0 épinglé dans r<r_h, vrai gouffre) ? Grille 40x40, D=0.05,
source rayures entretenue (lignes 32-39), T=800. r_h dans {0, 2, 4, 6}
cellules (r_h=0 = témoin sans trou). On regarde : profil radial a(r),
profondeur de l'ombre juste hors horizon vs loin, franges éventuelles.
Observation pure, zéro verdict."""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
N, D, T = 40, 0.05, 800
cx = cy = N // 2
ii, jj = np.mgrid[0:N, 0:N]
dd = np.sqrt((ii - cx) ** 2 + (jj - cy) ** 2)
xs = np.arange(N)
stripes = 0.6 * (0.5 + 0.5 * np.sin(2 * np.pi * xs / 8))


def run(rh):
    th = np.zeros((N, N))
    th[N // 2:, :] = stripes[None, :]
    trou = dd < rh
    for _ in range(T):
        lap = (np.roll(th, 1, 0) + np.roll(th, -1, 0) +
               np.roll(th, 1, 1) + np.roll(th, -1, 1) - 4 * th)
        th = th + D * lap
        th[trou] = 0.0
        th[32:, :] = stripes[None, :]
    a = np.abs(th)
    prof = []
    for r0 in range(0, 20):
        m = (dd >= r0) & (dd < r0 + 1)
        prof.append(round(float(a[m].mean()) if m.sum() else 0.0, 4))
    a_loin = float(np.mean(prof[14:]))
    bord = float(np.mean(prof[rh + 1:rh + 3])) if rh + 3 <= 20 else a_loin
    return {"r_h": rh, "a_loin": round(a_loin, 4),
            "a_bord": round(bord, 4),
            "contraste": round(1 - bord / a_loin, 4) if a_loin > 0 else 0.0,
            "profil": prof}


lignes = []
for rh in (0, 2, 4, 6):
    r = run(rh)
    lignes.append(r)
    print(f"[82] r_h={rh} : a_loin={r['a_loin']} a_bord={r['a_bord']} "
          f"contraste={r['contraste']}", flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "resultats", "exp82.json"), "w"), indent=1)
print("[82] OBSERVÉ : 4 horizons, profils archivés.")
