from manim import *

class Logo(Scene):
    def construct(self):
        t = SVGMobject("logo-t.svg").scale(2).set_color_by_gradient((WHITE, WHITE, GRAY, GRAY))
        s = SVGMobject("logo-s.svg").scale(2)

        self.play(
            Write(t),
            Write(s),
            run_time = 2
        )

        self.wait(0.3)

        self.play(
            FadeOut(t),
            FadeOut(s),
            run_time = 1
        )

class LogoBottomCorner(Scene):
    def construct(self):
        t = SVGMobject("logo-t.svg").scale(0.7).set_color_by_gradient((WHITE, WHITE, GRAY, GRAY))
        s = SVGMobject("logo-s.svg").scale(0.7)

        s.shift(DOWN * 2.8 + RIGHT * 6)
        t.shift(DOWN * 2.8 + RIGHT * 6)

        self.play(
            FadeIn(t),
            FadeIn(s),
        )
