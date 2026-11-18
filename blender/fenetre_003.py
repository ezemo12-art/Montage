"""ÉNIGME 003 — la fenêtre du salon vue du jardin, la nuit : vitre brisée, éclats de verre sur la pelouse.
blender -b --python blender/fenetre_003.py
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
import toonkit as tk  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dossiers", "ENIGME-003", "images", "jardin.png")
random.seed(7)

sc = tk.reset(1290, 726, transparent=False)
sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.05, 0.07, 0.16, 1)
sc.world.node_tree.nodes['Background'].inputs[1].default_value = 1.0
tk.lights(key=(0.55, 0.65, 1.0), rim=(1.0, 0.7, 0.35), energy=1.3)
sc.render.line_thickness = 1.3  # lune bleutée + lumière chaude

mur = tk.toon('mur', (0.62, 0.52, 0.46))
bois = tk.toon('cadre', (0.36, 0.2, 0.12))
herbe = tk.toon('herbe', (0.24, 0.42, 0.22))
interieur = tk.toon('interieur', (1.0, 0.72, 0.35), emit=1.6)
verre = tk.toon('verre', (0.8, 0.93, 1.0), emit=1.7)
rideau = tk.toon('rideau', (0.58, 0.1, 0.12))

# façade + sol
tk.box('facade', (0, 0.3, 2.0), (12, 0.4, 5.0), mur)
tk.box('pelouse', (0, -4, -0.05), (16, 9, 0.1), herbe)
tk.box('soubassement', (0, 0.05, 0.25), (12, 0.12, 0.5), tk.toon('pierre', (0.5, 0.47, 0.44)))
# fenêtre : ouverture lumineuse, cadre, croisillons
tk.box('lumiere', (0, 0.12, 2.0), (2.4, 0.05, 2.2), interieur)
for x in (-1.25, 1.25):
    tk.box('montant', (x, 0.05, 2.0), (0.14, 0.2, 2.5), bois)
for z in (0.82, 3.18):
    tk.box('traverse', (0, 0.05, z), (2.64, 0.2, 0.14), bois)
tk.box('croisillon_v', (0, 0.05, 2.0), (0.08, 0.16, 2.3), bois)
tk.box('croisillon_h', (0, 0.05, 2.0), (2.4, 0.16, 0.08), bois)
tk.box('appui', (0, -0.12, 0.72), (2.9, 0.4, 0.12), tk.toon('pierre2', (0.62, 0.58, 0.54)))
for x in (-0.95, 0.95):  # rideaux rouges vus de l'extérieur
    tk.box('rideau', (x, 0.14, 2.0), (0.42, 0.04, 2.2), rideau)

# vitres : 3 carreaux intacts (légers reflets) + 1 carreau brisé (morceaux restés dans le cadre)
reflet = tk.toon('reflet', (0.55, 0.7, 0.95), emit=0.25)
for cx, cz in ((-0.62, 2.6), (0.62, 2.6), (0.62, 1.4)):
    tk.box('vitre', (cx, 0.0, cz), (1.12, 0.02, 1.08), reflet)
for k in range(5):  # dents de verre sur les bords du carreau bas gauche
    a = k / 5 * 2 * math.pi
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.16, depth=0.01,
                                    location=(-0.62 + 0.45 * math.cos(a), -0.01, 1.4 + 0.42 * math.sin(a)),
                                    rotation=(math.radians(90), a + math.pi, 0))
    o = bpy.context.object; o.scale = (1, 1.9, 1); o.data.materials.append(verre)

# ÉCLATS DE VERRE SUR LA PELOUSE (dehors) : l'indice
for i in range(46):
    r = random.uniform(0.2, 2.2)
    a = random.uniform(-1.2, 1.2)
    x = -0.62 + r * math.sin(a) * 0.9
    y = -0.4 - r * math.cos(a)
    s = random.uniform(0.07, 0.14)
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=s, depth=0.01, location=(x, y, 0.04),
                                    rotation=(0, 0, random.uniform(0, 6.28)))
    bpy.context.object.data.materials.append(verre)

# buissons et arbre en silhouette
feuille = tk.toon('buisson', (0.16, 0.3, 0.18))
for x, s in ((-3.2, 0.9), (-4.3, 0.7), (3.3, 0.85), (4.4, 1.0)):
    tk.sph('buisson', (x, -0.5, s * 0.7), s, feuille, (1.2, 0.8, 0.9))
tk.sph('lune', (4.6, 6, 6.2), 0.5, tk.toon('lune', (1, 0.96, 0.85), emit=3))

tk.camera((0.4, -8.6, 3.0), (-0.2, -0.4, 1.3), lens=36)
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("Saved jardin")
