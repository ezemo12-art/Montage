#!/usr/bin/env python3
"""Banque de sujets DOSSIER 00.

  python3 scripts/sujets.py deja-fait "<affaire ou lien>"  → cherche dans les épisodes et la banque
  python3 scripts/sujets.py liste [statut]                  → fiches de BANQUE_SUJETS.md

Une ligne « prête » ne prouve rien : on vérifie toujours dans dossiers/ ET dans la banque.
"""
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANQUE = ROOT / "BANQUE_SUJETS.md"


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9 ]+", " ", "".join(c for c in s if unicodedata.category(c) != "Mn")).split()


def deja_fait(requete):
    mots = [m for m in norm(requete) if len(m) > 3] or norm(requete)
    lien = re.search(r"https?://\S+", requete)
    trouves = []
    sources = list((ROOT / "dossiers").glob("*/EPISODE.md")) + ([BANQUE] if BANQUE.exists() else [])
    for f in sources:
        txt = f.read_text(encoding="utf-8")
        if lien and lien[0] in txt:
            trouves.append((f, "même lien"))
            continue
        n = set(norm(txt))
        score = sum(m in n for m in mots) / len(mots)
        if score >= 0.75:
            trouves.append((f, f"{score:.0%} des mots"))
    return trouves


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "deja-fait":
        t = deja_fait(" ".join(sys.argv[2:]))
        for f, why in t:
            print(f"⚠ possible doublon : {f.relative_to(ROOT)} ({why})")
        print("✓ rien de trouvé" if not t else "→ vérifier à la main avant de produire")
        sys.exit(1 if t else 0)
    if sys.argv[1] == "liste":
        statut = sys.argv[2] if len(sys.argv) > 2 else None
        for bloc in BANQUE.read_text(encoding="utf-8").split("\n## ")[1:]:
            titre = bloc.splitlines()[0]
            st = re.search(r"Statut\s*:\s*(.+)", bloc)
            if not statut or (st and statut in st.group(1)):
                print(f"- {titre}  [{st.group(1).strip() if st else '?'}]")


if __name__ == "__main__":
    main()
