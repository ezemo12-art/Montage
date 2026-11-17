#!/usr/bin/env bash
# Ajoute des compositions du système graphique DOSSIER 00 à un projet HyperFrames d'épisode.
#   scripts/add_motion.sh <dossier-projet> <composition> [composition…]
#   ex. scripts/add_motion.sh dossiers/DOSSIER-001/motion ouverture-dossier carte cloture
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:?dossier du projet requis}"; shift
[ $# -gt 0 ] || { echo "Compositions dispo :"; ls "$ROOT/motion/compositions" | sed 's/\.html$//'; exit 1; }
[ -f "$DEST/index.html" ] || { echo "✗ $DEST n'est pas un projet HyperFrames (pas d'index.html). Lance d'abord : init $DEST"; exit 1; }
mkdir -p "$DEST/compositions" "$DEST/assets"
cp "$ROOT/da/da.css" "$DEST/assets/da.css"
for c in "$@"; do
  src="$ROOT/motion/compositions/$c.html"
  [ -f "$src" ] || { echo "✗ composition inconnue : $c"; exit 1; }
  cp "$src" "$DEST/compositions/$c.html"
  vars=$(python3 -I -c "
import re,json,sys
s=open(sys.argv[1]).read()
m=re.search(r\"data-composition-variables='(.*?)'\",s,re.S)
v=json.loads(m.group(1)) if m else []
print(json.dumps({x['id']:x.get('default') for x in v},ensure_ascii=False))" "$src")
  echo "✓ $c — bloc à coller dans index.html (régler data-start / data-duration / variables) :"
  echo "  <div id=\"$c\" data-composition-id=\"$c\" data-composition-src=\"compositions/$c.html\" data-start=\"0\" data-duration=\"7\" data-track-index=\"1\" data-track-kind=\"graphics\" data-width=\"1080\" data-height=\"1920\" data-variable-values='$vars'></div>"
done
echo "Rappel : la DA doit être en <style> dans index.html (copie de da/da.css), voir motion/README.md."
