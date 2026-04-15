---
name: creative
description: Use when exploring visual direction, generating moodboards, proposing color palettes, typography systems, or layout strategies for a new or refreshing design language. Activates for commands like /creative, "help me find a visual direction", "propose a palette", "what typography should we use", "what's our design direction", "moodboard", "color scheme", "font pairing", "grid system".
---

# /creative — Creative Direction

Router for creative-direction sub-agents. Use when no design language exists yet (L0/L1) or when refreshing one (L2/L3).

## Maturity Detection

Follow `${CLAUDE_PLUGIN_ROOT}/skills/shared/maturity-detection.md`. Run detection before routing.

- **L0 (Greenfield):** Full creative freedom — all options open. Output feeds into DESIGN.md via /map-design after exploration.
- **L1 (DESIGN.md exists):** Refine the existing design language. Load DESIGN.md as a constraint. Propose additions that extend it coherently.
- **L2 (DS exists):** Work within the design system. Respect existing tokens; only propose net-new additions not already covered.
- **L3 (Enterprise DS):** DS-constrained. Delegate any token creation proposals to /ds-make. Restrict to exploration and visual rationale.

Always announce the detected level before proceeding.

## Always Load

- `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/core-principles.md` (L1 — always)
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/creative-direction.md` (L2 — creative domain)

## Sub-Agent Router

Read the user's request and route to one sub-agent. When the request spans multiple domains, offer to run them in sequence.

| Trigger | Sub-Agent |
|---------|-----------|
| "mood", "theme", "vibe", "direction", "references", "moodboard", "feel" | Moodboard Generator |
| "palette", "color", "swatch", "hue", "dark mode", "color system" | Palette Architect |
| "type", "font", "typography", "scale", "font pairing", "type system" | Typography Director |
| "layout", "grid", "spacing", "composition", "density", "breakpoint" | Layout Strategist |

If the request is unclear, ask: "Which aspect do you want to explore — mood/theme, color, typography, or layout?" Then route.

---

## Sub-Agent: Moodboard Generator

**Load additionally:** None — `creative-direction.md` already covers the moodboard method.

**Optional L3 query:** `Grep pattern="<emotion keyword>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/psychological-principles.csv"` for emotional association backing.

### Ask first

1. What product or project is this for? (one sentence)
2. What adjectives describe the feeling you want? (2–4 words)
3. Any brands, products, or design languages you admire as references? (optional)
4. Dials: creativity (safe / balanced / bold), density (airy / balanced / packed)?

### Workflow

1. Confirm or derive a **theme statement** using the `<adjective> + <adjective> + <noun>` template from `creative-direction.md`.
2. Identify 5–7 reference touchpoints (existing design systems, art movements, industrial design objects, domains with analogous character). Do not use brand names as final answers — extract their underlying traits.
3. Extract 3–5 design traits per reference (e.g., "high contrast ratios", "generous whitespace", "mechanical precision").
4. Synthesize traits into 3 theme variants tuned to the creativity dial: safe, balanced, bold. Each variant = one theme statement + 4–5 trait bullets.
5. Present as a table:

| Variant | Theme Statement | Key Traits | Best For |
|---------|----------------|------------|----------|
| Safe | ... | ... | ... |
| Balanced | ... | ... | ... |
| Bold | ... | ... | ... |

6. Ask the user to pick a variant or iterate. Offer to move to Palette Architect or Typography Director next.

### Output format

Theme table + next-step prompt. No narrative paragraphs. Keep the table scannable.

---

## Sub-Agent: Palette Architect

**Load additionally:** `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/color-theory.md`

**Optional L3 query:** `Grep pattern="color" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/psychological-principles.csv"` for color-psychology backing on key choices.

### Ask first

1. Do you have a base hue in mind, or should I derive it from the theme statement?
2. Does this need a dark mode variant?
3. Any existing brand colors to anchor (hex values)?

### Workflow

1. Establish the anchor hue (from user input or derived from theme statement adjectives via `creative-direction.md` translation rules).
2. Generate the **neutral scale** — 11 steps using OKLCH (preferred) or HSL fallback. Step lightness by ~8–9% increments. Name: `neutral-50` through `neutral-950`.
3. Generate the **brand/primary scale** — 9 steps. Name: `brand-100` through `brand-900`.
4. Define **semantic colors** — success, warning, error, info. Each gets a mid-range and a surface variant.
5. Validate all foreground/background pairs against WCAG contrast ratios (4.5:1 text, 3:1 UI).
6. If dark mode requested: invert lightness mapping, preserve hue, adjust saturation for perceived balance.
7. Check for colorblind safety on the semantic palette (no red/green-only distinction).
8. Output as a table with hex + OKLCH values + WCAG pass/fail per pair.

### Output format

```
## Palette — <Theme Statement>

### Neutral Scale
| Token | Hex | OKLCH |
|-------|-----|-------|
...

### Brand Scale
...

### Semantic
| Role | Light | Dark | WCAG (text) |
...
```

Offer to hand off to Typography Director or token-naming via /ds-make.

---

## Sub-Agent: Typography Director

**Load additionally:** `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/typography.md`

**Optional L3 query:** `Grep pattern="readab" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/psychological-principles.csv"` for cognitive load references.

### Ask first

1. What is the primary tone — editorial (expressive), product UI (functional), or technical (dense data)?
2. Is variable font support available, or should we target static weights only?
3. Any existing font already in use that must be respected?

### Workflow

1. Recommend a **font pair**: primary (display/headings) + secondary (body/UI). Justify each choice against the tone. Provide a fallback stack.
2. Select a **modular scale ratio** from `typography.md` based on density dial: 1.125 (tight/product), 1.2 (balanced), 1.25 (editorial), 1.333 (expressive). Base: 16px.
3. Generate the **type scale** — 7 steps: `xs`, `sm`, `base`, `md`, `lg`, `xl`, `2xl`. Calculate size in px and rem. Map each to a semantic role (caption, body, label, heading-sm, heading-md, heading-lg, display).
4. Define **line height** per role: 1.4–1.6 for body, 1.1–1.3 for headings.
5. Define **letter spacing** per role: 0 for body, +0.5–1% for small labels, -0.5–1% for large display.
6. Flag any anti-patterns from `typography.md` triggered by the choices.
7. Output as a spec table.

### Output format

```
## Type System — <Theme Statement>

### Font Pair
Primary: <Font Name> — <Reason>
Secondary: <Font Name> — <Reason>
Fallback stack: ...

### Type Scale (ratio: X.XX, base: 16px)
| Token | Size (px) | Size (rem) | Role | Line Height | Letter Spacing |
...
```

Offer to feed into Layout Strategist or /ds-make Token Architect next.

---

## Sub-Agent: Layout Strategist

**Load additionally:** `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/layout.md`

**Optional L3 query:** `Grep pattern="navigation\|grid\|spacing" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/usability-homepage.csv"` for layout usability anchors.

### Ask first

1. What is the primary UI pattern — dashboard, content/reading, form-heavy, or marketing/landing?
2. Density preference (compact / default / comfortable)?
3. Mobile-first or desktop-first? Primary breakpoints needed?

### Workflow

1. Select the **grid system** from `layout.md` — 12-col for product UI (default), 8-col for dense data, fluid for marketing. Justify the choice.
2. Establish the **spacing base unit** (4px for dense UI, 8px standard) and generate the t-shirt scale: `xs`=4, `sm`=8, `md`=16, `lg`=24, `xl`=32, `2xl`=48, `3xl`=64.
3. Define **inset / stack / inline** spacing patterns with token references.
4. Define **breakpoints** — mobile-first unless otherwise specified: `sm`=480, `md`=768, `lg`=1024, `xl`=1280, `2xl`=1440.
5. Propose **density mode** parameterization — compact (0.75× base), default (1×), comfortable (1.25×).
6. Recommend the primary **composition pattern** matching the UI type (sidebar+main, card grid, list-detail, split-view, master-detail).
7. Flag anti-patterns from `layout.md` to avoid.

### Output format

```
## Layout System — <UI Type>

Grid: <type>, <columns>, <gutter>
Base unit: <value>px

### Spacing Scale
| Token | Value (px) | Use |
...

### Breakpoints
| Name | px | Notes |
...

### Density Modes
Compact: ...  Default: ...  Comfortable: ...

### Recommended Composition
<Pattern name> — <one-line rationale>
```

Offer to generate DESIGN.md via /map-design, or proceed to /ds-make for token scaffolding.
