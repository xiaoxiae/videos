from manim import *
from random import seed, shuffle, uniform
from math import comb
from itertools import combinations, product
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


def get_all_colorings(V, E, n):
    """Return a dictionary of all vertex colorings for a given graph."""
    colors = [RED, GREEN, BLUE, PINK, ORANGE, LIGHT_BROWN]

    def _is_valid(assignment):
        for u, v in E:
            if assignment[u] == assignment[v]:
                return False
        return True

    assignments = []
    for assignment in product(colors[:n], repeat=len(V)):
        if _is_valid(assignment):
            assignments.append(assignment)

    return assignments


class Introo(MovingCameraScene):
    def get_graphy_graphy(self, g_nx):
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

        bn = Tex("0").next_to(b, UP).set_z_index(1)
        cn = Tex("0").next_to(c, UP).set_z_index(1)
        dn = Tex("24").next_to(d, LEFT).set_z_index(1)

        x_label = ax.get_x_axis_label("n")

        graph = CurvesAsSubmobjects(graph).set_color_by_gradient(DARKER_GRAY,
                                                                 WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE,
                                                                 DARKER_GRAY)

        return ax, x_label, graph, a, b, c, d, bn, cn, dn


    def construct(self):
        seed(0xdeadbeef)

        g_nx = nx.windmill_graph(3, 3)

        p = Tex(r"""$$
\begin{aligned}
T(G) &= x^{6} + 3 x^{5} \\[-0.1cm]
    &+ 3 x^{4} y + 3 x^{4} \\[-0.1cm]
    &+ 6 x^{3} y + x^{3} \\[-0.1cm]
    &+ 3 x^{2} y^{2} + 3 x^{2} y \\[-0.1cm]
    &+ 3 x y^{2} + y^{3}
\end{aligned}$$""").scale(2)

        good_for = Tex(r"""
        \begin{itemize} \item $T_{1,1} = $ \# of spanning trees
                        \item $T_{2,0} = $ \# of acyclic orientations
                        \item measures network reliability
                        \item calculates linear codes
                        \item has ties to quantum field theory
                       \end{itemize}""")

        colorings = get_all_colorings(g_nx.nodes, g_nx.edges, 3)

        g = Graph.from_networkx(g_nx, layout="spring", layout_scale=0.8, layout_config={'seed': 1})\
                .scale(5)\
                .rotate(1.26)\
                .move_to(ORIGIN)

        coloring = get_coloring(g_nx.nodes, g_nx.edges)

        random_vertices = list(g.vertices)
        shuffle(random_vertices)

        a = Tex(r"\underline{How many $n$-colorings?}").scale(2.15)
        b = Tex(r"(adjacent vertices $=$ different colors)").scale(1.25).next_to(a, DOWN, buff=0.7)

        texts = VGroup(a, b)

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

        graph_grid = VGroup()

        for c in colorings:
            gc = g.copy()

            graph_grid.add(gc)

            for i, vertex in enumerate(gc.vertices):
                gc.vertices[vertex].set_color(c[i]).scale(2)

        graph_grid.scale(0.125).arrange_in_grid(cols=4, buff=0.2)

        box = SurroundingRectangle(graph_grid, color=GRAY, buff=0.25, corner_radius=0.2, stroke_width=5)

        ax, x_label, graph, a, b, c, d, bn, cn, dn = self.get_graphy_graphy(g_nx)

        d.set_z_index(1)
        dn.set_z_index(1)

        beeg_g = VGroup(ax, x_label, graph, a, b, c, d, bn, cn, dn)
        beeg_g.scale(0.9).align_to(g, DOWN).shift(DOWN * 4)  # god forgive me

        line = Line(
                start=Dot().scale(0.00001).next_to(box, RIGHT, buff=0).shift(DOWN * 0.5).get_center(),
                end=d.get_center(),
                color=GRAY,
        )

        c = Tex(f"$$\chi(G) = {polynomial_to_tex(chromatic(g_nx.nodes, g_nx.edges))}$$").next_to(beeg_g, DOWN, buff=-0.2)

        c[0][2].set_opacity(0)
        cin = g.copy().set_color(WHITE).move_to(c[0][2]).set_height(c[0][2].get_height())

        self.play(
            self.camera.frame.animate.move_to(VGroup(g, beeg_g, texts, c)),
            FadeIn(ax),
            FadeIn(x_label),
            Succession(Wait(0.25), Write(graph, run_time=1)),
            Succession(Wait(0.25), FadeIn(c, run_time=1)),
            Succession(Wait(0.5), FadeIn(cin, run_time=1)),
            AnimationGroup(
                *[FadeIn(o) for o in [a, b, c, d]],
                lag_ratio=0.25
            ),
            AnimationGroup(
                *[FadeIn(o) for o in [Dot().shift(LEFT * 1000), bn, cn, dn]],  # xd
                lag_ratio=0.25
            ),
        )

        t = 8
        self.play(
            AnimationGroup(
                Transform(g, graph_grid[t]),
                AnimationGroup(
                    FadeIn(graph_grid[:t]),
                    FadeIn(graph_grid[t:]),
                    FadeIn(box),
                    FadeIn(line),

                ),
                lag_ratio=0.5,
            ),
        )

        p[0][2].set_opacity(0)
        p.next_to(c, DOWN, buff=4)
        idkman = g.copy().set_color(WHITE).move_to(p[0][2]).set_height(p[0][2].get_height()).shift(DOWN * 0.04)

        self.play(
            AnimationGroup(
                self.camera.frame.animate.next_to(self.camera.frame, DOWN, buff=-2),
                AnimationGroup(
                    FadeIn(p),
                    FadeIn(idkman, run_time=1),
                ),
                lag_ratio=0.5,
            ),
        )

        good_for.scale(1.25).next_to(p, DOWN, buff=2).align_to(p, LEFT)

        good_for[0][0:22].set_color(RED)
        good_for[0][22:50].set_color(BLUE)

        self.play(FadeIn(good_for[0][0:22]))
        self.play(FadeIn(good_for[0][22:50]))

        s = 11

        seed(s)
        nxgraph = nx.erdos_renyi_graph(12, 0.45, seed=s)
        G = Graph.from_networkx(nxgraph, layout="spring", layout_scale=3.5, layout_config={'seed': s}).rotate(PI / 7 + PI).scale(1.15)

        for e in G.edges:
            G.edges[e].set_stroke_width(uniform(1, 7))
            G.edges[e].set_opacity(uniform(0, 1))
        for v in G.vertices:
            G.vertices[v].scale(uniform(2, 3.5))

        G.next_to(p, DOWN, buff=7)

        self.play(
            FadeIn(good_for[0][50:77]),
            FadeIn(G),
        )

        self.play(
            FadeOut(G),
        )

        quantum = ImageMobject("assets/index.png").set_width(self.camera.frame.get_width() * 0.5)
        quantum.next_to(p, DOWN, buff=8.4)

        lc = Tex(r"""$$\begin{pmatrix}
            1 & 1 & 0 & 1 & 0 & 0 & 0 \\
            0 & 1 & 1 & 0 & 1 & 0 & 0 \\
            0 & 0 & 1 & 1 & 0 & 1 & 0 \\
            0 & 0 & 0 & 1 & 1 & 0 & 1
        \end{pmatrix}$$""").scale(1.5)

        lc.next_to(p, DOWN, buff=8.4)

        self.play(
            FadeIn(good_for[0][77:99]),
            FadeIn(lc),
        )

        self.play(
            FadeOut(lc),
        )

        self.play(
            FadeIn(good_for[0][99:]),
            FadeIn(quantum),
        )

        title = ImageMobject("assets/handbook.png").set_width(self.camera.frame.get_width() * 0.8)
        title.next_to(self.camera.frame, RIGHT, buff=1)

        for m in self.mobjects:
            self.remove(m)
        self.add(p)
        self.add(good_for)
        self.add(idkman)
        self.add(quantum)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    self.camera.frame.animate.move_to(title),
                ),
                FadeIn(title),
                lag_ratio=0.75,
            )
        )

        self.play(
            FadeOut(title)
        )



class TP(ThreeDScene):
    def construct(self):
        resolution_fa = 24
        phi = 75 * DEGREES
        theta = 100 * DEGREES
        self.set_camera_orientation(phi=phi, theta=theta)

        rate = 0.2

        self.begin_ambient_camera_rotation(rate=rate)

        scale = 1/750

        f = lambda x, y: [x, y, (x**6 + 3*x**5 + 3*x**4*y + 3*x**4 + 6*x**3*y + x**3 + 3*x**2*y**2 + 3*x**2*y + 3*x*y**2 + y**3) * scale]

        surface = Surface(
            f,
            resolution=(resolution_fa, resolution_fa),
            v_range=[-3, +3],
            u_range=[-3, +3]
        )

        surface.scale(1.2, about_point=ORIGIN)
        surface.set_style(fill_opacity=1, stroke_color=WHITE)
        surface.set_fill_by_checkerboard(DARK_GRAY, DARKER_GRAY, opacity=1)
        axes = ThreeDAxes()

        spanning = f(1, 1)[-1] / scale
        orient = f(2, 0)[-1] / scale

        sw = 3

        a = Dot3D(point=axes.coords_to_point(1, 1, f(1, 1)[-1]), color=RED, stroke_width=sw, stroke_color=BLACK).scale(3)
        b = Dot3D(point=axes.coords_to_point(2, 0, f(2, 0)[-1]), color=BLUE, stroke_width=sw, stroke_color=BLACK).scale(3)

        self.add(axes)
        self.add(surface)

        st = Tex(f"\\textbf{{{int(spanning)}}}", color=RED, stroke_width=sw, stroke_color=BLACK)\
                .rotate(phi, axis=RIGHT)\
                .rotate(theta + PI / 2, axis=OUT)\
                .move_to(a).shift(OUT).scale(1.5)
        st.add_updater(lambda x, dt: x.rotate(rate * dt, axis=OUT))
        st.set_opacity(0)

        ori = Tex(f"\\textbf{{{int(orient)}}}", color=BLUE, stroke_width=sw, stroke_color=BLACK)\
                .rotate(phi, axis=RIGHT)\
                .rotate(theta + PI / 2, axis=OUT)\
                .move_to(b).shift(OUT).scale(1.5)
        ori.add_updater(lambda x, dt: x.rotate(rate * dt, axis=OUT))
        ori.set_opacity(0)

        self.add(st)
        self.add(ori)

        self.wait(5.2)
        self.play(
            FadeIn(a),
            st.animate.set_opacity(1)
        )
        self.wait(1.86666)
        self.play(
            FadeIn(b),
            ori.animate.set_opacity(1)
        )
        self.wait(2.7666666)
