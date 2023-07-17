import open3d as o3d
import scipy
import pycolmap
from manim import *
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLCamera
from pyglet.window import key


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


class TestCameraScene(Scene):
    def construct(self):
        s = Sphere(resolution=5).shift(LEFT * 2)
        c = Cube().shift(RIGHT * 2)

        self.add(s, c)

        cam2 = OpenGLCamera(euler_angles=[PI, PI, PI], focal_distance=5)

        ## moving objects
        #self.play(
        #    square.animate.shift(UP * 0.5),
        #    circle.animate.shift(DOWN * 0.5)
        #)

        ## rotating and filling the square (opacity 80%)
        ## scaling and filling the circle (opacity 80%)
        #self.play(
        #    square.animate.rotate(PI / 2).set_fill(RED, 0.8),
        #    circle.animate.scale(2).set_fill(BLUE, 0.8),
        #)

        #self.camera_states = []

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


class ColmapCameraObject(OpenGLGroup):
    def __init__(self, image: pycolmap.Image, project: pycolmap.Reconstruction, image_path, *args,
                 image_border_lines_stroke_width=1, line_resolution=5,
                 camera_lines_stroke_width=1, camera_dot_resolution=10,
                 camera_scale=1,
                 no_image=False,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.pycolmap_image = image
        self.pycolmap_camera = project.cameras[self.pycolmap_image.camera_id]

        w, h = np.abs(self.pycolmap_camera.image_to_world([0, 0]) * camera_scale * 2)

        center = image.projection_center()
        dist = image.transform_to_world([0, 0, camera_scale])

        d = np.linalg.norm(center - dist)

        self.image = OpenGLImageMobject(image_path / image.name) \
            .stretch_to_fit_width(w) \
            .stretch_to_fit_height(h)

        self.camera_dot = Dot3D(color=WHITE, radius=w * 0.05, resolution=camera_dot_resolution).shift(OUT * d)

        w /= 2
        h /= 2

        self.image_border_lines = OpenGLVGroup(
            Line3D(
                start=np.array([-w, -h, 0]), end=np.array([w, -h, 0]),
                color=WHITE, stroke_width=[image_border_lines_stroke_width],
                resolution=line_resolution,
            ),
            Line3D(
                start=np.array([-w, -h, 0]), end=np.array([-w, h, 0]),
                color=WHITE, stroke_width=[image_border_lines_stroke_width],
                resolution=line_resolution,
            ),
            Line3D(
                start=np.array([-w, h, 0]), end=np.array([w, h, 0]),
                color=WHITE, stroke_width=[image_border_lines_stroke_width],
                resolution=line_resolution,
            ),
            Line3D(
                start=np.array([w, -h, 0]), end=np.array([w, h, 0]),
                color=WHITE, stroke_width=[image_border_lines_stroke_width],
                resolution=line_resolution,
            ),
        )

        self.camera_lines = OpenGLVGroup(
            Line3D(
                start=self.camera_dot.get_center(),
                end=np.array([w, h, 0]),
                color=WHITE, stroke_width=[camera_lines_stroke_width],
                resolution=line_resolution,
            ),
            Line3D(
                start=self.camera_dot.get_center(),
                end=np.array([w, -h, 0]),
                color=WHITE, stroke_width=[camera_lines_stroke_width],
                resolution=line_resolution,
            ),
            Line3D(
                start=self.camera_dot.get_center(),
                end=np.array([-w, h, 0]),
                color=WHITE, stroke_width=[camera_lines_stroke_width],
                resolution=line_resolution,
            ),
            Line3D(
                start=self.camera_dot.get_center(),
                end=np.array([-w, -h, 0]),
                color=WHITE, stroke_width=[camera_lines_stroke_width],
                resolution=line_resolution,
            ),
        )

        if not no_image:
            self.add(self.image)

        self.add(self.camera_dot, self.camera_lines, self.image_border_lines)

        self.shift(center - self.camera_dot.get_center())

        self.scipy_rotmat = scipy.spatial.transform.Rotation.from_matrix(image.rotmat()).inv()
        self.euler_angles = self.scipy_rotmat.as_euler('xyz')

        self.rotate(self.euler_angles[0], axis=RIGHT, about_point=self.camera_dot.get_center())
        self.rotate(self.euler_angles[1], axis=UP, about_point=self.camera_dot.get_center())
        self.rotate(self.euler_angles[2], axis=OUT, about_point=self.camera_dot.get_center())
        self.scale(-1)


class TestPyColmapScene(Scene):
    def construct(self):
        project = pycolmap.Reconstruction("assets/test/sparse/0")

        orient_points = [
            np.array([5.95773, 2.50781, 8.62867]),
            np.array([3.70964, 3.14088, 7.81675]),
            np.array([2.82718, 0.187449, 11.3918]),
        ]

        # origin and axis of the centering
        avg = np.average(orient_points, axis=0)
        vec = np.cross(orient_points[0] - orient_points[1], orient_points[0] - orient_points[2])

        desired_vec = IN

        axis_vec = np.cross(vec, desired_vec)
        axis_angle = angle_between(vec, desired_vec)

        #self.camera.to_default_state()
        #self.camera.scale(2)

        # translate first
        project.transform(np.array([
            [1, 0, 0, -avg[0]],
            [0, 1, 0, -avg[1]],
            [0, 0, 1, -avg[2]],
        ]))

        # then rotate
        project.transform(
            np.concatenate(
                (
                    scipy.spatial.transform.Rotation.from_rotvec(
                        axis_vec / np.linalg.norm(axis_vec) * axis_angle
                    ).as_matrix(),
                    np.array([[0], [0], [0]]),
                ),
                axis=1
            )
        )

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(np.array([p.xyz for p in project.points3D.values()]))
        pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=10, std_ratio=0.4)

        pointcloud = OpenGLPMobject()
        pointcloud.add_points(pcd.points)
        # pointcloud.rotate(axis_angle, axis=axis_vec, about_point=avg)
        # pointcloud.scale(0.75, about_point=avg)

        self.add(pointcloud)

        for image_id in project.images:
            cam = ColmapCameraObject(project.images[image_id], project, Path("assets/test/images"), no_image=False)
            self.add(cam)

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
