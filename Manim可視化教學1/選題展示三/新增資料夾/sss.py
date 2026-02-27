from manim import *

class ExampleScene(Scene):
    def construct(self):

        text = Tex(
            r"這是一個包含中文的數學公式：$E = mc^2$")
        self.play(Create(text))
        self.wait(2)