# Minimal .ds-context.md Example

> Copy this to your project root as `.ds-context.md` and fill in your values.
> See `${CLAUDE_PLUGIN_ROOT}/skills/shared/ds-context-schema.md` for full field documentation.

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
