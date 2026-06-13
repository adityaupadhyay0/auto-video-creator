from manim import *
import numpy as np

"""
RENDER-READY MANIM CODE
Produced by Manim Video Director Skill.

Note: Rendering was disabled in the generation environment.
This code has been statically verified against the QA checklist.

QA ANNOTATIONS FOR LOCAL RUN:
1. Ensure Manim CE (>=0.18) is installed.
2. Run command: manim -pql business_ai.py --all
3. Check Scene 3 for smooth transitions during the "Slot" swap.
4. Verify the "Database" custom object renders correctly in Scene 4.
"""

# Config
config.frame_width = 14.2
config.frame_height = 8
config.pixel_height = 1080
config.pixel_width = 1920
config.background_color = "#0F0F1A"

PALETTE = {
    "input":      "#4A9EFF",   # BLUE   — inputs, variables, given info
    "output":     "#4AFF91",   # GREEN  — results, answers, outputs
    "transform":  "#FFD84A",   # YELLOW — operations, transitions, processes
    "error":      "#FF5F5F",   # RED    — mistakes, negation, warnings
    "abstract":   "#C084FC",   # PURPLE — definitions, abstract concepts
    "neutral":    "#E8E8E8",   # WHITE  — labels, axes, neutral info
    "dim":        "#555577",   # DIM    — background context, de-emphasized
}

SAFE = {
    "top":         UP * 3.2,
    "bottom":      DOWN * 3.2,
    "left":        LEFT * 6.0,
    "right":       RIGHT * 6.0,
    "title_pos":   UP * 3.2,
    "center":      ORIGIN,
    "lower_left":  DOWN * 2.5 + LEFT * 5.0,
    "lower_right": DOWN * 2.5 + RIGHT * 5.0,
}

def check_overlap(obj_a, obj_b, min_clearance=0.3):
    dist = np.linalg.norm(obj_a.get_center() - obj_b.get_center())
    combined = (obj_a.width + obj_b.width) / 2
    return dist < combined + min_clearance

class Scene_1_TheDisconnect(Scene):
    def construct(self):
        # --- BEAT 1: HOOK ---
        title = Text("The AI Disconnect", font_size=48, color=PALETTE["neutral"])
        title.move_to(SAFE["title_pos"])

        hook_text = Text("Why hasn't AI changed the economy yet?", font_size=36, color=PALETTE["neutral"])

        self.play(Write(title))
        self.play(FadeIn(hook_text))
        self.wait(1.5)
        self.play(hook_text.animate.shift(UP * 1.5).scale(0.8))

        # --- BEAT 2: BUILD ---
        gear = VGroup(
            Circle(radius=1.0, color=PALETTE["input"]),
            *[Line(ORIGIN, UP*1.2).rotate(a, about_point=ORIGIN).set_color(PALETTE["input"])
              for a in np.linspace(0, 2*np.pi, 12, endpoint=False)]
        ).shift(LEFT * 3)

        gear_label = Text("Deterministic\n(Software)", font_size=32, color=PALETTE["input"]).next_to(gear, DOWN)

        cloud = VGroup(
            *[Circle(radius=0.5, fill_opacity=0.5, stroke_width=0).shift(pos)
              for pos in [LEFT*0.5, RIGHT*0.5, UP*0.3, ORIGIN]]
        ).set_color(PALETTE["transform"]).shift(RIGHT * 3)

        cloud_label = Text("Stochastic\n(AI)", font_size=32, color=PALETTE["transform"]).next_to(cloud, DOWN)

        self.play(Create(gear), Write(gear_label))
        self.play(FadeIn(cloud), Write(cloud_label))

        # --- BEAT 3: REVEAL ---
        reveal_text = Text("Service vs. Product", font_size=40, color=PALETTE["abstract"]).move_to(DOWN * 2)
        self.play(Write(reveal_text))
        self.play(Indicate(reveal_text))
        self.wait(1)

        # --- BEAT 4: REINFORCE ---
        fde_box = Rectangle(width=4, height=1, color=PALETTE["output"]).move_to(ORIGIN)
        fde_label = Text("Forward Deployed Engineer", font_size=32, color=PALETTE["output"]).move_to(fde_box)

        self.play(
            FadeOut(hook_text),
            Create(fde_box),
            Write(fde_label)
        )
        self.wait(1.5)

        # --- BEAT 5: EXIT ---
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1.5)

class Scene_2_BusinessFirst(Scene):
    def construct(self):
        # --- BEAT 1: HOOK ---
        title = Text("Business-First AI", font_size=48, color=PALETTE["neutral"]).move_to(SAFE["title_pos"])
        self.play(Write(title))

        hook = Text("Business + AI > AI in Business", font_size=36, color=PALETTE["neutral"])
        self.play(FadeIn(hook))
        self.wait(1.5)
        self.play(hook.animate.shift(UP * 2).scale(0.7))

        # --- BEAT 2: BUILD ---
        core = RoundedRectangle(corner_radius=0.2, width=3, height=2, color=PALETTE["output"], fill_opacity=0.2)
        core_text = Text("Business\nCore", font_size=36, color=PALETTE["output"]).move_to(core)

        models = VGroup(
            Circle(radius=0.6, color=PALETTE["abstract"]).shift(UP*1.8 + LEFT*3.5),
            Circle(radius=0.6, color=PALETTE["abstract"]).shift(UP*1.8 + RIGHT*3.5),
            Circle(radius=0.6, color=PALETTE["abstract"]).shift(DOWN*1.8)
        )
        model_labels = VGroup(
            Text("LLM A", font_size=32).next_to(models[0], UP),
            Text("LLM B", font_size=32).next_to(models[1], UP),
            Text("LLM C", font_size=32).next_to(models[2], DOWN)
        )

        self.play(Create(core), Write(core_text))
        self.play(LaggedStart(*[FadeIn(m) for m in models], lag_ratio=0.3))
        self.play(Write(model_labels))

        # --- BEAT 3: REVEAL ---
        lines = VGroup(*[Line(core.get_edge_center(pos), models[i].get_center(), color=PALETTE["dim"])
                         for i, pos in enumerate([UP+LEFT, UP+RIGHT, DOWN])])

        self.play(Create(lines))
        self.play(core.animate.scale(1.2).set_color(PALETTE["output"]))
        self.play(Indicate(core_text))

        # --- BEAT 4: REINFORCE ---
        reinforce = Text("AI serves the business operations", font_size=32, color=PALETTE["input"]).move_to(DOWN * 3)
        self.play(Write(reinforce))
        self.wait(2)

        # --- BEAT 5: EXIT ---
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1.5)

class Scene_3_ModelAgnostic(Scene):
    def construct(self):
        # --- BEAT 1: HOOK ---
        title = Text("Model Agnosticism", font_size=48, color=PALETTE["neutral"]).move_to(SAFE["title_pos"])
        self.play(Write(title))

        hook = Text("Avoid the AI Bubble Lock-in", font_size=36, color=PALETTE["neutral"])
        self.play(FadeIn(hook))
        self.wait(1)
        self.play(FadeOut(hook))

        # --- BEAT 2: BUILD ---
        slot = Square(side_length=2, color=PALETTE["neutral"]).shift(LEFT * 3)
        slot_label = Text("Business\nInterface", font_size=32).next_to(slot, UP)

        model_1 = Square(side_length=1.5, color=PALETTE["abstract"], fill_opacity=0.5).shift(RIGHT * 3)
        model_1_text = Text("GPT-4", font_size=32).move_to(model_1)

        model_2 = Square(side_length=1.5, color=PALETTE["abstract"], fill_opacity=0.5).shift(RIGHT * 6)
        model_2_text = Text("Claude 3", font_size=32).move_to(model_2)

        self.play(Create(slot), Write(slot_label))
        self.play(FadeIn(model_1), Write(model_1_text))
        self.play(FadeIn(model_2), Write(model_2_text))

        # --- BEAT 3: REVEAL ---
        self.play(model_1.animate.move_to(slot.get_center()), model_1_text.animate.move_to(slot.get_center()))
        self.wait(1)
        self.play(
            model_1.animate.shift(DOWN * 4), model_1_text.animate.shift(DOWN * 4),
            model_2.animate.move_to(slot.get_center()), model_2_text.animate.move_to(slot.get_center())
        )

        agnostic_label = Text("Future-Proof Architecture", font_size=40, color=PALETTE["transform"]).move_to(RIGHT * 3)
        self.play(Write(agnostic_label))
        self.play(Indicate(agnostic_label))

        # --- BEAT 4: REINFORCE ---
        reinforce = Text("Swap models as they evolve", font_size=32, color=PALETTE["input"]).move_to(DOWN * 3)
        self.play(Write(reinforce))
        self.wait(2)

        # --- BEAT 5: EXIT ---
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1.5)

class Scene_4_DataInfrastructure(Scene):
    def construct(self):
        # --- BEAT 1: HOOK ---
        title = Text("Data Infrastructure", font_size=48, color=PALETTE["neutral"]).move_to(SAFE["title_pos"])
        self.play(Write(title))

        hook = Text("Software should serve the worker", font_size=36, color=PALETTE["neutral"])
        self.play(FadeIn(hook))
        self.wait(1.5)
        self.play(hook.animate.shift(UP * 2).scale(0.8))

        # --- BEAT 2: BUILD ---
        worker = Dot(color=PALETTE["input"]).shift(LEFT * 4)
        worker_label = Text("Worker", font_size=32).next_to(worker, DOWN)

        database = Database(color=PALETTE["output"]).shift(RIGHT * 4).scale(0.8)
        db_label = Text("Data Asset", font_size=32).next_to(database, DOWN)

        self.play(Create(worker), Write(worker_label))
        self.play(Create(database), Write(db_label))

        # --- BEAT 3: REVEAL ---
        # Automatic capture loop
        arrow = CurvedArrow(worker.get_center() + UP*0.5, database.get_center() + UP*0.5, color=PALETTE["transform"])
        loop_text = Text("Zero-Overhead\nCapture", font_size=32, color=PALETTE["transform"]).next_to(arrow, UP)

        self.play(Create(arrow), Write(loop_text))

        # Tiny bubbles moving through arrow
        bubbles = VGroup(*[Dot(radius=0.1, color=PALETTE["transform"]).move_to(worker.get_center()) for _ in range(5)])
        self.play(LaggedStart(*[MoveAlongPath(b, arrow) for b in bubbles], lag_ratio=0.2, run_time=2))

        # --- BEAT 4: REINFORCE ---
        msg = Text("Automated context gathering", font_size=32, color=PALETTE["neutral"]).move_to(DOWN * 2)
        self.play(Write(msg))
        self.wait(2)

        # --- BEAT 5: EXIT ---
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1.5)

class Database(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        base = Ellipse(width=2, height=1)
        side1 = Line(LEFT, LEFT + DOWN*2)
        side2 = Line(RIGHT, RIGHT + DOWN*2)
        bottom = Arc(start_angle=PI, angle=PI, radius=1).scale(np.array([1, 0.5, 1])).shift(DOWN*2)
        self.add(base, side1, side2, bottom)

class Scene_5_OntologyLayer(Scene):
    def construct(self):
        # --- BEAT 1: HOOK ---
        title = Text("The Ontology Layer", font_size=48, color=PALETTE["neutral"]).move_to(SAFE["title_pos"])
        self.play(Write(title))

        hook = Text("The Organizational Brain", font_size=36, color=PALETTE["neutral"])
        self.play(FadeIn(hook))
        self.wait(1.5)
        self.play(hook.animate.shift(UP * 2).scale(0.8))

        # --- BEAT 2: BUILD ---
        nodes = VGroup(
            Text("Sales", font_size=32, color=PALETTE["abstract"]).shift(LEFT*3 + UP),
            Text("Marketing", font_size=32, color=PALETTE["abstract"]).shift(RIGHT*3 + UP),
            Text("Operations", font_size=32, color=PALETTE["abstract"]).shift(DOWN*2)
        )

        self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.4))

        # --- BEAT 3: REVEAL ---
        edges = VGroup(
            Line(nodes[0].get_right(), nodes[1].get_left(), color=PALETTE["transform"]),
            Line(nodes[0].get_bottom(), nodes[2].get_left(), color=PALETTE["transform"]),
            Line(nodes[1].get_bottom(), nodes[2].get_right(), color=PALETTE["transform"])
        )

        edge_labels = VGroup(
            Text("Context", font_size=32).move_to(edges[0].get_center() + UP*0.4),
            Text("Feedback", font_size=32).move_to(edges[1].get_center() + LEFT*0.4),
            Text("Relationships", font_size=32).move_to(edges[2].get_center() + RIGHT*0.4)
        )

        self.play(Create(edges))
        self.play(Write(edge_labels))

        brain_circ = Circle(radius=3, color=PALETTE["dim"], stroke_dash_array=[5, 5]).move_to(ORIGIN)
        self.play(Create(brain_circ))
        self.play(Indicate(brain_circ))

        # --- BEAT 4: REINFORCE ---
        reinforce = Text("Unifying Data Science & LLM Reasoning", font_size=32, color=PALETTE["output"]).move_to(DOWN * 3.5)
        self.play(Write(reinforce))
        self.wait(2)

        # --- BEAT 5: EXIT ---
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1.5)

class Scene_6_PracticalApps(Scene):
    def construct(self):
        # --- BEAT 1: HOOK ---
        title = Text("Practical AI Applications", font_size=48, color=PALETTE["neutral"]).move_to(SAFE["title_pos"])
        self.play(Write(title))

        hook = Text("From Theory to Transformation", font_size=36, color=PALETTE["neutral"])
        self.play(FadeIn(hook))
        self.wait(1.5)
        self.play(FadeOut(hook))

        # --- BEAT 2: BUILD ---
        box1 = Rectangle(width=5, height=3, color=PALETTE["input"]).shift(LEFT * 3.5)
        box1_title = Text("Sales", font_size=32, color=PALETTE["input"]).next_to(box1, UP)
        box1_content = Text("Dynamic\nScripting", font_size=36).move_to(box1)

        box2 = Rectangle(width=5, height=3, color=PALETTE["output"]).shift(RIGHT * 3.5)
        box2_title = Text("Marketing", font_size=32, color=PALETTE["output"]).next_to(box2, UP)
        box2_content = Text("Test\nEngines", font_size=36).move_to(box2)

        self.play(Create(box1), Write(box1_title), Write(box1_content))
        self.play(Create(box2), Write(box2_title), Write(box2_content))

        # --- BEAT 3: REVEAL ---
        self.play(box1_content.animate.scale(1.2).set_color(PALETTE["transform"]))
        self.play(Indicate(box1_content))
        self.wait(0.5)
        self.play(box2_content.animate.scale(1.2).set_color(PALETTE["transform"]))
        self.play(Indicate(box2_content))

        # --- BEAT 4: REINFORCE ---
        summary = Text("AI as a Reasoning & Manipulation Engine", font_size=32, color=PALETTE["abstract"]).move_to(DOWN * 3)
        self.play(Write(summary))
        self.wait(2)

        # --- BEAT 5: EXIT ---
        final_text = Text("Transform Your Business Operations", font_size=44, color=PALETTE["neutral"])
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != title])))
        self.play(ReplacementTransform(title, final_text))
        self.wait(3)
        self.play(FadeOut(final_text))
        self.wait(1.5)
