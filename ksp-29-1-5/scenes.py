from manim import *
from utilities import *


class Intro(MovingCameraScene):
    def construct(self):
        mapping = [2, 0, 3, 1, 5, 6, 5]

        N = len(mapping)

        upper_dots = VGroup(*[Dot().shift(UP + RIGHT * (i - N / 2 + 0.5)) for i in range(N)])
        lower_dots = VGroup(*[Square(fill_opacity=1, color=WHITE).set_width(Dot().width * 0.5).shift(DOWN + RIGHT * (i - N / 2 + 0.5)) for i in range(N)])
        arrows = VGroup(*[Arrow(start = upper_dots[i].get_center(),
                                end = lower_dots[v].get_center(),
                                tip_length=0.2
                                ) for i, v in enumerate(mapping)])

        self.camera.frame.set_width(Group(upper_dots, lower_dots, arrows).width * 1.5)

        lucistnici = VGroup(Tex("$n$ lučištníků")).arrange().next_to(upper_dots, UP, buff=0.5).scale(0.6)
        cile = VGroup(Tex("$n$ cílů")).arrange().next_to(lower_dots, DOWN, buff=0.5).scale(0.6)

        self.play(
            AnimationGroup(
                Write(upper_dots),
                Write(lower_dots),
                AnimationGroup(*[FadeIn(a) for a in arrows], lag_ratio=0.1),
                AnimationGroup(
                    FadeIn(lucistnici, shift=UP * 0.1),
                    FadeIn(cile, shift=DOWN * 0.1),
                    lag_ratio=0,
                ),
                lag_ratio=0.25,
            ),
        )

        self.play(
            AnimationGroup(
                *[a.animate(rate_func=there_and_back, run_time=1.5).set_color(RED) for a in arrows],
                lag_ratio=0.08,
            ),
            AnimationGroup(
                *[a.animate(rate_func=there_and_back, run_time=1.5).set_color(RED) for a in upper_dots],
                lag_ratio=0.08,
            ),
            AnimationGroup(
                *[lower_dots[mapping[i]].animate(rate_func=there_and_back, run_time=1.5).set_color(RED) for i in range(N)],
                lag_ratio=0.08,
            ),
        )

        arrows[1].set_z_index(1)
        arrows[2].set_z_index(1)
        arrows[4].set_z_index(1)
        arrows[6].set_z_index(1)

        for a in arrows:
            a.save_state()
        for a in upper_dots:
            a.save_state()
        for a in lower_dots:
            a.save_state()

        self.play(
            arrows[0].animate.set_color(DARKER_GRAY),
            arrows[3].animate.set_color(DARKER_GRAY),
            arrows[5].animate.set_color(DARKER_GRAY),
            arrows[1].animate.set_color(GREEN),
            arrows[2].animate.set_color(GREEN),
            arrows[4].animate.set_color(GREEN),
            arrows[6].animate.set_color(GREEN),
            upper_dots[1].animate.set_color(GREEN),
            upper_dots[2].animate.set_color(GREEN),
            upper_dots[4].animate.set_color(GREEN),
            upper_dots[6].animate.set_color(GREEN),
            lower_dots[mapping[1]].animate.set_color(GREEN),
            lower_dots[mapping[2]].animate.set_color(GREEN),
            lower_dots[mapping[4]].animate.set_color(GREEN),
            lower_dots[mapping[6]].animate.set_color(GREEN),
        )

        blob = get_gray_blob()

        q = Tex("Jak najít největší skupinu?").set_z_index(150)

        self.play(
            AnimationGroup(
                FadeIn(blob),
                FadeIn(q),
                lag_ratio=0.5
            )
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(blob),
                    FadeOut(q),
                ),
                AnimationGroup(
                    FadeOut(lucistnici),
                    FadeOut(cile),
                    AnimationGroup(*[a.animate.restore() for a in arrows]),
                    AnimationGroup(*[a.animate.restore() for a in upper_dots]),
                    AnimationGroup(*[a.animate.restore() for a in lower_dots]),
                ),
                lag_ratio=0.5,
            ),
        )

        def f(v):
            return bin(v)[2:].rjust(N, '0')

        def tex_above_upper_dots(v):
            g = VGroup(
                *[Tex("\\texttt{" + i + "}").scale(0.75).set_color(WHITE if v == 0 else GREEN if i == "1" else DARKER_GRAY) for i in f(v)]
            )

            for i, a in enumerate(g):
                a.next_to(upper_dots[i], UP, buff=0.3)

            return g

        g = tex_above_upper_dots(0)

        self.play(
            FadeIn(g, lag_ratio=0.1),
            self.camera.frame.animate.move_to(VGroup(g, lower_dots))
        )

        for a in arrows:
            a.save_state()
        for a in upper_dots:
            a.save_state()
        for a in lower_dots:
            a.save_state()

        for i in range(1, 2 ** N):
            set_thingy = set(mapping[i] for i, ll in enumerate(f(i)) if ll == "1")
            self.play(
                Transform(g, tex_above_upper_dots(i)),
                AnimationGroup(
                    *[a.animate.set_color(GREEN if f(i)[j] == "1" else DARKER_GRAY).set_z_index(1 if f(i)[j] == "1" else 0) for j, a in enumerate(arrows)]
                ),
                AnimationGroup(*[a.animate.set_color(GREEN if j in set_thingy else WHITE) for j, a in enumerate(lower_dots)]),
                AnimationGroup(*[a.animate.set_color(GREEN if f(i)[j] == "1" else WHITE) for j, a in enumerate(upper_dots)]),
                run_time=1 / i,
            )

        self.play(
            AnimationGroup(*[a.animate.restore() for a in arrows]),
            AnimationGroup(*[a.animate.restore() for a in upper_dots]),
            AnimationGroup(*[a.animate.restore() for a in lower_dots]),
            self.camera.frame.animate.move_to(VGroup(lower_dots, upper_dots)),
            FadeOut(g, lag_ratio=0.1),
        )

        deltas = [3, 1, -2, -2, -2, 0, 1, 2, -1, 1, -2, 1, 1, -1, -1, 2, 0, 0, 1, -4, 0]
        mapping_larger = [d + i for i, d in enumerate(deltas)]

        N_larger = len(mapping_larger)
        N_diff = (N_larger - N) // 2

        upper_dots_larger = VGroup(*[Dot().shift(UP + RIGHT * (i - N_larger / 2 + 0.5)) for i in range(N_larger)])
        lower_dots_larger = VGroup(*[Square(fill_opacity=1, color=WHITE).set_width(Dot().width * 0.5).shift(DOWN + RIGHT * (i - N_larger / 2 + 0.5)) for i in range(N_larger)])
        arrows_larger = VGroup(*[Arrow(start = upper_dots_larger[i].get_center(),
                                end = lower_dots_larger[v].get_center(),
                                tip_length=0.2
                                ) for i, v in enumerate(mapping_larger)])

        pozorovani = VGroup(Tex(r"Pozorování: \textit{nejlepší řešení je rozšířením nějakého předchozího.}")).next_to(upper_dots, UP, buff=0.5).scale(0.6)

        self.play(
            AnimationGroup(
                self.camera.frame.animate.scale(1.3),
                AnimationGroup(
                    FadeIn(arrows_larger[:N_diff]),
                    FadeIn(arrows_larger[-N_diff:]),
                    FadeIn(upper_dots_larger[:N_diff]),
                    FadeIn(upper_dots_larger[-N_diff:]),
                    FadeIn(lower_dots_larger[:N_diff]),
                    FadeIn(lower_dots_larger[-N_diff:]),
                ),
                lag_ratio=0.25,
            )
        )

        self.remove(*arrows)
        self.remove(*upper_dots)
        self.remove(*lower_dots)

        self.add(arrows_larger)
        self.add(upper_dots_larger)
        self.add(lower_dots_larger)

        curved_arrows = [CurvedArrow(Dot().next_to(upper_dots_larger[4 + N_diff], UP, buff=0.05).get_center(), Dot().next_to(upper_dots_larger[4 - i + N_diff], UP, buff=0.05).get_center(), tip_length=0.15, angle = 1)
                         for i in range(1, 11)]

        self.play(
            AnimationGroup(
                AnimationGroup(
                    arrows_larger[4 + N_diff].animate.set_color(ORANGE),
                    upper_dots_larger[4 + N_diff].animate.set_color(ORANGE),
                    lower_dots_larger[5 + N_diff].animate.set_color(ORANGE),
                    self.camera.frame.animate.move_to(arrows_larger[4 + N_diff]),
                ),
                AnimationGroup(*[Write(a) for a in curved_arrows], lag_ratio=0.1),
                lag_ratio=0.5,
            )
        )

        pozorovani.next_to(arrows_larger[4 + N_diff], DOWN, buff=1)

        self.play(
            FadeIn(pozorovani, shift=DOWN * 0.1),
            self.camera.frame.animate.shift(DOWN * 0.1),
        )

        self.play(FadeOut(VGroup(*curved_arrows)))
