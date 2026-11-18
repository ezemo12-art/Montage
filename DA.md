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
| **Narrateur** | L'Archiviste (personnage permanent), **dans un coin de l'écran**, qui pose l'énigme et explique |
| **Contenu** | **Énigmes criminelles et énigmes de situation** (fictives), PAS d'histoires vraies |
| **Objectif n°1** | **Vues et commentaires** : chaque vidéo finit sur une question à laquelle on répond en commentaire |

Mots-clés : *énigme · indice caché · suspects · piège · « t'as trouvé ? » · lumière ambre dans le noir.*
Jamais gore, jamais « cheap ». Personnages **atypiques et créatifs** (mime, dompteuse, ventriloque et sa
marionnette, majordome, jumeaux, horloger…), jamais des silhouettes génériques.

### Les 3 formats et leurs hooks (à alterner)

| Format | Hook (0–2 s, en gros texte + voix) | Exemples de thèmes |
| --- | --- | --- |
| **Énigme de situation** | « **1… 2… 3… raté.** » (compte à rebours puis tampon RATÉ) | évasion de prison, pièce fermée de l'intérieur, faux alibi, survie, braquage |
| **Enquête criminelle** | « **Tu penses être un enquêteur… ou plutôt nul à chier ?** » | trouver le coupable parmi 3 suspects, l'indice qui trahit, le mensonge |
| **Esprit criminel** | « **STOP. Penses-tu comme un criminel ?** » | « comment a-t-il réussi ? », « quelle erreur l'a fait tomber ? », le crime parfait |

Règles d'une bonne énigme virale :
- **Résoluble avec ce qui est montré** : l'indice décisif est dit OU visible à l'écran (jamais une info cachée).
- **Une seule bonne réponse**, vérifiable ; un piège plausible pour les autres réponses (ça fait débattre).
- **Courte** : 30–50 s. Une phrase = une image.
- **Pas de réponse dans la vidéo** : « Écris ta réponse en commentaire » ; la solution va dans le **commentaire
  épinglé** ou la **partie 2** (fait revenir et commenter).
- Fin qui pique l'ego : « Les vrais enquêteurs l'ont déjà trouvé. », « 90 % se trompent. »

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

## 6. Structure d'une vidéo énigme (30–50 s)

| # | Séquence | Durée indicative |
| --- | --- | --- |
| 1 | **Hook** (un des 3, gros texte plein écran, Archiviste dans le coin) | 0–3 s |
| 2 | La situation / le crime (1–2 images, bandeau titre en haut) | 3–12 s |
| 3 | Les suspects ou les éléments (cartes étiquetées, un par un, leur phrase en bulle) | 12–35 s |
| 4 | **La question** + compte à rebours 3-2-1 | 35–42 s |
| 5 | Appel au commentaire (« Écris ta réponse… ») + DOSSIER 00 | 42–50 s |

L'Archiviste est présent **pendant toute la vidéo**, en bas à gauche, et change de pose (explique, désigne,
réfléchit) selon ce qu'il dit. Plus d'apparition « plein écran » sauf exception.

La 1re image (0 s) doit déjà montrer le titre ou l'Archiviste : c'est la miniature.
**Hook** : un impact qui remplit l'écran dès 0 s ; aucun plan immobile de plus de 0,5 s dans les 4 premières
secondes (contrôle : `scripts/controle.py hook`).

**Calendrier** : 3 publications par jour, 8 h · 13 h · 18 h (Paris), Instagram + TikTok + YouTube Shorts,
jamais deux sur un même créneau (`scripts/calendrier.py`).

## 7. Son

- **Voix** : voix de l'Archiviste = ElevenLabs « Kevan – Narrateur Cinématique » (`AYfOkr1hDQYbhigmRZ16`),
  française, grave, sombre, intrigante ; un peu joueuse sur les hooks et la fin (balises [intrigued],
  [mischievous], [whispers], [pause]). Toujours la même voix.
- Nappe sombre (drone, piano grave, cordes basses), très en dessous de la voix.
- Sons discrets : papier, machine à écrire, tic d'horloge, souffle sur les titres.
- Interdit : bruitages cartoon, jump scares, cris, musique épique.

## 8. Mise en page (Reels / TikTok)

- Textes entre **x = 150 et x = 890 px** ; zone utile **y = 280 à 1230 px** (sous 1230 px, l'interface Reels peut cacher le texte).
- Rien d'important dans les 20 % du bas ni sur le bord droit.
- Titres en haut (~300–650 px), sous-titres au milieu (~900–1150 px).
- **Vidéos énigmes** : bandeau titre en haut (y ≈ 260–340), illustration au centre (y ≈ 360–1000),
  sous-titres (y ≈ 1030–1150), **Archiviste en bas à gauche** (x 0–380, y ≈ 1150–1560, il peut déborder
  sous la zone sûre : c'est un personnage, pas du texte).

## 9. Éthique (fait partie de la DA)

- Les énigmes sont **fictives** : personnages et lieux inventés, aucune vraie personne, aucune vraie affaire
  présentée comme telle (si un jour une vidéo s'inspire d'un fait réel : sources, statut judiciaire, présomption
  d'innocence, comme avant).
- Pas de gore, pas de cadavre montré : on suggère (chapeau tombé, gant, verre renversé).
- Pas de méthode réellement dangereuse détaillée (fabrication d'arme, poison précis, mode d'emploi d'une évasion
  réelle) : l'énigme reste un jeu de logique.
- Contenus générés par IA : mention IA cochée sur CHAQUE réseau, à chaque publication — Instagram « AI info »,
  TikTok « AI-generated content », YouTube Shorts « contenu modifié ou synthétique » (revérifier dans YouTube
  Studio : certains outils de programmation remettent la case à « non »).
- Droit d'auteur (art. L122-4 CPI) : une vidéo de référence inspire le sujet, jamais le contenu ; on ne reprend
  ni images, ni texte, ni montage d'autrui.

## 10. Phrase de style (à coller au début de chaque demande)

> DOSSIER 00 : énigmes criminelles fictives, animation 3D stylisée cinématographique, personnages atypiques.
> Palette stricte : noir charbon #101113, gris archive #29292B, ivoire #E5DDCB, ambre #D6A64A,
> rouge sombre #9E2929 (rare). Oswald majuscules + IBM Plex Mono. Mouvements lents et maîtrisés,
> une seule chose bouge à la fois. Narrateur : l'Archiviste (références officielles obligatoires).
> Jamais de rebonds, flashs, couleurs hors palette ni images gore.
