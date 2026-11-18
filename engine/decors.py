"""Décors illustrés (SVG) en couches pour la parallaxe : bg (fond), mid (plan d'action), fg (premier plan).

Chaque décor renvoie une Scene : défs SVG, couches, points d'ancrage (sol, porte, fenêtres…)
et l'échelle px/mètre utilisée pour dimensionner les personnages. Un même lieu (fiche) produit
toujours le même dessin, quel que soit le plan.
"""
from __future__ import annotations

import pathlib
from dataclasses import dataclass, field

from .style import PALETTE as C, ROOT as ROOT_DEPOT

W, H = 1080, 1920


@dataclass
class Scene:
    defs: list[str] = field(default_factory=list)
    bg: list[str] = field(default_factory=list)
    mid: list[str] = field(default_factory=list)
    fg: list[str] = field(default_factory=list)
    ancres: dict = field(default_factory=dict)
    px_par_metre: float = 90.0
    sol_y: float = 1080.0


# ---------------------------------------------------------------- éléments communs
def ciel_nuit(p: str, sc: Scene, horizon: float = 1080):
    sc.defs.append(
        f'<linearGradient id="{p}-ciel" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{C["charbon"]}"/><stop offset="1" stop-color="{C["archive"]}"/></linearGradient>'
        f'<radialGradient id="{p}-lune-halo"><stop offset="0" stop-color="{C["ivoire"]}" stop-opacity="0.35"/>'
        f'<stop offset="1" stop-color="{C["ivoire"]}" stop-opacity="0"/></radialGradient>')
    sc.bg.append(f'<rect x="-400" y="-400" width="{W+800}" height="{horizon+400}" fill="url(#{p}-ciel)"/>')
    etoiles = [(90, 240), (210, 150), (330, 300), (470, 190), (610, 120), (700, 260), (960, 180),
               (1010, 420), (150, 470), (420, 420), (880, 520), (60, 640), (980, 640), (520, 560)]
    sc.bg.append("".join(f'<circle cx="{x}" cy="{y}" r="{1.6 + (i % 3) * 0.6}" fill="{C["ivoire"]}" opacity="{0.25 + (i % 4) * 0.12:.2f}"/>'
                         for i, (x, y) in enumerate(etoiles)))
    sc.bg.append(f'<circle cx="830" cy="330" r="190" fill="url(#{p}-lune-halo)"/>'
                 f'<circle cx="830" cy="330" r="52" fill="{C["ivoire"]}" opacity="0.92"/>'
                 f'<circle cx="812" cy="318" r="9" fill="{C["archive"]}" opacity="0.18"/><circle cx="846" cy="346" r="6" fill="{C["archive"]}" opacity="0.15"/>')
    # Ligne d'arbres lointains
    pts = " ".join(f"{x},{horizon - 60 - ((x * 37) % 70) - (40 if (x // 90) % 2 else 0)}" for x in range(-400, W + 401, 45))
    sc.bg.append(f'<polygon points="-400,{horizon} {pts} {W+400},{horizon}" fill="{C["charbon"]}" opacity="0.75"/>')


def sol(p: str, sc: Scene, y: float):
    sc.mid.append(f'<rect x="-600" y="{y}" width="{W+1200}" height="{H-y+600}" fill="{C["charbon"]}"/>'
                  f'<line x1="-600" y1="{y+1}" x2="{W+600}" y2="{y+1}" stroke="{C["ivoire"]}" stroke-opacity="0.12" stroke-width="2"/>'
                  f'<line x1="-600" y1="{y+70}" x2="{W+600}" y2="{y+70}" stroke="{C["ivoire"]}" stroke-opacity="0.05" stroke-width="2"/>')


def lampadaire(p: str, sc: Scene, x: float, y: float):
    sc.defs.append(f'<radialGradient id="{p}-cone" cx="0.5" cy="0" r="1"><stop offset="0" stop-color="{C["ambre"]}" stop-opacity="0.32"/>'
                   f'<stop offset="1" stop-color="{C["ambre"]}" stop-opacity="0"/></radialGradient>')
    sc.fg.append(f'<polygon points="{x-6},{y-470} {x-170},{y+10} {x+150},{y+10}" fill="url(#{p}-cone)"/>'
                 f'<rect x="{x-7}" y="{y-480}" width="14" height="490" fill="{C["charbon"]}"/>'
                 f'<path d="M{x},{y-480} q30,-30 62,-6" stroke="{C["charbon"]}" stroke-width="12" fill="none"/>'
                 f'<rect x="{x+40}" y="{y-486}" width="44" height="18" rx="4" fill="{C["ambre"]}"/>')


# ---------------------------------------------------------------- maison
def maison(p: str, sc: Scene, fiche: dict, x0: float, gy: float, k: float = 1.0) -> dict:
    """Maison à 2 niveaux, porte au centre-gauche. Renvoie les ancres (porte, fenêtres)."""
    w, hm, toit = 520 * k, 380 * k, 210 * k
    top = gy - hm
    allumees = set(fiche.get("fenetres_allumees", []))
    sc.defs.append(f'<linearGradient id="{p}-int" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["ambre"]}" stop-opacity="0.85"/>'
                   f'<stop offset="1" stop-color="{C["charbon"]}"/></linearGradient>'
                   f'<radialGradient id="{p}-appl"><stop offset="0" stop-color="{C["ambre"]}" stop-opacity="0.5"/><stop offset="1" stop-color="{C["ambre"]}" stop-opacity="0"/></radialGradient>')
    s = []
    # cheminée, toit, mur
    s.append(f'<rect x="{x0+w*0.72}" y="{top-toit*0.9}" width="{46*k}" height="{toit*0.7}" fill="{C["charbon"]}" stroke="{C["ivoire"]}" stroke-opacity="0.12" stroke-width="2"/>')
    s.append(f'<polygon points="{x0-30*k},{top+4} {x0+w/2},{top-toit} {x0+w+30*k},{top+4}" fill="{C["charbon"]}" stroke="{C["ivoire"]}" stroke-opacity="0.18" stroke-width="2"/>')
    s.append(f'<rect x="{x0}" y="{top}" width="{w}" height="{hm}" fill="{C["archive"]}"/>')
    s.append("".join(f'<line x1="{x0}" y1="{top+i*28*k:.1f}" x2="{x0+w}" y2="{top+i*28*k:.1f}" stroke="{C["ivoire"]}" stroke-opacity="0.035" stroke-width="2"/>'
                     for i in range(1, int(hm / (28 * k)))))
    # fenêtres : 0,1 étage ; 2,3 rez-de-chaussée
    fen = [(60, 50), (370, 50), (60, 220), (370, 220)]
    ancres_f = []
    for i, (fx, fy) in enumerate(fen):
        x, y, fw, fh = x0 + fx * k, top + fy * k, 90 * k, 110 * k
        s.append(f'<rect x="{x}" y="{y}" width="{fw}" height="{fh}" fill="{C["charbon"]}" stroke="{C["ivoire"]}" stroke-opacity="0.2" stroke-width="3"/>')
        s.append(f'<rect id="{p}-f{i}" x="{x+4}" y="{y+4}" width="{fw-8}" height="{fh-8}" fill="{C["ambre"]}" opacity="{0.85 if i in allumees else 0}"/>')
        s.append(f'<line x1="{x+fw/2}" y1="{y}" x2="{x+fw/2}" y2="{y+fh}" stroke="{C["archive"]}" stroke-width="5"/>'
                 f'<line x1="{x}" y1="{y+fh*0.45}" x2="{x+fw}" y2="{y+fh*0.45}" stroke="{C["archive"]}" stroke-width="5"/>')
        ancres_f.append((x + fw / 2, y + fh / 2))
    # porte
    dw, dh = 90 * k, 195 * k
    dx = x0 + 215 * k
    s.append(f'<rect x="{dx-10*k}" y="{gy-dh-14*k}" width="{dw+20*k}" height="{dh+14*k}" fill="{C["charbon"]}" stroke="{C["ivoire"]}" stroke-opacity="0.18" stroke-width="2"/>')
    s.append(f'<rect id="{p}-seuil" x="{dx}" y="{gy-dh}" width="{dw}" height="{dh}" fill="url(#{p}-int)"/>')
    s.append(f'<g transform="translate({dx} {gy-dh})"><g id="{p}-porte" transform="scale(1 1)">'
             f'<rect width="{dw}" height="{dh}" fill="{C["charbon"]}" stroke="{C["ivoire"]}" stroke-opacity="0.22" stroke-width="2"/>'
             f'<rect x="{dw*0.15}" y="{dh*0.08}" width="{dw*0.7}" height="{dh*0.36}" fill="none" stroke="{C["ivoire"]}" stroke-opacity="0.1" stroke-width="2"/>'
             f'<rect x="{dw*0.15}" y="{dh*0.52}" width="{dw*0.7}" height="{dh*0.38}" fill="none" stroke="{C["ivoire"]}" stroke-opacity="0.1" stroke-width="2"/>'
             f'<circle cx="{dw*0.84}" cy="{dh*0.55}" r="{5*k}" fill="{C["ambre"]}"/></g></g>')
    # applique au-dessus de la porte + marche
    s.append(f'<circle cx="{dx+dw/2}" cy="{gy-dh-40*k}" r="{120*k}" fill="url(#{p}-appl)" id="{p}-appl-halo" opacity="{1 if fiche.get("applique", True) else 0}"/>'
             f'<rect x="{dx+dw/2-8*k}" y="{gy-dh-50*k}" width="{16*k}" height="{22*k}" rx="3" fill="{C["ambre"]}"/>')
    s.append(f'<rect x="{dx-24*k}" y="{gy-8*k}" width="{dw+48*k}" height="{10*k}" fill="{C["ivoire"]}" opacity="0.08"/>')
    sc.mid.append("".join(s))
    return {"porte_x": dx + dw / 2, "porte_haut": gy - dh, "porte_l": dw, "fenetres": ancres_f,
            "px_par_metre": dh / 2.1, "x0": x0, "largeur": w}


# ---------------------------------------------------------------- décors complets
def maison_nuit(p: str, lieu: dict) -> Scene:
    sc = Scene(sol_y=1080)
    ciel_nuit(p, sc, 1080)
    sol(p, sc, 1080)
    a = maison(p, sc, lieu, 300, 1080, 1.0)
    # allée vers la porte + trottoir (remplit le bas du cadre vertical)
    px = a["porte_x"]
    sc.mid.append(f'<polygon points="{px-52},1082 {px+52},1082 {px+260},1920 {px-260},1920" fill="{C["archive"]}" opacity="0.35"/>'
                  f'<rect x="-600" y="1300" width="{W+1200}" height="26" fill="{C["archive"]}" opacity="0.4"/>')
    # buissons au pied de la maison, lampadaire au premier plan
    sc.mid.append("".join(f'<ellipse cx="{x}" cy="1074" rx="{r}" ry="{r*0.6}" fill="{C["charbon"]}"/>'
                          for x, r in [(330, 44), (380, 30), (700, 50), (770, 36), (820, 40)]))
    lampadaire(p, sc, 120, 1080)
    sc.ancres = a | {"gauche": -120, "droite": W + 120}
    sc.px_par_metre = a["px_par_metre"]
    return sc


def couloir(p: str, lieu: dict) -> Scene:
    """Intérieur en perspective (point de fuite central), lampe suspendue, porte au fond."""
    sc = Scene(sol_y=1120, px_par_metre=300)
    vx, vy = 540, 760
    bw = (400, 620, 680, 900)  # mur du fond : x1, y1, x2, y2
    sc.defs.append(f'<radialGradient id="{p}-flaque"><stop offset="0" stop-color="{C["ambre"]}" stop-opacity="0.38"/><stop offset="1" stop-color="{C["ambre"]}" stop-opacity="0"/></radialGradient>'
                   f'<linearGradient id="{p}-mur" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["charbon"]}"/><stop offset="1" stop-color="{C["archive"]}"/></linearGradient>'
                   f'<linearGradient id="{p}-murd" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{C["charbon"]}"/><stop offset="1" stop-color="{C["archive"]}"/></linearGradient>')
    x1, y1, x2, y2 = bw
    sc.bg.append(f'<rect x="-300" y="-300" width="{W+600}" height="{H+600}" fill="{C["charbon"]}"/>'
                 f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="{C["archive"]}"/>'
                 # porte du fond + filet de lumière dessous
                 f'<rect x="500" y="700" width="80" height="200" fill="{C["charbon"]}" stroke="{C["ivoire"]}" stroke-opacity="0.15" stroke-width="2"/>'
                 f'<rect id="{p}-filet" x="500" y="896" width="80" height="5" fill="{C["ambre"]}"/>')
    # murs latéraux, plafond, sol
    sc.mid.append(f'<polygon points="-300,-300 {x1},{y1} {x1},{y2} -300,{H+300}" fill="url(#{p}-mur)"/>'
                  f'<polygon points="{W+300},-300 {x2},{y1} {x2},{y2} {W+300},{H+300}" fill="url(#{p}-murd)"/>'
                  f'<polygon points="-300,-300 {W+300},-300 {x2},{y1} {x1},{y1}" fill="{C["charbon"]}"/>'
                  f'<polygon points="{x1},{y2} {x2},{y2} {W+300},{H+300} -300,{H+300}" fill="{C["charbon"]}"/>')
    # lattes du sol vers le point de fuite
    sc.mid.append("".join(f'<line x1="{x1 + (x2-x1)*i/8}" y1="{y2}" x2="{-300 + (W+600)*i/8}" y2="{H+300}" stroke="{C["ivoire"]}" stroke-opacity="0.05" stroke-width="2"/>' for i in range(9)))
    # cadres sur les murs
    sc.mid.append(f'<polygon points="120,560 280,640 280,800 120,780" fill="none" stroke="{C["ivoire"]}" stroke-opacity="0.22" stroke-width="5"/>'
                  f'<polygon points="960,560 800,640 800,800 960,780" fill="none" stroke="{C["ivoire"]}" stroke-opacity="0.22" stroke-width="5"/>'
                  f'<polygon points="140,610 262,666 262,770 140,756" fill="{C["archive"]}" opacity="0.6"/>')
    # lampe suspendue + flaque de lumière
    sc.mid.append(f'<ellipse cx="{vx}" cy="1130" rx="420" ry="120" fill="url(#{p}-flaque)" id="{p}-flaque-l"/>'
                  f'<line x1="{vx}" y1="300" x2="{vx}" y2="470" stroke="{C["charbon"]}" stroke-width="4"/>'
                  f'<path d="M{vx-60},520 Q{vx},440 {vx+60},520 Z" fill="{C["charbon"]}" stroke="{C["ivoire"]}" stroke-opacity="0.2" stroke-width="2"/>'
                  f'<ellipse cx="{vx}" cy="522" rx="34" ry="8" fill="{C["ambre"]}"/>')
    sc.ancres = {"gauche": -200, "droite": W + 200, "fond_x": vx, "fond_y": y2}
    return sc


def voisinage(p: str, lieu: dict, voisin: dict) -> Scene:
    """La maison du récit au loin (droite) et la maison des voisins au premier plan (gauche)."""
    sc = Scene(sol_y=1080)
    ciel_nuit(p, sc, 1000)
    sc.mid.append(f'<rect x="-600" y="1000" width="{W+1200}" height="1200" fill="{C["charbon"]}"/>')
    loin = maison(p + "-m", sc, lieu, 590, 1010, 0.6)
    sol(p, sc, 1080)
    pres = maison(p + "-v", sc, voisin, -150, 1080, 1.05)
    # ondes sonores depuis la maison du récit
    cx, cy = loin["fenetres"][3]
    ondes = "".join(f'<g transform="translate({cx:.1f} {cy:.1f})"><g id="{p}-onde{i}" transform="scale(0.3)" opacity="0">'
                    f'<path d="M-60,-70 A92,92 0 0 0 -60,70" fill="none" stroke="{C["ivoire"]}" stroke-width="5" stroke-linecap="round"/>'
                    f'<path d="M60,-70 A92,92 0 0 1 60,70" fill="none" stroke="{C["ivoire"]}" stroke-width="5" stroke-linecap="round"/></g></g>' for i in range(3))
    sc.fg.append(ondes)
    # silhouette d'un voisin derrière une fenêtre allumée (buste)
    fx, fy = pres["fenetres"][1]
    sc.mid.append(f'<g id="{p}-voisin" opacity="0"><ellipse cx="{fx+8:.1f}" cy="{fy-8:.1f}" rx="17" ry="20" fill="{C["charbon"]}"/>'
                  f'<path d="M{fx-22:.1f},{fy+52:.1f} Q{fx+8:.1f},{fy+6:.1f} {fx+38:.1f},{fy+52:.1f} Z" fill="{C["charbon"]}"/></g>')
    sc.ancres = {"loin": loin, "pres": pres, "son": (cx, cy), "gauche": -120, "droite": W + 120}
    sc.px_par_metre = pres["px_par_metre"]
    return sc


# L'Archiviste : image officielle EXACTE (archiviste/references/Character_FullBody_v1.jpg), jamais redessinée.
ARCHIVISTE_IMG = (1206, 1162)       # taille de l'image officielle
ARCHIVISTE_ASSET = "assets/archiviste.jpg"


def archiviste(p: str, lieu: dict) -> Scene:
    """Plan narrateur : l'Archiviste sort de l'ombre, une lumière ambre l'éclaire.
    Le mouvement vient de la mise en scène (ombre, lumière, caméra) : son apparence n'est jamais modifiée."""
    w0, h0 = ARCHIVISTE_IMG
    w = W
    h = h0 * w / w0
    y = 1220 - h  # le bas de l'image s'arrête à la limite de la zone sûre
    sc = Scene(sol_y=1220)
    sc.defs.append(f'<linearGradient id="{p}-haut" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["charbon"]}"/>'
                   f'<stop offset="1" stop-color="{C["charbon"]}" stop-opacity="0"/></linearGradient>'
                   f'<linearGradient id="{p}-bas" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["charbon"]}" stop-opacity="0"/>'
                   f'<stop offset="1" stop-color="{C["charbon"]}"/></linearGradient>'
                   f'<radialGradient id="{p}-ambre"><stop offset="0" stop-color="{C["ambre"]}" stop-opacity="0.55"/>'
                   f'<stop offset="1" stop-color="{C["ambre"]}" stop-opacity="0"/></radialGradient>')
    sc.bg.append(f'<rect x="-300" y="-300" width="{W+600}" height="{H+600}" fill="{C["charbon"]}"/>'
                 f'<image href="{ARCHIVISTE_ASSET}" x="0" y="{y:.1f}" width="{w}" height="{h:.1f}" preserveAspectRatio="none"/>'
                 # raccords haut / bas de l'image avec le noir du cadre (habillage, l'image n'est pas modifiée)
                 f'<rect x="-300" y="{y-2:.1f}" width="{W+600}" height="160" fill="url(#{p}-haut)"/>'
                 f'<rect x="-300" y="{y+h-160:.1f}" width="{W+600}" height="162" fill="url(#{p}-bas)"/>'
                 f'<rect x="-300" y="{y+h:.1f}" width="{W+600}" height="{H}" fill="{C["charbon"]}"/>')
    sc.mid.append(f'<ellipse id="{p}-lumiere" cx="760" cy="{y + h*0.42:.1f}" rx="430" ry="560" fill="url(#{p}-ambre)" '
                  f'opacity="0" style="mix-blend-mode:screen"/>')
    sc.fg.append(f'<rect id="{p}-ombre" x="-300" y="-300" width="{W+600}" height="{H+600}" fill="{C["charbon"]}" '
                 f'opacity="{float(lieu.get("ombre_initiale", 0.9))}"/>')
    sc.ancres = {"visage": (W / 2, y + h * 0.30), "gauche": -200, "droite": W + 200}
    return sc


def illustration(p: str, plan: dict) -> Scene:
    """Plan illustré : image générée (Runway…) plein cadre, animée par le moteur
    (caméra, ombre, lumière ambre, ondes sonores). L'image est posée telle quelle."""
    sc = Scene(sol_y=1500)
    lx, ly = plan.get("lumiere_xy", [540, 700])
    sx, sy = plan.get("son_xy", [540, 700])
    sc.defs.append(f'<radialGradient id="{p}-ambre"><stop offset="0" stop-color="{C["ambre"]}" stop-opacity="0.6"/>'
                   f'<stop offset="1" stop-color="{C["ambre"]}" stop-opacity="0"/></radialGradient>')
    sc.bg.append(f'<rect x="-300" y="-300" width="{W+600}" height="{H+600}" fill="{C["charbon"]}"/>'
                 f'<image href="assets/plans/{p}{pathlib.Path(plan["image"]).suffix}" x="0" y="0" width="{W}" height="{H}" '
                 f'preserveAspectRatio="xMidYMid slice"/>')
    sc.mid.append(f'<ellipse id="{p}-lumiere" cx="{lx}" cy="{ly}" rx="{plan.get("lumiere_rayon", 260)}" '
                  f'ry="{plan.get("lumiere_rayon", 260)}" fill="url(#{p}-ambre)" opacity="0" style="mix-blend-mode:screen"/>')
    sc.fg.append("".join(f'<g transform="translate({sx} {sy})"><g id="{p}-onde{i}" transform="scale(0.3)" opacity="0">'
                         f'<path d="M-60,-70 A92,92 0 0 0 -60,70" fill="none" stroke="{C["ivoire"]}" stroke-width="5" stroke-linecap="round"/>'
                         f'<path d="M60,-70 A92,92 0 0 1 60,70" fill="none" stroke="{C["ivoire"]}" stroke-width="5" stroke-linecap="round"/></g></g>'
                         for i in range(3)))
    sc.fg.append(f'<rect id="{p}-ombre" x="-300" y="-300" width="{W+600}" height="{H+600}" fill="{C["charbon"]}" '
                 f'opacity="{float(plan.get("ombre_initiale", 0))}"/>')
    sc.ancres = {"son": (sx, sy), "visage": (lx, ly), "gauche": -200, "droite": W + 200}
    return sc


DECORS = {"maison_nuit": maison_nuit, "couloir": couloir, "voisinage": voisinage, "archiviste": archiviste,
          "illustration": illustration}
