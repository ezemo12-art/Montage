#!/usr/bin/env bash
# Version légère (< 48 Mo) pour l'envoi Telegram (limite Bot API : 50 Mo).
# Débit vidéo (kbit/s) = 360 000 / durée (s) − 128 pour le son, plafonné à 3600.
#   scripts/export_leger.sh <final.mp4> [sortie.mp4]
set -euo pipefail
IN="${1:?vidéo requise}"; OUT="${2:-${IN%.*}-envoi.mp4}"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
BR=$(python3 -c "print(max(500, min(3600, int(360000/float('$D')) - 128)))")
ffmpeg -v error -y -i "$IN" -c:v libx264 -preset slow -b:v ${BR}k -maxrate ${BR}k -bufsize $((BR*2))k \
  -c:a aac -b:a 128k -movflags +faststart "$OUT"
SZ=$(stat -c %s "$OUT" 2>/dev/null || stat -f %z "$OUT")
echo "✓ $OUT — $((SZ/1024/1024)) Mo, ${BR} kbit/s"
[ "$SZ" -lt $((48*1024*1024)) ] || { echo "✗ toujours > 48 Mo"; exit 1; }
