# Montage — Instagram videos on criminal investigations

This repo is used to produce vertical videos (Reels) with motion design, using
HyperFrames (HTML → MP4). Skills are installed in `.claude/skills/`.
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

**`DA.md` is the account's art direction. Read it before every video and follow it
for every video the user asks for**, unless the brief explicitly asks for an exception.
Its technical values live in `da/da.css`: copy it to `assets/da.css` of each new video
and link it (`<link rel="stylesheet" href="assets/da.css">`). If the user changes the DA,
update `DA.md` and `da/da.css` together.

## Method (always in this order)

1. **Prepare the rush** (`rush/`): cut the silences/hesitations, show the list of cuts before applying them.
2. **Transcribe, then storyboard** with a timestamped plan, **3 or 4 key moments max**.
   Build nothing before the user's OK.
3. **Build** in `videos/<slug>/` (`$H init videos/<slug> --skip-skills --skill=hyperframes`),
   format **1080 × 1920, 30 fps**.
4. **Iterate** (3 rounds max), then export:
   `$H render --quality delivery -o videos/<slug>/export/final.mp4`.

The `BRIEF.md` file is the brief template to fill in before each video.
`exemple-enquete/` is a working reference project (voice + subtitles + title).

## Benchmarks

- Big title: 0.8–1.2 s · word-by-word subtitle: 0.25–0.35 s/word · widget/card: 0.6–0.9 s
- Minimum reading time: 1.5 s per text
- A single thing moves at a time · 2 neutrals + 1 accent max
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
