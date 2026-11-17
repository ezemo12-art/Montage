# Moteur de motion design narratif — Architecture

Objectif : chaque passage important de la narration devient une **scène illustrée** où le
spectateur voit l'action (personnages, lieux, objets), synchronisée sur la voix.

## 1. Existant (conservé, rien n'est détruit)

| Brique | Rôle | État |
| --- | --- | --- |
| HyperFrames (HTML → MP4, GSAP, SVG, Three.js, Lottie, canvas) | Moteur d'animation et de rendu | ✅ installé, testé |
| FFmpeg / FFprobe | Assemblage, vérification | ✅ |
| Transcription whisper.cpp (FR, mots horodatés) | Synchro voix ↔ images | ✅ testé |
| Voix Kokoro (local) | Voix de démo | ✅ (pas de voix masculine FR) |
| Détourage local (`hyperframes remove-background`) | Personnages IA détourés → 2.5D | ✅ disponible |
| Système graphique `motion/` (9 compositions) | Infographies documentaires | ✅ |
| `scripts/gen_image.py` (OpenAI GPT Image + références) | Personnages / décors IA | ✅ codé, ⏳ clé API |
| Moteur vidéo IA (image → vidéo) | Mouvements complexes | ⏳ fournisseur à choisir |

**Choix : HyperFrames plutôt que Remotion.** HyperFrames fait déjà ce que Remotion apporterait
(composants HTML/SVG, React possible, Three.js, rendu déterministe, prévisualisation éditable),
est déjà intégré et testé ici, et n'impose pas de licence entreprise. Ajouter Remotion
doublerait le moteur sans gain.

## 2. Chaîne de production

```
script / voix off
   │  (1) ANALYSE — Claude lit le script et produit storyboard.json :
   │      personnages, lieux, objets, actions, émotion, ancre texte de chaque plan
   ▼
storyboard.json  ◄── bibliothèques persistantes : personnages/ lieux/ (réutilisés d'une vidéo à l'autre)
   │  (2) TIMING — la transcription (mots horodatés) place chaque plan sur la voix
   ▼
   │  (3) RENDU DE CHAQUE PLAN selon son style :
   │      a. « silhouettes » vectoriel (SVG articulé, procédural)  ← disponible maintenant
   │      b. « illustration 2.5D » : image IA par couche + détourage + parallaxe ← clé image
   │      c. « clip IA » : image de référence → vidéo (marche, conduite…) ← fournisseur vidéo
   │      d. « infographie » : compositions motion/ (carte, chronologie, document…) ← disponible
   ▼
projet HyperFrames (un plan = une sous-composition) + voix + sous-titres + grain
   │  (4) PRÉVISUALISATION / RETOUCHE plan par plan (Studio HyperFrames, storyboard.json)
   ▼  (5) RENDU MP4 9:16 + contrôle qualité (images décodées, durée, zones sûres)
```

## 3. Modules (`engine/`)

| Module | Rôle |
| --- | --- |
| `storyboard.py` | Schéma + validation du storyboard, calage des plans sur la transcription |
| `character.py` | Personnage articulé (squelette SVG : tête, torse, manteau, bras, jambes) généré depuis une fiche (sexe, âge, carrure, vêtements, chapeau, cheveux) → même apparence dans tous les plans |
| `actions.py` | Mouvements : marcher, s'arrêter, se retourner, entrer, téléphoner… (poses clés + cycles déterministes) |
| `decors.py` | Lieux : maison de nuit (portes, fenêtres allumables), intérieur couloir, voisinage, rue… même lieu = même design dans tous les plans |
| `props.py` | Objets et effets : ondes sonores, lumières, voiture… |
| `camera.py` | Caméra par plan : push-in, travelling, cadrage serré, parallaxe par couches |
| `compiler.py` | storyboard → projet HyperFrames (plans, voix, sous-titres, DA) |
| `providers/` | Connexions réelles : image (OpenAI GPT Image), vidéo (à brancher), voix |

Bibliothèques persistantes : `bibliotheque/personnages/*.json`, `bibliotheque/lieux/*.json`.

## 4. Interface de contrôle

- **Storyboard** (`storyboard.json`) : chaque plan est modifiable seul (texte d'ancre, lieu,
  personnages, action, caméra, style) ; recompiler ne touche que ce qui change.
- **Studio HyperFrames** (`preview`) : voir chaque plan, déplacer / raccourcir sur la timeline,
  prévisualiser le rendu final.
- **Régénérer un plan** : `scripts/engine.py build … --plan p3` (à venir) ; une image IA ratée se
  régénère seule sans refaire la vidéo.

## 5. Phases

1. ✅→ **Moteur silhouettes** (maintenant, sans clé) : personnages articulés, décors, actions,
   caméra, synchro voix, assemblage, démo sur la narration d'exemple.
2. ⏳ **Illustration 2.5D IA** : génération par couches (décor / personnage), détourage local,
   parallaxe et mouvements de caméra — nécessite la clé OpenAI.
3. ⏳ **Clips vidéo IA** pour les mouvements complexes — nécessite un fournisseur vidéo.
4. ⏳ **Analyse automatique** du script par l'API Claude (aujourd'hui faite par Claude Code).
5. ⏳ Bibliothèque élargie : femme, enfant, enquêteur, voiture animée, forêt, rue, ruban de police…
