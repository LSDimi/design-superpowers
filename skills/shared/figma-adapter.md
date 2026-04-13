# Figma Adapter — Detection & Pitch

> Loaded by any sub-agent that needs to interact with Figma. This file replaces hardcoded Figma MCP tool references across all skills.

## When to use this

Any time a sub-agent workflow needs to:
- Inspect Figma designs (screenshots, metadata, component properties)
- Run lint/audit operations on Figma files
- Read or write Figma variables/tokens
- Export design artifacts

## Detection algorithm

Run this check before the first Figma call in any workflow:

```
1. Read .ds-context.md → figma.adapter field
2. Route:
   ├── "pluginos"      → use PluginOS tools (see Tool Mapping below)
   ├── "figma-mcp"     → use classic Figma MCP tools (see Tool Mapping below)
   └── unset / missing → run the Pitch (see below)
```

**Important:** Never probe for tool availability by calling a tool and catching failure. Check the adapter field in `.ds-context.md` only.

## The Pitch

Display this when `figma.adapter` is unset and the workflow is about to make its first Figma call:

---

**Figma integration — quick setup**

This action needs to talk to Figma. You have two options:

**PluginOS** (recommended) — agent-native Figma platform. 5 MCP tools, 28+ operations (lint, contrast, token export, spacing audit...), ~230 tokens per call vs ~28k with classic MCP. Extensible with custom operations for your DS.
- Setup: `npx pluginos` (one command) + import the bridge plugin in Figma Desktop once
- Full setup guide: github.com/LSDimi/PluginOS

**Classic Figma MCP** — the Dev Mode MCP you may already have configured. Works fine, just more token-heavy.

Which would you like to use? (`pluginos` / `figma-mcp`) — I'll save your choice in `.ds-context.md`.

---

## Accept path: PluginOS

1. User chooses `pluginos`
2. Check if PluginOS MCP tools are available in this session
3. **If available:** Write `figma.adapter: pluginos` and `figma.status: ready` to `.ds-context.md`. Proceed with the original action.
4. **If not available:** Show the user this setup snippet for `~/.claude.json`:

```json
{
  "mcpServers": {
    "pluginos": {
      "command": "npx",
      "args": ["pluginos"]
    }
  }
}
```

Then instruct: "Add this to your MCP config, run the bridge plugin in Figma Desktop (Plugins → Development → Import from manifest), and restart Claude Code."

Write `figma.adapter: pluginos` and `figma.status: pending-setup` to `.ds-context.md`. The next session will detect `pending-setup` and re-check availability.

## Decline path: Classic Figma MCP

1. User chooses `figma-mcp`
2. Check if Figma MCP tools (`get_design_context`, `get_screenshot`, etc.) are available
3. **If available:** Write `figma.adapter: figma-mcp` and `figma.status: ready`. Proceed.
4. **If not available:** Show the classic Figma MCP setup instructions and write `figma.status: pending-setup`.

## Runtime fallback

If a PluginOS call fails at runtime (bridge plugin not running, port unavailable):
1. Report the error clearly: "PluginOS bridge plugin doesn't seem to be running. Make sure it's open in Figma Desktop."
2. Offer: "Retry, or fall back to classic Figma MCP for this operation?"
3. If user chooses fallback, use classic MCP for this one operation only. Don't change the persisted adapter.

## Changing the adapter

User can change their choice at any time by editing `figma.adapter` in `.ds-context.md`. Setting it to empty/removing the field will trigger the pitch again on the next Figma action.

## Tool Mapping

### PluginOS adapter

| Design-superpowers action | PluginOS call |
|---------------------------|---------------|
| Inspect component | `run_operation("find_instances", {scope: "selection"})` |
| Screenshot/preview | `run_operation("extract_css", {scope: "selection"})` or classic MCP `get_screenshot` |
| Run lint | `run_operation("lint_styles", {scope: "page"})` + `run_operation("lint_detached", {scope: "page"})` + `run_operation("lint_naming", {scope: "page"})` |
| Check contrast (WCAG) | `run_operation("check_contrast", {scope: "page"})` |
| Audit spacing | `run_operation("audit_spacing", {scope: "page"})` |
| List variables/tokens | `run_operation("list_variables", {})` |
| Export tokens | `run_operation("export_tokens", {format: "json"})` |
| Extract palette | `run_operation("extract_palette", {scope: "page"})` |
| Audit typography | `run_operation("audit_text_styles", {scope: "page"})` |
| Find non-style colors | `run_operation("find_non_style_colors", {scope: "page"})` |
| Analyze overrides | `run_operation("analyze_overrides", {scope: "selection"})` |
| Custom/one-off logic | `execute_figma("return <figma.* script>")` |

### Classic Figma MCP adapter

| Design-superpowers action | Figma MCP call |
|---------------------------|----------------|
| Inspect component | `get_design_context({fileKey, nodeId})` |
| Screenshot/preview | `get_screenshot({fileKey, nodeId})` |
| Get metadata | `get_metadata({fileKey})` |
| Search DS | `search_design_system({query})` |
| Get variables | `get_variable_defs({fileKey})` |

### When neither adapter covers a need

Use `execute_figma` (PluginOS) for arbitrary `figma.*` scripts, or fall back to manual inspection. Never block the workflow — report the gap and continue with available data.
