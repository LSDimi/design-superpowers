# Plugin Integration Plan — Tone DS MCP Server

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan.

**Goal:** Package both DS skills, shared foundation, and Figma plugin integrations into a private Talon.One MCP server for universal team distribution.

**Architecture:** MCP server wrapping two skills + CLI tools (Library Analytics) + Figma MCP proxy for Tone-aware operations. Tone Lint remains a Figma UI plugin (no headless API) but its rules are encoded in the skills for agent-level awareness.

---

## Plugin Inventory

### 1. Tone Lint (Figma UI Plugin)
- **Plugin ID:** `1618039184324640227`
- **Type:** Figma plugin (sandbox + iframe UI) — NO CLI, NO API
- **Source:** `/tone-lint/` (TypeScript, webpack build)
- **Capabilities:** 13 linting rules, auto-fix via variable binding, detached component detection, Auditor inventory mode

**Agent integration strategy:** Tone Lint cannot be called programmatically. However:
- Its 13 rule definitions are encoded in the DS Producer skill so agents know exactly what will be checked
- Agents can replicate core detection logic via Figma MCP (read node properties, check variable bindings against known Tone collection keys)
- The agent instructs the user to run Tone Lint and report results, or parses screenshots of lint output

### 2. Library Analytics (Node.js CLI)
- **Type:** Headless Node.js pipeline — fully automatable
- **Source:** `/figma-library-analytics-main/` (JavaScript)
- **Capabilities:** Measures component instance counts across all team files from 4 tracked libraries
- **Requirements:** `FIGMA_TOKEN` env var with scopes: `file_content:read`, `projects:read`, `library_content:read`

**Agent integration strategy:** Direct subprocess execution via MCP tool:
```bash
FIGMA_TOKEN=$TOKEN npm run build                    # Full pipeline
FIGMA_TOKEN=$TOKEN npm run build -- --skip-file-list  # Cached re-process
```
Parse `output/latest_library_instances.csv` for per-component, per-file, per-team metrics.

### 3. Prostar (Figma Plugin — details TBD)
- Generates property tables in Demo area
- Integration: user-triggered, results inspected via Figma MCP

---

## MCP Server Architecture

### Required External MCPs

| MCP | Purpose | Status |
|-----|---------|--------|
| Figma MCP | Component inspection, screenshots, design context, variable definitions | Connected |
| Shortcut MCP | Ticket lifecycle, changelogs, comments | Needs setup |
| uSpec MCP | Documentation generation in Figma | Needs setup |

### Custom MCP Tools to Build

#### Producer Tools

| Tool | Description | Implementation |
|------|-------------|----------------|
| `tone_analytics_run` | Run Library Analytics pipeline, return adoption metrics | Subprocess: `npm run build`, parse CSV output |
| `tone_analytics_report` | Get latest adoption report (per-team or per-squad) | Read cached `output/team_*.csv`, compute Tone vs Legacy ratios |
| `tone_analytics_component` | Get usage data for a specific component | Filter `latest_library_instances.csv` by component name |
| `tone_audit` | Run governance checklist on a Figma node via MCP | Figma MCP: get_design_context + rule evaluation |
| `tone_lint_rules` | Return the 13 Tone Lint rules for reference | Static: return rule definitions from skill |
| `tone_document` | Generate uSpec documentation | Delegate to uSpec MCP |
| `tone_publish_cascade` | Track cascading publish pipeline status | Shortcut MCP: linked ticket tracking |
| `shortcut_update` | Update ticket status and write changelog | Shortcut MCP: update story |

#### Consumer Tools

| Tool | Description | Implementation |
|------|-------------|----------------|
| `tone_component_search` | Find best-fit Tone component for a described need | Figma MCP: search_design_system on Components/Patterns files |
| `tone_evaluate_screen` | Run UX evaluation against design principles | Figma MCP: get_design_context + principle scoring |
| `tone_pattern_lookup` | Find relevant patterns for a product area | Figma MCP: get_metadata on Patterns file, filter by area |
| `tone_gap_request` | Submit component gap request (after user approval) | Shortcut MCP: create story with template |
| `tone_detached_check` | Check for detached components via Figma MCP | Figma MCP: inspect node tree for detachedInfo patterns |

#### Shared Tools

| Tool | Description | Implementation |
|------|-------------|----------------|
| `tone_inspect` | Tone-aware Figma inspection (adds library context) | Figma MCP wrapper: get_design_context + library key resolution |
| `talon_context` | Return product context for a Talon.One entity | Static: lookup from tone-ds-context.md entity table |

### Figma File Key Registry

Hardcoded in the MCP server config (matches both skills and Library Analytics):

```yaml
figma_files:
  foundations: Pn9sIWsLKN7gQKj1RkV75j
  components: rVLnzp5jPQee88ThJR81Ha
  components_demo: Lwxy3Us24a0UoTqQEdpbev
  patterns_l1: H4A6DU7tCNJ7Qt4UwCuQy2
  patterns_l2_gamification: qGiniOnkCUIww81UKNUkSs
  checklist: QCQcWpr372QodwEhZF1qbM
  legacy_library: dqlNDxAO5JY0LliAPadihh

figma_plugins:
  tone_lint:
    id: "1618039184324640227"
    type: figma_ui_plugin
    headless: false
  library_analytics:
    type: node_cli
    headless: true
    path: ./tools/figma-library-analytics/
  prostar:
    type: figma_ui_plugin
    headless: false
```

---

## Repository Structure

```
tone-ds-plugin/
├── skills/
│   ├── shared/
│   │   ├── tone-ds-context.md
│   │   └── design-principles.md
│   ├── ds-producer/
│   │   └── SKILL.md
│   └── ds-consumer/
│       └── SKILL.md
├── tools/
│   ├── figma-library-analytics/    # Git submodule or vendored copy
│   │   ├── build.js
│   │   ├── count-component-instances.js
│   │   ├── collate-instances.js
│   │   ├── get-file-list.js
│   │   ├── blacklists.js
│   │   └── input/teams.json
│   └── tone-lint/                  # Reference only (Figma plugin, not callable)
│       └── README.md               # Documents rules for agent awareness
├── src/
│   └── mcp-server/                 # MCP server implementation
│       ├── index.ts                # Server entry point
│       ├── tools/                  # Tool implementations
│       │   ├── analytics.ts        # tone_analytics_* tools
│       │   ├── audit.ts            # tone_audit, tone_lint_rules
│       │   ├── consumer.ts         # tone_component_search, tone_evaluate_screen, etc.
│       │   └── shortcut.ts         # shortcut_update, tone_gap_request
│       └── config.ts               # Figma file keys, library mappings
├── .claude-plugin/                 # Claude Code plugin manifest
│   └── manifest.json
├── CLAUDE.md
├── package.json
└── README.md
```

---

## Implementation Tasks

### Task 1: Scaffold MCP Server
- [ ] Initialize Node.js/TypeScript project
- [ ] Set up MCP server boilerplate (use `anthropic-skills:mcp-builder`)
- [ ] Define tool schemas for all 15 tools
- [ ] Configure Figma file key registry

### Task 2: Integrate Library Analytics
- [ ] Vendor or submodule `figma-library-analytics-main`
- [ ] Create `tone_analytics_run` tool (subprocess execution)
- [ ] Create `tone_analytics_report` tool (CSV parsing + aggregation)
- [ ] Create `tone_analytics_component` tool (filtered lookup)
- [ ] Test with real Figma token

### Task 3: Build Figma MCP Wrapper Tools
- [ ] Create `tone_inspect` (Figma MCP + library context enrichment)
- [ ] Create `tone_component_search` (search_design_system on Tone files)
- [ ] Create `tone_pattern_lookup` (metadata query on Patterns files)
- [ ] Create `tone_evaluate_screen` (get_design_context + principle evaluation)
- [ ] Create `tone_detached_check` (node tree inspection for detachedInfo)
- [ ] Create `tone_audit` (governance checklist evaluation via MCP)

### Task 4: Build Shortcut Integration Tools
- [ ] Create `shortcut_update` (ticket status + changelog)
- [ ] Create `tone_gap_request` (story creation with template)
- [ ] Create `tone_publish_cascade` (linked ticket tracking)

### Task 5: Package as Claude Code Plugin
- [ ] Create `.claude-plugin/manifest.json`
- [ ] Bundle skills into plugin
- [ ] Set up private Talon.One GitHub repository
- [ ] Write installation instructions
- [ ] Test end-to-end: install plugin → run Producer workflow → run Consumer workflow

---

## Tone Lint Rule Reference (for Agent Awareness)

Since Tone Lint cannot be called programmatically, agents need to know its rules to provide accurate guidance. These 13 rules are what the plugin checks:

| # | Rule | Applies To | Checks | Error Conditions |
|---|------|-----------|--------|-----------------|
| 1 | `fill` | Frames, shapes, text, instances | Fill variable binding | Unbound, uses style instead of variable, non-Tone collection |
| 2 | `stroke` | Frames, shapes, lines | Stroke color variable | Same as fill |
| 3 | `strokeWidth` | Nodes with strokes | Stroke weight variable | Unbound or non-Tone |
| 4 | `radius` | Frames, rectangles, instances | Corner radius variable (per-corner) | Unbound or non-Tone |
| 5 | `spacing` | Auto-layout nodes | Padding (4 sides) + itemSpacing variables | Unbound or non-Tone |
| 6 | `textStyle` | Text nodes | Text style origin | Missing, unresolvable, or non-Tone |
| 7 | `textComponent` | Text nodes | Wrapped in Tone typography component | Missing or detached typography component |
| 8 | `effectStyle` | Nodes with effects | Effect style origin | Missing or non-Tone |
| 9 | `gridStyle` | Nodes with grids | Grid style origin | Missing or non-Tone |
| 10 | `width` | Fixed-width nodes | Width variable binding | Unbound or non-Tone (skips FILL/HUG) |
| 11 | `height` | Fixed-height nodes | Height variable binding | Same as width |
| 12 | `instanceOverride` | Instances | Overridden properties | Any non-expected override (fills, strokes, spacing, fonts, etc.) |
| 13 | `naming` | All non-text nodes | Layer name hygiene | Default names ("Frame 12"), version suffixes on instances |

**Detection is key-based, not name-based.** Tone Lint syncs from the Tone Foundations file and caches all variable collection keys, text style keys, effect style keys, grid style keys, and component keys. A binding is "from Tone" only if its key matches the cache.

**Suggestion system:** For variable rules, Tone Lint suggests exact-match Tone variables filtered by scope (e.g., Surface/ prefix for frame fills, Text/ for text fills, Stroke/ for strokes, Icon/ for vectors).
