# 📋 FICHE-VALIDATION — théorie focale → réel (suivi unique)

> Règle chef : pas de hasard, on suit la fiche. D'abord TOUT ce qui peut
> sortir sur QPU, ensuite (si nécessaire) les autres outils en ligne.
> Objectif : prouver que l'univers virtuel est cohérent avec la réalité.

## Colonne QPU (IBM, gratuit) — 5 ponts

| # | Théorie (virtuel) | Pont | Statut 2026-09-22 |
|---|---|---|---|
| 1 | TEST-77 : capture k_c=6/24 tue la sync | PONT-77 (GHZ + k avalés → fidélité) | ✅ MESURÉ (marrakesh, F 0.84→0.00) |
| 2 | TEST-76 : U ÉRODÉ sous trou local | PONT-76 (Bell + bruit 1 côté → P(mêmes)) | ✅ MESURÉ (marrakesh, 0.98→0.31) |
| 3 | RUQ t_half=11 + TEST-60 flip piloté | PONT-60 (T1 + H-Rz-H) | ✅ MESURÉ (kingston, T1=285.4us, cosinus) |
| 4 | RUQ relaxation de phase | PONT-T2 (Ramsey → T2*) | ✅ MESURÉ (marrakesh, T2*=70.2us) |
| 5 | TEST-72 H2 : la structure récupère | PONT-72 (Ramsey vs écho Hahn → T2echo/T2*) | ✅ MESURÉ (kingston, 14.4→63.4us, x4.4) |

## Colonne autres outils (jumeaux prêts, cases téléphone à cocher)

| Théorie | Outil gratuit | Statut 2026-09-22 |
|---|---|---|
| TEST-82 : ombre absorbante 0.66 | Falstad Ripple Tank | ✅ VALIDÉ TÉLÉPHONE (chef : ombre vue, Obstacle) |
| TEST-81 : lentille en S | Falstad Slow Medium | ✅ VALIDÉ TÉLÉPHONE (chef : resserrement vu, zone bleue) |
| TEST-80 : twist −2 | Wokwi twist (firmware prêt) | ✅ VALIDÉ (Manus IA, Wokwi saturé : R=0.9096/0.4081 pile prédit) |
| TEST-84 : redshift monotone | Wokwi redshift (firmware prêt) | 🟡 JUMEAU OK (TEST-89 : −0.77→−0.11) — série à lire |
| TEST-74 : loi exponentielle 12/12 | analytique (déjà R²=0.998) | loi ajustée, pas de hardware |
| RUQ/porteurs/UKTZ (agents) | rien de gratuit adapté → reste virtuel | mobilité + fond + charges |

## Lecture
- QPU couvre : capture, érosion, relaxation, flip, récupération = le cœur
  « quantique » (cohérence, mémoire, contrôle).
- Les outils en ligne couvriront : ombre, lentille, twist, redshift = le
  versant « spatial/relativité ».
- Reste virtuel assumé : agents mobiles (RUQ/UKTZ/porteurs) — pas de
  banc gratuit adapté à ce jour.

---
*MAJ à chaque pont mesuré. Preuve visée : courbes réel≈simu sur les 5 ponts.* 🔒
