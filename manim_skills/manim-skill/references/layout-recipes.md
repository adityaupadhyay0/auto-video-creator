# Layout Recipes

Tested frame configurations. Occupancy stays in 50–75% range.
All coordinates use Manim CE default frame (±7.1 × ±4.0).
Safe zone: x ∈ [-6.5, 6.5], y ∈ [-3.6, 3.6].

---

## Single Object — Full Focus

Use when: One formula, one diagram, one key term.

```
┌────────────────────────────────────────┐
│                                        │
│                                        │
│           [PRIMARY OBJECT]             │  ← ORIGIN or slightly up
│                                        │
│                                        │
└────────────────────────────────────────┘
```

```python
primary.move_to(ORIGIN)
# Optional small label below
label.next_to(primary, DOWN, buff=0.5)
```

Occupancy check: primary.width should be 4–8 units wide.

---

## Title + Content (Most Common)

Use when: Scene has a label/title and a main visual.

```
┌────────────────────────────────────────┐
│  Scene Title                           │  ← UP*3.0, LEFT edge
│  ─────────────────────────────────     │
│                                        │
│           [MAIN VISUAL]                │  ← ORIGIN or DOWN*0.3
│                                        │
│                                        │
└────────────────────────────────────────┘
```

```python
title = Text("Title", font_size=44).to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.5)
divider = Line(LEFT*6.0, RIGHT*6.0, stroke_width=1).next_to(title, DOWN, buff=0.2)
main_visual.move_to(DOWN * 0.3)
```

---

## Two-Column Split

Use when: Comparing two things side by side (e.g., secant vs. tangent, input vs. output).

```
┌────────────────────────────────────────┐
│         Title (centered)               │
│                                        │
│  [LEFT OBJECT]     [RIGHT OBJECT]      │
│  LEFT*3.0          RIGHT*3.0           │
│                                        │
│  label_L           label_R             │
└────────────────────────────────────────┘
```

```python
title.move_to(UP * 3.0)
left_obj.move_to(LEFT * 3.2 + DOWN * 0.2)
right_obj.move_to(RIGHT * 3.2 + DOWN * 0.2)
divider = DashedLine(UP*2.5, DOWN*3.0, color=PALETTE["dim"])
# Each side's label:
left_label.next_to(left_obj, DOWN, buff=0.4)
right_label.next_to(right_obj, DOWN, buff=0.4)
```

Min spacing between objects: 1.5 units between inner edges.

---

## Graph + Annotation

Use when: Plotting a function with labels and callouts.

```
┌────────────────────────────────────────┐
│  Title                                 │
│                                        │
│   y                                    │
│   │    /curve                          │
│   │   /                                │
│   │  /     ← annotation (right side)   │
│   │ /                                  │
│   └──────── x                          │
│                                        │
└────────────────────────────────────────┘
```

```python
axes = Axes(
    x_range=[0, 4, 1], y_range=[0, 4, 1],
    x_length=7, y_length=5,
).move_to(LEFT * 0.8 + DOWN * 0.2)

# Annotation — RIGHT side, vertically centered
annotation.move_to(RIGHT * 4.5 + UP * 0.5)
# Keep annotation.width < 2.5 to avoid crowding
```

---

## Three-Step Horizontal Chain

Use when: A → B → C process (concepts, steps, transformations).

```
┌────────────────────────────────────────┐
│              Title                     │
│                                        │
│  [A] ──→──  [B] ──→──  [C]            │
│  LEFT*4.2   ORIGIN     RIGHT*4.2       │
│                                        │
└────────────────────────────────────────┘
```

```python
positions = [LEFT*4.2, ORIGIN, RIGHT*4.2]
y_offset = DOWN * 0.3

for i, (box, pos) in enumerate(zip(boxes, positions)):
    box.move_to(pos + y_offset)

# Arrow between each pair
# Horizontal: use Arrow from box[i].get_right() to box[i+1].get_left()
```

Box width: max 2.8 units each. Check: 3 × 2.8 + 2 × 1.0 (gaps) = 10.4 < 13 ✓

---

## Stacked Vertical Steps

Use when: Step-by-step derivation or proof (each line builds on previous).

```
┌────────────────────────────────────────┐
│  Title                                 │
│                                        │
│  Step 1: f(x) = ...     ← UP*1.8      │
│  Step 2: f'(x) = ...    ← UP*0.6      │
│  Step 3: f'(x) = 2x     ← DOWN*0.6   │
│                                        │
└────────────────────────────────────────┘
```

```python
steps = VGroup()
for i, formula in enumerate(formulas):
    step = MathTex(formula, font_size=38, color=PALETTE["neutral"])
    steps.add(step)

steps.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
steps.move_to(ORIGIN)

# Reveal one at a time
for step in steps:
    self.play(Write(step), run_time=0.8)
    self.wait(0.7)
```

Max 4 steps before splitting scene. If font_size must drop below 34, split.

---

## Full-Frame Animation (No Text)

Use when: The animation IS the explanation (particle motion, transformation, etc.).

```
┌────────────────────────────────────────┐
│                                        │
│                                        │
│         [ANIMATION FILLS FRAME]        │
│                                        │
│                                        │
│  tiny label (optional, bottom edge)    │
└────────────────────────────────────────┘
```

```python
# Use 80% of frame
animation_group.scale_to_fit_width(11.0)  # 11 / 14.2 = 77%
animation_group.move_to(ORIGIN)

# Optional caption — bottom edge
caption = Text("caption", font_size=28, color=PALETTE["dim"])
caption.to_edge(DOWN, buff=0.3)
```

---

## Occupancy Reference

| Objects | Recommended scale/size |
|---------|------------------------|
| 1 large formula | width 6–9 units |
| 1 axes graph | x_length=8, y_length=5 |
| 2 side-by-side | width 2.5–3.0 each |
| 3 chain boxes | width 2.2–2.8 each |
| 4 items | max width 1.8 each; use 2-row grid |

Frame total width = 14.2. Safe = 13.0 (minus margins).
Frame total height = 8.0. Safe = 7.2.
