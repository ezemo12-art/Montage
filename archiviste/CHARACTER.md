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

### ✅ Écarts tranchés (validé par l'utilisateur)

| Point | Image v1 | Décision officielle |
| --- | --- | --- |
| Fissure | Non visible | **Ajoutée** : fine fissure qui part de la tempe gauche du masque (gauche du personnage) vers l'orbite |
| Œil | Deux yeux sombres rougeâtres | **Un seul œil ambre lumineux** `#D6A64A` (œil gauche du personnage, côté fissure) ; l'autre orbite reste dans l'ombre |
| Cravate | Rouge vif | **Rouge sombre** `#9E2929` |
| Fond | Bleu nuit | **Noir charbon** `#101113` avec halo ambre très discret derrière le personnage |

Tout le reste de la v1 est conservé à l'identique : masque à bec ivoire et ses coutures, fedora,
manteau croisé, gants, canne dorée, pose, proportions.

**Référence v2** (`Character_FullBody_v2`) : la v1 corrigée de ces 4 points, générée depuis la v1
(`prompts/archiviste_v2.md`), puis validée par l'utilisateur. Après validation, la v2 devient la
référence principale ; la v1 reste dans `references/` comme source de la silhouette.

## 2. Accessoires fixes
Fedora noir · cravate rouge sombre · canne au pommeau doré · gants noirs · manteau long noir.
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
| Character_FullBody | `Character_FullBody_v1.jpg` | ✅ Officielle (fournie par l'utilisateur, silhouette) |
| Character_FullBody | `Character_FullBody_v2.png` | ⏳ À générer depuis v1 (corrections §1) puis valider |
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
- [ ] Fine fissure à la tempe gauche du masque
- [ ] Un seul œil ambre lumineux (côté fissure), l'autre dans l'ombre
- [ ] Fedora, cravate rouge sombre, canne dorée, gants noirs présents
- [ ] Manteau noir long à grands revers
- [ ] Proportions élancées respectées
- [ ] Couleurs dans la palette DOSSIER 00
- [ ] Style 3D stylisé cinématographique (pas photoréaliste, pas cartoon)
- [ ] Format demandé (9:16 pour les scènes)

Résultat noté dans le `QC.md` de l'épisode.
