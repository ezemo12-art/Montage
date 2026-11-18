#!/usr/bin/env bash
# Installe Blender + les bibliothèques OpenGL pour un rendu sans écran (skill blender-video-3d).
set -e
if ! command -v blender >/dev/null; then
  apt-get install -y -q blender || { apt-get update -q && apt-get install -y -q blender; }
fi
apt-get install -y -q libegl1 libgl1 libegl-mesa0 >/dev/null 2>&1 || true
blender --version | head -1
