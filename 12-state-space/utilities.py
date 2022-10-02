from manim import *
from typing import Dict


class Queue(VMobject):

    def __init__(self, scale: float = 1):
        super().__init__()

        ARROW_SIZE = 1.4

        self.buff = 0.1 * scale

        self.top = VGroup(
            Arrow(start=UP * ARROW_SIZE, end=ORIGIN),
            Line(start=LEFT, end=RIGHT),
        )

        self.bot = VGroup(
            Arrow(start=ORIGIN, end=DOWN * ARROW_SIZE),
            Line(start=LEFT, end=RIGHT),
        ).next_to(self.top, DOWN, buff=self.buff)

        self.items = []

        self.add(self.top, self.bot)

        self.scale(scale)

        # fuck this shit stupid library
        self.top[0].set_stroke_width(scale * 6)
        self.top[1].set_stroke_width(scale * 6)
        self.bot[0].set_stroke_width(scale * 6)
        self.bot[1].set_stroke_width(scale * 6)

    def animate_add(self, obj: Mobject) -> Animation:
        put_obj = obj.copy().next_to(self.top, DOWN, buff=self.buff)

        other_objs = VGroup(*(self.items + [self.bot]))

        self.items = [obj] + self.items

        return AnimationGroup(
            other_objs.animate.next_to(put_obj, DOWN, buff=self.buff),
            obj.animate.move_to(put_obj),
        )

    def animate_remove(self, pos) -> Animation:
        obj = self.items.pop()

        return AnimationGroup(
            self.bot.animate.next_to(self.top if len(self.items) == 0 else self.items[-1], DOWN, buff=self.buff),
            obj.animate.move_to(pos),
        )


def MyCode(code_raw, **kwargs):
    code = Code(code=code_raw, **kwargs, font="Fira Mono", line_spacing=0.65, style="Monokai", insert_line_no=False, language="python")
    code.background_mobject[0].set(color=BLACK, stroke_color=WHITE, stroke_width=5)
    code.remove(code[1])  # idk man what the fuck is the Manim code class
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


def code_parts_from_file(path: str) -> Dict[str, Code]:
    blocks = {}

    with open(path) as f:
        block_name = None
        block = ""

        for line in f.read().splitlines():
            if line.startswith("#"):
                parts = line.split()

                if len(parts) == 2 and parts[1] == "endblock":
                    if block_name is not None:
                        blocks[block_name] = MyCode(block)
                        blocks[block_name].code.set_z_index(10)

                    block_name = None
                    block = ""
                    continue

                if len(parts) == 3 and parts[1] == "block":
                    block_name = parts[2]
                    continue

            if block_name is not None:
                block += line + "\n"

    return blocks
