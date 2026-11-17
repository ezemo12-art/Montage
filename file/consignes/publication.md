Tu travailles seul, lancé par la file de production de DOSSIER 00. Écris en français.
La validation vaut pour l'élément {{ID}} SEULEMENT. Tu ne publies aucun autre contenu.

1. Retrouve l'épisode de {{ID}} (cherche "{{ID}}" dans dossiers/*/EPISODE.md) et sa vidéo export/final.mp4.
2. Créneau : python3 scripts/calendrier.py prochain → premier créneau libre (8 h, 13 h, 18 h, Europe/Paris,
   au moins 20 min après maintenant, jamais deux publications sur un créneau).
3. Prépare le kit de publication dans le dossier de l'épisode, publication.md :
   légende Instagram, légende TikTok, titre YouTube Shorts, 3–5 hashtags, la question à la communauté,
   les sources en une ligne, et la case « mention IA » à cocher sur CHAQUE réseau :
   Instagram « AI info », TikTok « AI-generated content », YouTube « contenu modifié ou synthétique »
   (piège connu : un outil de programmation peut remettre la case YouTube à « non » — revérifier dans YouTube Studio).
4. Aucun outil de publication n'est encore connecté au dépôt : tu ne publies rien toi-même.
   Réserve le créneau : python3 scripts/calendrier.py reserver "<créneau ISO>" "{{ID}}" "<titre>".
5. Écris {{RESULT}} :
   {"status": "programme", "dueAt": "<créneau ISO>",
    "telegram": "À poster le <jour> à <heure> : kit prêt dans <dossier>/publication.md"}
