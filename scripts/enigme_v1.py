#!/usr/bin/env python3
"""DOSSIER 00 — moteur de vidéos ÉNIGMES (format TikTok / Reels, 30–50 s).

  python3 scripts/enigme_v1.py <enigme.json> <projet> [--render] [--qualite delivery]

Le fichier enigme.json décrit : le format (situation / enquete / criminel), le hook, les segments
(scène, suspects, question) ancrés sur les mots de la voix, les images, et les poses de l'Archiviste
qui reste dans le coin de l'écran toute la vidéo. Voir dossiers/ENIGME-001/enigme.json.
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
def E(t):
    """Échappe et colle la ponctuation haute française (« coupable ? » ne se coupe jamais)."""
    t = html.escape(t)
    for p in ("?", "!", ":", ";", "»"):
        t = t.replace(" " + p, "\u00a0" + p)
    return t.replace("« ", "«\u00a0")


class TL:
    """Seule la 1re animation d'un élément fixe son état de départ ; les suivantes
    (immediateRender: false) ne s'appliquent qu'à leur moment."""
    def __init__(self):
        self.l, self.vus = [], set()

    def ft(self, sel, a, b, t, d, ease="power2.out"):
        b = dict(b, duration=round(d, 3), ease=ease)
        if sel in self.vus:
            b["immediateRender"] = False
        self.vus.add(sel)
        self.l.append(f'tl.fromTo("{sel}", {json.dumps(a)}, {json.dumps(b)}, {t:.3f});')

    def js(self):
        return "\n      ".join(self.l)


def build(spec_path: pathlib.Path, out: pathlib.Path):
    sp = json.loads(spec_path.read_text(encoding="utf-8"))
    d = spec_path.parent
    ws = mots(d / sp["transcription"], (d / sp["script"]).read_text(encoding="utf-8"))
    fin_voix = ws[-1]["e"]
    total = round(fin_voix + float(sp.get("queue", 1.6)), 2)
    t_mot = lambda phrase, apres=0: ws[trouver(ws, phrase, apres)]["s"]  # noqa: E731

    (out / "assets").mkdir(parents=True, exist_ok=True)
    for f in set(sp["images"].values()):
        shutil.copyfile(d / f, out / "assets" / pathlib.Path(f).name)
    voix = d / sp["voix"]
    shutil.copyfile(voix, out / "assets" / ("voix" + voix.suffix))
    img = lambda k: "assets/" + pathlib.Path(sp["images"][k]).name  # noqa: E731

    segs = sp["segments"]
    debuts = [0.0] + [max(0.0, t_mot(s["ancre"]) - 0.1) for s in segs]
    fins = debuts[1:] + [total]
    tl, parts, muets = TL(), [], []

    # ------------------------------------------------------------- HOOK
    h0, h1 = 0.0, debuts[1]
    hk = sp["hook"]
    lignes = []
    if hk.get("type") == "compte":  # 1… 2… 3… raté.
        for i, L in enumerate(hk["lignes"]):
            t = 0.0 if i == 0 else t_mot(L["mot"])
            cls = "hk-rate" if L.get("rate") else "hk-chiffre"
            lignes.append(f'<div id="hk{i}" class="{cls}">{E(L["texte"])}</div>')
            tl.ft(f"#hk{i}", {"opacity": 0, "scale": 1.6}, {"opacity": 1, "scale": 1}, t, 0.22, "power3.out")
            if i + 1 < len(hk["lignes"]) and not hk["lignes"][i + 1].get("rate"):
                tl.ft(f"#hk{i}", {"opacity": 1}, {"opacity": 0}, t_mot(hk["lignes"][i + 1]["mot"]) - 0.05, 0.08, "none")
    else:
        for i, L in enumerate(hk["lignes"]):
            t = 0.0 if i == 0 else max(0.0, t_mot(L["mot"]) - 0.05)
            cls = "hk-l" + (" hk-a" if L.get("accent") == "ambre" else " hk-r" if L.get("accent") == "rouge" else "")
            lignes.append(f'<div id="hk{i}" class="{cls}">{E(L["texte"])}</div>')
            tl.ft(f"#hk{i}", {"opacity": 0, "scale": 1.35}, {"opacity": 1, "scale": 1}, t, 0.25, "power3.out")
    parts.append(f'<div id="hook" class="clip" data-start="{h0:.2f}" data-duration="{h1 - h0:.2f}" data-track-index="1">'
                 f'<div id="hook-in" class="hk-{hk.get("type", "texte")}">{"".join(lignes)}</div></div>')
    tl.ft("#hook-in", {"scale": 1}, {"scale": 1.06}, 0, max(0.5, h1 - 0.1), "none")
    muets.append((h0, h1))

    # ------------------------------------------------------------- SEGMENTS
    for k, (s, t0, t1) in enumerate(zip(segs, debuts[1:], fins[1:] if len(fins) > 1 else [total])):
        sid, dur = f"s{k}", t1 - t0
        ban = f'<div id="{sid}-ban" class="ban"><span>{E(s.get("bandeau", ""))}</span></div>' if s.get("bandeau") else ""
        inner = ""
        if s["type"] == "scene":
            tags = ""
            for j, tg in enumerate(s.get("etiquettes", [])):
                tags += f'<div id="{sid}-tg{j}" class="tag" style="left:{tg["x"]}px;top:{tg["y"]}px">{E(tg["texte"])}</div>'
                tl.ft(f"#{sid}-tg{j}", {"opacity": 0, "y": 10}, {"opacity": 1, "y": 0}, t_mot(tg["mot"]), 0.3)
            inner = (f'<div id="{sid}-card" class="card"><img id="{sid}-img" src="{img(s["image"])}" alt="">'
                     f'{tags}</div>')
            tl.ft(f"#{sid}-card", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, t0, 0.45, "power3.out")
            tl.ft(f"#{sid}-img", {"scale": 1.0}, {"scale": 1.14}, t0, dur, "none")
        elif s["type"] == "suspects":
            cards = ""
            for j, su in enumerate(s["suspects"]):
                x = 120 + j * 285
                slate = (f'<div id="{sid}-sl{j}" class="slate">{E(su["ardoise"])}</div>' if su.get("ardoise") else "")
                cards += (f'<div id="{sid}-c{j}" class="sus" style="left:{x}px">'
                          f'<div class="sus-img"><img src="{img(su["image"])}" alt=""></div>{slate}'
                          f'<div class="sus-nom">{E(su["nom"])}</div></div>')
                tl.ft(f"#{sid}-c{j}", {"opacity": 0, "y": 40}, {"opacity": 0.45, "y": 0}, t0 + 0.15 * j, 0.4, "power3.out")
                ts = t_mot(su["ancre"])
                tl.ft(f"#{sid}-c{j}", {"opacity": 0.45, "scale": 1}, {"opacity": 1, "scale": 1.06}, ts - 0.1, 0.3)
                nxt = s["suspects"][j + 1]["ancre"] if j + 1 < len(s["suspects"]) else None
                if nxt:
                    tl.ft(f"#{sid}-c{j}", {"opacity": 1, "scale": 1.06}, {"opacity": 0.45, "scale": 1}, t_mot(nxt) - 0.1, 0.3)
                if su.get("ardoise"):
                    tl.ft(f"#{sid}-sl{j}", {"clipPath": "inset(0 100% 0 0)"}, {"clipPath": "inset(0 0% 0 0)"},
                          t_mot(su["ardoise"].split()[0]), 1.2, "steps(30)")
            inner = f'<div class="lineup">{cards}</div>'
        elif s["type"] == "question":
            minis = "".join(f'<div class="mini"><img src="{img(k2)}" alt=""><span>{E(n)}</span></div>'
                            for k2, n in s.get("rappel", []))
            tq = t0
            inner = (f'<div id="{sid}-q" class="q">{E(s["texte"])}</div><div class="minis" id="{sid}-m">{minis}</div>'
                     f'<div id="{sid}-cd" class="cd"><svg viewBox="0 0 200 200"><circle id="{sid}-ring" cx="100" cy="100" r="88" '
                     f'pathLength="1"/></svg><span id="{sid}-n3">3</span><span id="{sid}-n2">2</span><span id="{sid}-n1">1</span></div>'
                     f'<div id="{sid}-cta" class="cta">{E(s["cta"])}</div><div id="{sid}-logo" class="logo">DOSSIER 00</div>')
            tl.ft(f"#{sid}-q", {"opacity": 0, "scale": 1.3}, {"opacity": 1, "scale": 1}, tq, 0.3, "power3.out")
            tl.ft(f"#{sid}-m", {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0}, tq + 0.4, 0.4)
            tc = t_mot(s["compte_ancre"]) if s.get("compte_ancre") else tq + 0.8
            tl.ft(f"#{sid}-ring", {"strokeDashoffset": 0}, {"strokeDashoffset": 1}, tc, 3.0, "none")
            for i, n in enumerate((3, 2, 1)):
                tl.ft(f"#{sid}-n{n}", {"opacity": 0, "scale": 1.5}, {"opacity": 1, "scale": 1}, tc + i, 0.2, "power3.out")
                tl.ft(f"#{sid}-n{n}", {"opacity": 1}, {"opacity": 0}, tc + i + 0.85, 0.12, "none")
            tcta = t_mot(s["cta_ancre"]) if s.get("cta_ancre") else tc + 3
            tl.ft(f"#{sid}-cta", {"opacity": 0, "scale": 1.25}, {"opacity": 1, "scale": 1}, tcta, 0.3, "power3.out")
            tl.ft(f"#{sid}-cta", {"scale": 1}, {"scale": 1.05}, tcta + 0.6, 0.5, "sine.inOut")
            tl.ft(f"#{sid}-cta", {"scale": 1.05}, {"scale": 1}, tcta + 1.1, 0.5, "sine.inOut")
            tl.ft(f"#{sid}-logo", {"opacity": 0}, {"opacity": 1}, tcta + 0.8, 0.5)
            muets.append((t0, t1))
        if ban:
            tl.ft(f"#{sid}-ban", {"opacity": 0, "scale": 1.3}, {"opacity": 1, "scale": 1}, t0, 0.3, "power3.out")
        parts.append(f'<div id="{sid}" class="clip seg" data-start="{t0:.2f}" data-duration="{dur:.2f}" data-track-index="1">'
                     f'{ban}{inner}</div>')

    # ------------------------------------------------------------- ARCHIVISTE (coin bas gauche)
    poses = sp["archiviste"]["poses"]  # nom -> image
    plan = sp["archiviste"]["sequence"]  # [{"mot": "...", "pose": "..."}], première à 0
    imgs = "".join(f'<img id="ar-{p}" class="ar-p" src="{img(f)}" alt="" style="opacity:{1 if p == plan[0]["pose"] else 0}">'
                   for p, f in poses.items())
    cur = plan[0]["pose"]
    for st in plan[1:]:
        t = t_mot(st["mot"]) - 0.15
        if st["pose"] != cur:
            tl.ft(f"#ar-{cur}", {"opacity": 1}, {"opacity": 0}, t, 0.25, "power1.inOut")
            tl.ft(f"#ar-{st['pose']}", {"opacity": 0}, {"opacity": 1}, t, 0.25, "power1.inOut")
            cur = st["pose"]
    # respiration + petit hochement quand il parle
    n = int(total // 1.6)
    for i in range(n):
        tl.ft("#ar-in", {"y": 0}, {"y": -8}, i * 1.6, 0.8, "sine.inOut")
        tl.ft("#ar-in", {"y": -8}, {"y": 0}, i * 1.6 + 0.8, 0.8, "sine.inOut")
    tl.ft("#ar-halo", {"opacity": 0.35}, {"opacity": 0.8}, 0, 1.2, "sine.inOut")
    archi = (f'<div id="archi"><div id="ar-halo"></div><div id="ar-in">{imgs}</div>'
             f'</div>')

    # ------------------------------------------------------------- SOUS-TITRES
    garde = [w for w in ws if not any(a <= w["s"] < b for a, b in muets)]
    st_html, st_js = sous_titres(garde, total, sp.get("mots_cles", []))

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
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--charbon); }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      #fond {{ position: absolute; inset: 0; background: radial-gradient(ellipse 70% 45% at 50% 38%, #1d1c1d, var(--charbon) 70%); }}
      .seg, #hook {{ position: absolute; inset: 0; }}
      /* hook */
      .hk-texte {{ position: absolute; left: 90px; top: 420px; width: 900px; text-align: center; }}
      .hk-l {{ font-family: var(--font-display); font-weight: 700; font-size: 112px; line-height: 1.12; text-transform: uppercase; color: var(--ivoire); }}
      .hk-a {{ color: var(--ambre); }} .hk-r {{ color: var(--rouge); }}
      .hk-compte {{ position: absolute; left: 90px; top: 380px; width: 900px; height: 700px; }}
      .hk-chiffre {{ position: absolute; inset: 0; text-align: center; font-family: var(--font-display); font-weight: 700; font-size: 420px; line-height: 700px; color: var(--ivoire); }}
      .hk-rate {{ position: absolute; left: 0; right: 0; top: 230px; text-align: center; font-family: var(--font-display); font-weight: 700; font-size: 190px; color: var(--rouge); border: 14px solid var(--rouge); transform: rotate(-8deg); }}
      /* bandeau */
      .ban {{ position: absolute; left: 0; right: 0; top: 250px; text-align: center; }}
      .ban span {{ display: inline-block; background: var(--rouge); color: var(--ivoire); font-family: var(--font-display); font-weight: 700; font-size: 46px; letter-spacing: 0.08em; padding: 6px 26px; text-transform: uppercase; }}
      /* scène */
      .card {{ position: absolute; left: 150px; top: 350px; width: 780px; height: 660px; border-radius: 22px; overflow: hidden; border: 3px solid rgba(214,166,74,0.45); }}
      .card img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .tag {{ position: absolute; font-family: var(--font-mono); font-size: 32px; letter-spacing: 0.08em; color: var(--charbon); background: var(--ambre); padding: 4px 14px; text-transform: uppercase; }}
      /* suspects */
      .lineup {{ position: absolute; left: 0; top: 350px; width: 1080px; height: 660px; }}
      .sus {{ position: absolute; top: 0; width: 270px; height: 660px; transform-origin: 50% 60%; }}
      .sus-img {{ position: absolute; left: 0; top: 0; width: 270px; height: 560px; overflow: hidden; border-radius: 18px; border: 3px solid rgba(214,166,74,0.5); }}
      .sus-img img {{ width: 100%; height: 100%; object-fit: cover; }}
      .sus-nom {{ position: absolute; left: 0; right: 0; top: 578px; text-align: center; font-family: var(--font-display); font-weight: 700; font-size: 34px; color: var(--ivoire); text-transform: uppercase; }}
      .slate {{ position: absolute; left: 14px; right: 14px; top: 330px; background: #1b1d1b; border: 6px solid #6b5636; padding: 12px; font-family: var(--font-mono); font-size: 24px; line-height: 1.3; color: var(--ivoire); }}
      /* question */
      .q {{ position: absolute; left: 90px; top: 330px; width: 900px; text-align: center; font-family: var(--font-display); font-weight: 700; font-size: 96px; line-height: 1.12; text-transform: uppercase; color: var(--ivoire); }}
      .minis {{ position: absolute; left: 150px; top: 580px; width: 780px; display: flex; justify-content: space-between; }}
      .mini {{ width: 220px; text-align: center; }}
      .mini img {{ width: 220px; height: 260px; object-fit: cover; border-radius: 14px; border: 3px solid rgba(214,166,74,0.5); }}
      .mini span {{ display: block; margin-top: 8px; font-family: var(--font-display); font-weight: 700; font-size: 32px; color: var(--ivoire); text-transform: uppercase; }}
      .cd {{ position: absolute; left: 440px; top: 915px; width: 200px; height: 200px; }}
      .cd svg {{ position: absolute; inset: 0; }}
      .cd circle {{ fill: none; stroke: var(--ambre); stroke-width: 10; stroke-dasharray: 1; transform: rotate(-90deg); transform-origin: 50% 50%; }}
      .cd span {{ position: absolute; inset: 0; text-align: center; line-height: 200px; font-family: var(--font-display); font-weight: 700; font-size: 120px; color: var(--ambre); opacity: 0; }}
      .cta {{ position: absolute; left: 370px; top: 1150px; width: 520px; text-align: center; background: var(--ambre); color: var(--charbon); font-family: var(--font-display); font-weight: 700; font-size: 40px; line-height: 1.15; padding: 14px 18px; border-radius: 14px; text-transform: uppercase; opacity: 0; }}
      .logo {{ position: absolute; left: 370px; top: 1310px; width: 520px; text-align: center; font-family: var(--font-mono); font-size: 34px; letter-spacing: 0.3em; color: var(--ambre); opacity: 0; }}
      /* Archiviste */
      #archi {{ position: absolute; left: -10px; top: 1120px; width: 390px; height: 520px; z-index: 30;
        -webkit-mask-image: linear-gradient(to bottom, #000 72%, transparent 100%), linear-gradient(to right, #000 80%, transparent 100%);
        -webkit-mask-composite: source-in; mask-image: linear-gradient(to bottom, #000 72%, transparent 100%); }}
      #ar-halo {{ position: absolute; left: 40px; top: 30px; width: 320px; height: 420px; border-radius: 50%; background: radial-gradient(circle, rgba(214,166,74,0.35), rgba(214,166,74,0) 70%); }}
      #ar-in {{ position: absolute; inset: 0; }}
      .ar-p {{ position: absolute; left: 0; top: 0; width: 390px; height: 652px; object-fit: cover; object-position: 50% 0; }}
      #ar-nom {{ position: absolute; left: 30px; top: 470px; font-family: var(--font-mono); font-size: 26px; letter-spacing: 0.2em; color: var(--ambre); }}
      .st {{ position: absolute; left: 140px; top: 1035px; width: 800px; z-index: 40; }}
      .st .da-caption {{ text-shadow: 0 2px 14px rgba(16, 17, 19, 0.95); font-size: 70px; }}
      #fx-vignette {{ position: absolute; inset: 0; z-index: 50; pointer-events: none; background: radial-gradient(ellipse 85% 75% at 50% 45%, rgba(16,17,19,0) 60%, rgba(16,17,19,0.65) 100%); }}
      #fx-grain {{ position: absolute; inset: 0; z-index: 51; pointer-events: none; opacity: 0.06;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }}
    </style>
  </head>
  <body>
    <!-- Généré par scripts/enigme.py depuis {E(spec_path.name)} : modifier le fichier d'énigme puis regénérer. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="1080" data-height="1920">
      <div id="fond" data-layout-ignore></div>
      {chr(10).join("      " + p for p in parts).strip()}
      {archi}
      <audio id="voix" class="clip" src="assets/voix{voix.suffix}" data-start="0" data-duration="{fin_voix + 0.2:.2f}" data-track-index="9" data-volume="1"></audio>
      <div data-track-kind="captions">
      {st_html}
      </div>
      <div id="fx-vignette" data-layout-ignore></div>
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
    return total, list(zip([s.get("type") for s in [{"type": "hook"}] + segs], debuts, fins))


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
    r = subprocess.run(CLI + ["check", "--json"], cwd=out, env=ENV, capture_output=True, text=True)
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
