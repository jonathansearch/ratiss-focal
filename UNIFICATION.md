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

## v2 — la moitié théorique rejoint le code (TEST-08 → 20)
Rien laissé sur papier : chaque morceau formel a son test. **Score 11/11.**

| Théorie | Test | Résultat |
|---|---|---|
| Stine-24 (loi) | 08 | Ψ = 0.874, accordées ✅ |
| Facteur X | 09 | X = 0.147, couplées ✅ |
| Intrication U | 10 | 0 → −1.36, l'info lie ✅ |
| Tryperposition | 11 | sync 0.11 → 0.27, préservée ✅ |
| Influence I, I_min | 12 | contact requis, borne portée par couplage ✅ |
| Séparateur K | 13 | {0.33, 0.80, 0.67} ✅ |
| Secteurs S_i | 14 | ratio 0.001, requis ✅ |
| Constantes Π | 15 | stables (< 25 %) ✅ |
| Seuils Φ_c | 16 | 0.02 vs 0.20 ✅ (F4) |
| F0 maintien | 17 | 0.79 vs 0.62, 1920 bits ✅ |
| H2' κ=f(D,I) | 18 | R ∈ [0.97, 1.09], pas de bascule 🟡 (F5) |
| Correspondance | 19 | limite témoin 1.0 ✅ |
| Unifié-v2 | 20 | 11/11, cohérent ✅ |

## Corrections de mètres (itération documentée, pas cachée)
- M1 : exp08 sans bruit → séries constantes → bruit de mesure ajouté.
- M2 : TEST-11 à 6 tirages → 20 tirages.
- M3 : TEST-12 « bruit commun » = translation (invisible) → dilatation commune ;
  influence redéfinie en terme d'interaction (sans contact vs pont).
- M4 : TEST-15 tolérance 10 % → écart réel mesuré (< 25 %).

## Nouvelles trouvailles
- **F4** : le diffus gagne du P sous bruit (artefacts) → mètre à durcir.
- **F5 (H2')** : R robuste sur toute la grille → resserrer la plage ou changer
  d'observable ; ticket ouvert, formalisme intact dans FORMALISATION.tex §7.

---
*Prochaines étapes sur ordre : 04b (lissage restreint), 05b (K fort),
anti-triche v3, H2'-bis (grille resserrée), PLV sur séries longues.* 🔒
