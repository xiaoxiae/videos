import open3d as o3d
import pycolmap
import scipy
from manim import *
from manim.opengl import *


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


class ColmapCameraObject(OpenGLMobject):
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

        #self.scale(-1)


class ColmapObject(OpenGLGroup):
    def __init__(self, path: str, orientation_points: list[np.ndarray], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.project = pycolmap.Reconstruction(path)

        # origin and axis of the centering
        avg = np.average(orientation_points, axis=0)
        vec = np.cross(orientation_points[0] - orientation_points[1], orientation_points[0] - orientation_points[2])

        desired_vec = IN

        axis_vec = np.cross(vec, desired_vec)
        axis_angle = angle_between(vec, desired_vec)

        # translate first
        self.project.transform(np.array([
            [1, 0, 0, -avg[0]],
            [0, 1, 0, -avg[1]],
            [0, 0, 1, -avg[2]],
        ]))

        # then rotate
        self.project.transform(
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
        pcd.points = o3d.utility.Vector3dVector(np.array([p.xyz for p in self.project.points3D.values()]))
        pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=10, std_ratio=0.4)

        self.pointcloud = OpenGLPMobject()
        self.pointcloud.add_points(pcd.points)
        self.pointcloud.set_color(WHITE)

        self.add(self.pointcloud)

        self.cameras = {}
        for image_id in self.project.images:
            cam = ColmapCameraObject(self.project.images[image_id], self.project, Path("assets/test/images"))
            self.cameras[image_id] = cam
            self.add(cam)
