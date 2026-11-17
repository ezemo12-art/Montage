"""Personnage articulé en SVG, généré depuis une fiche (même apparence dans tous les plans).

Repère du squelette : 1000 unités de haut, origine aux pieds, y vers le bas (tête vers -1000),
personnage tourné vers la droite. Chaque membre est un groupe <g> dont l'attribut transform
(rotate(a)) est animé par GSAP (tween d'attribut) autour de son articulation.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .style import PALETTE

# Articulations (repère 1000)
HIP_Y, SHOULDER_Y, HEAD_Y = -480, -800, -905
THIGH, SHIN = 240, 240
UPPER_ARM, FOREARM = 200, 190


@dataclass
class Personnage:
    id: str
    nom: str = ""
    genre: str = "homme"            # homme | femme
    age: str = "adulte"             # adulte | enfant | age
    taille_cm: int = 180
    carrure: str = "normale"        # mince | normale | forte
    manteau: str = "long"           # long | court | aucun
    chapeau: bool = False
    cheveux: str = "courts"         # courts | longs | chignon | chauve
    couleur: str = PALETTE["silhouette"]
    contour: str = PALETTE["ambre"]
    description: str = ""           # pour les générateurs d'images IA (phase 2.5D)
    extra: dict = field(default_factory=dict)

    @classmethod
    def depuis_fiche(cls, cid: str, fiche: dict) -> "Personnage":
        champs = {k: v for k, v in fiche.items() if k in cls.__dataclass_fields__ and k != "id"}
        return cls(id=cid, **champs)

    # --- géométrie ---------------------------------------------------------
    @property
    def largeur(self) -> float:
        base = {"mince": 0.85, "normale": 1.0, "forte": 1.22}[self.carrure]
        return base * (0.9 if self.genre == "femme" else 1.0)


def _limb(w_top: float, w_bot: float, length: float) -> str:
    """Membre fuselé, de l'articulation (0,0) vers le bas."""
    a, b = w_top / 2, w_bot / 2
    return (f"M{-a},0 C{-a},{length*0.35} {-b},{length*0.7} {-b},{length} "
            f"L{b},{length} C{b},{length*0.7} {a},{length*0.35} {a},0 Z")


def svg(p: Personnage, prefix: str) -> str:
    """Renvoie le <g> du personnage (sans position : le groupe racine est placé par l'appelant)."""
    k = p.largeur
    fill, rim = p.couleur, p.contour
    # Silhouette pleine : le liseré ambre est posé une seule fois autour du corps entier (filtre rim()).
    st = f'fill="{fill}"'

    def leg(side: str) -> str:
        foot = (f'<path d="M-24,{SHIN-14} L58,{SHIN-10} Q78,{SHIN} 58,{SHIN+12} L-26,{SHIN+12} Z" {st}/>')
        return (f'<g id="{prefix}-{side}-cuisse" transform="translate(0 {HIP_Y})"><g id="{prefix}-{side}-cuisse-r" transform="rotate(0)">'
                f'<path d="{_limb(92*k, 66*k, THIGH)}" {st}/>'
                f'<g transform="translate(0 {THIGH})"><g id="{prefix}-{side}-tibia-r" transform="rotate(0)">'
                f'<path d="{_limb(66*k, 48*k, SHIN)}" {st}/>{foot}</g></g></g></g>')

    def arm(side: str) -> str:
        return (f'<g id="{prefix}-{side}-bras" transform="translate(0 {SHOULDER_Y+20})"><g id="{prefix}-{side}-bras-r" transform="rotate(0)">'
                f'<path d="{_limb(64*k, 52*k, UPPER_ARM)}" {st}/>'
                f'<g transform="translate(0 {UPPER_ARM})"><g id="{prefix}-{side}-avbras-r" transform="rotate(0)">'
                f'<path d="{_limb(52*k, 40*k, FOREARM)}" {st}/><circle cx="0" cy="{FOREARM+18}" r="{28*k}" {st}/></g></g></g></g>')

    # Torse / manteau
    sh, hp = 100 * k, 78 * k
    if p.manteau == "long":
        bas, evase = HIP_Y + 300, 112 * k
    elif p.manteau == "court":
        bas, evase = HIP_Y + 70, 90 * k
    else:
        bas, evase = HIP_Y + 10, hp
    if p.genre == "femme" and p.manteau == "aucun":
        bas, evase = HIP_Y + 200, 105 * k  # robe
    torse = (f'<path d="M{-sh},{SHOULDER_Y} Q0,{SHOULDER_Y-28} {sh},{SHOULDER_Y} '
             f'L{hp+6},{HIP_Y} L{evase},{bas} L{-evase},{bas} L{-hp-6},{HIP_Y} Z" {st}/>')
    col = ""
    cou = f'<rect x="-28" y="{HEAD_Y+50}" width="56" height="70" {st}/>'

    # Tête + cheveux + chapeau
    r = 66
    tete = f'<ellipse cx="6" cy="{HEAD_Y}" rx="{r}" ry="{r+8}" {st}/><path d="M{r-4},{HEAD_Y+4} l18,14 l-16,6" {st}/>'
    if p.cheveux == "longs":
        che = f'<path d="M-70,{HEAD_Y-30} Q-10,{HEAD_Y-110} 66,{HEAD_Y-30} L40,{HEAD_Y-20} Q-40,{HEAD_Y-40} -60,{HEAD_Y+40} L-78,{HEAD_Y+150} L-30,{HEAD_Y+150} Z" {st}/>'
    elif p.cheveux == "chignon":
        che = f'<circle cx="-62" cy="{HEAD_Y-40}" r="34" {st}/><path d="M-66,{HEAD_Y-20} Q0,{HEAD_Y-105} 68,{HEAD_Y-26}" fill="{fill}"/>'
    elif p.cheveux == "courts":
        che = f'<path d="M-66,{HEAD_Y} Q-60,{HEAD_Y-90} 30,{HEAD_Y-80} Q72,{HEAD_Y-66} 70,{HEAD_Y-30} L-40,{HEAD_Y-30} Z" {st}/>'
    else:
        che = ""
    chap = ""
    if p.chapeau:
        chap = (f'<ellipse cx="6" cy="{HEAD_Y-48}" rx="118" ry="20" {st}/>'
                f'<path d="M-58,{HEAD_Y-50} L-48,{HEAD_Y-130} Q6,{HEAD_Y-150} 60,{HEAD_Y-130} L70,{HEAD_Y-50} Z" {st}/>')

    return (f'<g id="{prefix}-corps">'
            f'{arm("arr")}{leg("arr")}{cou}{torse}{col}{leg("av")}'
            f'<g id="{prefix}-tete" transform="translate(0 0)"><g id="{prefix}-tete-r" transform="rotate(0)">{tete}{che}{chap}</g></g>'
            f'{arm("av")}</g>')


def rim(p: Personnage, fid: str, rayon: float = 2.4) -> str:
    """Filtre SVG : un seul liseré ambre autour de toute la silhouette (lumière de contre-jour)."""
    return (f'<filter id="{fid}" x="-20%" y="-10%" width="140%" height="120%">'
            f'<feMorphology in="SourceAlpha" operator="dilate" radius="{rayon}" result="d"/>'
            f'<feFlood flood-color="{p.contour}" flood-opacity="0.75"/><feComposite in2="d" operator="in" result="r"/>'
            f'<feMerge><feMergeNode in="r"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def echelle(p: Personnage, px_par_metre: float) -> float:
    """Facteur d'échelle du squelette (1000 u) pour une taille réelle à l'écran."""
    taille = p.taille_cm / 100.0
    if p.age == "enfant":
        taille = min(taille, 1.25)
    return taille * px_par_metre / 1000.0
