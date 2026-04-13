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
