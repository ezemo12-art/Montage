#!/usr/bin/env bash
# Crée un dossier d'épisode : scripts/new_episode.sh 001 "Titre de l'affaire"
set -euo pipefail
NUM=$(printf "%03d" "$((10#${1:?numéro requis}))")
TITRE="${2:?titre requis}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="$ROOT/dossiers/DOSSIER-$NUM"
[ -e "$DIR" ] && { echo "✗ $DIR existe déjà"; exit 1; }
mkdir -p "$DIR"/{sources,images,video,audio,motion,export}
for f in EPISODE.md QC.md; do
  sed -e "s/{{NUM}}/$NUM/g" -e "s/{{TITRE}}/$TITRE/g" "$ROOT/templates/episode/$f" > "$DIR/$f"
done
echo "✓ $DIR créé"
