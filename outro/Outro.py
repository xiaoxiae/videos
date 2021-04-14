from manim import *

class Outro(Scene):
    def construct(self):
        text = Tex("\Huge Thanks for watching!")
        self.play(
            Write(text),
            run_time = 1
        )

        self.wait(2)

        self.play(
            FadeOut(text),
            run_time = 1
        )


