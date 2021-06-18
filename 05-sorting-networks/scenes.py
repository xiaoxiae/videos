from utilities import *


class SortingNetwork(VMobject):
    def __init__(
            self,
            network,
            n,
            height = 2.5,
            width = 5.5,
            oriented = False,
            depth_labels = True,
    ):
        super().__init__()

        self.network = network
        self.n = n
        self.width = width
        self.height = height
        self.oriented = oriented
        self.compare_function = lambda a, b, nums: nums[min(a, b)] > nums[max(a, b)] if not self.oriented else (nums[a] > nums[b])

        corner_circles_radius = 0.05
        comparator_circles_radius = 0.11

        self.get_circle = lambda r: Circle(r, color=WHITE).set_fill(WHITE, opacity=1)

        self.starting_circles = [self.get_circle(corner_circles_radius) for _ in range(n)]
        self.ending_circles = [self.get_circle(corner_circles_radius) for _ in range(n)]

        # starting circles
        for i, circle in enumerate(self.starting_circles):
            circle.move_to(((i / (n - 1)) * height - height / 2) * DOWN + LEFT * width / 2)
            self.add(circle)

        # ending circles
        for i, circle in enumerate(self.ending_circles):
            circle.move_to(((i / (n - 1)) * height - height / 2) * DOWN + RIGHT * width / 2)
            self.add(circle)

        # main lines
        self.lines = []
        for a, b in zip(self.starting_circles, self.ending_circles):
            self.lines.append(Line(a.get_center(), b.get_center()))
            self.add(self.lines[-1])

        layer_spacing = 1
        sublayer_spacing = 0.3
        position = layer_spacing
        number = 1

        # add appropriately spaced comparators
        self.comparators = []
        self.comparator_layer_numbers = []
        for i, layer in enumerate(network):
            subpos = position
            for sublayer in layer:
                self.comparators.append([position, sublayer, i])  # position is horizontal
                position += sublayer_spacing
                subpos += position
            subpos = (subpos - position) / len(layer)
            self.comparator_layer_numbers.append((subpos, Tex(f"${number}$")))
            number += 1
            position = position - sublayer_spacing + layer_spacing

        # normalize the positions of the comparators accordingly (from 0 to 1)
        for comparator in self.comparators:
            comparator[0] /= position

        for i in range(len(self.comparator_layer_numbers)):
            pos, text = self.comparator_layer_numbers[i]
            pos /= position

            # labels will be below the layers of the comparator
            text.move_to(DOWN * (height / 2) * 1.3 + RIGHT * (-width / 2 + width * pos))
            self.comparator_layer_numbers[i] = (pos, text)

        if depth_labels:
            for _, text in self.comparator_layer_numbers:
                self.add(text)
        else:
            self.comparator_layer_numbers = []

        # transform the sublayer list into (a, b, Circle(a), Circle(b), line) list
        for position, sublayer, _ in self.comparators:
            for i in range(len(sublayer)):
                a, b = sublayer[i]

                a_pos = DOWN * ((a / (n - 1)) * height - height / 2) + RIGHT * (-width / 2 + width * position)
                b_pos = DOWN * ((b / (n - 1)) * height - height / 2) + RIGHT * (-width / 2 + width * position)

                a_circle = self.get_circle(comparator_circles_radius).move_to(a_pos)
                b_circle = self.get_circle(comparator_circles_radius).move_to(b_pos)

                if a < b:
                    a_pos += DOWN * comparator_circles_radius * 0.95
                    b_pos += UP * comparator_circles_radius * 0.95
                else:
                    a_pos += UP * comparator_circles_radius * 0.95
                    b_pos += DOWN * comparator_circles_radius * 0.95

                line = Line(a_pos, b_pos)
                if self.oriented:
                    line.add_tip(tip_length=0.2)

                sublayer[i] = (a, b, a_circle, b_circle, line)

                self.add(a_circle)
                self.add(b_circle)
                self.add(line)

    def animate_sort(self, scene, numbers = None, rate_func=linear, duration=7):
        """Animate a sorting of numbers. TODO: less numbers."""
        if numbers is None:
            numbers = [i + 1 for i in range(self.n)]
            shuffle(numbers)

        number_circles = []
        number_labels = []

        old_number_lines = []
        number_lines = []
        number_lines_starts = []

        for i, circle in enumerate(self.starting_circles):
            number_circle = self.get_circle(0.15).move_to(circle.get_center()).set_color(rainbow_to_rgb(numbers[i] / self.n))
            label = Tex(f"${numbers[i]}$").move_to(circle.get_center()).set_color(BLACK).scale(0.5)
            line = Line(number_circle.get_center(), number_circle.get_center()).set_color(rainbow_to_rgb(numbers[i] / self.n))

            number_lines_starts.append(number_circle.get_center())
            number_circles.append(number_circle)
            number_labels.append(label)
            number_lines.append(line)

        scene.play(*map(Write, number_circles))
        scene.play(*map(Write, number_labels))
        scene.add(*number_lines)

        def tmp(ob, dt):
            pos, _, _, = number_circles[0].get_center()
            pos += self.width / 2
            pos /= self.width

            for circle, label in zip(number_circles, number_labels):
                label.move_to(circle.get_center())

            for position, compars, _ in self.comparators:
                if pos > position > pos - dt:
                    for a, b, _, _, _ in compars:
                        if self.compare_function(a, b, numbers):
                            number_labels[a], number_labels[b] = number_labels[b], number_labels[a]
                            numbers[a], numbers[b] = numbers[b], numbers[a]
                            old_number_lines.append(number_lines[a])
                            old_number_lines.append(number_lines[b])
                            number_lines_starts[a] = number_circles[a].get_center()
                            number_lines_starts[b] = number_circles[b].get_center()
                            number_lines[a] = Line()
                            number_lines[b] = Line()
                            scene.add(number_lines[a], number_lines[b])

            for i in range(len(number_circles)):
                old_number_lines.append(number_lines[i])
                number_lines[i].become(Line(number_lines_starts[i], number_circles[i].get_center()).set_color(rainbow_to_rgb(numbers[i] / self.n)))

            for i in range(len(number_circles)):
                number_circles[i].set_color(rainbow_to_rgb(numbers[i] / self.n))

            for c in self.starting_circles:
                scene.bring_to_front(c)

            for c in self.ending_circles:
                scene.bring_to_front(c)

            for _, sublayer, _ in self.comparators:
                for _, _, a, b, c in sublayer:
                    scene.bring_to_front(a)
                    scene.bring_to_front(b)
                    scene.bring_to_front(c)

            for c in number_circles:
                scene.bring_to_front(c)

            for c in number_labels:
                scene.bring_to_front(c)

        number_labels[0].add_updater(tmp)

        numbers_copy = list(numbers)
        flash_positions = []

        for position, compars, _ in self.comparators:
            for a, b, _, _, _ in compars:
                if self.compare_function(a, b, numbers_copy):
                    numbers_copy[a], numbers_copy[b] = numbers_copy[b], numbers_copy[a]
                    flash_positions.append([position, number_circles[a], numbers_copy[a]])
                    flash_positions.append([position, number_circles[b], numbers_copy[b]])

        delayed_flash_function = lambda p, x: 0 if (rate_func(x) - p) < 0 else (rate_func(x) - p) * 10 if (rate_func(x) - p) <= 0.1 else 1

        scene.play(
                *[circle.animate.move_to(end.get_center()) for circle, end in zip(number_circles, self.ending_circles)],
                *[Flash(obj, rate_func=partial(delayed_flash_function, pos), color=(rainbow_to_rgb(p / self.n)), run_time=duration) for pos, obj, p in flash_positions],
                run_time = duration,
                rate_func=rate_func,
                )

        for number_label in number_labels:
            number_label.remove_updater(tmp)

        scene.play(
                *map(FadeOut, number_lines),
                *map(FadeOut, old_number_lines),
                *map(FadeOut, number_circles),
                *map(FadeOut, number_labels),
                )

        scene.remove(*number_lines)
        scene.remove(*old_number_lines)
        scene.remove(*number_circles)
        scene.remove(*number_labels)

    def animate_optimization(self, other, canvas):
        """Animate the optimization from one network to another. Note that they must be
        the same networks (same comparators) so they only get shifted together."""

        self_comparators = []
        other_comparators = []

        for _, comparators, _ in self.comparators:
            self_comparators += comparators

        for _, comparators, _ in other.comparators:
            other_comparators += comparators

        self_comparators = sorted(self_comparators, key=lambda a: (a[0], a[1]))
        other_comparators = sorted(other_comparators, key=lambda a: (a[0], a[1]))

        comparator_animations = [
                *[a[2].animate.move_to(b[2]) for a, b in zip(self_comparators, other_comparators)],
                *[a[3].animate.move_to(b[3]) for a, b in zip(self_comparators, other_comparators)],
                *[a[4].animate.move_to(b[4]) for a, b in zip(self_comparators, other_comparators)],
                ]

        self_label_count = len(self.comparator_layer_numbers)
        other_label_count = len(other.comparator_layer_numbers)

        if self_label_count > other_label_count:
            canvas.play(
                    *comparator_animations,
                    *[a[1].animate.move_to(b[1]) for a, b in zip(self.comparator_layer_numbers, other.comparator_layer_numbers)],
                    *[FadeOut(self.comparator_layer_numbers[i][1]) for i in range(other_label_count, self_label_count)],
                    )
        else:
            canvas.play(
                    *comparator_animations,
                    *[a[1].animate.move_to(b[1]) for a, b in zip(self.comparator_layer_numbers, other.comparator_layer_numbers)],
                    *[FadeIn(other.comparator_layer_numbers[i][1]) for i in range(self_label_count, other_label_count)],
                    )

    def animate_wires_swap(self, wires, canvas):
        """Animate wires swapping. Note that the wires must not overlap."""
        # difference between two lines
        line_diff = self.lines[0].get_center() - self.lines[1].get_center()

        animations = []
        updater_removals = []

        for a, b in wires:
            # swap lines and their circles
            animations += [
                    self.lines[a].animate.move_to(self.lines[b]),
                    self.lines[b].animate.move_to(self.lines[a]),
                    self.starting_circles[a].animate.move_to(self.starting_circles[b]),
                    self.starting_circles[b].animate.move_to(self.starting_circles[a]),
                    self.ending_circles[a].animate.move_to(self.ending_circles[b]),
                    self.ending_circles[b].animate.move_to(self.ending_circles[a]),
                    ]

            for _, comparators, _ in self.comparators:

                for c_pos, d_pos, c, d, e in comparators:
                    def f(i, line):
                        line2 = Line(i[0], i[1])

                        if self.oriented:
                            line2.add_tip(tip_length=0.2)

                        line.become(line2)

                    if c_pos == a: # c -> b
                        animations += [c.animate.shift(line_diff * (c_pos - b))]

                    if d_pos == a: # d -> b
                        animations += [d.animate.shift(line_diff * (d_pos - b))]

                    if c_pos == b: # c -> a
                        animations += [c.animate.shift(line_diff * (c_pos - a))]

                    if d_pos == b: # d -> a
                        animations += [d.animate.shift(line_diff * (d_pos - a))]

                    f = partial(f, (c, d))
                    e.add_updater(f)
                    updater_removals.append((e, f))

        canvas.play(*animations)

        for e, f in updater_removals:
            e.remove_updater(f)

    @classmethod
    def BubbleSorter(cls, n, optimized=False, **kwargs):
        """Create a bubble sort network of size n."""
        if not optimized:
            network = []
            for i in range(n):
                for j in range(i, n - 1):
                    network.append([[(j - i, j + 1 - i)]])
        else:
            network = []
            for i in range(1, n):
                network.append([[]])
                for j in range(0, i, 2):
                    if i % 2 == 0:
                        j += 1
                    network[-1][-1].append((j, j + 1))
            for i in reversed(range(1, n - 1)):
                network.append([[]])
                for j in range(0, i, 2):
                    if i % 2 == 0:
                        j += 1
                    network[-1][-1].append((j, j + 1))

        return SortingNetwork(network, n, **kwargs)

    @classmethod
    def BitonicSorter(cls, n, oriented=False, **kwargs):
        """Create a (possibly oriented) bitonic sort network of size 2**n."""
        # TODO: oriented
        network = []

        # https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/BitonicSort.svg/1920px-BitonicSort.svg.png
        # blue part
        for i in range(n):
            # orange and red parts
            for j in reversed(range(i + 1)):
                size = 2 ** (j + 1)
                network.append([])

                # orange part
                if j == i:
                    for _ in range(size // 2):
                        network[-1].append([])

                    for k in range((2 ** n) // size):
                        for l in range(size // 2):
                            network[-1][l].append((k * size + l, k * size + size - l - 1))

                # red part
                else:
                    for _ in range(size // 2):
                        network[-1].append([])

                    for k in range((2 ** n) // size):
                        for l in range(size // 2):
                            network[-1][l].append((k * size + l, k * size + l + size // 2))

        return SortingNetwork(network, (2 ** n), **kwargs)

    @classmethod
    def OptimalSorter(cls, n, optimized=True, **kwargs):
        """Create the optimal sorting network of size n (up to size 9)"""
        optimal_networks = [
                None,
                [#1
                    [],
                ],
                [#2
                    [[(0, 1)]],
                ],
                [#3
                    [[(1, 2)]],
                    [[(0, 1)]],
                    [[(1, 2)]],
                ],
                [#4
                    [[(0, 1), (2, 3)]],
                    [[(1, 3)], [(0, 2)]],
                    [[(1, 2)]],
                ],
                [#5
                    [[(1, 2), (3, 4)]],
                    [[(1, 3)], [(0, 2)]],
                    [[(2, 4)], [(0, 3)]],
                    [[(0, 1), (2, 3)]],
                    [[(1, 2)]],
                ],
                [#6
                    [[(0, 1), (2, 3), (4, 5)]],
                    [[(0, 2), (3, 5)],  [(1, 4)]],
                    [[(0, 1), (2, 3), (4, 5)]],
                    [[(1, 2), (3, 4)]],
                    [[(2, 3)]],
                ],
                [#7
                    [[(1, 2), (3, 4), (5, 6)]],
                    [[(0, 2), (4, 6)], [(3, 5)]],
                    [[(2, 6)], [(1, 5)], [(0, 4)]],
                    [[(2, 5)], [(0, 3)]],
                    [[(2, 4)], [(1, 3)]],
                    [[(0, 1), (2, 3), (4, 5)]],
                ],
                [#8
                    [[(0, 7)], [(1, 6)], [(2, 5)], [(3, 4)]],
                    [[(0, 3), (4, 7)], [(1, 2), (5, 6)]],
                    [[(0, 1), (2, 3), (4, 5), (6, 7)]],
                    [[(3, 5)], [(2, 4)]],
                    [[(1, 2), (3, 4), (5, 6)]],
                    [[(2, 3), (4, 5)]],
                    [[(3, 4)]],
                ],
                [#9
                    [[(1, 8)], [(2, 7)], [(3, 6)], [(4, 5)]],
                    [[(0, 2), (6, 7)], [(1, 4), (5, 8)]],
                    [[(2, 6), (7, 8)], [(0, 3), (4, 5)]],
                    [[(0, 1), (3, 5)], [(2, 4), (6, 7)]],
                    [[(1, 3), (5, 7)], [(4, 6)]],
                    [[(1, 2), (3, 4), (5, 6), (7, 8)]],
                    [[(2, 3), (4, 5)]],
                ],
            ]

        network = optimal_networks[n]

        # possibly de-optimize the network
        if not optimized:
            new_network = []
            for layer in network:
                for comparator in layer:
                    for c in comparator:
                        new_network.append([[c]])

            return SortingNetwork(new_network, n, oriented=False, **kwargs)
        else:
            return SortingNetwork(network, n, oriented=False, **kwargs)

    def get_comparators(self):
        """Return a list of VGroups of all comparators."""
        c = []
        for _, comparators, _ in self.comparators:
            for comparator in comparators:
                c.append(VGroup(comparator[2], comparator[3], comparator[4]))
        return c

    def get_lines(self):
        """Return a list of VGroups of lines."""
        return [VGroup(*items) for items in zip(self.lines, self.starting_circles, self.ending_circles)]

    def get_layer_numbers(self):
        """Return a list of MObjects of layer numbers."""
        return [text for _, text in self.comparator_layer_numbers]

    def get_layers(self):
        """Return a list of VGroups of layers (just their comparators)."""
        c = []

        layer = 0
        sub_c = []
        for _, comparators, l in self.comparators:
            if l != layer:
                c.append(VGroup(*sub_c))
                sub_c = []
                layer = l

            for comparator in comparators:
                sub_c += [comparator[2], comparator[3], comparator[4]]

        return c + [VGroup(*sub_c)]


class Introduction(Scene):
    @fade
    def construct(self):
        sn = SortingNetwork.OptimalSorter(7, width=9, height=4.5, depth_labels=False, optimized=False)
        sn_optimized = SortingNetwork.OptimalSorter(7, width=9, height=4.5, depth_labels=False, optimized=True)
        sn_optimized_layers = SortingNetwork.OptimalSorter(7, width=9, height=4.5, depth_labels=True, optimized=True)

        self.play(Write(sn))

        lines = sn.get_lines()
        self.play(
            AnimationGroup(*[Indicate(line) for line in lines], lag_ratio=0.07),
            )

        comparators = sn.get_comparators()
        self.play(
            AnimationGroup(*[Indicate(comparator) for comparator in comparators], lag_ratio=0.07),
            )

        sn.animate_sort(self)

        sn.animate_optimization(sn_optimized, self)

        numbers = sn_optimized_layers.get_layer_numbers()
        self.play(*[FadeIn(number) for number in numbers])

        layers = sn_optimized.get_layers()
        self.play(
            *[layer.animate.set_color(rainbow_to_rgb(i / len(layers))) for i, layer in enumerate(layers)],
            *[layer.animate.set_color(rainbow_to_rgb(i / len(layers))) for i, layer in enumerate(numbers)],
        )

class BubbleSort(Scene):
    @fade
    def construct(self):
        title = Tex("\Large Bubble sort")

        self.play(Write(title))
        self.play(FadeOut(title))

        sn = SortingNetwork.BubbleSorter(5, width=7, height=3.5, optimized=False, oriented=True)
        sn_optimized = SortingNetwork.BubbleSorter(5, width=7, height=3.5, optimized=True)

        self.play(Write(sn))

        sn.animate_sort(self, rate_func=smooth, duration=4)

        sn.animate_optimization(sn_optimized, self)

class Bitonic(Scene):
    def construct(self):
        title = Tex("\Large Bitonic sort")

        self.play(Write(title))
        self.play(FadeOut(title))

    def construct(self):
        f = lambda x: -abs((x + 2) % 4 - 2 - 2) - abs(-2 * ((x + 2) % 4 - 2  - 2) - 5) + 5

        func = FunctionGraph(f, x_range = (-2, 2), fill_opacity=0, color=WHITE)

        self.play(Write(func))

        text = Tex("strictly bitonic")
        text.next_to(func, DOWN).shift(DOWN * 0.2)
        self.play(Write(text), run_time=1)

        func2 = FunctionGraph(f, x_range = (-2, 2), fill_opacity=0, color=WHITE)
        func2.shift(RIGHT * 2)
        func2.set_color(DARK_GRAY)

        func3 = FunctionGraph(f, x_range = (-2, 2), fill_opacity=0, color=WHITE)
        func3.shift(LEFT * 2)
        func3.set_color(DARK_GRAY)

        self.play(
                func.animate.shift(LEFT * 2),
                )

        # FUCK THIS

        self.play(Write(func2))


        self.add(func3)
        func.set_color(DARK_GRAY)

        start = func3.get_center()

        def f(fan):
            current = float((func3.get_center() - start)[0])
            my = lambda x: -abs((x + 2) % 4 - 2 - 2) - abs(-2 * ((x + 2) % 4 - 2  - 2) - 5) + 5
            fan_new = FunctionGraph(my, x_range = (-2 + current, 2 + current), fill_opacity=0, color=WHITE)
            fan_new.move_to(fan)
            fan.become(fan_new)

        func3.add_updater(f)
        self.play(func3.animate.shift(RIGHT * 4))
