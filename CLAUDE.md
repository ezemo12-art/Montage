# DOSSIER 00 — true-crime brand (Instagram / TikTok) + investigation games shop

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
