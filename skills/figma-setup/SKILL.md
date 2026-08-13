---
name: figma-setup
description: Install or verify PluginOS for Figma work in design-superpowers. Use when the user runs `/figma-setup`, asks how to set up Figma integration, or hits a Figma command without PluginOS installed.
---

# /figma-setup

Guided setup for the PluginOS Figma integration. Same pitch the figma-adapter shows on first Figma action — this command makes it accessible upfront.

## What you do

### Step 0 — Check current state

Check whether `mcp__pluginos__*` tools are already available in this session.

- **If yes:** call `mcp__pluginos__get_status`.
  - Connected → tell the user: "PluginOS is installed and the Bridge plugin is running. You're set." Stop.
  - Disconnected → skip to "Bridge plugin troubleshooting" below. Do NOT print the install pitch (PluginOS is already installed).
- **If no:** print the install pitch (Step 1) and continue.

### Step 1 — Print the install pitch

> **Maintenance note:** Steps 1–3 below are verbatim-identical to the install pitch in `${CLAUDE_PLUGIN_ROOT}/skills/shared/figma-adapter.md`. Keep them in sync when editing — only the closing line and the placement of the "Figma integration setup" heading (this skill places it inside the displayed block; the adapter places it above the block) legitimately differ.

Show the user this verbatim:

---

**Figma integration setup**

Figma work in design-superpowers uses **PluginOS** — a separate Claude Code plugin that talks to your Figma file via a small bridge plugin. You'll install it once.

**Step 1 — Install the PluginOS plugin** (paste both commands in this chat, in order):

```
/plugin marketplace add github:LSDimi/pluginos
/plugin install pluginos
```

**Step 2 — Install the free Bridge plugin in Figma Desktop:**

https://www.figma.com/community/plugin/1626608701431483287

(The Community listing is approved. If the page shows "under review" the install button still works.)

**Step 3 — Open the Bridge plugin in Figma once.** It auto-reconnects after that.

When all three are done, send a message saying "ready" — I'll wait, then verify the install on your next message.

---

### Step 2 — Verify after the user says "ready"

When the user confirms:

1. Call `mcp__pluginos__get_status`.
2. **Connected:** write `figma.adapter: pluginos` and `figma.status: ready` to `.ds-context.md` (creating the file if missing). Tell the user: "PluginOS is connected. You can now run any Figma command in design-superpowers."
3. **Tools missing entirely:** the user did Step 1 in a different chat or hasn't restarted Claude Code. Ask them to restart the session and re-run `/figma-setup`.
4. **Tools present but disconnected:** Bridge plugin isn't running. Continue to "Bridge plugin troubleshooting".

### Bridge plugin troubleshooting

The Bridge plugin is what actually talks to Figma — without it, PluginOS calls fail.

1. Direct the user to https://www.figma.com/community/plugin/1626608701431483287 — install if missing.
2. Tell them: open Figma Desktop → Plugins menu → run "PluginOS MCP Bridge".
3. After they confirm it's open, re-call `mcp__pluginos__get_status`.
4. Once connected, write the sticky preference per Step 2.

## Boundaries

- **Do not** install plugins on the user's behalf. Claude Code does not expose a way to execute slash commands programmatically; the user pastes them once.
- **Do not** edit `.ds-context.md` until `mcp__pluginos__get_status` returns connected. Premature writes lock the user into an unverified state.
- **Do not** present Figma MCP as an alternative during setup. This command's job is to install PluginOS. Figma MCP is a manual-override path documented in `${CLAUDE_PLUGIN_ROOT}/skills/shared/figma-adapter.md`, not a peer choice.

## Cross-references

- Routing rules and tool mapping: `${CLAUDE_PLUGIN_ROOT}/skills/shared/figma-adapter.md`
- Field reference for `.ds-context.md`: `${CLAUDE_PLUGIN_ROOT}/skills/shared/ds-context-schema.md`
