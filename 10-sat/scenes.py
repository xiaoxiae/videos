from utilities import *

class Intro(MovingCameraScene):
    @fade
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
                        FadeOut(bsat[0][0:7], shift=DOWN * 0.5),
                        FadeOut(bsat[0][10:], shift=DOWN * 0.5),
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

        self.play(AnimationGroup(AnimationGroup(FadeOut(problems), FadeOut(arrows)), AnimationGroup(sat.animate.next_to(table, UP), FadeIn(table, shift=UP * 0.3)), lag_ratio=0.5))

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

        ade = [1, 13, 19]

        equals = Tex("$=$").rotate(PI / 2).scale(0.75)
        one = Tex("$1$").scale(0.85).next_to(equals, DOWN, buff=0.15)

        combined = VGroup(equals, one)

        combined_copies = VGroup(*[combined.copy().next_to(groups[0][i], DOWN) for i in ade])

        self.play(
            AnimationGroup(
                *[FadeIn(combined_copy, shift=DOWN * 0.2) for combined_copy in combined_copies],
                lag_ratio=0.1,
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


class RANDSAT(MovingCameraScene):
    def construct(self):
        rand = Tex(r"RAND-SAT").scale(3)

        self.play(Write(rand))

        # TODO: možná trochu víc

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

        equals = Tex("$=$").rotate(PI / 2).scale(0.75)
        one = Tex("$1$").scale(0.85).next_to(equals, UP, buff=0.15)
        zero = Tex("$0$").scale(0.85).next_to(equals, UP, buff=0.15)

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

        # left this out? \frac{\sum p_{\text{sat}}\ \text{of $i$-th clause}}{\text{\# of clauses}}
        prob = Tex(r"$$\mathbb{E}\left[\text{\# of sat. clauses}\right] =  \ge 1/2$$").next_to(example, DOWN, buff=1.0)

        self.play(
            FadeIn(prob, shift=DOWN * 0.3),
            self.camera.frame.animate.move_to(VGroup(prob, example)),
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

        lp_table.arrange_in_grid(cols=2, col_alignments="rl", row_alignments="uuu", buff=(0.5, 0.8))

        new_lp = lp.copy().scale(0.75)
        VGroup(new_lp, lp_table).arrange(DOWN, buff=1)

        self.play(Transform(lp, new_lp))

        self.play(Write(lp_table[0:2]))
        self.play(Write(lp_table[2:4]))
        self.play(Write(lp_table[4:6]))



class SATOld(MovingCameraScene):
    @fade
    def construct(self):
        sat = Tex(r"\Huge SAT")

        sat_definition_table = VGroup(
                Tex(r"{\bf Input:}"),
                Tex(r"formula in the form \(C_1 \land C_2 \land \ldots \land C_n\)"),
                Tex(r""),
                Tex(r"each \(C_i\) is in the form \((x_{i,1} \lor x_{i,2} \lor \ldots \lor x_{i,k})\)"),
                Tex(r"{\bf Output:}"),
                Tex(r"variable assignment \(\left\{0, 1\right\}^n\)"),
                Tex(r"{\bf Goal:}"),
                Tex(r"satisfy all clauses"),
                )

        sat_definition_table.arrange_in_grid(cols=2, col_alignments="rl")
        VGroup(sat, sat_definition_table).arrange(DOWN, buff=0.8)

        max_sat = Tex(r"\Huge MAX", color=BLUE)
        dash = Tex("\Huge -", color=BLUE)
        max_sat_goal = Tex(r"maximize the number of satisfied clauses", color=BLUE).move_to(sat_definition_table[-1]).align_to(sat_definition_table[-1], LEFT)

        new_sat = sat.copy()
        VGroup(max_sat, dash, new_sat).arrange(buff=0.3).move_to(sat)
        dash.shift(LEFT * 0.08)

        self.play(Write(sat), Write(sat_definition_table))

        self.play(
                sat.animate.move_to(new_sat),
                FadeIn(max_sat, shift=LEFT),
                FadeIn(dash, shift=LEFT),
                )

        self.play(FadeOut(sat_definition_table[-1], shift=UP * 0.5), FadeIn(max_sat_goal, shift=UP * 0.5))
