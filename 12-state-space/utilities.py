from manim import *
from typing import Dict
import networkx as nx


BIG_OPACITY = 0.2
ALIGN_SPACING = 1
MINOTAUR_MOVE_SPEED = 1.5
MINOTAUR_MOVE_DELAY = 0.15


class Queue(VMobject):

    def __init__(self, scale: float = 1):
        super().__init__()

        self.max_height = 10
        self.item_height = 1

        ARROW_SIZE = 1.4

        self.buff = 0.15 * scale

        top_arrow = VGroup(
            Tex("In").scale(ARROW_SIZE * 2/3),
            Arrow(start=UP * ARROW_SIZE, end=ORIGIN),
        ).arrange(RIGHT)

        top_line = Line(start=LEFT, end=RIGHT)

        top_arrow.next_to(top_line, UP, buff=self.buff / 2)

        self.top = VGroup(
            top_arrow,
            top_line,
        )

        bot_arrow = VGroup(
            Tex("Out").scale(ARROW_SIZE * 2/3),
            Arrow(start=ORIGIN, end=DOWN * ARROW_SIZE),
        ).arrange(RIGHT)

        bot_line = Line(start=LEFT, end=RIGHT)

        bot_arrow.next_to(bot_line, DOWN, buff=self.buff / 2)

        self.bot = VGroup(
            bot_arrow,
            bot_line,
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

        if not config.quality.startswith("medium"):
            self.play(*map(FadeOut, self.mobjects))

    return inner

def get_fade_rect(*args):
    if len(args) == 0:
        return Square(fill_opacity=1 - BIG_OPACITY, color=BLACK).scale(1000).set_z_index(1000000)
    else:
        return SurroundingRectangle(VGroup(*args), fill_opacity=1 - BIG_OPACITY, color=BLACK).set_z_index(1000000)

def maze_to_vgroup(contents):
    maze = VGroup()
    maze_dict = {}

    for y, row in enumerate(contents):
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

def CreateHighlight(obj):
    return SurroundingRectangle(
        obj,
        color=YELLOW,
        fill_opacity=0.15
    ).set_z_index(1)


def CreateHighlightCodeLine(code, line, start=None, end=None):
    return CreateHighlight(code.code[line][start or 0:end or len(code.code[line])])


def CreateHighlightCodeLines(code, lines, offset=1):  # TODO: offset is scuffed af
    return CreateHighlight(VGroup(*[l[offset:] for i, l in enumerate(code.code) if i in lines]))


def align_code(groups, buff=ALIGN_SPACING):
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

def get_tree(depth):

    def can_build_robot(ores, cost):
        for o, c in zip(ores, cost):
            if o < c:
                return False
        return True

    def next_states(remaining, ores, robots, blueprint):
        """Return the next state, given the current ores and robots."""
        states = [(list(ores), list(robots))]

        # attempt to build more robots
        # we're assuming that we can built at most one each turn
        for i, cost in enumerate(blueprint):
            if can_build_robot(ores, cost):
                states.append(
                    (
                        [o - c - (0 if i != j else 1)
                         for j, (o, c) in enumerate(zip(ores, cost))],
                        [r + (0 if i != j else 1)
                         for j, r in enumerate(robots)],
                    )
                )

        for (ores, robots) in states:
            for i in range(len(ores)):
                ores[i] += robots[i]

            yield remaining - 1, tuple(ores), tuple(robots)


    blueprint = """Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian."""
    parts = blueprint.strip().split()

    # robot costs
    blueprint = (
        (
            (int(parts[6]), 0, 0, 0), # ore
            (int(parts[12]), 0, 0, 0), # clay
            (int(parts[18]), int(parts[21]), 0, 0),  # obsidian
            (int(parts[27]), 0, int(parts[30]), 0),  # geode
        )
    )

    #                   Ores        Robots
    #               Or Cl Ob Ge   Or Cl Ob Ge
    queue = [(24, (0, 0, 0, 0), (1, 0, 0, 0))]
    visited = {queue[0]: None}

    while len(queue) != 0:
        current = queue.pop(0)

        if current[0] == 24 - depth:
            continue

        for next_state in next_states(*current, blueprint):
            if next_state not in visited:
                queue.append(next_state)
                visited[next_state] = current

    for k, v in visited.items():
        if v == None:
            del visited[k]
            break

    return nx.from_edgelist([(k, v) for (k, v) in visited.items()])
