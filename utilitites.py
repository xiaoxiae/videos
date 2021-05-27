"""Various utilities used throughout the videos."""
from manim import *
from math import *
from random import *
from yaml import *
from pulp import *
from functools import *
from itertools import *
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

def get_coloring(vertices, edges):
    """Get the coloring of a set of edges, returning a vertex: color dictionary."""
    n = len(vertices)
    colors = [RED, GREEN, BLUE, PINK, ORANGE, LIGHT_BROWN]

    mapping = {}
    inverse_mapping = {}
    for i, vertex in enumerate(vertices):
        mapping[vertex] = i
        inverse_mapping[i] = vertex

    seed(0)

    model = LpProblem(sense=LpMinimize)

    chromatic_number = LpVariable(name="chromatic number", cat='Integer')

    variables = [[LpVariable(name=f"x_{i}_{j}", cat='Binary') \
                  for i in range(n)] for j in range(n)]

    for i in range(n):
        model += lpSum(variables[i]) == 1

    for u, v in edges:
        for color in range(n):
            model += variables[mapping[u]][color] + variables[mapping[v]][color] <= 1

    for i in range(n):
        for j in range(n):
            model += chromatic_number >= (j + 2) * variables[i][j]

    model += chromatic_number

    status = model.solve(PULP_CBC_CMD(msg=False))

    return {inverse_mapping[i]: colors[j]
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

def induced_subgraphs(vertices, edges, min_size=1, max_size=None):
    """A generator of all induced subgraphs of the graph, sorted by size (largest to smallest)."""
    n = len(vertices)

    if max_size is None:
        max_size = n + 1

    # an induced subgraph of each size (besides 0)
    for i in reversed(range(min_size, max_size)):
        for subset in combinations(vertices, r=i):
            yield list(subset), [(u, v) for u, v in edges if u in subset and v in subset]

def get_maximum_clique(vertices, edges):
    n = len(vertices)

    model = LpProblem(sense=LpMaximize)

    mapping = {}
    inverse_mapping = {}
    for i, vertex in enumerate(vertices):
        mapping[vertex] = i
        inverse_mapping[i] = vertex

    seed(0)

    # is the given vertex a part of the clique
    variables = [LpVariable(name=f"x_{i}", cat='Binary') for i in range(n)]

    non_edges = [(u, v) for u in range(n) for v in range(u + 1, n) if (inverse_mapping[u], inverse_mapping[v]) not in edges and (inverse_mapping[v], inverse_mapping[u]) not in edges]

    # non-edges are not together in the clique
    for u, v in non_edges:
        model += variables[u] + variables[v] <= 1

    # the clique has to be maximal
    model += lpSum(variables)

    status = model.solve(PULP_CBC_CMD(msg=False))

    return [inverse_mapping[i] for i in range(n) if variables[i].value()]
