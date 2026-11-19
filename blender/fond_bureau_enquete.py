"""Fond GÉNÉRIQUE réutilisable (toutes les énigmes) : le bureau d'enquête de DOSSIER 00, la nuit.
Mur de liège avec photos, post-it, carte et fils rouges ; bureau avec lampe allumée, dossiers, loupe, café.
Rendu vertical 1080×1920 → bibliotheque/fonds/bureau-enquete.png
blender -b --python blender/fond_bureau_enquete.py
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
import toonkit as tk  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bibliotheque", "fonds", "bureau-enquete.png")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
random.seed(4)

sc = tk.reset(1080, 1920, transparent=False)
sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.05, 0.05, 0.07, 1)
tk.lights(key=(1.0, 0.86, 0.66), rim=(0.55, 0.65, 1.0), energy=1.6)

Y = 3.0  # plan du mur
# ------------------------------------------------------------------ mur, lambris, fenêtre à stores
tk.box('mur', (0, Y + 0.1, 3.5), (12, 0.2, 10), tk.toon('mur', (0.33, 0.2, 0.15)))
tk.box('lambris', (0, Y - 0.02, 0.6), (12, 0.12, 1.6), tk.toon('lambris', (0.26, 0.14, 0.09)))
tk.box('fenetre', (-3.05, Y - 0.03, 4.6), (1.5, 0.05, 3.2), tk.toon('nuit', (0.2, 0.32, 0.6), emit=0.9))
store = tk.toon('store', (0.85, 0.76, 0.58))
for k in range(16):
    tk.box('lame', (-3.05, Y - 0.08, 3.1 + k * 0.2), (1.5, 0.03, 0.09), store, rot=(math.radians(25), 0, 0))
tk.box('cadre_fen', (-3.05, Y - 0.06, 4.6), (1.7, 0.04, 3.4), tk.toon('cadre_fen', (0.2, 0.12, 0.08)))
bpy.data.objects['cadre_fen'].location.y = Y - 0.0  # derrière la vitre

# ------------------------------------------------------------------ tableau de liège
tk.box('cadre_liege', (0.15, Y - 0.06, 4.75), (4.5, 0.08, 3.9), tk.toon('cadre_liege', (0.32, 0.19, 0.1)))
tk.box('liege', (0.15, Y - 0.11, 4.75), (4.2, 0.04, 3.6), tk.toon('liege', (0.74, 0.54, 0.33)))
yb = Y - 0.14  # surface du liège

blanc = tk.toon('polaroid', (0.97, 0.95, 0.9))
photos = [tk.toon(f'photo{i}', c) for i, c in enumerate([(0.25, 0.32, 0.45), (0.35, 0.28, 0.25), (0.22, 0.3, 0.26), (0.4, 0.36, 0.44)])]
silh = tk.toon('silhouette', (0.08, 0.08, 0.1))
punaise = tk.toon('punaise', (0.75, 0.1, 0.1))
pins = []


def epingle(x, z):
    tk.sph('punaise', (x, yb - 0.07, z), 0.055, punaise)
    pins.append((x, z))


def polaroid(x, z, ang, photo, personne=True):
    rot = (0, math.radians(ang), 0)
    tk.box('polaroid', (x, yb - 0.01, z), (0.72, 0.02, 0.86), blanc, rot=rot)
    tk.box('photo', (x, yb - 0.025, z + 0.06), (0.6, 0.02, 0.6), photo, rot=rot)
    if personne:  # silhouette anonyme (tête + épaules)
        tk.sph('tete', (x, yb - 0.04, z + 0.13), 0.1, silh, (1, 0.3, 1.15))
        tk.sph('epaules', (x, yb - 0.04, z - 0.12), 0.22, silh, (1, 0.3, 0.55))
    epingle(x, z + 0.38)


def postit(x, z, ang, couleur=(0.98, 0.86, 0.35)):
    tk.box('postit', (x, yb - 0.015, z), (0.42, 0.015, 0.42), tk.toon(f'postit{couleur}', couleur), rot=(0, math.radians(ang), 0))
    for k in range(3):
        tk.box('ecriture', (x - 0.02, yb - 0.026, z + 0.1 - k * 0.09), (0.28 - k * 0.05, 0.01, 0.02), silh, rot=(0, math.radians(ang), 0))
    epingle(x, z + 0.16)


def coupure(x, z, ang):  # coupure de journal
    tk.box('journal', (x, yb - 0.012, z), (0.9, 0.015, 0.62), tk.toon('journal', (0.9, 0.87, 0.78)), rot=(0, math.radians(ang), 0))
    tk.box('titre', (x, yb - 0.022, z + 0.2), (0.75, 0.01, 0.08), silh, rot=(0, math.radians(ang), 0))
    for k in range(4):
        tk.box('ligne', (x, yb - 0.022, z + 0.05 - k * 0.09), (0.75, 0.01, 0.025), tk.toon('gris', (0.45, 0.43, 0.4)), rot=(0, math.radians(ang), 0))
    epingle(x - 0.3, z + 0.24)


# carte au centre
tk.box('carte', (0.25, yb - 0.008, 4.55), (1.4, 0.012, 1.0), tk.toon('carte', (0.86, 0.82, 0.66)))
for k in range(5):
    tk.limb('route', (-0.4 + k * 0.05, yb - 0.02, 4.1 + k * 0.2), (0.9 - k * 0.1, yb - 0.02, 4.35 + k * 0.12), 0.012, tk.toon('route', (0.55, 0.45, 0.3)))
tk.cyl('lac', (0.6, yb - 0.02, 4.75), 0.18, 0.01, tk.toon('lac', (0.45, 0.62, 0.8)), rot=(math.radians(90), 0, 0))
tk.cyl('cible', (0.0, yb - 0.025, 4.45), 0.09, 0.01, punaise, rot=(math.radians(90), 0, 0))
epingle(0.0, 4.45)

polaroid(-1.35, 5.85, 4, photos[0])
polaroid(1.6, 5.9, -5, photos[1])
polaroid(-1.4, 3.75, -3, photos[2])
polaroid(1.55, 3.7, 6, photos[3], personne=False)
postit(0.2, 6.2, 3)
postit(-0.5, 3.3, -6, (0.95, 0.6, 0.55))
postit(1.05, 3.25, 5)
coupure(-0.55, 5.4, -2)
coupure(1.05, 5.3, 4)

# fils rouges entre les punaises (le réseau d'enquête)
fil = tk.toon('fil_rouge', (0.9, 0.12, 0.1), emit=1.6)
for a, b in ((0, 4), (4, 1), (0, 2), (2, 6), (6, 9), (9, 3), (1, 10), (10, 3), (5, 9), (8, 0), (7, 9)):
    if a < len(pins) and b < len(pins):
        (x1, z1), (x2, z2) = pins[a], pins[b]
        tk.limb('fil', (x1, yb - 0.09, z1), (x2, yb - 0.09, z2), 0.03, fil)

# ------------------------------------------------------------------ bureau
bois = tk.toon('bureau', (0.45, 0.26, 0.13))
tk.box('plateau', (0, 0.6, 1.55), (6.5, 3.6, 0.16), bois, bevel=0.03)
tk.box('sous_main', (0.3, 0.3, 1.64), (2.4, 1.5, 0.02), tk.toon('sous_main', (0.14, 0.26, 0.2)))
laiton = tk.toon('laiton', (0.85, 0.66, 0.3))
# lampe de banquier ALLUMÉE
tk.box('socle', (-1.7, 1.6, 1.68), (0.7, 0.4, 0.1), laiton, bevel=0.02)
tk.cyl('tige', (-1.7, 1.6, 2.0), 0.04, 0.6, laiton)
tk.cyl('abat', (-1.7, 1.4, 2.35), 0.26, 1.0, tk.toon('abat', (0.15, 0.45, 0.25)), rot=(0, math.radians(90), 0))
tk.box('ampoule', (-1.7, 1.28, 2.24), (0.8, 0.06, 0.06), tk.toon('ampoule', (1, 0.85, 0.5), emit=8))
bpy.ops.object.light_add(type='POINT', location=(-1.7, 1.1, 2.0)); l = bpy.context.object
l.data.energy = 260; l.data.color = (1, 0.72, 0.38)
# piles de dossiers « confidentiels »
kraft = tk.toon('kraft', (0.86, 0.68, 0.38)); rouge = tk.toon('tampon', (0.62, 0.12, 0.12))
for i, (x, y) in enumerate(((1.6, 1.2), (2.2, 0.9))):
    for k in range(4 - i):
        tk.box('dossier', (x + random.uniform(-0.05, 0.05), y, 1.7 + k * 0.07), (1.1, 0.8, 0.06), kraft,
               rot=(0, 0, math.radians(random.uniform(-8, 8))))
    tk.box('bande', (x, y - 0.2, 1.71 + (4 - i) * 0.07), (0.7, 0.14, 0.01), rouge, rot=(0, 0, math.radians(-12)))
# dossier ouvert avec photo
tk.box('ouvert', (0.3, 0.1, 1.67), (1.5, 1.0, 0.02), kraft, rot=(0, 0, math.radians(-4)))
tk.box('feuille', (0.6, 0.1, 1.69), (0.7, 0.9, 0.01), blanc, rot=(0, 0, math.radians(-4)))
tk.box('photo_dossier', (-0.05, 0.15, 1.69), (0.5, 0.6, 0.01), photos[0], rot=(0, 0, math.radians(3)))
# loupe
tk.limb('manche', (1.1, -0.45, 1.68), (1.6, -0.9, 1.68), 0.05, tk.toon('manche', (0.25, 0.13, 0.07)))
bpy.ops.mesh.primitive_torus_add(major_radius=0.3, minor_radius=0.04, location=(0.85, -0.2, 1.68))
bpy.context.object.data.materials.append(laiton)
tk.cyl('verre_loupe', (0.85, -0.2, 1.68), 0.28, 0.01, tk.toon('verre_loupe', (0.75, 0.88, 1.0), emit=0.4))
# tasse de café
tk.cyl('tasse', (-0.9, 0.0, 1.8), 0.18, 0.3, tk.toon('tasse', (0.9, 0.88, 0.82)))
tk.cyl('cafe', (-0.9, 0.0, 1.95), 0.16, 0.01, tk.toon('cafe', (0.25, 0.14, 0.08)))
bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.025, location=(-0.7, 0.0, 1.8), rotation=(math.radians(90), 0, 0))
bpy.context.object.data.materials.append(tk.toon('tasse', (0.9, 0.88, 0.82)))
# téléphone à cadran
tk.box('tel', (-2.3, 0.0, 1.75), (0.8, 0.6, 0.25), tk.toon('bakelite', (0.1, 0.1, 0.11)), bevel=0.06)
tk.limb('combine', (-2.6, -0.05, 1.98), (-2.0, -0.05, 1.98), 0.07, tk.toon('bakelite', (0.1, 0.1, 0.11)))
# ampoule suspendue au plafond
tk.limb('fil_plafond', (0.9, 1.6, 9.0), (0.9, 1.6, 7.45), 0.015, silh)
tk.cyl('suspension', (0.9, 1.6, 7.3), 0.45, 0.35, tk.toon('suspension', (0.18, 0.2, 0.2)), r2=0.08)
tk.sph('ampoule_plafond', (0.9, 1.6, 7.1), 0.12, tk.toon('ampoule', (1, 0.85, 0.5), emit=8))
bpy.ops.object.light_add(type='POINT', location=(0.9, 1.4, 6.8)); l2 = bpy.context.object
l2.data.energy = 380; l2.data.color = (1, 0.8, 0.5)

tk.camera((0.0, -6.0, 3.9), (0.0, Y, 3.75), lens=38)
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("Saved fond")
