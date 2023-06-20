from __future__ import annotations
from manim import *
from utilities import *
from math import atan2


POTATO_COLOR = "#FAC551"
CARROT_COLOR = "#EC6B00"
FERTILIZER_COLOR = "#9E9645"

THERE_AND_BACK_SCALE = 1.12

OF_INITIAL = (1.2, 1.7)

KEY_ANIMATION_RUNTIME = 1.5


class TestTSP(MovingCameraScene):
    @fade
    def construct(self):
        G = GetTSPIllustration()
        self.add(G)

        self.wait()


class TestColoring(MovingCameraScene):
    @fade
    def construct(self):
        G = GetTSPIllustration()
        self.add(G)

        self.wait()


class Intro(MovingCameraScene):
    @fade
    def construct(self):
        img_scale = 0.4
        text_scale = 1.1
        subtext_scale = 0.75

        kantorovich = ImageMobject("assets/kantorovich.jpg")\
                      .set_height(self.camera.frame.get_height() * img_scale)

        kantorovich.add(SurroundingRectangle(kantorovich, color=WHITE, buff=-0.01))

        koopmans = ImageMobject("assets/koopmans.jpg")\
                   .set_height(self.camera.frame.get_height() * img_scale)

        koopmans.add(SurroundingRectangle(koopmans, color=WHITE, buff=-0.01))

        a = Group(
            VGroup(
                Tex(r"\underline{Win a Nobel Price}").scale(text_scale),
                Tex(r"\textit{Kantorovich, Koopmans (1975)}").scale(subtext_scale),
            ).arrange(DOWN, buff=0.25),
            Group(kantorovich, koopmans).arrange(),
        ).arrange(DOWN, buff=0.5)

        knapsack = ImageMobject("assets/midjourney/knapsack-out.png")\
                   .set_height(self.camera.frame.get_height() * img_scale)

        tsp = GetTSPIllustration()\
                   .set_height(self.camera.frame.get_height() * img_scale)

        b = Group(
            VGroup(
                Tex(r"\underline{Solve NP-hard Problems}").scale(text_scale),
                Tex(r"\textit{Knapsack, TSP, Vertex Cover, $\ldots$}").scale(subtext_scale),
            ).arrange(DOWN, buff=0.25),
            Group(knapsack, tsp).arrange(buff=0.5),
        ).arrange(DOWN, buff=0.5)

        transcendence = ImageMobject("assets/transcendence.png")\
                   .set_height(self.camera.frame.get_height() * img_scale)

        transcendence.add(SurroundingRectangle(transcendence, color=WHITE, buff=-0.01))

        imm = Tex(r"\underline{Achieve immortality}").scale(text_scale)
        imm.align_to(b, UP)
        imm[0][-1].align_to(b[0][0][0][-1], DOWN)

        c = Group(
            VGroup(
                imm,
                Tex(r"\textit{Sacrifices / Solving $\mathrm{P} = \mathrm{NP}$}").scale(subtext_scale),
            ).arrange(DOWN, buff=0.25),
            transcendence,
        ).arrange(DOWN, buff=0.5)

        g = Group(a, b, c).arrange(buff=1).scale(0.65)

        tspfaded = GetTSPIllustration(fade=True)\
                   .set_height(self.camera.frame.get_height() * img_scale)\
                   .move_to(tsp).scale(0.65)

        self.camera.frame.move_to(a).scale(0.65)

        self.play(
            AnimationGroup(
                Write(a[0][0], run_time=1),
                FadeIn(a[0][1], run_time=1),
                lag_ratio=0.5,
            ),
            Succession(
                Wait(0.5),
                FadeIn(a[1]),
            ),
        )

        self.play(
            a[0].animate.set_opacity(BIG_OPACITY),
            a[1][0].animate.set_opacity(BIG_OPACITY),
            a[1][1].animate.set_opacity(BIG_OPACITY),
            a[1][0][1].animate.set_color(DARKER_GRAY),
            a[1][1][1].animate.set_color(DARKER_GRAY),
            self.camera.frame.animate.move_to(b),
            AnimationGroup(
                Write(b[0][0], run_time=1),
                FadeIn(b[0][1], run_time=1),
                lag_ratio=0.5,
            ),
            Succession(
                Wait(0.5),
                FadeIn(b[1]),
            ),
        )

        tsp.save_state()

        self.play(
            AnimationGroup(
                Write(c[0][0], run_time=1),
                FadeIn(c[0][1], run_time=1),
                lag_ratio=0.5,
            ),

            b[0].animate.set_opacity(BIG_OPACITY),
            b[1][0].animate.set_opacity(BIG_OPACITY),
            Transform(b[1][1], tspfaded),
            self.camera.frame.animate.move_to(c),
            Succession(
                Wait(0.5),
                FadeIn(c[1]),
            ),
        )

        self.play(
            self.camera.frame.animate.move_to(Group(a, b)).scale(1.25),
            FadeOut(c),

            a[0].animate.set_opacity(1),
            a[1][0].animate.set_opacity(1),
            a[1][1].animate.set_opacity(1),
            a[1][0][1].animate.set_color(WHITE),
            a[1][1][1].animate.set_color(WHITE),
            b[0].animate.set_opacity(1),
            b[1][0].animate.set_opacity(1),
            tsp.animate.restore(),
        )

        lp = Tex(r"\sc Linear Programming").scale(1.5).next_to(Group(a, b), UP, buff=0.85)

        self.play(
            self.camera.frame.animate.move_to(Group(a, b, lp)),
            FadeIn(lp, shift=UP * 0.75),
        )


class Duality(MovingCameraScene):
    # Yeah I'm not proud but the bug is really weird
    # also makes logical sense to separate
    def construct(self):
        self.next_section(skip_animations=True)

        farm = ImageMobject("assets/midjourney/farm-12-16-out.png")\
                .set_height(self.camera.frame.get_height())\
                .align_to(self.camera.frame, LEFT).set_z_index(5)

        rect = ImageMobject("assets/midjourney/farm-12-16-rect.png")\
                .set_height(self.camera.frame.get_height())\
                .align_to(farm, RIGHT).set_z_index(6)

        rect_large = ImageMobject("assets/midjourney/farm-12-16-rect-large.png")

        rect_small = ImageMobject("assets/midjourney/farm-12-16-rect-small.png")\
                .set_height(self.camera.frame.get_height())\
                .align_to(farm, RIGHT).set_z_index(6)

        farm.save_state()
        rect.save_state()

        icon_scale = 1.65

        carrot = ImageMobject("assets/midjourney/carrot-cropped-flopped.png").set_height(0.45 * icon_scale)
        potato = ImageMobject("assets/midjourney/potato-cropped.png").set_height(0.3 * icon_scale)
        fertilizer = ImageMobject("assets/midjourney/fertilizer-cropped-flopped.png").set_height(0.3 * icon_scale)
        farmer = ImageMobject("assets/midjourney/farmer-outline.png").set_z_index(10).set_height(1.05)
        farmer_black = ImageMobject("assets/midjourney/farmer-black.png").set_z_index(9).set_height(1.05)

        self.add(rect, farm)

        fc = farm.copy()
        farm.move_to(Dot().next_to(self.camera.frame, LEFT))

        offset = 1


        # same as the next self.play
        rect_played = rect.copy().next_to(fc, RIGHT, buff=0).shift(LEFT * offset * 2)
        farm_played = farm.align_to(self.camera.frame, LEFT).shift(LEFT * offset)

        title = Tex(r"\underline{Farmer's Problem}").scale(1.5)

        goal = Tex("Goal: \it maximize profit").scale(1.25)

        points = VGroup(
            Tex(r"\begin{itemize} \item $3$ tons of potato seeds \end{itemize}"),
            Tex(r"\begin{itemize} \item $4$ tons of carrot seeds \end{itemize}"),
            Tex(r"\begin{itemize} \item $5$ tons of fertilizer (used 1:1) \end{itemize}"),
            Tex(r"\begin{itemize} \item " + str(OF_INITIAL[0]) + r"\$/kg for O, " + str(OF_INITIAL[1]) + r"\$/kg for O \end{itemize}"),
        )
        for i in range(3):
            align_object_by_coords(points[i + 1], points[i + 1][0][0], points[0][0][0])
            points[i + 1].shift(DOWN * 0.75 * (i + 1))

            if i == 2:
                points[i + 1].shift(DOWN * 0.3)

        guide = Dot().move_to(VGroup(Dot().align_to(rect_played, LEFT),
                                     Dot().align_to(self.camera.frame, RIGHT)))

        potato.next_to(points[0][0][-1], RIGHT)
        carrot.next_to(points[1][0][-1], RIGHT)
        fertilizer.next_to(points[2][0][-1], RIGHT)

        p2 = potato.copy().move_to(points[3][0][11])
        c2 = carrot.copy().move_to(points[3][0][-1]).shift(RIGHT * 0.1)
        points[3][0][11].scale(0.001).set_color(BLACK).set_opacity(0).set_z_index(-1)
        points[3][0][-1].scale(0.001).set_color(BLACK).set_opacity(0).set_z_index(-1)

        points[0][0][1].set_color(POTATO_COLOR)
        points[1][0][1].set_color(CARROT_COLOR)
        points[2][0][1].set_color(FERTILIZER_COLOR)
        points[0][0][8:13+1].set_color(POTATO_COLOR)
        points[1][0][8:13+1].set_color(CARROT_COLOR)
        points[2][0][8:17+1].set_color(FERTILIZER_COLOR)
        points[3][0][1:7+1].set_color(POTATO_COLOR)
        points[3][0][13:19+1].set_color(CARROT_COLOR)

        main_group = Group(Group(title, farmer).arrange(buff=0.4),
              Group(points, p2, c2, carrot, potato, fertilizer),
              goal,
              ).arrange(DOWN, buff=0.7).move_to(guide).set_z_index(10)

        title.set_z_index(7)

        farmer_copy = farmer.copy().move_to(title[0][0]).align_to(farmer, DOWN).set_opacity(0).set_z_index(1000)
        farmer_black.move_to(farmer).set_z_index(999)
        farmer_black_copy = farmer_black.copy().move_to(title[0][0]).align_to(farmer, DOWN).set_z_index(999)
        sr1 = SurroundingRectangle(title, color=BLACK, fill_opacity=1).set_z_index(8)
        sr2 = SurroundingRectangle(title, color=BLACK, fill_opacity=1).set_z_index(9)\
                .move_to(farmer_copy).align_to(Dot().move_to(farmer_copy), LEFT)

        self.add(sr1, title)

        self.play(
            rect.animate.next_to(fc, RIGHT, buff=0).shift(LEFT * offset * 2),
            farm.animate.align_to(self.camera.frame, LEFT).shift(LEFT * offset),
            ReplacementTransform(farmer_copy, farmer),
            ReplacementTransform(farmer_black_copy, farmer_black),
            FadeOut(sr1),
            sr2.animate.align_to(Dot().move_to(farmer), LEFT),
            run_time=2,
        )

        self.remove(farmer_black, sr2)

        self.play(
            AnimationGroup(
                Write(points[0], run_time=1.25),
                FadeIn(potato, shift=0.1 * RIGHT),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                Write(points[1], run_time=1.25),
                FadeIn(carrot, shift=0.1 * RIGHT),
                lag_ratio=0.5,
            )
        )

        self.play(
            Write(points[2][0][:17+1], run_time=1),
        )

        self.play(
            AnimationGroup(
                Write(points[2][0][17+1:], run_time=0.65),
                FadeIn(fertilizer, shift=0.1 * RIGHT),
                lag_ratio=0.3,
            )
        )

        self.play(
            AnimationGroup(
                Write(points[3][0][:12+1]),
                FadeIn(p2, run_time=0.5),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                Write(points[3][0][12+1:]),
                FadeIn(c2, run_time=0.5),
                lag_ratio=0.5,
            )
        )

        self.play(
            Write(goal[0][:5]), run_time=0.65,
        )

        self.play(
            Write(goal[0][5:]), run_time=1,
        )

        saved_x = main_group.animate.set_x(0),

        rect2 = rect_small.copy()\
                .flip().align_to(self.camera.frame, RIGHT)\
                .shift(RIGHT * 0.1)
        self.add(rect2)

        offset2 = 0.5

        equivalenece = SVGMobject("assets/iff.svg").set_height(0.6).set_z_index(10)
        equivalenece.move_to(Dot().align_to(self.camera.frame, RIGHT))

        equivalenece.set_opacity(0).shift(RIGHT * (0.65 - offset2))  # hack

        self.play(
            rect.animate.restore(),
            farm.animate.restore(),

            main_group.animate.set_x(-main_group.get_x() - offset2 / 2),
            rect2.animate.shift(LEFT * (main_group.get_x() * 2 + offset2)),
            equivalenece.animate.shift(LEFT * (main_group.get_x() * 2 + offset2)).set_opacity(1),
        )

        guide2 = Dot().move_to(VGroup(Dot().move_to(equivalenece),
                                     Dot().align_to(self.camera.frame, RIGHT)))

        var = ComplexTex("variables: $x_p, x_c$")
        var[0][-5:-3].set_color(POTATO_COLOR)
        var[0][-2:].set_color(CARROT_COLOR)

        ineqs = ComplexTex(r"""$$\begin{aligned}
        x_p, x_c  &\ge 0 \\[0.3em]
              x_p \phantom{{}+ x_c} &\le 3\,000 \\[-0.2em]
              x_c &\le 4\,000 \\[-0.2em]
              x_p + x_c &\le 5\,000
                \end{aligned}$$""")
        ineqs[0][0:2].set_color(POTATO_COLOR)
        ineqs[0][3:3+2].set_color(CARROT_COLOR)
        ineqs[0][7:7+2].set_color(POTATO_COLOR)
        ineqs[0][10].set_color(POTATO_COLOR)
        ineqs[0][11].set_color(POTATO_COLOR)
        ineqs[0][12].set_color(POTATO_COLOR)
        ineqs[0][13].set_color(POTATO_COLOR)
        ineqs[0][14:14+2].set_color(CARROT_COLOR)
        ineqs[0][17].set_color(CARROT_COLOR)
        ineqs[0][18].set_color(CARROT_COLOR)
        ineqs[0][19].set_color(CARROT_COLOR)
        ineqs[0][20].set_color(CARROT_COLOR)
        ineqs[0][21:21+2].set_color(POTATO_COLOR)
        ineqs[0][24:24+2].set_color(CARROT_COLOR)
        ineqs[0][27].set_color(FERTILIZER_COLOR)
        ineqs[0][28].set_color(FERTILIZER_COLOR)
        ineqs[0][29].set_color(FERTILIZER_COLOR)
        ineqs[0][30].set_color(FERTILIZER_COLOR)

        exp = ComplexTex(r"$$\max\ " + str(OF_INITIAL[0]) + r"x_p + " + str(OF_INITIAL[1]) + r" x_c$$")
        exp[0][3:3+5].set_color(POTATO_COLOR)
        exp[0][-5:].set_color(CARROT_COLOR)

        of = Tex(r"objective function").set_opacity(MED_OPACITY).scale(0.75)

        theory_group = Group(var, ineqs, exp).arrange(DOWN, buff=0.75).move_to(guide2).set_z_index(10)

        var.align_to(title, DOWN)
        exp.align_to(goal, UP)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    points[2].animate.set_opacity(BIG_OPACITY),
                    points[3].animate.set_opacity(BIG_OPACITY),
                    fertilizer.animate.set_opacity(BIG_OPACITY),
                    p2.animate.set_opacity(BIG_OPACITY),
                    c2.animate.set_opacity(BIG_OPACITY),
                    goal.animate.set_opacity(BIG_OPACITY),
                ),
                Write(var, run_time=1.25),
                lag_ratio=0.5,
            ),
        )

        self.play(
            Write(ineqs[0][:7]),
            run_time=1.25,
        )

        self.play(
            Write(ineqs[0][7:21]),
            run_time=1.5,
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    points[0].animate.set_opacity(BIG_OPACITY),
                    points[1].animate.set_opacity(BIG_OPACITY),
                    potato.animate.set_opacity(BIG_OPACITY),
                    carrot.animate.set_opacity(BIG_OPACITY),
                    points[2].animate.set_opacity(1),
                    fertilizer.animate.set_opacity(1),
                ),
                Write(ineqs[0][21:], run_time=1),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    points[2].animate.set_opacity(BIG_OPACITY),
                    fertilizer.animate.set_opacity(BIG_OPACITY),
                    points[3].animate.set_opacity(1),
                    p2.animate.set_opacity(1),
                    c2.animate.set_opacity(1),
                    goal.animate.set_opacity(1),
                ),
                Write(exp, run_time=1.5),
                lag_ratio=0.5,
            )
        )

        g = VGroup(
            exp.copy(),
            of,
        ).arrange(UP, buff=0.15).move_to(exp)

        self.play(
            Transform(exp, g[0]),
            FadeIn(of, shift=UP * 0.15)
        )

        self.play(
            points.animate.set_opacity(1),
            carrot.animate.set_opacity(1),
            potato.animate.set_opacity(1),
            fertilizer.animate.set_opacity(1),
        )

        theory_group.add(of)
        of.set_z_index(10)

        self.remove(rect, farm)

        rect3 = rect.copy()\
                .flip().align_to(self.camera.frame, RIGHT)\
                .set_z_index(rect2.get_z_index() - 1)\
                .shift(RIGHT * 0.1)
        self.add(rect3)

        guide3 = Dot().move_to(main_group)
        guide3.set_x(-guide3.get_x())

        numberplane = NumberPlane(
            x_range=(- 3 * 7.111111111111111, 3 * 7.111111111111111, 1),
            y_range=(- 3 * 4.0, 3 * 4.0, 1),
            stroke_width = 6,
            axis_config={
                "stroke_width": 4,
            },
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 3,
                "stroke_opacity": 0.6
            },
        )

        numberplane.background_lines.set_z_index(rect3.get_z_index() - 1 + 0.1)
        numberplane.axes.set_z_index(rect3.get_z_index() - 1 + 0.2)

        area = FeasibleArea2D(dots_z_index=rect3.get_z_index() - 1 + 0.99).set_z_index(rect3.get_z_index() - 1 + 0.4)

        i1 = Inequality2D(1, 0, ">=", 0).set_color(POTATO_COLOR).set_z_index(rect3.get_z_index() - 1 + 0.5)  # positive potatoes
        i2 = Inequality2D(0, 1, ">=", 0).set_color(CARROT_COLOR).set_z_index(rect3.get_z_index() - 1 + 0.5)  # positive carrots
        i3 = Inequality2D(1, 1, "<=", 5).set_color(FERTILIZER_COLOR).set_z_index(rect3.get_z_index() - 1 + 0.5)  # at most 5 kg fertilizer
        i4 = Inequality2D(1, 0, "<=", 3).set_color(POTATO_COLOR).set_z_index(rect3.get_z_index() - 1 + 0.5)  # at most 3kg potatoes
        i5 = Inequality2D(0, 1, "<=", 4).set_color(CARROT_COLOR).set_z_index(rect3.get_z_index() - 1 + 0.5)  # at most 3kg carrots

        i4_hp = i4.get_half_plane()

        area.add_inequalities([i1, i2, i3, i4, i5])

        #of_iq = AffineLine2D((1.9, 1.3)).set_color(BLUE).set_z_index(rect3.get_z_index() - 1 + 0.5)

        of_arrow = Arrow(start=ORIGIN, end=np.array((*OF_INITIAL, 0)), buff=0).set_z_index(area.dots_z_index - 0.01)
        of_arrow_shadow = of_arrow.copy().set_color(WHITE).set_z_index(of_arrow.get_z_index() - 0.000001)

        optimum = list(solve_farm(OF_INITIAL))
        optimum[0] /= 1000
        optimum[1] /= 1000

        sweep = AffineLine2D(OF_INITIAL).rotate(PI / 2)
        sweep.crop_to_screen(self.camera.frame)
        sweep.set_z_index(rect3.get_z_index() - 1 + 0.99).set_color(BLUE)

        # - hack after crop_to_screen
        sweep_goal = AffineLine2D(OF_INITIAL).rotate(-PI / 2).move_to([*optimum, 0])
        sweep_goal.set_z_index(rect3.get_z_index() - 1 + 0.99)

        sweep_angle = Angle(sweep.line, of_arrow, dot=True).set_z_index(99).set_color(BLUE)

        sweep.dots = VGroup()

        sweep.add(sweep.dots)

        sweep.lineextra = VGroup()
        sweep.add(sweep.lineextra)

        def sweep_updater(obj):
            dots = sweep.get_area_border_intersection(area)

            if len(dots) <= 1:
                return

            g = VGroup().set_z_index(100000)
            for i in range(len(dots)):
                for j in range(i + 1, len(dots)):
                    d1, d2 = dots[i], dots[j]

                    g.add(
                        Line(start=d1.get_center(),
                             end=d2.get_center(),
                             color=BLUE, stroke_width=LINE_STROKE + 2.5).set_z_index(100000)
                    )

            sweep.lineextra.become(g).set_z_index(100000)

            sweep.dots.become(dots).set_z_index(100000).set_color(BLUE)

        sweep_updater(None)

        sweep_dots_tmp = sweep.dots
        sweep.remove(sweep.dots)

        align_object_by_coords(
            VGroup(i1, i4_hp, i2, i3, i4, i5, area, numberplane, of_arrow, of_arrow_shadow, sweep, sweep_goal, sweep_angle, sweep_dots_tmp),
            area.dots.get_center(),
            guide3.get_center(),
        )

        i1.crop_to_screen(self.camera.frame)
        i2.crop_to_screen(self.camera.frame)
        i3.crop_to_screen(self.camera.frame)
        i4.crop_to_screen(self.camera.frame)
        i5.crop_to_screen(self.camera.frame)

        labels = VGroup(
            Tex("$x_p$").scale(1.2).move_to(numberplane)\
                    .next_to(numberplane.axes[0], DOWN, buff=0.33)\
                    .align_to(self.camera.frame, RIGHT).shift(LEFT * 0.2)\
                    .set_color(POTATO_COLOR),
            Tex("$x_c$").scale(1.2).move_to(numberplane)\
                    .next_to(numberplane.axes[1], LEFT, buff=0.23)\
                    .align_to(self.camera.frame, UP).shift(DOWN * 0.35)\
                    .set_color(CARROT_COLOR),
        ).set_z_index(i1.get_z_index() + 1)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    main_group.animate.shift(LEFT * theory_group.get_x() * 2),
                    rect2.animate.shift(LEFT * theory_group.get_x() * 2).set_opacity(0),
                    rect3.animate.shift(LEFT * theory_group.get_x() * 2).set_opacity(1),
                    var.animate.shift(LEFT * theory_group.get_x() * 2),
                    ineqs.animate.shift(LEFT * theory_group.get_x() * 2),
                    exp.animate.shift(LEFT * theory_group.get_x() * 2),
                    of.animate.shift(LEFT * theory_group.get_x() * 2),
                    #theory_group.animate.shift(LEFT * theory_group.get_x() * 2),
                    equivalenece.animate.shift(LEFT * theory_group.get_x() * 2).set_opacity(0),
                ),
                AnimationGroup(
                    FadeIn(numberplane.background_lines),
                    FadeIn(numberplane.axes),
                    #FadeIn(labels)
                ),
                lag_ratio=0.5,
            ),
        )

        labels_tmp = labels.copy()
        xptmp = var[0][10:10+2].copy()
        xctmp = var[0][13:13+2].copy()

        self.play(
            AnimationGroup(
                Transform(xptmp, labels_tmp[0]),
                Transform(xctmp, labels_tmp[1]),
                lag_ratio=0.25,
            )
        )

        self.remove(xptmp, xctmp)
        self.add(labels)

        sr = SurroundingRectangle(
            VGroup(
                Dot().align_to(self.camera.frame, UP + RIGHT),
                Dot().align_to(self.camera.frame, DOWN + RIGHT),
                Dot().align_to(rect3, RIGHT),
            ),
            fill_opacity=1,
        ).move_to(guide3).set_color_by_gradient((RED, GREEN)).set_opacity(0.35)
        sr.set_sheen_direction(unit_vector(OF_INITIAL[0] * RIGHT + OF_INITIAL[1] * UP))

        self.remove(main_group, rect2, equivalenece)

        big_hl = CreateHighlight(ineqs)
        hl = CreateHighlight(ineqs[0][7:7+7])

        self.play(
            exp.animate.set_opacity(BIG_OPACITY),
            of.animate.set_opacity(BIG_OPACITY),
            FadeIn(big_hl),
        )

        self.play(
            AnimationGroup(
                Transform(big_hl, hl),
                Create(i4),
                lag_ratio=0.5,
            ),
        )

        self.remove(big_hl)
        self.add(hl)

        self.play(FadeIn(i4_hp))

        self.play(
            AnimationGroup(
                FadeOut(hl),
                Create(i1),
                Create(i2),
                Create(i3),
                Create(i5),
                AnimationGroup(
                    FadeOut(i4_hp),
                    FadeIn(area),
                ),
                lag_ratio=0.25,
            ),
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(i1),
                    FadeOut(i2),
                    FadeOut(i3),
                    FadeOut(i4),
                    FadeOut(i5),
                ),
                lag_ratio=0.5,
            ),
        )

        self.play(area.area.animate(rate_func=there_and_back, run_time=1.25).set_fill(BLUE, 0.5))

        self.play(
            exp.animate.set_opacity(1),
            of.animate.set_opacity(MED_OPACITY),
            ineqs.animate.set_opacity(BIG_OPACITY),
        )

        self.add(sr)
        thingy = ImageMobject("assets/thingy.png")\
                .set_height(sr.get_height() * 2)\
                .move_to(sr).rotate(atan2(OF_INITIAL[1], OF_INITIAL[0]) - PI / 2)\
                .set_z_index(sr.get_z_index() + 0.1)

        self.play(
            AnimationGroup(
                # hack!
                thingy.animate(run_time=2).shift((OF_INITIAL[1] * UP + OF_INITIAL[0] * RIGHT) * 7),
                AnimationGroup(
                    Write(of_arrow),
                ),
                lag_ratio=0,
            )
        )

        self.remove(thingy)

        self.play(
            FadeIn(sweep),
            FadeIn(sweep_angle),
            FadeIn(sweep_dots_tmp),
            of_arrow.animate.set_color(BLUE),
        )

        sweep.add(sweep_dots_tmp)

        dl = DashedLine(ORIGIN - 0.0001, ORIGIN + 0.0001).set_z_index(of_arrow.get_z_index() - 0.00001).set_color(BLUE)

        def of_updater(obj):
            start = of_arrow.get_start()
            end = of_arrow.get_end()

            point = intersection(
                line(start, end),
                line(sweep.line.get_start(), sweep.line.get_end()),
            )

            new_point = np.array([*point, 0])

            of_arrow.put_start_and_end_on(
                new_point,
                new_point + np.array([*OF_INITIAL, 0])
            )

            sweep_angle.become(Angle(sweep.line, of_arrow, dot=True).set_color(BLUE).set_z_index(99))

        def dl_updater(obj):
            start = of_arrow_shadow.get_start()
            end = intersection(
                line(of_arrow_shadow.get_start(), of_arrow_shadow.get_end()),
                line(sweep.line.get_start(), sweep.line.get_end()),
            )
            end = np.array([*end, 0])

            l = 0.085
            lt = l * 2

            dist = distance(start, end)
            dist_rounded = int(dist / lt) * lt

            if abs(dist) < 0.001:
                return

            end_rounded = ((end - start) / dist) * dist_rounded + start + l / 10

            obj.become(DashedLine(end_rounded, start, dash_length=l, stroke_width=of_arrow.get_stroke_width() * 0.95)\
                    .set_color(BLUE)\
                    .set_z_index(of_arrow.get_z_index() - 0.0001))

        dl.add_updater(dl_updater)
        self.add(dl)

        # updaters are broken
        dummy = VMobject()
        dummy.add_updater(sweep_updater)
        dummy.add_updater(of_updater)
        self.add(dummy)

        self.camera.frame.save_state()
        theory_group.save_state()
        rect3.save_state()

        self.play(
            FadeIn(of_arrow_shadow),
            sweep.animate(run_time=3).move_to(sweep_goal),
        )

        self.remove(dummy)

        optimum = sweep.dots
        sweep.remove(sweep.dots)

        optimum_texts = VGroup(
            Tex(r"$1\,000\ \mathrm{kg}$").scale(0.8)\
                    .move_to(optimum).align_to(numberplane.axes[0], UP).shift(DOWN * 0.35)\
                    .set_z_index(100000),
            Tex(r"$4\,000\ \mathrm{kg}$").scale(0.8)\
                    .move_to(optimum).align_to(numberplane.axes[1], RIGHT).shift(LEFT * 0.35)\
                    .set_z_index(100000),
            Tex(r"$\$8\,000$").scale(0.8)\
                    .next_to(optimum, UP + RIGHT)\
                    .set_z_index(100000),
        )

        for i in range(3):
            optimum_texts[i].add(CreateSR(optimum_texts[i]))

        self.play(
            FadeIn(optimum_texts),
            FadeOut(sweep_angle),
            of_arrow.animate.set_opacity(0),
            ineqs.animate.set_opacity(1),
        )

        for i in [0, 1, 2]:
            self.play(
                optimum_texts[i].animate(rate_func=there_and_back).scale(THERE_AND_BACK_SCALE),
            )

        #vm = CreateMeaning(var, "$\mathbf{x} \in \mathbb{R}^{+}_{0}$")
        #vi = CreateMeaning(ineqs, r"$\begin{aligned}\mathbf{0} &\le \mathbf{x} \\[0.05em] A\mathbf{x} &\le \mathbf{b}\end{aligned}$")
        #vo = CreateMeaning(VGroup(of, exp), "$\max\ \mathbf{c}^T \mathbf{x}$")

        vm = CreateMeaning(var, "\small variables $\in \mathbb{R}^{+}_{0}$")
        vi = CreateMeaning(ineqs, r"\small s.t. linear \par inequalities")
        vo = CreateMeaning(VGroup(of, exp), "\small maximizing \par linear function")

        dl.remove_updater(dl_updater)
        self.play(
            FadeOut(optimum_texts),
            FadeOut(optimum),
            FadeOut(dl),
            FadeOut(sweep)
        )

        for o, rt in [(vm, 1.25), (vi, 1.5), (vo, 1.5)]:
            self.play(
                AnimationGroup(
                    FadeIn(o[0]),
                    Write(o[1], run_time=rt),
                    lag_ratio=0.5,
                )
            )

        print(numberplane.get_center())

        iextras = []
        ipts = [
            [np.array([0, 0]), np.array([1, -2]), 0.5, None],
            [np.array([0, 0]), np.array([1, -0.5]), 0.5, None],
            [np.array([3, 0]), np.array([4, 1]), 0.25, None],
            [np.array([3, 2]), np.array([2, 3.5]), 0.25, "<="],
            [np.array([0, 4]), np.array([-1, 3.7]), 0.15, "<="],
            [np.array([0, 4]), np.array([-1, 3]), 0.15, "<="],
            [np.array([0, 4]), np.array([-1, 0]), 0.2, "<="],
            [np.array([1, 4]), np.array([0, 4.9]), 0.05, "<="],
        ]
        inorms = []

        start = of_arrow_shadow.get_start()

        for p1, p2, s, op in ipts:
            a, b, c = Inequality2D.points_to_slope(p1, p2)
            iq = Inequality2D(a, b, op or ">=", c).set_opacity(0).shift(of_arrow_shadow.get_start())
            iextras.append(iq)
            self.add(iq)
            area.add_inequalities([iq])
            d = p2 - p1
            inorms.append((-d[1], d[0], 0) / np.linalg.norm(d))

            ino = np.array((-d[1], d[0])) / np.linalg.norm(d)

        def ineqs_complex_updater(obj, dt):
            obj._update_area()

            best_score = float('inf')
            best_pos = None

            for d in obj.dots:
                score = d.get_center()[0] * OF_INITIAL[0] + d.get_center()[1] * OF_INITIAL[1]

                if score < best_score:
                    best_score = score
                    best_pos = d.get_center()

            of_arrow_shadow.put_start_and_end_on(
                best_pos,
                best_pos + of_arrow_shadow.get_end() - of_arrow_shadow.get_start()
            )

        self.add(area)
        area.add_updater(ineqs_complex_updater)

        self.play(
            *[iextras[i].animate.shift(inorms[i] * ipts[i][-2])
             for i in range(len(ipts))],
            vi[1].animate.scale(1.25),
        )

        # TODO: 3D stuff here

        self.play(
            *[iextras[i].animate.shift(-inorms[i] * ipts[i][-2] * 1.1)
             for i in range(len(ipts))],
            FadeOut(vm, vi, vo),
        )

        area.remove_updater(ineqs_complex_updater)
        area.remove_inequalities(iextras)

        def of_line_updater(obj):
            vector  = of_arrow_shadow.get_end() - of_arrow_shadow.get_start()
            x, y, _ = vector

            optimum = list(solve_farm([x, y]))
            optimum[0] /= 1000
            optimum[1] /= 1000

            sweep.line.become(AffineLine2D([x, y]).line.set_color(BLUE).rotate(PI / 2)\
                    .move_to(of_arrow_shadow.get_start()).shift([*optimum, 0])
            )

            op = "+" if y >= 0 else "-"

            new_exp = Tex(f"$$\max\ {x:.1f}x_p {op} {abs(y):.1f}x_c$$")\
                    .move_to(exp).align_to(exp, DOWN)
            new_exp[0][3:3+5].set_color(POTATO_COLOR)
            new_exp[0][9:9+5].set_color(CARROT_COLOR)

            exp.become(new_exp)

        sm = Tex(r"\underline{Simplex Method}").set_z_index(10000000000).scale(1)
        sm.add(CreateSR(sm, buff=0.17))
        sm.align_to(self.camera.frame, RIGHT + UP).shift((LEFT * 1.2 + DOWN) * 0.25)

        self.play(
            AnimationGroup(
                FadeIn(sm[1]),
                Write(sm[0]),
                lag_ratio=0.2,
            )
        )

        self.play(
            FadeIn(optimum),
            FadeIn(dl),
            FadeIn(sweep)
        )

        srcp = sr.copy()\
               .set_z_index(sr.get_z_index() + 0.2)

        thingy = ImageMobject("assets/thingy.png")\
                .set_height(sr.get_height() * 2)\
                .move_to(sr).rotate(atan2(OF_INITIAL[1], OF_INITIAL[0]) - PI / 2)\
                .set_z_index(sr.get_z_index() + 0.1)

        thingy2 = ImageMobject("assets/thingy.png")\
                .set_height(sr.get_height() * 2)\
                .move_to(sr).rotate(atan2(-OF_INITIAL[1], -OF_INITIAL[0]) - PI / 2)\
                .set_z_index(sr.get_z_index() + 0.1)
        thingy2.shift(-unit_vector(OF_INITIAL[1] * UP + OF_INITIAL[0] * RIGHT) * 18)

        self.add(thingy, thingy2, srcp)

        self.play(
            thingy.animate(run_time=2.5).shift((OF_INITIAL[1] * UP + OF_INITIAL[0] * RIGHT) * 9),
            thingy2.animate(run_time=2.5).shift((OF_INITIAL[1] * UP + OF_INITIAL[0] * RIGHT) * 9),
        )

        self.remove(thingy, thingy2, srcp)

        dl.add_updater(dl_updater)

        self.play(
            *[MyFlash(d, color=WHITE, z_index=d.get_z_index() + 1)
              for d in area.dots],
            MyFlash(optimum, color=BLUE, z_index=optimum.get_z_index() + 2),
        )

        def sr_updater(obj):
            vector  = of_arrow_shadow.get_end() - of_arrow_shadow.get_start()
            obj.set_sheen_direction(unit_vector(vector))

        sr.add_updater(sr_updater)

        dummy = VMobject()
        dummy.add_updater(sweep_updater)
        dummy.add_updater(of_line_updater)
        self.add(dummy)

        angle = atan2(OF_INITIAL[1], OF_INITIAL[0])

        self.play(
            Rotate(of_arrow_shadow, -angle, about_point=of_arrow_shadow.get_start()),
            run_time=2,
        )

        self.play(
            *[MyFlash(d, color=BLUE, z_index=d.get_z_index() + 1)
              for d in sweep.dots],
        )

        self.play(
            Rotate(of_arrow_shadow, +angle - 2 * PI, about_point=of_arrow_shadow.get_start()),
            run_time=5,
        )

        self.remove(dummy)
        sr.remove_updater(sr_updater)
        dl.remove_updater(dl_updater)
        self.play(
            FadeOut(optimum),
            FadeOut(dl),
            FadeOut(sweep)
        )

        fade_rect = get_fade_rect()

        of_arrow_shadow.set_z_index(fade_rect.get_z_index() - 0.00000000001)

        of_arrow_shadow_2 = of_arrow_shadow.copy().set_color(BLUE).set_z_index(fade_rect.get_z_index() + 1)
        of_dot = Dot().scale(OPTIMUM_DOT_SCALE).set_color(BLUE).move_to(of_arrow_shadow_2.get_start())\
                .set_z_index(of_arrow_shadow_2.get_z_index())

        trace = TracedPath(of_dot.get_center).set_color(BLUE).set_stroke_width(8)\
                .set_z_index(area.dots[0].get_z_index() - 0.00001)

        G = VGroup(
            area,
            of_arrow_shadow,
            numberplane,
            labels[0],
        )

        l0 = Line(
            start=of_dot.get_center(),
            end=of_dot.get_center(),
            color=trace.get_color(),
            stroke_width=trace.get_stroke_width(),
        ).set_z_index(trace.get_z_index())
        p0 = Tex("pivot \#1").scale(0.75).next_to(l0, DOWN).shift(RIGHT * 1.5).set_z_index(l0.get_z_index())

        sweep.move_to(of_arrow_shadow_2.get_start())
        sweep.remove(sweep.lineextra)
        self.play(
            #FadeIn(sweep),
            FadeIn(of_arrow_shadow_2),
            FadeIn(of_dot),
        )

        self.play(
            #VGroup(of_arrow_shadow_2, of_dot, sweep).animate.shift(RIGHT * 3),
            VGroup(of_arrow_shadow_2, of_dot).animate.shift(RIGHT * 3),
            l0.animate.become(Line(
                start=of_dot.get_center() + RIGHT * 3,
                end=of_dot.get_center(),
                color=trace.get_color(),
                stroke_width=trace.get_stroke_width(),
            ).set_z_index(trace.get_z_index())),
            FadeIn(p0, run_time=1),
            run_time=2,
        )

        l1 = Line(
            start=of_dot.get_center(),
            end=of_dot.get_center(),
            color=trace.get_color(),
            stroke_width=trace.get_stroke_width(),
        ).set_z_index(trace.get_z_index())
        us1 = 0.5
        p1 = Tex("pivot \#2").scale(0.75).next_to(l1, RIGHT).shift(UP * (1 - us1)).set_z_index(l1.get_z_index())

        self.play(
            l0.animate.shift(DOWN * us1),
            p0.animate.shift(DOWN * us1),
            l1.animate.become(Line(
                start=of_dot.get_center() + UP * (2 - us1),
                end=of_dot.get_center() + DOWN * us1,
                color=trace.get_color(),
                stroke_width=trace.get_stroke_width(),
            ).set_z_index(trace.get_z_index())),
            G.animate.shift(DOWN * us1),
            FadeIn(p1, shift=DOWN * us1, run_time=1),
            #VGroup(of_arrow_shadow_2, of_dot, sweep).animate.shift(UP * (2 - us1)),
            VGroup(of_arrow_shadow_2, of_dot).animate.shift(UP * (2 - us1)),
            run_time=1.5,
        )

        l2 = Line(
            start=of_dot.get_center(),
            end=of_dot.get_center(),
            color=trace.get_color(),
            stroke_width=trace.get_stroke_width(),
        ).set_z_index(trace.get_z_index())
        p2 = Tex("pivot \#3").scale(0.75).next_to(l2.get_center(), UP + RIGHT).shift(LEFT).set_z_index(l1.get_z_index())
        us2 = 1

        self.play(
            l2.animate.become(Line(
                start=of_dot.get_center() + UP * (2 - us2) + LEFT * 2,
                end=of_dot.get_center() + DOWN * us2,
                color=trace.get_color(),
                stroke_width=trace.get_stroke_width(),
            ).set_z_index(trace.get_z_index())),
            l0.animate.shift(DOWN * us2),
            l1.animate.shift(DOWN * us2),
            p0.animate.shift(DOWN * us2),
            p1.animate.shift(DOWN * us2),
            G.animate.shift(DOWN * us2),
            FadeIn(p2, shift=DOWN * us2, run_time=1),
            #VGroup(of_arrow_shadow_2, of_dot, sweep).animate.shift(UP * (2 - us2) + LEFT * 2),
            VGroup(of_arrow_shadow_2, of_dot).animate.shift(UP * (2 - us2) + LEFT * 2),
            run_time=1.5,
        )

        self.play(
            MyFlash(of_dot, color=BLUE, z_index=optimum.get_z_index() + 2),
        )

        self.play(
            VGroup(numberplane, of_arrow_shadow, area, labels[0]).animate.shift(UP * (us1 + us2)),
            #FadeOut(sweep, of_arrow_shadow_2, of_dot, l0, l1, l2, shift=UP * (us1 + us2)),
            #FadeOut(sweep, of_arrow_shadow_2, of_dot, l0, l1, l2, p0, p1, p2, shift=UP * (us1 + us2)),
            FadeOut(of_arrow_shadow_2, of_dot, l0, l1, l2, p0, p1, p2, shift=UP * (us1 + us2)),
        )

        # fix positions, will be used later
        VGroup(l0, l1, l2, p0, p1, p2).shift(UP * (us1 + us2))

        # NOTE: WE ARE ALL COPIED
        ineqs2 = Tex(r"""$$\begin{aligned}
        x_1, x_2  &\ge 0 \\[0.3em]
              x_1 \phantom{{}+ x_2} &\le 3\,000 \\[-0.2em]
              x_2 &\le 4\,000 \\[-0.2em]
              x_1 + x_2 &\le 5\,000
                \end{aligned}$$""").align_to(ineqs, UP + RIGHT)
        exp2 = Tex(r"$$\max\ " + str(OF_INITIAL[0]) + r"x_1 + " + str(OF_INITIAL[1]) + r" x_2$$").align_to(exp, UP + LEFT)
        var2 = Tex("variables: $x_1, x_2$").align_to(var, UP + LEFT)

        labels2 = VGroup(
            Tex("$x_1$").scale(1.2).move_to(numberplane)\
                    .next_to(numberplane.axes[0], DOWN, buff=0.33)\
                    .align_to(self.camera.frame, RIGHT).shift(LEFT * 0.2),
            Tex("$x_2$").scale(1.2).move_to(numberplane)\
                    .next_to(numberplane.axes[1], LEFT, buff=0.23)\
                    .align_to(self.camera.frame, UP).shift(DOWN * 0.35)
        ).set_z_index(i1.get_z_index() + 1)

        labels2[0].align_to(labels[0], UP + LEFT)
        labels2[1].align_to(labels[1], UP + LEFT)

        self.play(
            Transform(ineqs, ineqs2),
            Transform(exp, exp2),
            Transform(var, var2),
            Transform(labels, labels2),
        )

        # NOTE: I'm copy pasted!
        of_arrow_shadow_2 = of_arrow_shadow.copy().set_color(BLUE).set_z_index(fade_rect.get_z_index() + 1)
        of_dot = Dot().scale(OPTIMUM_DOT_SCALE).set_color(BLUE).move_to(of_arrow_shadow_2.get_start())\
                .set_z_index(of_arrow_shadow_2.get_z_index())

        hl = CreateHighlight(ineqs[0][:7])

        self.play(
            FadeIn(of_dot),
            FadeIn(of_arrow_shadow_2),
            MyFlash(of_dot, color=BLUE, z_index=of_dot.get_z_index() + 1),
        )

        i1.set_color(YELLOW).set_opacity(0)
        i2.set_color(YELLOW).set_opacity(0)
        i3.set_color(YELLOW).set_opacity(0)
        i4.set_color(YELLOW).set_opacity(0)
        i5.set_color(YELLOW).set_opacity(0)

        self.play(
            FadeIn(hl),
            i1.animate.set_opacity(1),
            i2.animate.set_opacity(1),
        )

        val = Tex(r"$(0, 0)$").scale(0.6)\
            .next_to(of_dot, UP)\
            .set_z_index(10000000000)
        val.add(CreateSR(val))

        def value_updater(obj, dt):
            c = of_dot.get_center() - of_arrow_shadow.get_start()

            x = int(round(c[0] * 1000))
            y = int(round(c[1] * 1000))

            def fmt(x):
                x = str(x)
                if len(x) == 4:
                    return f"{x[0]}\,{x[1:]}"
                return x

            val2 = Tex(rf"$({fmt(x)}, {fmt(y)})$").scale(0.6)\
                .next_to(of_dot, UP)\
                .set_z_index(10000000000)
            val2.add(CreateSR(val2))

            val.become(val2)

        hl2 = CreateHighlight(ineqs[0][7:14])

        self.play(
            FadeIn(val),
        )

        self.play(
            FadeIn(p0),
            MyFlash(of_dot.copy().shift(RIGHT * 3), color=WHITE, z_index=of_dot.get_z_index() + 1),
        )

        val.add_updater(value_updater)

        a_surprise_weapon_that_will_help_us_later = VGroup(
            ineqs.copy(),
            exp.copy(),
            var.copy(),
            of.copy(),
        )

        self.play(
            of_arrow_shadow_2.animate.shift(RIGHT * 1.5),
            of_dot.animate.shift(RIGHT * 1.5),
            Transform(hl, CreateHighlight(ineqs[0][3:7])),
            i1.animate.set_opacity(0),
            run_time=1.5,
        )

        self.play(
            of_arrow_shadow_2.animate.shift(RIGHT * 1.5),
            of_dot.animate.shift(RIGHT * 1.5),
            FadeIn(hl2),
            i4.animate.set_opacity(1),
            run_time=1.5,
        )

        G = VGroup(
            area,
            of_arrow_shadow,
            numberplane,
            labels[0],
        )

        i1.line.put_start_and_end_on(
            i1.line.get_start() + UP * 5,
            i1.line.get_end() + DOWN * 5,
        )

        i3.line.put_start_and_end_on(
            i3.line.get_start() + (UP + LEFT) * 5,
            i3.line.get_end() + (DOWN + RIGHT) * 5,
        )

        p1.shift(DOWN * us1)
        p2.shift(DOWN * us1)

        self.play(
            G.animate.shift(DOWN * us1),
            p0.animate.shift(DOWN * us1),
            FadeIn(p1, shift=DOWN * us1),
            of_arrow_shadow_2.animate.shift(UP * (2 - us1)),
            of_dot.animate.shift(UP * (2 - us1)),
            Transform(hl, CreateHighlight(ineqs[0][21:])),
            i2.animate.set_opacity(0).shift(DOWN * us1),
            i3.animate.set_opacity(1).shift(DOWN * us1),
            run_time=1.5,
        )

        i2.shift(UP * us1)
        p2.shift(DOWN * us2)
        i5.shift(DOWN * us1)

        self.play(
            G.animate.shift(DOWN * us2),
            FadeIn(p2, shift=DOWN * us2),
            p0.animate.shift(DOWN * us2),
            p1.animate.shift(DOWN * us2),
            of_arrow_shadow_2.animate.shift(UP * (2 - us2) + LEFT * 2),
            of_dot.animate.shift(UP * (2 - us2) + LEFT * 2),
            Transform(hl2, CreateHighlight(ineqs[0][14:21])),
            i4.animate.set_opacity(0).shift(DOWN * us2),
            i5.animate.set_opacity(1).shift(DOWN * us2),
            i3.animate.shift(DOWN * us2),
            run_time=1.5,
        )

        val.remove_updater(value_updater)

        self.play(
            AnimationGroup(
                MyFlash(of_dot, color=BLUE, z_index=of_dot.get_z_index() + 1),
                val.animate(rate_func=there_and_back).scale(THERE_AND_BACK_SCALE),
                lag_ratio=0.25,
            )
        )

        self.play(
            G.animate.shift(UP * (us1 + us2)),
            i5.animate.set_opacity(0).shift(UP * (us1 + us2)),
            i3.animate.set_opacity(0).shift(UP * (us1 + us2)),
            FadeOut(hl, hl2),
            FadeOut(val, of_arrow_shadow_2, of_dot, p0, p1, p2, shift=UP * (us1 + us2)),
        )

        # NOTE: WE ARE ALL COPIED
        ineqs3 = ComplexTex(r"""$$\begin{aligned}
        x_1, x_2, s_1, s_2, s_3  &\ge 0 \\[0.3em]
              x_1 \phantom{{}+ x_2} + s_1 \phantom{{} + s_2 + s_3} &= 3\,000 \\[-0.2em]
              x_2 \phantom{{} + s_1} + s_2 \phantom{{} + s_3} &= 4\,000 \\[-0.2em]
              x_1 + x_2 \phantom{{} + s_1 + s_2} + s_3 &= 5\,000
                \end{aligned}$$""").move_to(ineqs).set_z_index(ineqs.get_z_index())
        var3 = ComplexTex("variables: $x_1, x_2, s_1, s_2, s_3$").move_to(var).set_z_index(var.get_z_index())

        space = 2.5

        guide4 = -guide2.get_center() + RIGHT * (space / 2)

        of3 = of.copy()
        exp3 = exp2.copy().move_to(exp).set_z_index(exp.get_z_index())

        theory_group_two = VGroup(of3, exp3, ineqs3, var3).move_to(guide4)

        i1.shift(RIGHT * space / 2)
        i2.shift(RIGHT * space / 2)
        i3.shift(RIGHT * space / 2)
        i4.shift(RIGHT * space / 2)
        i5.shift(RIGHT * space / 2)
        of_arrow_shadow_2.shift(RIGHT * space / 2)
        of_dot.shift(RIGHT * space / 2)

        VGroup(of3, exp3).align_to(of, UP)
        VGroup(var3).align_to(var, UP)
        VGroup(ineqs3).align_to(ineqs, UP)

        self.remove(rect3)
        rect_large.flip().set_height(rect3.get_height()).move_to(rect3).align_to(rect3, RIGHT).set_z_index(rect3.get_z_index())
        self.add(rect_large)

        var3[0][16:16+2].set_color(ORANGE)
        var3[0][19:19+2].set_color(ORANGE)
        var3[0][22:22+2].set_color(ORANGE)
        ineqs3[0][6:6+2].set_color(ORANGE)
        ineqs3[0][9:9+2].set_color(ORANGE)
        ineqs3[0][12:12+2].set_color(ORANGE)
        ineqs3[0][19:19+2].set_color(ORANGE)
        ineqs3[0][29:29+2].set_color(ORANGE)
        ineqs3[0][42:42+2].set_color(ORANGE)

        slack = Tex(r"slack").scale(0.7).set_color(ORANGE).next_to(
            VGroup(var3[0][16:16+2], var3[0][22:22+2]), UP, buff=0.25
        ).set_z_index(100000000000)

        # this took 3-5 years from my life
        self.play(
            rect_large.animate.shift(RIGHT * space),
            VGroup(
                area,
                of_arrow_shadow,
                numberplane,
                sr,
                labels[1],
            ).animate.shift(RIGHT * space / 2),
            Transform(exp, exp3),
            Transform(of, of3),
            AnimationGroup(
                Transform(var[0][:15], var3[0][:15]),
                AnimationGroup(
                    FadeIn(var3[0][15:]),
                    FadeIn(slack),
                ),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                AnimationGroup(
                    Transform(ineqs[0][:5], ineqs3[0][:5]),
                    Transform(ineqs[0][5:5+2], ineqs3[0][14:14+2]),
                ),
                FadeIn(ineqs3[0][5:5+9]),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                AnimationGroup(
                    Transform(ineqs[0][7:7+2], ineqs3[0][16:16+2]),
                    Transform(ineqs[0][9:9+5], ineqs3[0][21:21+5]),
                ),
                FadeIn(ineqs3[0][18:18+3]),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                AnimationGroup(
                    Transform(ineqs[0][14:14+2], ineqs3[0][26:26+2]),
                    Transform(ineqs[0][16:16+5], ineqs3[0][31:31+5]),
                ),
                FadeIn(ineqs3[0][28:28+3]),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                AnimationGroup(
                    Transform(ineqs[0][21:21+5], ineqs3[0][36:36+5]),
                    Transform(ineqs[0][26:], ineqs3[0][44:]),
                ),
                FadeIn(ineqs3[0][41:41+3]),
                lag_ratio=0.5,
            ),
        )

        #             ______
        #        .d$$$******$$$$c.
        #     .d$P"            "$$c
        #    $$$$$.           .$$$*$.
        #  .$$ 4$L*$$.     .$$Pd$  '$b
        #  $F   *$. "$$e.e$$" 4$F   ^$b
        # d$     $$   z$$$e   $$     '$.
        # $P     `$L$$P` `"$$d$"      $$
        # $$     e$$F       4$$b.     $$
        # $b  .$$" $$      .$$ "4$b.  $$
        # $$e$P"    $b     d$`    "$$c$F
        # '$P$$$$$$$$$$$$$$$$$$$$$$$$$$
        #  "$c.      4$.  $$       .$$
        #   ^$$.      $$ d$"      d$P
        #     "$$c.   `$b$F    .d$P"
        #       `4$$$c.$$$..e$$P"
        #           `^^^^^^^`

        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp3, ineqs3, var3, rect_large, area, of_arrow_shadow, numberplane, sr, labels, sm, slack)

        hl = CreateHighlight(VGroup(ineqs3[0][21], ineqs3[0][31], ineqs3[0][44]))

        a = Tex("$0$")
        a.add(Tex("$=$").scale(0.65).rotate(PI / 2).next_to(a, UP, buff=0.1))
        a.set_color(YELLOW).set_z_index(1000000000).next_to(var3[0][-8:-8+2], DOWN, buff=0.1).set_color(WHITE)

        b = a.copy().next_to(var3[0][-2:], DOWN, buff=0.1).set_color(WHITE)

        # undoes the last move
        of_arrow_shadow_2.shift(UP * -2 + LEFT * -2)
        of_dot.shift(UP * -2 + LEFT * -2 + UP * (us1 + us2))

        # copy-pasted
        val = Tex(r"$(3\,000, 2\,000)$").scale(0.6)\
            .next_to(of_dot, UP)\
            .set_z_index(10000000000)
        val.add(CreateSR(val))

        self.play(
            #FadeIn(of_arrow_shadow_2),
            FadeIn(val),
            FadeIn(of_dot),
            MyFlash(of_dot, color=BLUE, z_index=of_dot.get_z_index() + 1),
            i4.animate.set_opacity(1),
            i3.animate.set_opacity(1),
        )

        hl1 = CreateHighlight(ineqs3[0][16:26])
        hl2 = CreateHighlight(ineqs3[0][36:49])

        self.play(
            FadeIn(hl1),
            FadeIn(hl2),
            var3[0][16:16+2].animate.set_color(YELLOW).set_opacity(BIG_OPACITY),
            var3[0][22:22+2].animate.set_color(YELLOW).set_opacity(BIG_OPACITY),
            var3[0][18:18+1].animate.set_opacity(BIG_OPACITY), #,
            var3[0][21:21+1].animate.set_opacity(BIG_OPACITY), #,
            ineqs3[0][6:6+2].animate.set_color(YELLOW).set_opacity(BIG_OPACITY),
            ineqs3[0][12:12+2].animate.set_color(YELLOW).set_opacity(BIG_OPACITY),
            ineqs3[0][8:8+1].animate.set_opacity(BIG_OPACITY), #,
            ineqs3[0][11:11+1].animate.set_opacity(BIG_OPACITY), #,
            ineqs3[0][18:18+1].animate.set_opacity(BIGGER_OPACITY),
            ineqs3[0][19:19+2].animate.set_color(YELLOW).set_opacity(BIGGER_OPACITY),
            ineqs3[0][41:41+1].animate.set_opacity(BIGGER_OPACITY),
            ineqs3[0][42:42+2].animate.set_color(YELLOW).set_opacity(BIGGER_OPACITY),
        )

        self.play(
            FadeOut(hl1),
            FadeOut(hl2),
            FadeOut(of_dot),
            FadeOut(val),
            i4.animate.set_opacity(0),
            i3.animate.set_opacity(0),
            var3[0][16:16+2].animate.set_color(ORANGE).set_opacity(1),
            var3[0][22:22+2].animate.set_color(ORANGE).set_opacity(1),
            ineqs3[0][6:6+2].animate.set_color(ORANGE).set_opacity(1),
            ineqs3[0][12:12+2].animate.set_color(ORANGE).set_opacity(1),
            ineqs3[0][18:18+1].animate.set_opacity(1),
            ineqs3[0][19:19+2].animate.set_color(ORANGE).set_opacity(1),
            ineqs3[0][41:41+1].animate.set_opacity(1),
            ineqs3[0][42:42+2].animate.set_color(ORANGE).set_opacity(1),
            var3[0][18:18+1].animate.set_opacity(1), #,
            var3[0][21:21+1].animate.set_opacity(1), #,
            ineqs3[0][8:8+1].animate.set_opacity(1), #,
            ineqs3[0][11:11+1].animate.set_opacity(1), #,
        )

        # NOTE: I'm copy-pasted
        of_arrow_shadow_2 = of_arrow_shadow.copy().set_color(BLUE).set_z_index(fade_rect.get_z_index() + 1)
        of_dot = Dot().scale(OPTIMUM_DOT_SCALE).set_color(BLUE).move_to(of_arrow_shadow_2.get_start())\
                .set_z_index(of_arrow_shadow_2.get_z_index())

        vars_buff = 0.25

        nonbas_vars = VGroup(
            var3[0][10:10+2].copy().set_color(YELLOW),
            var3[0][13:13+2].copy().set_color(YELLOW),
        ).arrange(buff=vars_buff)

        bas_vars = VGroup(
            var3[0][16:16+2].copy().set_color(ORANGE),
            var3[0][19:19+2].copy().set_color(ORANGE),
            var3[0][22:22+2].copy().set_color(ORANGE),
        ).arrange(buff=vars_buff)

        VGroup(nonbas_vars, bas_vars).arrange(buff=1.5).move_to(var3).align_to(var3, DOWN)

        nonbasic = Tex("tight").scale(0.7).next_to(nonbas_vars, UP, buff=0.25).set_z_index(rect_large.get_z_index() + 1).set_opacity(0)
        basic = Tex("loose").scale(0.7).next_to(bas_vars, UP, buff=0.25).set_z_index(rect_large.get_z_index() + 1).set_opacity(0)
        nonbasic.align_to(basic, UP)

        nb = Tex("non-basic").scale(0.7).set_z_index(rect_large.get_z_index() + 1).set_opacity(0).move_to(nonbasic).align_to(nonbasic, UP)
        bb = Tex("basic").scale(0.7).set_z_index(rect_large.get_z_index() + 1).set_opacity(0).move_to(basic).align_to(nonbasic, UP)

        self.play(
            FadeIn(of_dot),
            FadeIn(of_arrow_shadow_2),
            MyFlash(of_dot, color=BLUE, z_index=of_dot.get_z_index() + 1),
        )

        self.play(
            Succession(
                Wait(0.5),  # hack since the next transform also makes var yellow
                AnimationGroup(
                    ineqs3[0][0:0+2].animate.set_color(YELLOW),
                    ineqs3[0][3:3+2].animate.set_color(YELLOW),
                    ineqs3[0][16:16+2].animate.set_color(YELLOW),
                    ineqs3[0][26:26+2].animate.set_color(YELLOW),
                    ineqs3[0][36:36+2].animate.set_color(YELLOW),
                    ineqs3[0][39:39+2].animate.set_color(YELLOW),
                    exp3[0][6:6+2].animate.set_color(YELLOW),
                    exp3[0][12:12+2].animate.set_color(YELLOW),
                    i1.animate.set_opacity(1),
                    i2.animate.set_opacity(1),
                ),
            ),
            AnimationGroup(
                # fadeouts
                AnimationGroup(
                    FadeOut(var3[0][:10]),
                    FadeOut(var3[0][12]),
                    FadeOut(var3[0][15]),
                    FadeOut(var3[0][18]),
                    FadeOut(var3[0][21]),
                    FadeOut(slack),
                ),
                # transforms
                AnimationGroup(
                    Transform(var3[0][10:10+2], nonbas_vars[0]),
                    Transform(var3[0][13:13+2], nonbas_vars[1]),
                    Transform(var3[0][16:16+2], bas_vars[0]),
                    Transform(var3[0][19:19+2], bas_vars[1]),
                    Transform(var3[0][22:22+2], bas_vars[2]),
                ),
                # fadeins
                AnimationGroup(
                    basic.animate.set_opacity(MED_OPACITY),
                    nonbasic.animate.set_opacity(MED_OPACITY),
                ),
                lag_ratio=0.5,
            ),
        )

        nb.set_opacity(MED_OPACITY)
        bb.set_opacity(MED_OPACITY)

        f = 0.3
        self.play(
            FadeIn(nb, shift=DOWN * f),
            FadeOut(nonbasic, shift=DOWN * f),
        )

        self.play(
            FadeIn(bb, shift=DOWN * f),
            FadeOut(basic, shift=DOWN * f),
        )

        self.play(
            FadeOut(nb, shift=UP * f),
            FadeIn(nonbasic, shift=UP * f),
            FadeOut(bb, shift=UP * f),
            FadeIn(basic, shift=UP * f),
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp3, ineqs3, bas_vars, nonbas_vars, rect_large, area, of_arrow_shadow, numberplane, sr, labels, sm,
                 basic, nonbasic, of_dot, of_arrow_shadow_2, i1, i2)

        self.play(
            AnimationGroup(
                FadeOut(ineqs3[0][:16]),
                ineqs3[0][16:].animate.move_to(ineqs3),
                lag_ratio=0.25,
            )
        )

        ineqs4 = ComplexTex(r"""$$\begin{aligned}
              s_1 &= 3\,000 - x_1 \\[-0.2em]
              s_2 &= 4\,000 \phantom{{} - x_1} - x_2 \\[-0.2em]
              s_3 &= 5\,000 - x_1 - x_2
                \end{aligned}$$""").move_to(ineqs3).align_to(ineqs3, DOWN)\
                        .set_z_index(ineqs3.get_z_index())

        ineqs4[0][0:0+2].set_color(ORANGE)
        ineqs4[0][10:10+2].set_color(ORANGE)
        ineqs4[0][20:20+2].set_color(ORANGE)

        ineqs4[0][8:8+2].set_color(YELLOW)
        ineqs4[0][18:18+2].set_color(YELLOW)
        ineqs4[0][28:28+2].set_color(YELLOW)
        ineqs4[0][31:31+2].set_color(YELLOW)

        self.play(
            AnimationGroup(
                # fadeouts
                AnimationGroup(
                    #+
                    FadeOut(ineqs3[0][18]),
                    FadeOut(ineqs3[0][28]),
                    FadeOut(ineqs3[0][41]),
                ),
                # transforms
                AnimationGroup(
                    #s_123
                    Transform(ineqs3[0][19:19+2+5], ineqs4[0][0:0+2+5]),
                    Transform(ineqs3[0][29:29+2+5], ineqs4[0][10:10+2+5]),
                    Transform(ineqs3[0][42:42+2+5], ineqs4[0][20:20+2+5]),
                    Transform(ineqs3[0][16:16+2], ineqs4[0][8:8+2]),
                    Transform(ineqs3[0][26:26+2], ineqs4[0][18:18+2]),
                    Transform(ineqs3[0][36:36+5], ineqs4[0][28:28+5]),
                ),
                # fadeins
                AnimationGroup(
                    FadeIn(ineqs4[0][7]),
                    FadeIn(ineqs4[0][17]),
                    FadeIn(ineqs4[0][27]),
                ),
                lag_ratio=0.5,
            ),
            run_time=2,
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp3, ineqs4, bas_vars, nonbas_vars, rect_large, area, of_arrow_shadow, numberplane, sr, labels, sm,
                 basic, nonbasic, of_dot, of_arrow_shadow_2, i1, i2)

        hl = CreateHighlight(
            VGroup(
                ineqs4[0][0],
                ineqs4[0][-12],
            ),
        ).set_color(BLUE)

        hlother = CreateHighlight(bas_vars).set_color(BLUE)

        self.play(
            FadeIn(hl, hlother),
        )

        a.next_to(nonbas_vars[0], DOWN, buff=0.1)
        b.next_to(nonbas_vars[1], DOWN, buff=0.1)

        hl1 = CreateHighlight(VGroup(nonbas_vars[0], a)).set_color(BLUE)
        hl2 = CreateHighlight(VGroup(nonbas_vars[1], b)).set_color(BLUE)
        hlof = CreateHighlight(exp3[0][3:3+11]).set_color(BLUE)
        zero = Tex("$$0$$").set_z_index(exp3.get_z_index()).move_to(exp3[0][3:3+11])

        self.play(
            AnimationGroup(
                AnimationGroup(
                    #FadeIn(a, b, zero),
                    FadeOut(hlother),
                    FadeIn(zero),
                    nonbas_vars[0].animate.set_opacity(BIG_OPACITY),
                    nonbas_vars[1].animate.set_opacity(BIG_OPACITY),
                    exp3[0][3:3+11].animate.set_opacity(BIG_OPACITY / 2),
                    exp3[0][8].animate.set_opacity(0),
                    ineqs4[0][7:7+3].animate.set_opacity(BIG_OPACITY),
                    ineqs4[0][17:17+3].animate.set_opacity(BIG_OPACITY),
                    ineqs4[0][27:27+3].animate.set_opacity(BIG_OPACITY),
                    ineqs4[0][30:30+3].animate.set_opacity(BIG_OPACITY),
                ),
                AnimationGroup(
                    #FadeIn(hl1, hl2, hlof),
                    FadeIn(hlof),
                    Transform(hl, CreateHighlight(
                        VGroup(
                            ineqs4[0][0],
                            ineqs4[0][3],
                            ineqs4[0][-7],
                            ineqs4[0][-12],
                        ),
                    ).set_color(BLUE)),
                ),
                lag_ratio=0,
            ),
        )

        self.play(
            #FadeOut(a, b, hl1, hl2, hlof, zero, hl),
            FadeOut(hlof, hl, zero),
            exp3[0][3:3+11].animate.set_opacity(1),
            ineqs4[0][7:7+3].animate.set_opacity(1),
            ineqs4[0][17:17+3].animate.set_opacity(1),
            ineqs4[0][27:27+3].animate.set_opacity(1),
            ineqs4[0][30:30+3].animate.set_opacity(1),
            nonbas_vars[0].animate.set_opacity(1),
            nonbas_vars[1].animate.set_opacity(1),
        )

        dpivot = Tex(r"\textit{Dantzig's pivot rule}").set_width(sm[0].get_width()).next_to(sm, DOWN, buff=0).set_z_index(10000000000)
        self.play(
            AnimationGroup(
                Transform(sm[1], CreateSR(VGroup(sm[0], dpivot), buff=0.17)),
                FadeIn(dpivot),
                lag_ratio=0.5,
            ),
        )

        hl1 = CreateHighlight(exp3[0][3:3+5]).set_color(GREEN)
        hl2 = CreateHighlight(exp3[0][9:9+5]).set_color(GREEN)

        # hackkk
        offset = -0.05

        dashed_x = Arrow(
            of_dot.get_center(),
            [of_arrow_shadow_2.get_end()[0] - offset, of_dot.get_center()[1], 0],
            stroke_width=LINE_STROKE + 0.01,
            buff=0,
        ).set_color(GREEN).set_z_index(of_arrow_shadow.get_z_index() - 0.001)

        dashed_y = Arrow(
            of_dot.get_center(),
            [of_dot.get_center()[0], of_arrow_shadow_2.get_end()[1] - offset, 0],
            buff=0,
            stroke_width=LINE_STROKE + 0.01,
        ).set_color(GREEN).set_z_index(of_arrow_shadow.get_z_index() - 0.001)

        a = of_arrow_shadow_2.copy().set_z_index(of_arrow_shadow.get_z_index() - 0.001)
        b = of_arrow_shadow_2.copy().set_z_index(of_arrow_shadow.get_z_index() - 0.001)

        self.play(
            FadeIn(hl1),
            FadeIn(hl2),
        )

        self.play(
            Transform(a, dashed_x),
            Transform(b, dashed_y),
            run_time=1,
        )

        self.remove(a, b)
        self.add(dashed_x, dashed_y)

        self.play(
            FadeOut(dashed_x),
            FadeOut(hl1),
        )

        b = VGroup(nonbas_vars[1].copy(), bas_vars[0].copy(), bas_vars[1].copy(), bas_vars[2].copy())
        b.arrange(buff=vars_buff)
        b.move_to(bas_vars)
        b[0].set_color(WHITE)

        nb = VGroup(nonbas_vars[0].copy())
        nb.move_to(nonbas_vars)

        downshift = 1

        self.play(
            AnimationGroup(
                FadeOut(dashed_y, shift=UP + DOWN * downshift),
                of_dot.animate.shift(UP + DOWN * downshift),
                of_arrow_shadow_2.animate.shift(UP + DOWN * downshift).set_opacity(1),
                i2.animate.set_opacity(0).shift(DOWN * downshift),

                of_arrow_shadow.animate.shift(DOWN * downshift),
                labels[0].animate.shift(DOWN * downshift),
                numberplane.animate.shift(DOWN * downshift),
                area.animate.shift(DOWN * downshift),

                FadeOut(hl2),
                Transform(nonbas_vars[0], nb[0]),
                Transform(nonbas_vars[1], b[0]),
                Transform(bas_vars[0], b[1]),
                Transform(bas_vars[1], b[2]),
                Transform(bas_vars[2], b[3]),
                ineqs4[0][18:18+2].animate.set_color(WHITE),
                ineqs4[0][31:31+2].animate.set_color(WHITE),
                exp3[0][-2:].animate.set_color(WHITE),
            ),
        )

        self.remove(nonbas_vars[0], nonbas_vars[1])
        self.remove(bas_vars[0], bas_vars[1], bas_vars[2])
        self.add(b, nb)
        nonbas_vars = nb
        bas_vars = b

        POSSIBLE_COLOR = GRAY

        i3.set_color(POSSIBLE_COLOR).shift(DOWN * downshift)
        i5.set_color(POSSIBLE_COLOR).shift(DOWN * downshift)

        inter = intersection(
            line(i3.line.get_start(), i3.line.get_end()),
            line(i1.line.get_start(), i1.line.get_end()),
        )

        idot = area.dots[0].copy().move_to([*inter, 0])

        inter = intersection(
            line(i5.line.get_start(), i5.line.get_end()),
            line(i1.line.get_start(), i1.line.get_end()),
        )

        idot_correct = area.dots[0].copy().move_to([*inter, 0]).set_z_index(area.dots[0].get_z_index() + 1)

        hls2 = CreateHighlight(ineqs4[0][10:10+2]).set_color(POSSIBLE_COLOR)
        hls3 = CreateHighlight(ineqs4[0][20:20+2]).set_color(POSSIBLE_COLOR)
        hl1 = CreateHighlight(ineqs4[0][13:13+4]).set_color(POSSIBLE_COLOR)
        hl2 = CreateHighlight(ineqs4[0][17:17+3]).set_color(POSSIBLE_COLOR)
        hl3 = CreateHighlight(ineqs4[0][23:23+4]).set_color(POSSIBLE_COLOR)
        hl4 = CreateHighlight(ineqs4[0][30:30+3]).set_color(POSSIBLE_COLOR)

        self.play(
            AnimationGroup(
                FadeIn(hl2),
                FadeIn(hl4),
                lag_ratio=0.07,
            )
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    ineqs4[0][10:10+2].animate.set_color(POSSIBLE_COLOR),
                    bas_vars[2].animate.set_color(POSSIBLE_COLOR),
                    i3.animate.set_opacity(1),
                    FadeIn(hls2),
                ),
                AnimationGroup(
                    ineqs4[0][20:20+2].animate.set_color(POSSIBLE_COLOR),
                    bas_vars[3].animate.set_color(POSSIBLE_COLOR),
                    i5.animate.set_opacity(1),
                    FadeIn(idot, hls3),
                ),
                lag_ratio=0.07,
            ),
        )

        self.add(idot_correct)

        G = VGroup(
            i5, i3, i1,
            labels[0],
            area, numberplane, of_arrow_shadow, of_dot, of_arrow_shadow_2,
            idot,
            idot_correct,
        )

        G.save_state()
        labels[1].save_state()

        # UP * 2 to scale from the very top of the screen
        self.play(
            G.animate.scale(1.75, about_point=(idot_correct.get_center() + UP * 3)).shift(RIGHT * 0.8),
            labels[1].animate.scale(1.75, about_point=(idot_correct.get_center() + UP * 3)).shift(RIGHT * 0.8),
        )

        self.play(
            ineqs4[0][10:10+2].animate.set_color(GREEN),
            bas_vars[2].animate.set_color(GREEN),
            i5.line.animate.set_color(GREEN).set_stroke_width(LINE_STROKE + 3),
            hls2.animate.set_color(GREEN),
            idot_correct.animate.set_color(GREEN),
            hl2.animate.set_color(GREEN),
            ineqs4[0][20:20+2].animate.set_color(RED),
            bas_vars[3].animate.set_color(RED),
            i3.line.animate.set_color(RED).set_stroke_width(LINE_STROKE + 3),
            hls3.animate.set_color(RED),
            idot.animate.set_color(RED),
            hl4.animate.set_color(RED),
        )

        correct = Tex("valid", color=GREEN).scale(0.85).set_z_index(idot.get_z_index()).next_to(idot_correct, LEFT + UP, buff=0.1)
        oob = Tex("out of bounds", color=RED).scale(0.85).set_z_index(idot.get_z_index()).next_to(idot, RIGHT + UP, buff=0.1)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    MyFlash(idot_correct, color=GREEN, z_index=idot_correct.get_z_index() + 1),
                    FadeIn(correct),
                ),
                AnimationGroup(
                    MyFlash(idot, color=RED, z_index=idot_correct.get_z_index() + 1),
                    FadeIn(oob),
                ),
                lag_ratio=0.75,
            ),
        )

        # self.play(
        #     idot_correct.animate(rate_func=there_and_back).scale(THERE_AND_BACK_SCALE),
        #     correct.animate(rate_func=there_and_back).scale(THERE_AND_BACK_SCALE),
        #     i5.line.animate(rate_func=there_and_back).set_stroke_width(LINE_STROKE + 6),
        # )

        self.play(
            FadeOut(correct),
            FadeOut(oob),
        )

        self.play(
            G.animate.restore(),
            labels[1].animate.restore(),
            ineqs4[0][10:10+2].animate.set_color(POSSIBLE_COLOR),
            ineqs4[0][20:20+2].animate.set_color(POSSIBLE_COLOR),
            bas_vars[2].animate.set_color(POSSIBLE_COLOR),
            bas_vars[3].animate.set_color(POSSIBLE_COLOR),
            hls2.animate.set_color(POSSIBLE_COLOR),
            hls3.animate.set_color(POSSIBLE_COLOR),
            hl2.animate.set_color(POSSIBLE_COLOR),
            hl4.animate.set_color(POSSIBLE_COLOR),
        )

        t1 = Tex("${} - 1\,000$").set_z_index(ineqs4.get_z_index() + 1)
        t1[0][1:].set_color(BLUE)
        align_object_by_coords(t1, t1[0][0].get_center(), ineqs4[0][17].get_center())
        t2 = Tex("${} - 1\,000$").set_z_index(ineqs4.get_z_index() + 1)
        t2[0][1:].set_color(BLUE)
        align_object_by_coords(t2, t2[0][0].get_center(), ineqs4[0][30].get_center())
        #hlt1 = CreateHighlight(t1).set_color(POSSIBLE_COLOR)
        #hlt2 = CreateHighlight(t2).set_color(POSSIBLE_COLOR)

        tmp1 = of_dot.copy()
        tmp2 = of_dot.copy()

        ineqs4[0][18:18+2].set_opacity(0),
        ineqs4[0][31:38+2].set_opacity(0),

        a = ineqs4[0][18:18+2].copy().set_opacity(1)
        b = ineqs4[0][31:38+2].copy().set_opacity(1)

        a.save_state()
        b.save_state()

        #brace = BraceBetweenPoints(
        #    Point().align_to(VGroup(t1, t2), UP + RIGHT).get_center(),
        #    Point().align_to(VGroup(t1, t2), DOWN + RIGHT).get_center(),
        #    RIGHT,
        #).set_z_index(ineqs4.get_z_index() + 1)

        #c = a.copy().next_to(brace, RIGHT)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(hl2),
                    FadeOut(hl4),
                ),
                AnimationGroup(
                    Transform(tmp1, t1[0][1:]),
                    Transform(tmp2, t2[0][1:]),
                    a.animate.next_to(t1, RIGHT + DOWN, buff=0.015).shift(UP * 0.13).set_opacity(0.4).scale(0.7),
                    b.animate.next_to(t2, RIGHT + DOWN, buff=0.015).shift(UP * 0.13).set_opacity(0.4).scale(0.7),
                ),
                lag_ratio=0.5,
            ),
        )

        self.remove(tmp1, tmp2)
        self.add(t1, t2)
        ineqs4[0][17].set_opacity(0)
        ineqs4[0][30].set_opacity(0)

        def tupdater(obj, dt):
            val = round((of_dot.get_center() - of_arrow_shadow.get_start())[1] * 1000)

            tt1 = Tex("${} - " + str(val)[0] + "\," + str(val)[1:] + "$").set_z_index(ineqs4.get_z_index() + 1)
            tt1[0][1:].set_color(BLUE)
            align_object_by_coords(tt1, tt1[0][0].get_center(), ineqs4[0][17].get_center())

            obj.become(tt1)

        def tupdater2(obj, dt):
            val = round((of_dot.get_center() - of_arrow_shadow.get_start())[1] * 1000)

            tt1 = Tex("${} - " + str(val)[0] + "\," + str(val)[1:] + "$").set_z_index(ineqs4.get_z_index() + 1)
            tt1[0][1:].set_color(BLUE)
            align_object_by_coords(tt1, tt1[0][0].get_center(), ineqs4[0][30].get_center())

            obj.become(tt1)

        t1.add_updater(tupdater)
        t2.add_updater(tupdater2)

        downshift = 1.5

        self.play(
            of_dot.animate.shift(UP * (3 - downshift)),
            of_arrow_shadow_2.animate.shift(UP * (3 - downshift)),
            VGroup(
                i3, i5, of_arrow_shadow, area, numberplane, labels[0],
                idot, idot_correct,
            ).animate.shift(DOWN * downshift),
            run_time=3,
        )

        t1.remove_updater(tupdater)
        t2.remove_updater(tupdater2)
        tupdater(t1, 0)
        tupdater2(t2, 0)
        self.remove(idot_correct)

        hlll = CreateHighlight(VGroup(ineqs4[0][13:13+4], t1)).set_color(YELLOW)

        self.play(
            bas_vars[2].animate.set_color(YELLOW),
            ineqs4[0][10:10+2].animate.set_color(YELLOW),
            ineqs4[0][20:20+2].animate.set_color(ORANGE),
            i5.animate.set_color(YELLOW),
            FadeIn(hlll),
            FadeOut(i3, idot),
            FadeOut(hls2, hls3),
        )

        t1.add_updater(tupdater)
        t2.add_updater(tupdater2)

        self.play(
            of_dot.animate.shift(UP * 0.5).set_color(RED),
            of_arrow_shadow_2.animate.shift(UP * 0.5).set_color(RED),
            hlll.animate.set_color(RED),
            run_time=1,
        )

        hls2.set_color(RED)

        self.play(
            FadeIn(hls2),
        )

        self.play(
            of_dot.animate.shift(DOWN * 0.5).set_color(BLUE),
            of_arrow_shadow_2.animate.shift(DOWN * 0.5).set_color(BLUE),
            hlll.animate.set_color(YELLOW),
            FadeOut(hls2),
            run_time=1,
        )

        hls2.set_color(POSSIBLE_COLOR)

        t1.remove_updater(tupdater)
        t2.remove_updater(tupdater2)

        self.play(
            bas_vars[2].animate.set_color(POSSIBLE_COLOR),
            ineqs4[0][10:10+2].animate.set_color(POSSIBLE_COLOR),
            ineqs4[0][20:20+2].animate.set_color(POSSIBLE_COLOR),
            i5.animate.set_color(POSSIBLE_COLOR),
            FadeOut(hlll),
            FadeIn(i3, idot),
            FadeIn(hls2, hls3),
            FadeOut(t1[0][1:]),
            FadeOut(t2[0][1:]),
            Succession(
                Wait(0.5),
                AnimationGroup(
                    AnimationGroup(
                        Transform(a, ineqs4[0][18:18+2].copy().set_opacity(1)),
                        Transform(b, ineqs4[0][31:31+2].copy().set_opacity(1)),
                    ),
                    AnimationGroup(
                        FadeIn(hl2),
                        FadeIn(hl4),
                    ),
                    lag_ratio=0.5,
                ),
            ),
        )

        self.remove(t1, t2)

        ineqs4[0][17:17+1].set_opacity(1)
        ineqs4[0][30:30+1].set_opacity(1)

        ineqs4[0][18:18+2].set_opacity(1)
        ineqs4[0][31:31+2].set_opacity(1)
        self.remove(a, b)

        four = Tex("$-4\,000$").move_to(hl1).align_to(ineqs4, RIGHT).shift(RIGHT * 0.5).set_z_index(ineqs4.get_z_index() + 1)
        five = Tex("$-5\,000$").move_to(hl3).align_to(ineqs4, RIGHT).shift(RIGHT * 0.5).set_z_index(ineqs4.get_z_index() + 1)

        ff = VGroup(four, five).scale(0.9).arrange(RIGHT, buff=0.6).next_to(ineqs4, UP, buff=0.5)
        gt = Tex("$>$", stroke_width=1.5).scale(0.5).move_to(VGroup(four, five)).set_z_index(ineqs4.get_z_index() + 1)

        a = ineqs4[0][13:13+4].copy()
        b = ineqs4[0][23:23+4].copy()
        am = ineqs4[0][17:17+1].copy()
        bm = ineqs4[0][30:30+1].copy()
        ah = CreateHighlight(four).set_color(POSSIBLE_COLOR)
        bh = CreateHighlight(five).set_color(POSSIBLE_COLOR)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Transform(a, four[0][1:]),
                    Transform(am, four[0][0]),
                    FadeIn(ah),
                ),
                AnimationGroup(
                    Transform(b, five[0][1:]),
                    Transform(bm, five[0][0]),
                    FadeIn(bh),
                ),
                lag_ratio=0.25,
            ),
        )

        self.remove(a, am, b, bm)
        self.add(four, five)

        self.play(
            FadeIn(gt),
            ah.animate.set_color(GREEN),
            bh.animate.set_color(RED),

            # NOTE: copy-pasted from the zoomin
            ineqs4[0][10:10+2].animate.set_color(GREEN),
            bas_vars[2].animate.set_color(GREEN),
            i5.line.animate.set_color(GREEN),
            hls2.animate.set_color(GREEN),
            hl2.animate.set_color(GREEN),
            ineqs4[0][20:20+2].animate.set_color(RED),
            bas_vars[3].animate.set_color(RED),
            i3.line.animate.set_color(RED),
            hls3.animate.set_color(RED),
            idot.animate.set_color(RED),
            hl4.animate.set_color(RED),
        )

        nb = VGroup(nonbas_vars[0].copy(), bas_vars[2].copy().set_color(YELLOW))
        nb.arrange(buff=vars_buff)
        nb.move_to(nonbas_vars)

        b = VGroup(bas_vars[0].copy(), bas_vars[1].copy(), bas_vars[3].copy().set_color(ORANGE))
        b.arrange(buff=vars_buff)
        b.move_to(bas_vars)

        self.play(
            FadeOut(five, bh, hl4, hls3),
            FadeOut(i3),
            FadeOut(gt),
            FadeOut(idot),
            ineqs4[0][20:20+2].animate.set_color(ORANGE),
        )

        self.play(
            Transform(nonbas_vars[0], nb[0]),
            Transform(bas_vars[2], nb[1]),
            Transform(bas_vars[0], b[0]),
            Transform(bas_vars[1], b[1]),
            Transform(bas_vars[3], b[2]),
            ineqs4[0][10:10+2].animate.set_color(YELLOW),
            FadeOut(four, ah, hl2, hls2),
            i5.animate.set_color(YELLOW),
        )

        hlp1 = CreateHighlight(ineqs4[0][10:10+2]).set_color(POSSIBLE_COLOR).set_color(RED)
        hlp2 = hl2.set_color(RED)
        hlp3 = hl4.set_color(RED)
        hlp4 = CreateHighlight(exp3[0][-5:]).set_color(POSSIBLE_COLOR).set_color(RED)

        t1 = Tex("tight").scale(0.6).next_to(hlp1, LEFT).set_z_index(hlp1.get_z_index()).set_color(RED)
        l1 = Tex("loose").scale(0.6).next_to(hlp2, RIGHT).set_z_index(hlp2.get_z_index()).set_color(RED)
        l2 = Tex("loose").scale(0.6).next_to(hlp3, RIGHT).set_z_index(hlp3.get_z_index()).set_color(RED)
        l3 = Tex("loose").scale(0.6).next_to(hlp4, RIGHT).set_z_index(hlp4.get_z_index()).set_color(RED)

        self.play(
            FadeIn(hlp1, hlp2, hlp3, hlp4),
            FadeIn(t1, shift=LEFT * 0.25),
            FadeIn(l1, shift=RIGHT * 0.25),
            FadeIn(l2, shift=RIGHT * 0.25),
            FadeIn(l3, shift=RIGHT * 0.25),
        )

        ineqs5 = ComplexTex(r"""$$\begin{aligned}
              s_1 &= 3\,000 - x_1 \\[-0.2em]
              x_2 &= 4\,000 \phantom{{} - x_1} - s_2 \\[-0.2em]
              s_3 &= 5\,000 - x_1 - (4\,000 - s_2)
                \end{aligned}$$""").set_z_index(ineqs4.get_z_index())

        align_object_by_coords(
            ineqs5,
            ineqs5[0][0].get_center(),
            ineqs4[0][0].get_center(),
        )

        ineqs5[0][0:0+2].set_color(ORANGE)
        ineqs5[0][20:20+2].set_color(ORANGE)
        ineqs5[0][8:8+2].set_color(YELLOW)
        ineqs5[0][18:18+2].set_color(YELLOW)
        ineqs5[0][28:28+2].set_color(YELLOW)
        ineqs5[0][37:37+2].set_color(YELLOW)

        ineqs6 = ComplexTex(r"""$$\begin{aligned}
              s_1 &= 3\,000 - x_1 \\[-0.2em]
              x_2 &= 4\,000 \phantom{{} - x_1} - s_2 \\[-0.2em]
              s_3 &= 1\,000 - x_1 + s_2
                \end{aligned}$$""").set_z_index(ineqs4.get_z_index())

        align_object_by_coords(
            ineqs6,
            ineqs6[0][0].get_center(),
            ineqs4[0][0].get_center(),
        )

        ineqs6[0][0:0+2].set_color(ORANGE)
        ineqs6[0][20:20+2].set_color(ORANGE)
        ineqs6[0][8:8+2].set_color(YELLOW)
        ineqs6[0][18:18+2].set_color(YELLOW)
        ineqs6[0][28:28+2].set_color(YELLOW)
        ineqs6[0][31:31+2].set_color(YELLOW)

        self.play(
            AnimationGroup(
                FadeOut(hlp1, hlp2),
                FadeOut(t1, l1),
                AnimationGroup(
                    ineqs4[0][18:18+2].animate.move_to(ineqs5[0][10:10+2]),
                    ineqs4[0][10:10+2].animate.move_to(ineqs5[0][18:18+2]),
                ),
                lag_ratio=0.5,
            ),
        )

        exp4 = Tex(r"$$\max\ " + str(OF_INITIAL[0]) + r"x_1 + " + str(OF_INITIAL[1]) + r" (4\,000 - s_2)$$").set_z_index(exp3.get_z_index())
        exp4[0][6:6+2].set_color(YELLOW)
        align_object_by_coords(
            exp4,
            exp4[0][0].get_center(),
            exp3[0][0].get_center(),
        )
        exp4[0][18:18+2].set_color(YELLOW)

        exp5 = Tex(r"$$\max\ " + str(OF_INITIAL[0]) + r"x_1 - " + str(OF_INITIAL[1]) + r" s_2 + 6\,800$$").set_z_index(exp3.get_z_index())
        exp5[0][6:6+2].set_color(YELLOW)
        exp5[0][12:12+2].set_color(YELLOW)
        exp5.move_to(exp3)
        exp5.shift(UP * (exp3[0][0].get_center() - exp5[0][0].get_center())[1])

        offset = RIGHT * 0.65

        self.play(
            AnimationGroup(
                AnimationGroup(
                    AnimationGroup(
                        FadeOut(hlp3),
                        FadeOut(l2),
                        FadeOut(ineqs4[0][31:31+2]),
                    ),
                    AnimationGroup(
                        Transform(ineqs4[0][13:13+5].copy(), ineqs5[0][32:32+5]),
                        Transform(ineqs4[0][10:10+2].copy(), ineqs5[0][37:37+2]),
                        rect_large.animate.shift(offset),
                        Group(
                            area,
                            of_arrow_shadow,
                            numberplane,
                            sr,
                            labels[1],
                            of_dot,
                            of_arrow_shadow_2,
                            i1,
                        ).animate.shift(offset/2),
                        Group(sm, dpivot).animate.shift(offset/4),
                    ),
                    AnimationGroup(
                        FadeIn(ineqs5[0][31]),
                        FadeIn(ineqs5[0][39]),
                    ),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    AnimationGroup(
                        FadeOut(hlp4),
                        FadeOut(l3),
                        FadeOut(exp3[0][-2:]),
                    ),
                    AnimationGroup(
                        Transform(ineqs4[0][13:13+5].copy(), exp4[0][13:13+5]),
                        Transform(ineqs4[0][10:10+2].copy(), exp4[0][18:18+2]),
                    ),
                    AnimationGroup(
                        FadeIn(exp4[0][12]),
                        FadeIn(exp4[0][20]),
                    ),
                    lag_ratio=0.5,
                ),
                lag_ratio=0.5,
            ),
        )

        nonbas_vars = nb
        bas_vars = b
        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp4, ineqs5, bas_vars, nonbas_vars, rect_large, area, of_arrow_shadow, numberplane, sr, labels, sm,
                 basic, nonbasic, of_dot, of_arrow_shadow_2, i1, i5, dpivot)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    AnimationGroup(
                        FadeOut(ineqs5[0][30]),
                        FadeOut(ineqs5[0][31]),
                        FadeOut(ineqs5[0][39]),
                    ),
                    AnimationGroup(
                        Transform(ineqs5[0][36:36+3], ineqs6[0][30:30+3]),
                        AnimationGroup(
                            ineqs5[0][32:32+4].animate.move_to(ineqs6[0][23:23+4]).set_opacity(0),
                            Transform(ineqs5[0][23], ineqs6[0][23]),
                            lag_ratio=0.1,
                        ),
                    ),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    AnimationGroup(
                        FadeOut(exp4[0][12]),
                        FadeOut(exp4[0][20]),
                        FadeOut(exp4[0][8]),
                    ),
                    AnimationGroup(
                        Transform(exp4[0][17], exp5[0][8]),
                        Transform(exp4[0][18:18+2], exp5[0][12:12+2]),
                        FadeTransform(exp4[0][13:13+4], exp5[0][15:15+4]),
                        Transform(exp4[0][9:9+3], exp5[0][9:9+3]),
                        Transform(exp4[0][:8], exp5[0][:8]),
                        rect_large.animate.shift(-offset),
                        Group(
                            area,
                            of_arrow_shadow,
                            numberplane,
                            sr,
                            labels[1],
                            of_dot,
                            of_arrow_shadow_2,
                            i1,
                            trace,
                        ).animate.shift(offset/2 * (-1)),
                        Group(sm, dpivot).animate.shift(-offset/4),
                    ),
                    AnimationGroup(
                        FadeIn(exp5[0][14]),
                    ),
                    lag_ratio=0.5,
                ),
                lag_ratio=0.5,
            ),
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp5, ineqs6, bas_vars, nonbas_vars, rect_large, area, of_arrow_shadow, numberplane, sr, labels, sm,
                 basic, nonbasic, of_dot, of_arrow_shadow_2, i1, i5, dpivot)

        hl1 = CreateHighlight(
            VGroup(
                ineqs6[0][0],
                ineqs6[0][3],
                ineqs6[0][10],
                ineqs6[0][21],
                ineqs6[0][26],
            ),
        ).set_color(BLUE)

        hl2 = CreateHighlight(exp5[0][-4:]).set_color(BLUE)

        self.play(
            FadeIn(hl1, hl2),
            ineqs6[0][7:7+3].animate.set_opacity(BIG_OPACITY),
            ineqs6[0][17:17+3].animate.set_opacity(BIG_OPACITY),
            ineqs6[0][27:27+6].animate.set_opacity(BIG_OPACITY),
            exp5[0][3:3+12].animate.set_opacity(BIG_OPACITY),
            nonbas_vars.animate.set_opacity(BIG_OPACITY),
        )

        self.play(
            VGroup(exp5[0][-4:], hl2).animate(rate_func=there_and_back)\
                    .scale(THERE_AND_BACK_SCALE),
        )

        self.play(
            FadeOut(hl1, hl2),
            ineqs6[0][7:7+3].animate.set_opacity(1),
            ineqs6[0][17:17+3].animate.set_opacity(1),
            ineqs6[0][27:27+6].animate.set_opacity(1),
            exp5[0][3:3+12].animate.set_opacity(1),
            nonbas_vars.animate.set_opacity(1),
        )

        hl1 = CreateHighlight(exp5[0][3:3+5]).set_color(GREEN)
        hl2 = CreateHighlight(exp5[0][9:9+5]).set_color(RED)

        # NOTE: next pivot starts here

        # 0 23 58 lines
        steps = ComplexTex(r"""\begin{enumerate}
                \setlength{\itemsep}{4pt}
                \setlength{\parskip}{0pt}
                \item \textbf{loosen variable} (Dantzig's rule)
                \item \textbf{tighten variable} (largest non-positive ratio)
                \item \textbf{fix equalities} (swap + substitute)
                \end{enumerate}""")

        rect_down = rect_large.copy()\
                    .move_to(ORIGIN)\
                    .rotate(PI / 2).align_to(ORIGIN, UP).shift(DOWN + RIGHT * 3.5)\
                    .set_z_index(rect_large.get_z_index() - 0.0001).shift(DOWN * 0.7)

        of_arrow_shadow.set_z_index(rect_down.get_z_index() - 0.00001)

        g = VGroup(of_dot, of_arrow_shadow_2, i1, i5, area, numberplane, of_arrow_shadow)

        rect_down.save_state()
        rect_down.align_to(Dot().next_to(self.camera.frame, DOWN), UP)
        self.add(rect_down)

        self.play(
            rect_down.animate.restore(),
            g.animate.shift(UP * 0.5),
        )

        VGroup(i2, i3, i4).shift(UP * 0.5)

        steps = ComplexTex(r"""\begin{enumerate}
                \setlength{\itemsep}{4pt}
                \setlength{\parskip}{0pt}
                \item \textbf{loosen} (Dantzig's rule)
                \item \textbf{tighten} (largest non-positive ratio)
                \item \textbf{fix} (swap + substitute)
                \end{enumerate}""").scale(0.65).set_z_index(rect_down.get_z_index() + 1)

        steps.next_to(rect_large, RIGHT, buff=0.5).align_to(rect_down, UP).shift(DOWN * 0.5)

        self.play(FadeIn(steps[0][:23]))
        self.play(FadeIn(steps[0][23:58]))
        self.play(FadeIn(steps[0][58:]))

        # hackkk
        offset = -0.05

        dashed_x = Arrow(
            of_dot.get_center(),
            [of_arrow_shadow_2.get_end()[0] - offset, of_dot.get_center()[1], 0],
            stroke_width=LINE_STROKE + 0.01,
            buff=0,
        ).set_color(GREEN).set_z_index(of_dot.get_z_index() - 0.000001)

        dashed_y = Arrow(
            of_dot.get_center(),
            [of_dot.get_center()[0], of_arrow_shadow_2.get_end()[1] - offset, 0],
            buff=0,
            stroke_width=LINE_STROKE + 0.01,
        ).set_color(RED).set_z_index(of_dot.get_z_index() - 0.000001)

        a = of_arrow_shadow_2.copy().set_z_index(of_dot.get_z_index() - 0.000001)
        b = of_arrow_shadow_2.copy().set_z_index(of_dot.get_z_index() - 0.000001)

        self.play(
            steps[0][23:58].animate.set_opacity(BIG_OPACITY),
            steps[0][58:].animate.set_opacity(BIG_OPACITY),
        )

        self.play(
            FadeIn(hl1),
            FadeIn(hl2),
        )

        self.play(
            Transform(a, dashed_x),
            Transform(b, dashed_y),
            run_time=1,
        )

        self.remove(a, b)
        self.add(dashed_x, dashed_y)

        self.play(
            FadeOut(dashed_y),
            FadeOut(hl2),
        )

        nb = VGroup(nonbas_vars[1].copy())
        nb.move_to(nonbas_vars)

        b = VGroup(nonbas_vars[0].copy().set_color(WHITE), bas_vars[0].copy(), bas_vars[1].copy(), bas_vars[2].copy())
        b.arrange(buff=vars_buff)
        b.move_to(bas_vars)
        b[0].set_color(WHITE)

        self.play(
            Transform(nonbas_vars[0], b[0]),
            Transform(nonbas_vars[1], nb[0]),
            Transform(bas_vars[0], b[1]),
            Transform(bas_vars[1], b[2]),
            Transform(bas_vars[2], b[3]),

            ineqs6[0][8:8+2].animate.set_color(WHITE),
            ineqs6[0][28:28+2].animate.set_color(WHITE),
            i1.animate.set_opacity(0),
            of_dot.animate.shift(RIGHT * 0.5),
            of_arrow_shadow_2.animate.shift(RIGHT * 0.5),
            FadeOut(dashed_x, shift=RIGHT * 0.5),
            FadeOut(hl1),
            exp5[0][6:6+2].animate.set_color(WHITE),
        )

        self.remove(nonbas_vars[0], nonbas_vars[1])
        self.remove(bas_vars[0], bas_vars[1], bas_vars[2])
        self.add(b, nb)
        nonbas_vars = nb
        bas_vars = b

        i3.set_color(POSSIBLE_COLOR).set_opacity(0)
        i4.set_color(POSSIBLE_COLOR).set_opacity(0)

        inter = intersection(
            line(i5.line.get_start(), i5.line.get_end()),
            line(i4.line.get_start(), i4.line.get_end()),
        )

        idot = area.dots[0].copy().move_to([*inter, 0])

        hls1 = CreateHighlight(ineqs6[0][0:0+2]).set_color(POSSIBLE_COLOR)
        hls3 = CreateHighlight(ineqs6[0][20:20+2]).set_color(POSSIBLE_COLOR)
        hl1 = CreateHighlight(ineqs6[0][3:3+4]).set_color(POSSIBLE_COLOR)
        hl2 = CreateHighlight(ineqs6[0][7:7+3]).set_color(POSSIBLE_COLOR)
        hl3 = CreateHighlight(ineqs6[0][23:23+4]).set_color(POSSIBLE_COLOR)
        hl4 = CreateHighlight(ineqs6[0][27:27+3]).set_color(POSSIBLE_COLOR)

        self.play(
            steps[0][:23].animate.set_opacity(BIG_OPACITY),
            steps[0][23:58].animate.set_opacity(1),
            steps[0][58:].animate.set_opacity(BIG_OPACITY),
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeIn(hl2),
                    ineqs6[0][0:0+2].animate.set_color(POSSIBLE_COLOR),
                    bas_vars[2].animate.set_color(POSSIBLE_COLOR),
                    i4.animate.set_opacity(1),
                    FadeIn(hls1, idot),
                ),
                AnimationGroup(
                FadeIn(hl4),
                    ineqs6[0][20:20+2].animate.set_color(POSSIBLE_COLOR),
                    bas_vars[3].animate.set_color(POSSIBLE_COLOR),
                    i3.animate.set_opacity(1),
                    FadeIn(hls3),
                ),
                lag_ratio=0.07,
            ),
        )

        four = Tex("$-3\,000$").move_to(hl1).align_to(ineqs6, RIGHT).shift(RIGHT * 0.5).set_z_index(ineqs6.get_z_index() + 1)
        five = Tex("$-1\,000$").move_to(hl3).align_to(ineqs6, RIGHT).shift(RIGHT * 0.5).set_z_index(ineqs6.get_z_index() + 1)

        ff = VGroup(four, five).scale(0.9).arrange(RIGHT, buff=0.6).next_to(ineqs6, UP, buff=0.5)
        gt = Tex("$<$", stroke_width=1.5).scale(0.5).move_to(VGroup(four, five)).set_z_index(ineqs6.get_z_index() + 1)

        a = ineqs6[0][3:3+4].copy()
        b = ineqs6[0][23:23+4].copy()
        am = ineqs6[0][7:7+1].copy()
        bm = ineqs6[0][27:27+1].copy()
        ah = CreateHighlight(four).set_color(POSSIBLE_COLOR)
        bh = CreateHighlight(five).set_color(POSSIBLE_COLOR)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Transform(a, four[0][1:]),
                    Transform(am, four[0][0]),
                    FadeIn(ah),
                ),
                AnimationGroup(
                    Transform(b, five[0][1:]),
                    Transform(bm, five[0][0]),
                    FadeIn(bh),
                ),
                lag_ratio=0.25,
            ),
        )

        inter = intersection(
            line(i5.line.get_start(), i5.line.get_end()),
            line(i3.line.get_start(), i3.line.get_end()),
        )

        idot_correct = area.dots[0].copy().move_to([*inter, 0]).set_z_index(area.dots[0].get_z_index() + 1)
        self.add(idot_correct)

        self.remove(a, am, b, bm)
        self.add(four, five)

        self.play(
            FadeIn(gt),
            bh.animate.set_color(GREEN),
            ah.animate.set_color(RED),

            # NOTE: copy-pasted from the zoomin
            ineqs6[0][20:20+2].animate.set_color(GREEN),
            bas_vars[3].animate.set_color(GREEN),
            i3.line.animate.set_color(GREEN),
            hls3.animate.set_color(GREEN),
            idot_correct.animate.set_color(GREEN),
            hl4.animate.set_color(GREEN),
            ineqs6[0][0:0+2].animate.set_color(RED),
            bas_vars[2].animate.set_color(RED),
            i4.line.animate.set_color(RED),
            hls1.animate.set_color(RED),
            idot.animate.set_color(RED),
            hl2.animate.set_color(RED),
        )

        nb = VGroup(nonbas_vars[0].copy(), bas_vars[3].copy().set_color(YELLOW))
        nb.arrange(buff=vars_buff)
        nb.move_to(nonbas_vars)

        b = VGroup(bas_vars[0].copy(), bas_vars[1].copy(), bas_vars[2].copy().set_color(ORANGE))
        b.arrange(buff=vars_buff)
        b.move_to(bas_vars)

        self.play(
            FadeOut(four, ah, hl2, hls1),
            FadeOut(idot),
            FadeOut(i4),
            FadeOut(gt),
            ineqs6[0][0:0+2].animate.set_color(ORANGE),
            bas_vars[2].animate.set_color(ORANGE),
        )

        self.play(
            FadeOut(five, bh, hl4, hls3),
            ineqs6[0][20:20+2].animate.set_color(YELLOW),
            i3.animate.set_color(YELLOW),
            Transform(nonbas_vars[0], nb[0]),
            Transform(bas_vars[3], nb[1]),
            Transform(bas_vars[0], b[0]),
            Transform(bas_vars[1], b[1]),
            Transform(bas_vars[2], b[2]),
            of_dot.animate.shift(RIGHT * 0.5),
            of_arrow_shadow_2.animate.shift(RIGHT * 0.5),
        )

        nonbas_vars = nb
        bas_vars = b

        hlp1 = hls3.set_color(RED)
        hlp2 = hl2.set_color(RED)
        hlp3 = hl4.set_color(RED)
        hlp4 = CreateHighlight(exp5[0][3:3+5]).set_color(POSSIBLE_COLOR).set_color(RED)

        self.play(
            steps[0][:23].animate.set_opacity(BIG_OPACITY),
            steps[0][23:58].animate.set_opacity(BIG_OPACITY),
            steps[0][58:].animate.set_opacity(1),
        )

        self.play(
            FadeIn(hlp1, hlp2, hlp3, hlp4),
        )

        ineqs7 = ComplexTex(r"""$$\begin{aligned}
              s_1 &= 3\,000 - x_1 \\[-0.2em]
              x_2 &= 4\,000 \phantom{{} - s_1} - s_2 \\[-0.2em]
              x_1 &= 1\,000 - s_3 + s_2
                \end{aligned}$$""").set_z_index(ineqs4.get_z_index())

        align_object_by_coords(
            ineqs7,
            ineqs7[0][0].get_center(),
            ineqs6[0][0].get_center(),
        )

        ineqs7[0][0:0+2].set_color(ORANGE)
        ineqs7[0][8:8+2].set_color(WHITE)
        ineqs7[0][18:18+2].set_color(YELLOW)
        ineqs7[0][20:20+2].set_color(WHITE)
        ineqs7[0][28:28+2].set_color(YELLOW)
        ineqs7[0][31:31+2].set_color(YELLOW)

        self.play(
            AnimationGroup(
                FadeOut(hlp1, hlp3),
                AnimationGroup(
                    ineqs6[0][20:20+2].animate.move_to(ineqs7[0][28:28+2]),
                    ineqs6[0][28:28+2].animate.move_to(ineqs7[0][20:20+2]),
                    ineqs6[0][30:].animate.move_to(ineqs7[0][30:]),
                    ineqs6[0][17:17+3].animate.move_to(ineqs7[0][17:17+3]),
                ),
                lag_ratio=0.5,
            ),
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp5, ineqs7, bas_vars, nonbas_vars, rect_large, rect_down, area, of_arrow_shadow, numberplane, sr, labels, sm,
                 basic, nonbasic, of_dot, of_arrow_shadow_2, i3, i5, dpivot, steps, hlp2, hlp4)

        ineqs8 = ComplexTex(r"""$$\begin{aligned}
              s_1 &= 2\,000 + s_3 - s_2 \\[-0.2em]
              x_2 &= 4\,000 \phantom{{} - s_1} - s_2 \\[-0.2em]
              x_1 &= 1\,000 - s_3 + s_2
                \end{aligned}$$""").set_z_index(ineqs4.get_z_index())

        align_object_by_coords(
            ineqs8,
            ineqs8[0][0].get_center(),
            ineqs7[0][0].get_center(),
        )

        ineqs8[0][0:0+2].set_color(ORANGE)
        ineqs8[0][8:8+2].set_color(YELLOW)
        ineqs8[0][11:11+2].set_color(YELLOW)
        ineqs8[0][21:21+2].set_color(YELLOW)
        ineqs8[0][31:31+2].set_color(YELLOW)
        ineqs8[0][34:34+2].set_color(YELLOW)

        exp6 = Tex(r"$$\max\ -1.2 s_3 - 0.5 s_2 + 8\,000$$").set_z_index(exp5.get_z_index())
        exp6[0][7:7+2].set_color(YELLOW)
        exp6[0][13:13+2].set_color(YELLOW)
        exp6.move_to(exp5)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    ineqs7[0][23:].copy().animate.align_to(ineqs7[0][3:9+1], DOWN).set_opacity(0),
                    Succession(
                        Wait(0.25),
                        AnimationGroup(
                            AnimationGroup(
                                FadeOut(ineqs7[0][3:9+1]),
                                FadeOut(hlp2),
                            ),
                            FadeIn(ineqs8[0][3:13]),
                            lag_ratio=0.2,
                            run_time=0.75,
                        ),
                    ),
                ),
                AnimationGroup(
                    ineqs7[0][23:].copy().animate.move_to(exp5[0][3:]).set_opacity(0),
                    Succession(
                        Wait(0.25),
                        AnimationGroup(
                            AnimationGroup(
                                FadeOut(exp5),
                                FadeOut(hlp4),
                            ),
                            FadeIn(exp6),
                            lag_ratio=0.2,
                            run_time=0.75,
                        ),
                    ),
                ),
                lag_ratio=0.75,
            ),
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp6, ineqs8, bas_vars, nonbas_vars, rect_large, rect_down, area, of_arrow_shadow, numberplane, sr, labels, sm,
                 basic, nonbasic, of_dot, of_arrow_shadow_2, i3, i5, dpivot, steps)

        self.play(
            steps[0][:23].animate.set_opacity(1),
            steps[0][23:58].animate.set_opacity(1),
            steps[0][58:].animate.set_opacity(1),
        )

        hl1 = CreateHighlight(exp6[0][4:4+5]).set_color(RED)
        hl2 = CreateHighlight(exp6[0][10:10+5]).align_to(hl1, DOWN).set_color(RED)

        self.play(
            FadeIn(hl1, hl2),
            steps[0][:23].animate.set_opacity(1),
            steps[0][23:58].animate.set_opacity(BIG_OPACITY),
            steps[0][58:].animate.set_opacity(BIG_OPACITY),
        )

        self.play(
            FadeOut(hl1, hl2),
            steps[0][:23].animate.set_opacity(1),
            steps[0][23:58].animate.set_opacity(1),
            steps[0][58:].animate.set_opacity(1),
        )

        hl1 = CreateHighlight(VGroup(ineqs8[0][0], ineqs8[0][6], ineqs8[0][23], ineqs8[0][24])).set_color(BLUE)
        hl2 = CreateHighlight(exp6[0][-4:]).set_color(BLUE)

        hltg = VGroup(ineqs8[0][13:13+7], ineqs8[0][23:23+7])
        hlt = CreateHighlight(hltg).set_color(BLUE)

        self.play(
            FadeIn(hl1, hl2),
            nonbas_vars.animate.set_opacity(BIG_OPACITY),

            ineqs8[0][7:7+6].animate.set_opacity(BIG_OPACITY),
            ineqs8[0][20:20+3].animate.set_opacity(BIG_OPACITY),
            ineqs8[0][30:30+6].animate.set_opacity(BIG_OPACITY),
            exp6[0][3:3+13].animate.set_opacity(BIG_OPACITY),
        )

        self.play(
            VGroup(exp6[0][-4:], hl2).animate(rate_func=there_and_back)\
                    .scale(THERE_AND_BACK_SCALE),
        )

        self.play(
            ineqs8[0][:7].animate.set_opacity(BIG_OPACITY),
            Transform(hl1, hlt),
        )

        self.play(
            VGroup(hltg, hl1).animate(rate_func=there_and_back)\
                    .scale(THERE_AND_BACK_SCALE),
        )

        self.play(
            FadeOut(hl1, hl2),
            nonbas_vars.animate.set_opacity(1),

            ineqs8[0][7:7+6].animate.set_opacity(1),
            ineqs8[0][20:20+3].animate.set_opacity(1),
            ineqs8[0][30:30+6].animate.set_opacity(1),
            exp6[0][3:3+13].animate.set_opacity(1),
        )

        # NOTE: this is correct
        self.next_section()

        a_surprise_weapon_that_will_help_us_later.move_to(VGroup(ineqs8, exp6, nonbas_vars, bas_vars, of3, nonbasic, basic))
        ineqs_base, exp_base, var_base, of_base = a_surprise_weapon_that_will_help_us_later

        labels[0].shift(UP * 0.5)
        labels[0].set_z_index(rect_down.get_z_index() - 0.0001)

        self.play(
            Succession(
                Wait(0.25),
                AnimationGroup(
                    FadeIn(ineqs_base, exp_base, var_base, of_base, shift=UP * self.camera.frame.height),
                    FadeOut(ineqs8, exp6, nonbas_vars, bas_vars, of3, nonbasic, basic, shift=UP * self.camera.frame.height),
                    run_time=1.5,
                ),
            ),
            Succession(
                Wait(0.25),
                rect_down.animate.align_to(Dot().next_to(self.camera.frame, DOWN), UP),
                run_time=1.5,
            ),
            Succession(
                Wait(0.25),
                VGroup(sm, dpivot).animate.align_to(Dot().next_to(self.camera.frame, UP), DOWN).set_opacity(0),
                run_time=1.5,
            ),
            Succession(
                Wait(0.25),
                VGroup(numberplane, of_dot, of_arrow_shadow_2, i3, i5, of_arrow_shadow, area, labels[0]).animate.shift(UP),
                run_time=1.5,
            ),
            AnimationGroup(
                FadeOut(steps[0][:23], run_time=0.5),
                FadeOut(steps[0][23:58], run_time=0.5),
                FadeOut(steps[0][58:], run_time=0.5),
                lag_ratio=0.2,
                run_time=1,
            )
        )

        hl1 = CreateHighlight(ineqs_base[0][7:])
        hlq = Tex("$\le\ ?$").set_z_index(ineqs_base.get_z_index()).next_to(exp_base, RIGHT, buff=0.3).align_to(exp_base[0][-6], DOWN).shift(DOWN * 0.03)
        hl2 = CreateHighlight(VGroup(exp_base[0][3:], hlq))

        self.play(FadeIn(hl1))
        self.play(FadeIn(hl2), FadeIn(hlq))

        self.play(FadeOut(hl1, hl2, hlq))

        a = Tex(r"$1.2\ \times$").set_z_index(ineqs_base.get_z_index()).set_color(BLUE).next_to(ineqs_base[0][7], LEFT).align_to(ineqs_base[0][7], DOWN)
        b = Tex(r"$1.7\ \times$").set_z_index(ineqs_base.get_z_index()).set_color(BLUE).next_to(ineqs_base[0][14], LEFT).align_to(ineqs_base[0][14], DOWN).align_to(a, RIGHT)

        self.play(FadeIn(a, shift=0.2 * LEFT))
        self.play(FadeIn(b, shift=0.2 * LEFT))

        an = Tex("$3\,600$").set_color(BLUE).set_z_index(ineqs_base.get_z_index()).move_to(ineqs_base[0][10:10+4])
        bn = Tex("$6\,800$").set_color(BLUE).set_z_index(ineqs_base.get_z_index()).move_to(ineqs_base[0][17:17+4])

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(a[0][-1]),
                    FadeOut(b[0][-1]),
                ),
                AnimationGroup(
                    a[0][:3].animate.next_to(ineqs_base[0][7], LEFT, buff=0.09).align_to(ineqs_base[0][7], DOWN),
                    b[0][:3].animate.next_to(ineqs_base[0][14], LEFT, buff=0.09).align_to(ineqs_base[0][14], DOWN),
                    ineqs_base[0][7:21].animate.set_color(BLUE),
                    ineqs_base[0][10:10+4].animate.set_opacity(0),
                    ineqs_base[0][17:17+4].animate.set_opacity(0),
                    FadeIn(an),
                    FadeIn(bn),
                ),
                lag_ratio=0.5,
            ),
        )

        t = Tex("${} \le 10\,400$").set_z_index(ineqs_base.get_z_index()).next_to(exp_base, RIGHT, buff=0.3).align_to(exp_base[0][-6], DOWN).shift(DOWN * 0.03).set_color(BLUE)

        expcp = exp_base.copy()
        VGroup(expcp, t).move_to(exp_base)

        expcp[0][3:3+5].set_color(BLUE)
        expcp[0][9:9+5].set_color(BLUE)

        exp_base.save_state()

        self.play(
            Transform(exp_base, expcp),
            Succession(
                Wait(0.25),
                AnimationGroup(
                    Addd(an, t),
                    Addd(bn, t),
                ),
            ),
            Succession(
                Wait(0.5),
                FadeIn(t),
            )
        )

        self.play(
            FadeOut(a[0][:3]),
            FadeOut(b[0][:3]),
            ineqs_base[0][10:10+4].animate.set_opacity(1).set_color(WHITE),
            ineqs_base[0][17:17+4].animate.set_opacity(1).set_color(WHITE),
            ineqs_base[0][7:10].animate.set_color(WHITE),
            ineqs_base[0][14:17].animate.set_color(WHITE),
            FadeOut(an),
            FadeOut(bn),
        )

        # NOTE: copy paste go brrrrrrrrrrrr
        a = Tex(r"$0.2\ \times$").set_z_index(ineqs_base.get_z_index()).set_color(BLUE).next_to(ineqs_base[0][7], LEFT).align_to(ineqs_base[0][7], DOWN)
        b = Tex(r"$0.7\ \times$").set_z_index(ineqs_base.get_z_index()).set_color(BLUE).next_to(ineqs_base[0][14], LEFT).align_to(ineqs_base[0][14], DOWN).align_to(a, RIGHT)
        c = Tex(r"$1.0\ \times$").set_z_index(ineqs_base.get_z_index()).set_color(BLUE).next_to(ineqs_base[0][21], LEFT).align_to(ineqs_base[0][21], DOWN).align_to(b, RIGHT)

        self.play(FadeIn(a, shift=0.2 * LEFT))
        self.play(FadeIn(b, shift=0.2 * LEFT))
        self.play(FadeIn(c, shift=0.2 * LEFT))

        an = Tex("$0\,600$").set_color(BLUE).set_z_index(ineqs_base.get_z_index()).move_to(ineqs_base[0][10:10+4])
        an[0][0].set_opacity(0)
        bn = Tex("$2\,800$").set_color(BLUE).set_z_index(ineqs_base.get_z_index()).move_to(ineqs_base[0][17:17+4])
        cn = Tex("$5\,000$").set_color(BLUE).set_z_index(ineqs_base.get_z_index()).move_to(ineqs_base[0][27:27+4])

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(a[0][-1]),
                    FadeOut(b[0][-1]),
                    FadeOut(c),
                ),
                AnimationGroup(
                    a[0][:3].animate.next_to(ineqs_base[0][7], LEFT, buff=0.09).align_to(ineqs_base[0][7], DOWN),
                    b[0][:3].animate.next_to(ineqs_base[0][14], LEFT, buff=0.09).align_to(ineqs_base[0][14], DOWN),
                    ineqs_base[0][7:].animate.set_color(BLUE),
                    ineqs_base[0][10:10+4].animate.set_opacity(0),
                    ineqs_base[0][17:17+4].animate.set_opacity(0),
                    ineqs_base[0][27:27+4].animate.set_opacity(0),
                    FadeIn(an),
                    FadeIn(bn),
                    FadeIn(cn),
                ),
                lag_ratio=0.5,
            ),
        )

        t2 = Tex("${} \le 8\,400$").set_z_index(ineqs_base.get_z_index()).next_to(exp_base, RIGHT, buff=0.3).align_to(exp_base[0][-6], DOWN).shift(DOWN * 0.03).set_color(BLUE)

        self.play(
            Succession(
                Wait(0.25),
                AnimationGroup(
                    Addd(an, t2),
                    Addd(bn, t2),
                    Addd(cn, t2),
                ),
            ),
            Succession(
                Wait(0.5),
                AnimationGroup(
                    FadeOut(t[0][-5:]),
                    FadeIn(t2[0][-4:]),
                ),
            ),
        )

        #self.add(of3, exp6, ineqs8, bas_vars, nonbas_vars, rect_large, rect_down, area, of_arrow_shadow, numberplane, sr, labels, sm,
        #         basic, nonbasic, of_dot, of_arrow_shadow_2, i3, i5, dpivot, steps)

        vary = Tex("variables: $y_1, y_2, y_3$").move_to(var_base)
        vary.set_x(-vary.get_x())

        ineqsy = Tex(r"""$$\begin{aligned}
        y_1, y_2, y_3  &\ge 0 \\[0.3em]
              y_1 \phantom{{} + y_2} + y_3 &\ge 1.2 \\[-0.2em]
              \phantom{y_1 + {}} y_2 + y_3 &\ge 1.7
                \end{aligned}$$""").move_to(ineqs_base)
        ineqsy.set_x(-ineqsy.get_x()).align_to(ineqs_base, UP)

        ofy = of_base.copy()
        expy = Tex(r"$$\begin{aligned}\min\ 3\,000 & y_1 \\[-0.27em] {} + 4\,000 & y_2 \\[-0.27em] {} + 5\,000 & y_3\end{aligned}$$")

        VGroup(ofy, expy).arrange(DOWN, buff=0.15).move_to(of3).align_to(exp_base, DOWN)
        expy.set_x(-expy.get_x())
        ofy.set_x(-ofy.get_x())
        VGroup(ofy, expy).shift(DOWN * 0.45)

        spacing2 = rect_large.get_x() + rect_large.width / 2 - 0.04  # weeeeeeeee

        self.play(
            FadeOut(a[0][:3]),
            FadeOut(b[0][:3]),
            ineqs_base[0][10:10+4].animate.set_opacity(1).set_color(WHITE),
            ineqs_base[0][17:17+4].animate.set_opacity(1).set_color(WHITE),
            ineqs_base[0][27:27+4].animate.set_opacity(1).set_color(WHITE),
            ineqs_base[0][7:10].animate.set_color(WHITE),
            ineqs_base[0][14:17].animate.set_color(WHITE),
            ineqs_base[0][21:27].animate.set_color(WHITE),
            FadeOut(an),
            FadeOut(bn),
            FadeOut(cn),
            rect_large.animate.shift(LEFT * spacing2),
            FadeOut(area, of_arrow_shadow, numberplane, of_dot, of_arrow_shadow_2, i3, i5, labels, sr),
            FadeOut(t[0][:-5]),
            FadeOut(t2[0][-4:]),
            exp_base.animate.restore(),
        )

        a = Tex(r"$y_1\ \times$").set_z_index(ineqs_base.get_z_index()).set_color(BLUE).next_to(ineqs_base[0][7], LEFT).align_to(ineqs_base[0][8], DOWN).shift(DOWN * 0.05)
        b = Tex(r"$y_2\ \times$").set_z_index(ineqs_base.get_z_index()).set_color(BLUE).next_to(ineqs_base[0][14], LEFT).align_to(ineqs_base[0][15], DOWN).align_to(a, RIGHT).shift(DOWN * 0.05)
        c = Tex(r"$y_3\ \times$").set_z_index(ineqs_base.get_z_index()).set_color(BLUE).next_to(ineqs_base[0][21], LEFT).align_to(ineqs_base[0][22], DOWN).align_to(b, RIGHT).shift(DOWN * 0.05)

        self.play(
            AnimationGroup(
                FadeIn(a),
                FadeIn(b),
                FadeIn(c),
                lag_ratio=0.1,
            )
        )

        acp = a.copy().set_opacity(0.5)
        bcp = b.copy().set_opacity(0.5)
        ccp = c.copy().set_opacity(0.5)

        self.add(acp, bcp, ccp)

        vary[0][10:10+2].set_color(BLUE)
        vary[0][13:13+2].set_color(BLUE)
        vary[0][16:16+2].set_color(BLUE)

        ineqsy[0][0:0+2].set_color(BLUE)
        ineqsy[0][3:3+2].set_color(BLUE)
        ineqsy[0][6:6+2].set_color(BLUE)

        ineqsy[0][10:10+2].set_color(BLUE)
        ineqsy[0][13:13+2].set_color(BLUE)

        ineqsy[0][19:19+2].set_color(BLUE)
        ineqsy[0][22:22+2].set_color(BLUE)

        expy[0][7:7+2].set_color(BLUE)
        expy[0][14:14+2].set_color(BLUE)
        expy[0][21:21+2].set_color(BLUE)
        expy[0][14:14+2].set_color(BLUE)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(a[0][-1]),
                    FadeOut(b[0][-1]),
                    FadeOut(c[0][-1]),
                ),
                AnimationGroup(
                    Transform(a[0][:2], vary[0][10:10+2]),
                    Transform(b[0][:2], vary[0][13:13+2]),
                    Transform(c[0][:2], vary[0][16:16+2]),
                ),
                AnimationGroup(
                    FadeIn(vary[0][:10]),
                    FadeIn(vary[0][12]),
                    FadeIn(vary[0][15]),
                ),
                lag_ratio=0.5,
            ),
        )

        self.play(
            FadeIn(ineqsy[0][:10]),
        )

        hl1 = CreateHighlight(VGroup(ineqs_base[0][21:21+2], ineqs_base[0][7:7+2])).set_color(GRAY)
        hl3 = CreateHighlight(exp_base[0][3:3+5]).set_color(GRAY)

        self.play(
            FadeIn(hl1, hl3),
        )

        self.play(
            FadeIn(ineqsy[0][10:19]),
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Transform(hl1, CreateHighlight(VGroup(ineqs_base[0][24:24+2], ineqs_base[0][14:14+2])).set_color(GRAY)),
                    Transform(hl3, CreateHighlight(exp_base[0][9:9+5]).set_color(GRAY)),
                ),
                FadeIn(ineqsy[0][19:]),
                lag_ratio=0.5,
            ),
        )

        self.play(
            AnimationGroup(
                FadeOut(hl3),
                Transform(hl1, CreateHighlight(VGroup(ineqs_base[0][10:10+4], ineqs_base[0][17:17+4], ineqs_base[0][27:27+4])).set_color(GRAY)),
                FadeIn(expy, ofy),
                lag_ratio=0.5,
            ),
        )

        self.play(
            FadeOut(hl1, acp, bcp, ccp),
        )

        primal = VGroup(
            var_base,
            ineqs_base,
            exp_base,
        )

        dual = VGroup(
            vary,
            ineqsy,
            expy,
        )

        self.play(
            var_base[0][10:10+2].animate.set_color(ORANGE),
            var_base[0][13:13+2].animate.set_color(ORANGE),
            ineqs_base[0][0:0+2].animate.set_color(ORANGE),
            ineqs_base[0][3:3+2].animate.set_color(ORANGE),
            ineqs_base[0][7:7+2].animate.set_color(ORANGE),
            ineqs_base[0][14:14+2].animate.set_color(ORANGE),
            ineqs_base[0][21:21+2].animate.set_color(ORANGE),
            ineqs_base[0][24:24+2].animate.set_color(ORANGE),
            exp_base[0][6:6+2].animate.set_color(ORANGE),
            exp_base[0][12:12+2].animate.set_color(ORANGE),
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(primal, dual, of_base, ofy, rect_large)

        primal_text = Tex(r"\underline{Primal}").move_to(var_base).set_z_index(var_base.get_z_index()).set_color(ORANGE).scale(1.25)
        dual_text = Tex(r"\underline{Dual}").move_to(vary).set_z_index(var_base.get_z_index()).set_color(BLUE).scale(1.25)

        leq = SVGMobject("assets/leq.svg").set_width(0.8).set_z_index(100000000)
        eq = SVGMobject("assets/eq.svg").set_width(0.8).set_z_index(100000000)

        self.play(
            AnimationGroup(
                FadeOut(of_base, ofy),
                AnimationGroup(
                    primal.animate.arrange(DOWN, buff=0.7).move_to(primal).align_to(primal, UP).shift(DOWN * 1),
                    dual.animate.arrange(DOWN, buff=0.6).move_to(dual).align_to(dual, UP).shift(DOWN * 1),
                ),
                AnimationGroup(
                    Write(primal_text),
                    Write(dual_text),
                    run_time=1,
                ),
                lag_ratio=0.5,
            ),
        )

        self.play(
            FadeIn(leq),
        )

        wdt = Tex("Weak", "Duality", "Theorem").arrange(DOWN, buff=0.15).set_z_index(var_base.get_z_index())
        wdt[1].shift(DOWN * 0.04)
        wdt.add(CreateSR(wdt).set_opacity(1).scale(1.1))

        leqcp = leq.copy()
        VGroup(wdt, leqcp).arrange(DOWN,buff=0.35)

        self.play(
            Succession(
                Wait(0.5),
                FadeIn(wdt),
            ),
            Transform(leq, leqcp),
            VGroup(primal, primal_text).animate.shift(LEFT * 0.5),
            VGroup(dual, dual_text).animate.shift(RIGHT * 0.5),
        )

        eq.move_to(leq)

        strong = Tex("Strong").set_z_index(var_base.get_z_index()).move_to(wdt[0]).align_to(wdt[0], UP)

        self.play(
            Transform(leq, eq),
        )

        self.play(
            FadeOut(wdt[0], shift=RIGHT * 2),
            FadeIn(strong, shift=RIGHT * 2),
        )


class Farmer(MovingCameraScene):
    def construct(self):
        self.next_section(skip_animations=True)

        farm = ImageMobject("assets/midjourney/farm-12-16-out.png")\
                .set_height(self.camera.frame.get_height())\
                .align_to(self.camera.frame, LEFT).set_z_index(5)

        rect = ImageMobject("assets/midjourney/farm-12-16-rect.png")\
                .set_height(self.camera.frame.get_height())\
                .align_to(farm, RIGHT).set_z_index(6)

        rect_large = ImageMobject("assets/midjourney/farm-12-16-rect-large.png")

        rect_small = ImageMobject("assets/midjourney/farm-12-16-rect-small.png")\
                .set_height(self.camera.frame.get_height())\
                .align_to(farm, RIGHT).set_z_index(6)

        farm.save_state()
        rect.save_state()

        icon_scale = 1.65

        carrot = ImageMobject("assets/midjourney/carrot-cropped-flopped.png").set_height(0.45 * icon_scale)
        potato = ImageMobject("assets/midjourney/potato-cropped.png").set_height(0.3 * icon_scale)
        fertilizer = ImageMobject("assets/midjourney/fertilizer-cropped-flopped.png").set_height(0.3 * icon_scale)
        farmer = ImageMobject("assets/midjourney/farmer-outline.png").set_z_index(10).set_height(1.05)
        farmer_black = ImageMobject("assets/midjourney/farmer-black.png").set_z_index(9).set_height(1.05)

        self.add(rect, farm)

        fc = farm.copy()
        farm.move_to(Dot().next_to(self.camera.frame, LEFT))

        offset = 1


        # same as the next self.play
        rect_played = rect.copy().next_to(fc, RIGHT, buff=0).shift(LEFT * offset * 2)
        farm_played = farm.align_to(self.camera.frame, LEFT).shift(LEFT * offset)

        title = Tex(r"\underline{Farmer's Problem}").scale(1.5)

        goal = Tex("Goal: \it maximize profit").scale(1.25)

        points = VGroup(
            Tex(r"\begin{itemize} \item $3$ tons of potato seeds \end{itemize}"),
            Tex(r"\begin{itemize} \item $4$ tons of carrot seeds \end{itemize}"),
            Tex(r"\begin{itemize} \item $5$ tons of fertilizer (used 1:1) \end{itemize}"),
            Tex(r"\begin{itemize} \item " + str(OF_INITIAL[0]) + r"\$/kg for O, " + str(OF_INITIAL[1]) + r"\$/kg for O \end{itemize}"),
        )
        for i in range(3):
            align_object_by_coords(points[i + 1], points[i + 1][0][0], points[0][0][0])
            points[i + 1].shift(DOWN * 0.75 * (i + 1))

            if i == 2:
                points[i + 1].shift(DOWN * 0.3)

        guide = Dot().move_to(VGroup(Dot().align_to(rect_played, LEFT),
                                     Dot().align_to(self.camera.frame, RIGHT)))

        potato.next_to(points[0][0][-1], RIGHT)
        carrot.next_to(points[1][0][-1], RIGHT)
        fertilizer.next_to(points[2][0][-1], RIGHT)

        p2 = potato.copy().move_to(points[3][0][11])
        c2 = carrot.copy().move_to(points[3][0][-1]).shift(RIGHT * 0.1)
        points[3][0][11].scale(0.001).set_color(BLACK).set_opacity(0).set_z_index(-1)
        points[3][0][-1].scale(0.001).set_color(BLACK).set_opacity(0).set_z_index(-1)

        points[0][0][1].set_color(POTATO_COLOR)
        points[1][0][1].set_color(CARROT_COLOR)
        points[2][0][1].set_color(FERTILIZER_COLOR)
        points[0][0][8:13+1].set_color(POTATO_COLOR)
        points[1][0][8:13+1].set_color(CARROT_COLOR)
        points[2][0][8:17+1].set_color(FERTILIZER_COLOR)
        points[3][0][1:7+1].set_color(POTATO_COLOR)
        points[3][0][13:19+1].set_color(CARROT_COLOR)

        main_group = Group(Group(title, farmer).arrange(buff=0.4),
              Group(points, p2, c2, carrot, potato, fertilizer),
              goal,
              ).arrange(DOWN, buff=0.7).move_to(guide).set_z_index(10)

        title.set_z_index(7)

        farmer_copy = farmer.copy().move_to(title[0][0]).align_to(farmer, DOWN).set_opacity(0).set_z_index(1000)
        farmer_black.move_to(farmer).set_z_index(999)
        farmer_black_copy = farmer_black.copy().move_to(title[0][0]).align_to(farmer, DOWN).set_z_index(999)
        sr1 = SurroundingRectangle(title, color=BLACK, fill_opacity=1).set_z_index(8)
        sr2 = SurroundingRectangle(title, color=BLACK, fill_opacity=1).set_z_index(9)\
                .move_to(farmer_copy).align_to(Dot().move_to(farmer_copy), LEFT)

        self.add(sr1, title)

        self.play(
            rect.animate.next_to(fc, RIGHT, buff=0).shift(LEFT * offset * 2),
            farm.animate.align_to(self.camera.frame, LEFT).shift(LEFT * offset),
            ReplacementTransform(farmer_copy, farmer),
            ReplacementTransform(farmer_black_copy, farmer_black),
            FadeOut(sr1),
            sr2.animate.align_to(Dot().move_to(farmer), LEFT),
            run_time=2,
        )

        self.remove(farmer_black, sr2)

        self.play(
            AnimationGroup(
                Write(points[0], run_time=1.25),
                FadeIn(potato, shift=0.1 * RIGHT),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                Write(points[1], run_time=1.25),
                FadeIn(carrot, shift=0.1 * RIGHT),
                lag_ratio=0.5,
            )
        )

        self.play(
            Write(points[2][0][:17+1], run_time=1),
        )

        self.play(
            AnimationGroup(
                Write(points[2][0][17+1:], run_time=0.65),
                FadeIn(fertilizer, shift=0.1 * RIGHT),
                lag_ratio=0.3,
            )
        )

        self.play(
            AnimationGroup(
                Write(points[3][0][:12+1]),
                FadeIn(p2, run_time=0.5),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                Write(points[3][0][12+1:]),
                FadeIn(c2, run_time=0.5),
                lag_ratio=0.5,
            )
        )

        self.play(
            Write(goal[0][:5]), run_time=0.65,
        )

        self.play(
            Write(goal[0][5:]), run_time=1,
        )

        saved_x = main_group.animate.set_x(0),

        rect2 = rect_small.copy()\
                .flip().align_to(self.camera.frame, RIGHT)\
                .shift(RIGHT * 0.1)
        self.add(rect2)

        offset2 = 0.5

        equivalenece = SVGMobject("assets/iff.svg").set_height(0.6).set_z_index(10)
        equivalenece.move_to(Dot().align_to(self.camera.frame, RIGHT))

        equivalenece.set_opacity(0).shift(RIGHT * (0.65 - offset2))  # hack

        self.play(
            rect.animate.restore(),
            farm.animate.restore(),

            main_group.animate.set_x(-main_group.get_x() - offset2 / 2),
            rect2.animate.shift(LEFT * (main_group.get_x() * 2 + offset2)),
            equivalenece.animate.shift(LEFT * (main_group.get_x() * 2 + offset2)).set_opacity(1),
        )

        guide2 = Dot().move_to(VGroup(Dot().move_to(equivalenece),
                                     Dot().align_to(self.camera.frame, RIGHT)))

        var = ComplexTex("variables: $x_p, x_c$")
        var[0][-5:-3].set_color(POTATO_COLOR)
        var[0][-2:].set_color(CARROT_COLOR)

        ineqs = ComplexTex(r"""$$\begin{aligned}
        x_p, x_c  &\ge 0 \\[0.3em]
              x_p \phantom{{}+ x_c} &\le 3\,000 \\[-0.2em]
              x_c &\le 4\,000 \\[-0.2em]
              x_p + x_c &\le 5\,000
                \end{aligned}$$""")
        ineqs[0][0:2].set_color(POTATO_COLOR)
        ineqs[0][3:3+2].set_color(CARROT_COLOR)
        ineqs[0][7:7+2].set_color(POTATO_COLOR)
        ineqs[0][10].set_color(POTATO_COLOR)
        ineqs[0][11].set_color(POTATO_COLOR)
        ineqs[0][12].set_color(POTATO_COLOR)
        ineqs[0][13].set_color(POTATO_COLOR)
        ineqs[0][14:14+2].set_color(CARROT_COLOR)
        ineqs[0][17].set_color(CARROT_COLOR)
        ineqs[0][18].set_color(CARROT_COLOR)
        ineqs[0][19].set_color(CARROT_COLOR)
        ineqs[0][20].set_color(CARROT_COLOR)
        ineqs[0][21:21+2].set_color(POTATO_COLOR)
        ineqs[0][24:24+2].set_color(CARROT_COLOR)
        ineqs[0][27].set_color(FERTILIZER_COLOR)
        ineqs[0][28].set_color(FERTILIZER_COLOR)
        ineqs[0][29].set_color(FERTILIZER_COLOR)
        ineqs[0][30].set_color(FERTILIZER_COLOR)

        exp = ComplexTex(r"$$\max\ " + str(OF_INITIAL[0]) + r"x_p + " + str(OF_INITIAL[1]) + r" x_c$$")
        exp[0][3:3+5].set_color(POTATO_COLOR)
        exp[0][-5:].set_color(CARROT_COLOR)

        of = Tex(r"objective function").set_opacity(MED_OPACITY).scale(0.75)

        theory_group = Group(var, ineqs, exp).arrange(DOWN, buff=0.75).move_to(guide2).set_z_index(10)

        var.align_to(title, DOWN)
        exp.align_to(goal, UP)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    points[2].animate.set_opacity(BIG_OPACITY),
                    points[3].animate.set_opacity(BIG_OPACITY),
                    fertilizer.animate.set_opacity(BIG_OPACITY),
                    p2.animate.set_opacity(BIG_OPACITY),
                    c2.animate.set_opacity(BIG_OPACITY),
                    goal.animate.set_opacity(BIG_OPACITY),
                ),
                Write(var, run_time=1.25),
                lag_ratio=0.5,
            ),
        )

        self.play(
            Write(ineqs[0][:7]),
            run_time=1.25,
        )

        self.play(
            Write(ineqs[0][7:21]),
            run_time=1.5,
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    points[0].animate.set_opacity(BIG_OPACITY),
                    points[1].animate.set_opacity(BIG_OPACITY),
                    potato.animate.set_opacity(BIG_OPACITY),
                    carrot.animate.set_opacity(BIG_OPACITY),
                    points[2].animate.set_opacity(1),
                    fertilizer.animate.set_opacity(1),
                ),
                Write(ineqs[0][21:], run_time=1),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    points[2].animate.set_opacity(BIG_OPACITY),
                    fertilizer.animate.set_opacity(BIG_OPACITY),
                    points[3].animate.set_opacity(1),
                    p2.animate.set_opacity(1),
                    c2.animate.set_opacity(1),
                    goal.animate.set_opacity(1),
                ),
                Write(exp, run_time=1.5),
                lag_ratio=0.5,
            )
        )

        g = VGroup(
            exp.copy(),
            of,
        ).arrange(UP, buff=0.15).move_to(exp)

        self.play(
            Transform(exp, g[0]),
            FadeIn(of, shift=UP * 0.15)
        )

        self.play(
            points.animate.set_opacity(1),
            carrot.animate.set_opacity(1),
            potato.animate.set_opacity(1),
            fertilizer.animate.set_opacity(1),
        )

        theory_group.add(of)
        of.set_z_index(10)

        self.remove(rect, farm)

        rect3 = rect.copy()\
                .flip().align_to(self.camera.frame, RIGHT)\
                .set_z_index(rect2.get_z_index() - 1)\
                .shift(RIGHT * 0.1)
        self.add(rect3)

        guide3 = Dot().move_to(main_group)
        guide3.set_x(-guide3.get_x())

        numberplane = NumberPlane(
            x_range=(- 3 * 7.111111111111111, 3 * 7.111111111111111, 1),
            y_range=(- 3 * 4.0, 3 * 4.0, 1),
            stroke_width = 6,
            axis_config={
                "stroke_width": 4,
            },
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 3,
                "stroke_opacity": 0.6
            },
        )

        numberplane.background_lines.set_z_index(rect3.get_z_index() - 1 + 0.1)
        numberplane.axes.set_z_index(rect3.get_z_index() - 1 + 0.2)

        area = FeasibleArea2D(dots_z_index=rect3.get_z_index() - 1 + 0.99).set_z_index(rect3.get_z_index() - 1 + 0.4)

        i1 = Inequality2D(1, 0, ">=", 0).set_color(POTATO_COLOR).set_z_index(rect3.get_z_index() - 1 + 0.5)  # positive potatoes
        i2 = Inequality2D(0, 1, ">=", 0).set_color(CARROT_COLOR).set_z_index(rect3.get_z_index() - 1 + 0.5)  # positive carrots
        i3 = Inequality2D(1, 1, "<=", 5).set_color(FERTILIZER_COLOR).set_z_index(rect3.get_z_index() - 1 + 0.5)  # at most 5 kg fertilizer
        i4 = Inequality2D(1, 0, "<=", 3).set_color(POTATO_COLOR).set_z_index(rect3.get_z_index() - 1 + 0.5)  # at most 3kg potatoes
        i5 = Inequality2D(0, 1, "<=", 4).set_color(CARROT_COLOR).set_z_index(rect3.get_z_index() - 1 + 0.5)  # at most 3kg carrots

        i4_hp = i4.get_half_plane()

        area.add_inequalities([i1, i2, i3, i4, i5])

        #of_iq = AffineLine2D((1.9, 1.3)).set_color(BLUE).set_z_index(rect3.get_z_index() - 1 + 0.5)

        of_arrow = Arrow(start=ORIGIN, end=np.array((*OF_INITIAL, 0)), buff=0).set_z_index(area.dots_z_index - 0.01)
        of_arrow_shadow = of_arrow.copy().set_color(WHITE).set_z_index(of_arrow.get_z_index() - 0.000001)

        optimum = list(solve_farm(OF_INITIAL))
        optimum[0] /= 1000
        optimum[1] /= 1000

        sweep = AffineLine2D(OF_INITIAL).rotate(PI / 2)
        sweep.crop_to_screen(self.camera.frame)
        sweep.set_z_index(rect3.get_z_index() - 1 + 0.99).set_color(BLUE)

        # - hack after crop_to_screen
        sweep_goal = AffineLine2D(OF_INITIAL).rotate(-PI / 2).move_to([*optimum, 0])
        sweep_goal.set_z_index(rect3.get_z_index() - 1 + 0.99)

        sweep_angle = Angle(sweep.line, of_arrow, dot=True).set_z_index(99).set_color(BLUE)

        sweep.dots = VGroup()

        sweep.add(sweep.dots)

        sweep.lineextra = VGroup()
        sweep.add(sweep.lineextra)

        def sweep_updater(obj):
            dots = sweep.get_area_border_intersection(area)

            if len(dots) <= 1:
                return

            g = VGroup().set_z_index(100000)
            for i in range(len(dots)):
                for j in range(i + 1, len(dots)):
                    d1, d2 = dots[i], dots[j]

                    g.add(
                        Line(start=d1.get_center(),
                             end=d2.get_center(),
                             color=BLUE, stroke_width=LINE_STROKE + 2.5).set_z_index(100000)
                    )

            sweep.lineextra.become(g).set_z_index(100000)

            sweep.dots.become(dots).set_z_index(100000).set_color(BLUE)

        sweep_updater(None)

        sweep_dots_tmp = sweep.dots
        sweep.remove(sweep.dots)

        align_object_by_coords(
            VGroup(i1, i4_hp, i2, i3, i4, i5, area, numberplane, of_arrow, of_arrow_shadow, sweep, sweep_goal, sweep_angle, sweep_dots_tmp),
            area.dots.get_center(),
            guide3.get_center(),
        )

        i1.crop_to_screen(self.camera.frame)
        i2.crop_to_screen(self.camera.frame)
        i3.crop_to_screen(self.camera.frame)
        i4.crop_to_screen(self.camera.frame)
        i5.crop_to_screen(self.camera.frame)

        labels = VGroup(
            Tex("$x_p$").scale(1.2).move_to(numberplane)\
                    .next_to(numberplane.axes[0], DOWN, buff=0.33)\
                    .align_to(self.camera.frame, RIGHT).shift(LEFT * 0.2)\
                    .set_color(POTATO_COLOR),
            Tex("$x_c$").scale(1.2).move_to(numberplane)\
                    .next_to(numberplane.axes[1], LEFT, buff=0.23)\
                    .align_to(self.camera.frame, UP).shift(DOWN * 0.35)\
                    .set_color(CARROT_COLOR),
        ).set_z_index(i1.get_z_index() + 1)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    main_group.animate.shift(LEFT * theory_group.get_x() * 2),
                    rect2.animate.shift(LEFT * theory_group.get_x() * 2).set_opacity(0),
                    rect3.animate.shift(LEFT * theory_group.get_x() * 2).set_opacity(1),
                    var.animate.shift(LEFT * theory_group.get_x() * 2),
                    ineqs.animate.shift(LEFT * theory_group.get_x() * 2),
                    exp.animate.shift(LEFT * theory_group.get_x() * 2),
                    of.animate.shift(LEFT * theory_group.get_x() * 2),
                    #theory_group.animate.shift(LEFT * theory_group.get_x() * 2),
                    equivalenece.animate.shift(LEFT * theory_group.get_x() * 2).set_opacity(0),
                ),
                AnimationGroup(
                    FadeIn(numberplane.background_lines),
                    FadeIn(numberplane.axes),
                    #FadeIn(labels)
                ),
                lag_ratio=0.5,
            ),
        )

        labels_tmp = labels.copy()
        xptmp = var[0][10:10+2].copy()
        xctmp = var[0][13:13+2].copy()

        self.play(
            AnimationGroup(
                Transform(xptmp, labels_tmp[0]),
                Transform(xctmp, labels_tmp[1]),
                lag_ratio=0.25,
            )
        )

        self.remove(xptmp, xctmp)
        self.add(labels)

        sr = SurroundingRectangle(
            VGroup(
                Dot().align_to(self.camera.frame, UP + RIGHT),
                Dot().align_to(self.camera.frame, DOWN + RIGHT),
                Dot().align_to(rect3, RIGHT),
            ),
            fill_opacity=1,
        ).move_to(guide3).set_color_by_gradient((RED, GREEN)).set_opacity(0.35)
        sr.set_sheen_direction(unit_vector(OF_INITIAL[0] * RIGHT + OF_INITIAL[1] * UP))

        self.remove(main_group, rect2, equivalenece)

        big_hl = CreateHighlight(ineqs)
        hl = CreateHighlight(ineqs[0][7:7+7])

        self.play(
            exp.animate.set_opacity(BIG_OPACITY),
            of.animate.set_opacity(BIG_OPACITY),
            FadeIn(big_hl),
        )

        self.play(
            AnimationGroup(
                Transform(big_hl, hl),
                Create(i4),
                lag_ratio=0.5,
            ),
        )

        self.remove(big_hl)
        self.add(hl)

        self.play(FadeIn(i4_hp))

        self.play(
            AnimationGroup(
                FadeOut(hl),
                Create(i1),
                Create(i2),
                Create(i3),
                Create(i5),
                AnimationGroup(
                    FadeOut(i4_hp),
                    FadeIn(area),
                ),
                lag_ratio=0.25,
            ),
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(i1),
                    FadeOut(i2),
                    FadeOut(i3),
                    FadeOut(i4),
                    FadeOut(i5),
                ),
                lag_ratio=0.5,
            ),
        )

        self.play(area.area.animate(rate_func=there_and_back, run_time=1.25).set_fill(BLUE, 0.5))

        self.play(
            exp.animate.set_opacity(1),
            of.animate.set_opacity(MED_OPACITY),
            ineqs.animate.set_opacity(BIG_OPACITY),
        )

        self.add(sr)
        thingy = ImageMobject("assets/thingy.png")\
                .set_height(sr.get_height() * 2)\
                .move_to(sr).rotate(atan2(OF_INITIAL[1], OF_INITIAL[0]) - PI / 2)\
                .set_z_index(sr.get_z_index() + 0.1)

        self.play(
            AnimationGroup(
                # hack!
                thingy.animate(run_time=2).shift((OF_INITIAL[1] * UP + OF_INITIAL[0] * RIGHT) * 7),
                AnimationGroup(
                    Write(of_arrow),
                ),
                lag_ratio=0,
            )
        )

        self.remove(thingy)

        self.play(
            FadeIn(sweep),
            FadeIn(sweep_angle),
            FadeIn(sweep_dots_tmp),
            of_arrow.animate.set_color(BLUE),
        )

        sweep.add(sweep_dots_tmp)

        dl = DashedLine(ORIGIN - 0.0001, ORIGIN + 0.0001).set_z_index(of_arrow.get_z_index() - 0.00001).set_color(BLUE)

        def of_updater(obj):
            start = of_arrow.get_start()
            end = of_arrow.get_end()

            point = intersection(
                line(start, end),
                line(sweep.line.get_start(), sweep.line.get_end()),
            )

            new_point = np.array([*point, 0])

            of_arrow.put_start_and_end_on(
                new_point,
                new_point + np.array([*OF_INITIAL, 0])
            )

            sweep_angle.become(Angle(sweep.line, of_arrow, dot=True).set_color(BLUE).set_z_index(99))

        def dl_updater(obj):
            start = of_arrow_shadow.get_start()
            end = intersection(
                line(of_arrow_shadow.get_start(), of_arrow_shadow.get_end()),
                line(sweep.line.get_start(), sweep.line.get_end()),
            )
            end = np.array([*end, 0])

            l = 0.085
            lt = l * 2

            dist = distance(start, end)
            dist_rounded = int(dist / lt) * lt

            if abs(dist) < 0.001:
                return

            end_rounded = ((end - start) / dist) * dist_rounded + start + l / 10

            obj.become(DashedLine(end_rounded, start, dash_length=l, stroke_width=of_arrow.get_stroke_width() * 0.95)\
                    .set_color(BLUE)\
                    .set_z_index(of_arrow.get_z_index() - 0.0001))

        dl.add_updater(dl_updater)
        self.add(dl)

        # updaters are broken
        dummy = VMobject()
        dummy.add_updater(sweep_updater)
        dummy.add_updater(of_updater)
        self.add(dummy)

        self.camera.frame.save_state()
        theory_group.save_state()
        rect3.save_state()

        self.play(
            FadeIn(of_arrow_shadow),
            sweep.animate(run_time=3).move_to(sweep_goal),
        )

        self.remove(dummy)

        optimum = sweep.dots
        sweep.remove(sweep.dots)

        optimum_texts = VGroup(
            Tex(r"$1\,000\ \mathrm{kg}$").scale(0.8)\
                    .move_to(optimum).align_to(numberplane.axes[0], UP).shift(DOWN * 0.35)\
                    .set_z_index(100000),
            Tex(r"$4\,000\ \mathrm{kg}$").scale(0.8)\
                    .move_to(optimum).align_to(numberplane.axes[1], RIGHT).shift(LEFT * 0.35)\
                    .set_z_index(100000),
            Tex(r"$\$8\,000$").scale(0.8)\
                    .next_to(optimum, UP + RIGHT)\
                    .set_z_index(100000),
        )

        for i in range(3):
            optimum_texts[i].add(CreateSR(optimum_texts[i]))

        self.play(
            FadeIn(optimum_texts),
            FadeOut(sweep_angle),
            of_arrow.animate.set_opacity(0),
            ineqs.animate.set_opacity(1),
        )

        for i in [0, 1, 2]:
            self.play(
                optimum_texts[i].animate(rate_func=there_and_back).scale(THERE_AND_BACK_SCALE),
            )

        #vm = CreateMeaning(var, "$\mathbf{x} \in \mathbb{R}^{+}_{0}$")
        #vi = CreateMeaning(ineqs, r"$\begin{aligned}\mathbf{0} &\le \mathbf{x} \\[0.05em] A\mathbf{x} &\le \mathbf{b}\end{aligned}$")
        #vo = CreateMeaning(VGroup(of, exp), "$\max\ \mathbf{c}^T \mathbf{x}$")

        vm = CreateMeaning(var, "\small variables $\in \mathbb{R}^{+}_{0}$")
        vi = CreateMeaning(ineqs, r"\small s.t. linear \par inequalities")
        vo = CreateMeaning(VGroup(of, exp), "\small maximizing \par linear function")

        dl.remove_updater(dl_updater)
        self.play(
            FadeOut(optimum_texts),
            FadeOut(optimum),
            FadeOut(dl),
            FadeOut(sweep)
        )

        for o, rt in [(vm, 1.25), (vi, 1.5), (vo, 1.5)]:
            self.play(
                AnimationGroup(
                    FadeIn(o[0]),
                    Write(o[1], run_time=rt),
                    lag_ratio=0.5,
                )
            )

        print(numberplane.get_center())

        iextras = []
        ipts = [
            [np.array([0, 0]), np.array([1, -2]), 0.5, None],
            [np.array([0, 0]), np.array([1, -0.5]), 0.5, None],
            [np.array([3, 0]), np.array([4, 1]), 0.25, None],
            [np.array([3, 2]), np.array([2, 3.5]), 0.25, "<="],
            [np.array([0, 4]), np.array([-1, 3.7]), 0.15, "<="],
            [np.array([0, 4]), np.array([-1, 3]), 0.15, "<="],
            [np.array([0, 4]), np.array([-1, 0]), 0.2, "<="],
            [np.array([1, 4]), np.array([0, 4.9]), 0.05, "<="],
        ]
        inorms = []

        start = of_arrow_shadow.get_start()

        for p1, p2, s, op in ipts:
            a, b, c = Inequality2D.points_to_slope(p1, p2)
            iq = Inequality2D(a, b, op or ">=", c).set_opacity(0).shift(of_arrow_shadow.get_start())
            iextras.append(iq)
            self.add(iq)
            area.add_inequalities([iq])
            d = p2 - p1
            inorms.append((-d[1], d[0], 0) / np.linalg.norm(d))

            ino = np.array((-d[1], d[0])) / np.linalg.norm(d)

        def ineqs_complex_updater(obj, dt):
            obj._update_area()

            best_score = float('inf')
            best_pos = None

            for d in obj.dots:
                score = d.get_center()[0] * OF_INITIAL[0] + d.get_center()[1] * OF_INITIAL[1]

                if score < best_score:
                    best_score = score
                    best_pos = d.get_center()

            of_arrow_shadow.put_start_and_end_on(
                best_pos,
                best_pos + of_arrow_shadow.get_end() - of_arrow_shadow.get_start()
            )

        self.add(area)
        area.add_updater(ineqs_complex_updater)

        self.play(
            *[iextras[i].animate.shift(inorms[i] * ipts[i][-2])
             for i in range(len(ipts))],
            vi[1].animate.scale(1.25),
        )

        # TODO: 3D stuff here

        self.play(
            *[iextras[i].animate.shift(-inorms[i] * ipts[i][-2] * 1.1)
             for i in range(len(ipts))],
            FadeOut(vm, vi, vo),
        )

        area.remove_updater(ineqs_complex_updater)
        area.remove_inequalities(iextras)

        def of_line_updater(obj):
            vector  = of_arrow_shadow.get_end() - of_arrow_shadow.get_start()
            x, y, _ = vector

            optimum = list(solve_farm([x, y]))
            optimum[0] /= 1000
            optimum[1] /= 1000

            sweep.line.become(AffineLine2D([x, y]).line.set_color(BLUE).rotate(PI / 2)\
                    .move_to(of_arrow_shadow.get_start()).shift([*optimum, 0])
            )

            op = "+" if y >= 0 else "-"

            new_exp = Tex(f"$$\max\ {x:.1f}x_p {op} {abs(y):.1f}x_c$$")\
                    .move_to(exp).align_to(exp, DOWN)
            new_exp[0][3:3+5].set_color(POTATO_COLOR)
            new_exp[0][9:9+5].set_color(CARROT_COLOR)

            exp.become(new_exp)

        sm = Tex(r"\underline{Simplex Method}").set_z_index(10000000000).scale(1)
        sm.add(CreateSR(sm, buff=0.17))
        sm.align_to(self.camera.frame, RIGHT + UP).shift((LEFT * 1.2 + DOWN) * 0.25)

        self.play(
            AnimationGroup(
                FadeIn(sm[1]),
                Write(sm[0]),
                lag_ratio=0.2,
            )
        )

        self.play(
            FadeIn(optimum),
            FadeIn(dl),
            FadeIn(sweep)
        )

        srcp = sr.copy()\
               .set_z_index(sr.get_z_index() + 0.2)

        thingy = ImageMobject("assets/thingy.png")\
                .set_height(sr.get_height() * 2)\
                .move_to(sr).rotate(atan2(OF_INITIAL[1], OF_INITIAL[0]) - PI / 2)\
                .set_z_index(sr.get_z_index() + 0.1)

        thingy2 = ImageMobject("assets/thingy.png")\
                .set_height(sr.get_height() * 2)\
                .move_to(sr).rotate(atan2(-OF_INITIAL[1], -OF_INITIAL[0]) - PI / 2)\
                .set_z_index(sr.get_z_index() + 0.1)
        thingy2.shift(-unit_vector(OF_INITIAL[1] * UP + OF_INITIAL[0] * RIGHT) * 18)

        self.add(thingy, thingy2, srcp)

        self.play(
            thingy.animate(run_time=2.5).shift((OF_INITIAL[1] * UP + OF_INITIAL[0] * RIGHT) * 9),
            thingy2.animate(run_time=2.5).shift((OF_INITIAL[1] * UP + OF_INITIAL[0] * RIGHT) * 9),
        )

        self.remove(thingy, thingy2, srcp)

        dl.add_updater(dl_updater)

        self.play(
            *[MyFlash(d, color=WHITE, z_index=d.get_z_index() + 1)
              for d in area.dots],
            MyFlash(optimum, color=BLUE, z_index=optimum.get_z_index() + 2),
        )

        def sr_updater(obj):
            vector  = of_arrow_shadow.get_end() - of_arrow_shadow.get_start()
            obj.set_sheen_direction(unit_vector(vector))

        sr.add_updater(sr_updater)

        dummy = VMobject()
        dummy.add_updater(sweep_updater)
        dummy.add_updater(of_line_updater)
        self.add(dummy)

        angle = atan2(OF_INITIAL[1], OF_INITIAL[0])

        self.play(
            Rotate(of_arrow_shadow, -angle, about_point=of_arrow_shadow.get_start()),
            run_time=2,
        )

        self.play(
            *[MyFlash(d, color=BLUE, z_index=d.get_z_index() + 1)
              for d in sweep.dots],
        )

        self.play(
            Rotate(of_arrow_shadow, +angle - 2 * PI, about_point=of_arrow_shadow.get_start()),
            run_time=5,
        )

        self.remove(dummy)
        sr.remove_updater(sr_updater)
        dl.remove_updater(dl_updater)
        self.play(
            FadeOut(optimum),
            FadeOut(dl),
            FadeOut(sweep)
        )

        fade_rect = get_fade_rect()

        of_arrow_shadow.set_z_index(fade_rect.get_z_index() - 0.00000000001)

        of_arrow_shadow_2 = of_arrow_shadow.copy().set_color(BLUE).set_z_index(fade_rect.get_z_index() + 1)
        of_dot = Dot().scale(OPTIMUM_DOT_SCALE).set_color(BLUE).move_to(of_arrow_shadow_2.get_start())\
                .set_z_index(of_arrow_shadow_2.get_z_index())

        trace = TracedPath(of_dot.get_center).set_color(BLUE).set_stroke_width(8)\
                .set_z_index(area.dots[0].get_z_index() - 0.00001)

        G = VGroup(
            area,
            of_arrow_shadow,
            numberplane,
            labels[0],
        )

        l0 = Line(
            start=of_dot.get_center(),
            end=of_dot.get_center(),
            color=trace.get_color(),
            stroke_width=trace.get_stroke_width(),
        ).set_z_index(trace.get_z_index())
        p0 = Tex("pivot \#1").scale(0.75).next_to(l0, DOWN).shift(RIGHT * 1.5).set_z_index(l0.get_z_index())

        sweep.move_to(of_arrow_shadow_2.get_start())
        sweep.remove(sweep.lineextra)
        self.play(
            #FadeIn(sweep),
            FadeIn(of_arrow_shadow_2),
            FadeIn(of_dot),
        )

        self.play(
            #VGroup(of_arrow_shadow_2, of_dot, sweep).animate.shift(RIGHT * 3),
            VGroup(of_arrow_shadow_2, of_dot).animate.shift(RIGHT * 3),
            l0.animate.become(Line(
                start=of_dot.get_center() + RIGHT * 3,
                end=of_dot.get_center(),
                color=trace.get_color(),
                stroke_width=trace.get_stroke_width(),
            ).set_z_index(trace.get_z_index())),
            FadeIn(p0, run_time=1),
            run_time=2,
        )

        l1 = Line(
            start=of_dot.get_center(),
            end=of_dot.get_center(),
            color=trace.get_color(),
            stroke_width=trace.get_stroke_width(),
        ).set_z_index(trace.get_z_index())
        us1 = 0.5
        p1 = Tex("pivot \#2").scale(0.75).next_to(l1, RIGHT).shift(UP * (1 - us1)).set_z_index(l1.get_z_index())

        self.play(
            l0.animate.shift(DOWN * us1),
            p0.animate.shift(DOWN * us1),
            l1.animate.become(Line(
                start=of_dot.get_center() + UP * (2 - us1),
                end=of_dot.get_center() + DOWN * us1,
                color=trace.get_color(),
                stroke_width=trace.get_stroke_width(),
            ).set_z_index(trace.get_z_index())),
            G.animate.shift(DOWN * us1),
            FadeIn(p1, shift=DOWN * us1, run_time=1),
            #VGroup(of_arrow_shadow_2, of_dot, sweep).animate.shift(UP * (2 - us1)),
            VGroup(of_arrow_shadow_2, of_dot).animate.shift(UP * (2 - us1)),
            run_time=1.5,
        )

        l2 = Line(
            start=of_dot.get_center(),
            end=of_dot.get_center(),
            color=trace.get_color(),
            stroke_width=trace.get_stroke_width(),
        ).set_z_index(trace.get_z_index())
        p2 = Tex("pivot \#3").scale(0.75).next_to(l2.get_center(), UP + RIGHT).shift(LEFT).set_z_index(l1.get_z_index())
        us2 = 1

        self.play(
            l2.animate.become(Line(
                start=of_dot.get_center() + UP * (2 - us2) + LEFT * 2,
                end=of_dot.get_center() + DOWN * us2,
                color=trace.get_color(),
                stroke_width=trace.get_stroke_width(),
            ).set_z_index(trace.get_z_index())),
            l0.animate.shift(DOWN * us2),
            l1.animate.shift(DOWN * us2),
            p0.animate.shift(DOWN * us2),
            p1.animate.shift(DOWN * us2),
            G.animate.shift(DOWN * us2),
            FadeIn(p2, shift=DOWN * us2, run_time=1),
            #VGroup(of_arrow_shadow_2, of_dot, sweep).animate.shift(UP * (2 - us2) + LEFT * 2),
            VGroup(of_arrow_shadow_2, of_dot).animate.shift(UP * (2 - us2) + LEFT * 2),
            run_time=1.5,
        )

        self.play(
            MyFlash(of_dot, color=BLUE, z_index=optimum.get_z_index() + 2),
        )

        self.play(
            VGroup(numberplane, of_arrow_shadow, area, labels[0]).animate.shift(UP * (us1 + us2)),
            #FadeOut(sweep, of_arrow_shadow_2, of_dot, l0, l1, l2, shift=UP * (us1 + us2)),
            #FadeOut(sweep, of_arrow_shadow_2, of_dot, l0, l1, l2, p0, p1, p2, shift=UP * (us1 + us2)),
            FadeOut(of_arrow_shadow_2, of_dot, l0, l1, l2, p0, p1, p2, shift=UP * (us1 + us2)),
        )

        # fix positions, will be used later
        VGroup(l0, l1, l2, p0, p1, p2).shift(UP * (us1 + us2))

        # NOTE: WE ARE ALL COPIED
        ineqs2 = Tex(r"""$$\begin{aligned}
        x_1, x_2  &\ge 0 \\[0.3em]
              x_1 \phantom{{}+ x_2} &\le 3\,000 \\[-0.2em]
              x_2 &\le 4\,000 \\[-0.2em]
              x_1 + x_2 &\le 5\,000
                \end{aligned}$$""").align_to(ineqs, UP + RIGHT)
        exp2 = Tex(r"$$\max\ " + str(OF_INITIAL[0]) + r"x_1 + " + str(OF_INITIAL[1]) + r" x_2$$").align_to(exp, UP + LEFT)
        var2 = Tex("variables: $x_1, x_2$").align_to(var, UP + LEFT)

        labels2 = VGroup(
            Tex("$x_1$").scale(1.2).move_to(numberplane)\
                    .next_to(numberplane.axes[0], DOWN, buff=0.33)\
                    .align_to(self.camera.frame, RIGHT).shift(LEFT * 0.2),
            Tex("$x_2$").scale(1.2).move_to(numberplane)\
                    .next_to(numberplane.axes[1], LEFT, buff=0.23)\
                    .align_to(self.camera.frame, UP).shift(DOWN * 0.35)
        ).set_z_index(i1.get_z_index() + 1)

        labels2[0].align_to(labels[0], UP + LEFT)
        labels2[1].align_to(labels[1], UP + LEFT)

        self.play(
            Transform(ineqs, ineqs2),
            Transform(exp, exp2),
            Transform(var, var2),
            Transform(labels, labels2),
        )

        # NOTE: I'm copy pasted!
        of_arrow_shadow_2 = of_arrow_shadow.copy().set_color(BLUE).set_z_index(fade_rect.get_z_index() + 1)
        of_dot = Dot().scale(OPTIMUM_DOT_SCALE).set_color(BLUE).move_to(of_arrow_shadow_2.get_start())\
                .set_z_index(of_arrow_shadow_2.get_z_index())

        hl = CreateHighlight(ineqs[0][:7])

        self.play(
            FadeIn(of_dot),
            FadeIn(of_arrow_shadow_2),
            MyFlash(of_dot, color=BLUE, z_index=of_dot.get_z_index() + 1),
        )

        i1.set_color(YELLOW).set_opacity(0)
        i2.set_color(YELLOW).set_opacity(0)
        i3.set_color(YELLOW).set_opacity(0)
        i4.set_color(YELLOW).set_opacity(0)
        i5.set_color(YELLOW).set_opacity(0)

        self.play(
            FadeIn(hl),
            i1.animate.set_opacity(1),
            i2.animate.set_opacity(1),
        )

        val = Tex(r"$(0, 0)$").scale(0.6)\
            .next_to(of_dot, UP)\
            .set_z_index(10000000000)
        val.add(CreateSR(val))

        def value_updater(obj, dt):
            c = of_dot.get_center() - of_arrow_shadow.get_start()

            x = int(round(c[0] * 1000))
            y = int(round(c[1] * 1000))

            def fmt(x):
                x = str(x)
                if len(x) == 4:
                    return f"{x[0]}\,{x[1:]}"
                return x

            val2 = Tex(rf"$({fmt(x)}, {fmt(y)})$").scale(0.6)\
                .next_to(of_dot, UP)\
                .set_z_index(10000000000)
            val2.add(CreateSR(val2))

            val.become(val2)

        hl2 = CreateHighlight(ineqs[0][7:14])

        self.play(
            FadeIn(val),
        )

        self.play(
            FadeIn(p0),
            MyFlash(of_dot.copy().shift(RIGHT * 3), color=WHITE, z_index=of_dot.get_z_index() + 1),
        )

        val.add_updater(value_updater)

        a_surprise_weapon_that_will_help_us_later = VGroup(
            ineqs.copy(),
            exp.copy(),
            var.copy(),
            of.copy(),
        )

        self.play(
            of_arrow_shadow_2.animate.shift(RIGHT * 1.5),
            of_dot.animate.shift(RIGHT * 1.5),
            Transform(hl, CreateHighlight(ineqs[0][3:7])),
            i1.animate.set_opacity(0),
            run_time=1.5,
        )

        self.play(
            of_arrow_shadow_2.animate.shift(RIGHT * 1.5),
            of_dot.animate.shift(RIGHT * 1.5),
            FadeIn(hl2),
            i4.animate.set_opacity(1),
            run_time=1.5,
        )

        G = VGroup(
            area,
            of_arrow_shadow,
            numberplane,
            labels[0],
        )

        i1.line.put_start_and_end_on(
            i1.line.get_start() + UP * 5,
            i1.line.get_end() + DOWN * 5,
        )

        i3.line.put_start_and_end_on(
            i3.line.get_start() + (UP + LEFT) * 5,
            i3.line.get_end() + (DOWN + RIGHT) * 5,
        )

        p1.shift(DOWN * us1)
        p2.shift(DOWN * us1)

        self.play(
            G.animate.shift(DOWN * us1),
            p0.animate.shift(DOWN * us1),
            FadeIn(p1, shift=DOWN * us1),
            of_arrow_shadow_2.animate.shift(UP * (2 - us1)),
            of_dot.animate.shift(UP * (2 - us1)),
            Transform(hl, CreateHighlight(ineqs[0][21:])),
            i2.animate.set_opacity(0).shift(DOWN * us1),
            i3.animate.set_opacity(1).shift(DOWN * us1),
            run_time=1.5,
        )

        i2.shift(UP * us1)
        p2.shift(DOWN * us2)
        i5.shift(DOWN * us1)

        self.play(
            G.animate.shift(DOWN * us2),
            FadeIn(p2, shift=DOWN * us2),
            p0.animate.shift(DOWN * us2),
            p1.animate.shift(DOWN * us2),
            of_arrow_shadow_2.animate.shift(UP * (2 - us2) + LEFT * 2),
            of_dot.animate.shift(UP * (2 - us2) + LEFT * 2),
            Transform(hl2, CreateHighlight(ineqs[0][14:21])),
            i4.animate.set_opacity(0).shift(DOWN * us2),
            i5.animate.set_opacity(1).shift(DOWN * us2),
            i3.animate.shift(DOWN * us2),
            run_time=1.5,
        )

        val.remove_updater(value_updater)

        self.play(
            AnimationGroup(
                MyFlash(of_dot, color=BLUE, z_index=of_dot.get_z_index() + 1),
                val.animate(rate_func=there_and_back).scale(THERE_AND_BACK_SCALE),
                lag_ratio=0.25,
            )
        )

        self.play(
            G.animate.shift(UP * (us1 + us2)),
            i5.animate.set_opacity(0).shift(UP * (us1 + us2)),
            i3.animate.set_opacity(0).shift(UP * (us1 + us2)),
            FadeOut(hl, hl2),
            FadeOut(val, of_arrow_shadow_2, of_dot, p0, p1, p2, shift=UP * (us1 + us2)),
        )

        # NOTE: WE ARE ALL COPIED
        ineqs3 = ComplexTex(r"""$$\begin{aligned}
        x_1, x_2, s_1, s_2, s_3  &\ge 0 \\[0.3em]
              x_1 \phantom{{}+ x_2} + s_1 \phantom{{} + s_2 + s_3} &= 3\,000 \\[-0.2em]
              x_2 \phantom{{} + s_1} + s_2 \phantom{{} + s_3} &= 4\,000 \\[-0.2em]
              x_1 + x_2 \phantom{{} + s_1 + s_2} + s_3 &= 5\,000
                \end{aligned}$$""").move_to(ineqs).set_z_index(ineqs.get_z_index())
        var3 = ComplexTex("variables: $x_1, x_2, s_1, s_2, s_3$").move_to(var).set_z_index(var.get_z_index())

        space = 2.5

        guide4 = -guide2.get_center() + RIGHT * (space / 2)

        of3 = of.copy()
        exp3 = exp2.copy().move_to(exp).set_z_index(exp.get_z_index())

        theory_group_two = VGroup(of3, exp3, ineqs3, var3).move_to(guide4)

        i1.shift(RIGHT * space / 2)
        i2.shift(RIGHT * space / 2)
        i3.shift(RIGHT * space / 2)
        i4.shift(RIGHT * space / 2)
        i5.shift(RIGHT * space / 2)
        of_arrow_shadow_2.shift(RIGHT * space / 2)
        of_dot.shift(RIGHT * space / 2)

        VGroup(of3, exp3).align_to(of, UP)
        VGroup(var3).align_to(var, UP)
        VGroup(ineqs3).align_to(ineqs, UP)

        self.remove(rect3)
        rect_large.flip().set_height(rect3.get_height()).move_to(rect3).align_to(rect3, RIGHT).set_z_index(rect3.get_z_index())
        self.add(rect_large)

        var3[0][16:16+2].set_color(ORANGE)
        var3[0][19:19+2].set_color(ORANGE)
        var3[0][22:22+2].set_color(ORANGE)
        ineqs3[0][6:6+2].set_color(ORANGE)
        ineqs3[0][9:9+2].set_color(ORANGE)
        ineqs3[0][12:12+2].set_color(ORANGE)
        ineqs3[0][19:19+2].set_color(ORANGE)
        ineqs3[0][29:29+2].set_color(ORANGE)
        ineqs3[0][42:42+2].set_color(ORANGE)

        slack = Tex(r"slack").scale(0.7).set_color(ORANGE).next_to(
            VGroup(var3[0][16:16+2], var3[0][22:22+2]), UP, buff=0.25
        ).set_z_index(100000000000)

        # this took 3-5 years from my life
        self.play(
            rect_large.animate.shift(RIGHT * space),
            VGroup(
                area,
                of_arrow_shadow,
                numberplane,
                sr,
                labels[1],
            ).animate.shift(RIGHT * space / 2),
            Transform(exp, exp3),
            Transform(of, of3),
            AnimationGroup(
                Transform(var[0][:15], var3[0][:15]),
                AnimationGroup(
                    FadeIn(var3[0][15:]),
                    FadeIn(slack),
                ),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                AnimationGroup(
                    Transform(ineqs[0][:5], ineqs3[0][:5]),
                    Transform(ineqs[0][5:5+2], ineqs3[0][14:14+2]),
                ),
                FadeIn(ineqs3[0][5:5+9]),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                AnimationGroup(
                    Transform(ineqs[0][7:7+2], ineqs3[0][16:16+2]),
                    Transform(ineqs[0][9:9+5], ineqs3[0][21:21+5]),
                ),
                FadeIn(ineqs3[0][18:18+3]),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                AnimationGroup(
                    Transform(ineqs[0][14:14+2], ineqs3[0][26:26+2]),
                    Transform(ineqs[0][16:16+5], ineqs3[0][31:31+5]),
                ),
                FadeIn(ineqs3[0][28:28+3]),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                AnimationGroup(
                    Transform(ineqs[0][21:21+5], ineqs3[0][36:36+5]),
                    Transform(ineqs[0][26:], ineqs3[0][44:]),
                ),
                FadeIn(ineqs3[0][41:41+3]),
                lag_ratio=0.5,
            ),
        )

        #             ______
        #        .d$$$******$$$$c.
        #     .d$P"            "$$c
        #    $$$$$.           .$$$*$.
        #  .$$ 4$L*$$.     .$$Pd$  '$b
        #  $F   *$. "$$e.e$$" 4$F   ^$b
        # d$     $$   z$$$e   $$     '$.
        # $P     `$L$$P` `"$$d$"      $$
        # $$     e$$F       4$$b.     $$
        # $b  .$$" $$      .$$ "4$b.  $$
        # $$e$P"    $b     d$`    "$$c$F
        # '$P$$$$$$$$$$$$$$$$$$$$$$$$$$
        #  "$c.      4$.  $$       .$$
        #   ^$$.      $$ d$"      d$P
        #     "$$c.   `$b$F    .d$P"
        #       `4$$$c.$$$..e$$P"
        #           `^^^^^^^`

        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp3, ineqs3, var3, rect_large, area, of_arrow_shadow, numberplane, sr, labels, sm, slack)

        hl = CreateHighlight(VGroup(ineqs3[0][21], ineqs3[0][31], ineqs3[0][44]))

        a = Tex("$0$")
        a.add(Tex("$=$").scale(0.65).rotate(PI / 2).next_to(a, UP, buff=0.1))
        a.set_color(YELLOW).set_z_index(1000000000).next_to(var3[0][-8:-8+2], DOWN, buff=0.1).set_color(WHITE)

        b = a.copy().next_to(var3[0][-2:], DOWN, buff=0.1).set_color(WHITE)

        # undoes the last move
        of_arrow_shadow_2.shift(UP * -2 + LEFT * -2)
        of_dot.shift(UP * -2 + LEFT * -2 + UP * (us1 + us2))

        # copy-pasted
        val = Tex(r"$(3\,000, 2\,000)$").scale(0.6)\
            .next_to(of_dot, UP)\
            .set_z_index(10000000000)
        val.add(CreateSR(val))

        self.play(
            #FadeIn(of_arrow_shadow_2),
            FadeIn(val),
            FadeIn(of_dot),
            MyFlash(of_dot, color=BLUE, z_index=of_dot.get_z_index() + 1),
            i4.animate.set_opacity(1),
            i3.animate.set_opacity(1),
        )

        hl1 = CreateHighlight(ineqs3[0][16:26])
        hl2 = CreateHighlight(ineqs3[0][36:49])

        self.play(
            FadeIn(hl1),
            FadeIn(hl2),
            var3[0][16:16+2].animate.set_color(YELLOW).set_opacity(BIG_OPACITY),
            var3[0][22:22+2].animate.set_color(YELLOW).set_opacity(BIG_OPACITY),
            var3[0][18:18+1].animate.set_opacity(BIG_OPACITY), #,
            var3[0][21:21+1].animate.set_opacity(BIG_OPACITY), #,
            ineqs3[0][6:6+2].animate.set_color(YELLOW).set_opacity(BIG_OPACITY),
            ineqs3[0][12:12+2].animate.set_color(YELLOW).set_opacity(BIG_OPACITY),
            ineqs3[0][8:8+1].animate.set_opacity(BIG_OPACITY), #,
            ineqs3[0][11:11+1].animate.set_opacity(BIG_OPACITY), #,
            ineqs3[0][18:18+1].animate.set_opacity(BIGGER_OPACITY),
            ineqs3[0][19:19+2].animate.set_color(YELLOW).set_opacity(BIGGER_OPACITY),
            ineqs3[0][41:41+1].animate.set_opacity(BIGGER_OPACITY),
            ineqs3[0][42:42+2].animate.set_color(YELLOW).set_opacity(BIGGER_OPACITY),
        )

        self.play(
            FadeOut(hl1),
            FadeOut(hl2),
            FadeOut(of_dot),
            FadeOut(val),
            i4.animate.set_opacity(0),
            i3.animate.set_opacity(0),
            var3[0][16:16+2].animate.set_color(ORANGE).set_opacity(1),
            var3[0][22:22+2].animate.set_color(ORANGE).set_opacity(1),
            ineqs3[0][6:6+2].animate.set_color(ORANGE).set_opacity(1),
            ineqs3[0][12:12+2].animate.set_color(ORANGE).set_opacity(1),
            ineqs3[0][18:18+1].animate.set_opacity(1),
            ineqs3[0][19:19+2].animate.set_color(ORANGE).set_opacity(1),
            ineqs3[0][41:41+1].animate.set_opacity(1),
            ineqs3[0][42:42+2].animate.set_color(ORANGE).set_opacity(1),
            var3[0][18:18+1].animate.set_opacity(1), #,
            var3[0][21:21+1].animate.set_opacity(1), #,
            ineqs3[0][8:8+1].animate.set_opacity(1), #,
            ineqs3[0][11:11+1].animate.set_opacity(1), #,
        )

        # NOTE: I'm copy-pasted
        of_arrow_shadow_2 = of_arrow_shadow.copy().set_color(BLUE).set_z_index(fade_rect.get_z_index() + 1)
        of_dot = Dot().scale(OPTIMUM_DOT_SCALE).set_color(BLUE).move_to(of_arrow_shadow_2.get_start())\
                .set_z_index(of_arrow_shadow_2.get_z_index())

        vars_buff = 0.25

        nonbas_vars = VGroup(
            var3[0][10:10+2].copy().set_color(YELLOW),
            var3[0][13:13+2].copy().set_color(YELLOW),
        ).arrange(buff=vars_buff)

        bas_vars = VGroup(
            var3[0][16:16+2].copy().set_color(ORANGE),
            var3[0][19:19+2].copy().set_color(ORANGE),
            var3[0][22:22+2].copy().set_color(ORANGE),
        ).arrange(buff=vars_buff)

        VGroup(nonbas_vars, bas_vars).arrange(buff=1.5).move_to(var3).align_to(var3, DOWN)

        nonbasic = Tex("tight").scale(0.7).next_to(nonbas_vars, UP, buff=0.25).set_z_index(rect_large.get_z_index() + 1).set_opacity(0)
        basic = Tex("loose").scale(0.7).next_to(bas_vars, UP, buff=0.25).set_z_index(rect_large.get_z_index() + 1).set_opacity(0)
        nonbasic.align_to(basic, UP)

        nb = Tex("non-basic").scale(0.7).set_z_index(rect_large.get_z_index() + 1).set_opacity(0).move_to(nonbasic).align_to(nonbasic, UP)
        bb = Tex("basic").scale(0.7).set_z_index(rect_large.get_z_index() + 1).set_opacity(0).move_to(basic).align_to(nonbasic, UP)

        self.play(
            FadeIn(of_dot),
            FadeIn(of_arrow_shadow_2),
            MyFlash(of_dot, color=BLUE, z_index=of_dot.get_z_index() + 1),
        )

        self.play(
            Succession(
                Wait(0.5),  # hack since the next transform also makes var yellow
                AnimationGroup(
                    ineqs3[0][0:0+2].animate.set_color(YELLOW),
                    ineqs3[0][3:3+2].animate.set_color(YELLOW),
                    ineqs3[0][16:16+2].animate.set_color(YELLOW),
                    ineqs3[0][26:26+2].animate.set_color(YELLOW),
                    ineqs3[0][36:36+2].animate.set_color(YELLOW),
                    ineqs3[0][39:39+2].animate.set_color(YELLOW),
                    exp3[0][6:6+2].animate.set_color(YELLOW),
                    exp3[0][12:12+2].animate.set_color(YELLOW),
                    i1.animate.set_opacity(1),
                    i2.animate.set_opacity(1),
                ),
            ),
            AnimationGroup(
                # fadeouts
                AnimationGroup(
                    FadeOut(var3[0][:10]),
                    FadeOut(var3[0][12]),
                    FadeOut(var3[0][15]),
                    FadeOut(var3[0][18]),
                    FadeOut(var3[0][21]),
                    FadeOut(slack),
                ),
                # transforms
                AnimationGroup(
                    Transform(var3[0][10:10+2], nonbas_vars[0]),
                    Transform(var3[0][13:13+2], nonbas_vars[1]),
                    Transform(var3[0][16:16+2], bas_vars[0]),
                    Transform(var3[0][19:19+2], bas_vars[1]),
                    Transform(var3[0][22:22+2], bas_vars[2]),
                ),
                # fadeins
                AnimationGroup(
                    basic.animate.set_opacity(MED_OPACITY),
                    nonbasic.animate.set_opacity(MED_OPACITY),
                ),
                lag_ratio=0.5,
            ),
        )

        nb.set_opacity(MED_OPACITY)
        bb.set_opacity(MED_OPACITY)

        f = 0.3
        self.play(
            FadeIn(nb, shift=DOWN * f),
            FadeOut(nonbasic, shift=DOWN * f),
        )

        self.play(
            FadeIn(bb, shift=DOWN * f),
            FadeOut(basic, shift=DOWN * f),
        )

        self.play(
            FadeOut(nb, shift=UP * f),
            FadeIn(nonbasic, shift=UP * f),
            FadeOut(bb, shift=UP * f),
            FadeIn(basic, shift=UP * f),
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp3, ineqs3, bas_vars, nonbas_vars, rect_large, area, of_arrow_shadow, numberplane, sr, labels, sm,
                 basic, nonbasic, of_dot, of_arrow_shadow_2, i1, i2)

        self.play(
            AnimationGroup(
                FadeOut(ineqs3[0][:16]),
                ineqs3[0][16:].animate.move_to(ineqs3),
                lag_ratio=0.25,
            )
        )

        ineqs4 = ComplexTex(r"""$$\begin{aligned}
              s_1 &= 3\,000 - x_1 \\[-0.2em]
              s_2 &= 4\,000 \phantom{{} - x_1} - x_2 \\[-0.2em]
              s_3 &= 5\,000 - x_1 - x_2
                \end{aligned}$$""").move_to(ineqs3).align_to(ineqs3, DOWN)\
                        .set_z_index(ineqs3.get_z_index())

        ineqs4[0][0:0+2].set_color(ORANGE)
        ineqs4[0][10:10+2].set_color(ORANGE)
        ineqs4[0][20:20+2].set_color(ORANGE)

        ineqs4[0][8:8+2].set_color(YELLOW)
        ineqs4[0][18:18+2].set_color(YELLOW)
        ineqs4[0][28:28+2].set_color(YELLOW)
        ineqs4[0][31:31+2].set_color(YELLOW)

        self.play(
            AnimationGroup(
                # fadeouts
                AnimationGroup(
                    #+
                    FadeOut(ineqs3[0][18]),
                    FadeOut(ineqs3[0][28]),
                    FadeOut(ineqs3[0][41]),
                ),
                # transforms
                AnimationGroup(
                    #s_123
                    Transform(ineqs3[0][19:19+2+5], ineqs4[0][0:0+2+5]),
                    Transform(ineqs3[0][29:29+2+5], ineqs4[0][10:10+2+5]),
                    Transform(ineqs3[0][42:42+2+5], ineqs4[0][20:20+2+5]),
                    Transform(ineqs3[0][16:16+2], ineqs4[0][8:8+2]),
                    Transform(ineqs3[0][26:26+2], ineqs4[0][18:18+2]),
                    Transform(ineqs3[0][36:36+5], ineqs4[0][28:28+5]),
                ),
                # fadeins
                AnimationGroup(
                    FadeIn(ineqs4[0][7]),
                    FadeIn(ineqs4[0][17]),
                    FadeIn(ineqs4[0][27]),
                ),
                lag_ratio=0.5,
            ),
            run_time=2,
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp3, ineqs4, bas_vars, nonbas_vars, rect_large, area, of_arrow_shadow, numberplane, sr, labels, sm,
                 basic, nonbasic, of_dot, of_arrow_shadow_2, i1, i2)

        hl = CreateHighlight(
            VGroup(
                ineqs4[0][0],
                ineqs4[0][-12],
            ),
        ).set_color(BLUE)

        hlother = CreateHighlight(bas_vars).set_color(BLUE)

        self.play(
            FadeIn(hl, hlother),
        )

        a.next_to(nonbas_vars[0], DOWN, buff=0.1)
        b.next_to(nonbas_vars[1], DOWN, buff=0.1)

        hl1 = CreateHighlight(VGroup(nonbas_vars[0], a)).set_color(BLUE)
        hl2 = CreateHighlight(VGroup(nonbas_vars[1], b)).set_color(BLUE)
        hlof = CreateHighlight(exp3[0][3:3+11]).set_color(BLUE)
        zero = Tex("$$0$$").set_z_index(exp3.get_z_index()).move_to(exp3[0][3:3+11])

        self.play(
            AnimationGroup(
                AnimationGroup(
                    #FadeIn(a, b, zero),
                    FadeOut(hlother),
                    FadeIn(zero),
                    nonbas_vars[0].animate.set_opacity(BIG_OPACITY),
                    nonbas_vars[1].animate.set_opacity(BIG_OPACITY),
                    exp3[0][3:3+11].animate.set_opacity(BIG_OPACITY / 2),
                    exp3[0][8].animate.set_opacity(0),
                    ineqs4[0][7:7+3].animate.set_opacity(BIG_OPACITY),
                    ineqs4[0][17:17+3].animate.set_opacity(BIG_OPACITY),
                    ineqs4[0][27:27+3].animate.set_opacity(BIG_OPACITY),
                    ineqs4[0][30:30+3].animate.set_opacity(BIG_OPACITY),
                ),
                AnimationGroup(
                    #FadeIn(hl1, hl2, hlof),
                    FadeIn(hlof),
                    Transform(hl, CreateHighlight(
                        VGroup(
                            ineqs4[0][0],
                            ineqs4[0][3],
                            ineqs4[0][-7],
                            ineqs4[0][-12],
                        ),
                    ).set_color(BLUE)),
                ),
                lag_ratio=0,
            ),
        )

        self.play(
            #FadeOut(a, b, hl1, hl2, hlof, zero, hl),
            FadeOut(hlof, hl, zero),
            exp3[0][3:3+11].animate.set_opacity(1),
            ineqs4[0][7:7+3].animate.set_opacity(1),
            ineqs4[0][17:17+3].animate.set_opacity(1),
            ineqs4[0][27:27+3].animate.set_opacity(1),
            ineqs4[0][30:30+3].animate.set_opacity(1),
            nonbas_vars[0].animate.set_opacity(1),
            nonbas_vars[1].animate.set_opacity(1),
        )

        dpivot = Tex(r"\textit{Dantzig's pivot rule}").set_width(sm[0].get_width()).next_to(sm, DOWN, buff=0).set_z_index(10000000000)
        self.play(
            AnimationGroup(
                Transform(sm[1], CreateSR(VGroup(sm[0], dpivot), buff=0.17)),
                FadeIn(dpivot),
                lag_ratio=0.5,
            ),
        )

        hl1 = CreateHighlight(exp3[0][3:3+5]).set_color(GREEN)
        hl2 = CreateHighlight(exp3[0][9:9+5]).set_color(GREEN)

        # hackkk
        offset = -0.05

        dashed_x = Arrow(
            of_dot.get_center(),
            [of_arrow_shadow_2.get_end()[0] - offset, of_dot.get_center()[1], 0],
            stroke_width=LINE_STROKE + 0.01,
            buff=0,
        ).set_color(GREEN).set_z_index(of_arrow_shadow.get_z_index() - 0.001)

        dashed_y = Arrow(
            of_dot.get_center(),
            [of_dot.get_center()[0], of_arrow_shadow_2.get_end()[1] - offset, 0],
            buff=0,
            stroke_width=LINE_STROKE + 0.01,
        ).set_color(GREEN).set_z_index(of_arrow_shadow.get_z_index() - 0.001)

        a = of_arrow_shadow_2.copy().set_z_index(of_arrow_shadow.get_z_index() - 0.001)
        b = of_arrow_shadow_2.copy().set_z_index(of_arrow_shadow.get_z_index() - 0.001)

        self.play(
            FadeIn(hl1),
            FadeIn(hl2),
        )

        self.play(
            Transform(a, dashed_x),
            Transform(b, dashed_y),
            run_time=1,
        )

        self.remove(a, b)
        self.add(dashed_x, dashed_y)

        self.play(
            FadeOut(dashed_x),
            FadeOut(hl1),
        )

        b = VGroup(nonbas_vars[1].copy(), bas_vars[0].copy(), bas_vars[1].copy(), bas_vars[2].copy())
        b.arrange(buff=vars_buff)
        b.move_to(bas_vars)
        b[0].set_color(WHITE)

        nb = VGroup(nonbas_vars[0].copy())
        nb.move_to(nonbas_vars)

        downshift = 1

        self.play(
            AnimationGroup(
                FadeOut(dashed_y, shift=UP + DOWN * downshift),
                of_dot.animate.shift(UP + DOWN * downshift),
                of_arrow_shadow_2.animate.shift(UP + DOWN * downshift).set_opacity(1),
                i2.animate.set_opacity(0).shift(DOWN * downshift),

                of_arrow_shadow.animate.shift(DOWN * downshift),
                labels[0].animate.shift(DOWN * downshift),
                numberplane.animate.shift(DOWN * downshift),
                area.animate.shift(DOWN * downshift),

                FadeOut(hl2),
                Transform(nonbas_vars[0], nb[0]),
                Transform(nonbas_vars[1], b[0]),
                Transform(bas_vars[0], b[1]),
                Transform(bas_vars[1], b[2]),
                Transform(bas_vars[2], b[3]),
                ineqs4[0][18:18+2].animate.set_color(WHITE),
                ineqs4[0][31:31+2].animate.set_color(WHITE),
                exp3[0][-2:].animate.set_color(WHITE),
            ),
        )

        self.remove(nonbas_vars[0], nonbas_vars[1])
        self.remove(bas_vars[0], bas_vars[1], bas_vars[2])
        self.add(b, nb)
        nonbas_vars = nb
        bas_vars = b

        POSSIBLE_COLOR = GRAY

        i3.set_color(POSSIBLE_COLOR).shift(DOWN * downshift)
        i5.set_color(POSSIBLE_COLOR).shift(DOWN * downshift)

        inter = intersection(
            line(i3.line.get_start(), i3.line.get_end()),
            line(i1.line.get_start(), i1.line.get_end()),
        )

        idot = area.dots[0].copy().move_to([*inter, 0])

        inter = intersection(
            line(i5.line.get_start(), i5.line.get_end()),
            line(i1.line.get_start(), i1.line.get_end()),
        )

        idot_correct = area.dots[0].copy().move_to([*inter, 0]).set_z_index(area.dots[0].get_z_index() + 1)

        hls2 = CreateHighlight(ineqs4[0][10:10+2]).set_color(POSSIBLE_COLOR)
        hls3 = CreateHighlight(ineqs4[0][20:20+2]).set_color(POSSIBLE_COLOR)
        hl1 = CreateHighlight(ineqs4[0][13:13+4]).set_color(POSSIBLE_COLOR)
        hl2 = CreateHighlight(ineqs4[0][17:17+3]).set_color(POSSIBLE_COLOR)
        hl3 = CreateHighlight(ineqs4[0][23:23+4]).set_color(POSSIBLE_COLOR)
        hl4 = CreateHighlight(ineqs4[0][30:30+3]).set_color(POSSIBLE_COLOR)

        self.play(
            AnimationGroup(
                FadeIn(hl2),
                FadeIn(hl4),
                lag_ratio=0.07,
            )
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    ineqs4[0][10:10+2].animate.set_color(POSSIBLE_COLOR),
                    bas_vars[2].animate.set_color(POSSIBLE_COLOR),
                    i3.animate.set_opacity(1),
                    FadeIn(hls2),
                ),
                AnimationGroup(
                    ineqs4[0][20:20+2].animate.set_color(POSSIBLE_COLOR),
                    bas_vars[3].animate.set_color(POSSIBLE_COLOR),
                    i5.animate.set_opacity(1),
                    FadeIn(idot, hls3),
                ),
                lag_ratio=0.07,
            ),
        )

        self.add(idot_correct)

        G = VGroup(
            i5, i3, i1,
            labels[0],
            area, numberplane, of_arrow_shadow, of_dot, of_arrow_shadow_2,
            idot,
            idot_correct,
        )

        G.save_state()
        labels[1].save_state()

        # UP * 2 to scale from the very top of the screen
        self.play(
            G.animate.scale(1.75, about_point=(idot_correct.get_center() + UP * 3)).shift(RIGHT * 0.8),
            labels[1].animate.scale(1.75, about_point=(idot_correct.get_center() + UP * 3)).shift(RIGHT * 0.8),
        )

        self.play(
            ineqs4[0][10:10+2].animate.set_color(GREEN),
            bas_vars[2].animate.set_color(GREEN),
            i5.line.animate.set_color(GREEN).set_stroke_width(LINE_STROKE + 3),
            hls2.animate.set_color(GREEN),
            idot_correct.animate.set_color(GREEN),
            hl2.animate.set_color(GREEN),
            ineqs4[0][20:20+2].animate.set_color(RED),
            bas_vars[3].animate.set_color(RED),
            i3.line.animate.set_color(RED).set_stroke_width(LINE_STROKE + 3),
            hls3.animate.set_color(RED),
            idot.animate.set_color(RED),
            hl4.animate.set_color(RED),
        )

        correct = Tex("valid", color=GREEN).scale(0.85).set_z_index(idot.get_z_index()).next_to(idot_correct, LEFT + UP, buff=0.1)
        oob = Tex("out of bounds", color=RED).scale(0.85).set_z_index(idot.get_z_index()).next_to(idot, RIGHT + UP, buff=0.1)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    MyFlash(idot_correct, color=GREEN, z_index=idot_correct.get_z_index() + 1),
                    FadeIn(correct),
                ),
                AnimationGroup(
                    MyFlash(idot, color=RED, z_index=idot_correct.get_z_index() + 1),
                    FadeIn(oob),
                ),
                lag_ratio=0.75,
            ),
        )

        # self.play(
        #     idot_correct.animate(rate_func=there_and_back).scale(THERE_AND_BACK_SCALE),
        #     correct.animate(rate_func=there_and_back).scale(THERE_AND_BACK_SCALE),
        #     i5.line.animate(rate_func=there_and_back).set_stroke_width(LINE_STROKE + 6),
        # )

        self.play(
            FadeOut(correct),
            FadeOut(oob),
        )

        self.play(
            G.animate.restore(),
            labels[1].animate.restore(),
            ineqs4[0][10:10+2].animate.set_color(POSSIBLE_COLOR),
            ineqs4[0][20:20+2].animate.set_color(POSSIBLE_COLOR),
            bas_vars[2].animate.set_color(POSSIBLE_COLOR),
            bas_vars[3].animate.set_color(POSSIBLE_COLOR),
            hls2.animate.set_color(POSSIBLE_COLOR),
            hls3.animate.set_color(POSSIBLE_COLOR),
            hl2.animate.set_color(POSSIBLE_COLOR),
            hl4.animate.set_color(POSSIBLE_COLOR),
        )

        t1 = Tex("${} - 1\,000$").set_z_index(ineqs4.get_z_index() + 1)
        t1[0][1:].set_color(BLUE)
        align_object_by_coords(t1, t1[0][0].get_center(), ineqs4[0][17].get_center())
        t2 = Tex("${} - 1\,000$").set_z_index(ineqs4.get_z_index() + 1)
        t2[0][1:].set_color(BLUE)
        align_object_by_coords(t2, t2[0][0].get_center(), ineqs4[0][30].get_center())
        #hlt1 = CreateHighlight(t1).set_color(POSSIBLE_COLOR)
        #hlt2 = CreateHighlight(t2).set_color(POSSIBLE_COLOR)

        tmp1 = of_dot.copy()
        tmp2 = of_dot.copy()

        ineqs4[0][18:18+2].set_opacity(0),
        ineqs4[0][31:38+2].set_opacity(0),

        a = ineqs4[0][18:18+2].copy().set_opacity(1)
        b = ineqs4[0][31:38+2].copy().set_opacity(1)

        a.save_state()
        b.save_state()

        #brace = BraceBetweenPoints(
        #    Point().align_to(VGroup(t1, t2), UP + RIGHT).get_center(),
        #    Point().align_to(VGroup(t1, t2), DOWN + RIGHT).get_center(),
        #    RIGHT,
        #).set_z_index(ineqs4.get_z_index() + 1)

        #c = a.copy().next_to(brace, RIGHT)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(hl2),
                    FadeOut(hl4),
                ),
                AnimationGroup(
                    Transform(tmp1, t1[0][1:]),
                    Transform(tmp2, t2[0][1:]),
                    a.animate.next_to(t1, RIGHT + DOWN, buff=0.015).shift(UP * 0.13).set_opacity(0.4).scale(0.7),
                    b.animate.next_to(t2, RIGHT + DOWN, buff=0.015).shift(UP * 0.13).set_opacity(0.4).scale(0.7),
                ),
                lag_ratio=0.5,
            ),
        )

        self.remove(tmp1, tmp2)
        self.add(t1, t2)
        ineqs4[0][17].set_opacity(0)
        ineqs4[0][30].set_opacity(0)

        def tupdater(obj, dt):
            val = round((of_dot.get_center() - of_arrow_shadow.get_start())[1] * 1000)

            tt1 = Tex("${} - " + str(val)[0] + "\," + str(val)[1:] + "$").set_z_index(ineqs4.get_z_index() + 1)
            tt1[0][1:].set_color(BLUE)
            align_object_by_coords(tt1, tt1[0][0].get_center(), ineqs4[0][17].get_center())

            obj.become(tt1)

        def tupdater2(obj, dt):
            val = round((of_dot.get_center() - of_arrow_shadow.get_start())[1] * 1000)

            tt1 = Tex("${} - " + str(val)[0] + "\," + str(val)[1:] + "$").set_z_index(ineqs4.get_z_index() + 1)
            tt1[0][1:].set_color(BLUE)
            align_object_by_coords(tt1, tt1[0][0].get_center(), ineqs4[0][30].get_center())

            obj.become(tt1)

        t1.add_updater(tupdater)
        t2.add_updater(tupdater2)

        downshift = 1.5

        self.play(
            of_dot.animate.shift(UP * (3 - downshift)),
            of_arrow_shadow_2.animate.shift(UP * (3 - downshift)),
            VGroup(
                i3, i5, of_arrow_shadow, area, numberplane, labels[0],
                idot, idot_correct,
            ).animate.shift(DOWN * downshift),
            run_time=3,
        )

        t1.remove_updater(tupdater)
        t2.remove_updater(tupdater2)
        tupdater(t1, 0)
        tupdater2(t2, 0)
        self.remove(idot_correct)

        hlll = CreateHighlight(VGroup(ineqs4[0][13:13+4], t1)).set_color(YELLOW)

        self.play(
            bas_vars[2].animate.set_color(YELLOW),
            ineqs4[0][10:10+2].animate.set_color(YELLOW),
            ineqs4[0][20:20+2].animate.set_color(ORANGE),
            i5.animate.set_color(YELLOW),
            FadeIn(hlll),
            FadeOut(i3, idot),
            FadeOut(hls2, hls3),
        )

        t1.add_updater(tupdater)
        t2.add_updater(tupdater2)

        self.play(
            of_dot.animate.shift(UP * 0.5).set_color(RED),
            of_arrow_shadow_2.animate.shift(UP * 0.5).set_color(RED),
            hlll.animate.set_color(RED),
            run_time=1,
        )

        hls2.set_color(RED)

        self.play(
            FadeIn(hls2),
        )

        self.play(
            of_dot.animate.shift(DOWN * 0.5).set_color(BLUE),
            of_arrow_shadow_2.animate.shift(DOWN * 0.5).set_color(BLUE),
            hlll.animate.set_color(YELLOW),
            FadeOut(hls2),
            run_time=1,
        )

        hls2.set_color(POSSIBLE_COLOR)

        t1.remove_updater(tupdater)
        t2.remove_updater(tupdater2)

        self.play(
            bas_vars[2].animate.set_color(POSSIBLE_COLOR),
            ineqs4[0][10:10+2].animate.set_color(POSSIBLE_COLOR),
            ineqs4[0][20:20+2].animate.set_color(POSSIBLE_COLOR),
            i5.animate.set_color(POSSIBLE_COLOR),
            FadeOut(hlll),
            FadeIn(i3, idot),
            FadeIn(hls2, hls3),
            FadeOut(t1[0][1:]),
            FadeOut(t2[0][1:]),
            Succession(
                Wait(0.5),
                AnimationGroup(
                    AnimationGroup(
                        Transform(a, ineqs4[0][18:18+2].copy().set_opacity(1)),
                        Transform(b, ineqs4[0][31:31+2].copy().set_opacity(1)),
                    ),
                    AnimationGroup(
                        FadeIn(hl2),
                        FadeIn(hl4),
                    ),
                    lag_ratio=0.5,
                ),
            ),
        )

        self.remove(t1, t2)

        ineqs4[0][17:17+1].set_opacity(1)
        ineqs4[0][30:30+1].set_opacity(1)

        ineqs4[0][18:18+2].set_opacity(1)
        ineqs4[0][31:31+2].set_opacity(1)
        self.remove(a, b)

        four = Tex("$-4\,000$").move_to(hl1).align_to(ineqs4, RIGHT).shift(RIGHT * 0.5).set_z_index(ineqs4.get_z_index() + 1)
        five = Tex("$-5\,000$").move_to(hl3).align_to(ineqs4, RIGHT).shift(RIGHT * 0.5).set_z_index(ineqs4.get_z_index() + 1)

        ff = VGroup(four, five).scale(0.9).arrange(RIGHT, buff=0.6).next_to(ineqs4, UP, buff=0.5)
        gt = Tex("$>$", stroke_width=1.5).scale(0.5).move_to(VGroup(four, five)).set_z_index(ineqs4.get_z_index() + 1)

        a = ineqs4[0][13:13+4].copy()
        b = ineqs4[0][23:23+4].copy()
        am = ineqs4[0][17:17+1].copy()
        bm = ineqs4[0][30:30+1].copy()
        ah = CreateHighlight(four).set_color(POSSIBLE_COLOR)
        bh = CreateHighlight(five).set_color(POSSIBLE_COLOR)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Transform(a, four[0][1:]),
                    Transform(am, four[0][0]),
                    FadeIn(ah),
                ),
                AnimationGroup(
                    Transform(b, five[0][1:]),
                    Transform(bm, five[0][0]),
                    FadeIn(bh),
                ),
                lag_ratio=0.25,
            ),
        )

        self.remove(a, am, b, bm)
        self.add(four, five)

        self.play(
            FadeIn(gt),
            ah.animate.set_color(GREEN),
            bh.animate.set_color(RED),

            # NOTE: copy-pasted from the zoomin
            ineqs4[0][10:10+2].animate.set_color(GREEN),
            bas_vars[2].animate.set_color(GREEN),
            i5.line.animate.set_color(GREEN),
            hls2.animate.set_color(GREEN),
            hl2.animate.set_color(GREEN),
            ineqs4[0][20:20+2].animate.set_color(RED),
            bas_vars[3].animate.set_color(RED),
            i3.line.animate.set_color(RED),
            hls3.animate.set_color(RED),
            idot.animate.set_color(RED),
            hl4.animate.set_color(RED),
        )

        nb = VGroup(nonbas_vars[0].copy(), bas_vars[2].copy().set_color(YELLOW))
        nb.arrange(buff=vars_buff)
        nb.move_to(nonbas_vars)

        b = VGroup(bas_vars[0].copy(), bas_vars[1].copy(), bas_vars[3].copy().set_color(ORANGE))
        b.arrange(buff=vars_buff)
        b.move_to(bas_vars)

        self.play(
            FadeOut(five, bh, hl4, hls3),
            FadeOut(i3),
            FadeOut(gt),
            FadeOut(idot),
            ineqs4[0][20:20+2].animate.set_color(ORANGE),
        )

        self.play(
            Transform(nonbas_vars[0], nb[0]),
            Transform(bas_vars[2], nb[1]),
            Transform(bas_vars[0], b[0]),
            Transform(bas_vars[1], b[1]),
            Transform(bas_vars[3], b[2]),
            ineqs4[0][10:10+2].animate.set_color(YELLOW),
            FadeOut(four, ah, hl2, hls2),
            i5.animate.set_color(YELLOW),
        )

        self.next_section()

        self.play(
            of_dot.animate.shift(UP * 2),
            of_arrow_shadow_2.animate.shift(UP * 2),
            VGroup(
                i5, of_arrow_shadow, area, numberplane, labels[0],
                idot, idot_correct,
            ).animate.shift(UP * 2),
            run_time=1,
        )

        return

        hlp1 = CreateHighlight(ineqs4[0][10:10+2]).set_color(POSSIBLE_COLOR).set_color(RED)
        hlp2 = hl2.set_color(RED)
        hlp3 = hl4.set_color(RED)
        hlp4 = CreateHighlight(exp3[0][-5:]).set_color(POSSIBLE_COLOR).set_color(RED)

        t1 = Tex("tight").scale(0.6).next_to(hlp1, LEFT).set_z_index(hlp1.get_z_index()).set_color(RED)
        l1 = Tex("loose").scale(0.6).next_to(hlp2, RIGHT).set_z_index(hlp2.get_z_index()).set_color(RED)
        l2 = Tex("loose").scale(0.6).next_to(hlp3, RIGHT).set_z_index(hlp3.get_z_index()).set_color(RED)
        l3 = Tex("loose").scale(0.6).next_to(hlp4, RIGHT).set_z_index(hlp4.get_z_index()).set_color(RED)

        self.play(
            FadeIn(hlp1, hlp2, hlp3, hlp4),
            FadeIn(t1, shift=LEFT * 0.25),
            FadeIn(l1, shift=RIGHT * 0.25),
            FadeIn(l2, shift=RIGHT * 0.25),
            FadeIn(l3, shift=RIGHT * 0.25),
        )

        ineqs5 = ComplexTex(r"""$$\begin{aligned}
              s_1 &= 3\,000 - x_1 \\[-0.2em]
              x_2 &= 4\,000 \phantom{{} - x_1} - s_2 \\[-0.2em]
              s_3 &= 5\,000 - x_1 - (4\,000 - s_2)
                \end{aligned}$$""").set_z_index(ineqs4.get_z_index())

        align_object_by_coords(
            ineqs5,
            ineqs5[0][0].get_center(),
            ineqs4[0][0].get_center(),
        )

        ineqs5[0][0:0+2].set_color(ORANGE)
        ineqs5[0][20:20+2].set_color(ORANGE)
        ineqs5[0][8:8+2].set_color(YELLOW)
        ineqs5[0][18:18+2].set_color(YELLOW)
        ineqs5[0][28:28+2].set_color(YELLOW)
        ineqs5[0][37:37+2].set_color(YELLOW)

        ineqs6 = ComplexTex(r"""$$\begin{aligned}
              s_1 &= 3\,000 - x_1 \\[-0.2em]
              x_2 &= 4\,000 \phantom{{} - x_1} - s_2 \\[-0.2em]
              s_3 &= 1\,000 - x_1 + s_2
                \end{aligned}$$""").set_z_index(ineqs4.get_z_index())

        align_object_by_coords(
            ineqs6,
            ineqs6[0][0].get_center(),
            ineqs4[0][0].get_center(),
        )

        ineqs6[0][0:0+2].set_color(ORANGE)
        ineqs6[0][20:20+2].set_color(ORANGE)
        ineqs6[0][8:8+2].set_color(YELLOW)
        ineqs6[0][18:18+2].set_color(YELLOW)
        ineqs6[0][28:28+2].set_color(YELLOW)
        ineqs6[0][31:31+2].set_color(YELLOW)

        self.play(
            AnimationGroup(
                FadeOut(hlp1, hlp2),
                FadeOut(t1, l1),
                AnimationGroup(
                    ineqs4[0][18:18+2].animate.move_to(ineqs5[0][10:10+2]),
                    ineqs4[0][10:10+2].animate.move_to(ineqs5[0][18:18+2]),
                ),
                lag_ratio=0.5,
            ),
        )

        exp4 = Tex(r"$$\max\ " + str(OF_INITIAL[0]) + r"x_1 + " + str(OF_INITIAL[1]) + r" (4\,000 - s_2)$$").set_z_index(exp3.get_z_index())
        exp4[0][6:6+2].set_color(YELLOW)
        align_object_by_coords(
            exp4,
            exp4[0][0].get_center(),
            exp3[0][0].get_center(),
        )
        exp4[0][18:18+2].set_color(YELLOW)

        exp5 = Tex(r"$$\max\ " + str(OF_INITIAL[0]) + r"x_1 - " + str(OF_INITIAL[1]) + r" s_2 + 6\,800$$").set_z_index(exp3.get_z_index())
        exp5[0][6:6+2].set_color(YELLOW)
        exp5[0][12:12+2].set_color(YELLOW)
        exp5.move_to(exp3)
        exp5.shift(UP * (exp3[0][0].get_center() - exp5[0][0].get_center())[1])

        offset = RIGHT * 0.65

        self.play(
            AnimationGroup(
                AnimationGroup(
                    AnimationGroup(
                        FadeOut(hlp3),
                        FadeOut(l2),
                        FadeOut(ineqs4[0][31:31+2]),
                    ),
                    AnimationGroup(
                        Transform(ineqs4[0][13:13+5].copy(), ineqs5[0][32:32+5]),
                        Transform(ineqs4[0][10:10+2].copy(), ineqs5[0][37:37+2]),
                        rect_large.animate.shift(offset),
                        Group(
                            area,
                            of_arrow_shadow,
                            numberplane,
                            sr,
                            labels[1],
                            of_dot,
                            of_arrow_shadow_2,
                            i1,
                        ).animate.shift(offset/2),
                        Group(sm, dpivot).animate.shift(offset/4),
                    ),
                    AnimationGroup(
                        FadeIn(ineqs5[0][31]),
                        FadeIn(ineqs5[0][39]),
                    ),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    AnimationGroup(
                        FadeOut(hlp4),
                        FadeOut(l3),
                        FadeOut(exp3[0][-2:]),
                    ),
                    AnimationGroup(
                        Transform(ineqs4[0][13:13+5].copy(), exp4[0][13:13+5]),
                        Transform(ineqs4[0][10:10+2].copy(), exp4[0][18:18+2]),
                    ),
                    AnimationGroup(
                        FadeIn(exp4[0][12]),
                        FadeIn(exp4[0][20]),
                    ),
                    lag_ratio=0.5,
                ),
                lag_ratio=0.5,
            ),
        )

        nonbas_vars = nb
        bas_vars = b
        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp4, ineqs5, bas_vars, nonbas_vars, rect_large, area, of_arrow_shadow, numberplane, sr, labels, sm,
                 basic, nonbasic, of_dot, of_arrow_shadow_2, i1, i5, dpivot)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    AnimationGroup(
                        FadeOut(ineqs5[0][30]),
                        FadeOut(ineqs5[0][31]),
                        FadeOut(ineqs5[0][39]),
                    ),
                    AnimationGroup(
                        Transform(ineqs5[0][36:36+3], ineqs6[0][30:30+3]),
                        AnimationGroup(
                            ineqs5[0][32:32+4].animate.move_to(ineqs6[0][23:23+4]).set_opacity(0),
                            Transform(ineqs5[0][23], ineqs6[0][23]),
                            lag_ratio=0.1,
                        ),
                    ),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    AnimationGroup(
                        FadeOut(exp4[0][12]),
                        FadeOut(exp4[0][20]),
                        FadeOut(exp4[0][8]),
                    ),
                    AnimationGroup(
                        Transform(exp4[0][17], exp5[0][8]),
                        Transform(exp4[0][18:18+2], exp5[0][12:12+2]),
                        FadeTransform(exp4[0][13:13+4], exp5[0][15:15+4]),
                        Transform(exp4[0][9:9+3], exp5[0][9:9+3]),
                        Transform(exp4[0][:8], exp5[0][:8]),
                        rect_large.animate.shift(-offset),
                        Group(
                            area,
                            of_arrow_shadow,
                            numberplane,
                            sr,
                            labels[1],
                            of_dot,
                            of_arrow_shadow_2,
                            i1,
                            trace,
                        ).animate.shift(offset/2 * (-1)),
                        Group(sm, dpivot).animate.shift(-offset/4),
                    ),
                    AnimationGroup(
                        FadeIn(exp5[0][14]),
                    ),
                    lag_ratio=0.5,
                ),
                lag_ratio=0.5,
            ),
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp5, ineqs6, bas_vars, nonbas_vars, rect_large, area, of_arrow_shadow, numberplane, sr, labels, sm,
                 basic, nonbasic, of_dot, of_arrow_shadow_2, i1, i5, dpivot)

        hl1 = CreateHighlight(
            VGroup(
                ineqs6[0][0],
                ineqs6[0][3],
                ineqs6[0][10],
                ineqs6[0][21],
                ineqs6[0][26],
            ),
        ).set_color(BLUE)

        hl2 = CreateHighlight(exp5[0][-4:]).set_color(BLUE)

        self.play(
            FadeIn(hl1, hl2),
            ineqs6[0][7:7+3].animate.set_opacity(BIG_OPACITY),
            ineqs6[0][17:17+3].animate.set_opacity(BIG_OPACITY),
            ineqs6[0][27:27+6].animate.set_opacity(BIG_OPACITY),
            exp5[0][3:3+12].animate.set_opacity(BIG_OPACITY),
            nonbas_vars.animate.set_opacity(BIG_OPACITY),
        )

        self.play(
            VGroup(exp5[0][-4:], hl2).animate(rate_func=there_and_back)\
                    .scale(THERE_AND_BACK_SCALE),
        )

        self.play(
            FadeOut(hl1, hl2),
            ineqs6[0][7:7+3].animate.set_opacity(1),
            ineqs6[0][17:17+3].animate.set_opacity(1),
            ineqs6[0][27:27+6].animate.set_opacity(1),
            exp5[0][3:3+12].animate.set_opacity(1),
            nonbas_vars.animate.set_opacity(1),
        )

        hl1 = CreateHighlight(exp5[0][3:3+5]).set_color(GREEN)
        hl2 = CreateHighlight(exp5[0][9:9+5]).set_color(RED)

        # NOTE: next pivot starts here

        # 0 23 58 lines
        steps = ComplexTex(r"""\begin{enumerate}
                \setlength{\itemsep}{4pt}
                \setlength{\parskip}{0pt}
                \item \textbf{loosen variable} (Dantzig's rule)
                \item \textbf{tighten variable} (largest non-positive ratio)
                \item \textbf{fix equalities} (swap + substitute)
                \end{enumerate}""")

        rect_down = rect_large.copy()\
                    .move_to(ORIGIN)\
                    .rotate(PI / 2).align_to(ORIGIN, UP).shift(DOWN + RIGHT * 3.5)\
                    .set_z_index(rect_large.get_z_index() - 0.0001).shift(DOWN * 0.7)

        of_arrow_shadow.set_z_index(rect_down.get_z_index() - 0.00001)

        g = VGroup(of_dot, of_arrow_shadow_2, i1, i5, area, numberplane, of_arrow_shadow)

        rect_down.save_state()
        rect_down.align_to(Dot().next_to(self.camera.frame, DOWN), UP)
        self.add(rect_down)

        self.play(
            rect_down.animate.restore(),
            g.animate.shift(UP * 0.5),
        )

        VGroup(i2, i3, i4).shift(UP * 0.5)

        steps = ComplexTex(r"""\begin{enumerate}
                \setlength{\itemsep}{4pt}
                \setlength{\parskip}{0pt}
                \item \textbf{loosen} (Dantzig's rule)
                \item \textbf{tighten} (largest non-positive ratio)
                \item \textbf{fix} (swap + substitute)
                \end{enumerate}""").scale(0.65).set_z_index(rect_down.get_z_index() + 1)

        steps.next_to(rect_large, RIGHT, buff=0.5).align_to(rect_down, UP).shift(DOWN * 0.5)

        self.play(FadeIn(steps[0][:23]))
        self.play(FadeIn(steps[0][23:58]))
        self.play(FadeIn(steps[0][58:]))

        # hackkk
        offset = -0.05

        dashed_x = Arrow(
            of_dot.get_center(),
            [of_arrow_shadow_2.get_end()[0] - offset, of_dot.get_center()[1], 0],
            stroke_width=LINE_STROKE + 0.01,
            buff=0,
        ).set_color(GREEN).set_z_index(of_dot.get_z_index() - 0.000001)

        dashed_y = Arrow(
            of_dot.get_center(),
            [of_dot.get_center()[0], of_arrow_shadow_2.get_end()[1] - offset, 0],
            buff=0,
            stroke_width=LINE_STROKE + 0.01,
        ).set_color(RED).set_z_index(of_dot.get_z_index() - 0.000001)

        a = of_arrow_shadow_2.copy().set_z_index(of_dot.get_z_index() - 0.000001)
        b = of_arrow_shadow_2.copy().set_z_index(of_dot.get_z_index() - 0.000001)

        self.play(
            steps[0][23:58].animate.set_opacity(BIG_OPACITY),
            steps[0][58:].animate.set_opacity(BIG_OPACITY),
        )

        self.play(
            FadeIn(hl1),
            FadeIn(hl2),
        )

        self.play(
            Transform(a, dashed_x),
            Transform(b, dashed_y),
            run_time=1,
        )

        self.remove(a, b)
        self.add(dashed_x, dashed_y)

        self.play(
            FadeOut(dashed_y),
            FadeOut(hl2),
        )

        nb = VGroup(nonbas_vars[1].copy())
        nb.move_to(nonbas_vars)

        b = VGroup(nonbas_vars[0].copy().set_color(WHITE), bas_vars[0].copy(), bas_vars[1].copy(), bas_vars[2].copy())
        b.arrange(buff=vars_buff)
        b.move_to(bas_vars)
        b[0].set_color(WHITE)

        self.play(
            Transform(nonbas_vars[0], b[0]),
            Transform(nonbas_vars[1], nb[0]),
            Transform(bas_vars[0], b[1]),
            Transform(bas_vars[1], b[2]),
            Transform(bas_vars[2], b[3]),

            ineqs6[0][8:8+2].animate.set_color(WHITE),
            ineqs6[0][28:28+2].animate.set_color(WHITE),
            i1.animate.set_opacity(0),
            of_dot.animate.shift(RIGHT * 0.5),
            of_arrow_shadow_2.animate.shift(RIGHT * 0.5),
            FadeOut(dashed_x, shift=RIGHT * 0.5),
            FadeOut(hl1),
            exp5[0][6:6+2].animate.set_color(WHITE),
        )

        self.remove(nonbas_vars[0], nonbas_vars[1])
        self.remove(bas_vars[0], bas_vars[1], bas_vars[2])
        self.add(b, nb)
        nonbas_vars = nb
        bas_vars = b

        i3.set_color(POSSIBLE_COLOR).set_opacity(0)
        i4.set_color(POSSIBLE_COLOR).set_opacity(0)

        inter = intersection(
            line(i5.line.get_start(), i5.line.get_end()),
            line(i4.line.get_start(), i4.line.get_end()),
        )

        idot = area.dots[0].copy().move_to([*inter, 0])

        hls1 = CreateHighlight(ineqs6[0][0:0+2]).set_color(POSSIBLE_COLOR)
        hls3 = CreateHighlight(ineqs6[0][20:20+2]).set_color(POSSIBLE_COLOR)
        hl1 = CreateHighlight(ineqs6[0][3:3+4]).set_color(POSSIBLE_COLOR)
        hl2 = CreateHighlight(ineqs6[0][7:7+3]).set_color(POSSIBLE_COLOR)
        hl3 = CreateHighlight(ineqs6[0][23:23+4]).set_color(POSSIBLE_COLOR)
        hl4 = CreateHighlight(ineqs6[0][27:27+3]).set_color(POSSIBLE_COLOR)

        self.play(
            steps[0][:23].animate.set_opacity(BIG_OPACITY),
            steps[0][23:58].animate.set_opacity(1),
            steps[0][58:].animate.set_opacity(BIG_OPACITY),
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeIn(hl2),
                    ineqs6[0][0:0+2].animate.set_color(POSSIBLE_COLOR),
                    bas_vars[2].animate.set_color(POSSIBLE_COLOR),
                    i4.animate.set_opacity(1),
                    FadeIn(hls1, idot),
                ),
                AnimationGroup(
                FadeIn(hl4),
                    ineqs6[0][20:20+2].animate.set_color(POSSIBLE_COLOR),
                    bas_vars[3].animate.set_color(POSSIBLE_COLOR),
                    i3.animate.set_opacity(1),
                    FadeIn(hls3),
                ),
                lag_ratio=0.07,
            ),
        )

        four = Tex("$-3\,000$").move_to(hl1).align_to(ineqs6, RIGHT).shift(RIGHT * 0.5).set_z_index(ineqs6.get_z_index() + 1)
        five = Tex("$-1\,000$").move_to(hl3).align_to(ineqs6, RIGHT).shift(RIGHT * 0.5).set_z_index(ineqs6.get_z_index() + 1)

        ff = VGroup(four, five).scale(0.9).arrange(RIGHT, buff=0.6).next_to(ineqs6, UP, buff=0.5)
        gt = Tex("$<$", stroke_width=1.5).scale(0.5).move_to(VGroup(four, five)).set_z_index(ineqs6.get_z_index() + 1)

        a = ineqs6[0][3:3+4].copy()
        b = ineqs6[0][23:23+4].copy()
        am = ineqs6[0][7:7+1].copy()
        bm = ineqs6[0][27:27+1].copy()
        ah = CreateHighlight(four).set_color(POSSIBLE_COLOR)
        bh = CreateHighlight(five).set_color(POSSIBLE_COLOR)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Transform(a, four[0][1:]),
                    Transform(am, four[0][0]),
                    FadeIn(ah),
                ),
                AnimationGroup(
                    Transform(b, five[0][1:]),
                    Transform(bm, five[0][0]),
                    FadeIn(bh),
                ),
                lag_ratio=0.25,
            ),
        )

        inter = intersection(
            line(i5.line.get_start(), i5.line.get_end()),
            line(i3.line.get_start(), i3.line.get_end()),
        )

        idot_correct = area.dots[0].copy().move_to([*inter, 0]).set_z_index(area.dots[0].get_z_index() + 1)
        self.add(idot_correct)

        self.remove(a, am, b, bm)
        self.add(four, five)

        self.play(
            FadeIn(gt),
            bh.animate.set_color(GREEN),
            ah.animate.set_color(RED),

            # NOTE: copy-pasted from the zoomin
            ineqs6[0][20:20+2].animate.set_color(GREEN),
            bas_vars[3].animate.set_color(GREEN),
            i3.line.animate.set_color(GREEN),
            hls3.animate.set_color(GREEN),
            idot_correct.animate.set_color(GREEN),
            hl4.animate.set_color(GREEN),
            ineqs6[0][0:0+2].animate.set_color(RED),
            bas_vars[2].animate.set_color(RED),
            i4.line.animate.set_color(RED),
            hls1.animate.set_color(RED),
            idot.animate.set_color(RED),
            hl2.animate.set_color(RED),
        )

        nb = VGroup(nonbas_vars[0].copy(), bas_vars[3].copy().set_color(YELLOW))
        nb.arrange(buff=vars_buff)
        nb.move_to(nonbas_vars)

        b = VGroup(bas_vars[0].copy(), bas_vars[1].copy(), bas_vars[2].copy().set_color(ORANGE))
        b.arrange(buff=vars_buff)
        b.move_to(bas_vars)

        self.play(
            FadeOut(four, ah, hl2, hls1),
            FadeOut(idot),
            FadeOut(i4),
            FadeOut(gt),
            ineqs6[0][0:0+2].animate.set_color(ORANGE),
            bas_vars[2].animate.set_color(ORANGE),
        )

        self.play(
            FadeOut(five, bh, hl4, hls3),
            ineqs6[0][20:20+2].animate.set_color(YELLOW),
            i3.animate.set_color(YELLOW),
            Transform(nonbas_vars[0], nb[0]),
            Transform(bas_vars[3], nb[1]),
            Transform(bas_vars[0], b[0]),
            Transform(bas_vars[1], b[1]),
            Transform(bas_vars[2], b[2]),
            of_dot.animate.shift(RIGHT * 0.5),
            of_arrow_shadow_2.animate.shift(RIGHT * 0.5),
        )

        nonbas_vars = nb
        bas_vars = b

        hlp1 = hls3.set_color(RED)
        hlp2 = hl2.set_color(RED)
        hlp3 = hl4.set_color(RED)
        hlp4 = CreateHighlight(exp5[0][3:3+5]).set_color(POSSIBLE_COLOR).set_color(RED)

        self.play(
            steps[0][:23].animate.set_opacity(BIG_OPACITY),
            steps[0][23:58].animate.set_opacity(BIG_OPACITY),
            steps[0][58:].animate.set_opacity(1),
        )

        self.play(
            FadeIn(hlp1, hlp2, hlp3, hlp4),
        )

        ineqs7 = ComplexTex(r"""$$\begin{aligned}
              s_1 &= 3\,000 - x_1 \\[-0.2em]
              x_2 &= 4\,000 \phantom{{} - s_1} - s_2 \\[-0.2em]
              x_1 &= 1\,000 - s_3 + s_2
                \end{aligned}$$""").set_z_index(ineqs4.get_z_index())

        align_object_by_coords(
            ineqs7,
            ineqs7[0][0].get_center(),
            ineqs6[0][0].get_center(),
        )

        ineqs7[0][0:0+2].set_color(ORANGE)
        ineqs7[0][8:8+2].set_color(WHITE)
        ineqs7[0][18:18+2].set_color(YELLOW)
        ineqs7[0][20:20+2].set_color(WHITE)
        ineqs7[0][28:28+2].set_color(YELLOW)
        ineqs7[0][31:31+2].set_color(YELLOW)

        self.play(
            AnimationGroup(
                FadeOut(hlp1, hlp3),
                AnimationGroup(
                    ineqs6[0][20:20+2].animate.move_to(ineqs7[0][28:28+2]),
                    ineqs6[0][28:28+2].animate.move_to(ineqs7[0][20:20+2]),
                    ineqs6[0][30:].animate.move_to(ineqs7[0][30:]),
                    ineqs6[0][17:17+3].animate.move_to(ineqs7[0][17:17+3]),
                ),
                lag_ratio=0.5,
            ),
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp5, ineqs7, bas_vars, nonbas_vars, rect_large, rect_down, area, of_arrow_shadow, numberplane, sr, labels, sm,
                 basic, nonbasic, of_dot, of_arrow_shadow_2, i3, i5, dpivot, steps, hlp2, hlp4)

        ineqs8 = ComplexTex(r"""$$\begin{aligned}
              s_1 &= 2\,000 + s_3 - s_2 \\[-0.2em]
              x_2 &= 4\,000 \phantom{{} - s_1} - s_2 \\[-0.2em]
              x_1 &= 1\,000 - s_3 + s_2
                \end{aligned}$$""").set_z_index(ineqs4.get_z_index())

        align_object_by_coords(
            ineqs8,
            ineqs8[0][0].get_center(),
            ineqs7[0][0].get_center(),
        )

        ineqs8[0][0:0+2].set_color(ORANGE)
        ineqs8[0][8:8+2].set_color(YELLOW)
        ineqs8[0][11:11+2].set_color(YELLOW)
        ineqs8[0][21:21+2].set_color(YELLOW)
        ineqs8[0][31:31+2].set_color(YELLOW)
        ineqs8[0][34:34+2].set_color(YELLOW)

        exp6 = Tex(r"$$\max\ -1.2 s_3 - 0.5 s_2 + 8\,000$$").set_z_index(exp5.get_z_index())
        exp6[0][7:7+2].set_color(YELLOW)
        exp6[0][13:13+2].set_color(YELLOW)
        exp6.move_to(exp5)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    ineqs7[0][23:].copy().animate.align_to(ineqs7[0][3:9+1], DOWN).set_opacity(0),
                    Succession(
                        Wait(0.25),
                        AnimationGroup(
                            AnimationGroup(
                                FadeOut(ineqs7[0][3:9+1]),
                                FadeOut(hlp2),
                            ),
                            FadeIn(ineqs8[0][3:13]),
                            lag_ratio=0.2,
                            run_time=0.75,
                        ),
                    ),
                ),
                AnimationGroup(
                    ineqs7[0][23:].copy().animate.move_to(exp5[0][3:]).set_opacity(0),
                    Succession(
                        Wait(0.25),
                        AnimationGroup(
                            AnimationGroup(
                                FadeOut(exp5),
                                FadeOut(hlp4),
                            ),
                            FadeIn(exp6),
                            lag_ratio=0.2,
                            run_time=0.75,
                        ),
                    ),
                ),
                lag_ratio=0.75,
            ),
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(of3, exp6, ineqs8, bas_vars, nonbas_vars, rect_large, rect_down, area, of_arrow_shadow, numberplane, sr, labels, sm,
                 basic, nonbasic, of_dot, of_arrow_shadow_2, i3, i5, dpivot, steps)

        self.play(
            steps[0][:23].animate.set_opacity(1),
            steps[0][23:58].animate.set_opacity(1),
            steps[0][58:].animate.set_opacity(1),
        )

        hl1 = CreateHighlight(exp6[0][4:4+5]).set_color(RED)
        hl2 = CreateHighlight(exp6[0][10:10+5]).align_to(hl1, DOWN).set_color(RED)

        self.play(
            FadeIn(hl1, hl2),
            steps[0][:23].animate.set_opacity(1),
            steps[0][23:58].animate.set_opacity(BIG_OPACITY),
            steps[0][58:].animate.set_opacity(BIG_OPACITY),
        )

        self.play(
            FadeOut(hl1, hl2),
            steps[0][:23].animate.set_opacity(1),
            steps[0][23:58].animate.set_opacity(1),
            steps[0][58:].animate.set_opacity(1),
        )

        hl1 = CreateHighlight(VGroup(ineqs8[0][0], ineqs8[0][6], ineqs8[0][23], ineqs8[0][24])).set_color(BLUE)
        hl2 = CreateHighlight(exp6[0][-4:]).set_color(BLUE)

        hltg = VGroup(ineqs8[0][13:13+7], ineqs8[0][23:23+7])
        hlt = CreateHighlight(hltg).set_color(BLUE)

        self.play(
            FadeIn(hl1, hl2),
            nonbas_vars.animate.set_opacity(BIG_OPACITY),

            ineqs8[0][7:7+6].animate.set_opacity(BIG_OPACITY),
            ineqs8[0][20:20+3].animate.set_opacity(BIG_OPACITY),
            ineqs8[0][30:30+6].animate.set_opacity(BIG_OPACITY),
            exp6[0][3:3+13].animate.set_opacity(BIG_OPACITY),
        )

        self.play(
            VGroup(exp6[0][-4:], hl2).animate(rate_func=there_and_back)\
                    .scale(THERE_AND_BACK_SCALE),
        )

        self.play(
            ineqs8[0][:7].animate.set_opacity(BIG_OPACITY),
            Transform(hl1, hlt),
        )

        self.play(
            VGroup(hltg, hl1).animate(rate_func=there_and_back)\
                    .scale(THERE_AND_BACK_SCALE),
        )

        self.play(
            FadeOut(hl1, hl2),
            nonbas_vars.animate.set_opacity(1),

            ineqs8[0][7:7+6].animate.set_opacity(1),
            ineqs8[0][20:20+3].animate.set_opacity(1),
            ineqs8[0][30:30+6].animate.set_opacity(1),
            exp6[0][3:3+13].animate.set_opacity(1),
        )


class TestSteps(MovingCameraScene):
    @fade
    def construct(self):
        ineqs8 = ComplexTex(r"""$$\begin{aligned}
              s_1 &= 2\,000 + s_3 - s_2 \\[-0.2em]
              x_2 &= 4\,000 \phantom{{} - x_1} - s_2 \\[-0.2em]
              x_1 &= 1\,000 - s_3 + s_2
                \end{aligned}$$""")

        ineqs8[0][0:0+2].set_color(ORANGE)
        ineqs8[0][8:8+2].set_color(YELLOW)
        ineqs8[0][11:11+2].set_color(YELLOW)
        ineqs8[0][21:21+2].set_color(YELLOW)
        ineqs8[0][31:31+2].set_color(YELLOW)
        ineqs8[0][34:34+2].set_color(YELLOW)

        self.add(ineqs8)

        self.wait()


class TestAddd(ThreeDScene):
    def construct(self):
        s = Square()
        self.add(s)

        self.play(Addd(s, RIGHT * 3))


class Test3D(ThreeDScene):
    @fade
    def construct(self):
        offset = np.array([ 1.12563452, -2,          0        ])

        axes = ThreeDAxes(
            x_range=(- 2 * 7.111111111111111, 2 * 7.111111111111111, 1),
            y_range=(- 2 * 7.111111111111111, 2 * 7.111111111111111, 1),
            z_range=(- 2 * 7.111111111111111, 2 * 7.111111111111111, 1),
            x_length=(6 * 7.111111111111111),
            y_length=(6 * 7.111111111111111),
            z_length=(3 * 7.111111111111111),
            axis_config={
                "stroke_width": 4,
                "include_ticks": False,
            },
            num_axis_pieces=10,  # mb edit this
            stroke_width = 6,
            tips=False,
        )

        axes.z_axis.set_opacity(0)

        area = FeasibleArea3D(test=False)

        seed(0xbeef)
        area.add_inequalities([
            Inequality3D(-1, 0, 0, "<=", 0),
            Inequality3D(0, -1, 0, "<=", 0),
            Inequality3D(1, 1, 0, "<=", 5),
            Inequality3D(1, 0, 0, "<=", 3),
            Inequality3D(0, 1, 0, "<=", 4),

            Inequality3D(0, 0, 1, "<=", 1.5),
            Inequality3D(0, 0, -1, "<=", 1.5),

            # the more complex inequalities
            # calculated from printing out the ones from Farmer scene
            Inequality3D(-2.0, -1, 0, "<=", -1.118033988749895),
            Inequality3D(-0.5, -1, 0, "<=", -0.5590169943749475),
            Inequality3D(1.0, -1, 0, "<=", 2.646446609406726),
            Inequality3D(1.5000000000000002, 1, 0, "<=", 6.0493060905670015),
            Inequality3D(-0.2999999999999998, 1, 0, "<=", 3.8433954023663417),
            Inequality3D(-1.0, 1, 0, "<=", 3.787867965644036),
            Inequality3D(-4.0, 1, 0, "<=", 3.175378874876468),
            Inequality3D(0.8999999999999999, 1, 0, "<=", 4.832731879764632),
        ])

        sorted_dots = sorted(list(area.dots), key=lambda x: tuple(x.get_center()))

        #for i, d in enumerate(sorted_dots):
        #    self.add(Tex(str(i)).move_to(d.get_center()).shift(OUT))

        # I'm too lazyyyyyy
        center = np.array((1.5, 1.5, 0))

        additional_ineqs = []
        for i in range(len(sorted_dots)):
            s = uniform(0.07, 0.15)

            norm = center - sorted_dots[i].get_center()

            d = np.dot(norm, sorted_dots[i].get_center() + norm * s)

            additional_ineqs.append(Inequality3D(*(-norm), "<=", -d))

        # TODO: tmp (to see topdown)
        top = Inequality3D(0, 0, 1, "<=", 0.01)
        bottom = Inequality3D(0, 0, -1, "<=", 0.01)
        additional_ineqs.append(top)
        additional_ineqs.append(bottom)

        OF_BIG = np.array((1.2, 1.7, 1.1))

        min_dot = min([(np.dot(OF_BIG, d.get_center()), d.get_center()) for d in area.dots])[1]

        arrow = Arrow3D(
            start=min_dot,
            end=min_dot + OF_BIG,
            resolution=8
        )

        vt = ValueTracker()
        vt.set_value(0.01)
        self.add(vt)

        def please_for_the_love_of_god_end_my_suffering_updater(obj, dt):
            """Feeling cute might nuke my CPU idk hehe 😊."""
            top.d = vt.get_value()
            bottom.d = vt.get_value()

            area._update_area()
            area.shift(offset)

        #vt.add_updater(please_for_the_love_of_god_end_my_suffering_updater)

        area.add_inequalities(additional_ineqs)

        axes.shift(offset)
        area.shift(offset)
        arrow.shift(offset)

        labels = VGroup(
            Tex("$x_p$").scale(1.2).move_to(axes)\
                    .next_to(axes.x_axis, DOWN, buff=0.33)\
                    .align_to(config.right_side, RIGHT).shift(LEFT * 0.2)\
                    .set_color(POTATO_COLOR),
            Tex("$x_c$").scale(1.2).move_to(axes)\
                    .next_to(axes.y_axis, LEFT, buff=0.23)\
                    .align_to(config.top, UP).shift(DOWN * 0.35)\
                    .set_color(CARROT_COLOR),
        )

        self.add(axes, area, arrow, labels)

        self.wait()

        return

        # TODO: add anims such that center of the polygon is in the center of the screen
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, added_anims=[axes.z_axis.animate.set_opacity(1), vt.animate.set_value(1.5)], run_time=3)


class TransparentSilhouettes(MovingCameraScene):
    @fade
    def construct(self):
        scale = 2

        student = SVGMobject("assets/silhouettes/student-cropped.svg").set_color(WHITE).scale(scale)
        sitting = SVGMobject("assets/silhouettes/sitting-cropped.svg").set_color(WHITE).scale(scale)\
                .scale(0.7).align_to(student, DOWN)
        returning = SVGMobject("assets/silhouettes/returning-cropped.svg").set_color(WHITE).scale(scale)
        looking_up = SVGMobject("assets/silhouettes/looking-up-cropped.svg").set_color(WHITE).scale(scale)\
                .scale(0.7).align_to(student, DOWN)
        professor = SVGMobject("assets/silhouettes/professor-cropped.svg").set_color(WHITE).scale(scale)

        self.play(FadeIn(student, shift=0.25 * RIGHT))

        return_distance = 5.5

        self.play(
            FadeOut(student, shift=RIGHT * return_distance),
            FadeIn(sitting, shift=RIGHT * return_distance),
            run_time=1.5,
        )

        self.play(
            FadeOut(sitting, shift=LEFT * return_distance),
            FadeIn(returning, shift=LEFT * return_distance),
            run_time=1.5,
        )

        self.play(
            FadeOut(returning, shift=RIGHT * return_distance),
            FadeIn(sitting, shift=RIGHT * return_distance),
            run_time=1.5,
        )

        prof_distance = 4

        professor.shift(LEFT * prof_distance)

        self.play(
            AnimationGroup(
                Succession(
                    Wait(0.3),
                    AnimationGroup(
                        FadeIn(looking_up),
                        FadeOut(sitting),
                        lag_ratio=0.1,
                        run_time=0.7,
                    ),
                ),
                self.camera.frame.animate.shift(LEFT * prof_distance / 2),
                FadeIn(professor),
            ),
            run_time=1.5,
        )

        name = Tex(r"\sc George B. Dantzig").next_to(looking_up, UP, buff=0.5)

        dantzig = ImageMobject("assets/dantzig-border.png")\
                .set_height(looking_up.get_height())\
                .align_to(self.camera.frame, LEFT).set_z_index(5)\
                .set_z_index(1)

        g = Group(
            dantzig,
            looking_up.copy(),
        ).arrange(buff=0.75).move_to(looking_up)

        #dantzig_bg = SurroundingRectangle(dantzig, buff=0, color=WHITE, stroke_width=8).set_z_index(0)
        #dantzig.add(dantzig_bg)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    self.camera.frame.animate.shift(RIGHT * prof_distance / 2).scale(0.65),
                    FadeOut(professor),
                ),
                FadeIn(name, shift=UP * 0.15),
                lag_ratio=0.75,
            ),
        )

        self.play(
            AnimationGroup(
                Transform(looking_up, g[1]),
                FadeIn(g[0]),
                lag_ratio=0.25,
            )
        )


class TransparentPauseV2(MovingCameraScene):
    def construct(self):
        pause = SVGMobject("assets/pause_v2.svg").scale(0.6).set_z_index(1000)

        # hack
        d = Dot().shift(UP * 0.6).scale(1.5).set_z_index(10001)
        d2 = Dot().shift(UP * 0.6).scale(1.25).set_z_index(10001)
        trace = TracedPath(d.get_center, stroke_width=9).set_color(WHITE).set_z_index(10001)

        self.add(trace, pause, d, d2)

        #self.play(FadeIn(pause))

        self.play(
            Rotate(d, 2 * PI, about_point=ORIGIN),
            run_time=5,
            rate_func=linear,
        )

class TransparentPause(MovingCameraScene):
    @fade
    def construct(self):
        line = Line(3*LEFT, 3*RIGHT, stroke_width=6).shift(UP * 0).set_color(GRAY)

        d1 = Dot().move_to(line.get_left()).scale(1.5)
        d2 = Dot().move_to(line.get_right()).scale(1.5)

        pause = SVGMobject("assets/pause.svg").move_to(line.get_left()).scale(0.3).set_z_index(1000)

        self.add(line, pause, d1, d2)

        trace = TracedPath(pause.get_center).set_color(WHITE).set_stroke_width(8)
        self.add(trace)

        self.play(pause.animate(rate_func=linear, run_time=5).move_to(d2))


class TransparentPauseWithHint(MovingCameraScene):
    @fade
    def construct(self):
        line = Line(3*LEFT, 3*RIGHT, stroke_width=6).shift(UP * 0).set_color(GRAY)
        d1 = Dot().move_to(line.get_left()).scale(1.5)
        d2 = Dot().move_to(line.get_right()).scale(1.5)
        dmiddle = Dot().move_to(VGroup(d1, d2)).scale(1.5)

        hint = Tex("\\bf Hint").next_to(dmiddle, UP, buff=0.45)

        pause = SVGMobject("assets/pause.svg").move_to(line.get_left()).scale(0.3).set_z_index(1000)
        #bulb = SVGMobject("assets/pause-hint.svg").scale(0.35).set_z_index(1000).move_to(VGroup(d1, d2))

        self.add(line, pause, d1, d2, dmiddle, hint)

        trace = TracedPath(pause.get_center).set_color(WHITE).set_stroke_width(8)
        self.add(trace)

        self.play(pause.animate(rate_func=linear, run_time=4).move_to(dmiddle))
        self.play(pause.animate(rate_func=linear, run_time=4).move_to(d2))


class TransparentFunnyXD(MovingCameraScene):
    @fade
    def construct(self):
        l = SVGMobject("assets/l_char.svg").set_color(WHITE).set(height=0.35 * self.camera.frame.height).set_z_index(1000)
        r = SVGMobject("assets/r_char.svg").set_color(WHITE).set(height=0.35 * self.camera.frame.height).set_z_index(1000)

        VGroup(l, r).arrange(buff=6).align_to(self.camera.frame, DOWN)

        ltext = Tex("The optimum is $8\,000$!").set_z_index(10)
        ltext.add(SurroundingRectangle(ltext, color=WHITE, fill_opacity=0.5, fill_color=BLACK, corner_radius=0.2, buff=0.3))

        rtext = Tex("Sir this is a McDonalds.").set_z_index(10)
        rtext.add(SurroundingRectangle(VGroup(rtext, ltext[0][4]), color=WHITE, fill_opacity=0.5, fill_color=BLACK, corner_radius=0.2, buff=0.3))

        rtext2 = Tex("Security!").set_z_index(10)
        rtext2.add(SurroundingRectangle(rtext2, color=WHITE, fill_opacity=0.5, fill_color=BLACK, corner_radius=0.2, buff=0.3))

        self.add(l, r)

        ltext.next_to(l, UP, buff=1).shift(RIGHT * 0.5)
        rtext.next_to(r, UP, buff=1).shift(LEFT * 0.5)
        rtext2.next_to(r, UP, buff=1)

        self.play(
            FadeIn(l, shift=RIGHT),
            FadeIn(r, shift=LEFT),
        )

        self.play(
            Wiggle(l),
            Succession(
                Wait(0.25),
                FadeIn(ltext, shift=UP),
            ),
        )

        self.play(
            Wiggle(r),
            Succession(
                Wait(0.25),
                FadeIn(rtext, shift=UP),
            )
        )

        self.play(
            r.animate.flip(),
            Succession(
                Wait(0.5),
                AnimationGroup(
                    FadeOut(rtext, shift=UP * 1.5),
                    FadeIn(rtext2, shift=UP * 1.5),
                ),
            )
        )


class ILP(MovingCameraScene):
    # no fade here to force me to use Kdenlive one
    def construct(self):
        numberplane = NumberPlane(
            x_range=(- 2 * 7.111111111111111, 2 * 7.111111111111111, 1),
            y_range=(- 2 * 4.0, 2 * 4.0, 1),
            stroke_width = 6,
            axis_config={
                "stroke_width": 4,
            },
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 3,
                "stroke_opacity": 0.6
            },
        )

        self.camera.frame.scale(0.95)

        numberplane.axes.set_z_index(200)

        area = FeasibleArea2D(dots_z_index=2).set_z_index(1)

        i1 = Inequality2D(1, 0.2, ">=", -3.5).set_z_index(10)
        i2 = Inequality2D(0, 1, ">=", -2.5).set_z_index(10)
        i3 = Inequality2D(1, 1, "<=", 3.8).set_z_index(10)
        i4 = Inequality2D(1, 0.3, "<=", 3.1 + 0.5).set_z_index(10)
        i5 = Inequality2D(-0.1, 1, "<=", 2.7).set_z_index(10)

        ineqs = [i1, i2, i3, i4, i5]

        for p1, p2, sym in [
            ((4, -0.85), (3, -2), ">="),
            ((-2, 3), (-3, 1), "<="),
            ((-1, 3), (2, 2), "<="),
            ((0, -3), (-3, -1.8), ">="),
        ]:
            Inequality2D.points_to_slope(p1, p2)

            a, b, c = Inequality2D.points_to_slope(p1, p2)
            i = Inequality2D(a, b, sym, c)
            ineqs.append(i)

        dots = VGroup()

        for x in range(-10, 10 + 1):
            for y in range(-5, 5 + 1):
                dots.add(Dot().set_color(DARK_GRAY).move_to(RIGHT * x + UP * y).scale(0.8))

                for i in ineqs:
                    if not i.satisfies(x, y):
                        break
                else:
                    dots[-1].set_color(WHITE).scale(1/0.8 * NORMAL_DOT_SCALE * 0.8)

                dots[-1].set_z_index(100)

        area.add_inequalities(ineqs)

        self.play(
            FadeIn(numberplane.background_lines),
            FadeIn(numberplane.axes),
        )

        inr = Tex(r"$$\mathbf{x} \in \mathbb{R}$$").scale(1.5).set_z_index(100000).align_to(self.camera.frame, UP + RIGHT).shift((LEFT * 1.3 + DOWN * 1) * 0.7)
        inn = Tex(r"$$\mathbf{x} \in \mathbb{N}$$").scale(1.5).set_z_index(100000).move_to(inr)

        inrr = CreateSR(inr).set_color(BLACK).scale(1.25)

        self.play(
            FadeIn(area),
            FadeIn(inr, inrr),
        )

        self.play(
            *[
                Succession(
                    Wait(distance(ORIGIN, d.get_center()) / 8),
                    FadeIn(d)
                )
                for d in dots
            ],
            area.area.animate.set_stroke_color(DARK_GRAY),
            area.dots.animate.set_color(DARK_GRAY),

            FadeOut(inr[0][-1], shift=UP * 0.75),
            FadeIn (inn[0][-1], shift=UP * 0.75),
        )

        fade_rect = get_fade_rect(opacity=1 - BIG_OPACITY / 1.1)

        ilp = Tex(r"\underline{Integer Linear Programming (ILP)}").scale(1.4).set_z_index(fade_rect.get_z_index() + 1)

        a = Tex("Is the problem easier or harder?").set_z_index(fade_rect.get_z_index() + 1)
        b = Tex("Can we still solve it efficiently?").set_z_index(fade_rect.get_z_index() + 1)

        VGroup(a, b).arrange(DOWN, buff=0.4)

        VGroup(ilp, VGroup(a, b)).arrange(DOWN, buff=1.5)

        align_object_by_coords(VGroup(a, b), a.get_center(), ORIGIN)
        VGroup(a, b).shift(DOWN * 0.5)
        VGroup(b).shift(DOWN * 0.2)

        self.play(
            AnimationGroup(
                FadeIn(fade_rect),
                FadeIn(ilp),
                lag_ratio=0.5,
            )
        )

        self.play(
            Write(a),
            run_time=1.5,
        )

        self.play(
            Write(b),
            run_time=1.5,
        )


class TransparentBinaryHint(MovingCameraScene):
    @fade
    def construct(self):
        a = Tex("$b_1$").set_z_index(1000000000)
        b = Tex(r"$1 \ge b_1$").set_z_index(1000000000)
        c = Tex(r"$b_1 \ge 0$").set_z_index(1000000000)

        d = Tex(r"$1 \ge b_1 \ge 0$")

        align_object_by_coords(b, b[0][2].get_center(), a[0][0].get_center())
        align_object_by_coords(c, c[0][0].get_center(), a[0][0].get_center())

        b.shift(DOWN * 0.7)
        c.shift(DOWN * 0.7 * 2)

        self.camera.frame.scale(0.5).move_to(VGroup(a, b, c))
        self.add(a, b, c)
        d.move_to(VGroup(a, b, c))

        sr = SurroundingRectangle(VGroup(a, b, c), fill_color=BLACK, stroke_color=WHITE, buff=0.35, fill_opacity=0.5)
        sr2 = SurroundingRectangle(d, fill_color=BLACK, stroke_color=WHITE, buff=0.35, fill_opacity=0.5)

        self.play(FadeIn(a, b, c, sr))

        self.play(
            Transform(sr, sr2),
            align_object_by_coords(a, a[0][0].get_center(), b[0][2].get_center(), animation=True),
            align_object_by_coords(c, c[0][0].get_center(), b[0][2].get_center(), animation=True),
        )



class Knapsack(MovingCameraScene):
    @fade
    def construct(self):
        seed(0xBADC0FFEE2)

        n = 8
        weights = [2 + i for i in range(n)]
        shuffle(weights)
        prices = [randint(1, 30) for _ in range(n)]

        title = Tex(r"\underline{Knapsack Problem}").scale(1.5)

        knapsack = ImageMobject("assets/midjourney/knapsack-out.png")\
                .set_height(title.get_height()).scale(1.2)

        knapsack.next_to(title, RIGHT, buff=0.3)

        title_plus_knapsack = Group(knapsack, title)

        title_plus_knapsack.next_to(config.top, DOWN, buff=1)

        self.play(
            AnimationGroup(
                Write(title, run_time=1),
                FadeIn(knapsack),
                lag_ratio=0.5,
            )
        )

        cols = color_gradient(["#FEBA33", "#CE6019", "#9A6354", "#FCA72B", "#86270A"], n)

        items = VGroup(
            *[VGroup(Dot().scale(w).set_color(cols[i]).set_sheen(0.5), Tex(f"${int(w)}$").scale(0.2 * w).set_z_index(1).set_color(BLACK)) for i, w in enumerate(weights)],
            *[Tex(f"${p}\\scriptstyle \$$").scale(1) for p in prices],
        ).arrange_in_grid(rows=2, cell_alignment=DOWN, buff=(0.2, 0.4)).align_to(DOWN).shift(DOWN * 0.7).scale(1.2)

        self.play(
            FadeIn(*[i[0] for i in items[:n]], lag_ratio=0.05),
            run_time=1,
        )

        self.play(
            FadeIn(*[i[1] for i in items[:n]], lag_ratio=0.05),
            run_time=1,
        )

        self.play(
            FadeIn(*[i for i in items[n:]], shift=DOWN * 0.1, lag_ratio=0.05),
            run_time=1,
        )

        bp = Tex(r"Given a O with carry weight $17\,\mathrm{kg}$, {\bf maximize price}.").scale(0.9)
        bp[0][6].set_opacity(0)

        bp.next_to(items.copy().shift(UP * 0.7), DOWN, buff=0.9)
        bpcp = knapsack.copy().scale(0.45).move_to(bp[0][6])

        k = Group(bp, bpcp)

        self.play(
            AnimationGroup(
                items.animate.shift(UP * 0.7),
                AnimationGroup(
                    Write(bp[0][:-15], run_time=1.5),
                    FadeIn(bpcp),
                ),
                lag_ratio=0.5,
            ),
        )

        self.play(
            Write(bp[0][-15:], run_time=1),
        )

        self.remove(bp, bpcp)
        self.add(k)

        # oof
        sol = solve_sack(prices, weights, 17)

        s = 0.9

        var = Tex("variables: $1 \ge b_1, b_2, b_3, b_4, b_5, b_6, b_7, b_8 \ge 0$").scale(s)

        for i in range(8):
            var[0][12 + 3 * i:12+2 + 3 * i].set_color(cols[i])

        var.next_to(items, UP, buff=0.35).shift(DOWN * 0.75)

        # NOTE: yes, weights hardcoded bad
        ineqs = Tex(r"""$$\begin{aligned}
              4b_1 + 2b_2 + 8b_3 + 3b_4 + 7b_5 + 5b_6 + 9b_7 + 6b_8  &\le 17
                \end{aligned}$$""").scale(s)
        for i in range(8):
            ineqs[0][1 + 4 * i:1+2 + 4 * i].set_color(cols[i])

        iq = Tex(r"subject to").set_opacity(MED_OPACITY).scale(0.75)
        ineqs = VGroup(iq, ineqs).arrange(DOWN, buff=0.15).move_to(ineqs)

        exp = Tex(r"$$\max\ 19b_1 + 17b_2 + 30b_3 + 13b_4 + 25b_5 + 29b_6 + 23b_7 + 10b_8$$").scale(s)
        for i in range(8):
            exp[0][5 + 5 * i:5+2 + 5 * i].set_color(cols[i])

        of = Tex(r"objective function").set_opacity(MED_OPACITY).scale(0.75)
        exp = VGroup(of, exp).arrange(DOWN, buff=0.15).move_to(exp)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    items.animate.shift(DOWN * 0.75),
                    k.animate.shift(DOWN * 0.45),
                ),
                FadeIn(var),
                lag_ratio=0.5,
            ),
        )

        ineqs.move_to(items[:n])

        exp.move_to(items[n:])

        self.play(
            AnimationGroup(
                AnimationGroup(
                    # weights
                    *[
                        Transform(
                            items[i][1],
                            ineqs[1][0][0 + 4 * i:0+1 + 4 * i],
                        )
                        for i in range(8)
                    ],
                    # balls
                    *[
                        Transform(
                            items[i][0],
                            ineqs[1][0][1 + 4 * i:1+2 + 4 * i],
                        )
                        for i in range(8)
                    ],
                    Transform(
                        k[0][0][22:22+2],
                        ineqs[1][0][-2:],
                    ),
                    FadeOut(k[0][0][:22]),
                    FadeOut(k[0][0][22+2:]),
                    FadeOut(k[1]),
                ),
                AnimationGroup(
                    FadeIn(ineqs[0]),
                    *[
                        FadeIn(
                            ineqs[1][0][3 + 4 * i:3+1 + 4 * i],
                        )
                        for i in range(7)
                    ],
                    FadeIn(ineqs[1][0][-3]),
                ),
                lag_ratio=.5,
            )
        )

        hls = VGroup(*[CreateHighlight(o) for o in [ ineqs[1][0][1:1+2], ineqs[1][0][5:5+2], ineqs[1][0][9:9+2], ineqs[1][0][13:13+2], ineqs[1][0][17:17+2], ineqs[1][0][21:21+2], ineqs[1][0][25:25+2], ineqs[1][0][29:29+2]]])
        hls2 = VGroup(*[CreateHighlight(o) for o in [ ineqs[1][0][0:0+3], ineqs[1][0][4:4+3], ineqs[1][0][8:8+3], ineqs[1][0][12:12+3], ineqs[1][0][16:16+3], ineqs[1][0][20:20+3], ineqs[1][0][24:24+3], ineqs[1][0][28:28+3]]])

        for obj in self.mobjects:
            self.remove(obj)
        self.add(title_plus_knapsack, var, ineqs, *[items[n+i] for i in range(8)])

        self.play(
            FadeIn(hls),

            ineqs[1][0][0].animate.set_opacity(BIG_OPACITY),
            ineqs[1][0][3:3+2].animate.set_opacity(BIG_OPACITY),
            ineqs[1][0][7:7+2].animate.set_opacity(BIG_OPACITY),
            ineqs[1][0][11:11+2].animate.set_opacity(BIG_OPACITY),
            ineqs[1][0][15:15+2].animate.set_opacity(BIG_OPACITY),
            ineqs[1][0][19:19+2].animate.set_opacity(BIG_OPACITY),
            ineqs[1][0][23:23+2].animate.set_opacity(BIG_OPACITY),
            ineqs[1][0][27:27+2].animate.set_opacity(BIG_OPACITY),
        )

        self.play(
            Transform(hls, hls2),

            ineqs[1][0][0:0+3].animate.set_opacity(1),
            ineqs[1][0][4:4+3].animate.set_opacity(1),
            ineqs[1][0][8:8+3].animate.set_opacity(1),
            ineqs[1][0][12:12+3].animate.set_opacity(1),
            ineqs[1][0][16:16+3].animate.set_opacity(1),
            ineqs[1][0][20:20+3].animate.set_opacity(1),
            ineqs[1][0][24:24+3].animate.set_opacity(1),
            ineqs[1][0][28:28+3].animate.set_opacity(1),
        )

        self.play(
            FadeOut(hls),
            ineqs[1][0].animate.set_opacity(1),
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    *[
                        FadeOut(items[n+i][0][-1:])
                        for i in range(8)
                    ],
                ),
                AnimationGroup(
                    *[
                        Transform(
                            items[n+i][0][:-1],
                            exp[1][0][3 + 5 * i:3+2 + 5 * i],
                        )
                        for i in range(8)
                    ],
                ),
                AnimationGroup(
                    FadeIn(exp[0]),
                    *[
                        FadeIn(
                            exp[1][0][5 + 5 * i:5+3 + 5 * i],
                        )
                        for i in range(8)
                    ],
                    FadeIn(exp[1][0][:3]),
                ),
                lag_ratio=.5,
            )
        )

        hls = VGroup(*[CreateHighlight(o) for o in [ exp[1][0][3:3+4], exp[1][0][8:8+4], exp[1][0][13:13+4], exp[1][0][18:18+4], exp[1][0][23:23+4], exp[1][0][28:28+4], exp[1][0][33:33+4], exp[1][0][38:38+4], ]])

        self.play(
            FadeIn(hls),
            exp[1][0][:3].animate.set_opacity(BIG_OPACITY),
            exp[1][0][7].animate.set_opacity(BIG_OPACITY),
            exp[1][0][12].animate.set_opacity(BIG_OPACITY),
            exp[1][0][17].animate.set_opacity(BIG_OPACITY),
            exp[1][0][22].animate.set_opacity(BIG_OPACITY),
            exp[1][0][27].animate.set_opacity(BIG_OPACITY),
            exp[1][0][32].animate.set_opacity(BIG_OPACITY),
            exp[1][0][37].animate.set_opacity(BIG_OPACITY),
        )

        self.play(
            FadeOut(hls),
            exp[1][0].animate.set_opacity(1),
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(title_plus_knapsack, var, ineqs, exp)

        var_s = Tex("variables: $1 \ge \mathbf{b} \ge 0$").move_to(var)
        var_s[0][12].set_color_by_gradient((cols[0], cols[2], cols[-1]))

        ineqs_s = Tex(r"""$$\begin{aligned}
              \text{weights} \cdot \mathbf{b} &\le \text{carry weight}
                \end{aligned}$$""").move_to(ineqs)
        ineqs_s[0][8].set_color_by_gradient((cols[0], cols[2], cols[-1]))
        iq = Tex(r"subject to").set_opacity(MED_OPACITY).scale(0.75)
        ineqs_s = VGroup(iq, ineqs_s).arrange(DOWN, buff=0.15).move_to(ineqs)
        align_object_by_coords(ineqs_s, ineqs_s[0].get_center(), ineqs[0].get_center())

        exp_s = Tex(r"$$\max\ \text{prices} \cdot \mathbf{b}$$").move_to(exp)
        exp_s[0][10].set_color_by_gradient((cols[0], cols[2], cols[-1]))
        of = Tex(r"objective function").set_opacity(MED_OPACITY).scale(0.75)
        exp_s = VGroup(of, exp_s).arrange(DOWN, buff=0.15)
        align_object_by_coords(exp_s, exp_s[0].get_center(), exp[0].get_center())

        self.play(
            Transform(var[0][:12], var_s[0][:12]),
            Transform(var[0][12:-2], var_s[0][12:-2]),
            Transform(var[0][-2:], var_s[0][-2:]),

            Transform(
                VGroup(
                    ineqs[1][0][1:1+2],
                    ineqs[1][0][5:5+2],
                    ineqs[1][0][9:9+2],
                    ineqs[1][0][13:13+2],
                    ineqs[1][0][17:17+2],
                    ineqs[1][0][21:21+2],
                    ineqs[1][0][25:25+2],
                    ineqs[1][0][29:29+2],
                ),
                ineqs_s[1][0][8],
            ),
            Transform(
                ineqs[1][0][-3],
                ineqs_s[1][0][-12],
            ),
            Transform(
                ineqs[1][0][-3:],
                ineqs_s[1][0][-12:],
            ),
            Transform(
                VGroup(
                    ineqs[1][0][0],
                    ineqs[1][0][3:3+2],
                    ineqs[1][0][7:7+2],
                    ineqs[1][0][11:11+2],
                    ineqs[1][0][15:15+2],
                    ineqs[1][0][19:19+2],
                    ineqs[1][0][23:23+2],
                    ineqs[1][0][27:27+2],
                ),
                ineqs_s[1][0][:8],
            ),

            Transform(
                exp[1][0][:3],
                exp_s[1][0][:3],
            ),
            Transform(
                VGroup(
                    exp[1][0][5:5+2],
                    exp[1][0][10:10+2],
                    exp[1][0][15:15+2],
                    exp[1][0][20:20+2],
                    exp[1][0][25:25+2],
                    exp[1][0][30:30+2],
                    exp[1][0][35:35+2],
                    exp[1][0][40:40+2],
                ),
                exp_s[1][0][-1],
            ),
            Transform(
                VGroup(
                    exp[1][0][3:3+2],
                    exp[1][0][7:7+3],
                    exp[1][0][12:12+3],
                    exp[1][0][17:17+3],
                    exp[1][0][22:22+3],
                    exp[1][0][27:27+3],
                    exp[1][0][32:32+3],
                    exp[1][0][37:37+3],
                ),
                exp_s[1][0][3:3+7],
            ),
        )

        for o in self.mobjects:
            self.remove(o)

        self.add(exp_s, ineqs_s, var_s, title_plus_knapsack)

        g = VGroup(var_s, ineqs_s, exp_s).set_z_index(10)

        code = MyCode("code/knapsack.py").scale(0.52).next_to(title_plus_knapsack, DOWN)

        gcp = g.copy().scale(0.4).align_to(code, RIGHT + UP).shift(LEFT * 0.2 + DOWN * 0.2)
        bg = SurroundingRectangle(gcp, buff=0.2, corner_radius=0.1, color=WHITE, fill_opacity=0)

        self.play(
            AnimationGroup(
                Transform(g, gcp),
                AnimationGroup(
                    FadeIn(code.background_mobject),
                    FadeIn(bg),
                ),
                lag_ratio=0.5,
            ),
        )

        self.play(
            FadeIn(code.code[0], run_time=0.7)
        )

        self.play(
            AnimationGroup(
                FadeIn(code.code[3]),
                FadeIn(code.code[4]),
                FadeIn(code.code[5]),
                FadeIn(code.code[6]),
                FadeIn(code.code[7]),
                lag_ratio=0.05,
                run_time=1.5,
            ),
        )

        sr = CreateHighlight(code.code[12])
        sr2 = CreateHighlight(var_s)

        self.play(
            AnimationGroup(
                FadeIn(code.code[9]),
                FadeIn(code.code[10]),
                FadeIn(code.code[12]),
                FadeIn(code.code[14]),
                FadeIn(code.code[16]),
                lag_ratio=0.05,
                run_time=1.5,
            ),
            Succession(
                Wait(0.5),
                AnimationGroup(
                    FadeIn(sr), FadeIn(sr2)
                ),
            ),
        )

        self.play(
            Transform(sr, CreateHighlight(code.code[14])),
            Transform(sr2, CreateHighlight(ineqs_s)),
        )
        self.play(
            Transform(sr, CreateHighlight(code.code[16])),
            Transform(sr2, CreateHighlight(exp_s)),
        )

        self.play(
            FadeOut(sr),
            FadeOut(sr2),
            AnimationGroup(
                FadeIn(code.code[18]),
                FadeIn(code.code[19]),
                FadeIn(code.code[20]),
                FadeIn(code.code[21]),
                lag_ratio=0.05,
                run_time=1.5,
            ),
        )

        outknap = MyCode("code/knapsack.out").scale(0.56).next_to(code, DOWN).align_to(code, LEFT).set_z_index(code.get_z_index() - 0.1)

        self.play(
            FadeIn(outknap, shift=DOWN),
            self.camera.frame.animate.move_to(VGroup(code, title, outknap)).scale(1.05),
        )

        hl = CreateHighlight(outknap.code[0][-4:])

        self.play(
            FadeIn(hl),
        )

        self.play(Transform(hl, CreateHighlight(outknap.code[0][-4:])))
        self.play(Transform(hl, CreateHighlight(outknap.code[1][10:10+3])))
        self.play(Transform(hl, CreateHighlight(outknap.code[1][18:18+3])))
        self.play(Transform(hl, CreateHighlight(outknap.code[1][22:22+3])))
        self.play(Transform(hl, CreateHighlight(outknap.code[1][26:26+3])))

        self.play(FadeOut(hl))

        fade_rect = get_fade_rect()

        text1 = Tex(r"NP-hard in \textit{theory}...").set_z_index(fade_rect.get_z_index() + 1)
        text2 = Tex(r"Very fast in \textit{practice}!").set_z_index(fade_rect.get_z_index() + 1)

        VGroup(text1, text2).arrange(DOWN, buff=0.3).move_to(code).scale(1.5)

        self.play(
            AnimationGroup(
                FadeIn(fade_rect),
                Write(text1, run_time=1.5),
                lag_ratio=0.5,
            )
        )

        self.play(
            Write(text2, run_time=1.5),
        )

        self.play(
            FadeOut(text1),
            FadeOut(text2),
            FadeOut(fade_rect),
        )

        farmer_title = Tex(r"\underline{Farmer's Problem}").scale(1.5)
        farmer = ImageMobject("assets/midjourney/farmer-outline.png").set_z_index(10).set_height(0.9)

        g = Group(farmer_title, farmer).arrange(buff=0.3)
        g.move_to(title_plus_knapsack).shift(RIGHT * self.camera.frame.width)
        code2 = MyCode("code/farmer.py").scale(0.56).move_to(code).shift(RIGHT * self.camera.frame.width)

        outfarm = MyCode("code/farmer.out").scale(0.56).next_to(code2, DOWN).align_to(code2, LEFT).set_z_index(code2.get_z_index() - 0.1)

        self.add(g)
        self.add(code2)
        self.add(outfarm)

        self.play(
            self.camera.frame.animate.shift(RIGHT * self.camera.frame.width),
            run_time=1.5,
        )


class RollTest(MovingCameraScene):
    @fade
    def construct(self):

        def sheen_updater(obj, dt):
            v = obj.get_sheen_direction()
            d = Dot().move_to(v).rotate_about_origin(PI / 30)
            obj.set_sheen_direction(d.get_center())

        d = Dot().scale(10).set_color(ORANGE).set_sheen(0.3)
        d.add_updater(sheen_updater)
        self.add(d)

        self.play(d.animate.shift(LEFT))


class TexTest(MovingCameraScene):
    @fade
    def construct(self):
        self.add(Tex("a \par b"))
        self.wait()


class Flows(MovingCameraScene):
    @fade
    def construct(self):
        with open("assets/g.txt") as f:
            graph = parse_graph(f.read())

        self.camera.frame.scale(0.9)

        start = Tex("\\bf start").next_to(graph.vertices[11], DOWN, buff=0.35).align_to(graph.vertices[11], RIGHT)
        start.add(Tex("\\bf ($\\mathbf{v}_1$)").next_to(start, DOWN, buff=0.1).scale(0.8))
        end = Tex("\\bf end").next_to(graph.vertices[14], DOWN, buff=0.35).align_to(graph.vertices[14], LEFT)
        end.add(Tex("\\bf ($\\mathbf{v}_m$)").next_to(end, DOWN, buff=0.1).scale(0.8))

        seed(0xDEADBEEF2)

        def get_weight(edge, weight, flow=None):
            val = str(weight) if flow is None else f"{flow}/{weight}"

            weight = Tex(val, color=BLACK).move_to(edge).scale(0.45).set_z_index(10)
            sr = SurroundingRectangle(weight, color=WHITE, fill_opacity=1, corner_radius=0.05, buff=0.05).move_to(weight).set_z_index(9)
            weight.add(sr)

            if flow is not None:
                weight[0][:len(str(flow))].set_color(DARK_BLUE)

            return weight

        weights = {}
        weights_vgroup = VGroup()
        for edge in graph.edges:
            weights[edge] = randint(5, 20)
            weights_vgroup.add(get_weight(graph.edges[edge], weights[edge]))

        for vertex in graph.vertices:
            graph.vertices[vertex].scale(1.5)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeIn(graph),
                    FadeIn(weights_vgroup),
                ),
                AnimationGroup(
                    FadeIn(start),
                    FadeIn(end),
                ),
                lag_ratio=0.5,
            ),
        )

        G = nx.DiGraph()
        for x, y in graph.edges:
            G.add_edge(x, y, capacity=weights[(x, y)])

        flow_value, flow_dict = nx.maximum_flow(G, 11, 14)
        used_vertices = set()
        for edge in graph.edges:
            if flow_dict[edge[0]][edge[1]] > 0:
                used_vertices.add(edge[0])
                used_vertices.add(edge[1])

        new_weights_group = VGroup()
        new_weights_group_dict = {}
        for edge in graph.edges:
            new_weights_group_dict[edge] = get_weight(graph.edges[edge], weights[edge], flow=flow_dict[edge[0]][edge[1]]).scale(0.8)
            new_weights_group.add(new_weights_group_dict[edge])

        self.play(
            *[
                AnimationGroup(
                    AnimationGroup(
                        Transform(a[0], b[0][len(str(flow_dict[e[0]][e[1]])) + 1:]),
                        Transform(a[1], b[1]),
                    ),
                    FadeIn(b[0][:len(str(flow_dict[e[0]][e[1]])) + 1]),
                    lag_ratio=0.5,
                )
                for a, b, e in zip(weights_vgroup, new_weights_group, graph.edges)
            ],
        )

        for o in self.mobjects:
            self.remove(o)

        self.add(start, end, graph, new_weights_group)

        self.camera.frame.save_state()

        v = 9

        for edge in graph.edges:
            graph.edges[edge].save_state()
            new_weights_group_dict[edge].save_state()

        for vertex in graph.vertices:
            graph.vertices[vertex].save_state()

        move_group = VGroup(graph.vertices[v])
        for edge in graph.edges:
            if v in edge:
                move_group.add(new_weights_group_dict[edge])

        in_values = []
        out_values = []
        in_values_edges = []
        out_values_edges = []

        for edge in graph.edges:
            if v == edge[1]:
                in_values.append(flow_dict[edge[0]][edge[1]])
                in_values_edges.append(edge)
            elif v == edge[0]:
                out_values.append(flow_dict[edge[0]][edge[1]])
                out_values_edges.append(edge)

        eq = Tex("$" + "+".join(list(map(str, in_values))) + "=" + "+".join(list(map(str, out_values))) + "$")\
                .scale(0.6).next_to(graph.vertices[v], UP)

        # NOTE: change if v changes
        eq[0][0].set_color(BLUE)
        eq[0][2].set_color(BLUE)
        eq[0][4].set_color(BLUE)
        eq[0][6].set_color(BLUE)

        self.play(
            self.camera.frame.animate.move_to(VGroup(move_group, eq)).scale(0.4),
            *[
                AnimationGroup(
                    graph.edges[edge].animate.set_color(BIG_COLOR),
                    new_weights_group_dict[edge][0].animate.set_opacity(BIG_OPACITY),
                    new_weights_group_dict[edge][1].animate.set_color(BIG_COLOR),
                )
                for edge in graph.edges
                if edge[0] != v and edge[1] != v
            ],
            *[
                graph.vertices[vertex].animate.set_color(BIG_COLOR)
                for vertex in graph.vertices
                if vertex != v
            ],
        )

        c1 = new_weights_group_dict[in_values_edges[0]][0][0][0].copy()
        c2 = new_weights_group_dict[in_values_edges[1]][0][0][0].copy()
        c3 = new_weights_group_dict[out_values_edges[0]][0][0][0].copy()
        c4 = new_weights_group_dict[out_values_edges[1]][0][0][0].copy()

        self.play(
            AnimationGroup(
                AnimationGroup(
                    # NOTE: change when v changes
                    Transform(c1, eq[0][0]),
                    Transform(c2, eq[0][2]),
                    Transform(c3, eq[0][4]),
                    Transform(c4, eq[0][6]),
                ),
                AnimationGroup(
                    # NOTE: change when v changes
                    FadeIn(eq[0][1]),
                    FadeIn(eq[0][3]),
                    FadeIn(eq[0][5]),
                ),
                lag_ratio=0,
            ),
        )

        self.play(
            self.camera.frame.animate.restore(),
            FadeOut(c1, c2, c3, c4),
            FadeOut(eq),
            *[
                AnimationGroup(
                    graph.edges[edge].animate.restore(),
                    new_weights_group_dict[edge].animate.restore(),
                )
                for edge in graph.edges
                if edge[0] != v and edge[1] != v
            ],
            *[
                graph.vertices[vertex].animate.restore()
                for vertex in graph.vertices
                if vertex != v
            ],
        )

        for edge in graph.edges:
            angle = graph.edges[edge].get_normal_vector()

            graph.edges[edge].set_sheen_direction(-angle)

        self.play(
            *[
                graph.edges[edge].animate.set_stroke_width(weights[edge])\
                        .set_color_by_gradient([WHITE] * (weights[edge] - flow_dict[edge[0]][edge[1]]) + [BLUE] * flow_dict[edge[0]][edge[1]])\
                for edge in graph.edges
            ],
            *[
                weight.animate.scale(0.2).set_opacity(0)
                for weight in new_weights_group
            ],
            *[
                graph.vertices[vertex].animate.set_color(BLUE)
                for vertex in used_vertices
            ],
        )

        primal = VGroup(
            Tex("\\bf Primal (max-flow)").scale(1.5),
            VGroup(
                Tex("variables: $x_{u,v}$ for edges, $z$ for flow"),
                Tex(r"objective function: $\max z$"),
            ).arrange(DOWN, buff=0.35),
            Tex(r"""$$
\begin{aligned}
\sum_{u, v \in E} x_{u,v} - \sum_{v,u \in E} x_{v,u} &= \begin{cases}\phantom{-}z & u=1\\ -z & u=m \\ \phantom{-}0 & \text{otherwise}\end{cases}\\
x_{u,v} &\le k_{u,v} \\
x_{u,v} &\ge 0 \\
\end{aligned}
                $$"""),
        ).scale(0.8).arrange(DOWN, buff=0.5)

        primal[0][0][:6].set_color(BLUE)

        dual = VGroup(
            Tex("\\bf Dual (min-cut)").scale(1.5),
            VGroup(
                Tex("variables: $w_{u,v}$ for edges, $y_{u,v}$ for vertices"),
                Tex(r"objective function: $\min \sum_{u, v \in E} k_{u,v} w_{u,v}$"),
            ).arrange(DOWN, buff=0.35),
            Tex(r"""$$
\begin{aligned}
y_u - y_v + w_{u, v} &\ge 0 \\
y_m - y_1 &\ge 1 \\
w_{u,v} &\ge 0 \\
\end{aligned}
                $$"""),
        ).scale(0.8).arrange(DOWN, buff=0.5)

        dual[0][0][:4].set_color(ORANGE)

        g = VGroup(primal.copy(), dual).arrange(RIGHT, buff=2).next_to(graph, DOWN, buff=1)

        primal.move_to(g)
        dual.align_to(primal, UP)

        self.play(
            self.camera.frame.animate.move_to(Group(graph, primal)).set_height(Group(graph, primal).get_height() * 1.2),
            FadeIn(primal),
        )

        cut_value, partition = nx.minimum_cut(G, 11, 14)

        self.play(
            AnimationGroup(
                Transform(primal, g[0]),
                FadeIn(dual),
                lag_ratio=0.5,
            ),
        )

        cut_edges = []
        for edge in graph.edges:
            if edge[0] in partition[0] and edge[1] in partition[1]:
                cut_edges.append(edge)

        line = Line(
            graph.edges[cut_edges[0]].get_center(),
            graph.edges[cut_edges[1]].get_center(),
            stroke_width=5,
        ).scale(1.5).set_color(ORANGE).shift((UP + LEFT) * 0.1)  # to look nicer

        self.play(
            AnimationGroup(
                AnimationGroup(
                    *[
                        graph.edges[edge].animate.set_stroke_width(weights[edge])\
                                .set_color_by_gradient(ORANGE)\
                                .set_opacity(BIG_OPACITY)\
                        for edge in graph.edges
                        if edge[0] in partition[0] and edge[1] in partition[1]
                    ],
                    *[
                        graph.edges[edge].animate.set_stroke_width(weights[edge])\
                                .set_color(LIGHT_ORANGE)\
                        for edge in graph.edges
                        if edge[0] in partition[0] and edge[1] in partition[0]
                    ],
                    *[
                        graph.edges[edge].animate.set_stroke_width(weights[edge])\
                                .set_color(DARK_ORANGE)\
                        for edge in graph.edges
                        if edge[0] in partition[1] and edge[1] in partition[1]
                    ],
                    *[
                        graph.vertices[vertex].animate.set_color(LIGHT_ORANGE)
                        for vertex in graph.vertices
                        if vertex in partition[0]
                    ],
                    *[
                        graph.vertices[vertex].animate.set_color(DARK_ORANGE)
                        for vertex in graph.vertices
                        if vertex in partition[1]
                    ],
                ),
                Create(line),
                lag_ratio=0.5,
            ),
        )


class Outro(MovingCameraScene):
    @fade
    def construct(self):
        text = Tex(r"\underline{What we've covered}").scale(1.5).shift(UP * 2)
        text_scale = 0.8
        subtext_scale = 0.65

        a = Rectangle(width=1.6, height=0.9, fill_color=BLACK)
        b = Rectangle(width=1.6, height=0.9, fill_color=BLACK)
        c = Rectangle(width=1.6, height=0.9, fill_color=BLACK)

        g = VGroup(a, b, c).arrange(buff=0.3).set(width = self.camera.frame.width * 0.85)

        at = Tex("Simplex Method").scale(text_scale).next_to(a, DOWN)
        bt = Tex("Duality").scale(text_scale).next_to(b, DOWN)
        ct = Tex("Integer LP").scale(text_scale).next_to(c, DOWN)

        att = VGroup(
            Tex(r"\it Initial solution?").scale(subtext_scale),
            Tex(r"\it Exponential?").scale(subtext_scale),
            Tex(r"\it Infinite loop?").scale(subtext_scale),
        ).arrange(DOWN, buff=0.15).next_to(at, DOWN, buff=0.3).set_color(RED)
        att[2].shift(UP * 0.05)

        btt = VGroup(
            Tex(r"\it General conversion?").scale(subtext_scale),
            Tex(r"\it Fast algorithms?").scale(subtext_scale),
        ).arrange(DOWN, buff=0.15).next_to(bt, DOWN, buff=0.3).set_color(RED)
        ctt = VGroup(
            Tex(r"\it Fast classes?").scale(subtext_scale),
            Tex(r"\it Fast algorithms?").scale(subtext_scale),
        ).arrange(DOWN, buff=0.15).next_to(ct, DOWN, buff=0.3).set_color(RED)

        self.play(FadeIn(text))

        self.play(FadeIn(a, at))
        self.play(Succession(Wait(0.25), FadeIn(b, bt)))

        self.play(Succession(Wait(0.25), FadeIn(c, ct)))

        self.play(FadeIn(att[0]))
        self.play(FadeIn(att[1]))
        self.play(FadeIn(att[2]))
        self.play(FadeIn(btt[0]))
        self.play(FadeIn(btt[1]))
        self.play(FadeIn(ctt[0]))
        self.play(FadeIn(ctt[1]))

        ineqs = []
        ipts = [
            [(-2, 4), (2, 4), "<="],
            [(2, 4), (5, 1), "<="],
            [(5, 1), (5, -2), "<="],
            [(5, -2), (4, -9), ">="],
            [(4, -9), (3, -12), ">="],
            [(3, -12), (1, -13), ">="],
            [(1, -13), (0, -13), ">="],
            [(0, -13), (-2, -12), ">="],
            [(-2, -12), (-4, -10), ">="],
            [(-4, -10), (-5, -2), ">="],
            [(-5, -2), (-4, 1), "<="],
            [(-4, 1), (-2, 4), "<="],
        ]

        area = FeasibleArea2D()

        for p1, p2, op in ipts:
            a_, b_, c_ = Inequality2D.points_to_slope(p1, p2)
            iq = Inequality2D(a_, b_, op, c_)
            ineqs.append(iq)

        area.add_inequalities(ineqs)

        for d in area.dots:
            d.scale(2)

        self.add(area)
        area.scale(0.8, about_point=ORIGIN)
        area.shift(DOWN * 4)
        area.set_opacity(0)

        for ineq in ineqs:
            ineq.scale(0.8, about_point=ORIGIN)
            ineq.shift(DOWN * 4)

        vt = ValueTracker()

        def updater(obj):
            if abs(vt.get_value()) <= 0.01:
                return

            obj._update_area()
            obj.set_color(BLUE)
            obj.fade(1 - vt.get_value())

        water = Inequality2D(0, 1, ">=", 0).set_color(BLUE)

        pengling = SVGMobject("assets/pengling/pengling.svg").set_height(1.25).next_to(area, UP, buff=0).shift(LEFT * 1 + DOWN * 0.17).set_z_index(10000000)

        area.add_inequalities([water])

        water.set_opacity(0)
        self.add(water)

        area.add_updater(updater)

        atc = at.copy()
        btc = bt.copy()
        ctc = ct.copy()

        compressed = VGroup(
            atc,
            VGroup(btc, ctc).arrange(buff=0.35),
        ).arrange(DOWN, buff=0.3).scale(0.7).move_to(bt).shift(RIGHT * 0.1)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(a),
                    FadeOut(b),
                    FadeOut(c),
                    att.animate.shift(DOWN * 5 + RIGHT * 2),
                    btt.animate.shift(DOWN * 5),
                    ctt.animate.shift(DOWN * 5 + LEFT * 2),
                ),
                AnimationGroup(
                    Transform(at, atc),
                    Transform(bt, btc),
                    Transform(ct, ctc),
                    water.animate.shift(DOWN * 2).set_opacity(1),
                    Succession(
                        Wait(0.5),
                        FadeIn(pengling, run_time=1),
                    ),
                    vt.animate.set_value(1),
                    run_time=1.5,
                    #run_time=0.2,
                ),
                lag_ratio=0.75,
            )
        )

        self.remove(att, btt, ctt)

        area.remove_updater(updater)
        area.remove_inequalities([water], update=False)

        def updater(obj):
            obj._update_area()
            obj.set_color(DARK_BLUE)

        a2 = deepcopy(area)
        area.dots.set_z_index(10000000)
        wi = deepcopy(water)
        wi.operation = "<="
        a2.add_inequalities([wi, water])
        a2.add_updater(updater)

        w = water.copy().set_z_index(10000)
        self.add(w)

        self.add(a2)

        sq = get_infinite_square(opacity=0.1).align_to(water, UP).set_z_index(0)

        water.set_opacity(BIG_OPACITY)

        self.camera.frame.save_state()

        seed(0xdead)

        q = 4

        text2 = [
            ("Other LP variants", -1, 0),
            ("Computational complexity", 1.15, 0),
            ("Unboundedness", -2, 0.5),
            ("Relaxation", -0.4, 0),
            ("Complementary slackness", 1.1, 0),
            ("Primal-dual algorithms", -2.2, 0.3),
            ("Pivot rules", 0.8, 0.2),
            ("Ellipsoid method", -0.2, 0),
            ("Interior path method", -1.8, 0),
            ("Total unimodularity", 1, 0.3),
            ("Gomory's cuts", -0.7, 0),
        ]

        texts = VGroup(
            *[
                Tex(t).scale(0.5).set_z_index(100000000000).set_opacity(0.9 - i / len(text2) * 0.85)
                for i, (t, _, _) in enumerate(text2)
            ]
        ).arrange(DOWN, buff=0.55).next_to(w, DOWN, buff=0.75)

        for i in range(len(text2)):
            texts[i].shift(text2[i][1] * RIGHT)

            if text2[i][2] != 0:
                texts[i:].shift(UP * text2[i][2])

        # XD
        sq = ineqs[0].get_half_plane().rotate(PI, about_point=ineqs[0].get_center())
        for i in ineqs[1:]:
            sq = Union(sq, i.get_half_plane().rotate(PI, about_point=i.get_center()))
        sq = Intersection(sq, w.get_half_plane().rotate(PI, about_point=w.get_center()), color=BLUE, fill_opacity=BIG_OPACITY, stroke_width=0).set_z_index(0)

        self.play(
            Succession(
                Wait(0.5),
                FadeIn(sq, run_time=1.5),
            ),
            Succession(
                Wait(0.2),
                AnimationGroup(*[Succession(Wait(0.07 * i), FadeIn(t)) for i, t in enumerate(texts)]),
            ),
            FadeOut(text),
            self.camera.frame.animate.shift(DOWN * 4).scale(1.45),
            water.animate.shift(DOWN * 8),
            #run_time=0.2,
            run_time=2,
        )

        a2.remove_updater(updater)

        tfw = Tex("Thanks for watching!").scale(1.75)
        tfw.align_to(self.camera.frame, UP).shift(UP * 0.5)

        self.play(
            self.camera.frame.animate.restore(),
            FadeOut(texts),
            FadeOut(at, bt, ct),
            Succession(
                Wait(1),
                Write(tfw, run_time=1.5),
            ),
            run_time=1.5,
        )
