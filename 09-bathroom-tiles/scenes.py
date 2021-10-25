from utilities import *

class Tile(VMobject):
    def __init__(
            self,
            colors,
            size=1,
    ):
        super().__init__()

        self.add(Square(size))

        cross = VGroup()
        cross.add(Line(start=(UP + RIGHT) * size / 2, end=(DOWN + LEFT) * size / 2, stroke_width=1))
        cross.add(Line(end=(DOWN + RIGHT) * size / 2, start=(UP + LEFT) * size / 2, stroke_width=1))

        self.add(cross)

        for i, (color, direction) in enumerate(zip(colors, [RIGHT, UP, LEFT, DOWN])):
            # TODO: maybe a better test for checking the color
            triangle = Polygon(
                np.array([size / 2, size / 2, 0]),
                np.array([size / 2, -size / 2, 0]),
                [0, 0, 0],
                stroke_width=0,
            ).rotate(PI / 2 * i, about_point=([0, 0, 0]))

            if len(color) == 7 and color.startswith("#"):
                triangle.set_fill(color, 1)
                self.add_to_back(triangle)
            else:
                # TODO: duplication!
                text = Tex(color).scale(0.6).scale(size).shift(direction / 3.5 * size)
                self.add_to_back(text)


class Wall(VMobject):
    def __init__(
            self,
            colors,
            input=None,  # if specified, the top color and width is ignored
            width=3,
            height=5,
            size=1,
    ):
        super().__init__()

        # input overwrites the width
        if input is not None:
            width = len(input)

        width *= size
        height *= size

        self.add(Rectangle(width=width, height=height, stroke_width=2))

        for i, (color, direction) in enumerate(zip(colors, [RIGHT, UP, LEFT, DOWN])):
            # yeah, not pretty
            # I was tired and didn't want to think
            c = 0.2

            if (direction == UP).all():
                pos = [
                    np.array([width / 2, height / 2, 0]),
                    np.array([width / 2 - c, height / 2 + c, 0]),
                    np.array([-width / 2 + c, height / 2 + c, 0]),
                    np.array([-width / 2, height / 2, 0]),
                ]
            if (direction == DOWN).all():
                pos = [
                    np.array([width / 2, -height / 2, 0]),
                    np.array([width / 2 - c, -height / 2 - c, 0]),
                    np.array([-width / 2 + c, -height / 2 - c, 0]),
                    np.array([-width / 2, -height / 2, 0]),
                ]
            if (direction == LEFT).all():
                pos = [
                    np.array([-width / 2, height / 2, 0]),
                    np.array([-width / 2 - c, height / 2 - c, 0]),
                    np.array([-width / 2 - c, -height / 2 + c, 0]),
                    np.array([-width / 2, -height / 2, 0]),
                ]
            if (direction == RIGHT).all():
                pos = [
                    np.array([width / 2, height / 2, 0]),
                    np.array([width / 2 + c, height / 2 - c, 0]),
                    np.array([width / 2 + c, -height / 2 + c, 0]),
                    np.array([width / 2, -height / 2, 0]),
                ]

            if (direction == UP).all() and input is not None:
                c = 0.3
                for i in range(len(input) + 1):
                    line = Line(start=[-width / 2 + i, height / 2, 0], end=[-width / 2 + i, height / 2 + c, 0], stroke_width=2)

                    self.add(line)

                    # TODO: duplication!
                    if i < len(input):
                        # TODO: YUCK! first fix the duplication
                        text = Tex(input[i]).scale(0.6).scale(size).move_to([-width / 2 + i + 0.5, height / 2, 0]).align_to([-width / 2 + i + 0.5, height / 2, 0], DOWN)
                        self.add(text)
            else:
                side = Polygon(*pos).set_fill(color, 1).set_stroke(WHITE)
                self.add_to_back(side)


class WriteTile(Write):
    """A special write for a tile (since we want the animation to be reversed)."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, reverse=True)


class Intro(Scene):
    def construct(self):
        tile = Tile(["a", RED, "B", BLUE]).shift(LEFT * 2)
        wall = Wall([RED, GREEN, ORANGE, YELLOW], input="abc").shift(RIGHT * 2)

        self.play(WriteTile(tile), Write(wall), reverse=True)
