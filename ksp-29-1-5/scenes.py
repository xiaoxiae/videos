from manim import *
from utilities import *


class SwitchZIndex(Animation):
    """An animation that fades in an object... but colorfully."""

    def __init__(self, mobject: Mobject, z_index, **kwargs):
        self.original = mobject
        self.z_index = z_index

        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        new_alpha = self.rate_func(alpha)

        if new_alpha > 0.5:
            self.original.set_z_index(self.z_index)


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

        #self.play(
        #    AnimationGroup(
        #        *[a.animate(rate_func=there_and_back, run_time=1.5).set_color(RED) for a in arrows],
        #        lag_ratio=0.08,
        #    ),
        #    AnimationGroup(
        #        *[a.animate(rate_func=there_and_back, run_time=1.5).set_color(RED) for a in upper_dots],
        #        lag_ratio=0.08,
        #    ),
        #    AnimationGroup(
        #        *[lower_dots[mapping[i]].animate(rate_func=there_and_back, run_time=1.5).set_color(RED) for i in range(N)],
        #        lag_ratio=0.08,
        #    ),
        #)

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

        def animate_combination(archers, colors):
            mapping_set = set([mapping[i] for i in archers])
            mapping_colors = {i:colors[index] for index, i in enumerate(archers)}
            self.play(
                *[arrows[i].animate.set_color(mapping_colors[i]) for i in archers],
                *[arrows[i].animate.set_color(DARKER_GRAY) for i in range(N) if i not in archers],
                *[upper_dots[i].animate.set_color(mapping_colors[i]) for i in archers],
                *[upper_dots[i].animate.set_color(DARKER_GRAY) for i in range(N) if i not in archers],
                #*[lower_dots[i].animate.set_color(mapping_colors[i]) for i in mapping_set],
                #*[lower_dots[i].animate.set_color(DARKER_GRAY) for i in range(N) if i not in mapping_set],
                *[SwitchZIndex(arrows[i], 1) for i in archers],
                *[SwitchZIndex(arrows[i], 0) for i in range(N) if i not in archers],
            )

        animate_combination([1, 2, 4, 6], [GREEN] * 4)
        self.wait(0.5)
        animate_combination([1, 6], [GREEN] * 2)
        self.wait(0.5)
        animate_combination([0, 3, 4, 5], [GREEN] * 4)

        self.wait(1)

        animate_combination([1, 2, 4, 5, 6], colors=[GREEN] * 3 + [RED] * 2)
        self.wait(0.5)
        animate_combination([0, 1, 2, 3, 4, 5, 6], colors=[RED] * 7)

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
                *[Tex("\\texttt{" + "Ne" if i == "0" else "Ano" + "}").scale(0.5).set_color(WHITE if v == 0 else GREEN if i == "1" else DARKER_GRAY) for i in f(v)]
            )

            for i, a in enumerate(g):
                a.next_to(upper_dots[i], UP, buff=0.3)

            return g

        g = tex_above_upper_dots(0)

        brace = BraceBetweenPoints(Dot().next_to(g[0], (UP + LEFT) * 0.1).get_center(),
                                   Dot().next_to(g[-1], (UP + RIGHT) * 0.1).get_center(),
                                   direction=UP)

        count = Tex("$n$").next_to(brace, UP).scale(0.75)

        self.play(
            FadeIn(g, lag_ratio=0.1),
            FadeIn(brace, shift=UP * 0.2),
            FadeIn(count, shift=UP * 0.2),
            self.camera.frame.animate.move_to(VGroup(g, lower_dots, brace, count))
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
                *[a.animate.set_color(GREEN if f(i)[j] == "1" else DARKER_GRAY) for j, a in enumerate(arrows)],
                *[a.animate.set_color(GREEN if j in set_thingy else WHITE) for j, a in enumerate(lower_dots)],
                *[a.animate.set_color(GREEN if f(i)[j] == "1" else DARKER_GRAY) for j, a in enumerate(upper_dots)],
                *[SwitchZIndex(a, 1 if f(i)[j] == "1" else 0) for j, a in enumerate(arrows)],
                run_time=1 / i,
            )

            if i > 5:
                return

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

        return
