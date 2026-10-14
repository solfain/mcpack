#!/usr/bin/env bash
# Rebuild the 1.21.11 port of the Vermeil pack from the source zip in this repo.
#
#   tools/build_port.sh
#
# Original (legacy, format 1) pack: vermeil_under_25mb.zip
# Result:                          dist/Vermeil-1.21.11.zip  (drop into .minecraft/resourcepacks)
set -euo pipefail
cd "$(dirname "$0")/.."

src_zip="${1:-vermeil_under_25mb.zip}"
[ -f "$src_zip" ] || { echo "missing $src_zip" >&2; exit 1; }

echo "==> extracting $src_zip"
rm -rf build/vermeil && mkdir -p build/vermeil
unzip -q -o "$src_zip" -d build/vermeil

if [ ! -f vanilla_all_paths.txt ]; then
  echo "==> fetching vanilla asset path list (needs the GitHub CLI)"
  tools/fetch_vanilla_paths.sh 1.21.11 vanilla_all_paths.txt
fi

echo "==> porting to 1.21.11 (pack format 75)"
mkdir -p dist docs

# Pillow is only needed to slice the legacy clock/compass animation strips
PY=python3
if [ ! -x .venv/bin/python ]; then
  if python3 -m venv .venv >/dev/null 2>&1; then
    .venv/bin/pip install --quiet pillow >/dev/null 2>&1 || true
  fi
fi
[ -x .venv/bin/python ] && PY=.venv/bin/python

"$PY" tools/port_pack.py \
  --src build/vermeil \
  --out build/port \
  --vanilla-paths vanilla_all_paths.txt \
  --fonts --force \
  --report docs/port-report.md \
  --zip dist/Vermeil-1.21.11.zip

echo "==> done: dist/Vermeil-1.21.11.zip"
