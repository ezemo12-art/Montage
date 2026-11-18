"""Storyboard : validation + calage des plans sur la transcription (mots horodatés)."""
from __future__ import annotations

import json
import pathlib
import re
import unicodedata

DECORS_CONNUS = {"maison_nuit", "couloir", "voisinage", "archiviste", "illustration", "motion"}
ACTIONS_CONNUES = {"marche", "court", "entre", "regarde_derriere", "telephone", "apparait", "disparait",
                   "tombe", "ouvre_porte", "ferme_porte", "lumieres", "eteint", "bruit", "voisin_regarde",
                   "sort_de_l_ombre", "lumiere_ambre"}


class ErreurStoryboard(ValueError):
    pass


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


BIBLIO = pathlib.Path(__file__).resolve().parent.parent / "bibliotheque"


def charger(path: str | pathlib.Path) -> dict:
    """Charge un storyboard. Un personnage / lieu peut venir de la bibliothèque persistante :
    {"bibliotheque": "homme-veste-noire"} (+ champs à surcharger)."""
    sb = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    for cle, dossier in (("personnages", "personnages"), ("lieux", "lieux")):
        for k, v in sb.get(cle, {}).items():
            if isinstance(v, dict) and "bibliotheque" in v:
                f = BIBLIO / dossier / f"{v['bibliotheque']}.json"
                if not f.exists():
                    raise ErreurStoryboard(f"{cle}/{k}: fiche introuvable dans la bibliothèque : {f.name}")
                sb[cle][k] = json.loads(f.read_text(encoding="utf-8")) | {x: y for x, y in v.items() if x != "bibliotheque"}
    valider(sb)
    return sb


def sauver_bibliotheque(type_: str, nom: str, fiche: dict) -> pathlib.Path:
    """Conserve un personnage / lieu pour les prochaines vidéos."""
    f = BIBLIO / type_ / f"{nom}.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(fiche, ensure_ascii=False, indent=2), encoding="utf-8")
    return f


def valider(sb: dict) -> None:
    err = []
    persos, lieux = sb.get("personnages", {}), sb.get("lieux", {})
    if not sb.get("plans"):
        err.append("aucun plan")
    ids, vus_motion = set(), set()
    for i, pl in enumerate(sb.get("plans", [])):
        pid = pl.get("id") or f"#{i+1}"
        if pid in ids:
            err.append(f"{pid}: id en double")
        ids.add(pid)
        if not re.fullmatch(r"[a-z][a-z0-9-]*", pid):
            err.append(f"{pid}: id invalide (minuscules, chiffres, tirets)")
        if pl.get("decor") not in DECORS_CONNUS:
            err.append(f"{pid}: décor inconnu {pl.get('decor')!r} (connus : {sorted(DECORS_CONNUS)})")
        if not pl.get("ancre"):
            err.append(f"{pid}: 'ancre' manquante (début du passage narré)")
        if pl.get("decor") == "motion":
            nom = pl.get("composition", "")
            if not (pathlib.Path(__file__).resolve().parent.parent / "motion" / "compositions" / f"{nom}.html").exists():
                err.append(f"{pid}: composition motion inconnue {nom!r}")
            if nom in vus_motion:
                err.append(f"{pid}: la composition {nom!r} ne peut servir qu'une fois par vidéo")
            vus_motion.add(nom)
        if pl.get("decor") == "illustration" and not pl.get("image"):
            err.append(f"{pid}: plan illustration sans 'image'")
        if pl.get("lieu") and pl["lieu"] not in lieux:
            err.append(f"{pid}: lieu {pl['lieu']!r} absent de 'lieux'")
        for pp in pl.get("personnages", []):
            if pp.get("qui") not in persos:
                err.append(f"{pid}: personnage {pp.get('qui')!r} absent de 'personnages'")
        for a in pl.get("actions", []):
            if a.get("action") not in ACTIONS_CONNUES:
                err.append(f"{pid}: action inconnue {a.get('action')!r}")
            if a.get("qui") and a["qui"] not in [pp["qui"] for pp in pl.get("personnages", [])]:
                err.append(f"{pid}: action sur {a['qui']!r} qui n'est pas dans le plan")
    if err:
        raise ErreurStoryboard("Storyboard invalide :\n- " + "\n- ".join(err))


def mots(transcript_path: str | pathlib.Path, texte: str | None = None) -> list[dict]:
    """Mots horodatés. Si le texte exact du script est fourni, on garde SES mots (sous-titres
    fidèles) et on ne prend à la transcription que les temps (alignement de séquences)."""
    d = json.loads(pathlib.Path(transcript_path).read_text(encoding="utf-8"))
    w = d if isinstance(d, list) else d["words"]
    ws = [{"t": x["text"], "n": _norm(x["text"]), "s": float(x["start"]), "e": float(x["end"])} for x in w]
    return aligner(texte, ws) if texte else ws


def aligner(texte: str, ws: list[dict]) -> list[dict]:
    import difflib
    script = []
    for t in texte.split():  # ponctuation isolée (« : », « « ») collée au mot voisin
        if not _norm(t) and script:
            script[-1]["t"] += ("\u00a0" if t in ":;?!»" else " ") + t
        elif not _norm(t):
            continue
        else:
            script.append({"t": t, "n": _norm(t)})
    for i in range(len(script) - 1):  # « ouvrant collé au mot suivant
        if script[i]["t"].endswith("«"):
            script[i]["t"] = script[i]["t"][:-1].rstrip()
            script[i + 1]["t"] = "«\u00a0" + script[i + 1]["t"]
    sm = difflib.SequenceMatcher(a=[x["n"] for x in script], b=[x["n"] for x in ws], autojunk=False)
    out = []
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == "equal":
            for i, j in zip(range(a0, a1), range(b0, b1)):
                out.append(dict(script[i], s=ws[j]["s"], e=ws[j]["e"]))
        elif op in ("replace", "insert"):
            if b1 > b0:
                s0, e0 = ws[b0]["s"], ws[b1 - 1]["e"]
            else:  # mot du script absent de la transcription : coller au voisin
                s0 = out[-1]["e"] if out else (ws[b0]["s"] if b0 < len(ws) else ws[-1]["e"])
                e0 = ws[b0]["s"] if b0 < len(ws) else s0 + 0.3
            n = a1 - a0
            for k, i in enumerate(range(a0, a1)):
                out.append(dict(script[i], s=s0 + (e0 - s0) * k / n, e=s0 + (e0 - s0) * (k + 1) / n))
        # "delete" : mot entendu en trop, ignoré
    return out


def trouver(ws: list[dict], phrase: str, apres: int = 0) -> int:
    """Index du mot où commence `phrase` (recherche tolérante, à partir de `apres`)."""
    # un « mot » = ce qui est séparé par des espaces dans le texte (« L'un » reste un seul mot)
    cible = [_norm(t).replace(" ", "") for t in phrase.split() if _norm(t)]
    if not cible:
        raise ErreurStoryboard("phrase vide")
    meilleur, score_max = None, 0.0
    for i in range(apres, len(ws)):
        n = min(len(cible), len(ws) - i)
        fenetre = [ws[i + j]["n"].replace(" ", "") for j in range(n)]
        score = sum(1 for j in range(n) if fenetre[j] == cible[j] or (len(cible[j]) > 3 and fenetre[j].startswith(cible[j][:4])))
        score /= len(cible)
        if score > score_max + 1e-9:
            meilleur, score_max = i, score
        if score == 1.0:
            break
    if meilleur is None or score_max < 0.5:
        raise ErreurStoryboard(f"ancre introuvable dans la voix : {phrase!r}")
    return meilleur


def caler(sb: dict, ws: list[dict], fin_audio: float) -> list[dict]:
    """Ajoute début / fin absolus à chaque plan, d'après son ancre."""
    plans, idx = [], 0
    for pl in sb["plans"]:
        i = trouver(ws, pl["ancre"], idx)
        idx = i + 1
        plans.append(dict(pl, _mot=i, debut=max(0.0, ws[i]["s"] - 0.12)))
    plans[0]["debut"] = 0.0
    for a, b in zip(plans, plans[1:]):
        a["fin"] = b["debut"]
    plans[-1]["fin"] = fin_audio + float(sb.get("queue", 1.2))
    for pl in plans:
        pl["duree"] = round(pl["fin"] - pl["debut"], 3)
        if pl["duree"] < 0.6:
            raise ErreurStoryboard(f"{pl['id']}: plan trop court ({pl['duree']} s) — fusionner avec le voisin")
    return plans


def temps(spec, plan: dict, ws: list[dict], defaut: float) -> float:
    """Temps local (s) dans le plan : fraction 0–1, ou {"mot": "..."} calé sur la voix."""
    if spec is None:
        return defaut * plan["duree"]
    if isinstance(spec, (int, float)):
        return float(spec) * plan["duree"]
    if isinstance(spec, dict) and "mot" in spec:
        i = trouver(ws, spec["mot"], plan["_mot"])
        return max(0.0, ws[i]["s"] - plan["debut"] + float(spec.get("decalage", 0)))
    raise ErreurStoryboard(f"temps invalide : {spec!r}")
