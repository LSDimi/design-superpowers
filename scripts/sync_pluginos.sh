#!/usr/bin/env bash
# Re-vendor the pluginos-figma skill from upstream @pluginos/claude-plugin.
#
# Usage: ./scripts/sync_pluginos.sh
#        PLUGINOS_BRANCH=feat/sprints-b-c-activation ./scripts/sync_pluginos.sh
#
# Clones github.com/LSDimi/PluginOS (shallow, branch = $PLUGINOS_BRANCH or main),
# copies the claude-plugin skill dir into skills/pluginos-figma/, updates
# UPSTREAM.md with the source SHA and sync date, and validates the result.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="$REPO_ROOT/skills/pluginos-figma"
UPSTREAM_MD="$SKILL_DIR/UPSTREAM.md"
SOURCE_DIR="packages/claude-plugin/skills/pluginos-figma"
BRANCH="${PLUGINOS_BRANCH:-main}"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "==> Cloning PluginOS (branch: $BRANCH)..."
git clone --depth=1 --branch "$BRANCH" https://github.com/LSDimi/PluginOS.git "$TMP/pluginos" >/dev/null 2>&1
cd "$TMP/pluginos"
UPSTREAM_SHA=$(git rev-parse HEAD)
cd - >/dev/null

SOURCE_PATH="$TMP/pluginos/$SOURCE_DIR"
if [[ ! -d "$SOURCE_PATH" ]]; then
  echo "ERROR: upstream skill dir not found at $SOURCE_DIR on branch $BRANCH" >&2
  echo "If v0.4.0 hasn't merged yet, try: PLUGINOS_BRANCH=feat/sprints-b-c-activation $0" >&2
  exit 1
fi

echo "==> Syncing skill directory (preserving UPSTREAM.md)..."
# Remove everything except UPSTREAM.md so stale files from upstream don't linger.
find "$SKILL_DIR" -mindepth 1 -not -name "UPSTREAM.md" -delete
cp -R "$SOURCE_PATH/." "$SKILL_DIR/"

TODAY=$(date +%Y-%m-%d)
echo "==> Updating UPSTREAM.md..."
cat >"$UPSTREAM_MD" <<EOF
# PluginOS Figma skill — vendored

**Source:** https://github.com/LSDimi/PluginOS/tree/$UPSTREAM_SHA/packages/claude-plugin
**Vendored at SHA:** \`$UPSTREAM_SHA\`
**Vendored from branch:** \`$BRANCH\`
**Vendored on:** \`$TODAY\`
**Synced by:** \`scripts/sync_pluginos.sh\`

This directory is a snapshot of the upstream \`@pluginos/claude-plugin\`
package. Do not hand-edit SKILL.md or references/ — changes will be
overwritten on the next sync. To update, run \`scripts/sync_pluginos.sh\`
at the repo root.
EOF

echo "==> Running validator..."
python3 "$REPO_ROOT/scripts/validate_plugin.py"

echo "==> Sync complete. Changes (if any):"
cd "$REPO_ROOT"
git status --short skills/pluginos-figma/
