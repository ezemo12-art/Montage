"""DOSSIER 00 — kit Blender headless (EEVEE, cel-shading) : personnages et décors low-poly.
D'après le skill blender-video-3d. Usage : blender -b --python script.py
"""
import math

import bpy
from mathutils import Vector

_mats = {}


def reset(w=600, h=1000, transparent=True):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _mats.clear()  # les matériaux de la scène précédente n'existent plus
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE'
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.eevee.taa_render_samples = 16
    sc.eevee.use_gtao = True
    sc.eevee.use_soft_shadows = True
    sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.render.film_transparent = transparent
    sc.render.use_freestyle = True  # contour dessiné autour des formes (look illustré)
    sc.render.line_thickness_mode = 'ABSOLUTE'; sc.render.line_thickness = 2.2
    ls = sc.view_layers[0].freestyle_settings.linesets.new('contour')
    ls.select_by_visibility = True; ls.select_by_edge_types = True
    ls.select_silhouette = True; ls.select_border = True; ls.select_crease = False
    ls.linestyle = bpy.data.linestyles.new('trait')
    ls.linestyle.color = (0.06, 0.05, 0.06); ls.linestyle.thickness = 2.4
    for autre in sc.view_layers[0].freestyle_settings.linesets:  # jeux de lignes par défaut sans style
        if autre.linestyle is None:
            autre.linestyle = ls.linestyle
    w_ = bpy.data.worlds.new('W'); sc.world = w_; w_.use_nodes = True
    w_.node_tree.nodes['Background'].inputs[0].default_value = (0.9, 0.88, 0.84, 1)
    w_.node_tree.nodes['Background'].inputs[1].default_value = 0.6
    return sc




def lin(c):
    return tuple(x ** 2.2 for x in c)


def toon(name, color, emit=0.0):
    """Matériau cel-shadé (couleur sRGB 0–1)."""
    if name in _mats:
        return _mats[name]
    color = lin(color)
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    if emit:
        e = nt.nodes.new('ShaderNodeEmission'); e.inputs[0].default_value = (*color, 1); e.inputs[1].default_value = emit
        nt.links.new(e.outputs[0], out.inputs[0])
    else:
        d = nt.nodes.new('ShaderNodeBsdfDiffuse')
        s2r = nt.nodes.new('ShaderNodeShaderToRGB')
        ramp = nt.nodes.new('ShaderNodeValToRGB')
        cr = ramp.color_ramp; cr.interpolation = 'EASE'
        cr.elements[0].position = 0.0; cr.elements[0].color = (0.40, 0.37, 0.46, 1)
        cr.elements[1].position = 0.45; cr.elements[1].color = (1, 1, 1, 1)
        mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
        mix.inputs[0].default_value = 1.0; mix.inputs[7].default_value = (*color, 1)
        em = nt.nodes.new('ShaderNodeEmission')
        nt.links.new(d.outputs[0], s2r.inputs[0]); nt.links.new(s2r.outputs[0], ramp.inputs[0])
        nt.links.new(ramp.outputs[0], mix.inputs[6]); nt.links.new(mix.outputs[2], em.inputs[0])
        nt.links.new(em.outputs[0], out.inputs[0])
    _mats[name] = m
    return m


def _fin(o, name, mat, parent):
    o.name = name
    o.data.materials.clear(); o.data.materials.append(mat)
    if parent:
        o.parent = parent
    bpy.ops.object.shade_smooth()
    return o


def box(name, loc, size, mat, parent=None, bevel=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        b = o.modifiers.new('bev', 'BEVEL'); b.width = bevel; b.segments = 3
    return _fin(o, name, mat, parent)


def sph(name, loc, r, mat, scale=(1, 1, 1), parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=24, ring_count=16)
    o = bpy.context.object; o.scale = scale
    return _fin(o, name, mat, parent)


def cyl(name, loc, r, depth, mat, rot=(0, 0, 0), parent=None, r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=r, depth=depth, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=20, radius1=r, radius2=r2, depth=depth, location=loc, rotation=rot)
    return _fin(bpy.context.object, name, mat, parent)


def limb(name, a, b, r, mat, parent=None, r2=None):
    """Cylindre (ou tronc de cône) entre deux points a et b."""
    a, b = Vector(a), Vector(b)
    d = b - a
    o = cyl(name, (a + b) / 2, r, d.length, mat, parent=parent, r2=r2)
    o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    return o


def empty(name, loc=(0, 0, 0)):
    o = bpy.data.objects.new(name, None); bpy.context.collection.objects.link(o); o.location = loc
    return o


def lights(key=(1.0, 0.92, 0.82), rim=(0.85, 0.65, 0.35), energy=3.2):
    bpy.ops.object.light_add(type='SUN'); s = bpy.context.object
    s.rotation_euler = (math.radians(55), 0, math.radians(-35)); s.data.energy = energy; s.data.color = key
    bpy.ops.object.light_add(type='SUN'); r = bpy.context.object
    r.rotation_euler = (math.radians(70), 0, math.radians(150)); r.data.energy = 2.0; r.data.color = rim


def camera(loc, target, lens=50):
    bpy.ops.object.camera_add(location=loc); c = bpy.context.object; c.data.lens = lens
    bpy.context.scene.camera = c
    d = Vector(target) - c.location
    c.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return c


def face(root, z, skin, eyes_scale=1.0, brows=(10, -10), tired=False, smirk=False, head_r=0.32):
    """Tête toon : sphère, yeux blancs + pupilles, sourcils inclinables, nez, bouche."""
    sph('tete', (0, 0, z), head_r, skin, parent=root)
    white, black = toon('blanc', (0.98, 0.97, 0.95)), toon('noir', (0.06, 0.06, 0.07))
    for s, ang in ((-1, brows[0]), (1, brows[1])):
        sph('oeil', (s * 0.11, -head_r * 0.86, z + 0.04), 0.075 * eyes_scale, white, (1, 0.6, 1.15), root)
        sph('pupille', (s * 0.11, -head_r * 0.86 - 0.05, z + 0.03), 0.034 * eyes_scale, black, parent=root)
        box('sourcil', (s * 0.11, -head_r * 0.9, z + 0.15), (0.12, 0.03, 0.025), black, root, rot=(0, math.radians(ang * s), 0))
        if tired:
            sph('cerne', (s * 0.11, -head_r * 0.8, z - 0.05), 0.06, toon('cerne', (0.45, 0.35, 0.45)), (1, 0.4, 0.45), root)
    sph('nez', (0, -head_r * 1.0, z - 0.03), 0.045, skin, (1, 1, 1.2), root)
    m = box('bouche', (0.03 if smirk else 0, -head_r * 0.92, z - 0.13), (0.11, 0.02, 0.022), toon('levres', (0.45, 0.15, 0.15)),
            root, rot=(0, math.radians(14 if smirk else 0), 0))
    return m
