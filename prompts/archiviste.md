# Prompts — L'Archiviste

Toujours envoyer `Character_FullBody_v1.jpg` (référence maîtresse, à reproduire exactement).
Toujours commencer le prompt par le **bloc personnage** puis le **bloc style**, sans les modifier.

## Bloc personnage (verrouillé)

```
The Archivist, the same character as in the reference image, exactly identical: a tall, slender,
elegant figure in a long black double-breasted overcoat with wide lapels reaching the ankles,
black waistcoat and shirt, a bright red tie, black gloves, a black fedora hat, and an ivory porcelain
plague-doctor mask with a long curved beak and stitched seams. Both gloved hands rest on the
golden handle of a slim golden cane. Two small dark eyes with a faint reddish glow behind the mask,
exactly as in the reference. No crack, no added details. Same proportions, same mask shape, same accessories
as the reference. Do not redesign the character.
```

## Bloc style (verrouillé)

```
Stylized cinematic 3D animation still, psychological thriller mood, dark and mysterious.
Strict palette: charcoal black #101113, archive grey #29292B, ivory #E5DDCB, amber #D6A64A
accents. The character's own colors (bright red tie, golden cane) stay exactly as in the reference. Soft volumetric amber key light, deep shadows,
subtle film grain, vignette. No text, no logo, no watermark. Not photorealistic, not cartoon.
```

## Références à créer

| Fichier cible | Taille | Prompt (après les 2 blocs) |
| --- | --- | --- |
| `Character_Front` | 1024x1536 | `Full-body front view, neutral standing pose, centered, plain charcoal background, character turnaround reference sheet style.` |
| `Character_Profile` | 1024x1536 | `Full-body side profile view facing left, beak in clear silhouette, plain charcoal background, character turnaround reference.` |
| `Character_Back` | 1024x1536 | `Full-body back view, coat and hat silhouette from behind, cane visible at the side, plain charcoal background, character turnaround reference.` |
| `Character_Closeup` | 1024x1536 | `Head and shoulders close-up, three-quarter view, detailed porcelain texture of the mask, stitched beak, hat brim casting shadow, plain charcoal background.` |
| `Character_Expressions` | 1536x1024 | `Character sheet with 4 head-and-shoulders panels in a row, same character: neutral, attentive (head tilted), menacing (head lowered, light from below), revelation (amber light on the mask). Plain charcoal background, consistent lighting.` |
| `Character_Poses` | 1536x1024 | `Character sheet with 4 full-body panels in a row, same character: walking slowly with the cane, holding an archive folder, pointing with a gloved hand, standing in front of archive shelves. Plain charcoal background.` |

## Scènes d'épisode (modèle)

```
[Bloc personnage] [Bloc style]
Scene: <lieu, époque, action lente de l'Archiviste>. Camera: <plan, angle>.
Vertical 9:16 composition, keep the top 15% and bottom 20% free of important details.
```
