# Maturity Level Detection

> Shared helper referenced by every command SKILL.md. Detects which of 4 project maturity levels applies and adapts behavior accordingly.

## Levels

| Level | Name | Signals |
|-------|------|---------|
| L0 | Greenfield | No DESIGN.md, no .ds-context.md, no Figma library keys in repo |
| L1 | Design Language Defined | DESIGN.md exists at project root; no DS library |
| L2 | Has Design System | .ds-context.md exists with Figma library keys |
| L3 | Enterprise DS | .ds-context.md names Tone OR `enterprise: true` flag present |

## Detection Workflow

1. Check for `DESIGN.md` at project root — `Glob pattern="DESIGN.md"`
2. Check for `.ds-context.md` at project root — `Glob pattern=".ds-context.md"`
3. If `.ds-context.md` exists: Read it and look for `enterprise: true` or `name: Tone`
4. Return the highest matched level

**Tie-break:** `.ds-context.md` always wins over `DESIGN.md` — a project can have both; use the higher level.

## Behavior Adaptation

| Level | /creative | /ds-make | /ds-manage | /design | /design-review | /map-design |
|-------|-----------|----------|------------|---------|----------------|-------------|
| L0 | Full creative freedom; offer to generate DESIGN.md | Scaffold new DS from scratch; require DESIGN.md first | Block — redirect to /ds-make | Block — require DESIGN.md first | Heuristics + a11y only; no DS compliance | Primary use case — extract to bootstrap DESIGN.md |
| L1 | Refine existing DESIGN.md; stay within defined language | Scaffold DS from DESIGN.md tokens | Block — redirect to /ds-make | Compose from DESIGN.md primitives | Heuristics + DESIGN.md conformance checks | Enrich existing DESIGN.md |
| L2 | Refine within DS constraints; propose additions only | Extend existing DS; load .ds-context.md | Full operations available | Full DS-aware composition | All 5 sub-agents active | Extract from DS to refresh DESIGN.md snapshot |
| L3 | Tone-aware; delegate token proposals to /ds-make | Delegate to ds-producer workflows | Full operations + Tone Lint via Figma MCP | Delegate to ds-consumer | All 5 + Tone Lint DS compliance check | Limited; Tone already has full DS |

## Telling the User

Always announce the detected level at the start of any command execution:

> "Detected maturity level: **L2** (project has a design system). Adapting behavior accordingly."

If detection is ambiguous (e.g., `.ds-context.md` exists but has no library keys), default to the lower level and state: "Defaulting to L1 — `.ds-context.md` found but no library keys detected. Run `/ds-make` to configure."

## Project Context Files

- **DESIGN.md** — Human-readable design language definition. Written by /creative and /map-design. Read by /design, /design-review, and /ds-make at L1.
- **.ds-context.md** — Machine-readable DS metadata. Written by /map-design or manually. Keys: `name`, `version`, `figmaLibraryKey`, `enterprise`. For Tone DS, `skills/shared/tone-ds-context.md` serves as the equivalent L3 context file.
