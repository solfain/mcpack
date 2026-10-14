#!/usr/bin/env bash
# Fetch the canonical vanilla asset tree for a Minecraft version.
# Used by port_pack.py to validate every rename against what the target version
# actually ships (so a rename that no longer exists is reported instead of guessed).
#
#   tools/fetch_vanilla_paths.sh [version] [output-file]
#
# Source: InventivetalentDev/minecraft-assets (a public mirror of the vanilla jars).
set -euo pipefail

ref="${1:-1.21.11}"
out="${2:-vanilla_all_paths.txt}"

gh api "repos/InventivetalentDev/minecraft-assets/git/trees/${ref}?recursive=1" \
  --jq '.tree[] | select(.type=="blob") | .path' > "$out"

echo "wrote $out ($(wc -l < "$out") paths for ${ref})"
