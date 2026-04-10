# Universal Design Plugin — Design Specification

> Approved 2026-04-09. This spec covers the architecture for a universal Claude Code design plugin with 6 commands, ~20 sub-agents, and a 4-layer knowledge system.

## Goal

Build a universal design intelligence plugin that handles 4 maturity levels — new projects (no DS), existing without DS, enterprise DS management (Tone as reference implementation), and crawl-and-build — through 6 top-level commands routed to specialized sub-agents.

## Architecture Overview

```
User → /command → Router → Sub-agent (with scoped knowledge)
                              ↓
                    4-Layer Knowledge System
                    ├── L1: Core Principles (~50, always loaded)
                    ├── L2: Domain References (per sub-agent)
                    ├── L3: CSV Lookup (queried on demand)
                    └── L4: Project Context (DESIGN.md, .ds-context.md)
```

## 6 Commands → Sub-Agent Map

### `/creative` — Ideation & Creative Direction
| Sub-agent | Purpose | Knowledge Layers |
|-----------|---------|-----------------|
| Moodboard Generator | Visual theme exploration, reference collection | L1 + L2:creative-direction + L3:psychological |
| Palette Architect | Color system creation, contrast validation | L1 + L2:color-theory + L3:psychological |
| Typography Director | Type system design, scale generation | L1 + L2:typography + L3:psychological |
| Layout Strategist | Grid systems, spatial relationships | L1 + L2:layout + L3:usability-homepage |

### `/ds-make` — DS Component Lifecycle
| Sub-agent | Purpose | Knowledge Layers |
|-----------|---------|-----------------|
| Token Architect | Token creation, naming, tier assignment | L1 + L2:token-architecture + L4:project |
| Component Builder | Component creation, variant matrix, API design | L1 + L2:component-patterns + L4:project |
| Deprecation Planner | Usage analysis, migration planning, removal | L1 + L2:governance + L4:project |
| Version Advisor | Semver decisions, changelog, breaking change detection | L1 + L2:governance + L4:project |

### `/ds-manage` — DS Operations & Governance
| Sub-agent | Purpose | Knowledge Layers |
|-----------|---------|-----------------|
| Publisher | Cascade pipeline execution, QA gates | L1 + L2:governance + L4:project |
| Analytics Reporter | Adoption metrics, usage trends, Monday reports | L1 + L4:project |
| Documentation Generator | uSpec generation, property tables, demo areas | L1 + L2:documentation + L4:project |
| Health Monitor | Library drift, legacy detection, consistency checks | L1 + L2:governance + L4:project |

### `/design` — Product Design with DS
| Sub-agent | Purpose | Knowledge Layers |
|-----------|---------|-----------------|
| Component Selector | Best-fit component recommendation | L1 + L2:component-patterns + L3:usability + L4:project |
| Layout Composer | Page/flow composition from DS patterns | L1 + L2:layout + L3:usability-homepage + L4:project |
| Pattern Matcher | Find existing patterns matching a need | L1 + L2:component-patterns + L4:project |
| Gap Detector | Identify missing DS coverage, draft requests | L1 + L2:governance + L4:project |

### `/design-review` — Design Validation
| Sub-agent | Purpose | Knowledge Layers |
|-----------|---------|-----------------|
| UX Critic | Heuristic evaluation, cognitive load, IA review | L1 + L2:ux-heuristics + L3:psychological + L3:usability |
| A11y Auditor | WCAG compliance, keyboard, screen reader, contrast | L1 + L2:accessibility |
| DS Compliance Checker | Token binding, override detection, detached components | L1 + L2:governance + L4:project |
| Visual Quality Inspector | Alignment, spacing consistency, visual rhythm | L1 + L2:visual-quality + L3:usability-homepage |
| Motion Reviewer | Animation purpose, timing, physics, performance | L1 + L2:motion + L3:psychological |

### `/map-design` — Design Extraction & Translation
| Sub-agent | Purpose | Knowledge Layers |
|-----------|---------|-----------------|
| Visual Parser | Screenshot/URL reading, element identification | L1 + L2:visual-quality |
| Token Extractor | Color, type, spacing extraction from designs | L1 + L2:token-architecture |
| Component Cataloger | Component identification, hierarchy mapping | L1 + L2:component-patterns |
| DESIGN.md Generator | 9-section DESIGN.md output | L1 + L2:design-md-schema |

## 4-Layer Knowledge System

### L1: Core Principles (~50, always loaded in every sub-agent)
Curated from the 53-row Design Principles CSV. Filtered to universal principles that apply regardless of domain. Loaded as a compact markdown section in every sub-agent's system prompt.

**Source:** `Design Principles, Performance Attributes, and Strategy Tenets Reference Table - Table 1.csv`
**Target:** `skills/shared/knowledge/core-principles.md` (~50 principles, <2K tokens)

### L2: Domain Reference Files (loaded per sub-agent)
10 focused reference files, each ~30 guidelines. Sub-agents load only the files they need.

| File | Content | Used By |
|------|---------|---------|
| `creative-direction.md` | Moodboard techniques, style exploration, configurable dials (creativity/density/variance/motion) | /creative agents |
| `color-theory.md` | Color systems, contrast ratios, palette generation, dark mode | Palette Architect |
| `typography.md` | Type scales, font pairing, readability, hierarchy | Typography Director |
| `layout.md` | Grid systems, spacing, responsive patterns, density | Layout Strategist, Layout Composer |
| `token-architecture.md` | 3-tier tokens, naming conventions, collection structure | Token Architect, Token Extractor |
| `component-patterns.md` | Component API design, variant strategies, composition patterns | Component Builder, Component Selector, Pattern Matcher, Component Cataloger |
| `governance.md` | Contribution process, versioning, deprecation, publishing cascade, consumption rules | /ds-make, /ds-manage agents |
| `ux-heuristics.md` | Nielsen's 10 + severity rating + cognitive load framework | UX Critic |
| `accessibility.md` | WCAG 2.1 AA checklist, keyboard patterns, ARIA, contrast | A11y Auditor |
| `motion.md` | Motion principles (Adobe Spectrum, Microsoft Fluent), timing, easing | Motion Reviewer |
| `visual-quality.md` | Alignment, spacing rhythm, visual balance, anti-patterns | Visual Quality Inspector, Visual Parser |
| `documentation.md` | uSpec templates, property table format, demo area structure | Documentation Generator |
| `design-md-schema.md` | 9-section DESIGN.md format (from awesome-design-md) | DESIGN.md Generator |

### L3: CSV Lookup (queried on demand, not pre-loaded)
Sub-agents query these when they need specific principles for a review finding or recommendation.

| File | Rows | Query Pattern |
|------|------|--------------|
| `psychological-principles.csv` | 100 | By category (vision, cognition, memory, motivation) |
| `usability-homepage.csv` | 79 | By area (homepage, navigation, categories, filtering) |
| `ecommerce-usability.csv` | 93 | By topic (forms, search, checkout, touch) |
| `design-principles.csv` | 53 | By framework (Dieter Rams, SOLID, Universal Design) |

### L4: Project Context (persisted per-project)
- `DESIGN.md` — 9-section design language definition (created by /map-design, consumed by all)
- `.ds-context.md` — DS-specific context (Figma file keys, token collections, library names)
- Detected via "teach" pattern: one-time exploration that interviews user and reads codebase

## File Structure (Target)

```
skills/
├── shared/
│   ├── knowledge/
│   │   ├── core-principles.md          # L1: ~50 always-loaded principles
│   │   ├── creative-direction.md       # L2: creative domain
│   │   ├── color-theory.md             # L2: color domain
│   │   ├── typography.md               # L2: typography domain
│   │   ├── layout.md                   # L2: layout domain
│   │   ├── token-architecture.md       # L2: token domain
│   │   ├── component-patterns.md       # L2: component domain
│   │   ├── governance.md               # L2: governance domain
│   │   ├── ux-heuristics.md            # L2: UX evaluation
│   │   ├── accessibility.md            # L2: a11y domain
│   │   ├── motion.md                   # L2: motion domain
│   │   ├── visual-quality.md           # L2: visual quality
│   │   ├── documentation.md            # L2: documentation domain
│   │   └── design-md-schema.md         # L2: DESIGN.md format
│   ├── data/                           # L3: CSV lookup files (curated)
│   │   ├── psychological-principles.csv
│   │   ├── usability-homepage.csv
│   │   ├── ecommerce-usability.csv
│   │   └── design-principles.csv
│   ├── tone-ds-context.md              # L4: Tone-specific (existing)
│   └── design-principles.md            # Legacy (to be refactored into knowledge/)
├── creative/
│   └── SKILL.md                        # /creative router + 4 sub-agents
├── ds-make/
│   └── SKILL.md                        # /ds-make router + 4 sub-agents
├── ds-manage/
│   └── SKILL.md                        # /ds-manage router + 4 sub-agents
├── design/
│   └── SKILL.md                        # /design router + 4 sub-agents
├── design-review/
│   └── SKILL.md                        # /design-review router + 5 sub-agents
├── map-design/
│   └── SKILL.md                        # /map-design router + 4 sub-agents
├── ds-producer/
│   └── SKILL.md                        # Existing (to be refactored)
└── ds-consumer/
    └── SKILL.md                        # Existing (to be refactored)
```

## Maturity Level Detection

Each command adapts behavior based on detected project maturity:

| Level | Detection Signal | Behavior |
|-------|-----------------|----------|
| L0: No DS | No DESIGN.md, no .ds-context.md, no Figma libraries | Full creative freedom, generate DESIGN.md |
| L1: Has DESIGN.md | DESIGN.md exists but no DS library | Use DESIGN.md as constraint, suggest DS creation |
| L2: Has DS | .ds-context.md exists, Figma library keys present | Full DS-aware mode, enforce consumption rules |
| L3: Enterprise | Tone-specific context detected | Full Tone governance, lint integration, cascade publishing |

## Sub-Agent Skill Structure

Each sub-agent SKILL.md follows this pattern:

```markdown
---
name: <sub-agent-name>
description: <when to activate>
---

# <Sub-Agent Name>

**Knowledge:** Load `skills/shared/knowledge/core-principles.md` (always).
Load `skills/shared/knowledge/<domain>.md` (domain-specific).

**Maturity awareness:** Check for DESIGN.md and .ds-context.md.
Adapt behavior per maturity level.

## Workflows
<numbered workflows with steps>

## Token Efficiency
<output format constraints>
```

## Relationship to Existing Skills

The existing `ds-producer` and `ds-consumer` skills become the L3 (Enterprise/Tone) specializations:
- `/ds-make` at L3 delegates to ds-producer workflows
- `/design` at L3 delegates to ds-consumer workflows
- At L0-L2, these commands use their universal sub-agents directly

## Key Design Decisions

1. **Sub-agents are prompt sections, not separate files** — each SKILL.md contains its sub-agent definitions inline to avoid file proliferation. The router section at the top dispatches to the right sub-agent section.
2. **L1 core principles are always loaded** — ~2K tokens is acceptable overhead for universal grounding.
3. **L3 CSVs are never pre-loaded** — sub-agents reference them by path and query on demand using Read tool with grep/search patterns.
4. **L4 project context uses "teach" pattern** — first invocation explores and interviews, subsequent invocations read persisted files.
5. **Tone DS is L3 reference implementation** — not hardcoded, detected via .ds-context.md content.
