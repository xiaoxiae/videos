from manim import *
from typing import Dict
import networkx as nx
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
from math import pi


BIG_OPACITY = 0.2
ALIGN_SPACING = 1
MINOTAUR_MOVE_SPEED = 1.5
MINOTAUR_MOVE_DELAY = 0.15

FAST_RUNTIME = 0.33


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

def get_tree(depth, root=(0, (0, 0, 0, 0), (1, 0, 0, 0)), force_expand=[]):

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

            yield remaining + 1, tuple(ores), tuple(robots)


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

    queue = [root]
    visited = {queue[0]: None}

    while len(queue) != 0:
        current = queue.pop(0)

        if current[0] >= depth and not current in force_expand:
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

def actually_get_tree(depth, root, angle, force_expand=[], only_layout=False):
    if not only_layout:
        myrobots = VGroup(*[
            SVGMobject("assets/robot-ore.svg"),
            SVGMobject("assets/robot-clay.svg"),
            SVGMobject("assets/robot-obsidian.svg"),
            SVGMobject("assets/robot-geode.svg"),
        ]).arrange(buff=0.8)

        myminerals = Group(*[
            ImageMobject("assets/minerals/ore.png"),
            ImageMobject("assets/minerals/clay.png"),
            ImageMobject("assets/minerals/obsidian.png"),
            ImageMobject("assets/minerals/geode.png"),
        ])

    def vertex_from_state(state, only_layout):
        if only_layout:
            return Dot()

        text = Tex("$$" + str(state) + "$$").set_z_index(10)
        g = Group(text)

        start = 1 + len(str(state[0])) + 2
        for i in range(4):
            s = start
            e = start + len(str(state[1][i]))

            g.add(
                myminerals[i].copy().set_height(text.get_height() * 0.5).next_to(text[0][s:e], UP, buff=0.05).set_z_index(10),
            )

            start += len(str(state[1][i])) + 1

        start += 2
        for i in range(4):
            s = start
            e = start + len(str(state[2][i]))

            g.add(
                myrobots[i].copy().set_height(text.get_height() * 0.5).next_to(text[0][s:e], UP, buff=0.05).set_z_index(10),
            )

            start += len(str(state[2][i])) + 1

        return g

    def vertex_bg_from_vertex(vertex):
        return SurroundingRectangle(vertex, corner_radius=0, color=BLACK, fill_color=BLACK, fill_opacity=1).set_z_index(5).scale(1.25)

    T = get_tree(depth, root=root, force_expand=force_expand)
    pos = graphviz_layout(T, prog="neato", root=root)

    scale = 10

    lt = {k: [(v[0] - pos[root][0]) / scale, (v[1] - pos[root][1]) / scale, 0] for k, v in pos.items()}

    tree = Graph.from_networkx(T, layout=lt)
    tree.rotate(angle, about_point=tree.vertices[root].get_center())

    state_objects = {k: vertex_from_state(k, only_layout).move_to(tree.vertices[k]) for k in tree.vertices}
    state_bgs = {k: vertex_bg_from_vertex(state_objects[k]) for k in tree.vertices}

    return tree, state_objects, state_bgs


class MyFlash(AnimationGroup):
    """Send out lines in all directions.

    Parameters
    ----------
    point
        The center of the flash lines. If it is a :class:`.~Mobject` its center will be used.
    line_length
        The length of the flash lines.
    num_lines
        The number of flash lines.
    flash_radius
        The distance from `point` at which the flash lines start.
    line_stroke_width
        The stroke width of the flash lines.
    color
        The color of the flash lines.
    time_width
        The time width used for the flash lines. See :class:`.~ShowPassingFlash` for more details.
    run_time
        The duration of the animation.
    kwargs
        Additional arguments to be passed to the :class:`~.Succession` constructor

    Examples
    --------
    .. manim:: UsingFlash

        class UsingFlash(Scene):
            def construct(self):
                dot = Dot(color=YELLOW).shift(DOWN)
                self.add(Tex("Flash the dot below:"), dot)
                self.play(Flash(dot))
                self.wait()

    .. manim:: FlashOnCircle

        class FlashOnCircle(Scene):
            def construct(self):
                radius = 2
                circle = Circle(radius)
                self.add(circle)
                self.play(Flash(
                    circle, line_length=1,
                    num_lines=30, color=RED,
                    flash_radius=radius+SMALL_BUFF,
                    time_width=0.3, run_time=2,
                    rate_func = rush_from
                ))
    """

    def __init__(
        self,
        point,
        line_length: float = 0.2,
        num_lines: int = 12,
        flash_radius: float = 0.1,
        line_stroke_width: int = 3,
        color: str = YELLOW,
        time_width: float = 1,
        run_time: float = 1.0,
        **kwargs
    ) -> None:
        if isinstance(point, Mobject):
            self.point = point.get_center()
        else:
            self.point = point
        self.color = color
        self.line_length = line_length
        self.num_lines = num_lines
        self.flash_radius = flash_radius
        self.line_stroke_width = line_stroke_width
        self.run_time = run_time
        self.time_width = time_width
        self.animation_config = kwargs

        self.lines = self.create_lines()
        animations = self.create_line_anims()
        super().__init__(*animations, group=self.lines)

    def create_lines(self) -> VGroup:
        lines = VGroup()
        for angle in np.arange(0, TAU, TAU / self.num_lines):
            line = Line(self.point, self.point + self.line_length * RIGHT).set_z_index(100000000000000)
            line.shift((self.flash_radius) * RIGHT)
            line.rotate(angle, about_point=self.point)
            lines.add(line)
        lines.set_color(self.color)
        lines.set_stroke(width=self.line_stroke_width)
        return lines

    def create_line_anims(self):
        return [
            ShowPassingFlash(
                line,
                time_width=self.time_width,
                run_time=self.run_time,
                **self.animation_config,
            )
            for line in self.lines
        ]
