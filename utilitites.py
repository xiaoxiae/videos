"""Various utilities used throughout the videos."""
from manim import *
from math import *
from random import *
from yaml import *
from pulp import *
from functools import *
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

def createHighlightedParagraph(*args, speed=0.04, width=22, size=r"\normalsize", splitBy = None):
    if splitBy is not None:
        args = args[0].split(splitBy)

    text = Tex(r"\parbox{" + str(width) + "em}{" + size + " " + args[0], *args[1:-1], args[-1] + "}")
    highlightText(text)
    return len("".join(args).replace("$", "")) * speed, text

def fade_all(self):
    self.play(*map(FadeOut, self.mobjects))

def fade(f):
    """A decorator for construct method of scenes where all objects should fade at the end."""
    def inner(self):
        f(self)
        self.play(*map(FadeOut, self.mobjects))

    return inner

def visuallyChangeColor(self, l):
    """Animations to visually change the color of something."""
    self.play(
            *[a.animate.set_color(b) for a, b in l],
            *[Flash(a, color=b) for a, b in l],
            )

def get_coloring(edges, one_indexing=False):
    n = len(set([u for u, v in edges] + [v for u, v in edges]))
    colors = [RED, GREEN, BLUE, PINK, ORANGE, LIGHT_BROWN]

    model = LpProblem(sense=LpMinimize)

    chromatic_number = LpVariable(name="chromatic number", cat='Integer')

    variables = [[LpVariable(name=f"x_{i}_{j}", cat='Binary') \
                  for i in range(n)] for j in range(n)]

    for i in range(n):
        model += lpSum(variables[i]) == 1

    for u, v in edges:
        for color in range(n):
            model += variables[u - (1 if one_indexing else 0)][color] + variables[v - (1 if one_indexing else 0)][color] <= 1

    for i in range(n):
        for j in range(n):
            model += chromatic_number >= (j + 2) * variables[i][j]

    model += chromatic_number

    status = model.solve(PULP_CBC_CMD(msg=False))

    return {i: colors[j]
          for i in range(n) for j in range(n) if variables[i][j].value()}

def get_independent_set(edges, one_indexing=False):
    n = len(set([u for u, v in edges] + [v for u, v in edges]))

    model = LpProblem(sense=LpMaximize)

    variables = [LpVariable(name=f"x_{i}", cat='Binary') for i in range(n)]

    for u, v in edges:
        model += variables[u - 1] + variables[v - 1] <= 1

    model += lpSum(variables)

    status = model.solve(PULP_CBC_CMD(msg=False))
    return [i + 1 for i in range(n) if int(variables[i].value()) == 1]

def parse_graph(graph, s=0.13, t=0.13):
    """Parse a graph in a format like this:
    ---
    1 2 <9.118072543948081, 4.650124351556167> <15.236742443226104, 4.832736111387815>
    3 2 <20.843227140026464, 7.251324476362457> <15.236742443226104, 4.832736111387815>
    3 4 <20.843227140026464, 7.251324476362457> <20.151957872799326, 1.2158150606935652>
    4 2 <20.151957872799326, 1.2158150606935652> <15.236742443226104, 4.832736111387815>
    """

    lt = {}
    edges = []
    vertices = set()

    for line in graph.strip().splitlines():
        line = line.strip()
        edge, p1, p2 = line.split("<")
        u, v = list(map(int, edge.strip().split()))
        u_x, u_y = list(map(float, p1[:-2].strip().split(", ")))
        v_x, v_y = list(map(float, p2[:-2].strip().split(", ")))

        lt[u] = [u_x, u_y, 0]
        lt[v] = [v_x, v_y, 0]

        edges.append((u, v))
        vertices.add(u)
        vertices.add(v)

    lt_avg_x = 0
    lt_avg_y = 0

    for i in lt:
        lt_avg_x += lt[i][0]
        lt_avg_y += lt[i][1]

    lt_avg_x /= len(lt)
    lt_avg_y /= len(lt)

    for i in lt:
        lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * t, 0)

    return Graph(sorted(list(vertices)), edges, layout=lt).scale(2)

def hsv_to_rgb(h, s, v):
    """HSV to RGB (normalized from 0 to 1)"""
    i = floor(h*6)
    f = h*6 - i
    p = v * (1-s)
    q = v * (1-f*s)
    t = v * (1-(1-f)*s)

    return [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i%6)]

def rainbow_to_rgb(i, s=0.7):
    """Return a random color from a gradient."""
    return rgb_to_hex(hsv_to_rgb(i, s, 1))
