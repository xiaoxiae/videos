from manim import *
from utilities import *


class Intro(MovingCameraScene):
    @fade
    def construct(self):
        with open("funf.c") as f:
            contents = f.read()

        q = Tex(r"\underline{How does it work?}").scale(1.15)

        code = MyCode(contents)

        q.next_to(code, UP, buff=1)

        g = VGroup(q, code)

        self.camera.frame.set_width(g.width * 1.4).move_to(g)

        self.play(
            Write(q, run_time=1),
            FadeIn(code),
        )

        sr = CreateHighlightCodeLines(code, [12, 13, 14, 15, 16, 17, 18], offset=0)
        sr_orig = sr.copy()

        sr.save_state()

        # self.play(Transform(sr, CreateHighlightCodeLine(code, 15, start=10)))
        sr.become(CreateHighlightCodeLine(code, 15, start=10))

        with open("funf.out") as f:
            contents = f.read()

        brace = BraceBetweenPoints(Dot().next_to(sr, LEFT, buff=-0.1).get_center(), Dot().next_to(sr, RIGHT, buff=-0.1).get_center(), direction=UP).next_to(sr, UP, buff=0)
        output = MyCode(contents).code.next_to(brace, UP).scale(1.5)

        sr = CreateHighlightObject(VGroup(brace, output, sr_orig))

        self.play(
            AnimationGroup(
                #Transform(sr, CreateHighlightObject(VGroup(CreateHighlightObject(VGroup(brace, output)), sr))),
                FadeIn(sr),
                FadeIn(output, shift=UP * 0.1),
                FadeIn(brace, shift=UP * 0.1),
            )
        )

        self.play(
            Transform(sr, CreateHighlightCodeLines(code, [2, 3, 4, 5, 6, 7, 8, 9, 10], offset=0)),
        )

        self.play(
            Transform(sr, CreateHighlightCodeLine(code, 4, start=2)),
        )

        self.play(
            Transform(sr, CreateHighlightCodeLines(code, [5, 6, 7, 8], offset=4)),
        )

        self.play(
            Transform(sr, CreateHighlightCodeLine(code, 9, start=2)),
        )

        x, y = MyCodeKindaTho("111101"), MyCodeKindaTho("11001")

        orig_color = x.code[0][0].color

        numbers = [
            (MyCodeKindaTho("100100"), MyCodeKindaTho("110010")),
            (MyCodeKindaTho("10110"), MyCodeKindaTho("1000000")),
            (MyCodeKindaTho("1010110"), MyCodeKindaTho("0000000")),
        ]

        sum = MyCodeKindaTho("x = sum").scale(0.75)
        carry = MyCodeKindaTho("y = carry").scale(0.75)

        table = Table(
            [
                [x],
                [y],
                [numbers[0][0]],
                [numbers[0][1]],
            ],
            arrange_in_grid_config={"col_alignments": "rr"},
            v_buff=0.4, h_buff=0.65,
            element_to_mobject = lambda x: x,
            row_labels=[
                code.code[2][10].copy(),
                code.code[2][17].copy(),
                code.code[6][7:-1].copy(),
                code.code[7][6:].copy()
            ],
        ).move_to(self.camera.frame)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(sr),
                    FadeOut(code),
                    FadeOut(code.code[-1]),
                    FadeOut(code.code[-2]),
                    FadeOut(code.code[15][18:]),
                    FadeOut(code.code[15][14]),
                    FadeOut(code.code[15][15]),
                    FadeOut(brace),
                    FadeOut(output),
                    FadeOut(q),
                ),
                AnimationGroup(
                    ReplacementTransform(code.code[2][10], table.get_row_labels()[0]),
                    ReplacementTransform(code.code[2][17], table.get_row_labels()[1]),
                    ReplacementTransform(code.code[6][7:-1], table.get_row_labels()[2]),
                    ReplacementTransform(code.code[7][6:], table.get_row_labels()[3]),
                    ReplacementTransform(code.code[15][12:14], x),
                    ReplacementTransform(code.code[15][16:18], y),
                ),
                lag_ratio=0.75,
            )
        )

        xor = table.get_entries((-1, 2))

        indexes = [0, 3]
        color_anim = []
        x.save_state()
        y.save_state()
        xor.save_state()

        for i in range(len(x.code[0])):
            color = RED if i not in indexes else GREEN

            color_anim.append(x.code[0][i].animate.set_color(color))
            xor.code[0][i].set_color(color)

            if i != 0:
                color_anim.append(y.code[0][i - 1].animate.set_color(color))

        h = CreateHighlightObject(table.get_row_labels()[2])

        self.play(
            FadeIn(h)
        )

        self.play(
            *color_anim,
            FadeIn(xor),
            Circumscribe(xor, color=WHITE),
        )

        self.play(
            x.animate.restore(),
            y.animate.restore(),
            xor.animate.restore(),
            Transform(h, CreateHighlightObject(table.get_row_labels()[3][1:6])),
        )

        indexes = [1, 2, 5]
        color_anim = []
        x.save_state()
        y.save_state()

        andd = table.get_entries((0, 2))
        andd.save_state()
        andd.code[0][-1].set_opacity(0)

        pos = andd.code[0][:-1].get_center()

        andd.code[0][:-1].align_to(andd.code[0][-1], RIGHT)

        andd.code[0][-1].save_state()

        for i in range(len(x.code[0])):
            color = RED if i not in indexes else GREEN

            color_anim.append(x.code[0][i].animate.set_color(color))
            andd.code[0][i-1].set_color(color)

            if i != 0:
                color_anim.append(y.code[0][i - 1].animate.set_color(color))

        self.play(
            *color_anim,
            FadeIn(andd),
            Circumscribe(andd, color=WHITE),
        )

        andd.code[0][-1].restore()

        self.play(
            AnimationGroup(
                Transform(h, CreateHighlightObject(table.get_row_labels()[3][8:])),
                AnimationGroup(
                    andd.code[0][:-1].animate.move_to(pos),
                    andd.code[0][-1].animate.set_opacity(1),
                ),
                lag_ratio=0.75,
            )
        )

        self.play(
            x.animate.restore(),
            y.animate.restore(),
            andd.animate.restore(),
        )

        table.get_row_labels().save_state()

        sum.move_to(table.get_row_labels()[2]).align_to(table.get_row_labels()[2], RIGHT)
        carry.move_to(table.get_row_labels()[3]).align_to(table.get_row_labels()[3], RIGHT)

        g = VGroup(
            table.get_entries((0, 2)),
            table.get_entries((-1, 2)),
            table.get_entries((-2, 2)),
            table.get_entries((-3, 2)),
        )

        plus = MyCodeKindaTho("+").move_to(table.get_entries((-2, 2))).next_to(table.get_entries((-2, 2)).code[0][1:], LEFT, buff=0.3).set_color(WHITE)

        self.play(
            FadeOut(h),
            FadeOut(table.get_row_labels()),
            self.camera.frame.animate.set_width(g.width * 2).move_to(g),
        )

        c = (table.get_entries((-1, 2)).get_center() + table.get_entries((-2, 2)).get_center()) / 2

        line = Line(
            Dot().move_to(c).align_to(table.get_entries((-3, 2)), LEFT).get_center(),
            Dot().move_to(c).align_to(table.get_entries((-3, 2)), RIGHT).get_center(),
            stroke_width=2,
        ).scale(1.25)

        self.play(
            AnimationGroup(
                Create(line),
                FadeIn(plus),
                lag_ratio=0.25,
            )
        )

        sum.next_to(table.get_entries((-1, 2)), DOWN, buff=0.1).align_to(table.get_entries((-2, 2)), RIGHT)
        sum.code[0][:3].set_color(WHITE)
        sum.code[0][3:].set_color(GREEN)
        sum.code[0][2].scale(0.7).next_to(sum.code[0][4], LEFT, buff=0.08)
        sum.code[0][0].scale(0.7).next_to(sum.code[0][2], LEFT, buff=0.08)

        carry.next_to(table.get_entries((0, 2)), DOWN, buff=0.1).align_to(table.get_entries((-2, 2)), RIGHT)
        carry.code[0][:3].set_color(WHITE)
        carry.code[0][3:].set_color(ORANGE)
        carry.code[0][2].scale(0.7).next_to(carry.code[0][4], LEFT, buff=0.08)
        carry.code[0][0].scale(0.7).next_to(carry.code[0][2], LEFT, buff=0.08).shift(DOWN * 0.03)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    xor.animate.set_color(GREEN),
                    x.code[0][0].animate.set_color(GREEN),
                    x.code[0][3].animate.set_color(GREEN),
                    y.code[0][2].animate.set_color(GREEN),
                ),
                FadeIn(sum, shift=DOWN * 0.1),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    andd.code[0][:-1].animate.set_color(ORANGE),
                    x.code[0][1].animate.set_color(ORANGE),
                    x.code[0][2].animate.set_color(ORANGE),
                    y.code[0][0].animate.set_color(ORANGE),
                    y.code[0][1].animate.set_color(ORANGE),
                    y.code[0][-1].animate.set_color(ORANGE),
                    x.code[0][-1].animate.set_color(ORANGE),
                ),
                FadeIn(carry, shift=DOWN * 0.1),
                lag_ratio=0.5,
            )
        )

        a, b = numbers[1]
        a.set_z_index(1)
        b.set_z_index(1)

        a.move_to(numbers[0][0]).align_to(numbers[0][0], RIGHT)
        b.move_to(numbers[0][1]).align_to(numbers[0][1], RIGHT)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(x),
                    FadeOut(y),
                    sum.animate.set_opacity(0.25),
                    carry.animate.set_opacity(0.25),
                ),
                AnimationGroup(
                    numbers[0][0].animate.move_to(x).align_to(x, RIGHT).set_color(orig_color),
                    numbers[0][1].animate.move_to(y).align_to(y, RIGHT).set_color(orig_color),
                    plus.animate.shift(0.2 * LEFT),
                    self.camera.frame.animate.move_to(VGroup(plus.copy().shift(0.2 * LEFT), x, y, numbers[0][0], numbers[0][1])).scale(1.1),
                ),
                lag_ratio=0.5,
            )
        )

        a.set_color(GREEN)
        b.code[0][:-1].set_color(ORANGE)

        self.play(
            FadeIn(a, shift=DOWN * 0.15),
            FadeIn(b, shift=DOWN * 0.15),
            sum.animate.set_opacity(1),
            carry.animate.set_opacity(1),
            numbers[0][0].code[0][1].animate.set_color(GREEN),
            numbers[0][0].code[0][3].animate.set_color(GREEN),
            numbers[0][0].code[0][4].animate.set_color(GREEN),
            numbers[0][1].code[0][1].animate.set_color(GREEN),
            numbers[0][1].code[0][3].animate.set_color(GREEN),
            numbers[0][1].code[0][4].animate.set_color(GREEN),
            numbers[0][0].code[0][0].animate.set_color(ORANGE),
            numbers[0][1].code[0][0].animate.set_color(ORANGE),
        )

        c, d = numbers[2]
        c.set_z_index(1)
        d.set_z_index(1)

        a.move_to(numbers[1][0]).align_to(numbers[1][0], RIGHT)
        b.move_to(numbers[1][1]).align_to(numbers[1][1], RIGHT)

        c.move_to(a).align_to(a, RIGHT)
        d.move_to(b).align_to(b, RIGHT)

        # TODO: move the line
        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(numbers[0][0]),
                    FadeOut(numbers[0][1]),
                    sum.animate.set_opacity(0.25),
                    carry.animate.set_opacity(0.25),
                ),
                AnimationGroup(
                    a.animate.move_to(numbers[0][0]).align_to(numbers[0][0], RIGHT).set_color(orig_color),
                    b.animate.move_to(numbers[0][1]).align_to(numbers[0][1], RIGHT).set_color(orig_color),
                    plus.animate.shift(0.2 * LEFT),
                    self.camera.frame.animate.move_to(VGroup(plus.copy().shift(0.2 * LEFT), a, b, numbers[0][0], numbers[0][1])).scale(1.1),
                ),
                lag_ratio=0.5,
            )
        )

        c.set_color(GREEN)
        d.code[0][:-1].set_color(ORANGE)

        self.play(
            FadeIn(c, shift=DOWN * 0.15),
            FadeIn(d, shift=DOWN * 0.15),
            sum.animate.set_opacity(1),
            carry.animate.set_opacity(1),
            a.code[0][0].animate.set_color(GREEN),
            a.code[0][2].animate.set_color(GREEN),
            a.code[0][3].animate.set_color(GREEN),
            b.code[0][0].animate.set_color(GREEN),
            b.code[0][2].animate.set_color(GREEN),
            b.code[0][4].animate.set_color(GREEN),
            b.code[0][5].animate.set_color(GREEN),
        )

        self.play(Circumscribe(VGroup(d, carry), color=ORANGE))

        eq = MyCodeKindaTho("=").set_color(WHITE).rotate(PI / 2).scale(1.25).next_to(c, DOWN)
        esix = MyCodeKindaTho("86").next_to(eq, DOWN).set_color(WHITE)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(plus),
                    FadeOut(a),
                    FadeOut(b),
                    FadeOut(d),
                    FadeOut(line),
                    FadeOut(sum),
                    FadeOut(carry),
                ),
                AnimationGroup(
                    FadeIn(eq, shift=DOWN * 0.15),
                    FadeIn(esix, shift=DOWN * 0.15),
                    c.animate.set_color(WHITE),
                    self.camera.frame.animate.move_to(VGroup(c, eq, esix)),
                ),
                lag_ratio=0.5,
            )
        )
