from manim import *
from utilities import *


class MinotaurMovement(MovingCameraScene):
    def construct(self):
        self.next_section(skip_animations=True)  # this is correct

        with open("maze/mask.txt") as f:
            contents = f.read().splitlines()

        theseus = ImageMobject("assets/theseus-nobackground.png").set_height(0.8).set_z_index(100)
        theseus_position = (22, 9)
        theseus_text = Tex("Theseus").next_to(theseus, DOWN, buff=-0.08).scale(0.25)

        #theseus_miniature = Tex("\\textbf{T}", color=BLUE).set_height(theseus.height * 0.65).move_to(RIGHT * (theseus_position[0] + 0.5) + DOWN * (theseus_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT)
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

        #minotaur_miniature = Tex("\\textbf{M}", color=RED).set_height(minotaur.height * 0.65).move_to(RIGHT * (minotaur_position[0] + 0.5) + DOWN * (minotaur_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT)
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

        maze = VGroup()
        maze_dict = {}

        for y, row in enumerate(contents):
            for x, symbol in enumerate(row):
                if symbol == "#":
                    r = Rectangle(width=1.0, height=1.0, fill_opacity=1, fill_color=WHITE)
                    r.set_z_index(10000)
                elif symbol == ".":
                    continue
                else:
                    r = Rectangle(width=1.0, height=1.0)
                    r.set_z_index(0.1)


                r.move_to((y + 0.5) * DOWN + (x + 0.5) * RIGHT + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT)
                maze.add(r)
                maze_dict[(x, y)] = r

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
            run_time=1.5,
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
                run_time=1.5,
            )

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(RIGHT), minotaur_miniature)),
            theseus_miniature.animate.shift(RIGHT),
        )

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy(), minotaur_miniature.copy().shift(RIGHT))),
            minotaur_miniature.animate.shift(RIGHT),
        )

        self.play(
            minotaur_miniature.animate.shift(DOWN * 0.1),
            rate_func=there_and_back,
            run_time=0.8
        )

        # 

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

        #

        self.play(
            self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(RIGHT), minotaur_miniature)),
            theseus_miniature.animate.shift(RIGHT),
        )

        self.play(
            minotaur_miniature.animate.shift(RIGHT * 0.1),
            rate_func=there_and_back,
            run_time=0.8
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

        rect = get_fade_rect()
        self.play(
            Transform(theseus_miniature, tm),
            minotaur_miniature.animate.shift(RIGHT),
            self.camera.frame.animate.scale(0.5),
            run_time=1.5,
        )

        self.play(
            Flash(minotaur_miniature, color=WHITE),
            FadeOut(minotaur_miniature),
        )

        buff=-0.14

        f1 = Circle(color=YELLOW).surround(theseus_miniature, buffer_factor=1)
        radius = f1.width / 2
        f1.scale((radius + buff) / radius)

        self.play(Create(f1))
        self.play(FadeOut(f1))

        self.play(FadeIn(minotaur_miniature))

        f2 = Circle(color=YELLOW).surround(minotaur_miniature, buffer_factor=1)

        radius = f2.width / 2
        f2.scale((radius + buff) / radius)

        self.play(Create(f1))

        self.play(Create(f2))

        self.play(
            FadeOut(f1),
            FadeOut(f2),
        )


class Intro(MovingCameraScene):
    @fade
    def construct(self):
        self.next_section(skip_animations=True)

        with open("maze/mask.txt") as f:
            contents = f.read().splitlines()

        theseus = ImageMobject("assets/theseus-nobackground.png").set_height(0.8).set_z_index(100)
        theseus_position = (22, 9)
        theseus_text = Tex("Theseus").next_to(theseus, DOWN, buff=-0.08).scale(0.25)

        #theseus_miniature = Tex("\\textbf{T}", color=BLUE).set_height(theseus.height * 0.65).move_to(RIGHT * (theseus_position[0] + 0.5) + DOWN * (theseus_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT)
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

        #minotaur_miniature = Tex("\\textbf{M}", color=RED).set_height(minotaur.height * 0.65).move_to(RIGHT * (minotaur_position[0] + 0.5) + DOWN * (minotaur_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT)
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

        maze = VGroup()
        maze_dict = {}

        for y, row in enumerate(contents):
            for x, symbol in enumerate(row):
                if symbol == "#":
                    r = Rectangle(width=1.0, height=1.0, fill_opacity=1, fill_color=WHITE)
                    r.set_z_index(10000)
                elif symbol == ".":
                    continue
                else:
                    r = Rectangle(width=1.0, height=1.0)
                    r.set_z_index(0.1)


                r.move_to((y + 0.5) * DOWN + (x + 0.5) * RIGHT + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT)
                maze.add(r)
                maze_dict[(x, y)] = r

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

        rect = get_fade_rect()

        canhe = Tex("Can he get out?").scale(1.5).move_to(self.camera.frame).set_z_index(10000000)

        self.play(
            AnimationGroup(
                FadeIn(rect),
                Write(canhe),
                lag_ratio=0.5
            )
        )

        self.play(
            FadeOut(rect),
            FadeOut(canhe),
        )

        self.play(
            Flash(minotaur_miniature, color=WHITE),
            FadeOut(minotaur_miniature),
        )

        self.play(
            self.camera.frame.animate.move_to(maze).set_height(maze.height * 1.25),
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
            #theseus_miniature.animate.set_color(WHITE),
            AnimationGroup(*[maze_dict[p].animate.set_fill(ORANGE, 0.75).set_stroke_color(ORANGE) for p in shortest_path], lag_ratio=0.02),
        )

        self.play(
            #theseus_miniature.animate.set_color(BLUE),
            AnimationGroup(*[maze_dict[p].animate.set_fill(WHITE, 0).set_stroke_color(WHITE) for p in shortest_path]),
        )

        bfs_text = Tex("BFS").scale(5).next_to(maze, RIGHT, buff=1.5).align_to(maze, UP).shift(DOWN)

        q = Queue(scale=2).next_to(bfs_text, DOWN, buff=2)

        self.next_section()

        self.play(
            FadeIn(q),
            FadeIn(bfs_text),
            self.camera.frame.animate.move_to(Group(maze, theseus_miniature, q, bfs_text)),
            #self.camera.frame.animate.shift(RIGHT * 7.5),
            run_time=1.5,
        )

        self.play(
            Circumscribe(q, stroke_width=15, buff=0.5),
        )

        return

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
                    animate_discover(states),
                    animate_add_to_queue(states),
                )

        self.play(
            #theseus_miniature.animate.set_color(WHITE),
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

        while len(queue) != 0:
            current = queue.pop(0)

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

                self.play(
                    AnimationGroup(
                        *[maze_dict[p].animate.set_fill(ORANGE, 0.75).set_stroke_color(ORANGE) for p in reversed(path)],
                        lag_ratio=0.02
                    ),
                )

                break

            add_neighbours(current)

            self.play(animate_leave(current))


class BFSMinotaur(MovingCameraScene):
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
                    blocks["bfs_better"],
                ]
            ],
        )

        start_group = VGroup(bfs, blocks['start'].background_mobject)

        blocks["output"].align_to(blocks["start"], RIGHT)

        self.camera.frame.move_to(blocks["bfs_better"]).set_height(blocks["bfs_better"].height * 1.2)

        self.add(*code_web)

        self.play(
            FadeCode(blocks["start"]),
            FadeCode(blocks["output"]),
            FadeCode(blocks["is_valid"]),
            FadeCode(blocks["next_states"]),
        )

        self.wait(1)

        self.play(
            AnimationGroup(
                FadeCode(blocks['bfs_better']),
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

        self.play(
            FadeIn(blocks_minotaur["start_partial"]),
            Flash(blocks_minotaur["start_partial"].code[4][8]),
        )

        blocks_minotaur["start_partial_2"].move_to(blocks_minotaur["start_partial"]).align_to(blocks_minotaur["start_partial"], UP)

        # TODO: hackish
        for mobject in self.mobjects:
            self.remove(mobject)

        # TODO: globally: fadetramsforms in code to just transforms to remove the weird fading effect (where applicable)
        # TODO: globally: write the code that currently fades in to visually distinguish it?
        # TODO: globally: tiny pauses between theseus and minotaur movements (0.5s?)

        self.add(blocks["is_valid"])
        self.add(blocks["next_states"])
        self.add(bfs)
        self.add(blocks["bfs_better"])
        self.add(blocks["output"])

        # TODO: shit fading

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeTransform(blocks_minotaur["start_partial"].background_mobject, blocks_minotaur["start_partial_2"].background_mobject),
                    Transform(blocks_minotaur["start_partial"].code[:14], blocks_minotaur["start_partial_2"].code[:14]),
                    Transform(blocks_minotaur["start_partial"].code[14:21], blocks_minotaur["start_partial_2"].code[15:22]),
                    Transform(blocks_minotaur["start_partial"].code[21:], blocks_minotaur["start_partial_2"].code[24:]),
                    self.camera.frame.animate.move_to(blocks_minotaur["start_partial_2"]).set_height(blocks_minotaur["start_partial_2"].height * 1.2),
                    blocks["output"].animate.align_to(blocks_minotaur["output"], UP)
                ),
                AnimationGroup(
                    Write(blocks_minotaur["start_partial_2"].code[14]),
                    Write(blocks_minotaur["start_partial_2"].code[22:24]),
                    run_time=1,
                ),
                lag_ratio=0.75,
            )
        )

class BFS(MovingCameraScene):
    def construct(self):
        self.next_section(skip_animations=True)
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

        self.next_section()

        self.play(
            Write(blocks['start'].code[15:22]),
            run_time=2.5,
        )

        question = Tex(r"\underline{What now?}").set_z_index(1000001).move_to(self.camera.frame).scale(2)
        answer = Tex(r"write smaller functions!").set_z_index(1000001).move_to(self.camera.frame).scale(1.25)

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
                Write(group[1], run_time=1),
                lag_ratio=0.75
            )
        )

        return

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
        self.play(FadeOut(highlight))

        self.play(Write(blocks['bfs'].code[1]), run_time=1)
        self.play(Write(blocks['bfs'].code[2]), run_time=1)

        self.play(Write(blocks['bfs'].code[4]), run_time=1)
        self.play(Write(blocks['bfs'].code[5]), run_time=1)

        self.play(Write(blocks['bfs'].code[7:10]), run_time=2.25)

        self.play(Write(blocks['bfs'].code[11:16]), run_time=3)

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
        self.play(Transform(highlight, CreateHighlightCodeLines(blocks["bfs_better"], [12, 13], offset=4)))
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
                self.camera.frame.animate.move_to(start_group),
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

        self.play(
            AnimationGroup(
                FadeCode(blocks['start']),
                self.camera.frame.animate.move_to(blocks['output']),
                WriteCode(blocks['output']),
                lag_ratio=0.5,
            )
        )

        self.play(
            UnfadeCode(blocks['start']),
            UnfadeCode(blocks['bfs_better']),
            UnfadeCode(blocks['is_valid']),
            UnfadeCode(blocks['next_states']),
            self.camera.frame.animate.move_to(VGroup(code_web,blocks['bfs_better'])).set_height(VGroup(code_web,blocks['bfs_better']).height * 1.2),
        )

        # TODO:
