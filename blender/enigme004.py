"""ÉNIGME 004 — « La panne » : indices (pendule électrique, bureau) + 3 suspects en 3D toon.
blender -b --python blender/enigme004.py [-- pendule bureau cuisiniere neveu jardinier]
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
import toonkit as tk  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dossiers", "ENIGME-004", "images")
os.makedirs(OUT, exist_ok=True)


def verre_mat():
    """Verre transparent légèrement bleuté (transparence EEVEE)."""
    m = bpy.data.materials.new('verre'); m.use_nodes = True; m.blend_method = 'BLEND'
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); em = nt.nodes.new('ShaderNodeEmission')
    em.inputs[0].default_value = (0.85, 0.93, 1.0, 1); em.inputs[1].default_value = 0.6
    mix = nt.nodes.new('ShaderNodeMixShader'); mix.inputs[0].default_value = 0.22
    nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], out.inputs[0])
    return m


def aiguille(cx, cz, y, ang_deg, long, larg, mat):
    a = math.radians(ang_deg)
    return tk.limb('aiguille', (cx, y, cz), (cx + long * math.sin(a), y, cz + long * math.cos(a)), larg, mat)


# ------------------------------------------------------------------ PENDULE ÉLECTRIQUE arrêtée à 21 h 40
def pendule():
    sc = tk.reset(1290, 726, transparent=False)
    tk.lights(energy=2.6)
    papier = tk.toon('papier_peint', (0.2, 0.36, 0.3))
    tk.box('mur', (0, 0.2, 1.5), (10, 0.2, 6), papier)
    for x in (-3.2, -1.6, 1.6, 3.2):  # rayures du papier peint
        tk.box('rayure', (x, 0.09, 1.5), (0.12, 0.02, 6), tk.toon('rayure_or', (0.55, 0.45, 0.25)))
    tk.box('lambris', (0, 0.05, -1.0), (10, 0.15, 1.6), tk.toon('lambris', (0.36, 0.2, 0.12)))
    bois, ivoire, noir = tk.toon('bois_pendule', (0.45, 0.26, 0.13)), tk.toon('cadran', (0.97, 0.93, 0.84)), tk.toon('noir', (0.06, 0.06, 0.07))
    cx, cz = 0, 1.6
    tk.cyl('boitier', (cx, 0.0, cz), 1.25, 0.25, bois, rot=(math.radians(90), 0, 0))
    tk.cyl('cadran', (cx, -0.13, cz), 1.08, 0.02, ivoire, rot=(math.radians(90), 0, 0))
    for k in range(60):
        a = math.radians(k * 6); r1 = 0.98; r0 = 0.84 if k % 5 == 0 else 0.93
        tk.limb('graduation', (cx + r0 * math.sin(a), -0.15, cz + r0 * math.cos(a)), (cx + r1 * math.sin(a), -0.15, cz + r1 * math.cos(a)),
                0.025 if k % 5 == 0 else 0.008, noir)
    aiguille(cx, cz, -0.17, (9 + 40 / 60) * 30, 0.55, 0.045, noir)  # heures : entre 9 et 10
    aiguille(cx, cz, -0.19, 40 * 6, 0.82, 0.03, noir)               # minutes : 40
    tk.sph('axe', (cx, -0.2, cz), 0.06, tk.toon('laiton', (0.85, 0.66, 0.3)))
    # câble électrique qui descend jusqu'à la prise murale (l'indice discret)
    cable = tk.toon('cable', (0.1, 0.1, 0.1))
    pts = [(0.35, -0.02, cz - 1.22), (0.45, -0.02, 0.0), (0.5, -0.02, -0.55), (0.9, -0.02, -0.7)]
    for a, b in zip(pts, pts[1:]):
        tk.limb('cable', a, b, 0.025, cable)
    tk.box('prise', (1.05, -0.02, -0.72), (0.38, 0.06, 0.38), tk.toon('prise', (0.92, 0.9, 0.86)), bevel=0.03)
    tk.box('fiche', (0.95, -0.08, -0.72), (0.16, 0.08, 0.2), tk.toon('fiche', (0.15, 0.15, 0.16)), bevel=0.02)
    # lumière froide d'orage depuis la gauche
    tk.camera((0.3, -7.5, 1.0), (0.3, 0, 1.0), lens=33)
    return sc


# ------------------------------------------------------------------ BUREAU : bougies, lampe éteinte, verre
def bureau():
    sc = tk.reset(1290, 726, transparent=False)
    sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.08, 0.06, 0.06, 1)
    tk.lights(key=(1.0, 0.85, 0.65), energy=2.3)
    bpy.ops.object.light_add(type='POINT', location=(-1.1, -0.4, 1.6)); bpy.context.object.data.energy = 120
    bpy.context.object.data.color = (1, 0.7, 0.35)
    tk.box('mur', (0, 1.6, 1.5), (10, 0.2, 5), tk.toon('mur_bibli', (0.3, 0.17, 0.12)))
    for i in range(16):  # dos de livres au fond
        h = 0.5 + (i * 37 % 7) * 0.05
        tk.box('livre', (-3.6 + i * 0.48, 1.45, 1.35 + h / 2), (0.4, 0.3, h),
               tk.toon(f'livre{i % 4}', [(0.55, 0.12, 0.12), (0.15, 0.3, 0.22), (0.18, 0.22, 0.4), (0.6, 0.45, 0.2)][i % 4]))
    tk.box('etagere', (0, 1.45, 1.33), (8, 0.4, 0.06), tk.toon('etagere', (0.32, 0.18, 0.1)))
    tk.box('plateau', (0, 0, 0.0), (7, 3.2, 0.2), tk.toon('chene', (0.5, 0.3, 0.15)), bevel=0.03)
    tk.box('sous_main', (0.6, 0.1, 0.11), (2.2, 1.4, 0.02), tk.toon('cuir_vert', (0.14, 0.28, 0.2)))
    # bougies (bien entamées) dans des bougeoirs en laiton, flammes allumées
    laiton = tk.toon('laiton', (0.85, 0.66, 0.3)); cire = tk.toon('cire', (0.96, 0.92, 0.82))
    flamme = tk.toon('flamme', (1.0, 0.78, 0.3), emit=6)
    for x, y, h in ((-2.1, 0.2, 0.42), (-1.65, -0.15, 0.28), (-1.25, 0.35, 0.36)):
        tk.cyl('bougeoir', (x, y, 0.16), 0.2, 0.08, laiton)
        tk.cyl('pied', (x, y, 0.3), 0.06, 0.24, laiton)
        tk.cyl('cire', (x, y, 0.42 + h / 2), 0.075, h, cire)
        tk.sph('coulure', (x + 0.06, y - 0.03, 0.42 + h * 0.6), 0.03, cire, (1, 1, 2.2))
        tk.cyl('flamme', (x, y, 0.42 + h + 0.09), 0.04, 0.16, flamme, r2=0.0)
    # lampe de banquier ÉTEINTE (abat-jour vert, câble branché)
    vert = tk.toon('abat_jour', (0.15, 0.42, 0.24))
    tk.box('socle', (-0.45, 0.45, 0.16), (0.7, 0.4, 0.1), laiton, bevel=0.02)
    tk.cyl('tige', (-0.45, 0.45, 0.5), 0.04, 0.6, laiton)
    tk.cyl('abat', (-0.45, 0.25, 0.85), 0.26, 1.0, vert, rot=(0, math.radians(90), 0))
    tk.limb('bras_lampe', (-0.45, 0.45, 0.8), (-0.45, 0.25, 0.85), 0.035, laiton)
    tk.box('ampoule_eteinte', (-0.45, 0.13, 0.74), (0.6, 0.05, 0.05), tk.toon('ampoule', (0.7, 0.7, 0.65)))
    tk.limb('cable_lampe', (-0.1, 0.5, 0.12), (1.6, 1.1, 0.12), 0.02, tk.toon('cable', (0.1, 0.1, 0.1)))
    tk.limb('cable_lampe2', (1.6, 1.1, 0.12), (2.0, 1.3, -0.2), 0.02, tk.toon('cable', (0.1, 0.1, 0.1)))
    # machine à écrire stylisée
    tk.box('machine', (0.75, 0.3, 0.25), (1.1, 0.7, 0.28), tk.toon('machine', (0.12, 0.12, 0.14)), bevel=0.05)
    tk.box('feuille', (0.75, 0.6, 0.55), (0.8, 0.02, 0.5), tk.toon('feuille', (0.97, 0.95, 0.9)), rot=(math.radians(-15), 0, 0))
    # verre de whisky : liquide ambré + 3 PIERRES À WHISKY grises (elles ne fondent jamais)
    gx, gy = 1.6, -0.55
    tk.cyl('whisky', (gx, gy, 0.24), 0.3, 0.2, tk.toon('whisky', (0.8, 0.45, 0.12)))
    pierre = tk.toon('pierre_whisky', (0.5, 0.5, 0.55))
    for dx, dy, rz in ((-0.08, -0.06, 15), (0.1, 0.0, 40), (-0.02, 0.11, 70)):
        tk.box('pierre', (gx + dx * 1.2, gy + dy * 1.2, 0.38), (0.16, 0.16, 0.16), pierre, bevel=0.012, rot=(0.2, 0.3, math.radians(rz)))
    for dx, dy, dz in ((-0.11, -0.12, 0.47), (0.12, -0.06, 0.47), (0.03, 0.06, 0.48)):  # mouchetures du granit
        tk.sph('moucheture', (gx + dx * 1.2, gy + dy * 1.2, dz), 0.016, tk.toon('noir', (0.06, 0.06, 0.07)))
    tk.cyl('verre', (gx, gy, 0.3), 0.33, 0.4, verre_mat())
    tk.camera((-0.1, -4.6, 3.1), (-0.1, 0.0, 0.35), lens=32)
    return sc


# ------------------------------------------------------------------ SUSPECTS
def scene_perso():
    tk.reset(600, 1000)
    tk.lights()
    tk.camera((0, -7.2, 1.2), (0, 0, 1.15), lens=88)


def jambes(root, mat, shoe, ecart=0.13, haut=0.75):
    for s in (-1, 1):
        tk.limb('jambe', (s * ecart, 0, haut), (s * ecart, 0, 0.1), 0.085, mat, root)
        tk.sph('chaussure', (s * ecart, -0.07, 0.06), 0.1, shoe, (1, 1.6, 0.55), root)


def cuisiniere():
    scene_perso()
    r = tk.empty('cuisiniere')
    skin = tk.toon('peau_c', (0.96, 0.78, 0.66))
    robe = tk.toon('robe_bordeaux', (0.45, 0.12, 0.2)); tablier = tk.toon('tablier', (0.97, 0.96, 0.93))
    jambes(r, tk.toon('bas', (0.3, 0.25, 0.25)), tk.toon('sabot', (0.25, 0.15, 0.1)), 0.12, 0.55)
    tk.cyl('robe', (0, 0, 0.95), 0.48, 1.0, robe, parent=r, r2=0.33)
    tk.box('tablier', (0, -0.36, 0.9), (0.5, 0.04, 0.85), tablier, r, bevel=0.03)
    tk.box('poche', (0, -0.39, 0.75), (0.24, 0.02, 0.16), tk.toon('poche', (0.85, 0.3, 0.3)), r)
    tk.sph('epaules', (0, 0, 1.45), 0.36, robe, (1.15, 0.85, 0.45), r)
    tk.cyl('cou', (0, 0, 1.55), 0.08, 0.14, skin, parent=r)
    tk.face(r, 1.82, skin, eyes_scale=1.1, brows=(-12, 12), head_r=0.33)
    for s in (-1, 1):
        tk.sph('joue', (s * 0.17, -0.26, 1.74), 0.06, tk.toon('joue', (0.95, 0.55, 0.5)), (1, 0.5, 0.7), r)
    hair = tk.toon('cheveux_gris', (0.75, 0.72, 0.7))
    tk.sph('cheveux', (0, 0.05, 1.9), 0.35, hair, (1.03, 1.0, 0.92), r)
    tk.sph('chignon', (0, 0.15, 2.2), 0.17, hair, parent=r)
    # plateau avec une bouteille de whisky
    tk.limb('bras', (0.36, 0, 1.45), (0.5, -0.2, 1.15), 0.075, robe, r)
    tk.limb('bras2', (-0.36, 0, 1.45), (-0.5, -0.2, 1.15), 0.075, robe, r)
    tk.box('plateau', (0, -0.42, 1.12), (1.05, 0.4, 0.04), tk.toon('argent', (0.8, 0.8, 0.82)), r, bevel=0.01)
    tk.cyl('bouteille', (0.2, -0.42, 1.35), 0.08, 0.4, tk.toon('bouteille', (0.6, 0.35, 0.1)), parent=r)
    tk.cyl('goulot', (0.2, -0.42, 1.62), 0.03, 0.15, tk.toon('bouteille', (0.6, 0.35, 0.1)), parent=r)
    tk.box('etiquette', (0.2, -0.505, 1.33), (0.12, 0.01, 0.12), tablier, r)


def neveu():
    scene_perso()
    r = tk.empty('neveu')
    skin = tk.toon('peau_n', (0.92, 0.74, 0.62))
    imper = tk.toon('imper_jaune', (0.93, 0.74, 0.18)); jean = tk.toon('jean', (0.2, 0.28, 0.45))
    jambes(r, jean, tk.toon('basket', (0.9, 0.9, 0.9)), 0.12, 0.8)
    tk.cyl('imper', (0, 0, 1.15), 0.36, 0.9, imper, parent=r, r2=0.3)
    tk.sph('epaules', (0, 0, 1.58), 0.32, imper, (1.15, 0.8, 0.4), r)
    tk.cyl('cou', (0, 0, 1.66), 0.08, 0.12, skin, parent=r)
    tk.face(r, 1.92, skin, eyes_scale=1.35, brows=(15, -15), head_r=0.31)
    tk.sph('cheveux_mouilles', (0, 0.06, 2.02), 0.3, tk.toon('cheveux_noirs', (0.1, 0.08, 0.07)), (1.05, 1.0, 0.75), r)
    goutte = tk.toon('goutte', (0.45, 0.7, 1.0), emit=1.2)
    for (x, z) in ((-0.22, 2.2), (0.25, 2.15), (0.32, 1.55), (-0.4, 1.3), (0.42, 0.95), (-0.35, 0.8)):
        tk.sph('goutte', (x, -0.32, z), 0.035, goutte, (1, 1, 1.6), r)
    # parapluie fermé qui dégouline
    tk.limb('bras', (0.34, 0, 1.6), (0.45, -0.1, 1.15), 0.07, imper, r)
    tk.sph('main', (0.46, -0.11, 1.1), 0.06, skin, parent=r)
    tk.cyl('parapluie', (0.5, -0.12, 0.65), 0.1, 0.9, tk.toon('parapluie', (0.12, 0.12, 0.2)), parent=r, r2=0.02)
    tk.cyl('manche', (0.47, -0.11, 1.18), 0.025, 0.18, tk.toon('manche', (0.4, 0.22, 0.1)), parent=r)
    tk.sph('flaque', (0.45, -0.1, 0.01), 0.3, goutte, (1.3, 1, 0.04), r)
    tk.limb('bras2', (-0.34, 0, 1.6), (-0.4, -0.05, 1.1), 0.07, imper, r)
    tk.sph('main2', (-0.4, -0.06, 1.05), 0.06, skin, parent=r)


def jardinier():
    scene_perso()
    r = tk.empty('jardinier')
    skin = tk.toon('peau_j', (0.85, 0.64, 0.5))
    salopette = tk.toon('salopette', (0.25, 0.42, 0.25)); chemise = tk.toon('chemise_carreaux', (0.75, 0.3, 0.22))
    jambes(r, salopette, tk.toon('botte', (0.2, 0.25, 0.15)), 0.13, 0.8)
    tk.cyl('chemise', (0, 0, 1.3), 0.34, 0.6, chemise, parent=r)
    tk.cyl('salopette', (0, 0, 1.0), 0.37, 0.55, salopette, parent=r)
    tk.box('bavette', (0, -0.33, 1.3), (0.38, 0.04, 0.35), salopette, r)
    for s in (-1, 1):
        tk.limb('bretelle', (s * 0.15, -0.34, 1.45), (s * 0.18, -0.1, 1.62), 0.025, salopette, r)
    tk.sph('epaules', (0, 0, 1.6), 0.34, chemise, (1.15, 0.8, 0.4), r)
    tk.cyl('cou', (0, 0, 1.68), 0.09, 0.12, skin, parent=r)
    tk.face(r, 1.93, skin, eyes_scale=0.95, brows=(5, -5), head_r=0.32)
    tk.sph('barbe', (0, -0.12, 1.78), 0.3, tk.toon('barbe', (0.55, 0.4, 0.25)), (1, 0.8, 0.7), r)
    paille = tk.toon('paille', (0.9, 0.78, 0.45))
    tk.cyl('bord_chapeau', (0, 0, 2.17), 0.55, 0.04, paille, parent=r)
    tk.cyl('chapeau', (0, 0, 2.3), 0.3, 0.26, paille, parent=r, r2=0.26)
    tk.cyl('ruban', (0, 0, 2.22), 0.305, 0.06, tk.toon('ruban', (0.5, 0.15, 0.12)), parent=r)
    # râteau
    tk.limb('bras', (0.38, 0, 1.6), (0.48, -0.1, 1.15), 0.08, chemise, r)
    tk.sph('main', (0.49, -0.12, 1.1), 0.065, skin, parent=r)
    bois = tk.toon('manche_bois', (0.55, 0.35, 0.18))
    tk.limb('manche', (0.5, -0.12, 0.1), (0.5, -0.12, 2.0), 0.03, bois, r)
    tk.box('tete_rateau', (0.5, -0.12, 2.02), (0.5, 0.06, 0.06), tk.toon('metal', (0.5, 0.5, 0.55)), r)
    for k in range(6):
        tk.limb('dent', (0.29 + k * 0.084, -0.12, 2.0), (0.29 + k * 0.084, -0.12, 2.12), 0.012, tk.toon('metal', (0.5, 0.5, 0.55)), r)
    tk.limb('bras2', (-0.38, 0, 1.6), (-0.42, -0.05, 1.1), 0.08, chemise, r)
    tk.sph('main2', (-0.42, -0.06, 1.05), 0.065, skin, parent=r)


TOUT = {"pendule": pendule, "bureau": bureau, "cuisiniere": cuisiniere, "neveu": neveu, "jardinier": jardinier}
noms = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else list(TOUT)
for nom in noms:
    TOUT[nom]()
    if nom in ("cuisiniere", "neveu", "jardinier"):
        bpy.data.objects[nom].rotation_euler[2] = math.radians(-20 if nom != "neveu" else 18)
    bpy.context.scene.render.filepath = os.path.join(OUT, f"{nom}.png")
    bpy.ops.render.render(write_still=True)
    print("Saved", nom)
