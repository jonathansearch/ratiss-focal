# 📱 Outils en ligne — protocoles téléphone (0 FCFA, 0 compte)

> Jumeaux validés localement (TEST-86→89). Ici : ce que le chef fait sur
> son téléphone, clic par clic, et les valeurs attendues.

## A. Falstad Ripple Tank — ombre (jumeau TEST-86)
1. Ouvrir `https://www.falstad.com/ripple/` (navigateur téléphone).
2. Menu **Setup** (en haut à droite) → **Plane Wave** (onde plane).
3. **Appui long** sur l'écran → menu contextuel → ajouter un **cercle /
   obstacle** au centre (le redimensionner en tirant les bords).
4. Regarder derrière l'obstacle : zone calme = **ombre** (TEST-86 :
   contraste 0.90/0.53/0.75 selon taille).
5. Refaire avec un tout petit obstacle : l'ombre se remplit (diffraction
   gagne quand le disque < longueur d'onde — constaté localement).
6. Bonus : cocher **3-D View** pour voir le relief de l'ombre.

## B. Falstad Ripple Tank — lentille (jumeau TEST-87)
1. Même page. Menu **Setup** → **Slow Medium** (zone bleue = ondes lentes).
2. Si le menu contextuel (appui long) propose une **zone de milieu en
   cercle**, la placer face à l'onde plane.
3. Regarder derrière la zone : resserrement brillant = **foyer**
   (TEST-87 : concentration x1.9 vs témoin).
4. Comparer avec Setup → **Plane Wave** seule (témoin uniforme).

## C. Wokwi — twist (jumeau TEST-88)
1. Ouvrir `https://wokwi.com` → nouveau projet **Arduino Uno**.
2. Remplacer `sketch.ino` par `outils_en_ligne/wokwi_twist/sketch.ino`
   (copier depuis le dépôt GitHub, bouton copier).
3. Icône diagramme → remplacer par `diagram.json` du même dossier.
4. ▶ Run → ouvrir le **moniteur série** (115200 bauds).
5. Attendu (TEST-88) : `G0=0 R=0.9096 twist=0` puis
   `G0=1 R=0.4081 twist=0`. Écart = me le signaler (bug de jumeau).

## D. Wokwi — redshift (jumeau TEST-89)
1. Même manip avec `outils_en_ligne/wokwi_redshift/`.
2. Attendu : 12 fréquences de −0.76 (osc0) à −0.11 (osc11),
   par paires (voir `resultats/exp89.json`).

---
*Chaque case cochée sur téléphone = entrée JOURNAL + commit.* 🔒
