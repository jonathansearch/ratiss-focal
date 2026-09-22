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

## TEST-30 — Subsistance C(X,Y) (V5)
- **Méthode** : G + Q isolés vs couplés, apparié, 2 régimes × 3 graines.
- **Critère M13** : 6/6 C fort > 0. **Résultat** : C_G=+0.096, C_Q=+0.040 ✅

## TEST-31 — Non-réduction (V5)
- **Méthode** : T=30 couplé, RED (l'autre seul) vs COH (propre + couplage).
- **Critère M14** : RED R²<0.1 + ratios<1. **Résultat** : RED≈0.00, ratios
  0.84/0.45 ✅ (décisif côté G)

## TEST-32 — Lois de secteurs (V5)
- **Méthode** : G T=16 (lin + noyau), Q T=60 (saturation), formes dictées
  par les données (M18→M23).
- **Critère** : lin>0.9 + noyau plat + forme Q>0.9 + saturation.
- **Résultat** : lin 0.989 ✅, noyau 0.305 plat ✅, saturation ✅,
  forme Q ouverte (expsat 0.83) 🟡

## TEST-33 — Ligne invisible (V5)
- **Méthode** : seuil sha256-uniforme, même géométrie relative, 30+30 essais.
- **Critère** : 30/30 ET indep<0.5. **Résultat** : 30/30 vs 0.333 ✅

## TEST-34 — Marqueurs (V5)
- **Méthode** : douceur post burn-in, causalité Q→G, même échelle.
- **Critère** : les trois. **Résultat** : causal 0.67 ✅, échelle ✅,
  douceur Q ✗ (F8 volatilité) 🟡

## TEST-35 — VERDICT D'UNIFICATION V5
- **Méthode** : fusion 30–34 → `univers/unifie_v5.json`.
- **Résultat** : 3/5 PARTIELLE (U1, U2, U4 ✅ ; U3, U5 🟡 côté Q).

## TEST-36 — Forme libre de S_quant (V6)
- **Méthode** : 4 candidats (stretched/Hill/double-exp/power), grille
  numpy, post-transitoire t≥10.
- **Critère** : meilleur R² > 0.9. **Résultat** : double-exp 0.968 ✅
  (a=0.41, k1=0.098, k2=0.001 — deux temps physiques)

## TEST-37 — Volatilité Q : signal ou bruit ? (V6)
- **Méthode** : anneau 24 + Kuramoto + bruit 0.04 + lissage 0.5, T=100 ;
  spectre, skew/kurt, bursts, autocorr.
- **Critère** : classe assignée par règles. **Résultat** : STRUCTURÉE ✅
  (pente −0.72, ac1 0.63, kurt 2.97, 0 bursts — mémoire, pas blanc)

## TEST-38 — Ligne sous bruit Q natif (V6)
- **Méthode** : M22 + jitter 0.04 indépendant par région, 30+30 essais.
- **Critère** : partage≥20 ET séparation≥10.
- **Résultat** : 28/30 vs 9/30, séparation 19 ✅ (capsule robuste)

## TEST-39 — Unification V6 (Q révélé ?)
- **Méthode** : fusion 36–38 → `univers/unifie_v6.json`.
- **Résultat** : 3/3 ✅ + ticket NOYAU_RÉSIDUEL_G (V7).

## TEST-40 — Loi du noyau G (V7)
- **Méthode** : scan α×σ×N (3×3×3=27), T=14, plancher = moy. 4 derniers.
- **Critère** : forme simple R² > 0.9. **Résultat** : logF 0.920 ✅
  (exp(−0.29−7.16α−6.59σ+0.0012N) — M24)

## TEST-41 — Collapse ↔ noyau (V7)
- **Méthode** : 1 pré + branches {0.1..0.5}×3 masques, 6 pas post.
- **Critère** : classe nette. **Résultat** : COUPLÉ ✅ (corr −0.87,
  non invariant : −0.10 → −0.21)

## TEST-42 — Choc extrême (V7)
- **Méthode** : 14 baseline + 3 choc (α=−0.15, σ×10) + 10 relâche.
- **Critère** : survit. **Résultat** : PLASTIQUE ✅ (0.345→0.273 stable)

## TEST-43 — Unification V7 (noyau révélé ?)
- **Méthode** : fusion 40–42 → `univers/unifie_v7.json`.
- **Résultat** : 3/3 ✅

---
## TEST-44 — Spectre Q post-choc (V8)
- **Méthode** : Q TEST-37, 300 baseline + 3 choc (K=0, σ×10) + 300 relâche.
  Spectres pré/post (250 pts, burn-in 50).
- **Critère** : filtre passe-bas (basses ≥, hautes ≤50 %, centroïde ↓).
- **Résultat** : RÉFUTÉ ❌ — BLANCHIMENT : basses 0.85→0.61, hautes
  0.08→0.18, centroïde 0.06→0.15, ac1 0.78→0.43. Niveau −2 % (vs G −21 %).

## TEST-45 — Ligne invisible sous choc (V8)
- **Méthode** : TEST-38 + fenêtre choc pas 11-13 (transport −0.12, jitter
  ×10), T=33. 30 partagé + 30 indépendant.
- **Critère** : SANCTUAIRE (barre TEST-38). **Résultat** : 28/30 vs 9/30,
  sép 19 — IDENTIQUE à TEST-38 ✅ U indépendant de G.

## TEST-46 — Reconstruction 1000 pas (V8)
- **Méthode** : G (14+3+1000) et Q (60+3+1000). Ajustements single/double-exp.
- **Critère** : double-exp gagne R²>0.9 sur G.
- **Résultat** : double-exp R²=0.902 ✅ (tout juste) — plancher VRAI 0.095
  (≠ 0.273 à 10 pas !), τ_lent ≈ 400 pas, oscillations détectées (pic 77).
  Q : niveau récupéré (0.789→0.796), série plate.

## TEST-47 — Unification V8 (mémoire Q ?)
- **Méthode** : fusion 44–46 → `univers/unifie_v8.json`.
- **Résultat** : 2/3 (M1 ❌ réfutation franche, M2 ✅, M3 ✅)

---
## TEST-48 — Escalier G, 6 chocs (V9)
- **Méthode** : tore TEST-42, 14 baseline + 6×(3 choc + 1000 relâche).
  Gmin(k) = moy. 50 derniers (k=0..6). H1/H2/H3 en grille.
- **Critère** : f(N) avec R²>0.95.
- **Résultat** : H3 SATURANTE R²=0.978 ✅ — noyau absolu 0.083.
  0.345→0.097→0.073→0.088→0.110→0.064→0.073 (bande [0.06,0.11],
  non monotone ; λ=3.0 en borne = chute instantanée).

## TEST-49 — Sanctuaire U cumulé (V9)
- **Méthode** : TEST-45 à k=0..6 fenêtres de choc (T=10+23k), 30+30/niveau.
- **Critère** : ΔS_U=0 (absolu) ou N_c identifié.
- **Résultat** : 28/30 aux 7 niveaux, Δ=0 ✅ SANCTUAIRE_ABSOLU, N_c=néant.

## TEST-50 — Fatigue Q cumulée (V8→V9)
- **Méthode** : Q TEST-37, 60 + 6×(3 choc + 300 relâche). Ajustement par
  segment → τ_lent(k), Q_final(k). Règle FATIGUE/INFATIGABLE/MIXTE.
- **Critère** : classe nette. **Résultat** : FATIGUE ✅ (dérive 13 %,
  N_bascule=2) — MAIS par bistabilité (0.78↔0.87), pas déclin ;
  Q_final(6)=0.868 ≈ Q_final(1). Fits médiocres (R² 0.15–0.71).

## TEST-51 — Unification V9 (sanctuaire éternel ?)
- **Méthode** : fusion 48–50 → `univers/unifie_v9.json`.
- **Résultat** : 3/3 ✅

---
## TEST-52 — Phase initiale vs attracteur (V10)
- **Méthode** : 40 runs Q (60+3 choc+300), phases init uniformes (seed
  5200+j). Prédicteurs <φ₀>, R₀. Bimodal si trou>0.04 (≥8/côté).
- **Critère** : DÉTERMINISTE (seuil, exactitude ≥85 %).
- **Résultat** : MONOSTABLE ❌ — continuum [0.76,0.91], trou max 0.018.
  La « bistabilité » TEST-50 (n=6) ne réplique pas (n=40).

## TEST-53 — Profondeur du bassin Q (V10)
- **Méthode** : départ HIGH (≥0.84) + sonde I∈{0.25,0.5,1,2,4} + 300
  relâche. P_switch(I), I_50. Barrière : ≥3 niveaux à ≥8 valides.
- **Critère** : ROBUSTE ou FRAGILE. **Résultat** : FRAGILE ✅ —
  P=1.0 PARTOUT (44/44 HIGH→LOW), I_50=0.25 (sous plancher).

## TEST-54 — Attracteur Q ↔ ligne U (V10)
- **Méthode** : σ fluctuations mesurée par état Q (12 runs) → ligne
  TEST-38 avec jitter=σ_mesuré (30+30/cas). Barrière : écart σ ≥10 %.
- **Critère** : INDÉPENDANT (Δ=0).
- **Résultat** : CORRÉLÉ Δ=3 ❌ — σ 0.054→26/30, σ 0.031→29/30.
  U robuste mais faiblement couplé à la volatilité Q.

## TEST-55 — Unification V10 (porte ou mur ?)
- **Méthode** : fusion 52–54 → `univers/unifie_v10.json`.
- **Résultat** : 1/3 (B1 ❌, B2 ✅ fragile, B3 ❌ corrélé)

---
*Exécution : `cd ratiss-focal-local && python3 experiences/expNN_*.py`
dans l'ordre, 01 → 55.* 🔒
