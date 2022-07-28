from utilities import *

class Intro(MovingCameraScene):
    def construct(self):
        bsat = Tex("\Huge Boolean Satisfiability Problem").scale(0.7)

        sat = Tex("\Huge SAT").scale(2)
        sat_cp = sat.copy()

        p = Tex(r"\Huge \textbf{P}").scale(1.3)
        np = Tex(r"\Huge \textbf{NP}").scale(1.3)

        p_np = VGroup(p, np).arrange(buff=1.5).shift(UP * 0.6)

        self.play(Write(bsat), run_time=1.5)

        self.play(
                AnimationGroup(
                    AnimationGroup(
                        FadeOut(bsat[0][0:7], shift=LEFT * 0.25),
                        FadeOut(bsat[0][10:], shift=RIGHT * 0.25),
                    ),
                    AnimationGroup(
                        FadeTransform(bsat[0][7], sat[0][0]),
                        Transform(bsat[0][8], sat[0][1]),
                        Transform(bsat[0][9], sat[0][2]),
                    ),
                    lag_ratio=0.5,
                )
            )

        for mobject in self.mobjects:
            self.remove(mobject)

        sat.become(sat_cp)

        self.add(sat)

        sat_to_surround = sat.copy().shift(DOWN * 1.1).scale(1/4)

        p_circle = Circle(color=WHITE).surround(p, buffer_factor=1.45)
        np_circle = Circle(color=WHITE).surround(p_np + VGroup(sat_to_surround), buffer_factor=1.15)

        self.play(
                AnimationGroup(
                    Transform(sat, sat_to_surround),
                    AnimationGroup(
                        Write(p_np),
                        Write(p_circle),
                        Write(np_circle),
                        lag_ratio=0.1,
                    ),
                lag_ratio=0.6))

        self.play(
                self.camera.frame.animate.scale(1/3).move_to(sat),
                p_circle.animate.shift(UP + LEFT),
                p.animate.shift(UP + LEFT),
                np.animate.shift(UP + RIGHT),
                np_circle.animate.scale(2),
                sat.animate.scale(1/2)
                )

        problems = VGroup(*map(Tex, ["graph\n\ncoloring", "knapsack", "hamiltonian\n\ncycle", "subset\n\nsum"]))

        directions = [LEFT * 1.5, UP, RIGHT * 1.5, DOWN]
        arrows = VGroup()

        # TODO: tohle lépe
        for i, problem in enumerate(problems):
            problem.scale(1/3).move_to(sat).shift((directions[i] + directions[i - 1]) * 0.7)
            arrow = Arrow(start=problem.get_center(), end=sat.get_center(), buff=0.45)
            arrows.add(arrow)

        self.play(
            AnimationGroup(
                AnimationGroup(*[FadeIn(problem, run_time=1, shift=(sat.get_center() - problem.get_center()) * 0.2) for problem in problems], lag_ratio=0.25),
                AnimationGroup(*[FadeIn(arrow, shift=(sat.get_center() - arrow.get_center()) * 0.2) for arrow in arrows], lag_ratio=0.25),
                lag_ratio=0.0,
            )
        )

        turtles = VGroup(*[SVGMobject("assets/turtle.svg").scale(0.09).next_to(problem, UP, buff=0.075) for problem in problems])
        rabbit = SVGMobject("assets/rabbit.svg").scale(0.135).next_to(sat, UP, buff=0.075)

        self.camera.frame.save_state()

        self.play(
            *[FadeIn(turtle, shift=0.02 * UP) for turtle in turtles],
            FadeIn(rabbit, shift=0.02 * UP),
        )

        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{booktabs}")
        myTemplate.add_to_preamble(r"\usepackage{xcolor}")

        table = Tex(r"""
\renewcommand\arraystretch{1.3}
\begin{table}[ht]
\centering
\begin{tabular}[t]{lll}
\toprule
& \textbf{exact} &\textbf{approximation} \\
\midrule
\textbf{running time}&$\mathcal{O}(\mathrm{exponential})$&$\mathcal{O}(\mathrm{polynomial})$\\
\textbf{solution}&optimal&almost optimal\\
\bottomrule
\end{tabular}
\end{table}%
""", tex_template=myTemplate).scale(1/3).move_to(sat).shift(DOWN * 0.2)

        d = 17
        table[0][48-d:62-d].set_color(RED)
        table[0][62-d:75-d].set_color(GREEN)
        table[0][83-d:90-d].set_color(GREEN)
        table[0][90-d:103-d].set_color(RED)

        self.play(
            self.camera.frame.animate.restore(),
            AnimationGroup(
                AnimationGroup(FadeOut(problems), FadeOut(arrows), FadeOut(turtles), FadeOut(rabbit)),
                AnimationGroup(sat.animate.next_to(table, UP), FadeIn(table, shift=UP * 0.3)),
                lag_ratio=0.5,
            )
        )

        self.play(Circumscribe(VGroup(table[0][48-d:62-d], table[0][83-d:90-d]), color=YELLOW, stroke_width=0.7, buff=0.05, time_width=0.5, run_time=1))
        self.play(Circumscribe(VGroup(table[0][62-d:75-d], table[0][90-d:103-d]), color=YELLOW, stroke_width=0.7, buff=0.05, time_width=0.5, run_time=1))

        lp = Tex(r"\Large LP-SAT \\ \vspace{0.3em} \normalsize \textit{also random, based on \\ linear programming}").scale(1/3).move_to(sat).shift(RIGHT + DOWN)
        rand = Tex(r"\Large RAND-SAT \\ \vspace{0.3em} \normalsize \textit{assignment is \\ entirely random}").scale(1/3).move_to(sat).shift(LEFT + DOWN)

        self.play(FadeOut(table))

        best_sat = Tex(r"\Huge BEST").scale(1/4)
        dash = Tex("\Huge -").scale(1/4)
        new_sat = sat.copy()
        VGroup(best_sat, dash, new_sat).arrange(buff=0.07).move_to(sat)

        self.play(
                FadeIn(lp, shift=UP * 0.3),
                FadeIn(rand, shift=UP * 0.3),
                sat.animate.move_to(new_sat),
                FadeIn(best_sat, shift=LEFT * 0.1),
                FadeIn(dash, shift=LEFT * 0.1),
                )

SIZE = 0.75

class RANDSATText(MovingCameraScene):
    @fade
    def construct(self):
        sat = Tex(r"\Huge RAND-SAT").scale(SIZE)

        self.play(Write(sat))


class LPSATText(MovingCameraScene):
    @fade
    def construct(self):
        sat = Tex(r"\Huge LP-SAT").scale(SIZE)

        self.play(Write(sat))


class SATusingLPText(MovingCameraScene):
    @fade
    def construct(self):
        satulp = Tex(r"\Huge MAX-SAT using LP").scale(SIZE)

        self.play(Write(satulp))

class RelaxedSATusingLPText(MovingCameraScene):
    @fade
    def construct(self):
        satulp = Tex(r"\Huge Relaxed MAX-SAT using LP").scale(SIZE)

        self.play(Write(satulp))

class LPExampleText(MovingCameraScene):
    @fade
    def construct(self):
        example = Tex(r"\Huge Example").scale(SIZE)

        self.play(Write(example))


class CrossText(MovingCameraScene):
    @fade
    def construct(self):
        cross = Tex(r"\Huge $$\times$$").set_color(RED).scale(6)

        self.play(FadeIn(cross))

        text = Tex(r"Integer Linear Programming is \textbf{NP-hard}.")
        text[0][26:26+7].set_color(RED)

        new_cross = cross.copy().scale(0.5)

        VGroup(new_cross, text).arrange(DOWN, buff=1)

        self.play(Transform(cross, new_cross))
        self.play(Write(text, run_time=1.5))


class SAT(MovingCameraScene):
    def construct(self):
        sat = Tex(r"\Huge SAT")

        self.play(Write(sat))

        sat.save_state()

        example = Tex(r"$$(a \lor \lnot b \lor \lnot c) \land (\lnot a \lor d \lor \lnot e) \land (e \lor f)$$").shift(DOWN * 0.5).scale(1.25)
        example[0][9].scale(0.75)
        example[0][19].scale(0.75)

        self.play(
            sat.animate.shift(UP * 2),
            FadeIn(example, shift=UP * 0.5),
        )

        def straight_brace_points(p1, p2):
            p2[1] = p1[1]
            return p1, p2

        braces = VGroup(
            BraceBetweenPoints(*straight_brace_points(example[0][0].get_center(), example[0][8].get_center())),
            BraceBetweenPoints(*straight_brace_points(example[0][10].get_center(), example[0][18].get_center())),
            BraceBetweenPoints(*straight_brace_points(example[0][20].get_center(), example[0][24].get_center())),
        ).shift(DOWN * 0.3)

        for brace in braces:
            brace.add(Tex("clause").next_to(brace, DOWN))

        self.play(AnimationGroup(*[FadeIn(brace, shift=UP * 0.1) for brace in braces], lag_ratio=0.1))

        groups = Tex(r"$$[a, \lnot b, \lnot c] \quad [\lnot a, d, \lnot e] \quad [e, f]$$").move_to(example).scale(1.6)

        variable_pos_example = [[1], [3, 4], [6, 7], [11, 12], [14], [16, 17], [21], [23]]
        variable_pos_groups = [[1], [3, 4], [6, 7], [10, 11], [13], [15, 16], [19], [21]]

        all_variable_pos_example = sum(variable_pos_example, [])
        all_variable_pos_groups = sum(variable_pos_groups, [])

        for q in [1, 2]:
            self.play(
                AnimationGroup(
                *[VGroup(*[example[0][ii] for ii in i]).animate.set_color(RED if len(i) == 2 else GREEN) for i in variable_pos_example if len(i) == q],
                lag_ratio=0.1,
                ),
                AnimationGroup(
                *[Circumscribe(VGroup(*[example[0][ii] for ii in i]), color=RED if len(i) == 2 else GREEN, shape=Circle, buff=0.05, stroke_width=1.5) for i in variable_pos_example if len(i) == q],
                lag_ratio=0.1,
                )
            )

        for i in variable_pos_groups:
            VGroup(*[groups[0][ii] for ii in i]).set_color(RED if len(i) == 2 else GREEN)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(braces),
                    *[FadeOut(s) for i, s in enumerate(example[0]) if i not in all_variable_pos_example],
                ),
                AnimationGroup(
                    *[ReplacementTransform(VGroup(*[example[0][ii] for ii in i]), VGroup(*[groups[0][jj] for jj in j])) for i, j in zip(variable_pos_example, variable_pos_groups)]
                ),
                AnimationGroup(
                    *[FadeIn(s) for i, s in enumerate(groups[0]) if i not in all_variable_pos_groups],
                ),
                lag_ratio=0.5
            )
        )

        ade = [variable_pos_groups[0], variable_pos_groups[4], variable_pos_groups[6]]
        not_ae = [variable_pos_groups[3], variable_pos_groups[5]]
        otherslmao = [variable_pos_groups[1], variable_pos_groups[2], variable_pos_groups[7]]

        equals = Tex("$=$").rotate(PI / 2).scale(0)
        one = Tex("$1$").scale(0.85).next_to(equals, DOWN, buff=0.15)
        zero = Tex("$0$").scale(0.85).next_to(equals, DOWN, buff=0.15)
        q = Tex("$*$").scale(0.85).next_to(equals, DOWN, buff=0.20)

        combined = VGroup(equals, one)
        combined_zero = VGroup(equals, zero)
        combined_q = VGroup(equals, q)

        lmao = [combined.copy().next_to(VGroup(*[groups[0][j] for j in i]), DOWN, buff=0.2) for i in ade]
        lmao2 = [combined_zero.copy().next_to(VGroup(*[groups[0][j] for j in i]), DOWN, buff=0.2) for i in not_ae]
        lmao3 = [combined_q.copy().next_to(VGroup(*[groups[0][j] for j in i]), DOWN, buff=0.2) for i in otherslmao]

        for o in lmao3:
            o.align_to(lmao2[0], UP)

        combined_copies = VGroup(lmao[0], lmao3[0], lmao3[1], lmao2[0], lmao[1], lmao2[1], lmao[2], lmao3[2])

        self.play(
            AnimationGroup(
                *[FadeIn(combined_copy, shift=DOWN * 0.2) for combined_copy in combined_copies],
                lag_ratio=0.05,
            )
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(groups[0]),
                    FadeOut(combined_copies),
                ),
                sat.animate.shift(DOWN * 1.5),
                lag_ratio=0.5,
            )
        )

        max_sat = Tex(r"\Huge MAX", color=BLUE)
        dash = Tex("\Huge -", color=BLUE)

        new_sat = sat.copy()
        ms = VGroup(max_sat, dash, new_sat).arrange(buff=0.3).move_to(sat)
        dash.shift(LEFT * 0.08)

        self.play(
            sat.animate.move_to(new_sat),
            FadeIn(max_sat, shift=LEFT * 0.5),
            FadeIn(dash, shift=LEFT * 0.5),
        )

        goal = Tex(r"Maximize the number of satisfied clauses.").next_to(ms, DOWN, buff=0.5)
        goal[0][0:8].set_color(BLUE)

        self.play(FadeIn(goal, shift=DOWN * 0.5))


class RANDSATFormal(MovingCameraScene):
    def construct(self):
        example = Tex(r"$$(a \lor \lnot b \lor \lnot c) \land (\lnot a \lor d \lor \lnot e) \land (e \lor f)$$").scale(1.25)
        variable_pos_example = [[1], [3, 4], [6, 7], [11, 12], [14], [16, 17], [21], [23]]
        for i in variable_pos_example:
            VGroup(*[example[0][ii] for ii in i]).set_color(RED if len(i) == 2 else GREEN)

        self.play(FadeIn(example, shift=DOWN * 0.2))

        brace = BraceBetweenPoints(example[0][0].get_center(), example[0][8].get_center()).shift(DOWN * 0.3)

        k = Tex("$$k = 3$$").next_to(brace, DOWN)

        self.camera.frame.save_state()

        self.play(
            FadeOut(example[0][9:]),
            FadeIn(VGroup(brace, k), shift=DOWN * 0.2),
            self.camera.frame.animate.move_to(VGroup(example[0][:9], brace, k)).scale(1/2),
        )

        equals = Tex("--").rotate(PI / 2).scale(0.7)
        one = Tex("$1$").scale(0.85).next_to(equals, UP, buff=0.2)
        zero = Tex("$0$").scale(0.85).next_to(equals, UP, buff=0.2)

        combined_one = VGroup(equals, one)
        combined_zero = VGroup(equals, zero)

        combined_copies = VGroup(
            combined_zero.copy().next_to(VGroup(*[example[0][i] for i in variable_pos_example[0]]), UP),
            combined_one.copy().next_to(VGroup(*[example[0][i] for i in variable_pos_example[1]]), UP),
            combined_one.copy().next_to(VGroup(*[example[0][i] for i in variable_pos_example[2]]), UP),
        )

        for i, c in enumerate(combined_copies[1:]):
            c.align_to(combined_copies[i], DOWN)

        combined_copies.shift(UP * 0.1)

        self.play(
            AnimationGroup(
                *[FadeIn(combined_copy, shift=UP * 0.2) for combined_copy in combined_copies],
                lag_ratio=0.05,
            ),
            self.camera.frame.animate.move_to(VGroup(example[0][:9], brace, k, combined_copies)),
        )

        psat = Tex(r"$$p_{\lnot \text{sat}} = \left(\frac{1}{2}\right)^k$$").move_to(k).scale(0.55)

        self.play(
            FadeOut(k, shift=DOWN * 0.3),
            FadeIn(psat, shift=DOWN * 0.3),
        )

        sat = Tex(r"$$p_{\text{sat}} = 1 - \left(\frac{1}{2}\right)^k$$").move_to(k).scale(0.55)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(psat[0][1]),
                ),
                AnimationGroup(
                    AnimationGroup(
                        ReplacementTransform(psat[0][0], sat[0][0]),
                        ReplacementTransform(psat[0][2:6], sat[0][1:5]),
                        ReplacementTransform(psat[0][6:], sat[0][7:]),
                    ),
                    AnimationGroup(
                        FadeIn(sat[0][5:7]),
                    ),
                    lag_ratio=0.25,
                ),
                lag_ratio=0.75,
            )
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(combined_copies),
                    FadeOut(sat),
                    FadeOut(brace),
                    self.camera.frame.animate.restore(),
                ),
                FadeIn(example[0][9:]),
                lag_ratio=0.3,
            )
        )

        prob = Tex(r"$$\mathbb{E}\left[\text{\% of sat. clauses}\right] \ge 1/2$$").next_to(example, DOWN, buff=1.0).scale(1.25)

        braces = VGroup(
            BraceBetweenPoints(example[0][0].get_center(), example[0][8].get_center(), UP),
            BraceBetweenPoints(example[0][10].get_center(), example[0][18].get_center(), UP),
            BraceBetweenPoints(example[0][20].get_center(), example[0][24].get_center(), UP),
        ).shift(UP * 0.3)

        for i, brace in enumerate(braces):
            brace.add(Tex(r"$$\ge 1/2$$").scale(0.75).next_to(brace, UP))

        self.play(AnimationGroup(*[FadeIn(brace, shift=UP * 0.1) for brace in braces], lag_ratio=0.1))

        self.play(
            FadeIn(prob, shift=DOWN * 0.3),
            self.camera.frame.animate.move_to(VGroup(prob, example, braces)),
        )



class LPSAT(MovingCameraScene):
    def construct(self):
        lpsat = Tex(r"LP-SAT").scale(3)

        lp = Tex("Linear Programming").scale(2)

        self.play(Write(lpsat))

        self.play(
            AnimationGroup(
                FadeOut(lpsat[0][2:]),
                TransformMatchingShapes(lpsat[0][0:2], lp),
                lag_ratio=0.5,
            ),
        )

        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{amsmath}")

        lp_table = VGroup(
                Tex(r"{\bf Variables:}"),
                Tex(r"$$a, b, c, d \in \mathbb{R}$$"),
                Tex(r"{\bf Inequalities:}"),
                Tex(r"""\begin{flalign*}
& \mathbin{\hphantom{-}}500a+10b+230c+10d \le \hphantom{5}50 \\
& \mathbin{\hphantom{-}}\hphantom{5}10a+\hphantom{1}2b-\hphantom{10}7c+\hphantom{10}d \le 125 \\
& \hphantom{5}-50a\mathbin{\hphantom{+}}\hphantom{12b}-\hphantom{1}15c\mathbin{\hphantom{+}}\hphantom{10d} \le 500 &
\end{flalign*}""", tex_template=myTemplate),
                Tex(r"{\bf Maximize:}"),
                Tex(r"18a + 2b + 10c + 7d"),
                )

        lp_table.arrange_in_grid(cols=2, col_alignments="rl", row_alignments="uuu", buff=(0.5, 0.65))

        new_lp = lp.copy().scale(0.75)
        VGroup(new_lp, lp_table).arrange(DOWN, buff=1)

        self.play(Transform(lp, new_lp))

        self.play(Write(lp_table[0:2], run_time=1.25))
        self.play(Write(lp_table[2:4], run_time=2.75))
        self.play(Write(lp_table[4:6], run_time=1.25))


class Proof(MovingCameraScene):
    #@fade
    def construct(self):
        # TODO: intro

        tex_ag = Tex(r"$$\prod_{i = 1}^{n} \sqrt[n]{a_i} \le \frac{1}{n} \sum_{i = 1}^{n} a_i$$")

        sr_ag = SurroundingRectangle(tex_ag, buff=0.25, color=WHITE)

        text_ag = Tex("A")

        tex_jen = Tex(
            r"$f$ concave on $[0, 1]$, $f(0) = a$, $f(1) = a + b$",
            r"$$\implies$$",
            r"$$\forall x \in \left[0, 1\right]: f(x) \le a + bx$$"
        )
        tex_jen[1].rotate(-PI / 2).scale(0.85)

        sr_jen = SurroundingRectangle(tex_jen, buff=0.35, color=WHITE)

        text_jen = Tex("B")

        ag = VGroup(tex_ag, sr_ag)
        jen = VGroup(tex_jen, sr_jen)

        self.play(Write(ag[0], run_time=2))
        self.play(Write(ag[1]))

        self.play(
            Circumscribe(ag[0][0][0:10], color=RED),
            ag[0][0][0:10].animate.set_color(RED),
        )

        self.play(
            Circumscribe(ag[0][0][11:], color=BLUE),
            ag[0][0][11:].animate.set_color(BLUE),
        )

        copies = VGroup(
            ag.copy().set_height(1.25),
            jen.copy().set_height(1.25),
        ).arrange().align_to(config.top, UP).shift(DOWN * 0.4)

        text_ag.move_to(copies[0])
        copies[0][0].set_opacity(0.2).set_color(WHITE)
        self.play(
            Succession(
                Transform(ag, copies[0]),
                Write(text_ag),
            )
        )

        ag.add(text_ag)

        self.play(
            AnimationGroup(
                Write(tex_jen[0], run_time=1.5),
                FadeIn(tex_jen[1], shift=DOWN * 0.25),
                Write(tex_jen[2], run_time=1.5),
                lag_ratio=0.7,
            )
        )

        self.play(Write(sr_jen))

        text_jen.move_to(copies[1])
        self.play(
            Transform(jen, copies[1]),
        )

        def f1(x):
            return (1-x)**4+2*(1-x)**2-4*(1-x)+2

        def f2(x):
            return x+1

        axes = Axes(
                x_range=[-0.25, 1.15],
                y_range=[0, 3],
                x_axis_config={
                    "numbers_to_include": [0, 1],
                    "numbers_to_exclude": None,
                    },
                x_length=5,
                y_length=3,
                )
        labels = axes.get_axis_labels(x_label="x", y_label="y")
        labels[0].scale(0.8)
        labels[1].scale(0.8)

        d1 = Dot().move_to(axes.coords_to_point(*(0, 1))).set_z_index(1)
        d2 = Dot().move_to(axes.coords_to_point(*(1, 2))).set_z_index(1)
        d3 = Dot().move_to(axes.coords_to_point(*(0, 2))).set_z_index(1)

        g1 = axes.plot(f1, color=RED)
        g2 = axes.plot(f2, color=BLUE, x_range=[0, 1])

        a = Tex("$a$").scale(0.4).next_to(d1, LEFT, buff=0.1)
        apb = Tex("$a+b$").scale(0.4).next_to(d3, RIGHT, buff=0.1)

        l1 = axes.get_graph_label(g1, "f(x)", x_val=0.85, direction=DOWN + RIGHT, buff=0.1).scale(0.7)
        l2 = axes.get_graph_label(g2, "a + bx", x_val=0.7, direction=UP, buff=0.2).scale(0.7)

        g = VGroup(axes, labels, g1, g2, d1, d2, l1, l2, a, apb).shift(DOWN * 0.65)

        self.play(
            AnimationGroup(
                AnimationGroup(FadeIn(axes), FadeIn(labels)),
                AnimationGroup(
                    Write(d1),
                    Write(d2),
                    Write(a),
                    Write(apb),
                    AnimationGroup(AnimationGroup(Write(g1), Write(l1)), AnimationGroup(Write(g2), Write(l2)), lag_ratio=0.5),
                ),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    jen[0].animate.set_opacity(0.2),
                    FadeOut(g),
                ),
                Write(text_jen),
                lag_ratio=0.5,
            ),
        )

        jen.add(text_jen)

        lp_table = VGroup(
                Tex(r"{\bf Variables:}"),
                Tex(r"$$y_i\ \text{(literals) and}\ z_j\ \text{(clauses)}$$"),
                Tex(r"{\bf Inequalities:}"),
                Tex(r"$$z_j \le \sum_{\text{positive}} y_i + \sum_{\text{negative}} \left(1-y_i\right)$$"),
                Tex(r"{\bf Maximize:}"),
                Tex(r"$$\sum z_j\ \text{(satisfied clauses)}$$ "))

        lp_table.arrange_in_grid(cols=2, col_alignments="rl", row_alignments="uuu", buff=(0.5, 0.8)).scale(0.75).shift(DOWN * 0.75)
        lp_table[2].shift(DOWN * 0.10)
        lp_table[4].shift(DOWN * 0.095)

        self.play(Write(lp_table[0:2], run_time=1.5))
        self.play(Write(lp_table[2:4], run_time=1.5))
        self.play(Write(lp_table[4:6], run_time=1.5))

        consider = Tex(r"$$y_i^*, z_j^* \qquad C_j\ \text{with}\ k_j\ \text{variables}$$").shift(DOWN * 0.5)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(lp_table[0]),
                    FadeOut(lp_table[1]),
                    FadeOut(lp_table[2]),
                    FadeOut(lp_table[3]),
                    FadeOut(lp_table[4]),
                    FadeOut(lp_table[5]),
                ),
                AnimationGroup(
                    AnimationGroup(
                        ReplacementTransform(lp_table[1][0][0], VGroup(consider[0][0])),
                        ReplacementTransform(lp_table[1][0][1], VGroup(consider[0][2])),
                        ReplacementTransform(lp_table[1][0][15], VGroup(consider[0][4])),
                        ReplacementTransform(lp_table[1][0][16], VGroup(consider[0][6])),
                    ),
                    Write(VGroup(consider[0][1], consider[0][3], consider[0][5], consider[0][7:]), run_time=1.5),
                    lag_ratio=1,
                ),
                lag_ratio=0.5,
            )
        )

        proof_not_satisfied = Tex(r"""$$
\begin{aligned}
    \mathrm{Pr}\left[C_j\ \text{is not satisfied}\right] &= \overbrace{\prod_{i:\ x_i \in C_j} (1 - y^*_i)}^{\text{positive}}\overbrace{\prod_{i:\ \lnot x_i \in C_j} y^*_i}^{\text{negative}} & \\
    &\overset{A}{\le} \left[\frac{1}{k_j} \left(\sum_{i:\ x_i \in C_j} (1 - y^*_i) + \sum_{i:\ \lnot x_i \in C_j} y^*_i\right)\right]^{k_j} & \\
    &= \left[1 - \frac{1}{k_j} \left(\sum_{i:\ x_i \in C_j} y^*_i + \sum_{i:\ \lnot x_i \in C_j} (1 - y^*_i)\right)\right]^{k_j} & \\
    &\le \left[1 - \frac{z_j^*}{k_j}\right]^{k_j}
\end{aligned}$$""").scale(0.65)

        p1 = VGroup(proof_not_satisfied[0][:75]).move_to(ORIGIN).shift(DOWN * 0.2)
        p2 = VGroup(proof_not_satisfied[0][75:119]).next_to(p1, DOWN).align_to(p1[0][19], LEFT)

        self.play(
            AnimationGroup(
                consider.animate.next_to(VGroup(ag, jen), DOWN, buff=0.5),
                Write(p1, run_time=2),
                lag_ratio=0.75
            )
        )

        combined = VGroup(p1.copy(), p2.copy()).move_to(ORIGIN).align_to(p1, UP)

        self.play(
            Transform(p1, combined[0]),
            FadeIn(p2.become(combined[1].set_color(BLUE)), shift=LEFT),
            ag.animate.set_color(BLUE),
            ag[0].animate.set_opacity(1).set_color(BLUE),
            ag[2].animate.set_opacity(0),
        )

        p1_firstpart = p1[0][19:]

        p2_copy = p2.copy()
        align_object_by_coords(p2_copy, p2_copy[0][1].get_center(), p1[0][19].get_center())
        p3 = VGroup(proof_not_satisfied[0][119:164]).next_to(p2_copy, DOWN).align_to(p2[0][1], LEFT)

        self.play(
            FadeOut(p1_firstpart, shift=UP * 1.45),
            align_object_by_coords(p2, p2[0][1].get_center(), p1[0][19].get_center(), animation=True),
            FadeIn(p3, shift=UP * 1.45),
        )

        self.play(
            Circumscribe(p3[0][9:41], run_time=1.5),
            p3[0][9:41].animate(run_time=1.5).set_color(YELLOW),
        )

        p3_copy = p3.copy()
        align_object_by_coords(p3_copy, p3_copy[0][0].get_center(), p2[0][1].get_center())
        p4 = VGroup(proof_not_satisfied[0][164:]).next_to(p3_copy, DOWN).align_to(p3[0][0], LEFT)

        p4[0][4:4+3].set_color(YELLOW)

        self.play(
            FadeOut(p2, shift=UP * 1.45),
            align_object_by_coords(p3, p3[0][0].get_center(), p2[0][1].get_center(), animation=True),
            FadeIn(p4, shift=UP * 1.45),
        )

        self.play(
            FadeOut(p3, shift=UP * 1.3),
            align_object_by_coords(p4, p4[0][0].get_center(), p3[0][0].get_center(), animation=True).set_color(WHITE),
        )

        p5 = Tex(r"$$\ge 1 - \left[1 - \frac{z_j^*}{k_j}\right]^{k_j}$$").scale(0.65)
        p5_with_overset = Tex(r"$$\ge \overbrace{1 - \left[1 - \frac{z_j^*}{k_j}\right]^{k_j}}^{f(z_j^*)}$$").scale(0.65)

        align_object_by_coords(p5, p5[0][0].get_center(), p4[0][0].get_center())
        align_object_by_coords(p5_with_overset, p5_with_overset[0][0].get_center(), p4[0][0].get_center())

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(p1[0][7:7+3]),
                    p4[0][0].animate.flip(),
                    ReplacementTransform(p4[0][1:], p5[0][3:]),
                ),
                AnimationGroup(
                    FadeIn(p5[0][1:3]),
                    p1[0][:7].animate.shift(RIGHT * 0.55),
                ),
                lag_ratio=0.35,
            ),
        )


        self.remove(p4)
        self.remove(p4[0][0])
        self.add(p5)

        self.play(FadeIn(p5_with_overset[0][1:13], shift=UP * 0.10))

        self.remove(p5)
        self.add(p5_with_overset)

        p6 = Tex(r"$$\overset{B}{\ge} \left[1 - \left(1 - \frac{1}{k_j}\right)^{k_j}\right] z^*_j$$").scale(0.65).set_color(RED)
        p6.next_to(p5, DOWN).align_to(p5, LEFT)

        self.play(
            FadeIn(p6, shift=UP * 0.25),
            jen.animate.set_color(RED),
            jen[0].animate.set_opacity(1).set_color(RED),
            jen[2].animate.set_opacity(0),
        )

        self.remove(p5)

        p7 = Tex(r"$$\ge \left(1 - \frac{1}{e}\right) z^*_j \approx 0.63z^*_j$$").scale(0.65)
        p6_copy = p6.copy()
        align_object_by_coords(p6_copy, p6_copy[0][1].get_center(), p5_with_overset[0][0].get_center())
        p7.next_to(p6_copy, DOWN).align_to(p6_copy[0][1], LEFT)

        self.play(
            p6[0][5:15].animate.set_color(YELLOW),
            Circumscribe(p6[0][5:15]),
        )

        p7[0][4:4+3].set_color(YELLOW)

        self.play(
            FadeOut(p5_with_overset, shift=UP * 1.15),
            align_object_by_coords(p6, p6[0][1].get_center(), p5_with_overset[0][0].get_center(), animation=True),
            FadeIn(p7, shift=UP * 1.15),
        )

        p7_copy = p7[0][:-3].copy().set_color(WHITE)
        align_object_by_coords(p7_copy, p7_copy[0][0].get_center(), p6[0][1].get_center())

        p1_copy = p1[0][:19].copy()

        VGroup(p1_copy, p7_copy).scale(1.5).move_to(ORIGIN).shift(UP * 0.2)

        p1_copy[7:7+3].set_opacity(0)
        p1[0][7:7+3].set_opacity(0)

        self.play(
            FadeOut(p7[0][-3:], shift=RIGHT * 0.5),
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(p6),
                    FadeOut(ag),
                    FadeOut(jen),
                    FadeOut(consider),
                ),
                AnimationGroup(
                    Transform(p1[0][:19], p1_copy),
                    Transform(p7[0][:-3], p7_copy),
                ),
                lag_ratio=0.5,
            )
        )
