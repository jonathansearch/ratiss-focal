# 🌉 PASSERELLE-RÉEL — tester l'univers focal pour 0 FCFA

> Le chef n'a ni labo ni budget. Ce doc liste les outils EN LIGNE gratuits
> (vérifiés sept. 2026) pour confronter nos prédictions au réel, du plus
> facile au plus fort. Zéro carte bancaire partout ci-dessous.

## 1. Ce soir, sans compte : le bac à ondes (TEST-73/82)
- **Falstad Ripple Tank** : `https://www.falstad.com/ripple/` (gratuit,
  navigateur, rien à installer).
- Protocole ombre (5 min) : menu *Setup* → obstacle circulaire absorbant
  au centre, source d'ondes en bas → observer l'ombre derrière le disque
  (TEST-82 dit : contraste ~0.66). Puis remplacer le disque par une
  source ponctuelle secondaire (mur non absorbant) → pas d'ombre franche
  (TEST-73 dit : un point actif fait un puits, pas une ombre).
- Noter : profondeur de l'ombre vs taille du disque (saturation ?).

## 2. Cette semaine : VRAIS qubits gratuits (PONT-77)
- **IBM Quantum, plan Open** : `https://quantum.ibm.com` — compte gratuit
  (identifiant IBM, sans carte), vrais processeurs jusqu'à 127 qubits,
  10 min/mois de temps quantique (= des milliers de petits runs),
  simulateurs illimités.
- **Quantum Inspire (QuTech, Pays-Bas)** : plateforme cloud, processeur
  Tuna-17 (17 qubits supraconducteurs) gratuit et ouvert aux chercheurs,
  étudiants et enseignants du monde entier, compatible Qiskit.
- Protocole prêt : `passerelle_quantique/pont77_capture_reelle.py`
  (GHZ 6 qubits + capture de k qubits, fidélité vs k).
  Validé sur simulateur : F = 1.00 / 0.50 / 0.10 / 0.30 / 0.00
  pour k = 0..4 (fluctuation à 10 tirages, tendance nette).
  Marche à suivre : créer le compte → copier le token → lancer
  `python3 pont77_capture_reelle.py --reel TOKEN` → comparer la courbe
  réelle à la courbe simulateur.
- **Mesure du 2026-09-22** (job dap7su82fm4c73f6dsrg, ibm_marrakesh) :
  F réelle = 0.84 / 0.41 / 0.10 / 0.27 / 0.00 (k=0..4), même allure que
  simu (1.00 / 0.50 / 0.10 / 0.30 / 0.00), bruit réel ~0.84 à k=0.
  Figure : `passerelle_quantique/plot_pont77.png`. Outil files :
  `file_qpu.py TOKEN [JOB_ID]` (choisir le QPU le moins saturé avant
  d'envoyer — conseil du chef).
- **PONT-76** (`pont76_sanctuaire_reel.py`, pont avec TEST-76) : paire de
  Bell + flip local p sur 1 qubit. Mesure du 2026-09-22 (job
  dap8368pqrnc739avu2g, ibm_marrakesh) : P(mêmes) = 0.98 / 0.98 / 0.88 /
  0.69 / 0.41 / 0.31 (p=0→0.5), réel à ~1% du simu. Érosion graduelle.
  Figure : `passerelle_quantique/plot_pont76.png`.
- **PONT-60** (`pont60_relaxation_flip.py`, ponts RUQ + TEST-60) : T1 et
  flip piloté. Mesure du 2026-09-22 (job dap88g02fm4c73f6eb3g,
  ibm_kingston) : T1=285.4 us (R2=0.9994, simu plat) ; flip en cosinus
  simu=réel. Figure : `passerelle_quantique/plot_pont60.png`.
- **PONT-T2** (`pontT2_decoherence.py`, pont RUQ) : Ramsey H-délai-H.
  Mesure du 2026-09-22 (job dap8ca78gn2s739osa10, ibm_marrakesh) :
  T2*=70.2 us (R2=0.96). Simu expo+binomial retrouve 188.5 pour 180.
  Figure : `passerelle_quantique/plot_pontT2.png`.
- **D-Wave Leap** : niveau gratuit développeur historiquement (1 min QPU
  + 20 min solveur hybride/mois, code public sur GitHub) + programme
  LaunchPad (essai 3 mois). À vérifier à l'inscription (offre 2023).

## 3. Hardware simulé gratuit (avant le réel)
- **Wokwi** (`https://wokwi.com`, compte gratuit) : Arduino/ESP32 simulés
  dans le navigateur — futur anneau d'oscillateurs (twist TEST-79/80).
- **Tinkercad Circuits** (compte Autodesk gratuit) : électronique + Arduino.
- **PhET** (`https://phet.colorado.edu`, sans compte) : simus physiques
  pédagogiques (ondes, interférences).

## 4. Calcul gratuit (gros runs virtuels)
- **Google Colab** (`https://colab.research.google.com`, compte Google) :
  CPU/GPU gratuits — pour rejouer nos 84 tests + balayages lourds.
- **Kaggle Notebooks** (compte gratuit) : GPU hebdomadaires gratuits.

## 5. Vitrine gratuite (montrer au monde)
- **Hugging Face Spaces** (compte gratuit) : héberger une démo interactive
  de l'univers focal (curseurs MU/sigma → puits en direct).
- **Zenodo** (compte gratuit) : archive DOI permanente du dépôt.
- **YouTube** : publier les runs filmés (métronomes, ripple tank, courbes).

## 6. Bonus : le téléphone-labo
- **phyphox** (appli gratuite, Android/iPhone) : utilise les capteurs du
  téléphone (micro, accéléromètre) comme instruments — mesurer de vraies
  fréquences/pendules à 0 FCFA.

## Écarté (honnêteté)
- **LabsLand** (vrais labos distants : Arduino, FPGA, électronique) : réel
  et pilotable par navigateur, MAIS accès par licences payantes. Pas
  retenu tant que le budget = 0. À reconsidérer si partenariat université.

---
*Ordre conseillé : 1 (ce soir) → 2 (cette semaine) → 4 (calcul) → 5 (vitrine).
Chaque confrontation réelle = entrée JOURNAL + commit.* 🔒
