#!/usr/bin/env python3
"""DOSSIER 00 — file de production. Un passage = une seule tâche. Lancée toutes les 10 minutes.

D'après le guide « Monter ton système de vidéos avec Claude Code » (Eigenflow, nov. 2026),
adapté à DOSSIER 00 : épisodes d'enquêtes, moteur narratif, DA et Archiviste du dépôt.

Rien ne se publie sans ton bouton « Valider ». Claude tourne en `claude -p` sur ton abonnement :
vérifie qu'aucune variable ANTHROPIC_API_KEY ne traîne dans l'environnement de cron / launchd.
"""
import fcntl
import json
import os
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent            # file/
DEPOT = BASE.parent                               # racine du dépôt Montage (cwd de Claude)
INBOX, EVENTS, STATE = BASE / "inbox.jsonl", BASE / "events.jsonl", BASE / "state.json"
CLAUDE = os.environ.get("CLAUDE_CMD", "claude")   # chemin complet si cron / launchd ne le trouve pas
MODELE = os.environ.get("CLAUDE_MODELE", "opus")  # toujours le donner, sinon modèle par défaut des réglages
TIMEOUT = {"production": 6 * 3600, "reprise": 3 * 3600, "publication": 2 * 3600, "apprentissage": 3600}
ATTENTE = ("pret", "revoir", "question")          # une vidéo attend ta réponse : rien de neuf ne démarre
DELAI_NOTE = 600                                  # 10 min après un sujet reçu, le temps que ta note suive
REGLES = {("valider", "pret"): "valide", ("valider", "revoir"): "valide", ("revoir", "pret"): "revoir",
          "rejeter": "rejete", "remarque": "a_reprendre", "reviens_ici": "dans_la_session",
          "pour_info": "apprise"}


def lire(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def ecrire(p, data):  # fichier temporaire puis renommage : jamais un fichier écrit à moitié
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    tmp.replace(p)


def interpreter(texte):
    """Ce que vaut une réponse (routeur, partie 6 du guide)."""
    t = texte.strip().lower()
    if t in ("ok", "validé", "valide", "gg", "go", "parfait", "c'est bon"):
        return "valider"
    if t in ("laisse tomber", "laisse tomber."):
        return "rejeter"
    if t.startswith("reviens ici"):
        return "reviens_ici"
    return "remarque"  # un compliment suivi d'un changement reste un changement


def relever(st):
    connus = {i["id"] for i in st["items"]}
    for e in lire(INBOX):
        if e["id"] in connus:
            continue
        note = e.get("note", "")
        st["items"].append({"id": e["id"], "url": e.get("url", ""), "note": note, "recu": e.get("ts", time.time()),
                            "status": "apprise_a_faire" if any(m in note.lower() for m in ("pour info", "référence", "retiens"))
                            else "a_faire", "essais": 0, "reprises": 0, "remarques": []})
    evs = lire(EVENTS)
    for e in evs[st["ev_lus"]:]:
        it = next((i for i in st["items"] if i["id"] == e["item"]), None)
        if not it or it["status"] in ("programme", "sorti", "rejete"):
            continue
        typ = e["type"]
        if typ == "remarque":
            typ = interpreter(e["text"])
            if typ == "remarque":
                it["remarques"].append(e["text"])
        it["status"] = REGLES.get((typ, it["status"]), REGLES.get(typ, it["status"]))
    st["ev_lus"] = len(evs)


def choisir(st):
    for statut, tache in (("valide", "publication"), ("a_reprendre", "reprise"), ("en_cours", "production"),
                          ("apprise_a_faire", "apprentissage")):
        for it in (i for i in st["items"] if i["status"] == statut):
            if tache == "reprise" and it["reprises"] >= 3:
                it["status"] = "dans_la_session"  # trois versions refusées : la quatrième se fait avec toi
                continue
            return tache, it
    if not any(i["status"] in ATTENTE for i in st["items"]):
        for it in st["items"]:
            if it["status"] == "a_faire" and time.time() - it["recu"] >= DELAI_NOTE:
                return "production", it
    return None, None


def lancer(tache, it):
    d = BASE / "items" / it["id"]
    d.mkdir(parents=True, exist_ok=True)
    res = d / "result.json"
    if res.exists():
        res.rename(d / f"result-{int(time.time())}.json")
    consigne = (BASE / "consignes" / f"{tache}.md").read_text()
    for k, v in {"ID": it["id"], "URL": it["url"] or "(aucun)", "NOTE": it["note"] or "(aucune)", "RESULT": str(res),
                 "REMARQUES": "\n".join(it["remarques"]) or "(aucune)", "DOSSIER_ITEM": str(d)}.items():
        consigne = consigne.replace("{{" + k + "}}", v)
    cmd = [CLAUDE, "-p", consigne, "--model", MODELE, "--output-format", "json",
           "--permission-mode", "auto", "--permission-prompts", "none"]
    if sys.platform == "darwin":
        cmd = ["caffeinate", "-i"] + cmd  # le Mac ne s'endort pas pendant la tâche
    with open(d / f"{tache}-{int(time.time())}.log", "w") as log:
        try:
            subprocess.run(cmd, cwd=DEPOT, stdout=log, stderr=subprocess.STDOUT, timeout=TIMEOUT[tache])
        except subprocess.TimeoutExpired:
            pass
    try:
        return json.loads(res.read_text())
    except (OSError, ValueError):
        return None


def message(it, texte, video=None, boutons=False):
    (BASE / "outbox").mkdir(exist_ok=True)
    ecrire(BASE / "outbox" / f"{time.time_ns()}.json", {"item": it["id"], "text": texte, "video": video, "boutons": boutons})


def apres(tache, it, r):
    if not r:  # pas de result.json : le passage suivant réessaie, trois fois au plus
        it["essais"] += 1
        if it["essais"] >= 3:
            it["status"] = "erreur"
            message(it, "Trois essais ratés, à regarder à la main.")
        return
    it["essais"], s = 0, r.get("status")
    if s == "pret":
        it["status"], it["reprises"] = "pret", it["reprises"] + (tache == "reprise")
        it["dossier"] = r.get("dossier")
        message(it, r.get("telegram", "Prête à valider."), r.get("envoi"), boutons=True)
    elif s == "question":
        it["status"] = "question"
        message(it, r.get("telegram", "Une question avant de continuer."))
    elif s in ("programme", "deja_fait", "apprise"):
        it["status"] = {"programme": "programme", "deja_fait": "deja_fait", "apprise": "apprise"}[s]
        message(it, r.get("telegram") or f"{s} {r.get('dueAt', '')}".strip())
    else:
        it["status"] = "erreur"
        message(it, r.get("telegram") or "Erreur, à regarder à la main.")


def main():
    verrou = open(BASE / ".lock", "w")
    try:
        fcntl.flock(verrou, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return  # le passage précédent travaille encore
    st = json.loads(STATE.read_text()) if STATE.exists() else {"items": [], "ev_lus": 0}
    relever(st)
    tache, it = choisir(st)
    if tache == "production":
        it["status"] = "en_cours"  # coupure en route : le passage suivant reprend cet élément
    ecrire(STATE, st)
    if tache:
        apres(tache, it, lancer(tache, it))
        ecrire(STATE, st)


if __name__ == "__main__":
    main()
