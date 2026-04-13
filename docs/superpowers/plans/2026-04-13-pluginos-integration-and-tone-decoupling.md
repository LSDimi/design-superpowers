# PluginOS Integration & Tone Decoupling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Decouple all Tone/Talon.One references from `main`, add PluginOS pitch flow, rewrite ds-producer/ds-consumer as generic enterprise DS specializations, and preserve the Tone configuration on a `tone-example` branch.

**Architecture:** Every DS-specific behavior reads from `.ds-context.md` at project root via a shared schema + loader. PluginOS is pitched as preferred Figma adapter on first Figma action, with graceful fallback to classic Figma MCP. L3 enterprise tier is triggered by `ds.maturity: enterprise`, not brand detection.

**Tech Stack:** Claude Code skills (Markdown SKILL.md format), PluginOS MCP, Figma MCP (fallback)

**Spec:** `docs/superpowers/specs/2026-04-13-pluginos-integration-and-tone-decoupling.md`

---

## Phase 1: Branch Snapshot & Foundation Files

### Task 1: Create `tone-example` branch

**Files:**
- No file changes — git operations only

- [ ] **Step 1: Create the branch from current HEAD**

```bash
git checkout -b tone-example
```

- [ ] **Step 2: Switch back to main**

```bash
git checkout main
```

- [ ] **Step 3: Verify branch exists**

```bash
git branch --list tone-example
```

Expected: `  tone-example` appears in the list.

---

### Task 2: Create `skills/shared/ds-context-schema.md`

**Files:**
- Create: `skills/shared/ds-context-schema.md`

- [ ] **Step 1: Write the schema documentation**

```markdown
# .ds-context.md Schema

> Loaded by ds-producer, ds-consumer, and any sub-agent that needs project-level DS configuration. This file documents every field in `.ds-context.md`, its valid values, and defaults.

## Location

`.ds-context.md` lives at the **project root** (same level as `DESIGN.md`). It is created automatically when `/ds-make` scaffolds a new DS, or manually by the user.

## Format

YAML frontmatter for structured fields. Optional prose body for free-form notes.

---

## Field Reference

### `ds` — Identity

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ds.name` | string | yes | — | Human-readable DS name (e.g. "Acme DS") |
| `ds.slug` | string | yes | — | Machine name for file prefixes, token namespaces (e.g. "acme") |
| `ds.version` | string | no | `"0.1.0"` | Current DS version. Used by Version Advisor. |
| `ds.maturity` | enum | yes | `"greenfield"` | One of: `greenfield`, `defined`, `system`, `enterprise`. Maps to L0–L3. |

**Maturity values:**
- `greenfield` (L0) — No DS exists. Full creative freedom.
- `defined` (L1) — Design language exists (DESIGN.md). Commands use it as constraint.
- `system` (L2) — DS with Figma libraries and token collections. Full DS-aware composition.
- `enterprise` (L3) — Full governance: cascade publishing, lint gates, documentation generation. Activates ds-producer/ds-consumer delegation.

### `figma` — Figma Integration

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `figma.adapter` | enum | no | unset | `pluginos`, `figma-mcp`, or unset. See `skills/shared/figma-adapter.md` for detection flow. |
| `figma.status` | enum | no | unset | `ready`, `pending-setup`, or unset. |
| `figma.libraries` | array | no | `[]` | Figma library entries. Each has `name`, `key`, and `role`. |

**Library roles:** `tokens`, `components`, `patterns`, `icons`, `documentation`, or custom strings. Role determines which cascade stage a library belongs to.

### `tokens` — Token System

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `tokens.collections` | array | no | `["primitive", "semantic", "component"]` | Token collection names in your variable system. |
| `tokens.format` | enum | no | `"figma-variables"` | `w3c-dtcf`, `style-dictionary`, `figma-variables`, or `custom`. |
| `tokens.export_path` | string | no | `"tokens/"` | Where exported token JSON lives in repo. |

### `governance` — Governance (drives L3 behavior)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `governance.tier` | enum | no | `"lightweight"` | `lightweight`, `standard`, or `enterprise`. Enterprise activates full cascade + lint gates. |
| `governance.cascade` | array | no | `[]` | Ordered list of publish stages. Each stage must pass QA before the next publishes. |
| `governance.lint.tool` | string | no | `"none"` | Lint plugin or tool name (e.g. "ds-lint", "stylelint-ds"). |
| `governance.lint.command` | string | no | — | CLI command to run lint (e.g. "npx @acme/ds-lint"). |
| `governance.docs.tool` | enum | no | `"none"` | `uspec`, `storybook`, `zeroheight`, `custom`, or `none`. |
| `governance.docs.repo` | string | no | — | Docs tool repo or URL. |
| `governance.contribution_process` | string | no | — | Path or URL to contribution guide. |
| `governance.versioning` | enum | no | `"semver"` | `semver`, `calver`, or `custom`. |

### `code` — Code Side

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `code.framework` | string | no | — | `react`, `vue`, `svelte`, `web-components`, or other. |
| `code.component_libs` | array | no | `[]` | npm package names for DS component libraries. |
| `code.token_import` | string | no | — | npm package or path for token imports. |

### `product` — Product Context (for /design)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `product.name` | string | no | — | Product name. |
| `product.docs_url` | string | no | — | Product documentation URL. |
| `product.personas` | array | no | `[]` | Target user personas. |

---

## Minimal Example

```yaml
---
ds:
  name: "My DS"
  slug: "myds"
  maturity: system
figma:
  adapter: pluginos
  status: ready
  libraries:
    - { name: "Components", key: "abc123", role: "components" }
---
```

## Enterprise Example

See the `tone-example` branch for a fully populated enterprise-tier `.ds-context.md`.
```

- [ ] **Step 2: Verify the file exists and is well-formed**

```bash
head -5 skills/shared/ds-context-schema.md
```

Expected: `# .ds-context.md Schema` as the first line.

- [ ] **Step 3: Commit**

```bash
git add skills/shared/ds-context-schema.md
git commit -m "feat: add .ds-context.md schema documentation"
```

---

### Task 3: Create `skills/shared/ds-context-loader.md`

**Files:**
- Create: `skills/shared/ds-context-loader.md`

- [ ] **Step 1: Write the context loader**

```markdown
# DS Context Loader

> Shared step loaded by ds-producer and ds-consumer workflows. Run this as Step 0 before any workflow logic.

## Purpose

Read and validate `.ds-context.md` from the project root. Extract structured fields for the current workflow. Report missing required fields clearly.

## Procedure

### Step 1: Locate context file

Read `.ds-context.md` from the project root (same directory as `DESIGN.md` or `CLAUDE.md`).

**If missing:** Stop. Tell the user:
> "This workflow requires a `.ds-context.md` file at the project root. Run `/ds-make` to scaffold your DS and create this file, or create one manually using the schema in `skills/shared/ds-context-schema.md`."

### Step 2: Parse frontmatter

Extract the YAML frontmatter between `---` delimiters. Parse into structured fields.

### Step 3: Validate required fields

**Always required:**
- `ds.name` — DS name
- `ds.slug` — machine name
- `ds.maturity` — must be one of: `greenfield`, `defined`, `system`, `enterprise`

**Required for L3 (enterprise) workflows:**
- `governance.tier` — must be `enterprise`
- `governance.cascade` — at least 2 stages
- `figma.libraries` — at least 1 library with a role

**If a required field is missing:** Ask the user to provide it. Offer to write it back to `.ds-context.md`.

### Step 4: Apply defaults for optional fields

| Field | Default |
|-------|---------|
| `tokens.collections` | `["primitive", "semantic", "component"]` |
| `tokens.format` | `"figma-variables"` |
| `governance.versioning` | `"semver"` |
| `governance.lint.tool` | `"none"` |
| `governance.docs.tool` | `"none"` |

### Step 5: Check Figma adapter

Read `figma.adapter`:
- If `pluginos` → use PluginOS tools for any Figma operations in this workflow
- If `figma-mcp` → use classic Figma MCP tools
- If unset → follow the pitch flow in `skills/shared/figma-adapter.md`

### Step 6: Return context object

Make the following values available to the workflow:

```
ds.name, ds.slug, ds.version, ds.maturity
figma.adapter, figma.status, figma.libraries[]
tokens.collections, tokens.format, tokens.export_path
governance.tier, governance.cascade[], governance.lint.tool,
governance.lint.command, governance.docs.tool, governance.docs.repo,
governance.versioning
code.framework, code.component_libs, code.token_import
product.name, product.docs_url, product.personas[]
```

Plus any free-form prose from the body section as `ds.notes`.

## Usage in workflows

Every ds-producer and ds-consumer workflow begins with:

> **Step 0 — Load context:** Follow `skills/shared/ds-context-loader.md`. Extract `ds.name`, `governance.cascade`, `figma.libraries`, and any other fields this workflow needs. If context is missing or invalid, stop and guide the user.

Individual workflows then reference specific context values like `{{ds.name}}`, `{{governance.cascade}}`, `{{governance.lint.command}}` etc. These are not literal template variables — they mean "use the value you loaded in Step 0."
```

- [ ] **Step 2: Commit**

```bash
git add skills/shared/ds-context-loader.md
git commit -m "feat: add shared ds-context-loader for enterprise workflows"
```

---

### Task 4: Create `skills/shared/figma-adapter.md`

**Files:**
- Create: `skills/shared/figma-adapter.md`

- [ ] **Step 1: Write the Figma adapter pitch and detection flow**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add skills/shared/figma-adapter.md
git commit -m "feat: add Figma adapter pitch, detection, and tool mapping"
```

---

### Task 5: Create `skills/shared/examples/minimal-ds-context.example.md`

**Files:**
- Create: `skills/shared/examples/minimal-ds-context.example.md`

- [ ] **Step 1: Create the examples directory and write the minimal example**

```bash
mkdir -p skills/shared/examples
```

Write `skills/shared/examples/minimal-ds-context.example.md`:

```markdown
# Minimal .ds-context.md Example

> Copy this to your project root as `.ds-context.md` and fill in your values.
> See `skills/shared/ds-context-schema.md` for full field documentation.

```yaml
---
ds:
  name: "My DS"
  slug: "myds"
  maturity: system              # greenfield | defined | system | enterprise

figma:
  libraries:
    - { name: "Components", key: "YOUR_FIGMA_FILE_KEY", role: "components" }
---

## Notes
Add any DS-specific conventions, exceptions, or current initiatives here.
```

For a fully populated enterprise-tier example, see the `tone-example` branch.
```

- [ ] **Step 2: Commit**

```bash
git add skills/shared/examples/minimal-ds-context.example.md
git commit -m "feat: add minimal .ds-context.md example template"
```

---

### Task 6: Rewrite `skills/shared/maturity-detection.md`

**Files:**
- Modify: `skills/shared/maturity-detection.md` (44 lines)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/shared/maturity-detection.md
```

- [ ] **Step 2: Rewrite the file**

Replace the entire file content. The new version must:
- Remove all references to "Tone" (lines 12, 30, 43)
- L3 detection: `ds.maturity == enterprise` OR `governance.tier == enterprise` in `.ds-context.md`
- Remove `name: Tone` check from detection logic
- Replace "Tone-aware" in behavior table with "Enterprise DS-aware"
- Remove "For Tone DS, `skills/shared/tone-ds-context.md` serves as the equivalent" sentence
- Replace with: "See `skills/shared/ds-context-schema.md` for the full schema."

Write the complete new file:

```markdown
# Maturity Detection

> Loaded by every command router before routing to sub-agents. Determines project maturity level (L0–L3) which controls sub-agent behavior.

## Detection procedure

Run these checks in order. Stop at the first match:

1. Check if `.ds-context.md` exists at the project root.
2. If it exists: Read the YAML frontmatter.
   - If `ds.maturity` is `enterprise` OR `governance.tier` is `enterprise` → **L3 Enterprise DS**
   - Otherwise → **L2 Has design system**
3. If `.ds-context.md` does not exist: Check if `DESIGN.md` exists at the project root.
   - If `DESIGN.md` exists → **L1 Design language defined**
   - If neither exists → **L0 Greenfield**

## Announce

Every command must announce the detected level before proceeding:

> "Detected maturity level: **L2 — Has design system** (`{{ds.name}}`). Adapting behavior accordingly."

At L3, also announce:

> "Enterprise DS detected. ds-producer/ds-consumer specializations are active."

## Behavior adaptation by level

| Level | /creative | /ds-make | /ds-manage | /design | /design-review | /map-design |
|-------|-----------|----------|------------|---------|----------------|-------------|
| L0 | Full freedom; no constraints | Scaffold from scratch | Not available (no DS to manage) | Use DESIGN.md or freeform | Visual quality + UX only | Full extraction; generate DESIGN.md |
| L1 | Refine existing design language | Extend toward a DS | Limited; governance not defined | Use DESIGN.md as constraint | All L0 + DESIGN.md conformance | Refresh DESIGN.md from current state |
| L2 | DS-constrained exploration | Extend the DS; use .ds-context.md | Full operations with governance.md rules | Full DS-aware composition | All + DS compliance checking | Refresh mode; snapshot DS state |
| L3 | DS-constrained; flag if exploring outside DS | Delegate to ds-producer workflows | Full operations + lint via configured adapter | Delegate to ds-consumer | All + lint-based DS compliance | Limited; enterprise DS already defined |

## User patterns → maturity signals

| User says... | Likely level |
|--------------|-------------|
| "start a design system", "create tokens from scratch" | L0 |
| "I have a DESIGN.md, extend it" | L1 |
| "use our component library", "check against our DS" | L2 |
| "publish to the cascade", "run lint", "generate docs" | L3 |

## Project context files

- **DESIGN.md** — Human-readable design language definition. Generated by `/map-design`, used as constraint by all commands at L1+.
- **.ds-context.md** — Machine-readable DS metadata: library keys, token collections, governance config, Figma adapter. See `skills/shared/ds-context-schema.md` for the full schema.
```

- [ ] **Step 3: Verify no Tone/Talon references remain**

```bash
grep -in "tone\|talon" skills/shared/maturity-detection.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add skills/shared/maturity-detection.md
git commit -m "feat: rewrite maturity detection — L3 via ds.maturity, remove Tone"
```

---

## Phase 2: Generalize Enterprise Skills

### Task 7: Rewrite `skills/ds-producer/SKILL.md`

**Files:**
- Modify: `skills/ds-producer/SKILL.md` (274 lines, ~48 Tone references)

This is the heaviest rewrite. Every Tone-specific value becomes a `.ds-context.md` read.

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/ds-producer/SKILL.md
```

- [ ] **Step 2: Rewrite the file**

Apply these changes throughout the file:

**Header (lines 1–15):**
- Line 3: `"Tone DS components"` → `"design system components"`
- Line 8: `"You are a Design System Producer agent for Tone DS (Talon.One's design system)."` → `"You are a Design System Producer agent. You manage the lifecycle of DS artifacts — tokens, components, patterns, documentation — for the project's enterprise-tier design system."`
- Line 10: `"See skills/shared/tone-ds-context.md for Tone DS structure"` → `"See skills/shared/ds-context-loader.md for context loading. See skills/shared/ds-context-schema.md for field reference."`
- Line 14: `"L3 (Enterprise/Tone) specialization...identifies Tone"` → `"L3 (Enterprise) specialization invoked by /ds-make when .ds-context.md declares ds.maturity: enterprise or governance.tier: enterprise."`

**All workflows — add Step 0:**
Every workflow section gets a new opening step:
> **Step 0 — Load context:** Follow `skills/shared/ds-context-loader.md`. Extract `ds.name`, `governance.cascade`, `governance.lint.tool`, `governance.lint.command`, `governance.docs.tool`, `figma.libraries`, `tokens.collections`, and `governance.versioning`.

**Workflow-specific changes:**

Throughout all workflows, apply these replacements:
- `"Tone DS"` / `"Tone"` (as DS name) → `"the DS"` or `"{{ds.name}}"`
- `"Tone Lint"` → `"the configured lint tool ({{governance.lint.tool}})"` or `"DS lint"`
- `"Tone. Foundations"` / `"Tone. Components"` / `"Tone. Patterns"` → `"the foundations library ({{figma.libraries[role=tokens]}})"`, `"the components library ({{figma.libraries[role=components]}})"`, `"the patterns library ({{figma.libraries[role=patterns]}})"`
- `"Talon.One"` → remove or replace with `"the product ({{product.name}})"`
- `"tone-ds-context.md"` → `".ds-context.md"` or `"ds-context-schema.md"` as appropriate
- Hardcoded cascade order → `"follow {{governance.cascade}} order"`
- Hardcoded Figma file keys → `"use {{figma.libraries}} keys"`
- `"use_figma"` tool references → `"use your configured Figma adapter (see skills/shared/figma-adapter.md)"`

**Tone Lint integration section (lines ~151–192):**
Rewrite as a generic lint integration section:
- Replace specific Tone Lint rules table with: "Run the project's configured lint tool (`{{governance.lint.command}}`). If using PluginOS, call `run_operation('lint_styles')`, `run_operation('lint_detached')`, and `run_operation('lint_naming')` for built-in checks."
- Remove Tone Lint plugin data namespace references (`sharedPluginData`, `tone_lint`)
- Keep the concept of "pre-publish QA gate with lint" but make it tool-agnostic

**Library Analytics section (lines ~207–223):**
- Remove hardcoded library names ("Tone. Foundations", "Tone. Components", etc.)
- Replace with: "Track adoption across all libraries declared in `{{figma.libraries}}`. Compare DS library usage vs. legacy/unstyled usage."
- Remove "Legacy Library" as a specific name — generalize to "non-DS libraries"

**Quality gate (line ~261):**
- `"Tone Lint — no violations"` → `"DS lint — no violations ({{governance.lint.tool}})"`

- [ ] **Step 3: Verify no Tone/Talon references remain**

```bash
grep -in "tone\|talon" skills/ds-producer/SKILL.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add skills/ds-producer/SKILL.md
git commit -m "feat: generalize ds-producer — read all config from .ds-context.md"
```

---

### Task 8: Rewrite `skills/ds-consumer/SKILL.md`

**Files:**
- Modify: `skills/ds-consumer/SKILL.md` (179 lines, ~38 Tone references)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/ds-consumer/SKILL.md
```

- [ ] **Step 2: Rewrite the file**

Apply these changes:

**Header (lines 1–15):**
- Line 3: `"Talon.One product features"` → `"product features using an enterprise DS"`
- Line 8: `"You are a Product Design agent for Talon.One. You help the design team use Tone DS"` → `"You are a Product Design agent. You help the design team use the project's enterprise-tier design system to build product features."`
- Line 10: `"skills/shared/tone-ds-context.md for Tone DS structure"` → `"skills/shared/ds-context-loader.md for context loading. See skills/shared/ds-context-schema.md for field reference."`
- Line 14: `"L3 (Enterprise/Tone)...identifies Tone"` → `"L3 (Enterprise) specialization invoked by /design when .ds-context.md declares ds.maturity: enterprise."`

**Hard rules (lines 18–24):**
- `"Never apply overrides to Tone components"` → `"Never apply overrides to DS components"`
- `"Never detach Tone instances"` → `"Never detach DS component instances"`
- All rules: replace "Tone" with "DS" or "the DS"

**Add Step 0 to every workflow:**
> **Step 0 — Load context:** Follow `skills/shared/ds-context-loader.md`. Extract `ds.name`, `figma.libraries`, `product.name`, `product.docs_url`, `product.personas`, and `governance.lint.tool`.

**Workflow-specific changes:**
- All `"Tone DS"` → `"the DS"` or `"{{ds.name}}"`
- All `"Tone components"` → `"DS components"`
- All `"Tone Patterns"` → `"DS patterns ({{figma.libraries[role=patterns]}})"`
- All `"Talon.One"` → `"the product ({{product.name}})"`
- All `"docs.talon.one"` → `"{{product.docs_url}}"`
- All `"use_figma"` → `"configured Figma adapter (see skills/shared/figma-adapter.md)"`

**Product Awareness section (lines ~137+):**
- `"Talon.One Product Awareness"` → `"Product Awareness"`
- Remove hardcoded entity definitions (campaigns, coupons, loyalty, achievements, etc.)
- Replace with: "Refer to `{{product.docs_url}}` for entity definitions and domain terminology. Key personas: `{{product.personas}}`."
- Keep the structure (the concept of product awareness) but make content dynamic

- [ ] **Step 3: Verify no Tone/Talon references remain**

```bash
grep -in "tone\|talon" skills/ds-consumer/SKILL.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add skills/ds-consumer/SKILL.md
git commit -m "feat: generalize ds-consumer — read all config from .ds-context.md"
```

---

## Phase 3: Scrub Command Routers (Tier 1)

### Task 9: Scrub `skills/ds-make/SKILL.md`

**Files:**
- Modify: `skills/ds-make/SKILL.md` (245 lines, 6 refs)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/ds-make/SKILL.md
```

- [ ] **Step 2: Apply edits**

- Line 8: `"L3 (Tone/Enterprise)"` → `"L3 (Enterprise)"`
- Line 17: `"L3 (Tone/Enterprise)"` → `"L3 (Enterprise DS): Delegate to ds-producer. Load .ds-context.md for all DS configuration."`
- Line 45: `"token creation within Tone"` → `"token creation within the enterprise DS"`
- Line 91: `"building in Tone"` → `"building within the enterprise DS"`
- Line 164: `"plan a Tone Lint"` → `"plan a DS lint (using the configured lint tool)"`

- [ ] **Step 3: Verify no Tone/Talon references remain**

```bash
grep -in "tone\|talon" skills/ds-make/SKILL.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add skills/ds-make/SKILL.md
git commit -m "feat: scrub Tone refs from /ds-make router"
```

---

### Task 10: Scrub `skills/design/SKILL.md`

**Files:**
- Modify: `skills/design/SKILL.md` (246 lines, 7 refs)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/design/SKILL.md
```

- [ ] **Step 2: Apply edits**

- Line 8: `"At L3 (Tone/Enterprise)"` → `"At L3 (Enterprise)"`
- Line 17: `"L3 (Tone/Enterprise)"` → `"L3 (Enterprise DS): Delegate to ds-consumer."`
- Line 58: `"L3 Tone"` → `"L3 enterprise DS"`
- Line 157: `"Tone Patterns (L1) and Squad Patterns (L2)"` → `"DS patterns (from {{figma.libraries[role=patterns]}}) and squad patterns"`
- Line 183: `"Tone Patterns L1 / Squad Patterns L2"` → `"DS Patterns / Squad Patterns"`

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" skills/design/SKILL.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add skills/design/SKILL.md
git commit -m "feat: scrub Tone refs from /design router"
```

---

### Task 11: Scrub `skills/ds-manage/SKILL.md`

**Files:**
- Modify: `skills/ds-manage/SKILL.md` (279 lines, 13 refs)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/ds-manage/SKILL.md
```

- [ ] **Step 2: Apply edits**

- Line 8: `"At L3 (Tone)"` → `"At L3 (Enterprise)"`
- Line 19: `"L3 (Tone/Enterprise)"` → `"L3 (Enterprise DS)"`
- Line 59: `"Use use_figma to read Tone Lint"` → `"Use the configured Figma adapter to run DS lint (see skills/shared/figma-adapter.md)"`
- Line 71: `"Tone Lint — no violations"` → `"DS lint — no violations"`
- Line 102: `"Tone Lint (L3)"` → `"DS lint (L3)"`
- Line 124: `"Tracked libraries: Tone. Foundations..."` → `"Tracked libraries: read from {{figma.libraries}} in .ds-context.md"`
- Lines 135–137: Replace all `"Tone instances vs. Legacy Library"` → `"DS component instances vs. non-DS usage"`
- Line 150: `"Team | Tone | Legacy"` → `"Team | DS Library | Non-DS | Adoption % | Trend"`
- Lines 226, 239–240: Replace all `"Tone Lint"` → `"DS lint"` and `"use_figma"` → `"configured Figma adapter"`

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" skills/ds-manage/SKILL.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add skills/ds-manage/SKILL.md
git commit -m "feat: scrub Tone refs from /ds-manage router"
```

---

### Task 12: Scrub `skills/design-review/SKILL.md`

**Files:**
- Modify: `skills/design-review/SKILL.md` (317 lines, 10 refs)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/design-review/SKILL.md
```

- [ ] **Step 2: Apply edits**

- Line 17: `"L3 (Tone/Enterprise)"` → `"L3 (Enterprise DS)"`
- Line 47: `"Tone Lint"` in routing table → `"DS lint"`
- Line 225: `"this sub-agent reads Tone Lint results via use_figma"` → `"this sub-agent reads DS lint results via the configured Figma adapter (see skills/shared/figma-adapter.md)"`
- Lines 234–241: Replace all `"At L3 (Tone DS)"` → `"At L3 (Enterprise DS)"`, all `"Tone Lint"` → `"DS lint"`, all `"use_figma"` → `"configured Figma adapter"`
- Line 250: `"Tone Lint run"` → `"DS lint run"`
- Line 258: `"Lint source: Tone Lint automated"` → `"Lint source: DS lint (automated via {{governance.lint.tool}})"`

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" skills/design-review/SKILL.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add skills/design-review/SKILL.md
git commit -m "feat: scrub Tone refs from /design-review router"
```

---

### Task 13: Scrub `skills/creative/SKILL.md`

**Files:**
- Modify: `skills/creative/SKILL.md` (208 lines, ~3 refs but 2 are generic "tone" usage)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/creative/SKILL.md
```

- [ ] **Step 2: Apply edits**

- Line 17: `"L3 (Tone/Enterprise)"` → `"L3 (Enterprise DS)"`
- Lines 129, 135: These use "tone" generically (as in "tone — editorial", "against the tone") — **keep as-is**, these are not DS references

- [ ] **Step 3: Verify only generic "tone" usage remains**

```bash
grep -in "tone" skills/creative/SKILL.md
```

Expected: Only lines with "tone" in the sense of "editorial tone" or "color tone" — NOT "Tone DS".

- [ ] **Step 4: Commit**

```bash
git add skills/creative/SKILL.md
git commit -m "feat: scrub Tone DS refs from /creative router"
```

---

### Task 14: Scrub `skills/map-design/SKILL.md`

**Files:**
- Modify: `skills/map-design/SKILL.md` (372 lines, ~2 refs)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/map-design/SKILL.md
```

- [ ] **Step 2: Apply edits**

- Line 17: `"L3 (Tone/Enterprise)"` → `"L3 (Enterprise DS)"`
- Line 297: `"color tone"` — **keep as-is**, this is a generic design term

- [ ] **Step 3: Verify**

```bash
grep -in "tone" skills/map-design/SKILL.md
```

Expected: Only "color tone" (generic design term).

- [ ] **Step 4: Commit**

```bash
git add skills/map-design/SKILL.md
git commit -m "feat: scrub Tone DS refs from /map-design router"
```

---

## Phase 4: Scrub Shared Files (Tier 2)

### Task 15: Generalize `skills/shared/design-principles.md`

**Files:**
- Modify: `skills/shared/design-principles.md` (127 lines, 9 refs)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/shared/design-principles.md
```

- [ ] **Step 2: Apply edits**

- Line 19: `"Reuse Tone Patterns (L1)"` → `"Reuse DS patterns"`
- Line 67: `"Use Tone components"` → `"Use DS components"`
- Line 72: `"Run Tone Lint"` → `"Run DS lint"`
- Line 74: `"Tone DS Governance Checklist"` → `"DS Governance Checklist"`
- Line 84: `"Tone colors, typography"` → `"DS colors, typography"`
- Lines 116–117: `"Tone components used"` → `"DS components used"`, `"Tone spacing applied"` → `"DS spacing applied"`

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" skills/shared/design-principles.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add skills/shared/design-principles.md
git commit -m "feat: generalize design-principles.md — remove Tone refs"
```

---

### Task 16: Delete `skills/shared/tone-ds-context.md` from main

**Files:**
- Delete: `skills/shared/tone-ds-context.md`

- [ ] **Step 1: Remove the file**

```bash
git rm skills/shared/tone-ds-context.md
```

- [ ] **Step 2: Commit**

```bash
git commit -m "feat: remove tone-ds-context.md from main — lives on tone-example branch"
```

---

### Task 17: Generalize `skills/shared/knowledge/governance.md`

**Files:**
- Modify: `skills/shared/knowledge/governance.md` (122 lines, 8 refs)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/shared/knowledge/governance.md
```

- [ ] **Step 2: Apply edits**

- Line 53: `"Use Tone components"` → `"Use DS components"`
- Line 58: `"Run Tone Lint"` → `"Run DS lint ({{governance.lint.command}})"`
- Line 68: `"run Tone Lint"` → `"run DS lint"`
- Line 70: `"Tone DS Governance Checklist"` → `"DS Governance Checklist"`
- Line 82: `"Tone colors, typography"` → `"DS colors, typography"`
- Lines 115–116: `"Tone components"` → `"DS components"`, `"Tone spacing"` → `"DS spacing"`

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" skills/shared/knowledge/governance.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add skills/shared/knowledge/governance.md
git commit -m "feat: generalize governance.md — remove Tone refs"
```

---

### Task 18: Generalize `skills/shared/knowledge/token-architecture.md`

**Files:**
- Modify: `skills/shared/knowledge/token-architecture.md` (80 lines, 2 refs)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/shared/knowledge/token-architecture.md
```

- [ ] **Step 2: Apply edit**

- Line 3: `"See skills/shared/tone-ds-context.md for the Tone DS implementation example"` → `"3-tier model (primitive/semantic/component) is a common pattern. Your project's token collections are configured in .ds-context.md under tokens.collections."`

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" skills/shared/knowledge/token-architecture.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add skills/shared/knowledge/token-architecture.md
git commit -m "feat: generalize token-architecture.md — remove Tone ref"
```

---

### Task 19: Generalize `skills/shared/knowledge/documentation.md`

**Files:**
- Modify: `skills/shared/knowledge/documentation.md` (153 lines, 1 ref)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/shared/knowledge/documentation.md
```

- [ ] **Step 2: Apply edit**

- Line 127: `"Figma \"Demo Area\" file (see skills/shared/tone-ds-context.md for file key)"` → `"Figma Demo Area file (if one exists — check {{figma.libraries}} for a library with role \"documentation\")"`

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" skills/shared/knowledge/documentation.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add skills/shared/knowledge/documentation.md
git commit -m "feat: generalize documentation.md — remove Tone ref"
```

---

## Phase 5: Scrub Project Docs (Tier 3)

### Task 20: Rewrite `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md` (106 lines, 11 refs)

- [ ] **Step 1: Read the current file**

```bash
cat -n CLAUDE.md
```

- [ ] **Step 2: Apply edits**

- Line 7: `"Talon.One design team"` → `"design teams"`
- Lines 17–19: `"L3 Specializations (Tone/Enterprise):"` → `"L3 Specializations (Enterprise DS):"`, `"(Tone DS detected)"` → `"(enterprise DS detected via .ds-context.md)"`
- Line 25: `"skills/shared/tone-ds-context.md"` → remove from L4 list, replace with `".ds-context.md (project root)"`
- Line 29: `"Figma (Tone DS) — inspect via Figma MCP"` → `"Figma — inspect via PluginOS (preferred) or Figma MCP (see skills/shared/figma-adapter.md)"`
- Line 33: `"Tone Lint (validation), Prostar (property tables)"` → `"Configured via governance.lint.tool in .ds-context.md"`
- Line 61: `"tone-ds-context.md"` comment → remove line or replace with `"ds-context-schema.md     # .ds-context.md field documentation"`
- Lines 69–70: `"# L3 Tone specialization"` → `"# L3 Enterprise DS specialization"`
- Line 80: `"At L3 (Tone DS), /ds-make delegates"` → `"At L3 (Enterprise DS), /ds-make delegates"`
- Line 99: `"docs.talon.one | Product context for DS Consumer"` → remove row or replace with `"Product docs URL | Configured via product.docs_url in .ds-context.md"`

Also update project name references:
- Line 7: update to mention `design-superpowers`

Also update File Structure to reflect new files:
- Add `ds-context-schema.md`, `ds-context-loader.md`, `figma-adapter.md`, `examples/` directory
- Remove `tone-ds-context.md`

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" CLAUDE.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "feat: generalize CLAUDE.md — remove all Tone/Talon refs"
```

---

### Task 21: Update `README.md`

**Files:**
- Modify: `README.md` (95 lines, 7 refs)

- [ ] **Step 1: Read the current file**

```bash
cat -n README.md
```

- [ ] **Step 2: Apply edits**

- Line 18: `"when Tone DS is detected"` → `"when enterprise DS is detected via .ds-context.md"`
- Lines 22-23: `"when Tone DS is detected"` → `"when ds.maturity is enterprise"`
- Line 43: `".ds-context.md names Tone (or equivalent)"` → `".ds-context.md declares ds.maturity: enterprise"`
- Line 63: `"tone-ds-context.md      # L4 Tone-specific context"` → `"ds-context-schema.md    # .ds-context.md field documentation"`, add new shared files
- Lines 71-72: `"# L3 Tone specialization"` → `"# L3 Enterprise DS specialization"`
- Line 94: `"Internal Talon.One project. Not currently licensed for external distribution."` → `"MIT" or appropriate open license`

Also update file tree to add new files and remove deleted ones.

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" README.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "feat: generalize README.md — remove Tone/Talon refs"
```

---

### Task 22: Update `skills/README.md`

**Files:**
- Modify: `skills/README.md` (106 lines, 5 refs)

- [ ] **Step 1: Read the current file**

```bash
cat -n skills/README.md
```

- [ ] **Step 2: Apply edits**

- Line 18: `"L3 Tone specializations"` → `"L3 Enterprise DS specializations"`
- Lines 22–23: `"when Tone DS is detected"` → `"when ds.maturity is enterprise"`
- Line 66: `"tone-ds-context.md"` → `"ds-context-schema.md"` in knowledge architecture diagram
- Line 81: `".ds-context.md names Tone"` → `".ds-context.md declares ds.maturity: enterprise"`
- Line 104: `"Tone Lint"` → `"DS lint (configured via governance.lint.tool)"`

Also update MCP integrations table to include PluginOS:
```
| MCP | Status | Purpose |
|-----|--------|---------|
| PluginOS | Recommended | Agent-native Figma operations (~230 tok/call) |
| Figma MCP | Fallback | Component inspection, screenshots, design context |
```

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" skills/README.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add skills/README.md
git commit -m "feat: generalize skills/README.md — add PluginOS, remove Tone refs"
```

---

### Task 23: Archive `PROJECT_CONTEXT.md`

**Files:**
- Move: `PROJECT_CONTEXT.md` → `docs/archive/PROJECT_CONTEXT.md`

- [ ] **Step 1: Create archive directory and move the file**

```bash
mkdir -p docs/archive
git mv PROJECT_CONTEXT.md docs/archive/PROJECT_CONTEXT.md
```

- [ ] **Step 2: Commit**

```bash
git commit -m "chore: archive PROJECT_CONTEXT.md — historical two-skill era doc"
```

---

## Phase 6: Scrub Historical Docs (Tier 4)

### Task 24: Scrub `docs/superpowers/specs/2026-04-09-universal-design-plugin-design.md`

**Files:**
- Modify: `docs/superpowers/specs/2026-04-09-universal-design-plugin-design.md` (208 lines)

- [ ] **Step 1: Read the file**

```bash
cat -n docs/superpowers/specs/2026-04-09-universal-design-plugin-design.md
```

- [ ] **Step 2: Replace all Tone/Talon references**

Search and replace throughout:
- `"Tone"` (as DS name) → `"the project DS"` or `"enterprise DS"`
- `"Tone DS"` → `"enterprise DS"`
- `"Talon.One"` → `"the product"`
- `"Tone Lint"` → `"DS lint"`
- `"Tone-specific"` → `"DS-specific"`

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" docs/superpowers/specs/2026-04-09-universal-design-plugin-design.md
```

Expected: No output (allow "tone" only in generic design sense like "color tone").

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/specs/2026-04-09-universal-design-plugin-design.md
git commit -m "chore: scrub Tone refs from original spec"
```

---

### Task 25: Scrub `docs/superpowers/plans/2026-04-09-universal-design-plugin.md`

**Files:**
- Modify: `docs/superpowers/plans/2026-04-09-universal-design-plugin.md` (1359 lines)

- [ ] **Step 1: Read the file in chunks**

```bash
cat -n docs/superpowers/plans/2026-04-09-universal-design-plugin.md | head -500
cat -n docs/superpowers/plans/2026-04-09-universal-design-plugin.md | tail -n +501 | head -500
cat -n docs/superpowers/plans/2026-04-09-universal-design-plugin.md | tail -n +1001
```

- [ ] **Step 2: Find all references and replace**

```bash
grep -in "tone\|talon" docs/superpowers/plans/2026-04-09-universal-design-plugin.md
```

For each match, apply the same replacement rules:
- `"Tone"` (DS name) → `"enterprise DS"` or `"the project DS"`
- `"Tone Lint"` → `"DS lint"`
- `"Talon.One"` → `"the product"`
- `"tone-ds-context.md"` → `".ds-context.md"`
- `"Tone. Foundations"` etc. → `"foundations library"` etc.

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" docs/superpowers/plans/2026-04-09-universal-design-plugin.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/plans/2026-04-09-universal-design-plugin.md
git commit -m "chore: scrub Tone refs from universal design plugin plan"
```

---

### Task 26: Scrub `docs/superpowers/plans/2026-04-08-plugin-integration.md`

**Files:**
- Modify: `docs/superpowers/plans/2026-04-08-plugin-integration.md` (214 lines)

- [ ] **Step 1: Read and find references**

```bash
cat -n docs/superpowers/plans/2026-04-08-plugin-integration.md
```

- [ ] **Step 2: Replace all Tone/Talon references**

Same replacement rules as Task 25. Replace all `tone_analytics_report`, `tone_lint_rules`, `tone_component_search`, `tone_inspect`, `talon_context` identifiers with generic equivalents: `ds_analytics_report`, `ds_lint_rules`, `ds_component_search`, `ds_inspect`, `ds_context`.

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" docs/superpowers/plans/2026-04-08-plugin-integration.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/plans/2026-04-08-plugin-integration.md
git commit -m "chore: scrub Tone refs from plugin integration plan"
```

---

### Task 27: Scrub `docs/superpowers/plans/2026-04-08-headless-tone-lint.md`

**Files:**
- Modify: `docs/superpowers/plans/2026-04-08-headless-tone-lint.md` (452 lines)

- [ ] **Step 1: Read and find references**

```bash
cat -n docs/superpowers/plans/2026-04-08-headless-tone-lint.md
```

- [ ] **Step 2: Replace all Tone/Talon references**

This file documents a Tone Lint-specific integration. Generalize:
- File title: `"Headless Tone Lint"` → `"Headless DS Lint"`
- All `"Tone Lint"` → `"DS lint"`
- All `"tone_lint"` (code identifiers) → `"ds_lint"`
- All `"Tone"` (as DS name) → `"the DS"` or `"enterprise DS"`

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" docs/superpowers/plans/2026-04-08-headless-tone-lint.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/plans/2026-04-08-headless-tone-lint.md
git commit -m "chore: scrub Tone refs from headless lint plan"
```

---

### Task 28: Scrub `docs/superpowers/plans/2026-04-07-tone-ds-skills.md`

**Files:**
- Modify: `docs/superpowers/plans/2026-04-07-tone-ds-skills.md` (797 lines)

- [ ] **Step 1: Read in chunks and find references**

```bash
grep -in "tone\|talon" docs/superpowers/plans/2026-04-07-tone-ds-skills.md | head -60
```

- [ ] **Step 2: Replace all Tone/Talon references**

This has ~100 references. Apply:
- `"Tone DS Skills"` (title) → `"DS Skills"`
- `"Tone DS"` → `"enterprise DS"` or `"the DS"`
- `"Talon.One"` → `"the product"`
- `"Tone Lint"` → `"DS lint"`
- `"tone-ds-context.md"` → `".ds-context.md"`
- All hardcoded library names → generic equivalents

- [ ] **Step 3: Verify**

```bash
grep -in "tone\|talon" docs/superpowers/plans/2026-04-07-tone-ds-skills.md
```

Expected: No output.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/plans/2026-04-07-tone-ds-skills.md
git commit -m "chore: scrub Tone refs from original DS skills plan"
```

---

## Phase 7: Delete Tools & Final Cleanup

### Task 29: Delete `tools/tone-lint-agent/` from main

**Files:**
- Delete: `tools/tone-lint-agent/` (entire directory)

- [ ] **Step 1: Remove the directory**

```bash
git rm -r tools/tone-lint-agent/
```

- [ ] **Step 2: Check if tools/ directory is now empty**

```bash
ls tools/ 2>/dev/null || echo "tools/ directory is empty or gone"
```

If empty, remove it:
```bash
rmdir tools/ 2>/dev/null
```

- [ ] **Step 3: Commit**

```bash
git add -A tools/
git commit -m "feat: remove tone-lint-agent from main — lives on tone-example branch"
```

---

### Task 30: Full repo verification

**Files:**
- No changes — verification only

- [ ] **Step 1: Search entire repo for remaining Tone/Talon references**

```bash
grep -rin "tone\|talon" --include="*.md" --include="*.js" . | grep -v "node_modules" | grep -v ".git/"
```

- [ ] **Step 2: Triage results**

For each match, classify:
- **Generic "tone"** (color tone, tone of voice, editorial tone) → **keep**
- **"Tone" as DS name, "Talon.One", "Talon"** → **must fix** — note the file and line

- [ ] **Step 3: Fix any remaining references**

If any non-generic references remain, edit each file to replace them using the same patterns from earlier tasks.

- [ ] **Step 4: Final commit if needed**

```bash
git add -A
git commit -m "chore: final Tone/Talon scrub — clean main branch"
```

---

## Phase 8: Tone-Example Branch Finalization

### Task 31: Create `.ds-context.md` on `tone-example` branch

**Files:**
- Create: `.ds-context.md` (on `tone-example` branch only)

- [ ] **Step 1: Switch to tone-example branch**

```bash
git checkout tone-example
```

- [ ] **Step 2: Merge main to pick up all generalized skills**

```bash
git merge main
```

Resolve any conflicts. The conflicts will be in files where main deleted/generalized content that the branch still has in original form. In all cases, take main's version (the generalized version).

- [ ] **Step 3: Create `.ds-context.md` with Tone configuration**

Write `.ds-context.md` at project root:

```yaml
---
ds:
  name: "Tone"
  slug: "tone"
  version: "2.4.1"
  maturity: enterprise

figma:
  adapter: pluginos
  status: ready
  libraries:
    - { name: "Tone. Foundations", key: "Pn9sIWsLKN7gQKj1RkV75j", role: "tokens" }
    - { name: "Tone. Components", key: "rVLnzp5jPQee88ThR81Ha", role: "components" }
    - { name: "Tone. Patterns", key: "H4A6DU7tCNJ7Qt4UwCuQy2", role: "patterns" }

tokens:
  collections: ["primitive", "semantic", "component"]
  format: "figma-variables"
  export_path: "tokens/"

governance:
  tier: enterprise
  cascade:
    - foundations
    - components
    - patterns
    - squad-patterns
    - final
  lint:
    tool: "tone-lint"
    command: "npx tone-lint"
  docs:
    tool: "uspec"
    repo: "github.com/redongreen/uSpec"
  contribution_process: "docs/contributing.md"
  versioning: semver

code:
  framework: "react"
  component_libs: ["@talon-one/tone-ui"]
  token_import: "@talon-one/tone-tokens"

product:
  name: "Talon.One"
  docs_url: "docs.talon.one"
  personas: ["admin", "marketer", "developer"]
---

## Tone DS Notes

Tone is Talon.One's design system. Built on React + ArkUI + Zag.js.

### Figma plugins
- **Tone Lint** — foundation validation, detached component detection
- **Prostar** — property table generation in Demo area

### Key conventions
- 3-tier token architecture: primitive → semantic → component
- Publishing cascade must be followed in order
- Pre-handoff: run Tone Lint → designer UX review → engineering handoff
```

- [ ] **Step 4: Commit on tone-example branch**

```bash
git add .ds-context.md
git commit -m "feat: add Tone .ds-context.md — enterprise DS configuration"
```

- [ ] **Step 5: Switch back to main**

```bash
git checkout main
```

---

### Task 32: Verify both branches

- [ ] **Step 1: Verify main is clean**

```bash
git checkout main
grep -rin "tone\|talon" --include="*.md" --include="*.js" . | grep -v "node_modules" | grep -v ".git/" | grep -iv "color tone\|editorial tone\|tone of voice\|primary tone"
```

Expected: No output (or only generic "tone" usage in design context).

- [ ] **Step 2: Verify tone-example has the config**

```bash
git checkout tone-example
cat .ds-context.md | head -10
git checkout main
```

Expected: First 10 lines show the Tone YAML frontmatter.

- [ ] **Step 3: Count the diff**

```bash
git diff main..tone-example --stat
```

Expected: `.ds-context.md` is the primary unique file on the branch, plus any Tone-specific files that were deleted from main.

---

## Phase 9: PluginOS Improvement Proposals

### Task 33: Export PluginOS improvement suggestions to standalone file

**Files:**
- Create: `docs/superpowers/pluginos-improvements.md`

- [ ] **Step 1: Write the PluginOS improvements document**

Extract PluginOS improvement suggestions from the spec (`docs/superpowers/specs/2026-04-13-pluginos-integration-and-tone-decoupling.md`, Section 6) into a standalone actionable document. Structure it as:

```markdown
# PluginOS Improvement Proposals for Design Superpowers

> Proposed additions to [PluginOS](https://github.com/LSDimi/PluginOS) that would supercharge design-superpowers agents. Ordered by impact.
> 
> **Status:** Proposals — not blocking design-superpowers v1. Agents use existing operations + `execute_figma` fallback.

## High Impact

### 1. `get_selection_context`
**Category:** inspection
**Why:** Every sub-agent needs "what's selected?" before routing. Currently requires manual inspection or multiple calls.
**Returns:** `{ nodes: [{id, name, type, isInstance, componentName, parentFrame, appliedStyles, appliedVariables}], summary: "3 frames selected: 'Header', 'Card', 'Footer'. 2 are component instances." }`
**Token cost:** ~230 tok (1 call vs manual inspection chain)
**Used by:** All 6 commands at workflow start

### 2. `validate_ds_compliance`
**Category:** lint
**Why:** Agents currently need 4 round-trips for a full compliance check. This meta-operation runs `lint_styles` + `lint_detached` + `lint_naming` + `check_contrast` and returns a unified report.
**Returns:** `{ checks: [{name, passed, failed, details}], summary: "4 checks run. 2 pass, 2 have findings (3 detached instances, 1 contrast failure)." }`
**Token cost:** ~230 tok vs ~920 (4 separate calls)
**Used by:** /design-review DS Compliance Checker, /ds-manage Health Monitor, ds-producer Quality Audit

### 3. `get_node_properties`
**Category:** inspection
**Why:** Full property table for a selected node — fills, strokes, effects, auto-layout settings, constraints, component properties. This is what agents need for /design-review and replaces the Prostar Figma plugin dependency.
**Returns:** `{ fills, strokes, effects, autoLayout, constraints, componentProperties, boundVariables, summary }`
**Token cost:** ~230 tok vs ~700 (execute_figma fallback)
**Used by:** /design-review Visual Quality Inspector, ds-consumer Component Selection, /ds-manage Documentation Generator

### 4. `apply_variables`
**Category:** tokens
**Why:** Agents creating or fixing tokens need to bind variables to node properties. Currently only possible via execute_figma fallback.
**Params:** `{ nodeId, property: "fill" | "stroke" | "effect" | ..., variableName: "color/primary" }`
**Returns:** `{ success, summary: "Variable 'color/primary' bound to fill of 'Button/Primary'" }`
**Token cost:** ~230 tok vs ~700 (execute_figma fallback)
**Used by:** ds-producer Token publishing, /ds-make Token Architect

## Medium Impact

### 5. `diff_versions`
**Category:** components
**Why:** Compare two versions of a component and report what changed — added/removed properties, size changes, style changes. Powers the Version Advisor without manual diffing.
**Params:** `{ nodeIdA, nodeIdB }` or `{ componentName, versionA, versionB }`
**Returns:** `{ added, removed, changed, summary }`
**Used by:** /ds-make Version Advisor, /ds-manage Health Monitor

### 6. `batch_operations`
**Category:** meta
**Why:** Execute N operations in one MCP call. Cascade audits go from N round-trips to 1. Operations execute sequentially server-side; results return as array.
**Params:** `{ operations: [{ op, params }, ...] }`
**Returns:** `{ results: [result1, result2, ...], summary: "3 operations executed. All succeeded." }`
**Used by:** /design-review (full chain), /ds-manage Publisher (cascade QA)

### 7. `export_component_sheet`
**Category:** export
**Why:** Export a component's anatomy as structured spec: property table, variant matrix, slot structure, token bindings. Powers doc generation without reconstructing anatomy from raw nodes.
**Params:** `{ nodeId }` or `{ componentName }`
**Returns:** `{ properties, variants, slots, tokenBindings, summary }`
**Used by:** /ds-manage Documentation Generator, ds-producer Documentation workflow

### 8. `subscribe_selection` (event-based)
**Category:** events
**Why:** Push selection changes to the agent over WebSocket instead of polling. Enables real-time "design companion" mode.
**Protocol:** Requires WebSocket event subscription extension.
**Used by:** Future real-time design assistant mode

## Architecture Suggestion

### Operation Registry Manifest
Currently each operation is a separate TypeScript file discovered via `list_operations`. If PluginOS exposed a `pluginos.registry.json` manifest listing all operations with their schemas, agents could:
- Read it once and cache it (avoid `list_operations` on every session)
- Make smarter operation selection based on schema inspection
- Declare operation categories and dependencies (e.g., "batch these 3 for a full audit")

## Integration Path

These proposals are additive. Design-superpowers agents should:
1. Use existing PluginOS operations where available
2. Fall back to `execute_figma` for anything missing
3. Discover new operations automatically via `list_operations` as they ship

No skill rewrites needed when new operations land.
```

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/pluginos-improvements.md
git commit -m "docs: export PluginOS improvement proposals to standalone file"
```

---

## Summary

| Phase | Tasks | What it does |
|-------|-------|-------------|
| 1 | 1–6 | Branch snapshot + foundation files (schema, loader, adapter, example, maturity rewrite) |
| 2 | 7–8 | Generalize ds-producer and ds-consumer (heaviest rewrites) |
| 3 | 9–14 | Scrub 6 command router SKILL.md files |
| 4 | 15–19 | Scrub shared knowledge files + delete tone-ds-context.md |
| 5 | 20–23 | Scrub project docs (CLAUDE.md, READMEs, archive PROJECT_CONTEXT.md) |
| 6 | 24–28 | Scrub historical plans and specs |
| 7 | 29–30 | Delete tools directory + full repo verification |
| 8 | 31–32 | Finalize tone-example branch with .ds-context.md |
| 9 | 33 | Export PluginOS improvement proposals |

**Total: 33 tasks, ~290 references scrubbed, 5 new files created, 2 files deleted, 1 archived.**
