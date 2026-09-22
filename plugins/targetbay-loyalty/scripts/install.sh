#!/bin/sh
# Install TargetBay Loyalty Skills without npm.
#
#   curl -fsSL https://raw.githubusercontent.com/targetbay360/targetbay-agent-skills/main/plugins/targetbay-loyalty/scripts/install.sh | sh
#   sh scripts/install.sh --global            -> ~/.claude/skills
#   sh scripts/install.sh /custom/skills/dir  -> that directory
#   sh scripts/install.sh --force             -> overwrite skills already present
#
# Defaults to ./.claude/skills, and leaves an existing skill alone unless --force,
# both matching install.mjs.
#
# Downloads the latest release tarball for THIS plugin and copies its skills/ into the
# destination. Releases are tagged <plugin>@<version>, so the lookup filters by prefix
# rather than using /releases/latest, which would return whichever plugin shipped last.

set -eu

REPO="targetbay360/targetbay-agent-skills"
PLUGIN="targetbay-loyalty"
FORCE=0
DEST=""
for arg in "$@"; do
  case "$arg" in
    --force)  FORCE=1 ;;
    --global) DEST="$HOME/.claude/skills" ;;
    -*)       echo "unknown option: $arg" >&2; exit 1 ;;
    *)        DEST="$arg" ;;
  esac
done
[ -n "$DEST" ] || DEST="./.claude/skills"

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

# A skill cites ../../rules/, ../../knowledge/ and ../../schemas/ from inside the plugin tree.
# Flattening skills/ into $DEST puts those targets out of reach, so point them at the released
# files instead — the same full-URL rule this repository applies to any reference that leaves its
# own directory. Sibling-skill links (../other-skill/SKILL.md) still resolve and are left alone.
# Rewriting is scoped to the skill just copied: $DEST may hold skills from another plugin, whose
# citations resolve against a different plugin directory.
BLOB="https://github.com/$REPO/blob/$TAG/plugins/$PLUGIN"

WRITTEN=0
SKIPPED=0

for skill in "$SRC"/*/; do
  name=$(basename "$skill")

  if [ "$FORCE" -eq 0 ] && [ -d "$DEST/$name" ]; then
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  rm -rf "$DEST/$name"
  cp -R "$skill" "$DEST/$name"

  find "$DEST/$name" -name '*.md' -type f -exec sed -i.bak \
    -e "s#\[\.\./\.\./\([^]]*\)\](\.\./\.\./\([^)]*\))#[\1]($BLOB/\2)#g" \
    -e "s#](\.\./\.\./\([^)]*\))#]($BLOB/\1)#g" {} +
  find "$DEST/$name" -name '*.md.bak' -type f -delete

  WRITTEN=$((WRITTEN + 1))
done

echo "$WRITTEN skills installed into $DEST"

if [ "$SKIPPED" -gt 0 ]; then
  echo "$SKIPPED already present, left alone — rerun with --force to overwrite"
fi

# Parity with install.mjs, which installs slash commands alongside a .claude tree.
CMD_SRC=$(find "$TMP" -type d -path "*/plugins/$PLUGIN/commands" | head -n 1)
case "$DEST" in
  */.claude/skills|*/.claude/skills/)
    if [ -n "$CMD_SRC" ]; then
      CMD_DEST="$(dirname "$DEST")/commands"
      mkdir -p "$CMD_DEST"
      cp -R "$CMD_SRC"/. "$CMD_DEST"/
      echo "slash commands installed into $CMD_DEST"
    fi
    ;;
esac

echo
echo "These skills plan only. They need the TargetBay Loyalty MCP to read store data,"
echo "and they never send or activate anything without your explicit approval."
