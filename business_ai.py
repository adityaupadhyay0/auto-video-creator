from manim import *
import numpy as np

"""
RENDER-READY MANIM CODE (10X IMPROVED VERSION)
Produced by Manim Video Director Skill.

UPGRADES:
- Advanced Staging: Uses staggering and focus-indication (Indicate/Flash).
- Dynamic Systems: Stochastic jitter for AI and flowing data loops.
- Title Cards: Standardized scene openers for professional pacing.
- Network Intelligence: Pulsing edges for the Organizational Brain.
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
}

# --- HELPERS ---

def make_title_card(scene_obj, title_text, subtitle_text=None):
    title = Text(title_text, font_size=52, color=PALETTE["neutral"])
    title.move_to(SAFE["title_pos"])
    if subtitle_text:
        subtitle = Text(subtitle_text, font_size=32, color=PALETTE["dim"])
        subtitle.next_to(title, DOWN, buff=0.4)
        scene_obj.play(Write(title), FadeIn(subtitle, shift=DOWN * 0.2))
        scene_obj.wait(1.0)
        scene_obj.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), FadeOut(subtitle))
    else:
        scene_obj.play(Write(title))
        scene_obj.wait(1.0)
        scene_obj.play(title.animate.scale(0.7).to_edge(UP, buff=0.3))
    return title

def exit_scene(scene_obj):
    all_objects = VGroup(*scene_obj.mobjects)
    scene_obj.play(FadeOut(all_objects, shift=LEFT * 0.5), run_time=0.8)
    scene_obj.wait(0.3)

class Database(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        base = Ellipse(width=2, height=1)
        side1 = Line(LEFT, LEFT + DOWN*2)
        side2 = Line(RIGHT, RIGHT + DOWN*2)
        bottom = Arc(start_angle=PI, angle=PI, radius=1).scale(np.array([1, 0.5, 1])).shift(DOWN*2)
        self.add(base, side1, side2, bottom)

# --- SCENES ---

class Scene_1_TheDisconnect(Scene):
    def construct(self):
        title = make_title_card(self, "The AI Disconnect", "Why hasn't the economy changed yet?")

        # --- BEAT 2: BUILD ---
        # Gear (Deterministic)
        gear = VGroup(
            Circle(radius=1.0, color=PALETTE["input"], stroke_width=4),
            *[Line(ORIGIN, UP*1.2).rotate(a, about_point=ORIGIN).set_color(PALETTE["input"])
              for a in np.linspace(0, 2*np.pi, 12, endpoint=False)]
        ).shift(LEFT * 3.5 + DOWN * 0.5)

        gear_label = Text("DETERMINISTIC", font_size=28, color=PALETTE["input"]).next_to(gear, DOWN)

        # Stochastic Cloud (AI)
        cloud_dots = VGroup(*[Dot(radius=0.1, color=PALETTE["transform"]) for _ in range(20)])
        for d in cloud_dots:
            d.move_to(RIGHT*3.5 + UP*np.random.uniform(-0.5, 0.5) + RIGHT*np.random.uniform(-0.5, 0.5))

        def jitter_cloud(mobject, dt):
            for d in mobject:
                d.shift(np.random.uniform(-0.05, 0.05) * UP + np.random.uniform(-0.05, 0.05) * RIGHT)

        cloud_dots.add_updater(jitter_cloud)
        cloud_label = Text("PROBABILISTIC", font_size=28, color=PALETTE["transform"]).next_to(cloud_dots, DOWN, buff=1.2)

        self.play(Create(gear), Write(gear_label))
        self.play(FadeIn(cloud_dots), Write(cloud_label))

        # Gear rotates
        self.play(Rotate(gear, angle=2*PI, run_time=3, rate_func=linear), run_time=3)

        # --- BEAT 3: REVEAL ---
        vs = Text("VS", font_size=48, color=PALETTE["error"]).move_to(DOWN*0.5)
        reveal_text = Text("Product vs. Service", font_size=44, color=PALETTE["abstract"]).move_to(DOWN * 2.5)

        self.play(Write(vs))
        self.play(FadeIn(reveal_text, shift=UP))
        self.play(Indicate(reveal_text, color=PALETTE["transform"]))
        self.wait(1.5)

        exit_scene(self)

class Scene_2_BusinessFirst(Scene):
    def construct(self):
        title = make_title_card(self, "Business-First AI", "The Core Principle")

        # --- BEAT 2: BUILD ---
        core = RoundedRectangle(corner_radius=0.3, width=4, height=2.5, color=PALETTE["output"], stroke_width=6)
        core_text = Text("BUSINESS\nOPERATIONS", font_size=36, color=PALETTE["output"]).move_to(core)

        models = VGroup(
            Circle(radius=0.7, color=PALETTE["dim"]).shift(UP*2.2 + LEFT*4.5),
            Circle(radius=0.7, color=PALETTE["dim"]).shift(UP*2.2 + RIGHT*4.5),
            Circle(radius=0.7, color=PALETTE["dim"]).shift(DOWN*2.2)
        )
        model_labels = VGroup(
            Text("Claude", font_size=24, color=PALETTE["dim"]).next_to(models[0], UP),
            Text("OpenAI", font_size=24, color=PALETTE["dim"]).next_to(models[1], UP),
            Text("Llama", font_size=24, color=PALETTE["dim"]).next_to(models[2], DOWN)
        )

        self.play(Create(core), Write(core_text))
        self.play(LaggedStart(*[FadeIn(m) for m in models], lag_ratio=0.3), Write(model_labels))

        # --- BEAT 3: REVEAL ---
        # Models serve the core
        arrows = VGroup(*[Arrow(m.get_center(), core.get_boundary_point(m.get_center()-core.get_center()),
                               color=PALETTE["transform"], tip_length=0.2) for m in models])

        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2))
        self.play(core.animate.scale(1.1).set_fill(PALETTE["output"], opacity=0.1))
        self.play(Flash(core, color=PALETTE["output"], line_length=0.5))

        insight = Text("AI fits the Business,\nnot vice-versa.", font_size=32, color=PALETTE["neutral"]).to_edge(RIGHT, buff=1)
        self.play(Write(insight))
        self.wait(2)

        exit_scene(self)

class Scene_3_ModelAgnostic(Scene):
    def construct(self):
        title = make_title_card(self, "Model Agnosticism", "Future-Proofing your stack")

        # --- BEAT 2: BUILD ---
        interface = Square(side_length=2.5, color=PALETTE["neutral"], stroke_width=2).shift(LEFT * 3.5)
        interface_label = Text("STANDARD\nINTERFACE", font_size=28).next_to(interface, UP)

        model_1 = VGroup(
            Square(side_length=2.2, color=PALETTE["abstract"], fill_opacity=0.2),
            Text("Model V1", font_size=32)
        ).shift(RIGHT * 3.5)

        model_2 = VGroup(
            Square(side_length=2.2, color=PALETTE["abstract"], fill_opacity=0.2),
            Text("Model V2", font_size=32)
        ).shift(RIGHT * 8)

        self.play(Create(interface), Write(interface_label))
        self.play(FadeIn(model_1, shift=LEFT))
        self.play(FadeIn(model_2, shift=LEFT))

        # --- BEAT 3: REVEAL ---
        # Swap animation
        self.play(model_1.animate.move_to(interface.get_center()), run_time=1.2)
        self.wait(0.5)
        self.play(
            model_1.animate.shift(DOWN * 5),
            model_2.animate.move_to(interface.get_center()),
            run_time=1.2
        )

        self.play(Indicate(interface, color=PALETTE["transform"]))

        protect = Text("Economic Incentive:\nNo Vendor Lock-in", font_size=36, color=PALETTE["output"]).shift(RIGHT * 3.5)
        self.play(Write(protect))
        self.wait(2)

        exit_scene(self)

class Scene_4_DataInfrastructure(Scene):
    def construct(self):
        title = make_title_card(self, "Robust Data Infra", "Software that serves people")

        # --- BEAT 2: BUILD ---
        worker = VGroup(Circle(radius=0.4, color=PALETTE["input"]), Dot()).shift(LEFT * 4.5)
        worker_label = Text("Sales/Ops Worker", font_size=24).next_to(worker, DOWN)

        db = Database(color=PALETTE["output"]).scale(0.7).shift(RIGHT * 4.5 + UP*0.5)
        db_label = Text("Organizational Intelligence", font_size=24).next_to(db, DOWN, buff=1.5)

        self.play(Create(worker), Write(worker_label))
        self.play(Create(db), Write(db_label))

        # --- BEAT 3: REVEAL ---
        # Data Pipeline
        path = CurvedArrow(worker.get_top(), db.get_top() + LEFT*0.5, angle=-PI/3, color=PALETTE["transform"])
        pipeline_text = Text("Automatic Context Capture", font_size=28, color=PALETTE["transform"]).next_to(path, UP)

        self.play(Create(path), Write(pipeline_text))

        # Flowing data packets
        packets = VGroup(*[Dot(radius=0.08, color=PALETTE["transform"]) for _ in range(8)])
        self.play(LaggedStart(*[MoveAlongPath(p, path) for p in packets], lag_ratio=0.15, run_time=3))

        # Overhead warning
        overhead = Text("ZERO OVERHEAD", font_size=40, color=PALETTE["output"]).move_to(DOWN*2.5)
        self.play(FadeIn(overhead, scale=1.5))
        self.play(Circumscribe(overhead, color=PALETTE["output"]))
        self.wait(2)

        exit_scene(self)

class Scene_5_TheOntologyLayer(Scene):
    def construct(self):
        title = make_title_card(self, "The Ontology Layer", "Mapping the Business Brain")

        # --- BEAT 2: BUILD ---
        nodes = VGroup(
            Text("SALES", font_size=32, color=PALETTE["abstract"]).shift(UP*1.5 + LEFT*3),
            Text("MARKETING", font_size=32, color=PALETTE["abstract"]).shift(UP*1.5 + RIGHT*3),
            Text("OPS", font_size=32, color=PALETTE["abstract"]).shift(DOWN*1.5)
        )

        circles = VGroup(*[Circle(radius=1.2, color=PALETTE["dim"]).move_to(n) for n in nodes])

        self.play(LaggedStart(*[Create(c) for c in circles], lag_ratio=0.3),
                  LaggedStart(*[Write(n) for n in nodes], lag_ratio=0.3))

        # --- BEAT 3: REVEAL ---
        # Connect the nodes with pulsing lines
        edges = VGroup(
            Line(nodes[0], nodes[1], color=PALETTE["transform"]),
            Line(nodes[1], nodes[2], color=PALETTE["transform"]),
            Line(nodes[2], nodes[0], color=PALETTE["transform"])
        )

        def pulse_edge(mobject, dt):
            mobject.set_stroke(width=2 + np.sin(self.time*3)*2)

        for e in edges: e.add_updater(pulse_edge)

        self.play(Create(edges))

        labels = VGroup(
            Text("Relationships", font_size=24).move_to(UP*2),
            Text("Context", font_size=24).move_to(LEFT*2.5 + DOWN*0.5),
            Text("Knowledge", font_size=24).move_to(RIGHT*2.5 + DOWN*0.5)
        )
        self.play(Write(labels))

        # The Unification
        unify = Text("Data Science + LLM Reasoning", font_size=36, color=PALETTE["output"]).move_to(DOWN*3.2)
        self.play(Write(unify))
        self.play(Indicate(unify))
        self.wait(2)

        exit_scene(self)

class Scene_6_PracticalApps(Scene):
    def construct(self):
        title = make_title_card(self, "Practical Transformation", "Real-world Outcomes")

        # --- BEAT 2: BUILD ---
        apps = VGroup(
            VGroup(RoundedRectangle(width=4.5, height=2.5, color=PALETTE["input"]),
                   Text("Sales:\nDynamic Scripts", font_size=32)).shift(LEFT*3.5),
            VGroup(RoundedRectangle(width=4.5, height=2.5, color=PALETTE["output"]),
                   Text("Marketing:\nTest Engines", font_size=32)).shift(RIGHT*3.5)
        ).shift(DOWN*0.5)

        for app in apps:
            self.play(FadeIn(app, shift=UP*0.5))
            self.wait(0.5)

        # --- BEAT 3: REVEAL ---
        reasoning = Text("LLMs as Reasoning Engines", font_size=40, color=PALETTE["transform"]).move_to(UP*1.2)
        self.play(Write(reasoning))
        self.play(Flash(reasoning, color=PALETTE["transform"]))

        # Summary chain
        chain = Text("Analyze → Strategize → Execute", font_size=32, color=PALETTE["neutral"]).move_to(DOWN*3)
        self.play(Write(chain))
        self.wait(2)

        # --- FINAL EXIT ---
        final_msg = Text("TRANSFORM YOUR OPERATIONS", font_size=48, color=PALETTE["output"])
        self.play(FadeOut(Group(*self.mobjects)))
        self.play(Write(final_msg))
        self.play(Indicate(final_msg))
        self.wait(3)
        self.play(FadeOut(final_msg))
