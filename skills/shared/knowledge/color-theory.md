# Color Theory (L2)

> Loaded by /creative Palette Architect, /map-design Token Extractor. Covers palette structure, scale generation, contrast, dark mode, and semantics.

## Palette Structure

Every palette has three layers. Never mix layers — a semantic token should never hold a raw hex.

| Layer | Contents | Examples |
|-------|----------|---------|
| **Neutral scale** | 11 steps, 0–100 (0=white-adjacent, 100=black-adjacent) | `neutral-0` through `neutral-100` |
| **Brand scale** | 9 steps, key hue at step 50 | `brand-10` through `brand-90` |
| **Semantic colors** | Mapped from brand/neutral primitives | `success`, `warning`, `error`, `info` + their foreground/background/border variants |

Minimum viable palette: 1 neutral scale + 1 brand scale + 4 semantic roles. Add secondary brand scales only when UI genuinely requires them.

## Scale Generation

**Preferred: OKLCH**

OKLCH (Lightness, Chroma, Hue) produces perceptually uniform steps — equal numeric lightness steps look equally spaced visually.

```
neutral-0:   oklch(98% 0.005 250)
neutral-10:  oklch(93% 0.008 250)
neutral-20:  oklch(86% 0.010 250)
...
neutral-100: oklch(10% 0.005 250)
```

Lightness step rule: decrease by ~8–9 points per step for neutral; brand scales can use 7–10 depending on hue.

**Fallback: HSL**

If OKLCH is not available, use HSL with manual lightness compensation. Blues and purples appear darker than yellows at the same L value — compensate by bumping L +5 for cool hues at mid-scale steps.

**Scale checkpoints:**
- Steps 10–20: backgrounds, surfaces
- Steps 30–40: borders, dividers
- Steps 50–60: secondary text, placeholder
- Steps 70–80: primary text
- Steps 90–100: darkest — use for headings and high-emphasis only

## Contrast Validation

Always validate after generating a scale. Required pairs to check:

| Use case | Minimum ratio | Target ratio | Standard |
|----------|--------------|--------------|----------|
| Body text on background | 4.5:1 | 7:1 | WCAG 2.1 AA / AAA |
| Large text (≥18px bold / ≥24px regular) | 3:1 | 4.5:1 | WCAG 2.1 AA |
| UI components (borders, icons) | 3:1 | — | WCAG 2.1 AA |
| Decorative / non-informative | No requirement | — | — |

**Verify programmatically.** Do not eyeball. Use the WCAG contrast formula or a tool. Check both light and dark mode.

**Common failure modes:**
- Placeholder text on input backgrounds (often fails 4.5:1)
- Disabled states that are too low-contrast to be perceived at all
- Success/error icons without a text label backup

## Dark Mode

Dark mode is not simply inverted light mode. Follow this approach:

1. **Invert lightness, preserve hue:** If light mode uses `brand-60` for a CTA, dark mode uses `brand-40` (same hue, lower lightness step).
2. **Adjust saturation slightly:** Slightly reduce chroma in dark mode — saturated colors vibrate against dark surfaces. Reduce by ~5–10% chroma.
3. **Semantic tokens swap automatically:** If you built semantic tokens on top of primitives, dark mode is just a second theme that re-maps semantics to different primitive steps. Primitives themselves do not change.
4. **Surfaces stack upward in dark mode:** `surface-0` (darkest) → `surface-1` → `surface-2` (elevated). This is the inverse of light mode convention (light = white, elevated = slightly darker).

| Token | Light value | Dark value |
|-------|------------|-----------|
| `color.bg.default` | `neutral-0` (98% L) | `neutral-95` (12% L) |
| `color.bg.subtle` | `neutral-5` (93% L) | `neutral-90` (18% L) |
| `color.text.default` | `neutral-90` (18% L) | `neutral-5` (93% L) |

## Color Semantics

**Cultural considerations:**
- Red = danger/error in Western contexts; in some East Asian contexts it signals good fortune. For global products, pair semantic color with an icon or label — never rely on hue alone.
- Green = success, go. Yellow/amber = warning. Blue = info/neutral. These are near-universal in product UI and safe defaults.

**Colorblind safety:**
- ~8% of males have red-green deficiency (deuteranopia/protanopia). Never use red and green as the only differentiators.
- Safe pairs: blue + orange, purple + yellow, blue + red.
- Always pair color with shape, pattern, or label for critical status communication.
- Test palettes in a deuteranopia simulator before shipping.

**Brand accent vs. semantic collision check (run whenever a brand hue is chosen):**
- If the brand/accent hue lands near the **error red** (roughly hue 0–20° / 340–360°), the primary CTA and the error state read as the same color — users can't tell "buy" from "something broke." Same risk for a green-ish brand vs. **success green**, or an amber brand vs. **warning**.
- Check the brand hue against all four semantic hues (success/warning/error/info). If any pair is within ~25° of hue at similar chroma/lightness, either shift the brand hue, or shift the semantic hue and re-verify contrast — and always back semantics with an icon/label so the distinction never rests on hue alone.

## Working With Color (craft)

- **Text on a colored surface:** never drop a neutral grey onto color — it looks muddy. Use opacity-reduced white/black so the surface hue bleeds through, or hand-pick a lighter/darker tint of the *background* hue.
- **Tint your greys and shadows** toward a hue (cool blue-grey for tech/corporate, warm for approachable) and tint shadows toward the background, rather than using pure neutral grey / pure-black shadows.
- **Off-black / off-white:** avoid pure #000 and #fff for text/surfaces; slightly tinted near-black and near-white read softer and more premium.
- **Restraint:** one accent color per surface, kept consistent. Tune chroma *to* the lightness rather than assuming a fixed saturation — near mid-lightness a color needs more chroma to read as vivid, while at very high or very low lightness even a little chroma is strongly perceptible (and too much reads garish).
- **Adjust in HSL/OKLCH, not hex** — reasoning about hue/saturation/lightness (or lightness/chroma) is what lets you build coherent scales and states.
- **Elevation via tone (optional):** some systems (e.g. Material 3) express elevation as a tonal tint of the surface using the primary color, not only drop shadows — a useful technique for flat, shadow-light UIs.

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| **Hue-only scale** — single hue, only lightness changes | Looks washed out; insufficient contrast range at mid-steps | Add subtle chroma variation across the scale |
| **Arbitrary lightness jumps** — steps at 0, 15, 47, 80 | Inconsistent visual weight; hard to use systematically | Use a consistent step interval (7–10 points L per step) |
| **Missing semantic roles** — direct use of primitive tokens in components | Can't theme or dark-mode without touching components | Always route through semantic tokens |
| **Too many brand scales** — 3+ primary hues | Palette fights itself; no clear identity | Cap at 2 brand hues (primary + accent); all others are semantic |
| **Contrast assumed, not verified** — choosing colors visually | Passes no accessibility check | Run contrast check on every text/background pair |
