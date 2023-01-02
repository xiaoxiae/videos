from manim import *
from utilities import *

from random import uniform, seed
from math import sin


ROBOT_RATE_FUNC = lambda x: rush_into(x * 2) if x < 0.5 else rush_into((1 - x) * 2)
MINERAL_RATE_FUNC = lambda x: 0 if x < 0.5 else slow_into((x - 0.5) * 4) if x < 0.75 else slow_into((1 - x) * 4)


def cool_graphy_graphy(bs=1):
    values = []

    for f in [
        "programs/graphs/results/bfs.txt",
        "programs/graphs/results/bfs-wtb.txt",
        "programs/graphs/results/bfs-wtb-max-prune.txt",
        "programs/graphs/results/astar-best.txt",
    ]:
        with open(f) as fd:
            values.append(int(fd.read().splitlines()[-1].split()[1]))

    chart = BarChart(
        values=values,
        bar_names=["bfs", "prune v1", "prune v2", "A*"],
        y_length=4,
        x_length=9,
        x_axis_config={"font_size": 36, "stroke_width": bs},
        y_axis_config={"stroke_width": bs},
        bar_colors=[
            "#FF6962",
            "#FF8989",
            "#7ABD91",
            "#5FA777",
        ],
        tips=True,
        bar_stroke_width = bs,
    )

    c_bar_lbls = chart.get_bar_labels(font_size=48)

    chart[2].remove(chart[2][3])

    chart[1].set_z_index(100000)
    chart[2].set_z_index(100000)

    return chart, c_bar_lbls


class Increment(Animation):

    def __init__(self, mobject: Mobject, number, distance, **kwargs):
        super().__init__(mobject, **kwargs)
        self.number = number
        self.distance = distance
        self.became = False

        self.start = mobject.get_center()

    def interpolate_mobject(self, alpha: float):
        if alpha > 0.5 and not self.became:
            self.mobject.become(Tex(r"\textbf{" + str(self.number) + "}").move_to(self.mobject))
            self.became = True

        new_alpha = MINERAL_RATE_FUNC(alpha)
        self.mobject.move_to(self.start + UP * self.distance * new_alpha)


class MinotaurMovement(MovingCameraScene):
    @fade
    def construct(self):
        self.next_section(skip_animations=True)  # this is correct

        with open("maze/mask.txt") as f:
            contents = f.read().splitlines()

        theseus = ImageMobject("assets/theseus-nobackground.png").set_height(0.8).set_z_index(100)
        theseus_position = (22, 9)
        theseus_text = Tex("Theseus").next_to(theseus, DOWN, buff=-0.08).scale(0.25)

        theseus_miniature = ImageMobject("assets/theseus-nobackground-outline.png").set_height(0.8).move_to(RIGHT * (theseus_position[0] + 0.5) + DOWN * (theseus_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT).set_z_index(1000000 + 1)

        self.camera.frame.move_to(Group(theseus, theseus_text)).set_height(theseus.height * 2)

        self.play(
            AnimationGroup(
                FadeIn(theseus),
                FadeIn(theseus_text, lag_ratio=0.1),
                lag_ratio=0.5,
            )
        )

        minotaur = ImageMobject("assets/minotaur-nobackground.png").set_height(0.8).next_to(theseus, RIGHT, buff=0.3).set_z_index(100)
        minotaur_position = (33, 9)
        minotaur_text = Tex("Minotaur").next_to(minotaur, DOWN, buff=-0.08).scale(0.25)

        minotaur_miniature = ImageMobject("assets/minotaur-nobackground-outline.png").set_height(0.8).move_to(RIGHT * (minotaur_position[0] + 0.5) + DOWN * (minotaur_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT).set_z_index(1000000 + 1)
        minotaur_miniature_fade = ImageMobject("assets/minotaur-nobackground-outline-fade.png").set_height(0.8).move_to(RIGHT * (minotaur_position[0] + 0.5) + DOWN * (minotaur_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT).set_z_index(1000000 + 1)

        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(Group(theseus, minotaur)).scale(1.25),
                AnimationGroup(
                    FadeIn(minotaur),
                    FadeIn(minotaur_text, lag_ratio=0.1),
                    lag_ratio=0.5,
                ),
                lag_ratio=0.25,
            ),
        )

        maze, maze_dict = maze_to_vgroup(contents)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(theseus_text),
                    FadeOut(minotaur_text),
                ),
                AnimationGroup(
                    self.camera.frame.animate.move_to(Group(theseus_miniature, minotaur_miniature)).set_height(maze.height * 0.65),
                    FadeTransform(theseus, theseus_miniature),
                    FadeTransform(minotaur, minotaur_miniature),
                ),
                AnimationGroup(
                    FadeIn(maze),
                ),
                lag_ratio=0.5,
                run_time=2,
            )
        )

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature, minotaur_miniature.copy().shift(LEFT * 2))).scale(0.85),
            minotaur_miniature.animate.shift(LEFT * 2),
        )

        for i in range(1):
            self.play(
                self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(LEFT), minotaur_miniature.copy().shift(LEFT * 2))).scale(0.85),
                minotaur_miniature.animate.shift(LEFT * 2),
                theseus_miniature.animate.shift(LEFT),
            )

        self.next_section() # this is correct too

        minotaur_miniature.shift(LEFT * 2)
        theseus_miniature.shift(RIGHT)
        self.camera.frame.move_to(Group(theseus_miniature, minotaur_miniature))

        self.camera.frame.scale(0.75)

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(RIGHT), minotaur_miniature)),
            theseus_miniature.animate.shift(RIGHT),
        )

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy(), minotaur_miniature.copy().shift(LEFT * 2))),
            minotaur_miniature.animate.shift(LEFT * 2),
            rate_func=double_smooth,
            run_time=MINOTAUR_MOVE_SPEED,
        )

        minotaur_miniature.save_state()
        theseus_miniature.save_state()
        self.camera.frame.save_state()

        rect = get_fade_rect()

        self.play(
            AnimationGroup(
                FadeIn(rect, run_time=2, rate_func=there_and_back),
                AnimationGroup(
                    self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(LEFT * 6 + UP * 1), minotaur_miniature.copy().shift(LEFT * 4))),
                    theseus_miniature.animate.shift(LEFT * 6 + UP * 1),
                    minotaur_miniature.animate.shift(LEFT * 4),
                    run_time=1,
                ),
                lag_ratio=0.25,
            )
        )

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(UP), minotaur_miniature)),
            theseus_miniature.animate.shift(UP),
        )

        for i in range(2):
            self.play(
                minotaur_miniature.animate.shift(LEFT * 0.1),
                rate_func=there_and_back,
                run_time=0.8
            )

            self.play(
                self.camera.frame.animate.move_to(Group(theseus_miniature.copy(), minotaur_miniature.copy().shift(UP))),
                minotaur_miniature.animate.shift(UP),
                run_time=MINOTAUR_MOVE_SPEED/2,
            )

        for i in range(2):
            self.play(
                self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(DOWN), minotaur_miniature)),
                theseus_miniature.animate.shift(DOWN),
            )

            self.play(
                self.camera.frame.animate.move_to(Group(theseus_miniature.copy(), minotaur_miniature.copy().shift(LEFT * 2))),
                minotaur_miniature.animate.shift(LEFT * 2),
                rate_func=double_smooth,
                run_time=MINOTAUR_MOVE_SPEED,
            )

            self.wait(MINOTAUR_MOVE_DELAY)

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(RIGHT), minotaur_miniature)),
            theseus_miniature.animate.shift(RIGHT),
        )

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy(), minotaur_miniature.copy().shift(RIGHT))),
            minotaur_miniature.animate.shift(RIGHT),
        )

        self.wait(MINOTAUR_MOVE_DELAY)

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(LEFT), minotaur_miniature)),
            theseus_miniature.animate.shift(LEFT),
        )

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy(), minotaur_miniature.copy().shift(LEFT))),
            minotaur_miniature.animate.shift(LEFT),
        )

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy(), minotaur_miniature.copy().shift(DOWN))),
            minotaur_miniature.animate.shift(DOWN),
        )

        self.wait(MINOTAUR_MOVE_DELAY)

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(RIGHT), minotaur_miniature)),
            theseus_miniature.animate.shift(RIGHT),
        )

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy(), minotaur_miniature.copy().shift(DOWN))),
            minotaur_miniature.animate.shift(DOWN),
        )

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy(), minotaur_miniature.copy().shift(RIGHT))),
            minotaur_miniature.animate.shift(RIGHT),
            FadeOut(theseus_miniature),
        )

        tm = theseus_miniature.copy().shift(LEFT)
        theseus_miniature.set_opacity(0)

        self.play(
            Transform(theseus_miniature, tm),
            minotaur_miniature.animate.shift(RIGHT),
            self.camera.frame.animate.scale(0.5),
            run_time=1.5,
        )

        question = Tex(r"\underline{How to approach this problem?}").set_z_index(1000001).next_to(Group(theseus_miniature, minotaur_miniature), UP).scale(0.65)

        rect = get_fade_rect()

        self.play(
            AnimationGroup(
                FadeIn(rect),
                AnimationGroup(
                    self.camera.frame.animate.move_to(Group(theseus_miniature, minotaur_miniature, question)),
                    FadeIn(question, shift=UP * 0.25),
                ),
                lag_ratio=0.5
            )
        )

        self.play(
            FadeOut(maze),
        )

        self.remove(rect)

        table = Table(
            [
                [Tex(r"$(t_x, t_y)$"), Tex(r"$((t_x, t_y), (m_x, m_y))$")],
                [Tex(r"$t$ is not a wall"), Tex(r"$t$, $m$ is not a wall, $t \neq m$")],
            ],
            element_to_mobject=lambda x: x,
            col_labels=[Tex("Placeholder"), Tex("Placeholder")],
            row_labels=[Tex("State"), Tex("Validity")],
        )

        table.next_to(question, DOWN, buff=1.5)

        a = theseus_miniature.copy().set_height(table.get_col_labels()[0].get_height() * 2.5)
        b = Group(
            theseus_miniature.copy().set_height(table.get_col_labels()[0].get_height() * 2.5),
            Tex("+").set_height(table.get_col_labels()[0].get_height() * 1.2),
            minotaur_miniature.copy().set_height(table.get_col_labels()[0].get_height() * 2.5)
        ).arrange()

        a.move_to(table.get_col_labels()[0])
        b.move_to(table.get_col_labels()[1])

        new_question = question.copy().scale(2).next_to(table, UP, buff=1)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    ReplacementTransform(theseus_miniature, a),
                    ReplacementTransform(theseus_miniature.copy(), b[0]),
                    ReplacementTransform(minotaur_miniature, b[2]),
                    Transform(question, new_question),
                    self.camera.frame.animate.scale(2.7).move_to(Group(table, new_question))
                ),
                AnimationGroup(
                    FadeIn(table.get_horizontal_lines()),
                    FadeIn(table.get_vertical_lines()),
                    FadeIn(table.get_row_labels()),
                    FadeIn(b[1]),
                ),
                lag_ratio=0.75,
            )
        )

        self.play(Write(table.get_entries_without_labels((1,1))), run_time=1)
        self.play(Write(table.get_entries_without_labels((1,2))), run_time=1)
        self.play(Write(table.get_entries_without_labels((2,1))), run_time=1)
        self.play(Write(table.get_entries_without_labels((2,2))), run_time=1)


class Intro(MovingCameraScene):
    def construct(self):
        with open("maze/mask.txt") as f:
            contents = f.read().splitlines()

        theseus = ImageMobject("assets/theseus-nobackground.png").set_height(0.8).set_z_index(100)
        theseus_position = (22, 9)
        theseus_text = Tex("Theseus").next_to(theseus, DOWN, buff=-0.08).scale(0.25)

        theseus_miniature = ImageMobject("assets/theseus-nobackground-outline.png").set_height(0.8).move_to(RIGHT * (theseus_position[0] + 0.5) + DOWN * (theseus_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT).set_z_index(1000000 + 1)

        self.camera.frame.move_to(Group(theseus, theseus_text)).set_height(theseus.height * 2)

        self.play(
            AnimationGroup(
                FadeIn(theseus),
                FadeIn(theseus_text, lag_ratio=0.1),
                lag_ratio=0.5,
            )
        )

        minotaur = ImageMobject("assets/minotaur-nobackground.png").set_height(0.8).next_to(theseus, RIGHT, buff=0.3).set_z_index(100)
        minotaur_position = (27, 9)
        minotaur_text = Tex("Minotaur").next_to(minotaur, DOWN, buff=-0.08).scale(0.25)

        minotaur_miniature = ImageMobject("assets/minotaur-nobackground-outline.png").set_height(0.8).move_to(RIGHT * (minotaur_position[0] + 0.5) + DOWN * (minotaur_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT).set_z_index(1000000 + 1)

        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(Group(theseus, minotaur)).scale(1.25),
                AnimationGroup(
                    FadeIn(minotaur),
                    FadeIn(minotaur_text, lag_ratio=0.1),
                    lag_ratio=0.5,
                ),
                lag_ratio=0.25,
            ),
        )

        maze, maze_dict = maze_to_vgroup(contents)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(theseus_text),
                    FadeOut(minotaur_text),
                ),
                AnimationGroup(
                    self.camera.frame.animate.move_to(Group(theseus_miniature, minotaur_miniature)).set_height(maze.height * 0.3),
                    FadeTransform(theseus, theseus_miniature),
                    FadeTransform(minotaur, minotaur_miniature),
                ),
                AnimationGroup(
                    FadeIn(maze),
                ),
                lag_ratio=0.5,
                run_time=2,
            )
        )

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature, minotaur_miniature.copy().shift(LEFT * 2))).scale(0.85),
            minotaur_miniature.animate.shift(LEFT * 2),
        )

        for i in range(1):
            self.play(
                self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(LEFT), minotaur_miniature.copy().shift(LEFT * 2))).scale(0.85),
                minotaur_miniature.animate.shift(LEFT * 2),
                theseus_miniature.animate.shift(LEFT),
            )

        rect = get_fade_rect()

        canhe = Tex(r"\underline{Can he get out?}").scale(1.25).next_to(Group(theseus_miniature, minotaur_miniature), UP, buff=0.25).set_z_index(10000000)

        self.play(
            AnimationGroup(
                FadeIn(rect),
                AnimationGroup(
                    self.camera.frame.animate.move_to(Group(theseus_miniature, minotaur_miniature, canhe)),
                    FadeIn(canhe, shift=UP * 0.25),
                ),
                lag_ratio=0.5
            )
        )

        self.play(
            FadeOut(rect),
            FadeOut(canhe),
            self.camera.frame.animate.move_to(Group(theseus_miniature, minotaur_miniature)),
        )

        self.play(
            Flash(minotaur_miniature, color=WHITE),
            FadeOut(minotaur_miniature),
        )

        self.play(
            self.camera.frame.animate.move_to(maze).set_height(maze.height * 1.25),
            run_time=1.5,
        )

        shortest_path = [
            (21, 9),
            (22, 9),
            (23, 9),
            (24, 9),
            (25, 9),
            (26, 9),
            (27, 9),
            (27, 10),
            (27, 11),
            (27, 12),
            (27, 13),
            (27, 14),
            (27, 15),
            (28, 15),
            (29, 15),
            (30, 15),
            (31, 15),
            (32, 15),
            (33, 15),
            (34, 15),
            (35, 15),
            (36, 15),
            (37, 15),
            (37, 16),
            (37, 17),
            (38, 17),
            (39, 17),
            (39, 16),
            (39, 15),
            (40, 15),
        ]

        theseus_miniature.set_z_index(1)

        self.play(
            AnimationGroup(*[maze_dict[p].animate.set_fill(ORANGE, 0.75).set_stroke_color(ORANGE) for p in shortest_path], lag_ratio=0.02),
        )

        self.play(
            AnimationGroup(*[maze_dict[p].animate.set_fill(WHITE, 0).set_stroke_color(WHITE) for p in shortest_path]),
        )

        bfs_text = Tex("BFS").scale(5).next_to(maze, RIGHT, buff=1.5).align_to(maze, UP).shift(DOWN)

        q = Queue(scale=2).next_to(bfs_text, DOWN, buff=2)

        self.play(
            FadeIn(q),
            FadeIn(bfs_text),
            self.camera.frame.animate.move_to(Group(maze, theseus_miniature, q, bfs_text)),
            run_time=1,
        )

        theseus_position = (theseus_position[0] - 1, theseus_position[1])

        queue = [theseus_position]
        discovered = {theseus_position: None}

        def is_valid(position):
            x, y = position
            return 0 <= x < len(contents[0]) and 0 <= y < len(contents) and contents[y][x] != "#"

        def next_states(position):
            x, y = position
            states = []

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx = x + dx
                ny = y + dy

                if is_valid((nx, ny)):
                    states.append((nx, ny))

            return states

        def animate_discover(states):
            return AnimationGroup(*[maze_dict[p].animate.set_fill(BLUE, 0.75).set_stroke_color(BLUE) for p in states])

        def animate_leave(state):
            return maze_dict[state].animate.set_fill(LIGHT_GRAY, 0.75).set_stroke_color(LIGHT_GRAY).set_z_index(3)

        def animate_add_to_queue(states):
            fade_froms = [maze_dict[s] for s in states]
            state_texs = [Tex(s) for s in states]

            return q.animate_add_from(state_texs, fade_froms)

        def animate_pop_from_queue(state):
            copy = maze_dict[state].copy().set_fill(WHITE, 0).set_stroke_color(WHITE).set_z_index(0.05)

            return (AnimationGroup(
                q.animate_remove_to(copy),
                maze_dict[state].animate.set_fill(ORANGE, 0.75).set_stroke_color(ORANGE).set_z_index(2),
            ), copy)

        def stop_condition(state):
            return state == escape

        i = 1

        def add_neighbours(position):
            states = []
            for next_state in next_states(position):
                if next_state not in discovered:
                    discovered[next_state] = position
                    queue.append(next_state)
                    states.append(next_state)

            if len(states) != 0:
                self.play(
                    animate_leave(current),
                    animate_discover(states),
                    animate_add_to_queue(states),
                )
            else:
                self.play(
                    animate_leave(current),
                )

        self.play(
            animate_discover([theseus_position]),
            animate_add_to_queue([theseus_position]),
        )

        escape = (40, 15)

        queue2 = [theseus_position]
        discovered2 = {theseus_position: 0}

        while len(queue2) != 0:
            current = queue2.pop(0)

            for next_state in next_states(current):
                if next_state not in discovered2:
                    discovered2[next_state] = discovered2[current] + 1
                    queue2.append(next_state)

        self.play(
            AnimationGroup(
                *[AnimationGroup(*[maze_dict[p].animate(rate_func=there_and_back, run_time=1.5).set_color(BLUE).set_fill(BLUE, 0.75)
                                   for p in discovered2.keys()
                                   if discovered2[p] == d])
                  for d in range(0, max(discovered2.values()) + 1)],
                lag_ratio=0.025,
            )
        )

        # for debug
        path = list(reversed(shortest_path))

        while len(queue) != 0:
            current = queue.pop(0)

            if config.quality.startswith("medium") and i > 10:
                break

            i += 1

            a, o = animate_pop_from_queue(current)

            self.play(a)

            self.remove(o)
            self.remove(theseus_miniature)
            theseus_miniature.set_z_index(10000)
            self.add(theseus_miniature)

            if stop_condition(current):
                path = [current]
                while discovered[current] is not None:
                    current = discovered[current]
                    path.append(current)

                break

            add_neighbours(current)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    *[maze_dict[p].animate.set_fill(ORANGE, 0.75).set_stroke_color(ORANGE) for p in reversed(path)],
                    lag_ratio=0.02
                ),
                AnimationGroup(
                    *[maze_dict[k].animate.set_fill(WHITE, 0).set_stroke_color(WHITE)
                      for k in discovered2
                      if k not in path],
                ),
            lag_ratio=0.75,
            ),
        )

        self.wait()


class BFSMinotaur(MovingCameraScene):
    @fade
    def construct(self):
        self.next_section(skip_animations=True) # don't remove
        blocks = code_parts_from_file("programs/bfs.py")

        bfs = Tex("Breadth-first search").scale(1.65)

        code_web = align_code(
            [
                ("-", "c"),
                [
                    ("|", "c"),
                    bfs,
                    blocks["start"],
                    blocks["output"],
                ],
                [
                    ("|", "l"),
                    blocks["is_valid"],
                    blocks["next_states"],
                    blocks["bfs_better"],
                ]
            ],
        )

        start_group = VGroup(bfs, blocks['start'].background_mobject)

        blocks["output"].align_to(blocks["start"], RIGHT)

        self.camera.frame.move_to(blocks["bfs_better"]).set_height(blocks["bfs_better"].height * 1.2)

        self.add(*code_web)

        self.remove(blocks["output"])

        self.play(
            FadeCode(blocks["start"]),
            FadeCode(blocks["is_valid"]),
            FadeCode(blocks["next_states"]),
        )

        self.next_section() # don't remove

        highlight = CreateHighlightCodeLine(blocks["bfs_better"], 0, start=8, end=38)

        self.play(FadeIn(highlight))

        self.play(Transform(highlight, CreateHighlightCodeLines(blocks["bfs_better"], [20, 21, 22, 23], offset=2)))

        # via the next_states function
        self.play(Transform(highlight, CreateHighlightCodeLine(blocks["bfs_better"], 20, start=20, end=40)))

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeCode(blocks['bfs_better']),
                    FadeOut(highlight),
                ),
                self.camera.frame.animate.move_to(start_group),
                UnfadeCode(blocks['start']),
                lag_ratio=0.5,
            )
        )

        blocks_minotaur = code_parts_from_file("programs/minotaur.py")

        bfs_copy = bfs.copy()

        code_web_minotaur = align_code(
            [
                ("-", "c"),
                [
                    ("|", "c"),
                    bfs_copy,
                    blocks_minotaur["start"],
                    blocks_minotaur["output"],
                ],
                [
                    ("|", "l"),
                    blocks_minotaur["is_valid"],
                    blocks_minotaur["next_theseus_positions"],
                    blocks_minotaur["next_minotaur_position"],
                    blocks_minotaur["next_states"],
                    blocks_minotaur["bfs"],
                ]
            ],
        )
        blocks_minotaur["output"].align_to(blocks_minotaur["start"], RIGHT)

        align_object_by_coords(
            code_web_minotaur,
            blocks_minotaur["start"],
            blocks_minotaur["start"].copy().move_to(blocks["start"]).align_to(blocks["start"], UP).align_to(blocks["start"], RIGHT),
        )

        blocks_minotaur["start_partial"].move_to(blocks["start"])

        blocks_minotaur["start_partial_2"].set_z_index(10)

        self.camera.frame.save_state()

        self.play(
            self.camera.frame.animate.move_to(blocks_minotaur["start_partial"].code[0:10]).scale(0.5)
        )

        self.play(
            FadeIn(blocks_minotaur["start_partial"]),
            Flash(blocks_minotaur["start_partial"].code[4][8], color=blocks_minotaur["start_partial"].code[4][8].color, flash_radius=0.175),
        )

        self.play(self.camera.frame.animate.restore())

        blocks_minotaur["start_partial_2"].move_to(blocks_minotaur["start_partial"]).align_to(blocks_minotaur["start_partial"], UP)

        # TODO: hackish
        for mobject in self.mobjects:
            self.remove(mobject)

        self.add(blocks["is_valid"])
        self.add(blocks["next_states"])
        self.add(bfs)
        self.add(blocks["bfs_better"])

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeTransform(blocks_minotaur["start_partial"].background_mobject, blocks_minotaur["start_partial_2"].background_mobject),
                    Transform(blocks_minotaur["start_partial"].code[:14], blocks_minotaur["start_partial_2"].code[:14]),
                    Transform(blocks_minotaur["start_partial"].code[14:21], blocks_minotaur["start_partial_2"].code[15:22]),
                    Transform(blocks_minotaur["start_partial"].code[21:], blocks_minotaur["start_partial_2"].code[24:]),
                    self.camera.frame.animate.move_to(blocks_minotaur["start_partial_2"]).set_height(blocks_minotaur["start_partial_2"].height * 1.2),
                ),
                AnimationGroup(
                    Write(blocks_minotaur["start_partial_2"].code[14]),
                    Write(blocks_minotaur["start_partial_2"].code[22:24]),
                    run_time=1,
                ),
                lag_ratio=0.75,
            )
        )

        blocks_minotaur["start"].set_z_index(20)
        blocks_minotaur["start_partial_2"].set_z_index(20)
        blocks_minotaur["start_partial_2"].background_mobject.set_z_index(0)
        blocks_minotaur["start_this_sucks"].background_mobject.set_z_index(1)

        blocks_minotaur["start"].align_to(blocks_minotaur["start_partial_2"], LEFT)
        blocks_minotaur["start_this_sucks"].align_to(blocks_minotaur["start"], LEFT).align_to(blocks_minotaur["start"], UP)

        highlight = CreateHighlightCodeLine(blocks_minotaur["start"], -3, start=1).set_z_index(1000)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeTransform(blocks_minotaur["start_partial_2"].background_mobject, blocks_minotaur["start_this_sucks"].background_mobject),
                    Transform(blocks_minotaur["start_partial"].code[-1][4:12], blocks_minotaur["start"].code[-3][2:10]),
                    *[Transform(blocks_minotaur["start_partial"].code[-1][12 + i], blocks_minotaur["start"].code[-2][0 + i]) for i in range(20)],
                    Transform(blocks_minotaur["start_partial"].code[-1][33:-1], blocks_minotaur["start"].code[-2][24:]),
                    Transform(blocks_minotaur["start_partial"].code[-1][-1], blocks_minotaur["start"].code[-1][-1]),
                    self.camera.frame.animate.move_to(blocks_minotaur["start_this_sucks"]).set_height(blocks_minotaur["start_this_sucks"].height * 1.2),
                ),
                AnimationGroup(
                    Write(blocks_minotaur["start"].code[-3][:2]),
                    Write(blocks_minotaur["start"].code[-3][10:]),
                    Write(blocks_minotaur["start"].code[-2][20:23]),
                    run_time=1,
                ),
                lag_ratio=0.75,
            )
        )

        self.play(FadeIn(highlight))

        self.play(Transform(highlight, CreateHighlightCodeLine(blocks_minotaur["start"], -2, start=1).set_z_index(1000)))

        # TODO: hackish
        for mobject in self.mobjects:
            self.remove(mobject)

        self.add(blocks["is_valid"])
        self.add(blocks["next_states"])
        self.add(bfs)
        self.add(blocks_minotaur["start"])
        self.add(blocks["bfs_better"])

        blocks_minotaur["start"].background_mobject.become(blocks_minotaur["start_this_sucks"].background_mobject)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeCode(blocks_minotaur['start']),
                    FadeOut(highlight),
                ),
                self.camera.frame.animate.move_to(blocks['next_states']),
                UnfadeCode(blocks['next_states']),
                lag_ratio=0.5,
            )
        )

        ntp_copy = blocks_minotaur['next_theseus_positions'].copy().move_to(blocks['next_states'])

        self.play(
            FadeTransform(blocks['next_states'].code[0][9:9+6], ntp_copy.code[0][9:9+17]),
            Transform(blocks['next_states'].code[0][9+6:], ntp_copy.code[0][9+17:]),
        )

        # TODO: hackish
        for mobject in self.mobjects:
            self.remove(mobject)

        self.add(blocks["is_valid"])
        self.add(ntp_copy)
        self.add(bfs)
        self.add(blocks_minotaur["start"])
        self.add(blocks["bfs_better"])

        blocks_minotaur['is_valid'].set_opacity(BIG_OPACITY)
        blocks_minotaur['next_theseus_positions'].set_opacity(BIG_OPACITY)
        blocks_minotaur['bfs'].set_opacity(BIG_OPACITY)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Transform(blocks['is_valid'], blocks_minotaur['is_valid']),
                    Transform(ntp_copy, blocks_minotaur['next_theseus_positions']),
                    Transform(blocks['bfs_better'], blocks_minotaur["bfs"]),
                    self.camera.frame.animate.move_to(blocks_minotaur["next_minotaur_position"].background_mobject),
                ),
                AnimationGroup(
                    FadeIn(blocks_minotaur["next_minotaur_position"].background_mobject),
                ),
                lag_ratio=0.5,
            )
        )

        self.play(
            Write(blocks_minotaur["next_minotaur_position"].code[:2]),
        )

        highlight = CreateHighlightCodeLine(blocks_minotaur["next_minotaur_position"], 1, start=8, end=10)

        self.play(FadeIn(highlight))
        self.play(Transform(highlight, CreateHighlightCodeLine(blocks_minotaur["next_minotaur_position"], 1, start=25, end=26)))
        self.play(Transform(highlight, CreateHighlightCodeLine(blocks_minotaur["next_minotaur_position"], 1, start=42, end=44)))
        self.play(FadeOut(highlight))

        blocks_minotaur["next_minotaur_position_move_forward_example"].move_to(blocks_minotaur["next_minotaur_position"])

        self.camera.frame.save_state()

        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(blocks_minotaur["next_minotaur_position_move_forward_example"].code[3:6]).scale(0.5),
                FadeIn(blocks_minotaur["next_minotaur_position_move_forward_example"].code[3:6]),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                FadeOut(blocks_minotaur["next_minotaur_position_move_forward_example"].code[3:6]),
                self.camera.frame.animate.restore(),
                lag_ratio=0.5,
            )
        )

        self.play(
            Write(blocks_minotaur["next_minotaur_position"].code[2:]),
        )

        highlight = CreateHighlightCodeLines(blocks_minotaur["next_minotaur_position"], [8, 9, 10, 11, 12], offset=2)

        self.play(FadeIn(highlight))

        self.play(Transform(highlight, CreateHighlightCodeLines(blocks_minotaur["next_minotaur_position"], [14, 15, 16, 17, 18], offset=2)))

        self.play(Transform(highlight, CreateHighlightCodeLines(blocks_minotaur["next_minotaur_position"], [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], offset=1)))

        self.play(FadeOut(highlight))

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeCode(blocks_minotaur["next_minotaur_position"]),
                    self.camera.frame.animate.move_to(blocks_minotaur["next_states"].background_mobject),
                ),
                AnimationGroup(
                    FadeIn(blocks_minotaur["next_states"].background_mobject),
                    Write(blocks_minotaur["next_states"].code),
                ),
                lag_ratio=0.5,
            )
        )

        highlight = CreateHighlightCodeLines(blocks_minotaur["next_states"], [1], offset=1)

        self.play(FadeIn(highlight))

        self.play(Transform(highlight, CreateHighlightCodeLines(blocks_minotaur["next_states"], [4], offset=1)))
        self.play(Transform(highlight, CreateHighlightCodeLines(blocks_minotaur["next_states"], [5], offset=2)))
        self.play(Transform(highlight, CreateHighlightCodeLines(blocks_minotaur["next_states"], [7, 8], offset=2)))
        self.play(Transform(highlight, CreateHighlightCodeLines(blocks_minotaur["next_states"], [10], offset=2)))

        self.play(FadeOut(highlight))

        maze_str = [
            "##########",
            "#       E#",
            "#   #   ##",
            "# T # M  #",
            "#   #    #",
            "#   #    #",
            "#   #    #",
            "#  #     #",
            "##########",
        ]

        solution = [
            ((2, 3), (6, 3)),
            ((2, 4), (5, 4)),
            ((2, 5), (5, 5)),
            ((2, 6), (5, 6)),
            ((2, 7), (4, 7)),
            ((2, 6), (4, 7)),
            ((3, 6), (4, 7)),
            ((3, 5), (4, 7)),
            ((3, 4), (4, 7)),
            ((3, 3), (4, 7)),
            ((3, 2), (4, 7)),
            ((3, 1), (4, 7)),
            ((4, 1), (4, 7)),
            ((5, 1), (5, 6)),
            ((6, 1), (6, 5)),
            ((7, 1), (7, 4)),
            ((8, 1), (8, 3)),
        ]

        maze, maze_dict = maze_to_vgroup(maze_str)

        maze.next_to(blocks_minotaur['output'], LEFT, buff=ALIGN_SPACING)
        maze.align_to(blocks_minotaur['output'], UP)

        theseus = ImageMobject("assets/theseus-nobackground-outline.png").set_height(0.8).move_to(maze_dict[(solution[0][0])]).set_z_index(10000000)
        minotaur = ImageMobject("assets/minotaur-nobackground-outline.png").set_height(0.8).move_to(maze_dict[(solution[0][1])]).set_z_index(10000000)

        door = ImageMobject("assets/door-outline.png").set_height(0.8).move_to(maze_dict[(solution[-1][0])]).set_z_index(10000000000000000000000000)

        numbers_x = VGroup(*[Tex(str(i), color=BLACK).scale(0.85).move_to(maze_dict[(i, 0)]).set_z_index(1000000000)
                             for i in range(1, len(maze_str[0]) - 1)
                            ])

        numbers_y = VGroup(*[Tex(str(i), color=BLACK).scale(0.85).move_to(maze_dict[(0, i)]).set_z_index(1000000000)
                             for i in range(1, len(maze_str) - 1)
                            ])

        self.play(
            AnimationGroup(
                FadeCode(blocks_minotaur["next_states"]),
                AnimationGroup(
                    FadeIn(blocks_minotaur["output"].background_mobject),
                    Write(blocks_minotaur["output"].code),
                    self.camera.frame.animate.move_to(VGroup(maze, blocks_minotaur['output'])).scale(0.9),
                    FadeIn(maze),
                    FadeIn(theseus),
                    FadeIn(minotaur),
                    FadeIn(door),
                ),
                AnimationGroup(
                    AnimationGroup(*[FadeIn(n) for n in numbers_x], lag_ratio=0.05),
                    AnimationGroup(*[FadeIn(n) for n in numbers_y], lag_ratio=0.05),
                ),
                lag_ratio=0.5,
            ),
        )

        highlight = CreateHighlightCodeLine(blocks_minotaur["output"], 1)

        prev_m = None
        for i, (t, m) in enumerate(solution):
            anim = None

            if i == 0:
                anim = FadeIn(highlight)
            else:
                anim = Transform(highlight, CreateHighlightCodeLine(blocks_minotaur["output"], i + 1))

            anim2 = None
            if t == solution[-1][0]:
                anim2 = theseus.animate.set_opacity(0).move_to(maze_dict[t])
            else:
                anim2 = theseus.animate.move_to(maze_dict[t])

            if prev_m == m:
                maze_dict[t].set_z_index(0.05)
                self.play(
                    AnimationGroup(
                        AnimationGroup(anim, anim2),
                        maze_dict[t].animate.set_fill(ORANGE, 0.75).set_stroke_color(ORANGE),
                        lag_ratio=0.33,
                    ),
                )
            else:
                maze_dict[t].set_z_index(0.05)
                maze_dict[m].set_z_index(0.05)
                self.play(
                    AnimationGroup(
                        AnimationGroup(
                            AnimationGroup(anim, anim2),
                            maze_dict[t].animate.set_fill(ORANGE, 0.75).set_stroke_color(ORANGE),
                            lag_ratio=0.33,
                        ),
                        AnimationGroup(
                            minotaur.animate.move_to(maze_dict[m]),  # TODO: split it into two moves?
                            maze_dict[m].animate.set_fill(BLUE, 0.75).set_stroke_color(BLUE),
                            lag_ratio=0.33,
                        ),
                        lag_ratio=0.25,
                    ),
                )

            prev_m = m

        bfs = Tex("BFS").scale(2.5)
        bfs_full = Tex("(Breadth-first search)").scale(1.5).next_to(bfs, DOWN)

        a = VGroup(bfs, bfs_full)

        stop = Tex(r"\parbox{18em}{Solves problems that have \textit{states} where the goal is to get from the \textit{starting} state to an \textit{ending state} in the \textit{least amount of steps possible:}}")

        l1 = Tex(r"\begin{itemize} \item shortest path \end{itemize}")
        l2 = Tex(r"\begin{itemize} \item Theseus and the Minotaur \end{itemize}")

        l = VGroup(l1, l2).arrange(DOWN, buff=0.25)
        l2.align_to(l1, LEFT)

        b = VGroup(stop, l).arrange(DOWN, buff=0.75)

        VGroup(a, b).arrange(DOWN, buff=1).next_to(blocks_minotaur['bfs'], LEFT, buff=1.5)

        self.play(
            AnimationGroup(
                FadeOut(highlight),
                FadeOut(maze),
                FadeOut(blocks_minotaur["output"].background_mobject),
                FadeOut(blocks_minotaur["output"].code),
                FadeOut(theseus),
                FadeOut(minotaur),
                FadeOut(door),
                FadeOut(numbers_x),
                FadeOut(numbers_y),
                FadeOut(blocks_minotaur["next_states"]),
                FadeOut(blocks_minotaur["start"]),
                FadeOut(blocks_minotaur["next_minotaur_position"]),
                FadeOut(blocks_minotaur["next_theseus_positions"]),
            ),
            AnimationGroup(
                AnimationGroup(
                    UnfadeCode(blocks_minotaur['bfs']),
                    self.camera.frame.animate.move_to(VGroup(blocks_minotaur['bfs'], a, b)),
                ),
                Write(a),
                lag_ratio=0.75,
            ),
        )

        l.align_to(stop, LEFT).shift(RIGHT * 0.3)

        self.play(Write(stop), run_time=2.5)
        self.play(Write(l1), run_time=0.75)
        self.play(Write(l2), run_time=1)


class BFS(MovingCameraScene):
    @fade
    def construct(self):
        blocks = code_parts_from_file("programs/bfs.py")

        bfs = Tex("Breadth-first search").scale(1.65)

        code_web = align_code(
            [
                ("-", "c"),
                [
                    ("|", "c"),
                    bfs,
                    blocks["start"],
                    blocks["output"],
                ],
                [
                    ("|", "l"),
                    blocks["is_valid"],
                    blocks["next_states"],
                    blocks["bfs"],
                ]
            ],
        )

        start_group = VGroup(bfs, blocks['start'].background_mobject)

        self.camera.frame.move_to(start_group).set_height(start_group.height * 1.2),

        self.play(
            Write(bfs, run_time=1.5),
            Write(blocks['start'].background_mobject),
        )

        self.play(
            Write(blocks['start'].code[:11]),
            run_time=1.5,
        )

        highlight = CreateHighlightCodeLine(blocks["start"], 4, start=4, end=5)

        self.play(FadeIn(highlight))
        self.play(Transform(highlight, CreateHighlightCodeLine(blocks["start"], 2, start=10, end=11)))
        self.play(FadeOut(highlight))

        self.play(
            Write(blocks['start'].code[12:14]),
            run_time=1,
        )

        self.play(
            Write(blocks['start'].code[15:22]),
            run_time=2.5,
        )

        question = Tex(r"\underline{What now?}").set_z_index(1000001).move_to(self.camera.frame).scale(2)
        answer = Tex(r"write small functions!").set_z_index(1000001).move_to(self.camera.frame).scale(1.25)

        group = VGroup(question.copy(), answer)
        answer.next_to(question, DOWN, buff=0.25)

        self.play(
            AnimationGroup(
                FadeCode(blocks['start'], skip_lines=[22]),
                FadeIn(question),
                lag_ratio=0.5
            )
        )

        self.play(
            AnimationGroup(
                Transform(question, group[0]),
                FadeIn(group[1], run_time=1),
                lag_ratio=0.75
            )
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(question),
                    FadeOut(answer),
                ),
                self.camera.frame.animate.move_to(blocks['is_valid']),
                WriteCode(blocks['is_valid']),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                FadeCode(blocks['is_valid']),
                self.camera.frame.animate.move_to(blocks['next_states']),
                WriteCode(blocks['next_states']),
                lag_ratio=0.5,
            )
        )

        blocks['next_states'].code.set_z_index(1)

        highlight = CreateHighlightCodeLines(blocks['next_states'], [4, 5, 6], offset=1)

        self.play(FadeIn(highlight))

        self.play(Transform(highlight, CreateHighlightCodeLines(blocks['next_states'], [8, 9], offset=2)))

        self.play(Transform(highlight, CreateHighlightCodeLines(blocks['next_states'], [11], offset=1)))

        self.play(FadeOut(highlight))

        self.play(
            AnimationGroup(
                FadeCode(blocks['next_states']),
                self.camera.frame.animate.move_to(blocks['bfs']),
                Write(blocks['bfs'].background_mobject),
                lag_ratio=0.5,
            )
        )

        self.play(Write(blocks['bfs'].code[0]), run_time=1)

        highlight = CreateHighlightCodeLine(blocks["bfs"], 0, start=8, end=22)

        self.play(FadeIn(highlight))
        self.play(Transform(highlight, CreateHighlightCodeLine(blocks["bfs"], 0, start=24, end=38)))

        stop = Tex(r"\parbox{12em}{Allows us to support more complex ways of ending the BFS (multiple escape tiles).}").set_z_index(1000001).scale(0.5).next_to(highlight, DOWN)

        pointless = Tex(r"\parbox{12em}{Is this pointless?}").set_z_index(1000001).scale(0.5).next_to(highlight, DOWN)

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.move_to(VGroup(highlight, stop)).scale(0.25))
        self.play(FadeIn(pointless))
        self.play(
            FadeOut(pointless, shift=UP * 0.3),
            FadeIn(stop, shift=UP * 0.3),
        )

        self.play(
            AnimationGroup(
            FadeOut(stop),
            FadeOut(highlight),
            self.camera.frame.animate.restore(),
            lag_ratio=0.5,
            ),
        )

        self.play(Write(blocks['bfs'].code[1]), run_time=1)
        self.play(Write(blocks['bfs'].code[2]), run_time=1)

        self.play(Write(blocks['bfs'].code[4]), run_time=1)
        self.play(Write(blocks['bfs'].code[5]), run_time=1)

        self.play(Write(blocks['bfs'].code[7:10]), run_time=1.75)

        self.play(Write(blocks['bfs'].code[11:14]), run_time=1.75)
        self.play(Write(blocks['bfs'].code[14]), run_time=1)

        self.play(Write(blocks['bfs'].code[16]), run_time=1)

        blocks["bfs_mid"].align_to(blocks["bfs"], UP).align_to(blocks["bfs"], LEFT)
        blocks["bfs_better"].align_to(blocks["bfs"], UP).align_to(blocks["bfs"], LEFT)

        highlight = CreateHighlightCodeLine(blocks["bfs"], 2, 1)

        self.play(FadeIn(highlight))

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Transform(highlight, CreateHighlightCodeLine(blocks["bfs_mid"], 2, 1)),
                    Transform(blocks["bfs"].code[2][-1], blocks["bfs_mid"].code[2][-1]),
                ),
                FadeIn(blocks["bfs_mid"].code[2][-10:-1]),
                lag_ratio=0.5,
            )
        )

        self.play(Transform(highlight, CreateHighlightCodeLine(blocks["bfs_mid"], 2, start=15, end=29)))
        self.play(Transform(highlight, CreateHighlightCodeLine(blocks["bfs_mid"], 2, start=31, end=35)))

        blocks["bfs_mid"].code[14].move_to(blocks["bfs"].code[14]).align_to(blocks["bfs"].code[14], LEFT)

        h = highlight
        highlight = CreateHighlightCodeLine(blocks["bfs"], 14, start=4)

        self.play(
            FadeOut(h),
            FadeIn(highlight),
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Transform(highlight, CreateHighlightCodeLine(blocks["bfs_mid"], 14, start=4)),
                    FadeTransform(blocks["bfs"].code[14][14:19], blocks["bfs_mid"].code[14][14]),
                    FadeTransform(blocks["bfs"].code[14][19:19+7], blocks["bfs_mid"].code[14][-7:1000]),
                    FadeTransform(blocks["bfs"].code[14][-1], blocks["bfs_mid"].code[14][25]),
                    FadeTransform(blocks["bfs"].background_mobject, blocks["bfs_mid"].background_mobject)
                ),
                AnimationGroup(
                    FadeIn(blocks["bfs_mid"].code[14][14:25]),
                    FadeIn(blocks["bfs_mid"].code[14][27]),
                ),
                lag_ratio=0.5,
            )
        )

        self.play(FadeOut(highlight))

        # TODO: hackish
        for mobject in self.mobjects:
            self.remove(mobject)

        self.add(blocks["start"])
        self.add(blocks["is_valid"])
        self.add(blocks["next_states"])
        self.add(bfs)
        self.add(blocks["bfs_mid"])
        self.remove(blocks["start"].code[-1])

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeTransform(blocks["bfs_mid"].background_mobject, blocks["bfs_better"].background_mobject),
                    FadeTransform(blocks["bfs_mid"].code[10:], blocks["bfs_better"].code[19:]),
                    FadeTransform(blocks["bfs_mid"].code[9][3:], blocks["bfs_better"].code[18][3:]),
                    self.camera.frame.animate.move_to(blocks["bfs_better"]).set_height(blocks["bfs_better"].height * 1.2),
                ),
                FadeIn(blocks["bfs_better"].code[9:18]),
                lag_ratio=0.5,
            )
        )

        highlight = CreateHighlightCodeLine(blocks["bfs_better"], 10, start=3)

        self.play(FadeIn(highlight))
        self.play(Transform(highlight, CreateHighlightCodeLine(blocks["bfs_better"], 11, start=3)))
        self.play(Transform(highlight, CreateHighlightCodeLines(blocks["bfs_better"], [12], offset=4)))
        self.play(Transform(highlight, CreateHighlightCodeLines(blocks["bfs_better"], [13], offset=4)))
        self.play(Transform(highlight, CreateHighlightCodeLines(blocks["bfs_better"], [15, 16], offset=3)))
        self.play(FadeOut(highlight))

        # TODO: hackish
        for mobject in self.mobjects:
            self.remove(mobject)

        self.add(blocks["start"])
        self.add(blocks["is_valid"])
        self.add(blocks["next_states"])
        self.add(bfs)
        self.add(blocks["bfs_better"])
        self.remove(blocks["start"].code[-1])

        self.play(
            AnimationGroup(
                FadeCode(blocks['bfs_better']),
                self.camera.frame.animate.move_to(blocks['start'].code[22]),
                UnfadeCode(blocks['start'], skip_lines=[22]),
                lag_ratio=0.5,
            )
        )

        self.add(blocks["start"].code[-1])
        self.play(Write(blocks['start'].code[22]), run_time=1)

        highlight = CreateHighlightCodeLine(blocks['start'], 22, 4, 11)

        self.play(FadeIn(highlight))
        self.play(Transform(highlight, CreateHighlightCodeLine(blocks['start'], 22, 13, -1)))
        self.play(FadeOut(highlight))

        blocks["output"].align_to(blocks["start"], RIGHT)

        maze_str = [
            "##########",
            "#       E#",
            "#   #   ##",
            "# T #    #",
            "#   #    #",
            "#   #    #",
            "#   #    #",
            "#  #     #",
            "##########",
        ]

        solution = [
            (2, 3),
            (3, 3),
            (3, 2),
            (3, 1),
            (4, 1),
            (5, 1),
            (6, 1),
            (7, 1),
            (8, 1),
        ]

        maze, maze_dict = maze_to_vgroup(maze_str)

        maze.next_to(blocks['output'], LEFT, buff=ALIGN_SPACING)
        maze.align_to(blocks['output'], UP)

        theseus = ImageMobject("assets/theseus-nobackground-outline.png").set_height(0.8).move_to(maze_dict[(solution[0])]).set_z_index(100)

        door = ImageMobject("assets/door-outline.png").set_height(0.8).move_to(maze_dict[(solution[-1])]).set_z_index(10000000000000000)

        numbers_x = VGroup(*[Tex(str(i), color=BLACK).scale(0.85).move_to(maze_dict[(i, 0)]).set_z_index(1000000000)
                             for i in range(1, len(maze_str[0]) - 1)
                            ])

        numbers_y = VGroup(*[Tex(str(i), color=BLACK).scale(0.85).move_to(maze_dict[(0, i)]).set_z_index(1000000000)
                             for i in range(1, len(maze_str) - 1)
                            ])

        self.play(
            AnimationGroup(
                FadeCode(blocks['start']),
                AnimationGroup(
                    self.camera.frame.animate.move_to(VGroup(maze, blocks['output'])).scale(0.9),
                    FadeIn(maze),
                    FadeIn(theseus),
                    FadeIn(door),
                    WriteCode(blocks['output']),
                ),
                AnimationGroup(
                    AnimationGroup(*[FadeIn(n) for n in numbers_x], lag_ratio=0.05),
                    AnimationGroup(*[FadeIn(n) for n in numbers_y], lag_ratio=0.05),
                ),
                lag_ratio=0.5,
            ),
        )

        highlight = CreateHighlightCodeLine(blocks["output"], 1)

        for i, step in enumerate(solution):
            anim = None

            if i == 0:
                anim = FadeIn(highlight)
            else:
                anim = Transform(highlight, CreateHighlightCodeLine(blocks["output"], i + 1))

            anim2 = None
            if step == solution[-1]:
                anim2 = theseus.animate.set_opacity(0).move_to(maze_dict[step])
            else:
                anim2 = theseus.animate.move_to(maze_dict[step])
            maze_dict[step].set_z_index(0.05)

            self.play(
                AnimationGroup(
                    AnimationGroup(anim, anim2),
                    maze_dict[step].animate.set_fill(ORANGE, 0.75).set_stroke_color(ORANGE),
                    lag_ratio=0.33,
                )
            )

        # TODO: animate move camera to bfs and fade other things rthen then show a list of the things that im talking about ok?


class AOC(MovingCameraScene):
    @fade
    def construct(self):
        text = ImageMobject("assets/aoc/logo.png").set_height(0.75).shift(UP * 2)
        aoc = SVGMobject("assets/aoc/aoc.svg").set_width(self.camera.frame.get_width() * 0.8).next_to(text, DOWN, buff=1)

        seed(0xDEADBEEF)

        offsets = [uniform(0.05, 0.1) for _ in range(1000)]
        offsets2 = [uniform(0, 2 * pi) for _ in range(1000)]
        times = [0 for _ in range(1000)]
        original_position = []

        def bob(i, obj, dt):
            times[i] += dt
            offset = sin(self.renderer.time * pi + offsets2[(i - 1) // 3]) * offsets[(i - 1) // 3]

            obj.move_to(original_position[i-1] + UP * offset)

        # for-loop doesn't work because the variable changes in the lambda
        # I'm too lazy to fix it, sue me

        original_position.append(aoc[-1].get_center())
        aoc[-1].add_updater(lambda x, dt: bob(1, x, dt))

        original_position.append(aoc[-2].get_center())
        aoc[-2].add_updater(lambda x, dt: bob(2, x, dt))

        original_position.append(aoc[-3].get_center())
        aoc[-3].add_updater(lambda x, dt: bob(3, x, dt))

        original_position.append(aoc[-4].get_center())
        aoc[-4].add_updater(lambda x, dt: bob(4, x, dt))

        original_position.append(aoc[-5].get_center())
        aoc[-5].add_updater(lambda x, dt: bob(5, x, dt))

        original_position.append(aoc[-6].get_center())
        aoc[-6].add_updater(lambda x, dt: bob(6, x, dt))

        original_position.append(aoc[-7].get_center())
        aoc[-7].add_updater(lambda x, dt: bob(7, x, dt))

        original_position.append(aoc[-8].get_center())
        aoc[-8].add_updater(lambda x, dt: bob(8, x, dt))

        original_position.append(aoc[-9].get_center())
        aoc[-9].add_updater(lambda x, dt: bob(9, x, dt))

        original_position.append(aoc[-10].get_center())
        aoc[-10].add_updater(lambda x, dt: bob(10, x, dt))

        original_position.append(aoc[-11].get_center())
        aoc[-11].add_updater(lambda x, dt: bob(11, x, dt))

        original_position.append(aoc[-12].get_center())
        aoc[-12].add_updater(lambda x, dt: bob(12, x, dt))

        original_position.append(aoc[-13].get_center())
        aoc[-13].add_updater(lambda x, dt: bob(13, x, dt))

        original_position.append(aoc[-14].get_center())
        aoc[-14].add_updater(lambda x, dt: bob(14, x, dt))

        original_position.append(aoc[-15].get_center())
        aoc[-15].add_updater(lambda x, dt: bob(15, x, dt))

        original_position.append(aoc[-16].get_center())
        aoc[-16].add_updater(lambda x, dt: bob(16, x, dt))

        original_position.append(aoc[-17].get_center())
        aoc[-17].add_updater(lambda x, dt: bob(17, x, dt))

        original_position.append(aoc[-18].get_center())
        aoc[-18].add_updater(lambda x, dt: bob(18, x, dt))

        original_position.append(aoc[-19].get_center())
        aoc[-19].add_updater(lambda x, dt: bob(19, x, dt))

        original_position.append(aoc[-20].get_center())
        aoc[-20].add_updater(lambda x, dt: bob(20, x, dt))

        original_position.append(aoc[-21].get_center())
        aoc[-21].add_updater(lambda x, dt: bob(21, x, dt))

        original_position.append(aoc[-22].get_center())
        aoc[-22].add_updater(lambda x, dt: bob(22, x, dt))

        original_position.append(aoc[-23].get_center())
        aoc[-23].add_updater(lambda x, dt: bob(23, x, dt))

        original_position.append(aoc[-24].get_center())
        aoc[-24].add_updater(lambda x, dt: bob(24, x, dt))

        original_position.append(aoc[-25].get_center())
        aoc[-25].add_updater(lambda x, dt: bob(25, x, dt))

        original_position.append(aoc[-26].get_center())
        aoc[-26].add_updater(lambda x, dt: bob(26, x, dt))

        original_position.append(aoc[-27].get_center())
        aoc[-27].add_updater(lambda x, dt: bob(27, x, dt))

        original_position.append(aoc[-28].get_center())
        aoc[-28].add_updater(lambda x, dt: bob(28, x, dt))

        original_position.append(aoc[-29].get_center())
        aoc[-29].add_updater(lambda x, dt: bob(29, x, dt))

        original_position.append(aoc[-30].get_center())
        aoc[-30].add_updater(lambda x, dt: bob(30, x, dt))

        original_position.append(aoc[-31].get_center())
        aoc[-31].add_updater(lambda x, dt: bob(31, x, dt))

        original_position.append(aoc[-32].get_center())
        aoc[-32].add_updater(lambda x, dt: bob(32, x, dt))

        original_position.append(aoc[-33].get_center())
        aoc[-33].add_updater(lambda x, dt: bob(33, x, dt))

        original_position.append(aoc[-34].get_center())
        aoc[-34].add_updater(lambda x, dt: bob(34, x, dt))

        original_position.append(aoc[-35].get_center())
        aoc[-35].add_updater(lambda x, dt: bob(35, x, dt))

        original_position.append(aoc[-36].get_center())
        aoc[-36].add_updater(lambda x, dt: bob(36, x, dt))

        original_position.append(aoc[-37].get_center())
        aoc[-37].add_updater(lambda x, dt: bob(37, x, dt))

        original_position.append(aoc[-38].get_center())
        aoc[-38].add_updater(lambda x, dt: bob(38, x, dt))

        original_position.append(aoc[-39].get_center())
        aoc[-39].add_updater(lambda x, dt: bob(39, x, dt))

        original_position.append(aoc[-40].get_center())
        aoc[-40].add_updater(lambda x, dt: bob(40, x, dt))

        original_position.append(aoc[-41].get_center())
        aoc[-41].add_updater(lambda x, dt: bob(41, x, dt))

        original_position.append(aoc[-42].get_center())
        aoc[-42].add_updater(lambda x, dt: bob(42, x, dt))

        self.play(
            FadeIn(aoc),
            FadeIn(text),
        )

        highlight = CreateHighlight(aoc[0:50])

        aoc.set_z_index(10000)

        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(highlight),
                FadeIn(highlight),
                lag_ratio=0.25,
            )
        )

        self.remove(text)

        self.play(
            AnimationGroup(
                self.camera.frame.animate(run_time=1, rate_func=rush_into).scale(0.01),
                AnimationGroup(
                    FadeOut(aoc),
                    FadeOut(highlight),
                    run_time=0.2,
                ),
                lag_ratio=0.8,
            )
        )


class Robots(MovingCameraScene):
    @fade
    def construct(self):
        self.next_section(skip_animations=True)

        robots = VGroup(*[
            SVGMobject("assets/robot-ore.svg"),
            SVGMobject("assets/robot-clay.svg"),
            SVGMobject("assets/robot-obsidian.svg"),
            SVGMobject("assets/robot-geode.svg"),
        ]).arrange(buff=0.8)

        minerals = Group(*[
            ImageMobject("assets/minerals/ore.png"),
            ImageMobject("assets/minerals/clay.png"),
            ImageMobject("assets/minerals/obsidian.png"),
            ImageMobject("assets/minerals/geode.png"),
        ])

        robot_counts = VGroup(*[
            Tex(4).next_to(robots[0], DOWN),
            Tex(0).next_to(robots[1], DOWN),
            Tex(0).next_to(robots[2], DOWN),
            Tex(0).next_to(robots[3], DOWN),
        ])

        for m, r in zip(minerals, robots):
            m.set_height(1).next_to(r, UP)

        self.camera.frame.move_to(Group(minerals, robots))

        mineral_counts = VGroup(*[
            Tex(r"\textbf{0}").move_to(minerals[0]).set_z_index(1),
            Tex(r"\textbf{0}").move_to(minerals[1]).set_z_index(1),
            Tex(r"\textbf{0}").move_to(minerals[2]).set_z_index(1),
            Tex(r"\textbf{0}").move_to(minerals[3]).set_z_index(1),
        ])

        self.play(
            AnimationGroup(*[FadeIn(r, shift=DOWN * 0.25) for r in robots], lag_ratio=0.1)
        )

        for i in range(4):
            self.play(
                FadeIn(minerals[i], shift=UP * 0.25),
                FadeIn(mineral_counts[i], shift=UP * 0.25),
                run_time=0.75
            )

        minute_text = Tex("Minute:").scale(1.5)
        minute_count = Tex(r"\textbf{0}").scale(1.5).next_to(minute_text, RIGHT).align_to(minute_text, DOWN)

        VGroup(minute_text, minute_count).next_to(minerals, UP, buff=1)

        # TODO: check this

        self.play(
            AnimationGroup(
                AnimationGroup(
                    self.camera.frame.animate.move_to(VGroup(minute_text, robot_counts)),
                    robots[1].animate.set_opacity(BIG_OPACITY),
                    robots[2].animate.set_opacity(BIG_OPACITY),
                    robots[3].animate.set_opacity(BIG_OPACITY),
                    minerals[1].animate.set_opacity(BIG_OPACITY),
                    minerals[2].animate.set_opacity(BIG_OPACITY),
                    minerals[3].animate.set_opacity(BIG_OPACITY),
                    run_time=1,
                ),
                AnimationGroup(
                    *[FadeIn(c, shift=DOWN * 0.1) for c in robot_counts],
                    Write(minute_text),
                    FadeIn(minute_count),
                ),
                lag_ratio=0.5,
            ),
        )

        for i in range(1):
            minute_count_1 = Tex(r"\textbf{" + str(i + 1) + "}").scale(1.5).move_to(minute_count)
            self.play(
                FadeOut(minute_count, shift=DOWN * 0.65),
                FadeIn(minute_count_1, shift=DOWN * 0.65),
            )
            minute_count = minute_count_1

            self.play(
                robots[0].animate(rate_func=ROBOT_RATE_FUNC).next_to(minerals[0], DOWN, buff=0),
                minerals[0].animate(rate_func=MINERAL_RATE_FUNC).shift(UP * 0.08),
                Increment(mineral_counts[0], 4 * (i + 1), 0.08),
                run_time=1,
            )

        a = Tex(4).scale(0.8)
        b = minerals[0].copy().set_opacity(1).set_height(a.get_height()).next_to(a, buff=0.05)
        ore_cost = Group(a, b)

        a = Tex(2).scale(0.8)
        b = minerals[0].copy().set_opacity(1).set_height(a.get_height()).next_to(a, buff=0.05)
        clay_cost = Group(a, b)

        a = Tex(3).scale(0.8)
        b = minerals[0].copy().set_opacity(1).set_height(a.get_height()).next_to(a, buff=0.05)
        p = Tex("+").scale(0.8)
        c = Tex(14).scale(0.8)
        d = minerals[1].copy().set_opacity(1).set_height(c.get_height()).next_to(c, buff=0.05)

        obsidian_cost = Group(Group(a, b), p, Group(c, d)).arrange(buff=0.1)

        a = Tex(2).scale(0.8)
        b = minerals[0].copy().set_opacity(1).set_height(a.get_height()).next_to(a, buff=0.05)
        p = Tex("+").scale(0.8)
        c = Tex(7).scale(0.8)
        d = minerals[2].copy().set_opacity(1).set_height(c.get_height()).next_to(c, buff=0.05)

        geode_cost = Group(Group(a, b), p, Group(c, d)).arrange(buff=0.1)

        robot_costs = Group(*[
            ore_cost.next_to(robot_counts[0], DOWN, buff=0.5),
            clay_cost.next_to(robot_counts[1], DOWN, buff=0.5),
            obsidian_cost.next_to(robot_counts[2], DOWN, buff=0.5),
            geode_cost.next_to(robot_counts[3], DOWN, buff=0.5),
            geode_cost.copy().next_to(robot_counts[0], DOWN, buff=0.5), # hack
        ])

        self.play(
            self.camera.frame.animate.move_to(Group(minute_text, robot_costs)).scale(1.15),
            FadeIn(robot_costs[0], shift=DOWN * 0.25),
        )

        self.play(FadeIn(robot_costs[1], shift=DOWN * 0.25))
        self.play(FadeIn(robot_costs[2], shift=DOWN * 0.25))
        self.play(FadeIn(robot_costs[3], shift=DOWN * 0.25))

        # copied fml
        command = 1

        def rot(obj, dt):
            obj.rotate(-dt)

        gear = SVGMobject("assets/gear.svg").set_height(robot_counts[command].get_height()).next_to(robot_counts[command], RIGHT)
        gear.add_updater(rot)

        minute_count_1 = Tex(r"\textbf{2}").scale(1.5).move_to(minute_count)
        self.play(
            FadeOut(minute_count, shift=DOWN * 0.65),
            FadeIn(minute_count_1, shift=DOWN * 0.65),
        )
        minute_count = minute_count_1

        self.play(
            FadeIn(gear, shift=RIGHT * 0.25),
            Transform(mineral_counts[0], Tex(r"\textbf{2}").move_to(mineral_counts[0])),
            minerals[0].animate(rate_func=there_and_back).scale(0.75),
        )

        self.play(
            robots[0].animate(rate_func=ROBOT_RATE_FUNC).next_to(minerals[0], DOWN, buff=0),
            minerals[0].animate(rate_func=MINERAL_RATE_FUNC).shift(UP * 0.08),
            Increment(mineral_counts[0], 6, 0.08),
            run_time=1,
        )

        self.play(
            robots[command].animate.set_opacity(1),
            minerals[command].animate.set_opacity(1),
            Transform(robot_counts[command], Tex(1).move_to(robot_counts[command])),
            FadeOut(gear, shift=RIGHT * 0.25),
        )

        minute_count_1 = Tex(r"\textbf{" + str(0) + "}").scale(1.5).move_to(minute_count)

        self.play(
            FadeOut(minute_count, shift=DOWN * 0.65),
            FadeIn(minute_count_1, shift=DOWN * 0.65),
            robots[0].animate.set_opacity(1),
            robots[1].animate.set_opacity(BIG_OPACITY),
            robots[2].animate.set_opacity(BIG_OPACITY),
            robots[3].animate.set_opacity(BIG_OPACITY),
            minerals[0].animate.set_opacity(1),
            minerals[1].animate.set_opacity(BIG_OPACITY),
            minerals[2].animate.set_opacity(BIG_OPACITY),
            minerals[3].animate.set_opacity(BIG_OPACITY),
            Transform(robot_counts[0], Tex(1).move_to(robot_counts[0])),
            Transform(robot_counts[1], Tex(0).move_to(robot_counts[1])),
            Transform(mineral_counts[0], Tex(r"\textbf{0}").move_to(mineral_counts[0])),
            Transform(mineral_counts[1], Tex(r"\textbf{0}").move_to(mineral_counts[1])),
        )
        minute_count = minute_count_1

        g = VGroup(minute_count, minute_text)
        q = Tex(r"\textit{Maximize geodes in 24 minutes.}").move_to(g)

        gc = g.copy()
        cp = VGroup(gc, q).arrange(buff=2).move_to(g)

        self.play(
            AnimationGroup(
                g.animate.move_to(gc),
                Write(q, run_time=1.25),
                lag_ratio=0.75,
            )
        )

        materials_array = [0, 0, 0, 0]
        robots_array = [1, 0, 0, 0]

        commands = [
            None,
            None,
            1,
            None,
            1,
            None,
            1,
            None,
            None,
            None,
            2,
            1,
            None,
            None,
            2,
            None,
            None,
            3,
            None,
            None,
            3,
            None,
            None,
            None,
        ]

        for i, command in enumerate(commands):
            minute_count_1 = Tex(r"\textbf{" + str(i + 1) + "}").scale(1.5).next_to(minute_text, RIGHT).align_to(minute_text, DOWN)
            self.play(
                FadeOut(minute_count, shift=UP * 0.65),
                FadeIn(minute_count_1, shift=UP * 0.65),
            )
            minute_count = minute_count_1

            ### allocate for factory

            if command is not None:
                animations = []

                def rot(obj, dt):
                    obj.rotate(-dt)

                gear = SVGMobject("assets/gear.svg").set_height(robot_counts[command].get_height()).next_to(robot_counts[command], RIGHT)
                gear.add_updater(rot)

                animations.append(FadeIn(gear, shift=RIGHT * 0.25))

                prev_materials_array = list(materials_array)

                if command == 0:
                    materials_array[0] -= 4
                if command == 1:
                    materials_array[0] -= 2
                if command == 2:
                    materials_array[0] -= 3
                    materials_array[1] -= 14
                if command == 3:
                    materials_array[0] -= 2
                    materials_array[2] -= 7

                for j in range(4):
                    if prev_materials_array[j] != materials_array[j]:
                        animations.append(
                            Transform(mineral_counts[j], Tex(r"\textbf{" + str(materials_array[j]) + "}").move_to(mineral_counts[j]))
                        )
                        animations.append(
                            minerals[j].animate(rate_func=there_and_back).scale(0.75),
                        )

                self.play(
                    *animations,
                    run_time=1,
                )


            ### increment resources

            for j in range(4):
                materials_array[j] += robots_array[j]
            animations = []

            for j, robot in enumerate(robots_array):
                if robot != 0:
                    animations += [
                        robots[j].animate(rate_func=ROBOT_RATE_FUNC).next_to(minerals[j], DOWN, buff=0),
                        minerals[j].animate(rate_func=MINERAL_RATE_FUNC).shift(UP * 0.08),
                        Increment(mineral_counts[j], materials_array[j], 0.08),
                    ]

            self.play(
                *animations,
                run_time=1,
            )

            animations = []
            if command is not None:
                robots_array[command] += 1

                if robots_array[command] == 1:
                    animations.append(robots[command].animate.set_opacity(1))
                    animations.append(minerals[command].animate.set_opacity(1))

                animations.append(
                    Transform(robot_counts[command], Tex(robots_array[command]).move_to(robot_counts[command])),
                )

                prev_materials_array = list(materials_array)

                self.play(
                    *animations,
                    FadeOut(gear, shift=RIGHT * 0.25),
                    Transform(robot_counts[j], Tex(robots_array[j]).move_to(robot_counts[j])),
                    run_time=1,
                )

        rect = get_fade_rect()

        self.play(
            Circumscribe(minerals[-1], color=WHITE, buff=-0.08, shape=Circle)
        )

        canhe = Tex(r"\underline{What are the states/neighbours?}").scale(1.5).move_to(self.camera.frame).set_z_index(10000000)

        self.play(
            AnimationGroup(
                FadeIn(rect),
                FadeIn(canhe),
                lag_ratio=0.5
            )
        )

        self.play(
            FadeOut(rect),
            FadeOut(canhe),
        )

        # duplicit!!!
        def vertex_from_state(state):
            text = Tex("$$" + str(state) + "$$").set_z_index(10)
            g = Group(text)

            start = 1 + len(str(state[0])) + 2
            for i in range(4):
                s = start
                e = start + len(str(state[1][i]))

                g.add(
                    minerals[i].copy().set_height(text.get_height() * 0.5).next_to(text[0][s:e], UP, buff=0.05).set_z_index(10),
                )

                start += len(str(state[1][i])) + 1

            start += 2
            for i in range(4):
                s = start
                e = start + len(str(state[2][i]))

                g.add(
                    robots[i].copy().set_height(text.get_height() * 0.5).next_to(text[0][s:e], UP, buff=0.05).set_z_index(10),
                )

                start += len(str(state[2][i])) + 1

            return g

        root = (24, (6, 41, 8, 9), (1, 4, 2, 2))

        g = vertex_from_state(root).scale(1.5)

        g.move_to(self.camera.frame)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Transform(robots[0], g[0][0]),
                    Transform(robots[0], g[1+4+0]),
                    Transform(robots[1], g[1+4+1]),
                    Transform(robots[2], g[1+4+2]),
                    Transform(robots[3], g[1+4+3]),
                    Transform(minerals[0], g[1+0]),
                    Transform(minerals[1], g[1+1]),
                    Transform(minerals[2], g[1+2]),
                    Transform(minerals[3], g[1+3]),
                    FadeTransform(mineral_counts[0], g[0][0][5]),
                    FadeTransform(mineral_counts[1], g[0][0][7:9]),
                    FadeTransform(mineral_counts[2], g[0][0][10]),
                    FadeTransform(mineral_counts[3], g[0][0][12]),
                    FadeTransform(robot_counts[0], g[0][0][16]),
                    FadeTransform(robot_counts[1], g[0][0][18]),
                    FadeTransform(robot_counts[2], g[0][0][20]),
                    FadeTransform(robot_counts[3], g[0][0][22]),
                ),
                AnimationGroup(
                    FadeIn(g[0][0][4]),
                    FadeIn(g[0][0][6]),
                    FadeIn(g[0][0][9]),
                    FadeIn(g[0][0][11]),
                    FadeIn(g[0][0][13]),
                    FadeIn(g[0][0][14]),
                    FadeIn(g[0][0][15]),
                    FadeIn(g[0][0][17]),
                    FadeIn(g[0][0][19]),
                    FadeIn(g[0][0][21]),
                    FadeIn(g[0][0][23]),
                ),
                lag_ratio=0.75
            ),
        )

        self.next_section()

        self.play(
            AnimationGroup(
                FadeOut(minute_text),
                AnimationGroup(
                    FadeTransform(minute_count[0][0], g[0][0][1]),
                    FadeTransform(minute_count[0][1], g[0][0][2]),
                    q.animate.move_to(Group(q, minute_text)),
                ),
                AnimationGroup(
                    FadeIn(g[0][0][0]),
                    FadeIn(g[0][0][3]),
                    FadeIn(g[0][0][-1]),
                ),
                lag_ratio=0.5,
            ),
        )

        self.play(
            FadeOut(q),
            FadeOut(robot_costs[:4]),  # I should probably repent
        )


        for o in self.mobjects:
            self.remove(o)

        tree, state_objects, state_bgs = actually_get_tree(25, root, 0.159)

        self.camera.frame.scale(1/1.5)
        self.camera.frame.move_to(state_objects[root])

        self.add(state_objects[root])

        ng = Group(*[state_objects[s] for s in state_objects if s != root])

        for s in state_bgs:
            self.add(state_bgs[s])

        states = [
            root,
            (25, (4, 31, 10, 11), (1, 4, 3, 2)),
            (25, (3, 45, 10, 11), (2, 4, 2, 2)),
            (25, (7, 45, 10, 11), (1, 4, 2, 2)),
            (25, (5, 45, 3, 11), (1, 4, 2, 3)),
            (25, (5, 45, 10, 11), (1, 5, 2, 2)),
        ]

        def get_edge(a, b):
            return (a, b) if (a, b) in tree.edges else (b, a)

        tree.suspend_updating()
        tree.edges[get_edge(states[0], states[3])].rotate(pi)

        robot_edges = Group(*[
            robots[0].copy().set_height(state_objects[root].get_height() * 0.8).move_to(Group(state_objects[states[0]], state_objects[states[2]])),
            robots[1].copy().set_height(state_objects[root].get_height() * 0.8).move_to(Group(state_objects[states[0]], state_objects[states[5]])),
            robots[2].copy().set_height(state_objects[root].get_height() * 0.8).move_to(Group(state_objects[states[0]], state_objects[states[1]])),
            robots[3].copy().set_height(state_objects[root].get_height() * 0.8).move_to(Group(state_objects[states[0]], state_objects[states[4]])),
        ])

        b = Tex("Branching factor").scale(3)
        f = Tex("Average number of neighbouring states.").scale(1.5).next_to(b, DOWN, buff=0.5)

        bf = VGroup(b, f).next_to(ng, LEFT, buff=3)

        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(ng).set_height(ng.get_height() * 1.3),
                AnimationGroup(
                    AnimationGroup(
                    *[Create(tree.edges[e]) for e in tree.edges],
                    FadeIn(ng),
                    ),
                    FadeIn(robot_edges),
                    lag_ratio=0.25,
                ),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(Group(ng, bf)).set_width(Group(ng, bf).get_width() * 1.25),
                FadeIn(b, run_time=1),
                lag_ratio=0.5,
            )
        )

        self.play(Write(f, run_time=1.5))

        def persistent(obj, anim=False):
            scf = self.camera.frame
            w, h = scf.get_width(), scf.get_height()

            if anim:
                return obj.animate.set_height(h * 0.06).align_to(scf, UP).align_to(scf, RIGHT).shift((LEFT + DOWN) * h * 0.1)
            else:
                return obj.set_height(h * 0.06).align_to(scf, UP).align_to(scf, RIGHT).shift((LEFT + DOWN) * h * 0.1)

        # self.play(
        #     AnimationGroup(
        #         AnimationGroup(
        #             FadeOut(f),
        #             FadeOut(ng),
        #             FadeOut(state_objects[root]),
        #             *[FadeOut(tree.edges[e]) for e in tree.edges],
        #             FadeOut(robot_edges),
        #         ),
        #         AnimationGroup(
        #             persistent(b, anim=True),
        #             *[FadeOut(state_bgs[s], run_time=0.25) for s in state_bgs],
        #         ),
        #         lag_ratio=0.5,
        #     ),
        # )


class RobotGraph(MovingCameraScene):
    @fade
    def construct(self):
        self.next_section(skip_animations=True)

        #b = Tex("Branching factor")

        #self.add(b)

        #def persistent(obj, anim=False):
        #    scf = self.camera.frame
        #    w, h = scf.get_width(), scf.get_height()

        #    if anim:
        #        return obj.animate.set_height(h * 0.06).align_to(scf, UP).align_to(scf, RIGHT).shift((LEFT + DOWN) * h * 0.1)
        #    else:
        #        return obj.set_height(h * 0.06).align_to(scf, UP).align_to(scf, RIGHT).shift((LEFT + DOWN) * h * 0.1)

        #b.add_updater(lambda x: persistent(x))

        root = (0, (0, 0, 0, 0), (1, 0, 0, 0))

        tree, state_objects, state_bgs = actually_get_tree(8, root, -pi / 4)

        self.add(state_bgs[root])

        self.play(FadeIn(state_objects[root]))

        def neighbours(vertex):
            n = []
            for a, b in tree.edges:
                if vertex == a:
                    n.append(b)
                elif vertex == b:
                    n.append(a)
            return n

        def get_neighbours(vertices):
            """Return new vertices and corresponding edges."""
            new_vertices = []
            new_edges = []

            for v in vertices:
                for neighbour in neighbours(v):
                    if neighbour not in new_vertices and neighbour not in vertices:
                        new_vertices.append(neighbour)

                        a = neighbour
                        b = v

                        new_edges.append((a, b) if (a, b) in tree.edges else (b, a))

            return new_edges, new_vertices

        vertices = [root]
        edges = []
        for i in range(7):
            new_edges, new_vertices = get_neighbours(vertices)

            animations = []
            for v in new_vertices:
                animations.append(FadeIn(state_objects[v]))

            for e in new_edges:
                animations.append(Create(tree.edges[e]))

            vertices += new_vertices
            edges += new_edges

            g = Group(*[state_objects[v] for v in vertices])

            for v in new_vertices:
                self.add(state_bgs[v])

            # offset = RIGHT * g.get_width() / 9

            self.play(
                AnimationGroup(
                    self.camera.frame.animate(run_time=1.33333).move_to(g).set_width(g.get_width() * 1.5),
                    AnimationGroup(
                        *animations,
                        run_time=0.99,
                    ),
                    lag_ratio=0.25,
                )
            )

        self.next_section()

        graph, labels = cool_graphy_graphy(15)

        g = VGroup(graph, labels).set_height(self.camera.frame.get_height() * 0.26)

        scf = self.camera.frame

        g.align_to(scf, UP).align_to(scf, RIGHT).shift((DOWN * 2) * scf.get_height() * 0.05)

        self.play(
            AnimationGroup(
                scf.animate.move_to(Group(g, *[state_objects[v] for v in vertices])),
                AnimationGroup(
                    Write(graph[1]),
                    Write(graph[2]),
                ),
                AnimationGroup(
                    FadeIn(graph[0][0]),
                    FadeIn(labels[0]),
                ),
                lag_ratio=0.5,
            ),
        )


class AStar(MovingCameraScene):
    @fade
    def construct(self):
        self.next_section(skip_animations=True)  # LEAVE THIS; same as the start of the intro

        with open("maze/mask.txt") as f:
            contents = f.read().splitlines()

        theseus = ImageMobject("assets/theseus-nobackground.png").set_height(0.8).set_z_index(100)
        theseus_position = (22, 9)
        theseus_text = Tex("Theseus").next_to(theseus, DOWN, buff=-0.08).scale(0.25)

        theseus_miniature = ImageMobject("assets/theseus-nobackground-outline.png").set_height(0.8).move_to(RIGHT * (theseus_position[0] + 0.5) + DOWN * (theseus_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT).set_z_index(1000000 + 1)

        self.camera.frame.move_to(Group(theseus, theseus_text)).set_height(theseus.height * 2)

        self.play(
            AnimationGroup(
                FadeIn(theseus),
                FadeIn(theseus_text, lag_ratio=0.1),
                lag_ratio=0.5,
            )
        )

        minotaur = ImageMobject("assets/minotaur-nobackground.png").set_height(0.8).next_to(theseus, RIGHT, buff=0.3).set_z_index(100)
        minotaur_position = (27, 9)
        minotaur_text = Tex("Minotaur").next_to(minotaur, DOWN, buff=-0.08).scale(0.25)

        minotaur_miniature = ImageMobject("assets/minotaur-nobackground-outline.png").set_height(0.8).move_to(RIGHT * (minotaur_position[0] + 0.5) + DOWN * (minotaur_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT).set_z_index(1000000 + 1)

        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(Group(theseus, minotaur)).scale(1.25),
                AnimationGroup(
                    FadeIn(minotaur),
                    FadeIn(minotaur_text, lag_ratio=0.1),
                    lag_ratio=0.5,
                ),
                lag_ratio=0.25,
            ),
        )

        maze, maze_dict = maze_to_vgroup(contents)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(theseus_text),
                    FadeOut(minotaur_text),
                ),
                AnimationGroup(
                    self.camera.frame.animate.move_to(Group(theseus_miniature, minotaur_miniature)).set_height(maze.height * 0.3),
                    FadeTransform(theseus, theseus_miniature),
                    FadeTransform(minotaur, minotaur_miniature),
                ),
                AnimationGroup(
                    FadeIn(maze),
                ),
                lag_ratio=0.5,
                run_time=2,
            )
        )

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature, minotaur_miniature.copy().shift(LEFT * 2))).scale(0.85),
            minotaur_miniature.animate.shift(LEFT * 2),
        )

        for i in range(1):
            self.play(
                self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(LEFT), minotaur_miniature.copy().shift(LEFT * 2))).scale(0.85),
                minotaur_miniature.animate.shift(LEFT * 2),
                theseus_miniature.animate.shift(LEFT),
            )

        rect = get_fade_rect()

        canhe = Tex(r"\underline{Can he get out?}").scale(1.25).next_to(Group(theseus_miniature, minotaur_miniature), UP, buff=0.25).set_z_index(10000000)

        self.play(
            AnimationGroup(
                FadeIn(rect),
                AnimationGroup(
                    self.camera.frame.animate.move_to(Group(theseus_miniature, minotaur_miniature, canhe)),
                    FadeIn(canhe, shift=UP * 0.25),
                ),
                lag_ratio=0.5
            )
        )

        self.play(
            FadeOut(rect),
            FadeOut(canhe),
            self.camera.frame.animate.move_to(Group(theseus_miniature, minotaur_miniature)),
        )

        self.play(
            Flash(minotaur_miniature, color=WHITE),
            FadeOut(minotaur_miniature),
        )

        self.play(
            self.camera.frame.animate.move_to(maze).set_height(maze.height * 1.25),
            run_time=1.5,
        )

        shortest_path = [
            (21, 9),
            (22, 9),
            (23, 9),
            (24, 9),
            (25, 9),
            (26, 9),
            (27, 9),
            (27, 10),
            (27, 11),
            (27, 12),
            (27, 13),
            (27, 14),
            (27, 15),
            (28, 15),
            (29, 15),
            (30, 15),
            (31, 15),
            (32, 15),
            (33, 15),
            (34, 15),
            (35, 15),
            (36, 15),
            (37, 15),
            (37, 16),
            (37, 17),
            (38, 17),
            (39, 17),
            (39, 16),
            (39, 15),
            (40, 15),
        ]

        theseus_miniature.set_z_index(1)

        self.play(
            AnimationGroup(*[maze_dict[p].animate.set_fill(ORANGE, 0.75).set_stroke_color(ORANGE) for p in shortest_path], lag_ratio=0.02),
        )

        self.play(
            AnimationGroup(*[maze_dict[p].animate.set_fill(WHITE, 0).set_stroke_color(WHITE) for p in shortest_path]),
        )

        bfs_text = Tex("BFS").scale(5).next_to(maze, RIGHT, buff=1.5).align_to(maze, UP).shift(DOWN)
        astar_text = Tex("A*").scale(5).move_to(bfs_text)

        q = Queue(scale=2).next_to(bfs_text, DOWN, buff=2)

        self.play(
            FadeIn(q),
            FadeIn(bfs_text),
            self.camera.frame.animate.move_to(Group(maze, theseus_miniature, q, bfs_text)),
            run_time=1,
        )

        theseus_position = (theseus_position[0] - 1, theseus_position[1])

        queue = [theseus_position]
        discovered = {theseus_position: None}

        def is_valid(position):
            x, y = position
            return 0 <= x < len(contents[0]) and 0 <= y < len(contents) and contents[y][x] != "#"

        def next_states(position):
            x, y = position
            states = []

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx = x + dx
                ny = y + dy

                if is_valid((nx, ny)):
                    states.append((nx, ny))

            return states

        def animate_discover(states):
            return AnimationGroup(*[maze_dict[p].animate.set_fill(BLUE, 0.75).set_stroke_color(BLUE) for p in states])

        def animate_leave(state):
            return maze_dict[state].animate.set_fill(LIGHT_GRAY, 0.75).set_stroke_color(LIGHT_GRAY).set_z_index(3)

        def animate_add_to_queue(states):
            fade_froms = [maze_dict[s] for s in states]
            state_texs = [Tex(s) for s in states]

            return q.animate_add_from(state_texs, fade_froms)

        def animate_pop_from_queue(state):
            copy = maze_dict[state].copy().set_fill(WHITE, 0).set_stroke_color(WHITE).set_z_index(0.05)

            return (AnimationGroup(
                q.animate_remove_to(copy),
                maze_dict[state].animate.set_fill(ORANGE, 0.75).set_stroke_color(ORANGE).set_z_index(2),
            ), copy)

        def stop_condition(state):
            return state == escape

        i = 1

        def add_neighbours(position):
            states = []
            for next_state in next_states(position):
                if next_state not in discovered:
                    discovered[next_state] = position
                    queue.append(next_state)
                    states.append(next_state)

            if len(states) != 0:
                self.play(
                    animate_leave(current),
                    animate_discover(states),
                    animate_add_to_queue(states),
                )
            else:
                self.play(
                    animate_leave(current),
                )

        def dist(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        escape = (40, 15)

        queue2 = [escape]
        discovered2 = {escape: 0}

        while len(queue2) != 0:
            current = queue2.pop(0)

            for next_state in next_states(current):
                if next_state not in discovered2:
                    discovered2[next_state] = dist(next_state, escape)
                    queue2.append(next_state)

        self.next_section()

        all_colors = color_gradient([RED, GREEN], max(discovered2.values()) + 1)

        self.play(
            AnimationGroup(
                *[AnimationGroup(*[maze_dict[p].animate(run_time=0.5).set_color(all_colors[d]).set_fill(all_colors[d], 0.75)
                                   for p in discovered2.keys()
                                   if discovered2[p] == d])
                  for d in range(0, max(discovered2.values()) + 1)],
                lag_ratio=0.045,
            )
        )

        self.play(
            Transform(bfs_text, astar_text),
        )

        self.play(
            AnimationGroup(
                *[AnimationGroup(*[maze_dict[p].animate(run_time=1, rate_func=there_and_back).set_color(all_colors[d]).set_fill(all_colors[d], 1)
                                   for p in discovered2.keys()
                                   if discovered2[p] == d])
                  for d in range(0, max(discovered2.values()) + 1)],
                lag_ratio=0.025,
            )
        )

        self.play(
            *[maze_dict[k].animate.set_fill(WHITE, 0).set_stroke_color(WHITE)
              for k in discovered2],
        )

        self.play(
            animate_discover([theseus_position]),
            animate_add_to_queue([theseus_position]),
        )

        return


class PlotTest(MovingCameraScene):
    @fade
    def construct(self):
        #max_y = int(open("programs/graphs/results/bfs.txt").read().splitlines()[-1].split()[1])

        #ax = Axes(
        #    x_range=[10, 24],
        #    y_range=[0, max_y],
        #    tips=False,
        #    axis_config={"include_numbers": False, "include_ticks": False},
        #)

        #graphs = VGroup()

        #for f, color in [
        #    ("programs/graphs/results/bfs.txt", RED),
        #    ("programs/graphs/results/bfs-wtb.txt", ORANGE),
        #    ("programs/graphs/results/bfs-wtb-max-prune.txt", BLUE),
        #]:
        #    with open(f) as fd:
        #        contents = fd.read().splitlines()

        #    graphs.add(ax.plot_line_graph(
        #        x_values = [int(row.split()[0]) for row in contents],
        #        y_values = [int(row.split()[1]) for row in contents],
        #        line_color=color,
        #    ))

        #self.play(
        #    Create(ax),
        #    Create(graphs),
        #)

        graph, labels = cool_graphy_graphy(10)

        self.play(
            AnimationGroup(
                FadeIn(graph[0][0]),
                FadeIn(graph[1]),
                FadeIn(graph[2]),
                FadeIn(labels[0]),
                lag_ratio=0.5,
            )
        )

        for i in range(1, 4):
            self.play(
                FadeIn(graph[0][i]),
                FadeIn(labels[i]),
            )
