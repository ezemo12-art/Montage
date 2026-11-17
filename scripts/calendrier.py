#!/usr/bin/env python3
"""Calendrier de publication DOSSIER 00 : 3 créneaux par jour (8 h, 13 h, 18 h, Europe/Paris).

  python3 scripts/calendrier.py prochain                    → premier créneau libre (≥ 20 min, jamais doublé)
  python3 scripts/calendrier.py reserver <ISO> <id> <titre> → réserve un créneau
  python3 scripts/calendrier.py semaine [AAAA-MM-JJ]        → grille de la semaine

Les heures sont stockées en UTC et calculées avec le fuseau Europe/Paris (une heure UTC fixe
glisserait d'une heure au changement d'heure). Fichier : calendrier.json à la racine du dépôt.
"""
import json
import pathlib
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
CRENEAUX = (8, 13, 18)
FICHIER = pathlib.Path(__file__).resolve().parent.parent / "calendrier.json"


def charger():
    return json.loads(FICHIER.read_text()) if FICHIER.exists() else {"publications": []}


def occupes(cal):
    return {datetime.fromisoformat(p["utc"]).astimezone(timezone.utc) for p in cal["publications"]}


def premier_creneau(occ, maintenant, marge=timedelta(minutes=20)):
    t = maintenant + marge
    jour = t.astimezone(PARIS).date()
    while True:
        for h in CRENEAUX:
            c = datetime(jour.year, jour.month, jour.day, h, tzinfo=PARIS)
            if c >= t and c.astimezone(timezone.utc) not in occ:
                return c
        jour += timedelta(days=1)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prochain"
    cal = charger()
    if cmd == "prochain":
        print(premier_creneau(occupes(cal), datetime.now(timezone.utc)).isoformat())
    elif cmd == "reserver":
        iso, ident, titre = sys.argv[2], sys.argv[3], " ".join(sys.argv[4:])
        c = datetime.fromisoformat(iso)
        if c.tzinfo is None:
            c = c.replace(tzinfo=PARIS)
        cu = c.astimezone(timezone.utc)
        if cu in occupes(cal):
            sys.exit(f"✗ créneau déjà pris : {c.isoformat()}")
        if c.astimezone(PARIS).hour not in CRENEAUX:
            sys.exit(f"✗ {c.isoformat()} n'est pas un créneau (8 h, 13 h, 18 h)")
        cal["publications"].append({"utc": cu.isoformat(), "id": ident, "titre": titre, "statut": "programme"})
        cal["publications"].sort(key=lambda p: p["utc"])
        tmp = FICHIER.with_suffix(".tmp")
        tmp.write_text(json.dumps(cal, ensure_ascii=False, indent=1))
        tmp.replace(FICHIER)
        print(f"✓ {titre} → {c.astimezone(PARIS):%a %d/%m %H:%M} (Paris)")
    elif cmd == "semaine":
        debut = datetime.fromisoformat(sys.argv[2]).date() if len(sys.argv) > 2 else datetime.now(PARIS).date()
        debut -= timedelta(days=debut.weekday())
        par = {datetime.fromisoformat(p["utc"]).astimezone(PARIS).replace(tzinfo=None): p for p in cal["publications"]}
        print(f"Semaine du {debut:%d/%m}      " + "".join(f"{h:>2} h{'':<20}" for h in CRENEAUX))
        for i in range(7):
            j = debut + timedelta(days=i)
            cases = []
            for h in CRENEAUX:
                p = par.get(datetime(j.year, j.month, j.day, h))
                cases.append(f"{(p['titre'][:20] if p else '____'):<24}")
            print(f"{'lun mar mer jeu ven sam dim'.split()[i]}. {j:%d/%m}   " + "".join(cases))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
