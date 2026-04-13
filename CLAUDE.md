# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Six universal Claude Code commands for design teams, backed by a 4-layer knowledge system. See spec at `docs/superpowers/specs/2026-04-13-pluginos-integration-and-tone-decoupling.md`.

**Commands:**
- **`/creative`** (`skills/creative/SKILL.md`) — Visual direction, moodboards, palettes, typography, layout systems
- **`/ds-make`** (`skills/ds-make/SKILL.md`) — DS creation and lifecycle: tokens, components, deprecation, versioning
- **`/ds-manage`** (`skills/ds-manage/SKILL.md`) — DS operations: publish cascade, analytics, documentation generation, health monitoring
- **`/design`** (`skills/design/SKILL.md`) — Product design using an existing DS or design language; never creates new components
- **`/design-review`** (`skills/design-review/SKILL.md`) — Evaluate designs against heuristics, a11y, DS compliance, visual quality, motion
- **`/map-design`** (`skills/map-design/SKILL.md`) — Extract design language from any artifact and generate DESIGN.md

**L3 Specializations (Enterprise DS):**
- **DS Producer** (`skills/ds-producer/SKILL.md`) — Delegated to by `/ds-make` at L3 (enterprise DS detected)
- **DS Consumer** (`skills/ds-consumer/SKILL.md`) — Delegated to by `/design` at L3 (enterprise DS detected)

**Knowledge system (4 layers):**
- L1: `skills/shared/knowledge/core-principles.md` — always loaded into every sub-agent
- L2: 13 domain files in `skills/shared/knowledge/` — loaded per sub-agent as needed
- L3: 4 curated CSVs in `skills/shared/data/` — queried on demand via Grep, never pre-loaded
- L4: `DESIGN.md` (project root) / `.ds-context.md` — project-specific context

## Tech Stack

- **Design:** Figma — inspect via configured Figma adapter (see `skills/shared/figma-adapter.md`)
- **Code:** React, ArkUI, Zag.js
- **DS Documentation:** uSpec (`github.com/redongreen/uSpec`)
- **Project management:** Shortcut (tickets, changelogs)
- **Figma plugins:** DS lint (validation), Prostar (property tables)

## File Structure

```
skills/
├── shared/
│   ├── knowledge/
│   │   ├── core-principles.md      # L1 — always loaded
│   │   ├── governance.md           # L2 — DS governance, cascade, versioning
│   │   ├── component-patterns.md   # L2
│   │   ├── token-architecture.md   # L2
│   │   ├── color-theory.md         # L2
│   │   ├── typography.md           # L2
│   │   ├── layout.md               # L2
│   │   ├── motion.md               # L2
│   │   ├── documentation.md        # L2
│   │   ├── design-md-schema.md     # L2
│   │   ├── ux-heuristics.md        # L2
│   │   ├── accessibility.md        # L2
│   │   ├── visual-quality.md       # L2
│   │   └── creative-direction.md   # L2
│   ├── data/
│   │   ├── design-principles.csv         # L3 — queried on demand
│   │   ├── psychological-principles.csv  # L3
│   │   ├── usability-homepage.csv        # L3
│   │   └── ecommerce-usability.csv       # L3
│   ├── maturity-detection.md       # L0–L3 detection helper
│   ├── figma-adapter.md            # Figma adapter detection and tool mapping
│   ├── ds-context-loader.md        # Shared Step 0 context loading procedure
│   ├── ds-context-schema.md        # .ds-context.md field reference
│   └── design-principles.md        # Legacy — IA principles + anti-patterns (retained for ds-producer/ds-consumer compat)
├── creative/SKILL.md               # /creative — 4 sub-agents
├── ds-make/SKILL.md                # /ds-make — 4 sub-agents + L3 delegation to ds-producer
├── ds-manage/SKILL.md              # /ds-manage — 4 sub-agents
├── design/SKILL.md                 # /design — 4 sub-agents + L3 delegation to ds-consumer
├── design-review/SKILL.md          # /design-review — 5 sub-agents
├── map-design/SKILL.md             # /map-design — 4 sub-agents
├── ds-producer/SKILL.md            # L3 Enterprise specialization (delegated from /ds-make)
└── ds-consumer/SKILL.md            # L3 Enterprise specialization (delegated from /design)
docs/superpowers/
├── plans/                          # Implementation plans
└── specs/                          # Architecture specs
```

## Key Architecture Decisions

- Each command is a single SKILL.md acting as a router to inline sub-agent sections
- Commands detect project maturity (L0 Greenfield → L3 Enterprise) before routing; behavior adapts per level
- At L3 (Enterprise DS), /ds-make delegates to ds-producer and /design delegates to ds-consumer — the L3 skills are specializations, not replacements
- L3 CSVs are never pre-loaded; sub-agents query them on demand via Grep when a specific finding needs backing
- /design and ds-consumer NEVER create new components — gaps route to /ds-make
- Publishing follows cascade: Foundations → Components → Patterns → Squad Patterns → Final files; each level must pass QA before the next publishes
- DRY: knowledge lives in `skills/shared/knowledge/`; commands cross-reference, never duplicate

## Interaction Pattern

All commands ask 2-3 questions before non-trivial tasks. Skip when prompt is specific and unambiguous. Team has varying Claude Code experience.

## Reference Resources

| Resource | Used For |
|----------|----------|
| `github.com/murphytrueman/design-system-ops` | DS operations patterns, audit workflows |
| `github.com/nextlevelbuilder/ui-ux-pro-max-skill` | Skill authoring patterns |
| `github.com/redongreen/uSpec` | DS documentation generation |
| `skillscheck.ai` | Skill quality evaluation |
| `impeccable.style` | Design system standards |
| `.ds-context.md` `{{product.docs_url}}` | Product context for DS Consumer (configured per project) |

## Conventions

- All research notes and plans go in `docs/`
- Skills target the entire design team as audience
- Optimize for accuracy, quality, and token efficiency
