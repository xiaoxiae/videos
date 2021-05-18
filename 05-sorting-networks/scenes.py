from utilities import *

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


class SortingNetwork(VMobject):
    def __init__(
            self,
            network,
            n,
            height = 2.5,
            width = 5.5,
            oriented = False,
    ):
        super().__init__()

        self.network = network
        self.n = n
        self.width = width
        self.height = height
        self.oriented = oriented
        self.compare_function = lambda a, b, nums: nums[min(a, b)] < nums[max(a, b)] if not self.oriented else (nums[a] > nums[b])

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
        for layer in network:
            subpos = position
            for sublayer in layer:
                self.comparators.append([position, sublayer])  # position is horizontal
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

            # labels will be below the layers of the comaprator
            text.move_to(DOWN * (height / 2) * 1.4 + RIGHT * (-width / 2 + width * pos))
            self.comparator_layer_numbers[i] = (pos, text)

        # transform the sublayer list into (a, b, Circle(a), Circle(b), line) list
        for position, sublayer in self.comparators:
            for i in range(len(sublayer)):
                a, b = sublayer[i]

                a_pos = DOWN * ((a / (n - 1)) * height - height / 2) + RIGHT * (-width / 2 + width * position)
                b_pos = DOWN * ((b / (n - 1)) * height - height / 2) + RIGHT * (-width / 2 + width * position)

                a_circle = self.get_circle(comparator_circles_radius).move_to(a_pos)
                b_circle = self.get_circle(comparator_circles_radius).move_to(b_pos)

                #                    "": 0.25,
                #    "max_stroke_width_to_length_ratio": 5,
                #    "preserve_tip_size_when_scaling": True,

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

        for _, text in self.comparator_layer_numbers:
            self.add(text)

    def animate_sort(self, scene, numbers = None, rate_func=linear, duration=4):
        """Animate a sorting of numbers. TODO: less numbers"""
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

            for position, compars in self.comparators:
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

            for _, sublayer in self.comparators:
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

        for position, compars in self.comparators:
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

    def BubbleSorter(n, optimized=False):
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

        return SortingNetwork(network, n)

    def BitonicSorter(n, oriented=True):
        """Create a (possibly oriented) bitonic sort network of size 2**n."""
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

        return SortingNetwork(network, (2 ** n))


class Intro(Scene):
    @fade
    def construct(self):
        sn = SortingNetwork(optimal_networks[6], 6, oriented=True)
        #sn = SortingNetwork.BitonicSorter(2)
        #sn_op = SortingNetwork.BubbleSorter(5, optimized=True)

        self.play(Write(sn))

        sn.animate_sort(self)

        self.play(Unwrite(sn))
