from manim import *
from random import seed, shuffle
from math import comb
from itertools import combinations
import sympy
from sympy.abc import x, y
import networkx as nx
from pulp import *


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


def edgesToVertices(edges):
    return list(set([u for u, v in edges] + [v for u, v in edges]))

def neighbours(v, E):
    """Return the neighbours of v in E."""
    t = []
    for e in E:
        if v in e:
            t.append(e)
    return [a for a in edgesToVertices(t) if a != v]


def components(V, E):
    """Calculate the number of components of the graph."""
    total = 0
    explored = set()
    for v in V:
        if v in explored:
            continue

        queue = [v]
        explored.add(v)
        total += 1
        while len(queue) != 0:
            v = queue.pop(0)

            for w in neighbours(v, E):
                if w not in explored:
                    explored.add(w)
                    queue.append(w)

    return total


def tutte(V, E):
    """Return the Tutte polynomial of the graph."""
    polynomial = 0

    c_e = components(V, E)
    for k in range(len(E)+1):

        for F in combinations(E, k):
            c_f = components(V, F)

            r_e = len(V) - c_e
            r_f = len(V) - c_f
            n_f = len(F) - r_f

            polynomial += (x - 1) ** (r_e - r_f) * (y - 1) ** (n_f)

    return polynomial.as_poly()


def chromatic(V, E):
    p = tutte(V, E)
    k = components(V, E)

    return ((-1) ** (len(V) + k) * x ** k * p.subs(x, 1 - x).subs(y, 0))


def polynomial_to_tex(p):
    return sympy.latex(p.as_expr().expand())


class Intro(MovingCameraScene):
    def construct(self):
        seed(0xdeadbeef)

        self.camera.background_color = DARKER_GRAY

        g_nx = nx.windmill_graph(3, 3)

        # TODO:
        ax = Axes(
            x_range=[-0.25, 3, 1],
            y_range=[-5, 24, 1],
            tips=False,
            y_axis_config={
                "include_ticks": False,
            },
            x_axis_config={
                "include_ticks": False,
                "include_numbers": True,
            },
        )

        f = lambda i: float(chromatic(g_nx.nodes, g_nx.edges).subs(x, i))
        graph = ax.plot(f, x_range=[-0.35, 3.10, 0.01])

        a = Dot(ax.c2p(0, 0)).scale(1.5).set_z_index(1)
        b = Dot(ax.c2p(1, 0)).scale(1.5).set_z_index(1)
        c = Dot(ax.c2p(2, 0)).scale(1.5).set_z_index(1)
        d = Dot(ax.c2p(3, 24)).scale(1.5).set_z_index(1)

        x_label = ax.get_x_axis_label("x")

        graph = CurvesAsSubmobjects(graph).set_color_by_gradient(DARKER_GRAY,
                                                                 WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE,
                                                                 DARKER_GRAY)

        self.play(
            FadeIn(ax),
            FadeIn(x_label),
            Succession(Wait(0.25), Write(graph, run_time=1)),
            AnimationGroup(
                *[FadeIn(o) for o in [a, b, c, d]],
                lag_ratio=0.25
            )
        )

        return

        g = Graph.from_networkx(g_nx, layout="spring", layout_scale=0.8, layout_config={'seed': 1})\
                .scale(5)\
                .rotate(1.26)\
                .move_to(ORIGIN)

        coloring = get_coloring(g_nx.nodes, g_nx.edges)

        random_vertices = list(g.vertices)
        shuffle(random_vertices)

        a = Tex(r"\underline{How many colorings?}").scale(2.25)
        b = Tex(r"(adjacent vertices $\iff$ different colors)").scale(1.25).next_to(a, DOWN, buff=0.7)

        spacing = 3

        g.next_to(b, DOWN, buff=spacing)

        self.camera.frame.move_to(Group(a, b, g))
        g.move_to(self.camera.frame)

        self.play(Write(g))

        diff = -g.get_center() + g.copy().next_to(b, DOWN, buff=spacing).get_center()

        self.play(
            AnimationGroup(
                AnimationGroup(
                    g.animate.next_to(b, DOWN, buff=spacing),
                    AnimationGroup(
                        *[g.vertices[v].animate.set_color(coloring[v]).shift(diff)
                          for v in random_vertices],
                    ),
                ),
                AnimationGroup(
                    FadeIn(a),
                    FadeIn(b)
                ),
                lag_ratio=0.5,
            ),
        )

        self.play()

        return

        c = Tex(f"$$\chi(G) = {polynomial_to_tex(chromatic(g_nx.nodes, g_nx.edges))}$$")
        self.play(FadeIn(c))

        #formula = Tex(r"\chi(G) = ")

        ##p = tutte(g.nodes, g.edges())
        #
        #p = tutte([0, 1, 2, 3, 4], [(0, 1), (1, 2), (1, 3), (2, 3), (3, 4)])
        #c = chromatic([0, 1, 2, 3, 4], [(0, 1), (1, 2), (1, 3), (2, 3), (3, 4)])
        #print(str(p))
        #print(str(c))
        #print(p.subs(y, 0).subs(x, 1))
        #quit()


