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


