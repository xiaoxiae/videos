from manim import *
from typing import Dict


BIG_OPACITY = 0.25


class Queue(VMobject):

    def __init__(self, scale: float = 1):
        super().__init__()

        self.max_height = 10
        self.item_height = 1

        ARROW_SIZE = 1.4

        self.buff = 0.15 * scale

        self.top = VGroup(
            Arrow(start=UP * ARROW_SIZE, end=ORIGIN),
            Line(start=LEFT, end=RIGHT),
        )

        self.bot = VGroup(
            Arrow(start=ORIGIN, end=DOWN * ARROW_SIZE),
            Line(start=LEFT, end=RIGHT),
        )

        self.items = []

        self.add(self.top, self.bot)

        self.scale(scale)

        # fuck this shit stupid library
        self.top[0].set_stroke_width(scale * 6)
        self.top[1].set_stroke_width(scale * 6)
        self.bot[0].set_stroke_width(scale * 6)
        self.bot[1].set_stroke_width(scale * 6)

        self.bot.next_to(self.top, DOWN, buff=self.buff)

    #def animate_add(self, objs) -> Animation:
    #    put_objs = [self.top]

    #    new_total_height = (len(self.items) + len(objs)) * self.item_height + (len(self.items) + len(objs) - 1) * self.buff

    #    actual_height = self.item_height if new_total_height <= self.max_height else (self.max_height - (len(self.items) + len(objs) - 1) * self.buff) / (len(self.items) + len(objs))

    #    for obj in objs:
    #        obj.set_height(actual_height)
    #        put_objs.append(obj.copy().next_to(put_objs[-1], DOWN, buff=self.buff))
    #    put_objs.pop(0)

    #    other_objs = VGroup(*self.items)
    #    other_objs_new = other_objs.copy().set_height(len(other_objs) * actual_height + (len(other_objs) - 1) * self.buff).next_to(put_objs[-1], DOWN, buff=self.buff)

    #    for obj, put_obj in zip(objs, put_objs):
    #        obj.move_to(put_obj)

    #    self.items = objs + self.items

    #    lmao_scuffed = [self.top] + put_objs + list(other_objs_new)

    #    return AnimationGroup(
    #        AnimationGroup(
    #            *[Transform(a, b) for a, b in zip(other_objs, other_objs_new)],
    #        self.bot.animate.next_to(lmao_scuffed[-1], DOWN, buff=self.buff),
    #        ),
    #        AnimationGroup(*[FadeIn(o, shift=RIGHT * 2) for o in objs], lag_ratio=0.1, run_time=1),
    #        lag_ratio=0.25,
    #    )

    def animate_add_from(self, objs, froms) -> Animation:
        put_objs = [self.top]

        new_total_height = (len(self.items) + len(objs)) * self.item_height + (len(self.items) + len(objs) - 1) * self.buff

        actual_height = self.item_height if new_total_height <= self.max_height else (self.max_height - (len(self.items) + len(objs) - 1) * self.buff) / (len(self.items) + len(objs))

        for obj in objs:
            obj.set_height(actual_height)
            put_objs.append(obj.copy().next_to(put_objs[-1], DOWN, buff=self.buff))
        put_objs.pop(0)

        other_objs = VGroup(*self.items)
        other_objs_new = other_objs.copy().set_height(len(other_objs) * actual_height + (len(other_objs) - 1) * self.buff).next_to(put_objs[-1], DOWN, buff=self.buff)

        for obj, put_obj in zip(objs, put_objs):
            obj.move_to(put_obj)

        self.items = objs + self.items

        lmao_scuffed = [self.top] + put_objs + list(other_objs_new)

        froms_copies = []
        for f in froms:
            fc = f.copy()
            fc.set_z_index(0.01)
            froms_copies.append(fc)

        return AnimationGroup(
            AnimationGroup(
                *[Transform(a, b) for a, b in zip(other_objs, other_objs_new)],
            self.bot.animate.next_to(lmao_scuffed[-1], DOWN, buff=self.buff),
            ),
            AnimationGroup(*[ReplacementTransform(o1, o2) for o1, o2 in zip(froms_copies, objs)], lag_ratio=0.1, run_time=1),
            lag_ratio=0.25,
        )

    def animate_remove(self) -> Animation:
        obj = self.items.pop()

        new_total_height = (len(self.items)) * self.item_height + (len(self.items) - 1) * self.buff
        actual_height = self.item_height if new_total_height <= self.max_height else (self.max_height - (len(self.items) - 1) * self.buff) / (len(self.items))

        items_objs = VGroup(*self.items)
        items_objs_new = items_objs.copy().set_height(len(items_objs) * actual_height + (len(items_objs) - 1) * self.buff).next_to(self.top, DOWN, buff=self.buff)

        return AnimationGroup(
            AnimationGroup(
                *[Transform(a, b) for a, b in zip(items_objs, items_objs_new)],
                FadeOut(obj, shift=RIGHT * 2),
            ),
            self.bot.animate.next_to(self.top if len(self.items) == 0 else items_objs_new, DOWN, buff=self.buff),
            lag_ratio=0.25,
        )

    def animate_remove_to(self, to) -> Animation:
        obj = self.items.pop()

        new_total_height = (len(self.items)) * self.item_height + (len(self.items) - 1) * self.buff
        actual_height = self.item_height if new_total_height <= self.max_height else (self.max_height - (len(self.items) - 1) * self.buff) / (len(self.items))

        items_objs = VGroup(*self.items)
        items_objs_new = items_objs.copy().set_height(len(items_objs) * actual_height + (len(items_objs) - 1) * self.buff).next_to(self.top, DOWN, buff=self.buff)

        return AnimationGroup(
            AnimationGroup(
                *[Transform(a, b) for a, b in zip(items_objs, items_objs_new)],
                ReplacementTransform(obj, to),
            ),
            self.bot.animate.next_to(self.top if len(self.items) == 0 else items_objs_new, DOWN, buff=self.buff),
            lag_ratio=0.25,
        )

    #def animate_add_from(self, objs, fade_froms) -> Animation:
    #    put_objs = [self.top]
    #    for obj in objs:
    #        put_objs.append(obj.copy().next_to(put_objs[-1], DOWN, buff=self.buff))
    #    put_objs.pop(0)

    #    other_objs = VGroup(*(self.items + [self.bot]))

    #    for obj, put_obj in zip(objs, put_objs):
    #        obj.move_to(put_obj)

    #    self.items = objs + self.items

    #    return AnimationGroup(
    #        *[FadeTransform(f.copy(), o) for f, o in zip(fade_froms, objs)],
    #        other_objs.animate.next_to(obj, DOWN, buff=self.buff),
    #    )

    #def animate_remove_fade(self, fade_to) -> Animation:
    #    obj = self.items.pop()

    #    #return AnimationGroup(
    #    #    self.bot.animate.next_to(self.top if len(self.items) == 0 else self.items[-1], DOWN, buff=self.buff),
    #    #    obj.animate.move_to(pos),
    #    #)

    #    return AnimationGroup(
    #        self.bot.animate.next_to(self.top if len(self.items) == 0 else self.items[-1], DOWN, buff=self.buff),
    #        FadeTransform(obj, fade_to),
    #    )


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
    return SetCodeOpacity(*args, **kwargs, opacity=BIG_OPACITY)


def UnfadeCode(*args, **kwargs):
    return SetCodeOpacity(*args, **kwargs, opacity=1)


def fade(f):
    """A decorator for construct method of scenes where all objects should fade at the end."""
    def inner(self):
        f(self)
        self.play(*map(FadeOut, self.mobjects))

    return inner

def get_fade_rect():
    return Square(fill_opacity=0.85, color=BLACK).scale(1000).set_z_index(1000000)

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
