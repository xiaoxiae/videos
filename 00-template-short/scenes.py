from manim import *


class Intro(MovingCameraScene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY

        text = Tex("\Huge Intro")

        self.play(Write(text))
        self.play(FadeOut(text))
