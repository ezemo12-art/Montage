# DOSSIER 00

*Chaque détail cache une vérité.*

Système de production de DOSSIER 00 : épisodes d'enquêtes criminelles en vidéo verticale
(Instagram / TikTok) racontés par **l'Archiviste**, et boutique de jeux d'enquête PDF
**LES DOSSIERS CONFIDENTIELS**.

| Fichier / dossier | Rôle |
| --- | --- |
| `DA.md` · `da/da.css` | Direction artistique officielle (palette, polices, mouvements, structure) |
| `archiviste/` | Bible du personnage + références officielles + candidats à valider |
| `prompts/archiviste.md` | Prompts verrouillés du personnage et des références à créer |
| `engine/` · `scripts/engine.py` | Moteur narratif : script → storyboard → scènes illustrées animées → vidéo |
| `bibliotheque/` | Personnages et lieux réutilisables d'une vidéo à l'autre |
| `motion/` | Système graphique permanent : 9 compositions réutilisables + bande démo |
| `scripts/add_motion.sh` | Ajoute des compositions du système graphique à un épisode |
| `scripts/gen_image.py` | Génération d'images avec références (OpenAI GPT Image) |
| `scripts/new_episode.sh` | Crée `dossiers/DOSSIER-XXX/` à partir du modèle |
| `templates/episode/` | Modèle d'épisode + fiche contrôle qualité |
| `ROADMAP.md` | Ce qui est prêt, ce qui manque, ce qui bloque |
| `docs/` | Tes textes d'origine, conservés mot pour mot |
| `CLAUDE.md` | Règles de travail lues par Claude à chaque session |
| `exemple-enquete/` | Test technique (avant DOSSIER 00) |
