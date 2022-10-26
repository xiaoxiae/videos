from manim import *
from utilities import *


class Intro(MovingCameraScene):
    def construct(self):
        lines = open("cisla.txt").read().splitlines()

        primes = [2, 3, 5, 7, 11, 13]

        cool = 0.01
        fade = 0.25

        nesting_colors = ["#54d4ff", "#fdf39b", "#afffff"]

        nnn = 13

        def factors(n):
            if n == 0:
                return ["0"]
            if n == 1:
                return ["1"]

            f = []
            for i in range(2, n):
                count = 0
                while n % i == 0:
                    count += 1
                    n //= i

                if count == 1:
                    f.append(i)
                elif count != 0:
                    f.append(f"{i}^{count}")

            if n != 1:
                f.append(n)

            return f

        def factors_with_zeroes(n):
            if n == 0:
                return ["0"]
            if n == 1:
                return ["1"]

            f = []
            for i in range(2, n):
                count = 0
                while n % i == 0:
                    count += 1
                    n //= i

                if count != 0 or i in primes:
                    f.append(f"{i}^{count}")

            if n != 1:
                f.append(f"{n}^1")

            while f[-1].endswith("0"):
                f.pop()

            return f

        numbers_factors = VGroup(*[Tex("$$" + r" \cdot ".join(map(str, factors(i))) + "$$").scale(1.25) for i in range(nnn)]).arrange(DOWN, buff=0.3)
        numbers_factors_zero = VGroup(*[Tex("$$" + r" \cdot ".join(map(str, factors_with_zeroes(i))) + "$$").scale(1.25) for i in range(nnn)]).arrange(DOWN, buff=0.3)
        numbers_original = VGroup(*[Tex(i).scale(1.25) for i in range(nnn)]).arrange(DOWN, buff=0.3)
        numbers = VGroup(*[Tex(f"\\textbf{{{l}}}") for l in lines[:nnn]]).arrange(DOWN, buff=0.3)

        for a, b in zip(numbers_original, numbers):
            b.move_to(a)

        for i in range(1, len(numbers_original)):
            numbers_original[i].align_to(numbers_original[i - 1], RIGHT)

        numbers_super = numbers_original.copy()

        for a, b in zip(numbers, numbers_original):
            a.next_to(b, RIGHT, buff=0.5)

        for a, b in zip(numbers_original, numbers_factors):
            b.move_to(a).align_to(a, DOWN).align_to(a, RIGHT)

        for a, b in zip(numbers_original, numbers_factors_zero):
            b.move_to(a).align_to(a, DOWN).align_to(a, RIGHT)

        numbers[0].shift(DOWN * 0.1)

        for i, n in enumerate(numbers):
            nesting = 0
            for j, p in enumerate(lines[i]):
                if p == "(":
                    numbers[i][0][j].set_color(nesting_colors[nesting])
                    nesting += 1
                elif p == ")":
                    nesting -= 1
                    numbers[i][0][j].set_color(nesting_colors[nesting])

        self.camera.frame.move_to(numbers_original).set_height(numbers_original.get_height() * 1.3)

        self.play(FadeIn(numbers_original, lag_ratio=cool))

        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(VGroup(numbers, numbers_original)),
                FadeIn(numbers, lag_ratio=cool),
                lag_ratio=0.25,
            )
        )

        self.play(
            *[numbers_original[i].animate.set_opacity(fade) for i in range(len(numbers_original)) if i not in primes],
            *[numbers[i].animate.set_opacity(fade) for i in range(len(numbers)) if i  not in primes],
        )

        self.play(
            numbers_original.animate.set_opacity(1),
            numbers.animate.set_opacity(1),
        )

        self.play(
            AnimationGroup(
                *[Transform(numbers_original[i], numbers_factors[i]) for i in range(len(numbers_factors))],
                lag_ratio=cool
            ),
            self.camera.frame.animate.move_to(VGroup(numbers, numbers_original, numbers_factors)),
        )

        single_factors = primes + [0, 1, 6, 10]

        self.play(
            *[numbers_original[i].animate.set_opacity(fade) for i in range(len(numbers_original)) if i not in single_factors],
            *[numbers[i].animate.set_opacity(fade) for i in range(len(numbers_original)) if i not in single_factors],
        )

        sr1 = SR(VGroup(
            numbers_original[0],
            numbers_original[1],
            numbers[0],
            numbers[1],
                        ))

        self.play(Write(sr1))
        self.play(FadeOut(sr1))

        self.play(
            *[numbers_original[i].animate.set_opacity(1) for i in range(len(numbers_original)) if i not in single_factors],
            *[numbers[i].animate.set_opacity(1) for i in range(len(numbers_original)) if i not in single_factors],
            *[numbers_original[i].animate.set_opacity(fade) for i in range(len(numbers_original)) if i in single_factors],
            *[numbers[i].animate.set_opacity(fade) for i in range(len(numbers_original)) if i in single_factors],
        )

        self.play(
            numbers_original.animate.set_opacity(1),
            numbers.animate.set_opacity(1),
        )

        self.play(
            AnimationGroup(
                *[Transform(numbers_original[i], numbers_factors_zero[i]) for i in range(2, len(numbers_factors))],
                lag_ratio=cool
            ),
            self.camera.frame.animate.move_to(VGroup(numbers, numbers_original, numbers_factors, numbers_factors_zero)).set_width(VGroup(numbers, numbers_original, numbers_factors, numbers_factors_zero).width * 1.3),
        )

        anims = []
        for i in range(len(numbers_original)):
            num = numbers_original[i][0]

            for j in range(len(num)):
                if (i == 11 or i == 13) and j >= 13:
                    break

                if (j - 1) % 3 != 0:
                    anims.append(num[j].animate.set_opacity(fade))

            if i == 11:
                anims.append(num[-2].animate.set_opacity(fade))
            elif i == 11:
                anims.append(num[-2].animate.set_opacity(fade))
                anims.append(num[-5].animate.set_opacity(fade))

        anims2 = []
        for i in range(len(numbers)):
            num = numbers[i][0]
            anims2.append(num[0].animate.set_opacity(fade))
            anims2.append(num[-1].animate.set_opacity(fade))

        self.play(
            *anims,
            *anims2,
        )

        n1 = 5
        sr1 = SR(numbers_original[n1][0][1])
        sr2 = SR(numbers[n1][0][1])

        n2 = 9
        numbers_original[n1].save_state()
        numbers[n1].save_state()
        numbers_original[n2].save_state()
        numbers[n2].save_state()

        self.play(
            *[numbers_original[i].animate.set_opacity(fade) for i in range(nnn) if i != n1],
            *[numbers[i].animate.set_opacity(fade) for i in range(nnn) if i != n1],
            self.camera.frame.animate.move_to(VGroup(numbers[n1], numbers_original[n1])).set_width(VGroup(numbers[n1], numbers_original[n1]).width * 1.5),
        )

        self.play(
            FadeIn(sr1),
            FadeIn(sr2),
        )

        self.play(
            Transform(sr1, SR(numbers_original[n1][0][4])),
            Transform(sr2, SR(numbers[n1][0][2])),
        )

        self.play(
            Transform(sr1, SR(numbers_original[n1][0][7])),
            Transform(sr2, SR(numbers[n1][0][3:5])),
        )

        self.play(
            FadeOut(sr1),
            FadeOut(sr2),
            *[numbers_original[i].animate.set_opacity(fade) for i in range(nnn) if i != n2],
            *[numbers[i].animate.set_opacity(fade) for i in range(nnn) if i != n2],
            numbers[n2].animate.restore(),
            numbers_original[n2].animate.restore(),
            self.camera.frame.animate.move_to(VGroup(numbers[n2], numbers_original[n2])).set_width(VGroup(numbers[n2], numbers_original[n2]).width * 1.5),
        )

        sr1 = SR(numbers_original[n2][0][1])
        sr2 = SR(numbers[n2][0][1])

        self.play(
            FadeIn(sr1),
            FadeIn(sr2),
        )

        self.play(
            Transform(sr1, SR(numbers_original[n2][0][4])),
            Transform(sr2, SR(numbers[n2][0][2:6])),
        )

        self.play(
            FadeOut(sr1),
            FadeOut(sr2),
        )

        self.play(
            numbers_original.animate.set_opacity(1),
            numbers.animate.set_opacity(1),
            self.camera.frame.animate.move_to(VGroup(numbers_super, numbers)).set_height(VGroup(numbers_super, numbers).height * 1.3),
            AnimationGroup(
                *[Transform(numbers_original[i], numbers_super[i]) for i in range(len(numbers_factors))],
                lag_ratio=cool
            ),
        )
