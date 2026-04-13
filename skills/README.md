# Design Superpowers — Team Entry Point

Six Claude Code commands for design teams. Each command is a router that dispatches to inline sub-agents based on your request. All commands adapt to your project's maturity level before acting.

---

## Commands

| Command | What it does |
|---------|-------------|
| `/creative` | Explore visual direction — moodboards, color palettes, typography systems, layout strategies |
| `/ds-make` | Create or evolve design system artifacts — tokens, components, deprecations, version bumps |
| `/ds-manage` | Operate the DS — publish cascades, adoption analytics, documentation generation, health audits |
| `/design` | Design product features using an existing DS or design language — component selection, layout composition, gap detection |
| `/design-review` | Evaluate designs — UX heuristics, WCAG accessibility, DS compliance, visual quality, motion |
| `/map-design` | Extract design language from any artifact (screenshot, Figma, URL) and generate a `DESIGN.md` |

**L3 Enterprise specializations** (invoked automatically at L3 — not called directly):

| Skill | Delegated from |
|-------|---------------|
| `ds-producer` | `/ds-make` when enterprise DS is detected |
| `ds-consumer` | `/design` when enterprise DS is detected |

---

## Routing Matrix

| If you say... | Command |
|---------------|---------|
| "help me find a visual direction", "propose a palette", "what typography should we use" | `/creative` |
| "new component", "add token", "bump version", "deprecate X", "scaffold a design system" | `/ds-make` |
| "publish", "adoption report", "generate docs", "check health", "library drift" | `/ds-manage` |
| "design a feature", "which component should I use", "compose this page", "is there a pattern for" | `/design` |
| "review this design", "audit UI", "check accessibility", "WCAG check", "does this follow our DS" | `/design-review` |
| "extract tokens", "generate DESIGN.md", "crawl this design", "reverse-engineer this UI" | `/map-design` |

---

## Knowledge Architecture

```
┌─────────────────────────────────────────────────────────┐
│  L1 — Core Principles (always loaded)                   │
│  skills/shared/knowledge/core-principles.md             │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│  L2 — Domain Knowledge (loaded per sub-agent)           │
│  skills/shared/knowledge/                               │
│  governance · component-patterns · token-architecture   │
│  color-theory · typography · layout · motion            │
│  ux-heuristics · accessibility · visual-quality         │
│  documentation · design-md-schema · creative-direction  │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│  L3 — CSV Lookups (queried on demand, never pre-loaded) │
│  skills/shared/data/                                    │
│  design-principles.csv · psychological-principles.csv   │
│  usability-homepage.csv · ecommerce-usability.csv       │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│  L4 — Project Context (persisted, per-project)          │
│  DESIGN.md (root) · .ds-context.md                     │
└─────────────────────────────────────────────────────────┘
```

---

## Maturity Levels

Every command detects your project's maturity before acting:

| Level | Name | Signal | Effect |
|-------|------|--------|--------|
| L0 | Greenfield | No `DESIGN.md`, no `.ds-context.md` | Full freedom; `/creative` → `/map-design` to bootstrap |
| L1 | Design language defined | `DESIGN.md` exists | Commands use DESIGN.md as constraint |
| L2 | Has design system | `.ds-context.md` with Figma library keys | Full DS-aware behavior |
| L3 | Enterprise DS | `.ds-context.md` with `ds.maturity: enterprise` | `/ds-make` → ds-producer; `/design` → ds-consumer |

Commands announce the detected level at the start of every session: "Detected maturity level: L2. Adapting behavior accordingly."

---

## Plans and Specs

- **Implementation plan:** `docs/superpowers/plans/2026-04-09-universal-design-plugin.md`
- **Architecture spec:** `docs/superpowers/specs/2026-04-09-universal-design-plugin-design.md`
- **Project overview:** `CLAUDE.md` (repo root)

## MCP Integrations

| MCP | Status | Purpose |
|-----|--------|---------|
| Figma MCP | Connected | Component inspection, screenshots, design context |
| Shortcut MCP | Needs setup | Ticket lifecycle, changelogs, comments |

## Figma Plugins

| Plugin | Purpose |
|--------|---------|
| DS lint (configurable via `{{governance.lint.tool}}`) | Foundation validation, detached component detection |
| Prostar | Property table generation in Demo area |
