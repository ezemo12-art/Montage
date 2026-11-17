#!/usr/bin/env python3
"""DOSSIER 00 — moteur narratif : script → voix → storyboard → vidéo.

  python3 scripts/engine.py voix <dossier> "<texte>" [--voix ff_siwis] [--vitesse 0.85]
        → <dossier>/voix.wav + transcript.json (mots horodatés)
  python3 scripts/engine.py build <storyboard.json> <projet> [--check] [--render [--qualite draft|looks|delivery]]
        → projet HyperFrames (un plan = une composition), contrôle et rendu MP4

Le storyboard (personnages, lieux, plans, actions, caméra) est écrit par Claude à partir du
script : voir engine/README.md.
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import storyboard as S  # noqa: E402
from engine.compiler import compiler  # noqa: E402

CLI = ["node", str(ROOT / ".claude/skills/hyperframes/scripts/plugin-cli.mjs")]
ENV = dict(os.environ, HYPERFRAMES_TELEMETRY="0", DO_NOT_TRACK="1")


def hf(*args, cwd=None, check=True):
    r = subprocess.run(CLI + list(args), cwd=cwd, env=ENV, capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"✗ hyperframes {' '.join(args)}\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    return r


def cmd_voix(a):
    d = pathlib.Path(a.dossier).resolve()
    d.mkdir(parents=True, exist_ok=True)
    hf("tts", a.texte, "-v", a.voix, "-s", str(a.vitesse), "-o", str(d / "voix.wav"))
    hf("transcribe", str(d / "voix.wav"), "--engine", "whisper", "--model", "small", "--language", "fr", "--json", cwd=str(d))
    print(f"✓ {d/'voix.wav'} + {d/'transcript.json'}")


def cmd_build(a):
    sb_path = pathlib.Path(a.storyboard).resolve()
    out = pathlib.Path(a.projet).resolve()
    sb = S.charger(sb_path)
    if not (out / "hyperframes.json").exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        hf("init", str(out), "--skip-skills", "--skill=hyperframes")
    res = compiler(sb, sb_path.parent, out)
    print(f"✓ {len(res['plans'])} plans, {res['duree']} s → {out}")
    for p in res["plans"]:
        print(f"  {p['debut']:6.2f}s  {p['duree']:5.2f}s  {p['id']:<12} {p['decor']:<12} « {p['ancre']} »")
    if a.check or a.render:
        hf("check", "--json", cwd=str(out), check=False)
        chk = sorted((out / ".hyperframes/artifacts/checks").glob("*.json"), key=os.path.getmtime)[-1]
        d = json.loads(chk.read_text())
        erreurs = [f for v in d.values() if isinstance(v, dict) for f in v.get("findings", []) if f.get("severity") == "error"]
        for f in erreurs:
            print(f"  ✗ {f.get('code')}: {f.get('message','')[:160]}")
        print(f"  contrôle : {len(erreurs)} erreur(s)")
        if erreurs:
            sys.exit(1)
    if a.render:
        (out / "export").mkdir(exist_ok=True)
        dest = out / "export" / "final.mp4"
        if dest.exists():
            dest.unlink()
        hf("render", "--quality", a.qualite, "-o", str(dest), cwd=str(out))
        print(f"✓ {dest}")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    v = sp.add_parser("voix"); v.add_argument("dossier"); v.add_argument("texte"); v.add_argument("--voix", default="ff_siwis"); v.add_argument("--vitesse", type=float, default=0.85)
    b = sp.add_parser("build"); b.add_argument("storyboard"); b.add_argument("projet")
    b.add_argument("--check", action="store_true"); b.add_argument("--render", action="store_true")
    b.add_argument("--qualite", default="looks", choices=["draft", "looks", "delivery"])
    a = ap.parse_args()
    try:
        {"voix": cmd_voix, "build": cmd_build}[a.cmd](a)
    except S.ErreurStoryboard as e:
        sys.exit(f"✗ {e}")


if __name__ == "__main__":
    main()
