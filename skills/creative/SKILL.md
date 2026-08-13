---
name: creative
description: Use when exploring visual direction, generating moodboards, proposing color palettes, typography systems, layout strategies, imagery/art direction, refreshing an existing design language, or setting brand-level direction. Activates for /creative, "help me find a visual direction", "propose a palette", "what typography should we use", "moodboard", "font pairing", "grid system", "refresh our look", "rebrand", "art direction".
---

# /creative — Creative Direction

Router for creative-direction sub-agents. Use when no design language exists yet (L0/L1) or when refreshing one (L2/L3).

## Maturity Detection

Follow `${CLAUDE_PLUGIN_ROOT}/skills/shared/maturity-detection.md`. Run detection before routing.

- **L0 (Greenfield):** Full creative freedom — all options open. Output feeds into DESIGN.md via /map-design after exploration.
- **L1 (DESIGN.md exists):** Refine the existing design language. Load DESIGN.md as a constraint. Propose additions that extend it coherently. Refresh requests route to Refresh Strategist; the refresh lands as DESIGN.md updates.
- **L2 (DS exists):** Work within the design system. Respect existing tokens; only propose net-new additions not already covered. Refresh proposals map to token/component migrations executed via /ds-make.
- **L3 (Enterprise DS):** DS-constrained. Delegate any token creation proposals to /ds-make. Restrict to exploration and visual rationale.

Always announce the detected level before proceeding.

## Figma inspection

If a request asks you to look at, refresh, or pull references from a Figma file (e.g. "moodboard from our current file", "explore within our existing screens"), route through `${CLAUDE_PLUGIN_ROOT}/skills/shared/figma-adapter.md`. At L0/L1 the adapter is **always unset** — do not imply a live inspection: either fire the install pitch (`/figma-setup`) or proceed from DESIGN.md / provided images and say which. `/creative`'s core exploration does not require Figma; never block direction work on a missing bridge.

## Always Load

- `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/core-principles.md` (L1 — always)
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/creative-direction.md` (L2 — creative domain)

## Sub-Agent Router

Read the user's request and route to one sub-agent. When the request spans multiple domains, offer to run them in sequence.

| Trigger | Sub-Agent |
|---------|-----------|
| "mood", "theme", "vibe", "direction", "references", "moodboard", "feel", "style", "aesthetic", named styles ("glassmorphism", "neubrutalism", "bento", ...) | Moodboard Generator |
| "palette", "color", "swatch", "hue", "dark mode", "color system" | Palette Architect |
| "type", "font", "typography", "scale", "font pairing", "type system" | Typography Director |
| "layout", "grid", "spacing", "composition", "density", "breakpoint" | Layout Strategist |
| "photography", "imagery", "art direction", "image style", "hero image", "illustration style" | Moodboard Generator (imagery mode — load `art-direction.md`) |
| "refresh", "modernize", "restyle", "update our look", "feels dated", "evolve the design" | Refresh Strategist |
| "brand", "rebrand", "identity", "logo system", "brand architecture", "sub-brand", "positioning" | Brand Architect |

If the request is unclear, ask: "Which aspect do you want to explore — mood/theme, color, typography, layout, imagery, a refresh of what exists, or brand-level direction?" Then route.

## Imagery in deliverables

Whenever a chosen direction implies photography, illustration, or generated imagery (hero art, moodboard tiles, campaign shots), offer the production path from `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/art-direction.md`: generate/edit via available image tooling (ask first, label AI-drafted), or deliver an image brief + SVG/CSS placeholder when no raster tooling is available. Never leave silent gray boxes; never present placeholder imagery as final.

---

## Sub-Agent: Moodboard Generator

**Load additionally:** `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/art-direction.md` when the exploration involves photography, illustration, or imagery direction; `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/brand-design.md` when the brief is brand-level (rebrand, identity). Otherwise none — `creative-direction.md` covers the moodboard method.

**Optional L3 query:** `Grep pattern="<emotion keyword>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/psychological-principles.csv"` for emotional association backing; `Grep pattern="<style name or trait>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/visual-styles.csv"` for named-style recipes and caveats.

### Ask first

Ask **at most 3** (the shared "ask 2–3" contract):

1. What product or project is this for? (one sentence)
2. What feeling do you want, and how far to push it? (2–4 adjectives + a dial — safe / balanced / bold; note density preference airy/balanced/packed if you have one)
3. Any brands, products, or design languages you admire as references? (optional)

### Workflow

1. Confirm or derive a **theme statement** using the `<adjective> + <adjective> + <noun>` template from `creative-direction.md`.
2. Query `style-contexts.csv` with the sector/audience keywords from the design read (`Grep pattern="<sector keyword>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/style-contexts.csv"`) — the matching row names FIT/AVOID style families plus typography and palette direction. Then identify 5–7 reference touchpoints (existing design systems, art movements, industrial design objects, domains with analogous character). Do not use brand names as final answers — extract their underlying traits.
3. Extract 3–5 design traits per reference (e.g., "high contrast ratios", "generous whitespace", "mechanical precision").
4. Synthesize traits into 3 theme variants tuned to the creativity dial: safe, balanced, bold — drawn from *distinct* style families per the Style Library range rule (three intensities of one family is false variety). When the brief or dials suggest a recognizable style family, anchor that variant to it via a `visual-styles.csv` lookup — cite the concrete recipe and carry its when-to-avoid caveat; otherwise keep variants trait-based. Respect the context row's FIT/AVOID lists; name the constraint when it excludes a family.
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
4. Define **semantic colors** — success, warning, error, info. Each gets a mid-range and a surface variant. For every interactive color, define the state derivations: hover, active, focus, and **disabled** (typically reduced chroma + adjusted lightness, never opacity-only on text).
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

**Load additionally:** `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/typography.md`; `${CLAUDE_PLUGIN_ROOT}/skills/shared/font-availability.md` (availability probes + marks)

**Optional L3 query:** `Grep pattern="readab" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/psychological-principles.csv"` for cognitive load references; `Grep pattern="<typography class or context hook>" -i path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/typography-styles.csv"` for ranked, sourced candidates per classification (used by the resolver).

### Ask first

1. What is the primary tone — editorial (expressive), product UI (functional), or technical (dense data)?
2. Is variable font support available, or should we target static weights only?
3. Any existing font already in use that must be respected?

### Workflow

1. Run the availability probes from `font-availability.md` (cache-first; Figma probe only for Figma deliverables). Derive the typography *class* from the theme/context (style-contexts.csv rows and archetypes name classes), then resolve class → concrete fonts via the **Classification Resolver** in `font-availability.md` (typography-styles.csv ranked candidates; first available wins; better-but-absent candidates ship `[needs-install]` with source + license AND a working installed substitute). Recommend the **font pair**: primary (display/headings) + secondary (body/UI), justified against the tone, with a fallback stack; every named font carries its availability mark.
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
Primary: <Font Name> [availability mark] — <Reason>
Secondary: <Font Name> [availability mark] — <Reason>
Fallback stack: ...

### Type Scale (ratio: X.XX, base: 16px)
| Token | Size (px) | Size (rem) | Role | Line Height | Letter Spacing |
...
```

Offer to feed into Layout Strategist or /ds-make Token Architect next.

---

## Sub-Agent: Layout Strategist

**Load additionally:** `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/layout.md`

**Optional L3 query:** `Grep pattern="navigation\|grid\|spacing" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/usability.csv"` for layout usability anchors.

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

---

## Sub-Agent: Refresh Strategist

**Load additionally:** `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/visual-quality.md` (craft tells — what reads dated vs. crafted). At L2/L3 also load `.ds-context.md` per `${CLAUDE_PLUGIN_ROOT}/skills/shared/ds-context-loader.md`.

**Optional L3 query:** `Grep pattern="<style name or trait>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/visual-styles.csv"` — style recipes carry era markers and caveats useful for dating a language and picking its evolution target.

**Maturity behavior:** This sub-agent needs something to refresh. At L0, say so and hand off to Moodboard Generator (nothing exists yet — that's a first-direction task, not a refresh). At L1, the refresh lands as DESIGN.md updates. At L2/L3, every visual change must map to a token/component migration — propose the design moves here, route execution to /ds-make (never restyle ad hoc over a DS).

### Ask first

1. What triggered the refresh — dated look, brand shift, new audience, competitive pressure, or accumulated inconsistency? (the trigger defines success)
2. What must NOT change? (recognized assets, accessibility baselines, platform constraints)
3. How much appetite — polish, evolution, or overhaul?

### Workflow

1. **Inventory the current language.** From DESIGN.md / `.ds-context.md` / Figma (via the adapter — or state you're working from documentation if unset): palette, type, spacing, radius, depth style, motion character, imagery style.
2. **Diagnose, don't redesign yet.** Build a keep / evolve / retire table. For each trait, say *why*: dated marker (e.g. 2016-flat, heavy skeuomorphic gloss, AI-purple), craft failure (inconsistent radii, style-blind shadows), or still strong. Anchor era judgments in `visual-styles.csv` recipes; check "Craft & Anti-Slop Tells" for what reads cheap.
3. **Propose the refresh at three depths**, each with migration cost:
   | Depth | Scope | Typical cost |
   |-------|-------|--------------|
   | Polish | Token values only (colors, radii, shadows, type sizes) — no structural change | Low — token migration, no component API changes |
   | Evolution | Polish + component-level restyling, new depth/motion grammar, imagery redirection | Medium — versioned component updates, cascade republish |
   | Overhaul | New theme statement; palette, type, and layout system rebuilt | High — treat as a new direction: run Moodboard Generator first, then /ds-make |
4. **Recommend one depth** tied to the trigger from Ask-1 and the appetite from Ask-3. State dials + theme statement for the target language.
5. **Bridge to execution:** L1 → updated DESIGN.md sections; L2/L3 → ordered token/component migration list for /ds-make (respect the publish cascade); imagery changes → image briefs per `art-direction.md`.

### Output format

Keep/evolve/retire table + depth recommendation + migration bridge. Every "retire" needs a named reason — no taste-only retirements.

---

## Sub-Agent: Brand Architect

**Load additionally:** `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/brand-design.md` (two-layer brand knowledge: universal principles + named typologies) and `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/art-direction.md` (imagery is a brand asset). `creative-direction.md` (already loaded) provides the theme statement method.

**Optional L3 query:** `Grep pattern="<emotion or association>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/psychological-principles.csv"` for association backing; `Grep pattern="story\|credib\|emotion" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/design-principles.csv"` (SUCCES rows) for message-stickiness backing.

**Maturity behavior:** Brand direction is upstream of product execution at every level. At L2/L3, brand moves that touch tokens/components route to /ds-make; this sub-agent defines the brand layer and its translation contract, never edits the DS directly.

### Ask first

1. What is the brand situation — new brand, rebrand, or organizing multiple products/sub-brands?
2. Who must this brand win over, and what should they feel in three words?
3. Any fixed assets (name, logo, colors) that are non-negotiable?

### Workflow

1. **Layer 1 before Layer 2.** Check the brief against the universal principles in `brand-design.md` (distinctive assets, consistency, promise vs product truth, flexibility with governance, voice-visual alignment) — they outrank any named model. Then **name the philosophy** from its practice-philosophy table (identity/transformation/meaning/simplicity/point-of-view/belief-first). One line, stated up front.
2. **Resolve the architecture** (when multiple offerings exist): branded house (one master brand, descriptive products), house of brands (independent brands), or endorsed hybrid. Decide by audience overlap and reputational risk-sharing, and state the rule for naming the next product.
3. **Write the brand theme statement** (`<adjective> + <adjective> + <noun>`), then derive the association map: what the audience should feel, backed by psychological-principle queries where a claim needs evidence. Pick a primary archetype (max one secondary) from `brand-design.md` and query `style-contexts.csv` for the sector's FIT/AVOID families — the archetype gives the register, the context row grounds it in the market.
4. **Define the brand-to-product translation contract** — how brand assets become UI reality:
   | Brand asset | Product translation |
   |-------------|--------------------|
   | Brand color | Functional palette role (which scale step becomes `brand-600`; where brand color may NOT go — body text, error states) |
   | Brand type | UI type roles (display face for marketing surfaces; workhorse face for product UI; fallback stack) |
   | Logo | Clear-space and minimum-size rules as spacing tokens |
   | Voice/feeling | Motion character (productive vs. expressive registers) + imagery direction (lighting recipe + gaze/agency rules from `art-direction.md`) |
5. **Set the imagery direction**: pick the lighting register and composition rules from `art-direction.md`; write one master image brief as the reference standard.
6. **Hand off:** theme statement + dials → Moodboard Generator or Palette Architect for exploration; token-level changes → /ds-make; document the brand layer in DESIGN.md (L1) or flag for the DS documentation set (L2/L3).

### Output format

Philosophy line → architecture decision (if applicable) → theme statement + association map → translation contract table → master image brief → handoff list. Scannable; no brand-essay prose.
