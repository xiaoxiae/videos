from utilities import *
from string import digits

import manimpango

PALETTE = ["#b91e2f", "#f68828", "#cdd190", "#122f30"]
REDUCED_PALETTE = PALETTE[:2]

SUCCESS_COLOR = "#5A9B5A"


def is_hex_color(str):
    """Yeah I know, this is not pretty."""
    return (
        len(str) == 7
        and str.startswith("#")
        and all([c in digits + "abcdef" for c in str.lower()[1:]])
    )


class Tile(VMobject):
    TEXT_SCALE = 0.6
    TEXT_OFFSET = 1 / 3.5
    DIRECTIONS = [RIGHT, UP, LEFT, DOWN]

    def __str__(self):
        return f"Tile({self.colors})"

    __repr__ = __str__

    def __init__(self, colors, size=1):
        colors = list(map(str, colors))

        super().__init__()

        self.border = Square(size, color=WHITE)
        self.add(self.border)

        self.size = size

        self.colors = colors

        self.cross = VGroup()
        self.cross.add(
            Line(
                start=(UP + RIGHT) * self.size / 2,
                end=(DOWN + LEFT) * self.size / 2,
                stroke_width=1,
            )
        )
        self.cross.add(
            Line(
                end=(DOWN + RIGHT) * self.size / 2,
                start=(UP + LEFT) * self.size / 2,
                stroke_width=1,
            )
        )

        self.add(self.cross)

        self.color_objects = VGroup()
        for color, direction in zip(colors, Tile.DIRECTIONS):
            self.set_color_in_direction(color, direction, new=True)

        self.add_to_back(self.color_objects)

    def set_color_in_direction(self, color, direction, new=False):
        for i, d in enumerate(Tile.DIRECTIONS):
            if (direction == d).all():
                break

        if not new:
            self.colors[i] = color

        triangle = Polygon(
            np.array([self.size / 2 + self.get_x(), self.size / 2 + self.get_y(), 0]),
            np.array([self.size / 2 + self.get_x(), -self.size / 2 + self.get_y(), 0]),
            [self.get_x(), self.get_y(), 0],
            stroke_width=1,
            color=WHITE,
        ).rotate(PI / 2 * i, about_point=([self.get_x(), self.get_y(), 0]))

        if is_hex_color(color):
            triangle.set_fill(color, 1)

            if not new:
                self.color_objects[i] = triangle
            else:
                self.color_objects.add(triangle)
        else:
            text = (
                Tex(color)
                .scale(Tile.TEXT_SCALE * self.size)
                .shift(direction * self.size * Tile.TEXT_OFFSET)
            )

            if not new:
                self.color_objects[i] = text
            else:
                self.color_objects.add(text)

    def get_color_in_direction(self, direction):
        for i, d in enumerate(Tile.DIRECTIONS):
            if (direction == d).all():
                return self.colors[i]

    def get_color_object_in_direction(self, direction):
        """Return the color object in the given direction."""
        for i, d in enumerate(Tile.DIRECTIONS):
            if (direction == d).all():
                return self.color_objects[i]

    def animateWrite(self):
        return AnimationGroup(
            Write(self.cross),
            AnimationGroup(
                Write(self.get_color_object_in_direction(LEFT)),
                Write(self.get_color_object_in_direction(UP)),
                Write(self.get_color_object_in_direction(RIGHT)),
                Write(self.get_color_object_in_direction(DOWN)),
            ),
            Write(self.border),
            lag_ratio=0.2,
        )


class Wall(VMobject):
    def __init__(self, colors, input=None, width=3, height=5, size=1):
        super().__init__()

        colors = list(map(str, colors))

        # input overwrites the width
        if input is not None:
            width = len(input)

        self.input = input

        width *= size
        height *= size

        self.border = Rectangle(width=width, height=height)

        self.size = size

        self.tiles = VGroup()
        self.add(self.tiles)

        self.tile_position_dictionary = {}

        self.add(self.border)

        self.colors = colors

        self.color_objects = VGroup()

        self.w = width
        self.h = height

        for i, (color, direction) in enumerate(zip(colors, Tile.DIRECTIONS)):
            # yeah, not pretty
            # I was tired and didn't want to think
            c = 0.4  # outer offset
            d = 0  # inner offset

            if (direction == UP).all():
                pos = [
                    np.array([width / 2, height / 2 + d, 0]),
                    np.array([width / 2 - c, height / 2 + c, 0]),
                    np.array([-width / 2 + c, height / 2 + c, 0]),
                    np.array([-width / 2, height / 2 + d, 0]),
                ]
            if (direction == DOWN).all():
                pos = [
                    np.array([width / 2, -height / 2 - d, 0]),
                    np.array([width / 2 - c, -height / 2 - c, 0]),
                    np.array([-width / 2 + c, -height / 2 - c, 0]),
                    np.array([-width / 2, -height / 2 - d, 0]),
                ]
            if (direction == LEFT).all():
                pos = [
                    np.array([-width / 2 - d, height / 2, 0]),
                    np.array([-width / 2 - c, height / 2 - c, 0]),
                    np.array([-width / 2 - c, -height / 2 + c, 0]),
                    np.array([-width / 2 - d, -height / 2, 0]),
                ]
            if (direction == RIGHT).all():
                pos = [
                    np.array([width / 2 + d, height / 2, 0]),
                    np.array([width / 2 + c, height / 2 - c, 0]),
                    np.array([width / 2 + c, -height / 2 + c, 0]),
                    np.array([width / 2 + d, -height / 2, 0]),
                ]

            if (direction == UP).all() and input is not None:
                g = VGroup()

                self.input_colors = []
                self.input_lines = []

                for i in range(len(input) + 1):
                    c = (0.25 if i in (0, len(input)) else 0.5) * self.size
                    line = Line(
                        start=[-width / 2 + i * self.size, height / 2, 0],
                        end=[-width / 2 + i * self.size, height / 2 + c, 0],
                    )

                    g.add(line)
                    self.input_lines.append(line)

                    if i < len(input):
                        p = [-width / 2 + (i + 0.5) * self.size, height / 2, 0]

                        text = (
                            Tex(input[i])
                            .scale(Tile.TEXT_SCALE * self.size)
                            .move_to(p)
                            .align_to(p, DOWN)
                            .shift(UP * Tile.TEXT_OFFSET / 2)
                        )  # 2 is an eyeball magic constant
                        self.input_colors.append(text)
                        g.add(text)

                self.color_objects.add(g)
            else:
                g = VGroup()

                side = Polygon(*pos).set_stroke(WHITE)
                if is_hex_color(color):
                    g.add(side.set_fill(color, 1))
                else:
                    g.add(side)

                    text = Tex(color).scale(Tile.TEXT_SCALE * self.size).move_to(side)

                    g.add(text)

                self.color_objects.add(g)

        self.add(self.color_objects)

    def to_positive_coordinates(self, x, y):
        """Done so we can use -1."""
        return int(x % self.border.width), int(y % self.border.height)

    def index_to_position(self, x, y):
        x, y = self.to_positive_coordinates(x, y)

        return (
            Square(self.size)
            .align_to(self.border, UP + LEFT)
            .shift([x * self.size, -y * self.size, 0])
            .get_center()
        )

    def add_tiles(self, tiles, positions, **kwargs):
        for t, p in zip(tiles, positions):
            self.add_tile(t, *p, **kwargs)

    def add_tile(self, tile, x, y, copy=False):
        x, y = self.to_positive_coordinates(x, y)

        if copy:
            tile = tile.copy()

        tile.move_to(self.index_to_position(x, y))

        self.tiles.add(tile)

        # TODO: sort by tile position dictionary!

        self.tile_position_dictionary[(x, y)] = tile

        return tile

    def get_tile(self, x, y):
        x, y = self.to_positive_coordinates(x, y)

        return self.tile_position_dictionary[(x, y)]

    get_color_object_in_direction = Tile.get_color_object_in_direction

    def get_color_in_direction(self, direction):
        if (direction == UP).all() and self.input is not None:
            return self.input
        else:
            return Tile.get_color_in_direction(self, direction)

    def animateWrite(self):
        return AnimationGroup(
            AnimationGroup(*[t.animateWrite() for t in self.tiles], lag_ratio=0.1),
            Write(self.border),
            AnimationGroup(
                Write(self.get_color_object_in_direction(LEFT)),
                Write(self.get_color_object_in_direction(UP))
                if self.input is None
                else AnimationGroup(
                    AnimationGroup(
                        *[Write(c) for c in self.input_colors], lag_ratio=0.04
                    ),
                    AnimationGroup(
                        *[FadeIn(l) for l in self.input_lines], lag_ratio=0.04
                    ),
                    lag_ratio=0.3,
                ),
                Write(self.get_color_object_in_direction(RIGHT)),
                Write(self.get_color_object_in_direction(DOWN)),
            ),
            lag_ratio=0.2,
        )


class TileSet(VMobject):
    def __init__(self, *tiles, rows=1):
        super().__init__()

        self.tiles = VGroup(*tiles)
        self.tiles.arrange_in_grid(rows=rows, buff=0.6)

        self.commas = VGroup()

        n = len(tiles)
        for i in range(n - 1):
            self.commas.add(
                Tex("\Large $,$")
                .next_to(self.tiles[i], DOWN + RIGHT, buff=0)
                .shift(UP * 0.07 + RIGHT * 0.1)
            )

        brace_offset = -0.25
        self.braces = VGroup(
            BraceBetweenPoints(
                Point().next_to(self.tiles[0], UP + LEFT).get_center(),
                Point().next_to(self.tiles[0], DOWN + LEFT).get_center(),
                direction=LEFT,
            ).shift(LEFT * brace_offset),
            BraceBetweenPoints(
                Point().next_to(self.tiles[-1], UP + RIGHT).get_center(),
                Point().next_to(self.tiles[-1], DOWN + RIGHT).get_center(),
                direction=RIGHT,
            ).shift(RIGHT * brace_offset),
        )

        self.add(self.tiles)
        self.add(self.commas)
        self.add(self.braces)

    def animateWrite(self):
        return AnimationGroup(
            AnimationGroup(*[t.animateWrite() for t in self.tiles], lag_ratio=0.1),
            Write(self.commas),
            Write(self.braces),
            lag_ratio=0.2,
        )

    def __getitem__(self, i):
        return self.tiles[i]

    def __len__(self):
        return len(self.tiles)


def find_tiling_recursive(i, j, tileset: List[Tile], wallarray, w, h):
    def at(x, y):
        return wallarray[y + 1][x + 1]

    def set(x, y, tile):
        wallarray[y + 1][x + 1] = tile

    # if we're past (on the very right tile)
    if i == w:
        # check if the tile on the left is ok
        if at(i - 1, j).get_color_in_direction(RIGHT) != at(
            i, j
        ).get_color_in_direction(LEFT):
            return

        if j == h - 1:
            return wallarray

        i = 0
        j += 1

    for tile in tileset.tiles:
        if at(i, j - 1).get_color_in_direction(DOWN) != tile.get_color_in_direction(UP):
            continue

        if at(i - 1, j).get_color_in_direction(RIGHT) != tile.get_color_in_direction(
            LEFT
        ):
            continue

        # if we're last row
        if j == h - 1:
            if at(i, j + 1).get_color_in_direction(UP) != tile.get_color_in_direction(
                DOWN
            ):
                continue

        set(i, j, tile)
        result = find_tiling_recursive(i + 1, j, tileset, wallarray, w, h)
        if result is not None:
            return result
        set(i, j, None)


def find_tiling(tileset: List[Tile], wall: Wall, max_height=1):
    """Find if there exists a tiling of maximal height for a given wall."""
    w = wall.w
    for h in range(1, max_height + 1):
        wallarray = [[None] * (w + 2) for _ in range(h + 2)]

        for i in range(1, w + 1):
            wallarray[0][i] = Tile([None, None, None, wall.input[i - 1]])

        for i in range(1, w + 1):
            wallarray[-1][i] = Tile(
                [None, wall.get_color_in_direction(DOWN), None, None]
            )

        for i in range(1, h + 1):
            wallarray[i][-1] = Tile(
                [None, None, wall.get_color_in_direction(RIGHT), None]
            )

        for i in range(1, h + 1):
            wallarray[i][0] = Tile(
                [wall.get_color_in_direction(LEFT), None, None, None]
            )

        result = find_tiling_recursive(0, 0, tileset, wallarray, w, h)

        if result is not None:
            wall = Wall(wall.colors, wall.input, height=h)

            for x in range(w):
                for y in range(h):
                    wall.add_tile(result[y + 1][x + 1], x, y, copy=True)

            return wall


class WriteReverse(Write):
    """A special write for a tile and wall (since we want the animation to be reversed)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, reverse=True)


examples = {
    "even_size": (
        Wall([PALETTE[1], None, PALETTE[1], PALETTE[0]], height=1, input="111111"),
        TileSet(
            Tile([PALETTE[2], 1, PALETTE[1], PALETTE[0]]),
            Tile([PALETTE[1], 1, PALETTE[2], PALETTE[0]]),
        ),
    ),
    "divby3": (
        Wall([0, None, 0, PALETTE[0]], height=1, input="1010010"),
        TileSet(
            Tile([0, 0, 0, PALETTE[0]]),
            Tile([1, 0, 1, PALETTE[0]]),
            Tile([2, 0, 2, PALETTE[0]]),
            Tile([1, 1, 0, PALETTE[0]]),
            Tile([2, 1, 1, PALETTE[0]]),
            Tile([0, 1, 2, PALETTE[0]]),
        ),
    ),
    "parentheses": (
        Wall([BLACK, None, BLACK, BLACK], input="(()()(()))"),
        TileSet(
            Tile([PALETTE[1], "(", BLACK, BLACK]),
            Tile([BLACK, "(", BLACK, PALETTE[1]]),
            Tile([PALETTE[1], BLACK, PALETTE[1], BLACK]),
            Tile([BLACK, PALETTE[1], BLACK, PALETTE[1]]),
            Tile([BLACK, ")", BLACK, PALETTE[0]]),
            Tile([BLACK, PALETTE[0], BLACK, PALETTE[0]]),
            Tile([PALETTE[1], PALETTE[1], BLACK, BLACK]),
            Tile([BLACK, PALETTE[0], PALETTE[1], BLACK]),
            Tile([BLACK, ")", PALETTE[1], BLACK]),
        ),
    ),
    "parentheses_log": (
        Wall([PALETTE[1], None, PALETTE[0], BLACK], input="(((())))"),
        TileSet(
            Tile([1, "(", PALETTE[0], BLACK]),
            Tile([BLACK, BLACK, PALETTE[0], BLACK]),
            Tile([0, "(", 1, "+"]),
            Tile([1, "(", 0, BLACK]),
            Tile([1, "+", BLACK, BLACK]),
            Tile([1, BLACK, 1, BLACK]),
            Tile([0, BLACK, 0, BLACK]),
            Tile([BLACK, BLACK, 0, BLACK]),
            Tile([0, ")", 1, BLACK]),
            Tile([1, ")", 0, "-"]),
            Tile([PALETTE[1], ")", 1, BLACK]),
            Tile([0, "-", 1, BLACK]),
            Tile([1, "-", 0, "-"]),
            Tile([BLACK, "-", 1, BLACK]),
            Tile([PALETTE[1], BLACK, BLACK, BLACK]),
            Tile([PALETTE[1], BLACK, 0, BLACK]),
            Tile([BLACK, BLACK, BLACK, BLACK]),
        ),
    ),
    "palindrome": (
        Wall([PALETTE[0], None, PALETTE[1], BLACK], input="10100101"),
        TileSet(
            Tile([RED, "1", PALETTE[1], BLACK]),
            Tile([PALETTE[0], "1", RED, BLACK]),
            Tile([RED, "1", RED, "1"]),
            Tile([RED, "0", RED, "0"]),
            Tile([PALETTE[0], BLACK, PALETTE[0], BLACK]),
            Tile([PALETTE[1], BLACK, PALETTE[1], BLACK]),
            Tile([BLUE, "0", PALETTE[1], BLACK]),
            Tile([PALETTE[0], "0", BLUE, BLACK]),
            Tile([BLUE, "1", BLUE, "1"]),
            Tile([BLUE, "0", BLUE, "0"]),
            Tile([PALETTE[0], "0", PALETTE[1], BLACK]),
            Tile([PALETTE[0], "1", PALETTE[1], BLACK]),
        ),
    ),
}


class Motivation(Scene):
    @fade
    def construct(self):
        p1 = SVGMobject("pillar.svg").scale(2.8).shift(LEFT * 4.8)
        p2 = SVGMobject("pillar.svg").scale(2.8).shift(RIGHT * 4.8)

        ft = Text("Eureka!", font="Gelio Pasteli").scale(2)

        # TODO: when
        archimedes = (
            Text("– Archimedes", font="Gelio Pasteli")
            .scale(0.7)
            .next_to(ft, DOWN)
            .align_to(ft, RIGHT)
        )

        g = VGroup(ft, archimedes).move_to(ORIGIN)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Write(p1),
                    Write(p2),
                ),
                AnimationGroup(
                    Write(ft, run_time=1.3),
                    Write(archimedes),
                    lag_ratio=0.8,
                ),
                lag_ratio=0.3,
            ),
            run_time=3,
        )

        offset = 1.2

        ft2 = Text("Bathroom tiles!").scale(1.0).shift(DOWN * offset)
        tom = Text("- Tom").scale(0.6).next_to(ft2, DOWN).align_to(ft2, RIGHT)

        g2 = VGroup(ft2, tom)
        g2.move_to(ORIGIN).shift(DOWN * offset)

        self.play(g.animate.shift(UP * offset))

        self.play(
            AnimationGroup(
                Write(ft2, run_time=1.3),
                Write(tom),
                lag_ratio=0.8,
            )
        )


class Intro(MovingCameraScene):
    @fade
    def construct(self):
        w = 9
        h = 5

        wall = Wall(PALETTE, width=w, height=h)

        bl = BraceBetweenPoints([-w / 2, h / 2, 0], [-w / 2, -h / 2, 0])
        blt = Tex("\\footnotesize h").next_to(bl, LEFT * 0.5)

        bu = BraceBetweenPoints(
            [-w / 2, h / 2, 0], [w / 2, h / 2, 0], direction=UP
        ).scale([-1, 1, 0])
        but = Tex("\\footnotesize w").next_to(bu, UP * 0.5)

        self.play(Write(wall.border))

        self.play(Write(bu), Write(but))
        self.play(Write(bl), Write(blt))

        seed(0)
        tiles = [
            [Tile([choice(PALETTE) for _ in range(4)]) for _ in range(w)]
            for _ in range(h)
        ]

        for i in range(w):
            for j in range(h):
                wall.add_tile(tiles[j][i], i, j)

        self.play(
            AnimationGroup(*[FadeIn(t.border) for t in wall.tiles], lag_ratio=0.01)
        )

        tile = wall.get_tile(w // 2, h // 2)
        zoom_ratio = 0.2

        self.play(
            self.camera.frame.animate.scale(zoom_ratio).move_to(tile),
            rate_func=smooth,
            run_time=1.5,
        )

        self.play(AnimationGroup(Write(tile.cross), lag_ratio=0.3))

        self.bring_to_front(tile.border)

        for c in tile.color_objects:
            self.bring_to_back(c)
        self.bring_to_front(tile)

        self.play(
            *[
                FadeIn(tile.get_color_object_in_direction(d))
                for d in [LEFT, UP, RIGHT, DOWN]
            ],
            tile.border.animate.set_color(WHITE),
        )

        for t in wall.tiles:
            for c in t.color_objects:
                self.bring_to_back(c)
            self.bring_to_front(t)

        self.play(
            AnimationGroup(
                self.camera.frame.animate.scale(1 / zoom_ratio).move_to(ORIGIN),
                rate_func=smooth,
                run_time=1.5,
            ),
            *[t.border.animate.set_color(WHITE) for t in wall.tiles if t is not tile],
            *[Write(t.cross) for t in wall.tiles if t is not tile],
            *[Write(t.color_objects) for t in wall.tiles if t is not tile],
        )

        # color rows + columns
        changes = {}
        seed(1)
        for count, (i1, i2) in enumerate(
            zip((range(w - 1), range(w)), (range(h), range(h - 1)))
        ):
            for i in i1:
                for j in i2:
                    p1, p2 = (i, j), (i + 1, j) if not count else (i, j + 1)
                    d1, d2 = (RIGHT, LEFT) if not count else (DOWN, UP)

                    c1, c2 = tiles[p1[1]][p1[0]].get_color_in_direction(d1), tiles[
                        p2[1]
                    ][p2[0]].get_color_in_direction(d2)
                    new_color = choice([c1, c2])

                    if p1 not in changes:
                        changes[p1] = tiles[p1[1]][p1[0]].animate
                    changes[p1].set_color_in_direction(new_color, d1)

                    if p2 not in changes:
                        changes[p2] = tiles[p2[1]][p2[0]].animate
                    changes[p2].set_color_in_direction(new_color, d2)
        self.play(*changes.values())
        self.play(
            AnimationGroup(
                FadeOut(VGroup(bl, blt, bu, but)),
                FadeIn(wall.color_objects),
                lag_ratio=0.4,
            )
        )

        changes = {}

        for count, iterable in enumerate([range(w), range(h)]):
            for x in iterable:
                for index in range(2):
                    y = ((0, h - 1) if not count else (0, w - 1))[index]
                    direction = ((UP, DOWN) if not count else (LEFT, RIGHT))[index]

                    if count:
                        i, j = y, x
                    else:
                        i, j = x, y

                    if tiles[j][i].get_color_in_direction(
                        direction
                    ) != wall.get_color_in_direction(direction):

                        if (i, j) not in changes:
                            changes[(i, j)] = tiles[j][i].animate
                        changes[(i, j)].set_color_in_direction(
                            wall.get_color_in_direction(direction), direction
                        )

        self.play(*changes.values())


def animate_tile_pasting(tile, wall, positions, speed=0.07):
    def DelayedTransform(x, y, t):
        return Transform(
            x,
            y,
            run_time=1 + t,
            rate_func=lambda a: smooth(
                a if t == 0 else (0 if a < t else (a - t) / (1 - t))
            ),
        )

    n = len(positions)

    from_tiles = [tile.copy() for _ in range(n)]
    to_tiles = [
        tile.copy().move_to(wall.index_to_position(*position)) for position in positions
    ]

    return (
        [
            DelayedTransform(from_tiles[i], to_tiles[i], speed * (n - i - 1))
            for i in range(n)
        ],
        from_tiles,
        positions,
    )


class TileSetExample(Scene):
    @fade
    def construct(self):
        tiles = [
            Tile(
                [
                    REDUCED_PALETTE[1],
                    REDUCED_PALETTE[1],
                    REDUCED_PALETTE[0],
                    REDUCED_PALETTE[1],
                ]
            ),
            Tile(
                [
                    REDUCED_PALETTE[1],
                    REDUCED_PALETTE[1],
                    REDUCED_PALETTE[1],
                    REDUCED_PALETTE[1],
                ]
            ),
            Tile(
                [
                    REDUCED_PALETTE[0],
                    REDUCED_PALETTE[1],
                    REDUCED_PALETTE[1],
                    REDUCED_PALETTE[1],
                ]
            ),
        ]

        tiles = VGroup(*tiles)
        tiles.arrange_in_grid(rows=1)

        tileset = TileSet(*tiles)

        tileTypes = Tex("Tile Types $=$").shift(LEFT * 1)

        tileset_with_text = VGroup(tileTypes, tileset)

        tileset_with_text.arrange_in_grid(rows=1, buff=0.23).move_to([0, 0, 0])

        self.play(
            AnimationGroup(Write(tileTypes), tileset.animateWrite(), lag_ratio=0.6)
        )

        w = 8
        h = 3
        wall = Wall(REDUCED_PALETTE * 2, width=w, height=h)

        wall.shift(DOWN * 1.2)

        self.play(
            AnimationGroup(
                tileset_with_text.animate.shift(UP * 2.3),
                wall.animateWrite(),
                lag_ratio=0.6,
            )
        )

        question = Tex("?").scale(3).move_to(wall)

        self.play(Write(question))
        self.play(FadeOut(question))

        animations1, tiles1, positions1 = animate_tile_pasting(
            tiles[-1], wall, [(-1, i) for i in range(h)]
        )
        animations2, tiles2, positions2 = animate_tile_pasting(
            tiles[0], wall, [(0, i) for i in range(h)]
        )

        self.play(*animations1, *animations2)

        wall.add_tiles(tiles1, positions1)
        wall.add_tiles(tiles2, positions2)

        from_tile_wrong = tiles[-1].copy()
        to_tile_wrong = (
            tiles[-1].copy().move_to(wall.index_to_position(4, i)).rotate(-PI / 2)
        )

        cross = VGroup()
        r1 = Rectangle(width=0.2, height=3.3).set_fill(RED, 1).scale(0.5).rotate(PI / 4)
        r2 = (
            Rectangle(width=0.2, height=3.3).set_fill(RED, 1).scale(0.5).rotate(-PI / 4)
        )
        cross.add(
            Union(r1, r2)
            .set_stroke("#8b0000", 1.5)
            .set_fill(RED, 1)
            .move_to(to_tile_wrong)
        )

        self.play(Transform(from_tile_wrong, to_tile_wrong))

        self.play(FadeIn(cross), from_tile_wrong.animate.set_opacity(0.2))
        self.play(FadeOut(from_tile_wrong), FadeOut(cross))

        animations, tiles, positions = animate_tile_pasting(
            tiles[1],
            wall,
            [(i, j) for i in reversed(range(1, w - 1)) for j in reversed(range(h))],
            speed=0.03,
        )

        self.play(*animations)

        wall.add_tiles(tiles, positions)

        self.play(
            wall.get_color_object_in_direction(UP).animate.set_fill(REDUCED_PALETTE[0])
        )

        self.play(*[FadeOut(wall.get_tile(i, 0)) for i in range(wall.w)])


class HighlightedTex(Tex):
    def __init__(self, text, sep="|", color=YELLOW):
        super().__init__(*[s for s in text.split(sep) if len(s) != 0])

        for i in range(0 if text[0] == sep else 1, len(self), 2):
            self[i].set_color(YELLOW)


class PartialFlash(AnimationGroup):
    def __init__(
        self,
        point: np.ndarray,
        start_angle=0,
        end_angle=TAU,
        line_length: float = 0.3,
        num_lines: int = 6,
        flash_radius: float = 0.9,
        line_stroke_width: int = 2,
        color: str = YELLOW,
        time_width: float = 1,
        run_time: float = 1.0,
        **kwargs,
    ) -> None:
        self.point = point.get_center()
        self.color = color
        self.line_length = line_length
        self.num_lines = num_lines
        self.flash_radius = flash_radius
        self.line_stroke_width = line_stroke_width
        self.run_time = run_time
        self.time_width = time_width
        self.animation_config = kwargs
        self.start_angle = start_angle
        self.end_angle = end_angle

        self.lines = self.create_lines()
        animations = self.create_line_anims()
        super().__init__(*animations, group=self.lines)

    def create_lines(self) -> VGroup:
        lines = VGroup()
        for angle in np.arange(
            self.start_angle,
            self.end_angle + ((self.end_angle - self.start_angle) / self.num_lines) / 2,
            (self.end_angle - self.start_angle) / self.num_lines,
        ):
            line = Line(self.point, self.point + self.line_length * RIGHT)
            line.shift((self.flash_radius) * RIGHT)
            line.rotate(angle, about_point=self.point)
            lines.add(line)
        lines.set_color(self.color)
        lines.set_stroke(width=self.line_stroke_width)
        return lines

    def create_line_anims(self) -> Iterable["ShowPassingFlash"]:
        return [
            ShowPassingFlash(
                line,
                time_width=self.time_width,
                run_time=self.run_time,
                **self.animation_config,
            )
            for line in self.lines
        ]


class ProgrammingModel(Scene):
    @fade
    def construct(self):
        title = Tex("\Large Programming model")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 2.5))

        text = [
            (Tex("Input:"), HighlightedTex("|colors| on the |top side| of the wall")),
            (Tex("Program:"), HighlightedTex("finite set of |tile types|")),
            (
                Tex("Output:"),
                HighlightedTex("|accept| if there exists valid tiling, else |reject|"),
            ),
        ]

        text_scale = 0.85
        for i in range(len(text)):
            text[i][0].scale(text_scale).next_to(text[i - 1][0], DOWN).align_to(
                text[i - 1][0], RIGHT
            )
            text[i][1].scale(text_scale).next_to(text[i][0], RIGHT)

        g = VGroup()
        for i in range(len(text)):
            g.add(text[i][0])
            g.add(text[i][1])

        g.move_to(ORIGIN).shift(UP * 0.7)

        tile_scale = 1

        self.play(
            AnimationGroup(
                Write(text[0][0]), Write(text[1][0]), Write(text[2][0]), lag_ratio=0.15
            )
        )

        wall, ts = examples["even_size"]
        wall = wall.shift(DOWN * 2).scale(tile_scale)

        ts = ts.scale(tile_scale)

        self.play(Write(text[0][1]), wall.animateWrite())

        # TODO: leave others arbitrary (show the colors)

        ts.next_to(wall, RIGHT, buff=1)

        g = VGroup(ts, wall)

        self.play(wall.animate.set_x(wall.get_x() - g.get_x()))
        ts.next_to(wall, RIGHT, buff=1)

        self.play(ts.animateWrite(), Write(text[1][1]))

        # TODO: slower run time
        self.play(Write(text[2][1]))

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(title),
                    *[
                        FadeOut(text[i][j])
                        for i in range(len(text))
                        for j in range(len(text[0]))
                    ],
                ),
                AnimationGroup(
                    ts.animate.move_to(ORIGIN).shift(UP * 1.5),
                    wall.animate.move_to(ORIGIN).shift(DOWN * 1.5),
                ),
                lag_ratio=0.5,
            ),
            run_time=2,
        )

        for i in range(wall.w):
            animations, tiles, positions = animate_tile_pasting(
                ts[i % 2], wall, [(i, 0)]
            )
            self.play(*animations)
            wall.add_tiles(tiles, positions)

        self.play(
            wall.animate.set_stroke(SUCCESS_COLOR).set_shadow(0.5),
            PartialFlash(
                Dot().next_to(wall, LEFT).shift(RIGHT * 0.8),
                start_angle=PI / 2,
                end_angle=(PI / 2) * 3,
                color=SUCCESS_COLOR,
            ),
            PartialFlash(
                Dot().next_to(wall, RIGHT).shift(LEFT * 0.8),
                start_angle=-PI / 2,
                end_angle=PI / 2,
                color=SUCCESS_COLOR,
            ),
        )

        # TODO: show if it was odd


class AdvancedExample(Scene):
    @fade
    def construct(self):
        wall, tileset = examples["divby3"]

        tileset.move_to(ORIGIN).shift(UP * 1.5)
        wall.move_to(ORIGIN).shift(DOWN * 1.5)

        self.play(tileset.animateWrite(), wall.animateWrite())

        brace_offset = 0.25

        b = BraceBetweenPoints(
            Point().next_to(tileset[0], UP + LEFT, buff=0).get_center(),
            Point().next_to(tileset[2], UP + RIGHT, buff=0).get_center(),
            direction=UP,
            color=GRAY,
        ).scale([-1, 1, 1])

        bl = Tex(f"\small carry", color=GRAY).next_to(b, UP)

        self.play(
            AnimationGroup(
                Write(b),
                Write(bl, run_time=0.9),
                lag_ratio=0.3,
            )
        )

        b = BraceBetweenPoints(
            Point().next_to(tileset[3], UP + LEFT, buff=0).get_center(),
            Point().next_to(tileset[5], UP + RIGHT, buff=0).get_center(),
            direction=UP,
            color=GRAY,
        ).scale([-1, 1, 1])

        bl = Tex(f"\small increment", color=GRAY).next_to(b, UP)

        self.play(
            AnimationGroup(
                Write(b),
                Write(bl, run_time=0.9),
                lag_ratio=0.3,
            )
        )

        for tile, positions in [
            (3, [(0, 0)]),
            (1, [(1, 0)]),
            (4, [(2, 0)]),
            (2, [(4, 0), (3, 0)]),
            (-1, [(5, 0)]),
            (0, [(6, 0)]),
        ]:
            animations, tiles, positions = animate_tile_pasting(
                tileset[tile], wall, positions
            )
            self.play(*animations)
            wall.add_tiles(tiles, positions)

            # TODO: animate that it matches the input

        self.play(
            wall.animate.set_stroke(SUCCESS_COLOR),
            PartialFlash(
                Dot().next_to(wall, LEFT).shift(RIGHT * 0.8),
                start_angle=PI / 2,
                end_angle=(PI / 2) * 3,
                color=SUCCESS_COLOR,
            ),
            PartialFlash(
                Dot().next_to(wall, RIGHT).shift(LEFT * 0.8),
                start_angle=-PI / 2,
                end_angle=PI / 2,
                color=SUCCESS_COLOR,
            ),
        )
