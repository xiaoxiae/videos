from utilities import *

class BeforeIntro(Scene):
    def construct(self):
        petersen=nx.petersen_graph()
        tutte=nx.tutte_graph()
        complete=nx.complete_graph(8)

        A = Graph.from_networkx(petersen, layout="spring", layout_scale=4)
        B = Graph.from_networkx(tutte, layout="spring", layout_scale=4.5).rotate(PI / 4)
        C = Graph.from_networkx(complete, layout="circular", layout_scale=3)

        self.play(Write(A))
        self.play( A.edges[(0, 1)].animate.set_color(RED),
                    A.edges[(0, 4)].animate.set_color(BLUE), 
                    A.edges[(0, 5)].animate.set_color(GREEN), 
                    A.edges[(1, 2)].animate.set_color(PINK), 
                    A.edges[(1, 6)].animate.set_color(BLUE), 
                    A.edges[(2, 3)].animate.set_color(BLUE), 
                    A.edges[(2, 7)].animate.set_color(GREEN), 
                    A.edges[(3, 4)].animate.set_color(GREEN), 
                    A.edges[(3, 8)].animate.set_color(RED), 
                    A.edges[(4, 9)].animate.set_color(PINK), 
                    A.edges[(5, 7)].animate.set_color(PINK), 
                    A.edges[(5, 8)].animate.set_color(BLUE), 
                    A.edges[(6, 8)].animate.set_color(GREEN), 
                    A.edges[(6, 9)].animate.set_color(RED), 
                    A.edges[(7, 9)].animate.set_color(BLUE))

        self.play(Write(A), rate_func=lambda t: smooth(1-t))
        self.remove(A)

        self.play(Write(B))

        self.play(
            B.edges[(0, 1)].animate.set_color(RED),
            B.edges[(0, 2)].animate.set_color(GREEN),
            B.edges[(0, 3)].animate.set_color(BLUE),
            B.edges[(1, 4)].animate.set_color(GREEN),
            B.edges[(1, 26)].animate.set_color(BLUE),
            B.edges[(2, 10)].animate.set_color(BLUE),
            B.edges[(2, 11)].animate.set_color(RED),
            B.edges[(3, 18)].animate.set_color(RED),
            B.edges[(3, 19)].animate.set_color(GREEN),
            B.edges[(4, 5)].animate.set_color(BLUE),
            B.edges[(4, 33)].animate.set_color(RED),
            B.edges[(5, 6)].animate.set_color(RED),
            B.edges[(5, 29)].animate.set_color(GREEN),
            B.edges[(6, 7)].animate.set_color(BLUE),
            B.edges[(6, 27)].animate.set_color(GREEN),
            B.edges[(7, 8)].animate.set_color(GREEN),
            B.edges[(7, 14)].animate.set_color(RED),
            B.edges[(8, 9)].animate.set_color(RED),
            B.edges[(8, 38)].animate.set_color(BLUE),
            B.edges[(9, 10)].animate.set_color(GREEN),
            B.edges[(9, 37)].animate.set_color(BLUE),
            B.edges[(10, 39)].animate.set_color(RED),
            B.edges[(11, 12)].animate.set_color(BLUE),
            B.edges[(11, 39)].animate.set_color(GREEN),
            B.edges[(12, 13)].animate.set_color(GREEN),
            B.edges[(12, 35)].animate.set_color(RED),
            B.edges[(13, 14)].animate.set_color(BLUE),
            B.edges[(13, 15)].animate.set_color(RED),
            B.edges[(14, 34)].animate.set_color(GREEN),
            B.edges[(15, 16)].animate.set_color(BLUE),
            B.edges[(15, 22)].animate.set_color(GREEN),
            B.edges[(16, 17)].animate.set_color(GREEN),
            B.edges[(16, 44)].animate.set_color(RED),
            B.edges[(17, 18)].animate.set_color(BLUE),
            B.edges[(17, 43)].animate.set_color(RED),
            B.edges[(18, 45)].animate.set_color(GREEN),
            B.edges[(19, 20)].animate.set_color(BLUE),
            B.edges[(19, 45)].animate.set_color(RED),
            B.edges[(20, 21)].animate.set_color(RED),
            B.edges[(20, 41)].animate.set_color(GREEN),
            B.edges[(21, 22)].animate.set_color(BLUE),
            B.edges[(21, 23)].animate.set_color(GREEN),
            B.edges[(22, 40)].animate.set_color(RED),
            B.edges[(23, 24)].animate.set_color(RED),
            B.edges[(23, 27)].animate.set_color(BLUE),
            B.edges[(24, 25)].animate.set_color(GREEN),
            B.edges[(24, 32)].animate.set_color(BLUE),
            B.edges[(25, 26)].animate.set_color(RED),
            B.edges[(25, 31)].animate.set_color(BLUE),
            B.edges[(26, 33)].animate.set_color(GREEN),
            B.edges[(27, 28)].animate.set_color(RED),
            B.edges[(28, 29)].animate.set_color(BLUE),
            B.edges[(28, 32)].animate.set_color(GREEN),
            B.edges[(29, 30)].animate.set_color(RED),
            B.edges[(30, 31)].animate.set_color(GREEN),
            B.edges[(30, 33)].animate.set_color(BLUE),
            B.edges[(31, 32)].animate.set_color(RED),
            B.edges[(34, 35)].animate.set_color(BLUE),
            B.edges[(34, 38)].animate.set_color(RED),
            B.edges[(35, 36)].animate.set_color(GREEN),
            B.edges[(36, 37)].animate.set_color(RED),
            B.edges[(36, 39)].animate.set_color(BLUE),
            B.edges[(37, 38)].animate.set_color(GREEN),
            B.edges[(40, 41)].animate.set_color(BLUE),
            B.edges[(40, 44)].animate.set_color(GREEN),
            B.edges[(41, 42)].animate.set_color(RED),
            B.edges[(42, 43)].animate.set_color(GREEN),
            B.edges[(42, 45)].animate.set_color(BLUE),
            B.edges[(43, 44)].animate.set_color(BLUE))

        self.play(Write(B), rate_func=lambda t: smooth(1-t))
        self.remove(B)

        self.play(Write(C))

        self.play(
            C.edges[(0, 1)].animate.set_color(RED),
            C.edges[(0, 2)].animate.set_color(GREEN),
            C.edges[(0, 3)].animate.set_color(BLUE),
            C.edges[(0, 4)].animate.set_color(ORANGE),
            C.edges[(0, 5)].animate.set_color(PINK),
            C.edges[(0, 6)].animate.set_color(WHITE),
            C.edges[(0, 7)].animate.set_color(GRAY),
            C.edges[(1, 2)].animate.set_color(WHITE),
            C.edges[(1, 3)].animate.set_color(GREEN),
            C.edges[(1, 4)].animate.set_color(GRAY),
            C.edges[(1, 5)].animate.set_color(ORANGE),
            C.edges[(1, 6)].animate.set_color(BLUE),
            C.edges[(1, 7)].animate.set_color(PINK),
            C.edges[(2, 3)].animate.set_color(ORANGE),
            C.edges[(2, 4)].animate.set_color(PINK),
            C.edges[(2, 5)].animate.set_color(BLUE),
            C.edges[(2, 6)].animate.set_color(GRAY),
            C.edges[(2, 7)].animate.set_color(RED),
            C.edges[(3, 4)].animate.set_color(RED),
            C.edges[(3, 5)].animate.set_color(GRAY),
            C.edges[(3, 6)].animate.set_color(PINK),
            C.edges[(3, 7)].animate.set_color(WHITE),
            C.edges[(4, 5)].animate.set_color(WHITE),
            C.edges[(4, 6)].animate.set_color(GREEN),
            C.edges[(4, 7)].animate.set_color(BLUE),
            C.edges[(5, 6)].animate.set_color(RED),
            C.edges[(5, 7)].animate.set_color(GREEN),
            C.edges[(6, 7)].animate.set_color(ORANGE))

        self.play(Write(C), rate_func=lambda t: smooth(1-t))
        self.remove(C)

class Intro(Scene):
    def construct(self):
        title = Tex("\Huge Vizing's Theorem")

        self.play(Write(title))

        self.play(ApplyMethod(title.shift, UP))

        text = Tex("\parbox{23em}{Let $\Delta(G)$ be the maximum degree of a graph $G$. Then the ","number of colors $\chi'$"," needed to ","edge color"," a graph $G$ is either ","$\Delta(G)$"," or ","$\Delta(G) + 1$",".}")
        highlightText(text)

        text.next_to(title, 1.3 * DOWN)

        self.play(Write(text), run_time=4)

class Example(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5]

        edges = [(2, 3), (2,4), (1,4), (1, 5), (3, 4)]
        g = Graph(vertices, edges, layout="circular", layout_scale=3, labels=True)

        self.play(Write(g), run_time=3)

        text = Tex("$\Delta(G) = 3$")
        text.next_to(g.vertices[2], 6 * RIGHT)

        text2 = Tex("$\chi'(G) = \Delta(G)$")
        text2.next_to(text, DOWN)

        self.play(Write(text))

        self.play(
                g.edges[(2, 4)].animate.set_color(RED),
                g.edges[(3, 4)].animate.set_color(GREEN),
                g.edges[(1, 4)].animate.set_color(BLUE),
                g.edges[(1, 5)].animate.set_color(RED),
                g.edges[(2, 3)].animate.set_color(BLUE),
                )

        self.play(Write(text2))

        h = Graph(vertices, edges + [(3, 5), (2, 5)], layout="circular", layout_scale=3, labels=True)

        self.play(
                Write(h.edges[(3, 5)]),
                Write(h.edges[(2, 5)]),
                )

        text3 = Tex("$+\ 1$")
        text3.next_to(text2, RIGHT)

        self.play(
                h.edges[(3, 5)].animate.set_color(YELLOW),
                h.edges[(2, 5)].animate.set_color(GREEN),
                )

        self.play(Write(text3))

class LowerBound(Scene):
    def construct(self):
        title = Tex("\Large Lower bound")

        self.play(Write(title))

        self.play(ApplyMethod(title.shift, 2 * UP))

        N = 7
        vertices = [i + 1 for i in range(N)]

        edges = [(1, i + 1) for i in range(1, N)]
        g = Graph(vertices, edges, layout="circular", layout_scale=1.5)
        g.next_to(title, 3 * DOWN)

        self.play(Write(g))

        self.play(
                g.edges[(1, 2)].animate.set_color(RED),
                g.edges[(1, 3)].animate.set_color(GREEN),
                g.edges[(1, 4)].animate.set_color(BLUE),
                g.edges[(1, 5)].animate.set_color(YELLOW),
                g.edges[(1, 6)].animate.set_color(PINK),
                g.edges[(1, 7)].animate.set_color(GRAY),
                )

        self.play(ApplyMethod(g.shift, 2 * LEFT))

        text = Tex("$\Delta(G)\le \chi'(G)$")
        text.next_to(g, 3 * RIGHT)

        self.play(Write(text))

class UpperBound(Scene):
    def construct(self):
        title = Tex("\Large Upper bound")

        self.play(Write(title))
        self.play(FadeOut(title))


        seed(1)

        e = Ellipse(width=8, height=5,color=WHITE)

        text = Tex("$G$")
        text.shift(UP * 2 + RIGHT * 3.2)

        self.play(Write(e), Write(text))

        vertices = [i for i in range(10)]

        edges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (8, 4), (8, 7), (9, 7), (0, 9)]

        s = 0.3

        lt = {
                1: [(32.7448099360117  -37.5)*s, (24.434327797192754-20.85)*s, 0],
                2: [(30.06934351228568 -37.5)*s, (18.314489982954107-20.85)*s, 0],
                3: [(34.424961294659475-37.5)*s, (18.154452377859204-20.85)*s, 0],
                4: [(38.167198471557086-37.5)*s, (19.72097026586286 -20.85)*s, 0],
                5: [(40.08183144578378 -37.5)*s, (23.144101947056036-20.85)*s, 0],
                6: [(40.25588898889529 -37.5)*s, (26.799310352397896-20.85)*s, 0],
                7: [(43.201193299423025-37.5)*s, (16.591257981420444-20.85)*s, 0],
                8: [(40.16886021733954 -37.5)*s, (15.630618002742203-20.85)*s, 0],
                9: [(45.201193299423025-37.5)*s, (19.200000000000000-20.85)*s, 0],
                0: [(46.201193299423025-37.5)*s, (22.591257981420444-20.85)*s, 0],
                }

        g = Graph(vertices, edges, layout=lt, labels=True, layout_scale=0.2)

        # YUCK!!!!
        for i in g._labels:
            g._labels[i].scale(0)

        replace = Tex("$x$").move_to(g._labels[1]).set_color(BLACK)
        replace2 = Tex("$y$").move_to(g._labels[2]).set_color(BLACK)

        g.edges[(1, 2)].become(DashedLine(g.edges[(1, 2)].get_start(), g.edges[(1, 2)].get_end()))

        self.play(
                Write(g.vertices[1]),
                Write(g.vertices[2]),
                Write(g.edges[(1, 2)], run_time=1),
                FadeIn(replace),
                FadeIn(replace2),
                )

        a = Circle(radius=0.07, fill_opacity=1, color=RED)
        a.next_to(g.vertices[1], UP * 0.7)
        b = Circle(radius=0.07, fill_opacity=1, color=RED)
        b.next_to(g.vertices[2], UP * 0.7)
        self.play(FadeIn(a))
        self.play(FadeIn(b))

        self.play(
                g.edges[(1, 2)].animate.set_color(RED),
                )

        self.play(
                g.edges[(1, 2)].animate.set_color(WHITE),
                b.animate.set_color(PINK),
                )

        g.edges[(1, 3)].set_color(PINK),

        self.play(
                Write(g.vertices[3]),
                Write(g.edges[(1, 3)]),
                )

        c = Circle(radius=0.07, fill_opacity=1, color=BLUE)
        c.next_to(g.vertices[3], UP * 0.7)
        self.play(FadeIn(c))

        g.edges[(1, 4)].set_color(BLUE),
        g.edges[(1, 5)].set_color(GREEN),

        d = Circle(radius=0.07, fill_opacity=1, color=GREEN)
        d.next_to(g.vertices[4], UP * 0.7)

        e = Tex("?").scale(0.5)
        e.next_to(g.vertices[5], UP * 0.7)

        self.play(
                Write(g.vertices[4]),
                Write(g.edges[(1, 4)]),
                FadeIn(d),
                )

        self.play(
                Write(g.vertices[5]),
                Write(g.edges[(1, 5)]),
                FadeIn(e),
                )

        ee = Circle(radius=0.07, fill_opacity=1, color=RED)
        ee.next_to(g.vertices[5], UP * 0.7)

        case1 = Tex("\Large Case I")
        case1.shift(UP * 2.7 + LEFT * 4.8)

        self.play(
                Write(case1)
                )

        self.play(
                Transform(e, ee),
                )

        self.play(
                a.animate.set_color(GREEN),
                e.animate.set_color(GREEN),
                g.edges[(1, 5)].animate.set_color(RED),
                )

        self.play(
                a.animate.set_color(BLUE),
                d.animate.set_color(BLUE),
                g.edges[(1, 4)].animate.set_color(GREEN),
                )

        self.play(
                a.animate.set_color(PINK),
                c.animate.set_color(PINK),
                g.edges[(1, 3)].animate.set_color(BLUE),
                )

        self.play(
                a.animate.set_color(GRAY),
                b.animate.set_color(GRAY),
                g.edges[(1, 2)].animate.set_color(PINK),
                )

        eee = Tex("?").scale(0.5)
        eee.next_to(g.vertices[5], UP * 0.7)

        self.play(
                a.animate.set_color(RED),
                b.animate.set_color(PINK),
                c.animate.set_color(BLUE),
                d.animate.set_color(GREEN),
                Transform(e, eee),
                g.edges[(1, 2)].animate.set_color(WHITE),
                g.edges[(1, 3)].animate.set_color(PINK),
                g.edges[(1, 4)].animate.set_color(BLUE),
                g.edges[(1, 5)].animate.set_color(GREEN),
                )

        case2 = Tex("\Large I")
        case2.next_to(case1, RIGHT * 0.2)


        self.play(
            Write(case2)
        )

        ee.set_color(BLUE)
        self.play(
            Transform(e, ee),
        )


        self.play(
            Indicate(e),
            Indicate(g.edges[(1, 4)]),
        )

        replace3 = Tex("$v$").move_to(g._labels[5]).set_color(BLACK)
        replace4 = Tex("$w$").move_to(g._labels[4]).set_color(BLACK)

        g.edges[(8, 4)].set_color(RED)
        g.edges[(8, 7)].set_color(BLUE)
        g.edges[(9, 7)].set_color(RED)
        g.edges[(0, 9)].set_color(BLUE)

        self.play(
                FadeIn(replace3),
                FadeIn(replace4),
                )

        self.play(
                FadeIn(g.edges[(8, 4)]),
                FadeIn(g.vertices[7]),
                FadeIn(g.edges[(8, 7)]),
                FadeIn(g.vertices[8]),
                FadeIn(g.edges[(9, 7)]),
                FadeIn(g.edges[(0, 9)]),
                FadeIn(g.vertices[9]),
                FadeIn(g.vertices[0]),
                )

        self.play(
                g.edges[(1, 4)].animate.set_color(RED), 
                g.edges[(8, 4)].animate.set_color(BLUE), 
                g.edges[(8, 7)].animate.set_color(RED),
                g.edges[(9, 7)].animate.set_color(BLUE),
                g.edges[(0, 9)].animate.set_color(RED),
                a.animate.set_color(BLUE),
                )

        self.play(
                Indicate(g.vertices[4]), 
                Indicate(g.vertices[7]), 
                Indicate(g.vertices[8]), 
                Indicate(g.vertices[9]), 
                )

        self.play(
                Indicate(g.vertices[1]), 
                )

        self.play(
                Indicate(g.vertices[0]), 
                )

        self.play(FadeOut(case2))

        self.play(
                a.animate.set_color(PINK),
                c.animate.set_color(PINK),
                g.edges[(1, 3)].animate.set_color(BLUE),
                )

        self.play(
                a.animate.set_color(GRAY),
                b.animate.set_color(GRAY),
                g.edges[(1, 2)].animate.set_color(PINK),
                )
