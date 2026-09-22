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
## TEST-56 — Symétrie LOW→HIGH (V11)
- **Méthode** : 2 bras (HIGH/LOW, 15 valides, sonde standard + 300
  relâche). M25 : cap 40→80 tentatives (HIGH n=13/40 au 1er run).
- **Critère** : classe nette. **Résultat** : SYMÉTRIQUE ✅ —
  med_H=0.77 (LOW), med_L=0.84 (HIGH). Flip contrariant, pas dérive ;
  pas de Qbar (CONVERGENT réfuté).

## TEST-57 — Distribution du re-tirage n=200 (V11)
- **Méthode** : 200 runs (60+3+300), histogramme 12 classes, ajustements
  gaussienne/bêta.
- **Critère** : R²>0.95. **Résultat** : bêta R²=0.57 ❌ —
  moy 0.816, std 0.045, skew +0.69. Ni harmonique, ni barrières simples.

## TEST-58 — Courbe S_U(σ) (V11)
- **Méthode** : ligne TEST-38, σ∈[0.01,0.10] pas 0.005 (19 pts), 30+30/pt.
  σ_c = 1er σ avec partage ≤ plateau−4. Formes lin/exp/sigmoïde.
- **Critère** : SEUIL (σ_c + forme R²>0.9) ou ROBUSTE.
- **Résultat** : SEUIL ✅ — σ_c=0.06, sigmoïde R²=0.964.
  Plateau 29 (σ≤0.03) → 21 (σ=0.10). Contrôle indep stable (9/30).

## TEST-59 — Unification V11 (nord magnétique ?)
- **Méthode** : fusion 56–58 → `univers/unifie_v11.json`.
- **Résultat** : 2/3 (A1 ✅ symétrique, A2 ❌ distribution, A3 ✅ seuil)

---
## TEST-60 — Forçage du flip (V12)
- **Méthode** : settle60+choc → Qf0 (pré HIGH/LOW) → injection
  th=φ_inj+N(0,0.05) → relâche 300 → Qf. φ∈{kπ/4}×2 bras, 8 visés/cell.
  M26 : cap 25→60 tentatives + fix NameError (1er run : 13/16).
- **Critère** : CONTRÔLABLE (un φ à P≥0.9 dans les 2 bras).
- **Résultat** : CONTRÔLABLE ✅ (14/16) — φ∈[0,π]→LOW (P=1.0),
  φ∈{5π/4,3π/2}→HIGH (P=1.0), 7π/4 = transition (50 % ambigu).

## TEST-61 — Rupture U, σ∈[0.10,0.30] (V12)
- **Méthode** : ligne TEST-38, 11 pts pas 0.02, 50+50/pt. σ_rupture =
  partage ≤ indep+3. Réversibilité (secondaire) : 20 pas σ=0.20 puis
  20 pas σ=0.02 (T=40, 30+30).
- **Critère** : MORT ou ASYMPTOTIQUE.
- **Résultat** : MIXTE ❌ — pas de rupture (courbe 34→~15/50, plancher
  apparent ~30 % vs contrôle ~16 %, 5 pts plats) ; barrière
  ASYMPTOTIQUE ratée sur technicité (imax GLOBAL 15 au lieu du contrôle
  local ~8 — PAS de M27 : on ne réécrit pas un critère pour le passer).
  Réversibilité : IRRÉVERSIBLE (12/30 ≈ pur-haut 13, ≠ pur-bas 29).

## TEST-62 — Structure Q → robustesse U (V12)
- **Méthode** : séries Q HIGH/LOW (5+5, détrendées, renormalisées à
  σ=0.04 IDENTIQUE) injectées comme bruit corrélé dans ligne T=20.
  2 blocs × 30+30 par état. (Design non circulaire : structure, pas
  niveau — cf. docstring.)
- **Critère** : DÉCOUPLÉ (comptes identiques).
- **Résultat** : COUPLÉ_STRUCTUREL ❌ — blocA 25v23 (Δ=2), blocB 26v22
  (Δ=4), même signe. La structure HIGH protège légèrement mieux U.

## TEST-63 — Unification V12 (dompter le flip ?)
- **Méthode** : fusion 60–62 → `univers/unifie_v12.json`.
- **Résultat** : 1/3 (D1 ✅ contrôlable, D2 ❌ mixte, D3 ❌ couplé)

## TEST-64 — Sonde endogène v1 (piste Phase 17)
- **Méthode** : agent LZ (W=64, binarisation vs médiane causale, seuil
  propre μ+2σ base 50-150). 6 runs : syncQ/Φ/Psig × {calme, choc 200}.
- **Critère** : VALIDE si ≥2/3 (taux_post≥10 % + ratio≥5, calme ≤5 %).
- **Résultat** : AVEUGLE ❌ — pointe Phi réelle (pic=201, 4 flags) mais
  gates voulaient un plateau ; Psig calme 5.08 % (>5 % d'un cheveu).

## TEST-65 — Sonde v2 (W=16, graines fraîches)
- **Méthode** : idem, fenêtre courte + LZ brut + critère comparatif
  (rafale_choc ≥4 et ≥2× pire rafale calme).
- **Critère** : VALIDE si ≥2/3. **Résultat** : AVEUGLE ❌ —
  silence total (0 flags au choc) : LZ-16 sans dynamique (μ≈7,
  seuil≈7.6). Leçon : tension fenêtre/dynamique.

## TEST-66 — Sonde v3 deux-canaux (graines fraîches)
- **Méthode** : texture LZ-64 + volatilité |x−médiane| (seuils propres),
  flag = OU. Flaw principiel corrigé : la binarisation effaçait les
  sauts de niveau. Même critère comparatif.
- **Critère** : VALIDE si ≥2/3. **Résultat** : AVEUGLE ❌ —
  syncQ PASS (13 vs 0) ; Phi FAIL (12 vs 11) ; Psig FAIL (11 vs 12).
  La sonde SENT (rafales 11-13 au choc) mais la dérive calme rafale
  autant : horizon de mémoire (100 pas) trop court pour distinguer
  choc exogène de dérive endogène. ARRÊT des itérations (3/3).

---
## TEST-67 — UKTZ-S sémantiques (exploration ouverte)
- **Méthode** : 12 neurones (embedding R^8 + drive Lissajous forcé),
  monde tore graine 24. 300 balade + 300 groupés (boule commune).
- **Observables** (aucun critère) : similarité cosinus S(t).
- **Observé** : S 0.44 → 0.97. La proximité crée un code quasi-identique.

## TEST-68 — UKTZ-T topologiques (exploration ouverte)
- **Méthode** : 12 neurones, graphe FIXE (anneau + 2 hubs), Kuramoto +
  modulation par champ local. 300 + 300.
- **Observables** (aucun critère) : ordre R(t).
- **Observé** : R 0.72 → 0.69 (bump 0.89 à 450). La topologie fixe
  domine ; le partage sensoriel ne change presque rien.

## TEST-69 — RUQ-1 Réseau Universel Q (invention, exploration ouverte)
- **Méthode** : 12 neurones phase+charge ; Kuramoto SPATIAL + charge
  qui boit le champ et diffuse par proximité. 300 + 300.
- **Observables** (aucun critère) : R(t), var(q)(t), corr(q,s)(t).
- **Observé** : R 0.30 → 0.98, var(q) ÷9 (0.047→0.005). Le regroupement
  déclenche une transition : sync explosive + homogénéisation de charge.

---
## TEST-70 — Réversibilité RUQ-1 (H1/H2/H3 pré-enregistrées)
- **Méthode** : RUQ-1 (graine 7001), 400 pas groupés (barrière R≥0.85)
  → séparation brusque (positions dispersées, th/q intacts) → 300 pas.
- **Critère** : convergence A + classe nette (H1 ≤0.45 / H2 / H3 ≥0.85).
- **Résultat** : H1_RÉVERSIBLE ✅ — R 0.985 → 0.31 (≈ 0.30 TEST-69),
  t_half = 11 pas, var(q) récupère (0.048). L'unité s'efface comme un
  rêve : pas de cicatrice (attendu : aucun couplage à distance ni
  feedback q→th dans RUQ-1).

---
## TEST-71 — RUQ-2 feedback charge↔phase (exploration ouverte)
- **Méthode** : RUQ-1 + dth += 0.5·(q−q̄)·DT et dq += 0.05·sin(th−Ψ)
  (version circulaire-safe de la spec). 400 groupés (barrière R≥0.85)
  → séparation brusque → 300 pas. Graine 7101.
- **Observables** (zéro critère) : R(t), var(q)(t), corr(th,q) post,
  τ_relax (fit exp), q min/max.
- **Observé** : H1_RÉVERSIBLE (descriptif) — R 0.98 → 0.26, τ = 15.1
  (R²=0.51, relaxation fluctuante, pas proprement exponentielle),
  corr(th,q) = −0.57, q stable ([−0.12, 0.88], pas d'explosion).
  Le feedback local ne suffit pas : l'unité meurt à la séparation.

---
## TEST-72 — RUQ-3 graphe fixe (exploration ouverte)
- **Méthode** : RUQ-2 + Kuramoto sur graphe FIXE UKTZ-T (KFIX=2.0,
  indépendant de la distance). 400 groupés (barrière R≥0.85) →
  séparation brusque (graphe conservé) → 300 pas. Graine 7201.
- **Observables** (zéro critère) : R(t), var(q)(t), corr(th,q)(t),
  λ2 + entropie config (snapshots fin-A/début-B/fin-B).
- **Observé** : H2_HYSTÉRÉSIS (descriptif) — R 0.99 → chute 0.05 →
  RÉCUPÈRE 0.73 ; var(q) 0.012 → 0.197 ; corr −0.76 ; λ2 12 → 2.2.
  Le graphe fixe resynchronise l'essaim dispersé : cohérence fantôme
  puis reconstruction. Première mémoire collective qui tient SÉPARÉE.

---
---
## TEST-73 — Naissance d'une singularité (V13, feu vert chef)
- **Méthode** : grille 40×40, diffusion D=0.05, tueur focal gaussien
  (MU=0.02D, σ=0.05D imposés), source rayures entretenue (lignes 32-39),
  T=600. Observable : excès radial e(r)=a(r)−a_loin, ajusté en A/(r+eps).
- **Critère** : R²>0.9 ET R_h∈]0,maxD[. **NON REMPLI** (H0 honnête) :
  le tueur creuse un PUITS (a_centre=4.3, divergence négative), pas une
  ombre ; A/(r+eps) donne R²=0.88 ; l'exponentielle C·exp(−r/l) donne
  R²=0.98 (l=0.066). Chapeau mexicain (anneau de dépression). Leçons :
  T=250 insuffisant (q_max=0.22<0.30, tueur muet) ; sondes imposées
  interdites (v1 biaisée, remplacée en TEST-75 v2).

## TEST-74 — Loi de gravité focale (V13)
- **Méthode** : balayage 4 MU × 3 σ (12 runs, T=400), 4 candidats
  (A: A/(r+eps), B: 1/r², C: exp, D: constante) sur le profil radial.
- **Critère** : même gagnant ≥9/12 ET R² moyen >0.9. **REMPLI** :
  C (exponentielle) gagne 12/12, R²=0.998. Loi R_h=k·MU^p : p≈0 —
  la taille du puits est fixée par la diffusion, PAS par la masse.
  La gravité focale est à portée finie (écrantée), pas newtonienne.

## TEST-75 — Horloges près de la singularité (V13)
- **Méthode** : 24 sondes LIBRES (règle focale pure), frappées 1 fois
  à t=100, τ(r) par ajustement exp du retour (T=600). Classes DILATÉE
  (τ_in>1.2·τ_out) / INVERSÉE / PLATE.
- **Critère** : DILATÉE. **NON REMPLI** : PLATE (τ_in=29.2,
  τ_out=31.4, 12/24 valides — les 12 sondes centrales noyées dans la
  croissance du puits, pas de relaxation mesurable). Pas de dilatation
  temporelle détectée avec cet opérateur d'horloge.

## TEST-76 — U vs trou noir local (V13)
- **Méthode** : ligne TEST-38 (T=20, mêmes graines/messages), région B
  trouée (spaghettification N(0,1) dans r<1.0). 30 partagé + 30 indép.
  Classes TIENT (barre TEST-38) / ÉRODÉ / ROMPU.
- **Critère** : TIENT. **NON REMPLI** : ÉRODÉ (10/30 vs 4/30, sép=6
  ; réf TEST-38 : 28/30 vs 9/30). U survit partiellement : le sanctuaire
  encaisse mais perd plus de la moitié de sa fidélité partagée.

## TEST-77 — Q vs capture (V13)
- **Méthode** : anneau NQ=24 + hubs (K=3, DT=0.3), k oscillateurs
  proches de l'angle 0 re-tirés uniformes à chaque pas. R sur 20
  derniers pas. k∈{0,2,4,6,8,10}.
- **Critère** : k_c identifié (1er k avec R<0.5). **REMPLI** :
  k_c=6 (R : 0.83→0.57→0.69→0.34→0.38→0.26). La capture d'un quart
  de l'anneau tue la synchronisation globale.

## TEST-78 — Unification V13 (TEST-73→77)
- **Méthode** : fusion des 5 critères → univers/unifie_v13.json.
- **Observé** : score 2/5 (S2 loi expo, S5 capture Q). Verdict :
  singularité = puits exponentiel écranté + capture Q à k_c=6 ;
  Newton, dilatation des horloges et sanctuaire U NON établis.

---
*Exécution : `cd ratiss-focal-local && python3 experiences/expNN_*.py`
dans l'ordre, 01 → 78.* 🔒
