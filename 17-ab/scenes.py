from manim import *


class Intro(Scene):
    def construct(self):
        text = Tex("\Huge Intro")

        self.play(Write(text))
        self.play(FadeOut(text))

class Graphs(Scene):
    def construct(self):
        def get_benchmark_data():
            with open("benchmark/benchmark.txt") as f:
                lines = f.read().splitlines()

            lines = lines[3:]
            data = []

            i = 0
            while i < len(lines):
                n = int(lines[i].split()[-1][:-1])
                insert = float(lines[i + 2].split()[-1][:-3]) / 1000000 * 1e3
                search = float(lines[i + 2 + 6].split()[-1][:-3]) / 1000000 * 1e3
                delete = float(lines[i + 2 + 6 + 6].split()[-1][:-3]) / 1000000 * 1e3

                data.append((n, insert, search, delete))

                i += 19

            return np.array(data)

        ax = Axes(
            x_range=[1, 7, 1],
            y_range=[0, 12, 2],
            x_length=8.5,
            y_length=4.3,
            tips=False,
            axis_config={"include_numbers": True},
            x_axis_config={"scaling": LogBase(base=2, custom_labels=False)},
        )

        data = get_benchmark_data()

        g1 = ax.plot_line_graph(x_values=data[:,0], y_values=data[:,1], line_color=RED, add_vertex_dots=False)
        g2 = ax.plot_line_graph(x_values=data[:,0], y_values=data[:,2], line_color=GREEN, add_vertex_dots=False)
        g3 = ax.plot_line_graph(x_values=data[:,0], y_values=data[:,3], line_color=BLUE, add_vertex_dots=False)

        y_label = ax.get_y_axis_label(
            Tex("Average operation time (in $\mu$s)").scale(0.65).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.3,
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeIn(ax),
                    FadeIn(y_label),
                ),
                AnimationGroup(
                    Write(g1),
                    Write(g2),
                    Write(g3),
                    lag_ratio=0.33,
                ),
                lag_ratio=0.66,
            ),
        )
