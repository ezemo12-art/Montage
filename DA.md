# DOSSIER 00 — Direction artistique officielle

> **Règle absolue** : chaque vidéo, image, couverture et PDF suit ce fichier.
> Ne jamais modifier arbitrairement cette identité. Toute exception doit être demandée
> explicitement. Valeurs techniques : `da/da.css` (à copier dans `assets/` de chaque vidéo).
> Personnage : `archiviste/CHARACTER.md` — l'image officielle fait foi, exactement telle quelle.

## 1. Identité

| | |
| --- | --- |
| **Nom** | DOSSIER 00 |
| **Slogan** | *Chaque détail cache une vérité.* |
| **Langue** | Français |
| **Format** | Vertical 9:16 — 1080 × 1920, 30 images/s |
| **Style** | Animation 3D stylisée, cinématographique |
| **Ambiance** | Thriller psychologique : sombre, mystérieux, immersif |
| **Narrateur** | L'Archiviste (personnage permanent) |

Mots-clés : *archive · secret · lumière ambre dans le noir · silence · indice · révélation.*
Jamais sensationnaliste, jamais gore, jamais « cheap ».

## 2. Palette officielle (5 couleurs, aucune autre)

| Rôle | Nom | Code | Usage |
| --- | --- | --- | --- |
| Fond | Noir charbon | `#101113` | Fond de tous les écrans |
| Surfaces | Gris archive | `#29292B` | Dossiers, cartes, cadres, documents |
| Texte | Ivoire | `#E5DDCB` | Titres, sous-titres, textes — rappelle le masque |
| Accent principal | Ambre | `#D6A64A` | L'œil de l'Archiviste, indices, lumière, mot clé |
| Accent alerte | Rouge sombre | `#9E2929` | Crime, danger, révélation, tampon « CONFIDENTIEL » |

Règles :
- **L'ambre est l'accent par défaut.** Le rouge est rare : réservé aux moments forts (≤ 1 fois par scène).
- Jamais ambre et rouge sur le même élément.
- Ivoire à 60–85 % d'opacité pour les textes secondaires.
- Interdit : toute autre couleur, néons, dégradés colorés, blanc pur `#FFFFFF`.

## 3. Typographies (2)

| Rôle | Police | Style |
| --- | --- | --- |
| Titres, sous-titres, révélations | **Oswald** | Majuscules, 600–700, serré |
| Dates, lieux, n° de dossier, coordonnées, annotations | **IBM Plex Mono** | Majuscules, espacement 0,08–0,2 em |

Tailles (1080 × 1920) : grand titre 120–150 px · sous-titres 68–80 px (3–4 mots/ligne,
mot clé en ambre) · infos mono 32–40 px.

## 4. Mouvements

**Oui** : lent, maîtrisé — comme la gestuelle de l'Archiviste. Fondus, flou → net, masque qui
monte, trait qui se trace, texte tapé à la machine, push-in très lent, lumière ambre qui s'allume.
Courbes : `ease-in-out`, `expo.out`, `power2/power3`.

**Non** : rebonds, secousses, flashs, zooms brusques, rotations rapides, glitch agressif.

Règle : **une seule chose bouge à la fois.**
Durées : grand titre 0,8–1,2 s · sous-titre 0,25–0,35 s/mot (synchro voix) ·
carte/document 0,6–0,9 s · tout texte ≥ 1,5 s à l'écran.

## 5. Système graphique permanent (motion design)

Compositions réutilisées d'un épisode à l'autre (bibliothèque : `motion/`) :

1. **Ouverture dossier** — chemise gris archive qui s'ouvre, `DOSSIER N°XXX` en mono ambre, titre en Oswald ivoire.
2. **Chronologie** — ligne fine ivoire, dates en mono, point ambre sur la date clé.
3. **Carte géographique** — carte sombre, point ambre qui pulse doucement, coordonnées en mono.
4. **Empreinte digitale** — révélation progressive (scan ambre).
5. **Document confidentiel** — feuille ivoire sur gris archive, tampon rouge sombre, phrase clé surlignée.
6. **Tableau des suspects** — fiches reliées par des lignes ivoire qui se tracent (rouge = lien clé).
7. **Annotations et coordonnées** — flèches fines, cercles, textes mono manuscrits/tapés.
8. **Révélation typographique** — mot clé géant qui sort du noir, flou → net.

Texture : grain de film léger + vignettage sur les images 3D. Rien d'autre.

## 6. Structure d'un épisode (60–90 s)

| # | Séquence | Durée indicative |
| --- | --- | --- |
| 1 | **Hook immédiat** (révélation typographique ou image choc non gore) | 0–3 s |
| 2 | Présentation de l'affaire (ouverture dossier, date, lieu) | 3–12 s |
| 3 | Apparition de l'Archiviste | 12–18 s |
| 4 | Reconstitution cinématographique | 18–45 s |
| 5 | Présentation des indices (documents, carte, empreintes) | 45–60 s |
| 6 | Retournement narratif | 60–75 s |
| 7 | Conclusion + question au spectateur + slogan | 75–90 s |

La 1re image (0 s) doit déjà montrer le titre ou l'Archiviste : c'est la miniature.

## 7. Son

- **Voix** : narration française masculine, grave, posée, naturelle et reconnaissable
  (toujours la même voix — voir `archiviste/CHARACTER.md`).
- Nappe sombre (drone, piano grave, cordes basses), très en dessous de la voix.
- Sons discrets : papier, machine à écrire, tic d'horloge, souffle sur les titres.
- Interdit : bruitages cartoon, jump scares, cris, musique épique.

## 8. Mise en page (Reels / TikTok)

- Textes entre **x = 150 et x = 890 px** ; zone utile **y = 280 à 1230 px** (sous 1230 px, l'interface Reels peut cacher le texte).
- Rien d'important dans les 20 % du bas ni sur le bord droit.
- Titres en haut (~300–650 px), sous-titres au milieu (~900–1150 px).

## 9. Éthique (fait partie de la DA)

- Faits réels et sourcés ; à l'écran, distinguer **FAIT / ACCUSATION / HYPOTHÈSE**.
- Vérifier le statut judiciaire ; présomption d'innocence : aucune personne non condamnée présentée comme coupable.
- Jamais de preuve, témoignage ou document inventé dans une histoire vraie.
- Reconstitutions : stylisées 3D, jamais de visage réaliste d'une vraie victime, pas de gore.
- Contenus générés par IA : activer l'étiquette « IA » d'Instagram / TikTok.

## 10. Phrase de style (à coller au début de chaque demande)

> DOSSIER 00 : animation 3D stylisée cinématographique, thriller psychologique sombre.
> Palette stricte : noir charbon #101113, gris archive #29292B, ivoire #E5DDCB, ambre #D6A64A,
> rouge sombre #9E2929 (rare). Oswald majuscules + IBM Plex Mono. Mouvements lents et maîtrisés,
> une seule chose bouge à la fois. Narrateur : l'Archiviste (références officielles obligatoires).
> Jamais de rebonds, flashs, couleurs hors palette ni images gore.
