#!/usr/bin/env bash
# Télécharge une image / vidéo générée (Runway…) dans le dossier d'un épisode.
#   scripts/telecharger.sh "<url signée complète>" dossiers/DEMO-narratif/images/p2-approche.png
# L'URL signée doit être copiée telle quelle (avec son _jwt). Hôte autorisé dans l'environnement « Montage ».
set -euo pipefail
URL="${1:?url requise}"; OUT="${2:?fichier de sortie requis}"
mkdir -p "$(dirname "$OUT")"
curl -sSf --retry 3 -o "$OUT" "$URL"
python3 -c "from PIL import Image; im=Image.open('$OUT'); print('✓ $OUT', im.size)" 2>/dev/null || ls -la "$OUT"
