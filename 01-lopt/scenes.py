from utilities import *

class ChromaticNumber(Scene):
    def construct(self):
        title = Tex("\Large Chromatic Number ($\chi$)")

        self.play(Write(title), run_time = 1)

        text = Tex(r"\parbox{23em}{is the ","smallest"," number of colors needed to color the vertices of a graph $G$, such that ","no two"," neighbouring vertices have the ","same color",".}")

        for i in range(1, len(text), 2):
            text[i].set_color(YELLOW)

        self.play(ApplyMethod(title.shift, UP))

        text.next_to(title, 1.3 * DOWN)

        self.play(Write(text), run_time = 4)

        self.play(FadeOut(text), FadeOut(title))

        vertices = [1, 2, 3, 4, 5, 6]

        edges = [(1,2), (3,2), (2,4), (1,4), (2,5), (6,5), (3,6), (1,5)]
        g = Graph(vertices, edges, layout="circular", layout_scale=3,
                  labels=True)

        self.play(Write(g))

        h = Graph(vertices, edges, layout="circular", layout_scale=3,
                  labels=True,
                  vertex_config={
                      1: {"fill_color": RED},
                      2: {"fill_color": GREEN},
                      3: {"fill_color": RED},
                      4: {"fill_color": BLUE},
                      5: {"fill_color": BLUE},
                      6: {"fill_color": GREEN}
                  }
                  )

        self.play(Transform(g, h))

        self.play(ApplyMethod(g.shift, RIGHT * 1.3))

        text = Tex(r"$\chi(G) = 3$")
        text.next_to(g, LEFT).shift(LEFT * 1.3)

        self.play(Write(text))

        self.play(FadeOut(text), FadeOut(g))

        code = open("chromaticNumber.py").read()
        rendered_code = myCode(code=code, language="Python", scale_factor=0.25)

        self.play(*create_code(self, rendered_code), run_time = 1)

        line_count = len(code.splitlines())
        previous_lines = [i for i in range(1, line_count + 1)]
        for lines in [[3, 4], [6], [8], [9, 10], [12, 13], [14, 15, 16], [17, 18, 19], [21], [23], [25, 26, 27]] + [previous_lines]:
            self.play(
                *[(FadeIn if i in lines and i not in previous_lines else FadeOut)(rendered_code.line_numbers[i - 1]) for i in range(1, line_count + 1) if ((i in lines) != (i in previous_lines))],
                run_time = 0.5
            )
            previous_lines = lines

        output = open("chromaticNumber.out").read()

        rendered_output = myOutput(code=output, language="text", scale_factor=0.25)

        self.play(ApplyMethod(rendered_code.shift, UP))

        rendered_output.next_to(rendered_code, DOWN)

        self.play(*create_output(self, rendered_output), run_time = 1)

class Intro(Scene):
    def construct(self):
        title = Tex("\Large Linear Programming")

        self.play(Write(title), run_time = 1)

        text = Tex(r"\parbox{23em}{is a method of finding a ","minimum/maximum"," of a linear expression of variables, given linear inequalities as ","constraints",".}")

        for i in range(1, len(text), 2):
            text[i].set_color(YELLOW)

        self.play(ApplyMethod(title.shift, UP))

        text.next_to(title, DOWN)

        self.play(Write(text), run_time = 4)

        self.play(FadeOut(text), FadeOut(title))

        text = Tex(r"\centering \parbox{23em}{Find $(x, y)$ that ","maximizes"," the expression $$x + 3y$$given the ","constraints",r" $$\begin{aligned} y &\ge 5x - 10 \\ y &\le \frac{1}{2}x + 3\end{aligned}$$}")

        for i in range(1, len(text), 2):
            text[i].set_color(YELLOW)

        self.play(Write(text), run_time=4)

class Visualizepy(Scene):
    def construct(self):
        code = open("visualize.py").read()

        rendered_code = myCode(code=code, language="Python", scale_factor=0.3)

        self.play(*create_code(self, rendered_code), run_time = 1)

        line_count = len(code.splitlines())
        previous_lines = [i for i in range(1, line_count + 1)]
        for lines in [[1], [3], [5], [7, 8], [10], [12], [14, 15]] + [previous_lines]:
            self.play(
                *[(FadeIn if i in lines and i not in previous_lines else FadeOut)(rendered_code.line_numbers[i - 1]) for i in range(1, line_count + 1) if ((i in lines) != (i in previous_lines))],
                run_time = 0.5
            )
            previous_lines = lines

        output = open("visualize.out").read()

        rendered_output = myOutput(code=output, language="text", scale_factor=0.3)

        self.play(ApplyMethod(rendered_code.shift, UP))

        rendered_output.next_to(rendered_code, DOWN)

        self.play(*create_output(self, rendered_output), run_time = 1)


class Knapsack(Scene):
    def construct(self):
        title = Tex("\Large The Knapsack Problem")

        self.play(Write(title), run_time = 1)

        text = Tex(r"\parbox{23em}{We are given a knapsack of fixed ","load capacity"," and a list of $n$ objects, each with a ","weight"," $w_i$ and a ","price"," $p_i$. Determine the maximum price of objects to put in the knapsack while not exceeding its capacity.}")

        for i in range(1, len(text), 2):
            text[i].set_color(YELLOW)

        self.play(ApplyMethod(title.shift, 2 * UP))

        text.next_to(title, DOWN)

        self.play(Write(text), run_time = 4)

        self.play(FadeOut(text), FadeOut(title))


        code = open("knapsack.py").read()

        rendered_code = myCode(code=code, language="Python", scale_factor=0.3)

        self.play(*create_code(self, rendered_code), run_time = 1)

        line_count = len(code.splitlines())
        previous_lines = [i for i in range(1, line_count + 1)]
        for lines in [[3, 4, 5, 6], [8], [10], [12, 13], [15]] + [previous_lines]:
            self.play(
                *[(FadeIn if i in lines and i not in previous_lines else FadeOut)(rendered_code.line_numbers[i - 1]) for i in range(1, line_count + 1) if ((i in lines) != (i in previous_lines))],
                run_time = 0.5
            )
            previous_lines = lines

        output = open("knapsack.out").read()

        rendered_output = myOutput(code=output, language="text", scale_factor=0.3)

        self.play(ApplyMethod(rendered_code.shift, UP))

        rendered_output.next_to(rendered_code, DOWN)

        self.play(*create_output(self, rendered_output), run_time = 1)


class Visualize(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            x_min=-1,
            x_max=5,
            y_min=-1,
            y_max=5,
            x_labeled_nums=[0],
            **kwargs)

    def construct(self):
        self.setup_axes()
        f1 = lambda x: 1/2 * x + 3
        f2 = lambda x: 5 * x - 10

        curve1 = self.get_graph(f1, x_min = -5, x_max = 10)
        curve2 = self.get_graph(f2)

        label1 = self.get_graph_label(curve1, label=r"y = \frac{1}{2} x + 3", direction=DOWN, buff=0.6)
        label2 = self.get_graph_label(curve2, label=r"y = 5x - 10", direction=LEFT, buff=1)

        label1eq = self.get_graph_label(curve1, label=r"y \le \frac{1}{2} x + 3", direction=DOWN, buff=0.6)
        label2eq = self.get_graph_label(curve2, label=r"y \ge 5x - 10", direction=LEFT, buff=1)

        area1 = Polygon(self.coords_to_point(-5, f2(-5)), self.coords_to_point(10, f2(10)), self.coords_to_point(-5, 50), color=WHITE, fill_opacity=0.2, stroke_opacity=0)
        area_combined = Polygon(self.coords_to_point(-5, f2(-5)), self.coords_to_point(-5, f1(-5)), self.coords_to_point(26/9, 26/9 * 5  - 10 ), color=WHITE, fill_opacity=0.2, stroke_opacity=0)

        self.play(Create(curve1), Create(curve2), Write(label1), Write(label2))
        self.play(FadeIn(area1), Transform(label1, label1eq))
        self.play(FadeOut(area1), FadeIn(area_combined), Transform(label2, label2eq))

        dot = Dot().move_to(self.coords_to_point(0, 0))
        arrow = Arrow(self.coords_to_point(0, 0), self.coords_to_point(3 / sqrt(10), 1 / sqrt(10)) + [0], buff=0)

        text = Tex("$(0.0, 0.0)$")
        text.next_to(dot, UP)

        arrow_text = Tex("$x + 3y$")
        arrow_text.next_to(self.coords_to_point(3 / sqrt(10), 1 / sqrt(10)), UP)

        self.play(
            Create(dot),
            Create(arrow),
            Write(arrow_text)
        )

        self.play(
            Write(text),
            FadeOut(arrow_text)
        )

        line = Line(self.coords_to_point(0, 0), self.coords_to_point(30/14, 30/(14 * 3)))

        def update_text(text):
            x, y = map(abs, self.point_to_coords(dot.get_center()))

            txt = f"$({x:.1f}, {y:.1f})$"

            text.become(Tex(txt))
            text.next_to(dot, UP)
            arrow.become(Arrow(self.coords_to_point(x, y), self.coords_to_point(x + 3 / sqrt(10), y + 1 / sqrt(10)) + [0], buff=0))

        text.add_updater(update_text)
        self.add(text)

        self.play(
            MoveAlongPath(dot, line),
            run_time=1, rate_func=lambda t: 2 * smooth(t / 2)
        )

        line = Line(self.coords_to_point(30/14, 30/(14 * 3)), self.coords_to_point(26/9, 26/9 * 5  - 10 ))

        self.play(
            MoveAlongPath(dot, line),
            run_time=1, rate_func=lambda t: (smooth(1/2 + t / 2) - 1/2) * 2
        )

        text.remove_updater(update_text)

        x, y = map(abs, self.point_to_coords(dot.get_center()))
        txt = r"$\left(\frac{26}{9}, \frac{40}{9}\right)$"
        text2 = Tex(txt).next_to(dot, UP)

        self.play(Transform(text, text2), FadeOut(arrow))

        self.play(*[FadeIn(Dot(self.coords_to_point(x, y), radius=0.04)) for x in range(-20, 20) for y in range(-20, 20) if f1(x) >= y and f2(x) <= y])

        line = Line(self.coords_to_point(26/9, 26/9 * 5  - 10), self.coords_to_point(2, 4))

        x, y = map(abs, self.point_to_coords(dot.get_center()))
        txt = f"$({x:.1f}, {y:.1f})$"
        text3 = Tex(txt).next_to(dot, UP)
        self.play(Transform(text, text3))

        text.add_updater(update_text)
        self.play(
            MoveAlongPath(dot, line),
            run_time=1, rate_func=smooth
        )
        text.remove_updater(update_text)

        txt = r"$\left(2, 4\right)$"
        text4 = Tex(txt).next_to(dot, UP)

        self.play(Transform(text, text4))

