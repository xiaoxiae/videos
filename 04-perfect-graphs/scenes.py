from utilities import *
from chromatic import *


class Introduction(Scene):
    def construct(self):
        a = nx.complete_graph(5)
        A = Graph.from_networkx(a, layout="circular", layout_scale=0.8).scale(2)
        A.shift(LEFT * 2.5 + UP * 1.2)

        b = nx.windmill_graph(3, 4)
        B = Graph.from_networkx(b, layout="spring", layout_scale=0.8).scale(2)
        B.shift(RIGHT * 2.5 + UP * 1.2)

        c = nx.algorithms.bipartite.generators.random_graph(7, 5, 0.5)
        lt = {i:[(i * 0.5 if i < 7 else ((i - 6.5) * 6/5 * 0.5)) - 3.5/2,-2 if i < 7 else -2.6,0] for i in range(12)}
        C = Graph.from_networkx(c, layout=lt, layout_scale=0.8).scale(2)

        self.play(Write(A), Write(B), Write(C))

        a_coloring = get_coloring(a.edges)
        b_coloring = get_coloring(b.edges)
        c_coloring = get_coloring(c.edges)

        self.play(
            *[A.vertices[v].animate.set_color(a_coloring[v]) for v in a_coloring],
            *[B.vertices[v].animate.set_color(b_coloring[v]) for v in b_coloring],
            *[C.vertices[v].animate.set_color(c_coloring[v]) for v in c_coloring],
        )

        fade_all(self)

        text = Tex("\Large László Lovász (1972)").shift(UP * 2.3)
        image = SVGMobject("laszlo.svg").scale(2.7).shift(1.4 * DOWN + RIGHT * 0.7)

        self.play(
            Write(text),
            Write(image, run_time=3.5),
        )

        self.play( FadeOut(text), FadeOut(image),)


class Complement(Scene):
    def construct(self):
        title = Tex("\Large Graph complement")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 2.5))

        duration, text = createHighlightedParagraph("A graph", " $H$ ", "is a ","complement"," of the graph ","$G$",", if and only if each two vertices ","adjacent in $G$"," are ","not adjacent in $H$",".", size=r"\footnotesize")
        text.next_to(title, 2 * DOWN)

        self.play(Write(text), run_time=duration)

        vertices = [1, 2, 3, 4, 5]
        edges = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]

        gg = Graph(vertices, edges, layout="circular", layout_scale=1.5/2).scale(2)
        gg.shift(DOWN * 1.5 + LEFT * 3)

        hh = Graph(vertices, edges, layout="circular", layout_scale=1.5/2).scale(2)
        hh.shift(DOWN * 1.5 + RIGHT * 3)

        g_edges = [(1, 2), (1,5), (2,4), (2, 5), (3, 4)]
        g = Graph(vertices, g_edges, layout="circular", layout_scale=1.5/2).scale(2)
        g.shift(DOWN * 1.5 + LEFT * 3)
        g_text = Tex("G")
        g_text.next_to(g, RIGHT + UP).shift(DOWN * 0.80 + LEFT * 0.6)

        h_edges = [(1, 3), (1, 4), (2, 3), (3, 5), (4, 5)]
        h = Graph(vertices, h_edges, layout="circular", layout_scale=1.5/2).scale(2)
        h.shift(DOWN * 1.5 + RIGHT * 3)
        h_text = Tex("H")
        h_text.next_to(h, RIGHT + UP).shift(DOWN * 0.80 + LEFT * 0.6)

        self.play(Write(g), Write(g_text), Write(h), Write(h_text))
        self.play(
                FadeOut(g.edges[(1,2)]),
                FadeIn(hh.edges[(1,2)]),
                )
        self.play(
                FadeOut(g.edges[(2,5)]),
                FadeIn(hh.edges[(2,5)]),
                )
        self.play(
                FadeOut(h.edges[(1,4)]),
                FadeIn(gg.edges[(1,4)]),
                )
        self.play(
                FadeOut(h.edges[(3,5)]),
                FadeIn(gg.edges[(3,5)]),
                )

        fade_all(self)

class CliqueAndIndependentSet(Scene):
    def construct(self):
        title = Tex("\Large Clique and independent set")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 2.5))

        duration, text = createHighlightedParagraph("A ","clique"," is a ","subgraph"," of a graph, such that ","each two vertices are adjacent."," Analogically, and ","independent set"," of a graph is a ","set of vertices"," such that ","no two are adjacent.", size=r"\footnotesize")
        text.next_to(title, 2 * DOWN)

        self.play(Write(text[:6]), run_time=duration / 2)

        s = 0.13
        lt = {
            1:  [47.38483438230261, 14.060368360180616, 0],
            2:  [47.04426001805368, 21.347487665146264, 0],
            3:  [50.9944860441275, 17.87959586965124, 0],
            4:  [43.473770252465194, 17.531227666811304, 0],
            5:  [55.79878824615697, 21.754965041566994, 0],
            6:  [56.88020523754154, 15.782897747658021, 0],
            7:  [62.40430614599554, 13.054510220630755, 0] ,
            8:  [37.189798625724194, 17.32866367272487, 0],
            9:  [31.926414399437974, 14.144547277873158, 0],
            10: [31.749162068885, 20.199682815964888, 0]}

        lt_avg_x = 0
        lt_avg_y = 0

        for i in lt:
            lt_avg_x += lt[i][0]
            lt_avg_y += lt[i][1]

        lt_avg_x /= len(lt)
        lt_avg_y /= len(lt)

        for i in lt:
            lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * s, 0)

        vertices = [i + 1 for i in range(10)]
        edges = [(1, 2),  (1, 3), (1, 4),  (2, 3), (2, 4), (3, 4), (3, 5), (3, 6), (5, 6), (6, 7), (4, 8), (8, 9), (9, 10), (8, 10)]
        g = Graph(vertices, edges, layout=lt).scale(2)
        g.shift(DOWN * 1.65)

        self.play(Write(g))

        dark_color = DARKER_GRAY

        def to_color(color):
            return [g.vertices[i].animate.set_color(color) for i in vertices] + [g.edges[e].animate.set_color(color) for e in edges]

        def to_color_animate(g, color, no_vertices=False):
            return ([g.vertices[i].animate.set_color(color) for i in g.vertices] if not no_vertices else []) + [g.edges[e].animate.set_color(color) for e in g.edges]

        def to_color_no_animate(g, color):
            [g.vertices[i].set_color(color) for i in g.vertices]
            [g.edges[e].set_color(color) for e in g.edges]

        self.play(
                *to_color(dark_color),
                g.vertices[8].animate.set_color(WHITE),
                g.vertices[9].animate.set_color(WHITE),
                g.vertices[10].animate.set_color(WHITE),
                g.edges[(8,9)].animate.set_color(WHITE),
                g.edges[(8,10)].animate.set_color(WHITE),
                g.edges[(9,10)].animate.set_color(WHITE),
                )
        self.wait(0.5)
        self.play(
                *to_color(dark_color),
                g.vertices[5].animate.set_color(WHITE),
                g.vertices[6].animate.set_color(WHITE),
                g.edges[(5,6)].animate.set_color(WHITE),
                )
        self.wait(0.5)
        self.play(
                *to_color(dark_color),
                g.vertices[1].animate.set_color(WHITE),
                g.vertices[2].animate.set_color(WHITE),
                g.vertices[3].animate.set_color(WHITE),
                g.vertices[4].animate.set_color(WHITE),
                g.edges[(1,2)].animate.set_color(WHITE),
                g.edges[(1,3)].animate.set_color(WHITE),
                g.edges[(1,4)].animate.set_color(WHITE),
                g.edges[(2,3)].animate.set_color(WHITE),
                g.edges[(2,4)].animate.set_color(WHITE),
                g.edges[(3,4)].animate.set_color(WHITE),
                )
        self.wait(0.5)
        self.play(*to_color(WHITE))

        self.play(Write(text[6:]), run_time=duration / 2)

        self.play(
                *to_color(dark_color),
                g.vertices[8].animate.set_color(WHITE),
                g.vertices[2].animate.set_color(WHITE),
                g.vertices[6].animate.set_color(WHITE),
                )
        self.wait(0.5)
        self.play(
                *to_color(dark_color),
                g.vertices[10].animate.set_color(WHITE),
                g.vertices[7].animate.set_color(WHITE),
                )
        self.wait(0.5)
        self.play(
                *to_color(dark_color),
                g.vertices[9].animate.set_color(WHITE),
                g.vertices[4].animate.set_color(WHITE),
                g.vertices[5].animate.set_color(WHITE),
                g.vertices[7].animate.set_color(WHITE),
                )
        self.wait(0.5)
        self.play(*to_color(WHITE))

        omega = Tex(r"$\omega$(G) = 4")
        omega.next_to(g).shift(UP + LEFT * 1.7)
        alpha = Tex(r"$\alpha$(G) = 4")
        alpha.next_to(omega, DOWN)

        self.play(g.animate.shift(LEFT))
        self.play(
                Write(omega),
                )
        self.play(
                *to_color(dark_color),
                g.vertices[1].animate.set_color(WHITE),
                g.vertices[2].animate.set_color(WHITE),
                g.vertices[3].animate.set_color(WHITE),
                g.vertices[4].animate.set_color(WHITE),
                g.edges[(1,2)].animate.set_color(WHITE),
                g.edges[(1,3)].animate.set_color(WHITE),
                g.edges[(1,4)].animate.set_color(WHITE),
                g.edges[(2,3)].animate.set_color(WHITE),
                g.edges[(2,4)].animate.set_color(WHITE),
                g.edges[(3,4)].animate.set_color(WHITE),
                )

        self.play(*to_color(WHITE))
        self.play(
                Write(alpha),
                )

        self.play(
                *to_color(dark_color),
                g.vertices[9].animate.set_color(WHITE),
                g.vertices[4].animate.set_color(WHITE),
                g.vertices[5].animate.set_color(WHITE),
                g.vertices[7].animate.set_color(WHITE),
                )

        fade_all(self)

        a = nx.gnm_random_graph(7, 11)
        A = Graph.from_networkx(a, layout="circular", layout_scale=1.3).scale(2)

        b = nx.algorithms.operators.unary.complement(a)
        B = Graph.from_networkx(b, layout="circular", layout_scale=1.3).scale(2)

        C = Graph.from_networkx(b, layout="circular", layout_scale=1.3).scale(2)
        C.vertices[1].set_color(YELLOW),
        C.vertices[2].set_color(YELLOW),
        C.vertices[4].set_color(YELLOW),

        to_color_no_animate(B, dark_color)

        self.play(Write(B), Write(A))
        self.play(
                A.vertices[1].animate.set_color(YELLOW),
                A.vertices[2].animate.set_color(YELLOW),
                A.vertices[4].animate.set_color(YELLOW),
                A.edges[(1, 4)].animate.set_color(YELLOW),
                A.edges[(2, 4)].animate.set_color(YELLOW),
                A.edges[(1, 2)].animate.set_color(YELLOW),
                )

        self.play(
                *to_color_animate(A, dark_color, True),
                *to_color_animate(B, WHITE),
                A.edges[(1, 4)].animate.set_color("#3a4504"),
                A.edges[(2, 4)].animate.set_color("#3a4504"),
                A.edges[(1, 2)].animate.set_color("#3a4504"),
                FadeIn(C),
                )

class InducedSubgraph(Scene):
    def construct(self):
        title = Tex("\Large Induced subgraph")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 2.5))

        duration, text = createHighlightedParagraph("A graph ","$H$"," is an ","induced subgraph"," of ","$G$"," (denoted ","$H \subseteq G$","), if and only if we can get ","$H$"," by ","removing zero or more vertices"," from ","$G$",".", size=r"\footnotesize")
        text.next_to(title, 2 * DOWN)

        self.play(Write(text), run_time=duration)

        s = 0.13
        lt = {
            1:  [47.38483438230261, 14.060368360180616, 0],
            2:  [47.04426001805368, 21.347487665146264, 0],
            3:  [50.9944860441275, 17.87959586965124, 0],
            4:  [43.473770252465194, 17.531227666811304, 0],
            5:  [55.79878824615697, 21.754965041566994, 0],
            6:  [56.88020523754154, 15.782897747658021, 0],
            7:  [62.40430614599554, 13.054510220630755, 0] ,
            8:  [37.189798625724194, 17.32866367272487, 0],
            9:  [31.926414399437974, 14.144547277873158, 0],
            10: [31.749162068885, 20.199682815964888, 0]}

        lt_avg_x = 0
        lt_avg_y = 0

        for i in lt:
            lt_avg_x += lt[i][0]
            lt_avg_y += lt[i][1]

        lt_avg_x /= len(lt)
        lt_avg_y /= len(lt)

        for i in lt:
            lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * s, 0)

        vertices = [i + 1 for i in range(10)]
        edges = [(1, 2),  (1, 3), (1, 4),  (2, 3), (2, 4), (3, 4), (3, 5), (3, 6), (5, 6), (6, 7), (4, 8), (8, 9), (9, 10), (8, 10)]
        g = Graph(vertices, edges, layout=lt).scale(2)
        g.shift(DOWN * 1.65)

        self.play(Write(g))

        # TODO

        fade_all(self)

class ChromaticNumber(Scene):
    def construct(self):
        title = Tex("\Large Chromatic number")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 2.5))


        duration, text = createHighlightedParagraph( "The ","chromatic number $\chi(G)$"," of a graph ","$G$"," is the ","smallest number of colors"," we can use to color the graph's ","vertices",", such that ","no two adjacent vertices"," have the ","same color.","", size=r"\footnotesize")
        text.next_to(title, 2 * DOWN)

        self.play(Write(text), run_time=duration)

        s = 0.13
        lt = {
            1:  [47.38483438230261, 14.060368360180616, 0],
            2:  [47.04426001805368, 21.347487665146264, 0],
            3:  [50.9944860441275, 17.87959586965124, 0],
            4:  [43.473770252465194, 17.531227666811304, 0],
            5:  [55.79878824615697, 21.754965041566994, 0],
            6:  [56.88020523754154, 15.782897747658021, 0],
            7:  [62.40430614599554, 13.054510220630755, 0] ,
            8:  [37.189798625724194, 17.32866367272487, 0],
            9:  [31.926414399437974, 14.144547277873158, 0],
            10: [31.749162068885, 20.199682815964888, 0]}

        lt_avg_x = 0
        lt_avg_y = 0

        for i in lt:
            lt_avg_x += lt[i][0]
            lt_avg_y += lt[i][1]

        lt_avg_x /= len(lt)
        lt_avg_y /= len(lt)

        for i in lt:
            lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * s, 0)

        vertices = [i + 1 for i in range(10)]
        edges = [(1, 2),  (1, 3), (1, 4),  (2, 3), (2, 4), (3, 4), (3, 5), (3, 6), (5, 6), (6, 7), (4, 8), (8, 9), (9, 10), (8, 10)]
        g = Graph(vertices, edges, layout=lt).scale(2)
        g.shift(DOWN * 1.65)

        self.play(Write(g))

        coloring = get_coloring(g.edges, one_indexing=True)

        chi = Tex(r"$\chi$(G) = 4")
        chi.next_to(g).shift(UP * 0.65 + LEFT * 1.7)

        self.play(
            *[g.vertices[v + 1].animate.set_color(coloring[v]) for v in coloring],
        )

        self.play(g.animate.shift(LEFT))

        self.play( Write(chi))

        fade_all(self)
