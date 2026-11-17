#!/usr/bin/env python3
"""Construit le tracé SVG de la France métropolitaine (Natural Earth 1:50m, domaine public)
pour la composition `carte`. À lancer une seule fois ; le résultat est versionné.

  curl -sS -o /tmp/countries-50m.json https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-50m.json
  python3 -I scripts/build_france_map.py /tmp/countries-50m.json motion/assets/france.json

Projection : Mercator. Le JSON contient le tracé (viewBox 0 0 1000 H) et les paramètres
pour placer un point (lat, lon) avec la même formule côté HTML.
"""
import json, math, sys

src, out = sys.argv[1], sys.argv[2]
topo = json.load(open(src))
sx, sy = topo["transform"]["scale"]
tx, ty = topo["transform"]["translate"]

def decode(arc):
    x = y = 0
    pts = []
    for dx, dy in arc:
        x += dx; y += dy
        pts.append((x * sx + tx, y * sy + ty))
    return pts

arcs = [decode(a) for a in topo["arcs"]]

def ring(idx_list):
    pts = []
    for i in idx_list:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(a if not pts else a[1:])
    return pts

fr = next(g for g in topo["objects"]["countries"]["geometries"] if g.get("properties", {}).get("name") == "France")
polys = fr["arcs"] if fr["type"] == "MultiPolygon" else [fr["arcs"]]
LON = (-5.5, 10.0); LAT = (41.0, 51.5)  # métropole + Corse
rings = []
for poly in polys:
    outer = ring(poly[0])
    lons = [p[0] for p in outer]; lats = [p[1] for p in outer]
    if LON[0] <= sum(lons) / len(lons) <= LON[1] and LAT[0] <= sum(lats) / len(lats) <= LAT[1]:
        rings.append(outer)

merc = lambda lat: math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
allp = [p for r in rings for p in r]
lon_min = min(p[0] for p in allp); lon_max = max(p[0] for p in allp)
y_top = merc(max(p[1] for p in allp)); y_bot = merc(min(p[1] for p in allp))
k = 1000 / (lon_max - lon_min)
H = round((y_top - y_bot) * k, 1)

def proj(lon, lat):
    return ((lon - lon_min) * k, (y_top - merc(lat)) * k)

d = []
for r in rings:
    pts = [proj(*p) for p in r]
    d.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")

json.dump({"source": "Natural Earth 1:50m via world-atlas@2.0.2 (public domain)",
           "viewBox": [0, 0, 1000, H], "path": "".join(d),
           "projection": {"type": "mercator", "lonMin": lon_min, "yTop": y_top, "k": k}},
          open(out, "w"))
print(f"✓ {out}: {len(rings)} contours, viewBox 1000x{H}, {len(''.join(d))//1024} Ko")
