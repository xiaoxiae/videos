from manim import *
from typing import Dict


def MyCode(code_raw, **kwargs):
    code = Code(code=code_raw, **kwargs, font="Fira Mono", line_spacing=0.65, style="Monokai", language="c")
    code.remove(code[0])  # idk man what the fuck is the Manim code class
    code[0].set_color(GRAY)
    return code

def MyCodeKindaTho(code_raw, **kwargs):
    code = Code(code=code_raw, **kwargs, font="Fira Mono", line_spacing=0.65, style="Monokai", language="c")
    code.remove(code[0])  # idk man what the fuck is the Manim code class
    code.remove(code[0])  # idk man what the fuck is the Manim code class
    return code


def WriteCode(code):
    return Write(code, run_time = 0.3 * len(code.code) ** (1/2) + 1)


def SetCodeOpacity(code, skip_lines = None, opacity=1):
    return AnimationGroup(
        code.background_mobject.animate.set_opacity(opacity),
        VGroup(*[l for i, l in enumerate(code.code) if skip_lines is None or i not in skip_lines]).animate.set_opacity(opacity),
    )

    return Write(code, run_time = 0.4 * len(code.code) ** (1/2) + 1)


def FadeCode(*args, **kwargs):
    return SetCodeOpacity(*args, **kwargs, opacity=0.25)


def UnfadeCode(*args, **kwargs):
    return SetCodeOpacity(*args, **kwargs, opacity=1)

def CreateHighlightObject(obj):
    sr = SurroundingRectangle(
        obj,
        color=YELLOW,
        fill_opacity=0.15
    ).set_z_index(1)

    return sr

def CreateHighlightObjectSubtle(obj):
    sr = SurroundingRectangle(
        obj,
        color=YELLOW,
        fill_opacity=0.25,
        stroke_width=0,
        buff=0.05,
    ).set_z_index(-1)

    return sr


def CreateHighlightCodeLine(code, line, start=None, end=None):
    sr = SurroundingRectangle(
        code.code[line][start or 0:end or len(code.code[line])],
        color=YELLOW,
        fill_opacity=0.15
    ).set_z_index(1)

    return sr


def CreateHighlightCodeLines(code, lines, offset=1):  # TODO: offset is scuffed af
    sr = SurroundingRectangle(
        VGroup(*[l[offset:] for i, l in enumerate(code.code) if i in lines]),
        color=YELLOW,
        fill_opacity=0.15
    ).set_z_index(1)

    return sr


def align_code(groups, buff=1):
    dir = groups[0][0]
    align = groups[0][1]

    g = VGroup(*[(g if type(g) != list else align_code(g)) for g in groups[1:]])

    if dir == "-":
        g.arrange_in_grid(rows=1, row_alignments=align, buff=buff)
    else:
        g.arrange_in_grid(cols=1, col_alignments=align, buff=buff)

    return g


def align_object_by_coords(obj, current, desired, animation=False):
    """Align an object such that it's current coordinate coordinate will be the desired."""
    if isinstance(current, Mobject):
        current = current.get_center()

    if isinstance(desired, Mobject):
        desired = desired.get_center()

    if animation:
        return obj.animate.shift(desired - current)
    else:
        obj.shift(desired - current)

def fade(f):
    def inner(self):
        f(self)
        self.play(*map(FadeOut, self.mobjects))

    return inner
