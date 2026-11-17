#!/usr/bin/env python3
"""Contrôles qualité d'une vidéo exportée.

  python3 scripts/controle.py planches <video.mp4> [--fps 2]   → planches-contact à 2 images/s (PNG)
  python3 scripts/controle.py hook <video.mp4>                  → mouvement image par image sur les 4 premières s
  python3 scripts/controle.py voix <video.mp4> <script.txt>     → relit la voix (transcription) et compare au script

Règle du hook (DA) : aucun plan immobile de plus de 0,5 s dans les 4 premières secondes.
"""
import difflib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLI = ["node", str(ROOT / ".claude/skills/hyperframes/scripts/plugin-cli.mjs")]


def duree(v):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v],
                                capture_output=True, text=True, check=True).stdout)


def planches(v, fps=2.0):
    out = pathlib.Path(v).with_suffix("").parent / "planches"
    out.mkdir(exist_ok=True)
    n = int(duree(v) * fps)
    lignes = 4
    tuiles = 8
    for i in range(0, n, tuiles * lignes):
        dest = out / f"planche-{i // (tuiles * lignes) + 1:02d}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{i / fps:.2f}", "-i", v, "-vf",
                        f"fps={fps},scale=180:-1,drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=14:fontcolor=white:box=1:boxcolor=black@0.6,"
                        f"tile={tuiles}x{lignes}", "-frames:v", "1", str(dest)], check=True)
        print(dest)


def hook(v):
    """Différence moyenne entre images successives (10 im/s) sur 0–4 s ; signale ≥ 0,5 s sans mouvement."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-t", "4", "-i", v, "-vf", "fps=10,scale=108:192,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    taille = 108 * 192
    imgs = [raw[i:i + taille] for i in range(0, len(raw), taille) if len(raw[i:i + taille]) == taille]
    diffs = [sum(abs(imgs[k - 1][j] - imgs[k][j]) for j in range(0, taille, 7)) / (taille / 7) for k in range(1, len(imgs))]
    lents = [k / 10 for k, d in enumerate(diffs, 1) if 0.12 <= d < 0.5]
    if len(lents) >= 5:
        print(f"⚠ mouvement très lent sur {len(lents) / 10:.1f} s des 4 premières secondes : le hook gagnerait un vrai impact")
    figes, debut = [], None
    for k in range(1, len(imgs)):
        diff = diffs[k - 1]
        if diff < 0.12:  # image réellement figée (une lente avancée de caméra mesure ~0,3)
            debut = debut if debut is not None else (k - 1) / 10
        else:
            if debut is not None and k / 10 - debut >= 0.5:
                figes.append((debut, k / 10))
            debut = None
    if debut is not None and len(imgs) / 10 - debut >= 0.5:
        figes.append((debut, len(imgs) / 10))
    for a, b in figes:
        print(f"✗ image figée de {a:.1f} s à {b:.1f} s (hook)")
    print("✓ hook : ça bouge en continu sur 0–4 s" if not figes else "→ ajouter un mouvement ou un impact")
    return not figes


def voix(v, script_path):
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "voix.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
        subprocess.run(CLI + ["transcribe", wav, "--engine", "whisper", "--model", "small", "--language", "fr", "--json"],
                       cwd=d, capture_output=True, check=True, env=dict(os.environ, HYPERFRAMES_TELEMETRY="0"))
        t = json.loads(pathlib.Path(d, "transcript.json").read_text())
        entendu = " ".join(w["text"] for w in (t if isinstance(t, list) else t["words"]))
    n = lambda s: re.sub(r"[^\w ]+", " ", s.lower()).split()  # noqa: E731
    a, b = n(pathlib.Path(script_path).read_text()), n(entendu)
    ratio = difflib.SequenceMatcher(a=a, b=b).ratio()
    print(f"concordance voix / script : {ratio:.0%}")
    for op, a0, a1, b0, b1 in difflib.SequenceMatcher(a=a, b=b).get_opcodes():
        if op != "equal":
            print(f"  {op}: script « {' '.join(a[a0:a1])} » / entendu « {' '.join(b[b0:b1])} »")
    return ratio


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    c, v = sys.argv[1], sys.argv[2]
    if c == "planches":
        planches(v, float(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[3] == "--fps" else 2.0)
    elif c == "hook":
        sys.exit(0 if hook(v) else 1)
    elif c == "voix":
        voix(v, sys.argv[3])
    else:
        sys.exit(__doc__)
