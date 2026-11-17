#!/usr/bin/env python3
"""DOSSIER 00 — génération d'image avec références (API OpenAI GPT Image).

Usage :
  python3 scripts/gen_image.py --prompt-file p.txt --ref archiviste/references/Character_FullBody_v1.jpg \
      --out archiviste/candidats/Character_Front_v1.png --size 1024x1536

  --dry-run   affiche la requête sans appeler l'API (aucun coût).

Clé : variable d'environnement OPENAI_API_KEY (jamais dans le code ni dans git).
Dans un environnement cloud Claude Code, la clé peut être injectée par le proxy :
le script envoie alors une valeur factice que le proxy remplace.
Modèle : DOSSIER00_IMAGE_MODEL (défaut : gpt-image-2).

Règles : n'écrit jamais dans archiviste/references/ (seules les images validées y vont,
à la main). Chaque appel est journalisé dans generations.jsonl (suivi des coûts).
"""
import argparse, base64, datetime, json, os, pathlib, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
REFS_DIR = (ROOT / "archiviste" / "references").resolve()
LOG = ROOT / "generations.jsonl"
API = "https://api.openai.com/v1/images"


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt")
    g.add_argument("--prompt-file")
    ap.add_argument("--ref", action="append", default=[], help="image de référence (répétable)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1024x1536")
    ap.add_argument("--quality", default="high", choices=["low", "medium", "high", "auto"])
    ap.add_argument("--model", default=os.environ.get("DOSSIER00_IMAGE_MODEL", "gpt-image-2"))
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    prompt = a.prompt if a.prompt else pathlib.Path(a.prompt_file).read_text(encoding="utf-8").strip()
    out = pathlib.Path(a.out).resolve()
    if REFS_DIR in out.parents:
        sys.exit("✗ Refusé : on n'écrit jamais directement dans archiviste/references/. "
                 "Génère dans archiviste/candidats/ puis valide à la main.")
    if out.exists():
        sys.exit(f"✗ {out} existe déjà : choisis un nouveau numéro de version (pas d'écrasement).")
    refs = [pathlib.Path(r) for r in a.ref]
    for r in refs:
        if not r.is_file():
            sys.exit(f"✗ Référence introuvable : {r}")

    endpoint = f"{API}/edits" if refs else f"{API}/generations"
    summary = {"endpoint": endpoint, "model": a.model, "size": a.size, "quality": a.quality,
               "refs": [str(r) for r in refs], "out": str(out), "prompt_chars": len(prompt)}
    if a.dry_run:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print("--- prompt ---\n" + prompt)
        return

    import requests  # importé ici pour que --dry-run marche partout
    key = os.environ.get("OPENAI_API_KEY") or "proxy-injected"
    headers = {"Authorization": f"Bearer {key}"}
    data = {"model": a.model, "prompt": prompt, "size": a.size, "quality": a.quality, "n": "1"}

    last = None
    for attempt in range(1, a.retries + 1):
        files = [("image[]", (r.name, r.open("rb"))) for r in refs]
        try:
            if refs:
                resp = requests.post(endpoint, headers=headers, data=data, files=files, timeout=300)
            else:
                resp = requests.post(endpoint, headers=headers, json=data, timeout=300)
        except requests.RequestException as e:
            last = f"réseau : {e}"
        else:
            if resp.ok:
                break
            last = f"HTTP {resp.status_code} : {resp.text[:400]}"
            if resp.status_code not in (408, 409, 429, 500, 502, 503, 504):
                sys.exit(f"✗ {last}")  # erreur non temporaire : pas de nouvel essai (coût)
        finally:
            for _, (_, fh) in files:
                fh.close()
        wait = 5 * attempt
        print(f"… essai {attempt} échoué ({last}), nouvel essai dans {wait}s", file=sys.stderr)
        time.sleep(wait)
    else:
        sys.exit(f"✗ Échec après {a.retries} essais : {last}")

    body = resp.json()
    img = base64.b64decode(body["data"][0]["b64_json"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(img)
    entry = {**summary, "time": datetime.datetime.now().isoformat(timespec="seconds"),
             "usage": body.get("usage"), "bytes": len(img)}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"✓ {out} ({len(img)//1024} Ko) — à vérifier avec la checklist QC avant usage")


if __name__ == "__main__":
    main()
