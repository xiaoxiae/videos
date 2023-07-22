import glob

import open3d as o3d
from manim import *
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLCamera
from pyglet.window import key

from utilities import ColmapObject


class TestCameraScene(Scene):
    def construct(self):
        s = Sphere(resolution=5).shift(LEFT * 2)
        c = Cube().shift(RIGHT * 2)

        self.add(s, c)

        cam2 = OpenGLCamera(euler_angles=[PI, PI, PI], focal_distance=5)

        ## moving objects
        # self.play(
        #    square.animate.shift(UP * 0.5),
        #    circle.animate.shift(DOWN * 0.5)
        # )

        ## rotating and filling the square (opacity 80%)
        ## scaling and filling the circle (opacity 80%)
        # self.play(
        #    square.animate.rotate(PI / 2).set_fill(RED, 0.8),
        #    circle.animate.scale(2).set_fill(BLUE, 0.8),
        # )

        # self.camera_states = []

        self.interactive_embed()

    def on_key_press(self, symbol, modifiers):
        # + adds a new camera position to interpolate
        if symbol == key.PLUS:
            print("New position added!")
            self.camera_states.append(
                (
                    self.camera.get_center(),
                    np.array(self.camera.euler_angles),
                )
            )

        # P plays the animations, one by one
        elif symbol == key.P:
            print("Replaying!")
            for pos, ang in self.camera_states:
                print(pos)
                self.play(
                    self.camera.animate.move_to(ORIGIN).set_euler_angles(*ang).move_to(pos)
                )

        super().on_key_press(symbol, modifiers)


class TestPyColmapScene(Scene):
    def construct(self):
        colmap = ColmapObject(
            "assets/test/sparse/0",
            [
                np.array([5.95773, 2.50781, 8.62867]),
                np.array([3.70964, 3.14088, 7.81675]),
                np.array([2.82718, 0.187449, 11.3918]),
            ],
        )

        self.add(colmap)

        self.interactive_embed()


class TestPCDScene(Scene):
    def construct(self):
        pointcloud = OpenGLPMobject()

        pcd = o3d.io.read_point_cloud("assets/sparse-test.pcd")
        _, pcd = pcd.remove.remove_statistical_outlier()

        points = [p for p in pcd.points]

        pointcloud.add_points(points)

        # scale + color
        pointcloud.set_color_by_gradient((RED, GREEN, BLUE))

        self.play(Create(pointcloud))

        self.interactive_embed()


class TestFocusCameraScene(Scene):
    def construct(self):
        colmap = ColmapObject(
            "assets/test/sparse/0",
            [
                np.array([5.95773, 2.50781, 8.62867]),
                np.array([3.70964, 3.14088, 7.81675]),
                np.array([2.82718, 0.187449, 11.3918]),
            ],
        )

        cam = list(colmap.cameras.values())[0]

        for c in colmap.cameras.values():
            self.add(c)

        self.camera.move_to(cam.image)
        self.camera.set_height(self.camera.get_focal_distance())

        a, b, c = cam.scipy_rotmat.as_euler('zxz')
        self.camera.set_euler_angles(c, b, a)

        self.interactive_embed()


class SIFT(Scene):

    def on_key_press(self, symbol, modifiers):
        if symbol == key.NUM_0:
            self.highlight_scale([0, 1])
        if symbol == key.NUM_1:
            self.highlight_scale([1, 2])
        if symbol == key.NUM_2:
            self.highlight_scale([2, 3])
        if symbol == key.NUM_3:
            self.highlight_scale([3, 4])
        if symbol == key.NUM_4:
            self.highlight_scale([4, 5])
        if symbol == key.NUM_5:
            self.play(
                self.current_scale.animate.restore(),
                self.current_dog.animate.restore(),
            )

            self.current_scale.save_state()
            self.current_dog.save_state()

        super().on_key_press(symbol, modifiers)

    def highlight_scale(self, indexes):
        self.play(
            *[
                AnimationGroup(
                    self.current_scale[j][0].animate.set_opacity(0.15),
                    self.current_scale[j][1].animate.set_style(fill_opacity=0, stroke_opacity=0.15),
                )
                for j in range(len(self.current_scale))
                if j not in indexes
            ],
            *[
                AnimationGroup(
                    self.current_dog[j][0].animate.set_opacity(0.15),
                    self.current_dog[j][1].animate.set_style(fill_opacity=0, stroke_opacity=0.15),
                )
                for j in range(len(self.current_dog))
                if j != indexes[0]
            ],
        )

    def create_image_stack(self, paths):
        w, _ = Image.open(paths[0]).size

        scale = OpenGLGroup(*[OpenGLGroup(OpenGLImageMobject(p).set_width(w / 1000)) for p in reversed(paths)]).arrange(
            OUT, buff=0.5)

        for s in scale:
            s.add(SurroundingRectangle(s[0], color=WHITE, buff=0))

        scale.save_state()

        return scale

    def construct(self):
        self.input = OpenGLImageMobject("assets/gaussian/input.png")

        self.gaussian_paths = [
            sorted(glob.glob(folder + "/*"))
            for folder in sorted(glob.glob("assets/gaussian/gaussians/*"))
        ]

        self.dog_paths = [
            sorted(glob.glob(folder + "/*"))
            for folder in sorted(glob.glob("assets/gaussian/dogs/*"))
        ]

        self.gaussian_scales = [
            self.create_image_stack(self.gaussian_paths[0])
        ]

        self.dogs = [
            self.create_image_stack(self.dog_paths[0]).next_to(self.gaussian_scales[0], RIGHT, buff=1)
        ]

        self.current_scale = self.gaussian_scales[0]
        self.current_dog = self.dogs[0]

        self.current_scale.save_state()
        self.current_dog.save_state()

        self.add(self.current_scale)
        self.add(self.current_dog)


        #a = self.gaussian_scales[0][-1].copy().shift(IN * 0.01)
        #b = self.gaussian_scales[0][-2].copy().shift(IN * 0.01)

        #self.play(
        #    b.animate.next_to(self.gaussian_scales[0][-2], RIGHT, buff=1),
        #    a.animate.next_to(self.gaussian_scales[0][-1], RIGHT, buff=1),
        #)

        #self.play(
        #    a.animate(run_time=0.75).move_to(self.dogs[0][-1]).shift(IN * 0.01),
        #    b.animate(run_time=0.75).move_to(self.dogs[0][-1]).shift(IN * 0.01),
        #    Succession(
        #        Wait(0.6),
        #        FadeIn(self.dogs[0][-1], run_time=0.3),
        #    )
        #)

        self.interactive_embed()
