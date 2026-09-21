# 🌌 UNIFICATION — les 7 résultats fusionnés en un univers cohérent

*21/09 nuit. Tout rejouable : `python3 experiences/exp01_fond_temoin.py` … `exp07`.*

## Les 7 résultats
| # | Test | Résultat |
|---|------|----------|
| 01 | Fond + témoin | ✅ stable (1.003 ± 0.021, critère 15 %) — P_ref = 5.76 |
| 02 | Condensateur | ✅ info pure (entropie 0.997), P = 1.20, pas d'effondrement |
| 03 | Porteurs | ✅ tranches disjointes, franchissement I=3, S=4 (Φ_c=500) |
| 04 | Univers A | 🟡 focalise (étape 3) MAIS ΔP = −0.10 (voir F1) |
| 05 | Univers B | 🟡 focalise (étape 4), ΔP = +0.29, MAIS sync = 0.02 (voir F2) |
| 06 | Verdicts | ✅ sœurs (convergence) ; anti-triche 2.03, passe de justesse (voir F3) |
| 07 | Unifié-v1 | ✅ focalise (étape 3), croît à 1.19, cohérent |

## 3 trouvailles honnêtes (pas cachées, gravées)
- **F1 — le lissage ronge le fond** : en A, la règle de lissage s'applique à tout
  le nuage et érode les cycles du fond (−10 %). Piste : lisser seulement les
  points injectés, ou baisser le taux.
- **F2 — Kuramoto sous-critique** : en B, K/N × degré ≈ 0.33 ≈ seuil critique →
  le réseau implanté ne se synchronise pas (sync 0.02) en 12 pas. Piste : K plus
  fort ou T plus long. L'implantation donne quand même +29 % de P_sig.
- **F3 — anti-triche de justesse** : ratio 2.03 > 2.0, ça passe mais fragile.
  Piste : durcir le mètre (diagrammes complets au lieu des séries).

## L'univers unifié v1
`univers/unifie.json` : P_ref = 5.76, Φ_c^lab = 500, franchissements I=3/S=4,
mécanismes [fond, filet_info, transport, seuil], verdict d'origine « sœurs ».
Le run de démonstration focalise et croît sans s'effondrer → **cohérent**.

## Rejouer (R7)
```
cd ratiss-focal-local
for i in 01 02 03 04 05 06 07; do python3 experiences/exp${i}_*.py; done
```
Dépendances : numpy + ripser. Zéro clé, zéro cloud.

---
*Prochaines étapes sur ordre : TEST-04b (lissage restreint), TEST-05b (K fort),
anti-triche v3 (diagrammes complets).* 🔒
