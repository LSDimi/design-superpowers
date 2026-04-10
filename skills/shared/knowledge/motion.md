# Motion (L2)

> Loaded by /design-review Motion Reviewer, /creative Layout Strategist. Covers motion purpose, timing standards, easing, physics, performance, and accessibility.

## Motion Purpose Priority

Motion should always serve a clear purpose. Evaluate every animation against this hierarchy. If it serves nothing above P4, remove it.

| Priority | Purpose | Example |
|----------|---------|---------|
| **P1 — Feedback** | Confirms an action occurred | Button press state, form submission success |
| **P2 — Continuity** | Maintains user's sense of context across state changes | Page transition that preserves scroll context, modal that grows from trigger |
| **P3 — Orientation** | Communicates spatial relationships and navigation direction | Slide-in from right = going deeper; slide-out to right = going back |
| **P4 — Delight** | Adds personality after functional needs are met | Micro-interaction on empty state, celebratory confetti on completion |

**Decision rule:** If removing the animation makes the UI harder to understand, it's P1–P3 (keep). If the UI works identically without it, it's P4 (optional — evaluate against Motion dial).

## Timing Standards

Use these named durations as tokens. Never use arbitrary ms values.

| Token | Duration | Use cases |
|-------|----------|-----------|
| `duration-instant` | 0ms | State changes that need to feel immediate (toggle, checkbox) |
| `duration-micro` | 100ms | Hover states, icon swaps, color transitions |
| `duration-small` | 200ms | Dropdown open/close, tooltip appear, focus ring |
| `duration-medium` | 300ms | Modal enter/exit, panel slide, drawer open |
| `duration-large` | 500ms | Page transitions, large content reveals, onboarding steps |

**Rule:** Exits (dismiss, close, hide) use 70–80% of the enter duration. Leaving is faster than arriving — the user already knows what they're dismissing.

## Easing

| Curve | CSS | When to use |
|-------|-----|-------------|
| **Ease-out** | `cubic-bezier(0, 0, 0.2, 1)` | Elements **entering** the screen — fast start, slow end feels natural |
| **Ease-in** | `cubic-bezier(0.4, 0, 1, 1)` | Elements **exiting** — accelerates out; doesn't linger |
| **Ease-in-out** | `cubic-bezier(0.4, 0, 0.2, 1)` | Elements **repositioning** — smooth both ends |
| **Linear** | `linear` | Progress bars, loading indicators — steady state |
| **Spring** | Spring physics (mass/tension/friction) | Natural-feeling interactions — modals, drag-and-drop, gestures |

**Mnemonic:** Enter = ease-out (decelerates into place). Exit = ease-in (accelerates away). Move = ease-in-out. Natural = spring.

## Physics (Spring Motion)

Springs produce motion that feels physical rather than mechanical. Use when an interaction involves user gesture or direct manipulation.

Three parameters:
- **Mass** — how heavy the object feels. Higher mass = slower, more ponderous. Default: 1.
- **Tension (stiffness)** — how strong the spring is. Higher tension = snappier, faster to settle. Default: 170.
- **Friction (damping)** — how quickly oscillation dies. Higher friction = less bounce. Default: 26.

**Spring presets:**
| Preset | Mass | Tension | Friction | Character |
|--------|------|---------|----------|-----------|
| Gentle | 1 | 100 | 26 | Slow, smooth |
| Default | 1 | 170 | 26 | Balanced |
| Wobbly | 1 | 180 | 12 | Bouncy, playful |
| Stiff | 1 | 210 | 20 | Snappy, precise |

Use spring presets from Framer Motion, React Spring, or equivalent library. Never hand-code spring equations.

**When to use spring vs. duration:** If the motion ends at a fixed point → duration + easing. If the motion is driven by user input and could overshoot → spring.

## Performance

**Composited properties only.** Animating anything that triggers layout recalculation kills 60fps.

| Property | Triggers | Safe to animate |
|----------|----------|----------------|
| `transform` (translate, scale, rotate) | Composite only | Yes |
| `opacity` | Composite only | Yes |
| `width`, `height`, `margin`, `padding` | Layout + paint | No — use transform instead |
| `background-color` | Paint only | With caution — avoid on large elements |
| `filter`, `box-shadow` | Paint only | Short durations only; avoid on scroll |

**60fps budget:** Each frame has 16ms. JS + style + layout + paint must fit. Use `will-change: transform` on elements that animate frequently, but sparingly — it allocates a GPU layer.

**Avoid:** animating more than 5 elements simultaneously; staggering long lists (>10 items) with long delays; triggering animations on scroll without debouncing.

## Accessibility

**`prefers-reduced-motion`** — respect it, always.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Do not simply remove motion — some P1/P2 motion (like loading spinners and feedback indicators) should be replaced with an equivalent non-animated signal (text, icon, color change).

**Rules:**
- No infinite animations on visible UI elements — only loading/progress states, and even those should stop when complete.
- No flashing content faster than 3 times per second (WCAG 2.3.1 — seizure prevention).
- Never autoplay motion that lasts >5 seconds without a pause/stop control.
- Parallax effects on scroll must respect `prefers-reduced-motion`.

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| **Decorative-only motion** — animation with no P1–P3 purpose | Slows task completion; distracts | Remove unless Creativity/Motion dials are high AND user feedback supports it |
| **Long durations for common actions** | Every click feels slow; users wait | Keep P1 feedback at ≤200ms; P3 orientation at ≤300ms |
| **Bounce on every interaction** | Playful becomes annoying at high frequency | Reserve spring with overshoot (wobbly) for first-encounter moments only |
| **Simultaneous multi-element entrance** | Visual noise; nothing lands | Stagger by 30–50ms max; cap at 5 staggered elements |
| **Ignoring `prefers-reduced-motion`** | Vestibular disorder users experience nausea | Implement the CSS override; test with macOS Reduce Motion enabled |
