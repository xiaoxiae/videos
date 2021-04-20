from utilities import *

class Simple(Scene):
    def construct(self):
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')

        seed(134)

        for row in self.camera.get_coords_of_all_pixels():
            for x, y in row:
                if min_x > x:
                    min_x = x
                if min_y > y:
                    min_y = y
                if max_x < x:
                    max_x = x
                if max_y < y:
                    max_y = y

        n = 10

        dots = [Dot([uniform(min_x, max_x), uniform(min_y, max_y), 0]) for _ in range(n)]

        for dot in dots:
            x, y, _ = dot.get_center()
            x -= min_x
            y -= min_y

            xn = x / (max_x - min_x)
            yn = y / (max_y - min_y)

        self.play(LaggedStart(*map(FadeIn, dots)))

        colors = [(87, 211, 219), (161, 87, 219), (87, 112, 219), (87, 211, 219), (145, 219, 87), (87, 112, 219), (87, 211, 219), (87, 112, 219), (161, 87, 219), (145, 219, 87)]
        colors = [(color[0]/256, color[1]/256, color[2]/256) for color in colors]

        self.play(*[dot.animate.set_fill(rgb_to_hex(color)) for dot, color in zip(dots, colors)])

        center = Dot(ORIGIN)
        self.play(FadeIn(center))

        lines = [Line(center.get_center(), dots[i].get_center(), stroke_width = 2) for i in range(n)]

        def tmp(mob, dt):
            self.add(center)
            self.add(*dots)

        center.add_updater(tmp)

        self.play(*map(Create, lines))

        self.play(*map(FadeOut, lines[:6] + lines[7:]))

        self.play(center.animate.set_fill(rgb_to_hex(colors[0])), lines[6].animate.set_fill(rgb_to_hex(colors[0])))

        self.play(FadeOut(lines[6]), FadeOut(center))

        center.remove_updater(tmp)


class Points(Scene):
    def construct(self):
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')

        seed(134)

        for row in self.camera.get_coords_of_all_pixels():
            for x, y in row:
                if min_x > x:
                    min_x = x
                if min_y > y:
                    min_y = y
                if max_x < x:
                    max_x = x
                if max_y < y:
                    max_y = y

        n = 10

        def my_uniform(min_x, min_y, max_x, max_y, regions: int):

            k = 10
            points = []
            dot_points = []
            while len(points) != regions:
                best_p = None
                d_max = 0

                sample_points = []

                for _ in range(k * len(points) + 1):
                    p = (uniform(min_x, max_x), uniform(min_y, max_y))

                    if len(points) == 0:
                        best_p = p

                        break

                    sample_points.append(Dot([*p, 0], color="#373737"))

                    d_min = float('inf')
                    for x, y in points:
                        d = hypot(p[0]-x, p[1]-y)
   
                        if d < d_min:
                            d_min = d
   
                    if d_min > d_max:
                        d_max = d_min
                        best_p = p
   
                if best_p is None:
                    continue

                self.play(LaggedStart(*map(FadeIn, sample_points)), run_time = 1)

                best_p_dot = Dot([*best_p, 0], color=WHITE)

                self.play(*map(FadeOut, sample_points), FadeIn(best_p_dot), Flash(best_p_dot))
   
                points.append(best_p)
                dot_points.append(best_p_dot)

                if len(points) == 1:
                    def tmp(mob, dt):
                        self.add(*dot_points)

                    dot_points[0].add_updater(tmp)
   

            dot_points[0].remove_updater(tmp)
            return dot_points

        margin = 0.95

        dots = my_uniform(min_x * margin, min_y * margin, max_x * margin, max_y * margin, n)

        print([dot.get_center() for dot in dots])

        #for dot in dots:
        #    x, y= dot.get_center()[:2]

        #    xn, yn = x / (max_x - min_x) + 0.5, y / (max_y - min_y) + 0.5

        #    print(xn, yn)

        colors = [(145, 219, 87), (87, 211, 219), (87, 211, 219), (87, 211, 219), (161, 87, 219), (161, 87, 219), (87, 112, 219), (87, 112, 219), (87, 211, 219), (145, 219, 87)]
        colors = [(color[0]/256, color[1]/256, color[2]/256) for color in colors]

        self.play(*[dot.animate.set_fill(rgb_to_hex(color)) for dot, color in zip(dots, colors)])


class Metric(Scene):
    def construct(self):
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')

        seed(134)

        for row in self.camera.get_coords_of_all_pixels():
            for x, y in row:
                if min_x > x:
                    min_x = x
                if min_y > y:
                    min_y = y
                if max_x < x:
                    max_x = x
                if max_y < y:
                    max_y = y

        dot1start = Dot()
        dot1end = Dot()

        def euclid(text):
            text.next_to(dot1start.get_center(), UP * 8)

        formula = Tex("$\sqrt{x^2 + y^2}$")
        formulaname = Tex("Euclidean")
        formulaname.next_to(dot1start.get_center(), UP * 8)

        self.play(Write(formula), Write(formulaname))

        formulaname.add_updater(euclid)

        line = Line(ORIGIN, ORIGIN)

        formula_value = Tex("$0.00$")
        formula_value.next_to(ORIGIN, UP)

        self.play(Create(dot1end), Transform(formula, formula_value))

        self.add(line)
        self.add(dot1start)
        self.add(dot1end)

        def tmp(mob):
            line.become(Line(dot1start.get_center(), dot1end.get_center()))

        def text_update(text):
            x, y, _ = dot1end.get_center() - dot1start.get_center()
            xr, yr = round(x, 2), round(y, 2)

            txt = f"${round(sqrt(x * x + y * y), 2):.2f}$"
            text.become(Tex(txt))
            text.next_to(dot1end.get_center(), UP)

        line.add_updater(tmp)
        formula.add_updater(text_update)

        self.play(ApplyMethod(dot1end.shift, RIGHT*2), run_time=1, rate_func=smooth)
        self.play(ApplyMethod(dot1end.shift, LEFT + UP), run_time=1, rate_func=smooth)
        self.play(ApplyMethod(dot1end.shift, DOWN + LEFT * 4), run_time=1, rate_func=smooth)
        self.play(Rotating(dot1end, about_point=dot1start.get_center()), run_time=2, rate_func=smooth)
        self.play(ApplyMethod(dot1end.shift, RIGHT*3), run_time=1, rate_func=smooth)

        l1 = Line(ORIGIN, ORIGIN)
        l2 = Line(ORIGIN, ORIGIN)

        dot2start = Dot()
        dot2end = Dot()

        def tmp1(mob):
            l1.become(Line(dot2start.get_center(), [dot2end.get_center()[0], 0, 0]))

        def tmp2(mob):
            l2.become(Line([dot2end.get_center()[0], 0, 0], [dot2end.get_center()[0], dot2end.get_center()[1], 0]))

        def text_update2(text):
            x, y, _ = dot2end.get_center() - dot2start.get_center()

            txt = f"${round(abs(x) + abs(y), 2):.2f}$"
            text.become(Tex(txt))
            text.next_to(dot2end.get_center(), UP)

        self.play(ApplyMethod(dot1start.shift, LEFT*2), ApplyMethod(dot1end.shift, LEFT*2), run_time=1, rate_func=smooth)

        dot2start.shift(RIGHT*2)
        dot2end.shift(RIGHT*2)

        formula2 = Tex("$|x| + |y|$")
        formula2.move_to(dot2start.get_center())

        formula2_value = Tex("$0.00$")
        formula2_value.next_to(dot2start.get_center(), UP)

        l1.add_updater(tmp1)
        l2.add_updater(tmp2)

        self.add(l1)
        self.add(l2)

        def manhattan(text):
            text.next_to(dot2start.get_center(), UP * 8)

        formula2name = Tex("Manhattan")
        formula2name.next_to(dot2start.get_center(), UP * 8)

        self.play(Write(formula2), Write(formula2name))

        formula2name.add_updater(manhattan)

        self.play(Create(dot2end), Transform(formula2, formula2_value))
        formula2.add_updater(text_update2)

        self.add(dot2start)
        self.add(dot2end)

        self.play(ApplyMethod(dot1end.shift, RIGHT*2), ApplyMethod(dot2end.shift, RIGHT*2), run_time=1, rate_func=smooth)
        self.play(ApplyMethod(dot1end.shift, LEFT + UP), ApplyMethod(dot2end.shift, LEFT + UP), run_time=1, rate_func=smooth)
        self.play(ApplyMethod(dot1end.shift, DOWN + LEFT * 2), ApplyMethod(dot2end.shift, DOWN + LEFT * 2), run_time=1, rate_func=smooth)
        self.play(Rotating(dot1end, about_point=dot1start.get_center()), Rotating(dot2end, about_point=dot2start.get_center()), run_time=2, rate_func=smooth)
        self.play(ApplyMethod(dot1end.shift, RIGHT*1), ApplyMethod(dot2end.shift, RIGHT*1), run_time=1, rate_func=smooth)


class Color(Scene):
    def construct(self):
        dots = list(map(Dot, [[-0.22223248, -2.2748981 ,  0.        ], [5.02542935, 3.19432106, 0.        ], [-5.59603133,  3.22596847,  0.        ], [ 5.55709686, -2.98486069,  0.        ], [-0.3587377,  3.3184144,  0.       ], [-5.92227625, -3.12034469,  0.        ], [2.31565885, 0.53980622, 0.        ], [-2.78178311, -0.0077623 ,  0.        ], [ 2.69523115, -3.54040193,  0.        ], [-6.17100105,  0.11923881,  0.        ]]))

        colors = [(145, 219, 87),
                (87, 211, 219),
                (87, 211, 219),
                (161, 87, 219), #6
                (161, 87, 219),
                (87, 211, 219), #4
                (87, 112, 219),
                (87, 112, 219),
                (87, 211, 219),
                (145, 219, 87)]
        colors = [(color[0]/256, color[1]/256, color[2]/256) for color in colors]

        for dot, color in zip(dots, colors):
            dot.set_fill(rgb_to_hex(color))

        imgblank = ImageMobject("2blank.png")
        img = ImageMobject("2.png")

        self.play(FadeIn(imgblank))

        v = [(i + 1) for i, dot in enumerate(dots)]

        lt = {(i + 1): dots[i].get_center() for i, dot in enumerate(dots)}

        edges = [
                (v[0], v[6]),
                (v[0], v[7]),
                (v[0], v[8]),
                (v[1], v[4]),
                (v[1], v[6]),
                (v[1], v[3]),
                (v[2], v[4]),
                (v[2], v[9]),
                (v[2], v[7]),
                (v[3], v[8]),
                (v[3], v[6]),
                (v[4], v[7]),
                (v[4], v[6]),
                (v[5], v[7]),
                (v[5], v[9]),
                (v[6], v[8]),
                (v[7], v[9]),
                ]

        g = Graph(v, edges, labels=True, layout=lt,
                )

        h = Graph(v, edges, labels=True, layout=lt,
            vertex_config={(i + 1): {"fill_color": rgb_to_hex(color)} for i, color in enumerate(colors)}
                )

        self.play(Write(g))
        self.play(Transform(g, h))
        self.add(img)
        self.bring_to_back(img)
        self.remove(img)
        self.play(FadeIn(img))



