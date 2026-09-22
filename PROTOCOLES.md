# 📋 PROTOCOLES — 7 étapes majeures (TEST-01 → TEST-07)

*Ordre du chef 21/09 : séquentiel, chacun avec son résultat, puis unification.
R7 : 1 commande par test. Graines fixées partout.*

## TEST-01 — Fond + témoin (le conteneur tient ?)
- **Méthode** : construire le fond (tore + sphère = cycles H1/H2 stables),
  mesurer P_ref, puis 12 pas de bruit de mesure.
- **Critère** : P_sig(t)/P_ref stable (écart < 15 %). Sinon le labo ne tient pas.
- **Résultat** : `experiences/resultats/exp01.json`

## TEST-02 — Condensateur Q_info (l'info pure se charge ?)
- **Méthode** : 2048 bits, entropie + taille compressée, injection neutre
  (60 points) dans le fond.
- **Critère** : entropie ≈ 1 bit/bit (info pure) et P_sig ne s'effondre pas.
- **Résultat** : `experiences/resultats/exp02.json`

## TEST-03 — Porteurs (le transport concentre ?)
- **Méthode** : 8 porteurs Type-I (2048 bits) + 8 Type-S (512 bits),
  tranches disjointes vérifiées, transport vers le point focal, Φ(t).
- **Critère** : tranches strictement disjointes + Φ franchit Φ_c^lab=500.
- **Résultat** : `experiences/resultats/exp03.json`

## TEST-04 — Univers A (l'émergence opère ?)
- **Méthode** : fond + filet d'info (4 pts/pas) + lissage local + porteurs I
  + seuil → boucle de focalisation si franchi.
- **Critère** : séries P_sig(t) enregistrées ; focalisation = structure apparue.
- **Résultat** : `experiences/resultats/exp04.json`

## TEST-05 — Univers B (l'implantation opère ?)
- **Méthode** : fond + réseau implanté (24 nœuds, anneau + hubs, Kuramoto)
  + porteurs S + même seuil.
- **Critère** : séries P_sig(t) enregistrées, comparables à A (même pipeline).
- **Résultat** : `experiences/resultats/exp05.json`

## TEST-06 — Fil + anti-triche + verdicts (qui dit vrai ?)
- **Méthode** : même mètre sur A et B ; complexité(règles A) vs
  complexité(structure observée) via compression ; verdicts scellés §8.
- **Critère** : tableau comparatif + 1 verdict appliqué honnêtement.
- **Résultat** : `experiences/resultats/exp06.json`

## TEST-07 — Unification (un seul univers cohérent ?)
- **Méthode** : constantes mesurées (P_ref, Φ_c, franchissements) fusionnées
  en `univers/unifie.json` + run de démonstration 12 pas.
- **Critère** : l'univers unifié focalise et reste cohérent (pas d'effondrement).
- **Résultat** : `experiences/resultats/exp07.json` + `UNIFICATION.md`

## TEST-08 — Stine-24 (les couches restent accordées ?)
- **Méthode** : séries P par couche (avec bruit de mesure), fidélités f_i,
  Ψ_sync = racine cubique (f1·f2·f3).
- **Critère** : Ψ_final > 0.8. **Résultat** : Ψ = 0.874 ✅

## TEST-09 — Facteur X (les couches sont couplées ?)
- **Méthode** : X = moyenne des |corr| entre séries de couches (exp08).
- **Critère** : X > 0.1. **Résultat** : X = 0.147 ✅ (macro↔micro 0.33)

## TEST-10 — Intrication U (l'info lie les couches ?)
- **Méthode** : U = P_joint − ΣP_couches, fond (contrôle) vs chargé.
- **Critère** : |U_chargé| > |U_fond|. **Résultat** : 0 → −1.36 ✅

## TEST-11 — Tryperposition (le collapse préserve la sync ?)
- **Méthode** : 20 tirages, amputation 30 % d'une couche, sync avant/après.
- **Critère** : ratio > 0.7. **Résultat** : 0.11 → 0.27 ✅ (sync absolue faible)

## TEST-12 — Influence I + I_min (le contact compte ?)
- **Méthode** : I = terme d'interaction, injection loin vs pont ; I_min :
  bruits indépendants vs dilatation commune.
- **Critère** : I_pont > I_loin et Imin_commun > Imin_indep.
- **Résultat** : −0.004 → +0.0025 ; 0.26 → 0.99 ✅

## TEST-13 — Séparateur K (global/individuel mesurable ?)
- **Méthode** : K(L) = 1 − P_L/P_joint par couche.
- **Critère** : K ∈ [0,1]. **Résultat** : {0.33, 0.80, 0.67} ✅

## TEST-14 — Secteurs S_i (une loi par couche ?)
- **Méthode** : dynamiques différentes par couche, résidus 1 loi vs 3 lois.
- **Critère** : ratio < 0.5. **Résultat** : 0.001 ✅

## TEST-15 — Constantes (nombres du labo stables ?)
- **Méthode** : Π_c, Π_P, Π_H + 2e graine (écart réel mesuré).
- **Critère** : écart < 25 %. **Résultat** : stables ✅ (universalité ouverte)

## TEST-16 — Seuils par structure (Φ_c dépend de la forme ?)
- **Méthode** : boucle compacte vs nuage diffus, σ_c de survie sous bruit.
- **Critère** : σ_c différents. **Résultat** : 0.02 vs 0.20 ✅ (F4 : artefacts)

## TEST-17 — F0 (l'entretien tient sous bruit ?)
- **Méthode** : réinjection à chaque pas vs abandon, σ = 0.06, coût en bits.
- **Critère** : entretenu > 0.7 et > abandonné. **Résultat** : 0.79 vs 0.62 ✅

## TEST-18 — H2' (κ = f(D,I), bascule ?)
- **Méthode** : grille 3×3 distance × interaction, carte de R.
- **Critère** : cartographié. **Résultat** : R ∈ [0.97, 1.09], pas de bascule 🟡

## TEST-19 — Correspondance (injection → 0 = témoin ?)
- **Méthode** : niveaux 0/2/4, P final.
- **Critère** : niveau 0 ≈ 1.0 + monotone. **Résultat** : 1.0, monotone ✅

## TEST-20 — Unification v2 (tout en un univers ?)
- **Méthode** : fusion 08–19 + 01–07 → `univers/unifie_v2.json`.
- **Critère** : score 11/11. **Résultat** : 11/11 ✅ (H2' : ticket ouvert)

## TEST-21 (04b) — Lissage restreint (le fond survit ?)
- **Méthode** : univers A, masque (injecté seul), érosion = |P_fond/P_ref − 1|.
- **Critère** : érosion < 0.02. **Résultat** : 0.000 ✅ (F1 close)

## TEST-22 (05b) — Kuramoto fort (le réseau se synchronise ?)
- **Méthode** : K = 3.0 (×1.5), T = 24 (×2), point de bascule sync > 0.1.
- **Critère** : bascule ≤ 12 pas + stable + P tenu. **Résultat** : bascule 9,
  sync 0.51 ✅ (F2 close)

## TEST-23 — Anti-triche V3 (diagrammes complets + stats)
- **Méthode** : A durci, diagrammes H1/H2 complets, 3 graines (audit archivé).
- **Critère** : ratio moyen > 2.5. **Résultat** : 26.29 ± 1.33 ✅ (F3 close)

## TEST-24 (H2'-bis) — Grille resserrée (bascule ou réfutation ?)
- **Méthode** : D ∈ [1.8, 2.6] × I ∈ [4, 20], 3 tirages, règle formelle 2σ.
- **Critère** : détectée OU réfutée. **Résultat** : DÉTECTÉE (9 cellules) ✅ (F5 close)

## TEST-25 — PLV 1000 pas (la sync tient + survit ?)
- **Méthode** : contrôle positif (onde carrée commune), fenêtres de 50,
  collapse 30 %, M5→M6→M7 documentés.
- **Critère** : moyenne > 0.3, var < 0.05. **Résultat** : 0.866, var 0.0013,
  post 0.886 ✅

## TEST-26 — Unification V3 (base blindée ?)
- **Méthode** : fusion 21–25 → `univers/unifie_v3.json`.
- **Critère** : score 5/5. **Résultat** : 5/5 ✅

## TEST-27 — Loi de Proximité-Condensation (V4)
- **Méthode** : (A) gate doux, scan D ∈ [0.5, 5.0] → extraction ρ_c ;
  (B) interrupteur dur bilatéral → sync conditionnelle actifs/inactifs.
- **Critère** : contraste > 0.3 loin + actifs > 0.5 près + contrôles.
- **Résultat** : ρ_c = 8.01 ; à D=5 : actifs 0.98 vs inactifs 0.11 ✅

## TEST-28 — Indice de Résilience R (V4)
- **Méthode** : fond complet, 6 niveaux de bruit × 8 tirages, collapse neutre
  vs sélectif (30 %), R = C_post/C_pre.
- **Critère** : sélectif > neutre à fort bruit. **Résultat** : +3-4 pts ✅ ;
  R > 1 absolu : non au niveau P, oui au niveau sync (1.023, TEST-25).

## TEST-29 — Unification V4 (deux lois en un univers ?)
- **Méthode** : fusion 27–28 → `univers/unifie_v4.json`.
- **Critère** : score 2/2. **Résultat** : 2/2 ✅

---
*Exécution : `cd ratiss-focal-local && python3 experiences/expNN_*.py`
dans l'ordre, 01 → 29.* 🔒
