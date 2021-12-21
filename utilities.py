"""Various utilities used throughout the videos."""
from manim import *

def fade(f):
    def inner(self):
        f(self)
        self.play(*map(FadeOut, self.mobjects))

    return inner
