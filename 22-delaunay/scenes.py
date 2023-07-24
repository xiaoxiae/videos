from random import uniform

from manim import *
from scipy.spatial import Delaunay


class TransparentScene(MovingCameraScene):
    def construct(self):
        images = 10

        for _ in range(images):
            w = self.camera.frame.width * 1.25
            h = self.camera.frame.height * 1.25

            n = 30
            k = 4
            points = []
            for _ in range(n):
                def min_dist_to_other_points(p):
                    min_dist = float('inf')
                    for q in points:
                        min_dist = min(min_dist, np.linalg.norm(np.array(p) - np.array(q)))
                    return min_dist

                sampled_points = [
                    (uniform(-w / 2, w / 2), uniform(-h / 2, h / 2))
                    for _ in range(k)
                ]

                sampled_points.sort(key=min_dist_to_other_points)

                points.append(sampled_points[-1])

            tri = Delaunay(points)

            edges = []
            for s in tri.simplices:
                for i in range(3):
                    edges.append((points[s[i - 1]], points[s[i]]))

            graph = Graph(
                vertices=points,
                edges=edges,
                layout={p: (*p, 0) for p in points},
            )

            for v in graph.vertices:
                graph[v].scale(2.5)

            self.add(graph)
            self.wait()
            for o in self.mobjects:
                self.remove(o)
