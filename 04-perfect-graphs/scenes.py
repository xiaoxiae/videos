from utilities import *

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
    @fade
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


class Complement(Scene):
    @fade
    def construct(self):
        title = Tex("\Large Graph complement")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 2.5))

        duration, text = createHighlightedParagraph("A ","complement"," of a graph", " $G$ ", "is a graph ","$\overline{G}$",", such that ","each two vertices"," are adjacent in ","$\overline{G}$",", if and only if they are ","not adjacent"," in ","$G$",".", size=r"\footnotesize")
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

class CliqueAndIndependentSet(Scene):
    @fade
    def construct(self):

        title = Tex("\Large Clique and independent set")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 2.5))

        duration, text = createHighlightedParagraph("A ","clique"," is a ","subgraph"," of a graph, such that ","each two vertices are adjacent."," Analogically, an ","independent set"," of a graph is a ","set of vertices"," such that ","no two are adjacent.", size=r"\footnotesize")
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

class InducedSubgraph(Scene):
    @fade
    def construct(self):
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

class ChromaticNumber(Scene):
    @fade
    def construct(self):
        title = Tex("\Large Chromatic number")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 2.5))


        duration, text = createHighlightedParagraph( "The ","chromatic number $\chi(G)$"," of a graph ","$G$"," is the ","minimum number of colors"," we can use to color the graph's ","vertices",", such that ","no two adjacent vertices"," have the ","same color.","", size=r"\footnotesize")
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

class Lemma1(Scene):
    @fade
    def construct(self):

        title = Tex("\Large Lemma 1")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 1))

        duration, text = createHighlightedParagraph(r"A graph |$G$| is |perfect|, if and only if it contains an |independent set,| such that each m|aximum clique i|n $G$ |contains a vertex f|rom the set (called a v|ast independent set)|..", size=r"\footnotesize", splitBy="|")
        text.next_to(title, 2 * DOWN)

        self.play(Write(text), run_time=duration)

        self.play(FadeOut(title))
        self.play(text.animate.shift(UP * 3.3))

        l1 = Line(LEFT * 10, RIGHT * 10).next_to(text, DOWN).shift(DOWN * 0.12)

        self.play(Write(l1))

        s = 0.13
        t = 0.13
        lt = {
             1 : [37.07173774694345, 24.513069552487252, 0],
             2 : [42.21727425459074, 27.84392529421318, 0],
             3 : [36.61427318962413, 30.571308404791655, 0],
             4 : [48.00554555844992, 30.421376085990417, 0],
             5 : [53.19846946334912, 27.223933155066213, 0],
             6 : [47.5677835794533, 24.649184796285315, 0],
             7 : [52.438226317756744, 21.183244775108147, 0],
             8 : [59.343089264946734, 28.60991123463918, 0],
             9 : [65.13351173235914, 26.519184930589873, 0],
            10 : [64.1236082388095, 32.48951997100356, 0],
            11 : [55.00129702910227, 33.20668506985356, 0],
            12 : [59.047410413208894, 23.030623084674833, 0],
            13 : [42.182298604016225, 20.996876352207323, 0],
            14 : [42.84315130315794, 34.07480345101175, 0]}

        lt_avg_x = 0
        lt_avg_y = 0

        for i in lt:
            lt_avg_x += lt[i][0]
            lt_avg_y += lt[i][1]

        lt_avg_x /= len(lt)
        lt_avg_y /= len(lt)

        for i in lt:
            lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * t, 0)

        vertices = [i + 1 for i in range(14)]
        edges = [(1 ,  2), (2 ,  3), (1 ,  3), (2 ,  4), (4 ,  5), (6 ,  5), (2 ,  6), (5 ,  7), (6 ,  7), (5 ,  8), (9 ,  8), (10,  9), (10,  8), (11,  4), ( 9, 12), ( 1, 13), ( 3, 14 )]
        g = Graph(vertices, edges, layout=lt).scale(2)
        g.shift(DOWN * 1.1)

        ri = Tex(r"$\Huge\Rightarrow$").shift(UP * 1.2)
        li = Tex(r"$\Huge\Leftarrow$").shift(UP * 1.2)
        self.play(Write(ri))

        self.play(Write(g))

        coloring = get_coloring(g.edges, one_indexing=True)

        self.play(
            *[g.vertices[v + 1].animate.set_color(coloring[v]) for v in coloring],
        )

        take = (1, 2, 3, 8, 9, 10, 5, 6, 7)

        self.play(
            *[g.vertices[v].animate.set_color(dark_color) for v in vertices if v not in take],
            *[g.edges[(a, b)].animate.set_color(dark_color) for a, b in edges if a not in take or b not in take],
            g.edges[(5, 8)].animate.set_color(dark_color),
            g.edges[(2, 6)].animate.set_color(dark_color),
        )

        take2 = (9, 6, 3)

        self.play(
                *[g.vertices[v].animate.set_color(WHITE) for v in vertices if v not in take2 and v in take],
                *[g.vertices[v].animate.set_color(YELLOW) for v in vertices if v in take2],
                *[Circumscribe(g.vertices[v], Circle, fade_out=True) for v in vertices if v in take2],
                )

        self.play(
                FadeOut(g),
                )

        self.play(
                Transform(ri, li),
                )

        wow = Graph([0], []).scale(2).shift(DOWN * 0.3)

        self.play(
                Write(wow)
                )

        s = 0.13
        t = 0.13
        lt = {1 : [15.309880071637778, 13.88267275823302, 0],
            2 : [11.152629866734753, 18.473208465522124, 0],
            3 : [21.533770509017973, 14.062269409469383, 0],
            4 : [27.653696990616425, 14.33728783167967, 0],
            5 : [24.379606335811236, 19.510373877028115, 0],
            6 : [20.128537819154758, 24.02595082531033, 0],
            7 : [13.899970073784655, 24.08450707296808, 0],
            8 : [9.21073459378905, 28.051299475263892, 0],
            9 : [17.983654838438074, 18.871973067254114, 0],
            10 : [26.376723806437678, 27.54463130743147, 0],
            11 : [30.093540665815272, 21.669662723253982, 0],
            12 : [5.894245809297855, 20.83448131841834, 0],
            13 : [6.894245809297855, 13.784481318418347, 0]}

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
        edges = [(1, 2), (1, 3), (4, 3), (4, 5), (3, 5), (6, 5), (6, 7), (2, 7), (8, 7), (6, 9), (10, 6), (11, 5), (2, 9), (1, 9), (2, 12), (2, 13)]

        h = Graph(vertices, edges, layout=lt).scale(2)
        h.shift(DOWN * 1.1)
        h2 = Graph(vertices, edges, layout=lt).scale(2)
        h2.shift(DOWN * 1.1)

        take = (9, 4)

        gt = Tex("$G$").shift(RIGHT * 3.5 + UP * 0.2)
        ht = Tex("$H$").shift(RIGHT * 3.5 + UP * 0.2)
        gt_p = Tex("$G_\star$").shift(RIGHT * 3.5 + UP * 0.2)
        ht_p = Tex("$H_\star$").shift(RIGHT * 3.5 + UP * 0.2)

        self.play(
                Transform(wow, h)
                )

        self.play(
                Write(gt),
                )

        self.play(
                *[h.vertices[i].animate.set_color(YELLOW) for i in take],
                *[Circumscribe(h.vertices[i], Circle) for i in take],
                )

        self.play(
                FadeOut(h.vertices[take[0]]),
                FadeOut(h.vertices[take[1]]),
                )

        self.add(h2)
        self.remove(wow)
        self.play(
                *[FadeOut(h2.vertices[v]) for v in take],
                *[FadeOut(h2.edges[(u, v)]) for u, v in h2.edges if u in take or v in take],
                Transform(gt, ht),
                )

        coloring = get_coloring([(u, v) for u, v in h2.edges], one_indexing=True)
        coloring[4] = RED
        coloring[3] = GREEN
        self.play(
                *[h2.vertices[v + 1].animate.set_color(coloring[v]) for v in coloring if v + 1 not in take],
                Transform(gt, ht_p),
                )

        self.play(
                *[FadeIn(h2.vertices[v].set_color(GREEN)) for v in take],
                *[FadeIn(h2.edges[(u, v)]) for u, v in h2.edges if u in take or v in take],
                Transform(gt, gt_p),
                )


class Lemma2(Scene):
    @fade
    def construct(self):

        title = Tex("\Large Lemma 2")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 1))

        duration, text = createHighlightedParagraph(r"A graph |$G$| is |perfect|, then any graph constructed from |$G$| by |expanding| a vertex is also |perfect|.", size=r"\footnotesize", splitBy="|")
        text.next_to(title, 2 * DOWN)

        self.play(Write(text), run_time=duration)

        self.play(FadeOut(title))
        self.play(text.animate.shift(UP * 3.3))

        l1 = Line(LEFT * 10, RIGHT * 10).next_to(text, DOWN).shift(DOWN * 0.12)

        self.play(Write(l1))

        s = 0.16
        t = 0.16
        lt = { 1: [-12.029991806683347, 4.322127883398239, 0],
            2: [-12.076574068953635, -1.7412590025323897, 0],
            3: [-6.720733101887893, 1.2500538046558693, 0],
            4: [-0.49692711688713764, 1.1491474582769117, 0],
            5: [4.580001507046976, 5.772457897171072, 0],
            6: [2.8472799643190907, -5.4330886795147935, 0],
            7: [10.056125142803856, 5.6897045204928, 0],
            8: [6.62012252897766, -0.5945984711319062, 0],
            9: [10.98788525283437, -4.414560016084881, 0],
            10: [-4.057687247555594, -5.415416431868287, 0],
            11: [-6.465793761818169, 6.59644290985542, 0]}
        lt2 = {1 : [-12.029991806683347, 4.322127883398239, 0],
            2 : [-12.076574068953635, -1.7412590025323897, 0],
            3 : [-6.720733101887893, 1.2500538046558693, 0],
            4 : [-0.8722482728059152, 2.341019980268004, 0],
            5 : [4.580001507046976, 5.772457897171072, 0],
            6 : [2.8472799643190907, -5.4330886795147935, 0],
            7 : [10.056125142803856, 5.6897045204928, 0],
            8 : [6.62012252897766, -0.5945984711319062, 0],
            9 : [10.98788525283437, -4.414560016084881, 0],
            10 : [-4.057687247555594, -5.415416431868287, 0],
            11 : [-6.465793761818169, 6.59644290985542, 0],
            12 : [-1.5366450936795812, -1.6601239954250642, 0],
            13 : [2.318809025203322, 0.06587271750884371, 0]}

        lt_avg_x = 0
        lt_avg_y = 0

        for i in lt:
            lt_avg_x += lt[i][0]
            lt_avg_y += lt[i][1]

        lt_avg_x /= len(lt)
        lt_avg_y /= len(lt)

        for i in lt:
            lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * t, 0)
        for i in lt2:
            lt2[i] = ((lt2[i][0] - lt_avg_x) * s, (lt2[i][1] - lt_avg_y) * t, 0)

        vertices = [i + 1 for i in range(11)]
        vertices2 = [3, 4, 5, 6, 12, 13]
        edges = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 7), (6, 8), (9, 8), (6, 10), (1, 11)]
        edges2 = [(u, v) for u, v in [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 7), (6, 8), (9, 8), (6, 10), (1, 11), (4, 12), (13, 12), (4, 13), (3, 12), (3, 13), (13, 6), (6, 12), (13, 5), (5, 12)] if u in vertices2 and v in vertices2]
        g = Graph(vertices, edges, layout=lt).scale(2)
        g2 = Graph(vertices2, edges2, layout=lt2).scale(2)
        g.shift(DOWN * 0.8)
        g2.shift(g.vertices[3].get_center() - g2.vertices[3].get_center())

        g.vertices[4].set_color(YELLOW)
        g2.vertices[4].set_color(YELLOW)
        g2.vertices[12].set_color(YELLOW)
        g2.vertices[13].set_color(YELLOW)

        self.play(Write(g))
        self.play(Circumscribe(g.vertices[4], Circle))
        group = VGroup(g2.vertices[4], g2.vertices[12],g2.vertices[13])
        self.play(
                FadeTransform(g.vertices[4], group),
                *[FadeOut(g.edges[(u, v)]) for u, v in edges if u == 4 or v == 4],
                *[FadeIn(g2.edges[(u, v)]) for u, v in g2.edges],
                *[FadeIn(g2.vertices[v]) for v in g2.vertices if v not in (4, 12, 13)],
                )

        self.remove(group)
        self.play(
                 FadeOut(g2),
                *[FadeOut(g.edges[(u, v)]) for u, v in edges if u != 4 and v != 4],
                *[FadeOut(g.vertices[v]) for v in vertices if v != 4],
                 )

        g = Graph.from_networkx(nx.complete_graph(1), layout="circular", layout_scale=0.4).scale(2).shift(DOWN * 0.6)
        h = Graph.from_networkx(nx.complete_graph(2), layout="circular", layout_scale=0.4).scale(2).shift(DOWN * 0.6)

        self.play(
                Write(g)
            )

        self.play(
                FadeTransform(g, h)
            )

        coloring = get_coloring(h.edges)
        self.play( *[h.vertices[v].animate.set_color(coloring[v]) for v in coloring])

        self.play(
                FadeOut(h)
            )

        s = 0.16
        t = 0.16
        lt = {1 : [31.8034087985056, 21.180454392536536, 0],
            2 : [34.609439649137066, 15.785461954390827, 0],
            3 : [38.18419657345534, 20.835063248552107, 0],
            4 : [35.213109065971565, 26.23652372171837, 0],
            5 : [44.76233477480106, 20.86973516627854, 0],
            6 : [48.690086325063504, 16.052131276509638, 0],
            7 : [51.07614064122136, 21.579182218042003, 0],
            8 : [47.708359547565784, 26.402544082922805, 0],
            9 : [41.97052991769025, 15.384911836633577, 0],
            10 : [41.26645957589335, 26.325346343930015, 0],
            11 : [57.17698377454542, 22.616073172202213, 0],
            12 : [26.569111783890147, 24.5420949338908, 0],
            13 : [26.563703898682927, 17.828541284261505, 0]}
        lt2 = {1 : [31.8034087985056, 21.180454392536536, 0],
            2 : [34.609439649137066, 15.785461954390827, 0],
            3 : [38.18419657345534, 20.835063248552107, 0],
            4 : [35.213109065971565, 26.23652372171837, 0],
            5 : [44.76233477480106, 20.86973516627854, 0],
            6 : [48.690086325063504, 16.052131276509638, 0],
            7 : [51.07614064122136, 21.579182218042003, 0],
            8 : [47.708359547565784, 26.402544082922805, 0],
            9 : [41.97052991769025, 15.384911836633577, 0],
            10 : [41.26645957589335, 26.325346343930015, 0],
            11 : [57.17698377454542, 22.616073172202213, 0],
            12 : [26.569111783890147, 24.5420949338908, 0],
            13 : [26.563703898682927, 17.828541284261505, 0],
            14 : [53.55910399699539, 26.968055538883853, 0]}
        lt3 = {1 : [31.8034087985056, 21.180454392536536, 0],
            2 : [31.16604926939867, 15.750680233383367, 0],
            3 : [38.18419657345534, 20.835063248552107, 0],
            4 : [35.213109065971565, 26.23652372171837, 0],
            5 : [44.76233477480106, 20.86973516627854, 0],
            6 : [48.690086325063504, 16.052131276509638, 0],
            7 : [51.07614064122136, 21.579182218042003, 0],
            8 : [47.708359547565784, 26.402544082922805, 0],
            9 : [41.97052991769025, 15.384911836633577, 0],
            10 : [41.26645957589335, 26.325346343930015, 0],
            11 : [57.17698377454542, 22.616073172202213, 0],
            12 : [26.569111783890147, 24.5420949338908, 0],
            13 : [26.563703898682927, 17.828541284261505, 0],
            14 : [36.96822307643766, 15.350960722392697, 0]}

        lt_avg_x = 0
        lt_avg_y = 0

        for i in lt:
            lt_avg_x += lt[i][0]
            lt_avg_y += lt[i][1]

        lt_avg_x /= len(lt)
        lt_avg_y /= len(lt)

        for i in lt:
            lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * t, 0)
        for i in lt2:
            lt2[i] = ((lt2[i][0] - lt_avg_x) * s, (lt2[i][1] - lt_avg_y) * t, 0)
        for i in lt3:
            lt3[i] = ((lt3[i][0] - lt_avg_x) * s, (lt3[i][1] - lt_avg_y) * t, 0)

        vertices = [i + 1 for i in range(13)]
        vertices2 = [7, 11, 14]
        vertices3 = [1, 2, 3, 14]
        edges = [(1, 2), (3, 4), (1, 4), (3, 2), (3, 1), (3, 5), (5, 6), (5, 7), (6, 7), (5, 8), (5, 9), (10, 4), (7, 11), (1, 12), (1, 13)]
        edges2 = [(u, v) for u, v in [(1, 2), (3, 4), (1, 4), (3, 2), (3, 1), (3, 5), (5, 6), (5, 7), (6, 7), (5, 8), (5, 9), (10, 4), (7, 11), (1, 12), (1, 13), (11, 14), (7, 14)] if u in vertices2 and v in vertices2]
        edges3 = [(u, v) for u, v in [(1, 2), (3, 4), (1, 4), (3, 2), (3, 1), (3, 5), (5, 6), (5, 7), (6, 7), (5, 8), (5, 9), (10, 4), (7, 11), (1, 12), (1, 13), (11, 14), (1, 14), (2, 14), (3, 14)] if u in vertices3 and v in vertices3]
        g = Graph(vertices, edges, layout=lt).scale(2)
        g.shift(DOWN * 0.8)
        g2 = Graph(vertices2, edges2, layout=lt2).scale(2)
        g2.shift(- g2.vertices[7].get_center() + g.vertices[7].get_center())
        g2.vertices[11].set_color(GREEN)
        g3 = Graph(vertices3, edges3, layout=lt3).scale(2)
        g3.shift(- g3.vertices[1].get_center() + g.vertices[1].get_center())
        g3.vertices[2].set_color(BLUE)

        coloring = get_coloring(g.edges, one_indexing=True)

        v_label = Tex("$v$").next_to(g.vertices[2], LEFT)
        v_label_prime = Tex("$v'$").next_to(g3.vertices[14], RIGHT)

        g_orig = Tex("$G$").shift(RIGHT * 4.6 + DOWN * 1.9)
        g_label = Tex("$G$").shift(RIGHT * 4.6 + DOWN * 1.9)
        g_prime_label = Tex("$G'$").shift(RIGHT * 4.6 + DOWN * 1.9)

        for v in coloring:
            g.vertices[v + 1].set_color(coloring[v])

        self.play(
                Write(g),
                Write(g_label)
                )

        self.play(
                Write(v_label),
                )

        group = VGroup(g3.vertices[2], g3.vertices[14])
        self.play(
                FadeTransform(g.vertices[2], group),
                *[FadeOut(g.edges[(u, v)]) for u, v in edges if u == 2 or v == 2],
                v_label.animate.next_to(g3.vertices[2], LEFT),
                Transform(g_label, g_prime_label),
                *[FadeIn(g3.edges[(u, v)]) for u, v in g3.edges],
                )

        self.play(
                Write(v_label_prime),
                )

        self.play(
                Circumscribe(g3.vertices[14], Circle),
                g3.vertices[14].animate.set_color(YELLOW),
                )

        self.play(
                FadeOut(group),
                *[FadeIn(g.edges[(u, v)]) for u, v in edges if u == 2 or v == 2],
                *[FadeOut(g3.edges[(u, v)]) for u, v in g3.edges],
                FadeIn(g.vertices[2]),
                FadeOut(v_label),
                FadeOut(v_label_prime),
                Transform(g_label, g_orig),
                )

        v_label.next_to(g2.vertices[11], RIGHT)
        v_label_prime.next_to(g2.vertices[14], RIGHT)
        self.play(
                Write(v_label),
                )
        group = VGroup(g2.vertices[11], g2.vertices[14])
        self.play(
                FadeTransform(g.vertices[11], group),
                *[FadeOut(g.edges[(u, v)]) for u, v in edges if u == 11 or v == 11],
                Transform(g_label, g_prime_label),
                *[FadeIn(g2.edges[(u, v)]) for u, v in g2.edges],
                )

        self.play(
                Write(v_label_prime)
                )

        take = (3, 6, 10, 11)
        take2 = (3, 6, 10)
        self.play(
                *[Circumscribe(g.vertices[v], Circle, fade_out=True) for v in vertices if v in take],
                )

        self.play(
                *[g.edges[(u, v)].animate.set_color(dark_color) for u, v in g.edges if u in take2 or v in take2],
                *[g.vertices[v].animate.set_color(dark_color) for v in take2],
                g2.vertices[14].animate.set_color(dark_color),
                *[g2.edges[(u, v)].animate.set_color(dark_color) for u, v in g2.edges if u == 14 or v == 14],
                v_label_prime.animate.set_color(dark_color),
                )

        self.play(
                g2.vertices[11].animate.set_color(RED),
                Circumscribe(g2.vertices[11], Circle, color=RED),
                *[Circumscribe(g.vertices[v], Circle, color=g.vertices[v].color) for v in g.vertices if v not in take2],
                )

        self.play(
                *[g.edges[(u, v)].animate.set_color(WHITE) for u, v in g.edges if u in take2 or v in take2],
                *[g.vertices[v].animate.set_color(GREEN) for v in take2],
                g2.vertices[14].animate.set_color(GREEN),
                *[g2.edges[(u, v)].animate.set_color(WHITE) for u, v in g2.edges if u == 14 or v == 14],
                v_label_prime.animate.set_color(WHITE),
                )


class PerfectGraph(Scene):
    @fade
    def construct(self):

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


class Theorem(Scene):
    @fade
    def construct(self):
        title = Tex("\Large Weak perfect graph theorem")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 0.7))

        duration, text = createHighlightedParagraph(r"Graph |$G$ is perfect|, |if and only if| graph |$\bar{G}$ is perfect.", size=r"\footnotesize", splitBy="|")
        text[3].set_color(WHITE)
        text.next_to(title, 2 * DOWN)

        impl = Tex(r"\footnotesize$\Rightarrow$")

        self.play(Write(text), run_time=duration)

        self.play(FadeOut(title))

        self.play(
                text.animate.shift(UP * 3.6)
                )

        impl.move_to(text[3].get_center())

        l1 = Line(LEFT * 10, RIGHT * 10).shift(UP * 2.6)
        self.play(Write(l1))
        self.play(
                text[0].animate.shift(RIGHT * 0.9),
                text[1].animate.shift(RIGHT * 0.9),
                text[2].animate.shift(RIGHT * 0.9),
                Transform(text[3], impl),
                text[4].animate.shift(LEFT * 0.9),
                text[5].animate.shift(LEFT * 0.9),
                )

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

        ra = Rectangle(width = 8, height = 3.9 * 2).shift(LEFT * 4 + DOWN * 1.3)
        rb = Rectangle(width = 8, height = 3.9 * 2).shift(RIGHT * 4 + DOWN * 1.3)

        l2 = Line(UP * 2.6, DOWN * 10)
        self.play(
                Transform(a, ra),
                Transform(b, rb),
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
        L.vertices[0].set_color(RED)
        L.vertices[1].set_color(GREEN)
        L.vertices[2].set_color(BLUE)

        a_prime_text = Tex(r"$G'_{\star}$").move_to(a_text)

        isssst = [
            [Graph.from_networkx(nx.complete_graph(randint(2, 5)), layout="circular", layout_scale=0.2, vertex_config={0: {"fill_color": RED}}).scale(1.5).rotate(uniform(0, PI * 2)).move_to(issss[0].vertices[a]) for a in issss[0].vertices],
            [Graph.from_networkx(nx.complete_graph(randint(2, 5)), layout="circular", layout_scale=0.2, vertex_config={0: {"fill_color": GREEN}}).scale(1.5).rotate(uniform(0, PI * 2)).move_to(issss[1].vertices[a]) for a in issss[1].vertices],
            [Graph.from_networkx(nx.complete_graph(randint(2, 5)), layout="circular", layout_scale=0.2, vertex_config={0: {"fill_color": BLUE}}).scale(1.5).rotate(uniform(0, PI * 2)).move_to(issss[2].vertices[a]) for a in issss[2].vertices],
        ]

        self.play(
                FadeTransform(v, L),
                Transform(a_text, a_prime_text),
                *[FadeTransform(issss[0].vertices[a], b) for a, b in zip(issss[0].vertices, isssst[0])],
                *[FadeTransform(issss[1].vertices[a], b) for a, b in zip(issss[1].vertices, isssst[1])],
                *[FadeTransform(issss[2].vertices[a], b) for a, b in zip(issss[2].vertices, isssst[2])],
                )

        self.play(
                FadeOut(L),
                *[FadeOut(i) for i in isssst[0]],
                *[FadeOut(i) for i in isssst[1]],
                *[FadeOut(i) for i in isssst[2]],
                FadeOut(a_prime_text),
                FadeOut(a_text),
                )


        up_coeff = UP * 0.9

        vertices_1 = Tex(r"$|V(G'_{\star})|$").shift(up_coeff)
        vertices_2 = Tex(r"$=$").shift(up_coeff)
        vertices_3 = Tex(r"$t \cdot \alpha(G_{\star})$").shift(up_coeff)

        self.play(
                Write(vertices_1),
                )

        v = Graph([0], []).scale(2).move_to(ORIGIN + DOWN * 1.2)
        v.set_color_by_gradient((GREEN, GREEN, GREEN, RED, BLUE, BLUE, BLUE)),

        g = Graph.from_networkx(nx.complete_graph(3), layout="circular", layout_scale=0.3).scale(2).rotate(PI/6)
        g.move_to(ORIGIN + DOWN * 1.4)
        g.vertices[0].set_color(RED)
        g.vertices[1].set_color(GREEN)
        g.vertices[2].set_color(BLUE)

        self.play(Write(v))
        self.play(FadeTransform(v, g))

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
                FadeOut(g)
                )

        chi_1 = Tex(r"$\chi(G'_{\star})$").shift(up_coeff)
        chi_1_copy = Tex(r"$\chi(G'_{\star})$").shift(up_coeff)
        chi_2 = Tex(r"$\ge$").shift(up_coeff)
        chi_2_copy = Tex(r"$\ge$").shift(up_coeff)
        chi_3 = Tex(r"$|V(G'_{\star})|$").shift(up_coeff)
        chi_4 = Tex(r"$\alpha(G'_{\star})$").shift(up_coeff)
        chi_5 = Tex(r"$\alpha(G_{\star})$").shift(up_coeff)
        chi_6 = Tex(r"$t$").shift(up_coeff)
        chi_7 = Tex(r"$t \cdot \alpha(G_{\star})$")
        chi_line = Line(LEFT * (chi_3.width / 2), (chi_3.width / 2) * RIGHT).next_to(chi_2, RIGHT)
        chi_3.next_to(chi_line, UP * 0.5)
        chi_4.next_to(chi_line, DOWN * 0.5)
        chi_5.next_to(chi_line, DOWN * 0.5)
        chi_6.next_to(chi_2, RIGHT)
        chi_7.move_to(chi_3)

        vertices_3_copy = Tex(r"$t \cdot \alpha(G_{\star})$").move_to(vertices_3)

        self.play(
                Write(chi_1),
                )

        s = 0.11
        t = 0.11
        lt = {1 :[19.548217614388534, 21.340577554023504, 0],
            2 :[20.662008110549685, 15.382615667209869, 0],
            3 :[25.300617985296988, 19.402275147120974, 0],
            4 :[30.94295584178832, 16.726260097368442, 0],
            5 :[29.650114385797423, 23.773084129741097, 0],
            6 :[35.16952313921368, 21.143570822050012, 0],
            7 :[26.157058197320413, 13.318633839769966, 0],
            8 :[36.37430103474421, 15.313893361048475, 0],
            9 :[41.333240274979886, 22.35772831721661, 0],
            10: [13.362661329279078, 22.761201537059815, 0],
            11: [14.572572144179105, 17.06814491517606, 0],
            12: [23.748642306908586, 23.920326298309895, 0],
            13: [41.71468063949628, 16.2784339371247, 0]}


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
        edges = [(1, 2), (3, 2), (3, 1), (3, 4), (3, 5), (4, 6), (5, 6), (4, 7), (4, 8), (9, 6), (1, 10), (1, 11), (1, 12), (13, 8)]
        h = Graph(vertices, edges, layout=lt).scale(2)
        h.shift(DOWN * 1.5)

        self.play(Write(h))

        self.play(
                chi_1.animate.next_to(chi_2, LEFT),
                )

        self.play(
                Write(chi_2),
                Write(chi_3),
                Write(chi_line),
                Write(chi_4),
                )

        ins = get_independent_set(edges)
        self.play(
                *[Circumscribe(h.vertices[v], Circle, color=RED) for v in ins],
                *[h.vertices[v].animate.set_color(RED) for v in ins],
                )

        self.play(
                h.vertices[1].animate.set_color(GREEN),
                h.vertices[3].animate.set_color(BLUE),
                h.vertices[4].animate.set_color(GREEN),
                h.vertices[6].animate.set_color(BLUE),
                h.vertices[8].animate.set_color(BLUE),
                )

        self.play(
                TransformMatchingShapes(chi_4, chi_5)
                )

        self.add(vertices_3_copy)
        self.play(
                FadeOut(chi_3),
                TransformMatchingShapes(vertices_3, chi_7)
                )

        self.remove(chi_7)
        self.remove(vertices_3)

        group = VGroup(chi_5, chi_7, chi_line)
        self.play(
                Transform(group, chi_6)
                )

        self.remove(group)
        chi_2_copy.next_to(vertices_2, DOWN * 2.5)
        self.play(
                chi_2.animate.next_to(vertices_2, DOWN * 2.5),
                chi_6.animate.next_to(chi_2_copy, RIGHT),
                chi_1.animate.next_to(chi_2_copy, LEFT),
                FadeOut(h),
                )

        omega_1 = Tex(r"$\omega(G'_{\star})$").shift(up_coeff)
        omega_2 = Tex(r"$\le$").shift(up_coeff)
        omega_22 = Tex(r"$<$").shift(up_coeff)
        omega_3 = Tex(r"$t - 1$").shift(up_coeff)


        s = 0.10
        t = -0.10
        lt = {1 : [135.16695278754875, 21.799871409019467, 0],
            2 : [135.23974320121462, 26.995869054443364, 0],
            3 : [129.97095514212484, 21.872661822685316, 0],
            4 : [130.0437455557907, 27.068659468109214, 0],
            5 : [141.89096109447206, 35.392026752382, 0],
            6 : [135.63477405240312, 34.066543991842444, 0],
            7 : [129.5059688153642, 34.08623598267496, 0],
            8 : [123.54386010179873, 35.40080564245303, 0],
            9 : [122.63066582824992, 29.03885300896691, 0],
            10 : [121.54368309842575, 24.067955925975035, 0],
            11 : [115.63153661766992, 24.123476883046557, 0],
            12 : [112.83175634818338, 28.626425603912605, 0],
            13 : [141.47586853932546, 28.873495345254142, 0],
            14 : [142.5705309790387, 25.095144343663446, 0],
            15 : [146.7726222798732, 23.965170212346607, 0],
            16 : [146.96559967175557, 28.624210346460647, 0],
            17 : [151.1865837303296, 25.307014493285358, 0]}

        lt_avg_x = 0
        lt_avg_y = 0

        for i in lt:
            lt_avg_x += lt[i][0]
            lt_avg_y += lt[i][1]

        lt_avg_x /= len(lt)
        lt_avg_y /= len(lt)

        for i in lt:
            lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * t, 0)

        vertices = [i + 1 for i in range(17)]
        edges = [(1, 2), (3, 4), (4, 2), (3, 1), (1, 4), (3, 2)]
        h = Graph(vertices, edges, layout=lt).scale(2)
        h.shift(DOWN * 1.4)

        q_label = Tex("$Q$").shift(UP * 0.2 + RIGHT * 1.1)

        self.play(
                Write(h),
                Write(q_label),
                )


        self.play(
            h.vertices[1].animate.set_color(BLUE),
            h.vertices[2].animate.set_color(RED),
            h.vertices[3].animate.set_color(LIGHT_BROWN),
            h.vertices[4].animate.set_color_by_gradient((PINK, PINK, GREEN, GREEN)),
            h.vertices[5].animate.set_color(YELLOW),
            h.vertices[6].animate.set_color(YELLOW),
            h.vertices[7].animate.set_color(YELLOW),
            h.vertices[8].animate.set_color(YELLOW),
            h.vertices[13].animate.set_color(PINK),
            h.vertices[14].animate.set_color_by_gradient((PINK, PINK, PINK, RED, BLUE, BLUE, BLUE)),
            h.vertices[15].animate.set_color_by_gradient((RED, RED, BLUE, BLUE)),
            h.vertices[16].animate.set_color_by_gradient((PINK, PINK, BLUE, BLUE)),
            h.vertices[17].animate.set_color(RED),
            h.vertices[9].animate.set_color_by_gradient((LIGHT_BROWN, LIGHT_BROWN, GREEN, GREEN)),
            h.vertices[10].animate.set_color_by_gradient((LIGHT_BROWN, LIGHT_BROWN, GREEN, GREEN)),
            h.vertices[11].animate.set_color(LIGHT_BROWN),
            h.vertices[12].animate.set_color(GREEN),
            )

        self.play(FadeOut(q_label))
        self.play(Write(omega_1))

        self.play(omega_1.animate.next_to(omega_2, LEFT))
        omega_3.next_to(omega_2, RIGHT)
        self.play(
                Write(omega_2),
                Write(omega_3),
                )

        chi_1_copy.move_to(chi_1)
        self.add(chi_1_copy)

        self.play(
                chi_1.animate.next_to(omega_2, RIGHT),
                FadeOut(omega_3),
                Transform(omega_2, omega_22),
                )

        self.play(
                Circumscribe(VGroup(chi_1, omega_2, omega_1))
                )


class Theorem2(Scene):
    @fade
    def construct(self):
        title = Tex("\Large Strong perfect graph theorem")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 1.3))

        duration, text = createHighlightedParagraph(r"Graph |$G$ is perfect|, |if and only if| the |length| of its every |hole| and |antihole| (excluding length 3) is |even| (called a |Berge graph|).", size=r"\footnotesize", splitBy="|")
        text[3].set_color(WHITE)
        text.next_to(title, 2 * DOWN)

        self.play(Write(text), run_time=duration)
        self.play(FadeOut(title))
        self.play(text.animate.shift(UP * 3.7))

        l1 = Line(LEFT * 10, RIGHT * 10).next_to(text, DOWN).shift(DOWN * 0.12)

        self.play(Write(l1))

        s = 0.09
        t = 0.09
        lt = {1 : [-0.13468417754907686, -11.382616759291821, 0],
            2 : [-6.34849625738931, -11.40647453424448, 0],
            3 : [-3.2526218113979337, -6.242787222493782, 0],
            4 : [2.9143602874895524, -5.9709400410760605, 0],
            5 : [-9.769595162673074, -6.223457085564913, 0],
            6 : [-0.5868623771064418, -0.8392016711467933, 0],
            7 : [-6.797128201812322, -0.7758522039253336, 0]}

        lt_avg_x = 0
        lt_avg_y = 0

        for i in lt:
            lt_avg_x += lt[i][0]
            lt_avg_y += lt[i][1]

        lt_avg_x /= len(lt)
        lt_avg_y /= len(lt)

        for i in lt:
            lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * t, 0)

        vertices = [i + 1 for i in range(7)]
        edges = [(1, 2), (3, 1), (4, 1), (3, 2), (5, 2), (3, 6), (6, 7), (4, 6), (5, 7)]
        g = Graph(vertices, edges, layout=lt).scale(2)
        g.shift(DOWN * 1.1 + LEFT * 3)

        s = 0.13
        t = 0.13
        lt = {1 : [11.017918974171332, -6.591774340119114, 0],
            2 : [16.962897427793656, -4.746124663681754, 0],
            3 : [13.13398895475949, -9.70491764147956, 0],
            4 : [13.21453712023058, -3.5349324907386763, 0],
            5 : [16.912690271108087, -8.591990051119353, 0],
            6 : [22.979777239232465, -9.802147496310052, 0],
            7 : [23.059508184569292, -3.6947624028155706, 0]}

        lt_avg_x = 0
        lt_avg_y = 0

        for i in lt:
            lt_avg_x += lt[i][0]
            lt_avg_y += lt[i][1]

        lt_avg_x /= len(lt)
        lt_avg_y /= len(lt)

        for i in lt:
            lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * t, 0)

        vertices = [i + 1 for i in range(7)]
        edges = [(1, 2), (2, 3), (4, 5), (1, 5), (3, 4), (5, 6), (2, 7), (6, 7)]
        h = Graph(vertices, edges, layout=lt).scale(2)
        h.shift(DOWN * 1.1 + RIGHT * 3)

        take_g = (2, 3, 5, 6, 7)
        take_h = (1, 2, 3, 4, 5)

        self.play(Write(g), Write(h))

        hole = Tex("hole").next_to(g, UP)
        antihole = Tex("antihole").next_to(h, UP)

        self.play(
                *[g.vertices[v].animate.set_color(dark_color) for v in g.vertices if v not in take_g],
                *[g.edges[(u, v)].animate.set_color(dark_color) for u, v in g.edges if u not in take_g or v not in take_g],
                *[h.vertices[v].animate.set_color(dark_color) for v in h.vertices if v not in take_h],
                *[h.edges[(u, v)].animate.set_color(dark_color) for u, v in h.edges if u not in take_h or v not in take_h],
                )

        self.play(
                Write(hole),
                Write(antihole),
                )

        self.play(
                FadeOut(g),
                FadeOut(h),
                FadeOut(hole),
                FadeOut(antihole),
                )

        image1 = ImageMobject("proof1.png")
        image1.set_height(5).shift(LEFT * 2.1 + DOWN)
        image2 = ImageMobject("proof2.png")
        image2.set_height(5).shift(RIGHT * 2.1 + DOWN)

        self.play(
                FadeIn(image1),
                FadeIn(image2),
                )

