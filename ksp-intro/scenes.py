from manim import *


class MoveAlongPathShow(Animation):

    def __init__(
        self,
        mobject: Mobject,
        path: VMobject,
        suspend_mobject_updating: bool | None = False,
        **kwargs,
    ) -> None:
        self.path = path
        super().__init__(
            mobject, suspend_mobject_updating=suspend_mobject_updating, **kwargs
        )

    def interpolate_mobject(self, alpha: float) -> None:
        a = self.rate_func(alpha)
        point = self.path.point_from_proportion(a)

        if a > 0.75:
            self.mobject.set_z_index(2)

        self.mobject.move_to(point)


class Intro(MovingCameraScene):
    def construct(self):
        text = SVGMobject("ksp-text.svg").set_z_index(1)
        head = SVGMobject("ksp-head.svg")
        head_eyes = SVGMobject("ksp-head-eyes.svg")

        e = 1
        hand_l = SVGMobject("ksp-hand-l.svg").shift(LEFT * e).scale(0.2)
        hand_r = SVGMobject("ksp-hand-r.svg").shift(RIGHT * e).scale(0.2)

        self.play(FadeIn(text))

        self.add(hand_l)
        self.add(hand_r)

        point_coordinates = [ORIGIN, UP * 0.3, UP * 0.40, UP * 0.15]

        bezier = CubicBezier(*point_coordinates).scale(1.5)

        d = 1.63
        self.add(head)
        head.shift(UP * d)
        head_eyes.shift(UP * d)
        head.save_state()
        head.shift(DOWN * d)
        head.set_opacity(0)
        self.play(
            head.animate.restore(),
            self.camera.frame.animate.move_to(VGroup(text, head.copy().shift(UP * d))),
            Succession(
                Wait(0.45),
                AnimationGroup(
                    MoveAlongPathShow(hand_l, bezier.copy().shift(LEFT * 1.4 + UP * 0.8)),
                    MoveAlongPathShow(hand_r, bezier.copy().shift(RIGHT * 1.4 + UP * 0.8)),
                    lag_ratio=0.1,
                ),
            )
        )

        text_fade = SVGMobject("ksp-text-fade.svg").set_z_index(1)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Transform(head, head_eyes),
                    Transform(text, text_fade),
                    lag_ratio=0.3,
                ),
                self.camera.frame.animate(rate_func=rush_into).move_to(text.copy().shift(DOWN * 0.15)).scale(0.001),
                lag_ratio=0.75,
            )
        )
