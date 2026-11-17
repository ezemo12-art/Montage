# L'ARCHIVISTE — Bible du personnage

> Personnage **permanent**, narrateur officiel de tous les épisodes de DOSSIER 00.
> Ne jamais créer un nouveau personnage. Ne jamais remplacer une référence officielle sans
> validation écrite de l'utilisateur.

## 1. Caractéristiques permanentes

### Selon la charte (texte)
- Masque en **porcelaine ivoire**.
- **Fine fissure près de la tempe gauche** (gauche du personnage).
- **Un seul œil lumineux ambre** (`#D6A64A`).
- Long **manteau noir**.
- **Gants noirs**.
- Silhouette élégante et mystérieuse.
- Gestuelle **lente et maîtrisée**.

### Visible sur la référence officielle `Character_FullBody_v1.jpg`
- Masque à **long bec** (type médecin de peste), blanc/ivoire, coutures sur le bec.
- **Chapeau fedora** noir.
- **Cravate rouge** sur chemise et gilet noirs.
- Long manteau noir croisé à grands revers, jusqu'aux chevilles.
- Gants noirs, **mains jointes sur le pommeau d'une canne dorée/ambre**.
- Pose frontale, debout, immobile, très droite. Silhouette fine et allongée.
- Fond : dégradé bleu nuit, éclairage doux par le haut.

### ⚠️ Écarts à valider (avant toute génération)

| Point | Charte | Image officielle v1 | Décision |
| --- | --- | --- | --- |
| Fissure tempe gauche | Oui | Non visible | _à décider_ |
| Œil | Un seul œil ambre lumineux | Deux yeux sombres rougeâtres | _à décider_ |
| Rouge de la cravate | Rouge sombre `#9E2929` | Rouge vif | _à décider_ |
| Fond | Noir charbon `#101113` | Bleu nuit | _à décider_ |

Tant que ces points ne sont pas tranchés, **l'image v1 fait foi** et aucune nouvelle référence
n'est générée. Option recommandée : créer une **v2** fidèle à la v1 (même silhouette, bec,
chapeau, canne) en ajoutant la fissure et l'œil ambre unique, puis la valider.

## 2. Accessoires fixes
Fedora noir · cravate rouge · canne au pommeau doré · gants noirs · manteau long noir.
Aucun accessoire ajouté ou retiré sans validation.

## 3. Proportions
Silhouette très élancée (~8 têtes chapeau compris), épaules étroites et droites,
manteau qui tombe jusqu'aux chevilles, canne tenue au centre, devant le corps.

## 4. Comportement à l'écran
- Mouvements lents : tourne la tête, lève la main gantée, pose un dossier, ouvre un tiroir d'archives.
- Ne court jamais, ne crie jamais, aucun geste brusque.
- Son œil ambre « s'allume » au moment des révélations (signature visuelle).
- Apparaît souvent dans la pénombre, éclairé par une lumière ambre latérale.

## 5. Voix
Française, masculine, grave, posée, naturelle. Toujours la même voix pour toute la série.
Statut : _voix à choisir et à figer_ (voir `ROADMAP.md`). Ne jamais cloner la voix d'une vraie
personne sans son accord écrit.

## 6. Bibliothèque de références officielles

Dossier : `archiviste/references/`. Seules les images validées y entrent.
Les générations en attente vont dans `archiviste/candidats/`.

| Référence | Fichier | Statut |
| --- | --- | --- |
| Character_FullBody | `Character_FullBody_v1.jpg` | ✅ Officielle (fournie par l'utilisateur) |
| Character_Front | — | ⏳ À générer depuis FullBody |
| Character_Profile | — | ⏳ À générer |
| Character_Back | — | ⏳ À générer |
| Character_Closeup | — | ⏳ À générer (masque, fissure, œil) |
| Character_Expressions | — | ⏳ À générer (planche : neutre, attentif, menaçant, révélation…) |
| Character_Poses | — | ⏳ À générer (planche : marche, dossier en main, désigne, assis…) |

Nommage : `Character_<Type>_v<N>.png`. Une nouvelle version n'efface jamais l'ancienne.

## 7. Contrôle qualité d'une image de l'Archiviste

Comparer côte à côte avec la référence officielle. **Rejeter et régénérer** si l'un des points échoue :

- [ ] Masque : forme du bec, couleur ivoire, coutures identiques
- [ ] Fissure tempe gauche présente (une fois validée)
- [ ] Œil : conforme à la décision du §1
- [ ] Fedora, cravate rouge, canne dorée, gants noirs présents
- [ ] Manteau noir long à grands revers
- [ ] Proportions élancées respectées
- [ ] Couleurs dans la palette DOSSIER 00
- [ ] Style 3D stylisé cinématographique (pas photoréaliste, pas cartoon)
- [ ] Format demandé (9:16 pour les scènes)

Résultat noté dans le `QC.md` de l'épisode.
