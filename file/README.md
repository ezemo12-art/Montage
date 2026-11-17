# File de production DOSSIER 00

Tu envoies une affaire (ou un lien) à ton bot Telegram → ton ordinateur lance Claude Code toutes les
10 minutes → Claude recherche, vérifie, écrit, produit et contrôle l'épisode → tu reçois la vidéo avec
**Valider · À revoir · Rejeter**. **Rien ne part sans ton bouton.**

Adapté du guide « Monter ton système de vidéos avec Claude Code » (Eigenflow, novembre 2026).

## Pièces

| Fichier | Rôle |
| --- | --- |
| `relais.py` | Relais Telegram (toutes les minutes) : range tes messages, envoie ce que la file dépose. Aucune IA. |
| `file.py` | La file (toutes les 10 min) : une tâche par passage, lance `claude -p`, lit `result.json`. |
| `consignes/*.md` | Ce que Claude fait pour chaque tâche : production, reprise, publication, apprentissage. |
| `items/<id>/` | Journal et `result.json` de chaque élément. `state.json` : l'état de la file. |

## Le routeur

| Statut | Ce qui l'amène | Ce que fait la file |
| --- | --- | --- |
| à faire | une affaire ou un lien reçu | attend 10 min ta note, puis produit si aucune vidéo ne t'attend |
| à apprendre | ta note dit « pour info », « référence », « retiens » | décortique, range dans APPRENTISSAGES.md, rien à valider |
| en cours | la production a démarré | la reprend au passage suivant après une coupure |
| question | un point sensible sans option prudente | t'envoie la question ; ta réponse relance une version |
| prête | result.json dit « pret » | t'envoie la vidéo avec les 3 boutons |
| à reprendre | ta remarque (en réponse à la vidéo) | applique le changement, renvoie une version |
| validée | Valider, ou « ok », « validé », « gg » | prépare la publication |
| programmée | un créneau réservé (8 h, 13 h, 18 h) | t'envoie le kit à poster |
| rejetée | Rejeter, ou « laisse tomber » seul | rien |
| déjà faite | l'affaire existe déjà chez toi | te le dit en une ligne |
| dans la session | « reviens ici », ou 3 versions refusées | t'attend dans Claude Code |
| erreur | 3 essais sans result.json | te prévient, attend ta réponse |

Une remarque : réponds au message de la vidéo (appui long → Répondre). « Le titre est trop petit » est un
changement ; « c'est très fort » seul est un accord. Une note envoyée pendant une production ne vaut jamais validation.

## Installer (sur TON ordinateur, pas dans le cloud)

La file doit tourner sur une machine allumée (Mac ou serveur Linux) avec ce dépôt cloné, Node 22+, FFmpeg,
Python 3 et Claude Code connecté à ton abonnement.

1. `git clone` du dépôt, puis dans le dossier : `claude` une fois (connexion), `pip install kokoro-onnx soundfile requests`.
2. Telegram : crée ton bot avec **@BotFather** (`/newbot`), garde le jeton. Écris-lui un message, puis :
   ```bash
   python3 -c "import json,urllib.request;print(json.load(urllib.request.urlopen('https://api.telegram.org/botTON_JETON/getUpdates'))['result'][-1]['message']['chat']['id'])"
   mkdir -p ~/.config/dossier00
   echo '{"token": "TON_JETON", "chat_id": 123456789}' > ~/.config/dossier00/telegram.json
   chmod 600 ~/.config/dossier00/telegram.json
   ```
   Le jeton ne va **jamais** dans le dépôt ni dans une consigne.
3. Vérifie qu'aucune `ANTHROPIC_API_KEY` n'est définie pour cron / launchd (sinon la clé est facturée à l'usage).
   Pas d'option `--bare` (elle ne lit pas l'abonnement).
4. Lancer automatiquement :
   - **Linux** (`crontab -e`) — `claude.env` (chmod 600) contient `export CLAUDE_CODE_OAUTH_TOKEN=…` obtenu par `claude setup-token` :
     ```
     */10 * * * * cd $HOME/Montage/file && . $HOME/.config/dossier00/claude.env && python3 file.py >> file.log 2>&1
     * * * * * cd $HOME/Montage/file && python3 relais.py >> relais.log 2>&1
     ```
   - **Mac** : deux fichiers dans `~/Library/LaunchAgents/` (`com.dossier00.file.plist`, StartInterval 600, et
     `com.dossier00.relais.plist`, StartInterval 60), avec `PATH` contenant le dossier de `claude`, puis
     `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.dossier00.file.plist` (idem pour le relais).
     Le script empêche la veille pendant une tâche (`caffeinate -i`), pas le capot fermé.

Variables utiles : `CLAUDE_CMD` (chemin complet de `claude`), `CLAUDE_MODELE` (défaut `opus`).

## Garde-fous

- Publication uniquement après Valider ; aucune consigne ne publie, ne commit, n'écrit à quelqu'un ni ne crée de compte.
- Aucun code tiers lancé pendant une production. Seuls les outils du dépôt.
- Temps maximum : 6 h production, 3 h reprise, 2 h publication.
- Écriture atomique de l'état (fichier temporaire puis renommage) ; copie brute de chaque message Telegram avant traitement.
- Le bot ignore tout autre compte que le tien.

## Limites

- Ordinateur éteint = rien ne tourne (Telegram garde les messages 24 h).
- Aucun outil de publication n'est connecté : la file réserve le créneau et prépare le kit, tu postes
  (ou on branche Buffer plus tard).
- Une production coûte du temps (souvent plus d'une heure) et pèse sur la limite d'usage de ton abonnement.
- Testé hors ligne ici (Telegram et Claude simulés : sujet → production → remarque → reprise → Valider → programmé).
  Le premier vrai passage se fera sur ta machine.
