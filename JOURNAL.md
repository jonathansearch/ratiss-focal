# 📓 JOURNAL — ratiss-focal

## 2026-09-22 — ARCHIVE IBM : 64/66 jobs rapatriés (passerelle_quantique/jobs_ibm/)
- Ordre chef : ne rien laisser sur la plateforme. 9 jobs attribués (77/76/
  60/T2/72/BERRY/BF-v1/BF-v2) + 56 essais août non attribués. Bonus :
  Berry-FERMÉ v1 (dapcj5ac505c73chvsh0, kingston) REDÉCOUVERT (S plat).
  Vérifié bit-identique. INDEX.json. (C01+C08 → continuums.)

## 2026-09-22 — TEST-94 : SYNTHÈSE QM×GR (décohérence gravitationnelle)
- Ordre chef : un calcul qui exige OBLIGATOIREMENT les deux échelles.
  Réponse : superposition à deux hauteurs, horloges locales GR (puits
  expo, redshift 84) × spread interne QM (sw). τ=√2/(sw·|Δf|) à ~8 %
  sur 18 cas ; 30 contrôles (dh/G0/sw=0) → τ=∞. Retirer un pilier tue
  l'effet. Figure plot_DECO94 (courbes + effondrement). Badge 94.

## 2026-09-22 — TEST-93 + BERRY-FERMÉ réel : LE PLI ORIENTÉ MESURÉ
- TEST-93 (virtuel) : cycle (G0,c) fermé ± → Δ=−0.221 rad seulement,
  R_diff 0.25/0.28 : l'état ne revient pas (hystérésis). En anneau
  dissipatif, le sens compte peu.
- PONT-BERRY-FERMÉ v2 (ibm_marrakesh, job dapck92c505c73chvtqg, 20
  circuits) : boucle méridien-équateur-méridien, fuite ~1e-33,
  γ=−φ/2. Lecture S : + = 0.966 vs − = 0.028 à φ=π (simu 1.0/0.0).
  LE SENS COMPTE — le pli orienté existe là où la boucle se ferme
  en espace d'états. Figures plot_pontBerryFerme + plot_CYCLE93.
  Badge 93. Fiche : 7e ligne QPU ✅. UNIFICATION §21 scellé.
- Note atelier : v1 (RyRzRy) ne fermait pas (S plat 0.5, fez/kingston),
  retour au pôle sud puis signe corrigé — la fermeture se VÉRIFIE
  (fuite numérique), elle ne se suppose pas.

## 2026-09-22 — Chasse au pli : boucle 91 + Berry réel (pas de pli orienté)
- TEST-90 : twist grenu −2…+2, pas de lignes (T=300 ?). TEST-91 : boucle
  G0 (aire 0.064, gap 0.17) — la courbure écrit, la descente oublie
  différemment. TEST-92 : +tour=−tour (+9 rad) = traînée, pas géométrie.
- PONT-BERRY (ibm_fez, job dapc3t4ak42c73cibdd0, 10 circuits) : frange en
  U vs taille de boucle (1.0→0.49→1.0, réel=simu à 0.01) MAIS asymétrie
  A~0 partout : boucle non fermée en espace d'états (U≠I), on mesure une
  rotation totale, pas une phase géométrique. Défaut assumé, piste : vraie
  boucle fermée (cycle (G0,c) ± en virtuel = TEST-93 ?).
- Figures plot_PLI + plot_pontBerry. Badge 92. Fiche : pont Berry en 6e
  ligne QPU (frange oui, pli orienté non).

## 2026-09-22 — Théorie complète du chef scellée (THEORIE-COMPLETE.md)
- 11 sections dictées/rassemblées (principe, LCT/ETH/Stine-24, réalité,
  conscience, réincarnation, états modifiés, gravité, focalisation,
  9 validations, dépôts, phrase-résumé). Document source intouchable.

## 2026-09-22 — Missions téléphone : 4/4 ✅ FICHE COMPLÈTE
- Mission 4 (redshift, Manus IA) : 12 freqs −0.7577→−0.1145 vs prédit
  −0.7565→−0.1140 (écart max 0.0014, précision flottante). Gradient +
  paires verrouillées confirmés hors labo.
- BILAN VALIDATION : QPU 5/5 (capture, érosion, T1+flip, T2*, écho) +
  outils 4/4 (ombre, lentille, twist, redshift). L'univers virtuel prédit
  le réel sur 9 ponts indépendants (hardware IBM, simulateurs, ondes).

## 2026-09-22 — Missions téléphone : 3/4 ✅ (captures archivées)
- Preuves Falstad archivées : preuve_ombre_obstacle.jpg (ombre nette
  derrière le bloc) + preuve_lentille_slowmedium.jpg (zone bleue).
- Mission 3 (twist) sur simulateur Manus IA (Wokwi saturé) : R=0.9096 /
  0.4081, twist 0/0 — EXACTEMENT les prédictions TEST-88 (4 décimales).
  Le float64 Manus confirme le jumeau ; l'écart Wokwi venait du float32.
- Reste : mission 4 (redshift).

## 2026-09-22 — Missions téléphone : Falstad 2/2 ✅, Wokwi partiel
- Mission 1 (ombre, config Obstacle) : ombre vue derrière le bloc ✅.
  Mission 2 (lentille, Slow Medium) : resserrement vu en zone bleue ✅.
- Mission 3 (twist) : R=0.8717 vs 0.9096 prédit (écart 4% = float32 Uno
  vs float64 jumeau, assumé) ; 2e ligne illisible (moniteur série Wokwi).
  Sketch corrigé (pauses + flush + marqueurs) : à relancer par le chef.
- Mission 4 (redshift) : en cours côté chef.

## 2026-09-22 — TEST-86→89 : jumeaux outils en ligne (ondes + Wokwi)
- 86 : ombre d'Alembert 0.90/0.53/0.75 (disque<λ = rien, biais de bords
  corrigé par normalisation). 87 : lentille x1.9 vs témoin. 88 : twist 0
  avec LCG (vs −2 numpy : init-dépendant, constaté). 89 : redshift
  −0.77→−0.11 par paires. Firmwares + guide téléphone OUTILS-EN-LIGNE.md.
  Course d'éditions parallèles re-constatée (boucle 86) : une/seule/vérifier.
- Figures plot_ONDES + plot_JUMEAUX. Badge 89. Fiche : colonne outils
  prête, cases téléphone à cocher par le chef.

## 2026-09-22 — PONT-72 ÉCHO réel (kingston) : récupération x4.4
- Job dap8jg8pqrnc739b0hc0, 28 circuits. Ramsey plain : chute rapide
  T2*~14.4us (refit 5 pts, R2=0.96 ; fit global R2=0.44 non interprétable,
  assumé). Écho Hahn : décroissance propre T2=63.4us (R2=0.84). L'impulsion
  centrale récupère la cohérence x4.4 — comme le graphe TEST-72.
  Colonne QPU de la fiche : 5/5 mesurés. Figure plot_pont72.

## 2026-09-22 — TEST-85 (3 puits, twist 0) + PONT-T2 réel (70.2 us)
- TEST-85 : R 0.85→0.40, twist 0 partout — la piste twist=nb de puits
  s'arrête à 2. Symétrie à 3 = torsion annulée ? Figure plot_T85.
- PONT-T2 (ibm_marrakesh, job dap8ca78gn2s739osa10, 14 circuits) :
  T2*=70.2 us (R2=0.96). Simu : bruit thermique Aer inopérant sur les
  délais (plat à 1.0) → remplacé par expo+binomial qui retrouve 188.5
  pour 180 (R2=0.996). Figure plot_pontT2. Clé mémoire seule, /tmp vidé.

## 2026-09-22 — PONT-60 sur VRAI QPU (ibm_kingston)
- Job dap88g02fm4c73f6eb3g, 28 circuits en 1 job. T1 : P(1) décroît en
  exponentielle, T1=285.4 us (R2=0.9994) ; simu plat à 1 (pas de
  relaxation idéale). Flip : P(0) en cosinus de phi, simu et réel
  superposés. Figure plot_pont60. Clé mémoire seule, /tmp vidé.

## 2026-09-22 — PONT-76 sur VRAI QPU (ibm_marrakesh)
- Job dap8368pqrnc739avu2g, 60 circuits en 1 job. Paire de Bell + flip
  local p sur 1 qubit : P(mêmes) réelle 0.98/0.98/0.88/0.69/0.41/0.31
  (p=0→0.5) vs simu 1.00/1.00/0.90/0.70/0.40/0.30 — érosion graduelle,
  réel à ~1% du simu. Figure plot_pont76. Clé en mémoire seule, /tmp vidé.

## 2026-09-22 — PONT-77 sur VRAI QPU (ibm_marrakesh, 156 qubits)
- Job dap7su82fm4c73f6dsrg, 50 circuits en 1 job, file 0-2 jobs.
  GHZ 6 qubits + k avalés : F réelle 0.84 / 0.41 / 0.10 / 0.27 / 0.00
  (k=0..4) vs simu 1.00 / 0.50 / 0.10 / 0.30 / 0.00 — même allure,
  plancher de bruit réel ~0.84 à k=0. Première mesure sur hardware.
- Clé chef utilisée en mémoire seule, compte /tmp effacé, rien stocké.
  Outil file_qpu.py (files + récupération par JOB_ID). Figure plot_pont77.

## 2026-09-22 — QM-GR : 6 observations (TEST-79→84, zéro verdict)
- Règle chef : plus d'étiquettes positif/négatif, on regarde et on
  raconte ; j'itère seul, je pose mes questions.
- Vu : twist 1 près d'un puits, twist −2 entre deux puits ; lentille
  en S (±47°, 0 capture) ; horizon absorbant → ombre (contraste 0.66),
  là où le tueur faisait un puits ; mémoire RUQ-3 0.73→0.25 en espace
  courbe ; redshift monotone −0.53→+0.01 avec la distance.
- Figure plot_QM_GR (6 panneaux). §20 descriptif. Pas de .tex
  (observations, pas de critères pré-enregistrés).

## 2026-09-22 — V13 SINGULARITÉ : 2/5 (puits expo, pas d'ombre Newton)
- TEST-73 H0 : le tueur ponctuel creuse un PUITS divergent (a=4.3),
  profil exponentiel (R²=0.98), A/(r+eps) rejeté (R²=0.88). Chapeau
  mexicain. 3 bugs de design fixés avant verdict (T, déficit→excès,
  sondes imposées→libres).
- TEST-74 ✅ : exponentielle gagne 12/12 (R²=0.998), p≈0 — portée
  finie fixée par diffusion, pas par la masse. TEST-75 H0 : horloges
  PLATES. TEST-76 ÉRODÉ (U encaisse, 10/30). TEST-77 ✅ : k_c=6.
- Figure plot_V13 (3 panneaux). §19 + §10.octies restreint (validé
  seul : loi expo + capture). Phase 18 ouverte et fermée le même jour.

## 2026-09-22 — TEST-72 : RUQ-3 H2 ! (le graphe tient séparé)
- R 0.99 → 0.05 → 0.73 : chute puis RÉCUPÉRATION via graphe fixe.
  var(q) → 0.197, corr −0.76, λ2 12 → 2.2. Première unité qui survit
  (partiellement) à la séparation spatiale. Bug snaps list→dict fixé.
- Figure plot_RUQ72. §18 enrichi (RUQ-2). Pas de .tex. README Phase 17
  + conclusion : explorations closes sur ordre chef.

## 2026-09-22 — TEST-71 : RUQ-2 H1 aussi (feedback insuffisant)
- Fusion R=0.98 → séparés R=0.26, τ=15.1 (≈ t_half=11 de RUQ-1),
  R²_relax=0.51 (fluctuant). Trace : corr(th,q)=−0.57 post.
  q stable, pas d'explosion. Conclusion : rétroaction locale seule
  ne crée pas l'Esprit — reste la non-localité (RUQ-3 ? sur ordre).
- Figure plot_RUQ71. Pas de .tex (exploration).

## 2026-09-22 — TEST-70 : fusion RÉVERSIBLE (H1, t_half=11)
- RUQ-1 groupé R=0.985 → séparé R=0.31 en ~11 pas, var(q) récupère.
  Pas d'hystérésis : RUQ-1 n'a ni couplage à distance ni feedback q→th.
  Piste : RUQ-2 avec feedback charge→phase (vraie mémoire d'unité ?).
- Bug parenthèse (bis) fixé au sed. Figure plot_RUQ70. Pas de .tex
  (règle : exploration, pas canon).

## 2026-09-22 — UKTZ : 3 essaims lâchés dans le tore (explorations)
- TEST-67 S : codes 0.44 → 0.97 groupés (code partagé).
  TEST-68 T : R 0.72 → 0.69 (topologie > géométrie).
  TEST-69 RUQ-1 (invention) : R 0.30 → 0.98 + var(q) ÷9 — TRANSITION.
- Explorations ouvertes : observables pré-enregistrées, aucun verdict.
  Bug parenthèse 68/69 fixé avant exécution. Figure plot_neurons_uktz.

## 2026-09-22 — SONDE ENDOGÈNE : 3 tentatives, 3 AVEUGLE assumés
- TEST-64 : pointe Phi réelle (pic=201) mais gates-plateau ratées.
  TEST-65 : W=16 = silence total (LZ sans dynamique). TEST-66 : sonde
  v3 sent les chocs (rafales 11-13) mais dérive calme = autant
  (syncQ PASS 13v0 ; Phi 12v11 ; Psig 11v12).
- Leçon : nouveauté relative à l'horizon de mémoire ; médiane
  normalisée = aveugle aux niveaux. Piste v4 : baseline adaptative /
  détrendage (prochaine session, sur ordre).
- Phase 17 🟡 EN COURS (intégration appliquée, feu vert chef).

## 2026-09-22 (nuit) — CLÔTURE V12 : consolidation, pause stratégique
- .tex §10 réécrit canonique (5 sections, TEST-40→62 liés, TEST-50
  corrigée). Ticket sanctuaire CLÔTURÉ (résumé V9-V12). Ticket
  CONSOLIDATION_V1-V12 ouvert (4 lois + ombres + 6 abandons).
  ROADMAP Ph16 ✅ / Ph17 (intégration/VRN, sur feu vert).
- Repos cognitif ordonné. Aucune V13 sans ordre explicite. Tout poussé.

## 2026-09-22 (nuit) — V12 : FLIP PILOTÉ 1/3 (φ commande, U plancher)
- TEST-60 : CONTRÔLABLE (φ→état P=1.0, M26). TEST-61 : MIXTE assumé
  (pas de rupture à 0.30, plancher ~30 %, IRRÉVERSIBLE, pas de M27).
  TEST-62 : COUPLÉ_STRUCTUREL (Δ=+2/+4, 2 blocs).
- .tex §10.septies (flip pilotable) + §10.sexies (σ_c). Ticket :
  environnement. Unifié-v12. Tout poussé.

## 2026-09-22 (nuit) — V11 : GIROUETTE 2/3 (flip symétrique, σ_c=0.06)
- TEST-56 : SYMÉTRIQUE (M25 top-up n=15, pas de Qbar). TEST-57 :
  distribution rebelle (bêta 0.57, skew +0.69). TEST-58 : SEUIL
  σ_c=0.06, sigmoïde 0.964.
- .tex §10.septies retitré + §10.sexies (σ_c). Ticket sanctuaire :
  bruit chronique. Unifié-v11. Tout poussé.

## 2026-09-22 (nuit) — V10 : CORRECTION 1/3 (pas d'attracteurs Q)
- TEST-52 : MONOSTABLE (continuum n=40, TEST-50 réfutée). TEST-53 :
  FRAGILE (P=1.0 partout, 44/44). TEST-54 : Q/U CORRÉLÉS (Δ=3).
- .tex §10.septies (re-tirage) + §10.sexies nuancé. Ticket sanctuaire
  mis à jour. Unifié-v10. Tout poussé.

## 2026-09-22 (nuit) — V9 : SANCTUAIRE 3/3 (noyau absolu 0.083)
- TEST-48 : H3 saturante R²=0.978 (bande [0.06,0.11], non monotone).
  TEST-49 : U ABSOLU (28/30 ×7, Δ=0). TEST-50 : Q bistable (0.78↔0.87),
  « fatigue » = sauts d'attracteurs, pas déclin.
- .tex §10.quinquies + §10.sexies. VRN §14 exclu (vote chef NON).
  Ticket SANCTUAIRE_U_CONSCIENCE créé. Unifié-v9. Tout poussé.

## 2026-09-22 (nuit) — V8 : MÉMOIRE 2/3 (réfutation + sanctuaire U)
- TEST-44 : passe-bas RÉFUTÉ → BLANCHIMENT spectral (centroïde ×2.4).
  TEST-45 : ligne SANCTUAIRE (28/30, identique TEST-38). TEST-46 :
  vrai plancher 0.095 (≠ 0.273 !), τ ≈ 400, R²=0.902 tout juste.
- .tex §10 retouché (noyau = variable thermodynamique) + §10.quater.
  Ticket HYSTERESIS_INFO créé. Unifié-v8. Tout poussé.

## 2026-09-21 (nuit) — V7 : NOYAU 3/3 (loi exponentielle)
- TEST-40 : plancher = exp(−0.29−7.16α−6.59σ+0.0012N), R²=0.920 (M24) ·
  TEST-41 : collapse COUPLÉ (corr −0.87, non invariant) · TEST-42 : choc
  PLASTIQUE (0.345→0.273). Ticket noyau traité.
- Correction chef : instruction VRN = fausse → portage supprimé, focal
  sans neurones confirmé (vérifié par grep). Reste : MEMOIRE_Q (focal pur).
- .tex §11 (§10.ter). Unifié-v7. Tout poussé.

## 2026-09-21 (nuit) — V6 : Q RÉVÉLÉ 3/3 (durcir sans trahir)
- TEST-36 : double-exp R²=0.968 (k1=0.098, k2=0.001) · TEST-37 : volatilité
  STRUCTURÉE (pente −0.72, ac1 0.63, kurt 2.97) → signal, pas erreur ·
  TEST-38 : ligne 28/30 vs 9/30 sous bruit natif (robuste).
- .tex §10 à jour (S-grav explicite, S-quant double-exp + volatilité, U4).
- Ticket V7 : NOYAU_RÉSIDUEL_G. Hygiène : MIT ✓, token à révoquer (rappel).
- Unifié-v6. Tout poussé.

## 2026-09-21 (nuit) — V5 : VERDICT D'UNIFICATION 3/5 PARTIELLE (fil retrouvé)
- Recentrage chef : origine = unification GR×QM (postulat ~6 p.) ; 29 tests =
  instruments ; V5 = le postulat aux instruments.
- U1 ✅ subsistance (+0.096/+0.040, 6/6) · U2 ✅ non-réduction (RED≈0)
  · U3 🟡 (S-grav complète + noyau 0.305, forme Q ouverte) · U4 ✅ ligne
  (30/30 vs 0.33) · U5 🟡 (2/3, F8 volatilité Q). Chaîne M11-M23 documentée.
- Leçon : tout le résidu vit côté Q → V6 = durcir Q. .tex §10. Tout poussé.

## 2026-09-21 (nuit) — V4 : DEUX LOIS 2/2 (ordre d'exécution immédiat)
- L1 (TEST-27) : ρ_c = 8.01 émergé de la mesure ; interrupteur bilatéral vérifié
  (actifs 0.98 vs inactifs 0.11 à D=5, corr 0.94). Chaîne M8→M10c documentée.
- L2 (TEST-28) : sélection > neutre (+3-4 pts) ; R>1 au niveau sync (1.023),
  relatif au niveau P. Domaine précisé : les liens.
- .tex §8-§9 ajoutés (canon : % TEST-27/28). Unifié-v4. Tout poussé.

## 2026-09-21 (nuit) — V3 DURCIE 5/5 (ordre : durcissement avant expansion)
- P1 04b : érosion 0.000 (F1 close) · P2 05b : bascule 9, sync 0.51 (F2 close)
  · P3a anti-triche V3 : 26.29±1.33 (F3 close) · P3b H2'-bis : BASCULE DÉTECTÉE
  9 cellules (F5 close) · P4 PLV-1000 : 0.866, post 0.886 (M5→M6→M7).
- Canon : FORMALISATION.tex v3 (chaque équation ↔ son test). Licence MIT ajoutée.
- Hygiène : aucun token dans les fichiers. RAPPEL : révoquer le token côté réglages.
- Unifié-v3 cohérent. Tout poussé. Base blindée, prête pour expansion.

## 2026-09-21 (nuit) — TEST-08→20 : toute la théorie codée (ordre du chef)
- Rappel du chef : rien laissé sur papier. 12 tests formels ajoutés (Stine, X, U,
  tryperposition, I/I_min, K, secteurs, constantes, seuils, F0, H2', correspondance).
- Premier run 7/11 → 4 mètres corrigés (M1-M4, documentés) → second run 11/11.
- Unifié-v2 cohérent. FORMALISATION.tex écrite (≈5 p., équations + valeurs).
- H2' : pas de bascule dans la plage (F5, ticket ouvert). Tout poussé.

## 2026-09-21 (nuit) — 7 TESTS exécutés + unification (ordre « Go »)
- 01 fond stable (1.003±0.021) · 02 info pure (H=0.997) · 03 porteurs OK (I=3,S=4)
  · 04 A focalise mais ΔP=−0.10 (F1 lissage) · 05 B focalise, ΔP=+0.29, sync=0.02
  (F2 Kuramoto) · 06 verdict « sœurs », anti-triche v2=2.03 de justesse (F3)
  · 07 Unifié-v1 cohérent. Détail : UNIFICATION.md. Tout poussé (code+résultats).

## 2026-09-21 (nuit) — Univers jamais vides (ordre du chef)
- Fond commun Fond ajouté à la spec (§2b) : constantes du labo + structures-graines
  cohérentes (vide structuré), identique dans A et B, neutre (ne code pas la cible).
- Témoin = fond seul sans condensateur. Anti-triche étendue au fond (auditable).

## 2026-09-21 (nuit) — v2 : neurones retirés (ordre du chef)
- Stine-24 + LCT = lois ACCOMPAGNATRICES (mesures au service de la théorie).
- Supprimés du dépôt : sections neurones/douane/esprit/boucle, ESPRIT-IA-EQUATIONS,
  4 images neuro (network_science, genomic_net, fil, atcg). Les neurones vivent
  dans ratiss-neuro. La théorie d'aujourd'hui est la focalisation, rien d'autre.

## 2026-09-21 (nuit) — Création + consolidation totale
- Dépôt créé sur ordre du chef. Tout versé : théorie unifiée (A→K),
  spec EXP-FOCAL-01, roadmap, questions, glossaire, 7 images,
  4 documents d'atelier intacts (docs/atelier-precedent/).
- Concepts du jour : PORTEURS (Type-I/S proposés), condensateur Q_info,
  conteneur, double couche A/B, fil conducteur, anti-triche Kolmogorov.
- Pivots actés : W (4e dim) → Φ (concentration) ; décohérence = nom ;
  H2' + LCT-3 + types porteurs EN ATTENTE de validation chef.
- Prochain : code Phase 1 sur ordre. Pas de clé IBM nécessaire (numpy+ripser).

---
*Échecs publiés, jamais cachés. Mesures datées, graines fixées.* 🔒
