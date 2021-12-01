from utilities import *
from string import digits

import manimpango

PALETTE = ["#b91e2f", "#f68828", "#cdd190", "#122f30"]
REDUCED_PALETTE = PALETTE[:2]

DIRECTIONS = [RIGHT, UP, LEFT, DOWN]

NOTES_SCALE = 0.8
NOTES_COLOR = GRAY

QUESTION_MARK_SCALE = 3

INDICATE_SCALE = 1.5

FADE_COEFFICIENT = 0.85


def is_hex_color(str):
    """Yeah I know, this is not pretty."""
    return (
        len(str) == 7
        and str.startswith("#")
        and all([c in digits + "abcdef" for c in str.lower()[1:]])
    )


def get_text_speed(text, speed_by_char=0.095):
    return len("".join(text.split())) * speed_by_char


def get_item_by_direction(items, direction):
    for i, d in enumerate(DIRECTIONS):
        if (direction == d).all():
            return items[i]


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
        color: str = WHITE,
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


class Wiggle(Animation):
    def __init__(
        self,
        mobject: "Mobject",
        scale_value: float = INDICATE_SCALE,
        rotation_angle: float = 0.02 * TAU,
        n_wiggles: int = 3,
        scale_about_point: Optional[np.ndarray] = None,
        rotate_about_point: Optional[np.ndarray] = None,
        run_time: float = 1.5,
        **kwargs,
    ) -> None:
        self.scale_value = scale_value
        self.rotation_angle = rotation_angle
        self.n_wiggles = n_wiggles
        self.scale_about_point = scale_about_point
        self.rotate_about_point = rotate_about_point
        super().__init__(mobject, run_time=run_time, **kwargs)

    def get_scale_about_point(self) -> np.ndarray:
        if self.scale_about_point is None:
            return self.mobject.get_center()

    def get_rotate_about_point(self) -> np.ndarray:
        if self.rotate_about_point is None:
            return self.mobject.get_center()

    def interpolate_submobject(
        self,
        submobject: "Mobject",
        starting_submobject: "Mobject",
        alpha: float,
    ) -> None:
        submobject.points[:, :] = starting_submobject.points
        submobject.scale(
            interpolate(1, self.scale_value, there_and_back_with_pause(alpha)),
            about_point=self.get_scale_about_point(),
        )
        submobject.rotate(
            wiggle(alpha, self.n_wiggles) * self.rotation_angle,
            about_point=self.get_rotate_about_point(),
        )


class Tile(VMobject):
    TEXT_SCALE = 0.6
    TEXT_OFFSET = 1 / 3.35

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
        for color, direction in zip(colors, DIRECTIONS):
            self.set_color_in_direction(color, direction, new=True)

        self.add_to_back(self.color_objects)

    def set_color_in_direction(self, color, direction, new=False):
        for i, d in enumerate(DIRECTIONS):
            if (direction == d).all():
                break

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

            if new:
                self.color_objects.add(triangle)
            else:
                self.color_objects[i] = triangle
        else:
            text = (
                Tex(color)
                .scale(Tile.TEXT_SCALE * self.size)
                .shift(direction * self.size * Tile.TEXT_OFFSET)
            )

            if new:
                self.color_objects.add(text)
            else:
                self.color_objects[i] = text

    def get_color_in_direction(self, direction):
        return get_item_by_direction(self.colors, direction)

    def get_color_object_in_direction(self, direction):
        return get_item_by_direction(self.color_objects, direction)

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
        self.color_object_characters = []

        self.w = width
        self.h = height

        for color, direction in zip(colors, DIRECTIONS):
            self.set_color_in_direction(color, direction, new=True)

        self.add(self.color_objects)

    def set_color_in_direction(self, color, direction, new=False):
        for i, d in enumerate(DIRECTIONS):
            if (direction == d).all():
                break

        c = 0.4  # outer offset
        d = 0  # inner offset

        # yeah, not pretty
        # I was tired and didn't want to think
        if (direction == UP).all():
            pos = [
                np.array([(self.w / 2) * self.size, (self.h / 2 + d) * self.size, 0]),
                np.array(
                    [(self.w / 2 - c) * self.size, (self.h / 2 + c) * self.size, 0]
                ),
                np.array(
                    [(-self.w / 2 + c) * self.size, (self.h / 2 + c) * self.size, 0]
                ),
                np.array([(-self.w / 2) * self.size, (self.h / 2 + d) * self.size, 0]),
            ]
        if (direction == DOWN).all():
            pos = [
                np.array([(self.w / 2) * self.size, (-self.h / 2 - d) * self.size, 0]),
                np.array(
                    [(self.w / 2 - c) * self.size, (-self.h / 2 - c) * self.size, 0]
                ),
                np.array(
                    [(-self.w / 2 + c) * self.size, (-self.h / 2 - c) * self.size, 0]
                ),
                np.array([(-self.w / 2) * self.size, (-self.h / 2 - d) * self.size, 0]),
            ]
        if (direction == LEFT).all():
            pos = [
                np.array([(-self.w / 2 - d) * self.size, (self.h / 2) * self.size, 0]),
                np.array(
                    [(-self.w / 2 - c) * self.size, (self.h / 2 - c) * self.size, 0]
                ),
                np.array(
                    [(-self.w / 2 - c) * self.size, (-self.h / 2 + c) * self.size, 0]
                ),
                np.array([(-self.w / 2 - d) * self.size, (-self.h / 2) * self.size, 0]),
            ]
        if (direction == RIGHT).all():
            pos = [
                np.array([(self.w / 2 + d) * self.size, (self.h / 2) * self.size, 0]),
                np.array(
                    [(self.w / 2 + c) * self.size, (self.h / 2 - c) * self.size, 0]
                ),
                np.array(
                    [(self.w / 2 + c) * self.size, (-self.h / 2 + c) * self.size, 0]
                ),
                np.array([(self.w / 2 + d) * self.size, (-self.h / 2) * self.size, 0]),
            ]

        if (direction == UP).all() and self.input is not None:
            g = VGroup()

            self.input_colors = []
            self.input_lines = []
            self.color_object_characters.append([])

            for i in range(len(self.input) + 1):
                c = (0.25 if i in (0, len(self.input)) else 0.5) * self.size
                line = Line(
                    start=[-self.w / 2 + i * self.size, self.h / 2, 0],
                    end=[-self.w / 2 + i * self.size, self.h / 2 + c, 0],
                )

                g.add(line)
                self.input_lines.append(line)

                if i < len(self.input):
                    p = [-self.w / 2 + (i + 0.5) * self.size, self.h / 2, 0]

                    text = (
                        Tex(self.input[i])
                        .scale(Tile.TEXT_SCALE * self.size)
                        .move_to(p)
                        .align_to(p, DOWN)
                        .shift(UP * Tile.TEXT_OFFSET / 2)
                    )

                    self.input_colors.append(text)
                    self.color_object_characters[-1].append(text)

                    g.add(text)

            if new:
                self.color_objects.add(g)
            else:
                self.color_objects[i] = g
        else:
            g = VGroup()

            side = Polygon(*pos).set_stroke(WHITE)
            if is_hex_color(color):
                g.add(side.set_fill(color, 1))

                if new:
                    self.color_object_characters.append(None)
                else:
                    self.color_object_characters[i] = None
            else:
                g.add(side)

                text = Tex(color).scale(Tile.TEXT_SCALE * self.size).move_to(side)

                g.add(text)

                if new:
                    self.color_object_characters.append(text)
                else:
                    self.color_object_characters[i] = text
            if new:
                self.color_objects.add(g)
            else:
                self.color_objects[i] = g

    def to_positive_coordinates(self, x, y):
        """Done so we can use -1."""
        return x % self.w, y % self.h

    def get_tile_position(self, x, y):
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

        tile.move_to(self.get_tile_position(x, y))

        self.tiles.add(tile)

        self.tile_position_dictionary[(x, y)] = tile

        return tile

    def get_tile(self, x, y):
        x, y = self.to_positive_coordinates(x, y)

        return self.tile_position_dictionary[(x, y)]

    def remove_tile(self, tile):
        self.tiles.remove(tile)

    def get_color_object_in_direction(self, direction):
        return get_item_by_direction(self.color_objects, direction)

    def get_color_in_direction(self, direction):
        if (direction == UP).all() and self.input is not None:
            return self.input
        else:
            return get_item_by_direction(self.colors, direction)

    def get_color_object_characters_in_direction(self, direction):
        return get_item_by_direction(self.color_object_characters, direction)

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

    def animateFillFlash(self):
        c = PI / 6
        return [
            PartialFlash(
                Dot().next_to(self, LEFT).shift(RIGHT * 0.8),
                start_angle=PI / 2 + c,
                end_angle=(PI / 2) * 3 - c,
            ),
            PartialFlash(
                Dot().next_to(self, RIGHT).shift(LEFT * 0.8),
                start_angle=-PI / 2 + c,
                end_angle=PI / 2 - c,
            ),
        ]


class TileSet(VMobject):
    def __init__(self, *tiles, rows=1, exclude_commas=False):
        super().__init__()

        self.tiles = VGroup(*tiles)
        self.tiles.arrange_in_grid(rows=rows, buff=0.6)

        self.commas = VGroup()

        n = len(tiles)
        for i in range(n - 1):
            if not exclude_commas:
                self.commas.add(
                    Tex("\Large $,$")
                    .next_to(self.tiles[i], DOWN + RIGHT, buff=0)
                    .shift(UP * 0.07 + RIGHT * 0.1)
                )

        brace_offset = -0.25
        self.braces = VGroup(
            BraceBetweenPoints(
                Point().next_to(self.tiles[-1], UP + LEFT).get_center(),
                Point().next_to(self.tiles[-1], DOWN + LEFT).get_center(),
                direction=LEFT,
            ).next_to(self.tiles[0], LEFT),
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

    def __iter__(self):
        return iter(self.tiles)


def IndicateColorCharacter(char):
    return Indicate(char, color=YELLOW, scale=INDICATE_SCALE)


def find_tiling_recursive(i, j, tileset: List[Tile], wallarray, w, h):
    def at(x, y):
        return wallarray[y + 1][x + 1]

    def set(x, y, tile):
        wallarray[y + 1][x + 1] = tile

    def equal_or_none(a, b):
        """If some of the tiles are none, it means that there is no color and it's ok"""
        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        # JESUS CHRIST BURN IT WITH FIRE
        # I SHALL NOT BE REDEEMED FOR WRITING THIS UNHOLY ABOMINATION
        return a == "None" or b == "None" or a == b

    # if we're past (on the very right tile)
    if i == w:
        # check if the tile on the left is ok
        if not equal_or_none(
            at(i - 1, j).get_color_in_direction(RIGHT),
            at(i, j).get_color_in_direction(LEFT),
        ):
            return

        if j == h - 1:
            return wallarray

        i = 0
        j += 1

    for tile in tileset.tiles:
        if not equal_or_none(
            at(i, j - 1).get_color_in_direction(DOWN), tile.get_color_in_direction(UP)
        ):
            continue

        if not equal_or_none(
            at(i - 1, j).get_color_in_direction(RIGHT),
            tile.get_color_in_direction(LEFT),
        ):
            continue

        # if we're last row
        if j == h - 1:
            if not equal_or_none(
                at(i, j + 1).get_color_in_direction(UP),
                tile.get_color_in_direction(DOWN),
            ):
                continue

        set(i, j, tile)
        result = find_tiling_recursive(i + 1, j, tileset, wallarray, w, h)
        if result is not None:
            return result
        set(i, j, None)


def find_tiling(
    tileset: List[Tile],
    wall: Wall,
    w=None,
    min_height=1,
    max_height=1,
    ignore_sides=False,
):
    """Find if there exists a tiling of maximal height for a given wall."""
    if w is None:
        w = wall.w

    for h in range(min_height, max_height + 1):
        wallarray = [[None] * (w + 2) for _ in range(h + 2)]

        for i in range(1, w + 1):
            wallarray[0][i] = Tile(
                [None, None, None, None if ignore_sides else wall.input[i - 1]]
            )

        for i in range(1, w + 1):
            wallarray[-1][i] = Tile(
                [
                    None,
                    None if ignore_sides else wall.get_color_in_direction(DOWN),
                    None,
                    None,
                ]
            )

        for i in range(1, h + 1):
            wallarray[i][-1] = Tile(
                [
                    None,
                    None,
                    None if ignore_sides else wall.get_color_in_direction(RIGHT),
                    None,
                ]
            )

        for i in range(1, h + 1):
            wallarray[i][0] = Tile(
                [
                    None if ignore_sides else wall.get_color_in_direction(LEFT),
                    None,
                    None,
                    None,
                ]
            )

        result = find_tiling_recursive(0, 0, tileset, wallarray, w, h)

        if result is not None:
            wall = Wall(wall.colors, wall.input, width=w, height=h)

            for x in range(w):
                for y in range(h):
                    wall.add_tile(result[y + 1][x + 1], x, y, copy=True)

            return wall


def animate_tile_pasting(tile, wall, positions, speed=0.07, run_time=1.2):
    def DelayedTransform(x, y, t):
        return Transform(
            x,
            y,
            run_time=run_time + t,
            rate_func=lambda a: smooth(
                a if t == 0 else (0 if a < t else (a - t) / (1 - t))
            ),
        )

    n = len(positions)

    from_tiles = [tile.copy() for _ in range(n)]
    to_tiles = [
        tile.copy().move_to(wall.get_tile_position(*position)) for position in positions
    ]

    return (
        [
            DelayedTransform(from_tiles[i], to_tiles[i], speed * (n - i - 1))
            for i in range(n)
        ],
        from_tiles,
        positions,
    )


class WriteReverse(Write):
    """A special write for a tile and wall (since we want the animation to be reversed)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, reverse=True)


examples = {
    "even_size": (
        Wall([BLACK, None, BLACK, BLACK], height=1, input="111111"),
        TileSet(
            Tile([PALETTE[2], 1, PALETTE[1], PALETTE[0]]),
            Tile([PALETTE[1], 1, PALETTE[2], PALETTE[0]]),
        ),
    ),
    "divby3": (
        Wall([0, None, 0, PALETTE[0]], height=1, input="10110111"),
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
        Wall([PALETTE[3], None, PALETTE[3], PALETTE[3]], input="(()())()", height=2),
        TileSet(
            Tile([PALETTE[2], "(", PALETTE[3], PALETTE[3]]),
            Tile([PALETTE[3], ")", PALETTE[2], PALETTE[3]]),
            Tile([PALETTE[3], "(", PALETTE[3], PALETTE[1]]),
            Tile([PALETTE[3], PALETTE[1], PALETTE[3], PALETTE[1]]),
            Tile([PALETTE[1], PALETTE[3], PALETTE[1], PALETTE[3]]),
            Tile([PALETTE[1], PALETTE[1], PALETTE[3], PALETTE[3]]),
            Tile([PALETTE[3], PALETTE[0], PALETTE[1], PALETTE[3]]),
            Tile([PALETTE[3], PALETTE[0], PALETTE[3], PALETTE[0]]),
            Tile([PALETTE[3], ")", PALETTE[3], PALETTE[0]]),
            Tile([PALETTE[3], PALETTE[3], PALETTE[3], PALETTE[3]]),
        ),
    ),
    "parentheses_log": (
        Wall([PALETTE[0], None, PALETTE[0], PALETTE[0]], input="()(())"),
        TileSet(
            Tile([1, "(", PALETTE[0], PALETTE[0]]),
            Tile([1, "(", 0, PALETTE[0]]),
            Tile([0, "(", 1, "("]),
            Tile([1, PALETTE[0], 1, PALETTE[0]]),
            Tile([0, PALETTE[0], 0, PALETTE[0]]),
            Tile([0, ")", 1, PALETTE[0]]),
            Tile([1, ")", 0, ")"]),
            Tile([PALETTE[0], ")", 1, PALETTE[0]]),
            Tile([PALETTE[0], PALETTE[0], 0, PALETTE[0]]),
            Tile([PALETTE[0], PALETTE[0], PALETTE[0], PALETTE[0]]),
        ),
    ),
    "parentheses_log_compact": (
        Wall([0, None, 0, 0], input="()(())"),
        TileSet(
            Tile([0, "(", 1, "("]),
            Tile([1, "(", 0, 0]),
            Tile([0, 0, 0, 0]),
            Tile([1, 0, 1, 0]),
            Tile([0, ")", 1, 0]),
            Tile([1, ")", 0, ")"]),
        ),
    ),
    "power_of_two": (
        Wall([1, None, PALETTE[0], ""], input="11111111"),
        TileSet(
            Tile([0, 1, PALETTE[0], ""]),
            Tile([0, "", PALETTE[0], ""]),
            Tile([0, 1, 1, 1]),
            Tile([1, 1, 0, ""]),
            Tile([0, "", 0, ""]),
            Tile([1, "", 1, ""]),
            Tile([1, 1, PALETTE[0], ""]),
        ),
    ),
    "divisibleby": (
        Wall([0, None, 0, PALETTE[0]], input="2270268"),
        TileSet(
            *[
                Tile([(j * 10 + i) % 13, i, j, PALETTE[0]])
                for i in range(10)
                for j in range(13)
            ]
        ),
    ),
    "palindrome": (
        Wall([PALETTE[0], None, PALETTE[1], ""], input="10111101"),
        TileSet(
            Tile([0, "0", PALETTE[1], ""]),
            Tile([PALETTE[0], "0", 0, ""]),
            Tile([1, "1", PALETTE[1], ""]),
            Tile([PALETTE[0], "1", 1, ""]),
            Tile([PALETTE[0], "", PALETTE[0], ""]),
            Tile([PALETTE[1], "", PALETTE[1], ""]),
            Tile([1, "1", 1, "1"]),
            Tile([1, "0", 1, "0"]),
            Tile([0, "1", 0, "1"]),
            Tile([0, "0", 0, "0"]),
            Tile([PALETTE[0], 0, PALETTE[1], ""]),
            Tile([PALETTE[0], 1, PALETTE[1], ""]),
        ),
    ),
}


class WebExampleParenthesesLogMinimal(Scene):
    def construct(self):

        wall, tileset = examples["parentheses_log_compact"]

        result_wall = find_tiling(tileset, wall, max_height=2).next_to(tileset, DOWN)

        g = VGroup(tileset, result_wall).move_to(ORIGIN).scale(1.3)

        tileset = tileset.scale(0.6)

        for i, (text, start, end) in enumerate(
            [
                ("start + increment", tileset[0], tileset[1]),
                ("carry", tileset[2], tileset[3]),
                ("end + decrement", tileset[4], tileset[5]),
            ]
        ):
            b = BraceBetweenPoints(
                Point().next_to(start, UP + LEFT, buff=0).get_center(),
                Point().next_to(end, UP + RIGHT, buff=0).get_center(),
                direction=UP,
                color=NOTES_COLOR,
            ).scale([-1, NOTES_SCALE, 1])

            bl = (
                Tex(text, color=NOTES_COLOR)
                .next_to(b, UP)
                .scale(NOTES_SCALE)
                .shift(DOWN * 0.1)
            )

            if i == 1:
                bl.shift(DOWN * 0.05)

            g.add(b)
            g.add(bl)

        g.move_to(ORIGIN)
        self.add(g)


class WebExampleParenthesesLog(Scene):
    def construct(self):

        wall, tileset = examples["parentheses_log"]

        result_wall = find_tiling(tileset, wall, max_height=2).next_to(tileset, DOWN)

        g = VGroup(tileset, result_wall).move_to(ORIGIN).scale(1.3)

        tileset = tileset.scale(0.6)

        for i, (text, start, end) in enumerate(
            [
                ("start", tileset[0], tileset[0]),
                ("increment", tileset[1], tileset[2]),
                ("carry over", tileset[3], tileset[4]),
                ("decrement", tileset[5], tileset[6]),
                ("end", tileset[7], tileset[8]),
                ("fill", tileset[9], tileset[9]),
            ]
        ):
            b = BraceBetweenPoints(
                Point().next_to(start, UP + LEFT, buff=0).get_center(),
                Point().next_to(end, UP + RIGHT, buff=0).get_center(),
                direction=UP,
                color=NOTES_COLOR,
            ).scale([-1, NOTES_SCALE, 1])

            bl = (
                Tex(text, color=NOTES_COLOR)
                .next_to(b, UP)
                .scale(NOTES_SCALE)
                .shift(DOWN * 0.1)
            )

            if i == 2:
                bl.shift(DOWN * 0.05)

            g.add(b)
            g.add(bl)

        g.move_to(ORIGIN)
        self.add(g)


class WebExamplePowerOfTwo(Scene):
    def construct(self):

        wall, tileset = examples["power_of_two"]

        result_wall = find_tiling(tileset, wall, max_height=3).next_to(tileset, DOWN)

        tileset = tileset.scale(0.9)

        g = VGroup(tileset, result_wall)

        for i, (text, start, end) in enumerate(
            [
                ("eat the first one", tileset[0], tileset[1]),
                ("increment", tileset[2], tileset[3]),
                ("carry", tileset[4], tileset[5]),
                ("accept '1' too", tileset[6], tileset[6]),
            ]
        ):
            b = BraceBetweenPoints(
                Point().next_to(start, UP + LEFT, buff=0).get_center(),
                Point().next_to(end, UP + RIGHT, buff=0).get_center(),
                direction=UP,
                color=NOTES_COLOR,
            ).scale([-1, NOTES_SCALE, 1])

            bl = (
                Tex(text, color=NOTES_COLOR)
                .next_to(b, UP)
                .scale(NOTES_SCALE)
                .shift(DOWN * 0.1)
            )

            if i == 2 or i == 3:
                bl.shift(DOWN * 0.05)

            g.add(b)
            g.add(bl)

        g.move_to(ORIGIN)
        self.add(g)


class WebExampleDivisible(Scene):
    def construct(self):

        wall, tileset = examples["divisibleby"]

        result_wall = (
            find_tiling(tileset, wall, max_height=1)
            .scale(1.4)
            .next_to(tileset, DOWN)
            .shift(DOWN * 0.7)
        )

        TileSet(
            *[Tile([(j * 10 + i) % 13, i, j, ""]) for i in range(10) for j in range(13)]
        ),

        tileset = TileSet(
            Tex("all tiles in the form"),
            Tile(["j", "i", r"$k$", PALETTE[0]]),
            Tex(
                r"$\substack { {\forall i \in \left\{0, \ldots, 9\right\} } \\ {\forall j \in \left\{0, \ldots, 12\right\} } \\ {\forall k = (10j + i)\ \mathrm{mod}\ 13} }$"
            ),
            exclude_commas=True,
        )

        g = VGroup(tileset, result_wall).scale(1.2)

        g.move_to(ORIGIN)
        self.add(g)


class WebExamplePalindrome(Scene):
    def construct(self):

        wall, tileset = examples["palindrome"]

        result_wall = find_tiling(tileset, wall, max_height=4).next_to(tileset, DOWN)

        g = VGroup(tileset, result_wall).move_to(ORIGIN)

        tileset = tileset.scale(0.60)

        for i, (text, start, end) in enumerate(
            [
                ("start/end 0", tileset[0], tileset[1]),
                ("start/end 1", tileset[2], tileset[3]),
                ("carry sides", tileset[4], tileset[5]),
                ("carry input to next row", tileset[6], tileset[9]),
                ("odd size", tileset[10], tileset[11]),
            ]
        ):
            b = BraceBetweenPoints(
                Point().next_to(start, UP + LEFT, buff=0).get_center(),
                Point().next_to(end, UP + RIGHT, buff=0).get_center(),
                direction=UP,
                color=NOTES_COLOR,
            ).scale([-1, NOTES_SCALE, 1])

            bl = (
                Tex(text, color=NOTES_COLOR)
                .next_to(b, UP)
                .scale(NOTES_SCALE * 0.80)
                .shift(DOWN * 0.1)
            )

            if i == 0 or i == 1:
                bl.shift(DOWN * 0.05)

            if i == 4:
                bl.shift(UP * 0.07)

            g.add(b)
            g.add(bl)

        g.move_to(ORIGIN)
        self.add(g)


class FadeOutDirection(Transform):
    def __init__(
        self,
        mobject,
        dir,
        rate_func=smooth,
        move_factor=0.35,
        run_time=1,
        **kwargs,
    ) -> None:
        self.move_factor = move_factor
        self.obj = mobject
        self.dir = dir
        super().__init__(mobject, rate_func=rate_func, run_time=run_time, **kwargs)

    def create_target(self) -> "Mobject":
        target = self.obj.copy().shift(self.dir * self.move_factor).set_opacity(0)
        return target


def FadeOutUp(obj, *args, **kwargs):
    return FadeOutDirection(obj, UP, *args, **kwargs)


def FadeOutDown(obj, *args, **kwargs):
    return FadeOutDirection(obj, DOWN, *args, **kwargs)


class FadeInDirection(Transform):
    def __init__(
        self,
        mobject,
        dir,
        rate_func=lambda x: smooth(1 - x),
        move_factor=0.35,
        run_time=1,
        **kwargs,
    ) -> None:
        self.move_factor = move_factor
        self.obj = mobject
        self.dir = -dir
        super().__init__(mobject, rate_func=rate_func, run_time=run_time, **kwargs)

    def create_target(self) -> "Mobject":
        target = self.obj.copy().shift(self.dir * self.move_factor).set_opacity(0)
        return target


def FadeInUp(obj, *args, **kwargs):
    return FadeInDirection(obj, UP, *args, **kwargs)


def FadeInRight(obj, *args, **kwargs):
    return FadeInDirection(obj, RIGHT, *args, **kwargs)


def FadeInDown(obj, *args, **kwargs):
    return FadeInDirection(obj, DOWN, *args, **kwargs)


class HighlightedTex(Tex):
    def __init__(self, text, sep="|", color=YELLOW):
        super().__init__(*[s for s in text.split(sep) if len(s) != 0])

        c = 0
        for i in range(0 if text[0] == sep else 1, len(self), 2):
            if type(color) is str:
                self[i].set_color(color)
            else:
                self[i].set_color(color[c])
                c += 1


def WriteText(text):
    return Write(
        text,
        run_time=get_text_speed(
            text.text if isinstance(text, Text) else text.tex_string
        ),
    )


class BumpUp(Transform):
    def __init__(
        self,
        mobject: "Mobject",
        move_factor: float = 0.35,
        rate_func=there_and_back,
        **kwargs,
    ) -> None:
        self.move_factor = move_factor
        self.obj = mobject
        super().__init__(mobject, rate_func=rate_func, **kwargs)

    def create_target(self) -> "Mobject":
        target = self.obj.copy().shift(UP * self.move_factor)
        return target


class Motivation(MovingCameraScene):
    def construct(self):
        p1 = SVGMobject("assets/pillar.svg").scale(2.8).shift(LEFT * 4.8)
        p2 = SVGMobject("assets/pillar.svg").scale(2.8).shift(RIGHT * 4.8)

        ft = Text("Eureka!", font="Gelio Pasteli").scale(2)

        archimedes = (
            Text("– Archimedes", font="Gelio Pasteli")
            .scale(0.7)
            .next_to(ft, DOWN)
            .align_to(ft, RIGHT)
        )

        g = VGroup(ft, archimedes).move_to(ORIGIN)

        text_write_duration = 1

        self.play(
            FadeInUp(p1),
            FadeInUp(p2),
        )

        self.play(
            AnimationGroup(
                Write(ft, run_time=text_write_duration),
                Write(archimedes, run_time=text_write_duration),
                lag_ratio=0.8,
            )
        )

        offset = 1.2

        ft2 = Text("Bathroom tiles!").scale(1.0).shift(DOWN * offset)
        tom = Text("- Tom").scale(0.6).next_to(ft2, DOWN).align_to(ft2, RIGHT)

        g2 = VGroup(ft2, tom)
        g2.move_to(ORIGIN).shift(DOWN * offset)

        laptop = SVGMobject("assets/laptop.svg").shift(DOWN * 1.5)
        water = (
            SVGMobject("assets/water.svg")
            .scale(0.35)
            .next_to(laptop, UP + LEFT)
            .shift(RIGHT * 0.75 + DOWN * 0.73)
        )
        bolt = (
            SVGMobject("assets/bolt.svg").scale(0.30).move_to(laptop).shift(UP * 0.37)
        )

        self.play(
            g.animate.shift(UP * offset),
            FadeInUp(laptop),
        )

        self.play(
            AnimationGroup(
                FadeInUp(water),
                Write(bolt),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                FadeOutUp(VGroup(water, bolt, laptop)),
                AnimationGroup(
                    Write(ft2, run_time=text_write_duration),
                    Write(tom, run_time=text_write_duration / 3),
                    lag_ratio=0.8,
                ),
                lag_ratio=1,
            )
        )

        # bug?
        self.add(ft2)
        self.add(tom)

        w = 9
        h = 3

        wall = Wall(PALETTE, width=w, height=h)

        bl = BraceBetweenPoints([-w / 2, h / 2, 0], [-w / 2, -h / 2, 0])
        blt = Tex("\\footnotesize h").next_to(bl, LEFT * 0.5)

        bu = BraceBetweenPoints(
            [-w / 2, h / 2, 0], [w / 2, h / 2, 0], direction=UP
        ).scale([-1, 1, 0])
        but = Tex("\\footnotesize w").next_to(bu, UP * 0.5)

        self.play(
            AnimationGroup(
                AnimationGroup(*map(FadeOutUp, self.mobjects)),
                Write(wall.border),
                lag_ratio=0.8,
            )
        )

        self.play(Write(bu), Write(but))
        self.play(Write(bl), Write(blt))

        seed(3)
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

        self.play(
            AnimationGroup(
                FadeOut(VGroup(bl, blt, bu, but)),
                Write(wall.color_objects),
                AnimationGroup(*changes.values()),
                lag_ratio=0.6,
            )
        )

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

        tileset = TileSet(*tiles)

        self.play(
            AnimationGroup(
                *[FadeOut(t) for t in wall.tiles], lag_ratio=0.01, run_time=1
            )
        )

        for t in wall.tiles:
            wall.remove_tile(t)

        wall.generate_target()
        wall.target.shift(DOWN * 1.1)
        wall.target.get_color_object_in_direction(LEFT).set_fill(REDUCED_PALETTE[0])
        wall.target.get_color_object_in_direction(DOWN).set_fill(REDUCED_PALETTE[1])
        wall.target.get_color_object_in_direction(RIGHT).set_fill(REDUCED_PALETTE[0])

        tileset.next_to(wall.target, UP).shift(UP * 0.5)

        self.play(
            AnimationGroup(MoveToTarget(wall), tileset.animateWrite(), lag_ratio=0.8),
        )

        question = Tex("?").scale(QUESTION_MARK_SCALE).move_to(wall)

        self.play(Write(question))
        self.play(FadeOutUp(question))

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

        cross_size = 0.6

        cross = VGroup()
        r1 = Line(
            start=(UP + LEFT) * cross_size,
            end=(DOWN + RIGHT) * cross_size,
            stroke_width=6,
        ).set_stroke("#8b0000")
        r2 = Line(
            start=(RIGHT + UP) * cross_size,
            end=(DOWN + LEFT) * cross_size,
            stroke_width=6,
        ).set_stroke("#8b0000")

        cross.add(r1)
        cross.add(r2)

        self.play(
            from_tile_wrong.animate.move_to(wall.get_tile_position(4, 0)).rotate(
                -PI / 2
            )
        )

        cross.move_to(from_tile_wrong)

        self.play(Write(cross, run_time=0.5))
        self.play(FadeOutUp(from_tile_wrong), FadeOutUp(cross))

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
        for i in range(wall.w):
            wall.remove_tile(wall.get_tile(i, 0))


TASK_OFFSET = 0.6 * UP
WALL_OFFSET = 1.7 * DOWN
TILESET_OFFSET = UP * 0.7


class ProgrammingModel(Scene):
    @fade
    def construct(self):
        title = Tex("\Large Programming model")

        self.play(FadeInUp(title))
        self.play(title.animate.shift(UP * 2.5))

        text = [
            (Tex("Input:"), HighlightedTex("|colors| on the |top side| of the wall")),
            (
                Tex("Program:"),
                HighlightedTex(
                    "finite set of |tile types| and the |remaining wall colors|"
                ),
            ),
            (
                Tex("Output:"),
                HighlightedTex(
                    "|accept| if there exists valid tiling, else |reject| it",
                    color=[GREEN, RED],
                ),
            ),
        ]

        # align text to a grid
        text_scale = 0.85
        for i in range(len(text)):
            text[i][0].scale(text_scale).next_to(text[i - 1][0], DOWN).align_to(
                text[i - 1][0], RIGHT
            )
            text[i][1].scale(text_scale).next_to(text[i][0], RIGHT)

        # and move it
        g = VGroup()
        for i in range(len(text)):
            g.add(text[i][0])
            g.add(text[i][1])
        g.move_to(ORIGIN).shift(UP * 0.7)

        wall, tileset = examples["even_size"]
        wall = wall.shift(DOWN * 2)

        self.play(FadeInUp(text[0][0]))

        self.play(Write(text[0][1]), wall.animateWrite(), run_time=2.1)

        self.play(
            AnimationGroup(
                *[
                    Wiggle(wall.get_color_object_characters_in_direction(UP)[i])
                    for i in range(len(wall.input))
                ],
                lag_ratio=0.08,
            )
        )

        tileset.next_to(wall, RIGHT, buff=1)

        g = VGroup(tileset, wall)

        self.play(
            wall.animate.set_x(wall.get_x() - g.get_x()),
            FadeInUp(text[1][0]),
        )

        tileset.next_to(wall, RIGHT, buff=1)

        self.play(
            Write(text[1][1], run_time=2.8),
            AnimationGroup(
                tileset.animateWrite(),
                AnimationGroup(
                    wall.get_color_object_in_direction(LEFT).animate.set_fill(
                        PALETTE[1]
                    ),
                    wall.get_color_object_in_direction(DOWN).animate.set_fill(
                        PALETTE[0]
                    ),
                    wall.get_color_object_in_direction(RIGHT).animate.set_fill(
                        PALETTE[1]
                    ),
                ),
                lag_ratio=1,
            ),
        )

        self.play(FadeInUp(text[2][0]))

        n = 24
        self.play(Write(VGroup(text[2][1][0], text[2][1][1][:n]), run_time=1.8))

        self.play(
            Write(VGroup(text[2][1][1][n:], text[2][1][2], text[2][1][3]), run_time=1)
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOutUp(title),
                    *[
                        FadeOutUp(text[i][j])
                        for i in range(len(text))
                        for j in range(len(text[0]))
                    ],
                ),
                AnimationGroup(
                    tileset.animate.move_to(ORIGIN).shift(TILESET_OFFSET),
                    wall.animate.move_to(ORIGIN).shift(WALL_OFFSET),
                ),
                lag_ratio=0.0,
            ),
            run_time=1.5,
        )

        task = (
            HighlightedTex(
                r"{\bf Task:} |accept| input \(\Leftrightarrow\) it has even length",
                color=GREEN,
            )
            .next_to(tileset, UP)
            .shift(TASK_OFFSET)
        )

        self.play(FadeInUp(task))

        for i in range(wall.w // 2):
            animations, tiles, positions = animate_tile_pasting(
                tileset[i % 2], wall, [(i, 0)]
            )
            animations2, tiles2, positions2 = animate_tile_pasting(
                tileset[(i + 1) % 2], wall, [(wall.w - i - 1, 0)]
            )
            self.play(*animations, *animations2)

            if i != wall.w // 2 - 1:
                self.play(
                    Swap(tileset[0], tileset[1], path_arc=160 * DEGREES, run_time=1.25)
                )

            wall.add_tiles(tiles, positions)
            wall.add_tiles(tiles2, positions2)

        self.play(*wall.animateFillFlash())

        wall_old = wall
        tileset_old = tileset
        task_old = task

        wall, tileset = examples["divby3"]
        tileset.move_to(ORIGIN).shift(TILESET_OFFSET)
        wall.move_to(ORIGIN).shift(WALL_OFFSET)

        task = (
            HighlightedTex(
                r"{\bf Task:} |accept| input \(\Leftrightarrow\) \# of ones is divisible by 3",
                color=GREEN,
            )
            .next_to(tileset, UP)
            .shift(TASK_OFFSET)
        )

        # TODO: maybe edit this later
        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOutUp(wall_old), FadeOutUp(tileset_old), FadeOutUp(task_old)
                ),
                AnimationGroup(FadeInUp(wall), FadeInUp(tileset), FadeInUp(task)),
                lag_ratio=0.6,
            )
        )

        nums = [
            Tex(str(wall.input[: i + 1].count("1")), color=NOTES_COLOR)
            .scale(NOTES_SCALE)
            .next_to(wall.get_color_object_characters_in_direction(UP)[i], UP)
            for i in range(len(wall.input))
        ]

        self.play(
            AnimationGroup(
                *[
                    Wiggle(wall.get_color_object_characters_in_direction(UP)[i])
                    for i in range(len(wall.input))
                    if wall.input[i] == "1"
                ],
                lag_ratio=0.08,
            )
        )

        nums = [
            Tex(str(wall.input[: i + 1].count("1")), color=NOTES_COLOR)
            .scale(NOTES_SCALE)
            .next_to(wall.get_color_object_characters_in_direction(UP)[i], UP)
            for i in range(len(wall.input))
        ]

        nums_lag = 0.3
        nums_run_time = 1.5

        self.play(
            AnimationGroup(
                *([FadeInUp(n) for n in nums]),
                lag_ratio=nums_lag,
                run_time=nums_run_time,
            ),
        )

        nums_transformed = [
            Tex(str(wall.input[: i + 1].count("1") % 3), color=NOTES_COLOR)
            .scale(NOTES_SCALE)
            .move_to(nums[i])
            for i in range(len(nums))
        ]

        self.play(
            AnimationGroup(
                *[
                    AnimationGroup(
                        FadeOutUp(a, move_factor=0.25), FadeInUp(b, move_factor=0.25)
                    )
                    for a, b in zip(nums[3:], nums_transformed[3:])
                ],
                lag_ratio=nums_lag,
                run_time=nums_run_time,
            )
        )

        bs = []

        brace_offset = 0.25
        for i, (text, start, end) in enumerate(
            [
                ("carry", tileset[0], tileset[2]),
                ("increment", tileset[3], tileset[5]),
            ]
        ):
            b = BraceBetweenPoints(
                Point().next_to(start, UP + LEFT, buff=0).get_center(),
                Point().next_to(end, UP + RIGHT, buff=0).get_center(),
                direction=UP,
                color=NOTES_COLOR,
            ).scale([-1, NOTES_SCALE, 1])

            bl = (
                Tex(text, color=NOTES_COLOR)
                .next_to(b, UP)
                .scale(NOTES_SCALE)
                .shift(DOWN * 0.1)
            )

            bs += [b, bl]

            self.play(
                *[
                    Wiggle(
                        t.get_color_object_in_direction(UP),
                        run_time=2.5,
                        n_wiggles=5,
                    )
                    for t in tileset
                ][i * 3 : (i + 1) * 3]
            )

            self.play(
                FadeInUp(b),
                FadeInUp(bl)
                if i == 1
                else AnimationGroup(FadeInUp(bl), task.animate.shift(UP * 0.3)),
            )

            self.play(
                AnimationGroup(
                    *[
                        AnimationGroup(
                            Wiggle(
                                t.get_color_object_in_direction(LEFT),
                            ),
                            Wiggle(
                                t.get_color_object_in_direction(RIGHT),
                            ),
                            lag_ratio=0.1,
                        )
                        for t in tileset
                    ][i * 3 : (i + 1) * 3],
                    lag_ratio=0.35,
                )
            )

        for i, (tile, positions) in enumerate(
            [
                (3, [(0, 0)]),
                (1, [(1, 0)]),
                (4, [(2, 0)]),
                (5, [(3, 0)]),
                (0, [(4, 0)]),
                (3, [(5, 0)]),
                (4, [(6, 0)]),
                (5, [(7, 0)]),
            ]
        ):
            animations, tiles, positions = animate_tile_pasting(
                tileset[tile], wall, positions
            )

            self.play(*animations, run_time=1 - (i / wall.w) * 0.5)
            self.play(
                Wiggle(tiles[0].get_color_object_in_direction(RIGHT)),
                Wiggle((nums if i < 3 else nums_transformed)[i]),
                run_time=1.5,
            )

            wall.add_tiles(tiles, positions)

        self.play(*wall.animateFillFlash())

        self.play(
            AnimationGroup(
                *[
                    Wiggle(wall.get_color_object_characters_in_direction(UP)[i])
                    for i in range(len(wall.input))
                    if wall.input[i] == "1"
                ],
                lag_ratio=0.08,
            )
        )


class TimeComplexity(Scene):
    @fade
    def construct(self):
        title = Tex("\Large Time Complexity")

        self.play(FadeInUp(title))

        traditional = Tex("Traditional model")
        traditional_text = (
            Tex(
                "\parbox{15em}{Minimum number of instructions needed to compute the solution, based on the size of the input.}"
            )
            .scale(0.7)
            .next_to(traditional, DOWN)
            .shift(DOWN * 0.2)
        )

        for i, j in ((0, 7), (15, 27), (35, 42), (64, 80)):
            traditional_text[0][i:j].set_color(YELLOW)

        traditional_group = VGroup(traditional, traditional_text)
        traditional_group.move_to(ORIGIN).shift(LEFT * 3.2 + UP * 0.5)

        bathroom = Tex("Bathroom model")
        bathroom_text = (
            HighlightedTex(
                "\parbox{15em}{Minimum number of rows needed to accept the input, based on the size of the input.}"
            )
            .scale(0.7)
            .next_to(bathroom, DOWN)
            .shift(DOWN * 0.2)
        )

        for i, j in ((0, 7), (15, 19), (27, 33), (52, 73)):
            bathroom_text[0][i:j].set_color(YELLOW)

        bathroom_group = VGroup(bathroom, bathroom_text)
        bathroom_group.move_to(ORIGIN).shift(RIGHT * 3.2 + UP * 0.5)

        self.play(
            AnimationGroup(
                title.animate.shift(UP * 2.5),
                AnimationGroup(FadeInUp(traditional), FadeInUp(bathroom), run_time=0.8),
                lag_ratio=0.2,
            )
        )

        self.play(Write(traditional_text, run_time=3.5))

        traditional_examples = (
            Tex(
                r"""
                \begin{itemize}
                \itemsep0em
                \item {\bf Bubble sort:} \(\mathcal{O}(n^2)\)
                \item {\bf Binary search:} \(\mathcal{O}(\log n)\)
                \end{itemize}
                """
            )
            .scale(0.7)
            .next_to(traditional_text, DOWN)
            .shift(DOWN * 0.2)
        )

        bathroom_examples = (
            Tex(
                r"""
                \begin{itemize}
                \itemsep0em
                \item {\bf Even length:} \(\mathcal{O}(1)\)
                \item {\bf 3\(n\) ones in input:} \(\mathcal{O}(1)\)
                \end{itemize}
                """
            )
            .scale(0.7)
            .next_to(bathroom_text, DOWN)
            .shift(DOWN * 0.2)
        )

        n = 17
        self.play(FadeInUp(traditional_examples[0][0:n]))
        self.play(FadeInUp(traditional_examples[0][n:]))

        question = (
            Tex("?")
            .scale(QUESTION_MARK_SCALE)
            .move_to(VGroup(bathroom_text, *bathroom_examples))
        )

        self.play(Write(question))

        self.play(
            AnimationGroup(
                FadeOutDown(question),
                Write(bathroom_text, run_time=3.5),
                lag_ratio=0.3,
            )
        )

        n = 16
        self.play(
            AnimationGroup(
                FadeInUp(bathroom_examples[0][0:n]),
                FadeInUp(bathroom_examples[0][n:]),
                lag_ratio=0.3,
            )
        )


class ParenthesesExample(Scene):
    @fade
    def construct(self):
        task = HighlightedTex(
            r"{\bf Task:} |accept| input \(\Leftrightarrow\) parentheses are balanced",
            color=GREEN,
        )

        self.play(FadeInUp(task))

        parentheses = Tex("$(\ (\ )\ (\ )\ )\ (\ )$").next_to(task, DOWN).scale(2)

        self.play(
            AnimationGroup(
                task.animate.shift(UP),
                FadeInUp(parentheses),
            )
        )

        def BracketBetweenPoints(
            p1, p2, direction=UP, color=WHITE, width=0.06, height=0.22, **kwargs
        ):
            w = width
            h = height

            r1 = Rectangle(width=w, height=h).next_to(p1, direction, buff=0)
            r3 = Rectangle(width=w, height=h).next_to(p2, direction, buff=0)

            r2 = (
                Rectangle(width=(abs(p1[0] - p2[0]) + w), height=w)
                .align_to(r1, direction)
                .set_x((r1.get_x() + r3.get_x()) / 2)
            )

            return Union(r1, r2, r3, fill_color=color, fill_opacity=1, stroke_width=0)

        braces = [
            BracketBetweenPoints(
                Dot().next_to(parentheses[0][0], DOWN, buff=0.1).get_center(),
                Dot().next_to(parentheses[0][5], DOWN, buff=0.1).get_center(),
                direction=DOWN,
                height=0.43,
                color=GRAY,
            ).scale(0.95),
            BracketBetweenPoints(
                Dot().next_to(parentheses[0][1], DOWN, buff=0.1).get_center(),
                Dot().next_to(parentheses[0][2], DOWN, buff=0.1).get_center(),
                direction=DOWN,
                color=GRAY,
            ).scale(0.78),
            BracketBetweenPoints(
                Dot().next_to(parentheses[0][3], DOWN, buff=0.1).get_center(),
                Dot().next_to(parentheses[0][4], DOWN, buff=0.1).get_center(),
                direction=DOWN,
                color=GRAY,
            ).scale(0.78),
            BracketBetweenPoints(
                Dot().next_to(parentheses[0][6], DOWN, buff=0.1).get_center(),
                Dot().next_to(parentheses[0][7], DOWN, buff=0.1).get_center(),
                direction=DOWN,
                color=GRAY,
            ).scale(0.78),
        ]

        self.play(
            FadeInUp(braces[0], move_factor=0.1),
            FadeInUp(braces[1], move_factor=0.1),
            FadeInUp(braces[2], move_factor=0.1),
            FadeInUp(braces[3], move_factor=0.1),
            run_time=0.65,
        )

        wall, tileset = examples["parentheses"]
        tileset_scale = 0.7

        tileset.scale(tileset_scale)

        tileset.move_to(ORIGIN).shift(TILESET_OFFSET).shift(UP * 0.5)
        wall.move_to(ORIGIN).shift(WALL_OFFSET * 0.8)

        for i in range(len(wall.input)):
            wall.get_color_object_in_direction(UP).remove(
                wall.get_color_object_characters_in_direction(UP)[i]
            )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    task.animate.next_to(tileset, UP).shift(TASK_OFFSET * 0.8),
                    AnimationGroup(
                        FadeOutUp(braces[0], move_factor=0.1),
                        FadeOutUp(braces[1], move_factor=0.1),
                        FadeOutUp(braces[2], move_factor=0.1),
                        FadeOutUp(braces[3], move_factor=0.1),
                        run_time=0.5,
                    ),
                    *[
                        Transform(
                            parentheses[0][i],
                            wall.get_color_object_characters_in_direction(UP)[i].copy(),
                        )
                        for i in range(len(wall.input))
                    ],
                    run_time=1,
                ),
                AnimationGroup(
                    FadeInUp(wall),
                    FadeInUp(tileset),
                    run_time=0.7,
                ),
                lag_ratio=0.3,
            )
        )

        tileset.scale(1 / tileset_scale)

        result_wall = find_tiling(tileset, wall, max_height=2)

        for i in range(wall.w):
            for j in range(wall.h):
                wall.add_tile(result_wall.get_tile(i, j), i, j, copy=True)

        tileset.scale(tileset_scale)

        self.play(
            AnimationGroup(*[t.animateWrite() for t in wall.tiles], lag_ratio=0.01)
        )

        self.play(*wall.animateFillFlash())

        for i in range(wall.w):
            for j in range(wall.h):
                wall.remove_tile(result_wall.get_tile(i, j))

        parentheses_coefficient = 0.085

        shift = 0.43

        def highlight_parentheses(indexes, prev_indexes=[[]]):
            if prev_indexes == [[]]:
                for i in range(wall.w):
                    parentheses[0][i].scale(INDICATE_SCALE).shift(
                        UP * parentheses_coefficient
                        + (ORIGIN if i in indexes else DOWN * shift)
                    )
                    parentheses[0][i].save_state()
                    parentheses[0][i].scale(1 / INDICATE_SCALE).shift(
                        DOWN * parentheses_coefficient
                        + (ORIGIN if i in indexes else UP * shift)
                    )

            for i in range(wall.w):
                if i in prev_indexes[0]:
                    parentheses[0][i].save_state()

            result = AnimationGroup(
                *[
                    (
                        parentheses[0][i].animate.restore()
                        if i in indexes and i not in prev_indexes[0]
                        else (
                            parentheses[0][i]
                            .animate.scale(1 / INDICATE_SCALE)
                            .shift(DOWN * parentheses_coefficient)
                        ).fade(FADE_COEFFICIENT)
                        if i not in indexes and i in prev_indexes[0]
                        else parentheses[0][i].animate.fade(FADE_COEFFICIENT)
                        if prev_indexes == [[]]
                        else parentheses[0][i].animate.fade(0)
                    )
                    for i in range(wall.w)
                ]
            )

            prev_indexes[0] = indexes

            return result

        def highlight_tiles(indexes, cache=[[[]]]):
            first = False
            if cache == [[[]]]:
                first = True
                cache[0] = [(i, j) for i in range(wall.w) for j in range(wall.h)]

            for i in range(wall.w):
                for j in range(wall.h):
                    if (i, j) in cache[0]:
                        if first:
                            wall.shift(ORIGIN if (i, j) in indexes else DOWN * shift)

                        wall.get_tile(i, j).save_state()

                        if first:
                            wall.shift(ORIGIN if (i, j) in indexes else UP * shift)

            result = AnimationGroup(
                *[
                    wall.get_tile(i, j).animate.fade(FADE_COEFFICIENT)
                    if (i, j) not in indexes and (i, j) in cache[0]
                    else wall.get_tile(i, j).animate.restore()
                    if (i, j) in indexes
                    else wall.get_tile(i, j).animate.fade(0)
                    for i in range(wall.w)
                    for j in range(wall.h)
                ],
                run_time=0.75,
            )

            cache[0] = indexes

            return result

        p_copy = parentheses.copy().shift(DOWN * shift)

        self.play(highlight_parentheses([0, 5]))

        self.play(
            highlight_tiles(
                [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (5, 0)]
            )
        )

        brace_offset = 0.25
        bs = []
        for i, (text, start, end) in enumerate(
            [
                ("single", tileset[0], tileset[1]),
                (
                    ["opening", "closing"],
                    [tileset[2], tileset[8]],
                    [tileset[2], tileset[8]],
                ),
                ("path creation", tileset[3], tileset[7]),
                ("fill", tileset[9], tileset[9]),
            ]
        ):

            def get_b_local(t, s, e):
                b = BraceBetweenPoints(
                    Point().next_to(s, UP + LEFT, buff=0).get_center(),
                    Point().next_to(e, UP + RIGHT, buff=0).get_center(),
                    direction=UP,
                    color=NOTES_COLOR,
                ).scale([-1, NOTES_SCALE, 1])

                return [
                    b,
                    Tex(t, color=NOTES_COLOR)
                    .next_to(b, UP)
                    .scale(NOTES_SCALE)
                    .shift(DOWN * 0.1),
                ]

            b_local = []

            if type(text) is list:
                for t, s, e in zip(text, start, end):
                    b_local += get_b_local(t, s, e)
            else:
                b_local = get_b_local(text, start, end)

            bs += b_local

            additional = []

            if i == 3:
                b_local[-1].shift(UP * 0.08)

                additional += [highlight_tiles([(6, 1), (7, 1)])]
                additional += [highlight_parentheses([])]

            if i == 1:
                additional += [highlight_tiles([(0, 0), (5, 0)])]
                additional += [highlight_parentheses((0, 5))]

            if i == 2:
                additional += [
                    highlight_tiles(
                        [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (5, 0)]
                    )
                ]

            if i == 0:
                for b in b_local:
                    b.shift(DOWN * shift)

                self.play(
                    task.animate.shift(UP * shift / 2),
                    parentheses.animate.shift(DOWN * shift),
                    wall.animate.shift(DOWN * shift),
                    tileset.animate.shift(DOWN * shift),
                )

                self.play(
                    *[FadeInUp(b, move_factor=0.1) for b in b_local],
                    highlight_parentheses([1, 2, 3, 4, 6, 7]),
                    highlight_tiles([(2, 0), (1, 0), (3, 0), (4, 0), (6, 0), (7, 0)]),
                )

            else:
                self.play(*[FadeInUp(b) for b in b_local], *additional)

        self.play(
            highlight_tiles([(i, j) for i in range(wall.w) for j in range(wall.h)]),
            Transform(parentheses, p_copy),
        )

        wall.save_state()
        tileset.save_state()

        self.play(
            wall.get_tile(5, 0)
            .get_color_object_in_direction(DOWN)
            .animate.set_fill(PALETTE[1]),
            wall.get_tile(5, 1)
            .get_color_object_in_direction(UP)
            .animate.set_fill(PALETTE[1]),
            tileset[6].get_color_object_in_direction(UP).animate.set_fill(PALETTE[1]),
            tileset[7].get_color_object_in_direction(UP).animate.set_fill(PALETTE[1]),
            tileset[7].get_color_object_in_direction(DOWN).animate.set_fill(PALETTE[1]),
            tileset[8].get_color_object_in_direction(DOWN).animate.set_fill(PALETTE[1]),
        )

        self.play(
            Rotate(parentheses[0][5]),
            Rotate(parentheses[0][0]),
            Rotate(wall.get_tile(5, 0).get_color_object_in_direction(UP)),
        )

        self.play(
            wall.animate.restore(),
            tileset.animate.restore(),
            Rotate(parentheses[0][5], angle=-PI),
            Rotate(parentheses[0][0], angle=-PI),
            Rotate(wall.get_tile(5, 0).get_color_object_in_direction(UP), angle=-PI),
        )

        self.play(*[FadeOutUp(b) for b in bs])

        no2 = Tex(r"$\frac{1}{2}n$").next_to(task, DOWN)
        no2dot = Tex(r"$1 \cdot \frac{1}{2}n$").next_to(task, DOWN)
        no2o = (
            Tex(r"time complexity: $\mathcal{O}(n)$")
            .next_to(task, DOWN)
            .align_to(task[1][0], LEFT)
        )

        self.play(Write(no2))
        self.play(TransformMatchingShapes(no2, no2dot))
        self.play(TransformMatchingShapes(no2dot, no2o))

        self.play(
            no2o.animate.shift(DOWN * 2.2),
            task.animate.shift(DOWN * 2.2),
            FadeOutDown(wall, move_factor=2.2),
            FadeOutDown(tileset, move_factor=2.2),
            FadeOutDown(parentheses, move_factor=2.2),
        )

        opt = HighlightedTex(
            r"|optimal| time complexity: $\mathcal{O}(\log n)$"
        ).next_to(no2o, DOWN)
        opt.shift(LEFT * (-no2o[0][0].get_x() + opt[1][0].get_x()))

        self.play(FadeInDown(opt))

        arrows = [
            Arrow(
                start=UP,
                end=DOWN,
                stroke_width=10,
                max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5,
            )
            .align_on_border(DOWN)
            .shift(LEFT + UP),
            Arrow(
                start=UP,
                end=DOWN,
                stroke_width=10,
                max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5,
            )
            .align_on_border(DOWN)
            .shift(RIGHT + UP),
        ]

        self.play(
            opt.animate.shift(UP * 1.25),
            no2o.animate.shift(UP * 1.25),
            task.animate.shift(UP * 1.25),
            FadeInUp(arrows[0], move_factor=0.6),
            FadeInUp(arrows[1], move_factor=0.6),
        )


class ComputationalPower(Scene):
    @fade
    def construct(self):
        title = Tex("\Large Computational Power")

        self.play(FadeInUp(title))

        cf = 0.8
        c = 1.3

        tile = Tile(PALETTE).scale(2).shift(LEFT * cf)

        question = Tex("?").scale(QUESTION_MARK_SCALE * 1.5).shift(RIGHT * cf)

        self.play(
            ReplacementTransform(title, VGroup(tile, question)),
        )
        lang = (
            SVGMobject("assets/languages/python.svg")
            .next_to(ORIGIN, RIGHT)
            .shift(RIGHT * c)
        )

        sscale = 2.8

        l = Tex("$=$").scale(sscale)
        g = Tex("$>$").scale(sscale)
        ll = Tex("$\ll$").scale(sscale)

        self.play(
            tile.animate.next_to(ORIGIN, LEFT).shift(LEFT * c),
            FadeInRight(lang),
            question.animate.move_to(ORIGIN).fade(FADE_COEFFICIENT),
            FadeInUp(l),
        )

        self.play(
            FadeOutUp(l, move_factor=0.85),
            FadeInUp(g, move_factor=0.85),
        )

        self.play(
            FadeOutUp(g, move_factor=0.85),
            FadeInUp(ll, move_factor=0.85),
        )

        r = (
            Tex("$\Leftrightarrow$")
            .scale(sscale / 1.5)
            .move_to(tile)
            .rotate(PI / 2)
            .shift(DOWN * 0.5)
        )

        g = VGroup(tile, lang, ll, question)

        lbtm = Tex("LBTM").scale(sscale / 1.5).next_to(r, DOWN)

        self.play(
            AnimationGroup(
                g.animate.shift(UP * 1.2),
                AnimationGroup(
                    FadeInDown(r),
                    FadeInDown(lbtm),
                ),
                lag_ratio=0.5,
            )
        )

        lll = Tex("$<$").scale(sscale).move_to(ll)

        java = (
            SVGMobject("assets/languages/java.svg")
            .move_to(lang)
            .set_height(lang.height)
        )

        hs = SVGMobject("assets/languages/haskell.svg").move_to(lang)

        self.play(
            FadeOutUp(ll, move_factor=0.85),
            FadeInUp(lll, move_factor=0.85),
            FadeOut(question),
        )

        self.play(
            FadeOutUp(lang, move_factor=1.5),
            FadeInUp(java, move_factor=1.5),
        )

        self.play(
            FadeOutUp(java, move_factor=1.5),
            FadeInUp(hs, move_factor=1.5),
        )

        r2 = (
            Tex("$\Leftrightarrow$")
            .scale(sscale / 1.5)
            .set_x(hs.get_x())
            .set_y(r.get_y())
            .rotate(PI / 2)
        )

        g = VGroup(tile, lang, ll, question)

        tm = Tex("TM").scale(sscale / 1.5).next_to(r2, DOWN)

        self.play(
            FadeInDown(r2),
            FadeInDown(tm),
        )

        examples = (
            Tex(
                r"""
                \begin{itemize}
                \itemsep0em
                \item prime numbers
                \item divisibility
                \item power of two
                \end{itemize}
                """
            )
            .set_x(lang.get_x())
            .set_y(tile.get_y())
            .shift(LEFT * 0.5)
        )

        ns = [13, 26, 1000]

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOutUp(tm),
                    FadeOutUp(r2),
                    FadeOutUp(hs),
                    FadeOutUp(lll),
                ),
                FadeInUp(examples[0][0 : ns[0]]),
                lag_ratio=0.35,
            ),
        )
        self.play(FadeInUp(examples[0][ns[0] : ns[1]]))
        self.play(FadeInUp(examples[0][ns[1] : ns[2]]))

        impl = (
            Tex("$\Rightarrow$")
            .scale(sscale / 1.5)
            .next_to(lbtm, RIGHT)
            .shift(RIGHT * 0.35)
        )

        algorithm = (
            Tex(
                r"\parbox{10em}{$\exists$ an algorithm to find tiling (given the tileset and the input)}"
            )
            .next_to(impl, RIGHT)
            .shift(RIGHT * 0.5)
        )

        self.play(
            FadeInRight(impl),
            FadeInRight(algorithm),
        )


class ToInfinity(Scene):
    @fade
    def construct(self):
        w = 10
        h = 4

        w2 = w * 2
        h2 = h * 2 + 2

        s = 1.05

        wall = Wall(PALETTE, width=w, height=h, size=s)
        wall2 = Wall(PALETTE, width=w2, height=h2, size=s)

        self.play(Write(wall.border))

        seed(5)
        tiles = [
            [Tile([choice(PALETTE) for _ in range(4)], size=s) for _ in range(w)]
            for _ in range(h)
        ]

        tiles2 = [
            [Tile([choice(PALETTE) for _ in range(4)], size=s) for _ in range(w2)]
            for _ in range(h2)
        ]

        for i in range(w):
            for j in range(h):
                wall.add_tile(tiles[j][i], i, j)

        for i in range(w2):
            for j in range(h2):
                wall2.add_tile(tiles2[j][i], i, j)

        self.play(
            AnimationGroup(*[FadeIn(t.border) for t in wall.tiles], lag_ratio=0.01)
        )

        tls = [
            wall2.get_tile(i, j)
            for i in range(w2)
            for j in range(h2)
            if (
                (
                    i in range(int(w2 / 3), int(w2 / 3 * 2))
                    and j not in range(int(h2 / 3), int(h2 / 3 * 2))
                )
                or (
                    i not in range(int(w2 / 3), int(w2 / 3 * 2))
                    and j in range(int(h2 / 3), int(h2 / 3 * 2))
                )
                or (
                    i not in range(int(w2 / 3), int(w2 / 3 * 2))
                    and j not in range(int(h2 / 3), int(h2 / 3 * 2))
                )
            )
        ]

        tls = sorted(tls, key=lambda x: np.linalg.norm(x.get_center()))

        self.remove(wall.border)

        self.play(
            AnimationGroup(
                *[FadeIn(t.border) for t in tls], lag_ratio=0.005, run_time=2
            )
        )

        self.play(*[t.border.animate.fade(0.94) for t in list(wall.tiles) + tls])

        l1 = Tex(
            "1. If a tileset can fill the plane, can it also fill it periodically?"
        ).scale(0.9)
        l2 = (
            Tex("2. Is there an algorithm to check if a tiling exists?")
            .scale(0.9)
            .next_to(l1, DOWN)
        )

        questions = VGroup(l1, l2)

        self.play(Write(l1, run_time=2))

        self.play(Write(l2, run_time=2))

        no = Tex("No.", color=RED).scale(4).shift(DOWN)

        self.play(questions.animate.next_to(no, UP).shift(UP * 0.8))

        self.play(Write(no))

        impl = Tex("$\Rightarrow$").rotate(-PI / 2).scale(1.5).next_to(l1, DOWN)

        self.play(
            AnimationGroup(
                FadeOutDown(no),
                AnimationGroup(
                    l2.animate.shift(DOWN * 0.9),
                    FadeInDown(impl, move_factor=0.5),
                ),
                lag_ratio=0.5,
            )
        )

        impl2 = Tex("$\Rightarrow$").rotate(-PI / 2).scale(1.5).next_to(l2, DOWN)

        hp = Tex(r"$\lnot$ halting problem", color=RED).next_to(impl2, DOWN)

        self.play(
            AnimationGroup(
                FadeInDown(impl2, move_factor=0.5),
                FadeInDown(hp, move_factor=0.5),
            ),
        )

        not1 = (
            Tex(r"$\lnot$", color=RED)
            .move_to(questions[0][0][:2])
            .align_to(questions[0][0][:2], DOWN)
        )
        not2 = (
            Tex(r"$\lnot$", color=RED)
            .move_to(questions[1][0][:2])
            .align_to(questions[1][0][:2], DOWN)
        )

        l1p = questions[0][0][2:]
        l2p = questions[1][0][2:]

        self.play(
            Rotate(impl2, PI, about_point=impl2.get_center()),
            l2p.animate.set_color(RED),
            Transform(questions[1][0][:2], not2),
        )

        self.play(
            Rotate(impl, PI, about_point=impl.get_center()),
            l1p.animate.set_color(RED),
            Transform(questions[0][0][:2], not1),
        )

        def to_colors(c):
            return [PALETTE[{RED: 0, GREEN: 1, BLUE: 2, WHITE: 3}[a]] for a in c]

        tileset = (
            TileSet(
                Tile(to_colors([RED, RED, GREEN, RED])),
                Tile(to_colors([RED, BLUE, GREEN, BLUE])),
                Tile(to_colors([GREEN, RED, GREEN, GREEN])),
                Tile(to_colors([BLUE, WHITE, BLUE, RED])),
                Tile(to_colors([BLUE, BLUE, BLUE, WHITE])),
                Tile(to_colors([WHITE, WHITE, WHITE, RED])),
                Tile(to_colors([GREEN, RED, WHITE, BLUE])),
                Tile(to_colors([WHITE, BLUE, RED, BLUE])),
                Tile(to_colors([RED, BLUE, RED, WHITE])),
                Tile(to_colors([GREEN, GREEN, RED, BLUE])),
                Tile(to_colors([WHITE, RED, GREEN, RED])),
                rows=2,
            )
            .scale(1)
            .next_to(l1, DOWN)
        )

        result = find_tiling(
            tileset, wall2, w=w2, max_height=h2, min_height=h2, ignore_sides=True,
        ).scale(s)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOutDown(impl),
                    FadeOutDown(impl2),
                    FadeOutDown(l2),
                    FadeOutDown(not2),
                    FadeOutDown(hp),
                    l1.animate.set_color(WHITE).shift(UP * 0.3),
                ),
                AnimationGroup(Write(tileset)),
                lag_ratio=0.4,
            )
        )

        self.play(FadeOutDown(tileset), FadeOutDown(l1))

        tls = [result.get_tile(i, j) for i in range(w2) for j in range(h2)]
        tls = sorted(tls, key=lambda x: np.linalg.norm(x.get_center()))

        self.play(
            AnimationGroup(
                *[Write(t) for t in tls], lag_ratio=0.005, run_time=2
            )
        )


class Outro(Scene):
    @fade
    def construct(self):
        holes = Tex(
            r"""
                \begin{itemize}
                \itemsep0em
                \item reductions to automatons and grammars
                \item other convex shapes (triangles, hexagons)
                \item Penrose and Truchet tilings
                \item non-Euclidianity, higher dimensions
                \end{itemize}
                """
        )

        ns = [34, 72, 97, 10000]

        self.play(
            AnimationGroup(
                *[
                    FadeInUp(holes[0][0 if i == 0 else ns[i - 1] : ns[i]])
                    for i in range(len(ns))
                ],
                lag_ratio=0.25,
            )
        )

        w = 15
        h = 10

        wall = Wall(PALETTE, width=w, height=h)

        seed(3)
        tiles = [
            [Tile([choice(PALETTE) for _ in range(4)]) for _ in range(w)]
            for _ in range(h)
        ]

        for i in range(w):
            for j in range(h):
                wall.add_tile(tiles[j][i], i, j)

        self.play(FadeOutUp(holes))

        seed(5)
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

                    tiles[p1[1]][p1[0]].set_color_in_direction(new_color, d1)
                    tiles[p2[1]][p2[0]].set_color_in_direction(new_color, d2)

        self.play(
            AnimationGroup(
                *[Write(t.color_objects) for t in wall.tiles], lag_ratio=0.01
            ),
            run_time=2,
        )

        tile = Tile(PALETTE)
        pp = Tex(r"{ \bf ++ }").scale(2).next_to(tile, RIGHT)

        g = VGroup(tile, pp).scale(2).move_to(ORIGIN)

        self.play(*[t.color_objects.animate.fade(0.85) for t in wall.tiles])
        self.play(Write(g))
