"""ÉNIGME 003 — les 3 suspects en 3D toon, rendus un par un sur fond transparent.
blender -b --python blender/suspects_003.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
import toonkit as tk  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dossiers", "ENIGME-003", "images")
os.makedirs(OUT, exist_ok=True)


def scene():
    tk.reset(600, 1000)
    tk.lights()
    tk.camera((0, -7.2, 1.2), (0, 0, 1.15), lens=88)


def jambes(root, mat, shoe, ecart=0.13, haut=0.75):
    for s in (-1, 1):
        tk.limb('jambe', (s * ecart, 0, haut), (s * ecart, 0, 0.1), 0.085, mat, root)
        tk.sph('chaussure', (s * ecart, -0.07, 0.06), 0.1, shoe, (1, 1.6, 0.55), root)


def soeur():
    scene()
    r = tk.empty('soeur')
    skin = tk.toon('peau1', (0.96, 0.8, 0.68))
    coat = tk.toon('manteau_rouge', (0.62, 0.12, 0.14))
    hair = tk.toon('cheveux_bruns', (0.25, 0.14, 0.08))
    jambes(r, tk.toon('collant', (0.15, 0.13, 0.15)), tk.toon('bottine', (0.12, 0.08, 0.06)), 0.11, 0.6)
    tk.cyl('manteau', (0, 0, 1.0), 0.42, 1.1, coat, parent=r, r2=0.27)
    tk.sph('epaules', (0, 0, 1.52), 0.3, coat, (1.1, 0.8, 0.45), r)
    tk.cyl('cou', (0, 0, 1.6), 0.08, 0.16, skin, parent=r)
    tk.face(r, 1.86, skin, eyes_scale=1.25, brows=(-22, 22))
    tk.sph('cheveux', (0, 0.05, 1.92), 0.34, hair, (1.02, 1.0, 0.95), r)
    tk.sph('chignon', (0, 0.22, 2.12), 0.15, hair, parent=r)
    # bras droit : téléphone à l'oreille ; bras gauche serré contre elle
    tk.limb('bras', (0.3, 0, 1.5), (0.42, -0.05, 1.2), 0.07, coat, r)
    tk.limb('avbras', (0.42, -0.05, 1.2), (0.3, -0.12, 1.8), 0.06, coat, r)
    tk.sph('main', (0.3, -0.13, 1.83), 0.06, skin, parent=r)
    tk.box('telephone', (0.31, -0.15, 1.86), (0.05, 0.03, 0.17), tk.toon('tel', (0.08, 0.08, 0.1)), r, bevel=0.01)
    tk.limb('bras2', (-0.3, 0, 1.5), (-0.33, -0.05, 1.05), 0.07, coat, r)
    tk.sph('main2', (-0.33, -0.06, 1.0), 0.06, skin, parent=r)
    for z in (1.35, 1.15, 0.95):
        tk.sph('bouton', (0, -0.33 if z > 1.2 else -0.36, z), 0.03, tk.toon('or', (0.85, 0.68, 0.3)), parent=r)


def voisin():
    scene()
    r = tk.empty('voisin')
    skin = tk.toon('peau2', (0.93, 0.76, 0.66))
    pyj = tk.toon('pyjama', (0.45, 0.62, 0.86))
    rayure = tk.toon('rayure', (0.96, 0.96, 0.98))
    jambes(r, pyj, tk.toon('chausson', (0.55, 0.3, 0.2)), 0.14, 0.7)
    tk.sph('ventre', (0, 0, 1.1), 0.45, pyj, (1, 0.9, 1.05), r)
    for z in (0.8, 0.95, 1.1, 1.25, 1.4):
        rr = (0.45 ** 2 - ((z - 1.1) / 1.05) ** 2) ** 0.5 * 1.005
        tk.cyl('rayure', (0, 0, z), rr + 0.004, 0.035, rayure, parent=r)
    tk.cyl('cou', (0, 0, 1.55), 0.09, 0.12, skin, parent=r)
    tk.face(r, 1.82, skin, eyes_scale=1.45, brows=(8, -8), tired=True, head_r=0.34)
    tk.sph('moustache', (0, -0.31, 1.73), 0.12, tk.toon('gris', (0.85, 0.85, 0.85)), (1.3, 0.4, 0.35), r)
    # bonnet de nuit tombant + pompon
    bon = tk.toon('bonnet', (0.45, 0.62, 0.86))
    tk.cyl('bonnet', (0.0, 0.03, 2.12), 0.33, 0.4, bon, parent=r, r2=0.05)
    tk.sph('pompon', (0.02, 0.05, 2.34), 0.08, rayure, parent=r)
    tk.cyl('revers', (0, 0.02, 1.98), 0.345, 0.07, rayure, parent=r)
    # jumelles sur la poitrine
    noir = tk.toon('jumelles', (0.12, 0.12, 0.13))
    for s in (-1, 1):
        tk.cyl('jumelle', (s * 0.08, -0.47, 1.3), 0.055, 0.17, noir, rot=(math.radians(90), 0, 0), parent=r)
    tk.limb('sangle', (-0.1, -0.4, 1.33), (0, -0.12, 1.6), 0.012, noir, r)
    tk.limb('sangle2', (0.1, -0.4, 1.33), (0, -0.12, 1.6), 0.012, noir, r)
    for s in (-1, 1):
        tk.limb('bras', (s * 0.42, 0, 1.4), (s * 0.5, -0.1, 1.0), 0.08, pyj, r)
        tk.sph('main', (s * 0.5, -0.12, 0.95), 0.065, skin, parent=r)
    tk.cyl('tasse', (0.5, -0.2, 1.0), 0.06, 0.12, tk.toon('tasse', (0.95, 0.9, 0.8)), parent=r)


def associe():
    scene()
    r = tk.empty('associe')
    skin = tk.toon('peau3', (0.9, 0.72, 0.6))
    suit = tk.toon('costume', (0.25, 0.26, 0.3))
    jambes(r, suit, tk.toon('cuir_noir', (0.06, 0.05, 0.05)), 0.12, 0.9)
    tk.cyl('veste', (0, 0, 1.25), 0.3, 0.75, suit, parent=r, r2=0.36)
    tk.sph('epaules', (0, 0, 1.6), 0.36, suit, (1.15, 0.75, 0.35), r)
    tk.box('chemise', (0, -0.3, 1.48), (0.16, 0.04, 0.26), tk.toon('chemise', (0.96, 0.96, 0.97)), r)
    tk.box('cravate', (0, -0.33, 1.42), (0.06, 0.02, 0.32), tk.toon('cravate', (0.7, 0.1, 0.12)), r)
    tk.cyl('cou', (0, 0, 1.68), 0.08, 0.14, skin, parent=r)
    tk.face(r, 1.95, skin, eyes_scale=0.9, brows=(-5, 18), smirk=True, head_r=0.3)
    tk.sph('cheveux', (0, 0.06, 2.03), 0.31, tk.toon('gomina', (0.06, 0.05, 0.05)), (1.02, 1.05, 0.8), r)
    tk.limb('bras', (0.38, 0, 1.6), (0.42, -0.02, 1.0), 0.075, suit, r)
    tk.sph('main', (0.42, -0.03, 0.95), 0.06, skin, parent=r)
    tk.box('mallette', (0.47, -0.02, 0.72), (0.12, 0.5, 0.38), tk.toon('mallette', (0.42, 0.24, 0.12)), r, bevel=0.02)
    tk.box('poignee', (0.47, -0.02, 0.94), (0.03, 0.14, 0.05), tk.toon('or2', (0.85, 0.68, 0.3)), r)
    tk.limb('bras2', (-0.38, 0, 1.6), (-0.15, -0.3, 1.25), 0.075, suit, r)
    tk.sph('main2', (-0.12, -0.33, 1.25), 0.06, skin, parent=r)
    tk.box('montre', (-0.17, -0.31, 1.27), (0.07, 0.07, 0.03), tk.toon('or3', (0.9, 0.75, 0.35)), r)


for nom, f in (("soeur", soeur), ("voisin", voisin), ("associe", associe)):
    f()
    root = bpy.data.objects[nom]
    root.rotation_euler[2] = math.radians(-22 if nom != "voisin" else 18)  # trois-quarts
    bpy.context.scene.render.filepath = os.path.join(OUT, f"{nom}.png")
    bpy.ops.render.render(write_still=True)
    print("Saved", nom)
