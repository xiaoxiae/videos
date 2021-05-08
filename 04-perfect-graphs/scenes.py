from utilities import *
from chromatic import *

dark_color = DARKER_GRAY

class MyBulletedList(Tex):
    def __init__(
        self,
        *items,
        buff=MED_LARGE_BUFF,
        dot_scale_factor=2,
        tex_environment=None,
        **kwargs,
    ):
        self.buff = buff
        self.dot_scale_factor = dot_scale_factor
        self.tex_environment = tex_environment
        line_separated_items = [s + "\\\\" for s in items]
        Tex.__init__(
            self, *line_separated_items, tex_environment=tex_environment, **kwargs
        )
        for part in self:
            dot = MathTex("\\cdot").scale(self.dot_scale_factor)
            dot.next_to(part[0], LEFT, MED_SMALL_BUFF)
            part.add_to_back(dot)
        self.arrange(DOWN, aligned_edge=LEFT, buff=self.buff)

        for part, item in zip(self, items):
            parts = item.split(r"$\mid$")
            if len(parts) != 2:
                continue

            a, b = parts
            text = Tex(a + r"$\mid$", b).move_to(part)
            text[1].set_color(YELLOW),

            dot = MathTex("\\cdot").scale(self.dot_scale_factor)
            dot.next_to(text[0], LEFT, MED_SMALL_BUFF)
            text.add_to_back(dot)

            part.become(text)

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

        title = Tex("\Large Definitions")
        title.shift(UP * 2.5)

        self.play(Write(title))

        text = MyBulletedList(
                r"Complement graph $\mid$ $\overline{G}$",
                r"Clique, independent set $\mid$ $\omega(G), \alpha(G)$",
                r"(Proper) induced subgraph $\mid$ $H \subseteq G$, $H \subset G$",
                r"Chromatic number $\mid$ $\chi(G)$",
                r"Perfect graph $\mid$ $G_{\star}$",
                dot_scale_factor=3,
                buff=MED_SMALL_BUFF 
                )

        text.next_to(title, 2 * DOWN).shift(DOWN * 0.5)

        self.play(FadeIn(text))

        fade_all(self)


class Complement(Scene):
    def construct(self):
        title = Tex("\Large Graph complement")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 2.5))

        duration, text = createHighlightedParagraph("A ","complement"," of a graph", " $G$ ", "is a graph ","$\overline{G}$",", such that ","each to vertices"," are adjacent in ","$\overline{G}$",", if and only if they are ","not adjacent"," in ","$G$",".", size=r"\footnotesize")
        text.next_to(title, 2 * DOWN)

        self.play(Write(text), run_time=duration)

        vertices = [1, 2, 3, 4, 5]
        edges = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]

        gg = Graph(vertices, edges, layout="circular", layout_scale=.6).scale(2)
        gg.shift(DOWN * 1.75 + LEFT * 2.5)

        hh = Graph(vertices, edges, layout="circular", layout_scale=.6).scale(2)
        hh.shift(DOWN * 1.75 + RIGHT * 2.5)

        g_edges = [(1, 2), (1,5), (2,4), (2, 5), (3, 4)]
        g = Graph(vertices, g_edges, layout="circular", layout_scale=.6).scale(2)
        g.shift(DOWN * 1.75 + LEFT * 2.5)
        g_text = Tex("G")
        g_text.next_to(g, RIGHT + UP).shift(DOWN * 0.80 + LEFT * 0.6)

        h_edges = [(1, 3), (1, 4), (2, 3), (3, 5), (4, 5)]
        h = Graph(vertices, h_edges, layout="circular", layout_scale=.6).scale(2)
        h.shift(DOWN * 1.75 + RIGHT * 2.5)
        h_text = Tex("$\overline{G}$")
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
        global dark_color

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

        seed(2)
        a = nx.gnm_random_graph(7, 11)
        A = Graph.from_networkx(a, layout="circular", layout_scale=1.3).scale(2)

        b = nx.algorithms.operators.unary.complement(a)
        B = Graph.from_networkx(b, layout="circular", layout_scale=1.3).scale(2)

        C = Graph.from_networkx(b, layout="circular", layout_scale=1.3).scale(2)
        C.vertices[3].set_color(YELLOW),
        C.vertices[4].set_color(YELLOW),
        C.vertices[5].set_color(YELLOW),

        to_color_no_animate(B, dark_color)

        self.play(Write(B), Write(A))
        self.play(
                A.vertices[3].animate.set_color(YELLOW),
                A.vertices[4].animate.set_color(YELLOW),
                A.vertices[5].animate.set_color(YELLOW),
                A.edges[(3, 4)].animate.set_color(YELLOW),
                A.edges[(3, 5)].animate.set_color(YELLOW),
                A.edges[(4, 5)].animate.set_color(YELLOW),
                )

        self.play(
                *to_color_animate(A, dark_color, True),
                *to_color_animate(B, WHITE),
                A.edges[(3, 4)].animate.set_color("#3a4504"),
                A.edges[(3, 5)].animate.set_color("#3a4504"),
                A.edges[(4, 5)].animate.set_color("#3a4504"),
                FadeIn(C),
                )

        fade_all(self)

class InducedSubgraph(Scene):
    def construct(self):
        global dark_color
        title = Tex("\Large Induced subgraph")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 2.5))

        duration, text = createHighlightedParagraph("A graph ","$H$"," is an ","induced subgraph"," of ","$G$"," (denoted ","$H \subseteq G$","), if and only if we can get ","$H$"," by ","removing ","zero"," or more vertices"," from ","$G$",".", size=r"\footnotesize")
        text.next_to(title, 2 * DOWN)
        text[12].set_color(YELLOW)

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

        def to_color(color):
            return [g.vertices[i].animate.set_color(color) for i in vertices] + [g.edges[e].animate.set_color(color) for e in edges]

        self.play(
                g.vertices[9].animate.set_color(dark_color),
                g.vertices[10].animate.set_color(dark_color),
                g.edges[(8, 9)].animate.set_color(dark_color),
                g.edges[(8, 10)].animate.set_color(dark_color),
                g.edges[(9, 10)].animate.set_color(dark_color),
                g.vertices[7].animate.set_color(dark_color),
                g.edges[(6, 7)].animate.set_color(dark_color),
                g.vertices[1].animate.set_color(dark_color),
                g.edges[(1, 2)].animate.set_color(dark_color),
                g.edges[(1, 3)].animate.set_color(dark_color),
                g.edges[(1, 4)].animate.set_color(dark_color),
                )

        self.wait()

        self.play(
                *to_color(WHITE),
                g.vertices[10].animate.set_color(dark_color),
                g.vertices[1].animate.set_color(dark_color),
                g.vertices[2].animate.set_color(dark_color),
                g.vertices[5].animate.set_color(dark_color),
                g.edges[(9, 10)].animate.set_color(dark_color),
                g.edges[(8, 10)].animate.set_color(dark_color),
                g.edges[(1, 2)].animate.set_color(dark_color),
                g.edges[(1, 3)].animate.set_color(dark_color),
                g.edges[(1, 4)].animate.set_color(dark_color),
                g.edges[(2, 4)].animate.set_color(dark_color),
                g.edges[(2, 3)].animate.set_color(dark_color),
                g.edges[(3, 5)].animate.set_color(dark_color),
                g.edges[(5, 6)].animate.set_color(dark_color),
                )

        self.wait()

        self.play(
                *to_color(WHITE),
                g.vertices[1].animate.set_color(dark_color),
                g.vertices[2].animate.set_color(dark_color),
                g.vertices[4].animate.set_color(dark_color),
                g.vertices[7].animate.set_color(dark_color),
                g.edges[(1, 2)].animate.set_color(dark_color),
                g.edges[(1, 3)].animate.set_color(dark_color),
                g.edges[(1, 4)].animate.set_color(dark_color),
                g.edges[(2, 3)].animate.set_color(dark_color),
                g.edges[(2, 4)].animate.set_color(dark_color),
                g.edges[(3, 4)].animate.set_color(dark_color),
                g.edges[(4, 8)].animate.set_color(dark_color),
                g.edges[(6, 7)].animate.set_color(dark_color),
                )

        sis = Tex(r"\footnotesize proper ind. subg.").set_color(YELLOW)
        sis.move_to(text[3])

        subset = Tex(r"\footnotesize $H \subset G$").set_color(YELLOW)
        subset.move_to(text[7]).shift(UP * 0.024)

        one = Tex(r"\footnotesize one").set_color(YELLOW)
        one.move_to(text[12])

        title2 = Tex("\Large Proper induced subgraph")
        title2.move_to(title)

        self.play(Unwrite(title),
                Write(title2),
                run_time=1.0,
                )

        self.play(Unwrite(text[3]),
                Write(sis),
                run_time=1.0,
                )

        self.play(Unwrite(text[7]),
                Write(subset),
                run_time=1.0,
                )

        self.play(Unwrite(text[12]),
                Write(one),
                run_time=1.0,
                )

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

class PerfectGraph(Scene):
    def construct(self):
        global dark_color

        title = Tex("\Large Perfect graph")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 2.8))

        duration, text = createHighlightedParagraph(r"A graph |$G$| is |perfect| (informally denoted |$G_{\star}$|), if and only if |$$\forall H \subseteq G: \chi(H) = \omega(H)$$|", size=r"\footnotesize", splitBy="|")
        text.next_to(title, 2 * DOWN)

        self.play(Write(text), run_time=duration)

        s = 0.13
        t = 0.10
        lt = { 1 : [-23.077176841641393, -3.6014238478640053, 0],
            2 : [-17.53400032559717, -0.7232673082021435, 0],
            3 : [-17.585547717712963, -6.611537570521636, 0],
            4 : [-11.87839351679463, -3.7000433413833758, 0],
            5 : [-7.810612906695855, -0.14713004947159197, 0],
            6 : [-13.139976458938843, 2.483979391581951, 0],
            7 : [-7.873814738368363, -7.324043997994387, 0],
            8 : [-4.128425988901852, -3.7682916367758734, 0],
            9 : [0.9505618235022141, -7.371686271022552, 0],
            10 : [1.0132341302781502, -0.2549027730859073, 0],
            11 : [-28.505591928163522, -6.575932020162197, 0],
            12 : [-28.452365469134666, -0.5317762398287528, 0],
            13 : [-13.2486886857803, -9.86088904888131, 0]}

        lt_avg_x = 0
        lt_avg_y = 0

        for i in lt:
            lt_avg_x += lt[i][0]
            lt_avg_y += lt[i][1]

        lt_avg_x /= len(lt)
        lt_avg_y /= len(lt)

        for i in lt:
            lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * t, 0)

        vertices = [i + 1 for i in range(13)]
        edges = [(1, 2), (3, 2), (2, 4), (4, 5), (6, 4), (4, 7), (5, 7), (1, 3), (3, 4), (6, 5), (8, 4), (8, 7), (8, 5), (8, 9), (10, 8), (11, 1), (12, 11), (12, 1), (13, 7), (13, 4)]
        g = Graph(vertices, edges, layout=lt).scale(2)
        g.shift(DOWN * 1.3)

        self.play(Write(g))

        self.play(g.animate.shift(LEFT * 1.2))

        coloring = get_coloring(g.edges, one_indexing=True)

        chi = Tex("$\chi(G) = 4$")
        omega = Tex("$\omega(G) = 4$")
        chii = Tex("$\chi(H) = 3$")
        omegaa = Tex("$\omega(H) = 3$")

        def to_color(color):
            return [g.vertices[i].animate.set_color(color) for i in g.vertices] + [g.edges[e].animate.set_color(color) for e in g.edges]

        chi.next_to(g, RIGHT).shift(RIGHT * 0.3 + UP * 0.4)
        omega.next_to(chi, DOWN)
        chii.next_to(g, RIGHT).shift(RIGHT * 0.3 + UP * 0.4)
        omegaa.next_to(chi, DOWN)

        self.play(
            *[g.vertices[v + 1].animate.set_color(coloring[v]) for v in coloring],
            Write(chi),
        )
        self.wait()

        take = (4, 5, 7, 8)

        self.play(
            *to_color(YELLOW),
            *[g.vertices[v].animate.set_color(WHITE) for v in vertices if v not in take],
            *[g.edges[(a, b)].animate.set_color(WHITE) for a, b in edges if a not in take or b not in take],
            Write(omega),
        )
        self.wait()

        take = (11, 12, 1, 3, 2, 4)

        self.play(
            *to_color(WHITE),
            *[g.vertices[v].animate.set_color(dark_color) for v in vertices if v not in take],
            *[g.edges[(a, b)].animate.set_color(dark_color) for a, b in edges if a not in take or b not in take],
        )
        self.wait()

        less_edges = [(take.index(a), take.index(b)) for a, b in edges if a in take and b in take]
        less_coloring = get_coloring(less_edges)

        self.play(
            *[g.vertices[v].animate.set_color(less_coloring[i]) for i, v in enumerate(take)],
            TransformMatchingShapes(chi, chii),
        )
        self.wait()

        takeee = (1, 3, 2)

        self.play(
            *[g.vertices[v].animate.set_color(WHITE) for i, v in enumerate(take)],
            *[g.edges[(a, b)].animate.set_color(YELLOW) for a, b in edges if a in takeee and b in takeee],
            *[g.vertices[v].animate.set_color(YELLOW) for i, v in enumerate(takeee)],
            TransformMatchingShapes(omega, omegaa),
        )
        self.wait()

        fade_all(self)

def getFuzzyVertex(n):
    g = nx.complete_graph(n + 1)
    return Graph.from_networkx(g, layout="spring", layout_scale=0.15).scale(2).rotate(uniform(0, 2 * PI))

def drawFuzzyVertex(g):
    return [Write(g.vertices[0])] + [Write(g.edges[(a, b)]) for a, b in g.edges if a == 0 and b != 0]

class Theorem(Scene):
    def construct(self):

        global dark_color

        title = Tex("\Large Weak perfect graph theorem")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 0.7))

        duration, text = createHighlightedParagraph(r"Graph |$G$ is perfect|, |if and only if| graph |$\bar{G}$ is perfect.", size=r"\footnotesize", splitBy="|")
        text[3].set_color(WHITE)
        text.next_to(title, 2 * DOWN)

        _, text2 = createHighlightedParagraph(r"Graph |$G$ is perfect| $\Rightarrow$ graph |$\bar{G}$ is perfect.", size=r"\footnotesize", splitBy="|")

        self.play(Write(text), run_time=duration)

        self.play(FadeOut(title))

        self.play(
                text.animate.shift(UP * 3.6)
                )

        text2.move_to(text)

        l1 = Line(LEFT * 10, RIGHT * 10).shift(UP * 2.6)
        self.play(Write(l1))
        self.play(TransformMatchingShapes(text, text2))

        a = Ellipse(width=5, height=3,color=WHITE).shift(LEFT * 3.4 + DOWN)
        b = Ellipse(width=5, height=3,color=WHITE).shift(RIGHT * 3.4 + DOWN)

        a_text = Tex(r"$G_{\star}$").move_to(a).shift(UP * 2)
        b_text = Tex(r"$\bar{G}$").move_to(b).shift(UP * 2)

        aa = Ellipse(width=2.5, height=1.6,color=WHITE).shift(LEFT * 3.4 + DOWN * 1.2 + LEFT * 0.6)
        bb = Ellipse(width=2.5, height=1.6,color=WHITE).shift(RIGHT * 3.4 + DOWN * 1.2 + LEFT * 0.6)

        aa_text = Tex(r"$\bar{H}_{\star}$").move_to(a).shift(UP * 0.3 + RIGHT * 1.3)
        bb_text = Tex(r"$H$").move_to(b).shift(UP * 0.3 + RIGHT * 1.3)

        self.play(
                Write(a),
                Write(a_text),
                )

        self.play(
                Write(b),
                Write(b_text),
                )

        self.play(
                Write(bb),
                Write(bb_text),
                )

        self.play(
                Write(aa),
                Write(aa_text),
                )

        aaa_text = Tex("=").next_to(a_text, RIGHT)
        bbb_text = Tex("=").next_to(b_text, RIGHT)

        self.play(
                Transform(aa, a),
                Transform(bb, b),
                FadeIn(aaa_text),
                FadeIn(bbb_text),
                aa_text.animate.next_to(aaa_text, RIGHT),
                bb_text.animate.next_to(bbb_text, RIGHT),
                )

        ra = Rectangle(width = 8, height = 3.9 * 2).shift(LEFT * 4 + DOWN * 1.3).flip(DOWN)
        rb = Rectangle(width = 8, height = 3.9 * 2).shift(RIGHT * 4 + DOWN * 1.3).flip(DOWN)

        l2 = Line(UP * 2.6, DOWN * 10)
        self.play(
                Transform(a, ra, path_arc=-0.9),
                Transform(b, rb, path_arc=-0.9),
                FadeOut(aa),
                FadeOut(bb),
                FadeOut(aaa_text),
                FadeOut(bbb_text),
                FadeOut(aa_text),
                FadeOut(bb_text),
                a_text.animate.shift(UP * 0.9),
                b_text.animate.shift(UP * 0.9),
                )

        self.remove(a)
        self.remove(b)
        self.add(l2)

        seed(1)

        v = [
            Graph([0], []).scale(2).shift(RIGHT * 2 + DOWN * 0.2),
            Graph([0], []).scale(2).shift(RIGHT * 4 + DOWN * -1),
            Graph([0], []).scale(2).shift(RIGHT * 5 + DOWN * 1.1),
        ]

        a = nx.complete_graph(5)
        A = Graph.from_networkx(a, layout="circular", layout_scale=0.4).scale(2)
        A.shift(RIGHT * 2.5 + DOWN * 2.4)
        A.set_color(dark_color)

        self.play(
                Write(v[0]),
                Write(v[1]),
                Write(v[2]),
                Write(A)
                )

        b = nx.complete_graph(3)
        lt = {
                0: v[0].vertices[0].get_center() / 2,
                1: v[1].vertices[0].get_center() / 2,
                2: v[2].vertices[0].get_center() / 2,
                }
        B = Graph.from_networkx(b, layout=lt).scale(2).shift(LEFT * 5.5 + DOWN * 0.1)


        c = nx.complete_graph(5)
        C = Graph.from_networkx(a, layout="circular", layout_scale=0.4).scale(2)
        C.move_to(A).shift(LEFT * 7.3 + DOWN * 0.1)
        C.set_color(dark_color)

        v2 = [
            Graph([0], []).scale(2).move_to(C.vertices[0]).set_color(dark_color),
            Graph([0], []).scale(2).move_to(C.vertices[1]).set_color(dark_color),
            Graph([0], []).scale(2).move_to(C.vertices[2]).set_color(dark_color),
            Graph([0], []).scale(2).move_to(C.vertices[3]).set_color(dark_color),
            Graph([0], []).scale(2).move_to(C.vertices[4]).set_color(dark_color),
        ]

        self.play(
                Write(B),
                Write(v2[0]),
                Write(v2[1]),
                Write(v2[2]),
                Write(v2[3]),
                Write(v2[4]),
                )

        self.play(
                a_text.animate.shift(LEFT * a_text.get_x()),
                l2.animate.shift(RIGHT * 8),
                A.animate.shift(RIGHT * 8),
                b_text.animate.shift(RIGHT * 8),
                v[0].animate.shift(RIGHT * 8),
                v[1].animate.shift(RIGHT * 8),
                v[2].animate.shift(RIGHT * 8),
                B.animate.shift(RIGHT * 6 + DOWN * 0.8),
                v2[0].animate.shift(RIGHT * 1.5 + UP * 1.6),
                v2[1].animate.shift(RIGHT * 1.5 + UP * 1.6),
                v2[2].animate.shift(RIGHT * 1.5 + UP * 1.6),
                v2[3].animate.shift(RIGHT * 1.5 + UP * 1.6),
                v2[4].animate.shift(RIGHT * 1.5 + UP * 1.6),
                run_time=1.5
                )

        q_text = Tex("$Q_1$").move_to(B).shift(RIGHT * 0.3)
        i_text = Tex("$I_1$").move_to(v2[1]).shift(DOWN * 0.8 + LEFT * 0.2)

        self.play(
                Write(q_text),
                )

        self.play(
                Write(i_text),
                )

        qs = [
            Graph.from_networkx(nx.complete_graph(3), layout="circular", layout_scale=0.6).scale(2).rotate(uniform(0, 2 * PI)).shift(LEFT * 1.7 + UP * 0.2),
            Graph.from_networkx(nx.complete_graph(3), layout="circular", layout_scale=0.6).scale(2).rotate(uniform(0, 2 * PI)).shift(RIGHT * 2 + DOWN * 1.5),
            Graph.from_networkx(nx.complete_graph(3), layout="circular", layout_scale=0.6).scale(2).rotate(uniform(0, 2 * PI)).shift(DOWN * .7 + LEFT * 1.6),
            Graph.from_networkx(nx.complete_graph(3), layout="circular", layout_scale=0.6).scale(2).shift(RIGHT * 3 + DOWN * 1),
        ]

        iss = [
            Graph([0, 1, 2, 3, 4], [], layout="circular", layout_scale=0.6).scale(2).rotate(uniform(0, 2 * PI)).shift(RIGHT * 2.7 + DOWN * 1.2).set_color(dark_color),
            Graph([0, 1, 2, 3, 4], [], layout="circular", layout_scale=0.6).scale(2).rotate(uniform(0, 2 * PI)).shift(LEFT * 3).set_color(dark_color),
            Graph([0, 1, 2, 3, 4], [], layout="circular", layout_scale=0.6).scale(2).rotate(uniform(0, 2 * PI)).shift(RIGHT * 3).set_color(dark_color),
            Graph([0, 1, 2, 3, 4], [], layout="circular", layout_scale=0.6).scale(2).shift(LEFT * 3 + DOWN * 1).set_color(dark_color),
        ]

        iss_text = [Tex(f"$I_{str(i + 2) if i != len(iss) - 1 else 't'}$").move_to(iss[i].get_center_of_mass()) for i in range(len(iss))]
        qs_text = [Tex(f"$Q_{str(i + 2) if i != len(iss) - 1 else 't'}$").move_to(qs[i].get_center_of_mass()) for i in range(len(qs))]

        self.play(
                FadeOut(v2[0]),
                FadeOut(v2[1]),
                FadeOut(v2[2]),
                FadeOut(v2[3]),
                FadeOut(v2[4]),
                FadeOut(B),
                FadeOut(q_text),
                FadeOut(i_text),
                Write(qs[0]),
                Write(qs_text[0]),
                Write(iss[0]),
                Write(iss_text[0]),
                )

        for i in range(len(iss) - 1):
            self.play(
                    FadeOut(qs[i]),
                    FadeOut(qs_text[i]),
                    FadeOut(iss[i]),
                    FadeOut(iss_text[i]),
                    FadeIn(qs[i+1]),
                    FadeIn(qs_text[i+1]),
                    FadeIn(iss[i+1]),
                    FadeIn(iss_text[i+1]),
                    )


        self.play(
            FadeOut(qs[len(qs) - 1]),
            FadeOut(qs_text[len(qs) - 1]),
            FadeOut(iss[len(qs) - 1]),
            FadeOut(iss_text[len(qs) - 1]),
            )

        v_label = Tex("$v$")
        v_function = Tex("$f($", "$v$", "$) = 3$")

        v = Graph([0], []).scale(2).move_to(ORIGIN + UP * 0.6)

        self.play(
                Write(v),
                Write(v_label),
                )

        issss = [
            Graph([0, 1, 2, 3], [], layout="spring", layout_scale=0.5).scale(2).rotate(uniform(0, 2 * PI)).shift(LEFT * 4 + DOWN * 0.5 ).set_color(RED),
            Graph([0, 1, 2, 3], [], layout="spring", layout_scale=0.5).scale(2).rotate(uniform(0, 2 * PI)).shift(RIGHT * 4 + DOWN * 0.5).set_color(GREEN),
            Graph([0, 1, 2, 3], [], layout="spring", layout_scale=0.5).scale(2).rotate(uniform(0, 2 * PI)).shift(DOWN * 2.2).set_color(BLUE),
        ]

        issss_text = [
            Tex(f"$I_i$").move_to(issss[0].get_center_of_mass()),
            Tex(f"$I_j$").move_to(issss[1].get_center_of_mass()),
            Tex(f"$I_k$").move_to(issss[2].get_center_of_mass()),
            ]

        self.play(
                v.animate.set_color_by_gradient((GREEN, GREEN, GREEN, RED, BLUE, BLUE, BLUE)),
                Write(issss[0]),
                Write(issss[1]),
                Write(issss[2]),
                Write(issss_text[0]),
                Write(issss_text[1]),
                Write(issss_text[2]),
                )

        v_function.shift(LEFT * v_function[1].get_center() - v_label.get_center())

        self.play(
                Write(v_function[0]),
                Write(v_function[2]),
                )

        self.play(
                FadeOut(v_function[0]),
                FadeOut(v_function[2]),
                FadeOut(v_label),
                FadeOut(issss_text[0]),
                FadeOut(issss_text[1]),
                FadeOut(issss_text[2]),
                )

        L = Graph.from_networkx(nx.complete_graph(3), layout="circular", layout_scale=0.3).scale(2).rotate(PI/6)
        L.move_to(v)

        a_prime_text = Tex(r"$G'_{\star}$").move_to(a_text)

        isssst = [
            [Graph.from_networkx(nx.complete_graph(randint(2, 5)), layout="circular", layout_scale=0.2).scale(1.5).rotate(uniform(0, PI * 2)).move_to(issss[0].vertices[a]) for a in issss[0].vertices],
            [Graph.from_networkx(nx.complete_graph(randint(2, 5)), layout="circular", layout_scale=0.2).scale(1.5).rotate(uniform(0, PI * 2)).move_to(issss[1].vertices[a]) for a in issss[1].vertices],
            [Graph.from_networkx(nx.complete_graph(randint(2, 5)), layout="circular", layout_scale=0.2).scale(1.5).rotate(uniform(0, PI * 2)).move_to(issss[2].vertices[a]) for a in issss[2].vertices],
        ]

        self.play(
                Transform(v, L),
                Transform(a_text, a_prime_text),
                *[Transform(issss[0].vertices[a], b) for a, b in zip(issss[0].vertices, isssst[0])],
                *[Transform(issss[1].vertices[a], b) for a, b in zip(issss[1].vertices, isssst[1])],
                *[Transform(issss[2].vertices[a], b) for a, b in zip(issss[2].vertices, isssst[2])],
                )

        self.play(
                FadeOut(v),
                *[FadeOut(issss[0].vertices[a]) for a in issss[0].vertices],
                *[FadeOut(issss[1].vertices[a]) for a in issss[1].vertices],
                *[FadeOut(issss[2].vertices[a]) for a in issss[2].vertices],
                )

        vertices_1 = Tex(r"$|V(G')|$").shift(UP * 0.7)
        vertices_2 = Tex(r"$=$").shift(UP * 0.7)
        vertices_3 = Tex(r"$t \cdot \alpha(G)$").shift(UP * 0.7)

        self.play(
                Write(vertices_1),
                )

        self.play(
                vertices_1.animate.next_to(vertices_2, LEFT),
                )

        vertices_3.next_to(vertices_2, RIGHT)

        self.play(
                Write(vertices_2),
                Write(vertices_3),
                )

        self.play(
                vertices_1.animate.shift(LEFT * 4.5 + UP),
                vertices_2.animate.shift(LEFT * 4.5 + UP),
                vertices_3.animate.shift(LEFT * 4.5 + UP),
                )

        chi_1 = Tex(r"$\chi(G')$").shift(UP * 0.7)
        chi_2 = Tex(r"$\ge$").shift(UP * 0.7)
        chi_3 = Tex(r"$\frac{|V(G')|}{\alpha(G')}$").shift(UP * 0.7)
        chi_31 = Tex(r"$\frac{|V(G')|}{\alpha(G)}$").shift(UP * 0.7)
        chi_32 = Tex(r"$\frac{t \cdot \alpha(G)}{\alpha(G)}$").shift(UP * 0.7)
        chi_33 = Tex(r"$t$").shift(UP * 0.7)

        self.play(
                Write(chi_1),
                )

        self.play(
                chi_1.animate.next_to(chi_2, LEFT),
                )

        chi_3.next_to(chi_2, RIGHT)
        chi_31.next_to(chi_2, RIGHT)
        chi_32.next_to(chi_2, RIGHT)
        chi_33.next_to(chi_2, RIGHT)

        self.play(
                Write(chi_2),
                Write(chi_3),
                )

        self.remove(chi_3)
        self.play(TransformMatchingShapes(chi_3, chi_31))
        self.remove(chi_31)
        self.play(TransformMatchingShapes(chi_31, chi_32))
        self.remove(chi_32)
        self.play(Transform(chi_32, chi_33))
