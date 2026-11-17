#!/usr/bin/env python3
"""Génère les compositions qui contiennent des tracés calculés :
  motion/src/carte.src.html     → motion/compositions/carte.html     (carte de France, assets/france.json)
  motion/src/empreinte.src.html → motion/compositions/empreinte.html (empreinte digitale procédurale)

  python3 -I scripts/build_motion.py

Tout est déterministe : relancer donne exactement le même résultat.
"""
import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
M = ROOT / "motion"


def build_carte():
    fr = json.loads((M / "assets" / "france.json").read_text())
    vb = fr["viewBox"]
    s = (M / "src" / "carte.src.html").read_text()
    s = (s.replace("{{PATH}}", fr["path"])
          .replace("{{VIEWBOX}}", " ".join(str(v) for v in vb))
          .replace("{{VIEWBOX_ARR}}", ", ".join(str(v) for v in vb))
          .replace("{{PROJ}}", json.dumps(fr["projection"])))
    (M / "compositions" / "carte.html").write_text(s)


def ridges():
    """Crêtes d'une empreinte : anneaux déformés, coupés en arcs (bifurcations)."""
    cx, cy, out = 260.0, 330.0, []
    for i in range(30):
        rx = 10 + i * 8.6
        ry = rx * 1.32
        steps = 160
        pts = []
        for k in range(steps + 1):
            t = 2 * math.pi * k / steps
            wob = 1 + 0.05 * math.sin(3 * t + i * 0.55) + 0.025 * math.sin(7 * t + i * 1.3)
            # boucle : les anneaux s'aplatissent vers le bas
            yflat = 0.82 if math.sin(t) > 0 else 1.0
            pts.append((cx + rx * wob * math.cos(t), cy + ry * wob * yflat * math.sin(t) - i * 1.6))
        # coupures déterministes pour imiter les bifurcations
        gaps = {(i * 37 + j * 53) % steps for j in range(1 + i % 3)}
        seg = []
        for k, p in enumerate(pts):
            if any(abs(k - g) < 4 for g in gaps):
                if len(seg) > 3:
                    out.append(seg)
                seg = []
            else:
                seg.append(p)
        if len(seg) > 3:
            out.append(seg)
    return "".join(
        '<path class="em-ridge" d="M' + "L".join(f"{x:.1f},{y:.1f}" for x, y in seg) + '"/>' for seg in out)


def build_empreinte():
    s = (M / "src" / "empreinte.src.html").read_text().replace("{{RIDGES}}", ridges())
    (M / "compositions" / "empreinte.html").write_text(s)


# Bande démo : les compositions à la suite (id, durée du créneau en s).
SCENES = [("ouverture-dossier", 6.1), ("chronologie", 7.1), ("carte", 7.1), ("empreinte", 7.1),
          ("document", 7.1), ("suspects", 7.1), ("annotations", 8.1), ("revelation", 4.9), ("cloture", 6.4)]


def build_index():
    t, hosts = 0.0, []
    for sid, d in SCENES:
        hosts.append(f'''      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html"
        data-start="{t:.1f}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>''')
        t += d
    s = (M / "src" / "index.src.html").read_text()
    s = s.replace("{{TOTAL}}", f"{t:.1f}").replace("{{HOSTS}}", "\n".join(hosts))
    s = s.replace("{{DA_CSS}}", (ROOT / "da" / "da.css").read_text())
    (M / "index.html").write_text(s)
    return t


(M / "assets" / "da.css").write_text((ROOT / "da" / "da.css").read_text())  # synchro DA
build_carte()
build_empreinte()
total = build_index()
print(f"✓ carte.html, empreinte.html et index.html générés (bande démo {total:.1f} s)")
