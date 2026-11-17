"""Mouvements des personnages et des éléments de décor → lignes de timeline GSAP.

Tout est déterministe : chaque animation est un tween d'attribut `transform` / `opacity`
(fromTo) à un temps donné, relu identiquement à chaque image du rendu.
"""
from __future__ import annotations

import json

LIMBS = ["av-cuisse-r", "av-tibia-r", "arr-cuisse-r", "arr-tibia-r",
         "av-bras-r", "av-avbras-r", "arr-bras-r", "arr-avbras-r"]

# Poses clés (degrés, personnage tourné vers la droite ; + = vers l'arrière)
NEUTRE = dict.fromkeys(LIMBS, 0) | {"av-avbras-r": -6, "arr-avbras-r": -6}
PAS_A = {"av-cuisse-r": -24, "av-tibia-r": 6, "arr-cuisse-r": 20, "arr-tibia-r": 34,
         "av-bras-r": 18, "av-avbras-r": -10, "arr-bras-r": -18, "arr-avbras-r": -22}
PAS_B = {"av-cuisse-r": 20, "av-tibia-r": 34, "arr-cuisse-r": -24, "arr-tibia-r": 6,
         "av-bras-r": -18, "av-avbras-r": -22, "arr-bras-r": 18, "arr-avbras-r": -10}
COURSE_A = {k: v * 1.7 for k, v in PAS_A.items()} | {"av-avbras-r": -70, "arr-avbras-r": -70}
COURSE_B = {k: v * 1.7 for k, v in PAS_B.items()} | {"av-avbras-r": -70, "arr-avbras-r": -70}
TELEPHONE = NEUTRE | {"av-bras-r": -150, "av-avbras-r": -125}


class Timeline:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def attr(self, sel: str, a: str, b: str, t: float, d: float, ease: str = "sine.inOut", name="transform"):
        self.lines.append(
            f'tl.fromTo("{sel}", {{attr: {{{name}: {json.dumps(a)}}}}}, '
            f'{{attr: {{{name}: {json.dumps(b)}}}, duration: {max(d, 0.01):.3f}, ease: "{ease}"}}, {t:.3f});')

    def prop(self, sel: str, a: dict, b: dict, t: float, d: float, ease: str = "power2.inOut"):
        bb = dict(b, duration=round(max(d, 0.01), 3), ease=ease)
        self.lines.append(f'tl.fromTo("{sel}", {json.dumps(a)}, {json.dumps(bb)}, {t:.3f});')

    def js(self) -> str:
        return "\n    ".join(self.lines)


class Acteur:
    """Un personnage placé dans un plan : position, orientation, échelle."""

    def __init__(self, prefix: str, x: float, y: float, s: float, sens: int = 1):
        self.p, self.x, self.y, self.s, self.sens = prefix, x, y, s, sens
        self.pose = dict(NEUTRE)
        self.opacite = 1.0

    # groupes : #{p}-pos  translate(x y) · #{p}-bob translate(0 b) · #{p}-echelle scale(sx s)
    def pos_str(self, x, y):
        return f"translate({x:.1f} {y:.1f})"

    def echelle_str(self, sens=None):
        sens = self.sens if sens is None else sens
        return f"scale({sens * self.s:.4f} {self.s:.4f})"

    def _pose(self, tl: Timeline, cible: dict, t: float, d: float, ease="sine.inOut"):
        for k in LIMBS:
            a, b = self.pose[k], cible[k]
            if a != b:
                tl.attr(f"#{self.p}-{k}", f"rotate({a})", f"rotate({b})", t, d, ease)
        self.pose = dict(cible)

    # --- actions ------------------------------------------------------------
    def marche(self, tl: Timeline, t0: float, t1: float, x1: float, demi_pas: float = 0.42,
               a=PAS_A, b=PAS_B, amplitude_bob: float = 10):
        if x1 != self.x:
            self.oriente(tl, t0, 1 if x1 > self.x else -1)
        tl.attr(f"#{self.p}-pos", self.pos_str(self.x, self.y), self.pos_str(x1, self.y), t0, t1 - t0, "none")
        n = max(2, round((t1 - t0) / demi_pas))
        h = (t1 - t0) / n
        self._pose(tl, a, t0, h / 2)
        for i in range(1, n):
            self._pose(tl, b if i % 2 else a, t0 + h / 2 + (i - 1) * h, h)
        for i in range(n):
            tm = t0 + i * h
            tl.attr(f"#{self.p}-bob", "translate(0 0)", f"translate(0 {-amplitude_bob:.1f})", tm, h / 2, "sine.out")
            tl.attr(f"#{self.p}-bob", f"translate(0 {-amplitude_bob:.1f})", "translate(0 0)", tm + h / 2, h / 2, "sine.in")
        self._pose(tl, NEUTRE, t1 - h / 2, h / 2)
        self.x = x1

    def court(self, tl, t0, t1, x1):
        self.marche(tl, t0, t1, x1, demi_pas=0.24, a=COURSE_A, b=COURSE_B, amplitude_bob=16)

    def oriente(self, tl: Timeline, t: float, sens: int):
        if sens != self.sens:
            tl.attr(f"#{self.p}-echelle", self.echelle_str(), self.echelle_str(sens), t, 0.18, "power1.inOut")
            self.sens = sens

    def regarde_derriere(self, tl: Timeline, t: float, duree: float = 1.0):
        tl.attr(f"#{self.p}-tete", "scale(1 1)", "scale(-1 1)", t, 0.25, "power2.inOut")
        tl.attr(f"#{self.p}-tete", "scale(-1 1)", "scale(1 1)", t + duree, 0.25, "power2.inOut")

    def telephone(self, tl: Timeline, t: float, duree: float = 2.0):
        self._pose(tl, TELEPHONE, t, 0.6, "power2.inOut")
        self._pose(tl, NEUTRE, t + duree, 0.6, "power2.inOut")

    def disparait(self, tl: Timeline, t: float, d: float = 0.7):
        tl.prop(f"#{self.p}-pos", {"opacity": self.opacite}, {"opacity": 0}, t, d)
        self.opacite = 0

    def apparait(self, tl: Timeline, t: float, d: float = 0.7):
        tl.prop(f"#{self.p}-pos", {"opacity": 0}, {"opacity": 1}, t, d)
        self.opacite = 1

    def entre(self, tl: Timeline, t0: float, t1: float, x_porte: float):
        """Marche jusqu'au seuil puis s'enfonce dans l'embrasure (fondu)."""
        mid = t0 + (t1 - t0) * 0.7
        self.marche(tl, t0, mid, x_porte)
        tl.attr(f"#{self.p}-bob", "translate(0 0) scale(1)", "translate(0 -6) scale(0.94)", mid, t1 - mid, "power1.in")
        self.disparait(tl, mid + (t1 - mid) * 0.3, (t1 - mid) * 0.7)

    def tombe(self, tl: Timeline, t: float, d: float = 0.8):
        tl.attr(f"#{self.p}-bob", "translate(0 0) rotate(0)", f"translate(0 0) rotate({88 * self.sens})", t, d, "power2.in")
