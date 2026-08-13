# Figma Adapter — Routing Brain

> Single source of truth for how design-superpowers talks to Figma. Every sub-agent that needs a Figma operation references this file. Sub-agents do NOT call `mcp__pluginos__*` or `mcp__Figma__*` tools directly outside the rules below.

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
   (No .ds-context.md file at all — always true at L0/L1 — counts as "unset".)
2. Route:
   ├── "pluginos"  → confirm mcp__pluginos__* tools are available, then proceed
   ├── "figma-mcp" → user has manually opted into the fallback; proceed via Figma MCP
   └── unset       → run the install pitch (see "Install pitch" below)
```

If `figma.adapter: pluginos` is set but `mcp__pluginos__*` tools are NOT available in this session, treat it as if the field were unset and re-run the install pitch.

### Unset adapter (L0/L1) — do not imply an inspection that can't run

At L0/L1 there is no `.ds-context.md`, so the adapter is **always unset**. A sub-agent that needs Figma data here must **explicitly pick one of two paths and say which** — never silently "inspect the Figma file" as if a bridge were configured:

- **Pitch it:** run the install pitch (or nudge `/figma-setup`) so the user can connect PluginOS, then inspect for real; **or**
- **Proceed without live inspection:** work from DESIGN.md / user-provided screenshots only, and state that findings are not backed by a live Figma read (e.g. "no adapter configured — usage/instance counts are inferred from DESIGN.md, not measured").

Pick the pitch when the task genuinely needs live file data (adoption counts, drift, real style usage); pick proceed-without when DESIGN.md is sufficient. State the choice in the output.

## Iron rule — PluginOS strictly preferred

Once PluginOS is connected:

1. **Always call `mcp__pluginos__get_status` first** to confirm the bridge plugin is connected. If it returns disconnected, follow "Connection troubleshooting" — do NOT silently fall back to `mcp__Figma__*`.
2. **Use `mcp__pluginos__run_operation`** for any registered operation (lint, contrast, exports, audits, inspections — see Tool mapping below).
3. **Use `mcp__pluginos__execute_figma`** for arbitrary plugin scripts when no registered op fits.
4. **Only use `mcp__Figma__*`** for the enumerated exceptions in the next section.
5. **Never interleave** PluginOS and Figma MCP within a single Figma task — pick one path per request.

## Enumerated exceptions (the only times `mcp__Figma__*` is allowed)

`mcp__Figma__*` tools are allowed in exactly these four cases:

1. **Figma Code Connect mapping** — `mcp__Figma__add_code_connect_map`, `mcp__Figma__get_code_connect_map`, `mcp__Figma__create_design_system_rules`. PluginOS does not own this surface.
2. **`get_design_context` for code generation** — when the user explicitly asks for design-to-code generation against a node.
3. **Visual screenshot of a node or frame** — `mcp__Figma__get_screenshot`. PluginOS does not expose a screenshot operation; if a sub-agent needs a visual render (e.g. for visual-quality review), use this Figma MCP call. Prefer `mcp__pluginos__execute_figma` for any non-screenshot inspection that PluginOS can handle.
4. **Last-resort fallback** — PluginOS returns `no_operation_available` AND `execute_figma` cannot reasonably do the job. Report the gap to the user before falling back.

In all other cases, route through PluginOS.

## Install pitch (shown when `figma.adapter` is unset OR PluginOS tools are missing)

Halt the workflow and emit this message verbatim. Then ask the user to install and re-run the original command.

> **Maintenance note:** Steps 1–3 of the pitch below are verbatim-identical to `${CLAUDE_PLUGIN_ROOT}/skills/figma-setup/SKILL.md`. Keep them in sync when editing — only the closing line and the placement of the "Figma integration setup" heading (above vs inside the displayed block) legitimately differ.

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

Once both are done, re-run your last command (or run any Figma command).

---

You can also run `/figma-setup` at any time to see this same pitch and verify the install.

## Sticky write-back

After PluginOS is verified working in this session — i.e. `mcp__pluginos__get_status` returns connected — write the following to `.ds-context.md`:

```yaml
figma:
  adapter: pluginos
  status: ready
```

Subsequent sessions read these fields, confirm `mcp__pluginos__*` is still available, skip the pitch, and proceed.

If the user removes or empties `figma.adapter`, detection re-runs on the next Figma action.

**Never auto-write `figma.adapter: figma-mcp`.** That value is reserved for users who manually edit `.ds-context.md` to opt out of PluginOS.

## Connection troubleshooting

If `mcp__pluginos__get_status` returns disconnected:

1. Tell the user: "PluginOS is installed but the Bridge plugin isn't running in Figma Desktop."
2. Direct them to: https://www.figma.com/community/plugin/1626608701431483287 — install if missing, then run from Plugins menu in Figma.
3. After they confirm the Bridge plugin is open, re-call `mcp__pluginos__get_status`.
4. Do NOT fall back to `mcp__Figma__*` to "make it work anyway" — that's the silent-precedence-break the iron rule forbids.

## Tool mapping

### PluginOS (default — use these for every applicable action)

| Design-superpowers action | PluginOS call |
|---|---|
| Confirm bridge connected | `mcp__pluginos__get_status` (always first) |
| Discover available operations | `mcp__pluginos__list_operations` |
| Inspect component / find instances | `mcp__pluginos__run_operation("find_instances", {scope: "selection"})` |
| Run DS lint | `mcp__pluginos__run_operation("lint_styles", {scope: "page"})`, then `"lint_detached"` and `"lint_naming"` sequentially |
| Check contrast (WCAG) | `mcp__pluginos__run_operation("check_contrast", {scope: "page"})` |
| Audit spacing | `mcp__pluginos__run_operation("audit_spacing", {scope: "page"})` |
| List variables / tokens | `mcp__pluginos__run_operation("list_variables", {})` |
| Export tokens | `mcp__pluginos__run_operation("export_tokens", {format: "json"})` |
| Extract palette | `mcp__pluginos__run_operation("extract_palette", {scope: "page"})` |
| Audit typography | `mcp__pluginos__run_operation("audit_text_styles", {scope: "page"})` |
| Find non-style colors | `mcp__pluginos__run_operation("find_non_style_colors", {scope: "page"})` |
| Analyze overrides | `mcp__pluginos__run_operation("analyze_overrides", {scope: "selection"})` |
| Extract CSS / preview | `mcp__pluginos__run_operation("extract_css", {scope: "selection"})` |
| Custom / one-off logic | `mcp__pluginos__execute_figma("return <figma.* script>")` |

### Figma MCP (only for the four enumerated exceptions)

| Exception | Figma MCP call |
|---|---|
| Code Connect mapping | `mcp__Figma__add_code_connect_map`, `mcp__Figma__get_code_connect_map`, `mcp__Figma__create_design_system_rules` |
| `get_design_context` for code generation (user-requested) | `mcp__Figma__get_design_context` |
| Visual screenshot of a node or frame | `mcp__Figma__get_screenshot` |
| Last-resort fallback (PluginOS gap) | Whichever `mcp__Figma__*` call fits — report the gap to the user first |

## Scope resolution

Before any PluginOS run_operation call, decide scope from the user intent:

- **User pasted a Figma URL?** Parse `file_key` and `node_id` from the URL. Pass explicitly. Skip the scope question.
- **User has a selection + scoped prompt** ("check contrast on this frame"): use `scope: "selection"`.
- **User has a selection + generic prompt** ("audit the design"): ASK — "Just your selection, or the full page?"
- **No selection + scoped prompt to page** ("audit the whole page"): use `scope: "page"`. Expect `requires_confirm` for large pages — relay the node count, ask permission, re-call with `confirm: true`.

## Changing the adapter

User can change their choice at any time by editing `figma.adapter` in `.ds-context.md`:
- Remove the field → install pitch fires on next Figma action
- Set to `figma-mcp` → manual opt-out (allowed but never auto-written; you'll be on the Figma MCP path with no PluginOS routing)
