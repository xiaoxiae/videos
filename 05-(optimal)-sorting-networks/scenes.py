from utilities import *


networks = [
        None,
        None,
        [#2
            [(0, 1)],
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
            [[(0, 2), (3, 5)], [(1, 4)]],
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
    ):
        super().__init__()
        self.network = network

        major_circles_radius = 0.05
        minor_circles_radius = 0.11

        self.starting_circles = [Circle(major_circles_radius, color=WHITE).set_fill(WHITE, opacity=1) for _ in range(n)]
        self.ending_circles = [Circle(major_circles_radius, color=WHITE).set_fill(WHITE, opacity=1) for _ in range(n)]

        # starting circles
        for i, circle in enumerate(self.starting_circles):
            circle.move_to(((i / (n - 1)) * height - height / 2) * UP + LEFT * width / 2)
            self.add(circle)

        # ending circles
        for i, circle in enumerate(self.ending_circles):
            circle.move_to(((i / (n - 1)) * height - height / 2) * UP + RIGHT * width / 2)
            self.add(circle)

        # lines
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
        self.comparator_titles = []
        for layer in network:
            subpos = position
            for sublayer in layer:
                self.comparators.append([position, sublayer])
                position += sublayer_spacing
                subpos += position
            subpos = (subpos - position) / len(layer)
            self.comparator_titles.append((subpos, Tex(f"${number}$")))
            number += 1
            position = position - sublayer_spacing + layer_spacing

        # normalize the positions of the comparators accordingly
        for comparator in self.comparators:
            comparator[0] /= position

        for i in range(len(self.comparator_titles)):
            pos, text = self.comparator_titles[i]
            pos /= position
            text.move_to(UP * (height / 2) * 1.2 + RIGHT * (-width / 2 + width * pos))
            self.comparator_titles[i] = (pos, text)

        # transform the sublayer list into (a, b, Circle(a), Circle(b), line) list
        # a little messy but w/e
        for position, sublayer in self.comparators:
            for i in range(len(sublayer)):
                a, b = sublayer[i]

                a_circle = Circle(minor_circles_radius, color=WHITE).move_to(UP * ((a / (n - 1)) * height - height / 2) + RIGHT * (-width / 2 + width * position)).set_fill(WHITE, opacity=1)
                b_circle = Circle(minor_circles_radius, color=WHITE).move_to(UP * ((b / (n - 1)) * height - height / 2) + RIGHT * (-width / 2 + width * position)).set_fill(WHITE, opacity=1)
                line = Line(a_circle.get_center(), b_circle.get_center())

                sublayer[i] = (a, b, a_circle, b_circle, line)

                self.add(a_circle)
                self.add(b_circle)
                self.add(line)

        for _, text in self.comparator_titles:
            self.add(text)


class Intro(Scene):
    def construct(self):
        sn = SortingNetwork(networks[9], 9, width=7, height=5)

        self.play(Write(sn))
