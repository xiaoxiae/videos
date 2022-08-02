"""Various utilities used throughout the videos."""
from manim import *

def fade(f):
    def inner(self):
        f(self)
        self.play(*map(FadeOut, self.mobjects))

    return inner

def align_object_by_coords(obj, current, desired, animation=False):
    """Align an object such that it's current coordinate coordinate will be the desired."""
    if animation:
        return obj.animate.shift(desired - current)
    else:
        obj.shift(desired - current)

def distance(a: Mobject, b: Mobject):
    """Return the Euclidean distance of two mobjects."""
    return sum([(a.get_center()[i] - b.get_center()[i]) ** 2 for i in range(len(a.get_center()))]) ** (1/2)
    
