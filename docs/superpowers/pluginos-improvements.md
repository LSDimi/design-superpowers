# PluginOS Improvement Suggestions for Design Superpowers

> Additions to [PluginOS](https://github.com/LSDimi/PluginOS) that would supercharge design-superpowers agents. These are suggestions based on gaps identified during skill development — not blocking issues, but high-value enhancements.

## High Impact — New Operations

| Operation | Why | Token Savings |
|-----------|-----|---------------|
| `get_selection_context` | Every sub-agent needs "what's selected?" before routing. Returns structured summary: node types, component names, instance status, applied styles/variables. | ~230 tok (1 call vs manual inspection) |
| `validate_ds_compliance` | Meta-operation: `lint_styles` + `lint_detached` + `lint_naming` + `check_contrast` in one call. Unified compliance report with P0-P3 severity classification. | ~230 tok vs ~920 tok (4 separate calls) |
| `get_node_properties` | Full property table for a node — fills, strokes, effects, auto-layout, constraints, component properties. Replaces Prostar plugin dependency for doc generation. | ~230 tok vs ~700 tok (execute_figma fallback) |
| `apply_variables` | Bind variables to node properties programmatically. Essential for token workflows in /ds-make Token Architect. | ~230 tok vs ~700 tok (execute_figma fallback) |

## Medium Impact — New Operations

| Operation | Why |
|-----------|-----|
| `diff_versions` | Compare two component versions, report structural/property changes. Powers /ds-make Version Advisor without manual diffing. |
| `batch_operations` | Execute N operations in one MCP call. Cascade audits (/ds-manage Publisher) go from N round-trips to 1. |
| `export_component_sheet` | Component anatomy as structured spec: property table, variant matrix, token bindings. Powers /ds-manage Documentation Generator. |
| `get_library_analytics` | Adoption metrics: DS instances vs non-DS instances per file/page. Powers /ds-manage Analytics Reporter. |
| `find_overrides` | List all overrides on instances in scope, classified by type (text, property, structural). Powers /design-review DS Compliance Checker. |

## Event-Based Enhancement

| Feature | Why |
|---------|-----|
| `subscribe_selection` | Push selection changes instead of polling. Enables real-time design companion mode where the agent reacts to what the designer selects. |

## Architecture Suggestions

### Operation Registry Manifest

Expose a `pluginos.registry.json` manifest listing all operations with their full schemas (params, returns, category). Agents read once at session start, cache in memory, and make smarter operation selections without calling `list_operations` every time. Saves ~230 tok per session after the first call.

### Composite Operation Pattern

Allow operations to declare dependencies on other operations. For example, `validate_ds_compliance` could be defined as a composite of `lint_styles` + `lint_detached` + `lint_naming` + `check_contrast` without duplicating logic. This pattern enables users to compose project-specific meta-operations from existing building blocks.

### Per-Project Operation Directories

Support a `.pluginos/operations/` directory at the project root. Operations placed here are auto-discovered alongside the built-in set. This lets teams add DS-specific operations (e.g., `check_tone_compliance`, `generate_uspec`) without forking PluginOS.

## Integration Path

The design-superpowers Figma adapter (`skills/shared/figma-adapter.md`) already routes to PluginOS operations where available and falls back to `execute_figma` for gaps. As new operations ship in PluginOS, agents benefit automatically via `list_operations` discovery. No skill rewrites needed.

### Current coverage mapping

| Design-superpowers need | PluginOS operation (existing) | Gap (needs new op) |
|------------------------|------------------------------|-------------------|
| Lint styles/tokens | `lint_styles` | - |
| Detect detached components | `lint_detached` | - |
| Naming audit | `lint_naming` | - |
| WCAG contrast check | `check_contrast` | - |
| Touch target check | `check_touch_targets` | - |
| Component instance search | `find_instances` | - |
| Override analysis | `analyze_overrides` | - |
| Token export | `export_tokens` | - |
| Variable listing | `list_variables` | - |
| Spacing audit | `audit_spacing` | - |
| Typography audit | `audit_text_styles` | - |
| Palette extraction | `extract_palette` | - |
| Selection context | - | `get_selection_context` |
| Unified compliance report | - | `validate_ds_compliance` |
| Full node property table | - | `get_node_properties` |
| Variable binding | - | `apply_variables` |
| Version diffing | - | `diff_versions` |
| Batch execution | - | `batch_operations` |
| Component spec export | - | `export_component_sheet` |
| Library adoption metrics | - | `get_library_analytics` |
