# L'ARCHIVISTE — Bible du personnage

> Personnage **permanent**, narrateur officiel de tous les épisodes de DOSSIER 00.
> Ne jamais créer un nouveau personnage. Ne jamais remplacer une référence officielle sans
> validation écrite de l'utilisateur.

## 1. Caractéristiques permanentes

### Selon la charte (texte)
- Masque en **porcelaine ivoire**.
- ~~Fine fissure près de la tempe gauche~~ → non appliqué (l'image fait foi).
- ~~Un seul œil lumineux ambre~~ → non appliqué (l'image fait foi).
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

### ✅ Règle : l'image officielle fait foi, exactement telle quelle

Décision de l'utilisateur : **garder exactement l'image fournie**. Aucune correction, aucune v2.
Quand le texte de la charte et l'image diffèrent, **c'est l'image qui gagne** :

| Point | Texte de la charte | Ce qu'on applique (= l'image) |
| --- | --- | --- |
| Fissure tempe gauche | Oui | **Pas de fissure** |
| Œil | Un seul œil ambre | **Deux yeux** comme sur l'image (petits, sombres, reflets rougeâtres) |
| Cravate | — | **Rouge vif**, comme sur l'image |
| Fond de la référence | — | **Dégradé bleu nuit**, comme sur l'image |

La palette officielle (DA.md) s'applique aux décors, au motion design et aux textes,
**jamais pour modifier l'apparence de l'Archiviste**.

## 2. Accessoires fixes
Fedora noir · cravate rouge vif · canne au pommeau doré · gants noirs · manteau long noir.
Aucun accessoire ajouté ou retiré sans validation.

## 3. Proportions
Silhouette très élancée (~8 têtes chapeau compris), épaules étroites et droites,
manteau qui tombe jusqu'aux chevilles, canne tenue au centre, devant le corps.

## 4. Comportement à l'écran
- Mouvements lents : tourne la tête, lève la main gantée, pose un dossier, ouvre un tiroir d'archives.
- Ne court jamais, ne crie jamais, aucun geste brusque.
- Aux révélations, une lumière ambre l'éclaire (sans modifier son apparence).
- Apparaît souvent dans la pénombre, éclairé par une lumière ambre latérale.

## 4 bis. Dans les vidéos (en attendant les clés de génération)

Plan `archiviste` du moteur (`engine/README.md`) : l'**image officielle est utilisée telle quelle**, sans
détourage ni retouche. Le mouvement vient uniquement de la mise en scène : il sort de l'ombre, une lumière
ambre monte, la caméra avance vers son visage. Utilisé là où la structure le place (présentation, conclusion).
Le détourage (pour le poser dans les décors) et l'animation de ses gestes attendent l'accord de l'utilisateur
et les clés OpenAI / vidéo.

## 4 ter. Poses de narrateur (vidéos énigmes)

`archiviste/poses/` : `archi-explique.png` (index levé), `archi-designe.png` (désigne vers la droite),
`archi-reflechit.png` (main près du bec), générées le 18/11/2026 à partir de l'image officielle (ElevenLabs,
modèle de cohérence de personnage). Fidèles à la référence (bec, fedora, cravate rouge, canne dorée).
Utilisées en bas à gauche de chaque vidéo énigme. Nouvelles poses : toujours depuis l'image officielle.

## 5. Voix
Française, masculine, grave, posée, naturelle. Toujours la même voix pour toute la série.
Statut : **figée** — ElevenLabs « Kevan – Narrateur Cinématique » (`AYfOkr1hDQYbhigmRZ16`, modèle eleven_v4) (voir `ROADMAP.md`). Ne jamais cloner la voix d'une vraie
personne sans son accord écrit.

## 6. Bibliothèque de références officielles

Dossier : `archiviste/references/`. Seules les images validées y entrent.
Les générations en attente vont dans `archiviste/candidats/`.

| Référence | Fichier | Statut |
| --- | --- | --- |
| Character_FullBody | `Character_FullBody_v1.jpg` | ✅ Officielle (fournie par l'utilisateur) — **référence maîtresse, intouchable** |
| Character_Front | — | ⏳ À générer depuis FullBody |
| Character_Profile | — | ⏳ À générer |
| Character_Back | — | ⏳ À générer |
| Character_Closeup | — | ⏳ À générer (masque, bec, yeux, chapeau) |
| Character_Expressions | — | ⏳ À générer (planche : neutre, attentif, menaçant, révélation…) |
| Character_Poses | — | ⏳ À générer (planche : marche, dossier en main, désigne, assis…) |

Nommage : `Character_<Type>_v<N>.png`. Une nouvelle version n'efface jamais l'ancienne.

## 7. Contrôle qualité d'une image de l'Archiviste

Comparer côte à côte avec la référence officielle. **Rejeter et régénérer** si l'un des points échoue :

- [ ] Masque : forme du bec, couleur ivoire, coutures identiques
- [ ] Aucune fissure ajoutée
- [ ] Deux yeux comme sur l'image officielle
- [ ] Fedora, cravate rouge vif, canne dorée, gants noirs présents
- [ ] Manteau noir long à grands revers
- [ ] Proportions élancées respectées
- [ ] Personnage identique à l'image officielle ; décor dans la palette DOSSIER 00
- [ ] Style 3D stylisé cinématographique (pas photoréaliste, pas cartoon)
- [ ] Format demandé (9:16 pour les scènes)

Résultat noté dans le `QC.md` de l'épisode.
