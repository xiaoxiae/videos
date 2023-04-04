from manim import *
from utilities import *

from random import shuffle, seed
from math import sqrt

S = 1.4


class Fever(MovingCameraScene):
    @fade
    def construct(self):
        happened = VGroup(
            Tex("\sc Has This Ever"),
            Tex("\sc Happened to Y\kern-0.1em ou?"),
        ).scale(2.2).arrange(DOWN, buff=0.5)

        self.play(
            FadeIn(happened)
        )

        self.wait()

        self.camera.frame.save_state()

        self.remove(happened)

        binary_tree = ABTree(
            [
                [[4]],
                [[2], [6]],
                [[1], [3], [5], [7]],
            ]
        ).scale(1.5)

        binary_tree.subtree_by_index(1, 0).set_stroke_color(BLACK)
        binary_tree.node_by_index(1, 0).set_color(BLACK).set_z_index(-1)
        binary_tree.node_by_index(2, 1).set_color(BLACK).set_z_index(-1)
        binary_tree.subtree_by_index(2, 0).set_stroke_color(WHITE)\
                .move_to(binary_tree.subtree_by_index(1, 0))\
                .align_to(binary_tree.subtree_by_index(1, 0), UP)

        self.add(binary_tree)

        self.play(
            binary_tree.node_by_index(0, 0).animate.move_to(binary_tree.node_by_index(1, 1)),
            binary_tree.subtree_by_index(2, 0).animate.move_to(binary_tree.node_by_index(0, 0)).align_to(binary_tree.node_by_index(0, 0), UP),
            binary_tree.subtree_by_index(1, 1).animate.move_to(binary_tree.node_by_index(2, 3)).align_to(binary_tree.node_by_index(2, 3), UP),
            binary_tree.subtree_by_index(3, 1).animate.move_to(binary_tree.node_by_index(2, 2)).align_to(binary_tree.node_by_index(2, 2), UP),
            binary_tree.subtree_by_index(3, 0).animate.move_to(binary_tree.node_by_index(2, 0)).align_to(binary_tree.node_by_index(2, 0), UP),
            Transform(binary_tree.edges_by_node_index(0, 0)[0], binary_tree.edges_by_node_index(0, 0)[1].copy().rotate(PI)),
            Transform(binary_tree.edges_by_node_index(0, 0)[1], binary_tree.edges_by_node_index(1, 1)[1]),
            Transform(binary_tree.edges_by_node_index(2, 0)[0], binary_tree.edges_by_node_index(0, 0)[0]),
            Transform(binary_tree.edges_by_node_index(2, 0)[1], binary_tree.edges_by_node_index(1, 1)[0]),
            self.camera.frame.animate.scale(1.2).shift(DOWN * 0.75 + LEFT)
        )

        ono = Tex("\sc Oh no!").scale(3.5).move_to(self.camera.frame).shift(LEFT * 3 + DOWN * 0.75).set_z_index(10).rotate(-PI / 8)

        self.play(SpinInFromNothing(ono, angle=3 * PI))

        self.wait()

        rect = get_fade_rect()

        bw = VGroup(
            Tex("\sc Is there a"),
            Tex("\sc better way?"),
        ).scale(3.5).arrange(DOWN, buff=0.5).move_to(self.camera.frame).set_z_index(1000)

        thereis = Tex("\sc There is!").next_to(bw, DOWN).scale(4.5).set_z_index(1000)

        g = VGroup(
            bw.copy(),
            thereis,
        ).arrange(DOWN, buff=1.5).move_to(self.camera.frame)

        self.play(
            AnimationGroup(
                FadeIn(rect),
                FadeIn(bw),
                lag_ratio=0.5,
            )
        )

        self.play(
            Transform(bw, g[0]),
            FadeIn(thereis, shift=UP * 0.5),
        )

        self.wait()

        for m in self.mobjects:
            self.remove(m)

        self.camera.frame.restore()

        ab_tree = ABTree(
            [
                [[2, 4]],
                [[1], [3], [5, 6, 7]],
            ]
        ).scale(1.75)

        self.add(ab_tree)

        g = VGroup(
            Tex("\sc Fast!").scale(1.5).next_to(ab_tree.node_by_index(0, 0), LEFT, buff=1.5),
            Tex("\sc Simpl!").scale(1.5).next_to(ab_tree.node_by_index(0, 0), RIGHT, buff=1.2),
            Tex("\sc No rotations!").scale(1.5).rotate(PI).next_to(ab_tree.node_by_index(0, 0), UP, buff=0.75),
        )

        g[0].align_to(g[1], UP)

        self.play(
            FadeIn(g[0], shift=RIGHT * 0.5),
            run_time=0.33,
        )

        self.play(
            FadeIn(g[1], shift=LEFT * 0.5),
        )

        self.play(
            FadeIn(g[2], shift=DOWN * 0.5),
            self.camera.frame.animate.shift(UP * 0.75),
        )

class Intro(MovingCameraScene):
    @fade
    def construct(self):
        ab_tree = ABTree(
            [
                [[2, 4]],
                [[1], [3], [5, 6, 7]],
            ],
            fill_background=False,
        )

        binary_tree = ABTree(
            [
                [[4]],
                [[2], [6]],
                [[1], [3], [5], [7]],
            ],
            fill_background=False,
        )

        ab = VGroup(Tex(r"\underline{$(a,b)$-tree}").scale(1.25), ab_tree).arrange(DOWN, buff=1)
        bst = VGroup(Tex(r"\underline{binary search tree}").scale(1.25), binary_tree).arrange(DOWN, buff=1.2)

        ab.move_to(self.camera.frame.get_center())
        bst.move_to(self.camera.frame.get_center())

        self.camera.frame.scale(0.95)

        S = 0.8

        self.camera.frame.scale(S)

        self.play(
            Write(ab),
        )

        group_cp = VGroup(ab.copy(), bst).arrange(buff=1.15)
        group_cp[0].align_to(group_cp[1], UP)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    ab[0].animate.move_to(group_cp[0][0]),
                    ab[1].animate.move_to(group_cp[0][1]).align_to(bst, DOWN),
                    self.camera.frame.animate.scale(1/S),
                ),
                FadeIn(bst),
                lag_ratio=0.5,
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

        # TODO: wave

        keys = VGroup(*(list(ab_tree.keys) + list(binary_tree.keys)))

        min_x, max_x = float('inf'), float('-inf')
        for k in keys:
            min_x = min(k.get_x(), min_x)
            max_x = max(k.get_x(), max_x)

        wait_scale = 0.5

        self.play(
            *[
              Succession(
                Wait((k.get_x() - min_x) / (max_x - min_x) * wait_scale),
                k.animate(rate_func=there_and_back, run_time=1.25).scale(1.25).set_color(GREEN),
              )
              for k in keys]
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

        self.camera.frame.save_state()

        self.play(
            ab.animate.set_color(DARK_COLOR).shift(LEFT * 4),
            self.camera.frame.animate.move_to(bst),
        )

        # TARGET 5
        bubbles, node_bubbles = get_tree_bubbles(binary_tree)

        target = Tex("$5$").next_to(binary_tree.node_by_index(0, 0), UP).scale(0.8)

        self.play(
            FadeIn(target, shift=UP * 0.1),
        )

        self.play(FadeIn(bubbles))

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
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(1, 0)].animate.set_color(DARK_COLOR),
            binary_tree.node_edges[binary_tree.node_by_index(0, 0)][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(0, 0)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(1, 0)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(2, 0)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(2, 1)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(1, 0)][1][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(2, 0)][1][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(2, 1)][1][0].animate.set_color(DARK_COLOR),
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
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(2, 3)].animate.set_color(DARK_COLOR),
            binary_tree.node_edges[binary_tree.node_by_index(1, 1)][1].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(1, 1)][1][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(2, 3)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(2, 3)][1][0].animate.set_color(DARK_COLOR),
        )

        target_cp = binary_tree.node_by_index(2, 2)[0].copy().set_opacity(0)

        self.play(
            Transform(target, target_cp),
            binary_tree.node_by_index(2, 2).animate.set_color(GREEN),
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
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(1, 0)].animate.set_color(DARK_COLOR),
            binary_tree.node_edges[binary_tree.node_by_index(0, 0)][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(0, 0)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(1, 0)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(2, 0)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(2, 1)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(1, 0)][1][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(2, 0)][1][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(2, 1)][1][0].animate.set_color(DARK_COLOR),
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
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(2, 2)].animate.set_color(DARK_COLOR),
            binary_tree.node_edges[binary_tree.node_by_index(1, 1)][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(1, 1)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(2, 2)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[binary_tree.node_by_index(2, 2)][1][0].animate.set_color(DARK_COLOR),
        )

        # NOTE: copy-pasted
        bezier = CubicBezier(
            target.get_center(),
            Dot().move_to(binary_tree.node_by_index(3, 7)).align_to(target, DOWN).get_center(),
            Dot().move_to(binary_tree.node_by_index(3, 7)).align_to(target, DOWN).get_center(),
            target.copy().move_to(binary_tree.node_by_index(3, 7), UP).get_center(),
        )

        self.play(
            MoveAndFade(target, bezier),
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(3, 7)].animate.set_color(RED),
            node_bubbles[binary_tree.node_by_index(2, 3)][0][0].animate.set_color(DARK_COLOR),
            binary_tree.node_edges[binary_tree.node_by_index(2, 3)][0].animate.set_color(DARK_COLOR),
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(3, 6)].animate.set_color(DARK_COLOR),
        )

        self.remove(target_cp)

        self.play(
            binary_tree.animate.restore(),
            bubbles.animate.restore(),
        )

        old_bubbles = bubbles

        bubbles, node_bubbles = get_tree_bubbles(ab_tree)

        self.add(bubbles)

        self.play(
            ab.animate.set_color(WHITE).shift(RIGHT * 4),
            bst.animate.set_color(DARK_COLOR).shift(RIGHT * 4),
            bubbles.animate.shift(RIGHT * 4),
            old_bubbles.animate.set_color(DARK_COLOR).shift(RIGHT * 4),
            self.camera.frame.animate.move_to(ab).shift(RIGHT * 4),
        )

        self.remove(old_bubbles)

        # TARGET 5 AB, COPY PASTED!

        target = Tex("$5$").next_to(ab_tree.node_by_index(0, 0), UP).scale(0.8)

        self.play(
            Write(target),
        )

        ab_tree.save_state()
        bubbles.save_state()

        # NOTE: copy-pasted
        bezier = CubicBezier(
            target.get_center(),
            Dot().move_to(ab_tree.node_by_index(1, 2)).align_to(target, DOWN).get_center(),
            Dot().move_to(ab_tree.node_by_index(1, 2)).align_to(target, DOWN).get_center(),
            target.copy().next_to(ab_tree.node_by_index(1, 2), UP).get_center(),
        )

        self.play(
            MoveAlongPath(target, bezier),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(1, 0)].animate.set_color(DARK_COLOR),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(1, 1)].animate.set_color(DARK_COLOR),
            ab_tree.node_edges[ab_tree.node_by_index(0, 0)][0].animate.set_color(DARK_COLOR),
            ab_tree.node_edges[ab_tree.node_by_index(0, 0)][1].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(0, 0)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(0, 0)][1][0].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(1, 0)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(1, 0)][1][0].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(1, 1)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(1, 1)][1][0].animate.set_color(DARK_COLOR),
        )

        target_cp = ab_tree.node_by_index(1, 2)[0][0].copy().set_opacity(0)

        self.play(
            Transform(target, target_cp),
            ab_tree.node_by_index(1, 2).animate.set_color(GREEN),
            ab_tree.node_by_index(1, 2)[0][1].animate.set_color(WHITE),
            ab_tree.node_by_index(1, 2)[0][2].animate.set_color(WHITE),
        )

        ab_tree.node_by_index(1, 2)[0][1].set_color(WHITE)
        ab_tree.node_by_index(1, 2)[0][2].set_color(WHITE)

        self.remove(old_bubbles)
        bst.set_color(WHITE)

        self.play(
            ab_tree.animate.restore(),
            bubbles.animate.restore(),
        )

        # TARGET 8 AB, COPY PASTED!

        target = Tex("$8$").next_to(ab_tree.node_by_index(0, 0), UP).scale(0.8)

        self.play(
            Write(target),
        )

        ab_tree.save_state()
        bubbles.save_state()

        # NOTE: copy-pasted
        bezier = CubicBezier(
            target.get_center(),
            Dot().move_to(ab_tree.node_by_index(1, 2)).align_to(target, DOWN).get_center(),
            Dot().move_to(ab_tree.node_by_index(1, 2)).align_to(target, DOWN).get_center(),
            target.copy().next_to(ab_tree.node_by_index(1, 2), UP).get_center(),
        )

        self.play(
            MoveAlongPath(target, bezier),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(1, 0)].animate.set_color(DARK_COLOR),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(1, 1)].animate.set_color(DARK_COLOR),
            ab_tree.node_edges[ab_tree.node_by_index(0, 0)][0].animate.set_color(DARK_COLOR),
            ab_tree.node_edges[ab_tree.node_by_index(0, 0)][1].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(0, 0)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(0, 0)][1][0].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(1, 0)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(1, 0)][1][0].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(1, 1)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(1, 1)][1][0].animate.set_color(DARK_COLOR),
        )

        # NOTE: copy-pasted
        bezier = CubicBezier(
            target.get_center(),
            Dot().move_to(ab_tree.node_by_index(2, 7)).align_to(target, DOWN).get_center(),
            Dot().move_to(ab_tree.node_by_index(2, 7)).align_to(target, DOWN).get_center(),
            target.copy().move_to(ab_tree.node_by_index(2, 7), UP).get_center(),
        )

        self.play(
            MoveAndFade(target, bezier),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(2, 7)].animate.set_color(RED),
            node_bubbles[ab_tree.node_by_index(1, 2)][0][0].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(1, 2)][1][0].animate.set_color(DARK_COLOR),
            node_bubbles[ab_tree.node_by_index(1, 2)][2][0].animate.set_color(DARK_COLOR),
            ab_tree.node_edges[ab_tree.node_by_index(1, 2)][0].animate.set_color(DARK_COLOR),
            ab_tree.node_edges[ab_tree.node_by_index(1, 2)][1].animate.set_color(DARK_COLOR),
            ab_tree.node_edges[ab_tree.node_by_index(1, 2)][2].animate.set_color(DARK_COLOR),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(2, 4)].animate.set_color(DARK_COLOR),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(2, 5)].animate.set_color(DARK_COLOR),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(2, 6)].animate.set_color(DARK_COLOR),
        )

        self.play(
            ab_tree.animate.restore(),
            FadeOut(bubbles),
            bst.animate.shift(LEFT * 4),
            self.camera.frame.animate.move_to(VGroup(ab_tree, bst.copy().shift(LEFT * 4))),
        )

        ng = VGroup(binary_tree)

        self.play(
            ab.animate.set_color(DARK_COLOR).shift(LEFT * 4),
            bst[0].animate.set_color(DARK_COLOR).shift(UP * 4),
            self.camera.frame.animate.move_to(ng).set_height(ng.get_height() * 1.6),
        )

        ab.shift(LEFT * 10)

        a = binary_tree.node_by_index(3, 7)
        b = ABTree([[[8]]], fill_background=False).move_to(a).align_to(a, UP + LEFT)

        e = binary_tree.node_edges[binary_tree.node_by_index(2, 3)][1]

        ng = VGroup(binary_tree, b)

        self.play(
            self.camera.frame.animate.move_to(ng).set_height(ng.get_height() * 1.4),
            AnimationGroup(
                AnimationGroup(
                    ReplacementTransform(a, b.node_by_index(0, 0)),
                    ReplacementTransform(e, Line(e.points[0], Dot().scale(0.001).move_to(b).align_to(b, UP).get_center()))
                ),
                AnimationGroup(
                    FadeIn(b.node_by_index(1, 0)),
                    FadeIn(b.node_by_index(1, 1)),
                    FadeIn(b.node_edges[b.node_by_index(0, 0)]),
                ),
                lag_ratio=0.5,
            ),
        )

        # NOTE: copy-pasted!
        old_b = b
        a = old_b.node_by_index(1, 1)
        b = ABTree([[[9]]], fill_background=False).move_to(a).align_to(a, UP + LEFT)

        e = old_b.node_edges[old_b.node_by_index(0, 0)][1]

        ng = VGroup(binary_tree, b)

        self.play(
            self.camera.frame.animate.move_to(ng).set_height(ng.get_height() * 1.4),
            AnimationGroup(
                AnimationGroup(
                    ReplacementTransform(a, b.node_by_index(0, 0)),
                    ReplacementTransform(e, Line(e.points[0], Dot().scale(0.001).move_to(b).align_to(b, UP).get_center()))
                ),
                AnimationGroup(
                    FadeIn(b.node_by_index(1, 0)),
                    FadeIn(b.node_by_index(1, 1)),
                    FadeIn(b.node_edges[b.node_by_index(0, 0)]),
                ),
                lag_ratio=0.5,
            ),
        )

        # NOTE: copy-pasted!
        old_b = b
        a = old_b.node_by_index(1, 1)
        b = ABTree([[[10]]], fill_background=False).move_to(a).align_to(a, UP + LEFT)

        e = old_b.node_edges[old_b.node_by_index(0, 0)][1]

        ng = VGroup(binary_tree, b)

        self.play(
            self.camera.frame.animate.move_to(ng).set_height(ng.get_height() * 1.4),
            AnimationGroup(
                AnimationGroup(
                    ReplacementTransform(a, b.node_by_index(0, 0)),
                    ReplacementTransform(e, Line(e.points[0], Dot().scale(0.001).move_to(b).align_to(b, UP).get_center()))
                ),
                AnimationGroup(
                    FadeIn(b.node_by_index(1, 0)),
                    FadeIn(b.node_by_index(1, 1)),
                    FadeIn(b.node_edges[b.node_by_index(0, 0)]),
                ),
                lag_ratio=0.5,
            ),
        )

        avl = Tex("AVL trees")
        rb = Tex("R\&B trees")

        g = VGroup(avl, rb).scale(2).arrange(DOWN, buff=0.35)\
                .move_to(ng).align_to(ng, DOWN + LEFT).shift(LEFT * 1.4)
        avl.align_to(rb, RIGHT)

        self.play(
            FadeIn(avl, shift=RIGHT)
        )
        self.play(
            FadeIn(rb, shift=RIGHT)
        )

        rect = get_fade_rect(z_index=100)
        t = Tex(r"$\times$").move_to(VGroup(g, ng)).shift(DOWN * 0.25).scale(15).set_color(RED).set_z_index(101)

        self.play(
            AnimationGroup(
                FadeIn(rect),
                FadeIn(t),
                lag_ratio=0.5,
            )
        )

        ab_four = ABTree(
            [
                [[2, 4]],
                [[1], [3], [5, 6, 7]],
            ],
            fill_background=False,
        ).scale(2).next_to(self.camera.frame, LEFT).set_z_index(1000)

        self.add(ab_four)

        self.play(
            self.camera.frame.animate.move_to(ab_four)
        )

        self.play(
            self.camera.frame.animate(rate_func=rush_into)\
                    .move_to(ab_four.node_by_index(0, 0)).scale(0.005)
        )


class Basics(MovingCameraScene):
    @fade
    def construct(self):
        ab_tree = ABTree(
            [
                [[1, 3]],
                [[0], [2], [4, 5, 6]],
            ],
            fill_background=False,
        )

        bee = SVGMobject("assets/bee.svg")
        bees = VGroup()
        nums = VGroup()

        ab = VGroup(Tex(r"\underline{$(a,b)$-tree}").scale(1.25), ab_tree).arrange(DOWN, buff=1.2)
        two_four = Tex(r"\underline{$(2,4)$-tree}").scale(1.25).move_to(ab[0])

        self.camera.frame.scale(0.8)

        indexes = [
            (0, 0, 0),
            (0, 0, 1),
            (1, 0, 0),
            (1, 1, 0),
            (1, 2, 0),
            (1, 2, 1),
            (1, 2, 2),
        ]

        for x, y, i in indexes:
            item = ab_tree.node_by_index(x, y)[0][i]
            bees.add(bee.copy().set_height(item.get_height()).move_to(item))
            nums.add(item.copy())
            item.set_opacity(0)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Write(ab),
                ),
                FadeIn(bees, lag_ratio=0.1),
                lag_ratio=0.5,
            ),
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    *[FadeOut(bee, shift=DOWN * 0.25, run_time=0.75)
                    for bee in bees],
                    lag_ratio=0.1,
                ),
                AnimationGroup(
                    *[FadeIn(num, shift=DOWN * 0.25, run_time=0.75)
                    for num in nums],
                    lag_ratio=0.1,
                ),
                lag_ratio=0.1,
            ),
        )

        for x, y, i in indexes:
            ab_tree.node_by_index(x, y)[0][i].set_opacity(1)

        for num in nums:
            self.remove(num)

        self.play(
            ab_tree.edges.animate.set_color(DARK_COLOR),
        )

        self.play(
            *[node[1].animate.set_color(DARK_COLOR) for node in ab_tree.nodes]
        )

        symbols = VGroup(
            Tex("$<$", stroke_width=1.5).scale(0.4).move_to(ab_tree.node_by_index(0, 0)[0][0:2]),
            Tex("$<$", stroke_width=1.5).scale(0.4).move_to(ab_tree.node_by_index(1, 2)[0][0:2]),
            Tex("$<$", stroke_width=1.5).scale(0.4).move_to(ab_tree.node_by_index(1, 2)[0][1:3]),
        )

        self.play(
            Write(symbols)
        )

        self.play(
            symbols.animate.set_color(DARK_COLOR),
            *[node[0].animate.set_color(DARK_COLOR) for node in ab_tree.nodes],
            ab_tree.leafs.animate.set_color(WHITE),
        )

        self.play(
            ab_tree.animate.set_color(WHITE),
            symbols.animate.set_color(WHITE),
        )

        # each key separates two subtrees
        self.play(
            #ab_tree.node_by_index(0, 0)[0][0].animate.set_color(WHIE),
            #ab_tree.node_by_index(0, 0)[1].animate.set_color_by_gradient((GREEN, RED)),
            ab_tree.node_by_index(0, 0)[0][1].animate.set_color(DARK_COLOR),

            symbols.animate.set_color(DARK_COLOR),

            ab_tree.subtree_by_index(1, 2).animate.set_color(DARK_COLOR),

            ab_tree.edges_by_node_index(0, 0)[2].animate.set_color(DARK_COLOR),
        )


        symbol = Tex("$<$").scale(1)\
                .move_to(VGroup(Dot().next_to(ab_tree.node_by_index(1, 0), RIGHT), Dot().next_to(ab_tree.node_by_index(1, 1), LEFT)))

        self.play(
            ab_tree.subtree_by_index(1, 0).animate.set_color(RED),
            ab_tree.edges_by_node_index(0, 0)[0].animate.set_color_by_gradient((WHITE, WHITE, RED, RED)),
            FadeIn(symbol),
        )

        self.play(
            ab_tree.subtree_by_index(1, 1).animate.set_color(GREEN),
            ab_tree.edges_by_node_index(0, 0)[1].animate.set_color_by_gradient((WHITE, WHITE, GREEN, GREEN)),
        )

        symbol2 = Tex("$<$").scale(1)\
                .move_to(VGroup(Dot().next_to(ab_tree.node_by_index(1, 1), RIGHT), Dot().next_to(ab_tree.node_by_index(1, 2), LEFT)))

        self.play(
            FadeOut(symbol),
            FadeIn(symbol2),
            #ab_tree.node_by_index(0, 0)[0][0].animate.set_color(WHIE),
            #ab_tree.node_by_index(0, 0)[1].animate.set_color_by_gradient((GREEN, RED)),
            ab_tree.node_by_index(0, 0)[0][0].animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(0, 0)[0][1].animate.set_color(WHITE),

            ab_tree.subtree_by_index(1, 0).animate.set_color(DARK_COLOR),
            ab_tree.subtree_by_index(1, 1).animate.set_color(RED),
            ab_tree.subtree_by_index(1, 2).animate.set_color(GREEN),

            ab_tree.edges_by_node_index(0, 0)[0].animate.set_color(DARK_COLOR),
            ab_tree.edges_by_node_index(0, 0)[1].animate.set_color_by_gradient((WHITE, WHITE, RED, RED)),
            ab_tree.edges_by_node_index(0, 0)[2].animate.set_color_by_gradient((GREEN, GREEN, WHITE, WHITE)),

            symbols[1].animate.set_color(GREEN),
            symbols[2].animate.set_color(GREEN),
        )

        self.play(
            ab_tree.animate.set_color(WHITE),
            symbols.animate.set_color(WHITE),
            FadeOut(symbol2),
        )

        a1 = Arrow(ORIGIN, UP * 1.05).next_to(ab[0][0][1], DOWN, buff=0.35).set_color(GRAY)
        a2 = Arrow(ORIGIN, UP * 1.05).next_to(ab[0][0][3], DOWN, buff=0.35).set_color(GRAY)

        t1 = Tex(r"\underline{\phantom{(}min. children\phantom{)}    }").scale(0.6).next_to(a1, LEFT, buff=-0.075).align_to(a1, DOWN).set_color(GRAY)
        t2 = Tex(r"\underline{    \phantom{)}max. children\phantom{)}}").scale(0.6).next_to(a2, RIGHT, buff=-0.075).align_to(a2, DOWN).set_color(GRAY)

        non_root = Tex("($2$ for root)").scale(0.6).next_to(t1, DOWN, buff=0.12).set_color(GRAY).shift(LEFT * 0.05)

        ab_tree.save_state()
        symbols.save_state()

        counts = VGroup(
            Tex("3").move_to(ab_tree.node_by_index(0, 0)).scale(1).set_z_index(10),
            Tex("2").move_to(ab_tree.node_by_index(1, 0)).scale(1).set_z_index(10),
            Tex("2").move_to(ab_tree.node_by_index(1, 1)).scale(1).set_z_index(10),
            Tex("4").move_to(ab_tree.node_by_index(1, 2)).scale(1).set_z_index(10),
            #Tex("0").move_to(ab_tree.node_by_index(2, 0)).scale(0.24).set_z_index(10),
            #Tex("0").move_to(ab_tree.node_by_index(2, 1)).scale(0.24).set_z_index(10),
            #Tex("0").move_to(ab_tree.node_by_index(2, 2)).scale(0.24).set_z_index(10),
            #Tex("0").move_to(ab_tree.node_by_index(2, 3)).scale(0.24).set_z_index(10),
            #Tex("0").move_to(ab_tree.node_by_index(2, 4)).scale(0.24).set_z_index(10),
            #Tex("0").move_to(ab_tree.node_by_index(2, 5)).scale(0.24).set_z_index(10),
            #Tex("0").move_to(ab_tree.node_by_index(2, 6)).scale(0.24).set_z_index(10),
            #Tex("0").move_to(ab_tree.node_by_index(2, 7)).scale(0.24).set_z_index(10),
        ).set_color(BLUE)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    ab_tree.node_by_index(0, 0)[0].animate.set_opacity(0),
                    ab_tree.node_by_index(1, 0)[0].animate.set_opacity(0),
                    ab_tree.node_by_index(1, 1)[0].animate.set_opacity(0),
                    ab_tree.node_by_index(1, 2)[0].animate.set_opacity(0),
                    symbols.animate.set_opacity(0),
                ),
                AnimationGroup(
                    FadeIn(counts),
                    ab_tree.edges_by_node_index(0, 0).animate.set_color(BLUE),
                    ab_tree.edges_by_node_index(1, 0).animate.set_color(BLUE),
                    ab_tree.edges_by_node_index(1, 1).animate.set_color(BLUE),
                    ab_tree.edges_by_node_index(1, 2).animate.set_color(BLUE),
                ),
                lag_ratio=0.5,
            ),
        )

        self.play(
            AnimationGroup(
                FadeIn(a1, shift=UP * 0.25),
                FadeIn(a2, shift=UP * 0.25),
                lag_ratio=0.1,
            ),
        )

        self.play(
            FadeIn(t1),
        )

        self.play(
            FadeIn(t2),
        )

        at1 = VGroup(a1, t1)
        at2 = VGroup(a2, t2)

        rect = get_fade_rect(z_index=10)

        b_copy = ab[0][0][3].copy().next_to(two_four[0][3], UP, buff=0).scale(0.6)

        self.play(
            AnimationGroup(
                ab[0][0][1].animate.next_to(two_four[0][1], UP, buff=0).scale(0.6).align_to(b_copy, DOWN).set_color(GRAY),
                FadeIn(two_four[0][1]),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                ab[0][0][3].animate.next_to(two_four[0][3], UP, buff=0).scale(0.6).set_color(GRAY),
                FadeIn(two_four[0][3]),
                lag_ratio=0.5,
            ),
        )

        ab_tree.save_state()
        counts.save_state()

        self.play(
            counts.animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(0, 0).animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(1, 0).animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(1, 1).animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(1, 2).animate.set_color(DARK_COLOR),
            ab_tree.edges_by_node_index(0, 0).animate.set_color(DARK_COLOR),
            ab_tree.edges_by_node_index(1, 0).animate.set_color(DARK_COLOR),
            ab_tree.edges_by_node_index(1, 1).animate.set_color(DARK_COLOR),
            ab_tree.edges_by_node_index(1, 2).animate.set_color(DARK_COLOR),
        )

        self.play(
            ab_tree.animate.restore(),
            counts.animate.restore(),
            ab_tree.node_by_index(1, 0).animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(1, 1).animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(1, 2).animate.set_color(DARK_COLOR),
            ab_tree.edges_by_node_index(1, 0).animate.set_color(DARK_COLOR),
            ab_tree.edges_by_node_index(1, 1).animate.set_color(DARK_COLOR),
            ab_tree.edges_by_node_index(1, 2).animate.set_color(DARK_COLOR),
            counts[1:].animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(2, 0).animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(2, 1).animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(2, 2).animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(2, 3).animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(2, 4).animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(2, 5).animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(2, 6).animate.set_color(DARK_COLOR),
            ab_tree.node_by_index(2, 7).animate.set_color(DARK_COLOR),
        )

        self.play(
            FadeIn(non_root),
        )

        ab_tree.node_by_index(0, 0)[0].set_color(WHITE),
        ab_tree.node_by_index(1, 0)[0].set_color(WHITE),
        ab_tree.node_by_index(1, 1)[0].set_color(WHITE),
        ab_tree.node_by_index(1, 2)[0].set_color(WHITE),

        self.play(
            AnimationGroup(
                AnimationGroup(
                    ab_tree.animate(lag_ratio=0).set_color(WHITE),
                    FadeOut(counts, lag_ratio=0),
                ),
                AnimationGroup(
                    ab_tree.node_by_index(0, 0)[0].animate.set_opacity(1),
                    ab_tree.node_by_index(1, 0)[0].animate.set_opacity(1),
                    ab_tree.node_by_index(1, 1)[0].animate.set_opacity(1),
                    ab_tree.node_by_index(1, 2)[0].animate.set_opacity(1),
                    lag_ratio=0,
                ),
                lag_ratio=0.5,
            ),
        )

        title_scale = 0.85
        txt_scale = 0.75

        reqs_title = Tex(r"\textbf{Invariants}").scale(title_scale)
        reqs_list = VGroup(
            Tex(r"\begin{itemize} \item leafs on the same layer \end{itemize}"),
            Tex(r"\begin{itemize} \item $a \ge 2$,\kern0.5em$b \ge 2a - 1$ \end{itemize}"),
        ).arrange(DOWN, buff=0.2).scale(txt_scale)

        reqs = VGroup(reqs_title, reqs_list).arrange(DOWN, buff=0.3)

        ops_title = Tex(r"\textbf{Operations}").scale(title_scale)
        ops_list = VGroup(
            Tex(r"\begin{itemize} \item \textit{searching} for a key \end{itemize}"),
            Tex(r"\begin{itemize} \item \textit{inserting} a key \end{itemize}"),
            Tex(r"\begin{itemize} \item \textit{deleting} a key \end{itemize}"),
        ).arrange(DOWN, buff=0.2).scale(txt_scale)

        ops = VGroup(ops_title, ops_list).arrange(DOWN, buff=0.3)

        for l in [ops_list, reqs_list]:
            for b in l:
                b.align_to(l[0], LEFT)

        ops_list.align_to(ops_title, LEFT).shift(RIGHT * 0.1)
        reqs_list.align_to(reqs_title, LEFT).shift(RIGHT * 0.1)

        ops.next_to(ab, RIGHT, buff=1.5).align_to(ab, DOWN)
        reqs.next_to(ab, RIGHT, buff=1.5).align_to(ab[0][0][0], UP)

        brace = BraceBetweenPoints(
            Dot().move_to(ab_tree).align_to(ab_tree, UP + LEFT).shift(LEFT * 0.15).get_center(),
            Dot().move_to(ab_tree).align_to(ab_tree, DOWN + LEFT).shift(LEFT * 0.15 + DOWN * 0.1).get_center(),
        )

        t = Tex(r"$$\log(n)$$").scale(0.6).rotate(PI / 2).next_to(brace, LEFT)

        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(VGroup(ab_tree, at1, at2, ops, reqs, t)).scale(1.25),
                Write(reqs_title),
                lag_ratio=0.5,
            )
        )

        self.play(FadeIn(reqs_list[0], shift=RIGHT * 0.25))

        self.play(
            FadeIn(brace, shift=RIGHT * 0.2),
            FadeIn(t, shift=RIGHT * 0.2),
        )

        self.play(FadeIn(reqs_list[1][0][:5], shift=RIGHT * 0.25))

        self.play(FadeIn(reqs_list[1][0][5:], shift=RIGHT * 0.1))

        a = CreateHighlight(reqs_list[1][0][1:4])
        b = CreateHighlight(reqs_list[1][0][5:])

        self.play(FadeIn(a))
        self.play(Transform(a, b))
        self.play(FadeOut(a))

        self.play(Write(ops_title))

        for row in ops_list:
            self.play(FadeIn(row, shift=RIGHT * 0.25))

        # TODO: convert this to insertion start


class Outro(MovingCameraScene):
    def construct(self):
        tree = ABTree(
            [
                [[]],
            ],
            fill_background=False
        ).scale(S)

        self.camera.frame.scale(0.75)

        n = 50

        nums = list(range(n))
        seed(0xDEADBEEF)
        shuffle(nums)

        def get_camera_anim():
            w_ratio = (tree.get_width() * 1.2) / self.camera.frame.get_width()
            h_ratio = (tree.get_height() * 1.5) / self.camera.frame.get_height()

            print(w_ratio, h_ratio)

            return self.camera.frame.animate.move_to(tree).scale(max(w_ratio, h_ratio, 1))

        for ii, i in enumerate(nums):
            anim, tree = tree.insert(i, scale=S)

            self.play(
                anim,
                get_camera_anim(),
                run_time = (1 if ii <= 3 else 0.7 if ii <= 5 else 0.4 if ii <= 7 else 0.25),
            )

            # yuck
            for mobject in self.mobjects:
                self.remove(mobject)
            self.add(tree)

            result = tree.bubble_insert(3, scale=S, pause_between_shift=False)

            while result is not None:
                anim, tree = result

                self.play(
                    anim,
                    get_camera_anim(),
                    run_time = (1 if ii <= 3 else 0.7 if ii <= 5 else 0.4 if ii <= 7 else 0.25),
                )

                for mobject in self.mobjects:
                    self.remove(mobject)

                self.add(tree)

                result = tree.bubble_insert(3, scale=S, pause_between_shift=False)


class Thumbnail(MovingCameraScene):
    def construct(self):
        ab = ABTree(
            [
                [[1, 3]],
                [["0"], ["0"], [4, 5, 6]],
            ],
        ).scale(2.5)

        self.add(ab)

        the = Tex("\sc The").scale(0.75)
        a = Tex("\sc a").scale(1.2)
        b = Tex("\sc b").scale(1.2)
        trees = Tex("\sc Tree")
        dash = Tex("-").set_color(BLACK).scale(1.35)

        text = VGroup(the, a, b, trees, dash).scale(2.6)

        bg = Square(fill_opacity=1).set_z_index(-1).set_color_by_gradient(("#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51"))\
                .stretch_to_fit_width(self.camera.frame.get_width())\
                .stretch_to_fit_height(self.camera.frame.get_height())
        ab.set_color(BLACK)

        for e in ab.edges_individually:
            e.scale(1.25).set_stroke_width(15)

        ab.node_by_index(0, 0)[0].become(the.move_to(ab.node_by_index(0, 0)[0]))
        ab.node_by_index(1, 0)[0].become(a.move_to(ab.node_by_index(1, 0)[0]))
        ab.node_by_index(1, 1)[0].become(b.move_to(ab.node_by_index(1, 1)[0]))
        ab.node_by_index(1, 2)[0].become(trees.move_to(ab.node_by_index(1, 2)[0]))

        dash.scale(1.25)
        dash.move_to(VGroup(a, b))

        self.add(text, bg)

        self.wait()


class Search(MovingCameraScene):
    @fade
    def construct(self):

        ab_tree = ABTree(
            [
                [[1, 3]],
                [[0], [2], [4, 5, 6]],
            ],
            fill_background=False,
        )

        ab = VGroup(Tex(r"\underline{\textit{Search}}").scale(1.25), ab_tree).arrange(DOWN, buff=1).scale(S)

        self.play(
            AnimationGroup(
                Write(ab[0]),
                Write(ab_tree),
                lag_ratio=0.5,
            )
        )

        ab_tree.search_but_like_animate(5, self, scale=S)
        ab_tree.search_but_like_animate(7, self, scale=S, speedup=2)


class Insertion(MovingCameraScene):
    @fade
    def construct(self):
        ab_tree = ABTree(
            [
                [[1, 3]],
                [[0], [2], [4, 5, 6]],
            ],
            fill_background=False
        )

        ab = VGroup(Tex(r"\underline{\textit{Search}}").scale(1.25), ab_tree).arrange(DOWN, buff=1).scale(S)

        ins = Tex(r"\underline{\textit{Insertion}}").scale(1.25).scale(S).move_to(ab[0])

        self.add(ab)

        self.play(
            FadeOut(ab[0], shift=LEFT * 3.7),
            FadeIn(ins, shift=LEFT * 3.7),
        )

        target, qs = ab_tree.search_but_like_animate(7, self, scale=S, speedup=5, no_cleanup=True)

        def darken_our_tree(tree):
            tree.subtree_by_index(1, 0).set_color(DARK_COLOR)
            tree.subtree_by_index(1, 1).set_color(DARK_COLOR)
            tree.node_by_index(0, 0).set_color(DARK_COLOR)
            tree.edges_by_node_index(0, 0).set_color(DARK_COLOR)

        anim, tree = ab_tree.insert(7, scale=S, transform_instead=target, tree_transform_function=darken_our_tree)

        self.play(
            AnimationGroup(
                FadeOut(qs),
                anim,
                lag_ratio=0.5,
            )
        )

        # yuck
        for mobject in self.mobjects:
            self.remove(mobject)
        self.add(tree, ins)

        self.play(tree.animate.set_color(WHITE))

        self.play(
            tree.node_by_index(1, 2)[1].animate.set_stroke_color(RED),
            tree.node_by_index(1, 2)[0].animate.set_color(RED),
            tree.edges_by_node_index(1, 2).animate.set_color(RED),
        )

        anim, tree = tree.bubble_insert(4, scale=S, pause_between_shift=True)
        self.play(anim)

        # yuck
        for mobject in self.mobjects:
            self.remove(mobject)
        self.add(tree, ins)

        self.play(
            tree.node_by_index(0, 0).animate.set_color(BLUE),
            tree.edges_by_node_index(0, 0).animate.set_color(BLUE),
        )

        self.play(
            tree.node_by_index(0, 0).animate.set_color(WHITE),
            tree.edges_by_node_index(0, 0).animate.set_color(WHITE),
        )

        for i in [8, 9]:
            target = Tex(f"${i}$").next_to(tree.node_by_index(0, 0), UP).scale(1.2).set_z_index(10)
            self.play(FadeIn(target, shift=UP * 0.1))

            anim, tree = tree.insert(i, scale=S, transform_instead=target)

            self.play(anim)

            # yuck
            for mobject in self.mobjects:
                self.remove(mobject)
            self.add(tree, ins)

        self.play(
            tree.node_by_index(1, 3).animate.set_color(RED),
            tree.edges_by_node_index(1, 3).animate.set_color(RED),
        )

        anim, tree = tree.bubble_insert(4, scale=S)

        self.play(anim)

        for mobject in self.mobjects:
            self.remove(mobject)
        self.add(tree, ins)

        self.play(
            tree.node_by_index(0, 0).animate.set_color(RED),
            tree.edges_by_node_index(0, 0).animate.set_color(RED),
        )

        anim, tree = tree.bubble_insert(4, scale=S)

        new_ins = ins.copy().shift(UP)

        self.play(
            anim,
            self.camera.frame.animate.move_to(VGroup(new_ins, tree)).set_height(VGroup(new_ins, tree).get_height() * 1.4),
            Transform(ins, new_ins),
        )

        for mobject in self.mobjects:
            self.remove(mobject)
        self.add(tree, ins)

        self.camera.frame.save_state()
        tree.save_state()

        g = VGroup(tree.subtree_by_index(2, 3), tree.subtree_by_index(2, 4))

        eq = Tex(r"$$\lfloor (b+1)/2 \rfloor \ge  \lfloor 2a  / 2 \rfloor = a$$").next_to(g, DOWN, buff=0.75)
        g.add(eq)

        self.play(
            self.camera.frame.animate.move_to(g).scale(0.65),
            tree.subtree_by_index(1, 0).animate.set_color(DARK_COLOR),
            tree.node_by_index(0, 0).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(0, 0).animate.set_color(DARK_COLOR),
            tree.subtree_by_index(2, 2).animate.set_color(DARK_COLOR),
            tree.node_by_index(1, 1).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(1, 1).animate.set_color(DARK_COLOR),
            ins.animate.set_color(DARK_COLOR),
        )

        self.play(
            Write(eq[0][:9]),
        )

        ba = Tex(r"$$\overbrace{b \ge 2a - 1}^{\phantom{.}}$$").next_to(eq[0][9], DOWN, buff=0.05).scale(0.8).set_color(GRAY)

        self.play(
            FadeIn(eq[0][9]),
            FadeIn(ba),
        )

        self.play(
            Write(eq[0][10:]),
        )

        g = VGroup(tree.node_by_index(0, 0), tree.node_by_index(1, 0), tree.node_by_index(1, 1))

        a1 = Arrow(ORIGIN, RIGHT * 1.25).next_to(tree.node_by_index(0, 0), LEFT, buff=0.65)
        text = Tex("2 children").next_to(a1, LEFT)

        self.play(
            FadeOut(eq),
            FadeOut(ba),
            self.camera.frame.animate.move_to(g),
            tree.subtree_by_index(2, 0).animate.set_color(DARK_COLOR),
            tree.subtree_by_index(2, 1).animate.set_color(DARK_COLOR),
            tree.subtree_by_index(2, 2).animate.set_color(DARK_COLOR),
            tree.subtree_by_index(2, 3).animate.set_color(DARK_COLOR),
            tree.subtree_by_index(2, 4).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(1, 0).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(1, 1).animate.set_color(DARK_COLOR),

            tree.edges_by_node_index(0, 0).animate.set_color(WHITE),
            tree.node_by_index(0, 0).animate.set_color(WHITE),
            tree.node_by_index(1, 0).animate.set_color(WHITE),
            tree.node_by_index(1, 1).animate.set_color(WHITE),

            ins.animate.set_color(DARK_COLOR),
        )

        self.play(
            AnimationGroup(
                Write(text, run_time=1),
                FadeIn(a1),
                lag_ratio=0.5,
            ),
        )

        self.play(
            FadeOut(a1),
            FadeOut(text),
            self.camera.frame.animate.restore(),
            tree.animate.restore(),
            ins.animate.set_color(WHITE),
        )

class Deletion(MovingCameraScene):
    @fade
    def construct(self):
        ### NOTE: this is literally a copy-paste of the entire insertion
        self.next_section(skip_animations=True)


        ab_tree = ABTree(
            [
                [[1, 3]],
                [[0], [2], [4, 5, 6]],
            ],
            fill_background=False
        )

        ab = VGroup(Tex(r"\underline{\textit{Search}}").scale(1.25), ab_tree).arrange(DOWN, buff=1).scale(S)

        ins = Tex(r"\underline{\textit{Insertion}}").scale(1.25).scale(S).move_to(ab[0])

        self.add(ab)

        self.play(
            FadeOut(ab[0], shift=LEFT * 3.7),
            FadeIn(ins, shift=LEFT * 3.7),
        )

        target, qs = ab_tree.search_but_like_animate(7, self, scale=S, speedup=5, no_cleanup=True)

        def darken_our_tree(tree):
            tree.subtree_by_index(1, 0).set_color(DARK_COLOR)
            tree.subtree_by_index(1, 1).set_color(DARK_COLOR)
            tree.node_by_index(0, 0).set_color(DARK_COLOR)
            tree.edges_by_node_index(0, 0).set_color(DARK_COLOR)

        anim, tree = ab_tree.insert(7, scale=S, transform_instead=target, tree_transform_function=darken_our_tree)

        self.play(
            AnimationGroup(
                FadeOut(qs),
                anim,
                lag_ratio=0.5,
            )
        )

        # yuck
        for mobject in self.mobjects:
            self.remove(mobject)
        self.add(tree, ins)

        self.play(tree.animate.set_color(WHITE))

        self.play(
            tree.node_by_index(1, 2)[1].animate.set_stroke_color(RED),
            tree.node_by_index(1, 2)[0].animate.set_color(RED),
            tree.edges_by_node_index(1, 2).animate.set_color(RED),
        )

        anim, tree = tree.bubble_insert(4, scale=S, pause_between_shift=True)
        self.play(anim)

        # yuck
        for mobject in self.mobjects:
            self.remove(mobject)
        self.add(tree, ins)

        self.play(
            tree.node_by_index(0, 0).animate.set_color(BLUE),
            tree.edges_by_node_index(0, 0).animate.set_color(BLUE),
        )

        self.play(
            tree.node_by_index(0, 0).animate.set_color(WHITE),
            tree.edges_by_node_index(0, 0).animate.set_color(WHITE),
        )

        for i in [8, 9]:
            target = Tex(f"${i}$").next_to(tree.node_by_index(0, 0), UP).scale(1.2).set_z_index(10)
            self.play(FadeIn(target, shift=UP * 0.1))

            anim, tree = tree.insert(i, scale=S, transform_instead=target)

            self.play(anim)

            # yuck
            for mobject in self.mobjects:
                self.remove(mobject)
            self.add(tree, ins)

        self.play(
            tree.node_by_index(1, 3).animate.set_color(RED),
            tree.edges_by_node_index(1, 3).animate.set_color(RED),
        )

        anim, tree = tree.bubble_insert(4, scale=S)

        self.play(anim)

        for mobject in self.mobjects:
            self.remove(mobject)
        self.add(tree, ins)

        self.play(
            tree.node_by_index(0, 0).animate.set_color(RED),
            tree.edges_by_node_index(0, 0).animate.set_color(RED),
        )

        anim, tree = tree.bubble_insert(4, scale=S)

        new_ins = ins.copy().shift(UP)

        self.play(
            anim,
            self.camera.frame.animate.move_to(VGroup(new_ins, tree)).set_height(VGroup(new_ins, tree).get_height() * 1.4),
            Transform(ins, new_ins),
        )

        for mobject in self.mobjects:
            self.remove(mobject)
        self.add(tree, ins)

        self.camera.frame.save_state()
        tree.save_state()

        g = VGroup(tree.subtree_by_index(2, 3), tree.subtree_by_index(2, 4))

        eq = Tex(r"$$\lfloor (b+1)/2 \rfloor \ge  \lfloor 2a  / 2 \rfloor = a$$").next_to(g, DOWN, buff=0.75)
        g.add(eq)

        self.play(
            self.camera.frame.animate.move_to(g).scale(0.65),
            tree.subtree_by_index(1, 0).animate.set_color(DARK_COLOR),
            tree.node_by_index(0, 0).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(0, 0).animate.set_color(DARK_COLOR),
            tree.subtree_by_index(2, 2).animate.set_color(DARK_COLOR),
            tree.node_by_index(1, 1).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(1, 1).animate.set_color(DARK_COLOR),
            ins.animate.set_color(DARK_COLOR),
        )

        self.play(
            Write(eq[0][:9]),
        )

        ba = Tex(r"$$\overbrace{b \ge 2a - 1}^{\phantom{.}}$$").next_to(eq[0][9], DOWN, buff=0.05).scale(0.8).set_color(GRAY)

        self.play(
            FadeIn(eq[0][9]),
            FadeIn(ba),
        )

        self.play(
            Write(eq[0][10:]),
        )

        g = VGroup(tree.node_by_index(0, 0), tree.node_by_index(1, 0), tree.node_by_index(1, 1))

        a1 = Arrow(ORIGIN, RIGHT * 1.25).next_to(tree.node_by_index(0, 0), LEFT, buff=0.65)
        text = Tex("2 children").next_to(a1, LEFT)

        self.play(
            FadeOut(eq),
            FadeOut(ba),
            self.camera.frame.animate.move_to(g),
            tree.subtree_by_index(2, 0).animate.set_color(DARK_COLOR),
            tree.subtree_by_index(2, 1).animate.set_color(DARK_COLOR),
            tree.subtree_by_index(2, 2).animate.set_color(DARK_COLOR),
            tree.subtree_by_index(2, 3).animate.set_color(DARK_COLOR),
            tree.subtree_by_index(2, 4).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(1, 0).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(1, 1).animate.set_color(DARK_COLOR),

            tree.edges_by_node_index(0, 0).animate.set_color(WHITE),
            tree.node_by_index(0, 0).animate.set_color(WHITE),
            tree.node_by_index(1, 0).animate.set_color(WHITE),
            tree.node_by_index(1, 1).animate.set_color(WHITE),

            ins.animate.set_color(DARK_COLOR),
        )

        self.play(
            AnimationGroup(
                Write(text, run_time=1),
                FadeIn(a1),
                lag_ratio=0.5,
            ),
        )

        self.play(
            FadeOut(a1),
            FadeOut(text),
            self.camera.frame.animate.restore(),
            tree.animate.restore(),
            ins.animate.set_color(WHITE),
        )



        ### NOTE: the copy-paste ends here
        self.next_section()

        dl = Tex(r"\underline{\textit{Deletion}}").scale(1.25).scale(S).move_to(ins)

        self.play(
            FadeOut(ins, shift=LEFT * 4.2),
            FadeIn(dl, shift=LEFT * 4.2),
        )

        ab_tree = ABTree(
            [
                [[3]],
                [[1], [5, 7]],
                [[0], [2], [4], [6], [8, 9]],
            ],
            fill_background=False,
        ).scale(S).move_to(tree)

        for mobject in self.mobjects:
            self.remove(mobject)

        self.add(ab_tree, dl)

        target, qs = ab_tree.search_but_like_animate(9, self, scale=S, speedup=5, no_cleanup=True)

        def darken_our_tree(tree):
            tree.subtree_by_index(1, 0).set_color(DARK_COLOR)
            tree.subtree_by_index(2, 2).set_color(DARK_COLOR)
            tree.subtree_by_index(2, 3).set_color(DARK_COLOR)
            tree.node_by_index(0, 0).set_color(DARK_COLOR)
            tree.node_by_index(1, 1).set_color(DARK_COLOR)
            tree.edges_by_node_index(0, 0).set_color(DARK_COLOR)
            tree.edges_by_node_index(1, 1).set_color(DARK_COLOR)

        for mobject in self.mobjects:
            self.remove(mobject)

        self.add(dl)

        # NOTE: 9
        anim, tree = ab_tree.delete(9, scale=S, tree_transform_function=darken_our_tree)

        self.play(
            FadeOut(target),
            FadeOut(qs),
            anim,
        )

        for mobject in self.mobjects:
            self.remove(mobject)

        self.add(dl, tree)

        self.play(tree.animate.set_color(WHITE))

        # NOTE: 3
        target = Tex("$3$").next_to(tree.node_by_index(0, 0), UP).scale(0.8 * S)

        self.play(
            FadeIn(target, shift=UP * 0.1),
            target.animate.set_color(GREEN),
            tree.node_by_index(0, 0)[0].animate.set_color(GREEN),
        )

        self.play(
            FadeOut(target),
            tree.node_by_index(0, 0)[0].animate.set_opacity(0),
        )

        self.play(
            #tree.subtree_by_index(2, 0).animate.set_color(DARK_COLOR),
            #tree.subtree_by_index(2, 3).animate.set_color(DARK_COLOR),
            #tree.subtree_by_index(2, 4).animate.set_color(DARK_COLOR),

            tree.edges_by_node_index(2, 0).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(2, 3).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(2, 4).animate.set_color(DARK_COLOR),

            tree.edges_by_node_index(2, 1).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(2, 2).animate.set_color(DARK_COLOR),

            tree.node_by_index(1, 0).animate.set_color(DARK_COLOR),
            tree.node_by_index(1, 1).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(0, 0).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(1, 0).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(1, 1).animate.set_color(DARK_COLOR),

            tree.node_by_index(3, 0).animate.set_color(DARK_COLOR),
            tree.node_by_index(3, 1).animate.set_color(DARK_COLOR),
            tree.node_by_index(3, 2).animate.set_color(DARK_COLOR),
            tree.node_by_index(3, 3).animate.set_color(DARK_COLOR),
            tree.node_by_index(3, 4).animate.set_color(DARK_COLOR),
            tree.node_by_index(3, 5).animate.set_color(DARK_COLOR),
            tree.node_by_index(3, 6).animate.set_color(DARK_COLOR),
            tree.node_by_index(3, 7).animate.set_color(DARK_COLOR),
            tree.node_by_index(3, 8).animate.set_color(DARK_COLOR),
            tree.node_by_index(3, 9).animate.set_color(DARK_COLOR),
        )

        self.play(
            tree.subtree_by_index(2, 0).animate.set_color(DARK_COLOR),
            tree.subtree_by_index(2, 3).animate.set_color(DARK_COLOR),
            tree.subtree_by_index(2, 4).animate.set_color(DARK_COLOR),

            tree.node_by_index(2, 1).animate.set_color(ORANGE),
            tree.node_by_index(2, 2).animate.set_color(ORANGE),
        )

        self.play(
            tree.node_by_index(2, 1).animate.set_color(DARK_COLOR),
        )

        self.play(
            tree.node_by_index(1, 1).animate.set_color(WHITE),
            tree.edges_by_node_index(1, 1).animate.set_color(WHITE),
            tree.edges_by_node_index(0, 0)[1].animate.set_color(WHITE),
            tree.subtree_by_index(2, 3).animate.set_color(WHITE),
            tree.subtree_by_index(2, 4).animate.set_color(WHITE),

            tree.node_by_index(3, 4).animate.set_color(WHITE),
            tree.node_by_index(3, 5).animate.set_color(WHITE),
            tree.edges_by_node_index(2, 2).animate.set_color(WHITE),
        )

        self.play(
            tree.node_by_index(1, 1)[0].animate.set_color(DARK_COLOR),
            tree.node_by_index(2, 3)[0].animate.set_color(DARK_COLOR),
            tree.node_by_index(2, 4)[0].animate.set_color(DARK_COLOR),
        )

        new_tree = ABTree(
            [
                [[4]],
                [[1], [5, 7]],
                [[0], [2], [3], [6], [8]],
            ],
            fill_background=False,
        ).scale(S).move_to(tree)

        new_tree.subtree_by_index(1, 0).set_color(DARK_COLOR)
        new_tree.edges_by_node_index(0, 0)[0].set_color(DARK_COLOR)
        new_tree.node_by_index(2, 2)[0].set_color(ORANGE)
        new_tree.node_by_index(2, 2)[1].set_color(ORANGE)
        new_tree.node_by_index(0, 0)[0].set_color(DARK_GRAY)
        new_tree.node_by_index(1, 1)[0].set_color(DARK_COLOR)
        new_tree.node_by_index(2, 3)[0].set_color(DARK_COLOR)
        new_tree.node_by_index(2, 4)[0].set_color(DARK_COLOR)
        tree.node_by_index(0, 0)[0].set_color(DARK_GRAY)
        tree.node_by_index(1, 1)[0].set_color(DARK_COLOR)
        tree.node_by_index(2, 3)[0].set_color(DARK_COLOR)
        tree.node_by_index(2, 4)[0].set_color(DARK_COLOR)

        self.play(
            Transform(tree, new_tree),
            tree.node_by_index(2, 2)[0].animate.move_to(tree.node_by_index(0, 0)[0]),
            tree.node_by_index(0, 0)[0].animate.set_opacity(0),  # hack lmao
        )

        self.play(
            tree.animate.set_color(WHITE),
        )

        for mobject in self.mobjects:
            self.remove(mobject)

        tree = ABTree(
            [
                [[4]],
                [[1], [5, 7]],
                [[0], [2], [3], [6], [8]],
            ],
            fill_background=False,
        ).scale(S).move_to(tree)

        wow = tree.node_by_index(0, 0)[0].copy().set_opacity(1).move_to(tree.node_by_index(0, 0)[0])

        tree.node_by_index(2, 2)[0].set_opacity(0)

        def idk(tree):
            tree.node_by_index(0, 0)[0].become(wow)
            tree.node_by_index(2, 2)[0].set_opacity(0)

        self.add(dl)

        # NOTE: 4
        anim, tree = tree.delete(((2, 2), 3), scale=S, tree_transform_function=idk)

        self.play(
            anim,
        )

        for mobject in self.mobjects:
            self.remove(mobject)

        tree = ABTree(
            [
                [[4]],
                [[1], [5, 7]],
                [[0], [2], [], [6], [8]],
            ],
            fill_background=False,
        ).scale(S).move_to(tree)

        self.add(tree, dl)

        self.play(
            tree.node_by_index(2, 2).animate.set_color(RED),
            tree.edges_by_node_index(2, 2).animate.set_color(RED),
        )

        self.camera.frame.save_state()

        g = VGroup(tree.subtree_by_index(1, 1))

        a = VGroup(Tex(r"\textbf{a)} merge nodes"), Tex(r"\textbf{b)} steal a key")).arrange(DOWN)
        a[1].align_to(a[0], LEFT)
        a.next_to(g, RIGHT, buff=0.75)

        self.play(
            tree.subtree_by_index(1, 0).animate.set_color(DARK_COLOR),
            tree.node_by_index(0, 0).animate.set_color(DARK_COLOR),
            tree.edges_by_node_index(0, 0).animate.set_color(DARK_COLOR),
            self.camera.frame.animate.move_to(g).scale(0.65),
        )

        self.play(
            tree.node_by_index(2, 3).animate.set_color(BLUE),
        )

        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(VGroup(g, a)),
                FadeIn(a[0]),
                lag_ratio=0.5,
            ),
        )

        self.play(
            FadeIn(a[1]),
        )

        self.play(
            tree.subtree_by_index(3, 5).animate.set_color(BLUE),
            tree.subtree_by_index(3, 6).animate.set_color(BLUE),
            tree.edges_by_node_index(2, 3).animate.set_color(BLUE),
        )

        self.play(
            tree.subtree_by_index(1, 1).animate.set_color(WHITE),
            a[1].animate.set_color(DARK_COLOR),
        )

        for mobject in self.mobjects:
            self.remove(mobject)

        self.add(dl, a)
        self.add(tree.node_by_index(0, 0))

        def f(tree):
            tree.subtree_by_index(1, 0).set_color(DARK_COLOR),
            tree.node_by_index(0, 0).set_color(DARK_COLOR),
            tree.edges_by_node_index(0, 0).set_color(DARK_COLOR),

        anim, new_tree = tree.bubble_delete(2, scale=S, tree_transform_function=f)

        # this is supremely scuffed
        #self.add(new_tree.node_by_index(0, 0))
        self.add(dl)

        self.play(
            anim,
            AnimationGroup(
                Wait(1),
                AnimationGroup(
                    Transform(tree.subtree_by_index(1, 0), new_tree.subtree_by_index(1, 0), run_time=1),
                    Transform(tree.edges_by_node_index(0, 0), new_tree.edges_by_node_index(0, 0), run_time=1),
                ),
                lag_ratio=0.4,
            ),
        )

        for mobject in self.mobjects:
            self.remove(mobject)

        tree = ABTree(
            [
                [[4]],
                [[1], [7]],
                [[0], [2], [5, 6], [8]],
            ],
            fill_background=False,
        ).scale(S)

        align_object_by_coords(tree, tree.node_by_index(0, 0), new_tree.node_by_index(0, 0))

        self.add(dl, tree, a)

        f(tree)

        self.play(
            tree.node_by_index(1, 1).animate.set_color(BLUE),
            tree.edges_by_node_index(1, 1).animate.set_color(BLUE),
        )

        self.play(
            tree.node_by_index(1, 1).animate.set_color(WHITE),
            tree.edges_by_node_index(1, 1).animate.set_color(WHITE),
            a[0].animate.set_color(DARK_COLOR),
            a[1].animate.set_color(WHITE),
        )

        for mobject in self.mobjects:
            self.remove(mobject)

        self.add(dl, a)

        # NOTE: 8
        anim, tree = tree.delete(8, scale=S, tree_transform_function=f)

        self.play(
            anim,
        )

        for mobject in self.mobjects:
            self.remove(mobject)

        tree = ABTree(
            [
                [[4]],
                [[1], [7]],
                [[0], [2], [5, 6], []],
            ],
            fill_background=False,
        ).scale(S).move_to(tree)

        tree_to_transform = ABTree(
            [
                [[4]],
                [[1], [6]],
                [[0], [2], [5], [7]],
            ],
            fill_background=False,
        ).scale(S).move_to(tree)

        self.add(tree, dl, a)

        f(tree)
        f(tree_to_transform)

        self.play(
            tree.node_by_index(2, 3).animate.set_color(RED),
            tree.edges_by_node_index(2, 3).animate.set_color(RED),
        )

        self.play(
            tree.subtree_by_index(2, 2).animate.set_color(BLUE),
        )

        # TODO: yikes
        self.play(
            Transform(tree.subtree_by_index(1, 0), tree_to_transform.subtree_by_index(1, 0)),
            Transform(tree.edges_by_node_index(0, 0), tree_to_transform.edges_by_node_index(0, 0)),
            Transform(tree.node_by_index(0, 0), tree_to_transform.node_by_index(0, 0)),
            Transform(tree.node_by_index(1, 1)[0][0], tree_to_transform.node_by_index(2, 3)[0][0]),
            Transform(tree.node_by_index(2, 2)[0][1], tree_to_transform.node_by_index(1, 1)[0][0]),
            Transform(tree.node_by_index(2, 2)[0][0], tree_to_transform.node_by_index(2, 2)[0][0]),
            Transform(tree.node_by_index(2, 2)[1], tree_to_transform.node_by_index(2, 2)[1]),
            Transform(tree.node_by_index(3, 4), tree_to_transform.node_by_index(3, 4)),
            Transform(tree.node_by_index(3, 5), tree_to_transform.node_by_index(3, 5)),
            Transform(tree.node_by_index(3, 6), tree_to_transform.node_by_index(3, 6)),
            Transform(tree.node_by_index(3, 7), tree_to_transform.node_by_index(3, 7)),
            Transform(tree.edges_by_node_index(1, 1), tree_to_transform.edges_by_node_index(1, 1)),
            Transform(tree.edges_by_node_index(2, 2)[0], tree_to_transform.edges_by_node_index(2, 2)[0]),
            Transform(tree.edges_by_node_index(2, 2)[1], tree_to_transform.edges_by_node_index(2, 2)[1]),
            Transform(tree.edges_by_node_index(2, 2)[2], tree_to_transform.edges_by_node_index(2, 3)[0]),
            Transform(tree.edges_by_node_index(2, 3)[0], tree_to_transform.edges_by_node_index(2, 3)[1]),
            Transform(tree.node_by_index(2, 3)[1], tree_to_transform.node_by_index(2, 3)[1]),
        )

        ab_tree_both = ABTree(
            [
                [[4]],
                [[1], [6, 8]],
                [[0], [2], [5], [], [9, 10]],
            ],
            fill_background=False,
        ).scale(S * 0.75).move_to(tree).align_to(tree, RIGHT).align_to(tree, DOWN).shift(DOWN * 7.8)
        ab_tree_both.subtree_by_index(1, 0).set_color(DARK_COLOR)
        ab_tree_both.node_by_index(0, 0).set_color(DARK_COLOR)
        ab_tree_both.edges_by_node_index(0, 0).set_color(DARK_COLOR)

        ab_tree_both.subtree_by_index(2, 2).set_color(BLUE)
        ab_tree_both.subtree_by_index(2, 4).set_color(BLUE)

        self.add(ab_tree_both)

        # NOTE: sorta copy-pasted
        ab_tree_to_transform = ABTree(
            [
                [[4]],
                [[1], [6, 9]],
                [[0], [2], [5], [8], [10]],
            ],
            fill_background=False,
        ).scale(S * 0.75).move_to(ab_tree_both).align_to(ab_tree_both, RIGHT).align_to(ab_tree_both, DOWN)
        ab_tree_to_transform.subtree_by_index(1, 0).set_color(DARK_COLOR)
        ab_tree_to_transform.node_by_index(0, 0).set_color(DARK_COLOR)
        ab_tree_to_transform.edges_by_node_index(0, 0).set_color(DARK_COLOR)

        self.play(
            self.camera.frame.animate.shift(DOWN * 8),
            a[0].animate.shift(DOWN * 8).set_color(WHITE),
            a[1].animate.shift(DOWN * 8),
        )

        high = CreateHighlight(a[1])

        self.play(
            a[0].animate.set_color(DARK_COLOR),
            ab_tree_both.subtree_by_index(2, 2).animate.set_color(WHITE),
            ab_tree_both.subtree_by_index(2, 4).animate.set_color(GREEN),
        )

        self.play(
            Transform(ab_tree_both.subtree_by_index(1, 0), ab_tree_to_transform.subtree_by_index(1, 0)),
            Transform(ab_tree_both.node_by_index(0, 0), ab_tree_to_transform.node_by_index(0, 0)),
            Transform(ab_tree_both.edges_by_node_index(0, 0), ab_tree_to_transform.edges_by_node_index(0, 0)),

            Transform(ab_tree_both.edges_by_node_index(1, 1), ab_tree_to_transform.edges_by_node_index(1, 1)),
            Transform(ab_tree_both.node_by_index(1, 1)[1], ab_tree_to_transform.node_by_index(1, 1)[1]),
            Transform(ab_tree_both.node_by_index(1, 1)[0][0], ab_tree_to_transform.node_by_index(1, 1)[0][0]),
            Transform(ab_tree_both.node_by_index(1, 1)[0][1], ab_tree_to_transform.node_by_index(2, 3)[0][0]),
            Transform(ab_tree_both.node_by_index(2, 3)[1], ab_tree_to_transform.node_by_index(2, 3)[1]),
            Transform(ab_tree_both.node_by_index(2, 4)[1], ab_tree_to_transform.node_by_index(2, 4)[1]),
            Transform(ab_tree_both.node_by_index(2, 4)[0][0], ab_tree_to_transform.node_by_index(1, 1)[0][1]),
            Transform(ab_tree_both.node_by_index(2, 4)[0][1], ab_tree_to_transform.node_by_index(2, 4)[0][0]),

            Transform(ab_tree_both.edges_by_node_index(2, 3)[0], ab_tree_to_transform.edges_by_node_index(2, 3)[0]),
            Transform(ab_tree_both.edges_by_node_index(2, 4)[0], ab_tree_to_transform.edges_by_node_index(2, 3)[1]),
            Transform(ab_tree_both.edges_by_node_index(2, 4)[1], ab_tree_to_transform.edges_by_node_index(2, 4)[0]),
            Transform(ab_tree_both.edges_by_node_index(2, 4)[2], ab_tree_to_transform.edges_by_node_index(2, 4)[1]),

            Transform(ab_tree_both.node_by_index(3, 7), ab_tree_to_transform.node_by_index(3, 7)),
            Transform(ab_tree_both.node_by_index(3, 8), ab_tree_to_transform.node_by_index(3, 8)),
            Transform(ab_tree_both.node_by_index(3, 9), ab_tree_to_transform.node_by_index(3, 9)),

            Transform(ab_tree_both.subtree_by_index(2, 2), ab_tree_to_transform.subtree_by_index(2, 2)),
        )

        tree.set_color(WHITE)
        tc = tree.copy()
        tree.move_to(self.camera.frame).align_to(tc, DOWN)

        dl.align_to(dl.copy().move_to(tree), RIGHT)

        self.play(
            self.camera.frame.animate.move_to(VGroup(tree, dl)).scale(1/0.65),
            FadeOut(a),
        )


class Summary(MovingCameraScene):
    @fade
    def construct(self):
        ab_tree = ABTree(
            [
                [[2, 4]],
                [[1], [3], [5, 6, 7]],
            ],
            fill_background=False
        )

        ab = VGroup(Tex(r"Operation Summary").scale(1.25), ab_tree).arrange(UP, buff=1.5).scale(S)


        table = Table(
            [
                [Tex(r"\underline{\textit{Search}}"), Tex(r"find where in the node it should be and go down")],
                [Tex(r"\underline{\textit{Insertion}}"), Tex(r"search, insert the key + leaf and maybe split")],
                [Tex(r"\underline{\textit{Deletion}}"), Tex(r"search, remove (possibly swapping) and maybe merge/steal")],
            ],
            v_buff=0.8,
            h_buff=0.6,
            element_to_mobject=lambda x: x,
            include_outer_lines=True,
            arrange_in_grid_config={"col_alignments": "rl"},
            col_labels=[Tex(r"\textbf{Operation}"), Tex(r"\textbf{Summary}")],
        ).scale(0.7)

        table.remove(*table.get_vertical_lines())

        table.get_horizontal_lines()[2].set_stroke_width(1.5)
        table.get_horizontal_lines()[3].set_opacity(0)
        table.get_horizontal_lines()[4].set_opacity(0)

        #self.play(
        #    Write(ab[0], run_time=1),
        #)

        shift = 0.25
        for i in range(2):
            table.get_entries((2 + i + 1,1)).shift(UP * (shift) * (i + 1))
            table.get_entries((2 + i + 1,2)).shift(UP * (shift) * (i + 1))

        table.get_horizontal_lines()[1].shift(UP * (shift) * (i + 1))

        table.move_to(ab[1])


        self.play(
            FadeIn(
                VGroup(
                    table.get_horizontal_lines()[0],
                    table.get_col_labels(),
                    table.get_horizontal_lines()[2],
                    table.get_horizontal_lines()[1],
                )
            )
        )

        for i in range(3):
            self.play(
                FadeIn(table.get_entries((2 + i,1)), shift=RIGHT * 0.25)
            )

            self.play(
                Write(table.get_entries((2 + i,2)), run_time=1.5)
            )


class Benchmark(MovingCameraScene):
    @fade
    def construct(self):
        g = get_benchmark_graph()

        g = VGroup(*g)

        self.add(g[-1][0][1][7])
        self.add(g[-1][0][2][7])

        self.wait()


class SelectingAB(MovingCameraScene):
    @fade
    def construct(self):
        tree = ABTree(
            [
                [[4]],
                [[1], [6]],
                [[0], [2], [5], [7]],
            ],
            fill_background=False,
        )

        ab = VGroup(Tex(r"\underline{\textit{Deletion}}").scale(1.25), tree).arrange(DOWN, buff=1).scale(S)

        ab_text = Tex(r"\underline{$(a,b)$-tree}").scale(1.25).move_to(ab[0]).scale(S)

        # copy-pasted
        self.camera.frame.move_to(VGroup(ab)).set_height(VGroup(ab).get_height() * 1.4)

        self.add(ab)

        self.play(
            FadeOut(ab[0], shift=LEFT * 4.2),
            FadeIn(ab_text, shift=LEFT * 4.2),
        )

        q1 = Tex("?").move_to(ab_text[0][1]).scale(1.25 * S)
        q2 = Tex("?").move_to(ab_text[0][3]).scale(1.25 * S).align_to(q1, DOWN)

        two = Tex("2").move_to(ab_text[0][1]).scale(1.25 * S)
        four = Tex("4").move_to(ab_text[0][3]).scale(1.25 * S).align_to(q1, DOWN)

        self.play(
            self.camera.frame.animate.move_to(ab_text).scale(0.5),
            ReplacementTransform(ab_text[0][1], q1),
            ReplacementTransform(ab_text[0][3], q2),
            tree.animate.set_color(DARK_COLOR).shift(DOWN * 2),
        )

        q1.set_z_index(10)
        q2.set_z_index(10)
        ab_text.set_z_index(10)

        self.remove(tree)

        cpu = SVGMobject("assets/cpu.svg").next_to(ab_text, DOWN, buff=1).set_color(WHITE)

        self.play(
            self.camera.frame.animate.move_to(VGroup(ab_text, cpu)).scale(1.25),
            FadeIn(cpu),
        )

        cache = SVGMobject("assets/cache_line.svg").next_to(ab_text, DOWN, buff=1).scale(1.25)

        g = VGroup(cpu.copy(), cache).arrange(buff=1.5 / 2).move_to(cpu)

        tree_to_steal_from = ABTree(
            [
                [[2, 4]],
                [[1], [3], [5, 6, 7, 8]],
            ],
            fill_background=False,
        ).scale(0.75)

        self.play(
            AnimationGroup(
                Transform(cpu, g[0]),
                FadeIn(cache),
                lag_ratio=0.5,
            )
        )

        cache.set_z_index(10)

        self.camera.frame.save_state()

        a = tree_to_steal_from.node_by_index(0, 0).next_to(cache, RIGHT, buff=0.5)

        self.play(
            self.camera.frame.animate.move_to(cache).scale(0.75),
            cpu.animate.set_color(DARK_COLOR),
            q1.animate.set_color(DARK_COLOR),
            q2.animate.set_color(DARK_COLOR),
            ab_text.animate.set_color(DARK_COLOR),
            FadeIn(a),
        )

        self.play(
            a.animate.align_to(cache, LEFT).set_color(BLACK),
            cache[1].animate.set_color(GREEN)
        )

        a = tree_to_steal_from.node_by_index(1, 2).next_to(cache, RIGHT, buff=0.5)

        self.play(
            FadeIn(a),
        )

        self.play(
            a.animate.align_to(cache, LEFT).set_color(BLACK),
            cache[2].animate.set_color(GREEN),
        )

        cls = VGroup(
            Tex("$64\\mathrm{B}$").next_to(cache[1], RIGHT, buff=0.1).scale(0.4),
            Tex("$64\\mathrm{B}$").next_to(cache[2], RIGHT, buff=0.1).scale(0.4),
            Tex("$64\\mathrm{B}$").next_to(cache[3], RIGHT, buff=0.1).scale(0.4),
            Tex("$64\\mathrm{B}$").next_to(cache[4], RIGHT, buff=0.1).scale(0.4),
            Tex("$64\\mathrm{B}$").next_to(cache[5], RIGHT, buff=0.1).scale(0.4),
            Tex("$64\\mathrm{B}$").next_to(cache[6], RIGHT, buff=0.1).scale(0.4),
        )

        self.play(FadeIn(cls, shift=RIGHT * .25, lag_ratio=0.03))

        cls2 = VGroup(
            Tex("$64 \cdot 8\\mathrm{b}$").scale(0.4).move_to(cls[0]).align_to(cls[0], LEFT),
            Tex("$64 \cdot 8\\mathrm{b}$").scale(0.4).move_to(cls[1]).align_to(cls[1], LEFT),
            Tex("$64 \cdot 8\\mathrm{b}$").scale(0.4).move_to(cls[2]).align_to(cls[2], LEFT),
            Tex("$64 \cdot 8\\mathrm{b}$").scale(0.4).move_to(cls[3]).align_to(cls[3], LEFT),
            Tex("$64 \cdot 8\\mathrm{b}$").scale(0.4).move_to(cls[4]).align_to(cls[4], LEFT),
            Tex("$64 \cdot 8\\mathrm{b}$").scale(0.4).move_to(cls[5]).align_to(cls[5], LEFT),
        )

        self.play(
            *[
                Transform(cls[i][0][2:], cls2[i][0][2:])
                for i in range(len(cls))
            ]
        )

        # I'm sorry
        for mobject in self.mobjects:
            self.remove(mobject)
        self.add(ab_text, cache, cpu, cls2)

        self.play(
            self.camera.frame.animate.restore(),
            cpu.animate.set_color(WHITE),
            q1.animate.set_color(WHITE),
            q2.animate.set_color(WHITE),
            ab_text.animate.set_color(WHITE),
        )

        # hack
        self.remove(ab_text[0][1])
        self.remove(ab_text[0][3])

        self.play(
            Transform(q2, four),
        )

        self.play(
            Transform(q1, two),
        )

        ax, x_label, y_label, g1, g2, g3, texts, l1, l2, l3, ax_more_nums = get_benchmark_graph()

        g = VGroup(ax, x_label, y_label, g1, g2, g3, texts, l1, l2, l3, ax_more_nums)
        g.next_to(self.camera.frame, DOWN).scale(0.8)

        cache[0].set_z_index(-1)

        # hack
        ab_text[0].remove(ab_text[0][1])
        ab_text[0].remove(ab_text[0][2])

        self.play(
            AnimationGroup(
                AnimationGroup(
                    self.camera.frame.animate.move_to(g),
                    FadeOut(cpu),
                    FadeOut(cache[0]),
                    FadeOut(cls2),
                    FadeOut(ab_text),
                    FadeOut(q1),
                    FadeOut(q2),
                ),
                AnimationGroup(
                    FadeIn(ax),
                    FadeIn(ax_more_nums[0][1]),
                    FadeIn(x_label),
                    FadeIn(y_label),
                ),
                lag_ratio=0.25,
            ),
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Create(g1),
                    FadeIn(texts[0]),
                    lag_ratio=0.25,
                ),
                AnimationGroup(
                    Create(g2),
                    FadeIn(texts[1]),
                    lag_ratio=0.25,
                ),
                AnimationGroup(
                    Create(g3),
                    FadeIn(texts[2]),
                    lag_ratio=0.25,
                ),
                lag_ratio=0.33,
            )
        )

        self.camera.frame.save_state()

        self.play(
            AnimationGroup(
                AnimationGroup(
                    self.camera.frame.animate.move_to(VGroup(l1, l2, l3)).scale(0.5).shift(UP * 0.25),
                ),
                AnimationGroup(
                    FadeIn(l1, run_time=0.75),
                    FadeIn(l2, run_time=0.75),
                    FadeIn(l3, run_time=0.75),
                    lag_ratio=0.1,
                ),
                lag_ratio=0.75,
            ),
        )

        self.play(
            self.camera.frame.animate.move_to(VGroup(ab_text, cpu)).scale(2),
            FadeOut(l1),
            FadeOut(l2),
            FadeOut(l3),
            FadeOut(g1),
            FadeOut(g2),
            FadeOut(g3),
            FadeOut(ax),
            FadeOut(ax_more_nums[0][1]),
            FadeOut(x_label),
            FadeOut(y_label),

            FadeIn(cpu),
            FadeIn(cache[0]),
            FadeIn(cls2),
            FadeIn(ab_text),
            FadeIn(q1),
            FadeIn(q2),
        )

        rect = get_fade_rect()

        indx = rect.get_z_index() + 1

        ab_text.set_z_index(rect.get_z_index() + 1)
        q1.set_z_index(indx)
        q2.set_z_index(indx)

        t = Tex("Oversimplification!")\
                .move_to(VGroup(cpu, cache)).scale(1.45)\
                .set_z_index(indx)

        problems = VGroup(
            Tex(r"\begin{itemize} \item implementation-specific details \end{itemize}"),
            Tex(r"\begin{itemize} \item usage determines runtime \end{itemize}"),
        ).arrange(DOWN, buff=0.2).set_z_index(indx).scale(0.8)
        problems[1].align_to(problems[0], LEFT)

        self.play(
            AnimationGroup(
                FadeIn(rect),
                FadeIn(t),
                lag_ratio=0.5,
            )
        )

        problems.move_to(t)
        tmp = VGroup(t.copy(), problems).arrange(DOWN, buff=0.3).move_to(t)

        self.play(
            AnimationGroup(
                Transform(t, tmp[0]),
                FadeIn(problems[0]),
                lag_ratio=0.5,
            )
        )

        self.play(
            FadeIn(problems[1]),
        )

        paper = ImageMobject("assets/performance.png")\
                .set_height(self.camera.frame.get_height() * 0.85).next_to(self.camera.frame, RIGHT).shift(LEFT)\
                .set_z_index(indx)

        self.play(
            FadeIn(paper),
            self.camera.frame.animate.move_to(Group(t, paper)).scale(1.3)
        )



