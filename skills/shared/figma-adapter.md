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
