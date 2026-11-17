# DOSSIER 00 — Feuille de route de production

Ce qui est en place ✅, ce qui manque ⏳ et ce qu'il faut pour le débloquer.

## Phase 1 — Fondations ✅
- ✅ Direction artistique officielle : `DA.md` + `da/da.css`
- ✅ Bible de l'Archiviste + référence officielle v1 : `archiviste/`
- ✅ Prompts verrouillés du personnage : `prompts/archiviste.md`
- ✅ Script de génération d'images avec références : `scripts/gen_image.py`
- ✅ Modèle d'épisode (scénario, sources, storyboard, prompts, son, couverture, publication) + fiche QC
- ✅ Création d'un épisode : `scripts/new_episode.sh <num> "<titre>"`
- ✅ Montage motion design + voix + sous-titres + export MP4 (HyperFrames, testé)

## Phase 2 — Bibliothèque de l'Archiviste ⏳
- ✅ Règle fixée : l'image fournie fait foi exactement (`archiviste/CHARACTER.md` §1)
- ⏳ Générer Front, Profile, Back, Closeup, Expressions, Poses → `archiviste/candidats/` → validation → `references/`
- **Bloquant : clé API OpenAI** (GPT Image). Coût indicatif : quelques centimes par image en qualité haute
  (à confirmer sur la page tarifs OpenAI).

## Phase 3 — Système de motion design permanent ⏳
Compositions HyperFrames réutilisables dans `motion/` : ouverture dossier, chronologie, carte,
empreinte digitale, document confidentiel, tableau des suspects, annotations, révélation typographique.
- Rien de bloquant : faisable dès maintenant.

## Phase 4 — Voix officielle de l'Archiviste ⏳
Voix française masculine grave et toujours identique. Options :
1. **Voicebox** sur ton ordinateur (gratuit, local) : voix de synthèse ou ta propre voix clonée.
2. **ElevenLabs** (payant, API) : voix « designée » grave, automatisable ici.
3. Kokoro (installé ici) : gratuit, mais **pas de voix masculine française** → ne convient pas comme voix officielle.
- **Bloquant : choix du moteur.**

## Phase 5 — Animation vidéo de l'Archiviste ⏳
⚠️ L'API vidéo Sora d'OpenAI a été fermée (24/09/2026) : il faut un autre fournisseur.
Candidats avec images de référence (tarifs à vérifier sur les sites officiels) :
- **Google Veo 3.1** (Gemini API) — jusqu'à 3 images de référence.
- **Kling** (API officielle ou fal.ai) — modèle « reference to video ».
- **Runway** (API Gen-4.x).
- **Bloquant : choix du fournisseur + clé API.** Ensuite : script `scripts/gen_video.py`
  (image → vidéo, journal des coûts, nouvelles tentatives), sur le modèle de `gen_image.py`.

## Phase 6 — Premier épisode complet ⏳
Recherche → scénario → storyboard (validation) → images → vidéos → voix → montage → QC → publication manuelle.

## Phase 7 — Boutique « LES DOSSIERS CONFIDENTIELS » ⏳
Jeux d'enquête **fictifs** en PDF : EXPRESS 4,90 € · CLASSIQUE 9,90 € · CONFIDENTIEL 19,90 €.
- Faisable ici : écriture de l'enquête, vérification que la solution est unique et déductible,
  mise en page PDF imprimable + lisible sur téléphone.
- Mention « fiction » sur chaque document ; aucun faux document présenté comme authentique.
- Plus tard : plateforme de vente (Gumroad, Payhip, Shopify…) — choix et compte à toi.

## Phase 8 — Automatisation ⏳
Chaîne : affaire → recherche → sources → scénario → storyboard → images → vidéo → voix →
montage → couverture → publication préparée → PDF → fiches produits → suivi des ventes.
- **Validation humaine obligatoire** avant toute publication d'histoire vraie et toute mise en vente.
- Publication automatique sur Instagram/TikTok : nécessite leurs API officielles (comptes pro) — plus tard.

## Règles techniques
- Clés API uniquement dans des variables d'environnement / secrets de l'environnement, jamais dans git.
- Chaque génération journalisée (`generations.jsonl`) pour suivre les coûts.
- Pas de génération inutile : réutiliser une référence existante quand elle suffit.
- Rien n'est « terminé » sans vérification du fichier et de sa qualité (fiche QC).
