# PluginOS Integration & DS Decoupling Spec

> **Date:** 2026-04-13
> **Status:** Implemented. DS decoupling shipped on main. The "PluginOS as primary Figma adapter" portion was superseded and reshaped — see `2026-05-07-pluginos-marketplace-integration-design.md`, which treats PluginOS as a peer marketplace plugin instead of a vendored bundle. The graceful-fallback contract here is replaced by the iron-rule routing brain in `skills/shared/figma-adapter.md`.
> **Depends on:** `2026-04-09-universal-design-plugin-design.md` (original 6-command architecture)
> **Branch strategy:** `main` = generic, DS-agnostic; project-specific L3 configurations live in each consuming project's `.ds-context.md`

---

## 1. Goals

1. **PluginOS as primary Figma adapter** — pitch on first Figma action, persist choice, gracefully fall back to classic Figma MCP
2. **DS decoupling** — zero references to any specific design system on `main`; all DS-specific behavior reads from `.ds-context.md`
3. **L3 redefinition** — enterprise DS tier triggered by `ds.maturity: enterprise` in `.ds-context.md`, not brand detection
4. **Project rename** — `design-skills` → `design-superpowers`

---

## 2. PluginOS Pitch & Detection Flow

### Detection algorithm (runs when a sub-agent needs Figma)

```
1. Command needs Figma this turn?        (router decides)
2. If yes → read .ds-context.md → figma.adapter field
     ├── "pluginos"        → use PluginOS tools
     ├── "figma-mcp"       → use classic Figma MCP tools
     └── unset / missing   → run the pitch
```

### Pitch (shown once per project, inline in Claude Code)

Displayed when `figma.adapter` is unset and a sub-agent is about to make its first Figma call:

> **Figma integration — quick setup**
>
> This action needs to talk to Figma. You have two options:
>
> **PluginOS** (recommended) — agent-native Figma platform. 5 MCP tools, 28+ operations, ~230 tokens per call vs ~28k. Extensible with custom operations for your DS.
> - Setup: `npx pluginos` + import bridge plugin in Figma Desktop
>
> **Classic Figma MCP** — the Dev Mode MCP you may already have configured. Works fine, just more token-heavy.
>
> Which would you like to use? (`pluginos` / `figma-mcp`)

### Accept path (pluginos)

1. Check if `mcp__pluginos__*` tools are registered in the MCP session
2. **If not registered:** print `~/.claude.json` snippet, instruct user to run `npx pluginos` + import bridge plugin + restart Claude Code. Write `figma.adapter: pluginos`, `figma.status: pending-setup` to `.ds-context.md`
3. **If registered:** write `figma.adapter: pluginos`, `figma.status: ready`, proceed with original action

### Decline path (figma-mcp)

1. Check if `mcp__Figma__*` tools are registered
2. If yes → write `figma.adapter: figma-mcp`, proceed
3. If no → show classic MCP setup snippet, mark `pending-setup`

### Runtime fallback

If a PluginOS call fails at runtime (bridge plugin not running, port taken), sub-agent reports clearly and offers to retry or temporarily fall back to classic MCP for this operation.

### Change adapter

User edits `figma.adapter` in `.ds-context.md` directly, or a future `/design figma-adapter reset` command clears it.

### Where the logic lives

- **New file:** `skills/shared/figma-adapter.md` — pitch copy, detection algorithm, adapter-to-tool mapping, `.ds-context.md` schema for `figma` section
- Sub-agents that touch Figma reference this file in their Knowledge block instead of hardcoding tool names

---

## 3. `.ds-context.md` Schema

Project-root file with YAML frontmatter for structured fields, optional prose body for notes.

```yaml
---
# ─── Identity ─────────────────────────────────────
ds:
  name: "Acme DS"
  slug: "acme"
  version: "2.4.1"
  maturity: enterprise       # greenfield | defined | system | enterprise (L0–L3)

# ─── Figma integration ───────────────────────────
figma:
  adapter: pluginos          # pluginos | figma-mcp | unset
  status: ready              # ready | pending-setup | unset
  libraries:
    - { name: "Foundations",  key: "abc123", role: "tokens" }
    - { name: "Components",   key: "def456", role: "components" }
    - { name: "Patterns",     key: "ghi789", role: "patterns" }

# ─── Token system ────────────────────────────────
tokens:
  collections: ["primitive", "semantic", "component"]
  format: "w3c-dtcf"         # w3c-dtcf | style-dictionary | figma-variables | custom
  export_path: "tokens/"

# ─── Governance (drives L3 behavior) ─────────────
governance:
  tier: enterprise           # lightweight | standard | enterprise
  cascade:
    - foundations
    - components
    - patterns
    - squad-patterns
    - final
  lint:
    tool: "ds-lint"
    command: "npx @acme/ds-lint"
  docs:
    tool: "uspec"            # uspec | storybook | zeroheight | custom | none
    repo: "github.com/acme/uspec"
  contribution_process: "docs/contributing.md"
  versioning: semver         # semver | calver | custom

# ─── Code side ───────────────────────────────────
code:
  framework: "react"
  component_libs: ["@acme/ui"]
  token_import: "@acme/tokens"

# ─── Product context (for /design) ───────────────
product:
  name: "Acme Platform"
  docs_url: "docs.acme.com"
  personas: ["admin", "marketer", "developer"]
---

## DS notes
Free-form prose.
```

### Maturity detection (rewritten)

```
1. No .ds-context.md and no DESIGN.md             → L0 Greenfield
2. DESIGN.md exists, no .ds-context.md             → L1 Design language defined
3. .ds-context.md exists, maturity != enterprise   → L2 Has DS
4. .ds-context.md exists, maturity == enterprise
   OR governance.tier == enterprise                → L3 Enterprise DS
```

### Bootstrap path

Users creating a DS from scratch via `/ds-make`:
1. Sub-agents scaffold initial `.ds-context.md` as their first action
2. Prompt user for fields that can't be inferred
3. At end of first session, prompt: "Declare governance tier? (lightweight/standard/enterprise)"
4. From that point forward, project is L2 or L3 and `ds-producer`/`ds-consumer` become available

### Supporting files

| File | Purpose |
|------|---------|
| `skills/shared/ds-context-schema.md` | Documents every field, valid values, defaults, examples |
| `skills/shared/ds-context-loader.md` | Shared "read + validate context" step for ds-producer/ds-consumer |
| `skills/shared/examples/minimal-ds-context.example.md` | Minimal config for users to copy |

---

## 4. ds-producer / ds-consumer Generalization

### Activation rule

```
/ds-make  + ds.maturity == enterprise → delegate to ds-producer
/design   + ds.maturity == enterprise → delegate to ds-consumer
```

### ds-producer: context-driven rewrites

Every DS-specific assumption → `.ds-context.md` read:

| Hardcoded today | Reads from context |
|---|---|
| Cascade: Foundations → Components → Patterns → Squad → Final | `governance.cascade` |
| Lint: "run the DS lint plugin" | `governance.lint.tool` + `governance.lint.command` |
| Docs: "generate uSpec" | `governance.docs.tool` |
| Figma libraries: hardcoded file keys | `figma.libraries[]` with roles |
| Token collections: 3-tier | `tokens.collections` |
| Versioning: semver assumed | `governance.versioning` |

All 6 workflows open with a context-load step (from `ds-context-loader.md`): read `.ds-context.md`, parse, validate required fields, note missing optionals with defaults.

### ds-consumer: context-driven rewrites

| Hardcoded today | Reads from context |
|---|---|
| Hardcoded product name in feature briefs | "product features" (generic) via `product.name` |
| Hardcoded component library | DS components via `figma.libraries[role=components]` |
| Hardcoded product docs URL | `product.docs_url` |

All 4 workflows open with the same context-load step.

### File header update

Current: "L3 specialization for a specific DS"
New: "L3 Enterprise DS specialization. Activated when `.ds-context.md` declares `ds.maturity: enterprise`. Reads cascade, lint, docs, and library config from project context."

### Knowledge file updates

| File | Change |
|------|--------|
| `skills/shared/knowledge/governance.md` | Examples tool-agnostic; lint tools in "Known implementations" appendix |
| `skills/shared/knowledge/token-architecture.md` | 3-tier as recommendation, not requirement; `tokens.collections` can differ |
| `skills/shared/knowledge/documentation.md` | uSpec, Storybook, Zeroheight presented as equal options |

---

## 5. DS Scrub Plan

**Rule:** Zero references to any specific design system on `main`. DS-specific data lives in each consuming project's `.ds-context.md`, never in this repo.

### By tier

**Tier 1 — Active skill files (~8 files):** Generalize. Replace DS-specific names/keys/tools with `.ds-context.md` template variables. Keep structure and workflows.

- `skills/ds-producer/SKILL.md`
- `skills/ds-consumer/SKILL.md`
- `skills/ds-make/SKILL.md`
- `skills/design/SKILL.md`
- `skills/design-review/SKILL.md`
- `skills/ds-manage/SKILL.md`
- `skills/creative/SKILL.md`
- `skills/map-design/SKILL.md`

**Tier 2 — Shared knowledge/context:** Generalize or delete from main.

- The DS-specific shared context file → **Delete from main.** Its populated equivalent is each project's own `.ds-context.md`.
- `skills/shared/design-principles.md` → **Generalize.** IA principles and anti-patterns are universal; remove DS-specific names.
- `skills/shared/maturity-detection.md` → **Generalize.** L3 signal: `ds.maturity: enterprise`.

**Tier 3 — Project docs:** Generalize.

- `CLAUDE.md` — Remove all DS-specific references. Tech stack becomes adapter-agnostic.
- `README.md` — Already renamed. Generalize L3 row, file tree, license.
- `skills/README.md` — Generalize L3 table, maturity table, MCP/plugin tables.
- The historical onboarding doc from the two-skill era → **Delete from main.**

**Tier 4 — Plans and specs:** Generalize. All files in `docs/superpowers/plans/` and `docs/superpowers/specs/` — replace DS-specific references with generic equivalents or context-variable placeholders. These are historical docs but must still be clean on main.

**Tier 5 — Tools directory:**

- The DS-specific lint agent scripts → **Delete from main.** Superseded by PluginOS operations plus `governance.lint.*` config.

---

## 6. PluginOS Improvement Suggestions

Additions to PluginOS (github.com/LSDimi/PluginOS) that would supercharge design-superpowers agents.

### High impact

| Operation | Why | Token savings |
|-----------|-----|---------------|
| `get_selection_context` | Every sub-agent needs "what's selected?" before routing. Returns structured summary: node types, component names, instance status, applied styles/variables. | ~230 tok (1 call vs manual inspection) |
| `validate_ds_compliance` | Meta-operation: `lint_styles` + `lint_detached` + `lint_naming` + `check_contrast` in one call. Unified compliance report. | ~230 tok vs ~920 (4 separate calls) |
| `get_node_properties` | Full property table for a node — fills, strokes, effects, auto-layout, constraints, component properties. Replaces Prostar plugin dependency. | ~230 tok vs ~700 (execute_figma fallback) |
| `apply_variables` | Bind variables to node properties. Essential for token workflows. | ~230 tok vs ~700 (execute_figma fallback) |

### Medium impact

| Operation | Why |
|-----------|-----|
| `diff_versions` | Compare two component versions, report changes. Powers Version Advisor without manual diffing. |
| `batch_operations` | Execute N operations in one MCP call. Cascade audits go from N round-trips to 1. |
| `export_component_sheet` | Component anatomy as structured spec: property table, variant matrix, token bindings. Powers doc generation. |
| `subscribe_selection` (event-based) | Push selection changes instead of polling. Enables real-time design companion mode. |

### Architecture suggestion

Expose a `pluginos.registry.json` manifest listing all operations with schemas. Agents read once, cache, and make smarter operation selections without calling `list_operations` every time.

### Integration path

Agents should use existing PluginOS operations where available, fall back to `execute_figma` for gaps. As new operations ship, agents benefit automatically via `list_operations` discovery. No skill rewrites needed.

---

## 7. New Files Summary

| File | Purpose |
|------|---------|
| `skills/shared/figma-adapter.md` | Pitch copy, detection algorithm, adapter-to-tool mapping |
| `skills/shared/ds-context-schema.md` | `.ds-context.md` field documentation, valid values, defaults |
| `skills/shared/ds-context-loader.md` | Shared context-load step for ds-producer/ds-consumer workflows |
| `skills/shared/examples/minimal-ds-context.example.md` | Minimal config template |

## 8. Files Removed from Main

| File | Reason |
|------|--------|
| The DS-specific shared context file | Replaced by per-project `.ds-context.md` |
| The DS-specific lint agent scripts | Superseded by PluginOS + `governance.lint.*` config |
| The historical onboarding doc | Two-skill-era context, superseded by this spec |
