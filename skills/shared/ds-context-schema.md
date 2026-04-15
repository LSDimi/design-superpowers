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
| `figma.adapter` | enum | no | unset | `pluginos`, `figma-mcp`, or unset. See `${CLAUDE_PLUGIN_ROOT}/skills/shared/figma-adapter.md` for detection flow. |
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
