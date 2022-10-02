from manim import *
from utilities import *


class Intro(MovingCameraScene):
    def construct(self):
        with open("maze/mask.txt") as f:
            contents = f.read().splitlines()

        theseus = ImageMobject("assets/theseus-nobackground.png").set_height(0.8)
        theseus_position = (23, 9)
        theseus_text = Tex("Theseus").next_to(theseus, DOWN, buff=-0.08).scale(0.25)

        theseus_miniature = Tex("\\textbf{T}", color=BLUE).set_height(theseus.height * 0.65).move_to(RIGHT * (theseus_position[0] + 0.5) + DOWN * (theseus_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT)

        self.camera.frame.move_to(Group(theseus, theseus_text)).set_height(theseus.height * 2),

        self.play(
            AnimationGroup(
                FadeIn(theseus),
                FadeIn(theseus_text, lag_ratio=0.1),
                lag_ratio=0.5,
            )
        )

        minotaur = ImageMobject("assets/minotaur-nobackground.png").set_height(0.8).next_to(theseus, RIGHT, buff=0.3)
        minotaur_position = (30, 9)
        minotaur_text = Tex("Minotaur").next_to(minotaur, DOWN, buff=-0.08).scale(0.25)

        minotaur_miniature = Tex("\\textbf{M}", color=RED).set_height(minotaur.height * 0.65).move_to(RIGHT * (minotaur_position[0] + 0.5) + DOWN * (minotaur_position[1] + 0.5) + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT)

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
                else:
                    r = Rectangle(width=1.0, height=1.0)

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

        for i in range(2):
            self.play(
                self.camera.frame.animate.move_to(Group(theseus_miniature.copy().shift(LEFT), minotaur_miniature.copy().shift(LEFT * 2))).scale(0.85),
                minotaur_miniature.animate.shift(LEFT * 2),
                theseus_miniature.animate.shift(LEFT),
            )

        # TODO: can he get out text

        self.play(
            Flash(minotaur_miniature, color=RED),
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
            theseus_miniature.animate.set_color(WHITE),
            AnimationGroup(*[maze_dict[p].animate.set_fill(BLUE, 0.75).set_stroke_color(BLUE) for p in shortest_path], lag_ratio=0.02),
        )

        self.play(
            theseus_miniature.animate.set_color(BLUE),
            AnimationGroup(*[maze_dict[p].animate.set_fill(WHITE, 0).set_stroke_color(WHITE) for p in shortest_path]),
        )

        #new_maze = maze.copy().rotate(PI/2, about_point=theseus_miniature.get_center())

        #bfs_text = Tex("Breadth-First Search").scale(5).next_to(new_maze, RIGHT, buff=15).align_to(new_maze, UP)

        #q = Queue(scale=3).next_to(new_maze, RIGHT, buff=3).align_to(new_maze, UP)

        #self.add(q)
        #self.add(bfs_text)

        #self.play(
        #    Rotate(maze, PI / 2, about_point=theseus_miniature.get_center()),
        #    self.camera.frame.animate.move_to(VGroup(new_maze, q, bfs_text)).set_height(new_maze.height * 1.35),
        #    #run_time=1.5,
        #    run_time=0.01,
        #)

        #self.wait(1)

        bfs_text = Tex("BFS").scale(5).next_to(maze, RIGHT, buff=3).align_to(maze, UP)

        q = Queue(scale=3).next_to(bfs_text, DOWN, buff=2)

        self.add(q)
        self.add(bfs_text)

        self.play(
            #self.camera.frame.animate.move_to(VGroup(theseus_miniature, q, bfs_text)).set_height(maze.height * 1.25),
            self.camera.frame.animate.shift(RIGHT * 15),
            #run_time=1.5,
            run_time=0.01,
        )

        self.wait(1)


class QueueTest(MovingCameraScene):
    def construct(self):
        q = Queue()

        c = Circle().shift(LEFT + UP).scale(0.5)

        self.play(Write(q))

        self.play(q.animate_add(c))


        c = Circle().shift(RIGHT).scale(0.7)

        self.play(q.animate_add(c))

        self.play(q.animate_remove(LEFT * 5))


class CodeTest(MovingCameraScene):
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

        self.play(
            Write(blocks['start'].code[12:14]),
            run_time=1,
        )

        self.play(
            Write(blocks['start'].code[15:22]),
            run_time=1.5,
        )

        self.play(
            AnimationGroup(
                FadeCode(blocks['start'], skip_lines=[22]),
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

        self.play(FadeOut(highlight))

        highlight = CreateHighlightCodeLine(blocks["bfs"], 14, start=4)

        blocks["bfs_mid"].code[14].move_to(blocks["bfs"].code[14]).align_to(blocks["bfs"].code[14], LEFT)

        self.play(FadeIn(highlight))

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Transform(highlight, CreateHighlightCodeLine(blocks["bfs_mid"], 14, start=4)),
                    FadeTransform(blocks["bfs"].code[14][14:19], blocks["bfs_mid"].code[14][14]),
                    FadeTransform(blocks["bfs"].code[14][19:19+7], blocks["bfs_mid"].code[14][-7:1000]),
                    FadeTransform(blocks["bfs"].code[14][-1], blocks["bfs_mid"].code[14][25]),
                    Transform(blocks["bfs"].background_mobject, blocks["bfs_mid"].background_mobject)
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
        blocks["start"].code[-1].set_opacity(0)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeTransform(blocks["bfs_mid"].background_mobject, blocks["bfs_better"].background_mobject),
                    FadeTransform(blocks["bfs_mid"].code[9:], blocks["bfs_better"].code[20:]),
                    self.camera.frame.animate.move_to(blocks["bfs_better"]).set_height(blocks["bfs_better"].height * 1.2),
                ),
                FadeIn(blocks["bfs_better"].code[9:20]),
                lag_ratio=0.5,
            )
        )

        # TODO: highlights

        self.remove(blocks["bfs_mid"])
        self.add(blocks["bfs_better"])

        self.play(
            AnimationGroup(
                FadeCode(blocks['bfs_better']),
                self.camera.frame.animate.move_to(start_group),
                UnfadeCode(blocks['start'], skip_lines=[22]),
                lag_ratio=0.5,
            )
        )

        self.play(Write(blocks['start'].code[22]), run_time=1)

        highlight = CreateHighlightCodeLine(blocks['start'], 22, 4, 11)

        self.play(FadeIn(highlight))
        self.play(Transform(highlight, CreateHighlightCodeLine(blocks['start'], 22, 13, -1)))
        self.play(FadeOut(highlight))

        self.play(
            code_web.animate.set_opacity(1),
            self.camera.frame.animate.move_to(code_web).set_height(code_web.height * 1.2),
        )
