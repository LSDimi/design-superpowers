# PluginOS Bundled Integration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship design-superpowers v0.2.0 with PluginOS bundled as an auto-registered MCP server and a vendored `pluginos-figma` skill, plus a weekly CI sync to track upstream changes automatically.

**Architecture:** Declare `mcpServers.pluginos` in `.claude-plugin/plugin.json` (Claude Code auto-registers on install), vendor the upstream `pluginos-figma` skill into `skills/pluginos-figma/`, simplify `skills/shared/figma-adapter.md` to a single bridge-install step, and add `scripts/sync_pluginos.sh` + `.github/workflows/sync-pluginos.yml` that auto-PRs upstream updates weekly.

**Tech Stack:** Claude Code plugin manifests (JSON), Python 3.12 (validator, doctests), Bash (sync script), GitHub Actions, `peter-evans/create-pull-request@v6`.

**Spec:** `docs/superpowers/specs/2026-04-20-pluginos-bundled-integration-design.md`

---

## Task Order and Dependencies

```
Task 1 (validator extension, doctest TDD)
   ↓
Task 2 (plugin.json: version + mcpServers) ── depends on Task 1
   ↓
Task 3 (vendor pluginos-figma skill)        ── independent, run in parallel with 2
   ↓
Task 4 (sync_pluginos.sh)                   ── depends on Task 3 (directory must exist)
   ↓
Task 5 (weekly CI workflow)                 ── depends on Task 4
   ↓
Task 6 (figma-adapter.md rewrite)           ── independent of 1–5
   ↓
Task 7 (ds-context-schema.md defaults)      ── depends on Task 6
   ↓
Task 8 (README "Getting started" rewrite)   ── depends on Tasks 2, 3, 6
   ↓
Task 9 (final validation + release tag)     ── depends on all
```

---

## File Structure

**New files:**
- `skills/pluginos-figma/SKILL.md` — vendored from `@pluginos/claude-plugin`
- `skills/pluginos-figma/UPSTREAM.md` — records source SHA, vendored date
- `scripts/sync_pluginos.sh` — re-vendors the skill from upstream
- `.github/workflows/sync-pluginos.yml` — weekly cron, auto-PR

**Modified files:**
- `.claude-plugin/plugin.json` — add `mcpServers`, bump version to 0.2.0
- `scripts/validate_plugin.py` — add MCP command portability check
- `skills/shared/figma-adapter.md` — simplified pitch copy
- `skills/shared/ds-context-schema.md` — `figma.adapter` default becomes `pluginos`
- `README.md` — "Getting started" reflects bundled PluginOS

**Unchanged:** all six `/creative`, `/ds-make`, etc. skills, shared knowledge, existing specs.

---

### Task 1: Extend validator with doctest-driven MCP command check

**Files:**
- Modify: `scripts/validate_plugin.py`

- [ ] **Step 1: Add a failing doctest for `classify_mcp_command`**

Add this function stub near the top of `scripts/validate_plugin.py`, right after the existing regex constants (around line 30):

```python
def classify_mcp_command(cmd: str) -> str:
    """Classify an MCP server command string for portability.

    Returns one of: 'absolute', 'plugin-root', 'path-binary', 'relative'.

    >>> classify_mcp_command("/usr/local/bin/node")
    'absolute'
    >>> classify_mcp_command("${CLAUDE_PLUGIN_ROOT}/bin/server.sh")
    'plugin-root'
    >>> classify_mcp_command("npx")
    'path-binary'
    >>> classify_mcp_command("node")
    'path-binary'
    >>> classify_mcp_command("./scripts/local.sh")
    'relative'
    >>> classify_mcp_command("../other/thing.sh")
    'relative'
    """
    raise NotImplementedError
```

- [ ] **Step 2: Run doctests and confirm they fail**

Run:
```bash
python3 -m doctest scripts/validate_plugin.py -v 2>&1 | tail -20
```

Expected: `NotImplementedError` raised for every classify call; summary reports `***Test Failed***`.

- [ ] **Step 3: Implement `classify_mcp_command`**

Replace the `raise NotImplementedError` body with:

```python
    if cmd.startswith("${CLAUDE_PLUGIN_ROOT}"):
        return "plugin-root"
    if cmd.startswith("/"):
        return "absolute"
    if cmd.startswith("./") or cmd.startswith("../"):
        return "relative"
    return "path-binary"
```

- [ ] **Step 4: Run doctests and confirm they pass**

Run:
```bash
python3 -m doctest scripts/validate_plugin.py -v 2>&1 | tail -10
```

Expected: `6 tests in 1 items. 6 passed and 0 failed. Test passed.`

- [ ] **Step 5: Wire the classifier into `validate_plugin_json`**

Find the existing `validate_plugin_json` function. After the `missing` check (around line 58), append this block before the final `return`:

```python
    mcp_servers = data.get("mcpServers", {})
    for server_name, server_cfg in mcp_servers.items():
        cmd = server_cfg.get("command", "")
        if not cmd:
            errors.append(
                f"{PLUGIN_JSON.relative_to(ROOT)}: mcpServers.{server_name} missing 'command'"
            )
            continue
        classification = classify_mcp_command(cmd)
        if classification == "relative":
            errors.append(
                f"{PLUGIN_JSON.relative_to(ROOT)}: mcpServers.{server_name}.command "
                f"is a relative path ({cmd!r}); use absolute, "
                "${CLAUDE_PLUGIN_ROOT}/..., or a $PATH-resolvable binary"
            )
```

- [ ] **Step 6: Run the validator on current state**

Run:
```bash
python3 scripts/validate_plugin.py
```

Expected: `Plugin validation OK` (current `plugin.json` has no `mcpServers`, so the new block is a no-op).

- [ ] **Step 7: Commit**

```bash
git add scripts/validate_plugin.py
git commit -m "test: add classify_mcp_command doctest + wire into plugin.json validator

Adds a portability check for mcpServers commands: absolute paths,
\${CLAUDE_PLUGIN_ROOT}/... paths, and \$PATH-resolvable binaries pass;
relative ./... or ../... paths fail with a clear message.

Doctest-driven. Runs via: python3 -m doctest scripts/validate_plugin.py"
```

---

### Task 2: Add `mcpServers` block to `plugin.json` and bump version

**Files:**
- Modify: `.claude-plugin/plugin.json`

- [ ] **Step 1: Read current plugin.json**

```bash
cat .claude-plugin/plugin.json
```

Expected output:
```json
{
  "name": "design-superpowers",
  "version": "0.1.0",
  "description": "Six universal Claude Code commands for design teams...",
  "author": {
    "name": "Dimitrios Arapis"
  }
}
```

- [ ] **Step 2: Rewrite plugin.json with mcpServers and version bump**

Replace the file contents with:

```json
{
  "name": "design-superpowers",
  "version": "0.2.0",
  "description": "Six universal Claude Code commands for design teams, backed by a 4-layer knowledge system. Ships with PluginOS for Figma integration.",
  "author": {
    "name": "Dimitrios Arapis"
  },
  "mcpServers": {
    "pluginos": {
      "command": "npx",
      "args": ["-y", "pluginos"]
    }
  }
}
```

Note: version jumps 0.1.0 → 0.2.0 because this is a material behaviour change (auto-installs an MCP server). Description is updated to advertise the bundling.

- [ ] **Step 3: Verify JSON parses**

Run:
```bash
python3 -c "import json; json.load(open('.claude-plugin/plugin.json')); print('OK')"
```

Expected: `OK`.

- [ ] **Step 4: Run the validator (now exercises the new check)**

Run:
```bash
python3 scripts/validate_plugin.py
```

Expected: `Plugin validation OK`. (The `npx` command classifies as `path-binary`, no errors.)

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "feat(plugin): bundle PluginOS MCP server, bump to v0.2.0

Declares mcpServers.pluginos in plugin.json so Claude Code auto-registers
and starts \`npx -y pluginos\` when the plugin is installed. Removes the
prior manual ~/.claude/settings.json edit from the user's onboarding.

Floating (unpinned) install — PluginOS is in active development; pinning
would block bug fixes. Pin reactively if a bad release ships.

Spec: docs/superpowers/specs/2026-04-20-pluginos-bundled-integration-design.md"
```

---

### Task 3: Vendor the `pluginos-figma` skill from upstream

**Files:**
- Create: `skills/pluginos-figma/SKILL.md`
- Create: `skills/pluginos-figma/UPSTREAM.md`

- [ ] **Step 1: Clone PluginOS to a temp dir**

Run:
```bash
TMP=$(mktemp -d)
git clone --depth=1 https://github.com/LSDimi/PluginOS.git "$TMP/pluginos"
cd "$TMP/pluginos"
UPSTREAM_SHA=$(git rev-parse HEAD)
echo "Upstream SHA: $UPSTREAM_SHA"
cd -
```

Expected: clone succeeds, SHA printed.

- [ ] **Step 2: Verify the upstream skill exists**

Run:
```bash
ls "$TMP/pluginos/packages/claude-plugin/skills/pluginos-figma/SKILL.md"
```

Expected: the file path prints. If it doesn't exist (v0.4.0 PR not yet merged to main), fall back to cloning the PR branch:

```bash
rm -rf "$TMP/pluginos"
git clone --depth=1 --branch v0.4.0 https://github.com/LSDimi/PluginOS.git "$TMP/pluginos"
cd "$TMP/pluginos" && UPSTREAM_SHA=$(git rev-parse HEAD) && cd -
ls "$TMP/pluginos/packages/claude-plugin/skills/pluginos-figma/SKILL.md"
```

If neither works, STOP and report the issue — v0.4.0 is expected to be available per the spec; an investigation is needed.

- [ ] **Step 3: Create `skills/pluginos-figma/` and copy the skill**

Run:
```bash
mkdir -p skills/pluginos-figma
cp "$TMP/pluginos/packages/claude-plugin/skills/pluginos-figma/SKILL.md" skills/pluginos-figma/SKILL.md
```

- [ ] **Step 4: Verify the copied SKILL.md has valid frontmatter**

Run:
```bash
head -5 skills/pluginos-figma/SKILL.md
```

Expected: starts with `---`, contains `name:` and `description:` lines, closes with `---`.

- [ ] **Step 5: Create `UPSTREAM.md`**

Write `skills/pluginos-figma/UPSTREAM.md` with this exact content (substitute `<SHA>` and `<DATE>` with real values from Step 1):

```markdown
# PluginOS Figma skill — vendored

**Source:** https://github.com/LSDimi/PluginOS/tree/<SHA>/packages/claude-plugin
**Vendored at SHA:** `<SHA>`
**Vendored on:** `<DATE>` (YYYY-MM-DD)
**Synced by:** `scripts/sync_pluginos.sh`

This directory is a snapshot of the upstream `@pluginos/claude-plugin`
package. Do not hand-edit SKILL.md — changes will be overwritten on
the next sync. To update, run `scripts/sync_pluginos.sh` at the repo root.
```

Use real values: `<SHA>` = the upstream SHA from Step 1, `<DATE>` = today's date (`date +%Y-%m-%d`).

- [ ] **Step 6: Run the validator**

Run:
```bash
python3 scripts/validate_plugin.py
```

Expected: `Plugin validation OK`. The validator sees the new SKILL.md and checks its frontmatter. `UPSTREAM.md` is not a SKILL.md so it's skipped by the skill-frontmatter check but still subject to the path-reference check — any `${CLAUDE_PLUGIN_ROOT}/...` references it contains must resolve.

- [ ] **Step 7: Clean up the temp dir**

Run:
```bash
rm -rf "$TMP"
```

- [ ] **Step 8: Commit**

```bash
git add skills/pluginos-figma/
git commit -m "feat(skills): vendor pluginos-figma skill from @pluginos/claude-plugin

Snapshots the upstream Claude Code skill for PluginOS so design-superpowers
ships the full operation reference (~1100 tokens, 26 operations) without
requiring a separate plugin install.

Source SHA recorded in UPSTREAM.md. Re-sync with scripts/sync_pluginos.sh."
```

---

### Task 4: Write `scripts/sync_pluginos.sh`

**Files:**
- Create: `scripts/sync_pluginos.sh`

- [ ] **Step 1: Create the script**

Write `scripts/sync_pluginos.sh` with exactly this content:

```bash
#!/usr/bin/env bash
# Re-vendor the pluginos-figma skill from upstream @pluginos/claude-plugin.
#
# Usage: ./scripts/sync_pluginos.sh
#
# Clones github.com/LSDimi/PluginOS (shallow), copies the claude-plugin
# skill into skills/pluginos-figma/, updates UPSTREAM.md with the source
# SHA and sync date, and validates the result.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="$REPO_ROOT/skills/pluginos-figma"
UPSTREAM_MD="$SKILL_DIR/UPSTREAM.md"
SOURCE_SKILL="packages/claude-plugin/skills/pluginos-figma/SKILL.md"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "==> Cloning PluginOS..."
git clone --depth=1 https://github.com/LSDimi/PluginOS.git "$TMP/pluginos" >/dev/null 2>&1
cd "$TMP/pluginos"
UPSTREAM_SHA=$(git rev-parse HEAD)
cd - >/dev/null

SOURCE_PATH="$TMP/pluginos/$SOURCE_SKILL"
if [[ ! -f "$SOURCE_PATH" ]]; then
  echo "ERROR: upstream skill not found at $SOURCE_SKILL" >&2
  echo "Upstream may not have merged @pluginos/claude-plugin yet." >&2
  exit 1
fi

echo "==> Copying skill file..."
mkdir -p "$SKILL_DIR"
cp "$SOURCE_PATH" "$SKILL_DIR/SKILL.md"

TODAY=$(date +%Y-%m-%d)
echo "==> Updating UPSTREAM.md..."
cat >"$UPSTREAM_MD" <<EOF
# PluginOS Figma skill — vendored

**Source:** https://github.com/LSDimi/PluginOS/tree/$UPSTREAM_SHA/packages/claude-plugin
**Vendored at SHA:** \`$UPSTREAM_SHA\`
**Vendored on:** \`$TODAY\`
**Synced by:** \`scripts/sync_pluginos.sh\`

This directory is a snapshot of the upstream \`@pluginos/claude-plugin\`
package. Do not hand-edit SKILL.md — changes will be overwritten on
the next sync. To update, run \`scripts/sync_pluginos.sh\` at the repo root.
EOF

echo "==> Running validator..."
python3 "$REPO_ROOT/scripts/validate_plugin.py"

echo "==> Sync complete. Changes (if any):"
cd "$REPO_ROOT"
git status --short skills/pluginos-figma/
```

- [ ] **Step 2: Make the script executable**

Run:
```bash
chmod +x scripts/sync_pluginos.sh
```

- [ ] **Step 3: Run the script to verify idempotency**

Run:
```bash
./scripts/sync_pluginos.sh
```

Expected: script completes without error, validator says `Plugin validation OK`. If the vendored skill is already current, `git status --short skills/pluginos-figma/` output should show only `UPSTREAM.md` as modified (date updated) or nothing.

- [ ] **Step 4: Revert any date-only changes from the test run**

If Step 3 only changed `UPSTREAM.md`'s vendored-on date, restore it:
```bash
git restore skills/pluginos-figma/UPSTREAM.md
```

This keeps the commit from Task 3 intact as the authoritative vendoring checkpoint.

- [ ] **Step 5: Commit the script**

```bash
git add scripts/sync_pluginos.sh
git commit -m "feat(scripts): add sync_pluginos.sh for re-vendoring the skill

Shallow-clones PluginOS, copies packages/claude-plugin/skills/pluginos-figma/
SKILL.md into this repo's skills/pluginos-figma/, updates UPSTREAM.md,
and runs the validator. Intended for both maintainer-triggered runs
and the weekly CI sync workflow (Task 5)."
```

---

### Task 5: Weekly CI workflow with auto-PR

**Files:**
- Create: `.github/workflows/sync-pluginos.yml`

- [ ] **Step 1: Create the workflow**

Write `.github/workflows/sync-pluginos.yml` with exactly this content:

```yaml
name: Sync PluginOS skill

on:
  schedule:
    # Monday 06:00 UTC
    - cron: "0 6 * * 1"
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Run sync script
        run: ./scripts/sync_pluginos.sh

      - name: Create or update PR
        uses: peter-evans/create-pull-request@v6
        with:
          branch: chore/sync-pluginos
          title: "chore: sync pluginos-figma skill from upstream"
          body: |
            Weekly automated sync of the vendored `pluginos-figma` skill
            from [LSDimi/PluginOS](https://github.com/LSDimi/PluginOS).

            **Source SHA:** see `skills/pluginos-figma/UPSTREAM.md`
            **Script:** `scripts/sync_pluginos.sh`

            Close this PR if you don't want the update. It will be
            re-opened next week if upstream changes again.
          commit-message: "chore: sync pluginos-figma skill"
          delete-branch: false
```

Notes on choices:
- Fixed branch `chore/sync-pluginos` so subsequent runs update the existing PR instead of spawning new ones.
- `delete-branch: false` preserves the branch across runs.
- `workflow_dispatch` lets maintainers trigger a sync manually from the Actions tab.

- [ ] **Step 2: Lint the workflow locally (optional but recommended)**

If `actionlint` is available:
```bash
actionlint .github/workflows/sync-pluginos.yml
```

Expected: no output (no errors). If `actionlint` is not installed, skip — GitHub will surface errors on push.

- [ ] **Step 3: Run the existing validator to confirm nothing breaks**

Run:
```bash
python3 scripts/validate_plugin.py
```

Expected: `Plugin validation OK`.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/sync-pluginos.yml
git commit -m "ci: weekly auto-PR syncing pluginos-figma from upstream

Runs every Monday 06:00 UTC. Shallow-clones PluginOS, re-vendors the
skill via scripts/sync_pluginos.sh, and opens (or updates) a PR on
the fixed branch chore/sync-pluginos.

Also supports manual trigger via workflow_dispatch."
```

---

### Task 6: Rewrite `figma-adapter.md` pitch

**Files:**
- Modify: `skills/shared/figma-adapter.md`

- [ ] **Step 1: Read current figma-adapter.md**

```bash
cat skills/shared/figma-adapter.md
```

Note the current structure: pitch copy that offers PluginOS vs classic Figma MCP as a choice, with setup instructions for each.

- [ ] **Step 2: Rewrite the pitch to reflect bundled PluginOS**

Replace the entire contents of `skills/shared/figma-adapter.md` with:

````markdown
# Figma Adapter

How design-superpowers sub-agents talk to Figma.

## Default: PluginOS (bundled)

design-superpowers ships with PluginOS as its Figma adapter. When the plugin is installed, Claude Code auto-registers the `pluginos` MCP server (declared in `.claude-plugin/plugin.json`) and the `mcp__pluginos__*` tools become available in every session.

**Operation reference:** `${CLAUDE_PLUGIN_ROOT}/skills/pluginos-figma/SKILL.md` — vendored from `@pluginos/claude-plugin`. Sub-agents load this when routing a Figma operation.

## First-use bridge setup

The MCP server alone is not enough — PluginOS needs a bridge plugin running inside Figma Desktop for the tools to actually do anything. This is the only manual step.

**When to show this pitch:** if any `mcp__pluginos__*` tool call fails with a connection-refused or bridge-not-running error, the sub-agent stops and shows the pitch:

> **Figma bridge not running**
>
> design-superpowers uses PluginOS for Figma. Your MCP server is registered, but the bridge plugin inside Figma Desktop isn't connected yet.
>
> The [PluginOS MCP Bridge](https://www.figma.com/community/plugin/1626608701431483287/pluginos-mcp-bridge-for-llms) is currently under Figma Community review. Until approved, use dev-import:
>
> 1. Open Figma Desktop → **Plugins** → **Development** → **Import plugin from manifest**
> 2. Select the manifest from your PluginOS install. It prints the path on first `npx pluginos` run — check your Claude Code session log or run `npx pluginos --manifest-path`.
> 3. In Figma: **Plugins** → **Development** → **PluginOS MCP Bridge** to start it.
>
> Once the Community listing is live, one click from that URL will install the bridge — no dev-import required.
>
> Retry your command once the bridge is running.

## Detection algorithm (runs per Figma-touching sub-agent)

```
1. Sub-agent about to call mcp__pluginos__*?
2. Attempt the call.
3. On success: proceed.
4. On "bridge not running" error: show pitch (above), stop.
5. On any other error: surface it verbatim — sub-agent does not retry.
```

The sub-agent does NOT pre-check whether the bridge is running before each call — a pre-check is a waste of round-trips. The first real call either works or returns a bridge error, and the pitch handles the error case.

## `.ds-context.md` fields

The adapter still writes to `.ds-context.md` for project-level state, but the schema is simpler now:

```yaml
figma:
  adapter: pluginos         # default; only set explicitly if using figma-mcp fallback
  status: ready             # ready | bridge-pending
```

- `adapter` defaults to `pluginos`. Only set explicitly to `figma-mcp` if you're running the classic Figma Dev Mode MCP as an opt-in fallback.
- `status: bridge-pending` is written automatically on the first bridge-not-running error; cleared to `ready` on the first successful call.

## Fallback: classic Figma MCP

Users with the classic Figma Dev Mode MCP (`mcp__Figma__*`) already configured can opt in by setting `figma.adapter: figma-mcp` in `.ds-context.md`. Sub-agents then route to `mcp__Figma__*` tools instead of `mcp__pluginos__*`. No auto-pitch for this path — users who want it already have it configured.

## Where this logic lives

- **This file** — pitch copy, detection algorithm, `.ds-context.md` schema for `figma`.
- **Each sub-agent that touches Figma** — references this file in its Knowledge block instead of hardcoding tool names.
- **`skills/pluginos-figma/SKILL.md`** — vendored operation reference; sub-agents load it when composing PluginOS calls.
````

- [ ] **Step 3: Run the validator**

Run:
```bash
python3 scripts/validate_plugin.py
```

Expected: `Plugin validation OK`. The `${CLAUDE_PLUGIN_ROOT}/skills/pluginos-figma/SKILL.md` reference resolves because Task 3 created that file.

- [ ] **Step 4: Commit**

```bash
git add skills/shared/figma-adapter.md
git commit -m "feat(adapter): simplify figma-adapter pitch for bundled PluginOS

PluginOS is now bundled (see plugin.json mcpServers), so the adapter
no longer needs to pitch it vs classic Figma MCP on first use. The
remaining pitch covers the one manual step — bridge plugin install
in Figma Desktop — with a Community-listing link and dev-import
fallback for until approval.

Classic Figma MCP becomes an opt-in fallback via figma.adapter:
figma-mcp in .ds-context.md."
```

---

### Task 7: Update `ds-context-schema.md` defaults

**Files:**
- Modify: `skills/shared/ds-context-schema.md`

- [ ] **Step 1: Find the `figma.adapter` row in the schema**

Run:
```bash
grep -n "figma.adapter" skills/shared/ds-context-schema.md
```

Expected: one or more line numbers printed. Note them.

- [ ] **Step 2: Read the surrounding rows**

```bash
grep -n "figma\." skills/shared/ds-context-schema.md
```

Review the `figma.adapter`, `figma.status` rows and their `default` column.

- [ ] **Step 3: Update the defaults**

Use the Edit tool (or manual edit) to change:
- `figma.adapter` default: `unset` → `pluginos`
- `figma.status` default: `unset` → `ready`
- `figma.adapter` valid values: keep `pluginos | figma-mcp`; remove `unset` from the list if it's there

Also update the description text for `figma.adapter` to mention: "Defaults to `pluginos` — the bundled adapter. Only set explicitly to `figma-mcp` if opting into the classic Figma Dev Mode MCP fallback."

- [ ] **Step 4: Run the validator**

```bash
python3 scripts/validate_plugin.py
```

Expected: `Plugin validation OK`.

- [ ] **Step 5: Commit**

```bash
git add skills/shared/ds-context-schema.md
git commit -m "docs(schema): update figma.adapter default to 'pluginos'

Reflects the bundled PluginOS adapter shipped with v0.2.0. Users
who want the classic Figma Dev Mode MCP opt in explicitly by
setting figma.adapter: figma-mcp."
```

---

### Task 8: Update `README.md` "Getting started" section

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read the current "Getting started" section**

```bash
awk '/^## Getting started/,/^## Project layout/' README.md
```

Expected: prints the section. Note the current 3-step numbered list.

- [ ] **Step 2: Replace the section**

Use Edit tool to replace the content between `## Getting started` and `## Project layout` with:

```markdown
## Getting started

1. **Install the plugin.** Point Claude Code at this directory (or install from the GitHub release). On first session after install, Claude Code auto-registers the `pluginos` MCP server declared in `plugin.json` — no manual config edit required.

2. **Install the Figma bridge** (one-time, per machine).

   The [PluginOS MCP Bridge](https://www.figma.com/community/plugin/1626608701431483287/pluginos-mcp-bridge-for-llms) is currently under Figma Community review. Until approved, dev-import it:

   - Figma Desktop → Plugins → Development → Import plugin from manifest
   - Run `npx pluginos --manifest-path` in a terminal to get the path
   - Run the bridge from Plugins → Development → PluginOS MCP Bridge

   Once the Community listing is live, this becomes a single click from the URL above.

3. **Run any command.** `/creative`, `/ds-make`, `/design`, `/design-review`, `/map-design`, `/ds-manage` — each detects project maturity (L0 Greenfield → L3 Enterprise) and asks 2–3 clarifying questions before acting.

4. **Optional: for existing design systems**, create a `.ds-context.md` at your project root with Figma library keys, token collection names, and governance metadata. See `skills/shared/ds-context-schema.md` for the full schema.

**Team entry point:** [`skills/README.md`](skills/README.md) — routing matrix, architecture diagram, and a quick reference for designers.
```

- [ ] **Step 3: Verify the README still renders correctly**

Run:
```bash
head -60 README.md
```

Visually confirm the banner image, the "What it does" header, the command table, and the new "Getting started" flow all appear in order.

- [ ] **Step 4: Run the validator**

```bash
python3 scripts/validate_plugin.py
```

Expected: `Plugin validation OK`.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "docs(readme): reflect bundled PluginOS in Getting started

Step 1 is now 'install design-superpowers' — the MCP server is
auto-registered, no config edit. Step 2 is the one remaining manual
action (Figma bridge install) with both Community-listing and
dev-import paths covered."
```

---

### Task 9: Final validation pass + release tag

**Files:** none directly modified; this is a verification and release task.

- [ ] **Step 1: Run the validator from a clean state**

```bash
python3 scripts/validate_plugin.py
```

Expected: `Plugin validation OK`. If anything fails here, fix the failing check before proceeding.

- [ ] **Step 2: Run the doctests**

```bash
python3 -m doctest scripts/validate_plugin.py -v 2>&1 | tail -5
```

Expected: `Test passed.` summary.

- [ ] **Step 3: Dry-run the sync script**

```bash
./scripts/sync_pluginos.sh
```

Expected: clones, copies, validator passes. If it produces a diff, review it — may indicate upstream has updated since Task 3. Commit or discard as appropriate.

- [ ] **Step 4: Review the full commit log for this feature**

```bash
git log --oneline origin/main..HEAD
```

Expected: roughly 7–9 commits (one per task that produced commits — Task 4's Step 4 may or may not have committed).

- [ ] **Step 5: Push all commits to main**

```bash
git push origin main
```

Expected: push succeeds.

- [ ] **Step 6: Create and push the v0.2.0 tag**

```bash
git tag -a v0.2.0 -m "design-superpowers v0.2.0 — PluginOS bundled

PluginOS is now auto-registered as an MCP server when the plugin is
installed. The pluginos-figma skill is vendored into the repo.
Weekly CI sync keeps the skill current.

See docs/superpowers/specs/2026-04-20-pluginos-bundled-integration-design.md
for the design decisions."
git push origin v0.2.0
```

- [ ] **Step 7: Verify on GitHub**

Open in a browser:
- `https://github.com/LSDimi/design-superpowers/tags` — confirm `v0.2.0` is listed.
- `https://github.com/LSDimi/design-superpowers/actions` — confirm the `Validate plugin` workflow passed on the latest main.
- `https://github.com/LSDimi/design-superpowers/actions/workflows/sync-pluginos.yml` — confirm the new workflow is registered and can be manually dispatched.

If any check fails, fix before closing the plan.

- [ ] **Step 8: Manual install test (recommended)**

From a fresh Claude Code session in a test project:

```
/plugin install <github-url-or-local-path>
```

Then in the session, run `/creative` (or any command that exercises PluginOS). Expected:
- `npx -y pluginos` runs silently on first tool call.
- First `mcp__pluginos__*` call returns the "bridge not running" error.
- The `figma-adapter.md` pitch (Task 6) fires with the Community link and dev-import fallback.
- After bridge install, the command completes.

Document any surprises as follow-up tasks. Do NOT mark this step complete until the flow works end-to-end on at least one machine.

---

## Self-Review Checklist

- [x] **Spec coverage:**
  - Section 3 (plugin.json) → Task 2
  - Section 4 (vendored skill) → Task 3
  - Section 5 (sync script) → Task 4
  - Section 5 (CI sync) → Task 5
  - Section 6 (figma-adapter.md) → Task 6
  - Section 7 (Community handoff) → covered in Task 6 pitch copy + Task 8 README
  - Section 8 (validator updates) → Task 1
  - Section 9 (testing plan) → Task 9
  - Section 11 (resolved decisions) → embedded in each relevant task

- [x] **Placeholder scan:** No TBDs, TODOs, or "similar to Task N" references. All code and paths are explicit.

- [x] **Type/name consistency:** `classify_mcp_command` used consistently in Task 1 steps. `scripts/sync_pluginos.sh` path consistent across Tasks 4, 5, 9. `skills/pluginos-figma/SKILL.md` and `UPSTREAM.md` paths consistent across Tasks 3, 4, 5.

- [x] **No contradictions:** Task 2 bumps version to 0.2.0; Task 9 Step 6 tags `v0.2.0`. Match. `npx -y pluginos` used consistently. Figma Community URL identical across Tasks 6, 8.
