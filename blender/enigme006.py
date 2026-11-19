"""ÉNIGME 006 — « L'ombre de midi » : labo du parfumeur, la plage à midi (ombres courtes), la même plage
sur la photo de la photographe (soleil bas, ombres longues), et 3 suspects.
blender -b --python blender/enigme006.py [-- labo plage_midi plage_photo scaphandrier glacier photographe]
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
import toonkit as tk  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dossiers", "ENIGME-006", "images")
os.makedirs(OUT, exist_ok=True)


def soleil(elevation, azimut, energie=3.2):
    bpy.ops.object.light_add(type='SUN'); s = bpy.context.object
    s.rotation_euler = (math.radians(90 - elevation), 0, math.radians(azimut))
    s.data.energy = energie; s.data.color = (1.0, 0.95, 0.86); s.data.angle = math.radians(1.5)
    return s


def palmier(x, y, h=4.2):
    tronc = tk.toon('tronc', (0.55, 0.38, 0.22))
    pts = [(x, y, 0), (x + 0.15, y, h * 0.35), (x + 0.45, y, h * 0.7), (x + 0.8, y, h)]
    for a, b in zip(pts, pts[1:]):
        tk.limb('tronc', a, b, 0.17, tronc, r2=0.14)
    feuille = tk.toon('palme', (0.25, 0.6, 0.25))
    cx, cy, cz = pts[-1]
    for k in range(8):
        a = k / 8 * 2 * math.pi
        o = tk.sph('palme', (cx + 1.0 * math.cos(a), cy + 1.0 * math.sin(a), cz - 0.25), 0.55, feuille, (2.0, 0.45, 0.12))
        o.rotation_euler = (0, math.radians(20), a)
    tk.sph('coco', (cx, cy - 0.15, cz - 0.2), 0.16, tk.toon('coco', (0.4, 0.26, 0.12)))


def parasol(x, y):
    tk.limb('mat', (x, y, 0), (x, y, 2.3), 0.04, tk.toon('mat', (0.9, 0.88, 0.85)))
    tk.cyl('toile', (x, y, 2.35), 1.3, 0.45, tk.toon('toile_rouge', (0.85, 0.2, 0.18)), r2=0.08)
    tk.cyl('bord', (x, y, 2.14), 1.31, 0.06, tk.toon('toile_blanche', (0.97, 0.95, 0.9)))


def plage(elevation, azimut, nom):
    sc = tk.reset(1290, 726, transparent=False)
    sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.6, 0.75, 0.95, 1)
    sc.world.node_tree.nodes['Background'].inputs[1].default_value = 0.12  # peu de lumière ambiante → ombres nettes
    sc.eevee.shadow_cascade_size = '4096'
    soleil(elevation, azimut, 4.5 / max(0.35, math.sin(math.radians(elevation))))  # même éclairement du sable
    tk.box('ciel', (0, 40, 8), (120, 0.2, 30), tk.toon('ciel_fond', (0.55, 0.75, 0.95), emit=1.0))
    tk.box('sable', (0, 4, -0.05), (60, 30, 0.1), tk.toon('sable', (0.95, 0.85, 0.62)))
    tk.box('mer', (0, 14, -0.02), (60, 12, 0.1), tk.toon('mer_ete', (0.2, 0.6, 0.78)))
    tk.box('ecume', (0, 8.05, -0.0), (60, 0.25, 0.1), tk.toon('ecume', (0.97, 0.97, 0.95)))
    palmier(-2.2, 1.0)
    parasol(2.0, 0.6)
    tk.box('serviette', (2.0, -0.4, 0.01), (1.0, 1.9, 0.02), tk.toon('serviette', (0.25, 0.45, 0.8)))
    for k in range(5):
        tk.box('raie', (2.0, -1.2 + k * 0.4, 0.025), (1.0, 0.15, 0.01), tk.toon('raie_blanche', (0.97, 0.97, 0.95)))
    tk.box('seau', (0.4, -0.6, 0.18), (0.3, 0.3, 0.35), tk.toon('seau', (0.95, 0.75, 0.15)), bevel=0.04)
    tk.camera((0.0, -9.5, 2.4), (0.0, 1.0, 1.3), lens=34)
    return sc


def labo():
    sc = tk.reset(1290, 726, transparent=False)
    tk.lights(energy=2.6)
    tk.box('mur', (0, 2.0, 2.0), (12, 0.2, 6), tk.toon('mur_labo', (0.86, 0.8, 0.7)))
    # fenêtre ouverte sur la plage (en haut à droite)
    tk.box('vue_ciel', (2.6, 1.88, 2.9), (2.2, 0.02, 0.9), tk.toon('ciel', (0.55, 0.78, 0.97), emit=0.8))
    tk.box('vue_mer', (2.6, 1.87, 2.35), (2.2, 0.02, 0.35), tk.toon('mer_ete', (0.2, 0.6, 0.78), emit=0.6))
    tk.box('vue_sable', (2.6, 1.86, 1.95), (2.2, 0.02, 0.5), tk.toon('sable_vue', (0.95, 0.85, 0.62), emit=0.6))
    tk.box('cadre', (2.6, 1.9, 2.5), (2.5, 0.05, 1.95), tk.toon('cadre_bleu', (0.2, 0.4, 0.6)))
    bpy.data.objects['cadre'].location.y = 1.95
    # étagères de flacons colorés
    bois = tk.toon('etagere_bois', (0.55, 0.35, 0.2))
    couleurs = [(0.85, 0.3, 0.45), (0.95, 0.7, 0.2), (0.4, 0.7, 0.85), (0.55, 0.35, 0.75), (0.3, 0.7, 0.45)]
    for e, z in enumerate((1.4, 2.3, 3.2)):
        tk.box('etagere', (-2.0, 1.75, z), (3.6, 0.4, 0.08), bois)
        for k in range(9):
            c = couleurs[(k + e) % 5]
            tk.cyl('flacon', (-3.6 + k * 0.4, 1.7, z + 0.22), 0.12, 0.36, tk.toon(f'flacon{(k + e) % 5}', c, emit=0.3))
            tk.cyl('bouchon', (-3.6 + k * 0.4, 1.7, z + 0.45), 0.05, 0.1, tk.toon('or', (0.85, 0.68, 0.3)))
    # paillasse, alambic, flacon renversé et flaque
    tk.box('paillasse', (0.5, 0.5, 0.45), (5.0, 1.6, 0.9), tk.toon('paillasse', (0.3, 0.32, 0.36)))
    tk.box('plan', (0.5, 0.5, 0.92), (5.1, 1.7, 0.06), tk.toon('marbre', (0.92, 0.9, 0.86)))
    verre = tk.toon('verrerie', (0.75, 0.9, 0.95), emit=0.4)
    tk.sph('alambic', (-0.3, 0.7, 1.3), 0.35, verre)
    tk.limb('col', (-0.3, 0.7, 1.6), (0.6, 0.7, 1.9), 0.05, verre)
    tk.cyl('flacon_renverse', (1.4, 0.3, 1.02), 0.12, 0.4, tk.toon('flacon0', couleurs[0], emit=0.3), rot=(0, math.radians(90), math.radians(20)))
    tk.sph('flaque', (1.75, 0.2, 0.955), 0.4, tk.toon('flaque', (0.9, 0.45, 0.6)), (1.4, 1.0, 0.03))
    tk.box('tabouret', (-1.2, -0.6, 0.2), (0.5, 0.5, 0.06), bois, rot=(math.radians(80), 0, math.radians(30)))
    tk.camera((0.0, -6.5, 2.2), (0.2, 1.0, 1.7), lens=30)
    return sc


# ------------------------------------------------------------------ SUSPECTS
def scene_perso():
    tk.reset(600, 1000)
    tk.lights()
    tk.camera((0, -7.2, 1.2), (0, 0, 1.15), lens=88)


def jambes(root, mat, shoe, ecart=0.13, haut=0.75, r=0.085):
    for s in (-1, 1):
        tk.limb('jambe', (s * ecart, 0, haut), (s * ecart, 0, 0.1), r, mat, root)
        tk.sph('chaussure', (s * ecart, -0.07, 0.06), 0.1 + (r - 0.085), shoe, (1, 1.6, 0.55), root)


def scaphandrier():
    scene_perso()
    r = tk.empty('scaphandrier')
    skin = tk.toon('peau_s', (0.88, 0.68, 0.55)); toile = tk.toon('toile_scaph', (0.58, 0.52, 0.42))
    laiton = tk.toon('laiton', (0.85, 0.62, 0.25)); goutte = tk.toon('goutte', (0.45, 0.7, 1.0), emit=1.2)
    jambes(r, toile, tk.toon('plomb', (0.25, 0.25, 0.28)), 0.15, 0.75, 0.12)
    tk.cyl('corps', (0, 0, 1.2), 0.42, 0.95, toile, parent=r, r2=0.4)
    tk.cyl('collerette', (0, 0, 1.68), 0.38, 0.1, laiton, parent=r)
    tk.cyl('cou', (0, 0, 1.76), 0.1, 0.1, skin, parent=r)
    tk.face(r, 1.98, skin, eyes_scale=1.0, brows=(-18, 18), head_r=0.29)
    tk.sph('cheveux', (0, 0.06, 2.08), 0.28, tk.toon('cheveux_mouilles', (0.15, 0.12, 0.1)), (1.04, 1.0, 0.6), r)
    tk.sph('barbe', (0, -0.15, 1.83), 0.2, tk.toon('barbe_rousse', (0.6, 0.3, 0.15)), (1.1, 0.7, 0.6), r)
    # casque de scaphandre en cuivre sous le bras
    tk.limb('bras', (0.42, 0, 1.6), (0.55, -0.1, 1.2), 0.11, toile, r)
    tk.sph('casque', (0.62, -0.25, 1.15), 0.32, laiton, parent=r)
    tk.cyl('hublot', (0.62, -0.56, 1.17), 0.15, 0.04, tk.toon('vitre_casque', (0.6, 0.8, 0.9), emit=0.5), rot=(math.radians(90), 0, 0), parent=r)
    tk.limb('bras2', (-0.42, 0, 1.6), (-0.5, -0.05, 1.05), 0.11, toile, r)
    tk.sph('gant', (-0.5, -0.06, 1.0), 0.09, tk.toon('gant_cuir', (0.35, 0.22, 0.12)), parent=r)
    for (x, z) in ((-0.25, 2.25), (0.22, 2.2), (-0.38, 1.4), (0.3, 0.9), (-0.2, 0.6), (0.45, 1.6)):
        tk.sph('goutte', (x, -0.42, z), 0.035, goutte, (1, 1, 1.6), r)
    tk.sph('flaque', (0, -0.05, 0.01), 0.45, goutte, (1.4, 1, 0.03), r)


def glacier():
    scene_perso()
    r = tk.empty('glacier')
    skin = tk.toon('peau_g', (0.95, 0.76, 0.62)); veste = tk.toon('veste_blanche', (0.97, 0.96, 0.94))
    rouge = tk.toon('rayure_rouge', (0.85, 0.18, 0.2))
    jambes(r, tk.toon('pantalon_bleu', (0.2, 0.25, 0.45)), tk.toon('chaussure_n', (0.1, 0.1, 0.1)), 0.13, 0.7)
    tk.sph('ventre', (0, 0, 1.15), 0.46, veste, (1, 0.9, 1.05), r)
    for z in (0.85, 1.0, 1.15, 1.3):  # tablier rayé
        tk.box('tablier', (0, -0.42, z), (0.55, 0.03, 0.07), rouge, r)
    tk.cyl('cou', (0, 0, 1.6), 0.09, 0.12, skin, parent=r)
    tk.face(r, 1.86, skin, eyes_scale=1.2, brows=(12, -12), head_r=0.32)
    tk.sph('moustache', (0, -0.3, 1.77), 0.12, tk.toon('moustache_n', (0.15, 0.1, 0.08)), (1.5, 0.4, 0.35), r)
    tk.cyl('casquette', (0, 0, 2.1), 0.3, 0.16, veste, parent=r)
    tk.cyl('bande', (0, 0, 2.06), 0.305, 0.06, rouge, parent=r)
    tk.box('visiere', (0, -0.32, 2.03), (0.42, 0.22, 0.03), rouge, r)
    # cornet de glace à la main
    tk.limb('bras', (0.42, 0, 1.45), (0.55, -0.2, 1.3), 0.08, veste, r)
    tk.sph('main', (0.57, -0.22, 1.3), 0.065, skin, parent=r)
    tk.cyl('cornet', (0.57, -0.24, 1.42), 0.09, 0.3, tk.toon('cornet', (0.85, 0.6, 0.3)), parent=r, r2=0.0, rot=(math.radians(180), 0, 0))
    tk.sph('boule1', (0.57, -0.24, 1.6), 0.1, tk.toon('fraise', (0.95, 0.55, 0.65)), parent=r)
    tk.sph('boule2', (0.57, -0.24, 1.75), 0.09, tk.toon('pistache', (0.6, 0.85, 0.5)), parent=r)
    tk.limb('bras2', (-0.42, 0, 1.45), (-0.5, -0.05, 1.0), 0.08, veste, r)
    tk.sph('main2', (-0.5, -0.06, 0.95), 0.065, skin, parent=r)


def photographe():
    scene_perso()
    r = tk.empty('photographe')
    skin = tk.toon('peau_p', (0.8, 0.58, 0.45)); gilet = tk.toon('gilet_kaki', (0.62, 0.58, 0.38))
    noir = tk.toon('noir', (0.06, 0.06, 0.07))
    jambes(r, tk.toon('short', (0.85, 0.8, 0.68)), tk.toon('sandale', (0.5, 0.32, 0.18)), 0.11, 0.6)
    for s in (-1, 1):
        tk.limb('mollet', (s * 0.11, 0, 0.6), (s * 0.11, 0, 0.15), 0.075, skin, r)
    tk.cyl('corps', (0, 0, 1.15), 0.28, 0.9, tk.toon('tshirt', (0.95, 0.93, 0.88)), parent=r, r2=0.3)
    tk.cyl('gilet', (0, 0, 1.2), 0.3, 0.75, gilet, parent=r, r2=0.31)
    for x in (-0.14, 0.14):
        tk.box('poche', (x, -0.3, 1.05), (0.14, 0.03, 0.14), tk.toon('poche_k', (0.55, 0.5, 0.32)), r)
    tk.sph('epaules', (0, 0, 1.6), 0.3, gilet, (1.15, 0.8, 0.4), r)
    tk.cyl('cou', (0, 0, 1.68), 0.07, 0.12, skin, parent=r)
    tk.face(r, 1.93, skin, eyes_scale=1.0, brows=(-8, 8), smirk=True, head_r=0.29)
    tk.sph('cheveux', (0, 0.12, 1.85), 0.3, tk.toon('cheveux_boucles', (0.1, 0.07, 0.05)), (1.15, 0.9, 1.1), r)
    for s in (-1, 1):  # lunettes de soleil remontées
        tk.box('lunette', (s * 0.11, -0.27, 2.08), (0.14, 0.03, 0.08), noir, r)
    paille = tk.toon('paille_chapeau', (0.92, 0.82, 0.55))
    tk.cyl('bord_chapeau', (0, 0, 2.15), 0.6, 0.03, paille, parent=r)
    tk.cyl('chapeau', (0, 0, 2.27), 0.27, 0.22, paille, parent=r, r2=0.24)
    tk.cyl('ruban', (0, 0, 2.2), 0.275, 0.05, tk.toon('ruban_rouge', (0.75, 0.15, 0.15)), parent=r)
    # appareil photo autour du cou, montré fièrement
    tk.limb('sangle', (-0.18, -0.22, 1.62), (0, -0.36, 1.3), 0.015, noir, r)
    tk.limb('sangle2', (0.18, -0.22, 1.62), (0, -0.36, 1.3), 0.015, noir, r)
    tk.box('appareil', (0, -0.42, 1.25), (0.36, 0.16, 0.24), noir, r, bevel=0.03)
    tk.cyl('objectif', (0, -0.55, 1.24), 0.08, 0.15, tk.toon('objectif', (0.2, 0.2, 0.22)), rot=(math.radians(90), 0, 0), parent=r)
    tk.cyl('lentille', (0, -0.63, 1.24), 0.06, 0.01, tk.toon('lentille', (0.4, 0.6, 0.8), emit=0.8), rot=(math.radians(90), 0, 0), parent=r)
    for s in (-1, 1):
        tk.limb('bras', (s * 0.3, 0, 1.6), (s * 0.22, -0.35, 1.3), 0.06, skin, r)


TOUT = {"labo": labo, "plage_midi": lambda: plage(80, 20, "midi"), "plage_photo": lambda: plage(30, -80, "photo"),
        "scaphandrier": scaphandrier, "glacier": glacier, "photographe": photographe}
noms = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else list(TOUT)
for nom in noms:
    TOUT[nom]()
    if nom in ("scaphandrier", "glacier", "photographe"):
        bpy.data.objects[nom].rotation_euler[2] = math.radians({"scaphandrier": -18, "glacier": 15, "photographe": -20}[nom])
    bpy.context.scene.render.filepath = os.path.join(OUT, f"{nom}.png")
    bpy.ops.render.render(write_still=True)
    print("Saved", nom)
