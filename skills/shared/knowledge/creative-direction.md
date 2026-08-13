# Creative Direction (L2)

> Loaded by /creative sub-agents. Covers configurable dials, moodboard method, theme statements, and translation to tokens.

## Configurable Dials

Four dials shape the output of every creative exploration. Users set them explicitly or implicitly through word choice. Default to the middle value unless cues suggest otherwise.

| Dial | Low | Mid | High | Read from user as |
|------|-----|-----|------|-------------------|
| **Creativity** | Safe — familiar patterns, minimal risk | Balanced | Bold — unconventional, provokes reaction | "clean/professional" → safe; "unexpected/fresh" → bold |
| **Density** | Airy — lots of whitespace, few elements per view | Balanced | Packed — high information density, compact spacing | "breathable/minimal" → airy; "data-rich/dashboard" → packed |
| **Variance** | Uniform — one visual style, tightly consistent | Balanced | Playful — deliberate variation in size, color, texture | "enterprise/serious" → uniform; "expressive/brand-forward" → playful |
| **Motion** | Static — no animation by default | Balanced | Kinetic — motion is a primary communication tool | "accessible/fast" → static; "engaging/dynamic" → kinetic |

**How to apply:** State the dial settings before proposing any direction. Example: "Treating this as: Creativity=Balanced, Density=Packed, Variance=Uniform, Motion=Static."

**Design read first.** Before proposing anything, emit a one-line read of the brief: *page/product kind · audience · vibe words · design-system or aesthetic family*, then the dials. Example: "Reading this as: B2B analytics SaaS for technical buyers, restrained/Linear-style, system=Northstar → Creativity=Safe, Density=Packed, Motion=Static." This makes assumptions inspectable and prevents defaulting to generic AI aesthetics.

**Context overrides aesthetic.** Quiet constraints — accessibility-first, regulated/fintech, trust-critical, kids', wellness — outrank style cues and force the dials (e.g. accessibility-critical → Motion=Static; fintech → no AI-purple; wellness/beauty → don't default to dark mode). Name the constraint when it overrides a stated preference.

## Moodboard Method

A structured approach to extract signal from references before generating anything.

### Step 1 — Gather references (5–7 sources)
Sources can include: existing product UIs, brand identities, physical products, editorial layouts, art movements, architecture. Aim for variety — at least 2 outside the direct category.

### Step 2 — Extract traits (3–5 per reference)
For each reference, name specific observable traits — not vague adjectives. Use:
- **Visual traits:** color temperature, contrast ratio, stroke weight, spatial density
- **Structural traits:** grid type, hierarchy levels, rhythm
- **Emotional traits:** what feeling does it trigger? (max 1–2 per reference)

### Step 3 — Cluster and synthesize
Group traits that appear in ≥2 references. Discard unique traits. The cluster that survives is the design signal.

### Step 4 — Write the theme statement
Synthesize the cluster into a single theme statement (see template below). Everything downstream — palette, type, motion — should be defensible against this statement.

## Theme Statement Template

Format: `<adjective> + <adjective> + <noun>`

- The adjectives describe feeling and character.
- The noun names a world or domain the design inhabits.
- Together they give the design a point of view.

**Examples:**
- `precise, confident, utilitarian` — B2B ops tool
- `warm, layered, editorial` — content-first consumer app
- `sharp, minimal, instrument` — developer tooling
- `playful, structured, workshop` — educational product

**Test:** Can you reject a design decision because it violates this statement? If yes, the statement is strong. If everything passes, it's too vague — tighten it.

## Translation to Tokens

The theme statement drives token decisions. Apply in order:

| Theme dimension | Token category | Decision rule |
|-----------------|---------------|---------------|
| Adjective 1 (character) | Color palette — hue, saturation | "Confident" → higher chroma brand color; "Restrained" → desaturated neutrals |
| Adjective 2 (feeling) | Typography — weight, letter-spacing | "Warm" → humanist sans, looser tracking; "Precise" → geometric, tighter |
| Noun (world) | Spacing rhythm + radius | "Instrument" → tight 4px grid, 0–2px radius; "Workshop" → 8px grid, generous radius |
| Creativity dial | Variance in scale steps | Safe → fewer, closer steps; Bold → wider range, more contrast |
| Motion dial | Duration + easing type | Static → 0ms transitions; Kinetic → spring physics, 200–500ms |

Work through each row before opening color theory or typography files. Anchor every choice to the theme.

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|-------------|--------------|-----|
| **Reference collage** — combining 7 references without synthesis | Produces contradiction, not direction | Complete Step 3 (cluster) before generating anything |
| **Skipping the theme statement** | Decisions lack a shared rationale; reviews become subjective | Always write the statement even if it feels obvious |
| **Overfitting to one reference** | Derivative, not original | Require at least one reference outside the direct category |
| **Dial drift** — changing dials mid-exploration without announcing | Inconsistent output; confuses stakeholders | Restate dials at the start of each new sub-agent call |
| **Adjective inflation** — "modern, clean, bold, friendly, professional" (5+ adjectives) | No point of view | Cap at 3 adjectives; force ranking if there are more |
| **False variety** — three variants that are one style family at different intensities | User believes they explored the option space; they saw one option three times | Draw variants from distinct style families (different depth/typography grammars); check against `style-contexts.csv` FIT lists |

## Style Library — Named Aesthetic Directions

`visual-styles.csv` holds concrete recipes for named style families (Swiss, glassmorphism, neubrutalism, Frutiger Aero, bento grids, brutalist typography, atmospheric gradients, and more) plus photography, illustration, and motion aesthetics. Use it to make creative alternatives *specific* instead of adjectival.

**How to use:**
- When a named style family genuinely fits the dials and brief, anchor that variant to its recipe — a "bold" variant becomes "neubrutalism: 3px borders, hard 4px offset shadows, one acid accent" instead of "more edgy." Don't force a named style onto every exploration; trait-based variants are the default.
- Always carry the style's caveat forward (every recipe has a when-to-avoid — neubrutalism excludes banking, neumorphism fails contrast math, Corporate Memphis reads dated). A named style without its caveat is a trend pitch, not direction.
- **Context still overrides aesthetic.** The style library offers alternatives; it never overrides the quiet constraints (accessibility-first, regulated, trust-critical). Name the constraint when it rules a style out.
- Style recipes are starting points to adapt to the theme statement, not templates to apply verbatim. Mixing depth grammars from two styles on one surface is a craft failure (see `visual-quality.md`).

**Context correlation first.** Before proposing style candidates, grep `style-contexts.csv` with the product's sector/audience keywords (from the design read). Context rows name which style families FIT and which to AVOID, with typography and palette direction and an evidence-confidence note. A traditional pasta brand and a paintball fan page get different candidate sets before taste enters the picture. If the user requests an AVOID-listed style, don't refuse — name the tension and show how to resolve it (or why not to).

**Offer a real range.** When presenting safe/balanced/bold variants, draw them from *distinct* style families — three intensities of one family is false variety. The range should span at least two different depth/typography grammars unless the context rules (Critical rows) constrain the field. When a context row narrows one grammar (e.g. heritage food → serif typography), differentiate the variants on the grammars that remain open — layout system, depth language, imagery register, density — instead of collapsing into one family at three intensities.

**Query patterns:**
- `Grep pattern="<style name or trait>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/visual-styles.csv"`
- `Grep pattern="<sector or audience keyword>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/style-contexts.csv"` (use `-i` — rows carry lowercase keyword tails, but case-insensitive is safer)

## Brand-Level Briefs

When the brief is brand-level (identity, rebrand, brand architecture), load `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/brand-design.md` — universal brand principles (Layer 1) and named typologies (archetypes, architecture types, practice philosophies — Layer 2). State the chosen practice philosophy in one line with the design read; it disciplines every downstream choice.

## L3 Lookup

When you need a deeper reference during evaluation, query these CSVs with Grep:

- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/psychological-principles.csv` — cognitive + perceptual principles
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/usability.csv` — homepage, navigation, forms, commerce, feedback, trust patterns
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/design-principles.csv` — classic design frameworks
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/visual-styles.csv` — named style recipes, photography, illustration, motion aesthetics
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/style-contexts.csv` — industry/audience → style, typography, palette correlations
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/typography-styles.csv` — typography classes → ranked, sourced font candidates (resolver input)

**Query pattern:** `Grep pattern="<keyword>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/<file>.csv"` — use `-i` (case-insensitive) for sector/topic keywords.
**Use sparingly:** Query only when a specific finding needs backing, not speculatively. *Exception:* `style-contexts.csv` is queried once up front during the design read (see Style Library) — there, the context row IS the finding.
