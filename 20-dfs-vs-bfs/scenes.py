from manim import *
from utilities import *

from random import uniform, seed, randint
from math import sin


class Intro(MovingCameraScene):
    @fade
    def construct(self):
        self.camera.background_color = BLACK

        with open("maze/mask.txt") as f:
            contents = f.read().splitlines()

        dfs_order = {}
        bfs_order = {}
        dfs_order_inverse = {}
        bfs_order_inverse = {}

        diff_order = {}

        def get_dfs_order(start):
            queue = [start]
            discovered = set(queue)
            dfs_order[0] = start
            dfs_order_inverse[start] = 0
            i = 1

            while len(queue) != 0:
                x, y = queue.pop()

                for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                    nx, ny = x + dx, y + dy

                    if (nx, ny) in discovered:
                        continue

                    if contents[ny][nx] == "#":
                        continue

                    dfs_order[i] = (nx, ny)
                    dfs_order_inverse[(nx, ny)] = i
                    queue.append((nx, ny))
                    discovered.add((nx, ny))
                    i += 1

            return i

        def get_bfs_order(start):
            queue = [start]
            discovered = set(queue)
            bfs_order[0] = start
            bfs_order_inverse[start] = 0
            i = 1

            while len(queue) != 0:
                x, y = queue.pop(0)

                for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                    nx, ny = x + dx, y + dy

                    if (nx, ny) in discovered:
                        continue

                    if contents[ny][nx] == "#":
                        continue

                    bfs_order[i] = (nx, ny)
                    bfs_order_inverse[(nx, ny)] = i
                    queue.append((nx, ny))
                    discovered.add((nx, ny))
                    i += 1

            return i

        maze, maze_dict = maze_to_vgroup(contents)
        maze.rotate(-PI / 2)

        width = len(contents[0])
        height = len(contents)

        start = (width // 2, height // 2 - 1)

        number_of_tiles = get_bfs_order(start)
        number_of_tiles = get_dfs_order(start)

        colors = color_gradient((GREEN, RED), number_of_tiles)

        diff_order = {}

        for i in dfs_order_inverse:
            diff_order[i] = (dfs_order_inverse[i] - bfs_order_inverse[i]) / number_of_tiles

        self.camera.frame.set_width(maze.get_width() * 1.2).move_to(maze)

        self.play(
            *[
                Succession(
                    Wait(i / number_of_tiles * 2/3),
                    FadeIn(maze_dict[bfs_order[i]], run_time=2/3),
                )
                for i in range(number_of_tiles)
            ],
            Succession(
                Wait(2/3),
                AnimationGroup(
                    *[
                        FadeIn(maze_dict[x])
                        for x in maze_dict
                        if x not in bfs_order.values()
                    ]
                )
            )
        )

        s = 5.5

        bfs = Tex(r"\underline{BFS}").scale(s)
        vs = Tex(r"vs.").scale(s)
        dfs = Tex(r"\underline{DFS}").scale(s)

        g = VGroup(bfs, vs, dfs).arrange(RIGHT, buff=1).next_to(maze, UP * s)
        vs.align_to(bfs[0][1], DOWN)

        # nearest
        # form the start (smaller)

        # nearest
        # form the current position (smaller)

        self.play(
            self.camera.frame.animate.move_to(VGroup(maze, bfs)),
            AnimationGroup(
                FadeIn(bfs, shift=DOWN),
                FadeIn(vs, shift=DOWN),
                FadeIn(dfs, shift=DOWN),
                lag_ratio=0.1,
            )
        )

        offset = - bfs.get_center() + g.get_center()
        title_s = 1.25

        self.play(
            bfs.animate.move_to(g).scale(title_s),
            vs.animate.shift(offset).set_opacity(0),
            dfs.animate.shift(offset).set_opacity(0),
        )

        # BFS fill
        self.play(
            *[
                Succession(
                    Wait(i / number_of_tiles * 4),
                    maze_dict[bfs_order[i]].animate(run_time=0.5).set_fill(colors[i], 1)
                )
                for i in range(number_of_tiles)
            ]
        )

        # tehehe
        for x in range(width):
            for y in range(height):
                if contents[y][x] == "#":
                    maze_dict[(x, y)].set_opacity(0)

        maze.save_state()

        # tehehe
        for x in range(width):
            for y in range(height):
                if contents[y][x] == "#":
                    maze_dict[(x, y)].set_opacity(1)

        # reset to DFS
        self.play(
            bfs.animate.shift(-offset * 2).scale(1 / title_s).set_opacity(0),
            MoveAndFadeThereBack(vs, -offset * 2),
            dfs.animate.shift(-offset * 2).set_opacity(1).scale(title_s),
            *[
                maze_dict[bfs_order[i]].animate(run_time=1).set_fill(BLACK, 0)
                for i in range(number_of_tiles)
            ]
        )

        # DFS fill
        self.play(
            *[
                Succession(
                    Wait(i / number_of_tiles * 6),
                    maze_dict[dfs_order[i]].animate(run_time=0.5).set_fill(colors[i], 1)
                )
                for i in range(number_of_tiles)
            ]
        )

        # tehehe
        for x in range(width):
            for y in range(height):
                if contents[y][x] == "#":
                    maze_dict[(x, y)].set_opacity(0)

        mc = maze.copy()

        # tehehe
        for x in range(width):
            for y in range(height):
                if contents[y][x] == "#":
                    maze_dict[(x, y)].set_opacity(1)

        # reset both
        self.play(
            bfs.animate.shift(offset).set_opacity(1).scale(title_s),
            dfs.animate.shift(offset),
            *[
                maze_dict[(x, y)].animate(run_time=1).set_opacity(0)
                for x in range(width)
                for y in range(height)
                if contents[y][x] == "#"
            ],
            *[
                maze_dict[(x, y)].animate(run_time=1).set_fill_color(DARKER_GRAY)
                for x in range(width)
                for y in range(height)
                if contents[y][x] != "#"
            ]
        )

        # comparison
        self.play(
            bfs.animate.set_color(BLUE),
            dfs.animate.set_color(ORANGE),
            *[
                maze_dict[i].animate.set_fill_color(interpolate_color(DARK_GRAY, BLUE, diff_order[i]))
                for i in diff_order
                if diff_order[i] >= 0
            ],
            *[
                maze_dict[i].animate.set_fill_color(interpolate_color(DARK_GRAY, ORANGE, abs(diff_order[i])))
                for i in diff_order
                if diff_order[i] < 0
            ]
        )

        self.play(
            bfs.animate.set_color(WHITE),
            dfs.animate.scale(1/title_s).set_opacity(BIG_OPACITY).set_color(WHITE),
            maze.animate.restore(),
        )


        bfs.set_z_index(10000000)
        dfs.set_z_index(10000000)

        d = Dot().next_to(maze, DOWN + RIGHT)
        d2 = Dot().next_to(maze, UP + LEFT)

        sq = Square(fill_color=BLACK, fill_opacity=1, stroke_color=WHITE, stroke_width=20).scale(100).next_to(d, LEFT, buff=0).set_z_index(100000000)
        sq.rotate(-PI / 4, about_point=d.get_center()).set_z_index(0.00002)
        sqcp = sq.copy().set_z_index(0.00001).set_stroke_width(0)

        sq2 = Square(fill_color=BLACK, fill_opacity=1, stroke_color=WHITE, stroke_width=20).scale(100).next_to(d2, LEFT, buff=0).set_z_index(100000000)
        sq2.rotate(-PI / 4, about_point=d2.get_center()).set_z_index(0.00002)
        sq2cp = sq2.copy().set_z_index(0.00001).set_stroke_width(0)

        self.add(sq)
        self.add(sqcp)

        # welp yeah
        sqcpcp = sqcp.copy()
        sqcp.move_to(sq2cp)
        sq2cp.move_to(sqcpcp)

        sqq = sq.copy()
        sq.move_to(sq2)
        sq2.move_to(sqq)

        maze_original = maze.copy()
        mc_original = mc.copy()

        for o in self.mobjects:
            self.remove(o)

        self.add(bfs)
        self.add(dfs)

        def maze_updater(obj, dt):
            for o, u in zip(maze_original, obj):
                n = Difference(o, sqcp,
                    stroke_width = o.get_stroke_width(),
                    color = o.get_color(),
                    fill_opacity = o.get_fill_opacity(),
                    stroke_color = o.get_stroke_color(),
                    z_index = o.get_z_index(),
                )

                n.set_opacity(o.get_fill_opacity())

                u.become(n)

        def mc_updater(obj, dt):
            for o, u in zip(mc_original, obj):
                n = Intersection(o, sqcp,
                    stroke_width = o.get_stroke_width(),
                    color = o.get_color(),
                    fill_opacity = o.get_fill_opacity(),
                    stroke_color = o.get_stroke_color(),
                    z_index = o.get_z_index(),
                )

                n.set_opacity(o.get_fill_opacity())

                u.become(n)

        self.add(mc)
        mc.add_updater(maze_updater)

        self.add(maze)
        maze.add_updater(mc_updater)

        sq.save_state()
        sqcp.save_state()

        self.play(
            bfs.animate.set_opacity(BIG_OPACITY).scale(1/title_s),
            dfs.animate.set_opacity(1).scale(title_s),
            MoveAndFadeThereBackKindaTho(sq, sq2),
            sqcp.animate().move_to(sq2cp),
            run_time=2,
        )

        mc.remove_updater(maze_updater)
        maze.remove_updater(mc_updater)

        self.play(
            bfs.animate.set_opacity(1).scale(title_s),
            *[
                maze_dict[i].animate.set_fill_color(interpolate_color(DARK_GRAY, BLUE, diff_order[i]))
                for i in diff_order
                if diff_order[i] >= 0
            ],
            *[
                maze_dict[i].animate.set_fill_color(interpolate_color(DARK_GRAY, ORANGE, abs(diff_order[i])))
                for i in diff_order
                if diff_order[i] < 0
            ],
        )
