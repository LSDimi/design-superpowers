# Typography (L2)

> Loaded by /creative Typography Director, /map-design Token Extractor. Covers type scale generation, font pairing, readability, hierarchy, and responsive type.

## Type Scale Generation

A type scale uses a modular ratio — each step is the previous multiplied by the ratio. Pick the ratio based on density need.

| Ratio | Name | Best for | Steps from 16px base |
|-------|------|----------|----------------------|
| **1.125** | Major Second | Dense UIs, data tables, compact dashboards | 11, 12, 14, 16, 18, 20, 23, 26 |
| **1.2** | Minor Third | General product UI | 11, 13, 16, 19, 23, 28, 33 |
| **1.25** | Major Third | Marketing, editorial-leaning product | 10, 13, 16, 20, 25, 31, 39 |
| **1.333** | Perfect Fourth | Landing pages, editorial, high visual hierarchy | 9, 12, 16, 21, 28, 37, 50 |

**Scale roles — map to semantic names, not pixel sizes:**

| Role | Typical size (1.25 ratio, 16px base) | Usage |
|------|--------------------------------------|-------|
| `text-xs` | 10px | Labels, captions, metadata |
| `text-sm` | 13px | Secondary body, helper text |
| `text-base` | 16px | Primary body copy |
| `text-lg` | 20px | Large body, card intros |
| `text-xl` | 25px | Section headings (h3) |
| `text-2xl` | 31px | Page headings (h2) |
| `text-3xl` | 39px | Display headings (h1) |

Never expose pixel values in components. Reference semantic tokens only.

## Font Pairing

**Pairing principles:**
- Maximum 2 typefaces in product UI (display + body). A third face is decorative-only and rare.
- Contrast on axis: pair a geometric sans with a humanist sans, or a serif with a sans — not two similar styles.
- Variable fonts preferred: single file, weight + optical size axes reduce load and tokens.

| Pairing type | Display | Body | Character |
|-------------|---------|------|-----------|
| Technical / precise | Geist, Inter | Inter, DM Sans | Developer tools, B2B |
| Editorial / warm | Playfair Display | Source Serif 4 | Content, publishing |
| Brand-forward | Custom / display face | System sans | Consumer, marketing |
| Neutral / system | System UI | System UI | Performance-first, utility |

**Fallback stacks:**
```
Sans: Inter, "Helvetica Neue", Arial, sans-serif
Serif: "Georgia", "Times New Roman", serif
Mono: "JetBrains Mono", "Fira Code", Consolas, monospace
System: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
```

## Readability

**Line length:** 45–75 characters per line for body text. Wider than 75ch causes eye fatigue tracking line starts. Narrower than 45ch causes choppy reading rhythm.
- Apply via `max-width: 65ch` on prose containers.
- Tables, forms, and data views are exempt — measure based on content.

**Line height:**
| Context | Line height | Reason |
|---------|------------|--------|
| Body text (14–18px) | 1.5–1.6 | Reading comfort, adequate leading |
| Small text (<14px) | 1.4–1.5 | Tighter at small sizes avoids gaps |
| Headings (≥24px) | 1.1–1.3 | Large type needs less leading |
| Display (≥40px) | 1.0–1.1 | Tightest — decorative, not read in paragraphs |

**Letter spacing:**
- Body: 0 to +0.01em (default tracking is usually correct)
- All-caps labels: +0.05em to +0.1em — all-caps text requires loose tracking to read
- Display headings: -0.01em to -0.02em for geometric/display faces

## Hierarchy

Three levers — use all three, not just size:

| Lever | Strong | Weak | Note |
|-------|--------|------|------|
| **Size** | 2–3 clear tiers visible at a glance | One size for everything | Use scale roles, not arbitrary px |
| **Weight** | Bold (600–700) vs. regular (400) for contrast | Semibold (500) everywhere | Avoid weights 100–300 for UI text |
| **Color** | High-contrast primary, mid-contrast secondary, low-contrast tertiary | Same color for all text | Map to semantic tokens: `text-primary`, `text-secondary`, `text-tertiary` |

Rule: **never use size alone to establish hierarchy.** A large, low-weight, low-contrast heading will not read as heading. Combine at least two levers.

## Responsive Type

**Fluid type with `clamp()`:**

```css
/* Syntax: clamp(min, preferred, max) */
font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
```

- `min`: smallest readable size at narrowest viewport
- `preferred`: scales linearly with viewport width
- `max`: caps growth at wide viewports

**Breakpoint-based approach (simpler):**

```css
/* Mobile first */
font-size: var(--text-base);        /* 16px */
@media (min-width: 768px) {
  font-size: var(--text-lg);        /* 20px */
}
```

Use `clamp()` for display headings where smooth scaling matters most. Use breakpoints for body/UI text where precise control is needed.

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| **More than 7 type sizes** | Hierarchy becomes noise; no clear tiers | Audit and merge — group similar sizes into one role |
| **Weights below 400 in UI** | Thin strokes fail contrast at small sizes; inaccessible | Min weight 400 for all functional text; 500+ preferred for small labels |
| **Decorative fonts for body copy** | Legibility fails at paragraph length; not accessible | Decorative faces for 1–3 word display only; body always uses readable face |
| **Pixel-locked type** | Ignores user browser font size preferences | Use `rem` units based on 16px root; never `px` for font-size |
| **Missing fallback stack** | Flash of unstyled text; broken layout before font loads | Always declare 3-level fallback: custom → generic → system |
| **All-caps body text** | Slows reading speed by ~14%; fails readability | Reserve all-caps for labels ≤3 words and UI chrome only |
