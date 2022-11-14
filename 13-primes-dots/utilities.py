from manim import *

def SR(obj):
    return SurroundingRectangle(
        obj,
        color=BLUE,
        fill_opacity=0.20
    ).set_z_index(1)

def fade(f):
    def inner(self):
        f(self)
        self.play(*map(FadeOut, self.mobjects))

    return inner
