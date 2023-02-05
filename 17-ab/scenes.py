from manim import *
from utilities import *


class Intro(MovingCameraScene):
    def construct(self):

        ab_tree = ABTree(
            2, 4,
            [
                [[2, 4]],
                [[1], [3], [5, 6, 7]],
            ]
        )

        binary_tree = ABTree(
            2, 4,
            [
                [[4]],
                [[2], [6]],
                [[1], [3], [5], [7]],
            ]
        )

        ab = VGroup(Tex(r"\underline{$(a,b)$-tree}").scale(1.25), ab_tree).arrange(DOWN, buff=1.2)
        bst = VGroup(Tex(r"\underline{binary search tree}").scale(1.25), binary_tree).arrange(DOWN, buff=1.2)

        ab.move_to(self.camera.frame.get_center())
        bst.move_to(self.camera.frame.get_center())
        ab.align_to(bst, UP)
        ab[1].align_to(bst, DOWN)

        self.play(
            Write(ab),
        )

        group_cp = VGroup(ab.copy(), bst).arrange(buff=1.25)
        group_cp[0].align_to(group_cp[1], UP)

        self.play(
            AnimationGroup(
                ab.animate.move_to(group_cp[0]),
                Write(bst),
                lag_ratio=0.75,
            ),
        )

        a1 = Arrow(ORIGIN, DOWN * 1.25).next_to(ab_tree.node_by_index(1, 2), UP).set_color(BLUE)
        a2 = Arrow(ORIGIN, DOWN * 1.25).next_to(ab_tree.node_by_index(0, 0), UP).set_color(BLUE)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    ab_tree.node_by_index(0, 0).animate.set_color(BLUE),
                    ab_tree.node_edges[ab_tree.node_by_index(0, 0)].animate.set_color(BLUE),
                    FadeIn(a2, shift=DOWN * 0.25),
                ),
                AnimationGroup(
                    ab_tree.node_by_index(1, 2).animate.set_color(BLUE),
                    ab_tree.node_edges[ab_tree.node_by_index(1, 2)].animate.set_color(BLUE),
                    FadeIn(a1, shift=DOWN * 0.25),
                ),
                lag_ratio=0.1,
            ),
        )

        self.play(
            FadeOut(a1),
            FadeOut(a2),
            ab_tree.node_by_index(0, 0).animate.set_color(WHITE),
            ab_tree.node_edges[ab_tree.node_by_index(0, 0)].animate.set_color(WHITE),
            ab_tree.node_by_index(1, 2).animate.set_color(WHITE),
            ab_tree.node_edges[ab_tree.node_by_index(1, 2)].animate.set_color(WHITE),
        )

        #useful = Tex(r"\textit{Used for quickly storing and locating items based on their keys.}")\
        #        .move_to(group_cp).align_to(ab[0], DOWN).shift(DOWN * 0.5).scale(0.65)

        #self.play(
        #    AnimationGroup(
        #        AnimationGroup(
        #            ab[0].animate.shift(UP * 0.25),
        #            bst[0].animate.shift(UP * 0.25),
        #            ab[1].animate.shift(DOWN * 0.25),
        #            bst[1].animate.shift(DOWN * 0.25),
        #        ),
        #        Write(useful),
        #        lag_ratio=0.6,
        #    )
        #)

        self.play(
            ab.animate.set_color(DARKER_GRAY).shift(LEFT * 4),
            self.camera.frame.animate.move_to(bst),
        )

        def get_bubble(symbol):
            dot = Dot().scale(2)
            symbol = Tex(f"${symbol}$", color=BLACK).scale(0.5).set_z_index(1).move_to(dot)

            return VGroup(dot, symbol)

        bubbles = VGroup()
        node_bubbles = {}
        for layer in range(len(binary_tree.layers)):
            for position in range(len(binary_tree.layers[layer])):
                node = binary_tree.node_by_index(layer, position)
                edges = binary_tree.node_edges[node]

                if edges is None:
                    continue

                l, r = edges

                l_bubble = get_bubble("<").move_to(l).scale(1 - layer * 0.25).set_z_index(2)
                r_bubble = get_bubble("<").move_to(r).scale(1 - layer * 0.25).set_z_index(2)

                node_bubbles[node] = VGroup(l_bubble, r_bubble)

                bubbles.add(l_bubble, r_bubble)

        self.play(FadeIn(bubbles))


        # TARGET 5

        target = Tex("$5$").next_to(binary_tree.node_by_index(0, 0), UP).scale(0.8)

        self.play(
            Write(target),
        )

        binary_tree.save_state()
        bubbles.save_state()

        # NOTE: copy-pasted
        bezier = CubicBezier(
            target.get_center(),
            Dot().move_to(binary_tree.node_by_index(1, 1)).align_to(target, DOWN).get_center(),
            Dot().move_to(binary_tree.node_by_index(1, 1)).align_to(target, DOWN).get_center(),
            target.copy().next_to(binary_tree.node_by_index(1, 1), UP).get_center(),
        )

        self.play(
            MoveAlongPath(target, bezier),
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(1, 0)].animate.set_color(DARK_GRAY),
            binary_tree.node_edges[binary_tree.node_by_index(0, 0)][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(0, 0)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(1, 0)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(2, 0)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(2, 1)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(1, 0)][1][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(2, 0)][1][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(2, 1)][1][0].animate.set_color(DARK_GRAY),
        )

        # NOTE: copy-pasted
        bezier = CubicBezier(
            target.get_center(),
            Dot().move_to(binary_tree.node_by_index(2, 2)).align_to(target, DOWN).get_center(),
            Dot().move_to(binary_tree.node_by_index(2, 2)).align_to(target, DOWN).get_center(),
            target.copy().next_to(binary_tree.node_by_index(2, 2), UP).get_center(),
        )

        self.play(
            MoveAlongPath(target, bezier),
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(2, 3)].animate.set_color(DARK_GRAY),
            binary_tree.node_edges[binary_tree.node_by_index(1, 1)][1].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(1, 1)][1][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(2, 3)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(2, 3)][1][0].animate.set_color(DARK_GRAY),
        )

        target_cp = binary_tree.node_by_index(2, 2)[0].copy().set_opacity(0)

        self.play(
            Transform(target, target_cp),
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(2, 2)].animate.set_color(GREEN),
            node_bubbles[binary_tree.node_by_index(2, 2)][0][0].animate.set_color(GREEN),
            node_bubbles[binary_tree.node_by_index(2, 2)][1][0].animate.set_color(GREEN),
        )

        self.remove(target_cp)

        self.play(
            binary_tree.animate.restore(),
            bubbles.animate.restore(),
        )


        # TARGET 8, COPY PASTED!

        target = Tex("$8$").next_to(binary_tree.node_by_index(0, 0), UP).scale(0.8)

        self.play(
            Write(target),
        )

        binary_tree.save_state()
        bubbles.save_state()

        # NOTE: copy-pasted
        bezier = CubicBezier(
            target.get_center(),
            Dot().move_to(binary_tree.node_by_index(1, 1)).align_to(target, DOWN).get_center(),
            Dot().move_to(binary_tree.node_by_index(1, 1)).align_to(target, DOWN).get_center(),
            target.copy().next_to(binary_tree.node_by_index(1, 1), UP).get_center(),
        )

        self.play(
            MoveAlongPath(target, bezier),
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(1, 0)].animate.set_color(DARK_GRAY),
            binary_tree.node_edges[binary_tree.node_by_index(0, 0)][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(0, 0)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(1, 0)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(2, 0)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(2, 1)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(1, 0)][1][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(2, 0)][1][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(2, 1)][1][0].animate.set_color(DARK_GRAY),
        )

        # NOTE: copy-pasted
        bezier = CubicBezier(
            target.get_center(),
            Dot().move_to(binary_tree.node_by_index(2, 3)).align_to(target, DOWN).get_center(),
            Dot().move_to(binary_tree.node_by_index(2, 3)).align_to(target, DOWN).get_center(),
            target.copy().next_to(binary_tree.node_by_index(2, 3), UP).get_center(),
        )

        self.play(
            MoveAlongPath(target, bezier),
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(2, 2)].animate.set_color(DARK_GRAY),
            binary_tree.node_edges[binary_tree.node_by_index(1, 1)][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(1, 1)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(2, 2)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[binary_tree.node_by_index(2, 2)][1][0].animate.set_color(DARK_GRAY),
        )

        target_cp = target.copy().set_opacity(0).move_to(binary_tree.node_by_index(3, 7)[0])

        self.play(
            Transform(target, target_cp),
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(3, 7)].animate.set_color(RED),
        )

        self.remove(target_cp)

        self.play(
            binary_tree.animate.restore(),
            bubbles.animate.restore(),
        )

        self.play(
            ab.animate.set_color(WHITE).shift(RIGHT * 4),
            bst.animate.set_color(DARKER_GRAY).shift(RIGHT * 4),
            bubbles.animate.set_color(DARKER_GRAY).shift(RIGHT * 4),
            self.camera.frame.animate.move_to(ab).shift(RIGHT * 4),
        )



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
