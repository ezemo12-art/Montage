# DOSSIER 00 — Système graphique permanent (motion design)

Compositions HyperFrames réutilisées dans **tous** les épisodes. Format 1080 × 1920, 30 im/s,
palette et polices de `DA.md`. Chaque composition se personnalise par **variables** (textes,
chiffres, coordonnées) sans toucher au code.

Bande démo : `index.html` → `export/dossier00-motion-demo.mp4` (les 9 à la suite, 61 s).

## Catalogue

| Composition | Durée | Ce qu'elle montre | Variables |
| --- | --- | --- | --- |
| `ouverture-dossier` | 6 s | Chemise d'archive fermée (visible dès 0 s = miniature) qui s'ouvre : n° de dossier tapé, titre, trait ambre, date — lieu | `numero`, `titre`, `date_lieu` |
| `chronologie` | 7 s | Ligne verticale qui se trace, 4 dates qui apparaissent une à une, la date clé en ambre avec halo | `titre`, `d1..d4`, `e1..e4`, `cle` (1–4) |
| `carte` | 7 s | Carte de France réelle (Natural Earth) qui se dessine, point ambre placé par GPS, léger zoom, nom du lieu + coordonnées | `titre`, `lieu`, `lat`, `lon` |
| `empreinte` | 7 s | Empreinte digitale révélée par un scan ambre, 3 points de comparaison, compteur de correspondance | `titre`, `statut`, `resultat` (%), `label` |
| `document` | 7 s | Feuille de rapport, lignes tapées à la machine, ligne clé surlignée ambre, tampon rouge | `titre`, `reference`, `l1..l4`, `cle` (1–4), `tampon` |
| `suspects` | 7 s | 3 fiches de personnes reliées par des lignes ; le lien clé en rouge sombre | `titre`, `n1..n3`, `s1..s3` (statuts) |
| `annotations` | 8 s | Cercle, flèche, annotation tapée, coordonnées — à poser **par-dessus** une image ou un plan 3D | `note`, `coord`, `fond` (`demo` / `transparent`) |
| `revelation` | 5 s | Mot géant qui sort du noir (flou → net) avec halo ambre | `mot` (≤ 8 lettres), `sous_titre` |
| `cloture` | 6 s | Question au spectateur + slogan « Chaque détail cache une vérité. » + DOSSIER 00 | `question` |

Texture de marque (dans `index.html`) : grain de film léger + vignettage, au-dessus de tout.

## Réutiliser dans un épisode

```bash
scripts/add_motion.sh dossiers/DOSSIER-001/motion carte document cloture
```

Copie les compositions + la DA dans le projet de l'épisode, puis affiche le bloc à coller dans son
`index.html`, avec les variables à remplir :

```html
<div id="carte" data-composition-id="carte" data-composition-src="compositions/carte.html"
  data-start="12" data-duration="7.1" data-track-index="1" data-track-kind="graphics"
  data-width="1080" data-height="1920"
  data-variable-values='{"lieu":"Marseille","lat":43.2965,"lon":5.3698}'></div>
```

## Règles techniques (à respecter)

- **La DA doit être écrite en `<style>` dans l'`index.html` de chaque vidéo** (pas seulement en
  `<link>`) : sinon le moteur de rendu ne trouve pas Oswald / IBM Plex Mono et met une police par défaut.
  `build_motion.py` le fait pour la bande démo.
- `carte.html`, `empreinte.html` et `index.html` sont **générés** depuis `src/` :
  modifier `src/…` puis lancer `python3 -I scripts/build_motion.py`.
- Le tracé de la France vient de `assets/france.json` (`scripts/build_france_map.py`, domaine public).
- Les compositions sont muettes : le son (voix, nappe, bruitages) se pose dans chaque épisode.
- Zone de texte sûre : x 150–890 px, y 280–1230 px.
