from manim import Scene, Text

class Test(Scene):
    def construct(self):
        text = Text("Hello, Manim!")
        self.play(text.animate.scale(2))
        self.wait(2)
