# Fonds réutilisables (vidéos énigmes)

| Fichier | Contenu | Fabriqué avec |
|---|---|---|
| `bureau-enquete.png` (1080×1920) | Bureau d'enquête de DOSSIER 00, la nuit : mur de liège, photos anonymes, fils rouges, lampe, dossiers, loupe | Blender (`blender/fond_bureau_enquete.py`), gratuit, régénérable |

**Fond par défaut** de `scripts/enigme.py` : une énigme sans clé `"fond"` prend `bureau-enquete.png`
(flou 11, voile 0.4, lumière 1.35 : réglages vérifiés, le texte rouge du hook reste lisible).
Pour une énigme dont le lieu est fort (manoir, chalet…), on peut donner un fond propre :
`"fond": {"image": "<clé ou chemin>", "flou": 8, "voile": 0.35, "decor": "pluie" | "horloges"}`.
`"fond": false` = ancien fond papier.

Pour en ajouter : nouvelle scène Blender dans `blender/`, rendu ici, puis une ligne dans ce tableau.
