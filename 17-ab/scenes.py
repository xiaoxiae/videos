from manim import *
from utilities import *

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

        rect = get_fade_rect()

        bw = VGroup(
            Tex("\sc There has to be"),
            Tex("\sc a better way..."),
        ).scale(2.5).arrange(DOWN, buff=0.5).move_to(self.camera.frame).set_z_index(1000)

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

        self.wait()


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

        self.camera.frame.save_state()

        self.play(
            ab.animate.set_color(DARKER_GRAY).shift(LEFT * 4),
            self.camera.frame.animate.move_to(bst),
        )

        # TARGET 5
        bubbles, node_bubbles = get_tree_bubbles(binary_tree)

        target = Tex("$5$").next_to(binary_tree.node_by_index(0, 0), UP).scale(0.8)

        self.play(Write(target))

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
            node_bubbles[binary_tree.node_by_index(2, 3)][0][0].animate.set_color(DARK_GRAY),
            binary_tree.node_edges[binary_tree.node_by_index(2, 3)][0].animate.set_color(DARK_GRAY),
            binary_tree.node_subtree_mobjects[binary_tree.node_by_index(3, 6)].animate.set_color(DARK_GRAY),
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

        old_bubbles = bubbles

        bubbles, node_bubbles = get_tree_bubbles(ab_tree)

        self.play(FadeIn(bubbles))

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
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(1, 0)].animate.set_color(DARK_GRAY),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(1, 1)].animate.set_color(DARK_GRAY),
            ab_tree.node_edges[ab_tree.node_by_index(0, 0)][0].animate.set_color(DARK_GRAY),
            ab_tree.node_edges[ab_tree.node_by_index(0, 0)][1].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(0, 0)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(0, 0)][1][0].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(1, 0)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(1, 0)][1][0].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(1, 1)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(1, 1)][1][0].animate.set_color(DARK_GRAY),
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
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(1, 0)].animate.set_color(DARK_GRAY),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(1, 1)].animate.set_color(DARK_GRAY),
            ab_tree.node_edges[ab_tree.node_by_index(0, 0)][0].animate.set_color(DARK_GRAY),
            ab_tree.node_edges[ab_tree.node_by_index(0, 0)][1].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(0, 0)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(0, 0)][1][0].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(1, 0)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(1, 0)][1][0].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(1, 1)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(1, 1)][1][0].animate.set_color(DARK_GRAY),
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
            node_bubbles[ab_tree.node_by_index(1, 2)][0][0].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(1, 2)][1][0].animate.set_color(DARK_GRAY),
            node_bubbles[ab_tree.node_by_index(1, 2)][2][0].animate.set_color(DARK_GRAY),
            ab_tree.node_edges[ab_tree.node_by_index(1, 2)][0].animate.set_color(DARK_GRAY),
            ab_tree.node_edges[ab_tree.node_by_index(1, 2)][1].animate.set_color(DARK_GRAY),
            ab_tree.node_edges[ab_tree.node_by_index(1, 2)][2].animate.set_color(DARK_GRAY),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(2, 4)].animate.set_color(DARK_GRAY),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(2, 5)].animate.set_color(DARK_GRAY),
            ab_tree.node_subtree_mobjects[ab_tree.node_by_index(2, 6)].animate.set_color(DARK_GRAY),
        )

        self.play(
            ab_tree.animate.restore(),
            FadeOut(bubbles),
            bst.animate.shift(LEFT * 4),
            self.camera.frame.animate.move_to(VGroup(ab_tree, bst.copy().shift(LEFT * 4))),
        )

        ng = VGroup(binary_tree)

        self.play(
            ab.animate.set_color(DARK_GRAY).shift(LEFT * 4),
            bst[0].animate.set_color(DARK_GRAY).shift(UP * 4),
            self.camera.frame.animate.move_to(ng).set_height(ng.get_height() * 1.4),
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
                [[2, 4]],
                [[1], [3], [5, 6, 7]],
            ],
            fill_background=False,
        )

        ab = VGroup(Tex(r"\underline{$(a,b)$-tree}").scale(1.25), ab_tree).arrange(DOWN, buff=1.2)
        two_four = Tex(r"\underline{$(2,4)$-tree}").scale(1.25).move_to(ab[0])

        self.camera.frame.scale(0.8)

        self.play(
            Write(ab),
        )

        self.play(
            ab_tree.edges.animate.set_color(DARKER_GRAY),
        )

        self.play(
            *[node[1].animate.set_color(DARKER_GRAY) for node in ab_tree.nodes]
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
            symbols.animate.set_color(DARKER_GRAY),
            *[node[0].animate.set_color(DARKER_GRAY) for node in ab_tree.nodes],
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
            ab_tree.node_by_index(0, 0)[0][1].animate.set_color(DARKER_GRAY),

            symbols.animate.set_color(DARKER_GRAY),

            ab_tree.subtree_by_index(1, 2).animate.set_color(DARKER_GRAY),

            ab_tree.edges_by_node_index(0, 0)[2].animate.set_color(DARKER_GRAY),
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
            ab_tree.node_by_index(0, 0)[0][0].animate.set_color(DARKER_GRAY),
            ab_tree.node_by_index(0, 0)[0][1].animate.set_color(WHITE),

            ab_tree.subtree_by_index(1, 0).animate.set_color(DARKER_GRAY),
            ab_tree.subtree_by_index(1, 1).animate.set_color(RED),
            ab_tree.subtree_by_index(1, 2).animate.set_color(GREEN),

            ab_tree.edges_by_node_index(0, 0)[0].animate.set_color(DARKER_GRAY),
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

        non_root = Tex("(besides root)").scale(0.6).next_to(t1, DOWN, buff=0.12).set_color(GRAY).shift(LEFT * 0.05)

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

        # > two_four[0][1].set_z_index(11).set_color(ORANGE)
        # > two_four[0][3].set_z_index(11).set_color(BLUE)
        # > ab[0][0][1].set_z_index(11)
        # > ab[0][0][3].set_z_index(11)
        # > ab_tree.subtree_by_index(1, 0).set_z_index(11)
        # > ab_tree.subtree_by_index(1, 2).set_z_index(11)
        # > symbols[1].set_z_index(11)
        # > symbols[2].set_z_index(11)
        # > at1.set_z_index(11)
        # > at2.set_z_index(11)

        # TODO: shift a and b up and make them smaller

        b_copy = ab[0][0][3].copy().next_to(two_four[0][3], UP, buff=0).scale(0.6)

        # > self.play(
        # >     FadeIn(rect),
        # >     AnimationGroup(
        # >         ab[0][0][1].animate.next_to(two_four[0][1], UP, buff=0).scale(0.6).align_to(b_copy, DOWN).set_color(ORANGE),
        # >         FadeIn(two_four[0][1]),
        # >         lag_ratio=0.5,
        # >     ),
        # >     AnimationGroup(
        # >         ab[0][0][3].animate.next_to(two_four[0][3], UP, buff=0).scale(0.6).set_color(BLUE),
        # >         FadeIn(two_four[0][3]),
        # >         lag_ratio=0.5,
        # >     ),
        # >     ab_tree.subtree_by_index(1, 0).animate.set_color(ORANGE),
        # >     ab_tree.subtree_by_index(1, 2).animate.set_color(BLUE),
        # >     symbols[1].animate.set_color(BLUE),
        # >     symbols[2].animate.set_color(BLUE),
        # >     at1.animate.set_color(ORANGE),
        # >     at2.animate.set_color(BLUE),
        # > )

        # > non_root.set_color(WHITE).set_z_index(11)

        # > self.play(
        # >     FadeOut(rect),
        # >     ab.animate.set_color(WHITE),
        # >     symbols.animate.set_color(WHITE),
        # >     non_root.animate.set_color(GRAY),
        # >     at1.animate.set_color(GRAY),
        # >     at2.animate.set_color(GRAY),
        # >     two_four[0][1].animate.set_color(WHITE),
        # >     two_four[0][3].animate.set_color(WHITE),
        # > )

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

        self.play(
            FadeIn(non_root),
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

        self.play(FadeIn(reqs_list[1], shift=RIGHT * 0.25))

        self.play(Write(ops_title))

        for row in ops_list:
            self.play(FadeIn(row, shift=RIGHT * 0.25))


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


class Thumbnail(MovingCameraScene):
    def construct(self):
        ab = ABTree(
            [
                [[2, 4]],
                [["0"], ["0"], [5, 6, 7]],
            ],
        ).scale(2.5)

        self.add(ab)

        the = Tex("\sc The").scale(0.75)
        a = Tex("\sc a")
        b = Tex("\sc b")
        trees = Tex("\sc Tree")
        dash = Tex("-")

        text = VGroup(the, a, b, trees, dash).scale(2.45)

        ab.node_by_index(0, 0)[0].become(the.move_to(ab.node_by_index(0, 0)[0]))
        ab.node_by_index(1, 0)[0].become(a.move_to(ab.node_by_index(1, 0)[0]))
        ab.node_by_index(1, 1)[0].become(b.move_to(ab.node_by_index(1, 1)[0]))
        ab.node_by_index(1, 2)[0].become(trees.move_to(ab.node_by_index(1, 2)[0]))

        dash.scale(1.25)
        dash.move_to(VGroup(a, b))

        self.add(text)

        self.wait()


class Search(MovingCameraScene):
    @fade
    def construct(self):

        ab_tree = ABTree(
            [
                [[2, 4]],
                [[1], [3], [5, 6, 7]],
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

        ab_tree.search_but_like_animate(6, self, scale=S)
        ab_tree.search_but_like_animate(8, self, scale=S)


class Insertion(MovingCameraScene):
    @fade
    def construct(self):

        ab_tree = ABTree(
            [
                [[2, 4]],
                [[1], [3], [5, 6, 7]],
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

        target, qs = ab_tree.search_but_like_animate(8, self, scale=S, speedup=5, no_cleanup=True)

        def darken_our_tree(tree):
            tree.subtree_by_index(1, 0).set_color(DARK_GRAY)
            tree.subtree_by_index(1, 1).set_color(DARK_GRAY)
            tree.node_by_index(0, 0).set_color(DARK_GRAY)
            tree.edges_by_node_index(0, 0).set_color(DARK_GRAY)

        anim, tree = ab_tree.insert(8, scale=S, transform_instead=target, tree_transform_function=darken_our_tree)

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

        for i in [9, 10]:
            target = Tex(f"${i}$").next_to(tree.node_by_index(0, 0), UP).scale(1.2).set_z_index(10)
            self.play(FadeIn(target, shift=UP * 0.1))

            anim, tree = tree.insert(i, scale=S, transform_instead=target)

            self.play(anim)

            # yuck
            for mobject in self.mobjects:
                self.remove(mobject)
            self.add(tree, ins)

        anim, tree = tree.bubble_insert(4, scale=S)

        self.play(anim)

        for mobject in self.mobjects:
            self.remove(mobject)
        self.add(tree, ins)

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


class Deletion(MovingCameraScene):
    @fade
    def construct(self):
        self.next_section(skip_animations=True)
        ab_tree = ABTree(
            [
                [[3]],
                [[1], [5, 7]],
                [[0], [2], [4], [6], [8, 9]],
            ],
            fill_background=False,
        )

        ab = VGroup(Tex(r"\underline{\textit{Insertion}}").scale(1.25), ab_tree).arrange(DOWN, buff=1).scale(S)

        dl = Tex(r"\underline{\textit{Deletion}}").scale(1.25).scale(S).move_to(ab[0])

        # copy-pasted
        self.camera.frame.move_to(VGroup(ab)).set_height(VGroup(ab).get_height() * 1.4),

        self.add(ab)

        self.play(
            FadeOut(ab[0], shift=LEFT * 4.2),
            FadeIn(dl, shift=LEFT * 4.2),
        )

        target, qs = ab_tree.search_but_like_animate(9, self, scale=S, speedup=5, no_cleanup=True)

        def darken_our_tree(tree):
            tree.subtree_by_index(1, 0).set_color(DARK_GRAY)
            tree.subtree_by_index(2, 2).set_color(DARK_GRAY)
            tree.subtree_by_index(2, 3).set_color(DARK_GRAY)
            tree.node_by_index(0, 0).set_color(DARK_GRAY)
            tree.node_by_index(1, 1).set_color(DARK_GRAY)
            tree.edges_by_node_index(0, 0).set_color(DARK_GRAY)
            tree.edges_by_node_index(1, 1).set_color(DARK_GRAY)

        self.next_section()

        for mobject in self.mobjects:
            self.remove(mobject)

        self.add(dl)

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

        target = Tex("$3$").next_to(tree.node_by_index(0, 0), UP).scale(0.8 * S)

        self.play(
            FadeIn(target, shift=UP * 0.1),
        )

        self.play(target.animate.set_color(GREEN), tree.node_by_index(0, 0)[0].animate.set_color(GREEN))
