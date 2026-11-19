"""ÉNIGME 005 — « L'évasion de Roc-Noir » : l'île-prison + les 3 évadés (funambule, nageur, mime).
blender -b --python blender/enigme005.py [-- ile funambule nageur mime]
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
import toonkit as tk  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dossiers", "ENIGME-005", "images")
os.makedirs(OUT, exist_ok=True)
ORANGE = (0.93, 0.5, 0.16)


# ------------------------------------------------------------------ L'ÎLE-PRISON, la nuit
def ile():
    random.seed(11)
    sc = tk.reset(1290, 726, transparent=False)
    sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.1, 0.13, 0.28, 1)
    tk.lights(key=(0.6, 0.7, 1.0), rim=(1.0, 0.75, 0.45), energy=2.0)
    mer = tk.toon('mer', (0.12, 0.27, 0.5))
    tk.box('mer', (0, 10, -0.05), (80, 60, 0.1), mer)
    # côte au loin (droite) avec maisons éclairées
    cote = tk.toon('cote', (0.25, 0.32, 0.24))
    for k in range(6):  # collines de la côte
        tk.sph('cote', (15.5 + (k % 2) * 1.5, 2 + k * 4.5, -0.3), 3.2, cote, (1.2, 1.3, 0.45))
    for k in range(7):
        tk.box('maison', (13.2 + random.uniform(0, 1), 4 + k * 2.6, 1.2), (0.6, 0.6, 0.6), tk.toon('maison', (0.75, 0.68, 0.6)))
        tk.box('fenetre', (12.88, 4 + k * 2.6, 1.25), (0.05, 0.2, 0.2), tk.toon('lueur', (1, 0.8, 0.4), emit=4))
    # LA CHAUSSÉE SUBMERSIBLE : rochers à fleur d'eau + bande d'eau plus claire (peu profonde)
    roche = tk.toon('rocher', (0.42, 0.4, 0.38))
    for k in range(26):
        t = k / 25
        x, y = -0.6 + t * 12.6, 7.0 - t * 1.6
        tk.sph('rocher', (x + random.uniform(-0.2, 0.2), y + random.uniform(-0.15, 0.15), -0.06), random.uniform(0.12, 0.22), roche, (1.4, 1, 0.45))
    # île rocheuse
    tk.sph('ile', (-3.5, 8, -0.6), 3.4, tk.toon('roc', (0.38, 0.34, 0.3)), (1.4, 1.1, 0.42))
    # murs d'enceinte
    mur = tk.toon('mur_prison', (0.62, 0.6, 0.56))
    for (x, y, sx, sy) in ((-3.5, 6.0, 5.6, 0.25), (-3.5, 10.0, 5.6, 0.25), (-6.2, 8.0, 0.25, 4.0), (-0.8, 8.0, 0.25, 4.0)):
        tk.box('mur', (x, y, 1.6), (sx, sy, 1.4), mur)
    # bâtiment des cellules (fenêtres à barreaux)
    tk.box('cellules', (-4.4, 8.4, 2.0), (2.8, 2.0, 2.2), tk.toon('cellules', (0.7, 0.66, 0.6)))
    for k in range(5):
        for z in (1.6, 2.4):
            tk.box('fen_cell', (-5.5 + k * 0.55, 7.38, z), (0.22, 0.04, 0.3), tk.toon('lueur', (1, 0.8, 0.4), emit=4))
    # mirador + projecteur et son faisceau
    tk.cyl('mirador', (-1.2, 6.4, 2.4), 0.25, 3.0, mur)
    tk.box('cabine', (-1.2, 6.4, 4.1), (0.9, 0.9, 0.6), tk.toon('cabine', (0.5, 0.48, 0.45)))
    tk.box('toit', (-1.2, 6.4, 4.5), (1.1, 1.1, 0.12), tk.toon('toit', (0.25, 0.2, 0.18)))
    tk.sph('projecteur', (-0.85, 6.1, 4.05), 0.14, tk.toon('lampe', (1, 0.95, 0.75), emit=8))
    faisceau = bpy.data.materials.new('faisceau'); faisceau.use_nodes = True; faisceau.blend_method = 'BLEND'
    nt = faisceau.node_tree; nt.nodes.clear(); o = nt.nodes.new('ShaderNodeOutputMaterial')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); em = nt.nodes.new('ShaderNodeEmission')
    em.inputs[0].default_value = (1, 0.92, 0.6, 1); em.inputs[1].default_value = 1.5
    mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs[0].default_value = 0.25
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o.inputs[0])
    tk.limb('faisceau', (-0.85, 6.1, 4.05), (-3.6, 7.3, 0.6), 0.05, faisceau, r2=0.9)
    # câble électrique tendu entre les cellules et le mirador (le chemin du funambule)
    tk.limb('cable', (-3.1, 7.6, 3.2), (-1.2, 6.4, 3.9), 0.025, tk.toon('cable', (0.08, 0.08, 0.08)))
    tk.sph('lune', (8, 40, 14), 1.2, tk.toon('lune', (1, 0.96, 0.85), emit=3))
    tk.camera((3.8, -5.8, 3.8), (2.6, 8.0, 1.0), lens=23)
    return sc


# ------------------------------------------------------------------ LES 3 ÉVADÉS
def scene_perso():
    tk.reset(600, 1000)
    tk.lights()
    tk.camera((0, -7.2, 1.2), (0, 0, 1.15), lens=88)


def jambes(root, mat, shoe, ecart=0.13, haut=0.75):
    for s in (-1, 1):
        tk.limb('jambe', (s * ecart, 0, haut), (s * ecart, 0, 0.1), 0.085, mat, root)
        tk.sph('chaussure', (s * ecart, -0.07, 0.06), 0.1, shoe, (1, 1.6, 0.55), root)


def numero(root, z, mat):
    tk.box('matricule', (0.12, -0.31, z), (0.18, 0.02, 0.1), tk.toon('matricule', (0.97, 0.95, 0.9)), root)
    tk.box('chiffres', (0.12, -0.325, z), (0.13, 0.01, 0.03), mat, root)


def funambule():
    scene_perso()
    r = tk.empty('funambule')
    skin = tk.toon('peau_f', (0.95, 0.8, 0.68)); combi = tk.toon('combi_orange', ORANGE); noir = tk.toon('noir', (0.06, 0.06, 0.07))
    jambes(r, combi, tk.toon('chausson_cuir', (0.9, 0.85, 0.75)), 0.09, 0.85)
    tk.cyl('corps', (0, 0, 1.25), 0.24, 0.8, combi, parent=r, r2=0.27)
    tk.sph('epaules', (0, 0, 1.62), 0.27, combi, (1.15, 0.8, 0.4), r)
    numero(r, 1.4, noir)
    tk.cyl('cou', (0, 0, 1.7), 0.07, 0.12, skin, parent=r)
    tk.face(r, 1.95, skin, eyes_scale=1.0, brows=(-10, 10), smirk=True, head_r=0.28)
    tk.sph('cheveux', (0, 0.05, 2.06), 0.27, noir, (1.02, 1.0, 0.7), r)
    for s in (-1, 1):  # moustache en guidon
        tk.limb('moustache', (0, -0.27, 1.85), (s * 0.17, -0.25, 1.9), 0.022, noir, r)
        tk.sph('pointe', (s * 0.17, -0.25, 1.92), 0.025, noir, parent=r)
    # bras écartés tenant la longue perche d'équilibre
    for s in (-1, 1):
        tk.limb('bras', (s * 0.27, 0, 1.62), (s * 0.55, -0.15, 1.45), 0.06, combi, r)
        tk.sph('main', (s * 0.57, -0.17, 1.44), 0.055, skin, parent=r)
    tk.limb('perche', (-1.4, -0.17, 1.38), (1.4, -0.17, 1.5), 0.025, tk.toon('perche', (0.85, 0.75, 0.5)), r)


def nageur():
    scene_perso()
    r = tk.empty('nageur')
    skin = tk.toon('peau_na', (0.86, 0.66, 0.52)); combi = tk.toon('combi_orange', ORANGE); noir = tk.toon('noir', (0.06, 0.06, 0.07))
    jambes(r, combi, skin, 0.15, 0.75)
    tk.cyl('corps', (0, 0, 1.2), 0.42, 0.9, combi, parent=r, r2=0.36)
    tk.sph('epaules', (0, 0, 1.62), 0.42, combi, (1.25, 0.8, 0.45), r)
    numero(r, 1.42, noir)
    tk.cyl('cou', (0, 0, 1.72), 0.12, 0.12, skin, parent=r)
    tk.face(r, 1.98, skin, eyes_scale=0.95, brows=(-15, 15), head_r=0.3)
    tk.sph('bonnet', (0, 0.03, 2.05), 0.31, tk.toon('bonnet_bain', (0.2, 0.45, 0.85)), (1.02, 1.02, 0.85), r)
    for s in (-1, 1):  # lunettes de natation remontées sur le front
        tk.cyl('lunette', (s * 0.1, -0.27, 2.12), 0.07, 0.05, tk.toon('verre_lunette', (0.3, 0.8, 0.85), emit=0.5), rot=(math.radians(90), 0, 0), parent=r)
    tk.limb('elastique', (-0.17, -0.25, 2.12), (0.17, -0.25, 2.12), 0.015, noir, r)
    # gros bras musclés, manches retroussées
    for s in (-1, 1):
        tk.limb('biceps', (s * 0.5, 0, 1.6), (s * 0.62, -0.05, 1.2), 0.12, skin, r)
        tk.sph('muscle', (s * 0.56, -0.05, 1.42), 0.14, skin, parent=r)
        tk.limb('avbras', (s * 0.62, -0.05, 1.2), (s * 0.6, -0.12, 0.95), 0.1, skin, r)
        tk.sph('poing', (s * 0.6, -0.13, 0.9), 0.1, skin, parent=r)


def mime():
    scene_perso()
    r = tk.empty('mime')
    blanc = tk.toon('fard', (0.97, 0.96, 0.94)); combi = tk.toon('combi_orange', ORANGE); noir = tk.toon('noir', (0.06, 0.06, 0.07))
    jambes(r, combi, noir, 0.11, 0.8)
    tk.cyl('corps', (0, 0, 1.22), 0.27, 0.85, tk.toon('marin_blanc', (0.95, 0.95, 0.95)), parent=r, r2=0.29)
    for z in (0.92, 1.05, 1.18, 1.31, 1.44):  # marinière
        tk.cyl('rayure', (0, 0, z), 0.285 + (z - 0.8) * 0.02, 0.05, noir, parent=r)
    tk.cyl('ceinture', (0, 0, 0.82), 0.3, 0.12, combi, parent=r)
    tk.sph('epaules', (0, 0, 1.62), 0.28, tk.toon('marin_blanc', (0.95, 0.95, 0.95)), (1.15, 0.8, 0.4), r)
    tk.cyl('cou', (0, 0, 1.7), 0.07, 0.12, blanc, parent=r)
    tk.face(r, 1.95, blanc, eyes_scale=1.3, brows=(20, -20), head_r=0.29)
    for s in (-1, 1):  # larmes noires peintes
        tk.box('larme', (s * 0.11, -0.27, 1.86), (0.025, 0.01, 0.08), noir, r)
    tk.sph('levres', (0, -0.27, 1.83), 0.05, tk.toon('rouge_levres', (0.8, 0.1, 0.12)), (1.2, 0.5, 0.5), r)
    tk.cyl('beret', (0.04, 0.02, 2.2), 0.3, 0.08, noir, parent=r, rot=(0, math.radians(-12), 0))
    tk.sph('queue_beret', (0.06, 0.02, 2.27), 0.03, noir, parent=r)
    gant = tk.toon('gant', (0.98, 0.98, 0.97))
    # geste du mime : mains à plat contre une vitre invisible
    for s in (-1, 1):
        tk.limb('bras', (s * 0.28, 0, 1.62), (s * 0.4, -0.25, 1.75), 0.06, tk.toon('marin_blanc', (0.95, 0.95, 0.95)), r)
        tk.box('main', (s * 0.42, -0.33, 1.8), (0.16, 0.04, 0.2), gant, r, bevel=0.03)


TOUT = {"ile": ile, "funambule": funambule, "nageur": nageur, "mime": mime}
noms = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else list(TOUT)
for nom in noms:
    TOUT[nom]()
    if nom != "ile":
        bpy.data.objects[nom].rotation_euler[2] = math.radians({"funambule": -15, "nageur": 18, "mime": -22}[nom])
    bpy.context.scene.render.filepath = os.path.join(OUT, f"{nom}.png")
    bpy.ops.render.render(write_still=True)
    print("Saved", nom)
