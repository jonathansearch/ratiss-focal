# 🧪 SPEC EXP-FOCAL-01 — Le conteneur, le condensateur, les porteurs, les jumeaux

*Protocole d'expérience complet. Zéro code ici — spec exécutable par OpenHands
ou Arena sur ordre du chef. Dépendances v0 : numpy + ripser. Pas de clé IBM.*

## 1. Objectif
Tester si la cohérence émerge de l'information pure : charger un conteneur
topologique, observer si une structure focalisée apparaît, comparer émergence (A)
vs implantation (B).

## 2. Le conteneur
Mini-univers topologique : nuage de points + filtration Vietoris-Rips
(cycles H1/H2 suivis). Cohérence minimale requise `Φ_conteneur ≥ Φ_c^lab`
(le labo doit tenir). Graines fixées (R7).

## 2b. Le fond : des univers JAMAIS vides ✅ (ordre du chef 21/09)
Chaque univers naît avec un fond commun identique (noté Fond) — neutre,
cohérent, qui ne code PAS la structure cible. Deux choses dedans :
1. **Les constantes du labo** : Φ_c^lab (seuil du conteneur), P_sig^ref
   (ligne de base du témoin), graines R7, pas de temps, portée VR.
2. **Des structures-graines cohérentes** : petit ensemble de cycles H1/H2
   stables + nuage de référence = un « vide structuré ».
Rôle : donner au fil conducteur quelque chose à suivre (les écarts au fond)
et à l'émergence quelque chose à continuer. Témoin = fond seul, sans
condensateur. Fond auditable (graines + paramètres scellés).

## 3. Le condensateur Q_info
Charge d'information pure (équations simples, règles locales — JAMAIS de
structure cible). Lecture : `P_sig(t)`, événements `Φ ≥ Φ_c`.

## 4. LES PORTEURS (nouveau — spec détaillée)
- **Nature** : cubes-qubits simulés (état + position + tranche métrique).
- **Types proposés (À VALIDER)** : **Type-I** (charge info pure → univers A),
  **Type-S** (charge structure/réseau → univers B).
- **Métriques porteuses disjointes** : chaque porteur porte une tranche disjointe
  (`m_i ∩ m_j = ∅`) — pas de double comptage, partition stricte de l'info.
- **Transport** : condensateur externe → regroupement vers le point focal donné
  dans l'univers virtuel → concentration jusqu'au seuil (Φ_c / oscillation P_sig)
  → une structure apparaît. Même machinerie dans A et B, cargaison différente.

## 5. Univers jumeaux (jamais vides : fond commun Fond + contenu propre)
- **A (émergence)** : fond + règles simples network-agnostiques + porteurs Type-I.
- **B (implantation)** : fond + équations DU réseau + porteurs Type-S.
- Même code conteneur, mêmes graines. Mesures identiques des deux côtés.

## 6. Fil de linéarité conductrice
Même pipeline métrique linéaire branché sur A et B (P_sig(t), Φ, focalisations).
Un seul mètre pour deux réalités superposées.

## 7. Anti-triche (scellé)
Complexité de Kolmogorov(règles de A) << complexité(structure observée).
Si A produit ce que ses règles ne peuvent encoder → émergence prouvée, pas implantée.

## 8. Verdicts (à sceller formellement avant exécution)
A+B sœurs → convergence · A seul → info suffit · B seul → structure requise ·
aucun → seuils/conteneur à revoir. Échecs publiés dans JOURNAL.

## 9. Roadmap d'implémentation
P1 conteneur v0 (nuage+VR+H1/H2) → P2 condensateur+porteurs (2 types) →
P3 univers A → P4 univers B + fil → P5 verdicts + rapport.
Critère de sortie P1 : P_sig(t) stable sur conteneur vide (témoin).

---
*RATISS Labs — EXP-FOCAL-01. R7 : 1 commande par phase, graines fixées.* 🔒
