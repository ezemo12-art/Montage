# DOSSIER 00 — criminal RIDDLE videos (Instagram / TikTok) + investigation games shop

> **Since 18/11/2026 the channel makes fictional criminal / situation RIDDLES, not true stories**
> (brief: `docs/DOSSIER00_BRIEF_ENIGMES.md`, rules: `DA.md` §1 and §6). Goal n°1: views and comments.
> Riddle videos are built with `python3 scripts/enigme.py <enigme.json> <project> --render`
> (example: `dossiers/ENIGME-001/enigme.json`). Rotate the 3 hooks: « 1… 2… 3… raté. » (situation),
> « T'es un enquêteur ou nul à chier ? » + the fixed opening lines in `DA.md` §1 (criminal investigation),
> « STOP. Penses-tu comme un criminel ? » (criminal mind). Archiviste in the bottom-left corner the whole
> video (poses in `archiviste/poses/`), atypical creative characters, voice = ElevenLabs
> « Kevan – Narrateur Cinématique » (voice_id AYfOkr1hDQYbhigmRZ16, model eleven_v4). The solution goes in the
> pinned comment, never in the video. **Look v2 (19/11): light warm paper background, energetic pace, sound
> design** — engine `scripts/enigme.py` (v2; v1 dark kept as `scripts/enigme_v1.py`), reusable sounds in
> `bibliotheque/sons/` (+ episode sounds via the "sons" key), example `dossiers/ENIGME-002/enigme.json`.
> ElevenLabs free plan has a DAILY image cap: fall back to Runway when it is reached.
>
> **After EVERY riddle video, end the chat reply with the solution, ready to copy and pin** (user request,
> 19/11): a « Réponse à épingler » block at the very bottom of the message, written as the pinned comment.
>
> **Credits (user decision, 19/11): ElevenLabs credits are low → keep them for the VOICE (~920 credits / video) and
> at most 1–2 sound effects; make images in Blender first** (characters, clue objects, places: `blender/toonkit.py`,
> examples `blender/enigme004.py`). Default background = the reusable generic `bibliotheque/fonds/bureau-enquete.png`
> (applied automatically by `scripts/enigme.py`); reuse `bibliotheque/sons/` before generating any sound.
>
> **Use ALL the tools the user gave, never stop at one (user reminder, 19/11).** Checked 19/11/2026:
> - Images: ElevenLabs (daily cap, resets each day) → Runway (credits) → **local, unlimited**: the
>   `anthropic-skills:blender-video-3d` skill (Blender 4.0 installable with apt here) for 3D scenes and
>   characters that REALLY move, HyperFrames registry blocks (`catalog`, e.g. `lottie-character-walk`),
>   Three.js / SVG in HyperFrames, and the `engine/` silhouettes.
> - Video generation: paid plan needed on both ElevenLabs and Runway (blocked on free plans) → real motion
>   comes from Blender or Lottie, camera/punch motion from HyperFrames.
> - Voice and sound effects: ElevenLabs (credits, no daily cap seen). Music bed: ElevenLabs sfx (~50 credits). Images: ElevenLabs (gemini-nano-banana-2.1 ≈ 204 credits; the
> character-consistent gemini-3-pro-image ≈ 1 830 credits — use only when a reference must be followed) or
> Runway (≈ 6 credits per 2K image). Downloads: hosts allowed in the « Montage » environment.

This repo is the production system of DOSSIER 00 (slogan: « Chaque détail cache une vérité. »):
vertical 9:16 episodes (60–90 s) narrated by a permanent character, **the Archiviste**, plus a
shop of fictional investigation games in PDF (LES DOSSIERS CONFIDENTIELS).
Videos are assembled with HyperFrames (HTML → MP4); skills are in `.claude/skills/`.
Roadmap and what is blocked: `ROADMAP.md`.
The user's original briefs, kept verbatim, are in `docs/` (source of truth with `DA.md`).
Always respond in French.

## Start of session (cloud container = fresh environment)

Run these checks before the first video, and install whatever is missing:

1. `node -v` (≥ 22) and `ffmpeg -version`
2. Local French voice-over (Kokoro): `pip install kokoro-onnx soundfile`
3. CLI: `node .claude/skills/hyperframes/scripts/plugin-cli.mjs doctor --json`
4. Transcription: whisper.cpp is compiled on first `transcribe` (~1 min).
   For French: `--engine whisper --model small --language fr` (never `small.en`).

Shortcut used below: `H="node $PWD/.claude/skills/hyperframes/scripts/plugin-cli.mjs"`.

## Art direction — MANDATORY

**`DA.md` is the official art direction. Read it before every production and follow it for every
video, image, cover and PDF**, unless the user explicitly asks for an exception. Never change the
identity on your own. Technical values: `da/da.css` — copy it to `assets/da.css` of each video and
link it (`<link rel="stylesheet" href="assets/da.css">`). If the user changes the DA, update
`DA.md` and `da/da.css` together.

## The Archiviste — permanent character, MANDATORY

- Bible: `archiviste/CHARACTER.md`. Official references: `archiviste/references/` (validated only).
- **The official image `Character_FullBody_v1.jpg` is kept EXACTLY as given** (user decision): when
  the text charter differs from it (crack, single amber eye), the image wins. Never "fix" it.
- Never create a new character or redesign him. Always pass the official reference image(s) to any
  image/video engine that accepts them, and always start prompts with the locked blocks in
  `prompts/archiviste.md`.
- New generations go to `archiviste/candidats/` (or the episode folder), never straight into
  `references/`. Never replace an official reference without the user's written validation.
- QC every image/shot against the reference (`CHARACTER.md` §7); significant drift → regenerate.

## Motion design system — MANDATORY

- Reusable compositions live in `motion/compositions/` (catalogue + variables: `motion/README.md`).
  Always reuse them in episodes (`scripts/add_motion.sh <episode-project> <names…>`) instead of
  hand-building a new opening, timeline, map, fingerprint, document, suspects board, annotation,
  reveal or closing.
- **Inline `da/da.css` in a `<style>` in every video's `index.html`** (a `<link>` alone makes the
  renderer fall back to a default serif font). Always check decoded MP4 frames, not only snapshots.
- `carte.html`, `empreinte.html` and the demo `index.html` are generated from `motion/src/`
  by `python3 -I scripts/build_motion.py`.

## Narrative motion engine — MANDATORY for illustrating the story

- To show what the narration tells (characters, places, objects, actions), use the engine in
  `engine/` (doc: `engine/README.md`, architecture: `docs/ARCHITECTURE_MOTION_NARRATIF.md`):
  analyse the script → write `storyboard.json` (one shot per visual idea, anchored on the spoken
  words) → `python3 scripts/engine.py build <storyboard> <project> --check / --render`.
- Pass the exact script as `"texte"` so captions use the script's words (Whisper only gives timings).
- Reuse characters/places from `bibliotheque/`; never redesign a recurring character between shots.
- Silhouettes stay anonymous for real cases (no real victim's face, no gore).

## Production queue, calendar, topic bank (from the Eigenflow guide)

- `file/` = automated queue (Telegram → `claude -p` → result.json → Valider/À revoir/Rejeter). It runs on the
  user's own machine, not in this cloud container; see `file/README.md`. Its instructions live in `file/consignes/`.
- Before producing: `python3 scripts/sujets.py deja-fait "<case>"`; topic sheets in `BANQUE_SUJETS.md`.
- Calendar: `python3 scripts/calendrier.py prochain|reserver|semaine` (8 h, 13 h, 18 h Europe/Paris).
- QC tools: `python3 scripts/controle.py hook|planches|voix`; Telegram-size export: `scripts/export_leger.sh`.
- Never publish, commit, create accounts or run third-party code during a queued production.

## Episodes

- One folder per episode: `scripts/new_episode.sh <num> "<titre>"` → `dossiers/DOSSIER-<num>/`
  (`EPISODE.md`, `QC.md`, `sources/ images/ video/ audio/ motion/ export/`).
- Structure (DA.md §6): hook · affaire · Archiviste · reconstitution · indices · retournement · question.
- Nothing is « done » until the file exists and `QC.md` is filled. Human validation before publishing.

## APIs and keys

- Images: `scripts/gen_image.py` (OpenAI GPT Image, `--dry-run` first). Video: no provider chosen
  yet (OpenAI Sora API is shut down) — see `ROADMAP.md`. Verify an API exists and its price before use.
- Keys only via environment / environment secrets (`request_credential`), never in files or git.
- Avoid useless generations (cost); every call is logged in `generations.jsonl`.

## Method (always in this order)

1. **Prepare the rush** (`rush/`): cut the silences/hesitations, show the list of cuts before applying them.
2. **Transcribe, then storyboard** with a timestamped plan, **3 or 4 key moments max**.
   Build nothing before the user's OK.
3. **Build** in `dossiers/DOSSIER-<num>/motion/` (`$H init <dir> --skip-skills --skill=hyperframes`),
   format **1080 × 1920, 30 fps**.
4. **Iterate** (3 rounds max), then export:
   `$H render --quality delivery -o dossiers/DOSSIER-<num>/export/final.mp4`.

The `BRIEF.md` file is the brief template to fill in before each video.
`exemple-enquete/` is a technical test made before DOSSIER 00 (old palette — do not copy its style).

## Benchmarks

- Big title: 0.8–1.2 s · word-by-word subtitle: 0.25–0.35 s/word · widget/card: 0.6–0.9 s
- Minimum reading time: 1.5 s per text
- A single thing moves at a time · official palette only (amber accent, dark red rare)
- Animations synced to the voice (transcribe before animating)

## Check before posting

- Nothing important in the bottom ~20% or on the right edge (hidden by the Instagram interface)
- Title already visible at 0 s (it's the thumbnail)
- `$H check --json` clean, snapshots reviewed
- Export 1080 × 1920, 30 fps, with the original sound

## Ethics specific to true crime

- Real facts only, verified sources; distinguish facts / allegations / hypotheses.
- Presumption of innocence: no accusing an unconvicted person by name.
- Respect for victims and families: no exploitation of images of victims, no gore.
- AI voice-over: enable Instagram's "AI" label when publishing. Clone only the user's own voice.
