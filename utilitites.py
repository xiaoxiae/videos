"""Various utilities used throughout the videos."""
from manim import *
from math import *

def create_code(self, code):
    """Create code more evenly."""
    return [Create(code.background_mobject), Write(code.code), Write(code.line_numbers)]

def myCode(*args, **kwargs):
    code = Code(*args, **kwargs, font="Fira Mono", line_spacing=0.35, style="Monokai")
    code.background_mobject[0].set_style(fill_opacity=0)
    return code



