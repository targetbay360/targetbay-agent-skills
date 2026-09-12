#!/bin/sh
# Install TargetBay Reviews Skills without npm.
#
#   curl -fsSL https://raw.githubusercontent.com/targetbay360/targetbay-agent-skills/main/plugins/targetbay-reviews/scripts/install.sh | sh
#   sh scripts/install.sh /custom/skills/dir
#
# Downloads the latest release tarball for THIS plugin and copies its skills/ into the
# destination. Releases are tagged <plugin>@<version>, so the lookup filters by prefix
# rather than using /releases/latest, which would return whichever plugin shipped last.

set -eu

REPO="targetbay360/targetbay-agent-skills"
PLUGIN="targetbay-reviews"
DEST="${1:-$HOME/.claude/skills}"

command -v curl >/dev/null 2>&1 || { echo "curl is required" >&2; exit 1; }
command -v tar  >/dev/null 2>&1 || { echo "tar is required" >&2; exit 1; }

TAG=$(curl -fsSL "https://api.github.com/repos/$REPO/releases?per_page=100" \
  | sed -n 's/.*"tag_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
  | grep "^$PLUGIN@" \
  | head -n 1)

if [ -z "$TAG" ]; then
  echo "could not resolve the latest $PLUGIN release of $REPO" >&2
  echo "check https://github.com/$REPO/releases" >&2
  exit 1
fi

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "downloading $REPO $TAG"
curl -fsSL "https://github.com/$REPO/archive/refs/tags/$TAG.tar.gz" | tar xz -C "$TMP"

SRC=$(find "$TMP" -type d -path "*/plugins/$PLUGIN/skills" | head -n 1)
if [ -z "$SRC" ]; then
  echo "no plugins/$PLUGIN/skills/ directory in the $TAG tarball" >&2
  exit 1
fi

mkdir -p "$DEST"
cp -R "$SRC"/. "$DEST"/

echo "$(find "$DEST" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ') skills installed into $DEST"
echo
echo "These skills plan only. They need the TargetBay Reviews MCP to read store data,"
echo "and they never send or activate anything without your explicit approval."
