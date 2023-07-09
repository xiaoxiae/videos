from manim import *
from typing import Dict
import networkx as nx
import networkx as nx
from math import pi


BIG_OPACITY = 0.2


def fade(f):
    """A decorator for construct method of scenes where all objects should fade at the end."""
    def inner(self):
        f(self)

        self.play(*map(FadeOut, self.mobjects))

    return inner

def maze_to_vgroup(contents):
    maze = VGroup()
    maze_dict = {}

    for y, row in enumerate(contents):
        i = 0
        for x, symbol in enumerate(row):
            if symbol == "#":
                r = Rectangle(width=1.0, height=1.0, fill_opacity=1, fill_color=WHITE)
                r.set_z_index(10000)
            elif symbol == ".":
                continue
            else:
                r = Rectangle(width=1.0, height=1.0)
                r.set_z_index(0.1)

            r.move_to((y + 0.5) * DOWN + (x + 0.5) * RIGHT + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT)
            maze.add(r)
            maze_dict[(x, y)] = r

    return maze, maze_dict

class MoveAndFadeThereBack(Animation):

    def __init__(self, mobject: Mobject, shift=RIGHT, **kwargs):
        self.original = mobject.copy()
        self.shift = shift

        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        """A function that gets called every frame, for the animation to... animate."""
        new_alpha = self.rate_func(alpha)

        half_alpha = 1 - abs(new_alpha - 0.5) * 2

        new_mobject = self.original.copy().set_opacity(half_alpha).shift(self.shift * new_alpha)
        self.mobject.become(new_mobject)


class MoveAndFadeThereBackKindaTho(Animation):

    def __init__(self, mobject: Mobject, other: Mobject, **kwargs):
        self.original = mobject.copy()
        self.other = other

        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        """A function that gets called every frame, for the animation to... animate."""
        new_alpha = self.rate_func(alpha)

        half_alpha = min((1 - abs(new_alpha - 0.5) * 2) * 5, 1)

        self.mobject.move_to(
            self.original.get_center() * (1 - new_alpha) + self.other.get_center() * new_alpha
        )
        self.mobject.set_stroke_width(half_alpha * self.original.get_stroke_width())
        self.mobject.set_opacity(half_alpha)
