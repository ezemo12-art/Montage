#!/usr/bin/env python3
"""Relais Telegram : range tes sujets et tes boutons, envoie ce que la file dépose. Aucune IA ici.
Lancé toutes les minutes. Jeton et identifiant dans ~/.config/dossier00/telegram.json (chmod 600),
jamais dans le dépôt.

Ce que tu peux envoyer au bot :
  - un lien (article, reportage, vidéo de référence), avec une note si tu veux ;
  - un sujet en texte : « Affaire X, Lyon 1998 » ;
  - « pour info … » / « référence … » / « retiens … » : à apprendre, rien à valider ;
  - en RÉPONSE à une vidéo envoyée (appui long → Répondre) : une remarque, « ok », « laisse tomber »,
    « reviens ici ».
"""
import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
CONF_PATH = Path.home() / ".config" / "dossier00" / "telegram.json"
BOUTONS = (("v", "Valider"), ("r", "À revoir"), ("x", "Rejeter"))
CODES = {"v": "valider", "r": "revoir", "x": "rejeter"}


def conf():
    c = json.loads(CONF_PATH.read_text())
    return f"https://api.telegram.org/bot{c['token']}/", c["chat_id"]


def appel(methode, **params):
    api, _ = conf()
    req = urllib.request.Request(api + methode, json.dumps(params).encode(), {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))["result"]


def ajouter(nom, ligne):
    with open(BASE / nom, "a") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")


def traiter(u, moi, repondre=None):
    """Range une mise à jour Telegram. `repondre` = fonction d'accusé (remplacée en test)."""
    if "callback_query" in u and u["callback_query"]["from"]["id"] == moi:
        q = u["callback_query"]
        code, item = q["data"].split("|")
        ajouter("events.jsonl", {"type": CODES[code], "item": item, "ts": time.time()})
        if repondre:
            repondre("answerCallbackQuery", callback_query_id=q["id"], text="Transmis à la file")
        return
    m = u.get("message") or {}
    if m.get("chat", {}).get("id") != moi:  # le bot ignore tous les autres comptes
        return
    texte = m.get("text", "")
    vise = (m.get("reply_to_message") or {}).get("message_id")
    journal = BASE / "envoyes.jsonl"
    envois = {e["message_id"]: e["item"] for e in map(json.loads, open(journal))} if journal.exists() else {}
    if vise in envois:  # une réponse à une vidéo envoyée : remarque sur cette vidéo
        ajouter("events.jsonl", {"type": "remarque", "item": envois[vise], "text": texte, "ts": time.time()})
        return
    lien = re.search(r"https?://\S+", texte)
    if lien or texte.strip():
        ajouter("inbox.jsonl", {"id": f"q{u['update_id']}", "url": lien[0] if lien else "",
                                "note": texte.replace(lien[0], "").strip() if lien else texte.strip(), "ts": time.time()})


def recevoir():
    _, moi = conf()
    f = BASE / "offset.txt"
    for u in appel("getUpdates", offset=int(f.read_text()) if f.exists() else 0, timeout=0):
        ajouter("updates.jsonl", u)  # copie brute d'abord : rien ne se perd si la suite plante
        f.write_text(str(u["update_id"] + 1))
        try:
            traiter(u, moi, appel)
        except Exception as e:  # noqa: BLE001
            ajouter("erreurs.jsonl", {"update": u["update_id"], "erreur": repr(e)})


def envoyer():
    api, moi = conf()
    for f in sorted((BASE / "outbox").glob("*.json")):
        m = json.loads(f.read_text())
        clavier = {"inline_keyboard": [[{"text": t, "callback_data": f"{c}|{m['item']}"} for c, t in BOUTONS]]}
        if m["video"]:  # moins de 50 Mo, sinon Telegram refuse (scripts/export_leger.sh)
            cmd = ["curl", "-sf", api + "sendVideo", "-F", f"chat_id={moi}", "-F", f"video=@{m['video']}",
                   "-F", "supports_streaming=true", "--form-string", f"caption={m['text']}"]
            cmd += ["--form-string", f"reply_markup={json.dumps(clavier)}"] if m["boutons"] else []
            res = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)["result"]
        else:
            res = appel("sendMessage", chat_id=moi, text=m["text"], **({"reply_markup": clavier} if m["boutons"] else {}))
        ajouter("envoyes.jsonl", {"message_id": res["message_id"], "item": m["item"]})
        f.unlink()


if __name__ == "__main__":
    recevoir()
    envoyer()
