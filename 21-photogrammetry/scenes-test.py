from random import uniform

from manim import *
from manim.opengl import *

from pyglet.window import key
from scipy.spatial import ConvexHull


class CameraScene(Scene):
    def construct(self):
        square = Square(color=RED).shift(LEFT * 2)
        circle = Circle(color=BLUE).shift(RIGHT * 2)

        self.play(Write(square), Write(circle))

        # moving objects
        self.play(
            square.animate.shift(UP * 0.5),
            circle.animate.shift(DOWN * 0.5)
        )

        # rotating and filling the square (opacity 80%)
        # scaling and filling the circle (opacity 80%)
        self.play(
            square.animate.rotate(PI / 2).set_fill(RED, 0.8),
            circle.animate.scale(2).set_fill(BLUE, 0.8),
        )

        self.camera_states = []

        self.interactive_embed()

    def on_key_press(self, symbol, modifiers):
        # + adds a new camera position to interpolate
        if symbol == key.PLUS:
            print("New position added!")
            self.camera_states.append(self.camera.copy())

        # P plays the animations, one by one
        elif symbol == key.P:
            print("Replaying!")
            for cam in self.camera_states:
                self.play(self.camera.animate.become(cam))

        OpenGLSurfaceMesh

        super().on_key_press(symbol, modifiers)


class PolyhedronScene(Scene):
    def construct(self):
        octahedron = Octahedron(edge_length = 3)
        octahedron.graph[0].set_color(RED)
        octahedron.faces[2].set_color(YELLOW)
        self.add(octahedron)

        self.interactive_embed()
