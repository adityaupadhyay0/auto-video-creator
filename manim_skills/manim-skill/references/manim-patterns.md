# Manim Patterns Reference

Pre-verified, render-safe code patterns for common educational visuals.
Copy-paste directly. All use the PALETTE and SAFE constants from SKILL.md.

---

## 1. Axes + Function Graph

```python
class GraphScene(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 4, 1],
            x_length=9,
            y_length=5,
            axis_config={"color": PALETTE["neutral"], "stroke_width": 2},
            tips=True,
        ).move_to(ORIGIN)

        # Always add labels
        x_label = axes.get_x_axis_label("x", edge=RIGHT, direction=RIGHT)
        y_label = axes.get_y_axis_label("f(x)", edge=UP, direction=UP)

        graph = axes.plot(lambda x: x**2, color=PALETTE["input"], stroke_width=3)
        graph_label = axes.get_graph_label(graph, label=MathTex("x^2"),
                                            x_val=1.5, direction=UP+RIGHT)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(graph), Write(graph_label))
        self.wait(1.5)
```

---

## 2. Secant → Tangent (Derivative Intuition)

```python
class SecantToTangent(Scene):
    def construct(self):
        axes = Axes(x_range=[-1, 4, 1], y_range=[-1, 6, 1],
                    x_length=8, y_length=5).shift(LEFT * 1)
        func = lambda x: x**2
        curve = axes.plot(func, color=PALETTE["neutral"])

        x0 = 1.0  # point of tangency

        # Secant line — starts wide
        dx = 2.0
        secant = axes.get_secant_slope_group(
            x=x0, graph=curve, dx=dx,
            dx_line_color=PALETTE["input"],
            dy_line_color=PALETTE["output"],
            secant_line_color=PALETTE["transform"],
            secant_line_length=5,
        )

        # dx tracker for shrinking animation
        dx_tracker = ValueTracker(dx)

        def get_secant():
            return axes.get_secant_slope_group(
                x=x0, graph=curve, dx=dx_tracker.get_value(),
                dx_line_color=PALETTE["input"],
                dy_line_color=PALETTE["output"],
                secant_line_color=PALETTE["transform"],
                secant_line_length=5,
            )

        dynamic_secant = always_redraw(get_secant)

        self.play(Create(axes), Create(curve))
        self.play(Create(dynamic_secant))
        self.play(dx_tracker.animate.set_value(0.01), run_time=3)
        self.wait(2)
```

---

## 3. Highlighted Formula Reveal (Step by Step)

```python
class FormulaReveal(Scene):
    def construct(self):
        # Full formula — build part by part
        lhs = MathTex("f'(x)", color=PALETTE["output"], font_size=52)
        equals = MathTex("=", color=PALETTE["neutral"], font_size=52)
        limit = MathTex(r"\lim_{\Delta x \to 0}", color=PALETTE["abstract"], font_size=44)
        fraction = MathTex(
            r"\frac{f(x + \Delta x) - f(x)}{\Delta x}",
            color=PALETTE["neutral"], font_size=44
        )

        formula = VGroup(lhs, equals, limit, fraction).arrange(RIGHT, buff=0.3)
        formula.move_to(ORIGIN)

        # Reveal piece by piece
        self.play(Write(lhs))
        self.wait(0.5)
        self.play(Write(equals))
        self.play(Write(limit))
        self.wait(0.5)
        self.play(Write(fraction))
        self.wait(2)

        # Highlight the limit part
        box = SurroundingRectangle(limit, color=PALETTE["transform"], buff=0.15)
        self.play(Create(box))
        self.wait(2)
```

---

## 4. Concept Flow Arrow Chain

```python
class ConceptChain(Scene):
    def construct(self):
        concepts = ["Slope", "Rate of Change", "Derivative"]
        colors = [PALETTE["input"], PALETTE["transform"], PALETTE["output"]]

        boxes = VGroup()
        for label, color in zip(concepts, colors):
            box = RoundedRectangle(
                width=3.0, height=0.9, corner_radius=0.2,
                fill_color=color, fill_opacity=0.15,
                stroke_color=color, stroke_width=2
            )
            text = Text(label, font_size=32, color=color)
            text.move_to(box.get_center())
            boxes.add(VGroup(box, text))

        boxes.arrange(RIGHT, buff=1.5).move_to(ORIGIN)

        arrows = VGroup()
        for i in range(len(boxes) - 1):
            arrow = Arrow(
                start=boxes[i].get_right(),
                end=boxes[i+1].get_left(),
                color=PALETTE["neutral"],
                stroke_width=2.5,
                tip_length=0.2
            )
            arrows.add(arrow)

        # Animate left to right
        for i, box in enumerate(boxes):
            self.play(FadeIn(box, shift=UP * 0.2), run_time=0.6)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.5)
        self.wait(2)
```

---

## 5. Comparison Table (Two Columns)

```python
class ComparisonTable(Scene):
    def construct(self):
        headers = ["Average Rate", "Instantaneous Rate"]
        rows = [
            ["Over an interval", "At a single point"],
            [r"\frac{\Delta y}{\Delta x}", r"\frac{dy}{dx}"],
            ["Secant line", "Tangent line"],
        ]

        col_colors = [PALETTE["input"], PALETTE["output"]]
        header_group = VGroup()
        for i, (header, color) in enumerate(zip(headers, col_colors)):
            t = Text(header, font_size=36, color=color)
            header_group.add(t)
        header_group.arrange(RIGHT, buff=2.5).move_to(UP * 2.8)

        divider = Line(LEFT * 6, RIGHT * 6, stroke_width=1,
                       color=PALETTE["dim"]).move_to(UP * 2.3)

        content_rows = VGroup()
        for row_idx, row in enumerate(rows):
            row_group = VGroup()
            for col_idx, cell in enumerate(row):
                if "\\" in cell or "^" in cell or "_" in cell:
                    t = MathTex(cell, font_size=36, color=col_colors[col_idx])
                else:
                    t = Text(cell, font_size=32, color=col_colors[col_idx])
                row_group.add(t)
            row_group.arrange(RIGHT, buff=2.5)
            row_group.move_to(UP * (1.5 - row_idx * 1.0))
            content_rows.add(row_group)

        self.play(Write(header_group))
        self.play(Create(divider))
        for row in content_rows:
            self.play(FadeIn(row, shift=RIGHT * 0.1), run_time=0.5)
        self.wait(2)
```

---

## 6. Animated Number Line with Point

```python
class NumberLinePoint(Scene):
    def construct(self):
        nl = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            color=PALETTE["neutral"],
            include_numbers=True,
            label_direction=DOWN,
        ).move_to(ORIGIN)

        dot = Dot(nl.n2p(0), color=PALETTE["input"], radius=0.12)
        label = MathTex("x", color=PALETTE["input"], font_size=36)
        label.next_to(dot, UP, buff=0.3)
        label.add_updater(lambda m: m.next_to(dot, UP, buff=0.3))

        self.play(Create(nl))
        self.play(FadeIn(dot), Write(label))
        self.play(dot.animate.move_to(nl.n2p(3)), run_time=1.5)
        self.wait(1.5)
```

---

## 7. Scene Title Card (Scene Opener)

Use this at the start of every scene for visual consistency:

```python
def make_title_card(scene_obj, title_text, subtitle_text=None):
    """Call at the start of construct() for consistent scene openings."""
    title = Text(title_text, font_size=52, color=PALETTE["neutral"])
    title.move_to(SAFE["title_pos"])

    if subtitle_text:
        subtitle = Text(subtitle_text, font_size=32, color=PALETTE["dim"])
        subtitle.next_to(title, DOWN, buff=0.4)
        scene_obj.play(Write(title), FadeIn(subtitle, shift=DOWN * 0.2))
        scene_obj.wait(1.0)
        scene_obj.play(
            title.animate.scale(0.7).to_edge(UP, buff=0.3),
            FadeOut(subtitle)
        )
    else:
        scene_obj.play(Write(title))
        scene_obj.wait(1.0)
        scene_obj.play(title.animate.scale(0.7).to_edge(UP, buff=0.3))
    return title
```

---

## 8. Reveal-by-Indication (Focus Attention)

```python
# After object is on screen, draw attention to a specific part
self.play(Indicate(target_object, color=PALETTE["transform"], scale_factor=1.3))

# For formulas — highlight a sub-expression
self.play(Circumscribe(subexpression, color=PALETTE["transform"],
                        fade_out=True, run_time=1.5))

# Flash for emphasis
self.play(Flash(dot, color=PALETTE["output"], line_length=0.4,
                num_lines=12, flash_radius=0.5))
```

---

## 9. Smooth Scene Transition (Exit Pattern)

Use at the end of every scene — never hard-cut:

```python
# Fade everything out smoothly
all_objects = VGroup(*self.mobjects)
self.play(FadeOut(all_objects, shift=LEFT * 0.5), run_time=0.8)
self.wait(0.3)
# Next scene begins with FadeIn or fresh Write
```

---

## 10. Updating Variable Display

```python
class UpdatingVar(Scene):
    def construct(self):
        tracker = ValueTracker(0)

        # Live readout that updates with tracker
        readout = always_redraw(
            lambda: MathTex(
                f"x = {tracker.get_value():.2f}",
                font_size=44,
                color=PALETTE["input"]
            ).move_to(UP * 1.5)
        )

        self.add(readout)
        self.play(tracker.animate.set_value(5.0), run_time=3)
        self.wait(1.5)
```
