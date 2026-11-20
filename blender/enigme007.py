"""ÉNIGME 007 — « Chambre 312 » : façade de l'hôtel (complet), couloir du 3e, la porte ouverte
(Mme Laurent face à l'homme à la rose), et les 2 portraits.
blender -b --python blender/enigme007.py [-- hotel couloir porte laurent homme]
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
import toonkit as tk  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dossiers", "ENIGME-007", "images")
os.makedirs(OUT, exist_ok=True)


def texte(corps, loc, taille, mat, rot=(math.radians(90), 0, 0), extrude=0.01):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    t = bpy.context.object
    t.data.body = corps; t.data.size = taille; t.data.extrude = extrude
    t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'
    t.data.materials.append(mat)
    # pas de contour Freestyle sur les textes (sinon les lettres sont noyées sous le trait)
    col = bpy.data.collections.get('sans_trait')
    if col is None:
        col = bpy.data.collections.new('sans_trait'); bpy.context.scene.collection.children.link(col)
        for ls in bpy.context.scene.view_layers[0].freestyle_settings.linesets:
            ls.select_by_collection = True; ls.collection = col; ls.collection_negation = 'EXCLUSIVE'
    for c in t.users_collection:
        c.objects.unlink(t)
    col.objects.link(t)
    return t


# ------------------------------------------------------------------ PERSONNAGES (réutilisés dans la scène et en portrait)
def laurent(x=0.0, y=0.0, rz=0.0):
    """Mme Laurent : dame élégante en robe de chambre violette, bigoudis, collier de perles, caniche… en peluche."""
    r = tk.empty('laurent', (x, y, 0)); r.rotation_euler[2] = math.radians(rz)
    skin = tk.toon('peau_l', (0.96, 0.8, 0.7)); robe = tk.toon('robe_chambre', (0.5, 0.3, 0.62))
    for s in (-1, 1):
        tk.limb('jambe', (s * 0.1, 0, 0.5), (s * 0.1, 0, 0.1), 0.07, skin, r)
        tk.sph('chausson', (s * 0.1, -0.07, 0.06), 0.11, tk.toon('chausson_rose', (0.95, 0.6, 0.7)), (1, 1.6, 0.6), r)
    tk.cyl('robe', (0, 0, 0.98), 0.45, 1.0, robe, parent=r, r2=0.3)
    tk.box('ceinture', (0, -0.35, 1.05), (0.55, 0.04, 0.07), tk.toon('ceinture_or', (0.85, 0.68, 0.3)), r)
    tk.sph('epaules', (0, 0, 1.47), 0.33, robe, (1.15, 0.85, 0.45), r)
    tk.cyl('cou', (0, 0, 1.56), 0.07, 0.13, skin, parent=r)
    for k in range(9):  # collier de perles
        a = math.radians(-70 + k * 17.5)
        tk.sph('perle', (0.15 * math.sin(a), -0.13 * math.cos(a) - 0.05, 1.53 - 0.04 * math.cos(a)), 0.025, tk.toon('perle', (0.98, 0.96, 0.92)), parent=r)
    tk.face(r, 1.82, skin, eyes_scale=1.2, brows=(-14, 14), head_r=0.31)
    tk.sph('cheveux', (0, 0.05, 1.9), 0.33, tk.toon('cheveux_blond', (0.92, 0.82, 0.55)), (1.03, 1.0, 0.92), r)
    for k in range(5):  # bigoudis roses
        a = math.radians(-60 + k * 30)
        tk.cyl('bigoudi', (0.28 * math.sin(a), 0.05, 1.95 + 0.25 * math.cos(a)), 0.06, 0.16, tk.toon('bigoudi', (0.95, 0.45, 0.6)),
               rot=(0, math.radians(90), a), parent=r)
    tk.limb('bras', (0.33, 0, 1.47), (0.4, -0.2, 1.15), 0.065, robe, r)
    tk.sph('main', (0.42, -0.22, 1.12), 0.06, skin, parent=r)
    tk.limb('bras2', (-0.33, 0, 1.47), (-0.42, -0.1, 1.05), 0.065, robe, r)
    tk.sph('main2', (-0.43, -0.11, 1.0), 0.06, skin, parent=r)
    # caniche en peluche sous le bras
    blanc = tk.toon('caniche', (0.98, 0.97, 0.95))
    tk.sph('caniche', (0.5, -0.3, 1.18), 0.13, blanc, parent=r)
    tk.sph('caniche_tete', (0.6, -0.36, 1.3), 0.09, blanc, parent=r)
    return r


def homme(x=0.0, y=0.0, rz=0.0, frappe=False):
    """L'homme à la rose : costume bleu nuit, rose rouge à la boutonnière, montre dorée, fine moustache."""
    r = tk.empty('homme', (x, y, 0)); r.rotation_euler[2] = math.radians(rz)
    skin = tk.toon('peau_h', (0.9, 0.72, 0.6)); costume = tk.toon('costume_nuit', (0.14, 0.18, 0.32))
    noir = tk.toon('noir', (0.06, 0.06, 0.07))
    for s in (-1, 1):
        tk.limb('jambe', (s * 0.12, 0, 0.9), (s * 0.12, 0, 0.1), 0.085, costume, r)
        tk.sph('chaussure', (s * 0.12, -0.07, 0.06), 0.1, tk.toon('vernis', (0.05, 0.04, 0.04)), (1, 1.7, 0.55), r)
    tk.cyl('veste', (0, 0, 1.25), 0.3, 0.75, costume, parent=r, r2=0.35)
    tk.sph('epaules', (0, 0, 1.6), 0.35, costume, (1.15, 0.75, 0.35), r)
    tk.box('chemise', (0, -0.3, 1.48), (0.16, 0.04, 0.26), tk.toon('chemise_bl', (0.96, 0.96, 0.97)), r)
    tk.box('noeud', (0, -0.33, 1.58), (0.14, 0.03, 0.06), noir, r)
    rose = tk.toon('rose', (0.85, 0.08, 0.15))
    tk.sph('rose', (-0.18, -0.33, 1.5), 0.055, rose, parent=r)
    tk.sph('feuille', (-0.15, -0.32, 1.44), 0.03, tk.toon('tige', (0.2, 0.5, 0.2)), (1.5, 1, 0.6), r)
    tk.cyl('cou', (0, 0, 1.68), 0.08, 0.14, skin, parent=r)
    tk.face(r, 1.95, skin, eyes_scale=0.95, brows=(-6, 16), smirk=True, head_r=0.3)
    tk.sph('cheveux', (0, 0.06, 2.03), 0.31, tk.toon('gomina2', (0.12, 0.08, 0.06)), (1.02, 1.05, 0.8), r)
    tk.limb('moustache', (-0.1, -0.29, 1.85), (0.1, -0.29, 1.85), 0.018, noir, r)
    tk.limb('bras', (0.36, 0, 1.6), (0.42, -0.02, 1.0), 0.075, costume, r)
    tk.sph('main', (0.42, -0.03, 0.95), 0.06, skin, parent=r)
    if frappe:  # poing gauche levé vers la porte : il vient de frapper
        tk.limb('bras2', (-0.36, 0, 1.6), (-0.7, -0.15, 1.6), 0.075, costume, r)
        tk.sph('poing', (-0.78, -0.17, 1.68), 0.065, skin, parent=r)
        tk.box('montre', (-0.66, -0.15, 1.62), (0.07, 0.07, 0.03), tk.toon('or_montre', (0.9, 0.75, 0.35)), r)
    else:
        tk.limb('bras2', (-0.36, 0, 1.6), (-0.15, -0.3, 1.25), 0.075, costume, r)
        tk.sph('main2', (-0.12, -0.33, 1.25), 0.06, skin, parent=r)
        tk.box('montre', (-0.17, -0.31, 1.28), (0.07, 0.07, 0.03), tk.toon('or_montre', (0.9, 0.75, 0.35)), r)
    return r


# ------------------------------------------------------------------ FAÇADE DE L'HÔTEL, la nuit
def hotel():
    random.seed(3)
    sc = tk.reset(1290, 726, transparent=False)
    sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.1, 0.1, 0.25, 1)
    tk.lights(key=(0.65, 0.7, 1.0), rim=(1.0, 0.75, 0.45), energy=1.8)
    tk.box('ciel', (0, 30, 8), (80, 0.2, 30), tk.toon('ciel_nuit', (0.16, 0.16, 0.38), emit=1.0))
    tk.sph('lune', (8, 29, 11), 1.0, tk.toon('lune', (1, 0.96, 0.85), emit=3))
    facade = tk.toon('facade', (0.85, 0.74, 0.6))
    tk.box('hotel', (0, 6, 4.0), (9, 3, 8.4), facade)
    tk.box('corniche', (0, 4.45, 8.25), (9.4, 0.3, 0.3), tk.toon('corniche', (0.6, 0.45, 0.3)))
    allume = tk.toon('fen_allumee', (1, 0.82, 0.45), emit=2.5); eteint = tk.toon('fen_eteinte', (0.2, 0.22, 0.35))
    for etage in range(5):
        for k in range(6):
            mat = allume if random.random() < 0.85 else eteint
            tk.box('fenetre', (-3.4 + k * 1.36, 4.48, 1.9 + etage * 1.4), (0.7, 0.05, 0.85), mat)
    tk.box('porte', (0, 4.48, 0.7), (1.6, 0.05, 1.4), tk.toon('porte_hall', (1, 0.8, 0.45), emit=2))
    tk.box('auvent', (0, 3.9, 1.55), (2.4, 1.2, 0.12), tk.toon('auvent_rouge', (0.62, 0.12, 0.14)))
    texte("GRAND HÔTEL DU LAC", (0, 4.38, 8.75), 0.55, tk.toon('enseigne', (1, 0.82, 0.4), emit=3))
    tk.box('panneau_complet', (3.0, 4.35, 1.0), (1.5, 0.08, 0.5), tk.toon('panneau', (0.12, 0.1, 0.1)))
    texte("COMPLET", (3.0, 4.28, 1.0), 0.32, tk.toon('complet', (1, 0.2, 0.2), emit=4))
    tk.box('lac', (0, -2, -0.05), (60, 12, 0.1), tk.toon('lac', (0.1, 0.18, 0.38)))
    tk.box('quai', (0, 3.5, 0.0), (60, 2.2, 0.2), tk.toon('quai', (0.45, 0.42, 0.4)))
    for x in (-6.5, 6.5):
        tk.limb('tronc', (x, 4.2, 0), (x, 4.2, 1.6), 0.12, tk.toon('tronc', (0.35, 0.22, 0.12)))
        tk.sph('arbre', (x, 4.2, 2.4), 1.0, tk.toon('feuillage', (0.15, 0.3, 0.2)), (1, 1, 1.2))
    tk.camera((0, -10, 3.6), (0, 4, 4.3), lens=30)
    return sc


# ------------------------------------------------------------------ COULOIR du 3e étage (et la porte ouverte)
def decor_couloir(porte_ouverte=False):
    sc = tk.reset(1290, 726, transparent=False)
    tk.lights(energy=2.6)
    tk.box('mur', (0, 1.0, 2.0), (14, 0.2, 5), tk.toon('papier_couloir', (0.9, 0.78, 0.55)))
    tk.box('plinthe', (0, 0.88, 0.15), (14, 0.06, 0.3), tk.toon('plinthe', (0.45, 0.25, 0.12)))
    tk.box('moquette', (0, -1, -0.02), (14, 4, 0.05), tk.toon('moquette', (0.6, 0.12, 0.15)))
    tk.box('tapis_bord', (0, -0.25, 0.005), (14, 0.08, 0.01), tk.toon('bord_or', (0.85, 0.68, 0.3)))
    bois = tk.toon('porte_bois', (0.48, 0.28, 0.14)); laiton = tk.toon('laiton', (0.88, 0.68, 0.3))
    for num, x in (("311", -3.4), ("312", 0.0), ("313", 3.4)):
        if num == "312" and porte_ouverte:
            tk.box('encadrement', (x, 0.88, 1.1), (1.4, 0.04, 2.3), tk.toon('interieur_chaud', (1, 0.85, 0.6), emit=1.3))
            tk.box('battant', (x - 0.85, 0.35, 1.1), (0.08, 1.1, 2.2), bois)
        else:
            tk.box('porte', (x, 0.86, 1.1), (1.2, 0.08, 2.2), bois, bevel=0.02)
            tk.sph('poignee', (x + 0.45, 0.78, 1.05), 0.05, laiton)
            tk.box('plaque', (x, 0.8, 1.75), (0.45, 0.03, 0.2), laiton)
            texte(num, (x, 0.775, 1.75), 0.15, tk.toon('chiffre', (0.15, 0.08, 0.05)))
        tk.box('applique', (x + 1.7, 0.85, 2.3), (0.18, 0.12, 0.3), tk.toon('applique', (1, 0.85, 0.55), emit=3))
    if porte_ouverte:  # numéro sur le chambranle
        tk.box('plaque', (0.95, 0.8, 1.75), (0.45, 0.03, 0.2), laiton)
        texte("312", (0.95, 0.775, 1.75), 0.15, tk.toon('chiffre', (0.15, 0.08, 0.05)))
    # ascenseur au bout du couloir (droite)
    tk.box('ascenseur', (6.0, 0.86, 1.2), (1.5, 0.08, 2.4), tk.toon('inox', (0.72, 0.74, 0.78)), bevel=0.02)
    tk.box('fente', (6.0, 0.8, 1.2), (0.03, 0.02, 2.3), tk.toon('noir', (0.06, 0.06, 0.07)))
    tk.box('indicateur', (6.0, 0.82, 2.65), (0.5, 0.04, 0.25), tk.toon('noir', (0.06, 0.06, 0.07)))
    texte("3", (6.0, 0.79, 2.65), 0.16, tk.toon('chiffre_lum', (1, 0.6, 0.2), emit=4))
    return sc


def couloir():
    decor_couloir(False)
    tk.camera((0.6, -7.0, 1.6), (0.9, 1.0, 1.3), lens=26)


def porte():
    decor_couloir(True)
    laurent(-0.15, 0.6, 15)
    homme(1.5, -0.5, -30, frappe=True)
    tk.camera((0.6, -6.0, 1.5), (0.6, 0.6, 1.3), lens=32)


def portrait(f):
    tk.reset(600, 1000)
    tk.lights()
    tk.camera((0, -7.2, 1.2), (0, 0, 1.15), lens=88)
    f()


TOUT = {"hotel": hotel, "couloir": couloir, "porte": porte,
        "laurent": lambda: portrait(lambda: laurent(0, 0, -15)), "homme": lambda: portrait(lambda: homme(0, 0, 18))}
noms = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else list(TOUT)
for nom in noms:
    TOUT[nom]()
    bpy.context.scene.render.filepath = os.path.join(OUT, f"{nom}.png")
    bpy.ops.render.render(write_still=True)
    print("Saved", nom)
