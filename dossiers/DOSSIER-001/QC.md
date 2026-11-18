# Contrôle qualité — DOSSIER 001

Rien n'est « terminé » sans cette fiche remplie. Validation humaine obligatoire avant publication.

## Faits
- [x] Chaque fait du scénario renvoie à une source listée
- [x] Faits / accusations / hypothèses distingués à l'écran
- [x] Statut judiciaire vérifié, présomption d'innocence respectée
- [x] Aucune preuve ni témoignage inventé
- [x] Pas d'image de vraie victime, rien de gore

## Archiviste (chaque image / plan)
| Plan | Masque | Accessoires | Proportions | Couleurs | Verdict |
| --- | --- | --- | --- | --- | --- |
| p4, p11 | image officielle telle quelle | ✓ | ✓ | ✓ | ✓ |

Écart important → régénérer la scène (checklist complète : `archiviste/CHARACTER.md` §7).

## Vidéo
- [x] Fichier final existe : `export/final.mp4`
- [x] 1080 × 1920, 30 im/s, durée 61,8 s (ffprobe)
- [x] Animations fluides, une seule chose bouge à la fois
- [x] Couleurs dans la palette, textes lisibles ≥ 1,5 s
- [x] Rien d'important en bas (20 %) ni sur le bord droit
- [x] Titre ou Archiviste visible à 0 s
- [x] Hook : impact qui remplit l'écran, aucun plan immobile > 0,5 s sur 0–4 s (`python3 scripts/controle.py hook export/final.mp4`)
- [x] Planches à 2 images/s regardées (`python3 scripts/controle.py planches export/final.mp4`) : rien de vide, figé ou trop lent
- [x] Voix relue : 92 % — noms anglais mal prononcés (Long Island, pick-up, Heuermann) et « 1993 » entendu « 1983 » : voix provisoire, sous-titres corrects
- [x] Version légère < 48 Mo (`scripts/export_leger.sh export/final.mp4`)
- [ ] Voix = voix officielle de l'Archiviste (✗ voix provisoire féminine) — sous-titres synchronisés ✓
- [x] `check --json` propre, images clés regardées

## Validation
- Validé par : ____  Date : ____
