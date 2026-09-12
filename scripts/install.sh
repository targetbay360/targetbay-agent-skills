#!/bin/sh
# Install TargetBay Email & SMS Marketing Skills without npm.
#
#   curl -fsSL https://raw.githubusercontent.com/targetbay360/targetbay-email-sms-marketing-skills/main/scripts/install.sh | sh
#   sh scripts/install.sh /custom/skills/dir
#
# Downloads the latest GitHub release tarball and copies skills/ into the destination.

set -eu

REPO="targetbay360/targetbay-email-sms-marketing-skills"
DEST="${1:-$HOME/.claude/skills}"

command -v curl >/dev/null 2>&1 || { echo "curl is required" >&2; exit 1; }
command -v tar  >/dev/null 2>&1 || { echo "tar is required" >&2; exit 1; }

TAG=$(curl -fsSL "https://api.github.com/repos/$REPO/releases/latest" \
  | sed -n 's/.*"tag_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
  | head -n 1)

if [ -z "$TAG" ]; then
  echo "could not resolve the latest release of $REPO" >&2
  echo "check https://github.com/$REPO/releases" >&2
  exit 1
fi

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "downloading $REPO $TAG"
curl -fsSL "https://github.com/$REPO/archive/refs/tags/$TAG.tar.gz" | tar xz -C "$TMP"

SRC=$(find "$TMP" -maxdepth 2 -type d -name skills | head -n 1)
if [ -z "$SRC" ]; then
  echo "no skills/ directory in the $TAG tarball" >&2
  exit 1
fi

mkdir -p "$DEST"
cp -R "$SRC"/. "$DEST"/

echo "$(find "$DEST" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ') skills installed into $DEST"
echo
echo "These skills plan only. They need the BayEngage MCP to read store data,"
echo "and they never send or activate anything without your explicit approval."
