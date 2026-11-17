# Contrôle qualité — DOSSIER {{NUM}}

Rien n'est « terminé » sans cette fiche remplie. Validation humaine obligatoire avant publication.

## Faits
- [ ] Chaque fait du scénario renvoie à une source listée
- [ ] Faits / accusations / hypothèses distingués à l'écran
- [ ] Statut judiciaire vérifié, présomption d'innocence respectée
- [ ] Aucune preuve ni témoignage inventé
- [ ] Pas d'image de vraie victime, rien de gore

## Archiviste (chaque image / plan)
| Plan | Masque | Accessoires | Proportions | Couleurs | Verdict |
| --- | --- | --- | --- | --- | --- |

Écart important → régénérer la scène (checklist complète : `archiviste/CHARACTER.md` §7).

## Vidéo
- [ ] Fichier final existe : `export/final.mp4`
- [ ] 1080 × 1920, 30 im/s, durée 60–90 s (ffprobe)
- [ ] Animations fluides, une seule chose bouge à la fois
- [ ] Couleurs dans la palette, textes lisibles ≥ 1,5 s
- [ ] Rien d'important en bas (20 %) ni sur le bord droit
- [ ] Titre ou Archiviste visible à 0 s
- [ ] Hook : impact qui remplit l'écran, aucun plan immobile > 0,5 s sur 0–4 s (`python3 scripts/controle.py hook export/final.mp4`)
- [ ] Planches à 2 images/s regardées (`python3 scripts/controle.py planches export/final.mp4`) : rien de vide, figé ou trop lent
- [ ] Voix relue par transcription et comparée au script (`python3 scripts/controle.py voix export/final.mp4 script.txt`)
- [ ] Version légère < 48 Mo (`scripts/export_leger.sh export/final.mp4`)
- [ ] Voix = voix officielle de l'Archiviste, sous-titres synchronisés
- [ ] `check --json` propre, images clés regardées

## Validation
- Validé par : ____  Date : ____
