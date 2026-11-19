#!/usr/bin/env python3
"""DOSSIER 00 — moteur de vidéos ÉNIGMES v2 (TikTok / Reels, 35–50 s) : fond clair, rythme vif, bruitages.

  python3 scripts/enigme.py <enigme.json> <projet> [--render] [--qualite delivery]

Le fichier enigme.json décrit : le hook, l'ouverture (enquête criminelle : crime, chrono 30 s, détail),
les segments (scènes avec zooms sur les indices, suspects, question) ancrés sur les mots de la voix,
les images, les sons, et les poses de l'Archiviste (médaillon en bas à gauche toute la vidéo).
Exemple complet : dossiers/ENIGME-002/enigme.json. (Ancien moteur fond sombre : scripts/enigme_v1.py.)

Sons automatiques (bibliotheque/sons/) : woosh à chaque changement de segment, impact sur chaque ligne
du hook et chaque bandeau, tic-tac pendant le chrono, montée de tension avant la question, ding sur
l'appel à commenter, nappe musicale sous toute la vidéo. Sons propres à l'énigme : clé "sons".
"""
import argparse
import html
import json
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine.compiler import sous_titres  # noqa: E402
from engine.storyboard import mots, trouver  # noqa: E402
from engine.style import DA_CSS  # noqa: E402

CLI = ["node", str(ROOT / ".claude/skills/hyperframes/scripts/plugin-cli.mjs")]
ENV = dict(os.environ, HYPERFRAMES_TELEMETRY="0", DO_NOT_TRACK="1")
SONS = ROOT / "bibliotheque" / "sons"
# Fond générique réutilisable (Blender, blender/fond_bureau_enquete.py) : réglages validés pour la lisibilité du texte
FOND_DEFAUT = {"image": "bibliotheque/fonds/bureau-enquete.png", "flou": 11, "voile": 0.4, "lumiere": 1.35}


def E(t):
    """Échappe et colle la ponctuation haute française (« coupable ? » ne se coupe jamais)."""
    t = html.escape(t)
    for p in ("?", "!", ":", ";", "»"):
        t = t.replace(" " + p, " " + p)
    return t.replace("« ", "« ")


class TL:
    """Seule la 1re animation d'un élément fixe son état de départ ; les suivantes
    (immediateRender: false) ne s'appliquent qu'à leur moment."""

    def __init__(self):
        self.l, self.vus = [], set()

    def ft(self, sel, a, b, t, d, ease="power2.out"):
        b = dict(b, duration=round(max(d, 0.01), 3), ease=ease)
        if sel in self.vus:
            b["immediateRender"] = False
        self.vus.add(sel)
        self.l.append(f'tl.fromTo("{sel}", {json.dumps(a)}, {json.dumps(b)}, {max(t, 0):.3f});')

    def js(self):
        return "\n      ".join(self.l)


class Mix:
    """Pistes audio : chaque son est un <audio> calé dans le temps."""

    def __init__(self, out):
        self.out, self.items, self.n = out, [], 0

    def add(self, fichier, t, vol=0.6, duree=None):
        src = pathlib.Path(fichier)
        if not src.exists():
            return
        nom = f"son-{src.stem}{src.suffix}"
        dst = self.out / "assets" / nom
        if not dst.exists():
            shutil.copyfile(src, dst)
        if duree is None:
            duree = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                          str(src)], capture_output=True, text=True).stdout or 1)
        self.n += 1
        self.items.append(f'<audio id="a{self.n}" class="clip" src="assets/{nom}" data-start="{max(t, 0):.2f}" '
                          f'data-duration="{duree:.2f}" data-track-index="{10 + self.n % 6}" data-volume="{vol}"></audio>')

    def html(self):
        return "\n      ".join(self.items)


FLECHES = {"sortant": "↗", "entrant": "↙"}


def telephone_html(ident, t):
    """Écran-liste horodaté (journal d'appels, panneau des marées, registre…) :
    {"icone", "titre", "date", "appels": [{heure, nom, info, sens?, duree?}]}."""
    rows = "".join(f'<div class="tel-r"><span class="tel-hr">{E(a["heure"])}</span><span class="tel-n">{E(a["nom"])}'
                   f'<small>{E(a.get("info", ""))}</small></span><span class="tel-d">{FLECHES.get(a.get("sens"), "")} '
                   f'{E(a.get("duree", ""))}</span></div>' for a in t["appels"])
    return (f'<div id="{ident}" class="tel"><div class="tel-h"><span>{E(t.get("icone", "📞"))} {E(t.get("titre", "APPELS RÉCENTS"))}</span>'
            f'<span>{E(t.get("date", ""))}</span></div>{rows}</div>')


def horloge(i, x, y, taille, h, m, total, tl):
    """Horloge d'horloger animée : trotteuse qui avance d'un cran par seconde."""
    tl.ft(f"#hz-s{i}", {"rotation": 0}, {"rotation": 6 * int(total)}, 0, total, f"steps({int(total)})")
    tl.ft(f"#hz-m{i}", {"rotation": m * 6}, {"rotation": m * 6 + total / 10}, 0, total, "none")
    return (f'<div class="hz" style="left:{x}px;top:{y}px;width:{taille}px;height:{taille}px">'
            + "".join(f'<i class="hz-g" style="transform:rotate({k * 30}deg)"></i>' for k in range(12))
            + f'<b class="hz-a hz-h" style="transform:rotate({(h % 12) * 30 + m / 2}deg)"></b>'
            f'<b id="hz-m{i}" class="hz-a hz-m"></b><b id="hz-s{i}" class="hz-a hz-s"></b><u></u></div>')


def theme_fond(sp, d, out, tl, total):
    """Fond en rapport avec l'énigme : image du lieu floutée et éclaircie (lisibilité) + décor animé.
    "fond": {"image": "<clé images>", "flou": 7, "voile": 0.5, "decor": "horloges"}"""
    f = sp.get("fond", FOND_DEFAUT)  # sans clé "fond" : bureau d'enquête générique ; "fond": false pour l'ancien papier
    if not f:
        return "", ""
    from PIL import Image, ImageEnhance, ImageFilter
    chemin = sp["images"].get(f["image"], f["image"])  # image de l'épisode, ou fond générique de bibliotheque/fonds/
    src = Image.open(ROOT / chemin if chemin.startswith(("archiviste/", "bibliotheque/")) else d / chemin).convert("RGB")
    w, h = src.size
    k = max(1080 / w, 1920 / h)
    src = src.resize((round(w * k), round(h * k)), Image.LANCZOS)
    l, t = (src.width - 1080) // 2, (src.height - 1920) // 2
    src = src.crop((l, t, l + 1080, t + 1920)).filter(ImageFilter.GaussianBlur(f.get("flou", 7)))
    src = ImageEnhance.Color(ImageEnhance.Brightness(src).enhance(f.get("lumiere", 1.45))).enhance(1.25)
    src = Image.blend(src, Image.new("RGB", src.size, (246, 228, 196)), f.get("voile", 0.35))  # voile chaud
    src.save(out / "assets" / "fond-theme.jpg", quality=90)
    tl.ft("#fond-img", {"scale": 1.0}, {"scale": 1.08}, 0, total, "none")
    html_ = '<div id="fond-t" data-layout-ignore><img id="fond-img" src="assets/fond-theme.jpg" alt=""></div>'
    css = ("#fond-t { position: absolute; inset: 0; overflow: hidden; } #fond-img { width: 100%; height: 100%; object-fit: cover; }\n"
           "      #grille { opacity: 0.18 !important; }")
    if f.get("decor") == "horloges":
        html_ += ('<div id="hz-l" data-layout-ignore>' + horloge(0, 40, 120, 150, 11, 5, total, tl)
                  + horloge(1, 880, 1500, 150, 11, 5, total, tl) + '</div>')
        css += ("\n      #hz-l { position: absolute; inset: 0; }"
                "\n      .hz { position: absolute; border-radius: 50%; background: #fbf7ee; border: 7px solid #6b4a24;"
                " box-shadow: 0 0 0 4px #d6a64a, 0 10px 24px rgba(16,17,19,0.35); opacity: 0.92; }"
                "\n      .hz-g { position: absolute; left: 50%; top: 4%; width: 4px; height: 12%; margin-left: -2px; background: #101113; transform-origin: 50% 383%; }"
                "\n      .hz-a { position: absolute; left: 50%; bottom: 50%; transform-origin: 50% 100%; border-radius: 3px; }"
                "\n      .hz-h { width: 8px; height: 26%; margin-left: -4px; background: #101113; }"
                "\n      .hz-m { width: 6px; height: 38%; margin-left: -3px; background: #101113; }"
                "\n      .hz-s { width: 3px; height: 42%; margin-left: -1.5px; background: #9e2929; }"
                "\n      .hz u { position: absolute; left: 50%; top: 50%; width: 14px; height: 14px; margin: -7px; border-radius: 50%; background: #9e2929; }")
    if f.get("decor") == "pluie":  # nuit d'orage : rideau de pluie qui tombe en continu (sans flash)
        tl.ft("#pluie", {"backgroundPosition": "0px 0px"}, {"backgroundPosition": f"-{int(total * 260)}px {int(total * 1400)}px"},
              0, total, "none")
        stries = "".join(f"%3Cline x1='{x}' y1='{y}' x2='{x - 9}' y2='{y + 46}'/%3E"
                         for x, y in ((20, 10), (70, 120), (130, 40), (180, 190), (40, 230), (110, 170), (160, 270), (90, 300)))
        html_ += '<div id="pluie" data-layout-ignore></div>'
        css += ("\n      #pluie { position: absolute; inset: 0; opacity: 0.55; background-image: url(\"data:image/svg+xml,"
                "%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='340'%3E%3Cg stroke='%23f7f1e3' stroke-width='3' "
                f"stroke-linecap='round' opacity='0.8'%3E{stries}%3C/g%3E%3C/svg%3E\"); background-size: 200px 340px; }}")
    return html_, css


def build(spec_path: pathlib.Path, out: pathlib.Path):
    sp = json.loads(spec_path.read_text(encoding="utf-8"))
    d = spec_path.parent
    ws = mots(d / sp["transcription"], (d / sp["script"]).read_text(encoding="utf-8"))
    fin_voix = ws[-1]["e"]
    total = round(fin_voix + float(sp.get("queue", 1.8)), 2)
    t_mot = lambda phrase: ws[trouver(ws, phrase, 0)]["s"]  # noqa: E731

    (out / "assets").mkdir(parents=True, exist_ok=True)
    for f in set(sp["images"].values()):
        shutil.copyfile(ROOT / f if f.startswith(("archiviste/", "bibliotheque/")) else d / f,
                        out / "assets" / pathlib.Path(f).name)
    voix = d / sp["voix"]
    shutil.copyfile(voix, out / "assets" / ("voix" + voix.suffix))
    img = lambda k: "assets/" + pathlib.Path(sp["images"][k]).name  # noqa: E731
    tl, mix, parts, muets = TL(), Mix(out), [], []
    fond_html, fond_css = theme_fond(sp, d, out, tl, total)

    segs = sp["segments"]
    debuts = [0.0] + [max(0.0, t_mot(s["ancre"]) - 0.12) for s in segs]
    fins = debuts[1:] + [total]

    # ------------------------------------------------------------- HOOK (punch + impacts)
    hk = sp["hook"]
    h1 = debuts[1]
    lignes = []
    for i, L in enumerate(hk["lignes"]):
        t = 0.0 if i == 0 else max(0.0, t_mot(L["mot"]) - 0.06)
        cls = "hk-l" + {"ambre": " hk-a", "rouge": " hk-r"}.get(L.get("accent"), "")
        lignes.append(f'<div id="hk{i}" class="{cls}">{E(L["texte"])}</div>')
        tl.ft(f"#hk{i}", {"opacity": 0, "scale": 1.8, "rotation": -4 if i % 2 else 4},
              {"opacity": 1, "scale": 1, "rotation": 0}, t, 0.22, "back.out(1.6)" if i else "power3.out")
        if i:
            mix.add(SONS / "impact.mp3", t, 0.7)
    parts.append(f'<div id="hook" class="clip" data-start="0" data-duration="{h1:.2f}" data-track-index="1">'
                 f'<div id="hook-in">{"".join(lignes)}</div></div>')
    tl.ft("#hook-in", {"scale": 1}, {"scale": 1.1}, 0, max(0.5, h1), "power1.in")
    muets.append((0, h1))

    chrono = None
    for k, (s, t0, t1) in enumerate(zip(segs, debuts[1:], fins[1:])):
        sid, dur = f"s{k}", t1 - t0
        mix.add(SONS / "woosh.mp3", t0 - 0.15, 0.55)
        ban = ""
        if s.get("bandeau"):
            ban = f'<div id="{sid}-ban" class="ban"><span>{E(s["bandeau"])}</span></div>'
            tl.ft(f"#{sid}-ban", {"opacity": 0, "scale": 1.6, "rotation": -6}, {"opacity": 1, "scale": 1, "rotation": -2},
                  t0 + 0.05, 0.25, "back.out(2)")
            mix.add(SONS / "impact.mp3", t0 + 0.1, 0.45)
        inner = ""

        if s["type"] == "ouverture":  # enquête criminelle : crime → chrono 30 s → un seul détail
            inner = (f'<div id="{sid}-card" class="card"><img id="{sid}-img" src="{img(s["image"])}" alt=""></div>'
                     f'<div id="{sid}-chrono" class="chrono"><span class="ch-ic">⏱</span>30 s</div>'
                     f'<div id="{sid}-det" class="det">UN SEUL <b>DÉTAIL</b></div>')
            tl.ft(f"#{sid}-card", {"opacity": 0, "x": 300, "rotation": 6}, {"opacity": 1, "x": 0, "rotation": -1.5}, t0, 0.35, "power3.out")
            tl.ft(f"#{sid}-img", {"scale": 1.0}, {"scale": 1.15}, t0, dur, "none")
            tc = t_mot(s["chrono_mot"])
            tl.ft(f"#{sid}-chrono", {"opacity": 0, "scale": 2}, {"opacity": 1, "scale": 1}, tc, 0.25, "back.out(2)")
            mix.add(SONS / "impact.mp3", tc, 0.5)
            td = t_mot(s["detail_mot"])
            tl.ft(f"#{sid}-card", {"opacity": 1}, {"opacity": 0.25}, td - 0.1, 0.25)
            tl.ft(f"#{sid}-det", {"opacity": 0, "scale": 2.2}, {"opacity": 1, "scale": 1}, td, 0.3, "back.out(1.8)")
            mix.add(SONS / "impact.mp3", td, 0.6)
            i = trouver(ws, s["chrono_mot"], 0)  # sous-titres coupés dès le début de la phrase du chrono :
            while i > 0 and not ws[i - 1]["t"].rstrip("»  ").endswith((".", "!", "?", "…")):
                i -= 1                             # le gros chrono puis « UN SEUL DÉTAIL » occupent leur zone
            muets.append((ws[i]["s"] - 0.05, t1))
            chrono = {"t_affiche": tc}

        elif s["type"] == "scene":
            imgs = s.get("images", [{"image": s.get("image")}])
            tags = ""
            for j, tg in enumerate(s.get("etiquettes", [])):
                tags += f'<div id="{sid}-tg{j}" class="tag" style="left:{tg["x"]}px;top:{tg["y"]}px">{E(tg["texte"])}</div>'
                tt = t_mot(tg["mot"])
                tl.ft(f"#{sid}-tg{j}", {"opacity": 0, "scale": 1.8}, {"opacity": 1, "scale": 1}, tt, 0.22, "back.out(2)")
                mix.add(SONS / "impact.mp3", tt, 0.35)
            cards = ""
            for j, im in enumerate(imgs):
                tj = t0 if j == 0 else t_mot(im["mot"]) - 0.1
                tfin = t1 if j == len(imgs) - 1 else t_mot(imgs[j + 1]["mot"]) - 0.1
                if im.get("telephone"):
                    media = telephone_html(f"{sid}-i{j}", im["telephone"])
                else:
                    pos = f' style="object-position:{im["position"]}"' if im.get("position") else ""
                    media = f'<img id="{sid}-i{j}" src="{img(im["image"])}" alt=""{pos}>'
                cercles = ""
                tl.ft(f"#{sid}-c{j}", {"opacity": 0, "x": 320, "rotation": 7}, {"opacity": 1, "x": 0, "rotation": -1.5 + j * 2},
                      tj, 0.35, "power3.out")
                tl.ft(f"#{sid}-i{j}", {"scale": 1.0, "x": 0, "y": 0}, {"scale": 1.12, "x": 0, "y": 0}, tj, tfin - tj, "none")
                if j:
                    mix.add(SONS / "woosh.mp3", tj - 0.1, 0.45)
                for zi, z in enumerate(im.get("zooms", [])):  # punch sur l'indice
                    tz = t_mot(z["mot"])
                    tl.ft(f"#{sid}-i{j}", {"scale": 1.12, "x": 0, "y": 0}, {"scale": z.get("echelle", 1.9), "x": z["dx"], "y": z["dy"]},
                          tz, 0.35, "power3.out")
                    tl.ft(f"#{sid}-i{j}", {"scale": z.get("echelle", 1.9), "x": z["dx"], "y": z["dy"]},
                          {"scale": z.get("echelle", 1.9) + 0.15, "x": z["dx"], "y": z["dy"]}, tz + 0.35,
                          z.get("tenue", max(0.5, tfin - tz - 0.35)), "none")  # tient jusqu'à l'image suivante
                    mix.add(SONS / "woosh.mp3", tz - 0.08, 0.4)
                    if z.get("cercle"):
                        cx, cy, r = z["cercle"][:3]
                        ry = z["cercle"][3] if len(z["cercle"]) > 3 else r * 0.7
                        cercles += (f'<svg class="cercle" viewBox="0 0 860 484"><ellipse id="{sid}-ce{j}-{zi}" cx="{cx}" cy="{cy}" '
                                    f'rx="{r}" ry="{ry}" pathLength="1"/></svg>')
                        tl.ft(f"#{sid}-ce{j}-{zi}", {"strokeDashoffset": 1}, {"strokeDashoffset": 0}, tz + 0.4, 0.5, "power2.inOut")
                cards += f'<div id="{sid}-c{j}" class="card">{media}{cercles}</div>'
            inner = cards + tags

        elif s["type"] == "suspects":
            sus, preuves = "", ""
            for j, su in enumerate(s["suspects"]):
                x = 70 + j * 320
                bulle = f'<div id="{sid}-b{j}" class="bulle">{E(su["bulle"])}</div>' if su.get("bulle") else ""
                sus += (f'<div id="{sid}-c{j}" class="sus" style="left:{x}px"><div class="sus-img"><img src="{img(su["image"])}" alt=""></div>'
                        f'<div class="sus-nom">{E(su["nom"])}</div>{bulle}</div>')
                tl.ft(f"#{sid}-c{j}", {"opacity": 0, "y": 260, "rotation": 8 - 8 * j}, {"opacity": 0.55, "y": 0, "rotation": -2 + 2 * j},
                      t0 + 0.12 * j, 0.35, "back.out(1.4)")
                ts = t_mot(su["ancre"])
                tl.ft(f"#{sid}-c{j}", {"opacity": 0.55, "scale": 1}, {"opacity": 1, "scale": 1.1}, ts - 0.1, 0.22, "back.out(2)")
                mix.add(SONS / "woosh.mp3", ts - 0.15, 0.35)
                if su.get("bulle"):
                    tl.ft(f"#{sid}-b{j}", {"opacity": 0, "scale": 0.4}, {"opacity": 1, "scale": 1}, ts + 0.3, 0.22, "back.out(2)")
                if su.get("preuve"):  # pièce à conviction du suspect (photo, écran…) : carte qui passe devant
                    pv = su["preuve"]
                    tp = t_mot(pv["mot"]) - 0.1
                    tq = (t_mot(s["suspects"][j + 1]["ancre"]) - 0.15) if j + 1 < len(s["suspects"]) else t1 - 0.1
                    media = (telephone_html(f"{sid}-pi{j}", pv["telephone"]) if pv.get("telephone")
                             else f'<img id="{sid}-pi{j}" src="{img(pv["image"])}" alt="">')
                    cer = ""
                    tl.ft(f"#{sid}-p{j}", {"opacity": 0, "y": 500, "rotation": 6}, {"opacity": 1, "y": 0, "rotation": 1.5}, tp, 0.35, "back.out(1.4)")
                    z = pv.get("zoom")
                    tz = t_mot(z["mot"]) if z else tq
                    tl.ft(f"#{sid}-pi{j}", {"scale": 1, "x": 0, "y": 0}, {"scale": 1.08, "x": 0, "y": 0}, tp, max(0.3, tz - tp), "none")
                    mix.add(SONS / "woosh.mp3", tp - 0.1, 0.45)
                    if su.get("bulle"):  # la bulle s'efface devant la pièce à conviction
                        tl.ft(f"#{sid}-b{j}", {"opacity": 1}, {"opacity": 0}, tp, 0.15)
                    if z:
                        tl.ft(f"#{sid}-pi{j}", {"scale": 1.08, "x": 0, "y": 0}, {"scale": z["echelle"], "x": z["dx"], "y": z["dy"]}, tz, 0.35, "power3.out")
                        mix.add(SONS / "woosh.mp3", tz - 0.08, 0.4)
                        if z.get("cercle"):
                            cx, cy, rr = z["cercle"][:3]
                            ry = z["cercle"][3] if len(z["cercle"]) > 3 else rr * 0.7
                            cer = (f'<svg class="cercle" viewBox="0 0 860 484"><ellipse id="{sid}-pce{j}" cx="{cx}" cy="{cy}" rx="{rr}" '
                                   f'ry="{ry}" pathLength="1"/></svg>')
                            tl.ft(f"#{sid}-pce{j}", {"strokeDashoffset": 1}, {"strokeDashoffset": 0}, tz + 0.4, 0.5, "power2.inOut")
                    tl.ft(f"#{sid}-p{j}", {"opacity": 1}, {"opacity": 0}, tq, 0.2)
                    preuves += f'<div id="{sid}-p{j}" class="card preuve">{media}{cer}</div>'
                nxt = s["suspects"][j + 1]["ancre"] if j + 1 < len(s["suspects"]) else None
                if nxt:
                    tn = t_mot(nxt) - 0.1
                    tl.ft(f"#{sid}-c{j}", {"opacity": 1, "scale": 1.1}, {"opacity": 0.55, "scale": 1}, tn, 0.2)
                    if su.get("bulle"):
                        tl.ft(f"#{sid}-b{j}", {"opacity": 1}, {"opacity": 0}, tn, 0.15)
            inner = f'<div class="lineup">{sus}</div>{preuves}'

        elif s["type"] == "question":
            minis = "".join(f'<div class="mini"><img src="{img(k2)}" alt=""><span>{E(n)}</span></div>' for k2, n in s.get("rappel", []))
            inner = (f'<div id="{sid}-q" class="q">{E(s["texte"])}</div><div class="minis" id="{sid}-m">{minis}</div>'
                     f'<div id="{sid}-cta" class="cta">{E(s["cta"])}</div><div id="{sid}-logo" class="logo">DOSSIER 00</div>')
            tl.ft(f"#{sid}-q", {"opacity": 0, "scale": 2}, {"opacity": 1, "scale": 1}, t0, 0.28, "back.out(1.8)")
            mix.add(SONS / "montee.mp3", t0 - 2.6, 0.5)
            mix.add(SONS / "impact.mp3", t0, 0.8)
            tl.ft(f"#{sid}-m", {"opacity": 0, "y": 40}, {"opacity": 1, "y": 0}, t0 + 0.35, 0.3, "back.out(1.6)")
            tcta = t_mot(s["cta_ancre"])
            tl.ft(f"#{sid}-cta", {"opacity": 0, "scale": 1.6}, {"opacity": 1, "scale": 1}, tcta, 0.25, "back.out(2)")
            for r in range(3):
                tl.ft(f"#{sid}-cta", {"scale": 1}, {"scale": 1.07}, tcta + 0.6 + r * 0.8, 0.4, "sine.inOut")
                tl.ft(f"#{sid}-cta", {"scale": 1.07}, {"scale": 1}, tcta + 1.0 + r * 0.8, 0.4, "sine.inOut")
            mix.add(SONS / "ding.mp3", tcta, 0.7)
            tl.ft(f"#{sid}-logo", {"opacity": 0}, {"opacity": 1}, tcta + 0.6, 0.4)
            muets.append((t0, t1))
            if chrono:
                chrono["t_fin"] = t0

        parts.append(f'<div id="{sid}" class="clip seg" data-start="{t0:.2f}" data-duration="{dur:.2f}" data-track-index="1">'
                     f'{ban}{inner}</div>')

    # ------------------------------------------------------------- CHRONO 30 s (coin haut droit, tic-tac)
    chrono_html = ""
    if chrono and "t_fin" in chrono:
        td, tf = t_mot(sp["chrono_depart"]), chrono["t_fin"]
        chrono_html = (f'<div id="chr" class="clip" data-start="{td:.2f}" data-duration="{tf - td:.2f}" data-track-index="3">'
                       f'<div id="chr-in"><span class="ch-ic">⏱</span><span id="chr-n">30</span><span> s</span></div></div>')
        tl.ft("#chr-in", {"opacity": 0, "y": -30}, {"opacity": 1, "y": 0}, td, 0.25, "back.out(2)")
        tl.ft("#chr-n", {"innerText": 30}, {"innerText": 0, "snap": {"innerText": 1}}, td, tf - td, "none")
        tl.ft("#chr-in", {"color": "#101113"}, {"color": "#9e2929"}, tf - 6, 0.5)
        t = td
        while t < tf - 0.5:
            mix.add(SONS / "tictac.mp3", t, 0.22, min(10.0, tf - t))
            t += 10.0

    # ------------------------------------------------------------- SONS PROPRES À L'ÉNIGME + NAPPE
    for so in sp.get("sons", []):
        mix.add(d / so["fichier"], t_mot(so["mot"]) + so.get("decalage", 0), so.get("volume", 0.5), so.get("duree"))
    nappe = SONS / sp.get("nappe", "nappe-enquete.mp3")
    t = 0.0
    while t < total:
        mix.add(nappe, t, sp.get("volume_nappe", 0.16), min(30.0, total - t))
        t += 30.0

    # ------------------------------------------------------------- ARCHIVISTE (médaillon bas gauche)
    poses, plan = sp["archiviste"]["poses"], sp["archiviste"]["sequence"]
    imgs = "".join(f'<img id="ar-{p}" class="ar-p" src="{img(f)}" alt="" style="opacity:{1 if p == plan[0]["pose"] else 0}">'
                   for p, f in poses.items())
    cur = plan[0]["pose"]
    for st in plan[1:]:
        t = t_mot(st["mot"]) - 0.15
        if st["pose"] != cur:
            tl.ft(f"#ar-{cur}", {"opacity": 1}, {"opacity": 0}, t, 0.18)
            tl.ft(f"#ar-{st['pose']}", {"opacity": 0}, {"opacity": 1}, t, 0.18)
            tl.ft("#medaillon", {"scale": 1, "rotation": -3}, {"scale": 1.06, "rotation": -1}, t, 0.15, "power2.out")
            tl.ft("#medaillon", {"scale": 1.06, "rotation": -1}, {"scale": 1, "rotation": -3}, t + 0.15, 0.3, "back.out(2)")
            cur = st["pose"]
    tl.ft("#medaillon", {"opacity": 0, "x": -300, "rotation": -12}, {"opacity": 1, "x": 0, "rotation": -3}, 0.0, 0.4, "back.out(1.5)")
    archi = (f'<div id="medaillon"><div id="ar-in">{imgs}</div><div id="ar-nom">L\'ARCHIVISTE</div></div>')

    # ------------------------------------------------------------- SOUS-TITRES (pop)
    garde = [w for w in ws if not any(a <= w["s"] < b for a, b in muets)]
    st_html, st_js = sous_titres(garde, total, sp.get("mots_cles", []))
    st_js = st_js.replace("{opacity: 0, y: 12}", "{opacity: 0, scale: 1.35}").replace("{opacity: 1, y: 0, duration: 0.22, ease: \"power2.out\"}",
                                                                                     "{opacity: 1, scale: 1, duration: 0.16, ease: \"back.out(2)\"}")

    page = f"""<!doctype html>
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
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--ivoire); }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      /* fond clair : papier ivoire, halo ambre chaud, quadrillage de dossier */
      #fond {{ position: absolute; inset: 0; background:
        radial-gradient(ellipse 75% 50% at 50% 38%, rgba(214,166,74,0.38), rgba(214,166,74,0) 72%),
        radial-gradient(ellipse 120% 80% at 50% 110%, rgba(158,41,41,0.10), rgba(158,41,41,0) 60%),
        linear-gradient(180deg, #efe6d3, #e5ddcb 55%, #d9cdb4); }}
      #grille {{ position: absolute; inset: 0; opacity: 0.35;
        background-image: linear-gradient(rgba(16,17,19,0.06) 2px, transparent 2px), linear-gradient(90deg, rgba(16,17,19,0.06) 2px, transparent 2px);
        background-size: 60px 60px; }}
      .seg, #hook {{ position: absolute; inset: 0; }}
      #hook-in {{ position: absolute; left: 70px; top: 420px; width: 940px; text-align: center; }}
      .hk-l {{ font-family: var(--font-display); font-weight: 700; font-size: 128px; line-height: 1.1; text-transform: uppercase; color: var(--charbon); }}
      .hk-a {{ color: #b07d20; }} .hk-r {{ color: var(--rouge); }}
      .ban {{ position: absolute; left: 0; right: 0; top: 245px; text-align: center; z-index: 5; }}
      .ban span {{ display: inline-block; background: var(--rouge); color: var(--ivoire); font-family: var(--font-display); font-weight: 700;
        font-size: 48px; letter-spacing: 0.08em; padding: 6px 28px; text-transform: uppercase; box-shadow: 6px 6px 0 var(--charbon); }}
      .card {{ position: absolute; left: 110px; top: 350px; width: 860px; height: 484px; overflow: hidden; border: 8px solid #fbf7ee;
        box-shadow: 0 18px 40px rgba(16,17,19,0.35); background: var(--charbon); }}
      .card img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .tel {{ position: absolute; inset: 0; background: linear-gradient(180deg, #1b1c20, #101113); color: var(--ivoire);
        font-family: var(--font-display); padding: 26px 46px; }}
      .tel-h {{ display: flex; justify-content: space-between; font-family: var(--font-mono); font-size: 26px; color: var(--ambre);
        letter-spacing: 0.08em; border-bottom: 2px solid rgba(229,221,203,0.25); padding-bottom: 12px; margin-bottom: 8px; }}
      .tel-r {{ display: flex; align-items: center; height: 108px; border-bottom: 2px solid rgba(229,221,203,0.12); }}
      .tel-hr {{ font-family: var(--font-mono); font-weight: 700; font-size: 50px; width: 190px; }}
      .tel-n {{ flex: 1; font-weight: 700; font-size: 46px; text-transform: uppercase; line-height: 1; }}
      .tel-n small {{ display: block; font-family: var(--font-mono); font-weight: 400; font-size: 24px; color: rgba(229,221,203,0.65);
        text-transform: none; margin-top: 6px; }}
      .tel-d {{ font-family: var(--font-mono); font-size: 30px; color: rgba(229,221,203,0.8); }}
      .preuve {{ z-index: 8; top: 380px; }}
      .cercle {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
      .cercle ellipse {{ fill: none; stroke: var(--rouge); stroke-width: 7; stroke-dasharray: 1; }}
      .tag {{ position: absolute; font-family: var(--font-display); font-weight: 700; font-size: 44px; color: var(--ivoire); background: var(--charbon);
        padding: 4px 18px; text-transform: uppercase; z-index: 6; box-shadow: 5px 5px 0 var(--rouge); }}
      .chrono {{ position: absolute; left: 0; right: 0; top: 856px; text-align: center; font-family: var(--font-mono); font-weight: 700;
        font-size: 100px; color: var(--charbon); }}
      .ch-ic {{ font-size: 0.7em; margin-right: 10px; }}
      .det {{ position: absolute; left: 0; right: 0; top: 520px; text-align: center; font-family: var(--font-display); font-weight: 700;
        font-size: 120px; line-height: 1.1; color: var(--charbon); text-transform: uppercase; }}
      .det b {{ color: var(--rouge); display: block; font-size: 190px; }}
      #chr {{ position: absolute; inset: 0; }}
      #chr-in {{ position: absolute; right: 200px; top: 170px; font-family: var(--font-mono); font-weight: 700; font-size: 56px;
        color: var(--charbon); background: #fbf7ee; border: 4px solid var(--charbon); padding: 2px 16px; box-shadow: 5px 5px 0 var(--ambre); }}
      .lineup {{ position: absolute; left: 0; top: 340px; width: 1080px; height: 700px; }}
      .sus {{ position: absolute; top: 0; width: 300px; height: 640px; transform-origin: 50% 70%; }}
      .sus-img {{ position: absolute; left: 0; top: 0; width: 300px; height: 540px; overflow: hidden; border: 7px solid #fbf7ee;
        box-shadow: 0 14px 30px rgba(16,17,19,0.35); background: var(--ivoire); }}
      .sus-img img {{ width: 100%; height: 100%; object-fit: cover; }}
      .sus-nom {{ position: absolute; left: -10px; right: -10px; top: 555px; text-align: center; font-family: var(--font-display); font-weight: 700;
        font-size: 36px; color: var(--ivoire); background: var(--charbon); text-transform: uppercase; padding: 2px 0; }}
      .bulle {{ position: absolute; left: -16px; right: -16px; top: 380px; background: #fbf7ee; border: 4px solid var(--charbon); border-radius: 22px;
        padding: 10px 14px; font-family: var(--font-display); font-weight: 600; font-size: 30px; line-height: 1.15; color: var(--charbon); text-align: center; }}
      .q {{ position: absolute; left: 70px; top: 330px; width: 940px; text-align: center; font-family: var(--font-display); font-weight: 700;
        font-size: 112px; line-height: 1.08; text-transform: uppercase; color: var(--charbon); }}
      .minis {{ position: absolute; left: 120px; top: 610px; width: 840px; display: flex; justify-content: space-between; }}
      .mini {{ width: 250px; text-align: center; }}
      .mini img {{ width: 250px; height: 300px; object-fit: cover; border: 6px solid #fbf7ee; box-shadow: 0 10px 22px rgba(16,17,19,0.3); }}
      .mini span {{ display: block; margin-top: 8px; font-family: var(--font-display); font-weight: 700; font-size: 32px; color: var(--charbon); text-transform: uppercase; }}
      .cta {{ position: absolute; left: 400px; top: 1020px; width: 500px; text-align: center; background: var(--rouge); color: var(--ivoire);
        font-family: var(--font-display); font-weight: 700; font-size: 44px; line-height: 1.12; padding: 16px 18px; text-transform: uppercase;
        box-shadow: 7px 7px 0 var(--charbon); }}
      .logo {{ position: absolute; left: 400px; top: 1215px; width: 500px; text-align: center; font-family: var(--font-mono); font-size: 34px;
        letter-spacing: 0.3em; color: var(--charbon); }}
      /* Archiviste : médaillon (ses images restent intactes) */
      #medaillon {{ position: absolute; left: 34px; top: 1160px; width: 330px; height: 420px; z-index: 30; background: var(--charbon);
        border: 6px solid var(--ambre); border-radius: 26px; overflow: hidden; box-shadow: 0 16px 34px rgba(16,17,19,0.45); }}
      #ar-in {{ position: absolute; inset: 0; }}
      .ar-p {{ position: absolute; left: -20px; top: 0; width: 370px; height: 620px; object-fit: cover; object-position: 50% 0; }}
      #ar-nom {{ position: absolute; left: 0; right: 0; bottom: 0; text-align: center; background: var(--ambre); color: var(--charbon);
        font-family: var(--font-mono); font-weight: 700; font-size: 24px; letter-spacing: 0.18em; padding: 4px 0; }}
      .st {{ position: absolute; left: 130px; top: 990px; width: 820px; z-index: 40; }}
      .st .da-caption {{ color: var(--charbon); font-size: 72px; text-shadow: 0 0 10px #f3ecdc, 0 0 22px #f3ecdc, 3px 3px 0 #f3ecdc; }}
      .st .da-caption em {{ color: var(--rouge); }}
      {fond_css}
      #fx-grain {{ position: absolute; inset: 0; z-index: 51; pointer-events: none; opacity: 0.08;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }}
    </style>
  </head>
  <body>
    <!-- Généré par scripts/enigme.py depuis {E(spec_path.name)} : modifier le fichier d'énigme puis regénérer. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="1080" data-height="1920">
      <div id="fond" data-layout-ignore></div>
      <div id="grille" data-layout-ignore></div>
      {fond_html}
      {chr(10).join("      " + p for p in parts).strip()}
      {chrono_html}
      {archi}
      <audio id="voix" class="clip" src="assets/voix{voix.suffix}" data-start="0" data-duration="{fin_voix + 0.2:.2f}" data-track-index="9" data-volume="1"></audio>
      {mix.html()}
      <div data-track-kind="captions">
      {st_html}
      </div>
      <div id="fx-grain" data-layout-ignore></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {tl.js()}
      {st_js}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (out / "index.html").write_text(page, encoding="utf-8")
    return total, list(zip(["hook"] + [s["type"] for s in segs], debuts, fins))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("projet")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--qualite", default="delivery")
    a = ap.parse_args()
    out = pathlib.Path(a.projet).resolve()
    if not (out / "hyperframes.json").exists():
        subprocess.run(CLI + ["init", str(out), "--skip-skills", "--skill=hyperframes"], env=ENV, capture_output=True, check=True)
    total, segs = build(pathlib.Path(a.spec).resolve(), out)
    print(f"✓ {total} s → {out}")
    for typ, t0, t1 in segs:
        print(f"  {t0:6.2f}–{t1:6.2f}  {typ}")
    subprocess.run(CLI + ["check", "--json"], cwd=out, env=ENV, capture_output=True, text=True)
    chk = sorted((out / ".hyperframes/artifacts/checks").glob("*.json"), key=os.path.getmtime)[-1]
    dd = json.loads(chk.read_text())
    errs = [f for v in dd.values() if isinstance(v, dict) for f in v.get("findings", []) if f.get("severity") == "error"]
    for f in errs:
        print(f"  ✗ {f.get('code')}: {f.get('message', '')[:140]} [{f.get('text') or f.get('selector')}]")
    print(f"  contrôle : {len(errs)} erreur(s)")
    if a.render and not errs:
        (out / "export").mkdir(exist_ok=True)
        dest = out / "export" / "final.mp4"
        dest.unlink(missing_ok=True)
        subprocess.run(CLI + ["render", "--quality", a.qualite, "-o", str(dest)], cwd=out, env=ENV, check=True, capture_output=True)
        print(f"✓ {dest}")


if __name__ == "__main__":
    main()
