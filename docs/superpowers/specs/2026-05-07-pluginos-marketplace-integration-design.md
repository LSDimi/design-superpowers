# PluginOS Marketplace Integration — Design Spec

> **Date:** 2026-05-07
> **Status:** Draft (awaiting user review)
> **Supersedes:** `2026-04-20-pluginos-bundled-integration-design.md` (vendoring approach is no longer the right path now that PluginOS is a first-class Claude Code plugin)
> **Builds on:** `2026-04-13-pluginos-integration-and-ds-decoupling.md` (foundation files: `figma-adapter.md`, `ds-context-loader.md`, `.ds-context.md` schema)

---

## 1. Context

PluginOS shipped its v0.4.3 release (2026-04-30) with a working `marketplace.json` at the repo root. The advertised install path now functions:

```
/plugin marketplace add github:LSDimi/pluginos
/plugin install pluginos
```

This installs both the `pluginos` MCP server and the `pluginos-figma` skill in one step. The Bridge plugin has been approved on Figma Community (https://www.figma.com/community/plugin/1626608701431483287) — public release pending.

The 2026-04-20 spec proposed vendoring the `pluginos-figma` skill and declaring `mcpServers` in our `plugin.json`. That work was never started, and it's now the wrong shape: PluginOS solves the install-friction problem upstream as its own plugin. Vendoring would create an upstream-sync burden for no user benefit.

This spec replaces the 2026-04-20 approach with a **separate-plugin** integration model: design-superpowers and PluginOS are peer plugins. Users install both. We own zero PluginOS surface area.

---

## 2. Goals

1. **Seamless install for non-technical users.** A designer who hits a Figma command without PluginOS installed gets a one-paste install pitch in-flow. A proactive user can run `/figma-setup` to install ahead of time.
2. **PluginOS strictly preferred over Figma MCP.** Every sub-agent that touches Figma routes through `figma-adapter.md`. The adapter's iron rule guarantees `pluginos.*` is tried first and `mcp__Figma__*` is used only for explicitly enumerated exceptions.
3. **Sticky preference.** Once PluginOS is verified working, `.ds-context.md` records `figma.adapter: pluginos`. Future sessions skip detection.
4. **Zero ongoing maintenance.** No vendored skill, no sync script, no `mcpServers` block, no upstream version tracking.

---

## 3. Non-Goals

- **Auto-executing slash commands on the user's behalf.** Claude Code does not expose a "run command" button to plugins. Install requires the user to paste two slash commands once. The skill content is shaped to make that moment as clear as possible.
- **Auto-installing the Bridge plugin in Figma Desktop.** The Figma Community URL is one click for the user; we cannot reduce that further.
- **Replacing the 2026-04-13 spec.** The DS-decoupling work is independent and already complete. This spec only supersedes the 2026-04-20 bundling approach.
- **Removing Figma MCP support entirely.** Code Connect mapping and `get_design_context` code generation are legitimate Figma MCP strengths. They remain available as documented exceptions.

---

## 4. Architecture

Three components, each with one job.

### 4.1 `skills/shared/figma-adapter.md` — the routing brain

Single source of truth for "how does design-superpowers talk to Figma." Every sub-agent that needs a Figma operation references this file. No sub-agent calls `mcp__pluginos__*` or `mcp__Figma__*` tools directly outside the rules in this file.

Sections:
- **Detection:** Read `.ds-context.md` `figma.adapter`. If unset, run the auto-detect flow (Section 4.2).
- **Iron rule:** Always call `pluginos.get_status` first. Use `pluginos.run_operation` for any registered operation. Use `pluginos.execute_figma` for arbitrary plugin scripts. Only fall back to `mcp__Figma__*` for the enumerated exceptions below.
- **Enumerated exceptions:** (1) Figma Code Connect mapping, (2) `get_design_context` for code generation when the user explicitly asks for it, (3) visual screenshot of a node or frame, (4) any operation where PluginOS returns `no_operation_available` AND `execute_figma` cannot reasonably do the job.
- **Tool mapping table:** lists every design-superpowers Figma action with its `pluginos.*` call. The `mcp__Figma__*` column lists only the four exceptions above.
- **Connection troubleshooting:** what to do when `pluginos.get_status` returns disconnected (point user to Bridge plugin Community URL).

### 4.2 First-action install pitch (combined 1A + 1B)

Two entry points share one setup module.

**Entry point A — implicit (auto-detect on first Figma action):**
A sub-agent is about to call a Figma tool. Before the call, the adapter checks: is `mcp__pluginos__*` available in this session?
- If yes → proceed with the call.
- If no → halt the workflow and emit the install pitch (below). Ask the user to install, then re-run the original command.

**Entry point B — explicit (`/figma-setup` slash command):**
New skill at `skills/figma-setup/SKILL.md`. Same pitch, callable on demand. Useful for onboarding, troubleshooting, or users who want to set up before their first Figma command.

**The pitch (shown by both entry points):**

```
Figma work in design-superpowers uses PluginOS — a separate Claude Code plugin
that talks to your Figma file via a small bridge plugin. You'll install it once.

Step 1 — Install the PluginOS plugin (paste both commands in this chat):

  /plugin marketplace add github:LSDimi/pluginos
  /plugin install pluginos

Step 2 — Install the free Bridge plugin in Figma Desktop:

  https://www.figma.com/community/plugin/1626608701431483287

  (Community listing is approved; if the page shows "under review" it just
   means the public listing hasn't gone live yet — the install button still
   works.)

Step 3 — Open the Bridge plugin in Figma once. It auto-reconnects after that.

Once both are done, re-run your last command (or run any /figma command).
```

After install, the adapter calls `pluginos.get_status`. If connected → write `figma.adapter: pluginos` and `figma.status: ready` to `.ds-context.md`, proceed. If disconnected → guide user back to step 3.

### 4.3 Sticky preference write-back

`.ds-context.md` already has the `figma.adapter` and `figma.status` fields per the 2026-04-13 spec. After a successful first PluginOS call, the adapter writes:

```yaml
figma:
  adapter: pluginos
  status: ready
```

Subsequent sessions read these fields, confirm `mcp__pluginos__*` is available, skip detection, proceed. If the user removes/empties `figma.adapter` (e.g., switches machines, fresh project), detection re-runs.

---

## 5. File Changes

| File | Change |
|---|---|
| `skills/shared/figma-adapter.md` | Rewrite. Drop the "PluginOS or Figma MCP, pick one" pitch. Replace with the iron-rule routing model + enumerated exceptions + the install pitch flow + Bridge troubleshooting. |
| `skills/figma-setup/SKILL.md` | New. Slash command that prints the install pitch and verifies setup. |
| `skills/shared/ds-context-schema.md` | Minor edit. `figma.adapter` field doc: list `pluginos` as the auto-detected default and `figma-mcp` as a manual-override-only value. Remove any wording that presents the two as equal peers the user picks between. |
| `docs/superpowers/specs/2026-04-20-pluginos-bundled-integration-design.md` | Add `> **Status:** Superseded by 2026-05-07-pluginos-marketplace-integration-design.md` banner at the top. Don't delete — historical record. |
| `docs/superpowers/pluginos-improvements.md` | No change. Improvement proposals remain valid as upstream wishlist. |
| `README.md` | Add a "Figma integration" section pointing at the install pitch. Mention `/figma-setup`. |
| `CLAUDE.md` | One-line update under "Tech Stack" — Figma adapter section now says "PluginOS (installed as a separate Claude Code plugin); see `skills/shared/figma-adapter.md`." |
| `.claude-plugin/plugin.json` | No change. We do NOT declare `mcpServers`. Version stays 0.1.0 — no material plugin behavior change. |

---

## 6. Routing Enforcement (the "PluginOS always above Figma MCP" guarantee)

Three layers enforce this:

1. **Adapter file is the only file that lists `mcp__Figma__*` tools.** Every other skill references `skills/shared/figma-adapter.md` rather than naming Figma tools directly. If a sub-agent needs a Figma operation, it consults the adapter's tool-mapping table.
2. **Iron rule is stated unconditionally.** No "if available," no "preferred when possible." The rule is: try PluginOS, fall back only for the four enumerated exceptions.
3. **Detection always defaults to `pluginos`.** When `figma.adapter` is unset and PluginOS install succeeds, we write `pluginos`. We never write `figma-mcp` automatically. The only way `figma.adapter: figma-mcp` ends up in `.ds-context.md` is if the user manually edits it.

---

## 7. Validation

Pre-merge testing:

1. **Fresh-machine test.** No PluginOS, no `.ds-context.md`. Run `/design audit this page`. Expected: pitch appears, user pastes the two commands, Bridge plugin link clicked, `pluginos.get_status` returns connected, `.ds-context.md` updated, command proceeds.
2. **Repeat-session test.** With PluginOS already installed and `.ds-context.md` populated, run any Figma command. Expected: no pitch, command proceeds immediately.
3. **Bridge-disconnected test.** PluginOS installed but Bridge plugin not running. Expected: clear error pointing user to Figma Desktop, no fallback to Figma MCP.
4. **Code Connect exception.** User says "generate Code Connect mapping for this component." Expected: adapter routes to `mcp__Figma__add_code_connect_map` per the enumerated exception.
5. **`/figma-setup` test.** Run before any Figma command. Expected: same pitch as auto-detect, same verification, same write to `.ds-context.md`.

---

## 8. Migration

This is a clean addition. No existing user state to migrate (the 2026-04-20 spec was never implemented). The 2026-04-13 foundation files (`figma-adapter.md`, `.ds-context.md` schema) already exist; we modify rather than rewrite from scratch.

For users who were testing with manual Figma MCP setup: the iron rule + enumerated exceptions explicitly preserve their Code Connect workflow. Anything else they were doing through `mcp__Figma__*` should be revisited against the PluginOS operation list — no migration script, just a one-paragraph note in the README pointing at the operation reference.

---

## 9. Out of Scope

- **Bundling PluginOS via `mcpServers`.** Decided against in Section 1. PluginOS is a peer plugin.
- **A meta-marketplace listing both plugins.** Possible future move; not needed now.
- **Hooks-based enforcement.** Considered (intercept `mcp__Figma__*` calls with a `PreToolUse` hook), rejected as overkill — documentation-level enforcement is sufficient and less surprising.
- **Auto-installing PluginOS via shell command.** Plugins can't shell out to install other plugins; the slash-command paste is the limit.

---

## 10. Open Questions

None. All previously open questions (vendoring vs separate-install, Figma Community status, version pinning) are resolved by the upstream changes that landed in PluginOS 0.4.x.
