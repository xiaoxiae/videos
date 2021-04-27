"""Various utilities used throughout the videos."""
from manim import *
from math import *
from random import *
import networkx as nx

def create_code(self, code):
    """Creates code more evenly."""
    return [Create(code.background_mobject), Write(code.code), Write(code.line_numbers)]

def myCode(*args, **kwargs):
    """Declares a nice-looking code block."""
    code = Code(*args, **kwargs, font="Fira Mono", line_spacing=0.35, style="Monokai")
    code.background_mobject[0].set_style(fill_opacity=0)
    return code

def create_output(self, output):
    """Create output more evenly."""
    return [Create(output.background_mobject), Write(output.code)]

def myOutput(*args, **kwargs):
    """Declares a nice-looking output block."""
    code = Code(*args, **kwargs, font="Fira Mono", line_spacing=0.35, style="Monokai", insert_line_no=False)
    code.background_mobject[0].set_style(fill_opacity=0)
    return code

def highlightText(text):
    for i in range(1, len(text), 2):
        text[i].set_color(YELLOW)

def fade(f):
    """A decorator for construct method of scenes where all objects should fade at the end."""
    def inner(self):
        f(self)
        self.play(*map(FadeOut, self.mobjects))

    return inner
