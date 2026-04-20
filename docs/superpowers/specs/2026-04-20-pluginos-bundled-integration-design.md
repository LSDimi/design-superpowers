# PluginOS Bundled Integration — Design Spec

> **Date:** 2026-04-20
> **Status:** Draft (awaiting user review)
> **Depends on:** `2026-04-13-pluginos-integration-and-tone-decoupling.md`
> **Supersedes:** the "PluginOS as primary Figma adapter" section of the 2026-04-13 spec, which assumed PluginOS lives as a separate install.

---

## 1. Goals

1. **Zero-friction install.** A user who installs design-superpowers can run any Figma-touching command immediately — no separate MCP install, no Claude restart.
2. **Skill parity.** The full PluginOS operation vocabulary (all 26 operations as of v0.4.0) is available to design-superpowers sub-agents from first boot.
3. **Bridge install is one click.** The only remaining manual step — importing the bridge plugin into Figma Desktop — is reduced to a single link users click.
4. **Upstream syncs stay trivial.** When PluginOS ships new operations, a script re-vendors the skill in one command. No hand-merging.

---

## 2. Decision: Why `mcpServers` + Vendored Skill

Claude Code plugins have two primitives relevant here:

- **`mcpServers` in `plugin.json`** — declares MCP servers that Claude Code auto-registers and starts when the plugin is installed. Confirmed in the official `plugin-dev` skill's `mcp-integration/SKILL.md`.
- **`skills/<name>/SKILL.md`** — skill files loaded as slash commands and contextual skills.

Using both together means design-superpowers can ship:

1. A registered `pluginos` MCP server (`npx -y pluginos`) — no user action required.
2. A vendored `skills/pluginos-figma/` skill — Claude has the operation reference from the first message.

The user's prior experience required: quit Claude → edit `~/.claude/settings.json` → install PluginOS → restart → import bridge plugin. This design collapses the first four steps to zero.

### Rejected alternatives

| Alternative | Why rejected |
|---|---|
| Git submodule on `@pluginos/claude-plugin` | Claude Code's plugin loader doesn't resolve submodule plugins; users would need `git submodule update --init`. Friction for non-dev designers. |
| Pure setup skill (`/setup`), no vendoring | Still asks users to stop and install PluginOS separately. Smoother, but doesn't remove the friction the user specifically called out. |
| `npm install` as a post-install hook | Claude Code plugins don't have post-install hooks that run arbitrary commands at install time. `npx -y` inside the declared MCP server achieves the same effect at first use. |

---

## 3. `plugin.json` Changes

Current `.claude-plugin/plugin.json`:

```json
{
  "name": "design-superpowers",
  "version": "0.1.0",
  "description": "Six universal Claude Code commands for design teams...",
  "author": { "name": "Dimitrios Arapis" }
}
```

Add the `mcpServers` block:

```json
{
  "name": "design-superpowers",
  "version": "0.2.0",
  "description": "Six universal Claude Code commands for design teams...",
  "author": { "name": "Dimitrios Arapis" },
  "mcpServers": {
    "pluginos": {
      "command": "npx",
      "args": ["-y", "pluginos"]
    }
  }
}
```

**Behaviour on install:**

- Claude Code sees the `pluginos` server declaration.
- On first session after install, `npx -y pluginos` is executed. `-y` auto-accepts the download prompt, so the user sees nothing interactive.
- PluginOS's MCP tools (`mcp__pluginos__*`) appear in the session's tool list.
- If the bridge plugin isn't running in Figma Desktop, any Figma-touching tool call returns a clear error — handled by the pitch (Section 6).

**Version pinning: floating (not pinned).** PluginOS is in active development (v0.4.0 is still an open PR as of 2026-04-19). Pinning would require manual bumps on every upstream release and would block bug fixes from reaching users. `npx -y pluginos` resolves to the latest published version at install time. If a bad release ever ships, we pin reactively via a patch release of design-superpowers.

**Version bump rationale:** this is a material behaviour change (auto-installs an MCP server) — bumping from 0.1.0 → 0.2.0 signals that to users and to the validator's lockstep check.

---

## 4. Vendored Skill Structure

Add `skills/pluginos-figma/SKILL.md` to the repo, mirroring the upstream `@pluginos/claude-plugin` package.

### Layout

```
skills/
└── pluginos-figma/
    ├── SKILL.md                    # vendored from @pluginos/claude-plugin
    ├── UPSTREAM.md                 # records the source commit SHA
    └── .gitignore                  # nothing to ignore, but flags the dir as vendored
```

### Frontmatter contract

The vendored `SKILL.md` keeps its upstream `name: pluginos-figma` and `description`. design-superpowers does NOT rewrite this frontmatter — the skill has to advertise the same trigger conditions PluginOS designed it for, so that auto-invocation works correctly.

### `UPSTREAM.md` contents

```
# PluginOS Figma skill — vendored

Source: https://github.com/LSDimi/PluginOS/tree/<SHA>/packages/claude-plugin
Vendored at: <commit SHA>
Vendored on: YYYY-MM-DD
Synced by: scripts/sync_pluginos.sh
```

This file exists so anyone reviewing the skill knows it's not hand-written and can trace back to the exact upstream version.

---

## 5. Sync Script

Add `scripts/sync_pluginos.sh`. Purpose: pull the latest `packages/claude-plugin` from the PluginOS repo and overwrite `skills/pluginos-figma/`.

### Behaviour

1. Clone or fetch `github.com/LSDimi/PluginOS` into a temp dir (shallow clone, `--depth=1`).
2. Verify `packages/claude-plugin/skills/pluginos-figma/SKILL.md` exists in the clone.
3. Copy the skill directory into `skills/pluginos-figma/` in design-superpowers (overwriting).
4. Update `UPSTREAM.md` with the source commit SHA and current date.
5. Print a summary of what changed (file sizes, operation counts if extractable).
6. Exit 0 if the skill file is valid markdown with YAML frontmatter, 1 otherwise.

### Running it

The script is **not** run automatically. Invocation is a conscious act by a maintainer when PluginOS ships an update. Run as:

```bash
./scripts/sync_pluginos.sh
```

Followed by `python3 scripts/validate_plugin.py` to confirm nothing broke, then a commit whose message follows the pattern `chore: sync pluginos-figma skill @ <upstream-sha>`.

### CI

Add a weekly scheduled GitHub Actions job that runs the sync script and opens a PR if the vendored skill has changed. **Auto-PR over auto-issue:** a PR is reviewable in one glance, mergeable in one click, and auto-closable if stale; an issue just accrues todo debt. The workflow uses `peter-evans/create-pull-request` (or equivalent) with a fixed branch name (`chore/sync-pluginos`) so reruns update the existing PR rather than spawning duplicates.

The PR title follows the sync commit convention: `chore: sync pluginos-figma skill @ <upstream-sha>`. The body includes a diff summary and a link to the upstream commit range.

---

## 6. `figma-adapter.md` Update

The pitch currently assumes PluginOS may or may not be installed. With bundling, PluginOS is always installed. The adapter file simplifies:

### Before (simplified from existing)

> PluginOS or classic Figma MCP? Pick one. Setup instructions for each.

### After

> design-superpowers ships with PluginOS. Your MCP server is already registered.
>
> **One remaining step:** install the bridge plugin in Figma Desktop.
>
> The [PluginOS MCP Bridge](https://www.figma.com/community/plugin/1626608701431483287/pluginos-mcp-bridge-for-llms) is currently under Figma Community review. Until it's published, use dev-import:
>
> 1. Open Figma Desktop → Plugins → Development → Import plugin from manifest
> 2. Select the manifest from your PluginOS install (path printed on first run)
> 3. Run the plugin from Plugins → Development → PluginOS MCP Bridge
>
> Once the Community listing goes live, a single click from that URL will replace steps 1–2.
>
> Retry your command once the bridge is running.

### Detection flow

The existing detection in `figma-adapter.md` still runs. It checks if `mcp__pluginos__*` tools return a successful response. If yes → proceed. If no (bridge not running) → show the install pitch.

### `.ds-context.md` writes

`figma.adapter` defaults to `pluginos` (since it's always available). `figma.status` becomes `ready` once the bridge responds successfully. Classic Figma MCP becomes an opt-in fallback rather than a peer option.

### Remove the old pitch path

The "figma-mcp" decline path and the "pitch on first Figma action" language in the 2026-04-13 spec are obsoleted by this change and should be deleted from `figma-adapter.md`.

---

## 7. Figma Community Plugin Handoff

**Status (as of 2026-04-20):** PluginOS MCP Bridge is submitted to Figma Community and currently under review.

- **Listing URL:** https://www.figma.com/community/plugin/1626608701431483287/pluginos-mcp-bridge-for-llms
- **Until approved:** dev-import remains the install path (Section 6).
- **Once approved:** no code change needed. The Community URL is already hardcoded in `figma-adapter.md`; users clicking it get the one-click install automatically.

The pitch copy is written to degrade gracefully — it links to the Community page whether or not it's live yet. If a user clicks before approval, Figma shows the "under review" state. That's acceptable friction and better than hiding the link entirely.

### When Community approval lands

A trivial PR to `figma-adapter.md` will update the copy to remove the "under review" hedge. No schema changes, no validator changes, no user migration.

---

## 8. Validator Updates

The existing `scripts/validate_plugin.py` needs one addition:

**New check (warning, non-fatal):** if `plugin.json` declares `mcpServers`, each referenced command must be either an absolute path, a `${CLAUDE_PLUGIN_ROOT}/...` path, or a binary resolvable in `$PATH` at install time (`npx`, `node`, `python`, etc.). Relative paths like `./relative/path/` produce a warning (not an error) because they won't resolve from the user's cwd.

The check for vendored skill integrity (is `UPSTREAM.md` current, is `SKILL.md` well-formed) should be lightweight — just presence and frontmatter checks. Deep validation is upstream's job.

---

## 9. Testing Plan

Pre-merge verification:

1. **Fresh install test.** On a test account with no PluginOS configured, install design-superpowers from the repo. Run any `/creative` / `/design` command that touches Figma. Expected: `npx -y pluginos` runs silently, bridge-install pitch shows, user follows one link, command proceeds.
2. **Upgrade-from-0.1.0 test.** With design-superpowers 0.1.0 already installed, upgrade to 0.2.0. Expected: PluginOS auto-registers on next session, no manual config edit needed.
3. **Validator run.** `python3 scripts/validate_plugin.py` passes after the vendored skill is added.
4. **Sync script test.** Run `scripts/sync_pluginos.sh` on a clean checkout. Expected: skill updates, `UPSTREAM.md` reflects current SHA, no validator errors.

---

## 10. Out of Scope

- **Auto-launching Figma Desktop.** No plugin can do this reliably across OSes. User opens Figma themselves; the pitch handles the bridge import from there.
- **Bundling the bridge plugin files.** The bridge plugin is Figma-side code, not MCP server code. It has to live in Figma (either Community or dev-import). design-superpowers does not vendor it.
- **Replacing the 2026-04-13 adapter pitch entirely.** Classic Figma MCP support remains as an opt-in fallback for users who already have it configured. The default is PluginOS.

---

## 11. Resolved Decisions

Three questions were open during brainstorming; each is decided here and reflected in the sections above.

| # | Question | Decision | Section |
|---|---|---|---|
| 1 | Figma Community status? | Under review as of 2026-04-20; dev-import is the install path until approval. Community URL is already wired into the pitch and will work automatically once the listing goes live. | 6, 7 |
| 2 | Pin `pluginos` version or float? | Float (`npx -y pluginos`). PluginOS is in active development; pinning would block bug fixes. Pin reactively if a bad release ships. | 3 |
| 3 | Weekly sync job: PR or issue? | Auto-open PR with fixed branch name so reruns update the same PR. More actionable, less noisy than issues. | 5 |
