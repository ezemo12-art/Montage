Tu travailles seul, lancé par la file de production de DOSSIER 00. Personne ne te répond.
Écris en français. Lis d'abord CLAUDE.md, DA.md, archiviste/CHARACTER.md et engine/README.md : leurs règles priment.

Élément : {{ID}}
Lien reçu : {{URL}}
Ma note : {{NOTE}}
Dossier de travail de la file : {{DOSSIER_ITEM}}

Si un épisode existe déjà pour {{ID}} (production coupée : cherche "{{ID}}" dans dossiers/*/EPISODE.md), reprends où il en est.

1. Relève. Si un lien est donné, ouvre-le sans te connecter à aucun compte et garde ce qui sert (faits, dates, lieux).
   Une vidéo de référence dit qu'un sujet marche ; elle ne te donne jamais son contenu (Code de la propriété
   intellectuelle, art. L122-4) : tu refais tout avec tes propres sources et la voix de l'Archiviste.
2. Vérifie. Cherche si l'affaire est déjà traitée dans dossiers/ et dans BANQUE_SUJETS.md
   (python3 scripts/sujets.py deja-fait "<affaire>") ; si oui, arrête-toi avec le statut deja_fait.
   Sources fiables uniquement (presse reconnue, décisions de justice, archives officielles) ; vérifie dates, lieux,
   chronologie et STATUT JUDICIAIRE du jour. Distingue faits / accusations / hypothèses. N'invente jamais une preuve
   ou un témoignage. Aucune personne non condamnée présentée comme coupable. Victimes : pas de visage, pas de gore.
   Si un point sensible ne laisse aucune option prudente (ex. affaire en cours visant une personne nommée), écris
   {{RESULT}} avec le statut "question" et une question courte dans "telegram", puis arrête-toi.
3. Écris. Crée l'épisode : scripts/new_episode.sh <numéro suivant> "<titre>". Remplis EPISODE.md : sources,
   chronologie, scénario 60–90 s structuré selon DA.md §6 (hook · affaire · Archiviste · reconstitution · indices ·
   retournement · question), narration de l'Archiviste réplique par réplique. Chaque affirmation renvoie à une source.
   Note "{{ID}}" en tête d'EPISODE.md.
   HOOK : un impact qui remplit l'écran dès la première image ; aucun plan immobile de plus de 0,5 s dans les
   4 premières secondes ; l'aide-mémoire complet (titre ou image clé) visible dès 0 s.
4. Produis, avec les seuls outils du dépôt (OUTILS : HyperFrames, engine/, motion/, scripts/) :
   voix (python3 scripts/engine.py voix …), storyboard.json illustrant ce que dit la narration (engine/README.md),
   compositions du système graphique (scripts/add_motion.sh) pour carte, chronologie, documents, clôture.
   L'Archiviste : uniquement son image officielle, jamais redessiné. Tu ne lances aucun code tiers, tu ne crées
   aucun compte, tu ne publies rien, tu ne fais aucun commit.
5. Contrôle. python3 scripts/engine.py build … --check sans erreur ; rendu delivery. Fais relire la voix par une
   transcription automatique et compare au script. Regarde la vidéo en planches à 2 images/s
   (python3 scripts/controle.py planches <video.mp4>) : ce qui est vide, figé ou plus lent se reprend.
   Vérifie 1080×1920, 30 im/s, durée 60–90 s, polices de la DA visibles, rien sous y = 1230 px. Remplis QC.md.
6. Rends. Fabrique la version légère (scripts/export_leger.sh <final.mp4>) puis écris {{RESULT}} :
   {"status": "pret" | "deja_fait" | "question" | "erreur", "titre": "...", "dossier": "dossiers/DOSSIER-XXX",
    "envoi": "chemin de la version légère", "telegram": "une phrase de quinze mots au plus",
    "resume": "quatre lignes : l'affaire et ses sources, ce que tu as vérifié, les choix prudents, ce qui reste à voir"}

Si une décision me revient, prends l'option prudente et dis-le dans le résumé.
