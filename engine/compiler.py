"""Storyboard → projet HyperFrames (un plan = une sous-composition) + voix + sous-titres."""
from __future__ import annotations

import html
import json
import pathlib
import shutil

from . import decors as D
from .actions import Acteur, Timeline
from .character import Personnage, echelle, rim, svg as svg_perso
from .storyboard import _norm, caler, mots, temps
from .style import DA_CSS, PALETTE as C

PARALLAXE = {"bg": 0.35, "mid": 1.0, "fg": 1.25}


# ---------------------------------------------------------------- caméra
def _focus(spec, sc: D.Scene):
    a = sc.ancres
    if isinstance(spec, (list, tuple)):
        return float(spec[0]), float(spec[1])
    if spec == "porte":
        return a["porte_x"], a["porte_haut"] + 90
    if spec == "visage" and "visage" in a:
        return a["visage"]
    if spec == "son" and "son" in a:
        return a["son"]
    return 540.0, sc.sol_y - 300


def _cam(z: float, fx: float, fy: float, pan: float, p: float) -> str:
    s = 1 + (z - 1) * p
    return f"translate({fx + pan * p:.1f} {fy:.1f}) scale({s:.4f}) translate({-fx:.1f} {-fy:.1f})"


def camera(spec: dict | None, sc: D.Scene):
    spec = spec or {}
    typ, z = spec.get("type", "push_in"), float(spec.get("zoom", 1.0))
    fx, fy = _focus(spec.get("focus"), sc)
    if typ == "fixe":
        z0, z1, p0, p1 = z, z, 0, 0
    elif typ == "cadrage":
        z0, z1, p0, p1 = z, z * 1.05, 0, 0
    elif typ == "travelling":
        z0, z1, p0, p1 = z, z, float(spec.get("pan", 70)), -float(spec.get("pan", 70))
    elif typ == "recul":
        z0, z1, p0, p1 = z * 1.15, z, 0, 0
    else:  # push_in
        z0, z1, p0, p1 = z, z * float(spec.get("intensite", 1.12)), 0, 0
    return {k: (_cam(z0, fx, fy, p0, f), _cam(z1, fx, fy, p1, f)) for k, f in PARALLAXE.items()}


# ---------------------------------------------------------------- un plan
def compiler_plan(pl: dict, sb: dict, ws: list[dict]) -> str:
    P = pl["id"]
    lieux = sb.get("lieux", {})
    lieu = lieux.get(pl.get("lieu"), {})
    if pl["decor"] == "voisinage":
        sc = D.voisinage(P, lieu, lieux.get(pl.get("voisin"), {}))
    elif pl["decor"] == "illustration":
        sc = D.illustration(P, pl)
    else:
        sc = D.DECORS[pl["decor"]](P, lieu)
    tl = Timeline()
    dur = pl["duree"]

    # personnages
    acteurs: dict[str, Acteur] = {}
    persos_svg = []
    for pp in pl.get("personnages", []):
        fiche = sb["personnages"][pp["qui"]]
        perso = Personnage.depuis_fiche(pp["qui"], fiche)
        x = pp.get("x", "gauche")
        if isinstance(x, str):
            x = sc.ancres.get("porte_x" if x == "porte" else x, 540)
        x = float(x) + float(pp.get("dx", 0))
        s = echelle(perso, sc.px_par_metre * float(pp.get("profondeur", 1.0)))
        y = sc.sol_y + float(pp.get("dy", 0))
        pref = f"{P}-{pp['qui']}"
        act = Acteur(pref, x, y, s, int(pp.get("sens", 1)))
        act.opacite = float(pp.get("opacite", 1))
        acteurs[pp["qui"]] = act
        sc.defs.append(rim(perso, f"{pref}-rim"))
        persos_svg.append(
            f'<g id="{pref}-pos" transform="{act.pos_str(x, y)}" opacity="{act.opacite}" filter="url(#{pref}-rim)">'
            f'<g id="{pref}-bob" transform="translate(0 0)"><g id="{pref}-echelle" transform="{act.echelle_str()}">'
            f'{svg_perso(perso, pref)}</g></g></g>')

    # actions
    for a in pl.get("actions", []):
        t0 = temps(a.get("de"), pl, ws, 0.0)
        t1 = temps(a.get("a"), pl, ws, 1.0)
        t1 = min(max(t1, t0 + 0.3), dur)
        typ = a["action"]
        act = acteurs.get(a.get("qui"))
        cible = a.get("vers")
        if isinstance(cible, str):
            cible = sc.ancres.get("porte_x" if cible == "porte" else cible, 540)
        if cible is not None:
            cible = float(cible) + float(a.get("dx", 0))
        if typ in ("marche", "court"):
            getattr(act, typ)(tl, t0, t1, float(cible))
        elif typ == "entre":
            act.entre(tl, t0, t1, sc.ancres["porte_x"])
        elif typ == "regarde_derriere":
            act.regarde_derriere(tl, t0, max(0.6, t1 - t0 - 0.3))
        elif typ == "telephone":
            act.telephone(tl, t0, max(0.8, t1 - t0 - 0.6))
        elif typ == "apparait":
            act.apparait(tl, t0)
        elif typ == "disparait":
            act.disparait(tl, t0)
        elif typ == "tombe":
            act.tombe(tl, t0)
        elif typ in ("ouvre_porte", "ferme_porte"):
            a0, b0 = ("scale(1 1)", "scale(0.12 1)") if typ == "ouvre_porte" else ("scale(0.12 1)", "scale(1 1)")
            tl.attr(f"#{P}-porte", a0, b0, t0, float(a.get("duree", 0.9)), "power2.inOut")
        elif typ in ("lumieres", "eteint"):
            pre = {"voisin": f"{P}-v", "recit": f"{P}-m"}.get(a.get("maison"), P)
            o0, o1 = (0, 0.85) if typ == "lumieres" else (0.85, 0)
            for k, f in enumerate(a.get("fenetres", [0, 1, 2, 3])):
                tl.prop(f"#{pre}-f{f}", {"opacity": o0}, {"opacity": o1}, t0 + k * 0.35, 0.5, "power1.out")
        elif typ == "bruit":
            for rep in range(int(a.get("repetitions", 2))):
                for i in range(3):
                    t = t0 + rep * 1.1 + i * 0.32
                    tl.attr(f"#{P}-onde{i}", "scale(0.3)", "scale(1.9)", t, 1.3, "power1.out")
                    tl.prop(f"#{P}-onde{i}", {"opacity": 0.95}, {"opacity": 0}, t, 1.3, "power1.in")
        elif typ == "sort_de_l_ombre":
            tl.prop(f"#{P}-ombre", {"opacity": float(pl.get("ombre_initiale", lieu.get("ombre_initiale", 0.9)))}, {"opacity": 0}, t0, max(0.8, t1 - t0), "power2.inOut")
        elif typ == "lumiere_ambre":
            tl.prop(f"#{P}-lumiere", {"opacity": 0}, {"opacity": 1}, t0, max(0.6, t1 - t0), "power2.inOut")
        elif typ == "voisin_regarde":
            tl.prop(f"#{P}-voisin", {"opacity": 0}, {"opacity": 1}, t0, 0.8)

    # caméra (sur toute la durée du plan)
    cam = camera(pl.get("camera"), sc)
    for k, (c0, c1) in cam.items():
        tl.attr(f"#{P}-cam-{k}", c0, c1, 0, dur, "none")  # mouvement constant : jamais d'image figée

    # incrustation (heure, lieu…)
    ov = ""
    inc = pl.get("incrustation")
    if inc:
        ov = (f'<div id="{P}-ov" style="position:absolute;left:150px;top:300px;width:740px">'
              f'<div id="{P}-ov-t" class="da-tag" style="font-size:46px;display:inline-block">{html.escape(inc["texte"])}</div>'
              + (f'<div id="{P}-ov-s" class="da-meta" style="margin-top:12px">{html.escape(inc["sous_texte"])}</div>' if inc.get("sous_texte") else "")
              + "</div>")
        tl.prop(f"#{P}-ov-t", {"clipPath": "inset(0 100% 0 0)"}, {"clipPath": "inset(0 0% 0 0)"}, 0.3, 0.6, "steps(8)")
        if inc.get("sous_texte"):
            tl.prop(f"#{P}-ov-s", {"opacity": 0}, {"opacity": 1}, 0.9, 0.5)

    # fondu d'entrée
    tl.prop(f"#{P}-noir", {"opacity": 1}, {"opacity": 0}, 0, 0.35, "power1.out")

    calques = {"bg": sc.bg, "mid": sc.mid + persos_svg, "fg": sc.fg}
    groupes = "".join(f'<g id="{P}-cam-{k}" transform="{cam[k][0]}">{"".join(v)}</g>' for k, v in calques.items())
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; background: {C["charbon"]}; overflow: hidden; }}
    #{P}-svg {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
    #{P}-noir {{ position: absolute; inset: 0; background: {C["charbon"]}; }}
  </style>
  <div id="root" data-composition-id="{P}" data-width="1080" data-height="1920">
    <svg id="{P}-svg" viewBox="0 0 1080 1920" data-layout-ignore><defs>{"".join(sc.defs)}</defs>{groupes}</svg>
    {ov}
    <div id="{P}-noir" data-layout-ignore></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {tl.js()}
    window.__timelines["{P}"] = tl;
  </script>
</template>
"""


# ---------------------------------------------------------------- sous-titres
def sous_titres(ws: list[dict], fin: float, mots_cles: list[str]) -> tuple[str, str]:
    cles = {_norm(m) for m in mots_cles}
    # Découpe par proposition (ponctuation), puis groupes équilibrés de 4 mots au plus :
    # « Chaque détail / cache une vérité. » plutôt que « Chaque détail cache une / vérité. »
    props, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        if w["t"].rstrip().endswith((".", ",", "?", "!", ";", ":")) or i == len(ws) - 1:
            props.append(cur)
            cur = []
    groupes = []
    for pr in props:
        n = -(-len(pr) // 4)
        base, reste = divmod(len(pr), n)
        tailles = [base] * (n - reste) + [base + 1] * reste  # les groupes les plus longs à la fin
        k = 0
        for t in tailles:
            groupes.append(pr[k:k + t])
            k += t
    divs, js = [], []
    for k, g in enumerate(groupes):
        s = g[0]["s"]
        e = groupes[k + 1][0]["s"] if k + 1 < len(groupes) else fin
        txt = " ".join(f"<em>{html.escape(w['t'])}</em>" if w["n"] in cles else html.escape(w["t"]) for w in g)
        divs.append(f'<div id="st{k}" class="clip st" data-start="{s:.2f}" data-duration="{max(0.4, e - s):.2f}" data-track-index="5">'
                    f'<span id="st{k}-t" class="da-caption" style="display:block">{txt}</span></div>')
        js.append(f'tl.fromTo("#st{k}-t", {{opacity: 0, y: 12}}, {{opacity: 1, y: 0, duration: 0.22, ease: "power2.out"}}, {s:.2f});')
    return "\n      ".join(divs), "\n      ".join(js)


# ---------------------------------------------------------------- projet complet
def compiler(sb: dict, sb_dir: pathlib.Path, out: pathlib.Path) -> dict:
    voix = (sb_dir / sb["voix"]).resolve()
    ws = mots(sb_dir / sb["transcription"], sb.get("texte"))
    fin_audio = ws[-1]["e"]
    plans = caler(sb, ws, fin_audio)
    total = plans[-1]["fin"]

    (out / "compositions").mkdir(parents=True, exist_ok=True)
    (out / "assets").mkdir(exist_ok=True)
    shutil.copyfile(voix, out / "assets" / ("voix" + voix.suffix))
    if any(p.get("decor") == "archiviste" for p in sb["plans"]):  # image officielle, copiée telle quelle
        shutil.copyfile(D.ROOT_DEPOT / "archiviste" / "references" / "Character_FullBody_v1.jpg", out / D.ARCHIVISTE_ASSET)
    (out / "assets" / "da.css").write_text(DA_CSS)
    hosts = []
    for pl in plans:
        if pl.get("decor") == "illustration":  # image générée, copiée telle quelle
            src = (sb_dir / pl["image"]).resolve()
            (out / "assets" / "plans").mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, out / "assets" / "plans" / f"{pl['id']}{src.suffix}")
        (out / "compositions" / f"{pl['id']}.html").write_text(compiler_plan(pl, sb, ws))
        hosts.append(f'<div id="{pl["id"]}" data-composition-id="{pl["id"]}" data-composition-src="compositions/{pl["id"]}.html" '
                     f'data-start="{pl["debut"]:.2f}" data-duration="{pl["duree"]:.2f}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
    st_html, st_js = sous_titres(ws, total, sb.get("mots_cles", []))
    index = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style id="da-inline">
{DA_CSS}
    </style>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--charbon); }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      .st {{ position: absolute; left: 150px; top: 1110px; width: 740px; z-index: 40; }}
      .st .da-caption {{ text-shadow: 0 2px 14px rgba(16, 17, 19, 0.95); }}
      #fx-vignette {{ position: absolute; inset: 0; z-index: 50; pointer-events: none;
        background: radial-gradient(ellipse 80% 70% at 50% 45%, rgba(16, 17, 19, 0) 55%, rgba(16, 17, 19, 0.7) 100%); }}
      #fx-grain {{ position: absolute; inset: 0; z-index: 51; pointer-events: none; opacity: 0.07;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }}
    </style>
  </head>
  <body>
    <!-- Généré par engine/compiler.py depuis le storyboard : modifier le storyboard puis recompiler. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="1080" data-height="1920">
      {chr(10).join("      " + h for h in hosts).strip()}
      <audio id="voix" class="clip" src="assets/voix{voix.suffix}" data-start="0" data-duration="{fin_audio + 0.1:.2f}" data-track-index="9" data-volume="1"></audio>
      <div data-track-kind="captions">
      {st_html}
      </div>
      <div id="fx-vignette" data-layout-ignore></div>
      <div id="fx-grain" data-layout-ignore></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {st_js}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (out / "index.html").write_text(index)
    resume = [{"id": p["id"], "debut": round(p["debut"], 2), "duree": p["duree"], "decor": p["decor"], "ancre": p["ancre"]} for p in plans]
    (out / "plans.json").write_text(json.dumps(resume, ensure_ascii=False, indent=2))
    return {"duree": round(total, 2), "plans": resume}
