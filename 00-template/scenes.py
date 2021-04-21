from utilities import *

class Intro(Scene):
    def construct(self):
        text = Tex("\Huge Intro")

        self.play(Write(text))
        self.play(FadeOut(text))
