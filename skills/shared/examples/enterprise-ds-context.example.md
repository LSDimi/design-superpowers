# Enterprise .ds-context.md Example

> Copy this to your project root as `.ds-context.md` and replace every `YOUR_*` placeholder with your DS's real values.
> See `${CLAUDE_PLUGIN_ROOT}/skills/shared/ds-context-schema.md` for full field documentation.
>
> This example shows the **enterprise** tier — full governance, cascade publishing, lint gates, dedicated documentation tooling. At this maturity level, `/ds-make` delegates to ds-producer and `/design` delegates to ds-consumer.

```yaml
---
ds:
  name: "Acme DS"
  slug: "acme"
  version: "2.4.0"
  maturity: enterprise
  description: "Acme's design system — foundations, components, patterns, and squad patterns"

figma:
  adapter: pluginos
  status: ready
  libraries:
    - { name: "Acme. Foundations", key: "YOUR_FOUNDATIONS_FILE_KEY", role: "foundations" }
    - { name: "Acme. Components",  key: "YOUR_COMPONENTS_FILE_KEY",  role: "components" }
    - { name: "Acme. Patterns",    key: "YOUR_PATTERNS_FILE_KEY",    role: "patterns" }
    - { name: "Acme. Checklist",   key: "YOUR_CHECKLIST_FILE_KEY",   role: "checklist" }
    - { name: "Acme. Demo Area",   key: "YOUR_DEMO_FILE_KEY",        role: "demo" }

tokens:
  format: figma-variables
  collections: ["primitive", "semantic", "component"]
  export_path: "tokens/"

governance:
  tier: enterprise
  cascade:
    - "Foundations"
    - "Components"
    - "Patterns (L1)"
    - "Squad Patterns (L2)"
    - "Final files"
  lint:
    tool: "Acme Lint"
    command: "npx acme-ds-lint"
  docs:
    tool: custom
    repo: "https://example.com/acme-ds-docs"
  versioning: semver

code:
  framework: react
  component_libs: ["@acme/ui"]
  token_import: "@acme/tokens"

product:
  name: "Acme Platform"
  docs_url: "https://docs.example.com"
  personas:
    - "Business User"
    - "Developer (API integration)"
    - "Admin (platform setup)"
---

## Notes

Use the prose body below the frontmatter for free-form DS context — anything that doesn't fit the schema but a sub-agent might need to know.

### Product Context (optional)

Define the product's key entities and preferred terminology here so `/design` writes copy in your house voice.

- **Entities** — list domain objects your product uses (e.g. "Order", "Customer", "Workflow") with one-line definitions.
- **Terminology** — preferred terms vs. terms to avoid (e.g. "Use `Customer`, not `User`").

### Figma Plugins (optional)

Document any DS-specific Figma plugins beyond PluginOS that sub-agents should know about.

| Plugin | Purpose |
|--------|---------|
| Your lint plugin | Foundation validation, detached-component detection |
| Your docs plugin | Property table / spec generation |
| Library Analytics | Adoption metrics across libraries |
```
