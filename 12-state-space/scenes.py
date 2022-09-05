from manim import *


class Intro(MovingCameraScene):
    def construct(self):
        image = ImageMobject("assets/theseus-nobackground.png").set_height(1)

        self.camera.frame.move_to(image).set_height(image.height * 2),

        self.play(FadeIn(image))

        with open("maze/mask.txt") as f:
            contents = f.read().splitlines()

        maze = VGroup()

        for y, row in enumerate(contents):
            for x, symbol in enumerate(row):
                if symbol == "#":
                    r = Rectangle(width=1.0, height=1.0, fill_opacity=1, fill_color=WHITE)
                else:
                    r = Rectangle(width=1.0, height=1.0)

                r.move_to(y * DOWN + x * RIGHT + len(contents) / 2 * UP + len(contents[0]) / 2 * LEFT)
                maze.add(r)

        self.add(maze)

        self.wait(1)

        self.play(
            self.camera.frame.animate.set_height(maze.height * 1.3),
        )
