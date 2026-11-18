# Moteur de motion design narratif

Transforme une narration en **scènes illustrées** synchronisées sur la voix : personnages
articulés, décors, objets, actions, caméra, sous-titres. Architecture : `docs/ARCHITECTURE_MOTION_NARRATIF.md`.

## Utilisation

```bash
# 1. Voix + mots horodatés (voix de démo Kokoro ; remplacer voix.wav par la vraie voix de l'Archiviste)
python3 scripts/engine.py voix dossiers/DOSSIER-001 "Texte prononcé…" --vitesse 0.85
#    (ou déposer sa propre voix.wav puis : hyperframes transcribe voix.wav --engine whisper --model small --language fr)

# 2. Claude écrit dossiers/DOSSIER-001/storyboard.json à partir du script (règles ci-dessous)

# 3. Compiler, contrôler, rendre
python3 scripts/engine.py build dossiers/DOSSIER-001/storyboard.json dossiers/DOSSIER-001/video --check
python3 scripts/engine.py build dossiers/DOSSIER-001/storyboard.json dossiers/DOSSIER-001/video --render --qualite delivery
```

Retoucher **un plan** = modifier son entrée dans `storyboard.json` et recompiler ; la prévisualisation
et la timeline éditable : `hyperframes preview` dans le dossier `video/`.

## Analyse du script (ce que Claude fait avant d'écrire le storyboard)

Pour chaque passage important : **qui** (personnages), **où** (lieu), **quoi** (objets),
**action**, **émotion / atmosphère**, **quand** (le mot de la voix où l'image doit apparaître).
Règles :
- Un plan = une idée visuelle qui suit le récit (pas d'animation générique sans rapport).
- `ancre` = les premiers mots du passage narré : le plan commence quand la voix les prononce.
- Actions calées sur un mot précis : `"de": {"mot": "entre"}` ; sinon fraction du plan (0 → 1).
- Plans ≥ 1,2 s ; une seule action principale à la fois (DA : une seule chose bouge).
- Personnages et lieux décrits une fois (fiche), réutilisés dans tous les plans.
- Histoires vraies : silhouettes anonymes, jamais le visage d'une vraie victime, pas de gore.

## Format du storyboard

```jsonc
{
  "texte": "Texte exact de la narration (sous-titres fidèles)",
  "voix": "voix.wav", "transcription": "transcript.json",
  "mots_cles": ["maison", "bruit"],          // mots en ambre dans les sous-titres
  "personnages": {
    "homme1": { "bibliotheque": "homme-veste-noire" },          // fiche réutilisée
    "femme1": { "genre": "femme", "taille_cm": 165, "manteau": "long", "cheveux": "longs" }
  },
  "lieux": { "maison1": { "bibliotheque": "maison-etage-nuit" } },
  "plans": [
    { "id": "p2", "ancre": "un homme entre discrètement", "decor": "maison_nuit", "lieu": "maison1",
      "camera": { "type": "cadrage", "zoom": 1.25, "focus": [430, 900] },
      "personnages": [ { "qui": "homme1", "x": "gauche" } ],
      "actions": [ { "qui": "homme1", "action": "marche", "vers": "porte", "dx": -120, "de": 0, "a": 1 } ],
      "incrustation": { "texte": "23:00", "sous_texte": "Lyon" } }
  ]
}
```

### Bibliothèques disponibles

| Type | Valeurs |
| --- | --- |
| Décors | `archiviste` (plan narrateur : image officielle de l'Archiviste telle quelle, il sort de l'ombre, lumière ambre, caméra sur son visage) · `maison_nuit` (maison à étage, porte qui s'ouvre, 4 fenêtres allumables, applique, lampadaire) · `couloir` (intérieur en perspective, lampe, porte du fond) · `voisinage` (maison du récit au loin + maison des voisins, ondes sonores, voisin à la fenêtre) |
| Actions personnage | `marche`, `court`, `entre`, `regarde_derriere`, `telephone`, `apparait`, `disparait`, `tombe` |
| Actions décor | `ouvre_porte`, `ferme_porte`, `lumieres`, `eteint`, `bruit`, `voisin_regarde` · plan archiviste : `sort_de_l_ombre`, `lumiere_ambre` |
| Caméra | `push_in` (+ `intensite`), `cadrage` (+ `zoom`, `focus`), `travelling` (+ `pan`), `recul`, `fixe` ; `focus` : `porte`, `son`, `visage` ou `[x, y]` |
| Personnage (fiche) | `genre` homme/femme · `age` adulte/enfant · `taille_cm` · `carrure` mince/normale/forte · `manteau` long/court/aucun · `chapeau` · `cheveux` courts/longs/chignon/chauve · `description` (pour les images IA) |

Bibliothèque persistante (réutilisée d'une vidéo à l'autre) : `bibliotheque/personnages/`, `bibliotheque/lieux/`.

## Ajouter un décor / une action

- Décor : une fonction dans `engine/decors.py` qui remplit les couches `bg / mid / fg`, les `ancres`
  (porte, fenêtres, sol…) et `px_par_metre`, puis l'enregistrer dans `DECORS` et `storyboard.DECORS_CONNUS`.
- Action : une méthode d'`Acteur` (`engine/actions.py`) à base de poses clés, puis la brancher dans
  `compiler_plan` et `storyboard.ACTIONS_CONNUES`.

## Limites actuelles (style « silhouettes » vectoriel)

- Vue de profil uniquement ; pas encore de visages, d'expressions ni de vue de face.
- 3 décors ; pas encore de voiture animée, rue, forêt, poste de police, ruban de sécurité.
- Les styles « illustration 2.5D IA » et « clips vidéo IA » attendent les clés API (voir ROADMAP).

## Plans illustrés par images générées (Runway)

Style « illustration » : une image générée par plan (Runway, offre gratuite = images seulement),
animée par le moteur. Exemple complet : `dossiers/DEMO-narratif/storyboard-illustre.json`.

```jsonc
{ "id": "p5", "ancre": "les voisins entendent", "decor": "illustration", "image": "images/p5-voisins.png",
  "camera": { "type": "push_in", "focus": [760, 900], "intensite": 1.15 },
  "son_xy": [790, 960], "lumiere_xy": [540, 595], "lumiere_rayon": 200,
  "actions": [ { "action": "bruit", "de": { "mot": "bruit" } }, { "action": "lumiere_ambre", "de": 0.1 } ],
  "incrustation": { "texte": "23:07" } }
```

Règles de génération :
- Image 9:16, 2K, style de `prompts/archiviste.md` (bloc style) ; personnages anonymes, vus de dos ou de loin.
- **Cohérence** : générer d'abord le lieu principal, puis passer son image en référence (`@maison`) aux plans
  suivants ; idem pour un personnage (`@homme`). Ne jamais régénérer ce qui existe déjà.
- Télécharger : `scripts/telecharger.sh "<url signée>" dossiers/<épisode>/images/<plan>.png`.
- Coût indicatif : ~6 crédits par image 2K.
