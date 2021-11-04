from utilities import *
from string import digits

PALETTE = ["#b91e2f","#f68828","#cdd190","#122f30"]
REDUCED_PALETTE = PALETTE[:2]


def is_hex_color(str):
    """Yeah I know, this is not pretty."""
    return len(str) == 7 and str.startswith("#") and all([c in digits + "abcdef" for c in str.lower()[1:]])


class Tile(VMobject):
    TEXT_SCALE = 0.6
    TEXT_OFFSET = 1/3.5
    DIRECTIONS = [RIGHT, UP, LEFT, DOWN]

    def __init__(self, colors, size=1):
        colors = list(map(str, colors))

        super().__init__()

        self.border = Square(size, color=WHITE)
        self.add(self.border)

        self.size = size

        self.colors = colors

        self.cross = VGroup()
        self.cross.add(Line(start=(UP + RIGHT) * self.size / 2, end=(DOWN + LEFT) * self.size / 2, stroke_width=1))
        self.cross.add(Line(end=(DOWN + RIGHT) * self.size / 2, start=(UP + LEFT) * self.size / 2, stroke_width=1))

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
            text = Tex(color) \
                .scale(Tile.TEXT_SCALE * self.size) \
                .shift(direction * self.size * Tile.TEXT_OFFSET)

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


class Wall(VMobject):
    def __init__(self, colors, input=None, width=3, height=5, size=1):
        super().__init__()

        # input overwrites the width
        if input is not None:
            width = len(input)

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
                for i in range(len(input) + 1):
                    c = (0.25 if i in (0, len(input)) else 0.5) * self.size
                    line = Line(start=[-width / 2 + i * self.size, height / 2, 0], end=[-width / 2 + i * self.size, height / 2 + c, 0])
                    self.add(line)

                    if i < len(input):
                        p = [-width / 2 + (i + 0.5) * self.size, height / 2, 0]

                        text = Tex(input[i]) \
                            .scale(Tile.TEXT_SCALE * self.size) \
                            .move_to(p) \
                            .align_to(p, DOWN) \
                            .shift(UP * Tile.TEXT_OFFSET / 2)  # 2 is an eyeball magic constant
                        self.add(text)
            else:
                side = Polygon(*pos).set_stroke(WHITE)
                if is_hex_color(color):
                    self.color_objects.add(side.set_fill(color, 1))
                else:
                    self.color_objects.add(side)

                    text = Tex(color) \
                        .scale(Tile.TEXT_SCALE * self.size) \
                        .move_to(side)

                    self.color_objects.add(text)

        self.add(self.color_objects)

    def to_positive_coordinates(self, x, y):
        """Done so we can use -1."""
        return int(x % self.border.width), int(y % self.border.height)

    def index_to_position(self, x, y):
        x, y = self.to_positive_coordinates(x, y)

        return Square(self.size) \
                .align_to(self.border, UP + LEFT) \
                .shift([x * self.size, -y * self.size, 0]) \
                .get_center()

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

    get_color_in_direction = Tile.get_color_in_direction
    get_color_object_in_direction = Tile.get_color_object_in_direction


class TileSet(VMobject):
    def __init__(self, *tiles):
        super().__init__()

        self.tiles = VGroup(*tiles)
        self.tiles.arrange_in_grid(rows=1, buff=0.6)

        self.commas = VGroup()

        n = len(tiles)
        for i in range(n - 1):
            self.commas.add(Tex("\Large $,$").next_to(self.tiles[i], DOWN + RIGHT, buff=0).shift(UP * 0.07 + RIGHT * 0.1))

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
            AnimationGroup(*[Write(t) for t in self.tiles], lag_ratio=0.1),
            Write(self.commas),
            Write(self.braces),
            lag_ratio=0.2,
        )


class WriteReverse(Write):
    """A special write for a tile and wall (since we want the animation to be reversed)."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, reverse=True)


class Intro(Scene):
    def construct(self):
        w = 8
        h = 5

        wall = Wall(PALETTE, width=w, height=h)

        bl = BraceBetweenPoints([-w/2, h/2, 0], [-w/2, -h/2, 0])
        blt = Tex("\\footnotesize h").next_to(bl, LEFT * 0.5)

        bu = BraceBetweenPoints([-w/2, h/2, 0], [w/2, h/2, 0], direction=UP).scale([-1, 1, 0])
        but = Tex("\\footnotesize w").next_to(bu, UP * 0.5)

        self.play(Write(wall.border))

        self.play(Write(bu), Write(but))
        self.play(Write(bl), Write(blt))

        tiles = [[Tile([choice(PALETTE) for _ in range(4)]) for _ in range(w)] for _ in range(h)]

        for i in range(w):
            for j in range(h):
                wall.add_tile(tiles[j][i], i, j)

        self.play(AnimationGroup(*[FadeIn(t.border) for t in wall.tiles], lag_ratio=0.01))

        for t in wall.tiles:
            for c in t.color_objects:
                self.bring_to_back(c)
            self.bring_to_front(t)

        self.play(
            *[t.border.animate.set_color(WHITE) for t in wall.tiles],
            *[Write(t.cross) for t in wall.tiles],
            *[Write(t.color_objects) for t in wall.tiles],
        )

        # color rows + columns
        changes = {}
        seed(1)
        for count, (i1, i2) in enumerate(zip((range(w-1), range(w)), (range(h), range(h-1)))):
            for i in i1:
                for j in i2:
                    p1, p2 = (i, j), (i + 1, j) if not count else (i, j + 1)
                    d1, d2 = (RIGHT, LEFT) if not count else (DOWN, UP)

                    c1, c2 = tiles[p1[1]][p1[0]].get_color_in_direction(d1), tiles[p2[1]][p2[0]].get_color_in_direction(d2)
                    new_color=choice([c1, c2])

                    if p1 not in changes:
                        changes[p1] = tiles[p1[1]][p1[0]].animate
                    changes[p1].set_color_in_direction(new_color, d1)

                    if p2 not in changes:
                        changes[p2] = tiles[p2[1]][p2[0]].animate
                    changes[p2].set_color_in_direction(new_color, d2)
        self.play(*changes.values())
        self.play(AnimationGroup(FadeOut(VGroup(bl, blt, bu, but)), FadeIn(wall.color_objects), lag_ratio=0.4))

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

                    if tiles[j][i].get_color_in_direction(direction) != wall.get_color_in_direction(direction):

                        if (i, j) not in changes:
                            changes[(i, j)] = tiles[j][i].animate
                        changes[(i, j)].set_color_in_direction(wall.get_color_in_direction(direction), direction)

        self.play(*changes.values())

        self.play(*[FadeOut(o) for o in self.mobjects])


def pasting_animations(tile, wall, positions, speed=0.07):
    def DelayedTransform(x, y, t):
        return Transform(x, y, run_time = 1 + t, rate_func=lambda a: smooth(a if t == 0 else (0 if a < t else (a - t) / (1 - t))))

    n = len(positions)

    from_tiles = [tile.copy() for _ in range(n)]
    to_tiles = [tile.copy().move_to(wall.index_to_position(*position)) for position in positions]

    return [DelayedTransform(from_tiles[i], to_tiles[i], speed * (n - i - 1)) for i in range(n)], from_tiles, positions


class TileSetExample(Scene):
    def construct(self):
        tiles = [
                Tile([REDUCED_PALETTE[1], REDUCED_PALETTE[1], REDUCED_PALETTE[0], REDUCED_PALETTE[1]]),
                Tile([REDUCED_PALETTE[1], REDUCED_PALETTE[1], REDUCED_PALETTE[1], REDUCED_PALETTE[1]]),
                Tile([REDUCED_PALETTE[0], REDUCED_PALETTE[1], REDUCED_PALETTE[1], REDUCED_PALETTE[1]]),
                ]

        tiles = VGroup(*tiles)
        tiles.arrange_in_grid(rows=1)

        tileset = TileSet(*tiles)

        self.play(tileset.animateWrite())

        tileTypes = Tex("Tile Types $=$").shift(LEFT * 1)

        tileset_with_text = VGroup(tileTypes, tileset)

        self.play(
            FadeIn(tileTypes),
            tileset_with_text.animate.arrange_in_grid(rows=1, buff=0.23).move_to([0, 0, 0])
        )

        w = 8
        h = 3
        wall = Wall(REDUCED_PALETTE * 2, width=w, height=h)

        wall.shift(DOWN * 1.2)

        self.play(
            AnimationGroup(
                tileset_with_text.animate.shift(UP * 2.3),
                Write(wall),
                lag_ratio=0.6,
            )
        )

        question = Tex("?").scale(3).move_to(wall)

        self.play(Write(question))
        self.play(FadeOut(question))

        animations1, tiles1, positions1 = pasting_animations(tiles[-1], wall, [(-1, i) for i in range(h)])
        animations2, tiles2, positions2 = pasting_animations(tiles[0], wall, [(0, i) for i in range(h)])

        self.play(*animations1, *animations2)

        wall.add_tiles(tiles1, positions1)
        wall.add_tiles(tiles2, positions2)

        from_tile_wrong = tiles[-1].copy()
        to_tile_wrong = tiles[-1].copy().move_to(wall.index_to_position(4, i)).rotate(-PI / 2)

        cross = VGroup()
        r1 = Rectangle(width=0.2, height=3.3).set_fill(RED, 1).scale(0.5).rotate(PI / 4)
        r2 = Rectangle(width=0.2, height=3.3).set_fill(RED, 1).scale(0.5).rotate(-PI / 4)
        cross.add(Union(r1, r2).set_stroke("#8b0000", 1.5).set_fill(RED, 1).move_to(to_tile_wrong))

        self.play(Transform(from_tile_wrong, to_tile_wrong))

        self.play(FadeIn(cross), from_tile_wrong.animate.set_opacity(0.2))
        self.play(FadeOut(from_tile_wrong), FadeOut(cross))

        animations, tiles, positions = pasting_animations(tiles[1], wall, [(i, j) for i in reversed(range(1, w - 1)) for j in reversed(range(h))], speed=0.03)

        self.play(*animations)

        wall.add_tiles(tiles, positions)

        self.play(wall.get_color_object_in_direction(UP).animate.set_fill(REDUCED_PALETTE[0]))

        self.play(*[FadeOut(wall.get_tile(i, 0)) for i in range(wall.w)])


class HighlightedTex(Tex):
    def __init__(self, text, sep='|', color=YELLOW):
        super().__init__(*[s for s in text.split(sep) if len(s) != 0])

        for i in range(0 if text[0] == sep else 1, len(self), 2):
            self[i].set_color(YELLOW)


class ProgrammingModel(Scene):
    def construct(self):
        title = Tex("\Large Programming model")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 2.5))

        text = [
            (Tex("Input:"), HighlightedTex("|colors| on the |top side| of the wall")),
            (Tex("Program:"), HighlightedTex("finite set of |tile types|")),
            (Tex("Output:"), HighlightedTex("|accept| if there exists valid tiling, else |reject|")),
        ]

        text_scale = 0.85
        for i in range(len(text)):
            text[i][0].scale(text_scale).next_to(text[i-1][0], DOWN).align_to(text[i-1][0], RIGHT)
            text[i][1].scale(text_scale).next_to(text[i][0], RIGHT)

        g = VGroup()
        for i in range(len(text)):
            g.add(text[i][0])
            g.add(text[i][1])

        g.move_to(ORIGIN).shift(UP * 0.7)

        tile_scale = 0.8

        self.play(AnimationGroup(Write(text[0][0]), Write(text[1][0]), Write(text[2][0]), lag_ratio=0.15))

        wall = Wall(PALETTE, input=[1, 0, 0, 1, 0], height = 1).shift(DOWN * 2).scale(tile_scale)

        seed(0)
        ts = TileSet(*[Tile([(choice(PALETTE) if i != 1 else randint(0, 1)) for i in range(4)]) for _ in range(4)]).scale(tile_scale)

        self.play(Write(text[0][1]), Write(wall))

        ts.next_to(wall, RIGHT, buff=1)

        g = VGroup(ts, wall)

        self.play(wall.animate.set_x(wall.get_x() - g.get_x()))
        ts.next_to(wall, RIGHT, buff=1)

        self.play(ts.animateWrite(), Write(text[1][1]))

        self.play(Write(text[2][1]))
