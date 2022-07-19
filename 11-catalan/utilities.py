from __future__ import annotations

from math import e
from manim import *
from typing import *
from random import seed
from itertools import permutations, combinations, product
import sympy


class StarUtilities:
    STAR_COLOR = GREEN
    STAR_N = 6
    STAR_SCALE = 0.12
    STAR_OFFSET = 0.36

    @classmethod
    def get_star_name(cls, i):
        return f"star_{i}"

    @classmethod
    def is_star_name(cls, s):
        return "star" in s

    @classmethod
    def get_star_index(cls, s):
        return int(s[len("star_"):])

    @classmethod
    def get_highest_star(cls, graph):
        max_index = 0
        max_name = None
        for v in graph.vertices:
            if cls.is_star_name(v):
                if cls.get_star_index(v) > max_index:
                    max_index = cls.get_star_index(v)
                    max_name = v
        return max_name


    @classmethod
    def create_star_object(cls, number, no_labels=False) -> VMobject:
        # this MUST be an odd number, else the rotation won't work
        star = Star(cls.STAR_N, density=1.5, color=cls.STAR_COLOR, fill_opacity=1).scale(cls.STAR_SCALE)

        if no_labels:
            return VGroup(star)

        text = Tex(str(number), color=BLACK).scale(3 * cls.STAR_SCALE).move_to(star)
        return VGroup(star, text)

    @classmethod
    def get_star_position(cls, graph, v, direction):
        """Get the star position, relative to the given vertex in a graph."""
        return graph.vertices[v].get_center() + (DOWN * 1.9 + direction) * cls.STAR_OFFSET

    @classmethod
    def attach_star_to_vertex(cls, graph, v, number, direction, no_labels=False):
        """Create star from the vertex in the given direction (LEFT/RIGHT)."""

        vertex = graph.add_vertices(
            cls.get_star_name(number),
            positions={
                cls.get_star_name(number): cls.get_star_position(graph, v, direction)
            },
            vertex_type=lambda: cls.create_star_object(number, no_labels),
        )[0]

        graph.add_edges(
            ((v, cls.get_star_name(number))),
            edge_type=lambda *args, **kwargs: Line(*args, color=cls.STAR_COLOR, **kwargs),
        )


    @classmethod
    def add_stars_to_graph(cls, graph: BinaryTree, no_labels=False):
        """Add stars to a binary tree. It is assumed that '' is the root."""

        count = 0

        # add stars sorted from left to right (so by the x, y coordinate of parent)
        for v in sorted(graph.get_non_full_vertices(), key = lambda v: (graph.vertices[v].get_center()[0], graph.vertices[v].get_center()[1])):
            descendants = [x for (w, x) in graph.edges if v == w]

            # add both stars
            if len(descendants) == 0:
                cls.attach_star_to_vertex(graph, v, count + 1, LEFT, no_labels)
                cls.attach_star_to_vertex(graph, v, count + 2, RIGHT, no_labels)
                count += 2

            # add one star
            else:
                d = descendants[0]

                if d[-1] == "l":
                    cls.attach_star_to_vertex(graph, v, count + 1, LEFT, no_labels)
                else:
                    cls.attach_star_to_vertex(graph, v, count + 1, RIGHT, no_labels)

                count += 1

        return [cls.get_star_name(i + 1) for i in range(count)]


def ChangeStars(graph, permutation: int) -> Animation:
    """Return the animation of changing the permutation on the stars."""
    n = (len(graph.vertices) + 1) // 2
    p = list(permutations(range(1, n + 1)))[permutation]  # computers are fast

    animations = []

    for vertex in graph.vertices:
        if StarUtilities.is_star_name(vertex):
            star = graph.vertices[vertex]

            new_index = p[StarUtilities.get_star_index(vertex) - 1]

            if StarUtilities.get_star_index(vertex) != new_index:
                new_star = StarUtilities.create_star_object(new_index)
                new_star[1].move_to(star[0])

                animations += [
                    star[0].animate(rate_func=there_and_back).scale(0.75),
                    star[1].animate.become(new_star[1]),
                ]

    return AnimationGroup(*animations)

def CreateStars(graph) -> Animation:
    """Return an animation of creating all of the stars of a graph."""
    animations = []

    for (u, v) in graph.edges:
        if StarUtilities.is_star_name(v):
            animations.append(
                (
                    graph.vertices[v].get_center()[0],
                    AnimationGroup(
                        FadeIn(graph.edges[(u, v)], run_time=0.4),
                        FadeIn(graph.vertices[v], run_time=0.4),
                        Flash(
                            graph.vertices[v],
                            color=graph.edges[(u, v)].color,
                            run_time=0.4,
                            line_length=0.05,
                            flash_radius=0.18,
                        ),
                        lag_ratio=0.3,
                    ),
                )
            )

    return AnimationGroup(*[a for (_, a) in sorted(animations, key=lambda x: x[0])], lag_ratio=0.1)


def RemoveHighestStar(graph) -> Animation:
    """Return an animation of removing the star with the highest number (along with its vertex) from the graph.
    We're assuming that we're not removing the very last vertex."""

    max_name = StarUtilities.get_highest_star(graph)

    max_name_parent = graph.get_parent(max_name)
    max_parent_squared = graph.get_parent(max_name_parent)
    children = graph.get_children(max_name_parent)

    # if the star's parent contains a non'star child
    if not StarUtilities.is_star_name(children[0]) or not StarUtilities.is_star_name(children[1]):
        non_star_child = children[0] if not StarUtilities.is_star_name(children[0]) else children[1]

        max_name_parent_vertex = graph.vertices[max_name_parent]
        removed = graph.remove_vertices(max_name_parent)
        removed += graph.remove_vertices(max_name)

        non_star_child_descendants = graph.get_all_descendants(non_star_child)

        animations = []

        # if the parent also has a parent
        if max_parent_squared is not None:
            edge = graph.add_edges((max_parent_squared, non_star_child))[0]
            edge.set_opacity(0)

            animations += [edge.animate.set_opacity(1)]

        return [
            *[FadeOut(r, run_time=0.5) for r in removed],
            *[graph.vertices[v].animate.shift(max_name_parent_vertex.get_center() - graph.vertices[non_star_child].get_center()) for v in non_star_child_descendants],
        ] + animations

    else:
        other_child = children[0] if max_name != children[0] else children[1]

        removed = graph.remove_vertices(max_name_parent)
        removed += graph.remove_vertices(max_name)

        # if max's parent is the only remaining regular vertex, don't add any edges; just remove max and its parent
        if max_parent_squared is None:
            return [*[FadeOut(r, run_time=0.5) for r in removed]]

        else:
            edge = graph.add_edges((max_parent_squared, other_child))[0]
            edge.set_color(StarUtilities.STAR_COLOR)
            edge.set_opacity(0)

            return [
                *[FadeOut(r, run_time=0.5) for r in removed],
                graph.vertices[other_child].animate.move_to(StarUtilities.get_star_position(graph, max_parent_squared, LEFT if max_parent_squared[-1] == "l" else RIGHT)),
                edge.animate.set_opacity(1),
            ]


class LinedPolygon(VMobject):

    @classmethod
    def generate_triangulated_polygons(cls, n: int) -> List[LinedPolygon]:
        """Generate all possible triangulated polygons on n vertices.
        Runs reasonably quickly for <= 10 vertices (~a minute)."""
        # computers are fast
        edges = list(combinations(range(n), r=2))

        # remove adjacent edges
        edges = [e for e in edges if abs(e[0] - e[1]) != 1 and abs(e[0] - e[1]) != n - 1]

        def _is_subset_intesecting(subset) -> bool:
            # check for intersections
            for i in range(len(subset)):
                for j in range(i + 1, len(subset)):
                    e1 = subset[i]
                    e2 = subset[j]

                    # if they share a vertex, they don't intersect
                    if len(set(e1 + e2)) != len(e1) + len(e2):
                        continue

                    p1, p2 = e1
                    p3, p4 = e2

                    if p1 < p3 < p2 and p3 < p2 < p4:
                        return True

            return False

        polygons = []

        for subset in combinations(edges, r = n - 3):
            if not _is_subset_intesecting(subset):
                polygons.append(LinedPolygon(n, subset))

        return polygons


    def __init__(self, n, edges):
        super().__init__()

        self.polygon = RegularPolygon(n, color=WHITE)

        if n == 4:
            self.polygon.rotate(2 * PI / 8)

        vertices = self.polygon.get_vertices()

        self.add(self.polygon)

        self.edges = {}

        for u, v in edges:
            self.edges[(u, v)] = Line(start=vertices[u], end=vertices[v])
            self.add(self.edges[(u, v)])


class DyckPath(VMobject):

    def __init__(self, delta: List[int], labels=False, spacing=0.5):
        super().__init__()

        vertices = list(range(len(delta) + 1))
        edges = [(i, i + 1) for i in vertices[:-1]]

        self.deltas = delta

        layout = {}

        pos = ORIGIN
        min_x, max_x = 0, 0
        min_y, max_y = 0, 0
        for i, (v, d) in enumerate(zip(vertices, [0] + list(delta))):
            if d == 1:
                pos = np.array(pos) + (RIGHT + UP) * spacing
            elif d == -1:
                pos = np.array(pos) +(RIGHT + DOWN) * spacing

            min_x = min(min_x, pos[0])
            max_x = max(max_x, pos[0])
            min_y = min(min_y, pos[1])
            max_y = max(max_y, pos[1])

            layout[v] = np.array(pos)

        for v in layout:
            layout[v][0] -= (max_x + min_x) / 2
            layout[v][1] -= (max_y + min_y) / 2

        self.path = Graph(vertices, edges, layout=layout)
        self.add(self.path)

        self.bottom_line = DyckPath.create_dyck_line(
            self.path.vertices[0].get_center(),
            self.path.vertices[len(self.path.vertices) - 1].get_center()
        )

        for v in self.path.vertices:
            self.path.vertices[v].set_z_index(1)

        self.add(self.bottom_line)

        if labels:
            for v, d in zip(vertices, delta):
                color = RED if d == -1 else GREEN
                label = Tex(str(d), color=color).scale(0.5).next_to(self.path.vertices[v], UP, buff=0.15)
                self.add(label)


    @classmethod
    def create_dyck_line(cls, start, end) -> VMobject:
        """Create a dyck x axis line between points a and b."""
        end[1] = start[1]  # make sure the line is straight

        return DashedLine(start, end, dashed_ratio=0.25, color=GRAY)


    @classmethod
    def generate_dyck_paths(cls, n: int) -> List[DyckPath]:
        paths = []

        for path in product([1, -1], repeat=n * 2):
            i = 0
            for j in path:
                i += j
                if i < 0:
                    break
            else:
                if i == 0:
                    paths.append(cls(path))

        return paths

    def get_last_hill_animations(self):
        dot = Dot().scale(0.01)

        if len(self.deltas) == 0:
            return self.path.vertices[0].animate.set_color(BLUE), lambda: None

        delta_sum = 0
        max_i = 0

        for i, d in enumerate(self.deltas[:-1]):
            if delta_sum == 0:
                max_i = i

            delta_sum += d

        def blue_by_closeness(obj):
            p1 = obj.get_center()
            p2 = dot.get_center()

            sigmoid = lambda x: clamp((2/(1 + e ** x)) ** 4, 0, 1)

            d = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])

            new_color = interpolate_color(WHITE, BLUE, sigmoid(d))

            if color_distance(obj.color, BLUE) > color_distance(new_color, BLUE):
                obj.color = new_color

        points = []
        for v in sorted(self.path.vertices)[max_i:]:
            points.append(self.path.vertices[v].get_center())
            self.path.vertices[v].add_updater(blue_by_closeness)

        path = Path(points)

        tpath = TracedPath(dot.get_center, stroke_width=6, stroke_color=BLUE)
        self.add(tpath)

        a1 = AnimationGroup(
            self.path.vertices[max_i].animate.set_color(BLUE),
            MoveAlongPath(dot, path, run_time=2),
            lag_ratio=0.25
        )

        crossed_path = DyckPath.create_dyck_line(
            self.path.vertices[max_i + 1].get_center(),
            self.path.vertices[len(self.deltas) - 1].get_center(),
        )

        l1 = Line(self.path.vertices[max_i].get_center(), self.path.vertices[max_i + 1].get_center(), stroke_width=6, stroke_color=BLUE)
        l2 = Line(self.path.vertices[len(self.deltas) - 1].get_center(), self.path.vertices[len(self.deltas)].get_center(), stroke_width=6, stroke_color=BLUE)

        a3 = Write(l1, run_time=0)
        a4 = Write(l2, run_time=0)

        a2 = AnimationGroup(
            Write(crossed_path, run_time=1),
            FadeOut(tpath),
            *[self.path.vertices[i].animate.set_color(WHITE)
              for i in range(max_i + 1, len(self.deltas))]
        )

        def to_do_after():
            self.add(l1)
            self.add(l2)
            self.add(crossed_path)
            self.remove(tpath)

        return Succession(a1, a3, a4, a2), to_do_after

    def get_left_right_subpaths(self, scale) -> Tuple[DyckPath]:
        delta_sum = 0
        max_i = 0

        for i, d in enumerate(self.deltas[:-1]):
            if delta_sum == 0:
                max_i = i

            delta_sum += d

        left = DyckPath(self.deltas[:max_i]).scale(scale)
        right = DyckPath(self.deltas[max_i + 1:-1]).scale(scale)

        align_object_by_coords(
            left,
            left.path.vertices[0].get_center(),
            self.path.vertices[0].get_center()
        )

        align_object_by_coords(
            right,
            right.path.vertices[0].get_center(),
            self.path.vertices[max_i + 1].get_center()
        )

        return (left, right)

    def __str__(self):
        return f"DyckPath({self.deltas})"

    __repr__ = __str__


class BinaryTree(Graph):

    def get_parent(self, v) -> str:
        """Return the parent of a vertex (given that it's not the root), else return None."""
        for x, y in self.edges:
            if v == y:
                return x

    def get_children(self, v) -> List[str]:
        """Return the parent of a vertex (given that it's not the leaf), else return []."""
        children = []
        for x, y in self.edges:
            if v == x:
                children.append(y)
        return children

    def get_all_descendants(self, v) -> List[str]:
        """Return all children of a vertex, including the vertex itself."""
        stack = [v]
        children = []

        while len(stack) != 0:
            u = stack.pop(0)
            children.append(u)

            for v in self.vertices:
                if v in children:
                    continue

                if (u, v) in self.edges:
                    stack.append(v)

        return children


    def get_non_full_vertices(self) -> List[str]:
        """Return all vertices of a graph (having '' as root) that don't have 2 children."""
        vertices = []

        for v in self.vertices:

            count = 0
            for w, _ in self.edges:
                if v == w:
                    count += 1

            if count != 2:
                vertices += [v]

        return vertices

    @classmethod
    def _generate_parentheses(cls, n: int) -> Optional[List]:
        """Generate all nested parentheses representing binary trees on n vertices.
        n = 1: [None, None]
        n = 2: [[None, None], None] and [None, [None, None]]
        n = 3: ..."""

        if n == 0:
            return None

        else:
            previous_trees = []
            trees = []

            for i in range(n):
                previous_trees.append(cls._generate_parentheses(i))

            for i in range(n):
                for l1 in (previous_trees[i] or [None]):
                    for l2 in (previous_trees[n - i - 1] or [None]):
                        trees.append([l1, l2])

            return trees

    @classmethod
    def _binary_tree_from_parentheses(cls, graph) -> VMobject:
        """Generate a binary tree from nested parentheses.
        Sample input: [None, [None, None]] (generating a 2-vertex binary tree)."""

        vertices = [""]
        edges = []

        def _populate(g, v):
            """Populate vertices and edges.
            Vertices to be deleted contain the 'L' symbol (leaf), for aligning."""
            if g == [None, None]:
                if cls == FullBinaryTree:
                    vertices.append(v + "lL")
                    edges.append((v, vertices[-1]))

                    vertices.append(v + "rL")
                    edges.append((v, vertices[-1]))

                return

            for i in range(2):
                s = "l" if i == 0 else "r"

                if g[i] != None:
                    vertices.append(v + s)
                    edges.append((v, vertices[-1]))

                    _populate(g[i], vertices[-1])
                else:
                    vertices.append(v + s + "L")
                    edges.append((v, vertices[-1]))

        _populate(graph, "")

        g = cls(
            vertices,
            edges,
            layout="tree",
            root_vertex="",
            layout_config={"vertex_spacing": (1.15, 1)},
            vertex_type=lambda: Dot().scale(1.5),
        )

        if cls != FullBinaryTree:
            for v in list(g.vertices):
                if "L" in v:
                    g.remove_vertices(v)

        return g

    @classmethod
    def generate_binary_trees(cls, n: int) -> List[BinaryTree]:
        """Generate all binary trees on n vertices."""
        return [cls._binary_tree_from_parentheses(p)
                for p in cls._generate_parentheses(n)]


class FullBinaryTree(BinaryTree):
    pass


def SwapChildren(graph, v, move_height=0.1, speed_ratio=0.75, **kwargs) -> List[Animation]:
    """Generates animations for swapping the children of a vertex."""

    def generate_swap_animations(parent, child, direction):
        """Generate the swap animations for a parent, given its child."""
        c_pos = graph.vertices[child].get_center()
        p_pos = graph.vertices[parent].get_center()

        mirror_c_pos = np.array([c_pos[0] + 2 * (p_pos[0] - c_pos[0]), c_pos[1], c_pos[2]])

        points = [
            c_pos,
            c_pos * speed_ratio + mirror_c_pos * (1 - speed_ratio),
            c_pos * (1 - speed_ratio) + mirror_c_pos * speed_ratio,
            mirror_c_pos,
        ]

        path = CubicBezier(
            points[0],
            points[1] + direction * move_height,
            points[2] + direction * move_height,
            points[3],
        )

        return [
            MoveAlongPath(
                graph.vertices[v],
                path.copy().shift(graph.vertices[v].get_center() - c_pos),
                **kwargs,
            )
            for v in graph.get_all_descendants(child)
        ]

    # find the children
    a, b = [x for (w, x) in graph.edges if v == w]

    # TODO: using AnimationGroup here stops updaters, I'm not sure how to prevent it
    return [
        *generate_swap_animations(v, a, DOWN),
        *generate_swap_animations(v, b, DOWN),
    ]


class Path(VMobject):
    def __init__(self, points, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.set_points_as_corners(points)

    def get_important_points(self):
        """Returns the important points of the curve."""
        # shot explanation: Manim uses quadratic Bézier curves to create paths
        # > each curve is determined by 4 points - 2 anchor and 2 control
        # > VMobject's builtin self.points returns *all* points
        # > we, however, only care about the anchors
        # > see https://en.wikipedia.org/wiki/Bézier_curve for more details
        return list(self.get_start_anchors()) + [self.get_end_anchors()[-1]]


def clamp(x, min_x, max_x):
    return max(min(x, max_x), min_x)


def color_distance(a, b):
    """Return the distance of two colors in terms of the sum of absolute values of
    differences of their RGB."""
    r1, g1, b1 = color_to_int_rgb(a)
    r2, g2, b2 = color_to_int_rgb(b)

    # lmao
    r1 = int(r1)
    r2 = int(r2)
    g1 = int(g1)
    g2 = int(g2)
    b1 = int(b1)
    b2 = int(b2)

    return abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)


def align_object_by_coords(obj, current, desired, animation=False):
    """Align an object such that it's current coordinate coordinate will be the desired."""
    if animation:
        return obj.animate.shift(desired - current)
    else:
        obj.shift(desired - current)


class Path(VMobject):
    def __init__(self, points, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.set_points_as_corners(points)

    def get_important_points(self):
        """Returns the important points of the curve."""
        return list(self.get_start_anchors()) + [self.get_end_anchors()[-1]]

    def __getitem__(self, i):
        return self.get_important_points()[i]


def create_polygon_triangles(p):
    vertices = p.polygon.get_vertices()
    n = len(vertices)

    all_edges = list(p.edges) + [(i, (i + 1) % n) for i in range(n)]

    triangles_brr = set()

    for e1 in all_edges:
        for e2 in all_edges:
            for e3 in all_edges:
                if e1 == e2 or e2 == e3 or e1 == e3:
                    continue

                s = tuple(set(e1).union(set(e2).union(set(e3))))

                if len(s) == 3 and s not in triangles_brr:
                    triangles_brr.add(s)

    colors = [RED, "#ffd166", "#06d6a0", BLUE]
    all_colors = color_gradient(colors, len(triangles_brr))

    triangles = VGroup(*[Polygon(vertices[a], vertices[b], vertices[c], fill_opacity=1, color=all_colors[i])
                 for i, (a, b, c) in enumerate(triangles_brr)])

    for t in triangles:
        t.round_corners(0.01)

    return triangles
