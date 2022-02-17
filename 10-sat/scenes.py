from utilities import *

class Intro(MovingCameraScene):
    def construct(self):
        sat = Tex("\Huge SAT").scale(2)

        p = Tex(r"\Huge \textbf{P}").scale(1.3)
        np = Tex(r"\Huge \textbf{NP}").scale(1.3)


        p_np = VGroup(p, np).arrange(buff=1.5).shift(UP * 0.6)

        self.play(Write(sat))

        self.play(AnimationGroup(sat.animate.shift(DOWN * 1.1).scale(1/4), Write(p_np), lag_ratio=0.3))

        p_circle = Circle(color=WHITE).surround(p, buffer_factor=1.45)
        np_circle = Circle(color=WHITE).surround(p_np + VGroup(sat), buffer_factor=1.15)

        self.play(Write(p_circle), Write(np_circle))

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
            arrow = Arrow(start=problem.get_center(), end=sat.get_center(), buff=0.35)
            arrows.add(arrow)

        self.play(AnimationGroup(*[Write(problem) for problem in problems], lag_ratio=0.7))

        self.play(FadeIn(arrows))

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
\textbf{solution}&optimal&not optimal\\
\bottomrule
\end{tabular}
\end{table}%
""", tex_template=myTemplate).scale(1/3).move_to(sat).shift(DOWN * 0.2)

        d = 17
        table[0][48-d:62-d].set_color(RED)
        table[0][62-d:75-d].set_color(GREEN)
        table[0][83-d:90-d].set_color(GREEN)
        table[0][90-d:100-d].set_color(RED)

        self.play(AnimationGroup(AnimationGroup(FadeOut(problems), FadeOut(arrows)), AnimationGroup(sat.animate.next_to(table, UP), FadeIn(table, shift=UP * 0.3)), lag_ratio=0.5))

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
