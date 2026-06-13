# Failure Gallery

Real patterns that cause bad renders, with exact fixes.
Each entry: symptom → root cause → copy-paste fix.

---

## F-01: Text Overlaps Formula

**Symptom:** Label text runs into a MathTex equation.

**Root cause:** `.next_to()` called without `buff`, or both placed at ORIGIN.

**Before (broken):**
```python
formula = MathTex(r"f'(x) = 2x").move_to(ORIGIN)
label = Text("Derivative").move_to(ORIGIN + DOWN)
# DOWN with no buff → overlaps at y≈0
```

**After (fixed):**
```python
formula = MathTex(r"f'(x) = 2x", font_size=48).move_to(UP * 0.4)
label = Text("Derivative", font_size=34, color=PALETTE["dim"])
label.next_to(formula, DOWN, buff=0.5)  # explicit buff
```

**Rule:** Always use `.next_to(obj, direction, buff=0.4)` minimum. Never manually calculate position when relative placement is intended.

---

## F-02: Object Clipped at Edge

**Symptom:** Part of a graph, equation, or arrow is cut off at screen boundary.

**Root cause:** Object placed at absolute coordinate without checking frame limits, or axes too wide.

**Before (broken):**
```python
axes = Axes(x_range=[-5, 5], x_length=14)  # 14 units = full frame width, no margin
axes.move_to(ORIGIN)
```

**After (fixed):**
```python
axes = Axes(x_range=[-5, 5], x_length=11)  # 11 / 14.2 = 77% of frame
axes.move_to(ORIGIN)
```

**Rule:** x_length should not exceed 11. y_length should not exceed 5.5. Always check against SAFE bounds.

---

## F-03: LaTeX Rendering Failure

**Symptom:** Manim throws LaTeX error; black screen or exception.

**Root cause 1:** Unescaped backslash in a regular string.
```python
# BROKEN — f-string eats the backslash
formula = MathTex(f"\frac{a}{b}")
```
```python
# FIXED — raw string
formula = MathTex(r"\frac{a}{b}")
```

**Root cause 2:** Curly braces conflict with Python f-string syntax.
```python
# BROKEN
formula = MathTex(f"\frac{{a}}{{b}}")  # double brace confusion
```
```python
# FIXED — never use f-strings inside MathTex; build string separately
numerator = "a"
denominator = "b"
formula = MathTex(r"\frac{" + numerator + r"}{" + denominator + r"}")
```

**Root cause 3:** Missing LaTeX package (e.g., `\mathbb`, `\therefore`).
Fix: Use standard LaTeX only. Avoid `\mathbb`, `\mathcal` unless you've verified the LaTeX installation has the required package.

---

## F-04: Three Objects on Screen at Once — Cluttered

**Symptom:** Three different VGroups visible simultaneously; frame feels overwhelmed.

**Root cause:** Each concept added without fading previous.

**Before (broken):**
```python
self.play(Write(concept_a))
self.play(Write(concept_b))  # A still visible
self.play(Write(concept_c))  # A and B still visible
```

**After (fixed):**
```python
self.play(Write(concept_a))
self.wait(1.5)
self.play(FadeOut(concept_a), Write(concept_b))
self.wait(1.5)
self.play(FadeOut(concept_b), Write(concept_c))
self.wait(1.5)
```

Or, if all three must be visible simultaneously: scale each down and arrange with layout recipe "Three-Step Horizontal Chain."

---

## F-05: Scene Ends Abruptly

**Symptom:** Video hard-cuts to black without transition.

**Root cause:** No `self.wait()` at end; final animation ends exactly as scene ends.

**Before (broken):**
```python
self.play(Write(final_formula))
# scene ends immediately
```

**After (fixed):**
```python
self.play(Write(final_formula))
self.wait(2.0)  # always hold final state
all_objects = VGroup(*self.mobjects)
self.play(FadeOut(all_objects), run_time=0.7)
self.wait(0.3)
```

**Rule:** Every scene must end with at least `self.wait(1.5)` after the final animation, followed by a FadeOut.

---

## F-06: Font Too Small After Scaling

**Symptom:** Text became unreadable after `.scale()` to fit alongside another object.

**Root cause:** Started with `font_size=36`, scaled to 0.5 → effectively 18px. Below minimum.

**Fix path:**
1. Reduce content first (fewer words)
2. If still too small: split the scene
3. Never scale text below effective 32px

```python
# Check effective size after scaling
text = Text("Label", font_size=48)
text.scale(0.7)
# effective = 48 * 0.7 = 33.6 ✓ (barely ok)

text.scale(0.5)
# effective = 48 * 0.5 = 24 ✗ (too small — split scene instead)
```

---

## F-07: Color Used Inconsistently

**Symptom:** "Input" variable shown in BLUE in Scene 1, GREEN in Scene 3. Viewer is confused.

**Root cause:** Hardcoded color strings instead of PALETTE.

**Before (broken):**
```python
# Scene 1
var_x = MathTex("x", color=BLUE)
# Scene 3
var_x = MathTex("x", color=GREEN)  # forgot it was BLUE before
```

**After (fixed):**
```python
# Always import PALETTE and use it by semantic name
var_x = MathTex("x", color=PALETTE["input"])  # always BLUE, always consistent
```

**Rule:** Search and replace all hardcoded color strings (BLUE, GREEN, etc.) with PALETTE["..."] before final render.

---

## F-08: Arrow Tip Missing or Tiny

**Symptom:** Arrow appears as a line with no visible tip, or tip is invisible.

**Root cause:** Arrow too short (< 0.5 units), or `tip_length` not set, or zero-length arrow.

**Before (broken):**
```python
arrow = Arrow(start=obj_a.get_right(), end=obj_b.get_left())
# If objects are touching, arrow has zero length → crash
```

**After (fixed):**
```python
# Ensure minimum spacing before creating arrow
if np.linalg.norm(obj_b.get_left() - obj_a.get_right()) < 0.5:
    obj_b.shift(RIGHT * 0.8)  # force gap

arrow = Arrow(
    start=obj_a.get_right(),
    end=obj_b.get_left(),
    tip_length=0.2,
    stroke_width=2.5,
    buff=0.1
)
```

---

## F-09: always_redraw() Causes Jitter

**Symptom:** Object using `always_redraw()` flickers or jumps during animation.

**Root cause:** The lambda creates a new Mobject every frame with slightly different positioning.

**Fix:**
```python
# BAD — positioning inside always_redraw creates instability
label = always_redraw(
    lambda: Text(f"x = {t.get_value():.2f}").move_to(UP * 2)
)

# GOOD — position outside, only content changes
label = always_redraw(
    lambda: Text(f"x = {t.get_value():.2f}", font_size=40,
                 color=PALETTE["input"]).move_to(UP * 2.0)
)
# Explicit font_size and color prevent style drift between frames
```

---

## F-10: Narration-Visual Mismatch

**Symptom:** Video shows "Result: 2x" while narration is still explaining the limit concept.

**Root cause:** Scene was built from code without storyboard; visual reveals came in wrong order.

**Fix:** Return to Stage 2. Redo the storyboard for affected scenes. Map each narration beat to an animation beat explicitly before writing any code.

```
NARRATION BEAT → ANIMATION BEAT MAPPING (example)
"What is the slope?"             → secant line appears
"As we bring the points closer"  → dx_tracker animates from 2.0 → 0.01
"We get the instantaneous rate"  → tangent line appears, Indicate()
"Which we call the derivative"   → formula Write()
```

Every narration beat must have a corresponding visual event. Build code from this map.
