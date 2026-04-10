# design-skills

Six universal Claude Code commands for design teams, backed by a 4-layer knowledge system. Built for the Talon.One design team; adapts from greenfield projects to enterprise design systems.

## What it does

Each command is a router that dispatches to specialized sub-agents based on your request. Every command detects project maturity (L0 Greenfield → L3 Enterprise) before acting, so the same skill works whether you're sketching a new design language or governing a published DS.

| Command | Use for |
|---------|---------|
| `/creative` | Visual direction, moodboards, palettes, typography, layout systems |
| `/ds-make` | Create or evolve DS artifacts — tokens, components, deprecations, versioning |
| `/ds-manage` | Operate the DS — publish cascades, adoption analytics, documentation, health monitoring |
| `/design` | Design product features using an existing DS — component selection, layout composition |
| `/design-review` | Evaluate designs — UX heuristics, WCAG, DS compliance, visual quality, motion |
| `/map-design` | Extract design language from any artifact and generate a `DESIGN.md` |

**L3 specializations** (auto-invoked when Tone DS is detected):
- `ds-producer` — delegated from `/ds-make`
- `ds-consumer` — delegated from `/design`

## Architecture

```
User → /command → Router → Sub-agent (with scoped knowledge)
                              │
                              ├── L1: Core principles (always loaded)
                              ├── L2: Domain references (per sub-agent)
                              ├── L3: CSV lookups (queried on demand)
                              └── L4: Project context (DESIGN.md, .ds-context.md)
```

- **6 commands** → **25 sub-agents** → **14 knowledge files** + **4 curated CSVs**
- Token-efficient: L1 core is ~1K words, loaded once; L2 loaded per sub-agent; L3 never pre-loaded

## Maturity levels

| Level | Signal | Behavior |
|-------|--------|----------|
| **L0** Greenfield | No `DESIGN.md`, no `.ds-context.md` | Full creative freedom; bootstrap via `/creative` → `/map-design` |
| **L1** Design language defined | `DESIGN.md` present | Commands use DESIGN.md as constraint |
| **L2** Has design system | `.ds-context.md` with library keys | Full DS-aware composition and compliance |
| **L3** Enterprise DS | `.ds-context.md` names Tone (or equivalent) | Delegates to ds-producer/ds-consumer; full governance |

Commands announce the detected level at the start of every session.

## Getting started

1. Install as a Claude Code plugin (this repo IS the plugin — point Claude Code at this directory)
2. Run any command in a project directory. The skill will detect your maturity level and ask 2-3 clarifying questions before proceeding
3. For existing design systems, create a `.ds-context.md` at your project root with Figma library keys and token collection names

**Team entry point:** [`skills/README.md`](skills/README.md) — routing matrix, architecture diagram, and a quick reference for designers

## Project layout

```
skills/
├── shared/
│   ├── knowledge/              # L1 core + 13 L2 domain references
│   ├── data/                   # L3 curated CSVs (queried on demand)
│   ├── maturity-detection.md   # How commands detect L0–L3
│   ├── tone-ds-context.md      # L4 Tone-specific context
│   └── design-principles.md    # Legacy, retained for backcompat
├── creative/SKILL.md           # /creative + 4 sub-agents
├── ds-make/SKILL.md            # /ds-make + 4 sub-agents (+ L3 → ds-producer)
├── ds-manage/SKILL.md          # /ds-manage + 4 sub-agents
├── design/SKILL.md             # /design + 4 sub-agents (+ L3 → ds-consumer)
├── design-review/SKILL.md      # /design-review + 5 sub-agents
├── map-design/SKILL.md         # /map-design + 4 sub-agents
├── ds-producer/SKILL.md        # L3 Tone specialization
└── ds-consumer/SKILL.md        # L3 Tone specialization
docs/superpowers/
├── plans/                      # Implementation plans
└── specs/                      # Architecture specs
src/data/                       # Raw CSV source material
tools/                          # Figma plugin integration scripts
```

## Documentation

- **Architecture spec:** [`docs/superpowers/specs/2026-04-09-universal-design-plugin-design.md`](docs/superpowers/specs/2026-04-09-universal-design-plugin-design.md)
- **Implementation plan:** [`docs/superpowers/plans/2026-04-09-universal-design-plugin.md`](docs/superpowers/plans/2026-04-09-universal-design-plugin.md)
- **Project conventions:** [`CLAUDE.md`](CLAUDE.md)

## Built with

- Claude Code skills (Markdown SKILL.md format)
- Figma MCP (`use_figma`) for design context
- Curated knowledge from Dieter Rams, Nielsen heuristics, WCAG 2.1 AA, Baymard usability research, and awesome-design-md conventions

## License

Internal Talon.One project. Not currently licensed for external distribution.
